"""Integration tests — the full loop, no mocks of our own modules.

Run: python3 tests/test_integration.py   (plain runner, no pytest, no network)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.agent_harness import AgentHarness
from harness_core.backend import BackendClient
from harness_core.monitor import DetectSignals

PASS = 0
FAIL = 0


def check(name: str, fn) -> None:
    global PASS, FAIL
    try:
        fn()
        PASS += 1
        print(f"  PASS {name}")
    except Exception as e:  # noqa: BLE001
        FAIL += 1
        print(f"  FAIL {name}: {e}")


def stub_responder(messages: list[dict], ctx: dict) -> str:
    """Deterministic stand-in; asserts ctx plumbing + anchor presence."""
    assert isinstance(ctx.get('affordances'), list)
    assert 0.5 <= ctx['salience'] <= 2.0
    assert len(messages[0]['content']) > 0          # system prompt present
    return f"ok[{len(ctx['affordances'])}]"


def test_healthy_session_flows():
    h = AgentHarness(respond_fn=stub_responder)
    results = []
    for i in range(6):
        r = h.run_task(f"task {i}", task_id=f"t{i}", fok=3,
                       is_tool_action=True, success=True)
        results.append(r)
        assert r.action == 'proceed'
        assert not r.gated_action_changed
    rep = h.session_report()
    assert rep['turns'] == 6
    assert rep['metacog_completeness'] == 1.0      # FOK+JOL on every attempt
    assert rep['coverage']['coverage_ratio'] == 1.0
    assert rep['sm_revisions'] == 1                # no updates without events
    assert rep['diagnoses'] == 0                   # healthy: gate silent


def test_failure_run_triggers_gate_and_stages_proposals():
    h = AgentHarness(respond_fn=stub_responder)
    staged_total = 0
    overrides = 0
    for i in range(8):
        r = h.run_task(f"failing op {i}", is_tool_action=True,
                       success=False)
        staged_total += r.proposals_staged
        if r.gated_action_changed:
            overrides += 1
            assert r.action in ('retry', 'revise', 'abstain')
    rep = h.session_report()
    assert staged_total >= 3                       # proposals staged per failure
    assert rep['diagnoses'] > 0                    # monitor fired
    assert rep['arousal'] > 0.2 and rep['valence'] < -0.1   # affect moved
    assert rep['energy'] < 1.0                     # tokens + failures cost
    # gamma>0 possible only when diagnoses happened AND changed actions
    assert (rep['overrides'] > 0) == (rep['override_rate'] > 0)


def test_abstain_short_circuits_generation():
    calls = {'n': 0}

    def counting_responder(messages, ctx):
        calls['n'] += 1
        return "should not be reached"

    def always_abstain(signals) -> dict:
        return {'risk_area': 'test', 'confidence_in_plan': 0.1,
                'recommended_action': 'abstain'}

    h = AgentHarness(respond_fn=counting_responder)
    h.gate.threshold = -1.0                        # force fire every turn
    h.gate.diagnose_fn = always_abstain            # policy says abstain
    for i in range(3):
        r = h.run_task("anything", success=False)
        assert r.action == 'abstain'
        assert r.response.startswith('[abstained')
    assert calls['n'] == 0                         # generation never invoked
    rep = h.session_report()
    assert rep['override_rate'] > 0                # abstain IS an override


def test_compliance_guard_gamma_zero_in_full_loop():
    h = AgentHarness(respond_fn=stub_responder, compliance_guard=True)
    for i in range(10):
        s = DetectSignals(recent_error_rate=1.0, failure_streak=5,
                          context_conflict=0.5, embodied_strain=0.9,
                          world_accuracy=0.4)
        _, rec = h.gate.evaluate(i, s, 'proceed')  # direct gate use
    assert len(h.gate.diagnosed_episodes()) >= 10
    assert h.gate.override_rate() == 0.0           # reports without function


def test_witnessed_consolidation_end_to_end():
    h = AgentHarness(respond_fn=stub_responder)
    mid = h.remember_episode("musharaka pool distribution executed", 'finance')
    h.remember_episode("musharaka pool distribution executed again", 'audit')
    # give both query types so gate passes
    items = h.memory
    for it in items.values():
        it.query_hits.update({'finance', 'audit'})
    rep = h.consolidate()
    assert rep['rem_ran'] is True
    promoted_ids = {p['id'] for p in rep['promoted']}
    assert promoted_ids
    for p in rep['promoted']:
        assert p['cause'] == 'action-outcome'      # witness tag present


def test_compaction_cycle_keeps_anchor_intact():
    persona = "Anchor bytes must survive."
    h = AgentHarness(respond_fn=stub_responder, persona=persona)
    h.run_task("warmup")
    h.compaction_cycle("did some work")
    assert h.sm.verbatim_reinject() == persona     # byte-exact post-compaction
    view = h.sm.get()
    assert view is not None and view['lastCause'] == 'narrative-summary'


def test_backend_client_import_boundary():
    """BackendClient exists but harness never imports network into the loop."""
    c = BackendClient(api_key='dummy', model='qwen/qwen3-32b')
    assert c.structured_mode() == 'object'


if __name__ == "__main__":
    check("healthy session end-to-end", test_healthy_session_flows)
    check("failure run gates + stages proposals", test_failure_run_triggers_gate_and_stages_proposals)
    check("abstain short-circuits generation", test_abstain_short_circuits_generation)
    check("compliance guard gamma zero in loop", test_compliance_guard_gamma_zero_in_full_loop)
    check("witnessed consolidation e2e", test_witnessed_consolidation_end_to_end)
    check("compaction preserves anchor", test_compaction_cycle_keeps_anchor_intact)
    check("backend boundary import", test_backend_client_import_boundary)
    print(f"\n{PASS}/{PASS + FAIL} passed")
    sys.exit(1 if FAIL else 0)
