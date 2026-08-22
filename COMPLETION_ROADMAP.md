# SpringFish / Spring-Loaded Door — COMPLETION ROADMAP

_Compiled 2026-08-23 from: V34.2.4 handoffs (2026-08-12), STUDY009R migration index,
programme status report (reviewed 2026-08-21, V34.2.7 merged checkpoint),
V33.2 complete archive, and the 2026-08-04 local-PC handoff (verifier PASS, Beta3 60/60)._

---

## 0. Where the programme actually stands

**One-line state:** an empirically grounded, internally validated, operational
institutional simulation laboratory — construction complete, external qualification at zero.

| Layer | Maturity | Basis |
|---|---|---|
| Theory (SLD + Architected Extraction) | **2/2 operational** | Master synthesis through Ch. 266 |
| Canonical graph V34.0 | **2/2** | 2,974 actors / 3,575 rel / 1,614 instruments / 1,364 mechanisms / 577 claims / 1,965 sources / 625 tasks |
| Empirical base | **2/2** | Panels (9,386 WID country-years; 164 IMF crises), historical falsification, RFQ markets (1.52M blocks), Bangladesh procurement, platform studies 007E–007H |
| Runtime | **2/2** | Beta3 CLI/adapters/cadCAD — verified here post-move (60/60) |
| AE qualification | **1/2 partial** | AEQ-001 Practice Fusion USD 959,700 bounded component, author-side only |
| Behavior calibration | **1/2** | Graph-calibrated Qwen actors; parameters partly synthetic |
| V34.2 consolidation | **1/2** | V34.2.7 merged runnable candidate — NOT canonical |
| Independent coding | **0/2** | Coder packet prepared, never executed by unaffiliated coder |
| External replication | **0/2** | Zero unaffiliated reruns |
| Prospective outcomes | **0/2** | RQ-621 holdout sealed until **2026-10-01 Asia/Dhaka** |

Validated core record: 16/16 pre-registered fire-vs-forbearance, 7/10 trajectories,
four falsified alternatives; L8 signature disconfirmed; directional classifier rejected.
Study 009V: 4 cases × 8 seeds × 4 model families × 12 constitutions = 384 paths /
9,600 quarterly rows (all SIM). C3 (PDVSA) is the honest instability case.

---

## 1. Folder map (what lives where now)

| Path | Contents |
|---|---|
| `THE_SPRING_LOADED_DOOR_COMPLETE_RESEARCH_ARCHIVE_V33_2_SPRINGFISH_V0_2_2026-07-31/` | Full theory+evidence+network+sim archive (start: `00_START_HERE.md`) |
| `SPRINGFISH_COMPLETE_RESEARCH_AND_HANDOFF_LOCAL_PC_2026_08_04/` | Beta3 engine + RQ621 freeze (**verified PASS post-move**) |
| `SPRINGFISH_COMPLETE_RESEARCH_MIGRATION_UPDATED_STUDY009R_2026_08_12/` | Nested portable migration → Study 009R candidate |
| `SPRINGFISH_V34_2_4_MIROFISH_BRIDGE_EXECUTION_MIGRATION_DELTA_2026_08_12/` | Ch.266 bridge execution delta + master synthesis copy |
| `SPRINGFISH_COMPLETE_RESEARCH_MIGRATION_HAMBA_FULL_2026_08_21.zip.part-*` | Full workspace mirror as of 08-21, stream-verified (`270420ac…`). Top state inside = V34.2.4 mirror + **V34.2.6 AEQ-001 qualification candidate** + **HAMBA pilot-001 frozen run**. WARNING: does NOT contain the V34.2.7 Study009V merge cited by the status report — that lives only on the producing machine |
| `HAMBA_HANDOFF/` | Extracted from parts via stream: Aug-21 `00_HANDOFF` (PROJECT_STATE `HAMBA-PILOT-001-RECOVERY-1`: 8/8 code tests, 12/12 gates, 58,368 paths, decision C10 control / C12 target / C11 red-team-only), MIGRATION_MANIFEST.json, checksums + file catalog |
| `HAMBA_HANDOFF/rq620_coder_packets/` | **RQ-620 external coder BLINDED packet (10 KB) + full external coder packet (93 KB)** — item C's ship-ready artifacts, now local |
| `SPRINGFISH_CANONICAL_RUNTIME_RECOVERY/` | V2.1D repaired runtime + legacy venv (shebangs stale after move — rebuild venv before use) |
| `THE_SPRING_LOADED_DOOR_MASTER_SYNTHESIS_V34_2_2/_V34_2_3…md`, `03_…_V34_RC2.md` | Synthesis generation chain |
| Network ledgers V17/V28/V32, priority waterfall, atlas, branch packs, ESC/Baraka bundle | Supporting evidence & packages |
| `SPRINGFISH_COMPLETE_STATUS_REPORT_2026_08_21.html` | The authoritative narrative status (source of §0) |

Canonical authority remains **V34.0 ledger + SpringFish V3.0 Beta3 engine** even though
V34.2.7 is the most complete merged runnable candidate.

---

## 2. Open items → governing boundary → concrete next action

### A. BLOCKER-0 (environmental): disk space for full HAMBA extraction
- **Status update (2026-08-23, second pass): RESOLVED.** Full stream-extraction of all
  4,799 entries (~1.60 GB) to `HAMBA_full/`; bundled `verify_migration.py` returned
  **checked=4797 mismatches=0 EXIT=0**. Parts remain untouched as provenance.
- **Known gap:** the V34.2.7 merged Study009V migration is NOT in this archive.
  Retrieve it from the producing machine, or proceed with V34.0 + Beta3 + V34.2.6
  candidate which ARE local and verified.
- **Clean-room runtime:** rebuilt at `runtime/.venv` (Python 3.13) from Beta3
  requirements; Beta3 suite reproduced **60/60, exit 0** in the fresh environment.

### B. Behavioural calibration pilot (the scientific frontier)
- **Boundary (Ch. 266.7 / detailed handoff):** consented, purpose-limited evidence;
  participant rights to access, correction, deletion, use-logging, benefit;
  comparison ladder fixed: deterministic → documentary-persona → demographic-persona
  → interview-grounded → self-retest ceiling → observed outcome.
  Empirical-frequency policy only from a versioned observed-action dataset.
- **Status:** design-only; Bangladesh, n=60–100 proposed.
- **Next action:** draft participant-governance & consent protocol (this folder,
  `pilot/01_participant_governance_protocol.md`) → then IRB-style review checklist →
  instrument design → held-out scenario sealed before first interview.

### C. Independent evidence coding (RQ-620)
- **Boundary:** external coder must be unaffiliated; blinded packet + codebook already
  exist and are NOW LOCAL at `HAMBA_HANDOFF/rq620_coder_packets/` (blinded 10 KB +
  full 93 KB, extracted from V34.2.6 candidate). Disagreements recorded and
  adjudicated, not forced to consensus; M2 stays unauthorised until coding completes.
- **Next action:** identify coder; ship the blinded packet; log inter-coder reliability.

### D. Unaffiliated computational replication
- **Boundary:** external team rebuilds env from requirements, verifies checksums, reruns
  code, tests alternative specifications, publishes deviation report.
  Author-side clean reproduction ≠ replication.
- **Next action:** package a replication brief pointing at Beta3 root + this roadmap §1 map.

### E. RQ-621 prospective evaluation
- **Boundary:** holdout SEALED until 2026-10-01 Asia/Dhaka. On/after date: record freeze
  root (`7aa3de34…`) BEFORE retrieval; open each reserved family ONCE; keep every
  null/conflict/withdrawal row; apply frozen formulas WITHOUT revision; rerun all gates.
  Promotion currently blocked 7 PASS / 8 FAIL with 0/10 non-null states.
- **Next action:** calendar the protocol; prepare scoring script skeleton now (no data touch).

### F. V34.2.x adjudication into canonical successor
- **Boundary:** claim-by-claim review required before any candidate row enters a
  successor to V34.0. No silent rewrites of frozen manifests (fail-closed gate stays).
- **Next action:** build adjudication worksheet enumerating candidate deltas per version
  (V34.2→V34.2.7), each with admit/reject rationale template.

### G. AE qualification path
- **Boundary:** six-condition admission firewall (entity, beneficiary, period, material
  benefit, causal link, review). AEQ-001 eligible for independent review but is a bounded
  gross recipient-side amount — never call it net social loss or universal parameter.
  Negative controls mandatory: theory must be able to say "not Architected Extraction."
- **Next action:** submit AEQ-001 packet to independent reviewer alongside item C.

### H. Publication edition freeze
- **Boundary:** four claim levels stay separated (model-tested / historical /
  structural interpretation / normative). Reviewers evaluate each at correct level.
- **Next action:** after B–G produce first results, split edition into theory volume +
  methods volume + forecast-registration annex; sentence-level copy-edit pass.

### I. Runtime hygiene (local)
- Old `.venv` shebangs point at Downloads paths — rebuild clean venv from
  `restored_beta3_engine/requirements.txt` when needed (handoff forbids reusing
  `.venv-beta4`). Verified-working interpreter here:
  `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3` (+nashpy installed)
  via `PYTHONPATH=<engine root>`.

### J. HAMBA physical three-cow protocol (second empirical track, discovered 2026-08-23)
- **State:** `HAMBA-PILOT-001-RECOVERY-1` frozen on branch `hamba/pilot-001`; prospective
  model complete (8/8 code tests, 12/12 gates, 58,368 portfolio paths across 256 seeds /
  12 constitutions / 19 stresses, 36 pure-Nash profiles, local-Qwen cells zero-fallback).
  All outputs SIM. RQ-621 untouched.
- **Constitution decision (frozen):** C10 Balanced claims-control-integrity = physical
  pilot control baseline; C12 Full-cost portable evidence = pricing/documentation target;
  C11 Evil HAMBA preserved ONLY as prohibited red-team comparator; C07 Lender priority
  flagged as warning (protects lender recovery partly by leaving manager pay unpaid).
- **Next action (per PROJECT_STATE):** run the physical three-cow protocol and replace
  frozen identity, cost, evidence-use and behaviour assumptions with observed pilot data.
  This is the fastest route to a first observed-action dataset that item B's
  versioning rules can consume.

---

## 3. Non-negotiable rules (carry forward verbatim)

1. Do not open the RQ-621 holdout before **2026-10-01 Asia/Dhaka**.
2. Do not revise frozen C1 formulas for any reason, including pilot findings.
3. Simulated actions remain `SIM` / `MESSAGE_ONLY` / no executor authority — always.
4. Repetition inside simulation never upgrades evidence class.
5. Model-implied frequencies are never real-world probabilities.
6. No synthetic substitutes for `NOT_AVAILABLE` empirical objects.
7. Frozen manifests are rejected by code, not edited in place.

## 4. Suggested sequencing (updated after instrument pass)

```
Done       : A extraction+verify, clean venv, all instruments drafted
Now        : author review of protocol v1.0 + three-cow draft; select coder & replicators
Next       : ship blinded packet + replication brief; launch three-cow prep
Oct 1 2026 : E holdout evaluation (one shot, frozen formulas)
After B+C  : F adjudication worksheets → G reviewer packet → H publication split
External   : V34.2.7 retrieval from producing machine (or adopt V34.2.6 formally)
```

## 5. Instruments prepared (2026-08-23, second pass)

| instrument | path | status |
|---|---|---|
| Held-out reveal session script | `pilot/HOLDOUT_REVEAL_INSTRUMENT.md` | ready; gated on prediction lock |
| Prediction-lock tool (fail-closed; tested: dry-run / lock / immutable-refusal) | `pilot/prediction_lock.py` | ready |
| RQ-621 opening procedure | `rq621/HOLDOUT_OPENING_PROTOCOL.md` | ready for 2026-10-01 |
| External replication brief | `replication/REPLICATION_BRIEF.md` | ready to send |
| Coder shipping + chain-of-custody | `coder/RQ620_CODER_SHIPPING_PACKAGE.md` | ready; packets verified local |
| Three-cow fieldwork protocol draft | `hamba/THREE_COW_FIELDWORK_PROTOCOL.md` | v0.1 — author review |
| Full HAMBA archive (verified) | `HAMBA_full/` | 4,797 checksums PASS |
| Clean runtime venv | `runtime/.venv` | Beta3 60/60 reproduced |

Still requiring the author personally: protocol v1.0 freeze approval; coder & replication
team selection; V34.2.7 retrieval decision; three-cow launch.
