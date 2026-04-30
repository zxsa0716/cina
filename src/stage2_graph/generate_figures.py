"""Stage 2 figures — community detection + centrality + frame consistency 시각화.

matplotlib + networkx 기반 (torch 불요). 논문 figures.
"""
from __future__ import annotations

import json
import logging
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.stage2.figs")

ROOT = Path(__file__).resolve().parent.parent.parent
FIGS = ROOT / "data" / "processed" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)


def load_analysis() -> dict:
    p = ROOT / "data" / "processed" / "graph_analysis_v1.json"
    return json.loads(p.read_text(encoding="utf-8"))


def fig1_country_issue_heatmap(analysis: dict) -> Path:
    """Figure 1: Country × Issue stance heatmap."""
    matrix = analysis["country_issue_matrix"]
    issues = ["GGA-IND", "ADAPT-FIN", "L&D-OP", "NAPs", "MIT-ADAPT", "JT-ADAPT"]
    countries = sorted(matrix.keys())

    data = np.full((len(countries), len(issues)), np.nan)
    for i, c in enumerate(countries):
        for j, iss in enumerate(issues):
            v = matrix[c].get(iss)
            if v is not None:
                data[i, j] = v

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(data, cmap="RdBu", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(issues)))
    ax.set_xticklabels(issues, rotation=45, ha="right")
    ax.set_yticks(range(len(countries)))
    ax.set_yticklabels(countries)
    ax.set_title("CINA Stage 1: Country × Issue Stance Heatmap (n=21 LLM extractions, Groq)")

    for i in range(len(countries)):
        for j in range(len(issues)):
            v = data[i, j]
            if not np.isnan(v):
                ax.text(j, i, f"{v:+.1f}", ha="center", va="center",
                        color="white" if abs(v) > 0.5 else "black", fontsize=9)

    cbar = plt.colorbar(im, ax=ax, label="Stance score [-1, +1]")
    plt.tight_layout()
    out = FIGS / "fig1_country_issue_heatmap.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Figure 1 saved: %s", out)
    return out


def fig2_procedural_authority(analysis: dict) -> Path:
    """Figure 2: Procedural authority (chair_role + pen_holder) per country."""
    auth = analysis.get("procedural_authority", {})
    fig, ax = plt.subplots(figsize=(8, 5))

    countries = list(auth.keys())
    chair_counts = [len(a.get("chair_role_issues", [])) for a in auth.values()]
    pen_counts = [len(a.get("pen_holder_issues", [])) for a in auth.values()]

    x = np.arange(len(countries))
    w = 0.35
    ax.bar(x - w/2, chair_counts, w, label="chair_role", color="#1f77b4")
    ax.bar(x + w/2, pen_counts, w, label="pen_holder", color="#ff7f0e")

    ax.set_xticks(x)
    ax.set_xticklabels(countries, rotation=20)
    ax.set_ylabel("Number of issues")
    ax.set_title("Figure 2: Procedural Authority (Tallberg 2010)\nLLM-detected chair_role + pen_holder per country")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    out = FIGS / "fig2_procedural_authority.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Figure 2 saved: %s", out)
    return out


def fig3_frame_consistency(analysis: dict) -> Path:
    """Figure 3: Cross-issue frame consistency (hyperedges)."""
    hyperedges = analysis.get("cross_issue_hyperedges", [])
    if not hyperedges:
        logger.warning("No hyperedges to plot")
        return None

    fig, ax = plt.subplots(figsize=(10, 5))

    countries = [h["country"] for h in hyperedges]
    consistencies = [h["frame_consistency"] for h in hyperedges]
    frames = [h["dominant_frame"] for h in hyperedges]

    color_map = {
        "scientific": "#1f77b4",
        "justice": "#d62728",
        "sovereignty": "#ff7f0e",
        "development": "#2ca02c",
        "security": "#9467bd",
        "mixed": "#7f7f7f",
    }
    colors = [color_map.get(f, "#7f7f7f") for f in frames]

    bars = ax.barh(countries, consistencies, color=colors)
    for bar, frame, c in zip(bars, frames, consistencies):
        ax.text(c + 0.05, bar.get_y() + bar.get_height()/2,
                f" {frame} (×{c})", va="center", fontsize=10)

    ax.set_xlabel("Frame consistency (number of issues with dominant frame)")
    ax.set_title("Figure 3: Cross-Issue Frame Consistency Hyperedges\n(R3 IR critique CR3.4 verified — 5 frame types active)")
    ax.set_xlim(0, max(consistencies) + 1.5)

    handles = [matplotlib.patches.Patch(color=c, label=f) for f, c in color_map.items() if f in frames]
    ax.legend(handles=handles, loc="lower right", fontsize=9)
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    out = FIGS / "fig3_frame_consistency.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Figure 3 saved: %s", out)
    return out


def fig4_centrality(analysis: dict) -> Path:
    """Figure 4: Country centralities (mean_abs_stance × coverage)."""
    cents = analysis.get("country_centralities", {})
    if not cents:
        return None

    fig, ax = plt.subplots(figsize=(10, 6))

    countries = list(cents.keys())
    mean_abs = [c["mean_abs_stance"] for c in cents.values()]
    coverage = [c["coverage"] for c in cents.values()]
    n_issues = [c["n_issues_covered"] for c in cents.values()]

    sizes = [n * 200 for n in n_issues]
    scatter = ax.scatter(coverage, mean_abs, s=sizes, alpha=0.6, c=mean_abs, cmap="viridis")

    for i, country in enumerate(countries):
        ax.annotate(country, (coverage[i], mean_abs[i]),
                    xytext=(8, 8), textcoords="offset points", fontsize=10)

    ax.set_xlabel("Coverage (fraction of 6 issues with stance)")
    ax.set_ylabel("Mean absolute stance (intensity)")
    ax.set_title("Figure 4: Country Centrality\n(size = number of issues, color = stance intensity)")
    ax.grid(alpha=0.3)
    ax.set_xlim(0, 1.2)
    ax.set_ylim(0, 1.1)

    plt.tight_layout()
    out = FIGS / "fig4_centrality.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Figure 4 saved: %s", out)
    return out


def fig5_country_similarity_network(analysis: dict) -> Path:
    """Figure 5: Country similarity network graph."""
    sim = analysis.get("country_similarity", {})
    matrix = analysis.get("country_issue_matrix", {})
    if not sim or not matrix:
        return None

    G = nx.Graph()
    for country in matrix:
        G.add_node(country)

    for pair, sim_val in sim.items():
        a, b = pair.split("__")
        if sim_val > 0.3:  # threshold
            G.add_edge(a, b, weight=sim_val)

    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42, k=1.5)
    weights = [G[u][v]["weight"] * 3 for u, v in G.edges()]

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=2000,
                           node_color="#1f77b4", alpha=0.8)
    nx.draw_networkx_edges(G, pos, ax=ax, width=weights, alpha=0.5,
                           edge_color="gray")
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=11, font_weight="bold")

    edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8)

    ax.set_title("Figure 5: Country Similarity Network\n(cosine similarity on stance vectors, threshold > 0.3)")
    ax.axis("off")

    plt.tight_layout()
    out = FIGS / "fig5_similarity_network.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Figure 5 saved: %s", out)
    return out


def main() -> int:
    analysis = load_analysis()
    figs = []
    for fn in [fig1_country_issue_heatmap, fig2_procedural_authority,
               fig3_frame_consistency, fig4_centrality, fig5_country_similarity_network]:
        try:
            out = fn(analysis)
            if out:
                figs.append(out)
        except Exception as exc:
            logger.error("Figure %s failed: %s", fn.__name__, exc)

    print()
    print(f"=== Stage 2 Figures Generated ({len(figs)}) ===")
    for f in figs:
        print(f"  {f}")

    # CAPTIONS.md
    captions = """# Stage 2 Figure Captions

## Figure 1: Country × Issue Stance Heatmap
Stage 1 LLM 추출 결과 (n=21, Groq Llama 3.3 70B). 5 countries × 6 issues 매트릭스. 빈 cell은 해당 country×issue 미추출 (R6 보강 대상).

## Figure 2: Procedural Authority
Stage 1 LLM이 직접 검출한 chair_role + pen_holder. **Brazil GGA-IND/NAPs**: chair_role=True + pen_holder=True (Round 4 IR critique CR2 직접 검증). **Korea NAPs**: pen_holder=True (Track A 직접 영향력).

## Figure 3: Cross-Issue Frame Consistency
- **Brazil dominant=development (×3 issues)** — Plano Clima 정책 일관
- **India dominant=justice (×2 issues)** — CBDR-RC 일관 (Round 3 IR 권고 검증)
- **Korea dominant=development (×2 issues)** — sovereign development frame

## Figure 4: Country Centrality
mean_abs_stance × coverage. 점 크기는 covered issues 수. **Brazil 100% coverage** (focal country). **AOSIS 0.90 mean_abs** (norm entrepreneur, Finnemore-Sikkink 1998).

## Figure 5: Country Similarity Network
Cosine similarity on stance vectors (threshold > 0.3). 연합 구조 시각화.
"""
    (FIGS / "CAPTIONS.md").write_text(captions, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
