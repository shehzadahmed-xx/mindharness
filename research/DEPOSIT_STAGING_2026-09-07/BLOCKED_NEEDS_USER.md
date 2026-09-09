# Deposit log (done by agent with your login)
- v1 published 2026-09-08: 10.5281/zenodo.22652652 (313 KB staging bundle).
- v2 published 2026-09-08: https://zenodo.org/records/22663261 (frozen paper 724b97f-era PDF + review + staging). Concept DOI above always resolves to latest.
- v3 published 2026-09-08: https://zenodo.org/records/22664712 (HEAD paper PDF + both-passes sheet + turns24 + review + staging). Concept DOI resolves here now.
- v4 published 2026-09-09: https://zenodo.org/records/22672511 (second-pass worksheet with agree column + current PDF, md5 40eaaab76471954e0da67251ab963681). Concept DOI resolves here now.
- Paper cites the concept DOI; no text change needed for v2.

# Still needs you (agent cannot do these)
## 1. Second rater for kappa (DONE by blinded agent 2026-09-08; human claim-level still R1)
- `kappa_worksheet.csv`: rater 1 (arm labels) + rater 2 (manifest purpose fields, blinded agent session) = 18/18 agree, kappa=1.000 degenerate by construction (both read assignment). Committed.
- Still needs a human: claim-level double-coding of individual claims (needs per-claim logging first) for a true reliability kappa.
## 3. Optional calibration run (half day)
- Run calibration plan in Limitations (threshold sweep 1–5%/0.5–2% is already staged in `threshold_sweep.json`; rerun per new domain).
## Status
- Staged and pushed: manifest + 19 SHAs + README + sweep + full worksheet + paper with honest disclosures (`84f6bef`).
- Paper standing: clarity READY, methods preprint-READY / Q1-NOT READY until 1+2.
