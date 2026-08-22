# HAMBA Three-Cow Physical Pilot — Fieldwork Protocol (draft v0.1)
_Roadmap item J. Implements the frozen next action from `HAMBA-PILOT-001-RECOVERY-1`:
"Run the physical three-cow protocol and replace frozen identity, cost, evidence-use
and behavior assumptions with observed pilot data."_

---

## Objective

Convert the frozen prospective HAMBA model (all outputs SIM) into the programme's first
**observed-action dataset** by running three real collateral-and-identity cycles and
logging what actually happens at each decision gate.

## Frozen references (do not modify)

| artifact | path under `HAMBA_full/…/workspace_mirror/work/` |
|---|---|
| Frozen contract | `hamba_pilot_engine/hamba_pilot/HAMBA_PILOT_001_FROZEN_CONTRACT.json` |
| Model findings | `hamba_pilot_run/03_RESULTS/MODEL_FINDINGS.json` |
| Constitution scorecard | `hamba_pilot_run/03_RESULTS/CONSTITUTION_DECISION_SCORECARD.csv` |
| Full report | `05_REPORT/SPRINGFISH_HAMBA_COMPLETE_MODEL_REPORT_2026_08_21.html` |

Constitution assignments stand as decided: **C10 Balanced claims-control-integrity =
pilot control**; C12 Full-cost portable evidence = pricing/documentation target;
C11 "Evil HAMBA" is a prohibited red-team comparator — it must never be operated.

## Design skeleton

- **Subjects:** 3 cows, each with identity collar; one operator/owner dyad.
- **Cycle:** per animal — intake identity registration → feed/cost log → health event
  or scheduled check → evidence-use gate (which documents satisfy which claim) →
  revenue event → settlement per C10 waterfall → exit/restock decision.
- **Observation window:** minimum one full cycle per animal; target 90 days.

## Observed variables (the point of the exercise)

1. **Identity:** collar-read success rate, failure modes, re-registration events.
2. **Costs:** every line item vs the model's frozen cost assumptions (log actuals).
3. **Evidence use:** at each gate, which evidence was demanded / supplied / accepted /
   rejected — mapped to the contract's evidence clauses.
4. **Behaviour:** each choice point recorded as (actor, options available, option taken,
   stated reason ≤ 20 words). This is the observed-action gold standard.

## Data rules (inherit programme discipline)

- Namespace `hamba_field_v0.1`, append-only, checksummed weekly; corrections create
  v0.2+, never mutate.
- Observed rows are graded **observed-participant/e-part analog**; they NEVER edit the
  frozen SIM outputs — comparison tables only, side by side.
- Empirical-frequency policies may consume this dataset only via the versioned-dataset
  rule (same as human-pilot §9).

## Human-subjects boundary

If any worker/family member is interviewed beyond task logging, the human-pilot
protocol's layered consent (§4) applies to that person for that activity.

## Pre-launch checklist

- [ ] 3 collars procured & tested; failure-mode log template ready
- [ ] Cost ledger template matches MODEL_FINDINGS assumption categories 1:1
- [ ] Choice-point register pre-listed from the frozen contract (so nothing is invented mid-cycle)
- [ ] Weekly checksum routine scheduled
- [ ] C11 prohibition acknowledged in writing by every operator
