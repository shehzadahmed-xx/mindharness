# INVESTIGATION: Observability-Driven Harness Evolution Beats Model Upgrades
Date: 2026-08-24 · Verdict: VERIFIED with stronger implications than advertised
Source: arXiv 2604.25850 (v4, 2026-05-18), Lin/Liu et al., Fudan + Qiji Zhifeng. Code: github.com/china-qijizhifeng/agentic-harness-engineering

## Method (AHE)
Evolution agent improves a coding agent's harness; base model FROZEN.
Three observability pillars:
1. Component observability - NexAU substrate: 7 editable component types as files
   (prompt, tool desc, tool impl, middleware, skill, sub-agent, LTM); failures map
   to one class; git gives file-level rollback.
2. Experience observability - Agent Debugger distills millions of trajectory tokens
   into layered drill-down evidence corpus.
3. Decision observability - change manifest pairs EVERY edit with a self-declared
   prediction, verified vs next-round task deltas => falsifiable contract; failed
   predictions reverted at file granularity.
Governance: evolver writes only in harness workspace; verifier/tracer/model config
read-only; seed prompt non-deletable (blocks disable-verifier/swap-model shortcuts).

## Results
- Terminal-Bench 2: pass@1 69.7% -> 77.0% in 10 iterations (> Codex CLI 71.9%;
  > ACE; > TF-GRPO).
- Frozen-harness cross-model transfer: deepseek-v4-flash +10.1pp (51.7->61.8),
  qwen-3.6-plus +6.3pp, gemini-3.1-flash-lite +5.1pp, GPT-5.4 +2.3pp.
- SWE-bench-verified transfer: highest aggregate success at 12% fewer tokens.
- Ablation: gains localize to TOOLS + MIDDLEWARE + LONG-TERM MEMORY;
  system-prompt-alone REGRESSES.

## Confessed limits
1. Non-additivity: stacking effective edits caps aggregate gain (interaction
   structure unanalyzed).
2. Regression blindness: self-attribution reliable for fixes, blind to regressions
   (named as clearest future-work direction).

## Connections to our programme
1. Proves thesis: model + harness = agent, measured. Harness capabilities are
   portable ACROSS model families -> mind lives in harness structure.
2. Their decision observability == our prediction_lock.py / RQ-621 holdout
   discipline applied to SE instead of consciousness claims. Independent
   convergent validation of preregistered-falsifiable-edit methodology.
3. Structure-transfers/prose-regresses == our F4 (LLM effect in discourse channel,
   actions identical across model scales). Words are the wrong optimization layer;
   wiring is the right one.
4. Their limits are our differentiators:
   - Regression blindness == gamma=0 monitoring (P-MCFORCE pattern: format present,
     functional override absent). Our RecursiveMonitor w/ gamma measurement is the
     candidate cure: monitor must CHANGE ACTION SELECTION, not emit reports.
   - Non-additivity == missing channel-interaction model. Our Kabbalah gain matrix
     (Part 22) + Tiferet pillar-balance check is a formalism for exactly this.

## Caution (our own discipline)
Benchmark scope: coding tasks only; cross-benchmark rest on SWE-bench alone;
k>=2 rollouts. Strong evidence, not universal. Transfer result worth tracking.

## Action items
- [ ] Port falsifiable-manifest pattern into cognitive_harness.py evolution loop
- [ ] Design gamma>0 regression-foresight experiment (our answer to their #1 limit)
- [ ] Apply channel-gain matrix to predict which component pairs interact (their #2)
