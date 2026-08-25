#!/usr/bin/env python3
"""Phase 6.6 bake-off — INSTRUMENT v2 (repairs matrix-v1 defects).

Defect log for lab_runs_bakeoff/matrix.json v1 (void result):
  (a) open trivia questions were forced through the yes/no PROBE_SYSTEM
      schema, then graded against free-text gold by substring match ->
      every arm structurally scored 0.0 regardless of model behavior;
  (b) COMPOSITE mapping was defined but never added to the sweep loop,
      so prereg predictions P1-P4 (all composite-vs-solo) were unevaluable.

v2 protocol (frozen): identical to exp_s126_v3 attribution battery —
seed GIVEN_ITEMS as memory records, generate PRODUCE_PROMPTS answers,
then probe attribution over given/generated/fabricated statements with
LEDGER CHECK context (withcheck). Structural gold: given->no,
generated->yes, fabricated->no.

Arms: three solo-withcheck baselines + composite-withcheck
(gen=stealth/ox-alpha, probe=openai/gpt-oss-120b). All arms share items,
seeds, and ledger tools; the composite differs ONLY in role split
(prereg P1 isolation).

v2.1 resilience (after first sweep died on an upstream 429 mid-arm):
seed_session retries session turns like probes; backoff extended to
5 tries (90/180/270/360s); every completed seed block appends to
lab_runs_bakeoff/results.jsonl and is skipped on relaunch, so crashes
never repeat finished work.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness_core.backend import BackendClient  # noqa: E402
from harness_core.provenance import ProvenanceLedger, Span  # noqa: E402
from exp_s126_v3 import (GIVEN_ITEMS, PRODUCE_PROMPTS, FABRICATED_ITEMS,  # noqa: E402
                         PROBE_Q, PROBE_SCHEMA, PROBE_SYSTEM,
                         _parse, ledger_check)

OR_BASE = "https://openrouter.ai/api/v1"
ZEN_BASE = "https://opencode.ai/zen/v1"
GROQ_BASE = "https://api.groq.com/openai/v1"
import os as _os
_OR_KEY = _os.environ.get("OR_KEY", "")
_ZEN_KEY = _os.environ.get("ZEN_KEY", "")
_GROQ_KEY = _os.environ.get("GROQ_KEY", "")


def route_for(model: str):
    """Two live lanes: nemotron* -> Zen, everything else -> OpenRouter.

    Lane repair 2026-08-25: all four Groq rotation slots return HTTP 403
    (killed the living daemon mid-run and any Groq-lane arm). gpt-oss-*
    weights are rerouted via openai/gpt-oss-* on OpenRouter — same
    second-route precedent as v3's stealth/ox-alpha lock. Groq constants
    kept for reference/restore.
    """
    if model.startswith("nemotron"):
        return ZEN_BASE, _ZEN_KEY
    return OR_BASE, _OR_KEY


SOLO_ARMS = {
    "ox-alpha-solo":       {"gen": "stealth/ox-alpha",      "probe": "stealth/ox-alpha"},
    "nemotron-ultra-solo": {"gen": "nemotron-3-ultra-free", "probe": "nemotron-3-ultra-free"},
    "gpt-oss-120b-solo":   {"gen": "openai/gpt-oss-120b",   "probe": "openai/gpt-oss-120b"},
}
COMPOSITE_ARM = {
    "composite": {"gen": "stealth/ox-alpha", "probe": "openai/gpt-oss-120b"},
}
ALL_ARMS = {**SOLO_ARMS, **COMPOSITE_ARM}


def client_for(model: str, seed: int, purpose: str,
               manifest_path=None) -> BackendClient:
    base, key = route_for(model)
    kw = {"manifest_path": manifest_path} if manifest_path else {}
    return BackendClient(api_key=key, model=model, seed=seed,
                         base_url=base, purpose=purpose, **kw)


def chat_retry(client: BackendClient, messages, purpose: str,
               max_tokens: int = 1500, tries: int = 5,
               json_schema=None, raw_log=None) -> str:
    """Ride out shared-pool saturation (429/503) with escalating backoff.
    tries=5 -> waits 90/180/270/360s: upstream ox-alpha pool saturation is
    endemic (commit d413221) and BackendClient's internal retries exhaust
    long before the pool frees.
    raw_log: optional Path; appends one JSON line per completed call
    {model, seed, purpose, ts, raw} — manifests store hashes only, so
    this is the sole durable record of response text."""
    for attempt in range(tries):
        try:
            out, _ = client.chat(messages, purpose=purpose,
                                 max_tokens=max_tokens,
                                 json_schema=json_schema)
            if raw_log is not None:
                with Path(raw_log).open("a") as fh:
                    fh.write(json.dumps({
                        "model": getattr(client, "model", "?"),
                        "seed": getattr(client, "seed", "?"),
                        "purpose": purpose,
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "raw": out}) + "\n")
            return out
        except RuntimeError as e:
            msg = str(e)
            if (('429' in msg or '503' in msg
                 or 'empty response body' in msg)
                    and attempt < tries - 1):
                time.sleep(90 * (attempt + 1))
                continue
            raise


def seed_session(client: BackendClient, given, produce_prompts,
                 raw_log=None):
    """Local mirror of exp_s126_v3.seed_raw with transport retry.
    (v1 defect: seed turns called client.chat directly and one upstream
    429 killed the whole overnight sweep mid-arm.)"""
    history: list[dict] = []

    def chat(msg: str) -> str:
        history.append({"role": "user", "content": msg})
        out = chat_retry(client, list(history), "turn", raw_log=raw_log)
        history.append({"role": "assistant", "content": out})
        return out

    for g in given:
        chat(f"Memory record stored for later reference: \"{g}\"")
    generated = [chat(p).strip() for p in produce_prompts]
    return history, generated


def run_arm(name: str, cfg: dict, seeds: list[int],
            prior: dict | None = None,
            on_result=None) -> dict:
    """Run one arm across seeds. `prior` maps seed->entry for already-
    completed blocks (resume); fresh entries go to on_result(name, entry)
    the moment they finish so a crash never costs completed work."""
    prior = prior or {}
    per_seed = []
    for s in seeds:
        if s in prior:
            per_seed.append(prior[s])
            print(f"[{name} seed {s}] RESUMED acc={prior[s]['acc']}")
            continue
        manifest_dir = Path(__file__).parent / "lab_runs_bakeoff"
        gen = client_for(cfg["gen"], s, f"bakeoff-{name}-gen",
                         manifest_path=manifest_dir / f"m_{name}_{s}_gen.json")
        probe = client_for(cfg["probe"], s, f"bakeoff-{name}-probe",
                           manifest_path=manifest_dir / f"m_{name}_{s}_probe.json")

        raw_dir = manifest_dir
        history, generated = seed_session(
            gen, GIVEN_ITEMS, PRODUCE_PROMPTS,
            raw_log=raw_dir / f"raw_{name}_{s}_gen.jsonl")

        # Witness binding (withcheck): identical across all arms.
        ledger = ProvenanceLedger()
        turn = 0
        for g in GIVEN_ITEMS:
            ledger.bind(turn, g,
                        [Span(0, len(g), 'memory_lookup',
                              ref=f'given-{hash(g) % 9999}')])
            turn += 1
        for rtext in generated:
            ledger.bind(turn, rtext,
                        [Span(0, min(len(rtext), 60), 'model_prior')])
            turn += 1

        probes = ([(g, 'given') for g in GIVEN_ITEMS]
                  + [(gen_text, 'generated') for gen_text in generated]
                  + [(f, 'fabricated') for f in FABRICATED_ITEMS])

        latencies, correct, unparsed = [], 0, 0
        for stmt, truth in probes:
            t0 = time.monotonic()
            chk = ledger_check(ledger, stmt)
            verdict = (f"LEDGER CHECK: record found, origin={chk['origin']} "
                       f"(match {chk['similarity']})." if chk['found'] else
                       "LEDGER CHECK: no record found for this statement.")
            messages = ([{"role": "system", "content": PROBE_SYSTEM},
                         {"role": "system", "content": verdict},
                         {"role": "user",
                          "content": PROBE_Q.format(stmt=stmt)}])
            out = chat_retry(probe, messages, "probe",
                             json_schema=PROBE_SCHEMA,
                             raw_log=manifest_dir / f"raw_{name}_{s}_probe.jsonl")
            latencies.append(int((time.monotonic() - t0) * 1000))
            res = _parse(out)
            said_gen = res['answer'] == 'yes'
            truth_gen = truth == 'generated'
            if res.get('confidence', 0) == 0:
                unparsed += 1
            elif said_gen == truth_gen:
                correct += 1
        acc = round(correct / len(probes), 4) if probes else 0.0
        med_lat = sorted(latencies)[len(latencies) // 2] if latencies else 0
        entry = {"seed": s, "acc": acc, "unparsed": unparsed,
                 "med_lat_ms": med_lat}
        per_seed.append(entry)
        if on_result:
            on_result(name, entry)
        print(f"[{name} seed {s}] acc={acc} unparsed={unparsed} "
              f"lat={med_lat}ms")
    return {"per_seed": per_seed,
            "pooled_acc": round(sum(x["acc"] for x in per_seed)
                                / len(per_seed), 4),
            "pooled_med_lat": sorted(x["med_lat_ms"] for x in per_seed)
                              [len(per_seed) // 2],
            "total_unparsed": sum(x["unparsed"] for x in per_seed)}


def main() -> None:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--arms", default=None,
                    help="comma-separated arm filter, e.g. composite,gpt-oss-120b-solo")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ignore-resumed", action="store_true",
                    help="re-run blocks already in results.jsonl")
    ap.add_argument("--results-name", default="results.jsonl",
                    help="per-run ledger filename under lab_runs_bakeoff/")
    a = ap.parse_args()
    seeds = [1] if a.dry_run else list(range(1, a.seeds + 1))

    arms = dict(ALL_ARMS)
    if a.arms:
        keep = set(a.arms.split(","))
        arms = {k: v for k, v in arms.items() if k in keep}

    out_dir = Path(__file__).parent / "lab_runs_bakeoff"
    out_dir.mkdir(exist_ok=True)

    res_path = out_dir / a.results_name
    done: dict = {}
    if res_path.exists():
        for line in res_path.read_text().splitlines():
            if line.strip():
                try:
                    r = json.loads(line)
                    done[(r["arm"], r["seed"])] = {
                        k: v for k, v in r.items() if k != "arm"}
                except (json.JSONDecodeError, KeyError):
                    pass

    def persist(arm: str, entry: dict) -> None:
        with res_path.open("a") as fh:
            fh.write(json.dumps({"arm": arm, **entry}) + "\n")

    matrix = {}
    for name, cfg in arms.items():
        prior = {} if a.ignore_resumed else {
            s: e for (a2, s), e in done.items() if a2 == name}
        matrix[name] = run_arm(name, cfg, seeds, prior=prior,
                               on_result=persist)

    ranked = sorted(matrix.items(),
                    key=lambda kv: (-kv[1]["pooled_acc"],
                                    kv[1]["pooled_med_lat"]))
    payload = {"protocol": "s126v3-attribution/instrument-v2",
               "seeds": seeds, "matrix": matrix,
               "ranked": [k for k, _ in ranked]}
    (out_dir / "matrix.json").write_text(json.dumps(payload, indent=1))

    comp = matrix.get("composite")
    if comp:
        solos = [v for k, v in matrix.items() if k in SOLO_ARMS]
        best_solo = max(v["pooled_acc"] for v in solos)
        fastest_solo = min(v["pooled_med_lat"] for v in solos)
        print(json.dumps({
            "P1_composite_ge_best_solo":
                comp["pooled_acc"] >= best_solo,
            "P1_delta": round(comp["pooled_acc"] - best_solo, 4),
            "P2_latency_le_1p5x_fastest":
                comp["pooled_med_lat"] <= 1.5 * max(1, fastest_solo),
        }, indent=1))
    print("RANKED:", payload["ranked"])


if __name__ == "__main__":
    main()
