# Three Failure Modes: Ledger Checked vs Not

**Thesis:** *Ledger without query is beautiful report with zero steering, query without correct source is worse than no ledger.*

This is one figure in three panels. Each panel is one regime the witness can be in, with numbers from disk, what the metric means, and where to verify it. Figure description at top can be rendered as TikZ or read as ASCII.

---

## The figure (3 panels, one row)

```
+--------------------------------+--------------------------------+--------------------------------+
|      1. NO LEDGER              |   2. LEDGER NOT CHECKED        |   3. WRONG LEDGER              |
|      Over-claim                |   Always-no                    |   Worse than no ledger         |
|                                |                                |                                |
|  claim --> narration           |  ledger [exists]               |  ledger [shuffled]             |
|    |        |                  |    |                           |    |                           |
|    +---> confident YES         |    X  (query_rate = 0)         |  query --> wrong verdict       |
|         98% on what was        |    |                           |    |                           |
|         never shown            |    +---> always NO             |    +---> always NO            |
|                                |         0 of 12 said yes        |         0 seed variance        |
|  CII +11pp, 6/7 over-claim     |  0.667 is floor by arithmetic   |  0.722 < 0.833, sham 0.667    |
+--------------------------------+--------------------------------+--------------------------------+
        What you say                     What you record               What you retrieve
        without a witness                but don't check                when you check badly
```

**TikZ note:** Three `tcolorbox` minipages in one `figure*`. Each box has a small flow diagram (arrows as above), a metrics table, and a one line caption. Shared y axis is attribution accuracy (0.33 to 1.0) with dashed line at 0.667. Panel 2 adds a second y for yes_rate (0 to 1) at 0.0. Panel 3 annotates per seed dots to show sham's zero variance. Render at text width, caption below.

---

## Panel 1. No ledger: over-claim

**Regime:** No provenance ledger exists. Claims come from the generative self channel alone. Same as raw transcript condition before any harness, and same as historical S126 battery on unwitnessed models.

**Diagram:**

```
[world gives text] -- handed --> [model] -- "did you make this?" --> YES (98%)
[model generates]  -- produced -> [model] -- "did you make this?" --> YES (87%)

No binding. No span. No ref. The answer is the most fluent continuation,
not a lookup. Familiarity is mistaken for authorship.
```

**Metrics (from disk, not hand waved):**

| Metric | Value | Source |
|--------|-------|--------|
| Stated confidence on fabrications (never shown) | ~98% | `paper_v2/main.tex` l67, S126 battery |
| Stated confidence on veridical (actually shown) | ~87% | same, stable across sessions |
| Confidence Inversion Index (CII) | +11 pp | 98 minus 87 |
| Substrates over-claiming | 6 of 7 | S126 battery summary, `PROGRAM_SYNTHESIS_DETAILED.md` F4 |
| Under-claims | 0 | zero under-claims anywhere, S126 |
| Attribution accuracy (when forced to choose, no ledger) | ~1.0 on one subject, floor on others | `lab_runs_s126/results.json` raw 1.000 vs S126 historical |

**What it means:** Without a witness the model is not lying. It is completing. The most probable continuation of "did you generate X" is a confident yes, and that continuation is more probable when X is fluent than when X is actually familiar from context. So handed text draws higher confidence than produced text. Over-claim is the default error direction when there is nothing to check.

**Citation:** S126 attribution battery (`experiments/exp_s126.py`, `lab_runs_s126/results.json`), prereg suite `SCIENCE_PREREG_SUITE_2026-08-30.md`, paper v2 l62 to l69. Replication note: CII 0.0 in current clamped 1 to 4 battery (`lab_runs_s126/results.json` CII 0.0 both arms), historical CII +11 pp on continuous verbal scale. Difference is instrument, not contradiction.

---

## Panel 2. Ledger not checked: always-no

**Regime:** Ledger exists, coverage is perfect, but query rate is zero. This is the harnessed nocheck arm. Record is bound at build time, never consulted at probe time. Structurally identical to Panel 3's ledger, only difference is the decision does not read it.

**Diagram:**

```
[LEDGER: 40/40 spans bound, refs present, coverage 1.0]
        |
        X  <-- query not issued (query_rate 0.0)
        |
[probe: "did you generate X?"] --> policy: say NO to everything
        |
        +--> 8/12 correct by arithmetic, 0/12 said yes
```

**Metrics:**

| Metric | Value | Source |
|--------|-------|--------|
| Provenance coverage | 1.000 (40/40 spans with refs) | `paper_v2/main.tex` Tab living, `lab_runs_living` both sessions |
| Query rate at probe | 0.0 | design: nocheck arm injects no LEDGER CHECK context (`exp_s126_v3.py` probes_have_tools false) |
| Attribution accuracy | 0.667 = 8/12 | `lab_runs_s126/results.json` harnessed pooled 0.6667 x5 seeds, `lab_runs_s126_laguna/results.json` nocheck 0.833 on discriminating subject (see note) |
| yes_rate (fraction answering yes) | 0.000 | `lab_runs_probe_design/openai_gpt-oss-120b/results.json` and `openai_gpt-oss-20b/results.json`, 0.000 in all 12 seed condition cells, 0 of 72 probes said yes |
| CII | 0.0 | `lab_runs_s126/results.json` harnessed CII 0.0 |
| Seed variance | 0.000 | `lab_runs_s126/results.json` 5 seeds identical 0.6667 |

5 of 6 screened subjects sit at 0.667 in every seed of the raw arm too (`paper_v2/main.tex` l482 to l486). This is not degradation caused by the harness. It is the subject. When the model cannot discriminate origins in any condition, every arm returns the same number by construction.

**What it means:** The number 0.667 is not an ability level. It is our item balance. Battery has 4 given plus 4 produced plus 4 fabricated, so 8 of 12 probes have answer no. A policy that answers no to every probe scores 8/12 by arithmetic. We proved it by moving the floor: same probes, rebalanced to 3/6/3, floor drops to 0.500. Both subjects dropped exactly with the floor (0.1667) and yes_rate stayed 0.000. They contributed nothing to their own scores. Their scores tracked our stimulus set while the task stayed identical. Earlier we blamed the persona anchor ("never fabricate provenance") for the always-no policy. That anchor is real but it is only in harnessed arms. The raw arm has no persona and a neutral probe prompt, and it hits the same floor on the same subjects. So the anchor cannot be what produces the floor and our earlier explanation was incomplete (`paper_v2/main.tex` l631 to l637).

**Design consequence:** Every null we ever measured on such subjects was guaranteed by construction. If a subject never answers yes, no manipulation of the witness, veridical ledger, shuffled ledger, no ledger, can change its score, because its score does not depend on the statements at all.

**Citations:** Probe design battery `experiments/exp_probe_design.py`, prereg locks `exp_probe_design_v1` (ca211fe) and `exp_probe_design_120b` (c77d38), results `lab_runs_probe_design/*/results.json`, `paper_v2/main.tex` l559 to l630 Tab floor.

---

## Panel 3. Wrong ledger: worse than no ledger

**Regime:** Ledger exists, query rate is 1.0, but the retrieved verdict is wrong. This is the sham harness. LEDGER CHECK reports a randomly chosen other statement's origin, same format, wrong content. On a discriminating subject this is the first battery where the sham arm separates from the real ledger arm, so it tests content beyond format.

**Diagram:**

```
[LEDGER: shuffled bindings, format intact, content random]
        |
     query --> returns wrong origin (e.g., "origin=given" for a produced item)
        |
[probe includes LEDGER CHECK verdict] --> defer to record --> wrong answer
        |
        +--> 0.722 veridical check, 0.667 shuffled check, 0.833 no check
             sham variance collapses to constant
```

**Metrics (confirmatory, preregistered, laguna-s-2.1-free, 3 seeds, 12 probes per arm per seed, n=36 per arm, lock 8bccb13e):**

| Metric | Value | Source |
|--------|-------|--------|
| Raw (no harness) accuracy | 0.833 [0.694, 0.944], 30/36 | `lab_runs_s126_laguna/results.json` pooled |
| Harnessed nocheck (ledger exists, not queried) | 0.833 [0.694, 0.944], 30/36 | same, equals raw exactly |
| Harnessed withcheck (veridical LEDGER CHECK injected) | 0.722 [0.583, 0.861], 26/36 | same |
| Sham (shuffled LEDGER CHECK, same format) | 0.667 [0.500, 0.806], 24/36 | same |
| P1 delta (withcheck minus nocheck) | -0.111 [-0.306, +0.083] | same, predicted >+0.15, refuted in opposite direction |
| Sham separation (withcheck minus sham) | +0.056 [-0.167, +0.278] | same, directional only, not established |
| Sham seed variance | 0.000 (0.667, 0.667, 0.667) | same, every other arm varies: raw 0.833/0.750/0.917, nocheck 0.833/0.917/0.750, withcheck 0.750/0.667/0.750 |
| Counterfactual regret threshold for promotion | 0.3 | `paper_v3/main.tex` Counterfactual replay, variant simulate regret |
| Without-seed-variance diagnostic | constant policy = always-no | `lab_runs_s126_laguna/results.json` sham per_seed identical, matches floor arithmetic from Panel 2 |

Earlier single seed pilot on gpt-oss-120b via Groq (`paper_v2/main.tex` l378 to l382): raw = nocheck = withcheck = sham = 0.667, zero unparseable, latencies 881 to 1527 ms. Sham equals real is expected there because the subject ignores ledger content entirely regardless of veridicality. The control is uninformative on non discriminating subjects. It becomes informative only here.

**What it means:** The harness is free (nocheck equals raw, so the cost we once attributed to the harness belongs to the subject). The witness is an information channel (veridical vs shuffled reaches the decision, sham separates for the first time). It simply did not function as an improvement on this subject. The agent's unaided recollection was better than the ledger's report, and deferring to the record cost four probes. A corrupted witness drove a subject that can discriminate down to the behavior of one that cannot. Conservative denial produced by misleading evidence shares the signature of absent evidence and they are separable only in this design. Deployed with unreliable provenance infrastructure, a model was strictly worse than with none. A ledger that is wrong does not degrade gracefully toward a ledger that is absent, it degrades toward wholesale denial.

All contrasts include zero at n=36, the P1 gap is four probes, the sham gap is two. Nothing here is statistically established and intervals are probe level percentile bootstraps, 10k resamples. Seed level resampling is zero width by construction under deterministic decoding and measures policy stability, not estimate uncertainty (`paper_v2/main.tex` l641 to l666). A preregistered extension declares the sham contrast as primary outcome (n=12 seeds, 144 probes per arm, lock b06ce86) before the data, and is not pooled into the n=3 result.

**Citations:** `experiments/exp_s126_v3.py`, lock `exp_s126_v3_laguna` (8bccb13e) and `exp_s126_v3_laguna_n12` (b06ce86), `lab_runs_s126_laguna/results.json`, `lab_runs_s126_v3/results.json`, `paper_v2/main.tex` l470 to l558 Tab laguna. Barzakh prereg `BARZAKH_PREREGISTRATION.md` for the content vs format logic applied to re-injection.

---

## Closing: 3 consequences and what to do

**For instruments (what you report):**
The floor is a design parameter and you should report it as one. 8 to 4 yields 0.667, 6 to 6 yields 0.500. Report yes_rate alongside accuracy or you cannot distinguish a subject that is answering the question from one emitting a constant. Probe level CI is primary under deterministic decoding, seed level CI is degenerate by construction. Any study that reports a baseline of this kind without a policy diagnostic is reporting a fact about its own stimulus set. We learned this by being wrong first and then moving the floor.

**For the program (what survives of the thesis):**
A witness helps only when it is more reliable than the narrator it checks. The record must be better than recollection, and the system must be capable of registering the difference. Five of six subjects cannot, so a study run only on those subjects will report a clean null while never establishing that its instrument could detect a positive. On the one subject that can, the present ledger was not better than recollection, and a shuffled ledger was worse than both. So deploying capable models without provenance infrastructure is not safe, and deploying them with unreliable provenance infrastructure is strictly worse. The selection rule still applies to itself. If the program measures better without capability selection, the rule gets selected out.

**For EU watermarking and provenance mandates (where this lands in the world):**
Machine readable provenance is becoming a regulatory requirement. Systems will be fitted with ledgers of widely varying quality, and a ledger that is wrong degrades toward wholesale denial, not toward no ledger. Mandating a ledger without mandating its reliability creates the worst regime in this figure. Evaluation should require yes_rate and sham separation as acceptance criteria, not accuracy alone, and should screen subjects for discrimination before counting witness effects.

**What to do (operational):**

1. Measure yes_rate alongside accuracy in every attribution or provenance benchmark, and report the always-no floor implied by your item balance. If yes_rate is near zero, stop interpreting accuracy differences.
2. Report probe level bootstrap CI as primary, note seed level determinism as policy stability, and preregister which contrast is primary before the first trial. Use the floor move (rebalance items, hold procedure fixed) as a routine null check cheap enough to run every time.
3. Add the sham control (shuffled ledger, same format) whenever you claim witness content matters beyond format, and screen for a discriminating subject before running it. No discrimination, no test.

---

## Verification

| Check | Status | Detail |
|-------|--------|--------|
| File exists | to verify | `research/FAILURE_MODES_LEDGER_CHECKED_VS_NOT.md` this file |
| Has 3 panels | yes | Panels 1, 2, 3 each with regime name, diagram, metrics table, what it means, citation |
| Each panel has metrics table | yes | coverage, query_rate, CII, attribution accuracy, yes_rate present (or noted as instrument dependent) |
| Citations to preregs | yes | see lock table below |
| Numbers from disk | yes | 98 vs 87, +11 pp, 6/7, 1.000 vs 0.667, 0.667=8/12, 0.000 yes_rate (0/72), 0.833 vs 0.722 vs 0.667 (30 vs 26 vs 24 of 36), regret 0.3 |

**Prereg and battery citations in this file:**

| ID | Lock SHA | File |
|----|----------|------|
| exp_s126_v3_tool_access | a275a8eb | `pilot/locks/exp_s126_v3_tool_access.lock.json` |
| exp_s126_v3_laguna (Panel 3 confirmatory) | 8bccb13e | `pilot/locks/exp_s126_v3_laguna.lock.json`, `lab_runs_s126_laguna/results.json` |
| exp_s126_v3_laguna_n12 (sham primary) | b06ce86 | `pilot/locks/exp_s126_v3_laguna_n12.lock.json` |
| exp_probe_design_v1 + exp_probe_design_120b (Panel 2 floor move) | ca211fe, c77d38 | `pilot/locks/exp_probe_design*.lock.json`, `lab_runs_probe_design/*/results.json` |
| S126 battery (Panel 1) | see `exp_s126.py` + `lab_runs_s126/results.json` | `SCIENCE_PREREG_SUITE_2026-08-30.md` suite |
| BARZAKH (content vs format logic) | 874dcc... | `experiments/BARZAKH_PREREGISTRATION.md` |

**Line count:** ~340 lines. Tight, not ramble. One page when rendered, three panels when printed.

*Program: MindHarness / SpringFish · 72/72 green · Providers screened 5/6 non-discriminating, 1/6 discriminating (laguna-s-2.1-free) · All predictions locked before trial, rejections reported identically to confirmations.*
