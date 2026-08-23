# SpringFish simulation report

- Case: **C2 — Ukraine wartime railway repair and GDP-linked recovery claims**
- Scenario: **honour_warrants_high_tariff**
- Behavioural policy: **openai**
- Model: `Qwen3.5-0.8B-Q3_K_S`
- Seed: `8`
- Validation: **PASS**

## Final macro state

| Metric | Value |
|---|---:|
| round_num | 3 |
| legitimacy | 0.5299999999999999 |
| service_continuity | 0.79 |
| public_loss | 0.0 |
| inequality | 0.46625000000000005 |
| trust | 0.4125 |
| verified_consensus | 0.25 |
| contaminated_consensus | 0.3333333333333333 |
| active_edges | 3575 |

## Game rounds

| Round | Row action | Column action | Pure Nash | Max regret | Engine |
|---:|---|---|---:|---:|---|
| 1 | exchange_and_cap | accept_exchange | Yes | 0.0000 | cadCAD.Executor |
| 2 | exchange_and_cap | accept_exchange | Yes | 0.0000 | cadCAD.Executor |
| 3 | exchange_and_cap | accept_exchange | Yes | 0.0000 | cadCAD.Executor |

## Validation summary

- **actors_loaded:** 2974
- **relationships_loaded:** 3575
- **active_personas:** 12
- **rounds_completed:** 3
- **all_actions_legal:** True
- **finite_regrets:** True
- **no_fabricated_observed_facts:** True
- **contaminated_memories:** 17
- **llm_fallback_calls:** 0
- **status:** PASS

## Scientific interpretation

This run is a conditional computational experiment. Exact games, accounting rules, evidence grades and graph structure remain explicit. The language model is only a behavioural policy inside those constraints. Simulated frequencies and narratives are not automatically real-world probabilities or causal estimates.

Memories marked contaminated were generated or propagated without sufficient provenance. They are retained for studying misinformation cascades but excluded from verified consensus.
