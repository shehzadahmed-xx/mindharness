# B2/B4 Preregistration — Recursive Depth During Non-Lucid REM Dreaming
## Testing Whether Conscious Experience Persists Without Recursive Self-Monitoring

_Preregistered before data collection per §136.8. This document is the binding worksheet.
Once timestamped (OSF or equivalent), no variable, criterion, threshold, or analysis order
may be changed. Deviations are logged and affected cells scored OPEN._

---

## 1. Hypothesis Under Test

**H1-minimal:** Conscious experience requires *some* self-monitoring relation (Level ≥ 2),
but does NOT require recursive depth (Level ≥ 4) or narrative self-modeling.

**Beautiful Loop depth-necessity:** Conscious experience requires recursive epistemic
depth (Level ≥ 3–5).

**Pattern A prediction (from H1-minimal):** Non-lucid REM dreaming will show V1 ✓, V2 ✓,
V3 ✓, V4 ↓/✓, **V5 absent** (at floor per preregistered equivalence criteria).

**Competing prediction (from Beautiful Loop):** If depth is necessary, either V1 drops
(no experience without depth) or V5 will NOT be at floor (depth persists below lucid
thresholds).

**Pattern B prediction (from H1 sufficiency):** If V5 is present while V1 is absent →
self-monitoring is not sufficient → attacks H1 from the opposite direction.

---

## 2. Study Design

### 2.1 Design Overview

Within-subjects, repeated-measures, multi-night sleep laboratory study.

| condition | description | nights |
|---|---|---|
| **Non-lucid REM** | Natural REM epochs without induced lucidity; auditory confidence probes delivered; immediate awakening after probe blocks | ≥3 |
| **Lucid REM** (positive control) | Verified lucid episodes via pre-sleep induction training + reality-check cues; eye-signal confirmation of lucid insight | ≥2 |
| **Waking baseline** (probe liveness control) | Same battery administered while awake, seated, eyes closed | 1 |
| **NREM stage 2** (negative control) | Same probes delivered during stable N2; expected: V1↓, all other cells open | ≥1 |

Minimum total: **7 laboratory nights** per participant.

### 2.2 Participants

- N = 12–16 (power analysis: detecting meta-d′ < 0.20 of within-subject SD at α=0.05,
  power=0.80, requires ~12 completers; oversample for attrition)
- Inclusion: healthy adults 21–45, regular sleepers (7–9h), no sleep disorders
  (PSG-screened), high dream recall frequency (≥4/week), no psychoactive medication
- Exclusion: apnea, restless leg, narcolepsy, psychiatric diagnosis, psychedelic use
  within 6 months

### 2.3 Apparatus

| channel | device/signal | purpose |
|---|---|---|
| EEG | 32-channel actiCap, BrainVision | Sleep staging, ERP (P300/N1), PCI-proxy complexity |
| EOG | Left + right outer canthus | Sleep staging, eye-movement detection, eye-signal recording |
| EMG | Submental | Atonia verification (REM confirmation) |
| Audio | Programmable closed-ear stimulator | Confidence probe delivery during REM (calibrated 55–70 dB SPL) |
| EMG finger | Accelerometer on dominant index finger | In-state motor response to probes |
| Respiratory belt | Chest expansion | Sleep staging support, autonomic anchor |

### 2.4 Auditory Probe Design

Probes are delivered during stable REM epochs (≥30 s after REM onset, no K-complexes
or arousals in preceding 60 s). Each probe block contains:

| probe type | stimulus | in-state response required | maps to |
|---|---|---|---|
| First-order discrimination | Two-tone sequence (high vs low pitch), randomized | Finger press: left = low, right = high | V2 |
| Internal-state probe | "Rate your current emotional state" via pre-trained category (calm/alert/negative/positive) | Finger press: one of four positions | V3 |
| Self/world probe | Pre-recorded voice says own name vs stranger name, randomized | Finger press: left = own, right = other | V4 |
| Type-2 confidence | After each first-order trial: "How confident?" | Finger press: 1–4 scale (pre-mapped to force levels) | V5 |
| PAS rating | "How clear was your perceptual experience?" | Finger press: PAS 1–4 scale | V1 |

Each probe block = 10 trials minimum. Blocks separated by ≥60 s of unprompted REM.
Maximum 4 blocks per REM period. Inter-stimulus interval jittered 2.0–3.5 s.

**Probe liveness verification (per §136.2):**
Before each night, subject demonstrates all finger responses while awake with eyes
closed. Positive controls embedded in each session:
- Waking baseline: all probes must exceed d′ > 1.0
- Light sleep (N1): first-order d′ must remain above chance if subject signals
- If no in-state response detected across entire REM period → all cells scored OPEN

---

## 3. Measured Variables (Locked)

| # | Variable | Operational definition | Scored when |
|---|---|---|---|
| V1 | Conscious experience | PAS rating from in-state finger press OR verbal report ≤60 s post-awakening tied to specific probe block | Probe fired in-state |
| V2 | First-order representation | Discrimination accuracy (d′) on two-tone task from in-state finger presses | ≥10 trials completed in-state |
| V3 | Internal-state representation | Accuracy on internal-state categorization from in-state responses | ≥5 trials in-state |
| V4 | Self/world relation | Own-name vs stranger-name discrimination accuracy | ≥5 trials in-state |
| V5 | Recursive monitoring | Meta-d′ computed from type-2 confidence calibration (first-order accuracy × confidence ratings) using HMeta-d hierarchical Bayesian estimation (Fleming 2017) | ≥20 paired trials in-state |

**V5 scoring detail:**

meta-d′ estimated via HMeta-d (hierarchical Bayesian, Fleming 2017). Computed per
participant per condition (non-lucid REM, lucid REM, waking). Preregistered equivalence
bound: meta-d′ < 0.20 (absolute value), with BF₀₁ > 3 for the null, AND positive control
(waking meta-d′) exceeding 0.50, AND minimum 20 trials met.

If fewer than 20 trials: cell scored **open**, not absent.

If meta-d′ cannot be estimated (all-same-confidence responses): cell scored **open**,
not absent, unless the response distribution passes a preregistered entropy check
(confirming responses were non-random and non-degenerate).

---

## 4. Positive Controls (Gate 1 — Locked)

Every cell scored "absent" requires its positive control to pass **in the same
participant, in the same session week**:

| variable | positive control | threshold |
|---|---|---|
| V1 PAS | Waking PAS rating of clearly visible stimulus = "clear" | Must register |
| V2 d′ | Waking discrimination d′ > 1.5 | Must exceed |
| V3 internal-state | Waking emotion categorization accuracy > 75% | Must exceed |
| V4 self/world | Waking own-name detection accuracy > 90% | Must exceed |
| V5 meta-d′ | Waking meta-d′ > 0.50 | Must exceed |
| Eye signal | Lucid dreaming eye-signal executed correctly | Must execute |

If ANY relevant positive control fails → ALL cells dependent on that probe scored
OPEN for that participant.

---

## 5. Null / Equivalence Criteria (Gate 1 continued — Locked)

A variable is scored **ABSENT** in non-lucid REM only when ALL conditions hold:

1. Probe demonstrated live in-state (in-state response recorded for ≥1 trial)
2. Positive control passed same participant, same session week
3. Equivalence test: TOST against smallest effect size of interest (SESOI =
   0.20 × waking value for meta-d′; SESOI = 0.20 × waking d′ for V2), with
   BF₀₁ > 3 for the null hypothesis
4. Replicated across ≥ 2 separate nights
5. Converging measure agrees: e.g., V5 absent on behavioral measure AND
   frontal-P300 absent on electrophysiological measure

If ANY condition fails: cell scored **UNDETECTED** (= open). Not absent. Not zero.
Open.

**p > 0.05 is never a floor.** Absence claims require equivalence testing, not
failure to reject.

---

## 6. Confound Battery (Gate 2 — Locked)

Measured every probe block:

| confound | measure |
|---|---|
| Arousal | EEG spectral power (delta/theta/alpha/beta ratios); heart rate from ECG channel |
| Attention | Probe-response latency variability; omission rate |
| Executive control | Response-switch cost within probe blocks |
| Confidence (non-type-2) | Mean raw confidence across all trials |
| Reportability | Post-awakening report completeness score (0–5 scale) |
| Memory | Delay between in-state event and awakening/report; dream recall fidelity |

No additional confounds may be added after data collection begins. Cells with missing
confound measures are scored OPEN.

---

## 7. Statistical Analysis Plan (Locked)

### 7.1 Primary Analysis — Variance Partitioning (§135.3)

Step 1: Linear mixed model:
```
consciousness_rating ~ arousal + attention + executive_control 
                     + confidence + reportability + memory
```

Step 2: Add depth term:
```
consciousness_rating ~ confounds + meta_dprime + recursive_confidence_correlation
```

Depth retained as explanatory candidate iff ΔR² significance (likelihood ratio test,
α = 0.05) AND Bayes factor BF₁₀ > 3.

### 7.2 Secondary Analyses

- Double dissociation: compare meta-d′ between non-lucid REM and matched-arousal
  waking (both at similar accuracy levels) — tests whether depth varies independently
  of performance
- P300 frontal-vs-parietal amplitude ratio as converging electrophysiological marker
  for V5 absence
- Per-participant meta-d′ forest plot with credible intervals

### 7.3 Multiple Comparisons

Primary hypothesis (V5 absent in non-lucid REM) tested at α = 0.05, one-tailed
(equivalence direction). All secondary analyses corrected via Benjamini-Hochberg FDR
at q = 0.05.

---

## 8. Outcome Patterns (Pre-Written Verdicts — Locked)

| pattern | observation (all gates passed) | verdict |
|---|---|---|
| **A** | V1 ✓ + V2 ✓ + V3 ✓ + V5 ABSENT (equivalence criteria met) | Recursive depth NOT necessary for conscious experience. H1-necessity challenged. Beautiful Loop depth-necessity challenged. Narrative-self dissociation confirmed at electrophysiological level. |
| **B** | V5 PRESENT + V1 absent/at-floor | Recursive monitoring NOT sufficient for conscious experience. Attacks H1-sufficiency. |
| **C** | Consciousness tracks depth transitions after confound partialling | Depth hypothesis STRENGTHENED (not proven — see §136.7) |
| **D** | Depth explains no unique variance after confounds | Depth construct WEAKENED — re-specify or abandon |

**Strongest permitted conclusion:** *"This result eliminates [X] as a [necessary/
sufficient] condition for conscious experience under the preregistered measurement
assumptions (Gates 1–3 passed)."*

**No outcome proves H1 or any theory** (§136.7).

---

## 9. Exclusions and Deviations (Locked)

1. Nights with insufficient REM (< 30 min total) excluded from primary analysis
2. Probe blocks contaminated by arousal (K-complex, EMG elevation) excluded
3. Any deviation from protocol logged with timestamp, description, and reason;
   affected trials/cells scored OPEN regardless of apparent result
4. Participants withdrawing after ≥1 night included for completed nights only
5. Data from participants failing > 2 positive controls across all sessions excluded
   entirely (probe-reliability failure, not consciousness finding)

---

## 10. Timeline

| phase | duration | deliverable |
|---|---|---|
| Ethics submission | 4 weeks | IRB approval |
| Pilot (N=2) | 2 weeks | Probe-liveness verification, timing optimization |
| Main collection (N=14) | 8 weeks | ≥12 completer datasets |
| Analysis (blinded coder) | 2 weeks | Unblinded results per locked plan |
| Report writing | 4 weeks | Manuscript draft per Ch.270 disclosure standards |

Total: approximately 20 weeks from ethics approval to manuscript draft.

---

## 11. What This Experiment Cannot Do

- Cannot prove subjective experience exists in dreaming (only measures functional
  markers correlated with it)
- Cannot prove H1 or any theory (No-Proving clause, §136.7)
- Cannot establish whether biology is necessary (that requires Series C designs)
- Cannot reach the identity claim ("generates" vs "is", §118) — that gap remains
  untouched by this design
- Cannot substitute for the artificial consciousness construction (§126) which tests
  sufficiency directly

It CAN eliminate recursive depth as a NECESSARY condition for conscious experience —
which would force both H1-minimal and Beautiful Loop to rebuild their necessity claims.
That elimination is worth the 20 weeks.

---

## 12. Researcher Commitments

- [ ] This document registered (OSF + timestamp) before any recruitment
- [ ] Analysis code written and tested on simulated data BEFORE collection
- [ ] Blinded scorer used for all post-awakening reports
- [ ] All deviations logged in real time
- [ ] Results reported regardless of direction
- [ ] Negative findings submitted for publication, not filed away
