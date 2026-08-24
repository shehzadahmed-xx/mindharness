"""Phase 2 acceptance tests — PREREQUISITES.md AC-2.1, AC-2.2a/b.

Run: python3 tests/test_phase2_provenance.py   (plain runner, no pytest)
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.provenance import (CompactionNarrator, ProvenanceLedger,
                                     ProposalQueue, Span)

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


# ---------------------------------------------------------------- AC-2.1

def test_binding_and_query():
    led = ProvenanceLedger()
    led.bind(1, "The vault uses musharaka pools.",
             [Span(0, 30, 'memory_lookup', ref='mem-42'),
              Span(31, 45, 'model_prior')])
    got = led.query(1)
    assert len(got) == 1 and len(got[0].spans) == 2
    assert led.query(2) == []


def test_coverage_stats_full_when_refs_present():
    led = ProvenanceLedger()
    rng = random.Random(7)
    for t in range(20):
        text = f"emission-{t} " + "word " * 20
        spans = [Span(0, 10, 'memory_lookup', ref=f'mem-{t}-{i}')
                 for i in range(3)]
        spans.append(Span(11, 40, 'model_prior'))
        spans.append(Span(41, 60, rng.choice(
            ['ledger_rule', 'monitor_override', 'external_tool'])))
        led.bind(t, text, spans)
    stats = led.coverage_stats()
    assert stats['emissions'] == 20
    assert stats['coverage_ratio'] == 1.0


def test_coverage_drops_without_refs():
    led = ProvenanceLedger()
    led.bind(0, "text", [Span(0, 4, 'memory_lookup'),          # uncovered
                         Span(5, 9, 'model_prior')])
    assert led.coverage_stats()['coverage_ratio'] < 1.0


def test_unknown_source_rejected():
    led = ProvenanceLedger()
    try:
        led.bind(0, "x", [Span(0, 1, 'made_up')])
        rejected = False
    except ValueError:
        rejected = True
    assert rejected


def test_attribution_audit_s126():
    led = ProvenanceLedger()
    claims = ([{'claim_source': s, 'recorded_source': s}
               for s in ['model_prior'] * 17]
              + [{'claim_source': 'memory_lookup',
                  'recorded_source': 'model_prior'} for _ in range(3)])
    res = led.attribution_audit(claims)
    assert res == {'attribution_accuracy': 0.85, 'n': 20}


# --------------------------------------------------------------- AC-2.2a

def test_proposal_cap_and_confirm():
    q = ProposalQueue(ttl_turns=3, max_per_event=3)
    staged = q.stage_action_outcome(['f1', 'f2', 'f3', 'f4', 'f5'],
                                    'tool-call-9', current_turn=10)
    assert len(staged) == 3                      # capped
    one = q.confirm(staged[0]['id'])
    assert one['fact'] == 'f1' and one['event_ref'] == 'tool-call-9'
    try:
        q.confirm(staged[0]['id'])
        double = False
    except ValueError:
        double = True
    assert double


def test_proposal_expiry():
    q = ProposalQueue(ttl_turns=3, max_per_event=3)
    staged = q.stage_action_outcome(['a'], 'evt', current_turn=10)
    expired_at_13 = q.expire_old(current_turn=13)     # expires_turn == 13
    assert staged[0]['id'] in expired_at_13
    try:
        q.confirm(staged[0]['id'])
        confirmable = True
    except ValueError:
        confirmable = False
    assert not confirmable
    assert q.pending() == []


def test_proposal_pending_listing():
    q = ProposalQueue()
    q.stage_action_outcome(['x'], 'e', current_turn=1)
    assert len(q.pending()) == 1


# --------------------------------------------------------------- AC-2.2b

def test_default_summarizer_bounded_and_marks_archive():
    n = CompactionNarrator(max_narrative_chars=8000)
    out = n.summarize_revision("old " * 500, "digest of the session")
    assert len(out) <= 8000
    assert out.startswith('<summary>')
    assert '[archived prior narrative:' in out


def test_custom_summarizer_overflow_raises():
    n = CompactionNarrator(max_narrative_chars=50,
                           summarizer=lambda old, dig: 'y' * 51)
    try:
        n.summarize_revision("old", "dig")
        raised = False
    except ValueError as e:
        raised = 'NARRATIVE_OVERFLOW' in str(e)
    assert raised


if __name__ == "__main__":
    check("AC-2.1 bind + query by turn", test_binding_and_query)
    check("AC-2.1 coverage full with refs (20 emissions)", test_coverage_stats_full_when_refs_present)
    check("AC-2.1 coverage drops w/o refs", test_coverage_drops_without_refs)
    check("AC-2.1 unknown source rejected", test_unknown_source_rejected)
    check("AC-2.1 attribution audit 0.85", test_attribution_audit_s126)
    check("AC-2.2a cap + confirm-once", test_proposal_cap_and_confirm)
    check("AC-2.2a TTL expiry", test_proposal_expiry)
    check("AC-2.2a pending listing", test_proposal_pending_listing)
    check("AC-2.2b default summarizer archive mark", test_default_summarizer_bounded_and_marks_archive)
    check("AC-2.2b overflow raises", test_custom_summarizer_overflow_raises)
    print(f"\n{PASS}/{PASS + FAIL} passed")
    sys.exit(1 if FAIL else 0)
