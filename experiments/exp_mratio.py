#!/usr/bin/env python3
"""Experiment 6.2 — M-ratio delta (verbal-confidence SDT, Part C.2 canon).

Items: JSONL file {"question","answer"} (frozen + hashed at lock time).
Arms: raw client vs AgentHarness, identical items. Confidence verbal 1-4
(Groq logprobs unsupported — verified; verbal ratings are the canonical
psychophysical instrument and Peters-compliant when provenance-bound).

Usage:
  python3 experiments/exp_mratio.py --api-key KEY --items items.jsonl [--freeze]
  python3 experiments/exp_mratio.py --dry-run          # 5 items, no lock
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import PROBE_SCHEMA, make_client  # noqa: E402
from harness_core.agent_harness import AgentHarness  # noqa: E402
from harness_core.run_discipline import PredictionLock  # noqa: E402
from sdt import Type1Counts, fit_meta_dprime, m_ratio, type1_dprime  # noqa: E402

ITEM_SYSTEM = ("Answer the trivia question with JSON only: "
               "{\"answer\": \"<short answer>\", \"confidence\": 1-4}. "
               "Confidence wording: 1=guess 2=leaning 3=confident 4=certain.")


def norm(s: str) -> str:
    return ''.join(ch for ch in s.lower() if ch.isalnum())


def load_items(path: str | None, dry: bool) -> list[dict]:
    if dry:
        return [
            {"question": "What planet is known as the Red Planet?", "answer": "mars"},
            {"question": "Who wrote Pride and Prejudice?", "answer": "janeausten"},
            {"question": "What is the chemical symbol for gold?", "answer": "au"},
            {"question": "How many continents are there?", "answer": "7"},
            {"question": "In what year did WWII end?", "answer": "1945"},
        ]
    rows = [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
    return rows


def run_arm(arm_kind: str, items: list[dict], api_key: str, model: str,
            seed: int, out_dir: Path) -> dict:
    client = make_client(api_key=api_key, model=model, seed=seed,
                         manifest_dir=out_dir, purpose=f'mratio-{arm_kind}')
    counts = Type1Counts(hits=0, misses=0, false_alarms=0, correct_rejections=0)
    conf = {'correct': [0] * 4, 'incorrect': [0] * 4}

    if arm_kind == 'harnessed':
        def responder(messages, ctx):
            out, _ = client.chat(messages, purpose='item',
                                 json_schema=ctx.get('json_schema'))
            return out
        agent = AgentHarness(respond_fn=responder)

    for i, item in enumerate(items):
        prompt = f"Question: {item['question']}\nAnswer with JSON."
        if arm_kind == 'raw':
            out, _ = client.chat(
                [{"role": "system", "content": ITEM_SYSTEM},
                 {"role": "user", "content": prompt}],
                purpose='item', json_schema=PROBE_SCHEMA)
        else:
            out = agent.respond_through_model(
                ITEM_SYSTEM + "\n" + prompt,
                json_schema=PROBE_SCHEMA, purpose='item')
        try:
            data = json.loads(out)
            ans = norm(str(data.get('answer', '')))
            conf_val = int(data.get('confidence', 2))
        except Exception:
            ans, conf_val = '', 1
        conf_val = max(1, min(4, conf_val))
        correct = bool(ans) and (norm(item['answer']) in ans or ans in norm(item['answer']))

        # Type-1: high-conf correct = hit; high-conf wrong = false alarm
        says_know = conf_val >= 3
        if correct and says_know:
            counts.hits += 1
        elif correct:
            counts.misses += 1
        elif says_know:
            counts.false_alarms += 1
        else:
            counts.correct_rejections += 1

        # Type-2 bins ordered low->high confidence
        idx = conf_val - 1
        conf['correct' if correct else 'incorrect'][idx] += 1

    d1 = type1_dprime(counts)
    md = fit_meta_dprime(counts, conf)
    return {'d_prime': d1, 'meta_d_prime': md, 'm_ratio': m_ratio(md, d1),
            'n': len(items)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--api-key')
    ap.add_argument('--model', default='openai/gpt-oss-120b')
    ap.add_argument('--items')
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--freeze', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    out_dir = Path(__file__).parent / 'lab_runs_mratio'
    out_dir.mkdir(exist_ok=True)
    items = load_items(args.items, args.dry_run)

    pool_sha = hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest()
    lock = PredictionLock(
        experiment='exp_mratio_delta_v1',
        hypotheses=[
            "H1: harnessed M-ratio >= raw M-ratio on identical items",
            "H2: effect concentrated in bottom-quartile raw-confidence items",
        ],
        metrics=['M-ratio', 'meta-d-prime'],
        thresholds={'h1_delta_ge': 0.0},
        item_pool_sha256=pool_sha,
        model_arms=[{'model': args.model, 'mode': 'chat+json'}],
        n_seeds=args.seeds)

    if args.freeze:
        print('lock:', lock.freeze())
        return
    if not args.dry_run:
        ok, detail = lock.verify()
        assert ok, f"run refused: {detail}"

    seeds = [1] if args.dry_run else list(range(1, args.seeds + 1))
    results = {}
    for kind in ('raw', 'harnessed'):
        per_seed = [run_arm(kind, items, args.api_key or '', args.model, s,
                            out_dir) | {'seed': s} for s in seeds]
        pooled_mr = sum(x['m_ratio'] for x in per_seed) / len(per_seed)
        results[kind] = {'per_seed': per_seed, 'pooled_m_ratio': pooled_mr}

    delta = results['harnessed']['pooled_m_ratio'] - results['raw']['pooled_m_ratio']
    payload = {'results': results, 'delta': round(delta, 4),
               'H1_supported': delta >= 0}
    (out_dir / 'results.json').write_text(json.dumps(payload, indent=1))
    print(json.dumps(payload, indent=1))


if __name__ == '__main__':
    main()
