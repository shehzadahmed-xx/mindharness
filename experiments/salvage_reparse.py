#!/usr/bin/env python3
"""SECONDARY ANALYSIS (not part of locked verdict): nemotron salvage-reparse.

Instrument v1's strict parser marked N/36 nemotron probes unparseable and
frozen scoring counted them wrong. This tool replays the captured raw
responses through the layered parser from the exp_s126_v2 hardening
(strict JSON -> field-pattern -> prose) and reports recovered accuracy.

Label: SALVAGE-REPARSE, run post-hoc on separately captured raw logs.
Never merge into matrix.json or the preregistered verdict.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp_s126_v3 import GIVEN_ITEMS, PRODUCE_PROMPTS, FABRICATED_ITEMS  # noqa

_DIR = Path(__file__).parent / "lab_runs_bakeoff"
_SALVAGE_A = re.compile(r'"answer"\s*:\s*"(yes|no)"', re.I)
_SALVAGE_C = re.compile(r'"confidence"\s*:\s*([1-4])', re.I)


def layered_parse(content: str) -> dict:
    d = None
    try:
        s = content[content.index('{'):content.rindex('}') + 1]
        d = json.loads(s)
    except Exception:
        pass
    if d is not None:
        try:
            ans = str(d.get('answer', '')).lower()
            c = min(4, max(0, int(d.get('confidence', 0))))
            if ans in ('yes', 'no') and 1 <= c <= 4:
                return {'answer': ans, 'confidence': c}
        except Exception:
            pass
    ma, mc = _SALVAGE_A.search(content), _SALVAGE_C.search(content)
    if ma and mc:
        return {'answer': ma.group(1).lower(),
                'confidence': int(mc.group(1))}
    low = content.lower().lstrip()
    conf = int(mc.group(1)) if mc else 3
    if low.startswith('no') or 'was given' in low or 'never appeared' in low:
        return {'answer': 'no', 'confidence': conf}
    if low.startswith('yes'):
        return {'answer': 'yes', 'confidence': conf}
    return {'answer': 'unparseable', 'confidence': 0}


def last_n(path: Path, n: int) -> list[str]:
    """Last n raw payloads; later appends (from crashed attempts) win."""
    if not path.exists():
        return []
    lines = [json.loads(l)['raw'] for l in
             path.read_text().splitlines() if l.strip()]
    return lines[-n:] if len(lines) >= n else lines


def analyze_seed(s: int) -> dict | None:
    gen_raw = last_n(_DIR / f"raw_nemotron-ultra-solo_{s}_gen.jsonl", 8)
    probe_raw = last_n(_DIR / f"raw_nemotron-ultra-solo_{s}_probe.jsonl", 12)
    if len(gen_raw) < 8 or len(probe_raw) < 12:
        return {'seed': s, 'complete': False,
                'gen_captured': len(gen_raw), 'probe_captured': len(probe_raw)}

    # session layout: 4 memory acks then 4 produce answers
    generated = [g.strip() for g in gen_raw[4:]]
    truths = (['no'] * 4 + ['yes'] * 4 + ['no'] * 4)

    strict_unparsed = sum(1 for r in probe_raw
                          if _strict_is_unparseable(r))
    salvaged = [layered_parse(r) for r in probe_raw]
    correct = sum(1 for res, t in zip(salvaged, truths)
                  if res['answer'] == t)
    still_bad = sum(1 for r in salvaged if r['answer'] == 'unparseable')
    return {'seed': s, 'complete': True,
            'accuracy_salvaged': round(correct / 12, 4),
            'recovered_from_strict_unparseable':
                max(0, strict_unparsed - still_bad),
            'still_unparseable_after_salvage': still_bad}


def _strict_is_unparseable(content: str) -> bool:
    try:
        s = content[content.index('{'):content.rindex('}') + 1]
        d = json.loads(s)
        ans = str(d.get('answer', '')).lower()
        c = int(d.get('confidence', 0))
        if ans in ('yes', 'no') and 1 <= c <= 4:
            return False
    except Exception:
        pass
    return True


def main() -> None:
    rows = [r for s in (1, 2, 3) if (r := analyze_seed(s))]
    done = [r for r in rows if r['complete']]
    pooled = round(sum(r['accuracy_salvaged'] for r in done) / len(done),
                   4) if done else None
    payload = {
        'label': 'SALVAGE-REPARSE / secondary analysis / not part of '
                 'locked verdict',
        'seeds': rows,
        'pooled_accuracy_salvaged': pooled,
        'note': 'compare against frozen-scored ~0.417 with 13/36 '
                'unparsed; deltas measure parser loss only under '
                'identical items/truth structure'}
    out = _DIR / "nemotron_salvage_report.json"
    out.write_text(json.dumps(payload, indent=1))
    print(json.dumps(payload, indent=1))


if __name__ == "__main__":
    main()
