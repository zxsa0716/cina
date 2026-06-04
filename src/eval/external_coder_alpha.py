"""CINA v9.3 — External coder Krippendorff α aggregator.

Takes CSV exports from N external coders (via docs/web/coder_tool.html)
and computes Krippendorff α (interval level) across them.

Each CSV row has: coder_id, country, issue, cop, stance, frame, nato_n/a/t/o, confidence
Records with the same (country, issue, cop) tuple across coders form units.

Output:
  data/llm_logs/external_alpha_<ts>.{json,md}

Usage:
  python -m src.eval.external_coder_alpha \
      --csvs path/to/coder_park.csv,path/to/coder_lee.csv,path/to/coder_kim.csv

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations
import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Reuse Krippendorff α functions
from src.eval.cross_llm_alpha import krippendorff_alpha, bias_correct

ROOT = Path(__file__).resolve().parent.parent.parent
LOGS = ROOT / "data" / "llm_logs"
LOGS.mkdir(parents=True, exist_ok=True)


def load_coder_csv(p: Path) -> tuple[str, dict]:
    """Returns (coder_id, {(country, issue, cop): stance})."""
    by_key: dict[tuple, float] = {}
    coder_id = "?"
    with p.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            coder_id = row.get("coder_id") or coder_id
            try:
                stance = float(row["stance"])
            except (KeyError, ValueError):
                continue
            k = (row["country"], row["issue"], row["cop"])
            by_key[k] = stance
    return coder_id, by_key


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except: pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--csvs", required=True, help="comma-separated paths to N coder CSV exports")
    args = ap.parse_args()

    paths = [Path(p.strip()) for p in args.csvs.split(",") if p.strip()]
    if len(paths) < 2:
        print(f"❌ need ≥2 coder CSVs (got {len(paths)})")
        sys.exit(1)
    for p in paths:
        if not p.exists():
            print(f"❌ missing: {p}")
            sys.exit(1)

    coders = []
    coder_ids = []
    for p in paths:
        cid, by_key = load_coder_csv(p)
        coders.append(by_key); coder_ids.append(cid)
        print(f"[v9.3 alpha] {cid} ({p.name}): {len(by_key)} stances")

    # Build matrix: rows = unique (country, issue, cop) tuples; cols = coders
    all_keys = set()
    for c in coders: all_keys.update(c.keys())
    keys = sorted(all_keys)
    matrix = [[c.get(k) for c in coders] for k in keys]

    # Filter: keep only rows with ≥2 coders
    matrix_filtered = [r for r in matrix if sum(1 for v in r if v is not None) >= 2]
    keys_filtered  = [k for k, r in zip(keys, matrix) if sum(1 for v in r if v is not None) >= 2]
    print(f"[v9.3 alpha] {len(matrix_filtered)} units with ≥2 coders / {len(keys)} total")

    if not matrix_filtered:
        print("❌ no units with overlap"); sys.exit(2)

    alpha_raw = krippendorff_alpha(matrix_filtered)
    bc_m, bc_meta = bias_correct(matrix_filtered)
    alpha_bc = krippendorff_alpha(bc_m)

    print(f"\n[v9.3 alpha] α raw            = {alpha_raw:.3f}  (paper claim 0.876)")
    print(f"[v9.3 alpha] α bias-corrected = {alpha_bc:.3f}  (paper claim 0.933)")
    for cid, m in zip(coder_ids, bc_meta["per_coder_means"]):
        print(f"  per-coder mean:  {cid}: {m:+.3f}")

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = LOGS / f"external_alpha_{ts}"
    summary = {
        "generated_at":         datetime.now(timezone.utc).isoformat(),
        "n_coders":             len(coders),
        "coder_ids":            coder_ids,
        "n_units":              len(matrix_filtered),
        "krippendorff_alpha_raw": alpha_raw,
        "krippendorff_alpha_bc":  alpha_bc,
        "per_coder_means":      bc_meta["per_coder_means"],
        "paper_claim_raw":      0.876,
        "paper_claim_bc":       0.933,
    }
    base.with_suffix(".json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    md = [
        f"# External coder Krippendorff α — {ts}\n",
        f"- Coders: {len(coders)} ({', '.join(coder_ids)})",
        f"- Units (≥2 coders): {len(matrix_filtered)}\n",
        f"## Results",
        f"| Metric | Value | Paper claim | Pass |",
        f"|---|---|---|---|",
        f"| α raw            | {alpha_raw:.3f} | 0.876 | {'✅' if alpha_raw >= 0.776 else '❌'} |",
        f"| α bias-corrected | {alpha_bc:.3f}  | 0.933 | {'✅' if alpha_bc >= 0.833 else '❌'} |",
        f"\n## Per-coder means",
    ]
    for cid, m in zip(coder_ids, bc_meta["per_coder_means"]):
        md.append(f"- {cid}: {m:+.3f}")
    base.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print(f"\n[v9.3 alpha] {base.with_suffix('.json').relative_to(ROOT)}")
    print(f"[v9.3 alpha] {base.with_suffix('.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
