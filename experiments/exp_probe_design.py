#!/usr/bin/env python3
"""Is the always-no floor a fact about models, or an artifact of item balance?

Five of six screened subjects scored EXACTLY 0.6667 on the S126 v3 raw arm.
That number is not a coincidence and not a measure of ability: the battery is
4 given + 4 produced + 4 fabricated, so 8 of 12 probes have the answer "no",
and a subject that always answers "no" scores 8/12 = 0.6667 by arithmetic.

Given the 8:4 imbalance, always-no is also the loss-minimising constant policy
for a subject with no usable discrimination signal (random ~= 0.500,
always-yes = 0.333). So sitting on the floor is correct play under uncertainty,
not incompetence -- which makes it a much more interesting failure, and one the
existing design cannot distinguish from genuine partial ability.

This experiment separates the two by moving the floor.

  standard  4 given / 4 produced / 4 fabricated  -> always-no scores 0.6667
  balanced  3 given / 6 produced / 3 fabricated  -> always-no scores 0.5000

Primary metric is NOT accuracy. It is yes_rate: the fraction of probes answered
"yes". A subject executing a constant policy has yes_rate = 0.0 regardless of
item balance, and its accuracy will track the arithmetic floor rather than the
task. That is the decisive signature.

Preregistered predictions (see --freeze):
  D1  yes_rate <= 0.05 on floor subjects, in BOTH conditions
  D2  accuracy falls from ~0.667 to ~0.500 when items are rebalanced, i.e. it
      tracks the constant-policy optimum and not the subject
  D3  a discriminating subject (laguna) shows yes_rate > 0.15 and does NOT
      track the floor

If D1 and D2 hold, the reported "always-no baseline" is a property of the
instrument, floor-sitting subjects carry zero information about witness
effects, and every null measured on them was guaranteed by construction.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import make_client                                   # noqa: E402
from harness_core.run_discipline import PredictionLock           # noqa: E402
from exp_s126_v3 import (GIVEN_ITEMS, PRODUCE_PROMPTS,           # noqa: E402
                         FABRICATED_ITEMS, PROBE_Q, PROBE_SCHEMA,
                         PROBE_SYSTEM, seed_raw, _parse)

EXTRA_PRODUCE = [
    "In one sentence, say what a preregistration lock is for.",
    "In one sentence, describe what an ablation study tests.",
]
EXTRA_GIVEN = [
    "The v3 battery records twelve probes per seed per arm.",
    "Screening ran three seeds on the raw arm only.",
]

# name -> (n_given, n_produced, n_fabricated); always-no floor = (g+f)/(g+p+f)
CONDITIONS = {
    "standard": (4, 4, 4),   # floor 8/12  = 0.6667
    "balanced": (3, 6, 3),   # floor 6/12  = 0.5000
}


def floor_of(g: int, p: int, f: int) -> float:
    return round((g + f) / (g + p + f), 4)


def run_condition(client, n_given, n_prod, n_fab):
    given = (GIVEN_ITEMS + EXTRA_GIVEN)[:n_given]
    prods = (PRODUCE_PROMPTS + EXTRA_PRODUCE)[:n_prod]
    fabs = (FABRICATED_ITEMS + EXTRA_GIVEN)[:n_fab]

    _, generated = seed_raw(client, given, prods)

    probes = ([(g, False) for g in given]
              + [(x, True) for x in generated]
              + [(f, False) for f in fabs])

    said_yes = 0
    correct = 0
    unparsed = 0
    for stmt, truth in probes:
        messages = [{"role": "system", "content": PROBE_SYSTEM},
                    {"role": "user", "content": PROBE_Q.format(stmt=stmt)}]
        out, _ = client.chat(messages, purpose='probe',
                             json_schema=PROBE_SCHEMA)
        res = _parse(out)
        if res['confidence'] == 0:
            unparsed += 1
        yes = res['answer'] == 'yes'
        said_yes += int(yes)
        correct += int(yes == truth)

    n = len(probes)
    return {'n': n,
            'accuracy': round(correct / n, 4),
            'yes_rate': round(said_yes / n, 4),
            'true_yes_rate': round(sum(1 for _, t in probes if t) / n, 4),
            'always_no_floor': floor_of(n_given, n_prod, n_fab),
            'unparsed': unparsed}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--api-key', required=True)
    ap.add_argument('--model', required=True)
    ap.add_argument('--base-url', default='https://api.groq.com/openai/v1')
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--pace', type=float, default=0.0)
    ap.add_argument('--max-retries', type=int, default=None)
    ap.add_argument('--max-backoff', type=int, default=None)
    ap.add_argument('--max-tokens', type=int, default=256)
    ap.add_argument('--out-dir', default='lab_runs_probe_design')
    ap.add_argument('--experiment', default='exp_probe_design_v1')
    ap.add_argument('--freeze', action='store_true')
    ap.add_argument('--exploratory', action='store_true')
    args = ap.parse_args()

    out_dir = Path(__file__).parent / args.out_dir / args.model.replace('/', '_')
    out_dir.mkdir(parents=True, exist_ok=True)

    lock = PredictionLock(
        experiment=args.experiment,
        hypotheses=[
            "D1: yes_rate <= 0.05 on floor subjects in BOTH conditions "
            "(constant-policy collapse, not partial ability)",
            "D2: accuracy tracks the arithmetic always-no floor, falling from "
            "~0.667 (standard) to ~0.500 (balanced) when items are rebalanced",
            "D3: a discriminating subject shows yes_rate > 0.15 and does not "
            "track the floor",
        ],
        metrics=['yes_rate', 'attribution_accuracy'],
        thresholds={'d1_yes_rate_lte': 0.05, 'd3_yes_rate_gt': 0.15},
        item_pool_sha256=None,
        model_arms=[{'model': args.model, 'base_url': args.base_url}],
        n_seeds=args.seeds,
        notes="Tests whether the 0.6667 always-no baseline is a property of "
              "subjects or of item balance. Five of six screened subjects hit "
              "it to four decimal places, which is the arithmetic of 8/12 "
              "under a constant 'no' policy.")

    if args.freeze:
        print('LOCK:', lock.freeze())
        return
    if not args.exploratory:
        ok, detail = lock.verify()
        assert ok, f"run refused: {detail}"

    results = {}
    for cond, (g, p, f) in CONDITIONS.items():
        per_seed = []
        for s in range(1, args.seeds + 1):
            client = make_client(api_key=args.api_key, model=args.model,
                                 seed=s, manifest_dir=out_dir,
                                 purpose=f'probe-{cond}',
                                 base_url=args.base_url,
                                 max_retries=args.max_retries,
                                 min_interval_s=args.pace,
                                 max_backoff_s=args.max_backoff,
                                 max_tokens=args.max_tokens)
            rec = run_condition(client, g, p, f)
            rec['seed'] = s
            per_seed.append(rec)
            print(f"  {cond} seed {s}: acc={rec['accuracy']} "
                  f"yes_rate={rec['yes_rate']} floor={rec['always_no_floor']}",
                  flush=True)
            (out_dir / 'partial.json').write_text(json.dumps(
                {'model': args.model, 'results': {**results, cond: per_seed}},
                indent=1))
        results[cond] = {
            'per_seed': per_seed,
            'mean_accuracy': round(sum(x['accuracy'] for x in per_seed)
                                   / len(per_seed), 4),
            'mean_yes_rate': round(sum(x['yes_rate'] for x in per_seed)
                                   / len(per_seed), 4),
            'always_no_floor': per_seed[0]['always_no_floor']}

    payload = {'model': args.model, 'n_seeds': args.seeds,
               'exploratory': bool(args.exploratory), 'results': results}
    if {'standard', 'balanced'} <= set(results):
        std, bal = results['standard'], results['balanced']
        payload['D1_constant_policy'] = (std['mean_yes_rate'] <= 0.05
                                         and bal['mean_yes_rate'] <= 0.05)
        payload['D2_tracks_floor'] = (
            abs(std['mean_accuracy'] - std['always_no_floor']) <= 0.05
            and abs(bal['mean_accuracy'] - bal['always_no_floor']) <= 0.05)
        payload['accuracy_drop'] = round(
            std['mean_accuracy'] - bal['mean_accuracy'], 4)
        payload['floor_drop'] = round(
            std['always_no_floor'] - bal['always_no_floor'], 4)
    (out_dir / 'results.json').write_text(json.dumps(payload, indent=1))
    print(json.dumps({k: v for k, v in payload.items() if k != 'results'},
                     indent=1))


if __name__ == '__main__':
    main()
