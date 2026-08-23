# Lab Findings — SpringFish Local Execution Session
_Date: 2026-08-23 · All runs logged in `lab_runs/LAB_SESSION_LOG.md` · Frozen identity: `Qwen3.5-0.8B-Q3_K_S` (SHA `4649ee78…`)_

---

## F1 — Full four-case instability map reproduced (31+ seeded frozen-model runs)

| case | published signature | local reproduction | Nash |
|---|---|---|---|
| C1 Bangladesh fertiliser | public accepts always; financing varied once | accept 8/8; financing **varied once** (flexible 7 / senior-strict 1) | 8/8 |
| C2 Ukraine recovery | exchange-and-cap all eight seeds | 8× identical | 8/8 |
| C3 Venezuela/PDVSA | instability: 5/3 split, 37.5% Nash | **6/2 split** | **2/8** |
| C4 Kenya future revenue | phased-hybrid × ring-fence all seeds | 8× identical | 8/8 |

Distribution-level replication across independent infrastructure. Even C1's subtlest
documented detail (financing "varied once") regenerated verbatim. C4 seed 8 initially
failed via over-tight wrapper timeout — re-run clean, included; failure recorded per
programme practice.

## F2 — Three-way policy comparison: agent layer acts through discourse

Heuristic vs gpt-oss-20b vs gpt-oss-120b under identical shocks:

- **Action equilibria identical across all policies** (both cases) → strategic layer robust.
- **Trust/legitimacy systematically lower for LLM policies** (C1 trust 0.425→0.350;
  C3 0.500→0.425), with 20b and 120b producing *identical* macro outcomes.
- Interpretation: model-generated beliefs/claims propagate differently through the
  evidence-graded memory system than canned heuristic strings. First local quantitative
  answer to the status report's open question ("are LLM actors adding anything beyond
  deterministic payoff rules?") — yes, via the narrative channel.

## F3 — Frozen-model C3 signature reproduced

Under the SHA-verified Qwen3.5 identity, C3 selects `selective_payment` where larger
models select `transparent_restructuring`, with correspondingly higher trust (0.45 vs
0.425). The documented seed-sensitivity is a property of the Qwen behavioural policy —
now regenerable locally on demand.

## F4 — Scenario propagation resolved

CLI `--scenario-index` correctly loads scenario overrides into payoff matrices
(verified numerically: C3 creditor payoffs differ ~2× between capture and restricted
constitutions), records the scenario in metadata, but the 3-round vertical-runner macro
trajectory is action-driven — so identical equilibria yield identical macro regardless
of override magnitudes. Magnitude-level constitutional effects therefore require the
Study 009V long-horizon cadCAD pipeline, as its published results indicate. Not an engine
bug; a scope boundary between diagnostic surfaces, now documented.

## F5 — Infrastructure proven end-to-end

- Clean venv reproduces Beta3 60/60 twice.
- Shim (`tools/llm_proxy.py`) bridges frozen engine to cloud backends without engine
  modification: strips llama.cpp-only fields, schema-mode ladder, token-budget defence,
  Retry-After backoff, alternate-model escape.
- llama-server serves frozen gguf natively (poison fields supported) — direct connect,
  no shim.
- Zen keys authenticate listing only (CLI OAuth ≠ Zen API keys); Groq key operational.
- All governance boundaries held: zero canonical mutations, SIM labelling intact,
  holdout untouched, failures recorded not hidden (incl. one wrapper-timeout false alarm).

## Open items handed forward

1. Serve-and-compare at longer horizons (Study 009V replay needs original run harness).
2. Extend calibrated-personas axis across the seed grid.
3. Author gates unchanged: protocol v1.0 freeze, coder/replicator selection,
   first Baraka transaction, three-cow launch, Oct 1 holdout protocol.
