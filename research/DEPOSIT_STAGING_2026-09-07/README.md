# Deposit staging — mint on upload
## What is staged
- `manifest.json` — 19 frozen prediction locks (names + timestamps)
- `locks.sha256` — SHA-256 per lock
## To mint (needs your Zenodo/OSF login — agent cannot mint)
1. Zip this folder: `zip -r deposit_2026-09-07.zip DEPOSIT_STAGING_2026-09-07/`
2. Upload to Zenodo (new upload, reserve DOI) or OSF (new registration for the 19 locks).
3. Paste the DOI + registry URL into `WE_ARE_THIS_PATTERN_PLAIN_2026-09-07.tex` Data availability + Methods pre-registration (replace "to be minted on upload").
## Kappa worksheet (pending second rater)
- Sample 10% of coverage claims, double-code present/absent pointer, report Cohen kappa + % agreement + N double-coded.
- Current status honestly labeled in paper: single-rater plus audit, kappa pending.
## Power note (in paper Methods)
- 964/2000 Wilson [0.460, 0.504] width ~4 points; 91-setting panel detects only large gaps (rule-of-three 3/91); 7/7 Wilson [0.646, 1.000].
