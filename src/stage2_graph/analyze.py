"""Community detection, centrality, cross-issue hypergraph analysis.

docs/05_stage2_graph_analysis.md §3 참조.
"""
from __future__ import annotations

from itertools import combinations
from typing import Iterable

import igraph as ig
import leidenalg
import networkx as nx
import numpy as np
from sklearn.neighbors import kneighbors_graph

from ..schemas import (
    BridgeCountry,
    CommunityCluster,
    CrossIssueHyperedge,
    EpistemicDivergence,
    IssueAnalysis,
)


# ---------------------------------------------------------------------------
# Community detection
# ---------------------------------------------------------------------------
def detect_communities(
    embeddings: np.ndarray,
    country_labels: list[str],
    k: int = 5,
    gamma: float = 1.0,
) -> list[CommunityCluster]:
    """Leiden community detection on k-NN graph of country embeddings."""
    sparse_knn = kneighbors_graph(embeddings, n_neighbors=k, mode="distance")
    dense = 1.0 / (sparse_knn.toarray() + 1e-6)
    np.fill_diagonal(dense, 0)

    g = ig.Graph.Weighted_Adjacency(dense.tolist(), mode="undirected")
    partition = leidenalg.find_partition(
        g,
        leidenalg.RBConfigurationVertexPartition,
        resolution_parameter=gamma,
    )
    membership = partition.membership

    clusters = {}
    for idx, cid in enumerate(membership):
        clusters.setdefault(cid, []).append(idx)

    results = []
    for cid, member_idx in sorted(clusters.items()):
        countries = [country_labels[i] for i in member_idx]
        centroid = embeddings[member_idx].mean(axis=0)
        agreement = float(
            np.mean(
                [
                    np.dot(embeddings[i], centroid)
                    / (np.linalg.norm(embeddings[i]) * np.linalg.norm(centroid) + 1e-8)
                    for i in member_idx
                ]
            )
        )
        results.append(
            CommunityCluster(
                cluster_id=cid,
                countries=countries,
                centroid_stance=float(centroid.mean()),
                within_cluster_agreement=agreement,
            )
        )
    return results


# ---------------------------------------------------------------------------
# Centrality
# ---------------------------------------------------------------------------
def compute_centralities(
    adjacency: np.ndarray,
    country_labels: list[str],
) -> dict[str, dict[str, float]]:
    G = nx.from_numpy_array(adjacency)
    mapping = {i: label for i, label in enumerate(country_labels)}
    G = nx.relabel_nodes(G, mapping)
    try:
        eig = nx.eigenvector_centrality(G, weight="weight", max_iter=1000)
    except nx.PowerIterationFailedConvergence:
        eig = {n: 0.0 for n in G.nodes}
    return {
        "betweenness": nx.betweenness_centrality(G, weight="weight", normalized=True),
        "eigenvector": eig,
        "degree": dict(G.degree(weight="weight")),
    }


def top_bridges(
    centralities: dict[str, dict[str, float]],
    n: int = 5,
) -> list[BridgeCountry]:
    bw = centralities["betweenness"]
    top = sorted(bw.items(), key=lambda kv: kv[1], reverse=True)[:n]
    return [BridgeCountry(country=c, betweenness=float(v)) for c, v in top]


# ---------------------------------------------------------------------------
# Cross-Issue Hypergraph (Issue Linkage)
# ---------------------------------------------------------------------------
def build_flex_matrix(
    stances: list[dict],
    country_labels: list[str],
    issue_labels: list[str],
) -> np.ndarray:
    """N x I binary matrix: 1 if country shows flexibility on issue."""
    country_idx = {c: i for i, c in enumerate(country_labels)}
    issue_idx = {s: i for i, s in enumerate(issue_labels)}
    F = np.zeros((len(country_labels), len(issue_labels)), dtype=int)
    for s in stances:
        ci = country_idx.get(s["country"])
        ii = issue_idx.get(s["issue"])
        if ci is None or ii is None:
            continue
        if s.get("flexibility_signals"):
            F[ci, ii] = 1
    return F


def detect_linkage_hyperedges(
    flex_matrix: np.ndarray,
    country_labels: list[str],
    issue_labels: list[str],
    min_support: float = 0.2,
    min_issues: int = 2,
    max_issues: int = 4,
) -> list[CrossIssueHyperedge]:
    """Apriori-style motif mining."""
    n_countries, n_issues = flex_matrix.shape
    hyperedges = []
    for size in range(min_issues, max_issues + 1):
        for combo in combinations(range(n_issues), size):
            jointly = flex_matrix[:, list(combo)].all(axis=1)
            support = jointly.mean()
            if support >= min_support:
                countries = [country_labels[i] for i in jointly.nonzero()[0]]
                pattern = _classify_pattern(countries, combo)
                hyperedges.append(
                    CrossIssueHyperedge(
                        issues=[issue_labels[i] for i in combo],
                        countries=countries,
                        support=float(support),
                        pattern=pattern,
                    )
                )
    return hyperedges


def _classify_pattern(countries: Iterable[str], combo: tuple[int, ...]) -> str:
    """Stub: 실제로는 stance 부호 패턴을 분석."""
    return "linked_concession"


# ---------------------------------------------------------------------------
# Epistemic Divergence
# ---------------------------------------------------------------------------
def epistemic_divergence_score(
    stances_for_issue: list[dict],
    country_power: dict[str, float] | None = None,
) -> EpistemicDivergence:
    """전문가 원안 vs 정치적 재작성 divergence 가능성."""
    country_power = country_power or {}
    aligned = sum(
        1 for s in stances_for_issue
        if s.get("epistemic_alignment", {}).get("aligns_with_expert_proposal") == "full"
    )
    divergent_records = [
        s for s in stances_for_issue
        if s.get("epistemic_alignment", {}).get("aligns_with_expert_proposal") == "divergent"
    ]
    divergent = len(divergent_records)
    political_weight = sum(country_power.get(s["country"], 1.0) for s in divergent_records)

    risk = political_weight / (aligned + political_weight + 1e-6)
    return EpistemicDivergence(
        predicted_divergence_risk=float(risk),
        high_political_weight_dissenters=[s["country"] for s in divergent_records],
        interpretation=f"aligned={aligned}, divergent={divergent}, political_weight={political_weight:.2f}",
    )


# ---------------------------------------------------------------------------
# Per-issue pipeline
# ---------------------------------------------------------------------------
def analyze_issue(
    issue_code: str,
    country_embeddings: np.ndarray,
    country_labels: list[str],
    adjacency: np.ndarray,
    knn_k: int = 5,
    leiden_gamma: float = 1.0,
) -> IssueAnalysis:
    clusters = detect_communities(country_embeddings, country_labels, k=knn_k, gamma=leiden_gamma)
    centralities = compute_centralities(adjacency, country_labels)
    bridges = top_bridges(centralities, n=5)
    attention_nodes = [
        {"country": c, "attention_sum": float(v)}
        for c, v in sorted(centralities["eigenvector"].items(), key=lambda kv: kv[1], reverse=True)[:5]
    ]
    return IssueAnalysis(
        issue_code=issue_code,
        communities=clusters,
        bridge_countries=bridges,
        top_attention_nodes=attention_nodes,
    )
