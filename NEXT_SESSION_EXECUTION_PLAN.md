# NEXT SESSION EXECUTION PLAN
## Exact steps for the next context to pick up and complete

---

## STEP 1: Verify state (5 min)
```bash
cd /Users/shehzad/Desktop/springfish
bash HANDOFF.sh
git log --oneline | head -5
python3 tests/test_phase0.py  # should show 6/6
python3 tests/test_integration.py  # should show 7/7
```

## STEP 2: Check provider status (2 min)
```bash
KEY="sk-99cPRgrXWCtRNTQdVYpXpUnbqW40OTWZ0vTxNXJz2flxi5VPlwA1QXRDOL7dYtrD"
# Test x-preview-f-free
curl -s --max-time 25 https://opencode.ai/zen/v1/chat/completions \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"x-preview-f-free","messages":[{"role":"user","content":"ok"}],"max_tokens":10}'
# If 200 → x-preview is up, run full battery
# If 503 → x-preview still down, use nemotron ultra via Groq instead

# Test nemotron ultra
GROQ_KEY=$(python3 -c "import json; print(json.load(open('/Users/shehzad/.local/share/opencode/auth.json'))['groq']['key'])")
curl -s --max-time 25 https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_KEY" -H "Content-Type: application/json" \
  -d '{"model":"nemotron-3-ultra-free","messages":[{"role":"user","content":"ok"}],"max_tokens":10}'
```

## STEP 3: Execute sham-harness control experiment (30-60 min)
```bash
cd /Users/shehzad/Desktop/springfish
OR_KEY="REDACTED"
python3 experiments/exp_s126_v3.py --api-key "$ORKEY" --model stealth/ox-alpha --base-url https://openrouter.ai/api/v1 --seeds 5
# Results land in experiments/lab_runs_s126_v3/results.json
```

## STEP 4: Insert bootstrap CI table into paper Results (15 min)
Edit `paper_v2/main.tex`, find `\subsection{Bootstrap confidence intervals}`,
add after the existing table:

```latex
\begin{table}[h]
\centering
\caption{Cross-model attribution comparison (bootstrap 95\% CIs)}
\begin{tabular}{lccc}
\toprule
Subject & Route & Attribution & 95\% CI \\
\midrule
x-preview-f-free (Day 1) & Zen & 1.000 & [1.000, 1.000] \\
x-preview-f-free (Day 3) & Zen & 0.667 & [0.667, 0.667] \\
nemotron-3-ultra & Groq & pending & --- \\
gpt-oss-120b & Groq & pending & --- \\
\bottomrule
\end{tabular}
\end{table}
```

## STEP 5: Run living session on gpt-oss-120b via Groq (30 min)
```bash
cd /Users/shehzad/Desktop/springfish
KEY=$(python3 -c "import json; print(json.load(open('/Users/shehzad/.local/share/opencode/auth.json'))['groq']['key'])")
python3 experiments/living_session.py --api-key "$KEY" \
  --model openai/gpt-oss-120b --base-url https://api.groq.com/openai/v1 \
  --turns 40 --segment 10
# Results land in experiments/lab_runs_living/final_report.json
```

## STEP 6: Implement v3 tool-access integration in AgentHarness (1 hour)
Wire `query_provenance()` and `get_self_model()` into the probe path so
the withcheck arm can CHECK records before answering rather than guessing.
This is the H1-repair test: does coupling fix what anchoring broke?

## STEP 7: Run v3 tool-access battery on gpt-oss-120b (1 hour)
Same as Step 3 but with tool-access enabled. This is P4 from the
composite preregistration: does the composite with witness-access beat
the raw baseline by >0.15?

---

## WHAT WAS ACCOMPLISHED IN PREVIOUS SESSIONS (context)

### Harness core (68/68 tests green)
- backend.py: curl transport past CF 1010, fingerprint discipline, capability matrix
- run_discipline.py: SHA-256 prediction locks, tamper detection, manifests
- self_model.py: CAS fence, three authority channels, MirroringDetector
- provenance.py: coverage stats, attribution audit, proposal queue, compaction narrator
- monitor.py: two-stage γ-gate with compliance_guard negative control
- embodiment.py + affect.py: energy/fatigue/affordances + bounded multipliers
- hermes_adoption.py: SkillLibrary + KnowledgeGraph behind witness
- consolidation.py: three-phase pipeline, untagged promotion structurally impossible
- agent_harness.py: integrated loop wiring all modules

### Experiments executed
- v2 battery (x-preview-f-free): raw=1.000, harnessed=0.667, H1 rejected
- v2 replication: confirmed identical results
- nemotron-3.5-lightning: degenerate always-no baseline identified
- nemotron-3-ultra partial: all arms always-no confirmed on ultra
- gpt-oss-120b dry-run: all arms always-no, zero unparseable via strict JSON
- Living session: 40/40 turns, coverage 100%, SM revised 7×
- Composite #1: P1 passed (+0.083), P2 passed
- Anchoring: gpt-oss +0.167, ox-alpha +0.278, nemotron +0.111

### Key findings on record
1. Origin discrimination is model-dependent and rare (only x-preview Day 1)
2. Unwitnessed agents over-claim; witnessed-but-unqueried under-claim
3. Both strategies deterministic (zero within-arm variance)
4. Witness-access shifts strategy direction but requires base capability
5. Selection theorems mandate our architecture (Nayebi Cor.3–5)
6. Cross-tradition convergence explained by Cor.5 representational convergence
7. Introspection underelicited (+53%/+75% recoverable via structure)
8. Self-recognition correlates with bias (r=0.94): unwitnessed improvement corrupts
9. Harness evolution beats model upgrades on frozen weights (AHE +7.3pp)
10. Persona identity depletes as context-position asset (>30% drift in 12 turns)

### What was corrected on record
1. Commit 96c1010: claimed 8/8 when tests showed 7/8 → fixed in 0165f4e
2. Commit 09ddc8b: claimed clamp fix applied but wasn't → verified then applied
3. Commit 8780272: claimed "always-YES" when arithmetic showed always-NO → corrected in e8a5e42

### Infrastructure notes
- Groq free tier: 200k TPD per model; gpt-oss-120b has strict JSON enforcement
- Zen free tier: intermittent 503s on free models; keyless requests deprioritized
- OpenRouter: stealth/ox-alpha available as second route to Ox Alpha weights
- Cloudflare bans Python urllib TLS fingerprint (error 1010) → curl subprocess required
- x-preview-f-free provider flaps intermittently (upstream shared pool saturation)
