# Shariah-Compliant Structure as Tested Constitution Design
## Formalizing Fiqh al-Muʿāmalāt as Institutional Mechanism Design

_Working draft v0.1 — prepared 2026-08-23. Sections 1–4 and 6–7 complete for internal review;
Section 5 (results) is a preregistered placeholder gated on the first observed Baraka
transaction run through the SpringFish engine._

_Backbone: `ESC_SLD_FIQH_CROSSMAP.md` (four-column map). Formal series: Event–State–Contract
Finance Papers 1–7 (`NextStep/Event–State–Contract-Finance/01_CURRENT_CANONICAL_SEVEN_PAPERS`)._

---

## Abstract

Islamic commercial law (fiqh al-muʿāmalāt) is usually presented as a system of prohibitions:
no riba, no gharar, no qimār. This paper proposes a structural rereading: the classical rules
compose into a *constitution of risk allocation* — an assignment of state-contingent losses to
named parties under explicit information and priority rules. We formalize this reading using
an event–state–contract framework (ESC series) in which financial architectures are compared
under identical shocks while varying only institutional rules. Under this lens, Shariah
compliance corresponds to a region of a measurable constitutional design space defined by
three axioms: state-contingency of returns (*against* the stipulated increment of riba),
specifiability of contingencies (*against* gharar), and liability-follows-gain (*al-ghunm
bil-ghurm; kharāj biḍ-ḍamān*). We show that the engine's constitutional-comparison operation
— same project, alternative loss-allocation constitutions, common random shocks — is exactly
the operational form of this axiomatic test, and we preregister a comparison ladder over
financing structures (interest-bearing loan, murābaḥa, salam-type milestone finance,
mushāraka) on identical productive templates. The framework yields three contributions: a
formal demonstration that coherent valuation requires no interest-bearing claim (ESC P1);
a measurable fidelity index ranking Islamic structures by genuine risk redistribution; and a
governance discipline (declared exhaustion rules, audited custody separation) that converts
compliance from certification into tested design. The paper claims structural analysis only:
simulation informs architecture; Sharīʿah validity remains with qualified scholarship.

**Keywords:** riba; gharar; ghurm bil-ghurm; mechanism design; incomplete contracts;
state prices; Islamic finance; simulation; constitutional political economy

**JEL:** G21; K12; D86; O16

---

## 1. Introduction

Two literatures ask one question in different languages. Incomplete-contract theory asks who
should hold residual control and bear residual risk when contracts cannot specify every state
(Hart [ref]; Grossman–Hart–Moore [ref]; Tirole [ref]). Classical fiqh al-muʿāmalāt answered a
version of the same question centuries earlier by regulating which claims may exist at all:
returns must remain contingent on real outcomes, uncertainties must be specified rather than
traded blind, and gain may not be severed from liability. The first literature has formal
power but treats Islamic law, at best, as an exotic case study; the second has a millennium
of juristic reasoning but lacks counterfactual instruments — clauses are argued permissible
or beneficial, rarely simulated against alternatives under named stresses.

This paper supplies the missing junction. Our contribution is not normative ("Islamic finance
is better") nor apologetic. It is architectural: we show that the classical axioms, read
structurally, define admissible regions of a contract-design space; that modern simulation
methods can locate structures within that space; and that doing so produces rankings,
stress diagnostics, and governance requirements that neither doctrine-only nor design-only
approaches generate alone.

The vehicle is the Event–State–Contract (ESC) Finance programme — seven papers establishing,
inter alia, that arbitrage-free pricing requires positive state prices rather than a traded
interest-bearing bond (Paper 1); that debt's economic functions decompose and its insurance
function survives reconstruction through funded state-contingent protection (Paper 2); that
every promise needs a complete claims constitution specifying funding assets, valuation rule,
first-loss party, exhaustion rule, and enforcement authority (Paper 3); that payment custody
and investment value must separate (Paper 4); that mutual protection diversifies idiosyncratic
but never common risk (Paper 5); that monetary support operates through incidence-bearing
outright operations rather than emergency loans (Paper 6); and that ownership is an
institution bundle — cash-flow, information, control, liquidity, access, and integrity rights
— rather than a profit share (Paper 7).

## 2. The axiomatic reading

We extract from the classical corpus three axioms, stated as constraints on claims:

- **A1 — Contingency (anti-riba).** No payoff may be fixed by stipulation while the
  underlying outcome remains uncertain to the payor. Formally: the claim's payoff function
  must vary across at least the states in which the underlying venture fails. The prohibited
  object is *al-ziyāda al-mashrūṭa*, the predetermined increment — not return per se, which
  muḍāraba and mushāraka lawfully generate precisely as compensation for borne risk.

- **A2 — Specification (anti-gharar).** Subject, quantity, delivery, and contingency
  structure must be determinate. Formally: the payoff function must be defined on a spanned
  (or explicitly declared-incomplete) state space; undefined contingencies may not be priced
  or transferred silently.

- **A3 — Liability symmetry (al-ghunm bil-ghurm; kharāj biḍ-ḍamān).** Entitlement to gain
  entails exposure to corresponding loss, and revenue rights over an asset entail
  responsibility for it. Formally: first-loss assignment in the claims constitution must be
  aligned with residual-claimant status; no agent may hold protected upside against another's
  unprotected downside absent explicit, priced, disclosed support.

Two derived principles follow. **Sadd al-dharīʿa** (blocking the means): structures that
recreate a prohibited payoff through indirect clauses fall under the prohibition — this is
the anti-formalism clause, and it is why a "Shariah-compliant" label cannot end analysis.
And **custody separation**: payment monies held as trust (*amānah / wadīʿa*) are categorically
distinct from investment monies taken on a profit-sharing basis (*muḍāraba*) — a balance-sheet
separation axiom centuries before the run-prevention literature reached the same conclusion
(ESC Paper 4 proves the trilemma that makes the separation necessary).

Read this way, compliance is not a binary certificate but a position in a design space whose
axes are exactly the ESC constitutional parameters: financing-rule fixity, evidence-gate
strictness, guarantee disclosure, ownership timing, waterfall priorities, transparency.

## 3. The formal bridge

Table 1 (in `ESC_SLD_FIQH_CROSSMAP.md`, Sections A–E) gives the complete mapping. Its load-
bearing rows:

| classical rule | constitutional parameter | ESC anchor |
|---|---|---|
| riba prohibition | financing-rule fixity (fixed vs state-contingent claim) | Ch.5 fixed/contingent chains; P1 pricing |
| gharar prohibition | evidence gates; contingency specification | P3 Prop.1–3 |
| ghurm bil-ghurm | waterfall priorities; first-loss assignment | P3 Prop.4 claims-location Λ(ℓ) |
| kharāj biḍ-ḍamān | ownership-timing; ownership-after-failure map | P7 ownership constitution ⟨F,I,C,L,A,R⟩ |
| amānah custody | payment/investment separation | P4 Props.1–2 |
| ḥisbah accountability | integrity rights R; audit + clawback | P7 fraud-deterrence condition |
| qarḍ ḥasan | lender-of-last-resort as trustee operation | P6 five-policy incidence taxonomy |

Three consequences follow.

**(i) Valuation without riba is a theorem, not a hope.** Absence of arbitrage requires
positive state prices, not a bond (ESC P1). The shadow price of certainty that emerges from
the pricing functional is a valuation object, not a loan; ι = 0 removes exactly the
stipulated increment. Prior κ-corpus measurements (81 analyses, retired corpus) survive as
orderings — contingent premia rank consistently across markets even though levels embed the
reserve-currency premium. The Sharīʿah question thereby reduces to a single decidable point
already posed to the board: is a fully contingent, loss-bearing premium permitted under
al-ghunm bil-ghurm?

**(ii) Structures rank by achieved risk redistribution.** Because A1 constrains payoff
fixity, we can define a *fidelity index*: the share of venture states in which each party's
realized payoff moves with realized outcome. Prediction: loan < murābaḥa ≈ near-debt (fixed
installments; title window aside) < salam-type milestone finance (contingency enters via
delivery verification) < mushāraka (full symmetry). This ordering is a hypothesis the
engine can falsify.

**(iii) Compliance requires published exhaustion rules.** A3 forbids silent migration of
loss onto unprotected parties; ESC P3 Prop.5 shows declared-exhaustion architectures are
more coherent than higher-stated-benefit ones. Takaful pools therefore cannot promise
benefits beyond funds (P5's quadrilemma) — classical takaful practice already knew this.

## 4. Method

We use the constitutional-comparison protocol of the parent programme: identical productive
template; alternative financing constitutions (loan / murābaḥa / salam-milestone /
mushāraka); common random numbers so differences attribute to rules; multiple seeds and
model families; all outputs labelled SIM until prospectively scored. Actor choices pass a
legal gate; equilibria and unilateral regret computed per cell; stress grid includes price,
mortality, delay, and buyer-default shocks (the Brazil tokenized-livestock analogue anchors
implementation plausibility; a domestic livestock pilot supplies observation).

Negative controls bind: a fairly-priced guarantee, a fully cost-internalizing project, and
access-without-wedge cases must produce non-firing verdicts; the framework must be able to
say "this compliant structure is merely expensive," not only "different."

## 5. Results — PREREGISTERED PLACEHOLDER

_Gated on the first observed Baraka equipment-finance transaction (frozen contract +
collar-verified identity + registered claim). Preregistered outputs, before any run:_

- R1: loss-path tables per structure under the common shock set (who absorbs, in order).
- R2: fidelity-index values with bootstrap intervals; test of ordering loan < murābaḥa <
  salam < mushāraka.
- R3: stability profile (pure-Nash share, maximum regret per cell).
- R4: divergence between doctrinal expectation and simulated incidence, flagged for
  board review rather than smoothed.
- R5: human-reference comparison when pilot data permit (self-retest ceiling methodology).

No results exist yet. This section intentionally contains no numbers.

## 6. Boundaries

Four limits discipline any reading of this work. **(i) Reductionism:** madhhab plurality and
maqāṣid objectives mean the axioms model a family of positions, not one monolith; the design
space admits school-specific parameterisations. **(ii) Authority:** structural analysis is
not fatwa; nothing here certifies permissibility, which remains with qualified scholarship —
the simulation advises the board's question, it does not answer it. **(iii) Honesty about
near-debt structures:** if murābaḥa simulates ≈ debt, we print that; industry-critical
findings from within the framework are features, not embarrassments. **(iv) Evidence
classes:** all simulation outputs are conditional, decision-support artifacts; no forecasting
claim attaches to them, and prospective scoring follows preregistered holdout discipline.

## 7. Implications and conclusion

For Islamic economics: fiqh al-muʿāmalāt gains a counterfactual instrument — doctrines
become comparable as designs, not only derivable as rulings. For mechanism design and
incomplete-contract theory: a thousand-year jurisprudential archive becomes a structured
laboratory of alternative risk-allocation constitutions. For practitioners: transaction
packages can carry computed loss-allocation architectures and fidelity scores alongside
certification, giving boards, investors, and affected parties one legible document.

The closing proposition mirrors the parent programme's: a genuinely riba-free system is not
one replacement contract but a constitution — measure events, specify contingencies, keep
returns state-contingent, align liability with gain, fund every promise, separate custody
from investment, publish exhaustion rules, and subject the whole design to adversarial
comparison before reality runs the test for you.

---

### References — status

ESC series Papers 1–7 (canonical seven, latest drafts v5) cited throughout; classical
doctrinal sources (al-Shāṭibī's maqāṣid treatment, madhhab muʿāmalāt primers, AAOIFI
governance standards) and modern finance anchors (Hart; Tirole; Duffie–Singleton via ESC
restoration appendices) to be completed with exact editions by author before circulation.
Placeholders deliberately not fabricated.
