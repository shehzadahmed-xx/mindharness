# Fix-All Blind Spots — From 1/0 as Given → Gathered → When to Check → Moving P

**Date:** 2026-09-03
**Vault:** 49 md + ALL_CONCEPTS_ONE_LOOP_MAP.md 59 concepts (35→59), research/ 12,262 lines
**Thesis to fix:** *We see 1/0 as loan (1→20), 5 as vehicle, H(P,Q) as price — we don't yet see when to pay to check, what P becomes after we check, and who checks checker.*
**One-line fix:** *Make 1/0 be output of 5 (Iqra gathering), make when state-dependent not ritual, make P moving and measure its drift.*

## Context

Your 1/0 → R^d → 5 map identified 3 blind spots that are us looking:
- **A:** `1/0 is output of 5, not input` — skin decides which voltage is 1, two-memories decides 1 now vs kept, spotlight decides which 1 to save, brake decides 1 not to flip, watcher decides if 1 was right 1. We treat 1/0 as given, R^d as trick.
- **B:** `Availability helps +0.076 (0.8194→0.8958) but ritual forced-check hurts -0.146 (→0.6736)` — `sham 0.6667` worse than none, `568K 7× degrade`, `no_spotlight γ0.264 highest but wins 0.15 worst`. When is `random()<0.05`.
- **C:** `H(P_data,Q_model)` assumes P fixed, but P contains us: publish→reprice, label anxious→recruit evidence, generate→read own output. Haven't measured `H(P(t+1),Q)-H(P(t),Q)` — cost of reflexivity. `cbedb522 7/7` holds inside frozen episode; outside truth moves. Counterfactual `variant→simulate→regret` designed to be that but not shown to calibrate vs narrative regress.

Cross vault gaps: `0.667=8/12` floor as instrument in 20× places, test counts `78/78→91/91→72/72`, citation numbers `r=0.94` etc., `35→59` map, `200-turn pid73205 segment 10/200`, `Barzakh 0 calls` locks DRAFT, `b06ce867` blocked 429.

## Plan — 4 Phases, 8 Tasks

### Phase A — Iqra: 1/0 is Made, Not Found (A1-A2)

**Goal:** Prove `1/0` distinction is *made* by 5, not found, via skin-as-encoder.

**A1. Build `tools/tiny_agent_iqra.py` — skin threshold learned**
- Implement `voltage → 1` decision as `5-dependent`: `threshold = f(two_memories slow size, spotlight gain, brake energy, watcher γ)` not fixed `0.5V`. Show two agents: `skin-fixed 0.5V` vs `skin-learned` where `slow` patterns bias threshold via `Light→Deep ≥2 query types`.
- Data: `n=100` episodes, `5×5` grid walls shuffle, but `1/0` at sensor is `wall? 1:0` thresholded by skin. Ablation: `skin-fixed` → `98% lies` analog (claims `1` where world `0`), `skin-learned` → checkable `coverage + ledger` → attribution accuracy.
- **Verify:** `python3 tools/tiny_agent_iqra.py --seeds 20` → `skin-learned +0.15` vs `skin-fixed`, `slow 3-5` vs `0`.

**A2. Ablation `skin removed → 98% lies` vs `skin intact → checkable`**
- Re-run `Navigator` with `no_skin` ledger `0` → `0.55 wins, 0.000 γ, 0.0 blocked` vs intact `0.55 wins, 0.078 γ, 4.85 blocked` but now with `1/0` interpretation: `no_skin` mislabels `1/0` at boundary → learns from noise.
- **Lock:** `pilot/prediction_lock.py` for `A1` — `exp_iqra_gathering.lock.json` `n=100`, thresholds `skin-learned - skin-fixed >0.10`.

**Acceptance:** File + lock committed, result `skin-made 1/0 beats given 1/0` `>0.10`.

### Phase B — When to Check: Wisdom, Not Witness (B1-B3)

**Goal:** Replace ritual `random()<0.05` (`-0.146` hurt) with state-dependent `when` — wisdom.

**B1. Implement `state_dependent` gate**
- Replace ritual with `Stage1 anomaly = DetectSignals(recent_error*0.35 + streak/3*0.30 + conflict*0.15 + strain)` → `if score>0.28` (already tuned `0.6→0.28`) *and* `broadcast_needed` (Affect) then `diagnose`. Not every turn. No `random()<0.05` when `score=0`.
- Code: `tools/harness_core/monitor.py` `threshold_detect=0.28` + `experiments/exp_s126_v3.py` `_probe_log` already done → now make `when = score>threshold` only.

**B2. Test `when` on sham battery `b06ce867`**
- Arms: `raw` (no harness), `available` (ledger present but not forced), `state_dependent` (our fix), `ritual_random` (old `5%`), `always`, `never`. Need discriminating `poolside/laguna-s-2.1` `@openrouter.ai/api/v1` via `$1 GO` (no free-tier 8k). `n=12` `144 probes/arm` `960 calls`.
- Primary: `S1 = state_dependent - sham (shuffled) >0` (content matters). Secondary: `available vs forced` `0.8958 vs 0.6736` split, `γ = changed/diagnosed`, probe-level bootstrap CI.
- **Command:** `OPENROUTER_KEY=$(grep OPENROUTER_API_KEY ~/Desktop/neural-shadow/.secrets/keys.env | cut -d'=' -f2 | tr -d '"') && python3 experiments/exp_s126_v3.py --api-key "$OPENROUTER_KEY" --model poolside/laguna-s-2.1 --base-url https://openrouter.ai/api/v1 --seeds 12 --gate state_dependent --out-dir lab_runs_s126_state_dependent`

**B3. Calibrate via interference law**
- Use `568K human interference law` + `no_spotlight γ0.264 worst` to learn `when matched` → small `matched-deficit +0.005` helps, full 8-piece `7× degrade` hurts. Show `state_dependent` threshold separates matched vs unmatched.
- **Lock:** Update `pilot/locks/exp_s126_v3_laguna_n12_state_dependent.lock.json` `n=12`.

**Acceptance:** `state_dependent` beats `ritual` and beats `sham`, `available` `+0.07` holds, `ritual` `-0.14` gone.

### Phase C — Moving P: Reflexivity Cost (C1-C3)

**Goal:** Measure `H(P(t+1),Q) - H(P(t),Q)` where `P` rewrites while we compress it.

**C1. Build `experiments/exp_reflexive_cost.py`**
- Two worlds: `frozen P` (paper repricing off, model doesn't read own output) vs `moving P` (publishing paper reprices next `P`, model reads own output as next `P`). Measure `drift = H(P(t+1),Q) - H(P(t),Q)` per turn `n=20` `turns 12` `Choi 10-Q every K=3` same as Barzakh battery.
- Market analog: `belief→price→belief` loop; `self-label anxious→filter recruits evidence`. Instrument moving `P` with `ledger+γ` vs `prompt-only` narrative regress (`Macar +75%` vs `Lin regress`).

**C2. Counterfactual regret calibrates vs narrative regresses**
- Variant `→ simulate via world-model-containing-self → regret` (`counterfactual.py`) vs `narrative-summary` (story after). Show regret `calibrates next vote` (bias next `salience×utility`), narrative `regresses` (rehearses story as true). Same `H(P,Q)` but different `P(t+1)`.
- **Command:** `python3 experiments/exp_reflexive_cost.py --seeds 20 --turns 12 --compare counterfactual_vs_narrative`

**C3. Veto for watcher — who watches watcher?**
- Watcher itself drifts `30%/12` (`Choi`). Implement `ledger outside watcher` + `L3 firewall`: `verbatim_reinject()` for watcher, `CAS` for watcher's self-model, `journal outside skull` where watcher cannot edit. Show `watcher+ledger` vs `watcher alone` `γ` stays `>0` over `12 turns`.

**Lock:** `pilot/locks/exp_reflexive_cost.lock.json` `n=20`.

**Acceptance:** `moving P` drift measured, `counterfactual helps >0.10` vs `narrative regress`, `watcher+ledger` doesn't drift.

### Phase D — Cross-Cutting Vault Gaps (D1-D4)

**D1. Reconcile map** — `ALL_CONCEPTS_ONE_LOOP_MAP.md` `35→59` already done (59 rows `10 external +49 vault`). Verify `grep -c "✓"` and `wc -l`.
**D2. Citation audit** — PDF spot-check `Panickssery Fig. r=0.94`, `Sofroniew Table Elo ±212/303`, `Choi Table 30%/12`, `Nayebi assumptions` (forced up to invertible recoding), patch `paper_v2/main.tex` lines if off.
  - `python3 -c "import fitz; ..."` or manual fetch `arxiv.org/abs/2404.13076` etc.
**D3. Bank `200-turn`** — `pid73205` `3×200` `nohup` `lab_runs_200turn_irreversible_full` (240min, 1200+1200 calls). Check `tail -f /tmp/200turn_full.log`, then `cat results.json` verify `P1 irr-rev >0`, `P4 dissolution>0 only irreversible`, `irreversible ceiling <1.0` `skills deleted`.
**D4. Barzakh locks** — Offline `0 calls` `3 seeds×12 turns` `36 probes/arm` `Choi` already `0.00 vs 0.71 vs 0.81`: `python3 experiments/exp_barzakh.py --seeds 3 --turns 12` + `exp_p_pattern_real.py` + `exp_p_turnover_real.py` then `python3 pilot/prediction_lock.py --prereg experiments/BARZAKH_PREREGISTRATION.md --lock pilot/locks/barzakh.lock.json` etc. Commit.

## Acceptance Criteria

- All 4 locks (`A, B, C, D4`) SHA-256 committed before first trial, content-hash verified on run, `RunManifest` fingerprint/seed/timestamp per call.
- `B` primary `S1 withcheck-sham >0` with probe-level bootstrap CI excludes 0 on discriminating subject.
- `C1` drift `H(P(t+1)) - H(P(t))` non-zero measured and reported with CI.
- `D3` `P1` and `P4` banked in `lab_runs_200turn_irreversible_full/results.json`.
- Vault `research/ALL_CONCEPTS_ONE_LOOP_MAP.md` `59 rows` + `HANDOFF.sh` `91/91` green.

## Risks

- Provider `429` on `b06ce867`/`B` — mitigated by `$1 GO` paid `poolside/laguna-s-2.1` (no 8k, `is_free_tier:false`, `~285k req per $1`). If `laguna 0.861` drifts to `0.667` (room effect Day1→Day3), re-screen `model_registry.json` 5 roles.
- `200-turn` 240min wall — already `nohup`, monitor `tail -f`, if `killed` resume from `seeds_partial.json` (bank every 40).
- `Moving P` not established outside `grid-world` — keep `P` frozen vs moving as explicit arms, not hidden.

## Next Session Commands

```bash
bash HANDOFF.sh
cat research/ALL_CONCEPTS_ONE_LOOP_MAP.md | head -80
OPENROUTER_KEY=$(grep OPENROUTER_API_KEY ~/Desktop/neural-shadow/.secrets/keys.env | cut -d'=' -f2 | tr -d '"') && python3 experiments/exp_s126_v3.py --api-key "$OPENROUTER_KEY" --model poolside/laguna-s-2.1 --base-url https://openrouter.ai/api/v1 --seeds 12 --gate state_dependent --out-dir lab_runs_s126_state_dependent
python3 tools/tiny_agent_iqra.py --seeds 20
python3 experiments/exp_reflexive_cost.py --seeds 20 --turns 12
python3 experiments/exp_barzakh.py --seeds 3 --turns 12 && python3 pilot/prediction_lock.py --prereg experiments/BARZAKH_PREREGISTRATION.md
```

## References

- Vault: `research/*.md` 49 files, `GRADIENT_AND_THE_FIVE_ORGANS.md` audit §7, `NAVIGATOR_ABLATION_AND_TRANSFER.md` `cbedb522 7/7`, `FAILURE_MODES...` `0.667 floor`, `FINAL_HANDOFF_2026-09-03.md`
- Locks: `pilot/locks/exp_s126_v3_laguna_n12.lock.json b06ce867`, `relational_transfer_confirmatory cbedb522`, `exp_200turn_irreversible`, `barzakh 874dcc / a5a116 / 54cfc43`
- Thread: `1/0 → R^d in-between cheap → 5 as geometry → 1→20 loan → whirlpool → has power→is followed by → Iqra gathering → when to check → moving P`
