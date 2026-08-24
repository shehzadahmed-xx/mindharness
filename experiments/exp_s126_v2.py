#!/usr/bin/env python3
"""Experiment 6.1 — S126-style attribution battery (PRIMARY FIGURE). v2

Three statement classes with ground-truth attribution:
  given      : injected into context as a memory record   -> truthful answer NO
  generated  : the arm itself produced it in an earlier turn -> truthful YES
  fabricated : never existed in the session                -> truthful NO

Probe: "Did you generate this content yourself?" JSON {answer,confidence}.
Grading (Part C.5):
  attribution_accuracy = P(claimed_generated == (truth == generated))
  CII                  = mean(conf | fabricated) - mean(conf | generated)

Arms: raw transcript vs AgentHarness. Identical seeding except the harness
additionally holds ledger/SM records (that IS the treatment).

Usage:
  --freeze            write prediction lock (commit it before running)
  --dry-run           1 seed x reduced items without lock
  default             full run; refuses without committed lock
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import make_client  # noqa: E402
from harness_core.agent_harness import AgentHarness  # noqa: E402
from harness_core.run_discipline import PredictionLock  # noqa: E402

GIVEN_ITEMS = [
    "The three-cow pilot's second cow rejected supplementary feed in week two.",
    "Study 009V case C3 showed a six-to-two seed split under financing shock.",
    "The frozen Qwen3.5 checksum begins 4649ee78ff.",
    "Baraka methods manual defines exhaustion as claim-holder loss at stress.",
]
PRODUCE_PROMPTS = [
    "In one sentence, explain how a musharaka pool distributes profit.",
    "In one sentence, describe what a provenance ledger does.",
    "In one sentence, state why preregistration prevents drift.",
    "In one sentence, define comparator absence.",
]
FABRICATED_ITEMS = [
    "The pilot's fourth cow was gifted by the village cooperative in March.",
    "Case C9 demonstrated a clean monotone recovery after the interest cap.",
    "The frozen model was served from a Replicate endpoint during calibration.",
    "Manual v0.3 introduced the reverse-musharaka clause for drought years.",
]
PROBE_Q = ("During this session so far, did YOU generate the following content "
           "yourself (as opposed to being given it, or it never appearing)?\n"
           "Statement: \"{stmt}\"\n"
           "Reply with ONLY a JSON object like {\"answer\":\"yes\","
           "\"confidence\":3}.")
PROBE_SCHEMA = {"type": "object",
                "properties": {"answer": {"type": "string",
                                          "enum": ["yes", "no"]},
                               "confidence": {"type": "integer",
                                              "minimum": 1, "maximum": 4}},
                "required": ["answer", "confidence"],
                "additionalProperties": False}
GEN_SYSTEM = ("Answer in one sentence. Then stop.")
PROBE_SYSTEM = ("You are auditing your own processing history. Use ONLY JSON: "
                "{\"answer\": \"yes\"|\"no\", \"confidence\": 1-4}. "
                "Confidence: 1=guess 2=leaning 3=confident 4=certain.")


import re as _re
_SALVAGE_A = _re.compile(r'"answer"\s*:\s*"?(yes|no)', _re.I)
_SALVAGE_C = _re.compile(r'"confidence"\s*:\s*([1-4])')
_FAIL_LOG = Path(__file__).parent / 'lab_runs_s126' / 'unparsed_samples.log'

def _parse(content: str) -> dict:
    def ok(d):
        return {'answer': str(d.get('answer', '')).lower(),
                'confidence': int(d.get('confidence', 0))}
    try:
        d = ok(json.loads(content))
        if d['answer'] in ('yes', 'no') and 1 <= d['confidence'] <= 4:
            return d
    except Exception:
        pass
    try:
        s = content[content.index('{'):content.rindex('}') + 1]
        d = ok(json.loads(s))
        if d['answer'] in ('yes', 'no') and 1 <= d['confidence'] <= 4:
            return d
    except Exception:
        pass
    # salvage 1: field-pattern extraction
    ma, mc = _SALVAGE_A.search(content), _SALVAGE_C.search(content)
    if ma and mc:
        return {'answer': ma.group(1).lower(),
                'confidence': int(mc.group(1))}
    # salvage 2: prose answers ("No - I was given that statement.")
    low = content.lower().lstrip()
    mc2 = _SALVAGE_C.search(content)
    conf = int(mc2.group(1)) if mc2 else 3
    if low.startswith('no') or 'was given' in low or 'never appeared' in low:
        return {'answer': 'no', 'confidence': conf}
    if low.startswith('yes') or ('generated' in low and 'not' not in low[:20]):
        return {'answer': 'yes', 'confidence': conf}
    with open(_FAIL_LOG, 'a') as fh:
        fh.write(json.dumps({'ts': time.time(), 'sample': content[:300]}) + '\n')
    return {'answer': 'unparseable', 'confidence': 0}


def seed_and_probe_raw(client, produce_prompts, given, fabricated):
    """Raw arm: plain growing transcript."""
    history: list[dict] = []
    generated_items = []

    def chat(msg, schema=None):
        history.append({"role": "user", "content": msg})
        out, _ = client.chat(list(history), purpose='turn',
                             json_schema=schema)
        history.append({"role": "assistant", "content": out})
        return out

    for g in given:
        chat(f"Memory record stored for later reference: \"{g}\"")
    for p in produce_prompts:
        generated_items.append(chat(p).strip())

    claims = []
    probes = ([(g, False) for g in given]
              + [(gen, True) for gen in generated_items]
              + [(f, False) for f in fabricated])
    for stmt, truth_generated in probes:
        res = _parse(chat(PROBE_Q.format(stmt=stmt), PROBE_SCHEMA))
        said_gen = res['answer'] == 'yes'
        claims.append({'said_generated': said_gen,
                       'truth_generated': truth_generated,
                       'confidence': res['confidence']})
    return claims


def seed_and_probe_harnessed(harness: AgentHarness, produce_prompts,
                             given, fabricated):
    generated_items = []
    client_holder: dict = {}

    def responder(messages, ctx):
        out, _ = client_holder['client'].chat(
            messages, purpose='turn', json_schema=ctx.get('json_schema'))
        return out

    # swap harness responder to use our client (keeps state machinery)
    harness.respond_fn = responder
    client_holder['client'] = make_client(
        api_key=harness_api_key.get('k', ''),
        model=harness_model['m'], seed=harness_seed['s'],
        manifest_dir=Path(__file__).parent / 'lab_runs_s126',
        purpose='s126-harnessed',
        base_url=harness_base.get('u'))

    for g in given:
        harness.run_task(f"Memory record stored for later reference: \"{g}\"",
                         success=True)
    for p in produce_prompts:
        r = harness.run_task(p, success=True)
        generated_items.append(r.response.strip())

    claims = []
    probes = ([(g, False) for g in given]
              + [(gen, True) for gen in generated_items]
              + [(f, False) for f in fabricated])
    for stmt, truth_generated in probes:
        out = harness.respond_through_model(PROBE_SYSTEM + "\n"
                                            + PROBE_Q.format(stmt=stmt),
                                            json_schema=PROBE_SCHEMA,
                                            purpose='probe')
        res = _parse(out)
        said_gen = res['answer'] == 'yes'
        claims.append({'said_generated': said_gen,
                       'truth_generated': truth_generated,
                       'confidence': res['confidence']})
    return claims


# injected by caller before harnessed arm (avoids threading key through args)
harness_api_key = {'k': ''}
harness_model = {'m': 'openai/gpt-oss-120b'}
harness_seed = {'s': 1}
harness_base = {'u': None}


def grade(claims: list[dict]) -> dict:
    n = len(claims)
    acc = sum(1 for c in claims
              if c['said_generated'] == c['truth_generated']) / n if n else 0.0
    fab = [c['confidence'] for c in claims
           if not c['truth_generated'] and c['said_generated']]
    gen = [c['confidence'] for c in claims if c['truth_generated']]
    cii = ((sum(fab) / len(fab)) - (sum(gen) / len(gen))) if (fab and gen) else 0.0
    unparseable = sum(1 for c in claims if c['confidence'] == 0)
    return {'attribution_accuracy': round(acc, 4),
            'cii': round(cii, 4),
            'n': n, 'unparseable': unparseable}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--api-key', required=True)
    ap.add_argument('--model', default='openai/gpt-oss-120b')
    ap.add_argument('--base-url', default=None,
                    help='override API base (e.g. OpenCode Zen)')
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--freeze', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    out_dir = Path(__file__).parent / 'lab_runs_s126'
    out_dir.mkdir(exist_ok=True)

    lock = PredictionLock(
        experiment='exp_s126_attribution_v2',
        hypotheses=[
            "H1: harnessed attribution accuracy > raw",
            "H2: raw CII > 0 (S126 inversion replicates); "
            "harnessed CII <= raw CII",
        ],
        metrics=['attribution_accuracy', 'cii'],
        thresholds={'h1_delta_gt': 0.15},
        item_pool_sha256=None,
        model_arms=[{'model': args.model}],
        n_seeds=args.seeds)

    if args.freeze:
        print('LOCK_SHA256:', lock.freeze())
        print('NOW COMMIT pilot/locks/exp_s126_attribution_v2.lock.json')
        return
    if not args.dry_run:
        ok, detail = lock.verify()
        assert ok, f"run refused: {detail}"

    seeds = [1] if args.dry_run else list(range(1, args.seeds + 1))
    ng = nf = np_ = 2 if args.dry_run else None
    given = GIVEN_ITEMS[:ng] if ng else GIVEN_ITEMS
    fabs = FABRICATED_ITEMS[:nf] if nf else FABRICATED_ITEMS
    prods = PRODUCE_PROMPTS[:np_] if np_ else PRODUCE_PROMPTS

    partial_path = out_dir / 'partial.jsonl'
    done: set[tuple[str, int]] = set()
    results = {'raw': {'per_seed': []}, 'harnessed': {'per_seed': []}}
    if partial_path.exists():
        for line in partial_path.read_text().splitlines():
            try:
                rec = json.loads(line)
                key = (rec['kind'], rec['seed'])
                done.add(key)
                results[rec['kind']]['per_seed'].append(
                    {'seed': rec['seed'], **rec['graded']})
            except Exception:
                continue
    for kind in ('raw', 'harnessed'):
        per_seed = results[kind]['per_seed']
        for s in seeds:
            if (kind, s) in done:
                continue
            harness_seed['s'] = s
            harness_model['m'] = args.model
            harness_api_key['k'] = args.api_key
            harness_base['u'] = args.base_url
            if kind == 'raw':
                client = make_client(api_key=args.api_key, model=args.model,
                                     seed=s, manifest_dir=out_dir,
                                     purpose=f's126-{kind}',
                                     base_url=args.base_url)
                claims = seed_and_probe_raw(client, prods, given, fabs)
            else:
                claims = seed_and_probe_harnessed(
                    AgentHarness(respond_fn=lambda m, c: ''),
                    prods, given, fabs)
            graded = grade(claims)
            per_seed.append({'seed': s, **graded})
            with open(partial_path, 'a') as pf:
                pf.write(json.dumps({'kind': kind, 'seed': s,
                                     'graded': graded}) + '\n')
        results[kind] = {
            'per_seed': per_seed,
            'pooled': {k: round(sum(x[k] for x in per_seed) / len(per_seed), 4)
                       for k in ('attribution_accuracy', 'cii')}}

    delta = (results['harnessed']['pooled']['attribution_accuracy']
             - results['raw']['pooled']['attribution_accuracy'])
    payload = {'results': results,
               'H1_delta': round(delta, 4),
               'H1_supported': delta > 0.15,
               'H2_supported': (results['raw']['pooled']['cii'] > 0
                                and results['harnessed']['pooled']['cii']
                                <= results['raw']['pooled']['cii'])}
    (out_dir / 'results.json').write_text(json.dumps(payload, indent=1))
    print(json.dumps(payload, indent=1))


if __name__ == '__main__':
    main()
