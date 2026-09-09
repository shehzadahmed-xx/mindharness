"""Succession acceptance tests — lineage with inheritance, not backup.

Run: python3 tests/test_successor.py   (plain runner, no pytest)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.agent_harness import AgentHarness, IrreversibleDamage
from harness_core.successor import (mutate_threshold, record_birth,
                                    snapshot_parent, spawn_successor)
from harness_core.world import World

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


def make_parent(seed: int = 21):
    w = World(seed=seed)
    h = AgentHarness(respond_fn=lambda m, c: "ok", world=w)
    h.remember_episode("parent lesson one", query_type="lesson")
    h.remember_episode("parent lesson two", query_type="lesson")
    return h, w


def test_snapshot_reads_without_mutating():
    h, _ = make_parent()
    before = (h.turn, len(h.memory), h.gate.threshold)
    snap = snapshot_parent(h)
    assert (h.turn, len(h.memory), h.gate.threshold) == before
    assert len(snap['memories']) == 2
    assert snap['world_params']['width'] == 8


def test_mutate_threshold_bounded_and_deterministic():
    assert mutate_threshold(0.6, 4) == 0.65   # even revision drifts up
    assert mutate_threshold(0.6, 5) == 0.55   # odd drifts down
    assert mutate_threshold(0.9, 4) == 0.9    # clamped at hi
    assert mutate_threshold(0.3, 5) == 0.3    # clamped at lo
    assert mutate_threshold(0.6, 4) == mutate_threshold(0.6, 4)


def test_child_inherits_constraints_not_trust():
    h, _ = make_parent()
    h.gate.threshold = 0.7
    snap = snapshot_parent(h)
    child, damage = spawn_successor(snap, lambda m, c: "ok")
    assert len(child.memory) == 2
    assert all(m.content.startswith("parent lesson") for m in child.memory.values())
    assert child.gate.threshold != 0.7  # varied, never cloned
    assert 0.3 <= child.gate.threshold <= 0.9
    assert damage.max_energy_ceiling == 1.0  # scars inherit (none yet)
    assert child.ledger.coverage_stats()['emissions'] == 0  # unwitnessed at birth
    assert child.world is not None and child.world is not h.world


def test_scars_inherit_nothing_forgiven():
    h, _ = make_parent()
    dmg = IrreversibleDamage()
    dmg.reduce_energy_ceiling(0.2, "test loss")
    h._damage = dmg
    child, damage = spawn_successor(snapshot_parent(h), lambda m, c: "ok")
    assert abs(damage.max_energy_ceiling - 0.8) < 1e-9
    assert len(damage.events) == 1  # history inherits too


def test_birth_is_witnessed_in_parent_ledger():
    h, _ = make_parent()
    n_before = h.ledger.coverage_stats()['emissions']
    record_birth(h)
    assert h.ledger.coverage_stats()['emissions'] == n_before + 1
    found = [e for e in h.ledger.all_emissions()
             if e.meta.get('succession')]
    assert len(found) == 1


if __name__ == '__main__':
    for name, fn in sorted(
            [(k, v) for k, v in globals().items() if k.startswith('test_')]):
        check(name, fn)
    print(f"\nsuccessor: {PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
