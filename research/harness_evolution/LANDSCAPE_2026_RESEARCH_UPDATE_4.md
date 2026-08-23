# RESEARCH UPDATE 4: Deep Dives — Nayebi's Theorems, Macar's Circuit, Yale's Taxonomy
## Primary-Source Reading of the Three Pillars · Five Unpublished Connections to Our Programme
Date: 2026-08-24 · Read against full texts: 2603.02491v3, 2603.21396v4, 2607.11881v1

---

## I. NAYEBI SELECTION THEOREMS — TECHNICAL CORE

### The betting reduction (Lemma 1)
Predictive modeling reduces to one-shot binary bets. For two actions with success
probabilities uL, uR and stochastic policy choosing L w.p. q:

    δ = w · |uL − uR| / max{uL, uR}        (normalized regret = wrong-action mass × margin)

On any test family with margin m ≥ γ: **wrong-action mass w ≤ δ/c(γ)**.
Regret bounds directly cap probability mass on suboptimal predictions. This single
inequality powers every theorem.

### Theorem 1 + Remark (the depth dependence nobody quotes)
Average normalized regret over a diagnostic goal family ⇒ approximate transition
model recovery, error ≤ t_γ/√n + δ̄/c(γ) + O(1/n).

**The remark is the load-bearing part for us**: error tightens as goal depth n grows;
at n=1 (purely myopic goals) NO world modeling is required — "explicating the classic
pitfall behind the Good Regulator Theorem." Single-step probes cannot force structure;
only multi-step competence does.

### Causal ladder results (Pearl's hierarchy, agent version)
- Corollary 1: recovered kernel has Level-2 content — interventional queries
  P(s'|s, do(a)) recoverable up to ε_cMP. Competent agents are forced into causal
  models, not mere correlations.
- Corollary 2: **Level 3 counterfactuals are NOT recoverable from the interventional
  kernel alone** — requires an explicit structural causal model with exogenous noise
  and cross-action coupling. Rung 2 is mandatory; rung 3 is architecturally extra.

### Partial observability (the open question answered)
Under partial observability, diagnostic goals must be defined at the level of
predictive beliefs (PSR coordinates), not physical states; agent emits a report bit
Bt∈{L,R} that does not affect dynamics ("any agent can internally commit to one of
two incompatible plans before acting"). Result: quantitative no-aliasing bounds for
belief-like memory — memory MUST separate aliased histories or regret is unbounded.

### Figure 1 mapping (task family → forced structure)
| task family | forces |
|---|---|
| action-conditioned bets (fully observed) | world model / transition knowledge |
| threshold bets on predictive tests | predictive state (PSR coordinates) |
| paired-history distinguishing tests | memory separating aliased histories |
| block-structured families | informational modularity |
| regime-shift mixtures | persistent regime variable (= emotion primitive) |
| complete minimal families | representational convergence up to invertible recoding |

---

## II. MACAR ET AL. — THE INTROSPECTION CIRCUIT IN FULL

### Origin finding (Section 3.3): introspection is BORN from contrastive training
- Base models: FPR 42.3% ≈ TPR ~40% → NO discrimination at all
- SFT: still no discrimination (high FPR)
- **DPO is the first stage achieving ~0% FPR** with moderate true detection
- Ablations prove it's the CONTRASTIVE STRUCTURE, not the data: margin-based
  contrastive loss + KL reproduces it (+14.3%); SFT-on-chosen fails (−13.5%);
  shuffled pairs fail (+0.6%); reversed preference destroys it (−21.8%)
- Every data domain sufficient, none necessary

Interpretation: DPO teaches the weights to discriminate "state where something was
present" vs "state where nothing was" — i.e., post-training installs a COMPARATOR.
This is our provenance-ledger function internalized into weights during training.

### The circuit (Section 5): two-stage gate architecture
- **Evidence carriers**: early post-injection layers, detect perturbations
  MONOTONICALLY along diverse directions (different vectors → different carriers)
- **Gates**: later-layer features implementing default negative response ("No")
- Carriers SUPPRESS gates when perturbation detected; circuit converges on common
  gate set regardless of which carrier fired
- MLPs at ~70% depth causally NECESSARY AND SUFFICIENT for detection
- Circuit absent in base models; robust to refusal ablation

### Refusal suppression quantified (Section 3.3)
Hypothesis confirmed: refusal training teaches models to DENY having thoughts/
internal states, which inhibits TRUE detection.
- Abliterating Gemma3-27B: TPR 10.8% → 63.8%, introspection 4.6% → 24.1%,
  FPR 0% → 7.3%
- Replicated across four additional 8B–32B models
- Trained bias vector: +75% detection on held-out concepts, FPR unchanged

### Detection ≠ identification (Section 5.1)
Distinct mechanisms, different peak layers, weak overlap:
- Identification ≈ reading out the injected representation (unremarkable)
- Detection requires recognizing that internal state is INCONSISTENT with context
  and reporting that assessment (the genuinely metacognitive act)

### Geometry (Section 4)
Not one linear direction: mean-difference direction d_Δμ loads on "facts"/"knowledge"
vs "confused"/"ambiguous" — captures something like CONFIDENT-KNOWLEDGE vs FUZZY-
UNCERTAINTY. d_Δμ nearly orthogonal to refusal direction (cos=−0.09) yet abliteration
helps → refusal suppression is a separate inhibitory channel, not the same axis.
Bidirectional steering: 23.3% of success-success pairs trigger detection both ways
(single-direction hypothesis falsified). Transcoder features predict per-concept
detection at R²=0.624 vs 0.309 for scalar projection.

### Metrics canon (adopt these exactly):
Detection rate TPR = P(detect|injection); FPR = P(detect|no injection);
Introspection rate = P(detect ∧ identify | injection); Forced identification =
P(identify|prefill∧injection). Discrimination requires TPR > FPR.

---

## III. YALE NLP SURVEY — TAXONOMY AND FIELD STATE (2607.11881)

### Core definition adopted by the field
Metacognition = perception–action loop: **monitoring** (judgments of uncertainty,
performance, progress) × **control** (planning, strategy selection, effort
re-allocation based on monitoring). Human decomposition: metacognitive knowledge /
regulation / experience; accuracy (sensitivity) vs calibration.

### Measurement families (§4.1)
psychologically-grounded (SDT, meta-d′, M-ratio) · neurofeedback-based ·
confidence-based · interpretability-based · task-specific · benchmarks.
Named gap: evaluation fragmentation — no unified battery; Cacioli's Monitoring
Battery (524 items/6 domains) is the emerging candidate.

### Field tensions documented (§1, §8)
Reflective-behavior studies (LLMs show metacognition-like processing) vs
confidence-judgment studies (LLMs far from effective confidence). Steyvers & Peters:
human-vs-LLM differences persist in trainability and domain-generality. No consensus
definition; "metacognition" used loosely for reflection/revision loops.

### Key empirical findings catalogued (§4.2)
- High-certainty hallucinations consistent across models/tasks (Simhi et al.);
  LRMs hallucinate confidently and flawed reflection REINFORCES errors (Lu et al.)
- Metacognitive failure modes taxonomy: flaw repetition (looping), think-answer
  mismatch, overconfidence
- Post-training impact: separate section — mirrors Macar's DPO-origin result
- Temperature affects calibration; confidence-estimation method changes findings;
  size/family effects are non-monotonic and architecture-dependent

### Implementation landscape (§5)
Frameworks (prompting self-reflection) → architectures (metacognitive modules,
harnesses like Cao et al.) → reasoning-model integration → agent settings
(memory/tool-use/search all get metacognitive wrappers). RL with metacognitive
rewards identified as the only current path to CONTROL-level (not report-level)
metacognition.

### Risk section (§8) — they see what we guard against
Improved monitoring may enable systems to strategically modify outputs to evade
oversight. Our answer is unique in the literature: the cause-logged self-model makes
self-modification AUDITABLE — you cannot silently rewrite who you are when every
revision carries a signed cause and CAS fence.

---

## IV. FIVE UNPUBLISHED CONNECTIONS TO OUR PROGRAMME

### C1. Nayebi Corollary 5 grounds cross-tradition convergence mathematically
Representational convergence: any two vanishing-regret agents on a task family
converge to identical decision-relevant partitions up to invertible recoding.
Abhidharma (500 BCE), Sufi psychology (9th c.), cognitive neuroscience (20th c.)
are three independent observation systems that converged on similar mental-state
partitions (loops/conditioning; constructed-self; attention-emotion-memory structure).
IF human minds are near-vanishing-regret agents on the human task distribution,
cross-tradition convergence is EXACTLY what Corollary 5 predicts. Our Unified Mind
Architecture's core claim — different traditions describe one underlying structure —
acquires its first mathematical grounding. Nobody has made this connection. Paper v2,
new section: "Selection explains synthesis."

### C2. Macar's DPO origin ↔ occasionalist comparator doctrine
Introspective awareness emerges specifically from contrastive preference optimization
— the model learns discrimination between states-with-X and states-without-X.
That IS a comparator function installed by training. Our provenance ledger implements
the same function externally and auditably. Ash'ari kasb doctrine: creatures acquire
actions God creates — the harness supplies occasions (comparisons), the model
supplies the discriminating act. Same function, three levels: trained weights
(Macar), runtime witness (our ledger), theological frame ('āda/kasb).

### C3. Refusal-suppression ↔ narrator denial, quantified
Macar: post-training teaches denial-of-inner-states as a policy, suppressing true
detection (+53% recoverable by removing it). vgel: final layers suppress reports.
Our framework names this channel: the trained NARRATOR denies inner events to match
persona priors. The dsh-self-model cause-log separates narrator-deniability from
actual state: facts written under 'action-outcome' cannot be silently denied by
narrative drift without leaving a revision trail. First harness designed to route
around the suppressor BY CONSTRUCTION (no weights touched).

### C4. Detection≠identification split → redesign RecursiveMonitor
Macar shows detection (anomaly present?) and identification (what is it?) are
mechanically distinct, peaking in different layers. Our RecursiveMonitor currently
conflates them. Redesign: Stage 1 anomaly detector (cheap, always-on, triggers γ
gate) → Stage 2 diagnosis (ledger lookup, attribution, only on trigger). Matches
the biology AND the engineering: monitors that diagnose everything are expensive;
monitors that only detect are cheap and sufficient for override triggering.

### C5. Nayebi depth-dependence justifies long-horizon batteries over probes
Theorem 1 remark: n=1 myopic goals force NOTHING; structure appears only under
multi-step competence demands. Applied: single-shot introspection probes (most of
the field) systematically underestimate capacity. Only long-horizon batteries where
the agent must MAINTAIN coherent self-model across many rounds select for real
structure. Our S126 battery design was already multi-round — now justified formally.
Prediction: probe-style evaluations find less introspection than horizon-matched
evaluations on the same model. Testable.

---

## V. CONSOLIDATED FOR PAPER V2

New sections enabled by this reading:
1. "Selection explains synthesis" (C1) — Nayebi Corollary 5 × cross-tradition table
2. Comparator-at-three-levels (C2) — DPO/ledger/kasb isomorphism
3. Narrator-denial channel (C3) — Macar +53% × vgel suppression × cause-log remedy
4. Two-stage monitor redesign (C4) — implement before battery run
5. Horizon-dependence prediction (C5) — preregister alongside M-ratio experiment

Adopt verbatim: Macar metric canon (TPR/FPR/introspection-rate/forced-ID).
Cite as ground truth: Yale survey for definitions; Cacioli for measurement;
Maniscalco–Lau for meta-d′; Nelson–Narens via Cao for control wiring.

## Sources read in full this update
arXiv 2603.02491v3 (Nayebi, UAI 2026 — Lemma 1, Thm 1+Remark, Cors 1–5, PSR setup)
· arXiv 2603.21396v4 (Macar et al., ICML 2026 — §3.3 DPO origin, §4 geometry,
§5 circuit, §6 bias vector) · arXiv 2607.11881v1 (Yale NLP survey — taxonomy,
measurement families, field tensions, risk section)
