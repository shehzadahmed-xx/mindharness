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
