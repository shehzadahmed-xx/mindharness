#!/bin/bash
# Run this in YOUR OWN Terminal.app window (double-click works too).
# Survives independent of any AI session. Checkpoint-resumable.
cd ~/Desktop/springfish
KEY=$(python3 -c "import json; print(json.load(open('/Users/shehzad/.local/share/opencode/auth.json'))['opencode']['key'])")
python3 experiments/exp_s126_v2.py --api-key "$KEY" --model x-preview-f-free \
  --base-url https://opencode.ai/zen/v1 --seeds 5
echo "DONE. Results:"
cat experiments/lab_runs_s126/results.json | python3 -m json.tool | head -40
