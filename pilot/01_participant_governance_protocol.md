# Participant Governance & Consent Protocol
## SpringFish Behavioural Calibration Pilot (Bangladesh, n=60–100)

_Version 0.2-draft — prepared 2026-08-23 against COMPLETION_ROADMAP.md item B._
_Changelog: v0.2 clarifies §8 ordering (agent predictions lock BEFORE participant reveal);
v0.1 initial draft._
_Status: DRAFT for author review; not yet an executed study. No data collected._

---

## 1. Purpose

Supply the four missing empirical objects recorded `NOT_AVAILABLE` in the V34.2.x releases:

1. interview-grounded agents;
2. a human self-retest ceiling;
3. a versioned observed-action dataset;
4. one held-out realised-outcome scenario score.

The pilot compares, on identical bounded institutional decisions, how far each agent class
tracks the behaviour of real, consented participants — nothing more.

## 2. Fixed comparison ladder (preregistered; do not amend post-freeze)

```
A1 deterministic rule baseline
A2 documentary-persona baseline        (public documents only)
A3 demographic / short-persona         (aggregate traits only)
A4 interview-grounded agent            (this protocol's consent scope)
H  participant self-retest ceiling     (same participant, same decision, ≥14 days apart)
O  observed outcome where available    (held-out scenario only)
```

An empirical-frequency policy may be added **only** after dataset versioning per §9.
No other baselines may be inserted after first results are seen.

## 3. Participant rights (non-negotiable, from Ch. 266.7)

Every participant holds, at all times and without justification:

| Right | Mechanism |
|---|---|
| Access | Plain-language export of everything stored about them, on request |
| Correction | Written amendment appended to record; originals retained with flag |
| Deletion | Full erasure incl. derived artifacts within 30 days of request |
| Use logging | Append-only log of every time their material trained/grounded an agent run |
| Benefit | Stated in advance: per-session compensation + summary of aggregate findings |

Deletion of interview material ⇒ deletion of any A4 agent grounded on it. Derived
artifacts inherit the lifecycle of their source.

## 4. Layered consent (separate signature per layer)

- **L1 Participation:** bounded decision tasks + short demographic form.
- **L2 Recording:** audio/text capture of interview sessions.
- **L3 Agent construction:** use of *their* interview to build an A4 agent that will be
  re-presented to *them* for validation (the self-retest ceiling H).
- **L4 Retention:** pseudonymised storage beyond study end (default: no).

Refusing L2/L3/L4 permits L1 participation. No layer is bundled.

## 5. Data classes and the evidence firewall

| Class | Grade | Rules |
|---|---|---|
| Observed participant choice | E-part | The only behavioural gold standard |
| Self-retest divergence | E-part | Defines ceiling; divergence > threshold flags instrument fault |
| Interview transcript | Source | Pseudonymised at ingest; identifiers stripped same-day |
| A4 agent outputs | **SIM-derived** | Never enter canonical graph, never upgrade evidence class |
| All simulation outputs | **SIM** | Per standing programme rule |

Standing rules carry over unchanged: repetition never upgrades evidence;
no synthetic substitution for missing values; SIM never becomes institutional authority.

## 6. Roles

- **Principal Investigator:** owns protocol deviations log; sole authority to unseal §8.
- **Data Steward:** maintains pseudonym key offline; executes deletion within SLA.
- **Participant Advocate:** independent of modelling team; reviews instruments for
  comprehension and coercion risk; receives complaints first.
- **Analysts:** blinded to which agent output is which during scoring where feasible.

## 7. Session structure (per participant)

1. Consent (layered) → demographic short form (feeds A3 only).
2. Bounded decision set 1 — fixed scenario battery, legal action sets only,
   no free-text strategy elicitation before tasks (order effects logged).
3. Semi-structured interview (~45 min): reasoning behind choices, role familiarity,
   constraints participants believe they face. Grounds A4.
4. Debrief + compensation + rights card (how to invoke §3).

Target n=60–100; stop early only for saturation of *instrument faults*, not favourable results.

## 8. Held-out scenario (sealed before first contact)

**Selected scenario: C3 — Venezuela/PDVSA sanctions, oil cash flow and creditor
realisation** (`case_id: C3` in the Beta3 engine library). Rationale recorded in
`sibling HELDOUT_FREEZE.json`: farthest from participants' lived context (minimal
topical contamination), and the programme's honest instability case — the only one
where seed-sensitive strategy selection and positive regret were observed, giving the
comparison ladder its best discriminating power.

**Binding ordering (v0.2 clarification):**

1. Freeze hash of the C3 definition + subgraph published in `HELDOUT_FREEZE.json`
   **before** the first consent is taken.
2. During fieldwork participants **never see** C3; it appears in no interview or
   decision battery.
3. After fieldwork closes, agent configurations A1–A4 are frozen and their C3
   predictions are produced, hashed and locked.
4. **Only after** prediction lock does a final brief reveal session show participants
   C3; their majority answer becomes the human reference target.
5. One scoring pass against participant-majority and (if available) realised outcomes;
   all attempts recorded including nulls.

Scoring targets are directional mechanism class and equilibrium status — never point
magnitudes — consistent with the programme's volatility-marker discipline.

## 9. Dataset versioning

First release = `observed_actions_v1.0`: immutable, checksummed, row schema =
(participant_pseudonym, scenario_id, action, timestamp, consent_layers).
Only from v1.0 may an empirical-frequency policy be computed — and it must cite the
exact version forever. Later corrections create v1.1+, never mutate v1.0.

## 10. Risk & harm minimisation

- **Political sensitivity:** scenarios concern institutions, finance, authority. No
  question asks participants' own political affiliation or exposes them as critics of
  named living officials. Depoliticised framings available on request.
- **Small-n re-identification:** report aggregates only; suppress cells <5;
  occupation+district combinations generalised.
- **Economic vulnerability:** compensation set above local median hourly rate,
  paid regardless of answers; no performance-contingent payment.
- **Agent misrepresentation:** participants may review their A4 agent's stated reasoning
  and mark it "not mine" — such flags are published alongside any result using that agent.

## 11. What this protocol does NOT authorise

- No forecasting claim about real institutions, markets or elections.
- No entry of participant-derived rows into the canonical V34.0 ledger.
- No Architected Extraction accusation against any entity from pilot material.
- No revision of RQ-621 frozen formulas or holdout handling (opens 2026-10-01 separately).
- No publication quoting identifiable speech without renewed written consent.

## 12. Pre-fieldwork checklist (gate to execution)

- [ ] Author approval of this protocol (v1.0 freeze, hash published)
- [ ] Participant Advocate named and independent
- [ ] Instruments back-translated (Bangla ⇄ English) and piloted on 2 dry-run volunteers
- [ ] HELDOUT_FREEZE.json committed before first consent
- [ ] Compensation budget funded
- [ ] Deletion-request workflow tested end-to-end on dummy record
