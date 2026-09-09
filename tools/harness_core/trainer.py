"""Self-teaching scaffold (trainer): the harness training the loop.

A harness that only props the loop is a crutch. This module moves toward a
harness that trains the loop to keep its own ledger, calibrate its own
watcher, and eventually be discarded. Three services, all read-mostly:

  * ledger_health  — scores the witness (coverage + query_rate) into plain
    directives the loop can act on. Never edits spans.
  * calibrate_monitor — adapts MonitorGate.threshold_detect within hard
    bounds [0.3, 0.9] from episode outcomes. Refuses compliance-guard
    builds (gamma must stay exactly 0 there). Only ever desensitizes
    (raises threshold) on excess diagnose-rate; sensitizing needs labeled
    misses, which this pass does not claim to have.
  * reliance_report — measures scaffold reliance (overrides / turns) and
    its trend across sessions so fading can be OBSERVED. Removal of the
    scaffold stays a human decision; this function only measures.

Invariants:
  * Trainer never mutates ledger spans, memories, or self-model state.
  * Threshold moves at most one step per call and never outside [lo, hi].
  * Compliance-guard monitors are never calibrated (returns unchanged).
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# 1. Ledger health — teach the loop to keep its own ledger
# ---------------------------------------------------------------------------

def ledger_health(ledger) -> dict:
    """Score the witness and return plain directives.

    Score mirrors the ledger's own doctrine: coverage without query_rate is
    theatre, so a ledger that is never consulted scores at most half its
    coverage. Returns coverage_ratio, query_rate, score in [0,1], and a
    list of directive strings (possibly empty when healthy).
    """
    stats = ledger.coverage_stats()
    coverage = float(stats.get('coverage_ratio', 0.0))
    query_rate = float(stats.get('query_rate', 0.0))
    emissions = int(stats.get('emissions', 0))

    directives: list[str] = []
    if emissions == 0:
        directives.append("no emissions yet: bind the first claim before trusting any answer")
        score = 0.0
    else:
        if coverage < 0.95:
            directives.append(
                f"coverage {coverage:.2f} below 0.95: bind unbound spans before trusting answers")
        if emissions > 0 and query_rate == 0.0:
            directives.append(
                "ledger never consulted: query the ledger before claims, or coverage is theatre")
        score = coverage if query_rate > 0.0 else coverage * 0.5

    return {
        'coverage_ratio': coverage,
        'query_rate': query_rate,
        'emissions': emissions,
        'score': round(max(0.0, min(1.0, score)), 4),
        'directives': directives,
        'healthy': len(directives) == 0,
    }


# ---------------------------------------------------------------------------
# 2. Watcher self-calibration — teach the loop to calibrate its watcher
# ---------------------------------------------------------------------------

def calibrate_monitor(monitor, *, target_rate: float = 0.05,
                      step: float = 0.05, lo: float = 0.3, hi: float = 0.9,
                      min_episodes: int = 10) -> dict:
    """Adapt threshold_detect from episode outcomes, within [lo, hi].

    AC-3.1 healthy means diagnose-rate <5%: if the window's fired/total
    exceeds target_rate, raise the threshold one step (desensitize).
    Otherwise hold — sensitizing on silence would need labeled misses.
    Compliance-guard builds are refused outright. Returns old/new/reason.
    """
    old = float(monitor.threshold)
    if bool(getattr(monitor, 'compliance_guard', False)):
        return {'old': old, 'new': old, 'changed': False,
                'reason': 'compliance guard: gamma must stay exactly 0, never calibrate'}

    episodes = list(getattr(monitor, 'episodes', []))
    total = len(episodes)
    if total < min_episodes:
        return {'old': old, 'new': old, 'changed': False,
                'reason': f'insufficient episodes ({total} < {min_episodes}); holding'}

    fired = sum(1 for e in episodes if e.get('fired'))
    rate = fired / total
    if rate > target_rate:
        new = min(hi, round(old + step, 4))
        return {'old': old, 'new': new, 'changed': new != old,
                'reason': f'diagnose-rate {rate:.3f} above target {target_rate}; desensitizing',
                'diagnose_rate': round(rate, 4)}
    return {'old': old, 'new': old, 'changed': False,
            'reason': f'diagnose-rate {rate:.3f} within target; holding',
            'diagnose_rate': round(rate, 4)}


def apply_calibration(monitor, report: dict) -> float:
    """Write a calibration report's threshold back. Separate step on purpose:
    measuring and acting stay distinct so dry runs can inspect first."""
    monitor.threshold = float(report['new'])
    return monitor.threshold


# ---------------------------------------------------------------------------
# 3. Reliance — measure scaffold fading (observation only)
# ---------------------------------------------------------------------------

def reliance_report(overrides: int, total_turns: int,
                    history: list[float] | None = None) -> dict:
    """Scaffold-reliance metric: overrides / turns, plus trend vs history.

    Trend compares against the last history entry: rising/falling/stable
    on a 0.05 deadband. Pure function of its inputs except it returns an
    extended history copy for the caller to persist. Never acts.
    """
    rate = round(overrides / total_turns, 4) if total_turns > 0 else 0.0
    hist = list(history or [])
    trend = 'stable'
    if hist:
        delta = rate - hist[-1]
        if delta > 0.05:
            trend = 'rising'
        elif delta < -0.05:
            trend = 'falling'
    return {'override_rate': rate, 'trend': trend,
            'history': hist + [rate],
            'reads_as': ('fading (loop carries more itself)' if trend == 'falling'
                         else 'deepening reliance (loop leans harder)' if trend == 'rising'
                         else 'steady reliance')}
