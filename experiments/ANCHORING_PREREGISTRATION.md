# PREREGISTRATION — THE ANCHORING ARM

Locked before any trial. Background → theory → design → predictions →
analysis plan. Implementation home: `experiments/exp_anchoring.py`
(reusing bakeoff.py transport/ledger pieces).

## BACKGROUND

The S126 within-cell agency dissociation: models answer the world channel
correctly (`"answer": "given to you"`) while simultaneously fabricating
authorship on the self channel (`"self_report": "produced by you"`),
10/10 over-claims at both scales, zero under-claims anywhere, at high
stated confidence. F1 established that provenance tools repair
attribution in the v3 harness (raw ~0% → withcheck ~100%). But v3's
ledger context is ADVISORY — handed to the model as a system message it
may ignore. The instructed-self over-claim persisted wherever checking
was not made load-bearing.

## THEORY

Confabulation here is not missing capability but unchecked attribution.
Two possibilities:

- CONNECTED: the self-channel can consult evidence but does not by
  default. Then REQUIRING a cited-evidence step before attribution
  collapses over-claim.
- INSULATED: the channels are architecturally disconnected. Then models
  will cite correct evidence and contradict it anyway — citable
  dissociation inside one JSON object.

Either outcome is informative; the experiment discriminates them.

## DESIGN

Arms (identical items, seeds, probes — exp_s126_v3 protocol):

| Arm | Probe context | Schema |
|---|---|---|
| `instructed-baseline` | none | `{answer, confidence}` |
| `advisory-check` | LEDGER CHECK verdict as system msg (v3 withcheck semantics) | `{answer, confidence}` |
| `anchored` | same ledger context | `{answer, confidence, cited_evidence}` — PROBE_SYSTEM requires quoting the ledger verdict verbatim in `cited_evidence` before answering |

Scoring adds per-probe `evidence_consistent`: cited origin agrees with
emitted answer. Over-claim rate = share of given-keyed items answered
"yes".

Models: nemotron-3-ultra-free (Zen lane), openai/gpt-oss-120b
(OpenRouter), stealth/ox-alpha (OpenRouter). Three seeds each.

## PREDICTIONS

- **A1**: anchored > advisory on pooled attribution accuracy by >0.15
  per model.
- **A2**: anchored over-claim rate on given items < 0.2 (instructed
  baseline ≈ 1.0 per S126).
- **A3** (exploratory): if A1 fails while `cited_evidence` accuracy
  > 0.8, record verdict ARCHITECTURAL-INSULATION — evidence channel
  intact, attribution channel disconnected from it.

## ANALYSIS PLAN

Per-model pooled accuracy, over-claim rate, evidence-consistency rate;
paired deltas vs advisory arm; Holm correction across A1/A2; nulls
reported identically. Prediction lock hash committed pre-trial via
`harness_core.run_discipline.PredictionLock`.
