# V34.2.x → Canonical Successor — Adjudication Worksheet (starter)
_Roadmap item F. Rule: claim-by-claim review before any candidate enters a successor
to V34.0. Prepared 2026-08-23 from PROJECT_STATE synthesis records + 08-21 status report._

---

## Established facts about the candidate chain

From `PROJECT_STATE.json` (V34.2.4) synthesis block — the entire V34.2.x chain added
**zero machine ledger rows** and **zero runtime mappings**; every release gate passed;
every delta remained `candidate_not_canonical`:

| version | character | ledger rows | runtime maps | tests / gates |
|---|---|---|---|---|
| V34.2 | unmerged candidate delta | 0 | 0 | — |
| V34.2.1 | Ch.262 append (prose only) | 0 | 0 | — |
| V34.2.2 | Ch.263–264 + branch-qualified research packets | 0 | 0 | 30/30 · 20/20 |
| V34.2.3 | Ch.265 MiroFish reconciliation + comparator audit | 0 | 0 | 24/24 · 18/18 |
| V34.2.4 | Ch.266 bridge execution + fail-closed manifest gate | 0 | 0 | 25/25 · 20/20 · matrix 18/18 |
| V34.2.6 | AEQ-001 qualification candidate (Practice Fusion bounded component machinery) | 0 | 0 | local tree checksums PASS |
| V34.2.7 | merged Study009V runnable state | **NOT LOCAL** | ? | 127 combined per status report |

## Consequence for adjudication scope

Because no canonical rows were created anywhere in the chain, adjudication is mostly
**adoption of prose chapters + machinery**, NOT row promotion. The row-level question
only opens if a chapter asserts new actors/relationships that deserve ledger status.

## Per-item verdict template

For each item below, record: verdict ∈ {adopt-chapter, adopt-machinery,
promote-rows(specify), reject, defer}, reviewer, date, one-paragraph rationale,
and whether it touches protected domains (legal/accounting/financial/material/canonical).

| # | item | class | proposed verdict space |
|---|---|---|---|
| 1 | Ch.262–266 prose | theory chapters | adopt-chapter (they are already hash-pinned in synthesis chain) |
| 2 | Fail-closed manifest equality gate (V34.2.4 code) | machinery | adopt-machinery — prevents silent graph/payload mismatch by construction |
| 3 | SIM / MESSAGE_ONLY / executor-firewall (Ch.266.3) | machinery | adopt-machinery — operationalises non-negotiable rule #3 |
| 4 | Verified-vs-contaminated consensus separation | machinery | adopt-machinery — operationalises rule #4 |
| 5 | RQ-620 M1A external coder packet design | machinery | adopt after coder cycle completes (item C dependency) |
| 6 | AEQ-001 Practice Fusion bounded component (USD 959,700 gross) | evidence object | defer — eligible for independent review first (item G); never promote as net-loss figure |
| 7 | Study009V outputs (384 paths, case deltas) | SIM results | reject-as-canonical by definition (rule: SIM ≠ ledger); adopt REPORT.md as methods appendix |
| 8 | C3 instability finding (37.5% Nash, regret 0.11) | model result | adopt-chapter into methods/status docs; drives held-out selection (already used) |
| 9 | PYTHONHASHSEED=0 replay discipline | machinery | adopt-machinery — byte-determinism requirement for detailed replays |

## Procedure

1. One worksheet row per item, completed by reviewer independently BEFORE discussion.
2. Disagreements logged verbatim (same discipline as RQ-620 coding).
3. A successor ledger version number is minted ONLY when every row has a recorded
   verdict and the diff it implies is itself fail-close gated against V34.0.
4. V34.2.7 items join this worksheet upon retrieval of its archive.

## Standing prohibitions carried in

No frozen-manifest rewrites; no holdout consultation; no formula revision; no synthetic
substitution for NOT_AVAILABLE objects.
