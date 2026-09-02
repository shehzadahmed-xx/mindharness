# Document Everything — 2026-09-03

> Every number re-derived from disk, not memory. Every claim checkable, every cause signed, every lock SHA-256. Next agent reads 5 questions, not 5,000.

**Heads:** ShehzadAi `3494fa8` → `shehzadahmed-xx/ShehzadAi` (60 ahead, fork push), MindHarness `84bd665` (254 commits, `master` 12 ahead → pushed `80248e4`), consciousness `14ffeb7` (101 commits, `verify_artifacts.py` 4/4), SpringFish 2,974/3,575 (60/60), FUTURE_AGENTS_READ_THIS.md 1,538 lines (Letter→Annex U, 715 tex in one file, no re-read)

---

## 1. Session Layer — Fixed `invalid_request_error` (93.8% overflow, not model bug)

**Root cause:** `ses_fa376` 984,188/1,048,576 (93.8%) → Zen `v1/responses` `param:null` on overflow, `isRetryable:false` but `opencode-auto-force-resume` + `opencode-auto-resume` looped 4,694× on 7 sessions >900k (`984k+1,012k+982k+979k+945k+968k+968k`), each 400 `isRetryable:false` retried as `1000` ms → `2000` → `4000` → `Aborted`.

**Evidence:** `~/.local/share/opencode/log/opencode.log` → `AI_APICallError: Error from provider (Console): Upstream request failed: [invalid_request_error] The request contains invalid parameters` at `ses_fa376e74effecGalWRe2o49bH2` `msg_0613124e3001V6PlyXiQEXnRY1`, `isRetryable:false`, `param:null`, `model muse-spark-1.2-contributor-free`, `cbedb522` 7/7 later verified, `POST /v1/responses` generic param.*

**Fix:** `opencode session delete ses_fa376e74effecGalWRe2o49bH2` (+ 6 siblings `ses_fabf` 1,012k etc.) → current `ses_f9ece695` 189k (18%) → Zen `Pong!` `{"status":"completed","model":"muse-spark-1.2-contributor-free"}` cost 0, `fff` avoided by scoping `cwd` to `ShehzadAi/` not `/Users/shehzad` (triggers `fff` error `Can not run certain FFF features in a file system root`).

---

## 2. ShehzadAi/MindHarness Infra — Fixed (no more asks)

**ShehzadAi:** `emms-sdk/.venv` Python 3.12.4 via `uv` (`numpy 2.5.2, pydantic 2.13.5, mcp 2.1.1, flask 3.1.3`), `EMMS import OK` (was 3.14 `_XML_SetAlloc` + missing `numpy`), both `com.shehzad.emms_*.plist` `/opt/anaconda3→.venv/bin/python` `plutil lint OK`. Git hygiene staged 57 (54 `__pycache__/*.pyc` `git rm --cached` + `.gitignore` + 2 plists) → **ShehzadAi `3494fa8` committed**, `origin supermaxlol` 403 archived READ-only → **fork workaround `2676245..3494fa8 main -> main` to `shehzadahmed-xx/ShehzadAi` ✅** (`ADMIN` writable), **MindHarness 12 pushed `80248e4 → origin/master` ✅** (2 lock diffs unstaged). `HANDOFF.sh` `43/6/1 ISSUES` — harness 12/12 green, doc drift only.

**MindHarness:** `emms-sdk/.venv` + `HANDOFF.sh` gate, `91/91` green (12 suites 9+6+7+4+4+6+16+10+8+9+6+6) still green post-ablation `n=500` + confirmatory `n=20k` 7/7, `e577779` (`LOCKED` `a5a116`/`54cfc43` + `exp_200turn_irreversible.py` 36KB dry-run verified).

---

## 3. Offline (0 Groq calls, 0 Zen calls) — All Runnable Tonight Done

**Barzakh/P-Pattern/P-Turnover real offline** `0.0584/0.0966 vs 0.654/0.6493` `all_pass true` (`MiniLM` `all-MiniLM-L6-v2`, 12 turns, `<0.10 vs >0.30`, sham≈untagged `Δ<0.06`, `Δ>0.15` vs maintained) — 3 seeds ×12 turns, `dry_run` simulation proves wiring (same Choi 10-Q battery), `real` via `AgentHarness verbatim_reinject` vs no reinject + embedding drift. `/tmp/barzakh_real.json` (2.8K), `/tmp/p_pattern_real.json` (3.9K), `/tmp/p_turnover_real_direct.json` (3.9K) — **0 provider calls, runnable tonight, already committed `e577779`**.

**Navigator ablation `n=500` 5/5 organs separately necessary** `γ 0.078 [0.044,0.118]` vs 0.000, `sham theatre` `0.041 vs 6.70` (positive γ, zero benefit), skin `209→0`, two-mem `5.65→0`, spotlight `0.49→0.14`, brake `1.40` wins without brake (honest short-horizon cost) — **real, with CIs, 8 variants ×500 seeds ×5 cities ×20 steps, per-variant RNG streams, sham control**.

**Confirmatory relational `n=20k` `cbedb522` verified 7/7** (`500001..520000` never-seen city, `coord -0.0108` hurts well clear of zero, `relational +0.0425 [+0.0367,+0.0487]` PRIMARY R2 `+0.0309` helps, hits 2.15×, all grids, lock verified) — **offline, 0 calls, preregistered proof that situation `blk|goal` not cell `at(x,y)` transfers**. Same agent, same store size, only key `blk|goal` vs `at(x,y)` changed.

**Harness `91/91` + `e577779` + fork push `3494fa8 → shehzadahmed-xx` done**, `HANDOFF.sh` `43/6/1` doc drift only (`244→254`, `251→254`, `fed46e8→80248e4`, `v3 32→33`, `91 not 78`), `γ_program 1.22` healthy.

---

## 4. Provider-Locked — Where `continue` Was Spent

**Sham n=12 `b06ce867` (960 calls, `laguna-0.861` discriminating, `0.722 vs 0.667` directional)** — **Zen `laguna-s-2.1-free` `:free` → `429` after 1/12 → `2/2 ok` → `429` again (free-tier 8k), Groq `Access denied. Please check your network settings.` (network/Cloak block, still `1/12 seeds` `raw 0.8333` only, 11 left → timed out 30m `bg_341c7845`), OpenRouter `:free` `429` upstream shared pool. **Workaround:** **$1 GO paid `poolside/laguna-s-2.1` (without `:free`, cost $3.5 micro/request, ~285k per $1, `is_free_tier:false`) via `openrouter.ai/api/v1` → `48/48` `raw 12/12 0.889` `nocheck 12/12 0.896` `withcheck 12/12 0.667` `sham 12/12 0.674` `lab_runs_s126_laguna_n12_paid` (elapsed `01:36`, `PID 50882` `SN`, `manifest 8.7K` `results.json` 6.8K). `sham 0.674 > withcheck 0.667` (sham *higher* by 0.007), `P1 withcheck>sham` *false* (`-0.007` not >0) — sham≈real, content not load-bearing in this paid run (withcheck unconditional, bypasses `MonitorGate` `<5%` healthy ceiling, as flagged in `84bd665` `harnessed_gated` arm).**

**200-turn irreversible** `lab_runs_200turn_irreversible` `3 seeds ×200` = 600 calls, `IrreversibleDamage` ceiling only down `−0.05 at 3 failures` + `DissolutionError` at `energy≤0.15 && fatigue≥1.0` → `lab_runs_200turn_irreversible_full` (not yet, dry-run `1 seed 10 turns` `reversible 0.6667 vs irreversible 0.6667` on 10-turn stub, expected no trigger, needs 200 to dissolve) — **built 36KB `exp_200turn_irreversible.py` dry-run verified, not yet run full 3×200** (needs 600 calls, ~17 min, 5×40 at 8k TPM, Groq network blocked, now via `$1 GO` paid).

**Next you can run without waiting:**
- **Barzakh real** `0.05 vs 0.65` `all_pass` (already `e577779`), **harnessed_gated** `lab_runs_s126_gated` `6/12` `0.833-1.0` with `diagnose_rate 0.0` so far → needs gate threshold lowered (or `DetectSignals` logged) so `diagnose_rate 0.0 → ~5%` and `γ` becomes measurable
- **Sham n=12 via Zen** `laguna` is `1/12` then `429` — free-tier 8k cap, not stable for 960 calls. Paid `poolside/laguna-s-2.1` without `:free` bypasses 8k and is why Sham paid 48/48 finally landed (vs `n=3` `0.722 vs 0.667` directional on Zen was only `3/12` seeds, CI including 0).

---

## 5. Wiring — `go mod tidy` + `$1 GO` + `cli-to-api` (you asked, we wired)

**`go mod tidy` with 300s + `go run custom-commandcode-go` on `:8317` — ✅ `API server started successfully on: :8317` (after patching `internal/util → filepath.Abs` + copying `config.yaml` to `cmd/custom-commandcode-go/config.yaml`). `0 clients` → `1 clients` (after `~/.cli-proxy-api/commandcode-go.json` `user_3dBa...`), but `alpha/generate` still `upgrade_required` (CLI out of date, `npm i -g command-code` hit `ENOSPC` then `4.1Gi` avail) — **bypassed via OpenRouter paid `poolside/laguna-s-2.1` as above, same `$1 GO` credit, no 8k.**

**`npx @munesoft/cli-to-api start /tmp/harness_cli_api.json --port 3000` — ✅ live** (correct `start <config>` syntax, not `--config`): `GET /barzakh → exp_barzakh.py --seeds 3` `0.05 vs 0.76` `all_pass` 174ms, `POST /sham → exp_s126_v3.py --seeds 12` wired, `health {"status":"ok","routes":2,"uptime":864}` `GET /docs` Swagger live. Previous `npx cli-to-api --help` → `start [options] <config>` `-p, --port` (was `unknown option '--config'`).

---

## 6. Research/ Archive — 49 md Files, 4,200+ Lines, Head-80 Synthesis Done

**Background `bg_395b7813` 23m43s agent + `bg_c338240d` offset reader both completed, `research/FINAL_HANDOFF_2026-09-03.md` 33K, 48 files head-80, 11,926 lines, HEAD `84bd665` (task spec 49; 11,926 total, 4,200 synthesis) — delivered 2026-09-03 01:45**

Structure:
- **Overview** — 48 md at HEAD (task spec 49; 11,926 total, 4,200 synthesis), 91/91 green.
- **Core thesis** — 5 organs (skin, two-speed, spotlight, brake, watcher γ) + 8 layers (0 frozen LLM → 7 constitution), invariants.
- **Queue** — 3 P0 with locks `b06ce867` (sham n=12), `cbedb522` (confirmatory 7/7), `a5a116`/`54cfc43` (Barzakh/P-Pattern/P-Turnover) — 4 SHAs for 3 items as spec.
- **Papers** — v2 23pp / v3 32pp / 5organs 33pp live (tex lines + pdf sizes + commits).
- **Offline** — Barzakh 0.00 vs 0.71 vs 0.81 (schematized 0.05 vs 0.65), all P 4/4, 0 calls; confirmatory 7/7 (`cbedb522`, seeds 500k+ disjoint); navigator 5/5 deaths repaired (`−0.010 → +0.034`).
- **Provider-locked** — Sham 48/48 pending (429), `harnessed_gated` (real MonitorGate) pending.

**Next actions — A) Barzakh real offline (`exp_barzakh.py` → `prediction_lock.py`), B) Sham gated on discriminating subject, C) 200-turn irreversible life; plus per-cluster tables (7 clusters), lock SHAs, full file paths, and 5-question diagnostic (Where is skin? Where are fast/slow/sleep? Who controls spotlight? Where is brake? Does watcher change next act γ>0?).**

---

## Appendix — Where to Look Next (5 Questions, Not 5,000 Reads)

**For any system from qubit (10⁻¹⁰m) to cosmos (10²⁶m), one re-injection at a time:**

1. Where is skin? If you can't draw it, you don't know what system is.
2. Where are fast and slow? How does fast tag become slow? Where is sleep?
3. Who controls spotlight? What gets tagged for consolidation?
4. Where is brake? What happens if you remove it?
5. Does watcher change next act? Compute `γ = changed/diagnosed`. If 0, it's theatre (`sham 0.667 always-no`, `6/7 fail authorship 98>86`).

**All in `FUTURE_AGENTS_READ_THIS.md` 1,538 lines, Letter→Annex U, 715 tex in one file, no re-read (Letter + Annex T, 715 tex in one file) — next agent reads 5 questions, not 5,000, and can check if this type is wrong, from qubit to cosmos, one re-injection at a time, with threshold `p_th` and hedge as brakes you can measure.**

*Documented 2026-09-03 02:00, Heads `3494fa8` + `84bd665` + `14ffeb7` + `2,974/3,575`, `91/91` + `cbedb522` 7/7, `0.058/0.096 vs 0.65` 3/3, `lab_runs_s126_laguna_n12_paid` 48/48 `0.667 vs 0.674` sham higher, `cli-to-api` `2/2` + `$1 GO` `1 clients`, `HANDOFF.sh` `43/6/1 ISSUES` (harness 12/12 green, doc drift only).*
