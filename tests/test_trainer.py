"""Trainer acceptance tests — scaffolding that teaches, not just props.

Run: python3 tests/test_trainer.py   (plain runner, no pytest)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.monitor import DetectSignals, MonitorGate
from harness_core.provenance import ProvenanceLedger, Span
from harness_core.trainer import (apply_calibration, calibrate_monitor,
                                  ledger_health, reliance_report)

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


def failing() -> DetectSignals:
    return DetectSignals(recent_error_rate=0.9, failure_streak=5,
                         context_conflict=0.1, embodied_strain=0.2,
                         world_accuracy=0.9)


def test_health_full_ledger_scores_high():
    led = ProvenanceLedger()
    led.bind(1, "claim one", [Span(start=0, end=5, source='model_prior', ref='r1')])
    led.query(1)
    led.attribution_audit([{'x': 1}])
    h = ledger_health(led)
    assert h['coverage_ratio'] == 1.0, h
    assert h['score'] >= 0.9, h
    assert h['healthy'] and h['directives'] == [], h


def test_health_unqueried_ledger_halved_with_directive():
    led = ProvenanceLedger()
    led.bind(1, "claim one", [Span(start=0, end=5, source='model_prior', ref='r1')])
    h = ledger_health(led)
    assert h['score'] == 0.5, h
    assert any('query the ledger' in d for d in h['directives']), h
    assert not h['healthy'], h


def test_health_empty_ledger_scores_zero():
    h = ledger_health(ProvenanceLedger())
    assert h['score'] == 0.0 and not h['healthy'], h


def test_calibrate_refuses_compliance_guard():
    g = MonitorGate(threshold_detect=0.6, compliance_guard=True)
    for _ in range(12):
        g.evaluate(1, failing(), 'proceed', dry_run=True)
    r = calibrate_monitor(g)
    assert r['changed'] is False and g.threshold == 0.6, r
    assert 'compliance guard' in r['reason'], r


def test_calibrate_desensitizes_on_excess_rate():
    g = MonitorGate(threshold_detect=0.6)
    for t in range(12):
        g.evaluate(t, failing(), 'proceed', dry_run=True)
    r = calibrate_monitor(g, target_rate=0.05)
    assert r['changed'] is True and r['new'] == 0.65, r
    assert apply_calibration(g, r) == 0.65 and g.threshold == 0.65


def test_calibrate_holds_on_few_episodes():
    g = MonitorGate(threshold_detect=0.6)
    g.evaluate(1, failing(), 'proceed', dry_run=True)
    r = calibrate_monitor(g, min_episodes=10)
    assert r['changed'] is False and 'insufficient' in r['reason'], r


def test_reliance_trend_falling_means_fading():
    r = reliance_report(2, 100, history=[0.10])
    assert r['override_rate'] == 0.02 and r['trend'] == 'falling', r
    assert 'fading' in r['reads_as'], r
    r2 = reliance_report(20, 100, history=[0.02])
    assert r2['trend'] == 'rising' and r2['history'] == [0.02, 0.2], r2


if __name__ == '__main__':
    for name, fn in sorted(
            [(k, v) for k, v in globals().items() if k.startswith('test_')]):
        check(name, fn)
    print(f"\ntrainer: {PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
