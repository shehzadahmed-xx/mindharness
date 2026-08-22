# AEQ-001 Independent Reviewer Packet — Assembly Guide
_Roadmap item G. Prepared 2026-08-23. Goal: independent admission (or refutation) of
the first author-side Architected Extraction component._

---

## What the reviewer receives

Ship the reviewer **read access to the V34.2.6 candidate tree** (or a zip of `aeq001/`)
plus this guide — never the author's interpretations alone.

Base path: `HAMBA_full/…/recovery/v3426/SPRINGFISH_V34_2_6_AEQ001_QUALIFICATION_CANDIDATE_2026_08_14/`

| # | artifact | role |
|---|---|---|
| 1 | `aeq001/cases/PRACTICE_FUSION_PAIN_CDS_2016_2019.json` | case file: entity, period, mechanism, bounded component |
| 2 | `aeq001/analysis/PRACTICE_FUSION_ADMISSION_AUDIT.json` | six-condition audit trail |
| 3 | `aeq001/AEQ001_ADJUDICATION_AND_QUALIFICATION_WORKBOOK.xlsx` (+ `.inspect.ndjson`) | line-by-line qualification workbook |
| 4 | `aeq001/validation/AEQ001_RELEASE_VALIDATION.json` + console txt | release-gate outputs |
| 5 | `run_aeq001_qualification.py`, `validate_aeq001_release.py`, `tests/test_aeq001.py`, `springfish/aeq001.py` | executable reproduction |
| 6 | `aeq001/prospective/AEQ_P01_PREREGISTRATION.md` | preregistration context |

## Reviewer mandate (state verbatim in the invitation)

1. Independently verify each of the six admission conditions against public sources:
   operating entity, period, beneficiary, institutional arrangement, material benefit,
   causal connection.
2. Recompute the bounded gross component (**USD 959,700, recipient-side**) from the
   cited documents. Confirm or contest the arithmetic and its documentary basis.
3. Attempt refutation: find any condition that fails, any double-count with other
   components, or any classification error (productive return / conversion rent /
   avoided-cost transfer / public-support value / uninternalized liability).
4. State explicitly whether the component is **admitted**, **admitted-with-correction**
   (specify), or **not admitted**.

## Boundaries printed on the packet

- This is a bounded gross recipient-side amount — reviewers are asked to evaluate THAT
  claim, not to produce a net social-loss estimate.
- Admission is not intent attribution; no finding implies deliberate design.
- Reviewer independence statement required (same wording as replication brief).
- Results publishable by the reviewer regardless of direction.

## Return format

Signed review memo + recomputation worksheet + condition-by-condition verdict table.
Author response rights: one memo, appended unedited.
