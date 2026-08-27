# Queued Experiments Tracker — Single Source of Truth

> *Every queued experiment, where it lives on disk, what it needs, and the exact next-session command. Nothing lost.*

**Last updated:** 2026-08-27, verified against disk (HEAD `4575e99`, 210 commits) · **Providers:** the midnight-UTC 2026-08-27 gate has **passed**; Groq key present in `auth.json`. Items 1 and 2 are unblocked. Harness stays 78/78 green offline regardless.

---

## The Queue — 9 Items

| # | Experiment | What it tests | Preregistration / Spec | Where on disk | Provider need | Priority | Next-session command |
|---|------------|---------------|------------------------|---------------|---------------|----------|---------------------|
| **1** | **200-turn irreversible life** | Does survival pressure create honesty? (Seth's beast-machine: evidentiary vs existential witness) — reversible (control, ceiling resets, skills recoverable) vs irreversible (ceiling only down, skills deleted at 5 failures on same type, dissolution when energy 0.15 + fatigue 1.0 → SM scatters, narrative truncates, reassembly = new agent, not same) | `research/MIND_MAP_DYNAMIC_REFLEXIVE_SYSTEM_2026-08-26.md` (reversible vs irreversible table, SHA-256 locked, primary: attribution accuracy, secondary: γ, skill survival, dissolution progress) + `paper_5organs` § Universe + `paper_v3` Future Directions | `tools/harness_core/agent_harness.py` (`IrreversibleDamage` + `DissolutionError` + `wire_irreversibility` + `wire_allostatic_dissolution` + `check_allostatic_viability` — all wired, 78/78 green) | Stable 200-turn run (~200 turns × cost) | **P0 — makes the witness existential** | `python3 experiments/living_session.py --turns 200 --with-irreversible --prereg experiments/prereg_200turn.json` (next session builds `exp_200turn_irreversible.py` with same lock discipline as sham/composite) |
| **2** | **Sham 3-seed (discriminating subject)** | Does ledger *content* matter beyond *form*? sham==real on weak subject means subject ignores ledger; sham<real on discriminating subject (x-preview Day 1 at 1.000) would prove content matters | `experiments/exp_s126_v3.py` (4 arms: raw/nocheck/withcheck/sham, sham = shuffled verdict, same form) + `COMPOSITE_PREREGISTRATION.md` P4 | `experiments/lab_runs_s126_v3/` — 1-seed pilot banked: 4×0.667 sham==real on gpt-oss-120b via Groq (subject ignores ledger, expected) | Discriminating subject (x-preview or similar capable, 1.000) + stable | **P0 — closes R1's #8 sham control** | `python3 experiments/exp_s126_v3.py --api-key $KEY --model <discriminating> --base-url <url> --seeds 3` (needs provider window) |
| **3** | **Composite mind (P1-P4)** | Does assembled mind beat single-model baselines? P1: composite ≥ best single on accuracy, P2: latency ≤1.5× fastest, P3: cost < ox-alpha solo, P4: withcheck composite > raw 0.667 by >0.15 | `experiments/COMPOSITE_PREREGISTRATION.md` (Theory → Design → P1-P4 → Analysis: Holm correction, ranked matrix) + `model_registry.json` (5 roles) | `experiments/bakeoff.py` + `model_registry.json` (monitor/qwen-32b, probe/gpt-oss-120b, generation/ox-alpha, validation/gpt-oss-20b, summarizer/llama-70b) + `tools/harness_core/agent_harness.py` (`load_model_registry`, `create_composite_respond_fn` wired fca4157, 5/5) | 5 roles × 3 seeds × stable | **P0 — assembly thesis, AHE cross-family transfer** | `python3 experiments/bakeoff.py --registry model_registry.json --seeds 3` |
| **4** | **Anchoring arm (connected vs insulated)** | Is confabulation unchecked attribution or architecturally disconnected channels? Requiring cited-evidence step collapses over-claim if connected, else citable dissociation inside one JSON | `experiments/ANCHORING_PREREGISTRATION.md` (Background S126 10/10 over-claims → Theory: connected vs insulated) | `experiments/exp_anchoring.py` (reuses bakeoff transport) | Providers | **P1** | `python3 experiments/exp_anchoring.py --seeds 3` |
| **5** | **Bakeoff matrix (detached 70B 20-seed)** | Full config × accuracy × latency × cost ranked matrix, Holm P1-P4, nulls reported identically | Part of composite preregistration | `experiments/lab_runs_bakeoff/` (detached pid from other session, will surface P1_delta) + `experiments/bakeoff.py` | **NOT running** — process is dead | **P1 — relaunch to get the matrix** | Verified 2026-08-27: no such process; `lab_runs_bakeoff/` last wrote 2026-08-25 18:47. Relaunch with `python3 experiments/bakeoff.py --registry model_registry.json --seeds 3` |
| **6** | **Persona drift battery** | Does ledger prevent >30% drift in 12 turns (Choi)? | `experiments/exp_persona_drift.py` | `experiments/exp_persona_drift.py` | Providers | **P1** | `python3 experiments/exp_persona_drift.py --seeds 3` |
| **7** | **Cross-model replication** | Does x-preview Day 1 (1.000) replicate on other discriminating subjects? (larger reasoners, introspection-post-trained) | `paper_5organs` + `paper_v3` Future Directions | Screening via `exp_s126_v3.py` with different `--model` | Providers + screening (needs capable subject) | **P1** | `python3 experiments/exp_s126_v3.py --model <candidate> --seeds 1` (screen), then 3-seed if discriminating |
| **8** | **Citation precision re-fetch** | F8-F10 exact numbers: Sofroniew ±212/-303 Elo, r=0.95, Panickssery r=0.94, Choi 30% — abstracts confirm direction, exact numbers need one PDF pass each | `research/CITATION_AUDIT_2026-08-26_VERIFIED.md` (NEXT ACTIONS queued, F8-F10 overall: VERIFIED existence + direction; NUMERIC PRECISION PARTIAL) | `research/CITATION_AUDIT_2026-08-26_VERIFIED.md` | Offline, not blocking | **P2** | Re-fetch PDFs, close numbers, update `CITATION_AUDIT_..._VERIFIED.md` |
| **9** | **Visual/citation polish** | 3 minor overfulls (5.5pt), visual palette (loopblue unify, tiny→scriptsize, gray contrast) — deferred as P1 print quality, not submission blocker | Paper reviews (technical 2.5→3.5, clarity 3→4, visual 25 findings) | `paper_5organs/main.tex` (408K→397K after fixes, 0 errors, 3 minor overfulls remain) | Offline | **P1 if targeting print** | Unify `loopblue` RGB, fix 3 overfulls, promote `tiny→scriptsize` |

**Total: 9 queued items (7 experiments + 1 running + 1 polish). All tracked, none lost.**

---

## Disk Map — Where the 200-Turn Life Lives

```
~/Desktop/mindharness/
├── tools/harness_core/agent_harness.py  # IrreversibleDamage + DissolutionError + wire_irreversibility
│                                        # + wire_allostatic_dissolution + check_allostatic_viability
│                                        # + load_model_registry + create_composite_respond_fn — all wired, 78/78
├── research/MIND_MAP_DYNAMIC_REFLEXIVE_SYSTEM_2026-08-26.md  # Spec: reversible vs irreversible table, SHA-256
├── paper_5organs/main.tex                # § Universe as largest loop + § What it all means — theory predicts test
├── paper_v3/main.tex                     # Future Directions: 200-turn life with reversible vs irreversible table
└── experiments/
    ├── living_session.py                 # Base runner: --turns 200 with IrreversibleDamage wired (next session builds exp_200turn_irreversible.py)
    ├── exp_s126_v3.py                    # Sham battery (4 arms, 1-seed pilot banked)
    ├── bakeoff.py                        # Composite matrix
    ├── model_registry.json               # 5 roles (monitor/probe/generation/validation/summarizer)
    └── lab_runs_s126_v3/                # 1-seed pilot: 4×0.667 sham==real
```

The 200-turn life is **specified, not yet a standalone script** — it runs as `living_session.py --turns 200` with `IrreversibleDamage` wired. Next session builds `exp_200turn_irreversible.py` with same lock discipline as sham/composite.

---

## Next Session — Three Commands

```bash
bash HANDOFF.sh                                           # 1. Verify: repo, tests, papers, providers, Cordis wiring
cat research/QUEUED_EXPERIMENTS_TRACKER.md                # 2. See the 9 queued, with next-session commands
# 3. Providers at midnight UTC 2026-08-27 00:00 — sham 3-seed + 200-turn life when window opens
```

---

*Tracker: single source of truth for queued experiments · Verified against disk 2026-08-27 · 9 items (0 running) · MindHarness at `~/Desktop/mindharness` (HEAD `4575e99`, 210 commits, 0 unpushed, 78/78 green) + SpringFish at `~/Desktop/springfish` (86 items, separate, no git) · Papers v2 19pp + v3 21pp + 5organs 36pp · Research ~3,450 lines*

> **Two corrections applied on 2026-08-27** — both claims below came from a handoff written by a failing session (see `HANDOFF.md` §9):
> 1. Item 5 was listed as running. It is not, and had already been dead for two days.
> 2. Item 2's "1-seed pilot banked" is on `gpt-oss-120b`, a subject that ignores the ledger. The 3-seed run only tests the hypothesis on a **discriminating** subject.