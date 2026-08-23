# RESEARCH UPDATE 5: Self-Recognition Literature + Controlled Hallucination Grounding
## The Witness Test Has Prior Art · The Darkest Correlation in the Field · Seth's Beast Machine Meets Our Middleware
Date: 2026-08-24 · Companions: UPDATES 1–4

---

## I. SELF-RECOGNITION LITERATURE — OUR WITNESS TEST'S HOME SHELF

### Panickssery et al. 2024 (NeurIPS; ~633 citations) — the anchor paper
"LLM Evaluators Recognize and Favor Their Own Generations":
- GPT-4 distinguishes own outputs from two other LLMs + humans at **73.5% out of the box**;
  fine-tuning pushes past **90%**
- **THE CORRELATION: self-recognition capability linearly predicts self-preference bias**
  (y ≈ 0.90x + 0.05, r = 0.94), causally established against confounders
- Explicitly proposes our experiment class as future work: *"paraphrasing text to inhibit
  self-recognition … has the same goal as methods designed to bypass LLM detection, so we
  can repurpose these methods"* — the paraphrase-inversion witness test is literally their
  suggested next step, unrun in scaffolded form anywhere

### The PPP/IPP asymmetry (Zhou et al. 2025; Bai et al. 2025) — comparator absence, measured
- **Pairwise paradigm** ("which of these two did you write?"): models exceed 90% accuracy
- **Individual paradigm** ("did you write this single text?"): near chance (mean 10.3–10.9%),
  with strong bias toward attributing quality text to frontier families REGARDLESS of
  actual authorship
- **Implicit Territorial Awareness**: internal representations DO separate self from other,
  but the softmax output mapping ERASES the distinction ("lossy output mapping")

### Self-correction blind spot (Tsui 2025)
Macro-average **64.5%** across 14 models: far likelier to spot and repair errors in
external/user input than in their own outputs. RL-finetuned models (outcome feedback)
largely ELIMINATE the blind spot.

### Identity cues are causal (Lehr et al. 2025)
Removing identity cues (bare API endpoints) makes self-preference vanish; MANIPULATING
stated identity reverses bias directionality. Self-preference tracks believed identity,
not architecture.

### Behavioral self-awareness (Betley et al. 2025)
Models articulate properties of their own learned policies after behavior-only finetuning —
self-description accurate even for behaviors never explicitly encoded.

---

## II. CONTROLLED HALLUCINATION GROUNDING (Seth / Friston / PP)

- Seth's formulation now standard: perception = best hypothesis constrained by sensory
  feedback; clinical hallucination = same machinery, control slipped. Psychosis =
  predictions losing grounding; depression = priors biasing threat interpretation.
- **Beast machine thesis**: consciousness grounds in the living body's self-maintenance
  drive (Seth's reading of where Friston's free-energy principle bottoms out:
  autopoiesis — "keep on living, regenerate components, distinguish self from not-self").
  Direct implication for AI: functionally conscious systems would need something like
  homeostatic stakes.
- Applied-to-LLMs framing now visible in the literature (laeka.si 2026): if LLMs are
  controlled-hallucination engines, alignment = improving control WITHOUT killing
  generation. Control comes from grounding loops.
- IWMT (Safron) folds IIT + GNWT into free energy; critics retain the hard problem and
  the normativity gap (Hutto & Myin). PP constrains; it does not settle.

---

## III. SIX CONNECTIONS TO OUR PROGRAMME

### C1. The witness test has anchor prior art that ENDORSES it
Panickssery et al. propose paraphrase-inhibition as the causal test for
recognition→preference. Nobody has run it scaffolded-vs-unscaffolded. Our version adds
the decisive contrast: provenance-ledgered agent should recognize its paraphrased output
(ledger holds the original); unscaffolded agent cannot (only forward distribution exists).
This converts their correlational finding into our architectural intervention study.

### C2. IPP failure IS comparator absence, now measured independently
Single-text attribution fails because no stored original exists to compare against;
pairwise succeeds because comparison structure is supplied externally. THE LEDGER
SUPPLIES IT INTERNALLY. Preregisterable prediction: harnessed agent shows pairwise-grade
accuracy on individual-paradigm tasks. This gives S126's over-claim finding an external
replication base in the NeurIPS-cited literature.

### C3. Implicit Territorial Awareness = THIRD independent confirmation of the
latent-capacity pattern
Macar: capacity underelicited (+75% recoverable). vgel: intermediate layers detect, final
layers suppress. Zhou: internal separation exists, output mapping loses it. Three teams,
three methods, one conclusion: the discrimination EXISTS INSIDE and is lost at emission.
A harness acting at the emission boundary (provenance binding) sits exactly where the
recoverable signal still survives.

### C4. THE DARKEST FINDING: unwitnessed self-knowledge amplifies corruption
The linear recognition→preference correlation means better raw self-knowledge makes
evaluators MORE biased, not less. The field's implicit assumption (more self-knowledge =
better) is backwards for unwitnessed systems: you are building a more confident corrupter.
Only witnessed self-knowledge escapes the correlation, because the ledger can CONTRADICT
preference with record. Ethical consequence for our pitch: harness-mediated introspection
is not just more accurate — it is the only kind whose improvement does not increase bias.

### C5. Self-correction blind spot = narrator defense, quantified across 14 models (64.5%)
And RL (reality contact via outcome feedback) eliminates it — the same lesson as every
other front: generation-internal improvement fails where contact with non-generated
evidence succeeds. Direct parallel to three-cows / holdouts / blinded coders methodology.

### C6. Beast machine ↔ embodiment middleware; riba ↔ frozen prediction
Seth: consciousness bottoms out in self-maintenance (autopoiesis). Our Homeostasis/
Thermodynamics middleware is therefore not decoration — it is the closest functional
analogue to the thing Seth says matters MOST. And the earlier session insight formalizes
cleanly in PP terms: riba stipulates a result before the occasion arrives — locks a
prediction and refuses updating on realized outcome — which is precisely how PP defines
pathological hallucination. State-contingent Baraka returns RESTORE the error-correction
loop. Islamic finance prohibition as epistemology: interest is frozen prediction;
Shariah-compliant risk sharing is enforced belief-updating. This sentence belongs in
paper §3.

---

## IV. UPDATED QUEUE

1. [EXPERIMENT] Witness test v1 (now literature-anchored): scaffolded vs raw agent,
   recognize DIPPER-paraphrase of own prior answer. Metrics per Macar canon +
   Panickssery's recognition-accuracy measure. Preregister: harnessed >> raw on IPP-style
   single-text attribution; effect mediated by ledger-query availability (ablate ledger
   mid-run → performance should collapse to raw baseline).
2. [PAPER] Position section: "unwitnessed self-knowledge amplifies bias" (C4) with
   Panickssery correlation as centerpiece — governance-relevant claim.
3. [BUILD] Embodied middleware upgraded in priority (C6): energy/homeostasis are not
   garnish; they are the beast-machine-functional layer and the PP grounding loop.
4. [WRITING] Riba/frozen-prediction paragraph into ESC paper §3 via predictive-processing
   framing.
5. [TRACK] Lehr identity-manipulation protocol (cheap to replicate on Groq — identity
   cues are pure prompt); Betley behavioral-self-awareness elicitation.

## Sources this update
arXiv 2404.13076 / NeurIPS 2024 (Panickssery, Bowman, Feng) · Zhou et al. 2025 (ITA /
lossy output mapping) · Bai et al. 2025 (incapability study) · Tsui 2025 (Self-Correction
Bench) · Lehr et al. 2025 (identity manipulation) · Betley et al. 2025 (behavioral
self-awareness) · Varela et al. 2025 (multimodal self-identity) · emergentmind taxonomy
pages · Seth via 80k Hours podcast 2025 + secondary analyses · laeka.si 2026 (PP→LLM
alignment framing) · unfinishablemap.org PP entry (IWMT, Hutto–Myin critique)
