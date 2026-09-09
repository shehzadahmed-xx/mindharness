#!/bin/zsh
# Watchdog: keeps the sham battery alive through server deaths.
# Checks every 60s: (1) llama-server on :8081 answers, else waits for
# launchd keep-alive to revive it; (2) pilot process alive, else relaunches
# (exp_s126_v3 resumes from banked results). Logs every action.
# Honest label: machine-tended, not self-tended. The loop does not restart
# itself; the OS restarts its world. Step one toward gap 1.
LOG=/tmp/watchdog.log
OUTDIR=lab_runs_s126_spark_n2
say() { echo "$(date '+%H:%M:%S') $1" >> "$LOG"; }

while true; do
  if ! curl -s -m 8 -o /dev/null http://127.0.0.1:8081/v1/models; then
    say "server down, waiting for launchd revival"
    sleep 60
    continue
  fi
  if ! pgrep -f "exp_s126_v3.*spark-x2.5-4b" > /dev/null; then
    if python3 -c "import json,sys; d=json.load(open('/Users/shehzad/Desktop/mindharness/experiments/$OUTDIR/results.json')); sys.exit(0 if len(d.get('results',{}).get('sham',{}).get('per_seed',[]))>=2 else 1)" 2>/dev/null; then
      say "pilot complete (2 sham seeds), watchdog standing down"
      exit 0
    fi
    say "pilot dead, relaunching (resume from banked)"
    nohup python3 -u /Users/shehzad/Desktop/mindharness/experiments/exp_s126_v3.py \
      --api-key local --base-url http://127.0.0.1:8081/v1 --model spark-x2.5-4b \
      --seeds 2 --out-dir "$OUTDIR" --exploratory --pace 1.0 --max-tokens 300 \
      >> /tmp/sham_spark_n2.log 2>&1 < /dev/null &
    disown %1 2>/dev/null
  fi
  sleep 60
done
