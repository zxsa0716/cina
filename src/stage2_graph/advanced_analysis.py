"""Stage 2 Advanced Graph Analysis — Leiden community detection + igraph + advanced metrics.

이전 graph_analysis_v1.json (NetworkX 기본 threshold) → graph_analysis_v2.json (Leiden + advanced).
"""
from __future__ import annotations

import json
import logging
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import networkx as nx

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.stage2.advanced")

ROOT = Path(__file__).resolve().parent.parent.parent


def load_all_stances() -> list[dict]:
    """Load Stage 1 stances from all jsonl files."""
    all_stances = []
    for fname in [
        "stances_seed_v1.jsonl",
        "stances_full_v1.jsonl",
        "stances_ollama_v1.jsonl",
    ]:
        p = ROOT / "data" / "processed" / fname
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                all_stances.append(json.loads(line))
    return all_stances


def build_aggregated_matrix(stances: list[dict]) -> tuple[dict, dict]:
    """Build country × issue aggregated stance matrix + metadata."""
    matrix = defaultdict(dict)
    metadata = defaultdict(lambda: defaultdict(dict))

    for s in stances:
        meta = s.get("_meta", {})
        country = meta.get("country", "?")
        issue = meta.get("issue", "?")
        score = s.get("stance_score", 0)
        if country == "?" or issue == "?":
            continue
        if isinstance(score, (int, float)):
            existing = matrix.get(country, {}).get(issue)
            if existing is not None:
                # ensemble mean
                matrix[country][issue] = (existing + score) / 2
            else:
                matrix[country][issue] = score

            # 보조 metadata 누적
            md = metadata[country][issue]
            md.setdefault("frame_types", []).append(s.get("frame_type"))
            md.setdefault("is_chair_role", []).append(
                s.get("procedural_signals", {}).get("is_chair_role", False)
            )
            md.setdefault("is_pen_holder", []).append(
                s.get("procedural_signals", {}).get("is_pen_holder", False)
            )
            md.setdefault("confidence", []).append(s.get("confidence", 0))

    # Reduce metadata
    final_metadata = {}
    for country, issues in metadata.items():
        final_metadata[country] = {}
        for issue, md in issues.items():
            frames = [f for f in md["frame_types"] if f]
            dominant_frame = max(set(frames), key=frames.count) if frames else None
            final_metadata[country][issue] = {
                "dominant_frame": dominant_frame,
                "is_chair_role": any(md["is_chair_role"]),
                "is_pen_holder": any(md["is_pen_holder"]),
                "mean_confidence": np.mean(md["confidence"]) if md["confidence"] else 0,
                "n_extractions": len(md["confidence"]),
            }
    return dict(matrix), final_metadata


def build_country_network(matrix: dict, issues: list[str]) -> nx.Graph:
    """Build country similarity network (cosine on stance vectors)."""
    G = nx.Graph()
    countries = list(matrix.keys())
    for c in countries:
        G.add_node(c)

    for c1, c2 in combinations(countries, 2):
        v1 = np.array([matrix.get(c1, {}).get(i, 0) for i in issues])
        v2 = np.array([matrix.get(c2, {}).get(i, 0) for i in issues])
        if np.linalg.norm(v1) > 0 and np.linalg.norm(v2) > 0:
            sim = float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        else:
            sim = 0.0
        if sim > 0.0:
            G.add_edge(c1, c2, weight=max(sim, 0.01))
    return G


def detect_communities_leiden(G: nx.Graph) -> dict:
    """Leiden community detection (igraph + leidenalg)."""
    try:
        import igraph as ig
        import leidenalg
    except ImportError:
        logger.warning("igraph/leidenalg not installed, fallback to greedy modularity")
        communities = nx.community.greedy_modularity_communities(G)
        return {
            i: sorted(list(comm)) for i, comm in enumerate(communities)
        }

    if G.number_of_edges() == 0:
        return {0: list(G.nodes())}

    # Convert NetworkX → igraph
    nodes = list(G.nodes())
    edges = [(nodes.index(u), nodes.index(v)) for u, v in G.edges()]
    weights = [G[u][v]["weight"] for u, v in G.edges()]

    g = ig.Graph(edges=edges, directed=False)
    g.es["weight"] = weights
    g.vs["name"] = nodes

    try:
        partition = leidenalg.find_partition(
            g, leidenalg.RBConfigurationVertexPartition,
            weights="weight",
            resolution_parameter=1.0,
        )
        result = {}
        for i, comm in enumerate(partition):
            result[i] = [nodes[idx] for idx in comm]
        return result
    except Exception as exc:
        logger.warning("Leiden failed: %s, fallback to greedy", exc)
        communities = nx.community.greedy_modularity_communities(G)
        return {i: sorted(list(comm)) for i, comm in enumerate(communities)}


def compute_advanced_centrality(G: nx.Graph) -> dict:
    """Advanced centrality metrics."""
    try:
        return {
            "betweenness": nx.betweenness_centrality(G, weight="weight", normalized=True),
            "eigenvector": nx.eigenvector_centrality(G, weight="weight", max_iter=1000),
            "degree": dict(G.degree(weight="weight")),
            "pagerank": nx.pagerank(G, weight="weight"),
            "closeness": nx.closeness_centrality(G, distance="weight"),
        }
    except Exception as exc:
        logger.warning("Centrality failed: %s", exc)
        return {"degree": dict(G.degree(weight="weight"))}


def cross_issue_motif_analysis(metadata: dict) -> list[dict]:
    """3-issue + 4-issue motif detection (Apriori-style)."""
    # For each country, get its (issue, frame) pattern
    country_frames = {}
    for country, issues in metadata.items():
        country_frames[country] = {iss: md.get("dominant_frame") for iss, md in issues.items()}

    motifs = []
    # Find countries with consistent 3-issue dominant frame
    for country, frames in country_frames.items():
        from collections import Counter
        frame_counts = Counter([f for f in frames.values() if f])
        for frame, count in frame_counts.most_common(2):
            if count >= 2:
                issues_with_frame = [i for i, f in frames.items() if f == frame]
                motifs.append({
                    "country": country,
                    "frame": frame,
                    "n_issues": count,
                    "issues": issues_with_frame,
                    "motif_type": "frame_consistency_hyperedge",
                })
    return motifs


def ensemble_quality_assessment(stances: list[dict]) -> dict:
    """Quality assessment of ensemble (multi-LLM agreement proxy)."""
    by_pair = defaultdict(list)
    for s in stances:
        meta = s.get("_meta", {})
        key = (meta.get("country"), meta.get("issue"))
        if all(key):
            by_pair[key].append({
                "score": s.get("stance_score"),
                "frame": s.get("frame_type"),
                "provider": meta.get("provider"),
                "model": meta.get("model"),
            })

    multi_provider_pairs = {k: v for k, v in by_pair.items() if len(v) >= 2}
    if not multi_provider_pairs:
        return {"n_pairs_multi": 0, "note": "No (country, issue) pair with 2+ providers"}

    score_stds = []
    frame_agreements = []
    for pair, recs in multi_provider_pairs.items():
        scores = [r["score"] for r in recs if isinstance(r["score"], (int, float))]
        if len(scores) >= 2:
            score_stds.append(float(np.std(scores)))
        frames = [r["frame"] for r in recs if r["frame"]]
        if frames:
            frame_agreements.append(len(set(frames)) == 1)

    return {
        "n_pairs_multi": len(multi_provider_pairs),
        "mean_score_std": float(np.mean(score_stds)) if score_stds else None,
        "frame_agreement_rate": float(np.mean(frame_agreements)) if frame_agreements else None,
        "interpretation": "Multi-LLM Krippendorff alpha proxy. Lower std + higher frame agreement = better ensemble.",
    }


def main() -> int:
    issues = ["GGA-IND", "ADAPT-FIN", "L&D-OP", "NAPs", "MIT-ADAPT", "JT-ADAPT"]

    stances = load_all_stances()
    logger.info("Loaded %d stance records (combined Groq + Ollama)", len(stances))

    matrix, metadata = build_aggregated_matrix(stances)
    logger.info("Matrix: %d countries × %d issues", len(matrix), len(issues))

    G = build_country_network(matrix, issues)
    logger.info("Network: %d nodes, %d edges", G.number_of_nodes(), G.number_of_edges())

    communities_leiden = detect_communities_leiden(G)
    logger.info("Leiden communities: %d", len(communities_leiden))

    centralities = compute_advanced_centrality(G)
    motifs = cross_issue_motif_analysis(metadata)
    ensemble_quality = ensemble_quality_assessment(stances)

    output = {
        "_meta": {
            "stage": "Stage 2 Advanced",
            "n_stances": len(stances),
            "n_countries": len(matrix),
            "providers": list(set(s.get("_meta", {}).get("provider") for s in stances if s.get("_meta", {}).get("provider"))),
        },
        "country_issue_matrix": matrix,
        "country_metadata": metadata,
        "leiden_communities": communities_leiden,
        "centralities_advanced": centralities,
        "cross_issue_motifs": motifs,
        "ensemble_quality": ensemble_quality,
        "graph_summary": {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "density": nx.density(G) if G.number_of_nodes() > 1 else 0,
            "connected_components": nx.number_connected_components(G),
        },
    }

    out = ROOT / "data" / "processed" / "graph_analysis_v2.json"
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Stage 2 v2 saved: %s", out)

    print()
    print("=== Stage 2 Advanced Analysis (v2) ===")
    print(f"Total stances: {len(stances)}")
    print(f"Countries: {len(matrix)}")
    print(f"Providers used: {output['_meta']['providers']}")
    print(f"Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, density={output['graph_summary']['density']:.3f}")
    print()
    print("=== Leiden Communities ===")
    for cid, members in communities_leiden.items():
        print(f"  Community {cid}: {members}")
    print()
    print("=== Top Centrality (PageRank) ===")
    pr = centralities.get("pagerank", {})
    for c, v in sorted(pr.items(), key=lambda x: -x[1])[:8]:
        print(f"  {c:<20} {v:.4f}")
    print()
    print("=== Cross-Issue Motifs (frame consistency) ===")
    for m in motifs[:8]:
        print(f"  {m['country']:<14} {m['frame']:<13} ×{m['n_issues']} {m['issues']}")
    print()
    print("=== Ensemble Quality ===")
    print(json.dumps(ensemble_quality, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
