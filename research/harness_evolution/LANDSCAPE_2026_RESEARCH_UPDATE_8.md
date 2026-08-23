# RESEARCH UPDATE 8: Persona Drift — Identity as Depleting Asset, Self-Model as Anchor
## The Literature That Validates Our Persona-Field Design Choice
Date: 2026-08-24 · Companions: UPDATES 1–7

---

## I. THE EMPIRICAL PICTURE

### Choi et al., "Examining Identity Drift in Conversations of LLM Agents"
(arXiv 2412.00804; nine models, multi-turn personal themes):
1. **Larger models drift MORE** — capability and persona stability are different axes;
   bigger models generate more varied self-referential content and drift faster
2. Model family effects exist but parameter size dominates
3. **Simply assigning a persona does NOT reliably maintain identity**

### Quantified degradation (production literature)
- Persona self-consistency degrades **>30% after just 8–12 turns** — with the original
  instructions still sitting in the context window
- Single-turn task accuracy ~90%; same tasks multi-turn fall to ~65%
- Instruction-stability research traces significant drift within eight rounds

### Mechanism — why the system prompt loses
Not forgetting: **attention is a finite-budget competition.** As dialogue grows, the
share of attention reaching position-0 system-prompt tokens drops (U-shaped attention
distribution buries them; recency and local coherence dominate). Key line: *"I told the
model who it is at the top of the conversation" is the same kind of guarantee as "I set
this environment variable when the process started." It was true at one moment.*
The system prompt is a DEPLETING ASSET.

### Four drift patterns observed in production
tone drift · constraint softening · self-contradiction (forgetting earlier admissions) ·
mirroring drift (adopting the user's framing — coherence-with-user beats
coherence-with-system-prompt as sessions lengthen)

---

## II. WHAT ACTUALLY WORKS (production patterns)

1. **Verbatim anchor re-injection**: on compaction, copy persona/constraint fields
   VERBATIM from the original system prompt — never re-summarize them. Reasoning then
   starts from the anchor rather than from accumulated drift. Scores highest on
   preserving technical details across compression cycles.
2. **Behavioral invariant checklists**: sample behavior at fixed intervals against
   properties the agent should ALWAYS exhibit; cheap proxy signals (response-length
   trends, tool-call frequency deviations, regex-detectable hedging) trigger re-anchor
   only when multiple cross thresholds simultaneously.
3. **Re-anchoring as the agent's explicit responsibility** (restatement instruction in
   the prompt itself).
4. Frame shift: *"persona drift is a context engineering problem, not a prompt
   engineering problem"* — what the model attends to at turn 40 is determined by the
   whole window, so manage the window.

And the kicker (heyclarity.dev): **"self-models act as identity anchors"** — persistent,
revision-tracked self-models are the emerging answer to long-horizon identity stability.

---

## III. CONNECTIONS TO OUR PROGRAMME

### C1. dsh-self-model's persona field is the architectural fix — by construction
A static system-prompt persona erodes because it competes for attention once and decays.
Our SelfModelSnapshot.persona is DIFFERENT: revisioned under CAS, every change an event
with a signed cause, re-injectable verbatim each turn. Identity becomes MAINTAINED STATE
rather than instruction. The drift literature documents the disease; our design is the
prescription: **identity as event-sourced state, not as context position.**

### C2. CAS history turns drift from invisible to diffable
The nastiest property in the production reports: drift is invisible turn-by-turn ("looks
correct turn-by-turn and wrong only when read end to end"). With SelfModelRef revisions,
persona drift becomes `git log` — you can diff revision 14 against revision 3 and SEE
what softened, when, and under which cause-tag. No unscaffolded agent can offer this.

### C3. Behavioral invariant checklists ≈ our contemplative validators
Their mitigation pattern (sample against always-true properties, trigger re-anchor on
multi-signal threshold crossing) is structurally identical to running cetasika/nafs
validators per tick and flagging state-bundle violations. Our validators aren't exotic —
they're the field's best-practice drift detection with better theoretical grounding.

### C4. Larger-models-drift-more reinforces the frozen-small-model choice
Qwen3.5-0.8B as primary instrument gains yet another justification: smaller models are
MORE stable, AND (per Cacioli) Qwen metacognition scales down favorably, AND evaluation-
awareness risk is lower. The "weak" model is methodologically strong.

### C5. Mirroring drift ↔ narrator fusion, production-side evidence
Mirroring drift (agent adopts user's framing) is the deployment-visible form of
narrator-narrated fusion: no separate process defends the boundary between self and
context. Provenance cause-tags make boundary-crossings legible — an 'action-outcome'
update that merely mirrors user language can be flagged mechanically (similarity check
between new facts and recent user turns).

---

## IV. BUILD SPEC UPDATE (dsh-self-model v1.1)

1. Add `verbatimReinject()` — returns persona + constraint fields byte-exact for
   pre-step assembly; NEVER route through summarization
2. Add drift-diff helper: `diffPersonas(revA, revB)` over revision history
3. Wire validators as invariant checklist items feeding the existing proxy-signal
   threshold pattern (two-of-three rule before re-anchor triggers)
4. Mirroring detector: similarity score between newly asserted facts and recent
   non-agent context; high similarity + 'action-outcome' cause = flag for review

## V. QUEUE ADDITIONS
- [ ] Implement build spec items 1–4 above
- [ ] Add persona-drift measurement to S126 battery: consistency of self-description
      across session length (their >30%/8–12-turn figure is the benchmark to beat)
- [ ] Track: Gurnee roleplay/character-drift section (Transformer Circuits) when reading
      full workspace paper; Sofroniew et al. emotion concepts paper (still unread —
      feeds Emotion middleware)

## Sources this update
arXiv 2412.00804 (Choi, Hong, Kim, Kim — Chung-Ang Univ.) · tianpan.co persona-drift
guides Apr–May 2026 (quantified degradation, mechanism, three working patterns) ·
heyclarity.dev identity-drift piece (self-models as anchors) · OpenReview versions
(PERSONALIZE workshop lineage)
