"""Counterfactual replay — Light→REM→Counterfactual→Deep pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.consolidation import Consolidator, MemoryItem, record_query_hit
from harness_core.counterfactual import CounterfactualReplay

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


def store_with(*contents: str) -> dict[str, MemoryItem]:
    items: dict[str, MemoryItem] = {}
    for i, c in enumerate(contents):
        it = MemoryItem(content=c, created_turn=i)
        items[it.id] = it
    return items


def ids(items: dict[str, MemoryItem]) -> list[str]:
    return list(items.keys())


def test_counterfactual_generates_variants():
    items = store_with("proceed without witness check")
    for mid in ids(items):
        for qt in ("a", "b"):
            record_query_hit(items, mid, qt)
    cr = CounterfactualReplay()
    c = Consolidator(items)
    rep = c.run(current_turn=5, cause_by_id={m: "action-outcome" for m in items},
                counterfactual_replay=cr)
    assert rep.counterfactuals_generated > 0, "should generate at least one variant"


def test_counterfactual_none_is_backward_compatible():
    items = store_with("well-used item for testing")
    for mid in ids(items):
        for qt in ("x", "y"):
            record_query_hit(items, mid, qt)
    c = Consolidator(items)
    rep = c.run(current_turn=5, cause_by_id={m: "action-outcome" for m in items},
                counterfactual_replay=None)
    assert rep.counterfactuals_generated == 0
    assert rep.counterfactual_high_regret == 0
    assert len(rep.promoted) == 1


def test_counterfactual_high_regret_flagged():
    items = store_with("proceed without witness check")
    for mid in ids(items):
        for qt in ("a", "b"):
            record_query_hit(items, mid, qt)
    cr = CounterfactualReplay(simulate_fn=lambda o, v: ("reduces confabulation", 0.8))
    c = Consolidator(items)
    rep = c.run(current_turn=5, cause_by_id={m: "action-outcome" for m in items},
                counterfactual_replay=cr)
    assert rep.counterfactual_high_regret > 0


def test_counterfactual_dry_run_skips():
    items = store_with("proceed without witness check")
    for mid in ids(items):
        for qt in ("a", "b"):
            record_query_hit(items, mid, qt)
    cr = CounterfactualReplay()
    c = Consolidator(items)
    rep = c.run(current_turn=5, cause_by_id={m: "action-outcome" for m in items},
                counterfactual_replay=cr, dry_run=True)
    assert rep.counterfactuals_generated == 0
    assert len(rep.promoted) == 0


def test_counterfactual_via_agent_harness():
    from harness_core.agent_harness import AgentHarness
    h = AgentHarness(respond_fn=lambda m, c: "ok")
    h.remember_episode("proceed without witness check extra words here", query_type="a")
    mid = h.remember_episode("proceed without witness check extra words here", query_type="b")
    h.memory[mid].query_hits.add("a")
    h.counterfactual_replay = CounterfactualReplay()
    r = h.consolidate()
    assert r["counterfactuals"] > 0
    assert "high_regret" in r


def test_counterfactual_no_candidates_no_crash():
    items: dict[str, MemoryItem] = {}
    cr = CounterfactualReplay()
    c = Consolidator(items)
    rep = c.run(current_turn=5, cause_by_id={}, counterfactual_replay=cr)
    assert rep.counterfactuals_generated == 0


if __name__ == "__main__":
    check("counterfactual generates variants", test_counterfactual_generates_variants)
    check("counterfactual None backward compatible", test_counterfactual_none_is_backward_compatible)
    check("counterfactual high regret flagged", test_counterfactual_high_regret_flagged)
    check("counterfactual dry_run skips", test_counterfactual_dry_run_skips)
    check("counterfactual via AgentHarness", test_counterfactual_via_agent_harness)
    check("counterfactual no candidates no crash", test_counterfactual_no_candidates_no_crash)
    print(f"\n{PASS}/{PASS + FAIL} passed")
    sys.exit(1 if FAIL else 0)
