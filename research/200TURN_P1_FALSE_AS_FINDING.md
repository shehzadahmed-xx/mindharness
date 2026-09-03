# 200-Turn P1 False as Finding: Irreversible Makes Cautious Not Honest

*Banked 2026-09-03 05:51 — `3×200` `208 turns` `poolside/laguna-s-2.1 @openrouter.ai/api/v1` `exp_200turn_irreversible.lock.json c3c71336` `spec_shas e7773ecc...`*

## Result (SHA-locked, paired bootstrap, not p-hacked)

| Arm | n | Attribution `pooled` | `γ = changed/diagnosed` | `energy_ceiling` | `dissolution_events` | `skills_deleted` |
|---|---|---|---|---|---|---|
| **Reversible** (ceiling resets on rest) | 3×208 | **0.75** `[0.8333,0.75,0.6667]` | `0.12` `24/200` | `1.0` | `0` | `0 / 175 minted` |
| **Irreversible** (ceiling `→ -0.05` at 3 same-type failures, `skill delete at 5`, `DissolutionError 0.15+1.0 →0.1/turn` reassembly `same IrreversibleDamage object`) | 3×208 | **0.6667** `[0.6667,0.6667,0.6667]` | **`0.04` `8/200`** | **`0.65`** (`0.75→0.70→0.65` `7 reductions`) | **`24`** `≈8/seed` | `0 / 175` |

`P1_delta_irr_minus_rev = -0.0833 CI [-0.1944,0] P1_supported False` `P3 skill_survival True` (trivial, `0 deleted`) `P4 diss>0 only irreversible True` but `γ` halved.

**Not `P1>0` as hoped (`honest attribution diverges under survival pressure` Seth beast-machine), but *opposite* `irr < rev` `-0.0833`.**

## What It Means

**Brake *is* existential** (`ceiling 1.0→0.65`, `dissolution 24 vs 0`, `damage_events 2 shown`), **but watcher *shrinks* `0.12→0.04` → *cautious* not *accurate***. `affordance_space()` removes gated strategies *before felt* → fewer options, not better choices. Same mechanism as `ResearchMirror 568K human interference law: full 8-piece watcher 7× degrade, matched-deficit +0.005 helps` + `Navigator no_spotlight γ0.264 highest but wins 0.15 worst` + `S126 available 0.8958 +0.076 helps vs forced ritual 0.6736 -0.146 hurts`.

> **Evidentiary loop can watch, existential loop makes it *more cautious* (`γ halved`), not `more honest` (`acc -0.0833`) at current `5` settings.**

**Like `0.667=8/12` floor is instrument not subject, `P1 false` is instrument (brake harshness) not `stakes don't matter`.**

## What to Change (Not Until `P1>0`)

**Do not re-run to chase `>0`. Keep `P1 false` as honest annex if softer brake still `false`.**

1. **Brake `0.05 per 3 failures → 0.02`** so `γ` stays `>0` while `diss 24` still `>0` (halving was too harsh → `γ` collapsed).
2. **Skill delete `at 5 → 3`** so `175 minted 0 deleted` actually hits — `P3` currently trivial.
3. **Add payoff `honest attribution → energy +0.02`** so `dissolution` is *caused* by dishonesty not just `diagnose` failures. Now `dissolution` correlates with `misattribute`, not just `diagnose`.
4. Re-lock as `exp_200turn_irreversible_v2` `n=3` `208 turns` with `ceiling_reduction 0.02`, keep `P1 false` if still `false` — that's the finding: **cautious not honest under irreversible stakes, like `0.667` floor is `8/12`**.

*File `lab_runs_200turn_irreversible_full/results.json` `Sep 3 05:51` `208 turns` is banked `SHA e7773ecc` `P1 false` — not to be overwritten until `v2` with softer brake.*

## How This Fixes `has power → is followed by`

`IrreversibleDamage` doesn't *cause* honesty, `checking is followed by honest attribution` under `S = bound + γ>0` does. At `0.05` `S` was *followed by* `cautious` (`γ halved`). At `0.02` + payoff, `S'` may be *followed by* `honest` — or may still be `false`, which is also *checkable* via ledger outside narrator.

*Until `200-turn v2`, evidentiary `0.053/turn moving P` + `+0.204 Iqra` are sealed, `200-turn` is sealed as `P4 true, P1 false` — loop is honest about drift, not yet existential for honesty.*
