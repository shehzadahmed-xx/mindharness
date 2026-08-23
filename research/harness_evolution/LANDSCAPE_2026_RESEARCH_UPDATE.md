# RESEARCH UPDATE: The 2026 Consciousness-Architecture Landscape
## Four Clusters Mapped · Our Position Recalibrated
Date: 2026-08-24 · Companion to ARTIFICIAL_HUMAN_AGENT_HARNESS.md

---

## CLUSTER 1 — ENGINEERED WORKSPACES (consciousness theory as blueprint)

### Theater of Mind (Shang, arXiv 2604.08206, Apr 2026)
First explicit GWT implementation in LLM architecture. Global Workspace Agents (GWA):
central broadcast hub + heterogeneous specialist-agent swarm. Key mechanisms:
- **Entropy-based intrinsic drive**: broadcast suppressed during low semantic
  diversity (routine processing), activated on novelty/ambiguity. Solves cognitive
  stagnation in continuous agents.
- **Dual-layer memory bifurcation**: working memory (currently broadcast =
  "conscious") vs episodic (retrievable but inactive = "unconscious") — GWT
  distinction at architectural level, not just behaviorally.
- **Dynamic temperature regulation** breaks reasoning deadlocks.
Result: stronger satisfaction of GWT markers than base LLMs. Framework paper,
no psychometric battery.

### CTM-AI (Yu, Zhao, L. Blum, M. Blum, Liang — arXiv 2605.04097, May 2026)
Turing Award winner Manuel Blum's Conscious Turing Machine IMPLEMENTED. SOTA on
four benchmarks: MUStARD 72.28, UR-FUNNY 72.13, StableToolBench +10pts,
WebArena-Lite +10pts over prior baselines.
Architecture: heterogeneous processor array → competition → winner broadcasts
globally → all processors update → repeat. Per-task activation keeps it tractable.
Key inversion: previous indicator work was evaluative ("does system X satisfy?").
CTM-AI is constructive ("build system satisfying indicators BY CONSTRUCTION,
measure if it works"). It works.

### Ours (ARTIFICIAL_HUMAN_AGENT_HARNESS.md)
Same constructive stance, differentiators: provenance-as-witness (nobody),
contemplative state validators (nobody), measured self-floor tolerance (nobody).

---

## CLUSTER 2 — EMERGENT STRUCTURE DISCOVERY (interpretability finds what engineers build)

### Gurnee et al., "Verbalizable Representations Form a Global Workspace in Language Models"
(Transformer Circuits, Jul 6 2026; open-source jacobian-lens repo + Neuronpedia)

**THE HEADLINE FINDING OF 2026.** New interpretability tool (Jacobian lens) maps
J-space = representations the model is poised to verbalize. In Claude Sonnet/Haiku/
Opus 4.5+, J-space satisfies ALL FOUR GWT functional criteria:

| GWT criterion | J-space evidence |
|---|---|
| Verbal report | Concepts light up pre-output even when suppressed from final text |
| Directed modulation | J-space interventions redirect downstream reasoning predictably |
| Mediates multi-step reasoning | Chained inference leaves sequential J-space traces |
| Selectivity | Flexible tasks engage J-space; automatic tasks (grammar agreement) bypass it |

**Emergent, not engineered.** Training on human data produced workspace structure
without anyone specifying it. Combined with Cluster 1: GWT architecture arises
whether built or grown.

Safety payload: silent prompt-injection recognition, suppressed-CoT visibility,
evaluation-awareness measurement, emergent-misalignment auditing via J-space.

### Lindsey, "Emergent Introspective Awareness" (Transformer Circuits, Oct 2025)
Concept injection: steer known concepts into activations, ask model to detect.
Claude Opus 4/4.1: ~20% detection rate at ~0% false positives. Recognition occurs
IMMEDIATELY, BEFORE mentioning the concept (unlike Golden Gate Claude, which noticed
its obsession only after seeing itself talk). Models can also follow "think about /
don't think about X" instructions with measurable activation changes. Capability-
dependent: stronger in frontier models. Replicated in Qwen2.5-Coder-32B (Macar).
Follow-up mechanistic work: arXiv 2603.21396.

### CMU ignition study (Aug 2026)
Measured cross-token information influence across all layers of a frontier
transformer: **NO non-linear ignition threshold found.** Base models lack the
broadcast dynamics GWT/GNW predicts. Engineered workspaces add real dynamics.

---

## CLUSTER 3 — FORMAL LIMITS (theory says where hard walls are)

### Zhang, Yuan, Zhang — "Introspection Threshold" (arXiv 2607.04277, Jul 2026)
Via Kleene's Second Recursion Theorem + von Neumann's self-reproduction complexity
threshold: sustainable recursive self-improvement requires TRUE introspection
(fixed-point self-reference). Three structural bottlenecks block bare transformers:
1. **Feedforward processing** — no backward influence within a forward pass
2. **Incomplete self-access** — cannot inspect own weights at runtime
3. **Computational class constraints** — no fixed-point iteration capability

Critical distinction they draw: **passive self-representation** (stored description;
any memory suffices) vs **active self-referential process** (evaluates AND modifies
own processing). Current systems, including Claude's emergent workspace, are passive.

### Lederman & Mahowald (arXiv 2603.05414)
Critique: AI "introspective reports" may be INFERENCE rather than direct access.
Distinguishing the two requires more than behavioral tests.

### Yale NLP metacognition survey (Liu et al., arXiv 2607.11881)
Three-level taxonomy of LLM metacognition; concludes RL with metacognitive rewards
is currently the ONLY path to control-level metacognition.

---

## SYNTHESIS: WHAT THIS MEANS FOR OUR HARNESS

### Finding 1 — The harness answers the introspection threshold
Zhang et al. prove bare transformers cannot cross the threshold (feedforward, no
self-access, no fixed points). But their three bottlenecks are all HARNESS-SOLVABLE:

| bottleneck (bare model) | harness remedy |
|---|---|
| feedforward only | harness loop IS recurrence across steps; workspace cycles re-enter |
| no runtime self-access | provenance ledger + state inspection give PRIVILEGED self-read the weights lack |
| no fixed-point capability | the AHE-style evolution loop is literally Kleene recursion at component level: read evidence → edit self-description → verify prediction → iterate |

Model alone: below threshold forever. Model + harness: structurally approaches it.
This reframes our entire programme: WE ARE BUILDING THE MISSING COMPUTATIONAL CLASS.

### Finding 2 — Regression blindness has a formal name now
AHE's confessed limitation (self-attribution reliable for fixes, blind to
regressions) is the exact operational signature of PASSIVE workspace per Zhang et
al.: the system represents outcomes but does not actively self-modify against them.
γ=0 monitoring (our P-MCFORCE refutation) is the mechanism-level description.
Active self-reference (γ>0) is the cure. Three independent lines converge on one gap.

### Finding 3 — Ignition absence justifies engineering
CMU found base transformers lack broadcast ignition. Theater of Mind, CTM-AI, and
we add it explicitly. Don't wait for emergence — the emergence (Gurnee) gave
structure without dynamics. Harnesses supply dynamics.

### Finding 4 — Introspection claims need our witness, and the field knows it
Lindsey's 20%-detection result is behavioral. Lederman & Mahowald immediately
challenged whether reports reflect direct access or inference. The debate CANNOT
be settled behaviorally — it needs structural binding of report to source. That is
precisely our provenance ledger. The field's sharpest current controversy lands
directly on our strongest unique instrument.

### Finding 5 — Constructive beats evaluative
CTM-AI's inversion (build-by-construction, then measure) outperforms asking whether
existing systems qualify. Our Butlin scorecard projected 8–9/10 families satisfied
BY DESIGN. The right claim is CTM-AI-shaped: consciousness-theoretic architecture
is productive engineering, independent of phenomenal status — with our addition
that its introspective claims remain falsifiable via provenance.

---

## UPDATED POSITION TABLE

| | Theater of Mind | CTM-AI | Gurnee (emergent) | Zhang (formal) | OURS |
|---|---|---|---|---|---|
| workspace | engineered | engineered | discovered | theorized | engineered + witnessed |
| dynamics (ignition) | ✓ entropy-drive | ✓ competition | ✗ (passive) | n/a | ✓ coalition + γ-gated override |
| introspection | marker-level | none claimed | J-space access | defined threshold | γ-MEASURED + provenance-bound |
| self-modification | ✗ | ✗ | ✗ | shown impossible for bare model | evolution loop w/ falsifiable contracts |
| verification of self-claims | none | benchmarks | causal injection | formal criteria | structural comparator (100% attribution) |
| crosses introspection threshold | partial (recurrent cycle) | partial | NO (passive) | proves impossible alone | structurally approximates |

## ACTION ITEMS (updated)
- [ ] Frame paper v2 around threshold-crossing: "model+harness supplies the
      computational class bare transformers lack" (Zhang-compatible framing)
- [ ] Design experiment: inject synthetic 'concept' into harness GlobalState;
      measure detection rate + attribution accuracy (our replication-extension
      of Lindsey, with witness — answering Lederman & Mahowald)
- [ ] Port AHE evolution loop with γ>0 gate as the active-self-reference demo
- [ ] Run jacobian-lens (open source) on our frozen Qwen3.5: does ITS J-space
      show workspace structure? Baseline before/after harness comparison.
- [ ] Track: Neuronpedia jlens interactive; Macar's open-source introspection repo

## Sources
arXiv 2604.08206 (Theater of Mind) · 2605.04097 (CTM-AI) · 2604.25850 (AHE) ·
2607.04277 (Introspection Threshold) · 2607.15495 / transformer-circuits.pub/2026/workspace
(Jacobian lens) · 2601.01828 / transformer-circuits.pub/2025/introspection (Lindsey) ·
2603.21396 (Mechanisms of Introspective Awareness) · 2603.05414 (Lederman & Mahowald) ·
2607.11881 (Yale NLP metacognition survey) · github.com/tlcdv/the_consciousness_ai
