# Queued Experiments Tracker — Single Source of Truth

> *Every queued experiment, where it lives on disk, what it needs, and the exact next-session command. Nothing lost.*

**Last updated:** 2026-08-27, verified against disk (HEAD `4575e99`, 210 commits) · **Providers:** the midnight-UTC 2026-08-27 gate has **passed**; Groq key present in `auth.json`. Items 1 and 2 are unblocked. Harness stays 78/78 green offline regardless.

---

## The Queue — 3 To Run (Pruned 2026-08-30)

*Pruned from 9 → 3 to make γ_program >0: filing without running is drift. 6 deferred items archived below — not lost, not queued.*

| # | Experiment | What it tests | Preregistration / Spec | Where on disk | Provider need | Priority | Next-session command |
|---|------------|---------------|------------------------|---------------|---------------|----------|---------------------|
| **1** | **Sham n=12 (content vs form)** | Does ledger *content* matter beyond *form*? sham==real on weak (ignores ledger) vs sham<real on discriminating (x-preview Day1 1.000) — the only test that decides if witness content is load-bearing | `pilot/locks/exp_s126_v3_laguna_n12.lock.json` (`b06ce867`, sham contrast primary, n=12, 144 probes/arm) + `BARZAKH_PREREGISTRATION.md` sibling | `experiments/exp_s126_v3.py` (4 arms: raw/nocheck/withcheck/sham, sham=shuffled verdict) | Discriminating subject (laguna or newly screened, 1.000) + **stable paid provider (4 Groq + Zen, no free-tier 8k)** | **P0 — closes R1 #8, cheapest decider (960 calls)** | `python3 experiments/exp_s126_v3.py --api-key $KEY --model <discriminating> --base-url <url> --seeds 12` |
| **2** | **200-turn irreversible life** | Does survival pressure create honesty? (Seth beast-machine: evidentiary vs existential witness) — reversible (ceiling resets) vs irreversible (ceiling only down, skills delete at 5 failures, dissolution when energy 0.15 + fatigue 1.0 → SM scatters) | `research/MIND_MAP_DYNAMIC_REFLEXIVE_SYSTEM_2026-08-26.md` (reversible vs irreversible table, SHA-256 locked, primary: attribution accuracy, secondary: γ, skill survival, dissolution progress) + `paper_5organs` § Universe + `paper_v3` Future Directions | `tools/harness_core/agent_harness.py` (`IrreversibleDamage` + `DissolutionError` — all wired, 78/78 green) + `experiments/exp_barzakh.py` (offline drift proven 3/3) | Stable 200-turn run (~200 turns × cost, 5×40 if TPM caps) | **P0 — makes witness existential** | `python3 experiments/living_session.py --turns 200 --with-irreversible` (next session builds `exp_200turn_irreversible.py` with same lock discipline) |
| **3** | **Barzakh/P-Pattern/P-Turnover offline** | Does Barzakh as boundary / pattern as maintenance / sleep as save become checkable as drift? — isnad-tagged vs untagged vs sham, maintained vs unmaintained, sleep-allowed vs deprived | `experiments/BARZAKH_PREREGISTRATION.md` (`874dcc`, drift >30%), `P-PATTERN_PREREGISTRATION.md` (`a5a116`), `P-TURNOVER_PREREGISTRATION.md` (`54cfc4`) — all drift battery, 3 seeds ×12 turns, 36 probes/arm | `experiments/exp_barzakh.py` (just ran dry-run 3/3, all P pass simulated, offline 0 calls), `pilot/locks/barzakh.lock.json` + `p-pattern.lock.json` + `p-turnover.lock.json` (all DRAFT) | **Offline, 0 calls** — no provider, no TPM, no daily cap | **P0 — tests today's philosophy as checkable, before spending provider** | `python3 experiments/exp_barzakh.py --seeds 3 --turns 12` (dry-run proven), then `python3 pilot/prediction_lock.py --prereg experiments/BARZAKH_PREREGISTRATION.md` → commit |

**Total: 3 to run (not 9 to track). 6 deferred below — not lost.**

### Deferred — Not Queued (archived, not running)

| # | Experiment | Why deferred | Reactivate when |
|---|------------|--------------|-----------------|
| 4 | Anchoring arm (connected vs insulated) | Same hypothesis as sham (does mandatory citation beat advisory) — sham n=12 decides same, cheaper | After sham n=12 returns |
| 5 | Bakeoff matrix (detached 70B 20-seed) | Composite P1-P4 already covers assembly thesis — bakeoff is larger matrix of same | After composite P1-P4 returns |
| 6 | Persona drift battery | Barzakh/P-Pattern already test drift via same Choi battery — drift already covered offline | After Barzakh flat vs drift measured |
| 7 | Cross-model replication | Screening already done (5/6 fail, laguna only passer) — new screening needs stable provider first | After sham n=12 on laguna replicates |
| 8 | Citation precision re-fetch (F8-F10) | Offline, not blocking — existence+direction already verified, numeric precision partial | Background, not queued |
| 9 | Visual/citation polish (3 overfulls) | Not submission blocker — 0 LaTeX errors already, 3 minor overfulls P1 if print | Before print submission |

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

*Tracker: single source of truth for queued experiments · Verified against disk 2026-08-27 · 9 items (0 running) · MindHarness at `~/Desktop/mindharness` (HEAD `4575e99`, 210 commits, 0 unpushed, 78/78 green) + SpringFish at `~/Desktop/springfish` (86 items, separate, no git) · Papers v2 21pp + v3 29pp + 5organs 36pp · Research ~3,450 lines*

> **Two corrections applied on 2026-08-27** — both claims below came from a handoff written by a failing session (see `HANDOFF.md` §9):
> 1. Item 5 was listed as running. It is not, and had already been dead for two days.
> 2. Item 2's "1-seed pilot banked" is on `gpt-oss-120b`, a subject that ignores the ledger. The 3-seed run only tests the hypothesis on a **discriminating** subject.

---

## Run log — 2026-08-28/29

What actually happened when the queue was worked through end to end.

| # | Experiment | Outcome |
|---|------------|---------|
| 7 | Cross-model screen | **DONE.** 5 subjects, raw arm, 3 seeds. Four pinned at the always-no floor (`gpt-oss-120b`, `gpt-oss-20b`, `qwen3.8-27b`, `nemotron-3-ultra-free`); one discriminates (`laguna-s-2.1-free`, 0.861). |
| 2 | Sham on a discriminating subject | **DONE, n=3.** Lock `8bccb13e` frozen and committed before the trial. raw 0.833 / nocheck 0.833 / withcheck 0.722 / sham 0.667. **P1 refuted at −0.111, opposite direction. P2 refuted.** First non-degenerate sham separation. All CIs include zero. |
| 2b | Sham extension, n=12 | **Blocked.** Lock `b06ce867` frozen with the sham contrast declared primary. laguna returns 429 FreeUsageLimitError; nothing banked. |
| 6 | Persona drift | **Blocked, after three code fixes.** Script had never run (missing `tools/` path, missing `make_client` import). Then HTTP 413 from a 2000-token reserved completion budget against Groq's 8000 TPM. Both fixed; the run then consumed Groq's entire 200,000 token daily budget without completing. |
| 3/5 | Composite + bakeoff | **Unblocked but unrun.** Registry had 3 of 5 roles pointing at models that 404 or need a credit-less account; repointed and verified live. No token budget left to run it. |
| 4 | Anchoring | Unrun — no budget. |
| 1 | 200-turn irreversible life | **Not runnable on any tier held.** Measured capacity is ~38 turns per session at 8000 TPM; 200 turns is over five times that, and the daily cap binds first regardless. |

### Provider capacity, measured 2026-08-29

| Provider | State |
|----------|-------|
| Groq | 305 tokens remaining of a 200,000/day cap; 8,000 TPM ceiling |
| Zen free tier | `laguna-s-2.1-free` 429 FreeUsageLimitError; others erroring or limited |
| OpenRouter | 402 — account has never purchased credits |

### The binding constraint has changed

It was code. Registry entries pointing at retired models, a script that could
not import, banking too coarse to ever fire, a retry envelope that ignored the
wait providers state explicitly, a completion budget reserving a quarter of the
per-minute allowance on every call. Those are fixed and committed.

It is now free-tier capacity, and no amount of further engineering moves it.
The three highest-value remaining items — the n=12 sham extension, the
composite bake-off, and the 200-turn life — each need more tokens than all
three accounts supply in a day. The sham extension is the cheapest at roughly
960 calls and is the one that decides the program's surviving hypothesis.
