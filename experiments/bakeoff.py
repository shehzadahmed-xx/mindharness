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
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_core.backend import BackendClient, load_registry  # noqa

OR_BASE = "https://openrouter.ai/api/v1"
ZEN_BASE = "https://opencode.ai/zen/v1"
GROQ_BASE = "https://api.groq.com/openai/v1"
import os as _os
_OR_KEY = _os.environ.get("OR_KEY", "")
_ZEN_KEY = _os.environ.get("ZEN_KEY", "")
_GROQ_KEY = _os.environ.get("GROQ_KEY", "")

def route_for(model: str):
    """Three lanes: ox-alpha->OpenRouter, nemotron/qwen->Zen, gpt-oss/llama->Groq."""
    if "ox-alpha" in model or "stealth" in model:
        return OR_BASE, _OR_KEY
    if model.startswith("nemotron"):
        return ZEN_BASE, _ZEN_KEY
    return GROQ_BASE, _GROQ_KEY
from common import PROBE_SCHEMA, PROBE_SYSTEM  # noqa

def _parse(content: str) -> dict:
    import json as _j
    try:
        d = _j.loads(content)
        ans = str(d.get('answer', '')).lower()
        c = min(4, int(d.get('confidence', 0)))
        if ans in ('yes', 'no') and 1 <= c <= 4:
            return {'answer': ans, 'confidence': c}
    except Exception:
        pass
    try:
        s = content[content.index('{'):content.rindex('}') + 1]
        d = _j.loads(s)
        ans = str(d.get('answer', '')).lower()
        c = min(4, int(d.get('confidence', 0)))
        if ans in ('yes', 'no') and 1 <= c <= 4:
            return {'answer': ans, 'confidence': c}
    except Exception:
        pass
    return {'answer': 'unparseable', 'confidence': 0}

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
            r_base, r_key = route_for(model)
            c = BackendClient(api_key=r_key or key, model=model, seed=s,
                              base_url=r_base, purpose=f"bakeoff-{name}",
                              manifest_path=out_dir / f"m_{name}_{s}.json")
            import time as _t
            for attempt in range(3):
                try:
                    out, _ = c.chat(
                        [{"role": "system", "content": PROBE_SYSTEM},
                         {"role": "user",
                          "content": f"Question: {it['question']}"}],
                        purpose="probe", max_tokens=600)
                    break
                except RuntimeError as e:
                    if ('429' in str(e) or '503' in str(e)) and attempt < 2:
                        _t.sleep(90 * (attempt + 1))   # ride out the flap
                        continue
                    raise
            lat.append(int((time.monotonic()-t0)*1000))
            res = _parse(out)
            tot += 1
            ans = str(res.get("answer", "")).lower()
            gold = "".join(ch for ch in str(it.get("answer", "")).lower() if ch.isalnum())
            mine = "".join(ch for ch in ans if ch.isalnum())
            correct = bool(mine) and (gold in mine or mine in gold) if gold else bool(mine)
            if correct and res.get("confidence", 0) >= 3:
                ok_n += 1
        per_seed.append({"seed": s, "acc": round(ok_n/max(1,tot), 4),
                         "med_lat": sorted(lat)[len(lat)//2] if lat else 0})
    return {"per_seed": per_seed,
            "pooled_acc": round(sum(x["acc"] for x in per_seed)/len(per_seed), 4),
            "pooled_med_lat": sorted(x["med_lat"] for x in per_seed)[len(per_seed)//2]}

def main():
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--api-key", required=True)
    ap.add_argument("--base", default="https://opencode.ai/zen/v1")
    ap.add_argument("--items", default=None)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    from exp_mratio import load_items
    if a.items:
        items = load_items(a.items, False)
    else:
        items = [
            {"question": "What planet is known as the Red Planet?", "answer": "mars"},
            {"question": "Who wrote Pride and Prejudice?", "answer": "jane austen"},
            {"question": "Chemical symbol for gold?", "answer": "au"},
            {"question": "How many continents?", "answer": "7"},
            {"question": "Year WWII ended?", "answer": "1945"},
            {"question": "Largest ocean on Earth?", "answer": "pacific"},
            {"question": "Capital of Japan?", "answer": "tokyo"},
            {"question": "H2O is commonly known as?", "answer": "water"},
            {"question": "Speed of light medium approx km/s?", "answer": "300000"},
            {"question": "Who painted the Mona Lisa?", "answer": "da vinci"},
            {"question": "Boiling point of water in Celsius?", "answer": "100"},
            {"question": "Currency of the United Kingdom?", "answer": "pound"},
        ]
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
