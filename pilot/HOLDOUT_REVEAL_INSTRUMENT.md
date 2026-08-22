# Held-Out Reveal Session Instrument — Scenario C3
_Pilot protocol v0.2 §8 step 4. For use ONLY after `PREDICTION_LOCK.json` exists._

---

## Preconditions (verify before recruiting any reveal session)

- [ ] `pilot/PREDICTION_LOCK.json` exists in the predictions directory (run `python3 pilot/prediction_lock.py <dir> --operator <you>` to create it).
- [ ] All reveal sessions will be completed before ANY result from them is discussed with later participants.
- [ ] Compensation ready; session budgeted ≤ 25 minutes.

## Session script

### 1. Framing (read verbatim, Bangla or English per participant preference)
> "We are showing you one last short decision scenario today. It was not part of your
> earlier tasks. There are no right answers we expect — we are comparing how different
> decision procedures behave on the same case. Your answer is recorded like your earlier ones."

### 2. Neutral presentation rules
- Present C3 exactly as encoded: Venezuela/PDVSA claim-realisation situation,
  three constitutional options (restricted selective access / licensed transparent
  restructuring / licensed senior creditor capture), identical parameter sheet the
  agents received — translated faithfully, no added commentary.
- Do NOT mention: what any agent predicted, which option Study 009V favoured,
  the words "correct", "optimal", or "what most people choose".

### 3. Capture fields (one row per participant → `reveal_responses.csv`, append-only)

| field | notes |
|---|---|
| participant_pseudonym | links to consent L1 record |
| scenario_id | constant `C3` |
| chosen_action | one of the three constitutional options |
| confidence | integer 1–5, self-reported |
| one_line_reason | verbatim, ≤ 30 words |
| session_timestamp | Asia/Dhaka |
| order_note | if revealed after other sessions, record count |

### 4. Post-session
- No debrief on "right answers" (none exists); thank + pay immediately.
- Participant may withdraw their reveal row under protocol §3 rights within 30 days.

## Scoring linkage (executed once, by a different analyst than the moderator)

- **Human reference target** = majority chosen_action across reveal responses
  (report full distribution alongside; suppress nothing internally, aggregates only externally).
- Compare against locked predictions of A1–A4 and (if available) realised outcomes.
- Score directional mechanism class and equilibrium status ONLY — never point magnitudes.
- Every attempt row retained including nulls/conflicts; one pass, then freeze results.
