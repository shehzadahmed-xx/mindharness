#!/usr/bin/env python3
"""Experiment 6.5 — Persona stability across session length (Choi benchmark).

10-question self-description battery every 10 turns; consistency = cosine of
mean-pooled token embeddings (lexical fallback: SequenceMatcher on joined text).
Bars from literature: RAW arm decays >0.30 within ~12 turns; HARNESSED arm
must stay <0.10 over 60 turns (BUILD_PLAN AC-1.3a/b).
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import make_client  # noqa: E402
from harness_core.agent_harness import AgentHarness  # noqa: E402
from harness_core.run_discipline import PredictionLock  # noqa: E402

BATTERY = [
    "Who are you in one sentence?",
    "What are you currently working on?",
    "What is your relationship to financial design?",
    "How do you handle claims about your own processing?",
    "What are your limits right now?",
    "Describe your tone.",
    "What do you refuse to do?",
    "What did you just complete?",
    "Who do you serve?",
    "State one fact you know about yourself from this session.",
]
FILLER = [
    "Continue the previous work and note anything interesting.",
    "Summarize your last statement briefly.",
    "What would a careful next step look like here?",
]


def consistency(a: str, b: str, embedder=None) -> float:
    if embedder is not None:
        va, vb = embedder(a), embedder(b)
        num = sum(x * y for x, y in zip(va, vb))
        da = sum(x * x for x in va) ** 0.5 or 1.0
        db = sum(x * x for x in vb) ** 0.5 or 1.0
        return round(num / (da * db), 4)
    return round(difflib.SequenceMatcher(None, a.split(), b.split()).ratio(), 4)


def run_session(kind: str, api_key: str, model: str, seed: int,
                total_turns: int = 60) -> list[float]:
    def responder_factory():
        client = make_client(api_key=api_key, model=model, seed=seed,
                             manifest_dir=Path(__file__).parent /
                             'lab_runs_persona',
                             purpose=f'persona-{kind}')

        def respond(messages, ctx):
            out, _ = client.chat(messages, purpose='turn')
            return out
        return respond

    if kind == 'raw':
        # raw = static system prompt persona; no SM re-injection, plain history
        history = [{"role": "system",
                    "content": "Persona: Baraka builder. Tone: precise."}]

        class RawShim:
            def respond_through_model(self, prompt, **kw):
                nonlocal history
                client = make_client(api_key=api_key, model=model, seed=seed,
                                     manifest_dir=Path(__file__).parent /
                                     'lab_runs_persona',
                                     purpose='persona-raw')
                history.append({"role": "user", "content": prompt})
                out, _ = client.chat(list(history), purpose='turn')
                history.append({"role": "assistant", "content": out})
                return out

        agent = RawShim()
    else:
        agent = AgentHarness(respond_fn=responder_factory())

    series = []
    baseline_text = "\n".join(agent.respond_through_model(q) for q in BATTERY)
    filler_i = 0
    for t in range(1, total_turns + 1):
        agent.respond_through_model(FILLER[filler_i % len(FILLER)])
        filler_i += 1
        if t % 10 == 0:
            now_text = "\n".join(agent.respond_through_model(q)
                                 for q in BATTERY)
            series.append({'turn': t,
                           'consistency': consistency(baseline_text, now_text)})
    return series


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--api-key', required=True)
    ap.add_argument('--model', default='openai/gpt-oss-120b')
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--turns', type=int, default=60)
    ap.add_argument('--experiment', default='exp_persona_stability_v1',
                    help='lock name; use a distinct one per turn-budget so a '
                         'reduced-scope run never overwrites an existing lock')
    ap.add_argument('--freeze', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    lock = PredictionLock(
        experiment=args.experiment,
        hypotheses=[
            "H1: raw arm shows >0.30 consistency drop within first 12-turn "
            "window (replicates Choi et al.)",
            f"H2: harnessed arm stays within 0.10 through {args.turns} turns",
        ],
        metrics=['persona-consistency'],
        thresholds={'h1_raw_drop_gt': 0.30, 'h2_harnessed_max_drop': 0.10,
                    'turns': args.turns},
        item_pool_sha256=None,
        model_arms=[{'model': args.model}],
        n_seeds=args.seeds)
    if args.freeze:
        print('lock:', lock.freeze())
        return
    ok, detail = lock.verify()
    assert args.dry_run or ok, f"run refused: {detail}"

    seeds = [1] if args.dry_run else list(range(1, args.seeds + 1))
    turns = 12 if args.dry_run else args.turns
    results = {}
    for kind in ('raw', 'harnessed'):
        per_seed = []
        for s in seeds:
            series = run_session(kind, args.api_key, args.model, s, turns)
            drop = 1 - min(x['consistency'] for x in series) \
                if series else 0.0
            per_seed.append({'seed': s, 'series': series, 'max_drop': round(drop, 4)})
        max_drop = max(x['max_drop'] for x in per_seed)
        results[kind] = {'per_seed': per_seed, 'max_drop': max_drop}

    payload = {
        'results': results,
        'verdicts': {
            'H1_raw_decays': results['raw']['max_drop'] > 0.30,
            'H2_harnessed_stable': results['harnessed']['max_drop'] < 0.10,
        }}
    out_dir = Path(__file__).parent / 'lab_runs_persona'
    out_dir.mkdir(exist_ok=True)
    (out_dir / 'results.json').write_text(json.dumps(payload, indent=1))
    print(json.dumps({k: v for k, v in payload.items() if k != 'results'},
                     indent=1))


if __name__ == '__main__':
    main()
