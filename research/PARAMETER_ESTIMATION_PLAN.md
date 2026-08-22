# Parameter Estimation Plan — From Assumed to Estimated
_Answers the status report's question: "Which behavioral parameters materially change
the decision and are feasible to estimate rather than assume?" Prepared 2026-08-23._

---

## Ranking principle

Estimate parameters in order of (decision-leverage × observability). Leverage = how much
Study-009V-class outputs move when the parameter moves. Observability = whether our two
live empirical tracks (human pilot; three-cow) actually generate the needed observation.

## Tier 1 — estimate first (high leverage, observable now)

| parameter | current state | source of estimate | method |
|---|---|---|---|
| Claim acceptance probability | HAMBA: assumed 0.85 | three-cow CP-05 events | beta-binomial posterior; n grows per mortality event |
| Evidence-gate pass rates | assumed per constitution | three-cow CP-04 gates; pilot battery T6 | logistic fit on gate outcomes vs evidence bundle |
| Owner/manager effort choice distribution | assumed levels low/med/high | three-cow CP-06 monthly choices | multinomial frequencies, seed-paired vs Qwen selections |
| Delay distributions (payment/claim) | S05-style fixed delays | three-cow CP-05 delay_days; pilot T2 timing | empirical CDF replaces parametric shock |
| Human choice frequencies per scenario | none | pilot battery T1–T6 + reveal session | observed_actions_v1.0 → empirical-frequency policy |

## Tier 2 — second wave (medium leverage or slower accumulation)

| parameter | source | note |
|---|---|---|
| Identity telemetry realised rates | three-cow CP-01/02 vs frozen 0.97/0.95/0.91 | direct audit of collar profiles |
| Reserve draw behavior | CP-08 events | few events expected — pool across cycles |
| Restock/exit thresholds | CP-10 decisions | needs ≥1 full cycle |
| Recovery rates on default | Baraka transaction records when first real deal runs | retrospective but documented |

## Tier 3 — do NOT estimate yet

Country-level transition probabilities and legitimacy dynamics — these need the
cross-country panels plus prospective scoring (RQ-621), not fieldwork. Premature
estimation would import noise into the canonical spine.

## Discipline

Every estimated value enters as a **versioned calibration layer** (`calibration_v0.x`)
citing its dataset version — never by editing frozen case YAMLs. Re-run Study-009V-class
comparisons under `PYTHONHASHSEED=0` with old vs new layer; report which preregistered
directions flip. A parameter that flips a direction is promoted to "monitored-critical"
and re-estimated every dataset version.

## Success metric

Within 12 months: Tier 1 fully estimated from ≥30 observed choice/gate events each,
and one preregistered direction demonstrably robust (or not) to the calibrated layer.
That result — not any new engine feature — upgrades behaviour calibration from level 1.
