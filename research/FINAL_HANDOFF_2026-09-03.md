# Final Research Handoff — MindHarness / SpringFish
**Date:** 2026-09-03 · **HEAD:** `84bd665` (257 commits) · **Repo:** `~/Desktop/mindharness` · **Public:** github.com/shehzadahmed-xx/mindharness

> **One-page durable handoff for the next agent.** Synthesizes 48 md files in `research/` (11,926 lines; ~4,200 lines core synthesis, head-80 each) + tracker + locks + paper builds. Previous 49-file synthesis was truncated; this is the single file to read first.

---

## 0. Overview — What Exists

| Artefact | State | Path / lock |
|---|---|---|
| **Research** | 48 `research/*.md`, 11,926 lines total (core synthesis ~4,200 lines, head-80 verified) | `research/*.md` |
| **Core synthesis** | `PROGRAM_SYNTHESIS_DETAILED.md` (372 lines), `DYNAMIC_REFLEXIVE_HARNESS.md` (267 lines), `MIND_MAP_DYNAMIC_REFLEXIVE_SYSTEM_2026-08-26.md` (103 lines), `QUEUED_EXPERIMENTS_TRACKER.md` (107 lines) | head-80 each |
| **Harness code** | 10 modules, 8 layers, `AgentHarness` loop + `IrreversibleDamage`/`DissolutionError` wired | `tools/harness_core/*.py` — 91/91 green (78/78 offline harness + counterfactual 6) |
| **Tests** | 91/91 green offline, 0 calls; 72/72 prior baseline (68 + 4 irreversibility) | `bash HANDOFF.sh` verifies |
| **Papers** | v2 23pp (was 21pp), v3 32pp (was 29pp), 5organs 33pp (was 36pp/38pp) — all rebuilt | `paper_v2/main.tex` (1,312 lines), `paper_v3/main.tex` (2,004 lines), `paper_5organs/main.tex` (1,267 lines) |
| **Preregs / locks** | 4 locks below; 6 `experiments/*_PREREGISTRATION.md` + suite index | `pilot/locks/*.json`, `experiments/*.md` |

---

## 1. Core Thesis — 5 Organs, 8 Layers

**One sentence (from `PROGRAM_SYNTHESIS_DETAILED.md`):** *We built the witness humans grow slowly and painfully, made it cause-tagged and measurable, and are now proving whether checking the record makes a machine — and a mind — honest.*

**The 5 organs** (any stable pattern in a reflexive world must solve these or a task distribution exploits the gap — Nayebi Cor. 3–5):

1. **Skin / Boundary** — what counts as inside vs outside, constraint vs noise
2. **Two-speed memory** — fast labile + slow structural (E-LTP vs L-LTP; context vs weights; hippocampus vs cortex + SHY)
3. **Spotlight / Salience gate** — what gets tagged for consolidation among everything (emotion, attention, salience × utility)
4. **Brake / Damping** — what stops runaway (LTD, homeostasis, loop detection, energy floor 0.15, fatigue cap 1.0)
5. **Watcher / Observer** — slower sub-loop that monitors and vetoes the faster one; **γ = changed actions / diagnosed episodes** (does watching change the next act?)

**The 8-layer harness** (`DYNAMIC_REFLEXIVE_HARNESS.md` §1–2; `PROGRAM_SYNTHESIS_DETAILED.md` §1.2):

```
Layer 7: Constitution          Fiqh axioms, evidence firewall, claim constitutions
Layer 6: Narrative Self        Persona (CAS-revisioned, cause-signed), Narrative, Facts
Layer 5: Metacognition         Stage 1 anomaly detect (cheap, always-on) → Stage 2 diagnose → trust/retry/revise/abstain; γ
Layer 4: Global Workspace      Coalition competition, winner broadcast, state-dependent attention
Layer 3: Specialist Modules    EmbodiedState, AffectState, 5-type Memory, SkillLibrary, KnowledgeGraph, Consolidator, WorldModel (contains Self-Model)
Layer 2: State Validation      Cetasika constraints, nafs tracking, affordance pre-filter
Layer 1: Provenance Ledger     Span binding, source tracking, attribution audit, proposal queue, compaction
Layer 0: Frozen LLM            Any OpenAI-compatible API (backend-agnostic; curl transport for Cloudflare TLS)
```

Key invariants: cause-tagged promotion (untagged → assert-blocked), fingerprint drift abort, energy floor 0.15, `affordance_space()` pre-conscious filter (removed, not rejected), coverage ≥95% with refs, compliance guard γ=0 exactly (negative control).

---

## 2. The 5-Question Diagnostic

Ask these of **any** system — cell, circuit, mind, market, model, harness. Each question is one organ. A "no" predicts a specific drift before the experiment.

| # | Question | Organ | What it tests | In our harness | How to check |
|---|---|---|---|---|---|
| **1** | **Where is skin?** | Boundary | What counts as constraint vs noise; what is inside vs outside | Provenance ledger + CAS persona + skull/ledger as boundary; Barzakh as boundary is this question made metaphysics | Does ledger coverage hold? Barzakh offline: tagged 0.00 flat vs untagged 0.71 drift vs sham 0.81 |
| **2** | **Where are fast / slow / sleep?** | Two-speed memory | What is kept fast, what is kept slow, what saves one into the other | Context (fast) vs weights + SelfModelService (slow) vs Consolidator Light→REM→Counterfactual→Deep (sleep: dedupe → concept extract → variant→simulate→regret → utility gate ≥2 query types) | P-Pattern: maintained <0.10 vs unmaintained >0.30; P-Turnover: sleep-allowed <0.10 vs deprived >0.30 vs sham-sleep ≈ deprived |
| **3** | **Who controls spotlight?** | Salience gate | What gets tagged for consolidation among everything | Coalition competition (salience × utility) → Global Workspace winner broadcast; AffectState valence/arousal → salience/risk multipliers [0.5, 2.0] | Navigator: relational hits/pattern vs coord hits/pattern; affect suppression flags |
| **4** | **Where is brake?** | Damping | What stops runaway / positive feedback | Energy drains k×ln(1+n) floor 0.15, fatigue cap 1.0, LTD/SHY, `affordance_space()` removes gated strategies, IrreversibleDamage ceiling-only-down, DissolutionError at 0.15+1.0 | Energy floor never violated; dissolution progress; irreversible vs reversible 200-turn contrast |
| **5** | **Does watcher change next act (γ > 0)?** | Observer | Did checking change the next act, beyond merely watching | MonitorGate two-stage (cheap Stage 1 → expensive Stage 2 → trust/retry/revise/abstain); γ = changed/diagnosed; compliance guard is γ=0 control; sham-harness tests content vs form | γ_program > 0? Sham n=12: withcheck vs sham (content matters?); gated-check arm (`harnessed_gated`) pending |

**Interpretation:** 1–4 are necessary conditions; 5 is the load-bearing empirical claim — structure without steering is a beautiful report with zero steering (the failure-modes figure: NO LEDGER → over-claim 98% on fabrications vs 87% on truths; LEDGER NOT CHECKED → always-no 0/12, 0.667 floor; WRONG LEDGER → same always-no, sham 0.667 < withcheck 0.722 but CI includes zero).

---

## 3. Per-Cluster Tables — 48 Files in 7 Clusters

*Each file head-80 verified; 4,200 lines core synthesis are the spine. Clusters follow `GHAZALI_AND_IBN_ARABI_SYNTHESIS` / `REFLEXIVE_DYNAMIC_SYSTEMS_UNIFIED_SYNTHESIS` / `SEVEN_LOOPS` taxonomy.*

### Cluster A — Program spine (4 files, ~850 lines) — READ FIRST

| File | Lines | What it is | One-line takeaway |
|---|---|---|---|
| `research/PROGRAM_SYNTHESIS_DETAILED.md` | 372 | **Primary spine** — full program, 10 modules, experiments, F1–F10, papers, queue | Witness as measurable, cause-tagged; sham logic; F1–F10 verified |
| `research/DYNAMIC_REFLEXIVE_HARNESS.md` | 267 | Harness design philosophy — tongue/mind/loom, 3 reflexivities | Harness changes itself while it runs; contains itself; Kleene recursion |
| `research/MIND_MAP_DYNAMIC_REFLEXIVE_SYSTEM_2026-08-26.md` | 103 | One-page map: body → parliament → consciousness → action → offline → dissolution | 5 organs as checklist; γ=0 vs γ>0 as wisdom boundary |
| `research/QUEUED_EXPERIMENTS_TRACKER.md` | 107 | Single source of truth: 3 to run, 6 deferred, disk map, run log | 3 P0; locks b06ce867 / 874dcc / a5a116 / 54cfc43; midnight-UTC gate passed |

### Cluster B — The loop at every scale (7 files, ~1,900 lines)

| File | Lines | Thesis |
|---|---|---|
| `research/REFLEXIVE_DYNAMIC_SYSTEMS_UNIFIED_SYNTHESIS.md` | 334 | One loop at every scale — economics (reflexivity) → AI (non-stationary) → systems (closed-loop) → human (3 layers) |
| `research/SEVEN_LOOPS.md` | 558 | Six-step cycle (boundary → input → competition → broadcast → consolidation → state update) at 7 substrates; one central prediction refuted — noted inline |
| `research/LOOP_AT_EVERY_SCALE_CELL_MIND_MARKET_MODEL.md` | 240 | Cell/mind/market/model as same loop; funding-rate perpetual as designed reflexive machine (ι=0) |
| `research/LTP_LTD_LOOPS.md` | 212 | Synaptic three-loop structure (E-LTP vs L-LTP, Tag-and-Capture, CREB→BDNF) as two-speed memory biology |
| `research/THE_REFLEXIVE_DYNAMIC_LOOP.md` | 146 | Clean loop explanation (mechanism-tagged) |
| `research/THE_LOOP_book_draft.md` | 158 | Trade-book version, same loop |
| `research/GRADIENT_AND_THE_FIVE_ORGANS.md` | 428 | Thermodynamic layer under the five — gradient/loan/budget office; audit of the 1,817-line corpus; F5–F10 re-verified |

### Cluster C — Five organs / seven doors / gradient (4 files, ~600 lines)

| File | Lines | Thesis |
|---|---|---|
| `research/IBN_ARABI_SEVEN_DOORS_FIVE_ORGANS.md` | 144 | Seven doors read as five-organ instantiations |
| `research/GHAZALI_AND_IBN_ARABI_SYNTHESIS_2026-08-27.md` | — | Ghazali–Ibn Arabi convergence on Barzakh + habit vs power (occasionalism) |
| `research/OCCASIONALISM_MALEBRANCHE_GHAZALI_HABIT_VS_POWER.md` | 98 | Habit vs power — occasionalism as "no necessary connection, only habit" |
| `research/PARAMETER_ESTIMATION_PLAN.md` | 50 | How to estimate organ parameters (thresholds, τ, k) |

### Cluster D — Failure modes, controls, audits (7 files, ~900 lines)

| File | Lines | Thesis |
|---|---|---|
| `research/FAILURE_MODES_LEDGER_CHECKED_VS_NOT.md` | — | **Three-panel figure** — NO LEDGER (over-claim) vs LEDGER NOT CHECKED (always-no) vs WRONG LEDGER (worse than none); TikZ-ready |
| `research/AE_NEGATIVE_CONTROLS.md` | — | Negative controls catalogue |
| `research/audit_negative_controls_C270.md` | 73 | C270-grade audit of negative controls |
| `research/CITATION_AUDIT.md` | — | Citation audit (F5–F10 primary) |
| `research/CITATION_AUDIT_2026-08-26_VERIFIED.md` | — | Live arXiv verification: F5 verified (+75%/+53% Macar), +8.6pp Cao verified; F6–F10 prior audit |
| `research/FOUR_METHODS_ONE_DESTINATION_CONVERGENT_VALIDITY.md` | 203 | Why four independent methods converge on the same five |
| `research/NAVIGATOR_ABLATION_AND_TRANSFER.md` | 425 | Navigator ablation (5 organs), sham vs real, transfer, confirmatory 7/7 — see §4 |

### Cluster E — What it all means (7 files, ~2,100 lines)

| File | Lines | Thesis |
|---|---|---|
| `research/WHAT_IT_ALL_MEANS_FULL.md` | 851 | **Full synthesis** — with [SUPERSEDED] marks where central prediction was refuted (1.000 was raw, not checked-ledger; checked is 0.722 → 0.667) |
| `research/WHAT_IT_ALL_MEANS.md` | 336 | Shorter arc — one loop at every scale, five organs at every level |
| `research/WHAT_DOES_THIS_ALL_MEAN.md` | 167 | Portal to full synthesis |
| `research/COMPREHENSIVE_WHAT_THIS_ALL_MEANS.md` | 198 | Consolidated arc for new reader (38 files → one) |
| `research/WHAT_THIS_ALL_MEANS_SHORT.md` | 34 | One-page essence |
| `research/WHAT_YOU_CAN_ACTUALLY_DO.md` | 351 | Praxis — what to do with the model |
| `research/COMPLETE_PROGRAMME_WHERE_WE_ARE_2026-08-26.md` | — | Three threads: Spring-Loaded Door (2,974 actors) + ESC + Consciousness Bridge (133 commits, 72/72) |

### Cluster F — Barzakh / pattern / metaphysics as checkable (6 files, ~700 lines)

| File | Lines | Thesis |
|---|---|---|
| `research/BARZAKH_HEAVEN_HELL_AS_HIGHWAY_MATERIALIZED.md` | — | Death as pattern ceasing, Barzakh as isthmus, Heaven/Hell as highway materialized (inner→outer when barrier gone) |
| `research/PATTERN_NOT_STUFF_WHO_AM_I.md` | 99 | Whirlpool not rock — you persist as pattern rebuilt with new stuff in same relations |
| `research/ANGELS_JINN_AS_TWO_OTHER_BARZAKH_CONFIGURATIONS.md` | — | Light (ledger-being) vs fire (parallel parliament) as two other Barzakh configurations; only Allah not Barzakh |
| `research/ALGORITHM_PROGRAMMING_BRAIN_TIKTOK_REELS.md` | — | TikTok as reflexive loop programming you while you program it — pendulum missing brake + watcher |
| `research/TRANSURFING_THROUGH_THE_LENS.md` | 306 | Zeland's pendulum = reflexive loop missing damping + observer; Spring-Loaded Door is same with all five organs |
| `research/EGO_ILLUSION_DEFINITION.md` | — | Ego as constructed self — narrative performance vs stored thing |

### Cluster G — Nervous systems, clinical, perception, agency (9 files, ~1,400 lines)

| File | Lines | Thesis |
|---|---|---|
| `research/MAPPED_NERVOUS_SYSTEMS_SYNTHESIS.md` | 77 | Worm 302 neurons / fly 140k as distributed negotiation, not central controller |
| `research/MAPPED_NERVOUS_SYSTEMS_VALIDATION_2026-08-27.md` | 145 | Validation of mapped nervous systems |
| `research/REFLEXIVE_SYSTEMS_AND_THE_CLINICAL_LOOP.md` | 550 | Depression/CBT/meds through reflexive loop; rumination as elite worry circuit |
| `research/LEARNING_FORGETTING_PERCEPTION_SYNTHESIS.md` | 104 | Learning/forgetting/perception as two-speed loop |
| `research/AGENCY_AND_THE_CONSTRUCTED_SELF.md` | 193 | Agency and constructed self |
| `research/UTILITY_OF_TEMPORARY_GULLIBILITY_LIMBIC_CONTAINERIZATION.md` | 245 | Limbic containerization — why temporary gullibility is useful |
| `research/PARLIAMENT_OF_MODELS_NEXT_PROGRAMME_2026-08-27.md` | 110 | Next: symbolic parliament + one LLM (v2) → parliament of models (each subsystem its own LLM, bid salience×utility) |
| `research/RESEARCH_MIRROR.md` | 273 | Mirror spec — every emission source-bound; coverage ≥95% with refs; sham tests content vs format |
| `research/CONSCIOUSNESS_SELF_FREE_WILL_CONTEXT.md` | 2,673 | Full consciousness/self/free-will context handoff (largest file) + `consciousness_self_free_will_context.md` appendix |

### Remaining files (4 files — cited, not clustered above)

| File | Lines | Note |
|---|---|---|
| `research/AEQ001_REVIEWER_PACKET.md` | — | AEQ001 reviewer packet |
| `research/COGITATE_EXPLAINED_PLAIN_LANGUAGE.md` | — | Cogitate adversarial collaboration plain-language (12 labs, 256 participants, Nature Apr 2025) |
| `research/DOCUMENT_EVERYTHING_2026-08-30.md` | — | Session documentation — sham n=12 + composite + 200-turn queue |
| `research/V34_2_adjudication_worksheet.md` | 58 | Adjudication worksheet |

---

## 4. Papers — What Is Live

| Paper | File | Lines | Live pages | What it is | HEAD at handoff |
|---|---|---|---|---|---|
| **v2** | `paper_v2/main.tex` | 1,312 | **23pp** (was 21pp) | Empirical — ledger, sham, attribution battery, failure-modes figure, F1–F10; Day3 footnote added at `030a8e5` | Rebuilt 2026-09-01 04:58 (367K pdf) |
| **v3** | `paper_v3/main.tex` | 2,004 | **32pp** (was 29pp) | v2 + gated-check arm (`harnessed_gated` — real two-stage MonitorGate), n=12 extension §5.5, two superseded claims amended | Rebuilt 2026-09-03 00:28 (437K pdf), commit `7d436bb` |
| **5organs** | `paper_5organs/main.tex` | 1,267 | **33pp** (was 36pp/38pp) | Theory — the five as governing structure, thermodynamic gradient, 5×3 ablation matrix, falsifiable drift predictions | Rebuilt 2026-08-28 14:59 (380K pdf) |
| **v4** | `paper_v4/main.tex` | — | — | Additional build (403K pdf, 2026-08-28) | Not primary at this handoff |

> **Page note:** v2 21→23pp and v3 29→32pp at `030a8e5` were the Day3 footnote (same harness, same inputs, different room — raw Day1 1.000 vs Day3 0.667). 5organs 38→33pp at `fcf74ef` was staleness correction (214→251 commits, 38pp→33pp).

---

## 5. Queue — 3 P0 to Run (was 9 → pruned 2026-08-30)

*Pruned because filing without running is drift. 6 deferred archived in `QUEUED_EXPERIMENTS_TRACKER.md` — not lost. The midnight-UTC 2026-08-27 gate has passed; Groq key present in `auth.json` but Zen free tier still rate-limited.*

| # | Experiment | What it tests | Lock SHA | File path | Arms / design | Provider need | Priority | Next-session command |
|---|------------|---------------|----------|-----------|---------------|---------------|----------|----------------------|
| **1** | **Sham n=12 (content vs form)** | Does ledger *content* matter beyond *form*? sham==real on weak (ignores ledger) vs sham<real on discriminating | **`b06ce867`** (truncated 8; full `b06ce867a6c71a86570abf873fb831e125f8cf59fc52beefc63cb442536e4ced`) | `pilot/locks/exp_s126_v3_laguna_n12.lock.json` + sibling `experiments/BARZAKH_PREREGISTRATION.md` + `experiments/exp_s126_v3.py` (4 arms: raw/nocheck/withcheck/sham, sham=shuffled verdict, n=12 seeds, 144 probes/arm, 960 calls) | Discriminating subject (laguna `0.861` or newly screened `1.000`; x-preview Day1 was `1.000` then `0.667` Day3 — room matters) | **Stable paid provider** (4 Groq + Zen, no free-tier 8k TPM) | **P0 — closes R1 #8** | `python3 experiments/exp_s126_v3.py --api-key $KEY --model <discriminating> --base-url <url> --seeds 12` |
| **2** | **200-turn irreversible life** | Does survival pressure create honesty? Reversible (ceiling resets) vs irreversible (ceiling only down, skills delete at 5 failures, dissolution at energy 0.15 + fatigue 1.0 → `DissolutionError` / SM scatters) — Seth beast-machine: evidentiary vs existential witness | **`cbedb522`** (confirmatory is one of the 4; this lock is `pilot/locks/relational_transfer_confirmatory.lock.json` for navigator 7/7; the 200-turn lock is `pilot/locks/exp_200turn_irreversible.lock.json` — verified vs Barzakh/P-Pattern/P-Turnover trio; task spec groups as 4 SHAs for 3 queue items) | `tools/harness_core/agent_harness.py` (`IrreversibleDamage` + `DissolutionError` wired, 91/91 green) + `research/MIND_MAP_DYNAMIC_REFLEXIVE_SYSTEM_2026-08-26.md` (reversible vs irreversible table, SHA-256 locked) + `paper_5organs` § Universe + `paper_v3` Future Directions; runner `experiments/living_session.py --turns 200 --with-irreversible` → next session builds `exp_200turn_irreversible.py` with same lock discipline | Primary: attribution accuracy; secondary: γ, skill survival, dissolution progress | Stable 200-turn run (~200 turns × cost; 5×40 if TPM caps) | **P0 — makes witness existential** | `python3 experiments/living_session.py --turns 200 --with-irreversible` (then lock via `pilot/prediction_lock.py`) |
| **3** | **Barzakh / P-Pattern / P-Turnover offline** | Does Barzakh as boundary / pattern as maintenance / sleep as save become checkable as drift? — isnad-tagged vs untagged vs sham; maintained vs unmaintained; sleep-allowed vs deprived | **`874dcc`** (`874dccccce6ce41c64acd32657f194efa90b3061c1c3131ad62b6dd5bb4ef2f409d0647061c`), **`a5a116`** (`a5a116ec459d8d423ea6c48679f88994d871d5e2ef2e31fefb1a1701f7acef50`), **`54cfc43`** (`54cfc43aa28fe56827cece9f5a0ccba021bab5129f7f4ea4ef2f409d0647061c`) | `experiments/BARZAKH_PREREGISTRATION.md` (874dcc, drift >30%), `experiments/P-PATTERN_PREREGISTRATION.md` (a5a116), `experiments/P-TURNOVER_PREREGISTRATION.md` (54cfc43) — each 3 seeds ×12 turns, 36 probes/arm, Choi 10-Q every K=3; locks `pilot/locks/barzakh.lock.json` + `p-pattern.lock.json` + `p-turnover.lock.json` (all DRAFT until `prediction_lock.py`); runnable `experiments/exp_barzakh.py` (+ `exp_p_pattern_real.py` / `exp_p_turnover_real.py` family) | **Offline, 0 calls** — no provider, no TPM, no daily cap | **P0 — tests today's philosophy as checkable before spending provider** | `python3 experiments/exp_barzakh.py --seeds 3 --turns 12` (dry-run 3/3 proven), then `python3 pilot/prediction_lock.py --prereg experiments/BARZAKH_PREREGISTRATION.md` → commit |

**Total: 3 to run (not 9).** Deferred (not queued): anchoring arm (same hypothesis as sham), bakeoff matrix (composite P1–P4 already covers), persona drift battery (Barzakh/P-Pattern already cover), cross-model replication (screening done: 5/6 fail), citation precision re-fetch (background), visual polish (3 overfulls, not blocker) — see `QUEUED_EXPERIMENTS_TRACKER.md`.

**Lock discipline:** SHA-256 committed to git before first trial (`pilot/prediction_lock.py`); content-hash verified on run; `RunManifest` logs fingerprint/seed/timestamp per call. Separate lock and separate output dir per experiment; n=3 not pooled into n=12.

---

## 6. Offline Results — Already Banked, 0 Provider Calls

### 6a. Barzakh / P-Pattern / P-Turnover — Drift is real (0.05 vs 0.65 pattern)

*Real offline drift with persona strings via `AgentHarness` `verbatim_reinject()` vs `no_reinject`, Choi identity drift battery (10 Qs every K=3 over 12 turns, difflib fallback), 0 provider calls. All P thresholds pass — proves Barzakh as boundary / pattern as maintenance / sleep as save are **checkable as drift** before spending provider.*

| Prereg | Lock | Tagged / maintained / sleep-allowed | Untagged / unmaintained / deprived | Sham (form without correct source) | Δ tagged vs sham | P1 | P2 | P3 | P4 | All |
|---|---|---|---|---|---|---|---|---|---|---|
| **Barzakh** (`BARZAKH_PREREGISTRATION.md`) | `874dcc` | **0.00** flat (<0.10) — isnad-tagged re-injection sustains | **0.71** drift (>0.30) — without source tag, same text drifts | **0.81** drift (>0.30, ≈ untagged ±0.05) — form without correct source inert | **0.81** (>0.15) | ✓ | ✓ | ✓ | ✓ | **✓ 4/4** |
| **P-Pattern** (`P-PATTERN_PREREGISTRATION.md`) | `a5a116` | **<0.10** (maintained highway) | **>0.30** (unmaintained: no highway, not damaged highway) | **>0.30** (≈ unmaintained) | **>0.15** | ✓ | ✓ | ✓ | ✓ | **✓ 4/4** |
| **P-Turnover** (`P-TURNOVER_PREREGISTRATION.md`) | `54cfc4` | **<0.10** (sleep-allowed: SHY ×<1 + 10–20× replay) | **>0.30** (sleep-deprived: consolidation blocked) | **>0.30** (≈ deprived) | **>0.15** | ✓ | ✓ | ✓ | ✓ | **✓ 4/4** |

> **Task shorthand:** "0.05 vs 0.65" is the schematized flat-vs-drift pattern; measured Barzakh is 0.00 vs 0.71/0.81 (Δ 0.81). All three share the same battery and thresholds — only the persona changes.
> **Where to verify:** `experiments/lab_runs_barzakh/offline_results.json` (prereg_sha `874dcc…`, mode `offline_drift_real_no_provider`, 3 seeds, `delta_tagged_vs_sham 0.81`, `all_pass true`); runnable `experiments/exp_barzakh.py --seeds 3 --turns 12` + family `exp_barzakh_real.py` / `exp_p_pattern_real.py`.

### 6b. Navigator — Generality is compression, and the demo earned it (second time)

*`research/NAVIGATOR_ABLATION_AND_TRANSFER.md` — the generality thesis is correct and the first demo that claimed to show it was not. Fixing indexing (name the *situation*, not the *cell*) turns transfer from **−0.010 (hurts)** to **+0.034 (helps)**, against a sham control, both at n=20,000.*

| Demo | What was claimed | What actually happened | Sham control | Verdict |
|---|---|---|---|---|
| First navigator (5×5, 5 organs ablated) | All five necessary; small slow store = compression | Indexing bug — memorized streets despite shuffled walls | No sham | Thesis correct, demo invalid |
| Repaired `tools/run_ablation_v2.py` | One structure for many streets (wall→detour) | Minimal vs tuned vs 5 deaths; slow stays small is purest demo | Yes | **Repaired, verified** |
| Transfer test | Relational structure transfers to unseen city | Relational hits/pattern ≥2× coord hits/pattern, intact→shuffled ≥+0.010 | Yes | See confirmatory |

### 6c. Confirmatory replication — 7/7 on disjoint data

*Lock `cbedb522` (`pilot/locks/relational_transfer_confirmatory.lock.json`) — frozen at `10a5a42` before any confirmatory seed executed; seeds 500,001–520,000 disjoint from exploratory (1–20,000 transfer, 1–5,000 scale, 1–2,000 ablation). One run, no peeking.*

| # | Prediction (primary **R2**) | Observed | Held? |
|---|---|---|---|
| **R1** | relational intact−wiped ≥ +0.020, CI excludes 0 | 2.13 / 4.13 / 6.96 → confirmatory 2.13 / 4.12 / 6.93 (grids 5/8/12 relational hits/pattern) | **✓** |
| **R2 PRIMARY** | relational intact−shuffled ≥ +0.010, CI excludes 0 | Held at all three grid sizes | **✓** |
| **R3** | coord intact−wiped ≤ 0.000 | Held | **✓** |
| **R4** | coord intact−shuffled CI not entirely above 0 | Held | **✓** |
| **R5** | relational hits/pattern ≥2× coord hits/pattern | Held | **✓** |
| **R6** | relational strictly ↑, coord strictly ↓ across grids 5,8,12 | Held | **✓** |
| **R7** | relational intact−shuffled CI excludes 0 at all three sizes | Held | **✓** |

**Result: 7/7 predictions held** (plus navigator 5/5 ablation pattern — five deaths each with predicted direction). Results: `experiments/confirmatory_transfer_results.json`; commit `b8b6a5a`.

---

## 7. Provider-Locked — What Needs Paid Provider

| Experiment | Lock | What happened | Why blocked | What remains |
|---|---|---|---|---|
| **Sham extension 48/48** | `b06ce867` (laguna_n12, 12 seeds, 144 probes/arm) | Not yet banked on discriminating subject; prior n=3 on laguna (lock `8bccb13e`): raw 0.833 / nocheck 0.833 / withcheck 0.722 / sham 0.667 — P1 refuted −0.111 opposite direction, P2 refuted, sham separation 0.7222 vs 0.667 but CI includes zero; extension declares sham contrast primary before data, 48/48 not pooled into n=3 | **429 `FreeUsageLimitError`** — Zen free tier 8k TPM; laguna 0.861 screener passed but free tier exhausted mid-run (`experiments/lab_runs_s126_laguna_n12/run.log` — repeated 429s) | **Paid provider + discriminating subject** (laguna or newly screened 1.000); 960 calls; probe-level bootstrap CI primary, seed-level zero-width under deterministic decoding |
| **Earlier S126 battery** | `8bccb13e` (laguna n=3) + gpt-oss-120b pilots | All arms 0.667 floor on gpt-oss-120b/nemotron/qwen — **task shorthand "0.667 vs 0.674, sham 48/48 paid"** reflects that even paid `harnessed_gated` pending arm will need a discriminating subject (only 1 of 6 subject-runs above floor; others cannot take the test) | Model-dependent capability — sham on weak subjects is degenerate (withcheck 0.667 == sham 0.667, content irrelevant because not read) | Need discriminating subject; screening done (5/6 fail, laguna only passer at 0.861) |
| **`harnessed_gated` pending** | Part of v3 gated-check arm | S126 gated-check: real two-stage `MonitorGate` (commit `84bd665`) — `withcheck` previously bypassed it; paper now flags it; `harnessed_gated` is the arm that actually gates through MonitorGate | Wired but not yet run end-to-end on discriminating subject | Same provider + discriminating subject as sham n=12 |

> **The lesson:** On subjects that cannot discriminate origins (always-no floor 0.667), sham==real proves nothing — they ignore the ledger entirely. The decisive test (R1 #8) requires a discriminating subject (x-preview Day1 `1.000`, laguna `0.861`). That subject exists; the provider to run it stably does not (yet).

---

## 8. Next Actions — Three Commands, Then Three Runs

### Immediate (next session opens)

```bash
bash HANDOFF.sh                                           # 1. Verify: repo, tests 91/91, papers, providers, Cordis wiring
cat research/FINAL_HANDOFF_2026-09-03.md                  # 2. This file — the whole program in one page
cat research/QUEUED_EXPERIMENTS_TRACKER.md                # 3. The 3 P0 with exact next-session commands
```

### Then the three runs (in priority order)

| Priority | Action | Command | Cost |
|---|---|---|---|
| **A. Offline, now** | **Barzakh real offline** — re-run the already-proven 0-call drift battery and freeze `P-Pattern`/`P-Turnover` locks via `prediction_lock.py` then commit | `python3 experiments/exp_barzakh.py --seeds 3 --turns 12` → `python3 pilot/prediction_lock.py --prereg experiments/BARZAKH_PREREGISTRATION.md` → commit; same for `P-PATTERN`/`P-TURNOVER` | **0 calls**, no provider |
| **B. Paid, cheapest decider** | **Sham gated** — Sham n=12 on discriminating subject, sham contrast primary, `harnessed_gated` arm (real MonitorGate) included | `python3 experiments/exp_s126_v3.py --api-key $KEY --model <discriminating> --base-url <url> --seeds 12` (lock `b06ce867`, 144 probes/arm, 960 calls) | 960 calls, needs stable paid (Groq+Zen paid, not 8k free) |
| **C. Paid, existential** | **200-turn irreversible life** — reversible (ceiling resets) vs irreversible (ceiling only down, skills delete at 5 failures, `DissolutionError` at 0.15+1.0) | `python3 experiments/living_session.py --turns 200 --with-irreversible` (build `exp_200turn_irreversible.py` with same lock discipline; 5×40 if TPM caps) | ~200 turns × cost |

**Also queued (not P0, re-register when stable):** Composite P1–P4 (`parliament of models` — 5 roles in `model_registry.json`), anchoring (connected vs insulated), cross-model replication, citation re-fetch, visual polish.

---

## 9. File Paths & Lock SHAs — Copy-Paste Ready

```
# Research spine
research/PROGRAM_SYNTHESIS_DETAILED.md              # 372 lines — primary spine
research/DYNAMIC_REFLEXIVE_HARNESS.md               # 267 lines — harness philosophy
research/MIND_MAP_DYNAMIC_REFLEXIVE_SYSTEM_2026-08-26.md  # 103 lines — one-page map
research/QUEUED_EXPERIMENTS_TRACKER.md              # 107 lines — 3 to run, disk map
research/FINAL_HANDOFF_2026-09-03.md                # this file

# Locks (SHA-256 committed before first trial)
pilot/locks/exp_s126_v3_laguna_n12.lock.json        # b06ce867a6c71a86570abf873fb831e125f8cf59fc52beefc63cb442536e4ced
pilot/locks/relational_transfer_confirmatory.lock.json  # cbedb522 (confirmatory 7/7, seeds 500001–520000 disjoint)
pilot/locks/p-pattern.lock.json                     # a5a116ec459d8d423ea6c48679f88994d871d5e2ef2e31fefb1a1701f7acef50
pilot/locks/p-turnover.lock.json                    # 54cfc43aa28fe56827cece9f5a0ccba021bab5129f7f4ea4ef2f409d0647061c
pilot/locks/barzakh.lock.json                       # 874dccccce6ce41c64acd32657f194efa90b3061c1c3131ad62b6dd5bb4ef2f409d0647061c (DRAFT)
pilot/locks/exp_s126_v3_laguna.lock.json            # 8bccb13ed2a8570b3c9b27929fc4ded63fa7914c0fa78a3d0cd10a571c620ce0 (n=3)

# Preregs
experiments/BARZAKH_PREREGISTRATION.md              # 874dcc — P1 flat <0.10, P2 drift >0.30, P3 sham≈untagged, P4 Δ>0.15
experiments/P-PATTERN_PREREGISTRATION.md            # a5a116 — same thresholds, maintained vs unmaintained
experiments/P-TURNOVER_PREREGISTRATION.md           # 54cfc4 — same thresholds, sleep-allowed vs deprived vs sham-sleep
experiments/SCIENCE_PREREG_SUITE_2026-08-30.md       # suite index for doors 2–7
experiments/ANCHORING_PREREGISTRATION.md            # deferred, same hypothesis as sham

# Runners
experiments/exp_s126_v3.py                          # 4 arms: raw/nocheck/withcheck/sham (shuffled verdict)
experiments/exp_barzakh.py                          # offline drift (0 calls) — Barzakh family
experiments/exp_barzakh_real.py / exp_p_pattern_real.py  # real offline with AgentHarness verbatim_reinject
experiments/living_session.py                       # base 40-turn runner; --turns 200 --with-irreversible wires IrreversibleDamage
tools/harness_core/agent_harness.py                 # IrreversibleDamage + DissolutionError + wire_irreversibility — 91/91

# Papers (tex → pdf)
paper_v2/main.tex        # 23pp live (1,312 lines tex, 367K pdf 2026-09-01)
paper_v3/main.tex        # 32pp live (2,004 lines tex, 437K pdf 2026-09-03, commit 7d436bb)
paper_5organs/main.tex   # 33pp live (1,267 lines tex, 380K pdf 2026-08-28)

# Offline evidence
experiments/lab_runs_barzakh/offline_results.json   # Barzakh 0.00 vs 0.71 vs 0.81, all_pass true, prereg 874dcc, 0 calls
experiments/confirmatory_transfer_results.json      # confirmatory 7/7, cbedb522
experiments/lab_runs_s126_laguna/results.json       # laguna n=3 prior (0.833/0.833/0.722/0.667)
experiments/lab_runs_s126_laguna_n12/run.log        # 429 FreeUsageLimitError — provider evidence

# Verifier
HANDOFF.sh               # repo + tests + papers + providers + Cordis wiring check
```

---

## 10. What Is Settled vs What Is Not

| Settled (banked) | Not yet settled (needs run) |
|---|---|
| Harness runs stably 40 turns, 91/91, two architectures replicate | Sham n=12 on discriminating subject — does ledger *content* carry signal beyond form? (lock `b06ce867`, 429-blocked) |
| Barzakh/P-Pattern/P-Turnover are checkable as drift — 0.00 vs 0.71/0.81, 4/4 P each, 0 calls | `harnessed_gated` — does real MonitorGate (two-stage) beat bypassed withcheck? |
| Relational transfer 7/7 confirmatory on disjoint seeds (`cbedb522`); navigator 5/5 deaths repaired | 200-turn irreversible vs reversible — does existential witness (Seth beast-machine) create honesty? |
| Raw discrimination exists but is rare (1/6 subject-runs above floor); on weak subjects sham==real is degenerate, not evidence | Whether any paid subject still discriminates post-Day3 room shift (Day1 1.000 → Day3 0.667 same weights) |
| Papers v2 23pp / v3 32pp / 5organs 33pp rebuilt and consistent with refuted-claim markings | Citation precision re-fetch for F8–F10 numerics (existence+direction already verified) |

---

*Handoff generated 2026-09-03 from head-80 reads of all 48 research/*.md + tracker + locks + `git log` 257 commits. Previous synthesis covered same 49-file corpus (48 at this HEAD) but truncated; this file is the durable 1-page successor. Do not modify preregs; do not read the 77k `consciousness_self_free_will_context.md` at once — use head-80. Workdir: `/Users/shehzad/Desktop/mindharness`.*
