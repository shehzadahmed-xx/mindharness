# reviewer_2_novelty

## Review (Reviewer 2 — Novelty & Significance)

**Overall recommendation: Weak reject / major revision.** There is a potentially interesting evaluation hook buried here, but the framing oversells known components, the ground-truth definition risks circularity, and the effect sizes are too thin to support the "architectural confabulation" narrative.

---

### 1. Novelty: largely recombination, with one salvageable kernel

Each component of the "provenance-bounded cognitive harness" maps onto existing constructs under a new name:

- **Witness ledger** ≈ append-only external memory with provenance
[REASONING]: The user wants me to act as "Reviewer 2" for NeurIPS, specifically a novelty/significance expert, reviewing a paper summary about "witnessed introspection" in language agent systems.

Let me analyze this carefully:

**The paper claims:**
1. LLMs confabulate self-attributions — this is "architectural"
2. A harness with: witness ledger, cause-signed self-model, γ-gated metacognition, witnessed consolidation, role-specialized routing
3. Results showing raw transcripts achieve perfect attribution (1

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
