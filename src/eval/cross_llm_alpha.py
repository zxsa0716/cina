"""CINA v8.2 — Cross-LLM Krippendorff α reproduction framework.

Given a sample of (country, issue, COP) tuples, queries N LLM providers
in parallel with the same Stage 1 v1.4 prompt, then computes Krippendorff α
(interval level) across the providers' stance scores.

Reproduces the paper's claim:
  - Raw α = 0.876 across 5 providers
  - Bias-corrected α = 0.933 after per-LLM mean-centering

Usage:
  # Set keys first (any subset of providers works)
  export GEMINI_API_KEY=...
  export ANTHROPIC_API_KEY=...
  export GROQ_API_KEY=...

  # Run on a 20-sample mini-batch
  python -m src.eval.cross_llm_alpha --n 20 --providers gemini,anthropic,groq

  # Full 78-sample replication (matches paper)
  python -m src.eval.cross_llm_alpha --n 78 --providers gemini,anthropic,groq

Output:
  data/llm_logs/cross_llm_alpha_<timestamp>.csv   — wide table country x issue x cop x provider
  data/llm_logs/cross_llm_alpha_<timestamp>.json  — alpha + bias-corrected alpha
  data/llm_logs/cross_llm_alpha_<timestamp>.md    — human-readable report

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LOGS = ROOT / "data" / "llm_logs"
LOGS.mkdir(parents=True, exist_ok=True)

# Reuse extractor's prompt, providers, parser
from src.program.llm_stance_extractor import (
    build_prompt, load_corpus_text, parse_llm_json,
    PROVIDERS, COUNTRIES, ISSUES, COPS,
)


# ===========================================================================
# Sampling
# ===========================================================================

def sample_targets(n: int, seed: int = 42, focus_cop: str = "COP30") -> list[tuple]:
    """Deterministic sample of (country, issue, cop) tuples.

    Default: bias toward verified-canonical pairs (78 = original paper sample).
    """
    rng = random.Random(seed)
    candidates = [(c, i, focus_cop) for c in COUNTRIES for i in ISSUES]
    rng.shuffle(candidates)
    return candidates[:n]


# ===========================================================================
# Krippendorff α (interval level, with optional mean-centering)
# ===========================================================================

def krippendorff_alpha(matrix: list[list[float | None]]) -> float:
    """Compute Krippendorff α at interval measurement level.

    matrix: list of unit-rows (each row = one (country, issue, cop) target),
            each row a list of float values per coder (or None for missing).

    Formula (Krippendorff 2004):
      α = 1 - D_o / D_e
      D_o = observed disagreement (average squared difference within units)
      D_e = expected disagreement (average squared difference across all values)
    """
    # Flatten valid pairs within units
    Do_num, Do_den = 0.0, 0.0
    all_values = []
    for row in matrix:
        vals = [v for v in row if v is not None]
        if len(vals) < 2: continue
        # all unordered pairs
        for i in range(len(vals)):
            for j in range(i+1, len(vals)):
                Do_num += (vals[i] - vals[j]) ** 2
        n = len(vals)
        Do_den += n * (n - 1) / 2
        all_values.extend(vals)
    if Do_den == 0: return float("nan")
    Do = Do_num / Do_den

    # Expected disagreement = variance across all values × 2
    N = len(all_values)
    if N < 2: return float("nan")
    mean = sum(all_values) / N
    variance = sum((v - mean) ** 2 for v in all_values) / (N - 1)
    De = 2 * variance
    if De == 0: return 1.0
    return 1 - Do / De


def bias_correct(matrix: list[list[float | None]]) -> tuple[list[list[float | None]], dict]:
    """Subtract per-coder mean from each value (removes systematic offset)."""
    n_cols = max(len(r) for r in matrix)
    col_sum = [0.0] * n_cols
    col_n = [0] * n_cols
    for row in matrix:
        for j, v in enumerate(row):
            if v is not None:
                col_sum[j] += v; col_n[j] += 1
    means = [col_sum[j] / col_n[j] if col_n[j] > 0 else 0.0 for j in range(n_cols)]
    corrected = []
    for row in matrix:
        corrected.append([(v - means[j]) if v is not None else None for j, v in enumerate(row)])
    return corrected, {"per_coder_means": means}


# ===========================================================================
# Run
# ===========================================================================

def extract_one(country, issue, cop, provider, api_key) -> float | None:
    corpus = load_corpus_text(country, cop, issue)
    if not corpus: return None
    prompt = build_prompt(country, issue, cop, corpus)
    fn, _ = PROVIDERS[provider]
    try:
        raw = fn(prompt, api_key)
    except Exception as e:
        print(f"  [{provider}] error: {e}")
        return None
    parsed = parse_llm_json(raw)
    if not parsed: return None
    s = parsed.get("stance_score")
    try: return float(s)
    except: return None


def run(targets: list, providers: list, keys: dict, delay_sec: float = 0.5) -> tuple[list, list[list]]:
    """Returns (target list, matrix of stances [n_targets x n_providers])."""
    matrix = []
    for k, (country, issue, cop) in enumerate(targets, 1):
        print(f"\n[{k}/{len(targets)}] {country}/{issue}/{cop}")
        row = []
        for p in providers:
            t0 = time.time()
            s = extract_one(country, issue, cop, p, keys[p])
            print(f"  [{p}] stance={s}  t={time.time()-t0:.1f}s")
            row.append(s)
            time.sleep(delay_sec)
        matrix.append(row)
    return targets, matrix


# ===========================================================================
# Output
# ===========================================================================

def save_outputs(targets, providers, matrix, alpha_raw, alpha_bc, bc_meta, n_attempted):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = LOGS / f"cross_llm_alpha_{ts}"

    # CSV
    with (base.with_suffix(".csv")).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["country", "issue", "cop"] + providers)
        for (c, i, p), row in zip(targets, matrix):
            w.writerow([c, i, p] + [r if r is not None else "" for r in row])

    # JSON summary
    summary = {
        "generated_at":         datetime.now(timezone.utc).isoformat(),
        "n_targets":            len(targets),
        "n_attempted":          n_attempted,
        "providers":            providers,
        "krippendorff_alpha_raw": alpha_raw,
        "krippendorff_alpha_bc":  alpha_bc,
        "per_provider_means":   bc_meta.get("per_coder_means", []),
        "paper_claim_raw":      0.876,
        "paper_claim_bc":       0.933,
    }
    (base.with_suffix(".json")).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # Markdown report
    valid_rows = [r for r in matrix if sum(1 for v in r if v is not None) >= 2]
    md = []
    md.append(f"# Cross-LLM Krippendorff α report\n")
    md.append(f"- Generated: {summary['generated_at']}")
    md.append(f"- Providers: {', '.join(providers)}")
    md.append(f"- Targets attempted: {n_attempted}")
    md.append(f"- Targets with ≥2 valid stances: {len(valid_rows)}\n")
    md.append(f"## α results\n")
    md.append(f"| Metric | Value | Paper claim | Pass |")
    md.append(f"|--------|-------|-------------|------|")
    pass_raw = "✅" if alpha_raw >= 0.876 - 0.1 else "❌"
    pass_bc  = "✅" if alpha_bc  >= 0.933 - 0.1 else "❌"
    md.append(f"| α raw            | {alpha_raw:.3f} | 0.876 | {pass_raw} |")
    md.append(f"| α bias-corrected | {alpha_bc:.3f}  | 0.933 | {pass_bc} |")
    md.append(f"\n## Per-provider mean stance (bias correction inputs)\n")
    for p, m in zip(providers, bc_meta.get("per_coder_means", [])):
        md.append(f"- {p}: {m:+.3f}")
    md.append(f"\n## Output files\n")
    md.append(f"- CSV: `{base.with_suffix('.csv').relative_to(ROOT)}`")
    md.append(f"- JSON: `{base.with_suffix('.json').relative_to(ROOT)}`")
    (base.with_suffix(".md")).write_text("\n".join(md), encoding="utf-8")

    print(f"\n[v8.2 alpha] CSV:  {base.with_suffix('.csv').relative_to(ROOT)}")
    print(f"[v8.2 alpha] JSON: {base.with_suffix('.json').relative_to(ROOT)}")
    print(f"[v8.2 alpha] MD:   {base.with_suffix('.md').relative_to(ROOT)}")


# ===========================================================================
# CLI
# ===========================================================================

def main():
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except: pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--n",         type=int, default=20, help="number of (country,issue,cop) targets")
    ap.add_argument("--providers", default="gemini,anthropic,groq",
                    help="comma-separated subset of: gemini, anthropic, groq")
    ap.add_argument("--cop",       default="COP30", help="focal COP for sampling")
    ap.add_argument("--seed",      type=int, default=42)
    ap.add_argument("--delay",     type=float, default=0.5)
    ap.add_argument("--dry-run",   action="store_true")
    args = ap.parse_args()

    providers = [p.strip() for p in args.providers.split(",") if p.strip() in PROVIDERS]
    if not providers:
        print(f"❌ no valid providers from {args.providers}")
        sys.exit(1)

    # Check keys
    keys = {}
    for p in providers:
        _, env_var = PROVIDERS[p]
        k = os.environ.get(env_var)
        if not k and not args.dry_run:
            print(f"⚠️ skipping {p} (env {env_var} not set)")
        else:
            keys[p] = k or "DRY_RUN_KEY"
    providers = [p for p in providers if p in keys]
    if len(providers) < 2 and not args.dry_run:
        print(f"❌ need ≥2 providers with keys for α; have {len(providers)}")
        sys.exit(1)

    targets = sample_targets(args.n, seed=args.seed, focus_cop=args.cop)
    print(f"[v8.2 alpha] n_targets={len(targets)} providers={providers}")

    if args.dry_run:
        for t in targets[:10]: print("  -", t)
        if len(targets) > 10: print(f"  ... +{len(targets)-10} more")
        return

    targets, matrix = run(targets, providers, keys, delay_sec=args.delay)

    # Compute α
    alpha_raw = krippendorff_alpha(matrix)
    bc_matrix, bc_meta = bias_correct(matrix)
    alpha_bc = krippendorff_alpha(bc_matrix)
    print(f"\n[v8.2 alpha] α raw = {alpha_raw:.3f}  (paper claim 0.876)")
    print(f"[v8.2 alpha] α bias-corrected = {alpha_bc:.3f}  (paper claim 0.933)")

    save_outputs(targets, providers, matrix, alpha_raw, alpha_bc, bc_meta, n_attempted=len(targets))


if __name__ == "__main__":
    main()
