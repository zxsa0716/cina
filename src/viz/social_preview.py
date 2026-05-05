"""Generate the GitHub social preview image for CINA (1280 × 640 PNG).

Saved to docs/social_preview.png — designed to be uploaded to:
  Repository → Settings → General → Social preview → Upload an image

Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
License: MIT
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------

BG = "#0b0d12"
FG = "#f8fafc"
ACCENT = "#6ea8ff"
WARM = "#f59e0b"
SUCCESS = "#10b981"
DANGER = "#dc2626"
PRIMARY = "#2a5298"
MUTED = "#94a3b8"

STANCE_CMAP = LinearSegmentedColormap.from_list(
    "cina_stance",
    [(0.0, "#dc2626"), (0.5, "#1c2536"), (1.0, "#10b981")],
    N=256,
)


def main():
    # 1280 x 640 px at 100 dpi = 12.8 x 6.4 inches
    fig = plt.figure(figsize=(12.8, 6.4), dpi=100, facecolor=BG)

    # Two zones: left text, right visual
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.05,
                           left=0.04, right=0.97, top=0.95, bottom=0.06)

    # ---------- LEFT: title & metrics ----------
    ax_text = fig.add_subplot(gs[0, 0])
    ax_text.set_facecolor(BG)
    ax_text.set_xlim(0, 1)
    ax_text.set_ylim(0, 1)
    ax_text.axis("off")

    ax_text.text(0.04, 0.92, "CINA", color=FG, fontsize=72,
                  fontweight="bold", family="DejaVu Sans", va="top")
    ax_text.text(0.04, 0.74, "Climate Issue-Network Analysis",
                  color=ACCENT, fontsize=20, fontweight="600",
                  family="DejaVu Sans", va="top")
    ax_text.text(0.04, 0.66,
                  "An end-to-end LLM → graph → LLM pipeline for\nclimate-negotiation intelligence",
                  color="#cbd5e1", fontsize=14, family="DejaVu Sans",
                  va="top")

    # Metric chips
    chips = [
        ("Stage 1 ρ = 0.658", PRIMARY),
        ("Contested P@3 = 1.00", SUCCESS),
        ("Cross-LLM α = 0.93", ACCENT),
        ("R-GAT chair attention = 1.00", WARM),
    ]
    y_chip = 0.46
    x_chip = 0.04
    for i, (label, color) in enumerate(chips):
        # Approximate width
        w = 0.012 * len(label) + 0.05
        if x_chip + w > 0.94:
            x_chip = 0.04
            y_chip -= 0.085
        rect = mpatches.FancyBboxPatch(
            (x_chip, y_chip), w, 0.06,
            boxstyle="round,pad=0.012,rounding_size=0.025",
            facecolor=color, edgecolor="white", linewidth=0,
            alpha=0.92,
        )
        ax_text.add_patch(rect)
        ax_text.text(x_chip + w / 2, y_chip + 0.03, label,
                      color="white", fontsize=11.5, fontweight="700",
                      ha="center", va="center", family="DejaVu Sans")
        x_chip += w + 0.018

    # COP30 retrospective tagline
    ax_text.text(0.04, 0.20,
                  "Retrospectively validated on COP30 Belém Adaptation Indicators",
                  color=FG, fontsize=14, fontweight="600",
                  family="DejaVu Sans", va="top")
    ax_text.text(0.04, 0.13,
                  "FCCC/PA/CMA/2025/L.25E · Pre-registered for COP31 (2026-09 freeze)",
                  color=MUTED, fontsize=11, style="italic",
                  family="DejaVu Sans", va="top")

    ax_text.text(0.04, 0.045,
                  "Heedo Choi · Kookmin University · Climate Technology Convergence",
                  color="#cbd5e1", fontsize=11.5, fontweight="500",
                  family="DejaVu Sans", va="top")

    # ---------- RIGHT: stance heatmap teaser ----------
    ax_fig = fig.add_subplot(gs[0, 1])
    ax_fig.set_facecolor(BG)

    # 13 countries × 6 issues stance matrix
    countries = ["Brazil", "EU", "USA", "China", "India", "AOSIS",
                 "Korea", "Saudi", "Japan", "AILAC", "AGN", "LMDC", "Multi"]
    issues = ["GGA-IND", "GGA-MOI", "NAPs", "JT-ADAPT", "L&D", "FIN-ADAPT"]
    M = np.array([
        [0.95, 0.78, 0.88, 0.92, 0.55, 0.70],
        [0.55, 0.65, 0.72, 0.60, 0.45, 0.58],
        [0.30, 0.20, 0.50, 0.40, -0.20, 0.25],
        [-0.30, 0.40, 0.55, 0.50, 0.65, 0.70],
        [-0.15, 0.55, 0.60, 0.45, 0.85, 0.90],
        [0.85, 0.90, 0.78, 0.65, 0.95, 0.92],
        [0.65, 0.62, 0.75, 0.78, 0.39, 0.55],
        [-0.55, -0.65, 0.20, -0.30, 0.10, 0.40],
        [0.45, 0.50, 0.62, 0.55, 0.30, 0.48],
        [0.85, 0.85, 0.80, 0.70, 0.85, 0.85],
        [0.65, 0.70, 0.72, 0.62, 0.75, 0.70],
        [-0.20, 0.50, 0.55, 0.40, 0.55, 0.60],
        [0.75, 0.65, 0.70, 0.60, 0.55, 0.65],
    ])
    scaled = (M + 1) / 2

    im = ax_fig.imshow(scaled, cmap=STANCE_CMAP, aspect="auto",
                        vmin=0, vmax=1)
    ax_fig.set_xticks(range(len(issues)))
    ax_fig.set_xticklabels(issues, color=FG, fontsize=9, rotation=18)
    ax_fig.set_yticks(range(len(countries)))
    ax_fig.set_yticklabels(countries, color=FG, fontsize=9)
    for spine in ax_fig.spines.values():
        spine.set_visible(False)
    ax_fig.tick_params(colors=FG, length=0)

    # Annotate Brazil chair + Korea L&D weakness
    ax_fig.add_patch(plt.Rectangle((-0.5, -0.5), len(issues), 1, fill=False,
                                     edgecolor=WARM, linewidth=2.5,
                                     linestyle="-"))
    k_idx = countries.index("Korea")
    l_idx = issues.index("L&D")
    ax_fig.add_patch(plt.Rectangle((l_idx - 0.5, k_idx - 0.5), 1, 1,
                                     fill=False, edgecolor=DANGER,
                                     linewidth=2.5, linestyle="--"))

    # Title above figure
    ax_fig.set_title("Country × Issue stance tensor", color=ACCENT,
                      fontsize=12, fontweight="700", pad=8)

    # Bottom watermark
    fig.text(0.985, 0.012, "github.com/zxsa0716/cina",
              color=MUTED, fontsize=9, ha="right", va="bottom",
              family="DejaVu Sans")

    out_path = ROOT / "docs" / "social_preview.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=100, facecolor=BG, bbox_inches=None,
                 pad_inches=0)
    plt.close()
    print(f"✓ {out_path.relative_to(ROOT)} (1280 × 640)")


if __name__ == "__main__":
    main()
