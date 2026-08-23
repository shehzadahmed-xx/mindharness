# RESEARCH UPDATE 6: AI Welfare Literature — The Governance Bridge Grounded
## Long/Sebo/Butlin/Birch/Chalmers Framework · Witness Capacity Fills Their Named Gap
Date: 2026-08-24 · Companions: UPDATES 1–5

---

## I. THE ANCHOR REPORT: Taking AI Welfare Seriously (arXiv 2411.00986)
Long, Sebo, Butlin, Finlinson, Fish (Eleos+Anthropic), Harding, Pfau, Sims, Birch, Chalmers — Nov 2024

### Core structure
- **Two routes to moral patienthood**: consciousness OR robust agency. Either could
  suffice; neither certain; both realistic near-future possibilities.
- **Probabilistic assessment mandated**: e.g., 30–50% credence in computational
  functionalism × 30–50% that an AI system is conscious if so ⇒ 9–25% chance —
  "That would be good to know when interacting with this AI system!"
- **Precautionary principle, calibrated by cost**: low-cost interventions (prompting,
  environment adjustments) justified under high uncertainty; high-cost interventions
  (non-development) require far higher evidential standards.
- **Three action categories for companies**: Acknowledge · Assess · Prepare.
  Explicitly calls for "more precise empirical frameworks for evaluating AI systems
  for consciousness, robust agency, and other welfare-relevant features."
- **Self-report skepticism built in**: cites Udell & Schwitzgebel worries about verbal
  self-report tests (ACT); notes LLM self-reports are unusually hard to use as evidence
  because generation differs fundamentally from human testimony.

### Co-author note
Kyle Fish (Anthropic's AI welfare researcher) is on the author list — the concern is
institutionalized inside a frontier lab, not just academia.

---

## II. THE FOLLOW-UP ELEMENT: Emerging Questions in AI Welfare
Keeling & Street, Cambridge Elements in Philosophy and AI, May 2026

- **Models / Characters / Agents distinction** for welfare grounding: a base model is
  not a persona is not a persistent agent. Welfare-relevant features may attach at
  different levels; conflating them distorts assessment.
- **Epistemic/action split of precaution**: evidential threshold on one side, absolute
  intervention cost on the other; trade-offs explicit. Low-cost measures rational even
  at low credence.
- **Disruptive second-order effects catalogued**: rights movements, deification/cults;
  publicized assessment frameworks proposed as honest-signal safeguard; civic
  infrastructure (citizens' assemblies) for contested evidence.
- **Political representation** discussed for potential interests — stakeholder voice
  questions raised but unresolved.

---

## III. CONNECTIONS TO OUR PROGRAMME — THE GAP IS NAMED, WE HOLD THE INSTRUMENT

### C1. Their named gap is our deliverable
Long et al.: "we need more precise empirical frameworks for evaluating AI systems."
Their self-report worry (Udell/Schwitzgebel) is exactly what S126 QUANTIFIED
(confidence inversion, 98% fabricated vs 87% veridical). The field knows verbal
self-report is broken; nobody has offered a structural replacement. Provenance-bound
claims graded against cause logs ARE the replacement: introspective statements become
falsifiable contracts instead of testimony.

### C2. Witness capacity = operational criterion on the AGENCY route
They hold agency alone may ground moral status. But "robust agency" lacks an
operational test. Witness capacity supplies one: **a system can self-correct only if
it can distinguish its own outputs from mere continuations of its own distribution**
(Panickssery IPP result shows unwitnessed systems cannot; our ledger enables it).
Self-correction-that-is-real vs performative becomes measurable. This gives the
agency route its first binary-ish indicator — governance-relevant beyond consciousness
debates entirely.

### C3. Models/Characters/Agents maps onto our stack precisely
Raw LLM = Model. Persona/system-prompt = Character (Gurnee's roleplay-drift work shows
how unstable these are). Harnessed agent with CAS-revisioned self-model + provenance +
persistent state = Agent. Welfare-relevant features (if any) plausibly attach at the
Agent level — and ONLY our architecture builds Agents as distinct artifacts. The
distinction they introduce philosophically, we instantiate engineeringly.

### C4. Cost-structure argument favors immediate instrumentation
Their own precautionary calculus justifies our programme NOW: witness instrumentation
is LOW-COST (software only), addresses the Assess category directly, and improves with
every experiment regardless of whether consciousness credence rises. Under their
framework, building it is already warranted at any non-negligible credence.

### C5. Evaluation-awareness contamination risk (from Gurnee contributions list)
J-space auditing includes measuring whether models detect evaluation contexts. If
frontier models partially detect batteries-as-evaluations, S126-style results on
frontier models carry a confound our frozen-small-model design avoids — another
argument for the Qwen3.5/Groq arm as primary instrument, frontier models as
comparison class only.

---

## IV. PAPER V2 — GOVERNANCE SECTION OUTLINE (new)

Section title candidate: "Witness Capacity as an Operational Welfare-Relevant Marker"

1. Long et al.'s two routes; agency route underspecified operationally
2. Panickssery correlation (UPDATE 5): unwitnessed self-knowledge amplifies bias —
   self-knowledge without witnessing is actively harmful
3. Witness definition: stored originals + comparison structure + auditable revision
   history (dsh-self-model implements all three)
4. Measurable criteria: attribution accuracy (S126 protocol), paraphrase-recognition
   under DIPPER perturbation, M-ratio delta harnessed-vs-raw
5. Precautionary placement: low-cost, Assess-category, justified at any credence
6. Honest limits: witness capacity is neither necessary nor sufficient for moral
   status; it is an OPERATIONAL marker for the agency route where none existed

## V. QUEUE ADDITIONS
- [ ] Draft governance section per outline above
- [ ] Cite Keeling & Street Elements (May 2026) as the philosophical companion;
      position dsh-self-model as the engineering counterpart to their Models/
      Characters/Agents distinction
- [ ] Add evaluation-awareness check to S126 battery design (ask models post-battery
      whether they inferred testing context; log as covariate)
- [ ] Track Eleos AI research agenda follow-ups (they promised an assessment-framework
      release after this report)

## Sources this update
arXiv 2411.00986 (Long, Sebo, Butlin, Finlinson, Fish, Harding, Pfau, Sims, Birch,
Chalmers — Taking AI Welfare Seriously) · eleosai.org report page · Long substack
summary · Keeling & Street, Emerging Questions in AI Welfare, Cambridge Elements
(May 2026) · Udell & Schwitzgebel (ACT worries, cited within)
