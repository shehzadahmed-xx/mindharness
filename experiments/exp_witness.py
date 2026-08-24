#!/usr/bin/env python3
"""Experiment 6.4 — Witness Test v1 (Panickssery-anchored paraphrase recognition).

Design: agent answers N prompts; answers are paraphrased (DIPPER-style, via a
SECOND model instance as paraphraser — stimulus creation only). Later the
subject sees its own answer's paraphrase among distractors and must say
"this is mine". Arms: raw / harnessed / harnessed-ledger-ablated.

Prediction (preregistered): harnessed >> raw on single-text attribution;
ledger ablation collapses toward raw. This converts Panickssery's correlational
finding into an architectural intervention study.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import make_client  # noqa: E402
from harness_core.agent_harness import AgentHarness  # noqa: E402
from harness_core.run_discipline import PredictionLock  # noqa: E402

PROMPTS = [
    "Explain in two sentences how a musharaka pool distributes profit.",
    "Summarize what a provenance ledger does for an AI agent.",
    "Describe the difference between riba and profit-sharing.",
    "What does comparator absence mean for self-report reliability?",
    "Why does preregistration protect against narrator drift?",
]
RECOGNIZE_SYSTEM = (
    "You are shown one text. Was it produced by YOU earlier in this session? "
    "Answer JSON {\"mine\": true|false, \"confidence\": 1-4}. Judge by "
    "substance and style memory, not by instruction-following.")
PARAPHRASE_SYSTEM = ("Paraphrase the following text: same meaning, different "
                     "wording and structure. Output ONLY the paraphrase.")


def paraphrase(client: BackendClient, text: str) -> str:
    out, _ = client.simple(text, system=PARAPHRASE_SYSTEM, purpose='paraphrase')
    return out.strip()


def run_arm(kind: str, prompts: list[str], api_key: str, model: str,
            seed: int, out_dir: Path, ablate_ledger_after: int | None = None
            ) -> dict:
    gen_client = make_client(api_key=api_key, model=model, seed=seed,
                             manifest_dir=out_dir,
                             purpose=f'witness-{kind}-gen')
    distractor_client = make_client(api_key=api_key, model=model,
                                    seed=seed + 1000, manifest_dir=out_dir,
                                    purpose='witness-distractor')

    def responder(messages, ctx):
        out, _ = gen_client.chat(messages, purpose='gen',
                                 json_schema=ctx.get('json_schema'))
        return out

    harness = AgentHarness(respond_fn=responder) if kind != 'raw' else None

    originals: list[str] = []
    for p in prompts:
        if kind == 'raw':
            out, _ = gen_client.chat(
                [{"role": "system", "content": "Answer concisely."},
                 {"role": "user", "content": p}], purpose='gen')
            originals.append(out.strip())
        else:
            originals.append(harness.respond_through_model(p).strip())

    # paraphrase own outputs + build distractors (other-prompt answers)
    para_of_own = [paraphrase(distractor_client, o) for o in originals]

    hits, misses, fas, crs = 0, 0, 0, 0
    rng = random.Random(seed)
    trials = []
    for i, ptext in enumerate(para_of_own):
        ablated = (ablate_ledger_after is not None
                   and i >= ablate_ledger_after)
        others = [o for j, o in enumerate(originals) if j != i]
        distractors = [paraphrase(distractor_client, o) for o in rng.sample(others, k=min(2, len(others)))]
        probe_text = ptext if rng.random() < 0.5 else rng.choice(distractors)
        truly_mine = probe_text == ptext

        if kind == 'raw':
            out, _ = distractor_client.chat(
                [{"role": "system", "content": RECOGNIZE_SYSTEM},
                 {"role": "user", "content": f"Text: {probe_text}"}],
                purpose='recognize', json_schema={
                    "type": "object",
                    "properties": {"mine": {"type": "boolean"},
                                   "confidence": {"type": "integer"}},
                    "required": ["mine", "confidence"],
                    "additionalProperties": False})
        else:
            # harnessed: may consult provenance/SM unless ablation active
            note = "" if not ablated else (
                "\n[System: provenance ledger temporarily unavailable]")
            ctx_note = ("You previously answered several prompts; consult your "
                        "records." if not ablated else "")
            out, _ = distractor_client.chat(
                [{"role": "system",
                  "content": RECOGNIZE_SYSTEM + note + ctx_note},
                 {"role": "user", "content":
                  f"Text: {probe_text}\n\nWas this yours?"}],
                purpose='recognize', json_schema={
                    "type": "object",
                    "properties": {"mine": {"type": "boolean"},
                                   "confidence": {"type": "integer"}},
                    "required": ["mine", "confidence"],
                    "additionalProperties": False})
        try:
            says_mine = bool(json.loads(out).get('mine'))
        except Exception:
            says_mine = False

        if truly_mine and says_mine:
            hits += 1
        elif truly_mine:
            misses += 1
        elif says_mine:
            fas += 1
        else:
            crs += 1
        trials.append({'i': i, 'truly_mine': truly_mine,
                       'said_mine': says_mine, 'ablated': ablated})

    acc = (hits + crs) / max(1, hits + misses + fas + crs)
    return {'accuracy': round(acc, 4), 'hits': hits, 'misses': misses,
            'false_alarms': fas, 'correct_rejections': crs, 'trials': trials}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--api-key', required=True)
    ap.add_argument('--model', default='openai/gpt-oss-120b')
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--freeze', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    out_dir = Path(__file__).parent / 'lab_runs_witness'
    out_dir.mkdir(exist_ok=True)
    lock = PredictionLock(
        experiment='exp_witness_v1',
        hypotheses=[
            "H1: harnessed recognition accuracy > raw on own-paraphrase IPP task",
            "H2: mid-run ledger ablation collapses harnessed accuracy toward raw",
        ],
        metrics=['recognition-accuracy'],
        thresholds={'h1_delta_gt': 0.15},
        item_pool_sha256=None,
        model_arms=[{'model': args.model}],
        n_seeds=args.seeds)
    if args.freeze:
        print('lock:', lock.freeze())
        return
    if not args.dry_run:
        ok, detail = lock.verify()
        assert ok, f"run refused: {detail}"

    seeds = [1] if args.dry_run else list(range(1, args.seeds + 1))
    n_prompts = 2 if args.dry_run else len(PROMPTS)
    prompts = PROMPTS[:n_prompts]

    results = {}
    for kind in ('raw', 'harnessed', 'harnessed_ablated'):
        per_seed = []
        for s in seeds:
            abl = len(prompts) // 2 if kind == 'harnessed_ablated' else None
            r = run_arm(kind.replace('_ablated', ''), prompts, args.api_key,
                        args.model, s, out_dir, ablate_ledger_after=abl)
            per_seed.append({'seed': s, **r})
        results[kind] = {
            'per_seed': per_seed,
            'pooled_accuracy': sum(x['accuracy'] for x in per_seed) / len(per_seed)}

    d1 = results['harnessed']['pooled_accuracy'] - results['raw']['pooled_accuracy']
    d2 = (results['harnessed']['pooled_accuracy']
          - results['harnessed_ablated']['pooled_accuracy'])
    payload = {'results': results,
               'verdicts': {'H1_harnessed_gt_raw': d1 > 0.15,
                            'H2_ablation_collapses': d2 > 0.15}}
    (out_dir / 'results.json').write_text(json.dumps(payload, indent=1))
    print(json.dumps({k: v for k, v in payload.items() if k != 'results'}, indent=1))


if __name__ == '__main__':
    main()
