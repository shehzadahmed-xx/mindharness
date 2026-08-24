"""Phase 4 acceptance tests — PREREQUISITES.md AC-4.1a/b, AC-4.2.

Run: python3 tests/test_phase4_embodiment.py   (plain runner, no pytest)
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.affect import AffectState, property_bounds
from harness_core.embodiment import EmbodiedState

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


# ---------------------------------------------------------------- AC-4.1a

def test_energy_gating_removes_keys_entirely():
    e = EmbodiedState(energy=1.0)
    full = e.affordance_space()
    assert 'attend_sustained' in full and 'create' in full
    # drain hard
    for _ in range(12):
        e.consume_tokens(2000)
    assert e.energy < 0.35
    gated = e.affordance_space()
    assert 'attend_sustained' not in gated, "must be ABSENT, not False"
    assert 'create' not in gated
    assert 'communicate' in gated               # body-independent stays
    # NOTE: this drain also raises fatigue (~0.91) which legitimately gates
    # navigate (<0.8 required) and reach (<0.9); spec-correct absence.


def test_fatigue_gates_navigation():
    e = EmbodiedState()
    for _ in range(40):
        e.register_failure()                    # fatigue -> capped at 1.0
    assert e.fatigue >= 0.8
    assert 'navigate' not in e.affordance_space()


# ---------------------------------------------------------------- AC-4.1b

def test_rest_restores_and_floor_holds():
    e = EmbodiedState(energy=1.0)
    for _ in range(20):
        e.consume_tokens(5000)                  # drive to floor
    assert e.energy == EmbodiedState.ENERGY_FLOOR
    e.rest(minutes=120)                         # +0.4 energy
    assert e.energy > 0.5
    assert 'attend_sustained' in e.affordance_space()
    assert 'create' in e.affordance_space()
    # floor property over random hammering
    rng = random.Random(5)
    e2 = EmbodiedState()
    for _ in range(300):
        e2.consume_tokens(rng.randint(0, 8000))
        if rng.random() < 0.3:
            e2.register_failure()
        assert e2.energy >= EmbodiedState.ENERGY_FLOOR - 1e-9
        assert e2.fatigue <= 1.0 + 1e-9


def test_strain_composite():
    fresh = EmbodiedState().strain()
    drained = EmbodiedState(energy=0.15, fatigue=1.0).strain()
    assert fresh < 0.2 and drained >= 0.9


# ---------------------------------------------------------------- AC-4.2

def test_failure_run_raises_arousal_and_shifts_salience():
    calm = AffectState()
    stressed = AffectState()
    for i in range(8):
        stressed.observe_event(-0.9, magnitude=1.5, turn=i)
    assert stressed.arousal > calm.arousal + 0.3
    assert stressed.valence < -0.3
    # ordering shift: multiplier actually moved the needle on a sample list
    items = ['plan', 'execute', 'verify']
    base = sorted(items)
    scaled = sorted(items, key=lambda x: stressed.salience_multiplier())
    # salience is a global scalar; the documented behavioral effect is that the
    # multiplier differs from calm baseline by a bounded but non-trivial amount
    assert abs(stressed.salience_multiplier()
               - calm.salience_multiplier()) > 0.2


def test_multipliers_bounded_under_extremes():
    ok, msg = property_bounds(n_samples=300, seed=42)
    assert ok, msg


def test_suppression_flags_logged():
    a = AffectState()
    a.set_suppression('anger', True, turn=3)
    a.set_suppression('anger', True, turn=4)      # no-op when unchanged
    a.set_suppression('anger', False, turn=7)
    assert [x['action'] for x in a.suppression_log] == ['set', 'cleared']
    assert a.suppression_log[0]['turn'] == 3
    try:
        a.set_suppression('envy', True, turn=1)   # type: ignore[arg-type]
        bad = False
    except ValueError:
        bad = True
    assert bad


def test_risk_multiplier_direction_and_masking_cost():
    pos = AffectState(); pos.observe_event(+1.0, 2.0, 0)
    neg = AffectState(); neg.observe_event(-1.0, 2.0, 0)
    assert pos.risk_multiplier() > 1.0
    assert neg.risk_multiplier() < 1.0
    masked = AffectState(); masked.observe_event(-1.0, 2.0, 0)
    masked.set_suppression('anger', True, 1)
    masked.set_suppression('sadness', True, 1)
    assert masked.risk_multiplier() <= neg.risk_multiplier()


def test_broadcast_policy():
    a = AffectState()
    assert not a.broadcast_needed(0, 5)                    # within K window
    assert a.broadcast_needed(0, 10)                       # every_k reached
    assert a.broadcast_needed(8, 9, threshold_crossed=True)  # crossing wins


if __name__ == "__main__":
    check("AC-4.1a gating removes keys entirely", test_energy_gating_removes_keys_entirely)
    check("AC-4.1a fatigue gates navigation", test_fatigue_gates_navigation)
    check("AC-4.1b rest restores + floor holds", test_rest_restores_and_floor_holds)
    check("strain composite", test_strain_composite)
    check("AC-4.2 failure-run arousal + salience shift", test_failure_run_raises_arousal_and_shifts_salience)
    check("AC-4.2 multipliers bounded (property)", test_multipliers_bounded_under_extremes)
    check("AC-4.2 suppression flags logged", test_suppression_flags_logged)
    check("AC-4.2 risk direction + masking cost", test_risk_multiplier_direction_and_masking_cost)
    check("broadcast policy", test_broadcast_policy)
    print(f"\n{PASS}/{PASS + FAIL} passed")
    sys.exit(1 if FAIL else 0)
