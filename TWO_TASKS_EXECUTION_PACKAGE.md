# TASK 1 — B2/B4 Dreaming Contrast Execution Package
## Recursive Depth During Non-Lucid REM — Tier 1 Priority

_Status: READY FOR ETHICS SUBMISSION · Preregistration sealed · Analysis code needed_

---

## What this task produces

Answer to: *"Does non-lucid REM dreaming show L1–L2 experience with L4–L5 recursive depth at floor, verified in-state?"*

Pattern A firing = recursive depth NOT necessary for conscious experience = H1-minimal necessity challenged + Beautiful Loop depth-necessity challenged.

## Completed already

- [x] Preregistration document (`pilot/B2B4_PREREGISTRATION.md`) — variables locked
- [x] Positive controls specified per §136.2
- [x] Null/equivalence criteria per §134.4 (TOST + BF₀₁ > 3)
- [x] Confound battery closed per §136.4
- [x] Outcome patterns pre-written per §136.6
- [x] No-Proving clause per §136.7

## Remaining to build (from this machine)

### 1a. Analysis pipeline (Python)
```
pilot/b2b4/analysis_pipeline.py
├── sleep_scoring.py          # EEG epoch classification
├── probe_delivery.py         # Auditory stimulus scheduling during REM
├── response_detection.py     # EMG finger-press detection + scoring
├── meta_dprime.py            # HMeta-d hierarchical Bayesian estimation
├── equivalence_testing.py    # TOST + Bayes factor for null
├── variance_partitioning.py  # §135.3 hierarchical regression
└── report_generator.py       # Auto-formatted results per §136.6 patterns
```
**Status:** NOT YET WRITTEN — needs ~500 lines Python using mne-python, pingouin, scipy

### 1b. Simulated data validation
```
pilot/b2b4/test_pipeline.py
├── Generate synthetic REM data with known depth values
├── Run pipeline on synthetic data
├── Verify: pipeline recovers known values within tolerance
├── Verify: Pattern A/B/C/D correctly identified on simulated outcomes
└── Freeze pipeline version BEFORE real collection
```
**Status:** NOT YET WRITTEN

### 1c. IRB submission package
```
pilot/b2b4/ethics/
├── protocol_summary.doc      # From preregistration
├── consent_form.doc          # Per governance protocol §4 layered consent
├── risk_assessment.doc       # Sleep disruption minimal; no deception
├── data_management_plan.doc  # Pseudonymised; local storage only
└── investigator_brochure.pdf # CVs, facilities, references
```
**Status:** TEMPLATE NEEDED — user fills institutional details

## External requirements (user must arrange)

| requirement | spec | est. cost |
|---|---|---|
| Sleep lab access | PSG-capable, ≥7 nights/participant | variable |
| EEG system | 32-channel actiCap or equivalent | existing or rent |
| Audio stimulator | Programmable, calibrated 55–70 dB | <$500 |
| EMG finger sensor | Accelerometer or piezo | <$100 |
| Participants | N=12–16, high dream recall | recruitment |
| Ethics approval | Institutional review board | timeline-dependent |

---

# TASK 2 — Three-Cow Pilot Launch Package
## Type-One Loop Survival Test — HAMBA-PILOT-001 Physical Phase

_Status: PROTOCOL COMPLETE · Choice-points registered · Data templates needed_

---

## What this task produces

Answer to: *"Can a type-one loop (cost-internalising, transparent, self-reinforcing through genuine value creation) survive at minimum viable scale inside a type-two ecology?"*

Pattern confirmed = architecture viable at n=1 operational unit → scales to full HAMBA deployment.
Pattern failed = specific failure point identifies which boundary structure needs reinforcement before retry.

## Completed already

- [x] Frozen contract (`HAMBA_PILOT_001_FROZEN_CONTRACT.json`)
- [x] Constitution decision (C10 control / C12 target / C11 prohibited)
- [x] Choice-point register CP-01 through CP-10 (`hamba/CHOICE_POINT_REGISTER.csv`)
- [x] Fieldwork protocol (`hamba/THREE_COW_FIELDWORK_PROTOCOL.md`)
- [x] Dataset schema (`datasets/hamba_field_v0.1.schema.json`)
- [x] Model predictions banked (58,368 portfolio paths, 36 pure-Nash profiles)

## Remaining to build (from this machine)

### 2a. Data collection templates
```
hamba/data_templates/
├── cp01_identity_log.csv         # collar reads per animal per day
├── cp02_telemetry_weekly.csv     # realised vs frozen telemetry rates
├── cp03_cost_ledger.csv          # actual costs vs frozen assumptions
├── cp04_evidence_gate_log.csv    # demanded/supplied/accepted/rejected
├── cp05_claim_decision.csv       # insurance claims filed/outcome/delay
├── cp06_effort_choice.csv        # monthly owner-management decisions
├── cp07_sale_consent.csv         # co-owner sale events (C-cow only)
├── cp08_reserve_draw.csv         # shortfall events and responses
├── cp09_settlement_order.csv     # actual payment order per cycle
└── cp10_exit_decision.csv        # restock/exit with stated reason
```
**Status:** HEADERS ONLY — column specs derived from CHOICE_POINT_REGISTER.csv but CSV files not yet generated

### 2b. Weekly checksum routine
```
hamba/checksum_routine.sh
├── sha256 all template files
├── append to integrity ledger
├── flag any file modified without corresponding entry
└── alert if >48h since last verification
```
**Status:** NOT YET WRITTEN — simple bash script

## External requirements (user must arrange)

| requirement | spec | notes |
|---|---|---|
| 3 cows | Healthy, identifiable, distinct owner arrangements | HAMBA-A (farmer-owned), HAMBA-B (owner+manager), HAMBA-C (co-owned) |
| 3 identity collars | OPEN_API_SOLAR / VENDOR_CLOUD / LOW_POWER_LONG_INTERVAL | per frozen contract profiles |
| Location | Bangladesh, rural, accessible weekly | near operator |
| Insurance | Per frozen contract claim terms | arranged before intake |
| Operator | Trained on choice-point register | records CP entries daily |

---

# SEQUENTIAL EXECUTION ORDER

```
TASK 1 (B2/B4 Dreaming)              TASK 2 (Three-Cow Pilot)
─────────────────────────           ─────────────────────────
Phase A: Build analysis code    │    Phase A: Build data templates
         + validate on sim data │    Phase B: Procure cows/collars
Phase B: Submit ethics          │    Phase C: Train operator  
Phase C: Recruit participants   │    Phase D: Launch fieldwork
Phase D: Collect sleep lab data │    Phase E: 90-day observation window
Phase E: Run analysis pipeline  │    Phase F: Score against model predictions
Phase F: Fire Pattern A/B/C/D   │    Phase G: Compare observed vs SIM
         ↓                               ↓
    Consciousness paper             HAMBA scaling decision
```

Tasks are INDEPENDENT — either can proceed without the other.
Recommended: start BOTH Phase As simultaneously (both buildable now).
