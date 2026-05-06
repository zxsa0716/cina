"""CINA Peer Review Orchestrator (10 simulated reviewers).

Reads each completed reviewer brief in docs/peer_review/R{1..10}_*.md and
aggregates them into docs/peer_review/SYNTHESIS.md per the protocol in
docs/peer_review/00_PROTOCOL.md.

Usage:
    # Just check which reviewers are complete
    python scripts/run_peer_review.py --status

    # Generate the synthesis from completed reviews
    python scripts/run_peer_review.py --synthesize

    # Validate that completed reviews fill the rubric
    python scripts/run_peer_review.py --validate

Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
License: MIT

Honesty disclosure: This script aggregates *simulated* peer review by LLM
personas. It is not a substitute for externally-recruited expert review.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
PR_DIR = ROOT / "docs" / "peer_review"

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REVIEWERS = [
    ("R1",  "Climate Sci",   "R1_climate_science.md"),
    ("R2",  "IR Theory",     "R2_international_relations.md"),
    ("R3",  "Practitioner",  "R3_diplomacy_practitioner.md"),
    ("R4",  "Policy Sci",    "R4_policy_science.md"),
    ("R5",  "SE / DevOps",   "R5_software_engineering.md"),
    ("R6",  "ML / NLP",      "R6_machine_learning_nlp.md"),
    ("R7",  "GNN / Network", "R7_graph_network_modeling.md"),
    ("R8",  "Stats",         "R8_quantitative_stats.md"),
    ("R9",  "Korean KCI",    "R9_korean_policy_KCI.md"),
    ("R10", "Editor",        "R10_academic_editor.md"),
]

DIMS = [
    ("D1",  "Theory"),
    ("D2",  "Method"),
    ("D3",  "Empirics"),
    ("D4",  "Honesty"),
    ("D5",  "Reprod"),
    ("D6",  "Policy"),
    ("D7",  "Literature"),
    ("D8",  "Writing"),
    ("D9",  "Novelty"),
    ("D10", "Ready"),
]


def parse_review(path: Path) -> Optional[dict]:
    """Parse a review markdown file. Returns None if incomplete (still has __/5 placeholders)."""
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")

    # Detect completion: a completed review has actual numbers in place of `__/5`
    # We look for "X/5" patterns where X is 0-5 in the rubric table
    rubric_rows = re.findall(r"\|\s*(D\d+)[^|]*\|\s*(\d(?:\.\d)?)/5\s*\|", text)
    if len(rubric_rows) < 5:
        # Less than half the rubric filled = incomplete
        return None

    scores = {}
    for dim_id, score_str in rubric_rows:
        try:
            scores[dim_id] = float(score_str)
        except ValueError:
            continue

    # Extract venue recommendation
    venue_match = re.search(r"###\s*Venue recommendation([\s\S]*?)(?=###|\Z)", text)
    venue_lines = venue_match.group(1).strip().split("\n") if venue_match else []
    chosen_venues = [
        line.strip().lstrip("☑").lstrip("✓").lstrip("☒").strip()
        for line in venue_lines
        if line.strip().startswith(("☑", "✓", "☒"))
    ]

    # Extract Top 3 weaknesses (look for numbered list under "Top 3 weaknesses")
    weak_match = re.search(r"Top 3 weaknesses[^\n]*\n([\s\S]*?)(?=###|\Z)", text)
    weaknesses = []
    if weak_match:
        for line in weak_match.group(1).split("\n"):
            line = line.strip()
            if re.match(r"^\d+\.", line):
                weaknesses.append(re.sub(r"^\d+\.\s*", "", line))

    # Extract reject reason
    reject_match = re.search(
        r"Most likely reject reason[^\n]*\n+([^\n]+(?:\n[^\n#]+)*)", text)
    reject_reason = reject_match.group(1).strip() if reject_match else ""

    return {
        "scores": scores,
        "venues": chosen_venues,
        "weaknesses": weaknesses[:3],
        "reject_reason": reject_reason,
        "complete": len(scores) >= 8  # Allow 8/10 dims for completion threshold
    }


def cmd_status():
    print("=" * 72)
    print(" CINA Peer Review Status")
    print("=" * 72)
    n_complete = 0
    n_partial = 0
    for rid, label, fname in REVIEWERS:
        path = PR_DIR / fname
        result = parse_review(path)
        if result is None:
            status = "⏸️  pending"
        elif result["complete"]:
            status = "✅ complete"
            n_complete += 1
        else:
            status = "🟡 partial"
            n_partial += 1
        print(f" {rid:>3} {label:<18} {status:<13} {fname}")
    print()
    print(f" Complete: {n_complete} / 10")
    print(f" Partial:  {n_partial} / 10")
    print(f" Pending:  {10 - n_complete - n_partial} / 10")
    print("=" * 72)


def cmd_validate():
    print("Validating completed reviews...")
    issues = []
    for rid, label, fname in REVIEWERS:
        path = PR_DIR / fname
        result = parse_review(path)
        if result is None or not result["complete"]:
            continue
        # Check rubric completeness
        missing_dims = [d[0] for d in DIMS if d[0] not in result["scores"]]
        if missing_dims:
            issues.append(f"{rid}: missing dims {missing_dims}")
        # Check venue selected
        if not result["venues"]:
            issues.append(f"{rid}: no venue selected")
        # Check weaknesses
        if len(result["weaknesses"]) < 3:
            issues.append(f"{rid}: less than 3 weaknesses listed")

    if issues:
        print("\n  Issues found:")
        for i in issues:
            print(f"    - {i}")
    else:
        print("\n  ✅ All completed reviews valid.")


def cmd_synthesize():
    print("Synthesizing 10 reviews...")
    reviews = {}
    for rid, label, fname in REVIEWERS:
        path = PR_DIR / fname
        result = parse_review(path)
        reviews[rid] = (label, result)

    n_complete = sum(1 for _, r in reviews.values()
                     if r is not None and r["complete"])
    if n_complete < 5:
        print(f"  ⚠ Only {n_complete}/10 reviews complete. "
              f"Synthesis needs at least 5; abort.")
        return

    # Build score matrix
    matrix = {}  # {dim: [scores from each reviewer]}
    for dim_id, _ in DIMS:
        matrix[dim_id] = []
        for rid, _, _ in REVIEWERS:
            _, r = reviews[rid]
            if r and r["complete"] and dim_id in r["scores"]:
                matrix[dim_id].append(r["scores"][dim_id])

    # Compute aggregates
    avg = {d: round(mean(matrix[d]), 2) if matrix[d] else None
           for d, _ in DIMS}
    sd = {d: round(stdev(matrix[d]), 2) if len(matrix[d]) > 1 else None
          for d, _ in DIMS}

    print()
    print("Average scores per dimension:")
    for d, label in DIMS:
        print(f"  {d} {label:<12} avg = {avg[d]} (σ = {sd[d]}, n = {len(matrix[d])})")

    # Decision gate
    print()
    print("Decision gate evaluation:")
    gates = [
        ("D2 ≥ 3.5", avg["D2"] is not None and avg["D2"] >= 3.5),
        ("D4 ≥ 4.0", avg["D4"] is not None and avg["D4"] >= 4.0),
        ("D5 ≥ 4.0", avg["D5"] is not None and avg["D5"] >= 4.0),
    ]
    for name, passed in gates:
        print(f"  {name}: {'✅' if passed else '❌'}")

    # Aggregate weaknesses (frequency count)
    all_weaknesses = []
    for rid, _, _ in REVIEWERS:
        _, r = reviews[rid]
        if r and r["complete"]:
            all_weaknesses.extend(r["weaknesses"])

    # Aggregate venues
    venue_counts = defaultdict(int)
    for rid, _, _ in REVIEWERS:
        _, r = reviews[rid]
        if r and r["complete"]:
            for v in r["venues"]:
                if v:
                    venue_counts[v] += 1

    # Write SYNTHESIS.md
    synthesis_path = PR_DIR / "SYNTHESIS.md"
    lines = []
    lines.append(f"# CINA Peer Review Synthesis (auto-generated)")
    lines.append("")
    lines.append(f"> {n_complete} / 10 reviewers complete · simulated peer review")
    lines.append("")
    lines.append("## Score matrix")
    lines.append("")
    header = "| Reviewer | " + " | ".join(d[0] for d in DIMS) + " | Total |"
    sep = "|" + "---|" * (len(DIMS) + 2)
    lines.append(header)
    lines.append(sep)
    for rid, label, _ in REVIEWERS:
        _, r = reviews[rid]
        if r and r["complete"]:
            row = [f"{r['scores'].get(d[0], '')}" for d in DIMS]
            total = sum(r["scores"].get(d[0], 0) for d in DIMS)
            lines.append(f"| {rid} {label} | " + " | ".join(row) + f" | {total:.1f} |")
        else:
            lines.append(f"| {rid} {label} | " + " | ".join(["—"] * 10) + " | — |")
    avg_row = "| **avg** | " + " | ".join(f"**{avg[d[0]]}**" for d in DIMS) + " | — |"
    sd_row = "| **σ** | " + " | ".join(f"{sd[d[0]] or '—'}" for d in DIMS) + " | — |"
    lines.append(avg_row)
    lines.append(sd_row)

    lines.append("")
    lines.append("## Decision gate")
    lines.append("")
    for name, passed in gates:
        lines.append(f"- {name}: {'✅ pass' if passed else '❌ fail'}")
    overall_pass = all(p for _, p in gates)
    lines.append(f"\n**Overall**: {'✅ READY for arXiv + Workshop' if overall_pass else '❌ NEEDS revision'}")

    lines.append("")
    lines.append("## Aggregated weaknesses (all reviewers)")
    lines.append("")
    for i, w in enumerate(all_weaknesses, 1):
        lines.append(f"{i}. {w}")

    lines.append("")
    lines.append("## Venue recommendation distribution")
    lines.append("")
    for v, c in sorted(venue_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {v}: {c}/{n_complete}")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Auto-generated by `scripts/run_peer_review.py --synthesize`. "
                 "Simulated peer review — see CRITICAL_REVIEW.md §3.2 for limitations.*")

    synthesis_path.write_text("\n".join(lines), encoding="utf-8")
    print()
    print(f"  ✅ {synthesis_path.relative_to(ROOT)} written")


def main():
    parser = argparse.ArgumentParser(description="CINA peer review orchestrator")
    parser.add_argument("--status", action="store_true",
                        help="Show completion status of all 10 reviewers")
    parser.add_argument("--validate", action="store_true",
                        help="Validate completed reviews fill the rubric")
    parser.add_argument("--synthesize", action="store_true",
                        help="Aggregate completed reviews into SYNTHESIS.md")
    args = parser.parse_args()

    if args.status:
        cmd_status()
    elif args.validate:
        cmd_validate()
    elif args.synthesize:
        cmd_synthesize()
    else:
        cmd_status()
        print("\nNext: `python scripts/run_peer_review.py --synthesize`")


if __name__ == "__main__":
    main()
