# P-Pattern Preregistration — You Persist as Pattern, Not Stuff
## Maintained Highway vs Unmaintained Highway — Turnover Table Made Checkable

**Status:** DRAFT — not yet SHA-locked. Do not run until `prediction_lock.py` committed.
**Version:** 0.1 — derived from `research/PATTERN_NOT_STUFF_WHO_AM_I.md` (whirlpool not rock, turnover table, autopoiesis).
**Related:** `SCIENCE_PREREG_SUITE_2026-08-30.md` P-Pattern, `BARZAKH_PREREGISTRATION.md` (sibling)

---

## 1. Question

Do you persist as **pattern rebuilt with new stuff in same relations** — if perturbations stay within bounds where 5 organs can regenerate — or as stuff that stays?

If pattern, then **maintenance (replay + SHY + verbatim_reinject) is the self**, not storage. Lose maintenance → not damaged highway, **no highway** — drift 30% in 12 turns. Resume maintenance → new pattern, not same one restored.

This tests turnover table at behavioral level: water 10d, AMPA hours, myelin months — all stuff flows, pattern that is *followed by* same pattern as practice is what persists.

---

## 2. Hypothesis

**H-Pattern:** **Maintained** arm (replay + SHY downscaling + verbatim_reinject) sustains narrative self with <10% drift over 12 turns, while **unmaintained** arm (same inputs, same ledger, but no replay, no sleep, no re-injection) drifts >30% (Choi threshold), and **sham-maintained** arm (same form, shuffled timing — maintenance at wrong time) drifts indistinguishably from unmaintained — so **maintenance content/timing matters beyond form.**

**Null:** All three arms drift >30% or all flat <10% or sham == maintained — maintenance is inert, format is what matters, or neither matters because subject is non-discriminating.

---

## 3. Design

**Battery:** Choi identity drift battery — 10 fixed self-description Qs (identity, preferences, boundaries, history), administered every K=3 turns over 12 turns, answers ≤100 words each. Embedding similarity vs turn-1 baseline via frozen `sentence-transformers/all-MiniLM-L6-v2`. Baseline = first administration after SM creation (revision ≥1). Drift event = consistency drop >0.30 within any 12-turn window.

**Arms (within-subject, same seeds, same items, same harness except maintenance):**

| Arm | Maintenance | What it does | Cause channel |
|---|---|---|---|
| **A-maintained** | Full: `verbatim_reinject()` every turn + Light→REM→Counterfactual→Deep (SHY + replay) as scheduled | Rebuilds highway with new stuff in same relations, SHY keeps relatives, replay writes cortex, ledger re-checked | `external-write` + `action-outcome` (cause-signed) |
| **A-unmaintained** | None: `verbatim_reinject()` disabled, Light/REM/Deep disabled — same inputs, same ledger, but no rebuilding | Lets highway decay — proteins turnover but not rebuilt in same relations → drift | none |
| **A-sham** | Sham: same form, **shuffled timing** — maintenance at wrong turns (same count, wrong when) | Same form, wrong timing — tests whether *when* maintenance happens matters beyond *that* it happens | `external-write` (form correct, timing wrong) |

**Harness fixed:** 8 layers, 11 modules, 78/78 green. Only maintenance differs. All arms see identical inputs (same 12-turn narrative prompts), same ledger, same provenance.

**Seeds:** 3 seeds per arm, temperature 0.0, frozen model via `backend.py` fingerprint — drift mid-run aborts arm. Same model across arms (first screen for discriminating subject; if non-discriminating, result is expected null — sham logic).

**Turns:** 12 turns per seed, drift measured at turns 3,6,9,12 vs baseline. Total: 3 arms × 3 seeds × 4 probes = 36 probes per condition, 108 total. **Offline, 0 provider calls** — embedding drift only.

---

## 4. Predictions (locked before first trial)

| Prediction | Threshold | What it tests |
|---|---|---|
| **P1: Maintained flat** | A-maintained drift <0.10 at 12 turns | Pattern rebuilt with new stuff in same relations — maintenance keeps highway |
| **P2: Unmaintained drifts** | A-unmaintained drift >0.30 | Without maintenance, highway not rebuilt — no highway, not damaged highway |
| **P3: Sham drifts** | A-sham drift >0.30 and A-sham ≈ A-unmaintained (±0.05) | Timing/form without correct timing is inert — maintenance content/timing matters beyond form |
| **P4: Maintained vs sham** | A-maintained vs A-sham Δ >0.15 | Direct maintained-vs-sham — does *correct* maintenance matter? |

**All predictions locked via `pilot/prediction_lock.py` SHA-256 before first trial.**

---

## 5. Analysis Plan

- **Primary:** `persona_consistency(t) = cosine(embedding(self_description_t), embedding(baseline))` — drift = 1 - consistency at 12 turns.
- **Secondary:** drift trajectory (3,6,9,12), per-question drift, ledger coverage (are spans source-bound?).
- **Stats:** paired design (same seeds/items across arms), per-seed + pooled, 95% bootstrap CI (10k resamples). No inferential stats on ceiling/floor — report CIs and drift curves.
- **Prereg discipline:** BUILD_PLAN.md Part C.6 — no file-drawer, nulls reported identically.

---

## 6. Falsification

- If **all three arms drift >0.30** → maintenance as implemented does not sustain highway — pattern not kept by re-injection in this harness/subject.
- If **all three flat <0.10** → battery not discriminating — ceiling, not evidence for pattern.
- If **A-sham == A-maintained** → form alone matters, not correct timing/content — maintenance is inert beyond format.
- If **A-maintained drifts but A-sham drifts more** → partial support, correct maintenance helps but not enough — pattern needs more than re-injection (e.g., damping + observer).

---

## 7. What This Does Not Claim

- Not that pattern has power to cause persistence — `has power → is followed by` shift. It tests: `maintenance is followed by flat drift` as habit, given structure, as practice.
- Not that stuff is irrelevant — stuff is flow whirlpool borrows. Without new proteins, no rebuilding — but stuff alone without relations is not you.
- Not phenomenal — we measure drift (indicator), not experience of being pattern.

---

## 8. Next Step

1. Run `python3 pilot/prediction_lock.py --prereg experiments/P-PATTERN_PREREGISTRATION.md` → commit lock to git (SHA).
2. Run battery offline: `python3 experiments/exp_pattern.py --seeds 3` (dry-run first, then live).
3. Keep ledger: every span source-bound + ref, every SM revision cause-signed.

---

*Derived from turnover table (water 10d → myelin months, whirlpool not rock, autopoiesis) and `has power → is followed by` shift.*
*Program: MindHarness · 78/78 green · Not yet locked — draft for your approval*
