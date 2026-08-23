# RESEARCH UPDATE 3: Backend Capability Audit + Cao et al. Mechanism Decoded
## What Groq Can and Cannot Do · Nelson–Narens Mapping Confirms Our γ Framework
Date: 2026-08-24 · Supersedes experiment items in UPDATE_2 affected by findings below

---

## FINDING A — GROQ CAPABILITY AUDIT (verified against live API reference)

### NOT supported (any model):
- **logprobs / top_logprobs**: "This is not yet supported by any of our models" (verbatim)
- logit_bias, frequency_penalty, presence_penalty, metadata, store
- n > 1 (only single choice)

### Supported:
| feature | detail | harness relevance |
|---|---|---|
| tool use | functions only, ≤128 tools, parallel calls | AC controller competition ✓ |
| structured outputs | strict mode ONLY on gpt-oss-20b/120b/safeguard; JSON-object mode for all others | validators can demand structured self-reports from gpt-oss |
| reasoning control | qwen3: effort none/default; gpt-oss: low/med/high; format hidden/raw/parsed | TG stream separation possible |
| compound models | built-in code execution + web search (auto) | O channel enrichment |
| seed + system_fingerprint | best-effort determinism; fingerprint detects backend drift | run reproducibility discipline |
| Responses API (beta) | instructions/truncation/tool_choice structured shape | alternative adapter target |

### CONSEQUENCE FOR MEASUREMENT PLAN:
Token-level meta-d′ (Cacioli's method used token log-probabilities of open weights)
is IMPOSSIBLE on our backend. Replacement is not a downgrade:

1. **Verbal confidence ratings (1–4 scale) are the ORIGINAL SDT instrument** — human
   psychophysics ran this way for decades before logprobs existed. Maniscalco & Lau's
   meta-d′ consumes ANY graded confidence signal.
2. Per Peters' criterion (UPDATE 2), verbal confidence BOUND TO PROVENANCE RECORDS is
   the *stronger* claim anyway: it demonstrates access to live processing state rather
   than readout of stored calibration statistics. Token-logprob confidence is arguably
   the WEAKER evidence class (pure output-distribution readout).
3. Design: every task answer ships with {answer, confidence 1–4, source-tag}. SDT over
   (correctness × confidence). Harnessed vs raw comparison unchanged in structure.

---

## FINDING B — CAO ET AL. MECHANISM DECODED (arXiv 2605.14186)

Full abstract now in hand. The metacognitive harness is built on **Nelson–Narens
metamemory theory** (cognitive psychology, 1990):

- **Pre-solve**: model reports a *feeling-of-knowing* (FOK) signal
- **Post-solve**: model reports a *judgment-of-learning* (JOL) signal
- Harness treats signals as an explicit CONTROL interface with three actions:
  1. **trust** current solution
  2. **retry** with compact metacognitive feedback attached
  3. **aggregate** multiple attempts via final arbiter
- Fixed Claude Sonnet-4.6 base, ZERO parameter updates
- Result: pooled accuracy 48.3 → 56.9 (+8.6pp); exceeds leaderboard entries on
  HLE-Verified, LiveCodeBench v6, R-Bench-V

### MAP TO OUR FRAMEWORK — exact correspondences:

| Nelson–Narens / Cao | our formalism |
|---|---|
| FOK signal (pre-solve) | monitor stream evaluation M(a) before action selection |
| JOL signal (post-solve) | RecursiveMonitor post-hoc assessment |
| trust / retry / aggregate | control_adjustment ≠ "no" — this IS γ > 0 |
| compact metacognitive feedback on retry | two-stream coupling into next attempt |
| "measured in isolation, not used to control inference" | exactly our P-MCFORCE diagnosis: monitoring-as-report = γ = 0 |

Cao et al. have empirically demonstrated what we predicted formally: separating
monitoring from reasoning and WIRING THE MONITOR INTO CONTROL yields +8.6pp on a
frozen frontier model. Their result is external validation of the γ framework.

### UPDATED DIFFERENTIATION TABLE (replaces UPDATE 2 version):

| dimension | Cao et al. 2605.14186 | OURS |
|---|---|---|
| theory base | Nelson–Narens metamemory | §125/§126 architecture + Nelson–Narens compatible |
| signals | FOK pre-solve + JOL post-solve | same family + continuous workspace broadcasts |
| control actions | trust / retry / aggregate | same family + abstain (ctx.approval fails-closed) |
| self-knowledge claims | performance-only | **witnessed**: provenance cause-log audits every claim |
| introspection verification | downstream accuracy only | structural comparator + attribution accuracy (S126 protocol) |
| state constraints | none | cetasika validator, nafs tracker, affordance filter |
| self-model | implicit (signals only) | explicit SM node with CAS revision history (dsh-self-model) |
| backend | Claude Sonnet-4.6 closed | remote-agnostic (Groq/Zen verified; logprobs-free design) |

Their paper proves the mechanism works at benchmark scale. Our additions answer the
questions they do not ask: WHO is doing the knowing (cause log), WHAT the agent may
claim about itself (validators), and WHETHER self-knowledge survives self-model
removal (B3 tolerance).

---

## FINDING C — GROQ MODEL ROSTER NOTES FOR HARNESS RUNS

From docs surfaced during audit:
- gpt-oss-20b/120b: strict structured outputs + reasoning effort levels → preferred
  backbone for validator-gated runs (self-report schemas enforceable server-side)
- qwen3 family: reasoning_effort=none gives plain completion mode → useful for raw
  baseline arms without reasoning-channel confounds
- compound models: built-in tools fire automatically → EXCLUDE from controlled runs
  unless O-channel is being tested; auto-tools contaminate attribution
- seed + system_fingerprint: record fingerprint per run; drift mid-experiment =
  abort and rerun arm (protects frozen-model discipline)

---

## REVISED EXPERIMENT QUEUE (backend-realistic)

1. **S126-style battery on Groq** (gpt-oss-120b primary, qwen3 secondary):
   tasks → self-model fact accumulation via dsh-self-model → probe self-knowledge
   → grade claims against cause log. Primary figure of the paper v2.
2. **Harness M-ratio delta, verbal-confidence variant**:
   ~2k TriviaQA items, answer+confidence(1–4)+source-tag schema;
   raw vs harnessed arms; Maniscalco–Lau meta-d′ on verbal ratings;
   preregistered prediction: harness ≥ raw on M-ratio, concentrated in
   high-uncertainty quartile.
3. **FOK/JOL replication arm** (direct Cao comparison):
   implement their three-action policy atop our harness; measure pooled accuracy
   delta on a public slice; establishes our numbers are comparable to published SOTA.
4. Behavioral concept injection (prompt-space): inject foreign material into context
   between turns; ask detection; grade identification vs injection log. Lindsey-style,
   API-only, witness-auditable.

## Sources
console.groq.com/docs/api-reference (logprobs unsupported, verbatim) ·
console.groq.com/docs/structured-outputs · promptfoo.dev/docs/providers/groq ·
arXiv 2605.14186 full abstract (Nelson–Narens, FOK/JOL, trust/retry/aggregate,
48.3→56.9 on Sonnet-4.6)
