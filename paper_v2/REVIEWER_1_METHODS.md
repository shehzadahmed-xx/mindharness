# Reviewer 1 — Methods & Statistics Assessment

## A. Statistical Invalidity

1. **"Zero variance" is a tautology, not a finding.** With a frozen model under (presumably) greedy decoding, identical inputs yield identical outputs *by construction*. Reporting "deterministic, zero variance" as an empirical result confuses algorithmic determinism with a population-level effect. There is nothing to test; the absence of variance reflects the decoding regime, not the phenomenon.

2. **No inferential statistics whatsoever.** A comparative claim (1.000 vs. 0.667) is made across arms with zero reported tests, confidence intervals, or bootstrap resampling *over probes* (the only defensible unit of resampling here). Two point estimates do not constitute evidence of a difference.

3. **Unit-of-analysis confusion.** Are the 120 probes items, sessions, or runs? "Converged deterministically to 0.667" — exactly 2/3 — smells like a coarse denominator (e.g., 80/120, or worse, 2/3 of a handful of aggregated bins). Without the raw per-probe distribution, the reader cannot distinguish stable behavior from aggregation artifacts.

4. **Ceiling effect.** A raw-arm score of exactly 1.000 means the task cannot discriminate anything above chance-plus-trivial. Either the probe set is too easy, leaked, or the metric is degenerate. Perfect scores demand a contamination audit before any interpretation.

5. **Spurious precision.** Three-decimal reporting of quantities claimed to have zero variance implies measurement resolution the design cannot support.

6. **No power analysis or sampling justification.** Why 120 probes? How were they drawn — random, hand-curated, adversarially constructed? Selection procedure unstated; with hand-picked probes, both 1.000 and 0.667 are unfalsifiable.

7. **Multiplicity nowhere addressed.** Multiple harness components (≥5), a "composite configuration," two "performance axes," multiple architectures — how many configurations were evaluated before one "passed both"? This is textbook garden-of-forking-paths. Report the full config × axis matrix or the claim is void.

## B. Missing Controls

8. **No sham-harness control.** To attribute effects to the harness's *content* (ledger, signatures), you need a structurally identical harness with shuffled/placebo entries. Absent, format-constraint effects are fully confounded with the proposed mechanism.

9. **No naive baselines.** Simple prompts ("cite your source"), chain-of-thought, or self-consistency baselines are absent. A five-component harness must beat trivial interventions to justify its complexity.

10. **No chance level stated.** What does 0.667 mean relative to base rates of denial in the corpus? If models deny 60% of the time unprompted, 0.667 is nothing.

11. **No ground-truth labeling protocol.** "Veridical knowledge" requires gold labels. Who annotated them? Inter-rater reliability? If the scorer is an LLM (especially the same family), self-preference bias is unaddressed.

12. **No contamination check.** Were transcripts or near-duplicates in pretraining data? For a frozen model, this is checkable and mandatory before claiming "attribution."

13. **Single decoding configuration.** Temperature, top-p, seed policy unstated. All determinism claims collapse if any stochasticity was present, and generalize nowhere even if it wasn't.

## C. Internal Contradictions

14. **The headline result contradicts the thesis.** Sentence 1: models *over*-claim credit (confabulation). Sentence 3: raw transcripts achieve "deterministic perfect attribution (1.000)." If raw performance is perfect, where is the confabulation? Either the metric does not measure what its name says, or the results refute the motivating claim. This must be resolved before anything else.

15. **"Across architectures" vs. "a frozen model."** The abstract asserts architectural generality ("this is architectural"; "across architectures") while describing exactly one model. How many architectures, which ones, how many probes each? As written, this is self-refuting.

16. **Harnessed arms fail, yet a composite "passes both axes."** Arms converge to "wholesale denial" (0.667), yet the composite passes preregistered performance. These statements are irreconcilable without knowing which configs were tested and how many failed — which returns us to weakness #7.

## D. Overclaims

17. **"Arch