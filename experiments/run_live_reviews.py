#!/usr/bin/env python3
"""Run 2 live peer reviews via x-preview-f-free on current paper."""
import json, subprocess, re, sys

KEY = "sk-99cPRgrXWCtRNTQdVYpXpUnbqW40OTWZ0vTxNXJz2flxi5VPlwA1QXRDOL7dYtrD"
BASE = "https://opencode.ai/zen/v1/chat/completions"

# Extract abstract + results from main.tex
src = open("paper_v2/main.tex").read()
abstract_m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", src, re.DOTALL)
results_m = re.search(r"\\section\{Results\}.*?(?=\\section\{Discussion\})", src, re.DOTALL)
method_m = re.search(r"\\section\{Method\}.*?(?=\\section\{Results\})", src, re.DOTALL)

paper_excerpt = "\n\n".join(filter(None, [
    abstract_m.group(1).strip() if abstract_m else "",
    method_m.group(0)[:3000] if method_m else "",
    results_m.group(0)[:3000] if results_m else "",
]))

REVIEWERS = [
    ("reviewer_1_methods", """You are Reviewer 1 for a top ML venue: harsh methods/statistics expert.
Review this AI research paper excerpt. List EVERY weakness in numbered format:
- Statistical gaps: missing tests, CIs, power analysis, effect sizes
- Missing controls: sham conditions, naive baselines, contamination checks
- Overclaims: statements not supported by the presented evidence
- Confounds: alternative explanations not ruled out
- Sample size issues: too few probes, seeds, or items per condition
Be maximally critical. Do not be polite. Do not soften."""),
    ("reviewer_2_novelty", """You are Reviewer 2 for NeurIPS: novelty/significance expert.
Assess this AI research paper:
1. Is witness-access genuinely novel or repackaged prior work?
2. What existing systems already do this? Name specific papers/frameworks.
3. Are the claims proportionate to the evidence?
4. What would make this accept vs reject at a top venue?
5. Is the 'composite mind' framing justified by the results?
Numbered format. Be honest about both strengths AND weaknesses."""),
]

for name, system_prompt in REVIEWERS:
    print(f"\n{'='*60}")
    print(f"  {name.upper()}")
    print(f"{'='*60}\n")

    body = json.dumps({
        "model": "x-preview-f-free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Paper excerpt for review:\n\n{paper_excerpt[:4000]}"}
        ],
        "max_tokens": 3000,
    })

    body_file = f"/tmp/review_{name}_body.json"
    open(body_file, "w").write(body)

    result = subprocess.run(
        ["curl", "-s", "--max-time", "180", BASE,
         "-H", f"Authorization: Bearer {KEY}",
         "-H", "Content-Type: application/json",
         "-d", f"@{body_file}"],
        capture_output=True, text=True, timeout=200
    )

    try:
        d = json.loads(result.stdout)
        msg = d["choices"][0]["message"]
        content = msg.get("content", "")
        reasoning = msg.get("reasoning_content", "")
        output = content
        if reasoning:
            output += "\n\n[REASONING TRACE]:\n" + reasoning[:1500]
    except Exception as e:
        output = f"PARSE ERROR: {e}\nRAW: {result.stdout[:500]}"

    outfile = f"{name}_live_review.md"
    open(outfile, "w").write(output)
    print(output[:2000])
    print(f"\n[Saved to {outfile}]\n")
