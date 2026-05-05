"""
Generate the R-GAT attention figure for the paper.

Reads data/processed/rgat_training_results.json, plots:
  (a) attention weight per relation type (bar chart)
  (b) val Spearman ρ training curve
  (c) coalition accuracy + P@3 contested over epochs

Saves to docs/web/figures/fig8_rgat_training.png (300 dpi).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main(input_path: str = "data/processed/rgat_training_results.json",
         output_path: str = "docs/web/figures/fig8_rgat_training.png") -> None:

    with open(input_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    history = results["history"]
    attn = results["attention_per_relation"]

    # Mean attention per relation (averaged across layers)
    relations = list(attn.keys())
    mean_attn = [np.mean(attn[r]) for r in relations]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=300)

    # ------ Panel (a): attention per relation type ------
    ax = axes[0]
    colors = {"co_chairs": "#f59e0b", "member_of": "#6ea8ff",
              "similar_to": "#10b981", "has_stance": "#94a3b8"}
    bar_colors = [colors.get(r, "#888") for r in relations]
    bars = ax.barh(relations, mean_attn, color=bar_colors, edgecolor="black", linewidth=0.6)
    for bar, v in zip(bars, mean_attn):
        ax.text(v + 0.01, bar.get_y() + bar.get_height() / 2,
                f"{v:.3f}", va="center", fontsize=10, fontweight="bold")
    ax.set_xlabel("Mean attention weight (across layers, heads)", fontsize=11)
    ax.set_title("(a) R-GAT learned attention per relation\n— procedural authority dominates",
                 fontsize=11, fontweight="bold")
    ax.set_xlim(0, 1.15)
    ax.grid(axis="x", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # ------ Panel (b): training curve ------
    ax = axes[1]
    epochs = [h["epoch"] for h in history]
    rho = [h["val_spearman"] for h in history]
    mse = [h["val_mse"] for h in history]
    ax.plot(epochs, rho, marker="o", color="#2a5298", lw=2, markersize=5,
            label="Validation Spearman ρ")
    ax.set_xlabel("Epoch", fontsize=11)
    ax.set_ylabel("Spearman ρ (validation)", fontsize=11, color="#2a5298")
    ax.tick_params(axis="y", labelcolor="#2a5298")
    ax.axhline(0.6, ls="--", color="#888", alpha=0.6, lw=1, label="ρ = 0.6 threshold")
    ax.set_title(f"(b) Stance prediction convergence\nfinal ρ = {rho[-1]:.3f}",
                 fontsize=11, fontweight="bold")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.3)
    ax.spines["top"].set_visible(False)

    ax2 = ax.twinx()
    ax2.plot(epochs, mse, marker="s", color="#dc2626", lw=1.5, markersize=4,
             alpha=0.7, label="Validation MSE")
    ax2.set_ylabel("MSE", color="#dc2626", fontsize=11)
    ax2.tick_params(axis="y", labelcolor="#dc2626")
    ax2.spines["top"].set_visible(False)

    # ------ Panel (c): multi-task metrics ------
    ax = axes[2]
    coal = [h["coalition_acc"] for h in history]
    p3 = [h["p_at_3_contested"] for h in history]
    ax.plot(epochs, coal, marker="^", color="#10b981", lw=2, markersize=6,
            label="Coalition accuracy")
    ax.plot(epochs, p3, marker="D", color="#f59e0b", lw=2, markersize=6,
            label="Contested P@3")
    ax.axhline(coal[-1], ls=":", color="#10b981", alpha=0.5)
    ax.axhline(p3[-1], ls=":", color="#f59e0b", alpha=0.5)
    ax.set_xlabel("Epoch", fontsize=11)
    ax.set_ylabel("Score", fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.set_title(f"(c) Multi-task heads\ncoal_acc = {coal[-1]:.2f}, P@3 = {p3[-1]:.2f}",
                 fontsize=11, fontweight="bold")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.suptitle("Figure 8 — Heterogeneous R-GAT training, attention, and multi-task metrics",
                 fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
