# Blocked — needs you (agent cannot do these)
## 1. Mint DOI (~15 min, needs your login)
- Zip: `zip -r deposit_2026-09-07.zip DEPOSIT_STAGING_2026-09-07/`
- Zenodo (zenodo.org → New upload → reserve DOI) or OSF (osf.io → new registration).
- Paste DOI + registry URL into `WE_ARE_THIS_PATTERN_PLAIN_2026-09-07.tex` Data availability + Methods pre-registration (2 lines), recompile, push.
## 2. Second rater for kappa (~1 h, needs an independent person)
- Open `kappa_worksheet.csv` (18 arm-seeds), fill `rater2_pointer_present` without seeing rater 1.
- Compute Cohen kappa + % agreement + N; paste into Methods Artifact control (replace "kappa pending").
## 3. Optional calibration run (half day)
- Run calibration plan in Limitations (threshold sweep 1–5%/0.5–2% is already staged in `threshold_sweep.json`; rerun per new domain).
## Status
- Staged and pushed: manifest + 19 SHAs + README + sweep + full worksheet + paper with honest disclosures (`84f6bef`).
- Paper standing: clarity READY, methods preprint-READY / Q1-NOT READY until 1+2.
