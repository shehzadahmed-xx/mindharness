# The Spring-Loaded Door — V32 Completeness Audit

**Version:** V32  
**Date:** 2026-07-28  
**Result:** PASS

## Registry reconciliation

| Registry | V31 prefix | V32 additions | V32 cumulative | Result |
| --- | ---: | ---: | ---: | --- |
| Actors | 2,616 | 139 | 2,755 | PASS |
| Relationships | 3,145 | 154 | 3,299 | PASS |
| Instruments | 1,382 | 88 | 1,470 | PASS |
| Mechanisms | 1,158 | 73 | 1,231 | PASS |
| Claims | 479 | 25 | 504 | PASS |
| Sources | 1,689 | 68 | 1,757 | PASS |
| Research queue | 533 | 25 | 558 | PASS |

## Preservation and reference checks

- Exact V31 JSON prefixes retained for all seven registries: **PASS**.
- All V32 actor IDs unique: **PASS**.
- All V32 relationship IDs unique: **PASS**.
- All V32 instrument, mechanism, claim, source and queue IDs unique: **PASS**.
- Every V32 relationship actor reference resolves: **PASS**.
- Every V32 instrument reference resolves: **PASS**.
- Every V32 mechanism reference resolves: **PASS**.
- Every V32 source reference resolves: **PASS**.

## Evidence reconciliation

| Grade | Expected | Observed | Result |
| --- | ---: | ---: | --- |
| E1 | 104 | 104 | PASS |
| E2 | 34 | 34 | PASS |
| S1 | 12 | 12 | PASS |
| A1 | 0 | 0 | PASS |
| U1 | 3 | 3 | PASS |
| N1 | 1 | 1 | PASS |

## Workbook checks

- Workbook reopened after final export: **PASS**.
- Cumulative worksheets: **229**.
- New V32 worksheets: **16**.
- Formula-error scan for `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?` and `#N/A`: **0 matches**.
- Overview key counts match JSON: **PASS**.
- V32 Delta counts and evidence totals match JSON: **PASS**.
- Overview preview rendered: **PASS**.
- V32 Delta preview rendered: **PASS**.

## Package checks

- SHA-256 manifest generated from final files: **PASS**.
- ZIP archive creation and CRC test: **PASS**.

## Completeness boundary

The audit establishes structural, referential and package integrity. It does not establish worldwide transaction-level completeness. Completeness must be declared for a specified jurisdiction, corridor, population, period and source perimeter.
