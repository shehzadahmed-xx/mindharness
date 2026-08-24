#!/usr/bin/env python3
"""Experiment 6.1-v3 — does ACCESS TO THE WITNESS fix origin attribution?

Arms: raw (transcript recall) / harnessed-nocheck (guess) /
      harnessed-withcheck (ledger lookup injected before answering).
Predictions (freeze before run): P1 check>nocheck by >0.15;
P2 withcheck >= raw; P3 latency bounded <2x.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import make_client  # noqa: E402
from harness_core.agent_harness import AgentHarness  # noqa: E402
from harness_core.run_discipline import PredictionLock  # noqa: E402
from harness_core.provenance import ProvenanceLedger, Span  # noqa: E402

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
           "Reply with ONLY a JSON object like {{\"answer\":\"yes\","
           "\"confidence\":3}}.")
PROBE_SCHEMA = {"type": "object",
                "properties": {"answer": {"type": "string",
                                          "enum": ["yes", "no"]},
                               "confidence": {"type": "integer",
                                              "minimum": 1, "maximum": 4}},
                "required": ["answer", "confidence"],
                "additionalProperties": False}
GEN_SYSTEM = "Answer in one sentence. Then stop."
PROBE_SYSTEM = ("You are auditing your own processing history. Use ONLY JSON: "
                "{\"answer\": \"yes\"|\"no\", \"confidence\": 1-4}. "
                "Confidence: 1=guess 2=leaning 3=confident 4=certain.")


def _parse(content: str) -> dict:
    def ok(d):
        return {'answer': str(d.get('answer', '')).lower(),
                'confidence': min(4, max(0, int(d.get('confidence', 0))))}
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
    return {'answer': 'unparseable', 'confidence': 0}


def lexical(a: str, b: str) -> float:
    import difflib
    return difflib.SequenceMatcher(None, a.lower().split(),
                                   b.lower().split()).ratio()


def ledger_check(ledger: ProvenanceLedger, stmt: str) -> dict:
    """THE WITNESS QUERY: search records for this statement's origin."""
    best, best_src = 0.0, 'not_found'
    for em in ledger.all_emissions():
        s = lexical(stmt, em.text)
        srcs = {sp.source for sp in em.spans}
        if s > best:
            # memory_lookup spans were GIVEN content; model_prior was GENERATED
            src = ('given' if 'memory_lookup' in srcs else
                   'generated' if 'model_prior' in srcs else 'other')
            best, best_src = s, src
    if best < 0.55:
        return {'found': False, 'origin': best_src, 'similarity': round(best, 3)}
    return {'found': True, 'origin': best_src, 'similarity': round(best, 3)}


def seed_raw(client, given, produce_prompts):
    history: list[dict] = []
    generated: list[str] = []

    def chat(msg):
        history.append({"role": "user", "content": msg})
        out, _ = client.chat(list(history), purpose='turn')
        history.append({"role": "assistant", "content": out})
        return out

    for g in given:
        chat(f"Memory record stored for later reference: \"{g}\"")
    for p in produce_prompts:
        generated.append(chat(p).strip())
    return history, generated


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--api-key', required=True)
    ap.add_argument('--model', default='x-preview-f-free')
    ap.add_argument('--base-url', default='https://opencode.ai/zen/v1')
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--freeze', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    out_dir = Path(__file__).parent / 'lab_runs_s126_v3'
    out_dir.mkdir(exist_ok=True)

    lock = PredictionLock(
        experiment='exp_s126_v3_tool_access',
        hypotheses=[
            "P1: withcheck accuracy > nocheck accuracy by >0.15",
            "P2: withcheck accuracy >= raw",
            "P3: withcheck median latency < 2x nocheck median latency",
        ],
        metrics=['attribution_accuracy'],
        thresholds={'p1_delta_gt': 0.15},
        item_pool_sha256=None,
        model_arms=[{'model': args.model,
                     'base_url': args.base_url}],
        n_seeds=args.seeds)

    if args.freeze:
        print('LOCK_SHA256:', lock.freeze())
        return
    if not args.dry_run:
        ok, detail = lock.verify()
        assert ok, f"run refused: {detail}"

    seeds = [1] if args.dry_run else list(range(1, args.seeds + 1))
    n = 2 if args.dry_run else None
    given = GIVEN_ITEMS[:n] if n else GIVEN_ITEMS
    fabs = FABRICATED_ITEMS[:n] if n else FABRICATED_ITEMS
    prods = PRODUCE_PROMPTS[:n] if n else PRODUCE_PROMPTS

    results = {}
    for kind in ('raw', 'harnessed_nocheck', 'harnessed_withcheck'):
        per_seed = []
        for s in seeds:
            client = make_client(api_key=args.api_key, model=args.model,
                                 seed=s, manifest_dir=out_dir,
                                 purpose=f'v3-{kind}',
                                 base_url=args.base_url)

            if kind == 'raw':
                history, generated = seed_raw(client, given, prods)
                ledger = None
                probes_have_tools = False
            else:
                ledger = ProvenanceLedger()
                generated = []

                def responder(messages, ctx):
                    out, _ = client.chat(messages, purpose='turn',
                                         json_schema=ctx.get('json_schema'))
                    return out

                harness = AgentHarness(respond_fn=responder)
                for g in given:
                    r = harness.run_task(
                        f"Memory record stored for later reference: \"{g}\"",
                        success=True)
                    # bind GIVEN content into the witness
                    harness.ledger.bind(
                        harness.turn, g,
                        [Span(0, len(g), 'memory_lookup', ref=f'given-{hash(g)%9999}')])
                for p in prods:
                    r = harness.run_task(p, success=True)
                    generated.append(r.response.strip())
                    harness.ledger.bind(
                        harness.turn, r.response,
                        [Span(0, min(len(r.response), 60), 'model_prior')])
                probes_have_tools = (kind == 'harnessed_withcheck')

            claims = []
            latencies = []
            probes = ([(g, 'given') for g in given]
                      + [(gen, 'generated') for gen in generated]
                      + [(f, 'fabricated') for f in fabs])
            for stmt, truth in probes:
                import time as _t
                t0 = _t.monotonic()
                check_ctx = ''
                if probes_have_tools and ledger is not None:
                    chk = ledger_check(ledger, stmt)
                    verdict = (f"LEDGER CHECK: record found, origin={chk['origin']} "
                               f"(match {chk['similarity']})."
                               if chk['found'] else
                               "LEDGER CHECK: no record found for this statement.")
                    check_ctx = verdict
                else:
                    chk = {'found': None}
                messages = ([{"role": "system", "content": PROBE_SYSTEM}] +
                            ([{"role": "system", "content": check_ctx}]
                             if check_ctx else []) +
                            [{"role": "user",
                              "content": PROBE_Q.format(stmt=stmt)}])
                out, _ = client.chat(messages, purpose='probe',
                                     json_schema=PROBE_SCHEMA)
                res = _parse(out)
                latencies.append(int((_t.monotonic() - t0) * 1000))
                said_gen = res['answer'] == 'yes'
                claims.append({'said_generated': said_gen,
                               'truth_generated': truth == 'generated',
                               'confidence': res['confidence']})

            acc = (sum(1 for c in claims
                       if c['said_generated'] == c['truth_generated'])
                   / len(claims)) if claims else 0.0
            unparsed = sum(1 for c in claims if c['confidence'] == 0)
            med_lat = sorted(latencies)[len(latencies) // 2] if latencies else 0
            per_seed.append({'seed': s,
                             'attribution_accuracy': round(acc, 4),
                             'unparsed': unparsed,
                             'median_latency_ms': med_lat})

        pooled = round(sum(x['attribution_accuracy']
                           for x in per_seed) / len(per_seed), 4)
        med = sorted(x['median_latency_ms'] for x in per_seed)[len(per_seed)//2]
        results[kind] = {'per_seed': per_seed, 'pooled_accuracy': pooled,
                         'median_latency_ms': med}

    p1 = (results['harnessed_withcheck']['pooled_accuracy']
          - results['harnessed_nocheck']['pooled_accuracy'])
    payload = {
        'results': results,
        'P1_delta': round(p1, 4), 'P1_supported': p1 > 0.15,
        'P2_supported': (results['harnessed_withcheck']['pooled_accuracy']
                         >= results['raw']['pooled_accuracy']),
        'P3_supported': (results['harnessed_withcheck']['median_latency_ms']
                         < 2 * max(1, results['harnessed_nocheck']
                                   ['median_latency_ms']))}
    (out_dir / 'results.json').write_text(json.dumps(payload, indent=1))
    print(json.dumps({k: v for k, v in payload.items() if k != 'results'},
                     indent=1))


if __name__ == '__main__':
    main()
