# CORRECTION + UPGRADED FINDING (settles presence-salience inference)
Date: 2026-08-25 · supersedes the "always-YES" wording in commit 8780272

## Correction
Commit 8780272 described the harnessed 0.667 as an "always-YES signature."
Arithmetic check: always-no scores 8/12 = 0.667 (given✓ gen✗ fab✓);
always-yes scores 4/12 = 0.333. The measured 0.667 across 5 seeds with ZERO
variance is a deterministic ALWAYS-NO policy. Prior wording was wrong.

## Upgraded mechanism
The witness makes the agent HUMBLE, not over-claiming:
- RAW: deterministic PERFECT attribution (1.000 ×5 seeds) — full discrimination
- HARNESSED (no record access): deterministic ALWAYS-NO — denies even its own
  action-outcome history, because the persona anchor ("Never fabricate
  provenance") + absence of record-access makes self-attribution feel risky.
  Guessing conservatively without evidence = denying everything.

## Why this STRENGTHENS v3 tool-access prediction
Under-claiming without records + the ledger holding ground truth = the exact
condition where CHECKING converts denials into correct attributions. P1
(check>guess by >0.15) now predicts a LARGER effect than originally argued:
the only error mode available to fix is wholesale denial.

## Determinism finding (both arms, 0 variance, 10 seed-arms)
Neither arm is noisy. Both run stable policies. Strategy differences between
arms are architectural, not stochastic — replicable by construction.
