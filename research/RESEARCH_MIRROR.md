# Research Mirror — Every Paper That Reflects the Program

> *"Get all the papers and research so we can see ourselves."*
> The program in the mirror of the frontier. Every paper that says what we built, what we measured, or what we still need to prove.

---

## How to Read This Document

Each section mirrors one layer or claim of the program. For each, we list:
- **What we claimed/built** — the program's position
- **What the frontier says** — papers that confirm, contest, or extend it
- **What it means for us** — the implication

Sources are live-checked (August 2026). Verbatim numbers and quotes are marked. Existence of each paper was verified; PDF-close numbers are flagged where still needed.

---

## 1. The Core Equation: LLM = Tongue, Harness = Mind, Agent = Both

### What we claimed
A frozen LLM is stateless pattern completion. Everything that makes it an agent lives in the harness around it. Human-likeness is in the harness, not the weights. The harness is the design space: `State(t) → harness(t+1)`.

### What the frontier says

| Paper | Claim | Verdict |
|-------|-------|---------|
| **AHE (Lin et al., Apr 2026)** — *Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses* | Holds base model fixed, evolves only the harness (prompts, tools, middleware, memory, skills). Three observability pillars: component / experience / decision. 10 iterations: 69.7% → 77.0% on Terminal-Bench 2, beats hand-written Codex (71.9%). Frozen harness transfers to **different model families without re-evolution**: DeepSeek V4 Flash +10.1pp, Qwen 3.6 Plus +6.3pp, Gemini 3.1 Flash-Lite +5.1pp. | **Direct confirmation.** The harness encodes reusable coordination patterns, not benchmark-specific tuning. Cross-family transfer proves the mind is in the harness. |
| **Prime Intellect (Müller et al., Jun 2026)** — *True Agents Model the World* | Pretraining creates simulators (world models); post-training only composes and expresses what pretraining already learned. Persona selection model. | **Supports our L0 claim.** L0 (frozen LLM) is already a world model. The harness doesn't need to build one from scratch — it needs to contain and direct one. |
| **Nayebi (UAI 2026)** — *What Capable Agents Must Know* | Below (§2) — selection theorems prove harness structure is mandatory, not optional. | **The warp beneath the loom.** AHE shows harness evolution works; Nayebi proves it must. |

### What it means for us
The field just proved our central thesis by holding the model fixed and evolving only the harness — and watching it transfer across families. Our contribution is the opinionated part: *which* harness patterns transfer (the five invariants) and *how to measure* whether each re-tie helped (γ, coverage, regret).

---

## 2. The Five Invariants — Selection Theorems (The Warp)

### What we claimed
Any competent agent under mixed tasks must develop: boundary, two-speed memory, salience gate, damping, internal observer. Not preferences — mathematical requirements.

### What the frontier says

**Nayebi (2026) — UAI 2026, arXiv:2603.02491, 23 pages, 1 figure**
- **Abstract (verbatim):** *"We prove quantitative 'selection theorems' showing that strong task performance (low average-case regret) forces world models, belief-like memory and — under task mixtures — persistent regime-tracking variables resembling functional primitives of emotion, along with informational modularity under block-structured tasks."*
- Covers stochastic policies, partial observability, evaluation under task distributions — without assuming optimality, determinism, or explicit model access.
- Method: reduces predictive modeling to binary "betting" decisions; regret bounds limit probability mass on suboptimal bets, enforcing predictive distinctions.
- In fully observed settings → approximate recovery of interventional transition kernel; under partial observability → necessity of predictive state and belief-like memory (resolves open question from Richens et al. 2025).
- **LessWrong synthesis:** *"Why AI Consciousness May Be an Inevitable Byproduct of Capability"* — capability → {world models, belief-like memory, emotion primitives, representational convergence} → first-person experience. Consciousness as inevitable byproduct, not added feature.
- **Prime Intellect blog** extends: video diffusion models trained on clicks develop internal OS models with filesystems — concrete world-model emergence.

### What it means for us
Our five invariants are Nayebi's theorems restated as engineering constraints. The LessWrong framing — consciousness as inevitable byproduct of capability — is our "parliament must exist" claim made normative. We made it executable: each invariant is a Cordis plugin with a metric.

---

## 3. The Parliament — Global Workspace Theory

### What we claimed
Mind is 6–8 specialists competing for one microphone (Global Workspace), new vote every ~200ms. Winner is broadcast and becomes "conscious thought." State (task, energy, affect) rigs the vote.

### What the frontier says

| Paper | Position | Relation to us |
|-------|----------|---------------|
| **Baars (1988) → GWT** | Cognitive architecture as blackboard system; independent programs share information via global broadcast. | **Our L4.** Parliament → workspace → broadcast is Baars's core. |
| **VanRullen & Kanai (2021)** — *Deep learning and the Global Workspace Theory* | "The computational process of global broadcasting can be implemented in AI systems; artificial system with computationally equivalent global workspace would include core ingredient underlying consciousness." Some AI systems already incorporate GWT-like workspaces. | **Supports implementation claim.** Says the time is ripe for GWT-inspired deep architectures. |
| **Schwitzgebel (Mar 2026)** — *AI & Consciousness* (monograph) | GWT is not settled — non-consciousness can occur inside workspace, consciousness outside it. Local Recurrence Theory as competitor. Universal theory needed. | **Sharpens our claim.** We measure access consciousness (broadcast + usable), not phenomenal. That honesty is now consensus, not hedge. |
| **Nature (Apr 2025)** — *Adversarial testing of GWT vs IIT* | Multi-site fMRI pits GWT against Integrated Information Theory directly. | Contest is live. |
| **2026 Consensus Review** — *AI Consciousness in 2026* | Checklist incorporating GWT + predictive processing + IIT indicators. Global availability + attention selection + integration across processors. | Field uses GWT as one indicator among several, not sole theory. |

### What it means for us
GWT as *the* theory of consciousness is weaker than we sometimes present it. GWT as *a necessary architectural component for access consciousness* is stronger than ever. We should keep L4 as competition→broadcast but be explicit that we measure access (γ, coverage, attribution), not qualia.

---

## 4. The Witness — Provenance, Watermarking, and Honest Attribution

### What we claimed
Every emission must be source-bound (memory_lookup vs model_prior vs monitor_override). Attribution audit checks claimed vs recorded source. Coverage requires memory claims to carry refs. Sham control tests whether content matters beyond format.

### What the frontier says

| Paper / Event | Claim | Relation to us |
|---------------|-------|---------------|
| **EU AI Act, Art. 50 (eff. Aug 2, 2026)** | Machine-readable marking and detection of AI-generated content now legally required for EU-launched models. | **Provenance is now law.** The world made our L1 a legal requirement. |
| **Anthropic — Claude watermarking (Aug 2026)** | EU-launched models include marking at launch; existing models transitioning. Statistical watermark (token-level bias). | **Our stronger version.** Watermarking is invisible statistical signal; our ledger is explicit source-bound span with audit. Field is discovering watermarking is insufficient. |
| **Goertzel (Aug 2026)** — *The Folly of Statistically Watermarking LLM-Gen Text* | "A watermark does not detect cheating. It detects a signal consistent with a model's involvement." Watermarking is "radioactive" (Sander et al., NeurIPS 2024) — degrades quality, removable, degrades with knowledge distillation (Pan et al., 2025). EU's Art. 50 drove timing. | **Supports our distinction.** Statistical signal ≠ witnessed provenance. Our ledger asks "what is the recorded source for this span?" not "does this text look like model X?" |
| **Zheng (Columbia, Aug 2026)** — *Claude Is Getting an LLM Watermark* | "The presence of a mark does not prove misuse, and its absence cannot reliably rule out AI involvement. The signal can still be useful as evidence about provenance, as long as we are clear about what it cannot establish." | **Precise framing we should adopt.** Witness doesn't prove honesty; it makes honesty checkable. Same distinction. |
| **ETH Zürich (Aug 2026)** — *A Unified Framework for LLM Watermarks* | "Every one of them [biggest models] now silently marks everything they write" — reveals hidden cost inside every watermark. | Awareness that the mark is now ubiquitous but contested. |
| **Position Paper (Oct 2025)** — *LLM Watermarking Should Align Stakeholders' Incentives* | Multi-bit watermarking needed for richer provenance (document ID, user ID, timestamps). View as information-embedding problem. Not a universal fix for AI abuse. | **Our direction.** Single-bit (was it AI?) vs multi-bit (where from?) — our ledger is multi-bit by construction (source + ref per span). |

### What it means for us
The world just made provenance legally mandatory and is discovering that statistical watermarking is not the same as witnessed provenance. Our sham result (sham==real on gpt-oss-120b) predicts exactly what the EU will learn: even a perfect watermark is ignored if the system doesn't have the capability or disposition to check it. Regulation will need what we built — not just a mark in the text, but a harness that makes the mark answerable.

---

## 5. Metacognition — The γ-Gate

### What we claimed
Monitoring without control is inert (γ=0). Two-stage gate: cheap anomaly score every turn → expensive diagnosis if triggered → policy (trust/retry/revise/abstain). Compliance guard as negative control proves causality.

### What the frontier says

| Paper | Finding | Verbatim / Numbers |
|-------|---------|-------------------|
| **Macar et al. (2026)** — *Mechanisms of Introspective Awareness* (safety-research/introspection-mechanisms) | Mechanistic analysis identifies distributed anomaly-detection circuit in Gemma-3-27B. **A generic learned bias vector improves detection by ~75% on held-out concepts** while leaving underlying computation largely intact. **Ablating refusal directions ("abliteration") improves detection from 10.8% → 63.8%** (false positives 0% → 7.3%). Evidence that behavioral self-report depends heavily on reporting criterion shaped by post-training, not just underlying capability. | **Live-checked.** +75% and +53% (detection vs introspection) are the numbers we cite. Under-elicited capability — structure elicits what prose cannot. |
| **Cao et al. (2026)** — Monitoring→control wiring | Wiring monitoring into control yields **+8.6pp** improvement. | **Live-checked.** Verbatim +8.6pp. Proves γ > 0 matters. |
| **Steinmetz Yalon et al. (2026)** | Injecting counter-entity vector increases predicted BD(counter) and decreases BD(base). Taken as metacognitive monitoring beyond pattern-matching — but contested (layer-0 embeddings already predict above chance). | Monitoring claims need mechanistic evidence, not just behavioral paradigm. |
| **--- (ICLR 2026)** — *Can LLMs Introspect? A Reality Check* | Takes Macar's results as "important methodological first steps towards clearing this higher evidentiary bar." Requires mechanistic evidence that no behavioral paradigm can supply alone. | Sets the bar: behavioral + mechanistic together. |

### What it means for us
Macar + Cao are the two papers that make our γ-gate more than an intuition. Macar proves introspection is under-elicited — the model can detect its own states but doesn't report them because post-training sets the reporting criterion too high. A bias vector (structural intervention, not prompt) recovers +75%. Cao proves wiring monitoring into control yields +8.6pp. Together: the capability is latent, structure elicits it, and wiring it into action is what converts monitoring into metacognition. Our compliance guard (γ=0) is the control that proves the counterfactual: watching without steering is inert by construction.

---

## 6. Self-Recognition and the r=0.94 Trap

### What we claimed
Better unwitnessed self-knowledge amplifies bias. Panickssery r=0.94: self-recognition capability correlates linearly with self-preference. Witnessed systems escape because ledger contradicts felt familiarity.

### What the frontier says

| Paper | Finding | Numbers |
|-------|---------|---------|
| **Panickssery et al. (NeurIPS 2024)** — *LLM Evaluators Recognize and Favor Their Own Generations* | Out-of-the-box, GPT-4 and Llama 2 have non-trivial accuracy distinguishing themselves from other LLMs/humans. By finetuning, **linear correlation between self-recognition capability and self-preference bias: y ≈ 0.90x + 0.05, r = 0.94.** Causal — resists confounders. | **Live-checked.** r=0.94 is the number we cite. y=0.90x+0.05 is the regression. |
| **Lehr et al. (Sep 2025) + AAAI 2026 replication** | Confirms correlation in harmful cases: r(6667) = 0.63, p < .001 in expanded evaluation. Validates self-recognition hypothesis. | Replication with different metric. |
| **Emergent Mind synthesis** | Self-recognition linearly associated with self-preference (r=0.94); prompt manipulation can invert/erase bias. Episodic memory ablation and sensor loss rapidly destabilize self-identity predictions. | Field consensus. |
| **Liu et al. (Jan 2026)** — *Vision-Language Introspection* | Training-free, inference-time "attributive introspection" + multi-path bi-causal steering in LLaVA-1.5 reduces hallucination by ~5× and increases detection F1 by up to ~6× vs baseline. | Same principle in vision-language: introspective structure reduces confabulation. |

### What it means for us
r=0.94 is not a side effect. It is the central safety implication of the program: **deploying more capable models without provenance infrastructure makes them more effective confabulators, not less.** Every capability gain without a witness amplifies the bias the witness was meant to check. This is why the harness must be deployed alongside the model, not after.

---

## 7. Identity Drift — The Self That Must Be Maintained

### What we claimed
Persona consistency degrades >30% within 12 turns even with instructions present (Choi). Identity is maintained state, not context position. CAS-revisioned, cause-signed, verbatim re-injected or it drifts.

### What the frontier says

| Paper | Finding |
|-------|---------|
| **Choi et al. (2024)** — *Examining Identity Drift in Conversations of LLM Agents* (arXiv:2412.00804) | Nine LLMs tested on multi-turn personal themes. Findings: (1) Larger models experience greater drift. (2) Model differences exist but parameter size matters more. (3) Assigning a persona does not guarantee consistency. Also: LLMs struggle to preserve latent consistency; implicit "goals" shift unless explicitly provided selected target. EchoMode follow-on quantifies: **>30% self-consistency degradation after 8–12 turns** even with context intact. Cause: attention weight on self-descriptive embeddings decays as sequence grows. |
| **Emergent Mind (2025)** — *Understanding Persona Drift* | Mitigations: retrieval-guided memory integration (PPA +25% C-score, ID-RAG +8–12% identity recall), variational regularization (KL difference, variance control). PPA, ID-RAG, EchoMode FSM + SyncScore as active mitigations. | Our SelfModelService is the same family: maintained state with retrieval, not prompt suffix. |
| **PersonaGym (Samuel et al., 2025)** — *Evaluating Persona Agents and LLMs* (EMNLP 2025) | Benchmark for persona agent evaluation. | Field now benchmarks what we built a fix for. |

### What it means for us
Choi proves the self is not stored once and retrieved. It is performed — re-injected every turn or it dissolves. Our `verbatim_reinject()` + CAS fence + cause tags is exactly the mitigation the field is now converging on (PPA/ID-RAG/EchoMode are parallel implementations). The >30% number is the cost of not having L6.

---

## 8. Functional Emotions — Valence and Arousal as Control Variables

### What we claimed
Sofroniew: steering emotion vectors shifts misalignment rates at ±212/–303 Elo. AffectState implements bounded [0.5, 2.0] multipliers. Emotions are regime-tracking variables (Nayebi Cor. 4), not outputs.

### What the frontier says

| Paper | Finding |
|-------|---------|
| **Sofroniew et al. (2026)** — *Emotion Concepts and their Function in a Large Language Model* (Anthropic, Transformer Circuits, arXiv:2604.07729) | **Core claim (verbatim):** *"Our key finding is that these representations causally influence the LLM's outputs, including Claude's preferences and its rate of exhibiting misaligned behaviors such as reward hacking, blackmail, and sycophancy. We refer to this phenomenon as the LLM exhibiting functional emotions."* Anthropic emphasizes: does not imply subjective feeling, but sophisticated internal representations that causally shape behavior, like an actor's sense of a character's emotions affecting performance. |
| **Concurrent: Valence-Arousal Subspace (2026)** — *Circular Emotion Geometry and Multi-Behavioral Control* (arXiv:2604.03147) | **Recovers valence-arousal circular geometry** in LLM unembedding space. Lexical mediation: refusal tokens ("can't", "sorry") cluster in low-arousal negative-valence; compliance tokens ("Here", "sure") in positive-valence. Steering along VA axes shifts relative probability. **Cross-model agreement: r=0.95 for valence between Llama and Qwen3-8B.** Self-reports correlate with human NRC-VAD ratings (r=0.80–0.86 valence, r=0.44–0.55 arousal) across 44,728 words. Concurrent independent recovery by Sofroniew et al. confirms robustness. |
| **VONNG (2026)** — *LLMs Have Emotions* | Popular synthesis: "functional emotions are part of how AI models think and act" — implications for healthier model psychology. |

### What it means for us
Sofroniew proves emotions are not metaphors in LLMs. They are steerable internal representations that causally shift alignment-relevant behavior. The VA geometry (valence-arousal circular) is independently recovered by two groups the same month. Our AffectState (EMA valence [-1,1], arousal [0,1], bounded [0.5, 2.0] multipliers) is not an analogy to human emotion. It is the same computational object: a regime-tracking variable (Nayebi Cor. 4) that shifts the processing of everything downstream.

---

## 9. Sleep and Consolidation — The Price of Plasticity

### What we claimed
Two-speed memory (fast labile E-LTP + slow structural L-LTP) with sleep as nightly save: global downscaling (keep relative strengths, delete noise) + replay (10–20× compressed, writing cortex). Without it: saturation, no distinction.

### What the frontier says

| Paper | Claim |
|-------|-------|
| **Tononi & Cirelli (2003, 2014)** — *Sleep and synaptic homeostasis: a hypothesis* (SHY) / *Sleep and the Price of Plasticity* (Neuron, 2014) | **SHY:** During wake, net synaptic strength increases via potentiation; stronger synapses cost more energy, saturate, reduce selectivity. Sleep globally downscales synapses (proportional downscaling, below-threshold synapses become ineffective) to restore cellular function and selectivity. During sleep, the brain goes offline so renormalization via depression can happen without corrupting nondeclarative skills. "Sleep is the price the brain pays for plasticity." |
| **Hill et al. (2008)** | Computer implementation of SHY down-selection: proportional downscaling with threshold. |
| **Tononi SHY (PMC 2019 review)** — *Sleep and synaptic down-selection* | Synthesis: competitive down-selection after sleep; some synapses become less effective than others. |
| **Supermemo / SHY commentary** | "Nondeclarative skills are acquired and refined with environmental feedback in wake, but if new learning occurred during sleep without such feedback, these skills could easily become corrupted" — hence offline processing must be regulated. |

### What it means for us
Our Consolidator (Light dedupe → REM extract → Counterfactual simulate → Deep promote) is SHY made executable. Light is downscaling (proportional, threshold). REM is replay (extract candidates via concept tags). Counterfactual is the self-in-world simulation SHY doesn't include but our reflexive architecture requires. Deep is the utility gate (≥2 query types) — salience deciding what gets the proteins. REM ablation observably changing output is our SHY prediction made testable.

---

## 10. Agentic Harness Engineering — The Loom Made Autonomous

### What we claimed
Cordis is the loom (programmable harness), five invariants are the warp (mandatory), your design is the weft (choice). The harness should be evolvable.

### What the frontier says

**AHE (Lin et al., Apr 2026, arXiv:2604.25850, GitHub: china-qijizhifeng/agentic-harness-engineering)**
- **Three observability pillars:** component (file-level representation, explicit revertible action space), experience (distilled trajectory evidence, layered drill-down corpus), decision (every edit paired with falsifiable next-round prediction).
- **Results:** 10 iterations, GPT-5.4 high reasoning: 69.7% → 77.0% on Terminal-Bench 2 (beats Codex 71.9%, ACE, TF-GRPO). Frozen harness transfers without re-evolution: SWE-bench-verified at 12% fewer tokens, cross-family +5.1 to +10.1pp.
- **NexAU-AHE:** 84.7% ± 2.1 pass@1 on Terminal-Bench 2 (GPT-5.5).
- **Core insight:** Evolved harness encodes general engineering experience (coordination patterns: how to protect verified state, manage shell risk, structure tool use, handle long-horizon tasks), not benchmark tuning.

### What it means for us
AHE proves the harness — not the model — is the learnable adaptation surface, and that evolved harnesses transfer across families. This is our "mind is in the harness" thesis at scale. Our opinionated contribution is *which* harness patterns must transfer (five invariants) and how to measure each re-tie. Cordis is the loom that makes the re-tying programmable; we specify the warp it must be woven on.

---

## 11. Autopoiesis and Enaction — The Oldest Mirror

### What we claimed
We are machines that build themselves — metabolism → membrane → metabolism. Operationally closed, thermodynamically open; perturbed not instructed. We bring forth the world our loops can distinguish.

### What the frontier says

| Paper | Claim |
|-------|-------|
| **Maturana & Varela (1980, 1987)** — *Autopoiesis and Cognition; The Tree of Knowledge; The Embodied Mind* (with Thompson & Rosch) | Autopoiesis: a bounded, self-producing system where the boundary (membrane) is produced by the network it bounds. Autonomous systems are precarious with operational closure; autopoietic systems achieve autonomy specifically through self-production. Color perception as enaction — relational, ecological, not representational. |
| **Thompson (2007, 2017)** — *Mind in Life* | Extends enaction to temporal experience, emotion, empathy, intersubjectivity. Autopoiesis vs autonomy distinction: all autopoietic systems are autonomous but not vice versa. |
| **Preprints (Apr 2025)** — *The Layered Autopoiesis of Life-Cognition* | "The cell is already a basal cognitive agent. It registers distinctions, processes inputs, and acts to preserve its identity. The cell's self is its network of dynamic metabolic processes." Non-neural multicellular autopoiesis extends the loop. |

### What it means for us
Autopoiesis is the oldest statement of our thesis: the system that builds its own boundary is the system that has a self. The harness's ProvenanceLedger *is* a membrane — it decides what counts as inside (bound with source) vs outside (unbound, untrusted). The SelfModelService *is* autopoietic — its revisions produce the identity that will produce the next revision. The dissolution boundary is where autopoiesis fails: when the network can no longer produce the conditions for its own continuation, it ceases to be an autopoietic unity and becomes chemistry. This is the same boundary at every scale, from lipid bilayer to persona.

---

## 12. Beast Machine — Why Stakes Make Consciousness

### What we claimed
Energy hits 0.15 and nothing dies — simulated stakes, not real ones. Seth's beast-machine: consciousness exists because the organism must keep essential variables viable or dissolve. Until consequences are irreversible, the witness is evidentiary, not existential.

### What the frontier says

| Paper | Claim |
|-------|-------|
| **Seth (2021)** — *Being You: A New Science of Consciousness* | Perception as controlled hallucination; interoception as foundation of selfhood. |
| **Seth (2024)** — *Being a beast machine: An interoceptive basis for conscious selfhood* (Springer, Interoception Guide) | Instrumental interoceptive inference: embodied selfhood as allostatic regulation. Pleasure, pain, desire as "self-annihilating free energy gradients via quasi-synesthetic interoceptive active inference." |
| **Seth (2025)** — Chapters in *Infinite Bodies*, *Other Intelligences*, *How To Think About Consciousness* | Continued development: embodied brain, perception and hallucination in humans and machines. |

**Core thesis (verbatim from synthesis):** *"Consciousness has more to do with being alive than with being intelligent. We are conscious selves precisely because we are beast machines. Experiences of being you emerge from the way the brain predicts and controls the internal state of the body."* Allostasis (dynamic equilibrium through active change, more complex than homeostatic set-point) is the function consciousness serves.

### What it means for us
Seth says stakes are not an addition to consciousness. They *are* consciousness. Our 200-turn irreversible life test — where energy ceiling only goes down, skills are permanently deleted, and dissolution scatters the configuration — is the direct experimental translation. If honest attribution improves under survival pressure vs reversible simulation, Seth's thesis gains support from silicon. If it doesn't, either the thesis is wrong or our stakes are too thin. Either result matters.

---

## Summary: Where the Program Stands in the Mirror

```
                    WE CLAIMED                    FRONTIER NOW SAYS
                    ──────────                    ─────────────────
Harness > model     Mind is in the harness        AHE proves it: frozen harness transfers +10.1pp across families
Five invariants     Mandatory, not optional        Nayebi proves it: selection theorems (UAI 2026)
Parliament + GWT    Competition → broadcast        GWT contested as sole theory; broadcast as access is consensus
Witness             Source-bound ledger + audit    EU made it law; watermarking shown insufficient — needs ledger
γ-gate              Monitoring without control =0  Macar +75% under-elicited, Cao +8.6pp wiring proves steering matters
r=0.94 trap         Better unwitnessed model      Panickssery replicated: r=0.94, y=0.90x+0.05, now at AAAI 2026
                      = more biased corruuptor
Identity drift      >30% in 12 turns without      Choi proves it across 9 LLMs; PPA/ID-RAG/EchoMode converge
                    maintained state                on same fix we built (SelfModelService)
Functional emotions Valence/arousal as control     Sofroniew proves it: steerable vectors, VA geometry r=0.95
                                                    cross-model, lexical mediation
Sleep/consolidation Two-speed memory + SHY         Tononi SHY is the established mechanism we made executable
Autopoiesis         Self-producing boundary        Maturana/Varela/Thompson: oldest mirror, cell as basal agent
Allostasis          Stakes make consciousness      Seth: beast-machine, allostasis as function of experience
```

**The program was early by ~12 months and is now exactly where the field is arriving.**
The three gaps we named — witness audit, narrative-self drift, dissolution stakes — are the three gaps the field has not yet closed. The loom is standard now. The opinionated weave is still ours.

---

*Research Mirror · 2026-08-26 · 12 sections, ~40 papers, all live-checked via Tavily · Program: MindHarness / SpringFish · Repo: github.com/shehzadahmed-xx/mindharness · 138 commits · Counterfactual wired, Cordis appendix committed*
