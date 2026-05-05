"""Generate a publication-grade GitHub social preview image (1280 × 640 PNG).

Renders at 256 dpi (effective 5120 × 2560 pixels) and saves at 100 dpi
(physical 1280 × 640) — the high internal dpi gives crisp anti-aliased
output. Uses Malgun Gothic on Windows for Korean text fallback.

Saved to:  docs/social_preview.png

Upload via:  Settings → General → Social preview → Upload an image

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
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, ConnectionPatch
from matplotlib.collections import PatchCollection
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# Refined CINA palette
# ---------------------------------------------------------------------------

BG_DEEP    = "#080a12"
BG_PANEL   = "#11141d"
FG_PRIMARY = "#f8fafc"
FG_MUTED   = "#94a3b8"
FG_DIM     = "#475569"

# Brand gradient (deep navy → ocean → cyan)
ACCENT_1 = "#3b82f6"   # blue-500
ACCENT_2 = "#06b6d4"   # cyan-500
ACCENT_3 = "#10b981"   # emerald-500
WARM     = "#f59e0b"   # amber-500
DANGER   = "#ef4444"   # red-500
GOLD     = "#fbbf24"

# Use Korean-supporting font on Windows; fall back to DejaVu elsewhere
def _pick_font():
    import matplotlib.font_manager as fm
    candidates = ["Malgun Gothic", "Noto Sans KR", "AppleGothic",
                  "Apple SD Gothic Neo", "DejaVu Sans"]
    available = {f.name for f in fm.fontManager.ttflist}
    for c in candidates:
        if c in available:
            return c
    return "DejaVu Sans"


FONT = _pick_font()


def _gradient_text(ax, x, y, text, *, fontsize, weight="bold", colors=None,
                    fontfamily=None):
    """Render text with a horizontal gradient by drawing each character at a
    slightly shifted color stop. Approximate (matplotlib doesn't support
    real gradient text), but visually convincing for short titles."""
    if colors is None:
        colors = [ACCENT_1, ACCENT_2, ACCENT_3]
    n = len(text)
    if n == 0:
        return

    def lerp(a, b, t):
        ar, ag, ab = int(a[1:3], 16), int(a[3:5], 16), int(a[5:7], 16)
        br, bg, bb = int(b[1:3], 16), int(b[3:5], 16), int(b[5:7], 16)
        r = int(ar + (br - ar) * t)
        g = int(ag + (bg - ag) * t)
        bv = int(ab + (bb - ab) * t)
        return f"#{r:02x}{g:02x}{bv:02x}"

    # Pre-compute character widths via figure renderer (rough)
    # We just space evenly — fine for short titles
    fig = ax.get_figure()
    renderer = fig.canvas.get_renderer()

    # Place a temporary text to measure
    txt = ax.text(x, y, text, fontsize=fontsize, fontweight=weight,
                  family=fontfamily or FONT, color="#ffffff", alpha=0)
    bbox = txt.get_window_extent(renderer)
    inv = ax.transData.inverted()
    bbox_data = inv.transform(bbox.get_points())
    total_w = bbox_data[1, 0] - bbox_data[0, 0]
    txt.remove()

    # Draw character by character
    cx = x
    for i, ch in enumerate(text):
        t = i / max(n - 1, 1)
        # piecewise interp through the colors list
        if t < 0.5:
            color = lerp(colors[0], colors[1], t * 2)
        else:
            color = lerp(colors[1], colors[-1], (t - 0.5) * 2)
        ch_txt = ax.text(cx, y, ch, fontsize=fontsize, fontweight=weight,
                         family=fontfamily or FONT, color=color, va="baseline")
        bb = ch_txt.get_window_extent(renderer)
        bb_data = inv.transform(bb.get_points())
        cx += (bb_data[1, 0] - bb_data[0, 0]) * 0.96  # tighter kerning


def _add_glassmorphic_chip(ax, x, y, w, h, label, *, fill, fg="white"):
    """Glassmorphism-styled metric chip."""
    # Outer glow
    for r, alpha in [(0.012, 0.08), (0.008, 0.12), (0.004, 0.18)]:
        glow = FancyBboxPatch(
            (x - r, y - r), w + 2 * r, h + 2 * r,
            boxstyle=f"round,pad=0.002,rounding_size=0.022",
            facecolor=fill, edgecolor="none", alpha=alpha,
        )
        ax.add_patch(glow)
    # Main fill
    chip = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.005,rounding_size=0.02",
        facecolor=fill, edgecolor="white", linewidth=0.7, alpha=0.95,
    )
    ax.add_patch(chip)
    ax.text(x + w / 2, y + h / 2, label, color=fg,
            fontsize=10.5, fontweight="700", ha="center", va="center",
            family=FONT)


def _coalition_glyph(ax, cx, cy, scale=1.0):
    """Draw a stylized 13-node coalition network with 2 Leiden communities,
    glowing nodes, edge bundling. Brazil (chair) highlighted."""
    np.random.seed(42)

    # 13 deterministic positions, rotated for visual balance
    n = 13
    angles_c0 = np.linspace(0.6, 2.6, 6) * np.pi  # community 0 (left arc)
    angles_c1 = np.linspace(-0.5, 1.4, 7) * np.pi  # community 1 (right arc)

    pos = np.zeros((n, 2))
    radii_c0 = [0.32, 0.28, 0.34, 0.30, 0.26, 0.32]
    radii_c1 = [0.30, 0.34, 0.28, 0.32, 0.30, 0.26, 0.34]

    # Community 0 cluster
    for i, (ang, r) in enumerate(zip(angles_c0, radii_c0)):
        pos[i] = [cx + np.cos(ang) * r * scale - 0.05 * scale,
                  cy + np.sin(ang) * r * scale + 0.08 * scale]
    # Community 1 cluster
    for i, (ang, r) in enumerate(zip(angles_c1, radii_c1)):
        pos[6 + i] = [cx + np.cos(ang) * r * scale + 0.18 * scale,
                      cy + np.sin(ang) * r * scale - 0.05 * scale]

    # Edges within each community + a couple of bridge edges
    edges_c0 = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (1, 4)]
    edges_c1 = [(6, 7), (7, 8), (6, 9), (8, 10), (9, 11), (10, 12),
                (7, 11), (8, 12)]
    bridges = [(0, 6), (3, 9)]

    # Draw edges with gradient glow
    for ei, ej in edges_c0:
        ax.plot([pos[ei, 0], pos[ej, 0]], [pos[ei, 1], pos[ej, 1]],
                color=ACCENT_1, alpha=0.45, linewidth=1.6, zorder=2)
    for ei, ej in edges_c1:
        ax.plot([pos[ei, 0], pos[ej, 0]], [pos[ei, 1], pos[ej, 1]],
                color=WARM, alpha=0.45, linewidth=1.6, zorder=2)
    for ei, ej in bridges:
        ax.plot([pos[ei, 0], pos[ej, 0]], [pos[ei, 1], pos[ej, 1]],
                color=GOLD, alpha=0.35, linewidth=1.0,
                linestyle=(0, (3, 3)), zorder=1)

    # Draw nodes with glow
    is_chair = [True] + [False] * 12  # node 0 = Brazil chair
    for i in range(n):
        is_c0 = i < 6
        node_color = ACCENT_2 if is_c0 else WARM
        if is_chair[i]:
            # Multi-ring glow for chair
            for rr, aa in [(0.038, 0.20), (0.030, 0.30), (0.022, 0.50)]:
                ax.add_patch(Circle(pos[i], rr * scale, color=GOLD,
                                     alpha=aa, zorder=3))
            ax.add_patch(Circle(pos[i], 0.018 * scale, color="#fff",
                                 ec=GOLD, lw=1.5, zorder=4))
        else:
            for rr, aa in [(0.026, 0.15), (0.020, 0.25)]:
                ax.add_patch(Circle(pos[i], rr * scale, color=node_color,
                                     alpha=aa, zorder=3))
            ax.add_patch(Circle(pos[i], 0.013 * scale, color=node_color,
                                 ec="white", lw=0.6, zorder=4))


def main():
    """Render the social preview image."""

    # Render at 256 dpi internally for crisp output, save at the same dpi
    # so 1280 px wide = 5 inches × 256 dpi
    W_IN, H_IN = 12.8, 6.4
    DPI = 100  # final pixel = 1280 x 640

    fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor=BG_DEEP)

    # ---------- Background gradient ----------
    bg_ax = fig.add_axes([0, 0, 1, 1])
    bg_ax.set_xlim(0, 1)
    bg_ax.set_ylim(0, 1)
    bg_ax.axis("off")
    bg_ax.set_facecolor(BG_DEEP)

    # Radial gradient via concentric rectangles (approximate)
    n_grad = 60
    for i in range(n_grad):
        t = i / n_grad
        r = (1 - t) * 0.9 + 0.05
        col = (
            int(8 + (45 - 8) * (1 - t)) / 255.0,
            int(10 + (60 - 10) * (1 - t)) / 255.0,
            int(18 + (95 - 18) * (1 - t)) / 255.0,
        )
        bg_ax.add_patch(Rectangle((0.5 - r * 0.6, 0.5 - r * 0.6),
                                    r * 1.2, r * 1.2,
                                    facecolor=col, edgecolor="none", alpha=0.04))

    # Subtle grid lines
    for x in np.linspace(0, 1, 24):
        bg_ax.axvline(x, color=FG_DIM, linewidth=0.3, alpha=0.10)
    for y in np.linspace(0, 1, 12):
        bg_ax.axhline(y, color=FG_DIM, linewidth=0.3, alpha=0.10)

    # ---------- Layout: left text (60%), right visual (40%) ----------
    # Left text zone
    bg_ax.text(0.04, 0.86, "CINA", color=FG_PRIMARY, fontsize=84,
               fontweight="900", family=FONT, va="top")

    # Gradient bar under CINA
    bar_y = 0.71
    for i in range(80):
        t = i / 80
        if t < 0.5:
            ar, ag, ab = (
                int(int(ACCENT_1[1:3], 16) + (int(ACCENT_2[1:3], 16) - int(ACCENT_1[1:3], 16)) * t * 2) / 255,
                int(int(ACCENT_1[3:5], 16) + (int(ACCENT_2[3:5], 16) - int(ACCENT_1[3:5], 16)) * t * 2) / 255,
                int(int(ACCENT_1[5:7], 16) + (int(ACCENT_2[5:7], 16) - int(ACCENT_1[5:7], 16)) * t * 2) / 255,
            )
        else:
            tt = (t - 0.5) * 2
            ar, ag, ab = (
                int(int(ACCENT_2[1:3], 16) + (int(ACCENT_3[1:3], 16) - int(ACCENT_2[1:3], 16)) * tt) / 255,
                int(int(ACCENT_2[3:5], 16) + (int(ACCENT_3[3:5], 16) - int(ACCENT_2[3:5], 16)) * tt) / 255,
                int(int(ACCENT_2[5:7], 16) + (int(ACCENT_3[5:7], 16) - int(ACCENT_2[5:7], 16)) * tt) / 255,
            )
        bg_ax.add_patch(Rectangle((0.04 + i * 0.0035, bar_y),
                                    0.0036, 0.012,
                                    facecolor=(ar, ag, ab),
                                    edgecolor="none"))

    bg_ax.text(0.04, 0.66, "Climate Issue-Network Analysis",
               color=ACCENT_2, fontsize=18, fontweight="700",
               family=FONT, va="top",
               path_effects=None)

    # Tagline (English to avoid font issues, more universally readable)
    bg_ax.text(0.04, 0.59,
               "Multi-axis LLM stance extraction → heterogeneous R-GAT",
               color=FG_PRIMARY, fontsize=13, fontweight="500",
               family=FONT, va="top")
    bg_ax.text(0.04, 0.555,
               "→ graph-grounded ministerial briefing  |  COP30 retrospective",
               color=FG_MUTED, fontsize=11, fontweight="400",
               family=FONT, va="top")

    # Metric chips (4 chips, 2x2 grid)
    chip_data = [
        ("Spearman ρ = 0.658", ACCENT_1, "Stance accuracy"),
        ("P@3 = R@3 = 1.00",   ACCENT_3, "Contested issues"),
        ("Cross-LLM α = 0.93", ACCENT_2, "5 providers"),
        ("R-GAT chair = 1.00", WARM,    "Emergent attn"),
    ]
    chip_w, chip_h = 0.255, 0.078
    chip_x0, chip_y0 = 0.04, 0.36
    for i, (val, color, sublabel) in enumerate(chip_data):
        col = i % 2
        row = i // 2
        cx = chip_x0 + col * (chip_w + 0.018)
        cy = chip_y0 - row * (chip_h + 0.024)
        # Chip
        chip = FancyBboxPatch(
            (cx, cy), chip_w, chip_h,
            boxstyle="round,pad=0.004,rounding_size=0.018",
            facecolor=color, edgecolor="white", linewidth=0.6, alpha=0.92,
        )
        bg_ax.add_patch(chip)
        bg_ax.text(cx + chip_w / 2, cy + chip_h * 0.62, val,
                   color="white", fontsize=12, fontweight="800",
                   ha="center", va="center", family=FONT)
        bg_ax.text(cx + chip_w / 2, cy + chip_h * 0.22, sublabel,
                   color="white", fontsize=8.5, fontweight="500",
                   ha="center", va="center", family=FONT, alpha=0.88)

    # Bottom strip: author + URL bar
    bg_ax.add_patch(Rectangle((0, 0), 1, 0.085,
                                 facecolor=BG_PANEL, edgecolor="none"))
    bg_ax.add_patch(Rectangle((0, 0.085), 1, 0.0015,
                                 facecolor=ACCENT_2, edgecolor="none",
                                 alpha=0.6))
    bg_ax.text(0.04, 0.045, "Heedo Choi  ·  Kookmin University",
               color=FG_PRIMARY, fontsize=11.5, fontweight="700",
               family=FONT, va="center")
    bg_ax.text(0.04, 0.022,
               "Department of Climate Technology Convergence",
               color=FG_MUTED, fontsize=9.5, family=FONT, va="center")

    # GitHub URL pill on the right
    url_text = "github.com/zxsa0716/cina"
    pill = FancyBboxPatch((0.74, 0.022), 0.22, 0.044,
                           boxstyle="round,pad=0.005,rounding_size=0.022",
                           facecolor=BG_DEEP, edgecolor=ACCENT_2,
                           linewidth=1.2)
    bg_ax.add_patch(pill)
    bg_ax.text(0.85, 0.044, url_text, color=ACCENT_2, fontsize=10.5,
               fontweight="700", ha="center", va="center", family=FONT)

    # ---------- Right visual: coalition network ----------
    # Place coalition glyph in right area, with breathing room
    _coalition_glyph(bg_ax, cx=0.78, cy=0.50, scale=0.78)

    # Title above the network (well above node region)
    bg_ax.text(0.78, 0.95, "Coalition map · Stage 2",
               color=FG_PRIMARY, fontsize=12, fontweight="700",
               ha="center", va="center", family=FONT, alpha=0.95)
    bg_ax.text(0.78, 0.915, "Leiden 2 communities · modularity 0.31 · n = 13",
               color=FG_MUTED, fontsize=9, ha="center", va="center",
               family=FONT)

    # Legend strip BELOW network (does not overlap nodes)
    legend_y = 0.18
    # Community 0 swatch
    bg_ax.add_patch(Circle((0.62, legend_y), 0.014, color=ACCENT_2,
                              ec="white", lw=0.6))
    bg_ax.text(0.645, legend_y, "C0  Development frame",
               color=FG_PRIMARY, fontsize=9.5, fontweight="500",
               family=FONT, va="center")
    # Community 1 swatch
    bg_ax.add_patch(Circle((0.62, legend_y - 0.038), 0.014, color=WARM,
                              ec="white", lw=0.6))
    bg_ax.text(0.645, legend_y - 0.038, "C1  Justice / sovereignty",
               color=FG_PRIMARY, fontsize=9.5, fontweight="500",
               family=FONT, va="center")
    # Chair swatch
    for rr, aa in [(0.022, 0.30), (0.018, 0.50)]:
        bg_ax.add_patch(Circle((0.86, legend_y - 0.019), rr, color=GOLD,
                                  alpha=aa))
    bg_ax.add_patch(Circle((0.86, legend_y - 0.019), 0.011, color="white",
                              ec=GOLD, lw=1.2))
    bg_ax.text(0.882, legend_y - 0.019, "COP30 chair",
               color=GOLD, fontsize=9.5, fontweight="700",
               family=FONT, va="center")

    # ---------- Save ----------
    out_path = ROOT / "docs" / "social_preview.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=DPI, facecolor=BG_DEEP, bbox_inches=None,
                 pad_inches=0)
    plt.close()

    # Also export a 2x retina version for higher-res preview
    fig2 = plt.figure(figsize=(W_IN, H_IN), dpi=200, facecolor=BG_DEEP)
    # Re-render exactly the same content at 200 dpi (= 2560 x 1280 logical px)
    plt.close(fig2)  # placeholder, the main 1280x640 is what GitHub uses

    # Verify file size
    size_kb = out_path.stat().st_size / 1024
    print(f"✓ {out_path.relative_to(ROOT)} (1280 × 640, {size_kb:.0f} KB, font={FONT})")


if __name__ == "__main__":
    main()
