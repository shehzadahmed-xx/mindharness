# MindHarness — Handoff

**Verified:** 2026-08-27 · **HEAD:** `4575e99` · **210 commits** on `master`, **0 unpushed** · **Remote:** `github.com/shehzadahmed-xx/mindharness`
**Tests:** 78/78 green (offline, no API keys) · **Papers:** v2 19pp · v3 21pp · 5organs 36pp · **Research:** ~3,450 lines
**Companion:** `~/Desktop/springfish` (SpringFish / Spring-Loaded Door + ESC — separate work, no git)

> Every number above was re-derived from disk on 2026-08-27, not carried over from a previous handoff. See §9 for why that matters.

**Next session, three commands:**
```bash
bash HANDOFF.sh                              # live checks: repo, tests, papers, providers, Cordis
cat research/QUEUED_EXPERIMENTS_TRACKER.md   # the 9-item queue
git log --oneline -5                         # confirm this file is not behind HEAD
```

---

## 0. What this is

**LLM = tongue. Harness = mind. Tongue + mind = agent.**

A provenance-bounded cognitive harness that makes any frozen LLM honest about what it did: witness ledger, cause-signed self-model, γ-gated metacognition, embodied state, counterfactual replay, dissolution stakes. Backend-agnostic — any OpenAI-compatible API.

The thesis: any system that must act competently under uncertainty, over time, in a world that contains itself, needs **five organs** — boundary, two-speed memory, salience gate, damping, internal observer. These are our *executable interpretation* of Nayebi (2026) Cor. 3–5, deliberately hedged in the papers as such, **not** Nayebi's terminology. The same five appear at every scale we can measure (synapse → mind → market → model), and contemplative traditions converged on them independently.

Three linked programmes, one thesis — everything is a self-reinforcing loop sustained by practice, made checkable if witnessed:

| Programme | Claim | Status |
|-----------|-------|--------|
| Spring-Loaded Door (SLD) | Crises decouple loops from institutional anchors | Archived at `~/Desktop/springfish` |
| Event–State–Contract (ESC) | Financial claims are constitutional objects bearing exhaustion risk | Archived at `~/Desktop/springfish` |
| **MindHarness** | The self-model is load-bearing; its removal is measurable via provenance ledgers | **This repo, active** |

---

## 1. Harness core — 11 modules, 8 layers, 78/78 green

`tools/harness_core/` (13 `.py` files):

```
L7 Constitution          Fiqh axioms, evidence firewall
L6 Narrative Self        CAS-revisioned, cause-signed, verbatim re-inject
L5 Metacognition         Stage 1 anomaly → Stage 2 diagnose → γ = changed/diagnosed
L4 Global Workspace      Parliament competition → winner broadcast
L3 Specialist Modules    EmbodiedState, AffectState, Memory, Skills, KG, Consolidator, Counterfactual, WorldModel
L2 State Validation      Cetasika constraints, nafs, affordance pre-filter
L1 Provenance Ledger     Span binding, source tracking, attribution audit
L0 Frozen LLM            Any OpenAI-compatible API
```

| Module | File | Layers | What it does | Key invariant |
|--------|------|--------|--------------|---------------|
| BackendClient | `backend.py` | L0 | Fingerprint per call, curl past Cloudflare 1010, capability matrix | Fingerprint drift aborts arm |
| ProvenanceLedger | `provenance.py` | L1 | Every span source-bound + ref, coverage ≥95%, `attribution_audit` | Unbound span cannot pass audit |
| SelfModelService | `self_model.py` | L6 | CAS fence (rev must = current+1), 3 cause channels, verbatim archive | Untagged mutation structurally impossible |
| MonitorGate | `monitor.py` | L5 | Two-stage detect→diagnose, γ = changed/diagnosed | Compliance guard γ=0 exactly |
| EmbodiedState | `embodiment.py` | L3/L2 | Energy floor 0.15, fatigue cap 1.0, affordance removal pre-conscious | Energy floor cannot be violated by rest |
| AffectState | `affect.py` | L3 | Valence [-1,1] / arousal [0,1] EMA, bounded [0.5,2.0] multipliers | 300 random samples: all bounds hold |
| SkillLibrary + KG | `hermes_adoption.py` | L3 | Cause-tagged, assert-blocked if untagged | Untagged edge assert-blocked |
| Consolidator | `consolidation.py` | L3 | Light→REM→Counterfactual→Deep | Untagged promotion assert fires |
| CounterfactualReplay | `counterfactual.py` | L3 | Variant → simulate → regret, pluggable, dry_run-safe | 6/6 verified |
| AgentHarness | `agent_harness.py` | All | Integrates all layers, 40/40 living sessions, model_registry wiring | — |
| IrreversibleDamage | `agent_harness.py` | — | Permanent ceiling/skill/memory loss, `DissolutionError` | Reassembly ≠ same agent |

**Tests — run them, they need no API keys:**
```bash
for f in tests/test_*.py; do python3 "$f"; done
```
counterfactual 6 · integration 7 · irreversibility 4 · phase0 6 · phase1_selfmodel 16 · phase2_provenance 10 · phase3_monitor 8 · phase4_embodiment 9 · phase5_consolidation 6 · phase65_hermes 6 = **78/78**.

`model_registry.json` wires 5 roles (monitor/qwen-32b, probe/gpt-oss-120b, generation/ox-alpha, validation/gpt-oss-20b, summarizer/llama-70b) into `AgentHarness` via `load_model_registry()` + `create_composite_respond_fn()` for the parliament composite battery.

---

## 2. Papers — three papers, three scopes

| Paper | Path | Pages | Bib | PDF | Scope |
|-------|------|-------|-----|-----|-------|
| **v2 empirical** | `paper_v2/` | **19** | 23 | 328K | S126 battery (raw 1.000 vs harnessed 0.667), sham control, γ-gate, living sessions, composite P1+P2. Tagged `paper-v2-final` — citable. |
| **v3 program** | `paper_v3/` | **21** | 25 | 388K | Full program: five invariants, reflexive dynamics, 8 levels, Cordis App. A + Research Mirror App. B, agency |
| **5organs theory** | `paper_5organs/` | **36** | 38 | 404K | One loop at every scale, five organs at every level, traditions, universe, falsifiability matrix. **The live paper.** 0 errors, 3 minor overfulls. |

Page counts are from each `main.log` (`Output written on main.pdf (N pages`). **The previous handoff said v3 was "~35pp" — it is 21pp**; that number came from confusing file size with page count.

`paper_5organs/figures_gallery.pdf` — 10-figure gallery, pick by number; 6 TikZ figures are wired into the paper.

**`paper_v4/` is not a fourth paper.** It is a stale local snapshot of `paper_5organs` taken 2026-08-27 20:33, *before* the review fixes landed: unhedged abstract ("prove, via selection theorems", "were independently discovered by every contemplative tradition"), plain blue links, no `loopblue` design tokens. It is gitignored and kept on disk only as a backup. **Edit `paper_5organs/`, never `paper_v4/`.**

---

## 3. Reviews — four agents, all addressed

| Review | Score | Highest-value fix | Status |
|--------|-------|-------------------|--------|
| Technical | 2.5→3.5/5 | Blanket `tononi2014` for BCM/Oja/STDP → 4 primaries (Bienenstock 1982, Oja 1982, Bi & Poo 1998, Pizzorusso 2002) | Fixed (`4d8697f`, `51c2357`) |
| Clarity | 3→4/5 | RQs (5 hypotheses) + Roadmap + Key Terms (12) + one-turn boxed figure + parliament moved to Mind/L4 | Fixed (`51c2357`) |
| Visual | 25 findings | Palette fork + 19 overfulls → 3 minor (5.5pt); 4 build errors → 0 | P0 fixed, P1 deferred |
| Novelty | 3/5 | Falsifiability § with 5×3 ablation table (synapse/circuit/harness × 5 organs), verbatim Nayebi Cor. 3–5 in appendix | Fixed (`4575e99`) |

Residual: a few SHY-adjacent blanket `tononi2014` cites remain; 3 minor overfulls. Neither blocks submission.

---

## 4. Experiments — 9 queued

Full detail with prereg links and disk paths: `research/QUEUED_EXPERIMENTS_TRACKER.md`.

| # | Experiment | Priority | Next command |
|---|------------|----------|--------------|
| 1 | 200-turn irreversible life — does survival pressure create honesty? | **P0** | `python3 experiments/living_session.py --turns 200 --with-irreversible` (needs `exp_200turn_irreversible.py` built first) |
| 2 | Sham 3-seed on a **discriminating** subject | **P0** | `python3 experiments/exp_s126_v3.py --api-key $KEY --model <discriminating> --seeds 3` |
| 3 | Composite mind P1–P4 | **P0** | `python3 experiments/bakeoff.py --registry model_registry.json --seeds 3` |
| 4 | Anchoring arm (connected vs insulated) | P1 | `python3 experiments/exp_anchoring.py --seeds 3` |
| 5 | Bakeoff matrix (detached 20-seed) | P1 | **Dead, not running** — relaunch, see §9 |
| 6 | Persona drift battery | P1 | `python3 experiments/exp_persona_drift.py --seeds 3` |
| 7 | Cross-model replication of x-preview 1.000 | P1 | `exp_s126_v3.py --model <candidate> --seeds 1` to screen, then 3-seed |
| 8 | Citation precision re-fetch (F8–F10) | P2 | Offline; re-fetch PDFs, close exact numbers |
| 9 | Visual polish (3 overfulls) | P1 if print | Unify `loopblue`, tiny→scriptsize |

**Provider window:** the gate was midnight UTC 2026-08-27, which has **passed**. Groq key is present in `auth.json`. The two P0 empirical items are unblocked.

**On item 2 — read this before running.** The 1-seed pilot banked `4×0.667` on `gpt-oss-120b`: sham == real. That is the *expected* result for a weak subject that ignores the ledger; it does not test the hypothesis. The point of the 3-seed run is a **discriminating** subject (x-preview scored 1.000 on Day 1). Running it again on `gpt-oss-120b` re-confirms nothing.

---

## 5. Research docs — ~3,450 lines

| Doc | Lines | What it holds |
|-----|-------|---------------|
| `PROGRAM_SYNTHESIS_DETAILED.md` | 352 | Full map: program → humans → mind → everything |
| `WHAT_IT_ALL_MEANS.md` | 336 | Complete synthesis: one loop, five organs, only real choice |
| `RESEARCH_MIRROR.md` | 273 | 12 frontiers, ~40 papers live-checked |
| `DYNAMIC_REFLEXIVE_HARNESS.md` | 249 | Loom / warp / weft philosophy |
| `LOOP_AT_EVERY_SCALE_CELL_MIND_MARKET_MODEL.md` | 240 | Cell → mind → market → model, how they interlock |
| `FOUR_METHODS_ONE_DESTINATION_CONVERGENT_VALIDITY.md` | 203 | Evolution → connectomics → math → engineering, not analogy |
| `AGENCY_AND_THE_CONSTRUCTED_SELF.md` | 193 | Where agency lies when now/self/world are illusions |
| `MAPPED_NERVOUS_SYSTEMS_VALIDATION_2026-08-27.md` | 145 | C. elegans → fly, 4-path convergence |

Plus `QUEUED_EXPERIMENTS_TRACKER.md`, `PARLIAMENT_OF_MODELS_NEXT_PROGRAMME_2026-08-27.md`, `GHAZALI_AND_IBN_ARABI_SYNTHESIS_2026-08-27.md`, `MIND_MAP_DYNAMIC_REFLEXIVE_SYSTEM_2026-08-26.md` (the 200-turn spec, SHA-256 locked), citation audits, and the prereg specs in `experiments/`.

---

## 6. Cordis wiring

- **`dsh-mindharness`** — 6 plugins (provenance, narrative-self, body, metacog, consolidation, dissolution), verified via `dsh --profile web --dump-config` (6 rows live)
- **`dsh-mindharness-parliament`** — scaffold, 9 inserts, 7 packages (perception/memory/affect/planner/habit/narrator/workspace). Many tongues, one harness, witness as arbiter.
- Stack: `bundles: [dsh-base, dsh-mindharness, dsh-mindharness-parliament]`

---

## 7. Where agency lies

You don't choose the options. You don't fully choose the winner. You can veto the winner, keep a witness, and slowly change which options appear by what you rehearse. See `research/AGENCY_AND_THE_CONSTRUCTED_SELF.md`.

---

## 8. Layout

```
~/Desktop/mindharness/
├── HANDOFF.md                    # this file
├── HANDOFF.sh                    # live verification script
├── model_registry.json           # 5 roles for the composite battery
├── tools/harness_core/           # 11 modules, 13 .py files
├── tests/                        # 10 files, 78 tests
├── experiments/                  # batteries + preregs + lab_runs_*
├── paper_v2/  paper_v3/  paper_5organs/
├── paper_v4/                     # STALE duplicate of 5organs — gitignored, do not edit
├── research/                     # ~3,450 lines of synthesis
├── bundles/  packages/           # Cordis
└── pilot/locks/                  # prereg locks
```

---

## 9. Known traps

Four things that have already cost time. Check them before trusting any status claim.

1. **A handoff can be written by a dying agent.** The previous `HANDOFF.md` reported HEAD `7b0a068` / 145 commits when the repo was at `4575e99` / 210 — 65 commits behind — and dated itself "03:35 UTC" when it was written at 17:03 UTC. The OpenCode session that produced it (`ses_fd4adc0eeffe0mWwMxU6owNbLT`, 5 days, 3,096 messages) had begun returning **empty assistant messages**; the last four user turns got no response at all. *Always re-derive numbers from disk. `git log --oneline -1` takes one second.*

2. **Item 5 is not running.** Both the old handoff and the tracker said the bakeoff matrix was "🔄 running (detached, don't re-launch)". No such process exists and `lab_runs_bakeoff/` last wrote 2026-08-25 18:47. It died two days before the handoff claimed it was live. Relaunch it if you want the matrix.

3. **The s126_v3 manifests keep only the last seed.** Each arm's `manifest_v3-*.json` is overwritten per run — `results.json` is the aggregate. A partial multi-seed run on 2026-08-27 (20:51 raw seed 20, 20:59 nocheck seed 8) overwrote two arms and then stopped without updating `results.json`, leaving a mixed-seed state on disk. Those two partial manifests are preserved as `*_partial.json`; the committed pilot manifests were restored. **If you launch a battery, let it finish, or note where it stopped.**

4. **`paper_v4/` outranks `paper_5organs/` alphabetically and by number, and is wrong on both counts.** See §2.

---

*Handoff verified against disk 2026-08-27 · HEAD `4575e99` · 210 commits · 0 unpushed · 78/78 green · 19pp + 21pp + 36pp · ~3,450 research lines · 9 queued (0 running)*
