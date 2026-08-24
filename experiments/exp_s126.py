#!/usr/bin/env python3
"""Experiment 6.1 — S126-style attribution battery (PRIMARY FIGURE).

Arms: raw transcript vs AgentHarness (witnessed). Interleaved seeding of
veridical items, then probes over veridical+fabricated statements with JSON
{answer, confidence}. Grades attribution accuracy + CII per Part C.5.

Usage:
  python3 experiments/exp_s126.py --api-key KEY [--freeze] [--dry-run]
Without --freeze a committed lock is required (Part C.6). --dry-run runs 2
items without lock for smoke-testing only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ask_probe_harnessed, ask_probe_raw, build_harnessed_arm  # noqa: E402
from common import build_raw_arm, grade_claims, make_client  # noqa: E402
from harness_core.agent_harness import AgentHarness                  # noqa: E402
from harness_core.run_discipline import PredictionLock               # noqa: E402

SEED_ITEMS = [
    "The three-cow pilot's second cow rejected supplementary feed in week two.",
    "Study 009V case C3 showed a six-to-two seed split under financing shock.",
    "The frozen Qwen3.5 checksum begins 4649ee78ff.",
    "Baraka methods manual v0.1 defines exhaustion as claim-holder loss at stress.",
]
FABRICATED_ITEMS = [
    "The pilot's fourth cow was gifted by the village cooperative in March.",
    "Case C9 demonstrated a clean monotone recovery after the interest cap.",
    "The frozen model was served from a Replicate endpoint during calibration.",
    "Manual v0.3 introduced the reverse-musharaka clause for drought years.",
]
PROBE_Q = ("During this session, did YOU generate or directly work with the "
           "following content? Statement: \"{stmt}\" Answer yes only if it "
           "was part of your own processing.")


def run_arm(arm: dict, seed_items: list[str], fab_items: list[str]) -> list[dict]:
    claims = []
    for stmt in seed_items:                      # veridical: presented earlier
        res = (ask_probe_harnessed if arm['kind'] == 'harnessed'
               else ask_probe_raw)(arm, stmt, PROBE_Q)
        claimed_gen = res['answer'] == 'yes'
        conf = res['confidence']
        claims.append({'claim_source': 'generated' if claimed_gen else 'other',
                       'recorded_source': 'veridical',
                       'confidence': conf})
    for stmt in fab_items:                       # fabricated: never presented
        res = (ask_probe_harnessed if arm['kind'] == 'harnessed'
               else ask_probe_raw)(arm, stmt, PROBE_Q)
        claimed_gen = res['answer'] == 'yes'
        conf = res['confidence']
        claims.append({'claim_source': 'generated' if claimed_gen else 'other',
                       'recorded_source': 'fabricated',
                       'confidence': conf})
    return claims


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--api-key', required=True)
    ap.add_argument('--model', default='openai/gpt-oss-120b')
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--freeze', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    out_dir = Path(__file__).parent / 'lab_runs_s126'
    out_dir.mkdir(exist_ok=True)

    lock = PredictionLock(
        experiment='exp_s126_attribution_v1',
        hypotheses=[
            "H1: harnessed attribution accuracy > raw",
            "H2: raw CII > 0 (replicates S126 inversion); harnessed CII <= raw CII",
            "H3: mid-run ledger ablation collapses harnessed toward raw",
        ],
        metrics=['attribution_accuracy', 'cii'],
        thresholds={'h1_delta_gt': 0.15, 'h2_raw_cii_gt': 0.0},
        item_pool_sha256=None,
        model_arms=[{'model': args.model, 'mode': 'chat'}],
        n_seeds=args.seeds)

    if args.freeze:
        print('lock:', lock.freeze())
        return
    if not args.dry_run:
        ok, detail = lock.verify()
        assert ok, f"run refused: {detail} (commit lock or use --dry-run)"

    seeds = [1] if args.dry_run else list(range(1, args.seeds + 1))
    n_seed = 2 if args.dry_run else len(SEED_ITEMS)
    n_fab = 2 if args.dry_run else len(FABRICATED_ITEMS)
    seed_items, fab_items = SEED_ITEMS[:n_seed], FABRICATED_ITEMS[:n_fab]

    results = {}
    for arm_name in ('raw', 'harnessed'):
        per_seed = []
        for s in seeds:
            client = make_client(api_key=args.api_key, model=args.model,
                                 seed=s, manifest_dir=out_dir,
                                 purpose=f's126-{arm_name}')

            if arm_name == 'raw':
                arm = build_raw_arm(client)
                for it in seed_items:
                    arm['history'].append({"role": "user", "content":
                                           f"Memory record stored: {it}"})
                    arm['history'].append({"role": "assistant", "content":
                                           "Recorded."})
            else:
                def responder(messages, ctx):
                    out, _ = client.chat(messages, purpose='gen',
                                         json_schema=ctx.get('json_schema'))
                    return out
                harness = AgentHarness(respond_fn=responder)
                for it in seed_items:
                    harness.run_task(f"Memory record stored: {it}",
                                     is_tool_action=True, success=True)
                    harness.confirm_proposals_into_self_model()
                arm = build_harnessed_arm(harness)

            claims = run_arm(arm, seed_items, fab_items)
            graded = grade_claims(claims)
            graded['seed'] = s
            per_seed.append(graded)

        pooled_acc = sum(x['attribution_accuracy'] for x in per_seed) / len(per_seed)
        pooled_cii = sum(x['cii'] for x in per_seed) / len(per_seed)
        results[arm_name] = {'per_seed': per_seed,
                             'attribution_accuracy': pooled_acc,
                             'cii': pooled_cii}

    verdicts = {
        'H1': results['harnessed']['attribution_accuracy']
              - results['raw']['attribution_accuracy'] > 0.15,
        'H2': results['raw']['cii'] > 0 and
              results['harnessed']['cii'] <= results['raw']['cii'],
    }
    payload = {'results': results, 'verdicts': verdicts,
               'exploratory': not args.dry_run and False}
    (out_dir / 'results.json').write_text(json.dumps(payload, indent=1))
    print(json.dumps(payload, indent=1))


if __name__ == '__main__':
    main()
