# Incident: blanket `git add -A` committed another session's work under my messages

**Date:** 2026-09-03. **Severity:** record integrity, not results.

Another agent session was writing to this repo concurrently. Five of my commits
used `git add -A`, and three of them swept in changes I never read, under
messages that describe entirely different work.

| commit | message is about | also silently contained |
|---|---|---|
| `ece947f` | reverting fabricated gating | `monitor.py` threshold **0.6 → 0.28** |
| `5c2aa4a` | restoring the threshold to 0.6 | *(this one was deliberate and correct)* |
| `cae4632` | gate dose-response results | threshold **0.6 → 0.28 again**, plus **`experiments/exp_reflexive_cost.py` (318 lines)** and **`tools/tiny_agent_iqra.py` (340 lines)** — 658 lines I never read |
| `7c01bdd` | recording gate outcomes | `backend.py` `max_tokens` **2000 → 800** |

## The part worth keeping

In `5c2aa4a` I wrote a commit message explaining that a blanket `git add -A`
had swept an unreviewed threshold change into `ece947f`. **Two commits later I
did the same thing to the same line.** Documenting a failure mode is not the
same as no longer having it, and the gap between the two is roughly two
commits wide.

## Results: not contaminated

Every gate run passed `--gate-threshold` explicitly (0.60, 0.28, and 0.28 for
the sham arm), so the library default never applied to a recorded run. The
`max_tokens` 2000 → 800 change is comfortably above what a `PROBE_SCHEMA`
response consumes. No banked number changes.

## Corrections

1. `monitor.py` threshold restored to the documented **0.6**, committed by
   explicit path rather than `git add -A`.
2. `exp_reflexive_cost.py` and `tiny_agent_iqra.py` remain in the tree — they
   are another session's work and not mine to delete — but they are **unreviewed
   by me**, and nothing in `paper_v3` cites them.
3. No further `git add -A` in this repo while a second session is writing to it.
   Stage by path.
