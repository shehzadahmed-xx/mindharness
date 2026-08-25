# POINT-BY-POINT RESPONSE TO REVIEWERS
Status: DRAFT — requires fresh session to implement fully

## R1 #14 (CRITICAL): Raw=1.000 contradicts thesis
RESOLUTION: S126 measured confidence inversion; v3 battery measured origin
discrimination. These are DIFFERENT capabilities. A model can discriminate
perfectly (v3 raw=1.000) while still confabulating about WHY it generated
something (S126 confidence inversion). Paper conflated them. FIX: separate
claims explicitly. The thesis applies to CONFIDENCE CALIBRATION, not to
ORIGIN DISCRIMINATION.

## R1 #1-2: Zero variance = tautology; no statistics
ACCEPT. Greedy decoding on frozen model gives identical outputs by
construction. Fix: report per-probe distribution, add bootstrap CI over
probes, remove "zero variance" as a finding. The FINDING is the direction
(always-no vs perfect), not the absence of noise.

## R1 #4: Ceiling effect on raw arm
ACCEPT. Task too easy for raw model. Fix: increase difficulty or add
harder probe classes. The 0.667 harnessed score is more informative than
the 1.000 raw score because it's below ceiling.

## R1 #8: No sham-harness control
VALID AND CRITICAL. Add sham-harness arm (structurally identical harness,
shuffled ledger entries) to isolate content effects from format effects.
Queued as next experiment.

## R1 #14 + #15: Narrow claims
ACCEPT. Remove "across architectures" from abstract (only one architecture
tested). Remove "architectural" claim about deterministic strategies
(decoding regime explains determinism). Narrow to "on this substrate."

## R2 #1: Prior work exists
ACCEPT. Cite Longpre et al. 2021 (knowledge conflicts), Turpin et al. 2023
(language models don't say what they think), Lanham et al. 2023. Our
contribution is the ENFORCEMENT MECHANISM (structural witness), not the
CONCEPT of knowledge-conflict resolution.

## PRIORITY ORDER FOR REVISION
1. Resolve #14 contradiction (reframe thesis)
2. Add sham control arm (#8)
3. Add probe-level bootstrap (#2)
4. Cite prior work properly (R2 #1)
5. Narrow all claims to match evidence (#15)
6. State decoding config (#13)
