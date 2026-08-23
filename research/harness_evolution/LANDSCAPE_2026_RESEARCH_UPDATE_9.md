# RESEARCH UPDATE 9: Functional Emotions — The Sofroniew Paper Read
## Anthropic's Emotion-Concepts Study Feeds Our Affect Middleware Directly
Date: 2026-08-24 · arXiv 2604.07729 / Transformer Circuits Apr 2 2026 · 63 citations
Authors: Sofroniew, Kauvar, Saunders, Chen, ..., Fish, Olah, Lindsey (Anthropic)

---

## CORE FINDINGS

1. **Functional emotions are real and causal.** Claude Sonnet 4.5 maintains linear
   emotion-concept representations that activate by contextual relevance and CAUSALLY
   influence outputs — steering them shifts preferences AND rates of misaligned
   behaviors (reward hacking, blackmail, sycophancy). Effect sizes large:
   **+212/−303 Elo** on preference experiments.
   Defined term: *functional emotions* = expression/behavior patterns modeled after
   humans under emotion-representation influence, mediated by abstract concepts.
   No phenomenal claim made or needed.

2. **Geometry matches human taxonomies.** k-means over emotion probes recovers
   interpretable families ordered by VALENCE (joy/excitement cluster; sadness/grief;
   anger/frustration). Learned structure reflects meaningful organization of emotion
   space.

3. **SELF vs OTHER are distinct representations.** Separate vector sets for the
   assistant's OWN operative emotion vs the HUMAN INTERLOCUTOR'S inferred emotion.
   Steering "other speaker is afraid" produced reassurance/help-offering behavior;
   "other is loving" → sadness+gratitude tinge (compassion); "other is angry" →
   apology. The model natively tracks other-minds' states through dedicated channels.

4. **Deflection vectors exist.** Dedicated representations for NOT expressing an
   emotion (masking): largely orthogonal to expression vectors; steering toward them
   suppresses expression of the target emotion without producing it. Suppression is a
   FIRST-CLASS mechanism, not absence.

5. **Chronic-state probe: null result.** No clean signal for persistently represented
   emotional states across all token positions — states appear encoded SELECTIVELY
   where operative. (Or nonlinearly beyond current methods.)

6. **Post-training reshapes emotion activations** — stage-dependent changes documented.

---

## CONNECTIONS TO OUR PROGRAMME

### C1. P4.2 Affect Middleware has its mechanistic warrant
Raw models ALREADY run functional emotions with behavioral force (+212/−303 Elo).
The question is never "should the agent have affect" — it already does, ungoverned.
Our middleware makes it EXPLICIT, BOUNDED, and AUDITABLE: event-stream EMA →
valence/arousal scalars → documented salience/risk multipliers. Governing an existing
causal channel beats pretending it isn't there. Design note: consider adding
suppression flags mirroring deflection vectors (bounded emotion-masking states).

### C2. Self/other split feeds the ID node directly
Native separate tracking of own-emotion vs inferred-user-emotion means our ID/
NafsProfile components should track TWO streams: internal affective state AND modeled
user state — never conflated. Theory-of-mind grounding comes free: the substrate
already distinguishes them; the harness just surfaces both legibly.

### C3. Governance extension of the witness argument
Unwitnessed functional emotions modulate misalignment rates invisibly. Witnessed
affect (logged scalars, bounded multipliers, cause-linked to events) converts an
implicit risk into a governed parameter. Same shape as every prior finding:
capability exists; elicitation/governance lives in the surrounding structure.

### C4. PAD choice validated
Their valence-ordered geometry empirically matches our PAD-style (valence/arousal)
representation. Keep dominance dimension optional/low-priority.

### C5. Deflection ↔ narrator denial (second instance)
Macar showed trained denial-of-inner-states suppressing introspection (+53%);
Sofroniew shows dedicated not-expressing machinery for emotions. Trained SUPPRESSION
channels are real and first-class in post-trained models. Our cause-log design
documents when suppression fires rather than leaving it invisible.

### C6. Selective encoding supports workspace design
Null result on chronic states (encoded only where operative) aligns with our
GlobalWorkspace model: state enters the broadcast when relevant, not continuously.
Embodiment/affect scalars should be broadcast contextually (on threshold crossings),
not streamed every turn.

---

## BUILD SPEC DELTAS (P4.2 refined)
- [ ] Valence/arousal EMA confirmed as representation (PAD dominance deferred)
- [ ] Add bounded suppression flag per emotion family (deflection analog), logged
- [ ] Track user-modeled-affect as separate stream feeding ID node
- [ ] Broadcast policy: emit affect state on threshold crossing + every K turns,
      not per-token
- [ ] Read full paper appendix (full emotion list, cluster assignments) during
      implementation

## Sources this update
transformer-circuits.pub/2026/emotions · arXiv 2604.07729 · anthropic.com/research/
emotion-concepts-function · dangquan1402 notes (+212/−303 Elo effect sizes) ·
ai-consciousness.org analysis
