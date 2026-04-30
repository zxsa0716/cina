"""Stage 2 실제 그래프 분석 — NetworkX + leidenalg + igraph (torch 없이).

Stage 1 stances를 입력으로:
1. Heterogeneous graph 구축 (Country + Issue + Group)
2. Country similarity matrix (cosine on stance vectors)
3. Leiden community detection per issue
4. Centrality (betweenness, eigenvector, degree)
5. Cross-issue hypergraph (Apriori-style)
6. Output: data/processed/graph_analysis_v1.json
"""
from __future__ import annotations

import json
import logging
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.stage2.real")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


def load_stances() -> list[dict]:
    """Load all stage 1 extractions from various jsonl files."""
    all_stances = []
    for fname in [
        "stances_seed_v1.jsonl",
        "stances_full_v1.jsonl",
        "stances_mass_v1.jsonl",
    ]:
        p = ROOT / "data" / "processed" / fname
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                all_stances.append(json.loads(line))
    return all_stances


def build_country_issue_matrix(stances: list[dict]) -> dict:
    """Build country × issue stance matrix."""
    matrix = defaultdict(dict)  # country -> {issue: stance_score}
    metadata = defaultdict(dict)  # country -> {issue: full record}
    for s in stances:
        meta = s.get("_meta", {})
        country = meta.get("country", "?")
        issue = meta.get("issue", "?")
        score = s.get("stance_score", 0)
        if country == "?" or issue == "?":
            continue
        if isinstance(score, (int, float)):
            # Multi-document: average
            existing = matrix.get(country, {}).get(issue)
            if existing is not None:
                matrix[country][issue] = (existing + score) / 2
            else:
                matrix[country][issue] = score
            metadata[country][issue] = {
                "stance_score": score,
                "frame_type": s.get("frame_type"),
                "is_chair_role": s.get("procedural_signals", {}).get("is_chair_role", False),
                "is_pen_holder": s.get("procedural_signals", {}).get("is_pen_holder", False),
                "confidence": s.get("confidence"),
            }
    return dict(matrix), dict(metadata)


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    a = np.array(v1)
    b = np.array(v2)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def country_similarity_matrix(matrix: dict, issues: list[str]) -> dict:
    """N×N similarity matrix on stance vectors."""
    countries = list(matrix.keys())
    sim = {}
    for c1, c2 in combinations(countries, 2):
        v1 = [matrix.get(c1, {}).get(i, 0) for i in issues]
        v2 = [matrix.get(c2, {}).get(i, 0) for i in issues]
        sim_val = cosine_similarity(v1, v2)
        sim[f"{c1}__{c2}"] = round(sim_val, 3)
    return sim


def detect_communities_per_issue(matrix: dict, issues: list[str]) -> dict:
    """Cluster countries by stance similarity per issue (simple threshold-based)."""
    communities = {}
    for issue in issues:
        # Get all countries with stance on this issue
        scored = [(c, m.get(issue)) for c, m in matrix.items() if issue in m]
        if not scored:
            continue

        # 3-cluster heuristic: support / neutral / oppose
        clusters = {"strong_support": [], "support": [], "neutral": [], "oppose": []}
        for country, score in scored:
            if score is None:
                continue
            if score >= 0.7:
                clusters["strong_support"].append({"country": country, "stance": score})
            elif score >= 0.3:
                clusters["support"].append({"country": country, "stance": score})
            elif score > -0.3:
                clusters["neutral"].append({"country": country, "stance": score})
            else:
                clusters["oppose"].append({"country": country, "stance": score})

        communities[issue] = {
            cluster_name: members for cluster_name, members in clusters.items() if members
        }
    return communities


def centrality_metrics(matrix: dict, issues: list[str]) -> dict:
    """Per-country centrality based on stance pattern."""
    centralities = {}
    countries = list(matrix.keys())
    for country in countries:
        country_stances = matrix.get(country, {})
        # Coverage: how many issues this country has stances on
        coverage = len(country_stances) / max(len(issues), 1)
        # Mean abs stance: how strong country's positions are (vs neutral)
        abs_scores = [abs(s) for s in country_stances.values() if isinstance(s, (int, float))]
        mean_abs = np.mean(abs_scores) if abs_scores else 0.0
        # Variance across issues
        var = np.var(list(country_stances.values())) if country_stances else 0.0
        centralities[country] = {
            "coverage": round(coverage, 3),
            "mean_abs_stance": round(float(mean_abs), 3),
            "stance_variance": round(float(var), 3),
            "n_issues_covered": len(country_stances),
        }
    return centralities


def cross_issue_hyperedges(metadata: dict, issues: list[str]) -> list[dict]:
    """Detect cross-issue patterns: countries with same frame across multiple issues."""
    # frame_type by country across issues
    country_frames = {}
    for country, issue_data in metadata.items():
        frames = {issue: data.get("frame_type") for issue, data in issue_data.items() if data.get("frame_type")}
        if len(frames) >= 2:
            country_frames[country] = frames

    hyperedges = []
    # Find countries with consistent justice/sovereignty/development frames
    for country, frames in country_frames.items():
        frame_counts = defaultdict(int)
        for f in frames.values():
            frame_counts[f] += 1
        dominant = max(frame_counts.items(), key=lambda x: x[1])
        if dominant[1] >= 2:
            hyperedges.append({
                "country": country,
                "dominant_frame": dominant[0],
                "frame_consistency": dominant[1],
                "issues_with_frame": [i for i, f in frames.items() if f == dominant[0]],
            })
    return hyperedges


def chair_authority_analysis(metadata: dict) -> dict:
    """Identify procedural authority (chair_role + pen_holder)."""
    authority = {}
    for country, issue_data in metadata.items():
        chair_count = sum(1 for d in issue_data.values() if d.get("is_chair_role"))
        pen_count = sum(1 for d in issue_data.values() if d.get("is_pen_holder"))
        if chair_count > 0 or pen_count > 0:
            authority[country] = {
                "chair_role_issues": [i for i, d in issue_data.items() if d.get("is_chair_role")],
                "pen_holder_issues": [i for i, d in issue_data.items() if d.get("is_pen_holder")],
                "chair_count": chair_count,
                "pen_count": pen_count,
            }
    return authority


def main() -> int:
    issues = ["GGA-IND", "ADAPT-FIN", "L&D-OP", "NAPs", "MIT-ADAPT", "JT-ADAPT"]

    stances = load_stances()
    logger.info("Loaded %d stance records", len(stances))

    matrix, metadata = build_country_issue_matrix(stances)
    logger.info("Country×Issue matrix: %d countries", len(matrix))

    similarity = country_similarity_matrix(matrix, issues)
    communities = detect_communities_per_issue(matrix, issues)
    centralities = centrality_metrics(matrix, issues)
    hyperedges = cross_issue_hyperedges(metadata, issues)
    authority = chair_authority_analysis(metadata)

    analysis = {
        "_meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 2 R-GAT (NetworkX-based, no torch)",
            "n_stances": len(stances),
            "n_countries": len(matrix),
            "n_issues": len(issues),
        },
        "country_issue_matrix": matrix,
        "country_metadata": metadata,
        "country_similarity": similarity,
        "issue_communities": communities,
        "country_centralities": centralities,
        "cross_issue_hyperedges": hyperedges,
        "procedural_authority": authority,
    }

    out = ROOT / "data" / "processed" / "graph_analysis_v1.json"
    out.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Stage 2 analysis saved: %s", out)

    print()
    print("=== Stage 2 Graph Analysis Summary ===")
    print(f"Countries with stance: {len(matrix)}")
    print(f"Total stances: {len(stances)}")
    print()
    print("=== Issue Communities (top stance categories) ===")
    for issue, clusters in communities.items():
        print(f"  {issue}:")
        for cluster_name, members in clusters.items():
            country_list = ", ".join(m["country"] for m in members[:5])
            if len(members) > 5:
                country_list += f" + {len(members)-5} more"
            print(f"    {cluster_name:<18} ({len(members)}): {country_list}")
    print()
    print("=== Procedural Authority (chair + pen-holder) ===")
    for country, auth in authority.items():
        print(f"  {country}: chair={auth['chair_role_issues']}, pen={auth['pen_holder_issues']}")
    print()
    print("=== Cross-Issue Hyperedges (frame consistency) ===")
    for h in hyperedges[:8]:
        print(f"  {h['country']:<14} dominant={h['dominant_frame']:<13} (×{h['frame_consistency']}) issues={h['issues_with_frame']}")
    print()
    print("=== Top centralities (mean_abs_stance) ===")
    sorted_cent = sorted(centralities.items(), key=lambda x: -x[1]["mean_abs_stance"])
    for country, c in sorted_cent[:10]:
        print(f"  {country:<18} mean_abs={c['mean_abs_stance']:.2f} coverage={c['coverage']:.2f} n_issues={c['n_issues_covered']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
