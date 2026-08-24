"""Phase 5 acceptance tests — PREREQUISITES.md AC-5.1/5.2/5.3.

Run: python3 tests/test_phase5_consolidation.py   (plain runner, no pytest)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.consolidation import (Consolidator, MemoryItem,
                                        endorse_human, record_query_hit)

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


# ---------------------------------------------------------------- AC-5.2

def test_utility_gate_requires_two_query_types():
    items = store_with("musharaka pool distribution rules")
    mid = ids(items)[0]
    record_query_hit(items, mid, 'finance-query')          # 1 type only
    c = Consolidator(items)
    cands = c.rem_pass(current_turn=10)
    promoted, skipped = c.deep_pass(cands, {mid: 'action-outcome'})
    assert not promoted and any(s['id'] == mid for s in skipped)
    record_query_hit(items, mid, 'audit-query')            # now 2 types
    cands = c.rem_pass(11)
    promoted, _ = c.deep_pass(cands, {mid: 'action-outcome'})
    assert len(promoted) == 1 and promoted[0]['cause'] == 'action-outcome'
    assert items[mid].tier == 'semantic'


def test_human_endorsement_bypasses_gate():
    items = store_with("rare edge case worth keeping")
    mid = ids(items)[0]
    endorse_human(items, mid)                              # zero query hits
    c = Consolidator(items)
    cands = c.rem_pass(5)
    promoted, _ = c.deep_pass(cands, {mid: 'narrative-summary'})
    assert len(promoted) == 1 and promoted[0]['via'] == 'human_endorsed'


def test_cause_tag_missing_blocks_promotion():
    items = store_with("well-used item")
    mid = ids(items)[0]
    for qt in ('a', 'b'):
        record_query_hit(items, mid, qt)
    c = Consolidator(items)
    cands = c.rem_pass(3)
    try:
        c.deep_pass(cands, {})                # NO cause supplied
        blocked = False
    except AssertionError as e:
        blocked = 'UNTAGGED PROMOTION BLOCKED' in str(e)
    assert blocked, "hard invariant must fire on missing cause"


# ---------------------------------------------------------------- AC-5.3

def test_rem_ablation_changes_output():
    def build():
        items = store_with(
            "quarterly report mentions fertilizer subsidy delays",
            "team meeting notes about scheduling",
            "fertilizer subsidy affects pilot timeline")
        for i, mid in enumerate(ids(items)):
            for qt in ('q1', 'q2'):
                record_query_hit(items, mid, qt)
        return items

    full_items = build()
    abl_items = build()

    c_full = Consolidator(full_items)
    rep_full = c_full.run(current_turn=10,
                          cause_by_id={m: 'external-write' for m in full_items})
    c_abl = Consolidator(abl_items, rem_ablation=True)
    rep_abl = c_abl.run(current_turn=10,
                        cause_by_id={m: 'external-write' for m in abl_items})

    assert rep_full.rem_ran is True and rep_abl.rem_ran is False
    # ablated run promotes nothing via REM (no candidates extracted)
    assert len(rep_full.promoted) > 0
    assert len(rep_abl.promoted) == 0


# ---------------------------------------------------------------- AC-5.1

def test_all_promotions_carry_valid_causes():
    items = store_with("item one used often", "item two endorsed by human",
                       "item three also popular")
    mids = ids(items)
    for mid in mids:
        if mid != mids[1]:
            record_query_hit(items, mid, 'x')
            record_query_hit(items, mid, 'y')
    endorse_human(items, mids[1])
    causes = {mids[0]: 'action-outcome', mids[1]: 'external-write',
              mids[2]: 'narrative-summary'}
    c = Consolidator(items)
    _, promoted, _ = (lambda r: (r.candidates, r.promoted, r.skipped))(
        c.run(current_turn=7, cause_by_id=causes))
    assert len(promoted) == 3
    for p in promoted:
        assert p['cause'] in ('action-outcome', 'narrative-summary',
                              'external-write')


# ------------------------------------------------------------------ dedup

def test_light_dedupe_merges_signal():
    items = store_with("the cow completed its grazing cycle today",
                       "the cow completed its grazing cycle today!")
    a, b = ids(items)
    record_query_hit(items, b, 'field-query')
    c = Consolidator(items)
    removed = c.light_pass()
    assert removed == 1 and b not in items
    assert 'field-query' in items[a].query_hits   # signal merged into survivor


if __name__ == "__main__":
    check("AC-5.2 gate needs two query types", test_utility_gate_requires_two_query_types)
    check("AC-5.2 endorsement bypasses gate", test_human_endorsement_bypasses_gate)
    check("AC-5.1 untagged promotion BLOCKED", test_cause_tag_missing_blocks_promotion)
    check("AC-5.3 REM-ablation changes output", test_rem_ablation_changes_output)
    check("AC-5.1 all causes valid", test_all_promotions_carry_valid_causes)
    check("light dedupe merges signal", test_light_dedupe_merges_signal)
    print(f"\n{PASS}/{PASS + FAIL} passed")
    sys.exit(1 if FAIL else 0)
