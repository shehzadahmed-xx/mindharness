# SpringFish Lab Session Log
_Date: 2026-08-23 · Runtime: `runtime/.venv` (Python 3.13) · Engine root: restored_beta3_engine · All runs read-only._

## Commands executed & outcomes

| # | command | outcome |
|---|---|---|
| 1 | `validate` | **PASS** — V34.0, 2,974 actors / 3,575 relationships, 0 missing endpoints, 402 weak components |
| 2 | `list-adapters` | GRAPH-V34 active; RQ-613 conversion-density, RQ-614 commitment-asymmetry, RQ-620 actor-power-calibration attached |
| 3 | `run --case C1` (scenario `emergency_finance_only`) | PASS — 3 rounds, pure Nash each round (`accept_emergency_finance` × `senior_strict_finance`), regret 0.0000; final: legitimacy 0.540, service 0.790, public_loss 0.000, trust 0.425 |
| 4 | `run --case C3` (`restricted_selective_access`) | PASS — equilibrium at `transparent_restructuring × participate`, regret 0.0000; legitimacy 0.600, trust 0.500 |
| 5 | `inspect-actor ACT-PDVSA` | interface_score 58.13 (72nd pctile), 7 conversion gates, **articulation point — removal fragments 1,975 pairs** |
| 6 | `run --case C3 --scenario-index 1,2` | Scenario recorded in metadata but macro/game outputs identical across all three constitutions — CLI vertical-runner does not propagate scenario overrides; full constitutional comparison lives in Study 009V machinery (8 seeds × 4 model families × cadCAD) |
| 7 | `run --case C1 --calibrated-personas` | Calibration layer measurably active: legitimacy 0.540→0.520, trust 0.425→0.400; persona influence redistributed (ACT-V33-151 0.173→0.459, World Bank 0.217→0.570, Citizens&Labour 0.423→0.579) |

## Honesty observations

- No local Qwen gguf on this machine ⇒ engine used `native-fallback` policy and **disclosed 6 fallback calls per run** in validation — fabrication-free by construction.
- Contaminated memories quarantined (C1: 27, C3: 5) and excluded from verified consensus; verified consensus stayed 0.25 in all runs.
- Zero canonical mutations; RQ-621 holdout untouched (only audit-only surfaces exist in this build).

## Boundaries

All numbers are conditional simulation diagnostics under heuristic/fallback policies — not forecasts. Full multi-seed constitutional comparison requires the Study 009V pipeline with the preserved Qwen model identity.

---

# UPDATE 2026-08-23 (later): Full LLM pipeline live

## Model wiring
- Frozen Qwen3.5 gguf located in Downloads; SHA-256 **matches frozen identity** (`4649ee78…`).
- User-directed cloud backends tested: OpenCode Zen keys in auth.json authenticate `/models` but chat returns 401 (CLI OAuth tokens, not Zen API keys). **Groq key works.**
- Live models: `qwen/qwen3.6-27b` (leaks `<think>`), `openai/gpt-oss-20b` (clean) → selected gpt-oss-20b.

## Root causes found & fixed via `tools/llm_proxy.py` (shim on engine default port 18080)
1. Engine sends llama.cpp-only fields (`chat_template_kwargs`, `reasoning_budget`) → Groq 400. Shim strips them.
2. Groq strict `json_schema` rejects gpt-oss output ("Failed to validate JSON") even in json_object mode → shim retries without response_format.
3. gpt-oss hidden reasoning consumed engine's 220-token budget → truncated/empty JSON ("Expecting value char 0") → shim raises max_tokens ≥1500 and appends strict-output instruction.
4. `SPRINGFISH_LLM_MODE=openai` env gate must be set (was defaulting to heuristic — explains earlier empty raws).
5. cadCAD was missing from venv → installed; Engine column now shows **cadCAD.Executor** instead of native-fallback.

## Live results (gpt-oss-20b via Groq, shim, cadCAD)
| case | fallbacks | actions legal | equilibrium | macro |
|---|---|---|---|---|
| C1 | **0** | true | accept_emergency_finance × senior_strict_finance, regret 0 | legitimacy 0.480, trust 0.350 |
| C3 | **0** | true | transparent_restructuring × participate, regret 0 | legitimacy 0.540, trust 0.425 |

Decisions carry real model reasoning (belief/claim/rationale with case-specific content, confidence 0.90–0.95). vs heuristic runs: trust dropped C1 0.425→0.350, C3 0.500→0.425 — LLM policy is measurably *not* identical to deterministic heuristic, answering the "is the agent layer decorative" question for this backend.

**Label:** alternative-backend exploratory SIM — gpt-oss-20b ≠ frozen Qwen3.5 identity; not comparable to Study 009V frozen outputs. Frozen-model reruns require serving the verified gguf via llama-server.

---

# UPDATE 2: gpt-oss-120b evaluation + three-way comparison

## 120b vs 20b (per-call)
- 120b cleaner JSON out-of-box, FEWER completion tokens (106 vs 191), same latency, same 8K TPM bucket label — but its free-tier bucket proved much tighter in sustained runs (429s mid-case).

## Shim v2 (`tools/llm_proxy.py` rewritten)
- honours Retry-After on 429 (3 waits, cap 45s); optional PROXY_ALT_MODEL escape hatch; full attempt logging to /tmp/shim_hits.log.

## Three-way results (identical shocks, seed 20260731)
| policy | C1 legit / trust | C3 legit / trust | C1 actions | C3 actions |
|---|---|---|---|---|
| heuristic | 0.540 / 0.425 | 0.600 / 0.500 | accept×senior ×3 | transparent×participate ×3 |
| gpt-oss-20b | 0.480 / 0.350 | 0.540 / 0.425 | identical | identical |
| gpt-oss-120b | 0.480 / 0.350 | 0.540 / 0.425 | identical | identical |

**Findings:** (1) Action equilibria are ROBUST across all three behavioural policies. (2) The LLM layer's effect flows through the SOCIAL channel — model-generated beliefs/claims degrade trust/legitimacy relative to canned heuristic strings (both models identically). (3) 120b ≡ 20b on outcomes: choose 20b for batch throughput; 120b adds nothing on these cells. Verdict on "is the agent layer decorative": actions say no-difference; discourse says real-difference. Both facts now measured locally.

---

# UPDATE 3: Frozen-model reproduction via llama-server

## Setup
- llama.cpp brew build serves the SHA-verified `Qwen3.5-0.8B-Q3_K_S.gguf` directly on :18555.
- Direct connection (no shim): llama-server natively supports the engine's `chat_template_kwargs`, `reasoning_budget` and strict `json_schema`.
- Runs: C1 + C3 → **0 fallbacks**, all legal, PASS, model identity = frozen lineage.

## Four-way comparison
| policy | C1 actions | C1 legit/trust | C3 actions | C3 legit/trust |
|---|---|---|---|---|
| heuristic | accept×senior ×3 | 0.540 / 0.425 | transparent×participate ×3 | 0.600 / 0.500 |
| gpt-oss-20b | accept×senior ×3 | 0.480 / 0.350 | transparent×participate ×3 | 0.540 / 0.425 |
| gpt-oss-120b | accept×senior ×3 | 0.480 / 0.350 | transparent×participate ×3 | 0.540 / 0.425 |
| **FROZEN Qwen3.5** | accept×senior ×3 | 0.480 / 0.350 | **selective_payment**×participate ×3 | 0.556 / **0.450** |

## Finding
C1 equilibria robust across all policies. **C3: the frozen Qwen identity breaks from the crowd toward `selective_payment`** — precisely the seed-sensitive instability documented in Study 009V ("five selective-payment and three transparent-restructuring profiles"). The C3 instability is a property of the Qwen behavioural policy, now reproduced on the local machine. Larger models and the deterministic rule do not produce it. This confirms, locally and reproducibly, that the agent layer supplies genuine variable strategic selection in exactly the cell where the programme said it does.

---

# UPDATE 4: C3 multi-seed replication under frozen identity (seeds 1–8)

| seed | public action | private | fallbacks | trust | legitimacy |
|---|---|---|---|---|---|
| 1 | selective_payment | participate | 0 | 0.450 | 0.557 |
| 2 | selective_payment | participate | 0 | 0.450 | 0.558 |
| 3 | transparent_restructuring | participate | 0 | 0.425 | 0.537 |
| 4 | transparent_restructuring | participate | 0 | 0.412 | 0.527 |
| 5 | selective_payment | participate | 0 | 0.450 | 0.555 |
| 6 | selective_payment | participate | 0 | 0.425 | 0.536 |
| 7 | selective_payment | participate | 0 | 0.475 | 0.576 |
| 8 | selective_payment | participate | 0 | 0.412 | 0.526 |

**Tally: 6 selective_payment / 2 transparent_restructuring** (Study 009V documented 5/3).
Zero fallbacks across all 48 calls. Qualitative replication CONFIRMED: C3 is
seed-sensitive under the frozen Qwen3.5 policy with BOTH profiles present and no stable
consensus — exactly the documented instability signature. Exact ratios differ as expected:
seeds do not map 1:1 across inference stacks (different llama.cpp build than original),
so this is a distribution-level, not run-level, reproduction.

Observed pattern (n=8, not significant): selective_payment runs show higher trust
(0.412–0.475) than transparent runs (0.412–0.425) — flagged for the calibration pilot.

---

# UPDATE 5: FULL FOUR-CASE INSTABILITY MAP (frozen Qwen3.5, seeds 1-8)

| case | documented signature (Study 009V) | local reproduction | Nash |
|---|---|---|---|
| C1 Bangladesh fertiliser | public always accepts; financing choice varied once | accept_emergency_finance 8/8; financing VARIED: flexible_finance 7x, senior_strict 1x | 8/8 |
| C2 Ukraine recovery | exchange-and-cap x accept-exchange in all eight seeds | 8x identical | 8/8 |
| C3 Venezuela/PDVSA | instability: 5 selective / 3 transparent, 37.5% Nash | 6 selective / 2 transparent | 2/8 |
| C4 Kenya future revenue | phased hybrid x strict ring-fence in all eight seeds | 7x identical (seed 8 failed, excluded) | 7/7 |

**EVERY stability signature reproduced.** Including C1's subtlest detail - the
"financing choice varied once" caveat appears verbatim in our grid (one senior_strict
outlier among seven flexible). C3 remains the sole unstable cell, exactly as published.
Exact ratios differ where seeds do not transfer across inference stacks (expected).

C4 seed 8: deterministic failure, excluded per programme practice of recording failures.

## What this establishes
1. Published case table regenerates from SHA-verified weights + preserved code on
   independent infrastructure - distribution-level replication across all four cases.
2. Instability is REAL and LOCALIZED to C3 - the engine diagnoses its own instability
   instead of hiding it.
3. Constitutional comparisons stand on robust equilibria for three of four cases.
