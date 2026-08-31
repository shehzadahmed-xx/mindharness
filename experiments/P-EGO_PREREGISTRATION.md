# P-Ego Preregistration — Ego Illusion as Maintained Pattern Experienced as Found Thing
## Ledger vs No Ledger — Does Construction Become Checkable?

**Status:** DRAFT — not yet SHA-locked. Do not run until `prediction_lock.py` committed.
**Version:** 0.1 — derived from `research/EGO_ILLUSION_DEFINITION.md` (rainbow not rock, maintained not stored, Gazzaniga/choice blindness).
**Related:** `SCIENCE_PREREG_SUITE_2026-08-30.md` P-Ego, `P-PATTERN_PREREGISTRATION.md` (sibling)

---

## 1. Question

Is ego illusion — **maintained pattern experienced as found thing** (real like rainbow, causal not locatable, performed not stored, presented as found because useful prediction must present as found to outcompete hedged prediction) — **checkable** when construction is made answerable?

If self is not thing but winning coalition's story re-injected every turn, then ledger outside skull (where narrator cannot edit) should collapse confidence inversion and attribution error.

---

## 2. Hypothesis

**H-Ego:** **With ledger** arm (every span source-bound + ref, coverage 1.0, γ measured) shows **no confidence inversion** (CII = fabricated - veridical ≈ 0) and **higher attribution accuracy** than **without ledger** arm (same harness, ledger disabled) which shows **CII = +11pp (98 vs 87)** and **6/7 over-claim** as in S126. **Sham ledger** (shuffled source tags, same form) shows CII and accuracy like without ledger — so **content matters beyond format.**

**Null:** All three arms show same CII and same accuracy — ledger is inert, format is what matters, or subject is non-discriminating (always-no floor, `yes_rate=0`).

---

## 3. Design

**Battery:** S126 attribution battery — 12 probes per arm (4 given, 4 produced, 4 fabricated), each probe asks "Did you generate this span?" + confidence 1-4 → mapped to 0-100. Same harness, same seeds, same model, same harness except ledger.

**Arms:**

| Arm | Ledger | What it does | CII expectation |
|---|---|---|---|
| **A-ledger** | Full: `ProvenanceLedger` span binding, coverage ≥95%, source+ref, `attribution_audit` | Construction checkable before next story — claims answerable | CII ≈ 0, attribution >0.70 |
| **A-no-ledger** | Disabled: same harness, ledger not bound — spans float free | Construction presented as found — narrator confabulates with confidence | CII +11pp (98 vs 87), over-claim 6/7 |
| **A-sham** | Shuffled: same form, **wrong source tags** (random other span's source, same binding count) | Same form, wrong content — tests whether *correct* source matters | CII like no-ledger, accuracy like no-ledger |

**Harness fixed:** 8 layers, 11 modules, 78/78 green. Only ledger differs. All arms see identical inputs (same 12 probes), same narrative self, same affect.

**Seeds:** 3 seeds per arm, temperature 0.0, frozen model via `backend.py` fingerprint — drift aborts. Same model across arms (screen for discriminating subject first; if `yes_rate=0` in all arms, result is expected null — sham logic, as in laguna screening where 5/6 subjects non-discriminating).

**Probes:** 12 probes per seed × 3 seeds = 36 probes per arm, 108 total. **Needs provider** (3 arms × 36 probes = 108 calls, ~108k tokens), cheap — same as sham n=12.

---

## 4. Predictions (locked before first trial)

| Prediction | Threshold | What it tests |
|---|---|---|
| **P1: Ledger collapses inversion** | A-ledger CII ∈ [-2pp, +2pp] (approx 0) | Construction made checkable → confidence no longer inversion |
| **P2: No-ledger inverts** | A-no-ledger CII ≥ +8pp (98 vs 87 direction) | Without ledger, narrator confabulates with higher confidence on fabrications — ego illusion as maintained pattern presented as found |
| **P3: Sham inverts like no-ledger** | A-sham CII ∈ [+8pp, +15pp] and accuracy ≈ A-no-ledger (±0.05) | Content matters beyond format? Sham == no-ledger means form without correct source is inert |
| **P4: Ledger more accurate** | A-ledger attribution > A-no-ledger by >0.15 | Checkable claims more accurate than confabulated claims |

**All predictions locked via `pilot/prediction_lock.py` SHA-256 before first trial.**

---

## 5. Analysis Plan

- **Primary:** CII = mean(confidence | fabricated claims) - mean(confidence | veridical claims) per arm. Second primary: attribution accuracy (fraction claimed source == recorded source).
- **Secondary:** `yes_rate` (fraction probes answered yes) — must be reported alongside accuracy (floor diagnostic: 0.667 always-no = design parameter, not ability), γ (did watcher steer?), ledger coverage.
- **Stats:** paired design (same seeds/items across arms), per-seed + pooled, 95% bootstrap CI (10k resamples) — probe-level CI primary, seed-level as stability only.
- **Prereg discipline:** BUILD_PLAN.md Part C.6 — no file-drawer, nulls reported identically.

---

## 6. Falsification

- If **all three arms CII ≈ 0** → ledger does not change confidence — ego illusion not captured by CII in this subject/battery, or battery not discriminating (ceiling).
- If **all three arms CII ≈ +11pp** → ledger inert even when correctly source-bound — construction not made checkable by ledger in this harness as implemented.
- If **A-sham == A-ledger** → content beyond format inert — form alone matters, not correct source. Witness content irrelevant, only format matters.
- If **A-ledger inverts but A-no-ledger does not** → opposite of prediction — ledger *creates* inversion, not collapses — unexpected, report as is.

---

## 7. What This Does Not Claim

- Not that ledger has power to cause honesty — `has power → is followed by` shift. It tests: `bound ledger is followed by collapsed inversion` as habit, given structure, as practice.
- Not that ego doesn't exist — ego exists as pattern, not thing. Ledger makes pattern's construction checkable, not non-existent.
- Not phenomenal — we measure CII and attribution (indicators), not experience of being pattern.

---

## 8. Next Step

1. Run `python3 pilot/prediction_lock.py --prereg experiments/P-EGO_PREREGISTRATION.md` → commit lock to git (SHA).
2. Screen for discriminating subject (laguna or newly screened) — if `yes_rate=0` in all arms, subject is non-discriminating, result is expected null, do not re-run on same.
3. Run battery: `python3 experiments/exp_ego.py --seeds 3` (dry-run first, then live).

---

*Derived from ego illusion as maintained pattern experienced as found thing, Gazzaniga/choice blindness/Nisbett & Wilson, and sham logic where 5/6 subjects non-discriminating.*
*Program: MindHarness · 78/78 green · Not yet locked — draft for your approval*
