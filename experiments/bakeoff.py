#!/usr/bin/env python3
"""Phase 6.6 bake-off: sweep per-role model configs across the v3 battery.

Configs: single-model baselines (each model does ALL roles) + composite
(registry-assigned per-role). Metrics: attribution accuracy, median latency,
total tokens. Output: ranked matrix results.json.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_core.backend import BackendClient, load_registry  # noqa
from common import _parse, PROBE_SCHEMA, PROBE_SYSTEM  # noqa

CONFIGS = {
    "ox-alpha-solo":     {"all": "stealth/ox-alpha"},
    "nemotron-ultra-solo": {"all": "nemotron-3-ultra-free"},
    "gpt-oss-120b-solo": {"all": "openai/gpt-oss-120b"},
}
COMPOSITE = {  # per-role assignment (the assembled mind)
    "seed":   "openai/gpt-oss-20b",
    "gen":    "stealth/ox-alpha",
    "probe":  "openai/gpt-oss-120b",
}

def run_config(name, mapping, items, key, base, out_dir, seeds):
    per_seed = []
    for s in seeds:
        lat, ok_n, tot = [], 0, 0
        for it in items:
            t0 = time.monotonic()
            model = mapping.get("all") or (
                COMPOSITE["gen"] if "explain" in it["question"].lower()
                else COMPOSITE["probe"])
            c = BackendClient(api_key=key, model=model, seed=s,
                              base_url=base, purpose=f"bakeoff-{name}",
                              manifest_path=out_dir / f"m_{name}_{s}.json")
            out, _ = c.chat(
                [{"role": "system", "content": PROBE_SYSTEM},
                 {"role": "user", "content": f"Question: {it['question']}"}],
                purpose="probe", max_tokens=600)
            lat.append(int((time.monotonic()-t0)*1000))
            res = _parse(out)
            tot += 1
            ans = str(res.get("answer", "")).lower()
            correct = bool(ans) and (norm := "".join(ch for ch in item_answer(it).lower() if ch.isalnum())) in "".join(ch for ch in ans.lower() if ch.isalnum())
            if res.get("confidence", 0) >= 3 and correct: ok_n += 1
            elif res.get("confidence", 0) >= 3: pass
        per_seed.append({"seed": s, "acc": round(ok_n/max(1,tot), 4),
                         "med_lat": sorted(lat)[len(lat)//2] if lat else 0})
    return {"per_seed": per_seed,
            "pooled_acc": round(sum(x["acc"] for x in per_seed)/len(per_seed), 4),
            "pooled_med_lat": sorted(x["med_lat"] for x in per_seed)[len(per_seed)//2]}

def item_answer(it): return it.get("answer", "")

def main():
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--api-key", required=True)
    ap.add_argument("--base", default="https://opencode.ai/zen/v1")
    ap.add_argument("--items", default=None)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    from exp_mratio import load_items
    items = load_items(a.items, a.dry_run)
    out_dir = Path(__file__).parent / "lab_runs_bakeoff"
    out_dir.mkdir(exist_ok=True)
    seeds = [1] if a.dry_run else list(range(1, a.seeds+1))
    matrix = {}
    for name, mapping in CONFIGS.items():
        matrix[name] = run_config(name, mapping, items, a.api_key, a.base, out_dir, seeds)
        print(name, "->", matrix[name]["pooled_acc"], "| lat", matrix[name]["pooled_med_lat"])
    ranked = sorted(matrix.items(), key=lambda kv: (-kv[1]["pooled_acc"], kv[1]["pooled_med_lat"]))
    (out_dir/"matrix.json").write_text(json.dumps(
        {"matrix": matrix, "ranked": [k for k,_ in ranked]}, indent=1))
    print("RANKED:", [k for k,_ in ranked])

if __name__ == "__main__":
    main()
