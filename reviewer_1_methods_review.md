# reviewer_1_methods

# Review — Recommendation: Reject

This summary reads as a proof-of-concept blog post dressed up as a NeurIPS paper. The statistical reporting is amateurish, the central construct is circular, and the headline claims contradict the paper's own numbers. Weaknesses, exhaustively:

## Statistical gaps and invalid tests

1. **No inferential statistics whatsoever.** Not a single p-value, confidence interval, standard error, or formal hypothesis test appears anywhere. Claims like "P1 passed (+0.083)" and "gpt-oss +0.167" are naked point estimates with zero uncertainty quantification. This alone is disqualifying at NeurIPS.
2. **"Zero variance" is a vacuous robustness claim.** Five seeds with (presumably) deterministic/greedy decoding produce identical outputs *by construction*. Reporting zero variance across seeds as evidence of stability is statistically illiterate — the seeds never sampled anything.
3. **Effect sizes are quantized micro-counts.** +0.083 ≈ 1/12, +0.167 ≈ 2/12, +0.111 ≈ 1/9, +0.278 �
[REASONING]: The user wants me to act as Reviewer 1 for NeurIPS, a harsh methods/statistics expert, reviewing this paper summary. I need to list every weakness in numbered format covering:
- Statistical gaps and invalid tests
- Missing controls and confounds
- Sample size and power issues
- Overclaims not supported by evidence
- Methodological flaws

Let me analyze the paper summary carefully.

Title: "Witnessed Introspection in Assembled Language-Agent Systems: A Provenance-Bounded Cognitive Harness for Hon

---


TITLE: Witnessed Introspection in Assembled Language-Agent Systems: A Provenance-Bounded Cognitive Harness for Honest Self-Attribution

ABSTRACT: Large language models confabulate self-attributions. We show this is architectural: across 120 probes on a frozen model, raw transcripts achieved deterministic perfect attribution (1.000, zero variance) while harnessed arms converged deterministically to wholesale denial (0.667, zero variance). We present a provenance-bounded cognitive harness — witness ledger, cause-signed self-model, γ-gated metacognition, witnessed consolidation, role-specialized routing. A composite configuration passed both preregistered performance axes; anchoring confirmed directionality across architectures.

RESULTS:
- Raw arm: perfect origin discrimination (1.000, 5 seeds, zero variance)
- Harnessed arm without ledger access: always-no strategy (0.667, deterministic)
- With-check arm: converts denials to correct attributions when ledger queried
- Composite (ox-alpha gen + gpt-oss validate + nemotron monitor): P1 passed (+0.083), P2 passed
- Living session: 40 turns complete, coverage 100%, SM revised 7 times
- Cross-model anchoring: gpt-oss +0.167, ox-alpha +0.278, nemotron +0.111
