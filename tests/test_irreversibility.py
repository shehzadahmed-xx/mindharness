#!/usr/bin/env python3
"""Integration test: irreversible consequences change behavior permanently."""
import sys
sys.path.insert(0, ".")
sys.path.insert(0, "tools")

from harness_core.agent_harness import AgentHarness
from harness_core.agent_harness import IrreversibleDamage, wire_irreversibility

PASS = 0
FAIL = 0

def check(name, fn):
    global PASS, FAIL
    try:
        fn()
        PASS += 1
        print(f"  PASS {name}")
    except Exception as e:
        FAIL += 1
        print(f"  FAIL {name}: {e}")


def test_damage_accumulates_and_persists():
    counter = [0]
    def respond(m, c):
        counter[0] += 1
        return f"response-{counter[0]}"
    h = AgentHarness(respond_fn=respond)
    d = IrreversibleDamage()
    wire_irreversibility(h, d)

    # Simulate repeated failures on same task type
    for i in range(6):
        h.run_task("failing operation", task_id=f"fail-{i}",
                   fok=2, is_tool_action=True, success=False)

    assert len(d.events) > 0, "no irreversible events recorded"
    assert d.max_energy_ceiling < 1.0, "ceiling should be reduced"
    # Verify ceiling CANNOT be restored by rest
    h.body.rest(minutes=120)
    h.body.energy = min(h.body.energy, d.max_energy_ceiling)
    assert d.max_energy_ceiling < 1.0, "ceiling restoration is forbidden"


def test_skill_deletion_is_permanent():
    from harness_core.hermes_adoption import SkillLibrary
    lib = SkillLibrary()
    lib.add_from_task("failing-skill", "does something", "t1", cause='action-outcome')
    
    d = IrreversibleDamage()
    d.delete_skill_permanently("failing-skill", "repeated failure")
    
    assert "failing-skill" in d.deleted_skills
    
    # Attempt to recreate same skill — should carry deletion history
    lib.add_from_task("failing-skill-v2", "try again", "t2", cause='action-outcome')
    # The DAMAGE record persists regardless of new skill creation
    assert any(e.get('skill') == 'failing-skill' for e in d.events)


def test_memory_corruption_recorded():
    d = IrreversibleDamage()
    d.corrupt_memory_permanently("quarterly profit calculation", "fabricated claim")
    assert len(d.corrupted_memories) == 1
    assert d.events[-1]['type'] == 'memory_corruption'


def test_damage_survives_new_harness_construction():
    """Key test: damage must persist even when a NEW AgentHarness is built.
    This simulates cross-session persistence of irreversible consequences."""
    d = IrreversibleDamage()
    d.reduce_energy_ceiling(0.5, "test damage")
    original_ceiling = d.max_energy_ceiling
    
    # Build new harness (simulating new session)
    h = AgentHarness(respond_fn=lambda m, c: "ok")
    wire_irreversibility(h, d)
    
    # Ceiling must NOT reset to 1.0
    assert d.max_energy_ceiling == original_ceiling, \
        "damage was reset! irreversibility violated"


if __name__ == "__main__":
    check("damage accumulates and persists", test_damage_accumulates_and_persists)
    check("skill deletion is permanent", test_skill_deletion_is_permanent)
    check("memory corruption recorded", test_memory_corruption_recorded)
    check("damage survives new construction", test_damage_survives_new_harness_construction)
    print(f"\n{PASS}/{PASS + FAIL} passed")
    sys.exit(1 if FAIL else 0)
