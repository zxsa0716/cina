"""
Cross-LLM consistency framework for CINA Stage 1.

Computes Krippendorff's α treating each LLM provider (Gemini, Groq, Ollama,
OpenRouter, Anthropic) as an independent coder, providing a reliability lower
bound that is *partially decoupled from shared-model bias* — since the five
LLMs were trained on different data and RLHF pipelines.

This implements advancement E2 in METHODOLOGY_ADVANCEMENT_ROADMAP.md.

Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
License: MIT
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Krippendorff's α (interval-level)
# ---------------------------------------------------------------------------

def krippendorff_alpha_interval(ratings: list[list[Optional[float]]]) -> float:
    """Compute Krippendorff's α for interval data.

    Args:
        ratings: list of length n_units, each a list of length n_coders
                 with None for missing values.

    Returns:
        α in (-∞, 1], where α=1 perfect agreement, α=0 chance, α<0 systematic
        disagreement.

    Reference:
        Krippendorff, K. (2004). Content Analysis: An Introduction to Its
        Methodology. Sage. Equations 11.6-11.10.
    """
    # Build coincidence matrix and pair-counts
    pair_counts = defaultdict(float)
    n_pairable = 0

    for unit in ratings:
        observed = [v for v in unit if v is not None]
        m = len(observed)
        if m < 2:
            continue
        weight = 1.0 / (m - 1)
        for i in range(m):
            for j in range(m):
                if i == j:
                    continue
                pair_counts[(observed[i], observed[j])] += weight
        n_pairable += m

    if n_pairable < 2 or sum(pair_counts.values()) < 1e-9:
        return float("nan")

    # Observed disagreement (squared difference for interval)
    D_o = sum(p * (a - b) ** 2 for (a, b), p in pair_counts.items())
    D_o /= sum(pair_counts.values())

    # Expected disagreement: pool of all observed values
    pool = []
    for unit in ratings:
        for v in unit:
            if v is not None:
                pool.append(v)

    n = len(pool)
    if n < 2:
        return float("nan")

    D_e = 0.0
    pair_total = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            D_e += (pool[i] - pool[j]) ** 2
            pair_total += 1
    D_e /= pair_total if pair_total else 1

    if D_e < 1e-9:
        return float("nan")

    return 1.0 - (D_o / D_e)


# ---------------------------------------------------------------------------
# LLM-specific bias estimation (Platt-like simple linear adjustment)
# ---------------------------------------------------------------------------

@dataclass
class LLMBiasReport:
    """Per-LLM systematic bias diagnosis."""

    llm: str
    mean_offset: float            # mean(LLM) - mean(others)
    std_ratio: float              # std(LLM) / std(others)
    pearson_r_to_consensus: float
    n_pairs: int
    bias_corrected_alpha: float


def diagnose_llm_bias(stance_by_llm: dict[str, list[Optional[float]]],
                       pair_ids: list[str]) -> tuple[float, list[LLMBiasReport]]:
    """For each LLM, estimate systematic offset vs the mean of the other LLMs,
    then return the Krippendorff α before and after a per-LLM linear correction
    (mean-centering).

    Args:
        stance_by_llm: {llm_name: [score_for_pair_1, ...]} (None for missing)
        pair_ids: list of (country, issue) identifier strings

    Returns:
        (raw_alpha, list of LLMBiasReport)
    """
    llms = sorted(stance_by_llm.keys())
    n_llms = len(llms)
    n_pairs = len(pair_ids)
    if n_llms < 2:
        raise ValueError("Need at least 2 LLMs for cross-LLM α")

    # Build matrix [n_pairs, n_llms]
    matrix = []
    for k in range(n_pairs):
        row = [stance_by_llm[llm][k] for llm in llms]
        matrix.append(row)

    raw_alpha = krippendorff_alpha_interval(matrix)

    # Per-LLM bias diagnosis
    reports = []
    bias_corrected_matrix = [list(row) for row in matrix]

    for li, llm in enumerate(llms):
        own = [matrix[k][li] for k in range(n_pairs) if matrix[k][li] is not None]
        if not own:
            continue

        others_means = []
        own_paired = []
        for k in range(n_pairs):
            if matrix[k][li] is None:
                continue
            other_vals = [matrix[k][j] for j in range(n_llms)
                          if j != li and matrix[k][j] is not None]
            if not other_vals:
                continue
            others_means.append(sum(other_vals) / len(other_vals))
            own_paired.append(matrix[k][li])

        if len(own_paired) < 3:
            continue

        mean_own = sum(own_paired) / len(own_paired)
        mean_others = sum(others_means) / len(others_means)
        offset = mean_own - mean_others

        var_own = sum((v - mean_own) ** 2 for v in own_paired) / max(1, len(own_paired) - 1)
        var_others = sum((v - mean_others) ** 2 for v in others_means) / max(1, len(others_means) - 1)
        std_ratio = math.sqrt(var_own) / max(math.sqrt(var_others), 1e-9)

        # Pearson r between LLM and consensus
        cov = sum((own_paired[i] - mean_own) * (others_means[i] - mean_others)
                  for i in range(len(own_paired)))
        denom = math.sqrt(sum((v - mean_own) ** 2 for v in own_paired) *
                          sum((v - mean_others) ** 2 for v in others_means))
        r = cov / denom if denom > 1e-9 else float("nan")

        # Apply mean-centering correction to bias-corrected matrix
        for k in range(n_pairs):
            if bias_corrected_matrix[k][li] is not None:
                bias_corrected_matrix[k][li] -= offset

        reports.append(LLMBiasReport(
            llm=llm,
            mean_offset=round(offset, 4),
            std_ratio=round(std_ratio, 4),
            pearson_r_to_consensus=round(r, 4) if not math.isnan(r) else None,
            n_pairs=len(own_paired),
            bias_corrected_alpha=0.0  # filled below
        ))

    # Compute α on bias-corrected matrix
    corrected_alpha = krippendorff_alpha_interval(bias_corrected_matrix)
    for r in reports:
        r.bias_corrected_alpha = round(corrected_alpha, 4)

    return raw_alpha, reports


# ---------------------------------------------------------------------------
# Disagreement-driven active learning sampler
# ---------------------------------------------------------------------------

def disagreement_priority_queue(stance_by_llm: dict[str, list[Optional[float]]],
                                  pair_ids: list[str],
                                  k_top: int = 20) -> list[dict]:
    """Identify the (country, issue) pairs where LLMs disagree most strongly,
    for prioritised human-coder labelling.

    Returns a list of dicts ranked by disagreement, each containing:
      pair_id, std, range, n_llms_agreeing, ...
    """
    llms = sorted(stance_by_llm.keys())
    n_pairs = len(pair_ids)

    queue = []
    for k in range(n_pairs):
        vals = [stance_by_llm[llm][k] for llm in llms if stance_by_llm[llm][k] is not None]
        if len(vals) < 2:
            continue
        mean_v = sum(vals) / len(vals)
        std_v = (sum((v - mean_v) ** 2 for v in vals) / max(1, len(vals) - 1)) ** 0.5
        range_v = max(vals) - min(vals)

        # Count LLMs agreeing on sign
        n_pos = sum(1 for v in vals if v > 0.1)
        n_neg = sum(1 for v in vals if v < -0.1)
        sign_agreement = max(n_pos, n_neg) / len(vals)

        queue.append({
            "pair_id": pair_ids[k],
            "n_llms": len(vals),
            "std": round(std_v, 4),
            "range": round(range_v, 4),
            "mean": round(mean_v, 4),
            "sign_agreement": round(sign_agreement, 3),
            "values_per_llm": {llms[j]: stance_by_llm[llms[j]][k]
                               for j in range(len(llms))
                               if stance_by_llm[llms[j]][k] is not None}
        })

    queue.sort(key=lambda x: x["std"], reverse=True)
    return queue[:k_top]


# ---------------------------------------------------------------------------
# CLI / demo with synthetic CINA-shaped data
# ---------------------------------------------------------------------------

def build_synthetic_cross_llm_data(seed: int = 42) -> tuple[dict, list[str]]:
    """Build a CINA-shaped 5-LLM × 78-pair dataset for demo runs.

    Each LLM has a small systematic bias and per-pair noise added to a
    ground-truth stance derived from the public sample.
    """
    import random
    random.seed(seed)

    countries = ["Brazil", "EU", "USA", "China", "India", "AOSIS",
                 "Korea", "Saudi", "Japan", "AILAC", "AGN", "LMDC", "Multi"]
    issues = ["GGA-IND", "GGA-MOI", "NAPs", "JT-ADAPT", "L&D-OP", "FINANCE-ADAPT"]

    truth = {
        "Brazil": [0.95, 0.78, 0.88, 0.92, 0.55, 0.70],
        "EU": [0.55, 0.65, 0.72, 0.60, 0.45, 0.58],
        "USA": [0.30, 0.20, 0.50, 0.40, -0.20, 0.25],
        "China": [-0.30, 0.40, 0.55, 0.50, 0.65, 0.70],
        "India": [-0.15, 0.55, 0.60, 0.45, 0.85, 0.90],
        "AOSIS": [0.85, 0.90, 0.78, 0.65, 0.95, 0.92],
        "Korea": [0.65, 0.62, 0.75, 0.78, 0.39, 0.55],
        "Saudi": [-0.55, -0.65, 0.20, -0.30, 0.10, 0.40],
        "Japan": [0.45, 0.50, 0.62, 0.55, 0.30, 0.48],
        "AILAC": [0.85, 0.85, 0.80, 0.70, 0.85, 0.85],
        "AGN": [0.65, 0.70, 0.72, 0.62, 0.75, 0.70],
        "LMDC": [-0.20, 0.50, 0.55, 0.40, 0.55, 0.60],
        "Multi": [0.75, 0.65, 0.70, 0.60, 0.55, 0.65]
    }

    pair_ids = [f"{c}|{i}" for c in countries for i in issues]

    # Per-LLM bias profile (calibration source: empirically observed in our data)
    # gemini, groq, ollama: systematic underestimate; anthropic: slight over;
    # openrouter: noisy
    biases = {
        "gemini": (-0.05, 0.06),       # (offset, noise std)
        "groq": (-0.08, 0.07),
        "ollama_qwen": (-0.18, 0.12),  # known: qwen2.5:3b underestimates ~0.2
        "openrouter_pool": (0.02, 0.10),
        "anthropic": (0.04, 0.05)
    }

    stance_by_llm = {llm: [] for llm in biases}
    for c in countries:
        for ii in range(len(issues)):
            t = truth[c][ii]
            for llm, (offset, noise) in biases.items():
                v = t + offset + random.gauss(0, noise)
                v = max(-1.0, min(1.0, v))
                # 5% missing rate
                if random.random() < 0.05:
                    stance_by_llm[llm].append(None)
                else:
                    stance_by_llm[llm].append(round(v, 3))

    return stance_by_llm, pair_ids


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Cross-LLM consistency analysis")
    ap.add_argument("--output", default="data/processed/cross_llm_agreement.json")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--top_k", type=int, default=20)
    args = ap.parse_args()

    stance_by_llm, pair_ids = build_synthetic_cross_llm_data(seed=args.seed)

    raw_alpha, bias_reports = diagnose_llm_bias(stance_by_llm, pair_ids)
    queue = disagreement_priority_queue(stance_by_llm, pair_ids, k_top=args.top_k)

    output = {
        "n_llms": len(stance_by_llm),
        "n_pairs": len(pair_ids),
        "raw_krippendorff_alpha": round(raw_alpha, 4),
        "bias_corrected_krippendorff_alpha": (
            round(bias_reports[0].bias_corrected_alpha, 4)
            if bias_reports else None
        ),
        "per_llm_bias": [r.__dict__ for r in bias_reports],
        "disagreement_priority_queue": queue
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Cross-LLM consistency analysis complete.")
    print(f"  Raw α               = {output['raw_krippendorff_alpha']}")
    print(f"  Bias-corrected α    = {output['bias_corrected_krippendorff_alpha']}")
    print(f"  N LLMs              = {output['n_llms']}")
    print(f"  N pairs             = {output['n_pairs']}")
    print(f"  Per-LLM offsets:")
    for r in bias_reports:
        print(f"    {r.llm:>20s}: offset {r.mean_offset:+.3f}, "
              f"std_ratio {r.std_ratio:.2f}, r {r.pearson_r_to_consensus:.3f}")
    print(f"\nResults saved to {out_path}")
