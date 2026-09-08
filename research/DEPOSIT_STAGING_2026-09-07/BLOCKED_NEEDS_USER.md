# Deposit log (done by agent with your login)
- v1 published 2026-09-08: 10.5281/zenodo.22652652 (313 KB staging bundle).
- v2 published 2026-09-08: https://zenodo.org/records/22663261 (frozen paper 724b97f-era PDF + review + staging). Concept DOI above always resolves to latest.
- Paper cites the concept DOI; no text change needed for v2.

# Still needs you (agent cannot do these)
## 1. Second rater for kappa (~1 h, needs an independent person)
- Open `kappa_worksheet.csv` (18 arm-seeds; rater1 already filled from arm metadata, blind to outcome: harnessed=present, raw=absent).
- Fill `rater2_pointer_present` WITHOUT opening rater1's column (code from the run record itself), then fill `agree`.
- Compute Cohen kappa + % agreement + N=18; paste into Methods Artifact control (replace "kappa pending").
- Limitation to keep disclosed: rater1 used arm assignment as proxy, so kappa measures record-vs-assignment agreement, not two fully independent reads.
## 3. Optional calibration run (half day)
- Run calibration plan in Limitations (threshold sweep 1–5%/0.5–2% is already staged in `threshold_sweep.json`; rerun per new domain).
## Status
- Staged and pushed: manifest + 19 SHAs + README + sweep + full worksheet + paper with honest disclosures (`84f6bef`).
- Paper standing: clarity READY, methods preprint-READY / Q1-NOT READY until 1+2.
