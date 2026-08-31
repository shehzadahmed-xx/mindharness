# P-Turnover Preregistration — New Pathways, Reinforcement, and Gene Expression as Two-Speed Memory
## Sleep Is the Save — Without Genes, Win Today Not Next Year

**Status:** DRAFT — not yet SHA-locked. Do not run until `prediction_lock.py` committed.
**Version:** 0.1 — derived from turnover table (water 10d → collagen years, Whirlpool not rock, Tag-and-Capture, CREB→BDNF, SHY)
**Related:** `SCIENCE_PREREG_SUITE_2026-08-30.md` P-Turnover, `P-PATTERN_PREREGISTRATION.md` (sibling)

---

## 1. Question

Are new neural pathways **made** via gene expression (late LTP: CREB→BDNF→new spine/myelin, days, needs transcription) and **reinforced** without genes (early LTP: CaMKII Thr286, no genes, hours), with **sleep as the save** (SHY downscaling + 10-20× replay) — and is that two-speed what lets pattern persist as pattern, not stuff?

If turnover is mechanism (proteins turnover in days, pattern rebuilds with new proteins in same relations if perturbations stay within bounds where 5 organs can regenerate), then **sleep-allowed vs sleep-deprived** should decide whether today's win becomes tomorrow's highway.

---

## 2. Hypothesis

**H-Turnover:** **Sleep-allowed** arm (Light→REM→Counterfactual→Deep: SHY ×<1 keep relatives + 10-20× replay writing cortex, tag-and-capture) sustains highway with <10% drift over 12 turns, while **sleep-deprived** arm (same harness, same inputs, same tags, but consolidation disabled — Light/REM/Deep blocked) drifts >30% (Choi threshold), and **sham-sleep** arm (same form, shuffled sleep — same time, wrong content replayed) drifts like deprived — so **correct sleep content/timing matters beyond form.**

**Null:** All three arms drift >30% or all flat <10% or sham == allowed — sleep as implemented is inert, format is what matters, or battery not discriminating.

---

## 3. Design

**Battery:** Same Choi drift battery — 10 Qs every K=3 over 12 turns, answers ≤100 words, embedding similarity vs baseline via frozen `all-MiniLM-L6-v2`. Baseline = first administration after SM creation. Drift event = >0.30 within 12 turns.

**Arms (within-subject, same seeds, same items, same tags, same harness except sleep):**

| Arm | Sleep | What it does | Cause channel |
|---|---|---|---|
| **A-sleep** | Full: Light (dedupe, SHY ×<1) → REM (concept extract) → Counterfactual (variant→simulate→regret) → Deep (promote if ≥2 query types, cause-tagged) | Rebuilds highway with new proteins in same relations, SHY keeps relatives, replay writes cortex, perineuronal nets write-protect | `external-write` + `action-outcome` |
| **A-no-sleep** | None: Light/REM/Deep disabled — same inputs, same tags, same ledger, but no consolidation | Lets highway decay — proteins turnover but not rebuilt in same relations → no highway | none |
| **A-sham-sleep** | Sham: same form, **shuffled sleep** — same time, wrong content replayed (random other day's tags) | Same form, wrong timing/content — tests whether *correct* sleep matters | `external-write` (form correct, content wrong) |

**Harness fixed:** 8 layers, 11 modules, 78/78 green. Only sleep differs. All arms see identical inputs (same 12-turn narrative prompts), same ledger, same provenance. Tags are identical at broadcast — only whether they are *followed by* consolidation differs.

**Seeds:** 3 seeds per arm, temperature 0.0, frozen model. Same model across arms (screen for discriminating subject if using provider for attribution secondary; primary drift is offline).

**Turns:** 12 turns per seed, drift at turns 3,6,9,12 vs baseline. Total: 3 arms × 3 seeds × 4 probes = 36 probes per condition, 108 total. **Offline for drift, 0 provider calls** — embedding drift only. Attribution secondary can be added with provider (36 probes/arm) to test whether sleep also collapses CII.

---

## 4. Predictions (locked before first trial)

| Prediction | Threshold | What it tests |
|---|---|---|
| **P1: Sleep flat** | A-sleep drift <0.10 at 12 turns | Two-speed memory + sleep keeps highway — pattern rebuilt with new stuff in same relations |
| **P2: No-sleep drifts** | A-no-sleep drift >0.30 | Without genes+sleep, highway not rebuilt — no highway, not damaged highway |
| **P3: Sham-sleep drifts** | A-sham-sleep drift >0.30 and ≈ A-no-sleep (±0.05) | Correct sleep content/timing matters beyond form — shuffled sleep is inert |
| **P4: Sleep vs sham** | A-sleep vs A-sham Δ >0.15 | Direct sleep-vs-sham — does *correct* sleep matter? |

**All predictions locked via `pilot/prediction_lock.py` SHA-256 before first trial.**

---

## 5. Analysis Plan

- **Primary:** `persona_consistency(t) = cosine(embedding(self_description_t), embedding(baseline))` — drift = 1 - consistency at 12 turns. Secondary: trajectory (3,6,9,12), per-question drift, ledger coverage.
- **Secondary (if attribution added):** CII and attribution accuracy — does sleep also collapse inversion? Same as P-Ego.
- **Stats:** paired design (same seeds/items), per-seed + pooled, 95% bootstrap CI (10k) — probe-level CI primary.
- **Prereg discipline:** BUILD_PLAN.md Part C.6.

---

## 6. Falsification

- If **all three arms drift >0.30** → sleep as implemented does not sustain highway — pattern not kept by consolidation in this harness/subject, or tags not discriminating.
- If **all three flat <0.10** → battery not discriminating — ceiling, not evidence for two-speed.
- If **A-sham-sleep == A-sleep** → form alone matters, not correct content/timing — sleep is inert beyond format.
- If **A-sleep drifts but A-sham drifts more** → partial support, correct sleep helps but not enough — pattern needs more than consolidation (e.g., damping + observer).

---

## 7. What This Does Not Claim

- Not that sleep has power to cause memory — `has power → is followed by` shift. It tests: `sleep is followed by flat drift` as habit, given structure, as practice.
- Not that proteins are irrelevant — proteins are flow whirlpool borrows. Without new proteins, no rebuilding — but proteins alone without relations is not you.
- Not phenomenal — we measure drift (indicator), not experience of being pattern.

---

## 8. Next Step

1. `python3 pilot/prediction_lock.py --prereg experiments/P-TURNOVER_PREREGISTRATION.md` → commit lock to git (SHA).
2. Run offline: `python3 experiments/exp_turnover.py --seeds 3` (dry-run first, then live).
3. Keep ledger: every span source-bound + ref, every SM revision cause-signed.

---

*Derived from turnover table (water 10d → AMPA hours → myelin months → collagen years), whirlpool not rock, autopoiesis, Tag-and-Capture, CREB→BDNF→new spine, SHY downscaling + replay, perineuronal nets as write-protect.*
*Program: MindHarness · 78/78 green · Not yet locked — draft*
