# Replication Brief — SpringFish V3.0 Beta3
_For an unaffiliated computational replication team. Prepared 2026-08-23._

---

## Objective

Independently rebuild the runtime, verify artifact integrity, rerun the authoritative
engine's test suite and a deterministic output subset, test alternative specifications,
and publish a deviation report. Author-side clean reproduction is explicitly NOT
replication; this brief exists because unaffiliated reruns are currently **zero**.

## You receive (read-only)

| artifact | location |
|---|---|
| Engine source | `SPRINGFISH_COMPLETE_RESEARCH_AND_HANDOFF_LOCAL_PC_2026_08_04/01_WORKSPACE_SNAPSHOT/restored_beta3_engine/` |
| Handoff verifier (stdlib-only) | `…/SPRINGFISH_COMPLETE_RESEARCH_AND_HANDOFF_LOCAL_PC_2026_08_04/verify_complete_handoff.py` |
| Requirements | `restored_beta3_engine/requirements.txt` (networkx, numpy, pandas, PyYAML, pytest, nashpy, scipy) |
| Canonical case configs | `restored_beta3_engine/config/cases/C1–C4 .yaml` + `data/case_subgraphs/` |

Reference results you should reproduce are recorded in the engine's
`EXECUTION_REPORT.md`, `MANIFEST.json` and `validation/`.

## Protocol

1. **Integrity first:** run `python3 verify_complete_handoff.py` from the handoff root.
   Expected: `COMPLETE HANDOFF VERIFICATION PASS` (1,226 files, 11/11 nested CRCs,
   12/12 freeze tests). Record your output.
2. **Environment:** any Python ≥ 3.11 in a FRESH venv from `requirements.txt`.
   Do not reuse author environments.
3. **Test suite:** `PYTHONPATH=restored_beta3_engine python -m pytest restored_beta3_engine/tests -q`.
   Author-side expectation: **60 passed, exit 0** (reproduced twice on macOS,
   Python 3.12 framework + Python 3.13 clean venv).
4. **Deterministic subset:** rerun any engine entry point whose outputs ship with frozen
   hashes; compare byte-for-byte where the manifest claims determinism.
   Note: detailed Study-009V-class replays require `PYTHONHASHSEED=0` — flag any file
   that varies even with it set.
5. **Alternative specifications (encouraged):** different seeds within declared ranges,
   permuted action ordering, re-derived equilibria via a second game-solver library.
6. **Deviation report:** every divergence gets: expected vs observed, minimal reproducer,
   environment fingerprint (`python -VV`, package versions), and your classification
   (environment / code / spec ambiguity).

## Boundaries

- Read-only on all canonical artifacts; no writes into author directories.
- No canonical ledger rows may be created; all simulation outputs remain SIM-classified.
- Your report is yours to publish; we ask only for a copy and the right to respond.

## Independence statement

Please include: prior exposure to this programme (none / reading only / collaboration),
and confirmation that no author was involved in producing your runs.
