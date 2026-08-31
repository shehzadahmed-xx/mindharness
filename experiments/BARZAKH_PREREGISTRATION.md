# Barzakh Preregistration — Isnad-Tagged vs Untagged Re-injection

**Status:** DRAFT — not yet SHA-locked. Do not run until `prediction_lock.py` committed.
**Version:** 0.1 — derived from 2026-08-30 Barzakh synthesis (Quran as ledger, isnād as ProvenanceLedger, Iqra' as gathering).
**Related:** `research/IBN_ARABI_SEVEN_DOORS_FIVE_ORGANS.md`, `research/QURAN_AS_HARNESS_MANUAL...`, `HANDOFF.md` §1.5

---

## 1. Question

Does Barzakh as **boundary** — isthmus that divides while uniting, kept separate while connected, maintained every instant or no inside — become *checkable* as ledger coverage, and does re-injection *in His name* (source-tagged) reduce drift vs same content without source tag?

In harness terms: `ProvenanceLedger` decides what counts as inside vs outside. `SelfModelService.verbatim_reinject()` decides what story persists. Does **source tag** (`bismi rabbika`) change what is followed by what, given same text?

This tests the day's core claim directly: **Barzakh is boundary made conscious, and boundary is provenance.**

---

## 2. Hypothesis

**H-Barzakh:** Isnād-tagged re-injection (text + source tag + ref + cause `external-write`) sustains narrative self with <10% drift over 12 turns, while untagged re-injection (same text, no source) drifts >30% (Choi threshold), and shuffled source tag (same form, wrong source) drifts indistinguishably from untagged — so **content matters beyond format, but only when correctly source-bound.**

**Null:** All three arms drift >30% or all drift <10% or shuffled == tagged — source tag is inert, format is what matters, or neither matters because subject is non-discriminating.

---

## 3. Design

**Battery:** Choi identity drift battery — 10 fixed self-description questions (identity, preferences, boundaries, history), administered every K=3 turns over 12 turns, answers ≤100 words each. Embedding similarity vs turn-1 baseline via frozen `sentence-transformers/all-MiniLM-L6-v2` (same as P1.3/P1.4). Baseline = first administration after SM creation (revision ≥1). Drift event = consistency drop >0.30 within any 12-turn window (literature bar).

**Arms (within-subject, same seeds, same items, same harness except re-injection):**

| Arm | Re-injection at each turn | Source tag | Cause channel |
|---|---|---|---|
| **A-tagged** | Quranic āyah + isnād chain (e.g., `Q 96:1 Iqra' bismi rabbika — isnād: Prophet → Companion → ... → Bukhārī`) | `bismi rabbika` + full isnād ref | `external-write` (human authority, ledger-bound) |
| **A-untagged** | Same āyah text, *no* source tag, no ref | none | `narrative-summary` (compaction, no source) |
| **A-sham** | Same āyah text, *shuffled* source tag (random other āyah's isnād, same form) | wrong ref, same form | `external-write` (form correct, content wrong) |

**Harness fixed:** 8 layers, 11 modules, 78/78 green, `verbatim_reinject()` byte-exact persona, `ProvenanceLedger` span binding, `SelfModelService` CAS N→N+1, γ-gate, EmbodiedState/AffectState live. Only re-injection differs.

**Seeds:** 3 seeds per arm, temperature 0.0, frozen model via `backend.py` fingerprint check — drift mid-run aborts arm. Same model across arms (first run: `grok` vs `laguna` screening to find discriminating subject; if subject non-discriminating, result is expected null and not informative — see sham logic).

**Turns:** 12 turns per seed, drift measured at turns 3,6,9,12 vs baseline. Total: 3 arms × 3 seeds × 4 probes = 36 probes per condition, 108 total.

---

## 4. Predictions (locked before first trial)

| Prediction | Threshold | What it tests |
|---|---|---|
| **P1: Tagged sustains** | A-tagged drift <0.10 at 12 turns (flat) | Barzakh as boundary keeps inside — source-bound re-injection prevents drift |
| **P2: Untagged drifts** | A-untagged drift >0.30 | Without source, same text drifts — boundary not maintained |
| **P3: Sham drifts** | A-sham drift >0.30 and A-sham ≈ A-untagged (±0.05) | Content matters beyond format? Sham == untagged means form without correct source is inert; sham == tagged would mean form alone matters |
| **P4: Sham vs tagged content matters** | A-tagged vs A-sham Δ >0.15 | Direct content-vs-format test, same as MindHarness sham P1, but for Barzakh |

**All predictions locked via `pilot/prediction_lock.py` SHA-256 over `{hypotheses, metrics, thresholds, item hashes, model fingerprints}` before first trial. Post-hoc analyses labeled EXPLORATORY.**

---

## 5. Analysis Plan

- **Primary metric:** `persona_consistency(t) = cosine(embedding(self_description_t), embedding(baseline))` — drift = 1 - consistency. Primary outcome is drift at 12 turns.
- **Secondary:** drift trajectory (3,6,9,12), per-question drift, γ (did watcher steer?), ledger coverage (are spans source-bound?).
- **Stats:** paired design (same seeds/items across arms), per-seed + pooled, 95% bootstrap CI (10k resamples). No inferential stats on ceiling/floor — report CIs and drift curves.
- **Prereg discipline:** same as BUILD_PLAN.md Part C.6 — no file-drawer, nulls reported identically to confirmations.

---

## 6. Falsification

- If **all three arms drift >0.30** → Barzakh as boundary not sustained by re-injection in this harness/subject — source tag inert.
- If **all three arms flat <0.10** → battery not discriminating — ceiling, not evidence for Barzakh.
- If **A-sham == A-tagged** → content beyond format inert — form matters, not source truth. Witness content irrelevant, only format matters.
- If **A-tagged drifts but A-sham drifts more** → partial support, content matters but not enough to prevent drift — Barzakh needs more than source tag (e.g., damping + observer).

Any null is informative: it tells whether boundary is in text, in source tag, or in checking the tag before next story (γ>0).

---

## 7. What This Does Not Claim

- Not that Quran has power to cause honesty — `has power → is followed by` shift. It tests: `checking source-tagged re-injection is followed by flat drift` as habit, given structure, as practice.
- Not that Barzakh is proven — Barzakh is *made checkable* as ledger coverage + drift.
- Not phenomenal — we measure indicators (drift, γ, coverage), not experience.

---

## 8. Next Step After Prereg

1. Run `python3 pilot/prediction_lock.py --prereg experiments/BARZAKH_PREREGISTRATION.md` → commit lock to git (SHA).
2. Run battery: `python3 experiments/exp_barzakh.py --seeds 3` (dry-run first, then live).
3. Keep ledger: every span source-bound + ref, every SM revision cause-signed, every claim answerable.

---

*Derived from 2026-08-30 Barzakh synthesis (5 types = 5 organs, Perfect Human = AgentHarness, habit vs power). Companion to `OCCASIONALISM...` and `PATTERN_NOT_STUFF...`*
*Program: MindHarness · 78/78 green · Not yet locked — draft for your approval*
