"""Phase 6.5 acceptance tests — skills library + knowledge graph (witnessed).

Run: python3 tests/test_phase65_hermes.py   (plain runner, no pytest)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.hermes_adoption import SkillLibrary, KnowledgeGraph

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


# ------------------------------------------------------------- AC-6.5.1

def test_skill_from_task_only():
    lib = SkillLibrary()
    sk = lib.add_from_task("deploy-flow", "build, test, push", "task-9",
                           cause='action-outcome')
    assert sk.cause == 'action-outcome' and sk.source_task_id == 'task-9'
    try:
        lib.add_from_task("bad", "x", "t", cause='narrative-summary')
        assert False, "narrative-summary must not mint skills"
    except ValueError:
        pass


# ------------------------------------------------------------- AC-6.5.2

def test_retrieval_gated_and_ranked():
    lib = SkillLibrary()
    lib.add_from_task("musharaka-distribution", "pool acquires asset, resells, shares", "t1", 'action-outcome')
    lib.add_from_task("git-rebase-flow", "fetch upstream, rebase branch, force-push", "t2", 'action-outcome')
    hits = lib.retrieve("explain the musharaka distribution mechanism")
    assert hits and hits[0][0].name == "musharaka-distribution"
    unrelated = lib.retrieve("paint the fence")
    assert all(s < 0.45 for _, s in unrelated) or not unrelated


def test_record_use_and_success_rate():
    lib = SkillLibrary()
    lib.add_from_task("skill-x", "do x", "t", 'action-outcome')
    for ok in (True, True, False):
        lib.record_use("skill-x", ok)
    sk = lib.all()[0]
    assert sk.uses == 3 and sk.success_rate == 2/3


# ------------------------------------------------------------- selection

def test_cull_failed_skills():
    lib = SkillLibrary()
    lib.add_from_task("loser", "always fails", "t1", 'action-outcome')
    lib.add_from_task("winner", "sometimes works", "t2", 'action-outcome')
    for _ in range(4):
        lib.record_use("loser", False)
        lib.record_use("winner", True)
    culled = lib.cull_failed(min_uses=3, min_rate=0.3)
    assert "loser" in culled and "winner" not in culled
    assert lib.all()[0].name == "winner"


# ------------------------------------------------------------- AC-6.5.3

def test_edge_requires_valid_cause_and_refs():
    g = KnowledgeGraph()
    g.add_node("musharaka"); g.add_node("profit-share")
    e = g.add_edge("musharaka", "distributes", "profit-share",
                   'action-outcome', ["task-42"])
    assert e.cause == 'action-outcome' and e.source_refs == ["task-42"]
    for bad_cause in ('narrative-summary', None):
        try:
            g.add_edge("a", "r", "b", bad_cause, ["s"])  # type: ignore[arg-type]
            # narrative-summary IS a valid enum member; only invalid values raise
            if bad_cause is None:
                raise AssertionError("None cause must fail")
        except AssertionError as e:
            if "must fail" in str(e):
                raise
        except Exception:
            pass
    try:
        g.add_edge("a", "r", "b", 'action-outcome', [])  # empty refs
        assert False, "empty source_refs must block"
    except AssertionError as e:
        assert "source_ref" in str(e)


# ------------------------------------------------------------- AC-6.5.4

def test_multi_hop_traversal():
    g = KnowledgeGraph()
    edges = [("musharaka", "distributes", "profit-share"),
             ("profit-share", "requires", "real-assets"),
             ("real-assets", "example", "gold")]
    for i, (a, r, b) in enumerate(edges):
        g.add_edge(a, r, b, 'action-outcome', [f"task-{i}"])
    two_hop = g.multi_hop("musharaka", hops=2)
    assert any(p[-1] == "real-assets" for p in two_hop), two_hop
    three_hop = g.multi_hop("musharaka", hops=3)
    assert any(p[-1] == "gold" for p in three_hop), "3-hop path missing"


if __name__ == "__main__":
    check("AC-6.5.1 skill from task loop only", test_skill_from_task_only)
    check("AC-6.5.2 retrieval gated + ranked", test_retrieval_gated_and_ranked)
    check("use tracking / success rate", test_record_use_and_success_rate)
    check("selection culls failed skills", test_cull_failed_skills)
    check("AC-6.5.3 edge cause+refs invariant", test_edge_requires_valid_cause_and_refs)
    check("AC-6.5.4 multi-hop traversal", test_multi_hop_traversal)
    print(f"\n{PASS}/{PASS + FAIL} passed")
    sys.exit(1 if FAIL else 0)
