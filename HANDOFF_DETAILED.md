# MindHarness — Detailed Handoff for a New Session

**So you pick up with zero prior context and know where everything is, what it all means, where we are, and what happened.**

---

## 0. Start Here — 30 Seconds

```bash
bash HANDOFF.sh                          # 1. Verify: repo, tests, papers, providers, Cordis wiring (78/78 green)
cat research/QUEUED_EXPERIMENTS_TRACKER.md  # 2. See the 9 queued, with next-session commands
cat HANDOFF_DETAILED.md                  # 3. This file — full state, one loop at every scale, so you know what everything means
```

- **Repo:** `~/Desktop/mindharness` (clean, HEAD `7b0a068`+ , 145 commits, remote `github.com/shehzadahmed-xx/mindharness`)
- **Companion:** `~/Desktop/springfish` (86 items, SpringFish / Spring-Loaded Door + ESC — separate work, same thesis, no git, untouched)
- **Harness:** 11 modules + counterfactual, 8 layers L0–L7, Light→REM→Counterfactual→Deep, 78/78 tests green
- **Papers:** v2 tagged `paper-v2-final` at `6385eb3` (19pp empirical) · v3 at `f236696`+ (~35pp program, 385K) · 5organs at `7b0a068` (theory, 402K, 38 bib, 0 errors, 6 TikZ wired + 10-figure gallery)
- **Research:** 8 synthesis docs, 2,136 lines (see § Research below) — every synthesis has its citations, every loop could be its own paper
- **Providers:** Groq 403, OpenRouter 50/day until midnight UTC 2026-08-27 00:00, Zen 500 — harness stays 78/78 green offline
- **Cordis:** `dsh-mindharness` (6 plugins, verified via `dsh --dump-config`) + `dsh-mindharness-parliament` scaffold (9 inserts, 7 packages, many tongues one harness)

---

## 1. What This Is — One Sentence

> **Everything is a self-reinforcing loop sustained by practice, made checkable if witnessed. One loop at every scale, five organs at every level, and the only real choice is what you feed the loop and whether the slower watcher can check the record before the next vote. Everything else is that same loop, woven tighter.**

Three linked programmes, one thesis:

| Programme | Claim | Method | Where |
|-----------|-------|--------|-------|
| **Spring-Loaded Door (SLD)** | Crises decouple loops from institutional anchors | Ledger V34.0 (2,974 actors / 3,575 edges) + cadCAD | `~/Desktop/springfish` (archived) |
| **Event–State–Contract (ESC)** | Financial claims are constitutional objects bearing exhaustion risk | 7-paper series + Baraka Protocol redesign (state-contingent, not interest) | `~/Desktop/springfish` (archived) |
| **MindHarness (active)** | The self-model is load-bearing; its removal is measurable via provenance ledgers; the same five that make a cell stable make a mind stable | 11-module harness + 3 preregistered batteries + 3 papers + 8 synthesis docs | **`~/Desktop/mindharness` (this repo, active)** |

**Active thread:** MindHarness program paper + parliament of models + the 5-organs theory. SLD/ESC remain at `~/Desktop/springfish`, untouched, no git. This handoff is for MindHarness.

---

## 2. Where the Files Are — So You Don't Get Lost

### Homes

| Home | Path | What is there | Git |
|------|------|---------------|-----|
| **MindHarness** | `~/Desktop/mindharness/` | Harness, papers, research, Cordis bundles, experiments — our life | Yes, `mindharness` remote, 145 commits, clean |
| **SpringFish** | `~/Desktop/springfish/` | Ledgers V17/V32, HAMBA, pilot, lab_runs, synthesis — SpringFish/SLD | No git (history moved with MindHarness, archives remain as files) |

### MindHarness — complete map

```
~/Desktop/mindharness/
├── README.md                    # loom/warp/weft, 8 layers, 5 invariants, quick start, research index
├── HANDOFF.md                   # short verified handoff (this file's companion — numbers re-derived from disk)
├── HANDOFF.sh                   # runnable verifier: repo, tests, papers, providers, Cordis wiring (bash HANDOFF.sh)
├── HANDOFF_DETAILED.md          # this file — full state, what everything means, where we are, what happened
├── BUILD_PLAN.md                # harness build spec, phases, governing principles
├── PREREQUISITES.md             # metric canon, gates, provider notes (paths now mindharness)
├── model_registry.json          # 5 roles: monitor/qwen-32b, probe/gpt-oss-120b, generation/ox-alpha, validation/gpt-oss-20b, summarizer/llama-70b
│
├── tools/harness_core/          # 11 modules, 8 layers L0–L7, 78/78 green
│   ├── backend.py               # L0: fingerprint per call, curl past Cloudflare 1010, capability matrix
│   ├── provenance.py            # L1: Span source-bound + ref, coverage, attribution_audit
│   ├── self_model.py            # L6: CAS fence, 3 cause channels, verbatim archive
│   ├── monitor.py               # L5: two-stage detect→diagnose, γ=changed/diagnosed, compliance guard γ=0
│   ├── embodiment.py            # L3/L2: energy floor 0.15, fatigue cap 1.0, affordance removal
│   ├── affect.py                # L3: valence/arousal EMA, bounded [0.5,2.0] multipliers
│   ├── hermes_adoption.py       # L3: SkillLibrary + KG, cause-tagged, assert-blocked
│   ├── consolidation.py         # L3: Light→REM→Counterfactual→Deep, untagged BLOCKED
│   ├── counterfactual.py        # L3: variant→simulate→regret, pluggable, dry_run-safe (6/6)
│   ├── agent_harness.py         # All layers: integrates everything, 40/40 livings, dissolution, model_registry wiring
│   └── __init__.py              # exports: CounterfactualReplay, etc. (78/78 via harness_core import)
│
├── tests/                       # 78/78 green: for f in tests/test_*.py; do python3 "$f"; done
│   ├── test_counterfactual.py   # 6/6: variants, backward compat, high-regret, dry_run, AgentHarness pluggable
│   ├── test_phase0.py           # 6/6: backend, fingerprint, capability
│   ├── test_phase1_selfmodel.py # 16/16: CAS fence, 3 causes, verbatim
│   ├── test_phase2_provenance.py# 10/10: spans, coverage, audit
│   ├── test_phase3_monitor.py   # 8/8: two-stage, γ, compliance guard
│   ├── test_phase4_embodiment.py# 9/9: energy, fatigue, affordances
│   ├── test_phase5_consolidation.py # 6/6: Light/REM/Deep, untagged BLOCKED
│   ├── test_phase65_hermes.py   # 6/6: SkillLibrary + KG
│   ├── test_integration.py      # 7/7: AgentHarness loop
│   └── test_irreversibility.py  # 4/4: IrreversibleDamage, DissolutionError
│
├── paper_v2/                    # 19pp empirical, tagged paper-v2-final at 6385eb3 (10 figs, preregistered locks, R1 17 weaknesses + R2)
│   └── main.pdf (327K) / main.tex (1098 lines, 23 bib)
├── paper_v3/                    # ~35pp program, at f236696+ (App. A Cordis + App. B Mirror, 385K, 0 errors)
│   └── main.pdf (385K) / main.tex (1656 lines, 25 bib)
├── paper_5organs/               # theory: The Dynamic Reflexive Loop and the Five Organs, at 7b0a068 (402K, 38 bib, 0 errors, 6 TikZ wired + 10-figure gallery)
│   ├── main.pdf (402K) / main.tex (1109 lines, 38 bib, 0 errors)
│   └── figures_gallery.pdf (198K, 10 figures, pick by number) + figures_gallery.tex
│
├── research/                    # 8 synthesis docs, 2,136 lines — every synthesis has citations, every loop could be its own paper
│   ├── PROGRAM_SYNTHESIS_DETAILED.md (352) — full map: program → humans → mind → everything
│   ├── DYNAMIC_REFLEXIVE_HARNESS.md (249) — loom/warp/weft philosophy
│   ├── RESEARCH_MIRROR.md (273) — 12 frontiers, ~40 papers live-checked
│   ├── AGENCY_AND_THE_CONSTRUCTED_SELF.md (193) — where agency lies when now/self/world are illusions
│   ├── MAPPED_NERVOUS_SYSTEMS_VALIDATION_2026-08-27.md (145) — every mapped system, 4-path convergence
│   ├── FOUR_METHODS_ONE_DESTINATION_CONVERGENT_VALIDITY.md (203) — evolution→connectomics→math→engineering
│   ├── WHAT_IT_ALL_MEANS.md (336) — complete synthesis: one loop, five organs, only real choice
│   ├── LOOP_AT_EVERY_SCALE_CELL_MIND_MARKET_MODEL.md (240) — cell→mind→market→model, how they interlock
│   └── QUEUED_EXPERIMENTS_TRACKER.md (8.1K) — 9 queued, single source of truth
│
├── experiments/                 # 7 queued + 1 running + batteries
│   ├── exp_s126_v3.py           # 4 arms: raw/nocheck/withcheck/sham (shuffled verdict), 1-seed pilot banked: 4×0.667 sham==real on gpt-oss-120b
│   ├── bakeoff.py               # composite matrix, model_registry.json (5 roles)
│   ├── exp_anchoring.py         # anchoring arm (connected vs insulated)
│   ├── exp_persona_drift.py     # persona drift battery (Choi >30% in 12 turns)
│   ├── living_session.py        # living sessions (40/40, base runner for 200-turn life)
│   ├── lab_runs_s126_v3/        # 1-seed pilot: results.json + 4 manifests
│   ├── lab_runs_anchoring/      # anchoring partial runs
│   ├── lab_runs_bakeoff/        # detached 70B 20-seed (pid from other session, will surface P1_delta)
│   ├── ANCHORING_PREREGISTRATION.md + COMPOSITE_PREREGISTRATION.md # preregistered, SHA-256 locked
│   └── model_registry.json      # also at top level (5 roles, wired fca4157)
│
├── bundles/                     # Cordis bundles
│   ├── dsh-mindharness/cordis.patch.yml (6 plugins, verified via dsh --dump-config)
│   └── dsh-mindharness-parliament/cordis.patch.yml (9 inserts, 7 packages: perception/memory/affect/planner/habit/narrator/workspace)
└── packages/mindharness-parliament/{perception,memory,affect,planner,habit,narrator,workspace}/src/index.ts
```

---

## 3. What Everything Means — One Loop, Five Organs, One Choice

> **One loop at every scale, five organs at every level, and the only real choice is what you feed the loop and whether the slower watcher can check the record before the next vote. Everything else is that same loop, woven tighter.**

### The one loop (System ↔ World, two channels)

A system that acts on a world that contains itself, so the world the system next perceives already contains the system's last act. Two channels: physical (order executes, calcium floods) and informational (others see you acted and change because of what it meant). When both run, three consequences: models rot from use, measurement corrupts, truth moves. Humans add a third: self-observation is also an action — labeling "anxious" installs a filter. Autopoiesis: you persist as a pattern, not as stuff. The loop builds the thing that runs it. Figure 1 in `paper_5organs` shows it.

### The five organs — the warp (mandatory, not optional)

Selection theorems (Nayebi UAI 2026, Cor. 3-5) prove any competent agent under mixed tasks is forced to develop these five or be exploited. They are the warp; everything else is weft.

| Organ | What it does | Without it | In harness |
|-------|--------------|------------|------------|
| **Boundary** | What counts as self vs world (selectively permeable) | Confabulation (98% on fabrications) | Provenance Ledger (L1): every span source-bound + ref, coverage 1.000 |
| **Two-speed memory** | Fast labile (one-shot) + slow structural + sleep | Catastrophic forgetting | Light→REM→Counterfactual→Deep, 12/12 tests |
| **Salience gate** | What gets tagged for consolidation | Saturation | AffectState [0.5,2.0], Sofroniew ±212/-303 Elo |
| **Damping** | What prevents runaway | Seizure, panic, blowup | cull_failed, Light dedup, dissolution |
| **Internal observer** | Slower loop vetoing faster one (γ = changed/diagnosed) | Inert watching (γ=0) | MonitorGate, compliance guard γ=0 |

Each organ at 8 scales (molecule→universe) — each loop could be its own paper, here together as one process. The same five were independently discovered by 8 traditions (Abhidharma's 52 factors, Sufism's stations, Ghazali's crisis, Ibn Arabi's khayal, Advaita's veil, Taoism's untellable loop, Stoicism's journal, phenomenology's bracketing) — not by borrowing, but by measuring the same constraint (Nayebi Cor. 5). Four methods (evolution 302 neurons → connectomics 140k → mathematics → engineering 78/78) converge on the same five — not analogy, convergent validity.

### The only real choice

What you feed the loop and whether the slower watcher can check the record before the next vote. You don't choose the options — affordance gating removes some before they appear. You don't fully choose the winner — parliament votes without a captain, 200ms before you feel you chose. You can veto the winner, keep a witness that makes the next winner more honest, and slowly change which options appear by what you rehearse. That's not the free will you were promised. It is the free will you actually have.

Practically: pick what you rehearse (myelination keeps receipt, 100× speed), protect sleep (SHY + 10-20× replay), buy BDNF with exercise, externalize the witness (write), never let a fast loop grade its own homework.

---

## 4. Where We Are — Honestly

| Layer | Built | Tested | Proved | What remains |
|-------|-------|--------|--------|--------------|
| Witness (L1 ledger) | Yes | Yes (78/78) | Without it, 98% on fabrications; with it but unqueried, always-no (0.667) | Sham 3-seed: does content matter beyond format? (queued) |
| Metacognition (γ-gate) | Yes | Yes | Monitoring without control is inert (γ=0); wiring it yields +8.6pp (Cao) | — |
| Embodiment + Affect | Yes | Yes | Exhaustion is an attractor (40/40 replicated cross-architecture) | — |
| Consolidation (Light→Deep) | Yes + counterfactual | Yes (12/12) | Untagged promotion BLOCKED; REM ablation changes output | — |
| Counterfactual replay | Yes (6/6) | Yes | Variant→simulate→regret, pluggable, dry_run-safe | Integrate into 200-turn life's consolidation |
| Irreversibility + Dissolution | Yes (wired) | 4/4 | DissolutionError + reassembly = new agent | **200-turn irreversible life: does survival pressure create honesty? (queued, P0)** |
| Papers | v2 19pp + v3 ~35pp + 5organs 402K | 0 errors, 38 bib | R1 17 weaknesses + R2 addressed, 2 reviews in (technical 3.5/5, clarity 4/5 after fixes) | Providers at midnight UTC for sham + 200-turn |
| Research | 8 docs, 2,136 lines | All live-checked | Every synthesis has citations, every loop its own paper | — |
| Cordis | 6 plugins verified + parliament scaffold (9 inserts) | Verified via dump-config | Wiring correct, providers are bottleneck | Many-model competition when window opens |

**Honest gaps:** Energy hits 0.15 and nothing dies — simulated stakes, not real (Seth's beast-machine). Sham 1-seed shows sham==real on weak subject (expected), needs discriminating subject for the real test. Papers are 0 errors but still have 3 minor overfulls (5.5pt) and 6 unused bib entries (low priority, not blocking).

---

## 5. What Happened — The Arc So Far

1. **Built the witness harness** around any frozen LLM: 11 modules, 8 layers, Light→REM→Counterfactual→Deep, 78/78 green, with an audit trail for every thought. The LLM is interchangeable; the harness is the authorship.

2. **Ran the batteries:** S126 attribution battery (raw 1.000 vs harnessed 0.667), living sessions 40/40 replicated cross-architecture (nemotron + gpt-oss-120b, coverage 1.000), composite P1+P2 passed, bakeoff queued, persona drift specified. Sham 1-seed pilot banked: 4×0.667 sham==real on weak subject (expected — subject ignores ledger).

3. **Wrote the papers:** v2 (19pp empirical, S126, sham, γ-gate, livings) tagged `paper-v2-final`; v3 (~35pp program, 5 invariants framing, reflexive systems, 8 levels, Cordis App. A + Research Mirror App. B); 5organs (theory, 402K, 38 bib, 0 errors, 6 TikZ + 10-figure gallery) — three papers, three scopes, no duplication.

4. **Mapped the same five everywhere:** 8 levels (molecule→universe) each detailed where each loop could be its own paper; 8 traditions independently found convergent insights (not same five, hedged); 4 methods (evolution/connectomics/math/engineering) converge — not analogy, convergent validity.

5. **Separated the homes:** `~/Desktop/mindharness` (clean, 0 dirty, 78/78, 145 commits) + `~/Desktop/springfish` (86 items, separate) — two homes, one thesis. Paths, paper URLs, and PREREQUISITES+D docs fixed from `springfish` → `mindharness`, papers recompiled, tests verified from new home.

6. **Wired the next direction:** `model_registry.json` (5 roles) per-role into `AgentHarness` (fca4157), parliament of models scaffold (9 inserts, 7 packages — many tongues, one workspace, witness as arbiter), figure gallery (10 figures, pick by number).

7. **Handled reviews:** 3 agents (technical 2.5→3.5, clarity 3→4, visual 25 findings) → 7 fixes one by one (RQs/Key Terms/one-turn figure, Nayebi hedge, parliament placement, citation integrity, holographic fix, duplicate removal, falsifiability matrix). Remaining: 3 minor overfulls + 6 unused bib (low priority).

---

## 6. How to Continue — Nothing Lost, Everything Queued

```bash
# 1. Verify (takes 30s, offline, no API keys)
bash HANDOFF.sh

# 2. See the 9 queued, with next-session commands
cat research/QUEUED_EXPERIMENTS_TRACKER.md

# 3. Read this handoff (full state) or HANDOFF.md (short verified)
cat HANDOFF_DETAILED.md  # this file

# 4. When providers recover (midnight UTC 2026-08-27 00:00):
#    - Sham 3-seed on discriminating subject (R1's #8 — does content matter?)
#    - 200-turn irreversible life (Seth — does survival pressure create honesty?)
#    Both wired, queued, P0 — model registry per-role already wired for parliament composite.
#    Detached 70B 20-seed (bakeoff) is still running — check with: ps aux | grep -E "bakeoff|battery"
```

**Papers:** v2 is tagged and citable (19pp); v3 (~35pp) + 5organs (402K) are 0 errors, pushed — remaining polish is 3 minor overfulls + 6 unused bib, not blocking. Research docs (2,136 lines) carry the deepest detail as companion; no further synthesis needed for "everything in detail" — audit closed.

**Two homes, one thesis, no shared working tree. Next observation belongs to the providers and to the 200-turn life that tests whether stakes make the witness existential.**

---

*Handoff: detailed, comprehensive, and runnable — a new session reads this file and knows where every file is, what everything means, where we are, and what happened, without needing any prior context.*

*Last updated: 2026-08-27 03:35 UTC · HEAD 7b0a068+ · 145 commits · 78/78 green · Papers 19pp + ~35pp + 402K · Research 2,136 lines · Cordis 6+9 plugins · 9 queued (1 running) · Providers queued for midnight UTC*
