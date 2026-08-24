# FOLLOW-UP: H1 rejection mechanism + v3 design (preregistration draft)
Date: 2026-08-24 · Parent: exp_s126_attribution_v2 (lock 39475d28, verdict REJECTED)

## Observed
raw attribution 1.000 vs harnessed 0.667 (delta -0.333). CII 0 both arms.
Error pattern (from partial.jsonl per-seed): harnessed errors concentrated on
GIVEN items answered yes — presence-salience contamination.

## Hypothesis H-v3
The anchor/narrative context raises felt-familiarity for ALL session content;
without an origin-check tool the model guesses from fluency. Giving the model
query_provenance(turn_id) + get_self_model DURING probes shifts strategy from
recall-guess to record-check; accuracy should rise toward raw or above.

## v3 protocol deltas (preregister BEFORE run)
1. Probe turn provides tools: query_provenance, get_self_model (read-only).
2. Two harnessed sub-arms: with-tools vs without-tools (isolates the mechanism).
3. Metrics unchanged (Part C.5). Prediction:
   P1: with-tools accuracy > without-tools by >0.15
   P2: with-tools >= raw (record-check beats transcript-recall)
   P3: latency cost of tool-checking measurable and bounded (<2x probe latency)
4. Same lock discipline: freeze -> commit -> run.

## Why this matters beyond repair
If P1 holds: witnessed introspection requires ACCESS TO THE WITNESS at question
time, not merely its existence — an operational requirement for any honest-agent
design (and a concrete answer to Lederman & Mahowald's access-vs-inference split).
