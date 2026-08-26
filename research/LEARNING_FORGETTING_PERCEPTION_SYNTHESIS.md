# HOW LLMS LEARN, FORGET, AND PERCEIVE THE WORLD
## A Comprehensive Synthesis Connecting to the SpringFish Programme

---

## 1. HOW LLMS LEARN

### 1.1 Pretraining: Compression of Human Knowledge
LLMs learn by predicting the next token across trillions of words. This forces them to encode grammar, facts, reasoning patterns, social dynamics, physical intuitions — everything needed to minimize prediction error. The result is not a database but a **compressed generative model of human text**, which implicitly encodes a model of the world that produced that text.

### 1.2 Fine-tuning: Specialization with Risk
Supervised fine-tuning adapts the base model to specific tasks. But every weight update risks **catastrophic forgetting** — overwriting previous capabilities to make room for new ones. This is the plasticity-stability dilemma.

### 1.3 In-context learning: Temporary adaptation without weight changes
LLMs can adapt behavior based on examples in their prompt without any weight update. This is the closest thing to "learning" that doesn't risk forgetting — but it's ephemeral, disappearing when the context window clears.

### 1.4 Continual learning: The frontier problem
Maintaining and refining knowledge across months of operation without losing prior capabilities. Four approaches:
- Regularization (EWC): protect important weights during new training
- Architecture (Titans): dedicated long-term memory module alongside attention
- Replay: periodically re-expose model to past examples
- Token-space: manage context window and external memory instead of weights

---

## 2. HOW LLMS FORGET

### 2.1 Catastrophic forgetting
New learning overwrites old knowledge. Not gradual decay but sudden collapse when weight updates shift shared parameters. The instruction vector hypothesis explains this mechanistically: fine-tuning on new tasks suppresses the computation graph associated with prior instructions.

### 2.2 Why our harness solves what fine-tuning cannot
Our witness ledger is append-only — nothing is ever overwritten. Skills are added but never removed except through explicit culling after measured failure. The self-model uses CAS fencing so revisions can't silently overwrite each other. Memory decays through retrieval scoring, not through weight updates that destroy other knowledge.

This is the structural advantage of harness-level learning over weight-level learning: **the harness can add without subtracting because it operates in a different medium** (files and state vs. parameter updates).

---

## 3. HOW LLMS PERCEIVE THE WORLD

### 3.1 Perception as pattern completion
LLMs don't see images or hear sounds. Their entire perceptual input is tokens — discrete symbols representing human-generated descriptions of reality. What they "perceive" is patterns in these symbols: statistical regularities that let them predict what comes next.

### 3.2 Emergent world models
Despite training only on text, LLMs develop internal representations that encode spatial relationships, temporal sequences, causal structures, and social dynamics. These are not explicitly programmed — they emerge as the most efficient way to compress the patterns in training data.

But these world models are:
- **Implicit**: encoded in weight configurations, not explicit data structures
- **Incomplete**: gaps where training data had no coverage
- **Unstable**: different prompts activate different subsets of the representation
- **Unverifiable**: no built-in mechanism to check whether the world model matches reality

### 3.3 The grounding gap
Human perception is grounded in sensorimotor experience — you know what "red" means because you've seen it. LLM perception is grounded in *descriptions* of experience — "red" is a token that co-occurs with certain contexts. This grounding gap is why models confabulate: their world model has no direct connection to the reality it describes.

---

## 4. HOW THIS CONNECTS TO OUR HARNESS

### 4.1 The harness adds what pretraining cannot provide

| what's missing | our solution |
|---|---|
| persistent memory | five-type store + witnessed consolidation |
| consequence loop | IrreversibleDamage + energy/fatigue |
| self-knowledge | cause-signed CAS self-model |
| verifiable claims | provenance ledger |
| metacognition | γ-gate with override-rate measurement |
| emotional regulation | bounded affect middleware |

### 4.2 The harness doesn't retrain the model

This is critical: our approach operates entirely at the state/memory/architecture level, never touching model weights. This means:
- No catastrophic forgetting (nothing is overwritten)
- No need for original training data
- Backend-agnostic (works with any frozen model)
- All changes are auditable (cause-tagged)

### 4.3 The witness prevents non-robust feature capture

Ilyas et al. proved that adversarial examples come from non-robust features: genuinely predictive patterns that are incomprehensible to humans. Similarly, unwitnessed self-attribution uses non-robust features of internal state that are predictive but don't correspond to reality. The narrator isn't lying — it's using the most available signal, which happens to be wrong.

The witness separates robust from non-robust by requiring every claim to reference its evidence. Non-robust claims (fluency-based, coherence-based) fail the check; robust claims (record-bound) pass.

---

## 5. KEY PAPERS ON LEARNING, FORGETTING, AND PERCEPTION

| paper | finding | relevance |
|---|---|---|
| Ilyas et al. NeurIPS 2019 | Adversarial examples from non-robust features | Narrator uses non-robust features |
| Luo et al. arXiv:2308.08747 | Catastrophic forgetting during LLM fine-tuning | Why we don't fine-tune |
| Huang et al. ACL 2024 | Self-Synthesized Rehearsal for continual learning | Model generates own rehearsal data |
| Kirkpatrick et al. PNAS 2017 | Elastic Weight Consolidation | Protects important weights |
| Google Titans NeurIPS 2025 | Dedicated long-term memory module | Architecture-level memory |
| Seth, Being You (2021) | Consciousness as controlled hallucination | Perception = constrained prediction |
| Clark, Surfing Uncertainty (2016) | Hierarchical Bayesian inference in brain | PP framework |
| Nayebi UAI 2026 | Selection theorems for competent agents | Structure is necessary |
| Gurnee et al. 2026 | Emergent workspace in Claude | Structure exists without engineering |
| Macar et al. 2603.21396 | Introspection underelicited (+75%) | Latent capacity needs structure |
| Panickssery NeurIPS 2024 | Self-recognition correlates with bias (r=0.94) | Unwitnessed improvement corrupts |

---

*All findings cited from primary sources retrieved via web search during this session.*
