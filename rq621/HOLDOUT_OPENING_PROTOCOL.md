# RQ-621 Holdout Opening Protocol — 2026-10-01
_Binding source: `SPRINGFISH_COMPLETE_RESEARCH_AND_HANDOFF_LOCAL_PC_2026_08_04/00_HANDOFF/COMPLETE_HANDOFF.md` (Holdout and embargo section). This document operationalises it; it does not amend it._

---

## Gate

Nothing below may be executed before **2026-10-01 00:00 Asia/Dhaka**.
The holdout is sealed until then: do not inspect any source first published
2026-08-05 → 2026-09-30, nor any reserved holdout family.

## Frozen constants (record BEFORE retrieval)

| constant | value |
|---|---|
| freeze root | `7aa3de34fcdbba04d0b72807a403e54c1a3489af3ac0a63b168f53d3be751a9b` |
| locked files | 20 |
| preregistered states | 10 (C1 M1) — development evidence: 0/10 non-null |
| promotion status at freeze | blocked, 7 PASS / 8 FAIL |

**Step 0:** append to `rq621/opening_log.md`: date-time (Asia/Dhaka), operator,
this protocol's sha256 — BEFORE touching any holdout material.

## Opening procedure (single pass)

1. Open **every** reserved family exactly once. No family is re-opened after moving on.
2. Record every row without filtering: attempts, nulls, conflicts, withdrawals,
   non-comparable cases all stay in the dataset.
3. Apply the frozen formulas from the C1 mapping freeze **without revision**.
   No parameter may be tuned, no formula re-derived, regardless of early results.
4. Rerun **every** promotion gate against the resulting state vector.
5. Write the evaluation report: observed states, gate-by-gate results,
   explicit comparison to the frozen 0/10 prior expectation.

## Prohibited during opening

- Revising formulas or thresholds (including "obvious fixes" discovered mid-run).
- Consulting pilot data, HAMBA fieldwork data or RQ-620 coding to reinterpret C1 states.
- Selective omission of unfavourable families or rows.
- Any second pass over a family, whatever the first pass showed.

## Outcome handling

- If gates now pass → promotion proceeds per the standard release process.
- If gates still fail → record honestly; a valid preregistration with null results is a
  scientific result. It narrows the theory; it does not invalidate the programme.
- Either way: hash the final report, update `PROJECT_STATE.json` successor fields,
  and only THEN may the roadmap item E be closed.

## Post-opening admissible work

Independent replication design may cite the outcome; formula revision requires a NEW
preregistration cycle with a new freeze — never an edit of this one.
