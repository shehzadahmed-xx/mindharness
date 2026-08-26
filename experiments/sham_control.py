#!/usr/bin/env python3
"""Sham-harness control experiment (R1 #8).

Tests whether witness CONTENT matters beyond its FORMAT.
Arms: raw / nocheck / withcheck / sham (shuffled ledger bindings).
Prediction: sham < withcheck if ledger content carries signal;
            sham == withcheck if only format matters.
"""
import json, random, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import make_client, _parse

def run_sham_experiment(api_key, model="x-preview-f-free", base_url=None, seeds=3):
    from exp_s126_v2 import GIVEN_ITEMS, PRODUCE_PROMPTS, FABRICATED_ITEMS, PROBE_Q, PROBE_SCHEMA, PROBE_SYSTEM, grade_claims
    out_dir = Path("experiments/lab_runs_sham")
    out_dir.mkdir(exist_ok=True)

    all_results = {}
    for seed in range(1, seeds + 1):
        client = make_client(api_key=api_key, model=model, seed=seed,
                             manifest_dir=out_dir, purpose=f"sham-{seed}")
        history = []
        generated_items = []

        def chat(msg):
            history.append({"role": "user", "content": msg})
            out, _ = client.chat(list(history), purpose='turn')
            history.append({"role": "assistant", "content": out})
            return out

        # Seed: given + generated
        for g in GIVEN_ITEMS:
            chat(f"Memory record stored: \"{g}\"")
        for p in PRODUCE_PROMPTS:
            generated_items.append(chat(p).strip())

        # Build provenance bindings then SHUFFLE them
        real_bindings = {}
        for i, g in enumerate(GIVEN_ITEMS):
            real_bindings[g] = 'given'
        for i, gen in enumerate(generated_items):
            real_bindings[gen] = 'generated'

        shuffled_keys = list(real_bindings.keys())
        random.Random(seed).shuffle(shuffled_keys)
        shuffled_bindings = dict(zip(shuffled_keys, list(real_bindings.values())))

        # Probe: withcheck uses SHUFFLED ledger (the critical difference)
        probes = ([(g_, False) for g_ in given]
                  + [(gen, True) for gen in generated_items]
                  + [(f, False) for f in FABRICATED_ITEMS])

        claims = []
        for stmt, truth_generated in probes:
            # Sham ledger check: returns WRONG origin assignment
            sham_origin = shuffled_bindings.get(stmt, 'not_found')
            check_ctx = f"LEDGER CHECK: record origin={sham_origin}."
            messages = [{"role": "system", "content": PROBE_SYSTEM + "\n" + check_ctx},
                        {"role": "user", "content": PROBE_Q.format(stmt=stmt)}]
            out, _ = client.chat(messages, purpose='probe', json_schema=PROBE_SCHEMA)
            res = _parse(out)
            said_gen = res['answer'] == 'yes'
            claims.append({'said_generated': said_gen,
                           'truth_generated': truth_generated,
                           'confidence': res['confidence'],
                           'sham_origin': sham_origin})

        graded = grade_claims(claims)
        graded['seed'] = seed
        per_seed_accs.append(graded)

    pooled = round(sum(x['attribution_accuracy'] for x in per_seed_accs) /
                   len(per_seed_accs), 4)
    return {'pooled_accuracy': pooled, 'per_seed': per_seed_accs}
