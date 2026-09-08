# Literature Review — We Are This Pattern
## What Stays Alive When Everything Changes — Plain Review of Papers Mentioned in Our Files + Web Verification
### 2026-09-07 · Sisyphus · 5906021 · 4f343dc · 292 commits · 36pp · 91/91 · 19 locks · verify 6/6 · γ_program 2.11
### Two lanes: Disk (papers we cited in md + bib) meets Web (live verification 2026-09-08)

> **How to read this review:** Each row is `Paper — What it says in one plain sentence — How it relates to our idea — Link — Where we cited it on disk`. No special words needed. `Skin` = fence that decides whose loan counts. `Two-mem` = fast sticky note + slow diary + night move. `Spotlight` = volume knob half to double before content. `Brake` = when to stop, floor fifteen percent. `Watcher` = slower loop checking faster loop (changed / checked). `Pe` = middle where flows swirl, not uniform. `1→20` = one high twenty low loan (5,800K → 255K). `R_T/T→0` = generalizing, not memorizing. `Horizon` = help only inside window.

---

## Part A — Disk: Papers We Already Cited In Our Files (Ground Truth)

### A1 — Heat, Flow, and Why Loops Must Pay (Consciousness §142)

| Paper | What it says (plain) | How it relates | Where cited on disk | Link |
|---|---|---|---|---|
| **England, J.L. 2013** Statistical physics of self-replication. *J. Chem. Phys.* 139, 121923. | Things that make copies must dump heat. There is a hard lower limit: heat depends on how fast you grow and how long you last. A common gut bacterium comes within three times of that limit. | Gives physical reason why `Pe>1` matters and why milk swirls 30-680% hold more spread than still milk. Sets why `Pe>1` middle is surfable, not magic. | `consciousness/consciousness_self_free_will_context.md:855` `DIAGNOSTIC_FRAMEWORK_NESS_FIVE_ORGANS_FORMAL.md` | https://doi.org/10.1063/1.4818538 |
| **Qian & Beard 2005** Thermodynamics of stoichiometric networks. *Biophys. Chem.* 114, 213. | Extends energy bookkeeping to open living networks. In a steady trickle (NESS), what comes in must go out; entropy production = flow × driving force, always zero or more. | Formal steady-trickle engine: living networks settle to a steady state kept by steady food/flow—exactly brain's steady condition. Your spread per second is flow × push / temperature. | same :857 | https://doi.org/10.1016/j.bpc.2004.12.003 |
| **Landauer 1961** Irreversibility and heat generation. *IBM J. Res. Dev.* 5, 183. | Erasing one known bit must release at least a tiny heat `kT ln2`. Erasing at random can be free. Thinking and forgetting have a heat cost. | Gives cost of Watcher and Brake: to forget, compare, or overwrite, brain must pay heat. Memory move is not free—limits how good Two-mem can be. In our harness, destroying a ledger is real erasure. | same :860 `mindharness/paper_5organs` | https://doi.org/10.1147/rd.53.0183 |
| **Kleckner et al. 2017** Large-scale brain system supporting allostasis. *Nat. Hum. Behav.* 1, 0069. | Brain has a big network that predicts body needs before they happen, not just reacts. | Shows where Watcher lives as a predictor that budgets energy, and where Spotlight lives as a volume knob that works before errors appear. | same :862 `embodiment.py energy 0.15` | https://doi.org/10.1038/s41562-017-0069 |
| **Ashrafi et al. 2020** Molecular tuning of axonal mitochondrial uniporter. *Neuron.* | Nerve ends far from the main cell make their own fuel on demand when firing; a special gate lowers the trigger so they can switch fuel type quickly. | Shows fueling is local: nerve tips hundreds of microns away must make fuel locally. Why heat is tightly tied to firing, and why skin (fuel import) is a bottleneck. | same :865 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7035162/ |
| **Friston 2013** Life as we know it. *J. R. Soc. Interface.* + **Sterling 2012** Allostasis | Variational free energy bounds surprise under a model; perception is controlled guessing. Allostasis is predict-before-error. | Tells apart two spreads: variational surprise (in bits) vs heat (in joules per kelvin). Same counting, different units. Watcher's precision weighting lives here. Our VFE is Shannon, not heat. | `consciousness §§141-142` `mindharness/paper_v3:202` | https://doi.org/10.1016/j.physbeh.2011.06.004 |
| **Schartner et al. 2015** Lempel-Ziv / PCI + **Anderson 2004** ACT-R | Roughness of brain signals tracks depth of consciousness, not hidden integration; ACT-R is a set of if-then production rules that model mind as modules. | Watcher: roughness tracks watcher level, not whole integration. Two-mem: ACT-R is template for our L0-L7 layers. | `consciousness/refs.bib` | — |

### A2 — Memory: Seven Items, Forgetting Curves, Seven to Diary

| Paper | What it says | How it relates | Where cited | Link |
|---|---|---|---|---|
| **Miller 1956** Magical number seven, plus or minus two. *Psychol. Rev.* | People hold about seven chunks at once, about four bits; chunking (recoding) stretches it. | Sets size of fast memory `7±2` → `M_w 7×d_w` and why spotlight can only light a few: Two-mem must compress rest. | `ShehzadAi/paper/references.bib` `emms-sdk/paper/references.bib` | https://doi.org/10.1037/h0043158 |
| **Atkinson & Shiffrin 1968** Human Memory: Proposed System | Memory flows working → short → long with control processes. | Canonical fast → slow → save. | both bibs | — |
| **Tulving 1972** Episodic & semantic | Self-memory system, autobiographical building. | Two-mem + Watcher story-self. | both | — |
| **Ebbinghaus 1885; Bartlett 1932; Loftus 1974** | Forgetting curve, schema rebuilds memory, language bends memory. | Why save `Θ` and skin record needed. | `emms-sdk/paper:189-200` | — |
| **Bliss & Lomo 1973** Long-lasting potentiation. *J. Physiol.* | A short burst for fifteen seconds can make a connection stronger for hours to days: weight can be written and kept. | Physical base for slow memory vs fast activity. Without it, no way to keep beyond flow. | — | https://doi.org/10.1113/jphysiol.1973.sp010273 |
| **Baars 1988** Global workspace; **Laird 2012** SOAR; **Anderson 2004** ACT-R | A stage where winners are broadcast = conscious access; SOAR/ACT-R are rule-based mind architectures. | Spotlight + Skin + Two-mem: our stage with nine inserts is workspace; L1 ledger is fence. | `consciousness/refs.bib` | — |

### A3 — Dissociation: 51 Tests That Pull Self Apart

| Paper | What it says | How it relates | Where cited | Link |
|---|---|---|---|---|
| **Chhikara et al. 2025** Mem0. arXiv:2504.19413 | A service for long-term memory outside the chat. | Two-mem substrate: our `d_tier 3.758 ≫ d_arch 0.105` test. | `paper_unified:9` | https://arxiv.org/abs/2504.19413 |
| **Packer et al. 2023** MemGPT. arXiv:2310.08560 | Talk to computer like it has an operating system that pages memory. | Two-mem + Skin paging. | same:18 | https://arxiv.org/abs/2310.08560 |
| **Shanahan et al. 2023** Role play. *Nature* 623 | Role can be unstable in chat. | Watcher: dissociation floor `<0.50`; betrayal null. | same:58 | — |
| **Lindsey et al. 2026** Introspective awareness; **Berg 2025** Subjective reports; **Macar et al. 2026** Mechanisms | Larger models can report their own states when nudged; vectors can turn it on +75%. | Watcher: awareness is underasked, but can be steered. Sham vs real `0.667 vs 0.903` lives here. | `CITATION_AUDIT:9 VERIFIED` `paper_unified:66,75,248` | — |
| **Nisbett & Wilson 1977** Telling more than we can know; **Johansson 2005** choice blindness | People make up reasons and miss when outcome swaps. | Watcher: why storyteller needs outside ledger. | `mem0-dissociation:178,421` | — |
| **Choi et al. 2024** Identity drift. arXiv:2412.00804 | Persona drifts >30% in eight to twelve turns, larger models worse. | Two-mem: prompt is a fading resource; careful ledger fixes it. | `paper_v3:261 VERIFIED` | https://arxiv.org/abs/2412.00804 |

### A4 — MindHarness: Why Five Are Forced (91/91)

| Paper | What it says | How it relates | Where cited | Link |
|---|---|---|---|---|
| **Nayebi et al. 2026** What Capable Agents Must Know. *UAI 2026* PMLR v337 4773-4795. arXiv:2603.02491 | If you do well on many tasks on average, you must build world models, belief-like memory, modular parts, and lasting emotion-like variables. Proved via betting. | Central proof for `R_T/T→0` → all five forced. Corollary 3→modularity, 4→emotion-like, Theorem 5→no-aliasing memory. Why Spotlight/Brake/Watcher emerge, not just engineered. | `paper_v3:99,185 VERIFIED` | https://proceedings.mlr.press/v337/nayebi26a.html https://arxiv.org/abs/2603.02491 |
| **Zhang et al. 2026** Introspection Threshold. arXiv:2607.04277 | Bare model cannot look at itself: no weight access, no fixed-point loop. | Watcher needs harness barrier; our loop `simulate_fn` = model as world model. | same:196 VERIFIED | https://arxiv.org/abs/2607.04277 |
| **Lin et al. 2026** AHE. arXiv:2604.25850 | Better scaffolding +7.3 points even with frozen weights, more than fancy wording. | Skin+Two-mem+Watcher: seeing better transfers families. | `paper_v3:67` | https://arxiv.org/abs/2604.25850 |
| **Macar et al. 2026** arXiv:2603.21396 | Concept steering finds 20% → 75% with little push, carrier suppresses gate. | Watcher: proves sham separation `0.667 vs 0.903` on our live check. | `CITATION_AUDIT VERIFIED` | — |
| **Panickssery et al. 2024** NeurIPS r=0.94 | Self-recognition tracks self-liking, line r=0.94. | Watcher: unwatched self-knowledge amplifies bias. | `paper_v3:177 VERIFIED` | — |
| **Sofroniew et al. 2026** arXiv:2604.07729 ±212/−303 Elo | Tiny emotion arrows causally move cheating, blackmail, flattery by hundreds of Elo. | Spotlight `G`: small knob moves existing channel. | `paper_v3:271 VERIFIED` | https://arxiv.org/abs/2604.07729 |
| **Cao et al. 2026** arXiv:2605.14186 +8.6pp 48.3→56.9 | Wiring checking into control (not just watching) helps. | Watcher: harness turns signal into steering. | `CITATION_AUDIT:14 VERIFIED` | https://arxiv.org/abs/2605.14186 |

### A5 — Embodied World Models: When Thinking Helps

| Paper | What it says | How it relates | Where cited | Link |
|---|---|---|---|---|
| **Assran et al. 2025** V-JEPA 2. arXiv:2506.09985 | Predicts future in representation space, not pixels; 62 hours robot data gives zero-shot planning. | World model = Two-mem + Watcher. Shows latent prediction helps acting; scales via masking. | `r:vjepa UGEA` | https://arxiv.org/abs/2506.09985 |
| **Maes et al. 2026** LeWM. arXiv:2603.19312 | First JEPA stable end-to-end from raw pixels with two losses; ~15M params, 48× faster planning, 96% Push-T. | Minimal JEPA proves horizon thesis at small scale: compressed latent prediction suffices. | `r:lewm UGEA` | https://arxiv.org/abs/2603.19312 |
| **Hafner et al. 2018 World Models; 2019 PlaNet; 2020 DreamerV3; 2024 TD-MPC2** | Latent dynamics for planning from pixels, mastering many tasks. | Horizon law: thinking substitutes for looking ahead; single-peaked help inside `[H_match,H_grd)`. | `r:ha r:planet r:dreamerv3 r:tdmpc2 UGEA` | — |
| **Pathak 2017 ICM; Burda 2019 RND; Sekar 2020 Plan2Explore** | Curiosity via prediction error or random distillation. | Spotlight (curiosity) + Brake: exploration vs settling 47/50 vs 1/50. | `r:icm r:rnd r:p2e UGEA` | — |

### A6 — Spring-Loaded Door: Why Crises Spring

| Paper | What it says | How it relates | Where cited | Link |
|---|---|---|---|---|
| **Piketty 2014** Capital. Harvard. `r>g` | When return on owns > growth persistently, own piles faster than made. | SLD driver: spring loaded by decades of `r−g` upstream of income/tax. No hidden plan needed. | `solow1956 piketty2014 springfish` | https://hup.harvard.edu/books/9780674430006 |
| **Minsky 1992** WP74 + **Keen 1995** Minsky model. *J. Post Keynesian Econ.* 17, 607. | Long calm → safe → stretch → need rising prices → snap. Banks make money when they lend. | SLD snap: calm itself makes fragility. Credit cycle like `Pe` drift beats diffusion until brake snaps. | `minsky1986 keen1995 springfish` | https://www.levyinstitute.org/pubs/wp74.pdf https://ideas.repec.org/a/mes/postke/v17y1995i4p607-635.html |
| **Turchin 2016** Ages of Discord; **2023** End Times + **Secular Cycles** | As surplus flows through owning faster than labor, the pump pulls up. Degrees outgrow jobs → fight inside top. | SLD fight: pump runs upstream of politics, naturally picks harder extraction. | `turchin springfish` | https://peterturchin.com/ |
| **Clark 2014** The Son Also Rises. Princeton. LSE WP180. `~0.75` | Using rare family names 1170-2012, deep standing correlates ~0.75 generation to generation, stable across centuries despite big reforms. Takes 15+ generations to fade. | SLD memory: complete rewrite does not reset system. Shows memory of pattern. | `clark2014 LSE WP180 springfish` | https://press.princeton.edu/books/hardcover/9780691162546/the-son-also-rises |
| **Solow 1956; Romer 1986; North 1990; Acemoglu 2012 Why Nations Fail; Jost 1994 system justification; Chetty 2014 mobility** | Growth via building, increasing returns, rules that include vs extract allocate leftovers along waterfall. | Brake `Γ_b` and Skin `I≤I_max`: how rules distribute leftovers. | `springfish_latex references.bib` | — |

---

## Part B — Web: Live Verification 2026-09-08 (Our MDs Mentioned These, Web Confirms)

### B1 — Brain Wiring That Constrains Learning (Video: 90 units → time-reverse → fail)

| Paper | What it says (plain) | How it relates | Link | Note on date |
|---|---|---|---|---|
| **Oby, Degenhart, Grigsby et al. 2025** Dynamical constraints on neural population activity. *Nature Neuroscience* 28, 383-393. Published **17 Jan 2025** (Issue Feb 2025). DOI 10.1038/s41593-024-01845-7 | Recorded ~90 units from monkey movement area, shrank to ten latent dims, gave dot feedback via two 2-d views. Monkeys moved freely in movement view but **could not traverse or time-reverse** natural path when shown the separating view, even strongly pushed. Timings persisted. | Pattern is channeled, not freely steerable. Activity follows flow set by wiring. Cannot play pattern backward at will—dynamics *are* computation. Lawful constraint, not lack of trying. Same as our brake/skin/spotlight story: `cannot reverse` = Brake `Γ_b` + Two-mem `Θ`; `cannot straighten` = `G` + `I_max`. | https://www.nature.com/articles/s41593-024-01845-7 · https://pubmed.ncbi.nlm.nih.gov/39825141/ · https://www.biorxiv.org/content/10.1101/2024.01.03.573543v1 | Your query said Jan 2026; real paper is Jan 2025 No Jan 2026 BCI with this design exists yet. Content is exactly as described. Companion: Orsborn 2025 doi:10.1038/s41593-024-01793-2 *Neural populations are dynamic but constrained*. |

### B2 — Complete Wiring That Shows What 166k Nodes Actually Cost/Enable

| Paper | What it says | How it relates | Link |
|---|---|---|---|
| **Berg, Beckett et al. 2026** Sexual dimorphism in complete *Drosophila* male central nervous system connectome. *Cell* 189, 5504-5526.e15. **03 Sep 2026** Open Access. DOI 10.1016/j.cell.2026.08.015 | **166,700 neurons, 11,710 types, 124.2M synapses**—first full male brain plus nerve cord wiring. Compared to female FlyWire to map same vs sex-specific vs different circuits; ~2.9% `fru+` and 0.2% `dsx+` neurons drive difference. | Pattern *is* wiring. Same base plan yields two stable forms via small switches. Shows what exhaustive microstructure reveals vs still needs dynamics, not just weights. Prototype for ``pattern made visible'' and what 166k costs/enables vs human 86B extrapolation. Structure constrains function; 1% wiring difference → dimorphic behavior. | https://www.cell.com/cell/fulltext/S0092-8674(26)00942-6 · https://male-cns.janelia.org/ · https://phys.org/news/2026-09-connectome-pursuing-fly-brain-rewired.html |

### B3 — World Models That Predict Without Drawing (Horizon Law)

| Paper | What it says | How it relates | Link |
|---|---|---|---|
| **V-JEPA 2 (Assran et al. 2025)** Announced 11 June 2025. arXiv:2506.09985. ViT-g encoder + predictor, >1M hours video + ~1M images. MIT license. | Predicts **future in representation space, not pixels**. V-JEPA 2 + V-JEPA 2-AC (62h robot data) hits 77.3% on action tasks, best on several understanding tests; enables **zero-shot image-goal planning** on arms 65-80% pick-and-place ~30× faster than heavy generative world models. | Latent predictive pattern scales with data/compute, generalizes zero-shot—core to horizon argument. Together with LeWM shows representation quality × horizon, not pixel sharpness. Horizon degradation remains open. | https://arxiv.org/abs/2506.09985 · https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/ |
| **LeWM (Maes et al. 2026)** 13 Mar 2026 v1, rev 03 Jun 2026 v3. arXiv:2603.19312. 15M params. | First JEPA stable end-to-end from raw pixels with two losses (one setting vs six). Single graphics card hours, 48× faster planning than big world models, 96% Push-T, competitive on other tasks; hidden probes read physical quantities. | Minimal JEPA proves horizon thesis at small scale: compressed latent prediction suffices. Same JEPA principle as V-JEPA 2 but accessible. Line: I-JEPA 2023→V-JEPA 2024→V-JEPA 2 2025→LeWM 2026→WA-JEPA Aug 2026. | https://arxiv.org/abs/2603.19312 |
| **Note on horizon law:** V-JEPA 2 §14 notes autoregressive prediction suffers pile-up of errors, long-horizon planning limited by exploding search (exponential with horizon); tested at horizon=1 only, needs subgoals for longer tasks. LeWM same. This *is* the horizon law `[H_match,H_grd)` plain: help only inside window where thinking substitutes for looking ahead. |

### B4 — Spring-Loaded Door: Four Pillars Verified Via Web Fetch

| Paper | What it says | How it relates | Link |
|---|---|---|---|
| **Piketty `r>g`** Capital in the Twenty-First Century (2013/2014) + *Capital is Back* QJE 2014 | When return on owns > growth long, owning piles faster than economy → inexorable concentration. Billionaires 6.4-6.8% real vs 2.1% avg 1987-2013. | SLD driver: spring loaded by decades of `r−g` upstream of income/tax. Competitive edge of owning compounds without plan. | https://hup.harvard.edu/books/9780674430006 · http://piketty.pse.ens.fr/files/PikettySaezZucman2013RKT.pdf |
| **Minsky FIH + Keen formalization** WP74 1992 + J Post Keynesian Econ 17, 607 1995 + Rev Political Econ 32, 342 2020 | Long calm → safe → stretch → need rising prices → snap. Banks make money when they lend; calm itself breeds risk. Keen derives from definitions + endogenous money; reproduces calm → snap and rising inequality as emergent. | SLD snap: why timing is hard but structure predicts inevitability. `Hedge→Speculative→Ponzi` is `Pe` drift beats diffusion until brake snaps. | https://www.levyinstitute.org/pubs/wp74.pdf · https://ideas.repec.org/a/mes/postke/v17y1995i4p607-635.html |
| **Turchin Wealth Pump + Elite Overproduction** Ages of Discord 2016; End Times 2023 | Surplus flows through owning faster than labor (pump). Degrees outgrow jobs → fight inside top, poor get poorer, state loses ability to mediate. | SLD fight: pump runs before politics, picks harder extraction. Late Rome, pre-Revolution France as images. | https://peterturchin.com/ |
| **Clark ~0.75** The Son Also Rises (Princeton 2014) + LSE WP180 | Using rare names 1170-2012, deep standing correlates ~0.75 generation to generation, stable across centuries despite industrial revolution, welfare, mass schooling, taxes. Takes 15+ generations to fade. Found same ~0.75 in US, Sweden, India, China, Japan. | SLD memory: complete rewrite does not reset system. Proposes latent standing with ~0.75 persistence: measured mobility overestimates true mobility because observed traits are noisy proxies. | https://press.princeton.edu/books/hardcover/9780691162546/the-son-also-rises · https://www.lse.ac.uk/asset-library/information/wp180.pdf |

---

## Part C — How To Use This Review For Your Plain Paper

- **For the whirlpool paragraph:** Pair England (heat bound) + Qian (steady trickle) + Landauer (erasure heat) as `Pe` + `S` + `H` footnotes boxed together. Add milk swirl `30-680%` with Lost City predicted as check.
- **For seven versus diary:** Pair Miller (capacity `7±2`) + Bliss & Lomo (durability hours-days) as ``capacity vs durability'' trade—why fast small and slow large must pair plus night move.
- **For ``not like, is pattern'':** Cite Nayebi `R_T/T→0` forces world models etc. + V-JEPA 2 latent prediction as ``theorem → implementation'' convergence. Cite Choi `>30%/12` vs Nayebi to show why prompt alone fades.
- **For BCI ``cannot reverse'':** Cite Oby et al. 2025 `Nat Neurosci` directly (17 Jan 2025 not Jan 2026) as ``cannot time-reverse natural trajectory even strongly incentivized''—ties to Brake `Γ_b` + Two-mem `Θ`.
- **For fly ``pattern is wiring'':** Cite Berg et al. 2026 `Cell` `03 Sep 2026` `166,700 / 11,710 / 124.2M`—prototype for ``pattern made visible'' and cost of 166k vs human 86B.
- **For horizon law `[H_match,H_grd)`:** Combine V-JEPA 2 + LeWM under heading Horizon Law; quote V-JEPA 2 error pile-up + exponential search space as limit. Contrast LeWM 48× speed vs same horizon limit.
- **For spring-loaded door:** Keep Piketty/Minsky/Turchin/Clark as single SLD section with four pillars: *Piketty loads the spring (`r>g`), Minsky describes snap (`Hedge→Ponzi`), Turchin shows who fights over released energy (elite overproduction), Clark shows why release doesn't reset (`0.75` persistence).*
- **Keep links as permalinks:** DOIs are permalinks; use AIP record, ScienceDirect, PMC, nature.com, cell.com, arXiv, levy publ., princ UP, LSE eprints as above.
- **Plain-language framing for new reader:** Each ``How it relates'' is already one plain sentence without jargon—copy-paste into `WE_ARE_THIS_PATTERN_PLAIN_2026-09-07.tex` footnotes or boxes as ``Why we need this.''

---

## Part D — Disk vs Web: What We Found While Checking

- **Nayebi 2026 is real and central.** Found at `proceedings.mlr.press/v337/nayebi26a.html` UAI 2026 Aug 17-21 Amsterdam, PMLR. If your `.md` cited it as ``theoretical,'' update to ``verified—in-print.'' It directly proves `R_T/T →0 ⇒ structured memory` move. Quote: *low average-case regret forces world models, belief-like memory and—under task mixtures—persistent regime-tracking variables resembling functional primitives of emotion*.
- **Thompson vs Miller vs Bliss:** Miller 1956 = `7±2`. Bliss & Lomo 1973 = long-lasting potentiation (Thompson's own 1973 engram work separate). Recommend citing both: Miller for capacity, Bliss/Lomo for persistence.
- **Pe=vL/D** as named brain formula has no single canonical paper—it is synthesis of England + Qian + diffusion physics; treat as derived quantity, not disputed.
- **Date correction:** BCI paper is Jan 2025 not Jan 2026; fly paper is 03 Sep 2026 (Open Access); V-JEPA 2 11 Jun 2025; LeWM 13 Mar 2026. Use these dates in review.

---

## Part E — Methods Statistics + Whole-Brain Emulation Timeline (added 2026-09-08)

Methods numbers added in Q1 passes need their own sources. Each row below is cited in the paper Methods/Results.

| Paper | What it says (plain) | Where used | Link |
|---|---|---|---|
| **Wilson 1927** Probable inference, the law of succession. *JASA* 22, 209--212. | The honest range for a share (e.g. 964 of 2000): center shifts inward and widens at small N, unlike the schoolbook plus-minus. | 95\% ranges for 964/2000, 7/7, 32/40, 30/40, 91/91. | https://doi.org/10.1080/01621459.1927.10502953 |
| **Cohen 1960** A coefficient of agreement for nominal scales. *Educ. Psychol. Meas.* 20, 37--46. | Agreement beyond chance between two raters: kappa. Needed before claiming the outside record is scored reliably. | Kappa worksheet (18 arm-seeds, second rater pending). | https://doi.org/10.1177/001316446002000104 |
| **Hanley & Lippman-Hand 1983** If nothing goes wrong, is everything all right? *JAMA* 249, 1743--1745. | With zero fails in N tries, the true fail rate could still be up to about 3/N (rule of three). | 91/91 zero-fail bound 3/91. | https://doi.org/10.1001/jama.1983.03330370053031 |
| **Page et al. 2021** PRISMA 2020 statement. *BMJ* 372, n71. | A review of many trials must state search, inclusion, and extraction-or it is a narrative review, not a systematic one. | Framing the ~568k-trial strand as cited synthesis, not a new experiment. | https://doi.org/10.1136/bmj.n71 |
| **Freeman 2026** From Worm to Human: Scaling Brain Emulation. MIT Media Arts and Sciences, March 2026 (Master's thesis; supervisor Boyden; readers Esvelt, Church). | Line-item engineering map from 302-neuron worm to 86-billion-neuron human: proofreading dominates cost (fly neuron ~$214 by 2025, mammalian $500--1,000; human connectome at $1B needs ~$0.01/neuron); compute near at hand (pessimistic ~6e20 FLOP/s, memory/interconnect the wall); wiring without receptor/channel/novel-modulator data is not emulation (strong sense open). Viral 50,000-H100 and $100/neuron and data-only-blocker versions are wrong: thesis says ~600,000 accelerators at dense FP16 under pessimistic assumptions and molecular data plus proofreading as major gaps. | Upload timeline in paper (fly-to-human path, 1 EB barrier, why wiring alone is not enough). Full PDF exceeds fetch limits; facts verified via thesis page + independent review 2026-04-22. | https://pdf.isaak.net/scaling-emulations · https://pdf.isaak.net/thesis |
| **Zanichelli, Schons, Freeman, Shiu & Arkhipov 2025** State of Brain Emulation Report 2025. arXiv:2510.15745. | Collaborative companion growing from the thesis: embodiment plus closed-loop benchmarks (activity prediction, behavior indistinguishability, perturbation) required; H100-class hardware simulates ~1M neurons with memory as bottleneck; worm/fly feasible on one GPU, mouse needs small clusters, human needs frontier-AI-scale clusters. | Same upload-timeline use; embodiment requirement matches our Skin/Watcher argument. | https://arxiv.org/abs/2510.15745 |
| **Sandberg & Bostrom 2008** Whole Brain Emulation: A Roadmap. Future of Humanity Institute TR #2008-3. | Original roadmap: scanning, translation, simulation plus embodiment; paths by capability level. | Historical anchor for emulation roadmap claims. | https://www.fhi.ox.ac.uk/brain-emulation-roadmap.pdf |
| **Dorkenwald et al. 2024** Adult fruit fly connectome. *Nature* 637. (139,255 neurons, >33 person-years proofreading.) | Proofreading cost anchor: one fly took 33 person-years; a cubic millimeter of human cortex holds ~3x the synapses of the whole fly brain. | Why proofreading dominates Freeman's cost curve. | https://www.nature.com/articles/s41586-024-07558-y |
| **Lu et al. 2024** 86-billion-neuron simulation on 14,012 GPUs, 60--120x slower than real time. | Largest human-scale run so far is simulation (no ground-truth connectome, simplified models), not emulation. | Why we call current 86B runs simulation: wiring without dynamics is not the loop holding. | (via Freeman thesis review 2026-04-22) |

---

*Literature review built 2026-09-07 23:53 → 2026-09-08 03:20 by Sisyphus · disk first (refs.bib + md where cited) then web (live websearch + webfetch 2026-09-08) → merged plain review `LITERATURE_REVIEW_2026-09-07.md` · keep desktop clean D → research/ holds 7 shores · every link re-derived, see DIAGNOSTIC_FRAMEWORK_NESS_FIVE_ORGANS_FORMAL.md 142 lines, verify_artifacts.py:201-252, HANDOFF.sh 49/49.*
*How to cite this file: Shehzad Ahmed (2026). We Are This Pattern: What Stays Alive When Everything Changes — Literature Review. mindharness/research/LITERATURE_REVIEW_2026-09-07.md · 7 shores → One Loop → whirlpool not rock · 5906021 · 91/91 · 19 locks.*

