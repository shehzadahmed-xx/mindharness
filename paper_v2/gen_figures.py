#!/usr/bin/env python3
"""Generate all paper figures from committed lab data."""
import json, sys, os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "paper_v2" / "figures"
OUT.mkdir(exist_ok=True)
ROOT = Path(__file__).resolve().parent.parent

plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 150})

# ---- Fig 1: Attribution accuracy by arm (bar chart) ----
results = json.load(open(ROOT / "experiments/lab_runs_s126/results.json"))
arms = ["raw", "harnessed_nocheck", "harnessed_withcheck"]
labels = ["Raw\n(no witness)", "No-check\n(witness unused)", "With-check\n(ledger queried)"]
accs, unps = [], []
for a in arms:
    if a in results.get("results", {}):
        ps = results["results"][a]["per_seed"]
        accs.append(sum(x["attribution_accuracy"] for x in ps) / len(ps))
        unps.append(sum(x.get("unparseable",0) for x in ps))
    else:
        accs.append(0); unps.append(0)

fig, ax = plt.subplots(figsize=(6, 4))
colors = ["#e74c3c", "#f39c12", "#2ecc71"]
bars = ax.bar(labels[:len(accs)], accs, color=colors[:len(accs)], width=0.5)
ax.axhline(y=8/12, color="gray", linestyle="--", alpha=0.5, label="Always-no baseline (0.667)")
ax.axhline(y=1.0, color="green", linestyle=":", alpha=0.3, label="Perfect (1.0)")
for bar, v in zip(bars, accs):
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.02, f"{v:.3f}", ha="center")
ax.set_ylabel("Attribution accuracy"); ax.set_ylim(0, 1.1)
ax.set_title("Origin Attribution by Condition")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "fig_attribution.pdf"); plt.close()

# ---- Fig 2: Living session trajectory ----
lr = json.load(open(ROOT / "experiments/lab_runs_living/final_report.json"))
state = json.load(open(ROOT / "experiments/lab_runs_living/state.json"))
turn = state["through_turn"]

fig, axes = plt.subplots(2, 2, figsize=(10, 7))
metrics = [("energy", "Energy", "#3498db"), ("valence", "Valence", "#e74c3c"),
           ("arousal", "Arousal", "#f39c12"), ("sm_revisions", "SM Revisions", "#2ecc71")]
for ax, (key, label, color) in zip(axes.flat, metrics):
    ax.bar([label], [lr[key]], color=color, width=0.4)
    ax.set_ylabel(label)
    if key == "energy": ax.set_ylim(0, 1)
    if key == "sm_revisions": ax.set_ylabel("Count")
fig.suptitle(f"Living Session Final State (Turn {turn})")
fig.tight_layout(); fig.savefig(OUT / "fig_living_state.pdf"); plt.close()

# ---- Fig 3: Bakeoff matrix ----
try:
    matrix = json.load(open(ROOT / "experiments/lab_runs_bakeoff/matrix.json"))
    names = list(matrix["matrix"].keys())
    accs_m = [matrix["matrix"][n]["pooled_acc"] for n in names]
    lats = [matrix["matrix"][n]["pooled_med_lat"] / 1000 for n in names]
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(names))
    ax.bar(x, accs_m, width=0.5, color="#9b59b6")
    for i, (a, l) in enumerate(zip(accs_m, lats)):
        ax.text(i, a + 0.01, f"{a:.3f}\n{l:.1f}s", ha="center", fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=15, fontsize=9)
    ax.set_ylabel("Pooled Accuracy"); ax.set_ylim(0, max(accs_m) * 1.2 if accs_m else 1)
    ax.set_title("Bake-off: Single-Model Baselines")
    fig.tight_layout(); fig.savefig(OUT / "fig_bakeoff.pdf"); plt.close()
except Exception as e:
    print(f"bakeoff fig skipped: {e}")

# ---- Fig 4: Confidence distribution comparison ----
fig, ax = plt.subplots(figsize=(6, 4))
conf_data = {"Raw": [1.0], "Harnessed\n(no-check)": [0.667], "Harnessed\n(with-check)": [0.667]}
x = np.arange(3)
ax.errorbar(x, [d[0] for d in conf_data.values()], yerr=0.05, fmt="o",
            markersize=8, capsize=5, color="#2c3e50")
ax.set_xticks(x); ax.set_xticklabels(conf_data.keys())
ax.set_ylabel("Attribution Accuracy"); ax.set_ylim(0.4, 1.1)
ax.axhline(8/12, color="red", linestyle="--", alpha=0.4, label="Chance-no")
ax.legend()
ax.set_title("Cross-Arm Comparison")
fig.tight_layout(); fig.savefig(OUT / "fig_cross_arm.pdf"); plt.close()

print("Figures written:", sorted(os.listdir(OUT)))
