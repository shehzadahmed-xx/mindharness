"""World acceptance tests — a world that acts back (gap 2).

Run: python3 tests/test_world.py   (plain runner, no pytest)
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

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


def test_harvest_collects_and_empties_cell():
    w = World(seed=1)
    w.cells[(w.agent_xy[0], w.agent_xy[1])] = 2
    before = w.energy
    c = w.act('harvest')
    assert c['harvested'] == 2, c
    assert w.energy == before + 2, (before, w.energy)
    assert w.cells[(w.agent_xy[0], w.agent_xy[1])] == 0


def test_move_costs_and_stays_in_bounds():
    w = World(width=4, height=4, seed=2)
    w.agent_xy = (0, 0)
    before = w.energy
    w.act('left')  # into the wall: position holds, no charge
    assert w.agent_xy == (0, 0) and w.energy == before
    w.act('right')
    assert w.agent_xy == (1, 0) and w.energy == before - w.move_cost


def test_broke_loop_cannot_act_until_regrow():
    w = World(seed=3)
    w.energy = 0.0
    w.cells[(w.agent_xy[0], w.agent_xy[1])] = 0
    w.act('think')
    assert w.energy == 0.0  # no credit
    w.act('up')
    assert w.energy == 0.0
    got = w.act('harvest')
    assert got['harvested'] == 0  # nothing under it, still broke


def test_unknown_action_raises():
    w = World(seed=4)
    try:
        w.act('fly')
    except ValueError:
        return
    raise AssertionError("unknown action did not raise")


def test_events_log_every_step():
    w = World(seed=5)
    w.act('harvest')
    w.act('rest')
    assert len(w.events) == 2, w.events
    assert w.events[0]['turn'] == 1 and w.events[1]['turn'] == 2
    assert set(w.events[0]) >= {'action', 'energy_before', 'energy_after',
                                'harvested'}


def test_save_load_round_trip():
    w = World(seed=6)
    w.act('harvest')
    w.act('right')
    p = os.path.join(tempfile.mkdtemp(prefix="world-test-"), "w.json")
    w.save(p)
    w2 = World.load(p)
    assert w2.to_dict() == w.to_dict()


def test_regrow_adds_tokens_over_time():
    w = World(width=8, height=8, regen=0.5, seed=7)
    w.cells.clear()
    for _ in range(20):
        w.act('rest')
    assert sum(w.cells.values()) > 0, "regrow never added a token"


def test_closed_loop_next_input_contains_last_action():
    from harness_core.agent_harness import AgentHarness
    w = World(seed=9)
    h = AgentHarness(respond_fn=lambda m, c: "ok", world=w)
    r1 = h.world_turn('harvest')
    r2 = h.world_turn('right')
    assert r2['sensed']['turn'] == r1['consequence']['turn']
    assert r2['sensed']['energy'] == r1['consequence']['energy_after']


def test_world_turn_without_world_raises():
    from harness_core.agent_harness import AgentHarness
    h = AgentHarness(respond_fn=lambda m, c: "ok")
    try:
        h.world_turn('harvest')
    except ValueError:
        return
    raise AssertionError("world_turn without world did not raise")


def test_staked_starvation_drops_ceiling_permanently():
    from harness_core.agent_harness import (AgentHarness, IrreversibleDamage,
                                            arm_world_stakes)
    from harness_core.world import World
    w = World(seed=11)
    h = AgentHarness(respond_fn=lambda m, c: "ok", world=w)
    arm_world_stakes(h, IrreversibleDamage())
    w.energy = 0.0
    w.cells[(w.agent_xy[0], w.agent_xy[1])] = 0
    out = h.world_turn('think')
    assert out['staked']['starving'] is True
    assert out['staked']['energy_ceiling'] < 1.0
    ceiling = out['staked']['energy_ceiling']
    out2 = h.world_turn('harvest')
    assert out2['staked']['energy_ceiling'] <= ceiling
    assert len(h._damage.events) >= 1


def test_staked_plenty_leaves_ceiling_intact():
    from harness_core.agent_harness import (AgentHarness, IrreversibleDamage,
                                            arm_world_stakes)
    from harness_core.world import World
    w = World(seed=12)
    h = AgentHarness(respond_fn=lambda m, c: "ok", world=w)
    arm_world_stakes(h, IrreversibleDamage())
    w.cells[(w.agent_xy[0], w.agent_xy[1])] = 3
    out = h.world_turn('harvest')
    assert out['staked']['starving'] is False
    assert out['staked']['energy_ceiling'] == 1.0
    assert h._damage.events == []


def test_arm_stakes_without_world_raises():
    from harness_core.agent_harness import (AgentHarness, IrreversibleDamage,
                                            arm_world_stakes)
    h = AgentHarness(respond_fn=lambda m, c: "ok")
    try:
        arm_world_stakes(h, IrreversibleDamage())
    except ValueError:
        return
    raise AssertionError("arm_world_stakes without world did not raise")


if __name__ == '__main__':
    for name, fn in sorted(
            [(k, v) for k, v in globals().items() if k.startswith('test_')]):
        check(name, fn)
    print(f"\nworld: {PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
