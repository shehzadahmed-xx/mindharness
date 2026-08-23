# SpringFish simulation report

- Case: **C1 — Bangladesh fertiliser emergency finance and food provisioning**
- Scenario: **emergency_finance_only**
- Behavioural policy: **openai**
- Model: `openai/gpt-oss-20b`
- Seed: `20260731`
- Validation: **PASS**

## Final macro state

| Metric | Value |
|---|---:|
| round_num | 3 |
| legitimacy | 0.5399999999999999 |
| service_continuity | 0.79 |
| public_loss | 0.0 |
| inequality | 0.5412500000000001 |
| trust | 0.425 |
| verified_consensus | 0.25 |
| contaminated_consensus | 0.16666666666666666 |
| active_edges | 3575 |

## Game rounds

| Round | Row action | Column action | Pure Nash | Max regret | Engine |
|---:|---|---|---:|---:|---|
| 1 | accept_emergency_finance | senior_strict_finance | Yes | 0.0000 | cadCAD.Executor |
| 2 | accept_emergency_finance | senior_strict_finance | Yes | 0.0000 | cadCAD.Executor |
| 3 | accept_emergency_finance | senior_strict_finance | Yes | 0.0000 | cadCAD.Executor |

## Validation summary

- **actors_loaded:** 2974
- **relationships_loaded:** 3575
- **active_personas:** 12
- **rounds_completed:** 3
- **all_actions_legal:** True
- **finite_regrets:** True
- **no_fabricated_observed_facts:** True
- **contaminated_memories:** 27
- **llm_fallback_calls:** 6
- **status:** PASS

## Scientific interpretation

This run is a conditional computational experiment. Exact games, accounting rules, evidence grades and graph structure remain explicit. The language model is only a behavioural policy inside those constraints. Simulated frequencies and narratives are not automatically real-world probabilities or causal estimates.

Memories marked contaminated were generated or propagated without sufficient provenance. They are retained for studying misinformation cascades but excluded from verified consensus.
