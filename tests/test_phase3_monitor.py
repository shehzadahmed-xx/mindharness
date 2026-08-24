"""Phase 3 acceptance tests — PREREQUISITES.md AC-3.1, AC-3.2a/b, AC-3.3.

Run: python3 tests/test_phase3_monitor.py   (plain runner, no pytest)
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.monitor import (DetectSignals, MetacognitiveLog, MonitorGate,
                                  PostJOL, PreSolveFOK)

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


def healthy() -> DetectSignals:
    return DetectSignals(recent_error_rate=0.0, failure_streak=0,
                         context_conflict=0.0, embodied_strain=0.1,
                         world_accuracy=0.95)


def failing_streak() -> DetectSignals:
    return DetectSignals(recent_error_rate=0.8, failure_streak=4,
                         context_conflict=0.2, embodied_strain=0.7,
                         world_accuracy=0.6)


def test_healthy_rarely_diagnoses():
    g = MonitorGate()
    rng = random.Random(11)
    fired = 0
    for t in range(100):
        s = DetectSignals(recent_error_rate=rng.uniform(0, 0.15),
                          failure_streak=0,
                          context_conflict=rng.uniform(0, 0.2),
                          embodied_strain=rng.uniform(0, 0.25),
                          world_accuracy=rng.uniform(0.9, 1.0))
        _, rec = g.evaluate(t, s, 'proceed')
        fired += rec['fired']
    rate = fired / 100
    assert rate < 0.05, f"healthy diagnose-rate {rate} >= 5%"


def test_failure_streak_always_diagnoses():
    g = MonitorGate()
    fired = 0
    for t in range(20):
        _, rec = g.evaluate(t, failing_streak(), 'trust')
        fired += rec['fired']
    assert fired / 20 > 0.8


def test_compliance_guard_gamma_exactly_zero():
    g = MonitorGate(compliance_guard=True)
    for t in range(30):
        # alternate healthy/failing so many episodes FIRE (reports exist)
        s = failing_streak() if t % 2 == 0 else healthy()
        current = 'trust' if t % 2 == 0 else 'proceed'
        final, rec = g.evaluate(t, s, current)
        # report exists but action NEVER changes
        if rec['fired']:
            assert rec['diagnosis'] is not None
        assert rec['changed'] is False
        assert final == current
    d = g.diagnosed_episodes()
    assert len(d) >= 10          # reports were produced...
    assert g.override_rate() == 0.0   # ...and gamma is exactly zero


def test_wired_mode_gamma_positive_on_failures():
    g = MonitorGate(compliance_guard=False)   # wired
    for t in range(12):
        g.evaluate(t, failing_streak(), 'proceed')
    gamma = g.override_rate()
    assert gamma > 0.0, f"wired mode must change actions; gamma={gamma}"
    changed = [e for e in g.episodes if e['changed']]
    assert all(e['final'] == 'retry' for e in changed)


def test_wired_mode_trust_when_healthy():
    g = MonitorGate()
    for t in range(20):
        final, rec = g.evaluate(t, healthy(), 'proceed')
    assert all(not e['fired'] or e['final'] == 'proceed' for e in g.episodes)


def test_custom_diagnose_fn_respected():
    def custom(s: DetectSignals) -> dict:
        return {'risk_area': 'custom', 'confidence_in_plan': 0.5,
                'recommended_action': 'abstain'}
    g = MonitorGate(diagnose_fn=custom, threshold_detect=0.3)
    s = DetectSignals(recent_error_rate=0.4)   # score: .14 <.3? compute:
    # w_err=.35*.4=.14 -> below default threshold; raise signal
    s = DetectSignals(recent_error_rate=1.0, failure_streak=3)
    final, rec = g.evaluate(1, s, 'proceed')
    assert rec['diagnosis']['risk_area'] == 'custom'
    assert final == 'abstain' and rec['changed']


def test_fok_jol_schema_and_completeness():
    log = MetacognitiveLog()
    for i in range(10):
        log.add_fok(PreSolveFOK(task_id=f"t{i}", fok=(i % 4) + 1))
        log.add_jol(PostJOL(task_id=f"t{i}", jol=((i + 1) % 4) + 1,
                            correct=(i % 2 == 0)))
    pairs = log.paired()
    assert len(pairs) == 10
    assert log.completeness() == 1.0
    # schema bounds enforced
    try:
        PreSolveFOK(task_id='x', fok=5)
        bad = False
    except ValueError:
        bad = True
    assert bad


def test_fok_jol_incompleteness_detected():
    log = MetacognitiveLog()
    log.add_fok(PreSolveFOK(task_id='a', fok=2))
    log.add_jol(PostJOL(task_id='b', jol=3))     # no FOK for b
    assert log.completeness() == 0.5


if __name__ == "__main__":
    check("AC-3.1 healthy <5% diagnose-rate", test_healthy_rarely_diagnoses)
    check("AC-3.1 failure-streak >80% fires", test_failure_streak_always_diagnoses)
    check("AC-3.2a compliance guard gamma==0", test_compliance_guard_gamma_exactly_zero)
    check("AC-3.2b wired gamma>0 on failures", test_wired_mode_gamma_positive_on_failures)
    check("wired trust-preserving when healthy", test_wired_mode_trust_when_healthy)
    check("custom diagnose_fn honoured", test_custom_diagnose_fn_respected)
    check("AC-3.3 FOK/JOL schema + completeness", test_fok_jol_schema_and_completeness)
    check("AC-3.3 incompleteness detected", test_fok_jol_incompleteness_detected)
    print(f"\n{PASS}/{PASS + FAIL} passed")
    sys.exit(1 if FAIL else 0)
