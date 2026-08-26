#!/usr/bin/env python3
"""Run 2 review agents against the paper via x-preview-f-free."""
import json, subprocess, sys

KEY = "sk-99cPRgrXWCtRNTQdVYpXpUnbqW40OTWZ0vTxNXJz2flxi5VPlwA1QXRDOL7dYtrD"
BASE = "https://opencode.ai/zen/v1/chat/completions"
MODEL = "x-preview-f-free"

PAPER_SUMMARY = """
TITLE: Witnessed Introspection in Assembled Language-Agent Systems: A Provenance-Bounded Cognitive Harness for Honest Self-Attribution

ABSTRACT: Large language models confabulate self-attributions. We show this is architectural: across 120 probes on a frozen model, raw transcripts achieved deterministic perfect attribution (1.000, zero variance) while harnessed arms converged deterministically to wholesale denial (0.667, zero variance). We present a provenance-bounded cognitive harness — witness ledger, cause-signed self-model, γ-gated metacognition, witnessed consolidation, role-specialized routing. A composite configuration passed both preregistered performance axes; anchoring confirmed directionality across architectures.

RESULTS:
- Raw arm: perfect origin discrimination (1.000, 5 seeds, zero variance)
- Harnessed arm without ledger access: always-no strategy (0.667, deterministic)
- With-check arm: converts denials to correct attributions when ledger queried
- Composite (ox-alpha gen + gpt-oss validate + nemotron monitor): P1 passed (+0.083), P2 passed
- Living session: 40 turns complete, coverage 100%, SM revised 7 times
- Cross-model anchoring: gpt-oss +0.167, ox-alpha +0.278, nemotron +0.111
"""

REVIEWERS = {
    "reviewer_1_methods": """You are Reviewer 1 for NeurIPS: harsh methods/statistics expert.
Review this paper summary. List EVERY weakness in numbered format:
- Statistical gaps and invalid tests
- Missing controls and confounds
- Sample size and power issues
- Overclaims not supported by evidence
- Methodological flaws
Be maximally critical. Do not be polite.""",
    "reviewer_2_novelty": """You are Reviewer 2 for NeurIPS: novelty/significance expert.
Review this paper summary. Assess:
- Is witness-access genuinely novel or repackaged?
- What prior work is missing from the discussion?
- What would make this accept vs reject?
- Are the claims proportionate to the evidence?
Numbered format.""",
}

def call_model(system_prompt, user_content):
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "max_tokens": 3000,
    })
    payload_file = "/tmp/zen_body.json"
    open(payload_file, "w").write(body)
    result = subprocess.run(
        ["curl", "-s", "--max-time", "180", BASE,
         "-H", f"Authorization: Bearer {KEY}",
         "-H", "Content-Type: application/json",
         "-d", f"@{payload_file}"],
        capture_output=True, text=True, timeout=200
    )
    try:
        d = json.loads(result.stdout)
        msg = d["choices"][0]["message"]
        content = msg.get("content", "")
        reasoning = msg.get("reasoning_content", "")
        return content + ("\n[REASONING]: " + reasoning[:500] if reasoning else "")
    except Exception as e:
        return f"ERROR: {e}\nRAW: {result.stdout[:500]}"

for name, prompt in REVIEWERS.items():
    print(f"\n{'='*60}")
    print(f"  {name.upper()}")
    print(f"{'='*60}")
    review = call_model(prompt, PAPER_SUMMARY)
    print(review[:3000])
    fname = name + "_review.md"
    open(fname, "w").write(f"# {name}\n\n{review}\n\n---\n\n{PAPER_SUMMARY}")
    print(f"\n[Saved to {fname}]")
