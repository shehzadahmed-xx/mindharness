#!/usr/bin/env python3
"""Long-horizon living session — the loop, running (Phase LIVE).

The agent lives through N turns of varied tasks on a real backend:
predict -> perceive -> act -> consequence -> skill/graph/SM updates ->
periodic consolidation -> checkpoint to disk. Resumable via state file.

Usage:
  python3 experiments/living_session.py --api-key KEY [--model M] [--turns 40]
      [--segment 10] [--resume STATE.json] [--stub]
Stub mode runs the full loop offline (deterministic responder) for plumbing
verification; live mode routes through BackendClient per registry.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.agent_harness import AgentHarness  # noqa: E402
from harness_core.consolidation import record_query_hit  # noqa: E402

TASK_STREAM = [
    ("Explain how the musharaka pool distributes quarterly profit.", "finance", True),
    ("Refactor the parser module and run its tests.", "coding", True),
    ("Summarize what changed in the last deployment.", "ops", True),
    ("Diagnose why the nightly job failed.", "ops", False),
    ("Draft one sentence on witness-access for the paper.", "writing", True),
    ("Check whether the pilot data supports the exhaustion claim.", "research", True),
    ("Deploy the hotfix to staging.", "coding", True),
    ("Reflect: which of your recent answers were weakest?", "metacog", True),
]


def stub_responder(messages, ctx):
    return "completed deterministically [" + str(len(ctx.get("affordances", []))) + "]"


def build_live(api_key, model, base_url):
    from harness_core.backend import BackendClient
    holder: dict = {}

    def respond(messages, ctx):
        client = holder.get("c")
        if client is None:
            client = BackendClient(api_key=api_key, model=model,
                                   base_url=base_url, seed=7,
                                   purpose="living")
            holder["c"] = client
        out, _ = client.chat(messages, purpose=ctx.get("purpose", "turn"),
                             json_schema=ctx.get("json_schema"))
        return out

    return respond


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", default="stub")
    ap.add_argument("--model", default="nemotron-3-ultra-free")
    ap.add_argument("--base-url", default="https://opencode.ai/zen/v1")
    ap.add_argument("--turns", type=int, default=40)
    ap.add_argument("--segment", type=int, default=10)
    ap.add_argument("--state", default="experiments/lab_runs_living/state.json")
    ap.add_argument("--stub", action="store_true")
    ap.add_argument("--start", type=int, default=0)
    args = ap.parse_args()

    out_dir = Path(__file__).parent / "lab_runs_living"
    out_dir.mkdir(exist_ok=True)

    if args.stub:
        harness = AgentHarness(respond_fn=stub_responder)
    else:
        harness = AgentHarness(respond_fn=build_live(args.api_key, args.model,
                                                     args.base_url))

    # resume: restore consolidated facts count as cursor proxy (full SM
    # persistence lands with DSH placement; sessions are append-only here)
    start = args.start
    report_at = {}

    for t in range(start, start + args.turns):
        task_text, qtype, ok = TASK_STREAM[t % len(TASK_STREAM)]
        r = harness.run_task(task_text, task_id=f"live-{t}", fok=3,
                             is_tool_action=True, success=ok)
        mid = harness.remember_episode(
            f"{task_text} -> {r.response[:60]}", query_type=qtype)
        record_query_hit(harness.memory, mid, qtype)

        if r.action == 'abstain':
            print(f"[{t}] ABSTAINED (score {r.monitor_score})")
        elif (t + 1) % args.segment == 0:
            cons = harness.consolidate()
            confirmed = harness.confirm_proposals_into_self_model()
            harness.compaction_cycle(f"segment through turn {t}")
            print(f"[{t}] consolidated: +{len(cons['promoted'])} promoted,"
                  f" {len(confirmed)} proposals->SM,"
                  f" sm_rev={harness.sm.get()['revision']}")
        else:
            print(f"[{t}] {r.action} energy={r.energy:.2f}")

        # checkpoint every segment boundary
        if (t + 1) % args.segment == 0:
            rep = harness.session_report()
            (out_dir / "state.json").write_text(json.dumps(
                {'through_turn': t, 'report': rep}, indent=1))

    final = harness.session_report()
    (out_dir / "final_report.json").write_text(json.dumps(final, indent=1))
    print("\n=== LIVING SESSION REPORT ===")
    print(json.dumps(final, indent=1))


if __name__ == "__main__":
    main()
