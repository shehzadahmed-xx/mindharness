# RESEARCH UPDATE 2: Selection Theorems, Underelicited Introspection, and the Metacognition Literature
## Five Findings · Two Directly About Our Model Family
Date: 2026-08-24 · Companion to LANDSCAPE_2026_RESEARCH_UPDATE.md

---

## FINDING 1 — Nayebi's Selection Theorems: Our Architecture Is Mathematically Mandatory
**arXiv 2603.02491 · UAI 2026 · Aran Nayebi (CMU ML Dept + Neuroscience & Robotics)**

Proves quantitative selection theorems: low average-case regret FORCES internal structure.
Performance is the selector; architecture follows. Four results:

| capability level | mathematically forced structure | our harness component |
|---|---|---|
| partial observability | world model (interventional transition kernel) | WorldModel ✓ |
| partial observability | belief-like memory | 5-store Memory ✓ |
| task mixtures | persistent regime-tracking variables "resembling functional primitives of emotion" | Emotion + GlobalState ✓ |
| block-structured tasks | informational modularity (distinct channels per task family) | specialist modules ✓ |

Every structure Nayebi proves necessary already exists in our harness BY DESIGN.
Also proves modular competitive processing (GWT-like architecture) converges from
optimality constraints ALONE — consciousness-theoretic architectures capture structural
necessities of competent agency, not biological accidents. Direct descendant of
Conant & Ashby 1970 ("every good regulator must be a model of that system").
Explicit scope limit: architectural necessity ≠ phenomenal status. Author's Alignment
Forum post title: "Why AI Consciousness May Be an Inevitable Consequence of Capability."

**Implication:** our design choices are no longer justifiable only by tradition-mapping
(Buddhist/Sufi/neuroscience). They are provable requirements for any low-regret agent.
Paper v2 gains a formal section: map each §125 component to its Nayebi theorem.

---

## FINDING 2 — Introspection Is Massively Underelicited: The Harness Thesis in Miniature
**Macar et al., "Mechanisms of Introspective Awareness" · arXiv 2603.21396 · ICML 2026 poster · code: github.com/safety-research/introspection-mechanisms**

Mechanistic investigation in open-weight models (Gemma3-27B best among open):
1. Detection and identification are SEPARABLE mechanisms — distinct layers, weak overlap
2. Robust 0% false positives across prompts and dialogue formats
3. Probability-matching confound accounts for SOME but not all detection behavior
4. **KEY RESULT: introspection is substantially underelicited —
   ablating refusal directions: +53% detection;
   trained bias vector: +75% on held-out concepts —
   both without increasing false positives**

Latent capacity exists that default prompting fails to surface. A trained bias vector
is a one-component harness edit that more than doubles genuine detection. This IS the
harness thesis measured at the activation level: capability lives in the model;
elicitation lives in the surrounding structure.

---

## FINDING 3 — Qwen Introspects But Its Final Layers Suppress It (OUR MODEL FAMILY)
**vgel, "Small Models Can Introspect, Too" (Dec 2025) · code: github.com/vgel/open-source-introspection · repeng library**

Applied concept injection to Qwen2.5-Coder-32B:
- Naive prompting: appears unable to introspect
- **Logit lens: detection signal PRESENT in intermediate layers; FINAL LAYERS SUPPRESS the report**
- Accurate introspection info in prompt: detection 0.3% → 39.9%
- Model detects emergent-misalignment concepts injected MID-KV-CACHE via model swap

Plus Cacioli's Metacognitive Monitoring Battery (arXiv 2604.15702, 524 items / 6 domains):
**metacognitive sensitivity scales DOWN with size in Qwen family** (GPT-5.4 scales UP,
Gemma flat). No universal scaling law; architecture-dependent.

**Implication for our frozen Qwen3.5-0.8B:** the suppression layer may be weaker in
smaller checkpoints, and family-relative metacognition may be BETTER at small scale.
Our 0.8B could be a disproportionately good introspection subject. Test protocol:
repeng-style steering vectors + logit lens on llama.cpp logits (already serving :18555).
If intermediate-layer detection exists but output suppresses, THE HARNESS READS THE
LOGITS DIRECTLY — we can route around the suppressor by construction. No published
work does this: witness-level access to the very layer that hides the signal.

---

## FINDING 4 — Meta-d′ Formalized for LLMs; RLMF Reaches 0.91 Efficiency
**Cacioli (arXiv 2603.25112 Type-2 SDT framework; 2604.15702 Monitoring Battery;
2603.14893 temperature-criterion analogy) · Servajean & Servajean methodology · Yale NLP survey 2607.11881**

ECE/Brier CONFLATE knowledge with metacognitive sensitivity. Type-2 SDT decomposes:
meta-d′ (confidence discriminates own correct/incorrect) vs d′ (task accuracy);
M-ratio = meta-d′/d′ = metacognitive efficiency.

Measured efficiency trajectory:
- Base pretrained autoregressive: **M-ratio ≈ 0.38** (latent certainty signals exist
  in residual stream but next-token objective never surfaces them)
- RLHF: ≈ 0.74
- **RLMF (RL with Metacognitive Feedback): ≈ 0.91** — near theoretical optimum

Megan Peters' criterion (MoC7 keynote): genuine metacognitive access requires
computing a higher-order Bayesian posterior from LIVE processing dynamics — NOT from
stored calibration statistics. Stored stats ≠ access.

**Implications:**
(a) Our Part 24 meta-d′ protocol is now field-standard, not novel — good; cite
    Cacioli/Servajean as method ground truth.
(b) Peters' live-vs-stored distinction is EXACTLY our provenance ledger argument:
    confidence from token probabilities = stored calibration; confidence bound to
    source records of what produced the answer = live access. We satisfy her criterion
    structurally.
(c) RLMF shows training can reach 0.91 — but training requires infrastructure we lack.
    The HARNESS alternative: measure M-ratio on raw model, then on harnessed agent,
    same tasks. If harness-mediated monitoring raises effective M-ratio without
    touching weights, we've demonstrated weight-free elicitation of the +53%/+75%
    latent capacity (Finding 2) at zero training cost.

---

## FINDING 5 — Prior Art Exists for Harness-Mediated Metacognition: Differentiate Now
**Cao et al., "LLMs know when they know, but do not act on it: A metacognitive harness
for test-time scaling" · arXiv 2605.14186**

Their title IS our γ=0 diagnosis: knowledge present, action absent. They build a
harness forcing models to ACT on calibrated uncertainty during test-time scaling.

**Differentiation (must be explicit in paper v2):**
| | Cao et al. | OURS |
|---|---|---|
| goal | test-time compute efficiency | witnessed self-knowledge |
| monitor source | token-probability calibration | provenance records (live, per Peters) |
| verification of self-claims | downstream accuracy | structural comparator + attribution accuracy |
| contemplative constraints | none | cetasika/nafs validators |
| self-model manipulation | none | B3 floor tolerance |

They prove harness-mediated metacognition WORKS. We add witnessing, state validation,
and self-floor tolerance. Complementary, citable, and a baseline to beat.

---

## CONSOLIDATED ACTION LIST (supersedes previous)

1. **[EXPERIMENT] Concept injection on frozen Qwen3.5 via llama.cpp**
   - Train steering vectors (repeng method) for 5+ concrete concepts
   - Inject at L=mid-layer during KV generation; probe detection at output AND via logit lens
   - Prediction (preregister via prediction_lock.py): detection signal present in
     intermediate layers even when output suppresses (per vgel); harness reading logits
     directly recovers it
   - Then rerun WITH cognitive_harness.py active: does harness-mediated monitoring
     raise behavioral detection rate? Compare against +53%/+75% ceilings from Macar.

2. **[EXPERIMENT] Harness M-ratio delta**
   - Cacioli SDT protocol, 224k-trial scale reduced to ~2k TriviaQA items feasible locally
   - Measure M-ratio: raw Qwen3.5 vs harnessed agent, identical items
   - Preregistered prediction: harness ≥ raw on M-ratio; effect concentrated in
     high-uncertainty quartile (where monitoring has something to say)

3. **[PAPER] v2 restructure**
   - Section: Nayebi mapping table (each component ↔ its necessity theorem)
   - Section: threshold-crossing framing (Zhang et al.) with harness remedies
   - Related work: Cao et al. differentiation table (above), Macar/vgel underelicitation,
     Cacioli/Peters measurement standards, Lederman & Mahowald critique answered by
     structural binding

4. **[TOOLING] Port repeng to llama.cpp logits** (steering vector training needs
   gradient access — use transformers locally for vector TRAINING on tiny model,
   apply vectors at llama.cpp inference; 0.8B trains fast on CPU/MPS)

5. **[TRACK] Neuronpedia jlens interactive; safety-research/introspection-mechanisms;
   vgel/open-source-introspection; Nayebi follow-ups; Cacioli battery releases**

---

## Sources (new this update)
2603.02491 (Nayebi selection theorems, UAI 2026) · 2603.21396 (Macar et al.,
ICML 2026) · github.com/safety-research/introspection-mechanisms ·
github.com/uzaymacar/introspective-awareness · vgel.me/posts/qwen-introspection +
github.com/vgel/open-source-introspection · 2603.25112 / 2604.15702 / 2603.14893
(Cacioli ×3) · 2605.14186 (Cao et al. metacognitive harness) · 2607.11881 (Yale NLP
survey) · Servajean & Servajean SDT methodology · Megan Peters MoC7 keynote ·
alignmentforum.org Nayebi post · transformer-circuits.pub/2026/emotions (Sofroniew
emotion concepts — noted, unread)
