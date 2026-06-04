"""CINA v9.1 — v5.1 (heuristic) + v5.2-llm (LLM) → v5.2-merged.

Overlay merge policy:
  For each (country, issue, COP) tuple, take the BEST available record by
  source_type priority:
     1. verified_llm        (LLM-extracted, evidence verified by RapidFuzz)
     2. verified_canonical  (corpus-grounded hand-curated)
     3. llm_unverified_quote (LLM-extracted, evidence failed verification)
     4. heuristic_extension (synthetic anchor)

Provenance + audit log:
  Each merged record carries:
    _meta.source_type      — final selected source
    _meta.overlay_history  — list of {source_type, dataset, kept|dropped} entries
  Audit log written to data/processed/stances_v5_merged_audit.json
  with counts of (kept, replaced, conflicted) per source_type.

The merged dataset is the canonical reference for CINA Q&A serving.

Usage:
  python -m src.data.merge_v5_llm                    # all targets
  python -m src.data.merge_v5_llm --dry-run          # report only

Output:
  data/processed/stances_v5_merged.jsonl
  data/processed/stances_v5_merged_meta.json
  data/processed/stances_v5_merged_audit.json

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HEURISTIC = ROOT / "data" / "processed" / "stances_v5.jsonl"
LLM       = ROOT / "data" / "processed" / "stances_v5_llm.jsonl"
OUT       = ROOT / "data" / "processed" / "stances_v5_merged.jsonl"
META      = ROOT / "data" / "processed" / "stances_v5_merged_meta.json"
AUDIT     = ROOT / "data" / "processed" / "stances_v5_merged_audit.json"

# Lower number = higher priority (kept)
PRIORITY = {
    "verified_llm":          1,
    "verified_canonical":    2,
    "llm_unverified_quote":  3,
    "heuristic_extension":   4,
    None:                    9,
}


def load_jsonl(p: Path) -> list[dict]:
    if not p.exists(): return []
    with p.open("r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def key_of(r: dict) -> tuple:
    m = r["_meta"]
    return (m["country"], m["issue"], m["cop"])


def src_of(r: dict) -> str | None:
    return r.get("_meta", {}).get("source_type")


def merge_records(heuristic_records: list[dict], llm_records: list[dict]) -> tuple[list[dict], dict]:
    """Apply overlay policy. Returns (merged_records, audit_dict)."""
    # Bucket all records by (country, issue, COP) key
    by_key = defaultdict(list)
    for r in heuristic_records:
        by_key[key_of(r)].append(("v5.1", r))
    for r in llm_records:
        by_key[key_of(r)].append(("v5.2-llm", r))

    merged: list[dict] = []
    audit_counts: dict = defaultdict(int)
    overlay_event_log: list[dict] = []

    for k, entries in by_key.items():
        # Sort by priority
        entries_sorted = sorted(entries, key=lambda e: PRIORITY.get(src_of(e[1]), 99))
        kept_ds, kept_rec = entries_sorted[0]
        dropped = [(ds, src_of(r)) for ds, r in entries_sorted[1:]]
        # Stamp overlay history
        kept_rec = dict(kept_rec)  # shallow copy
        kept_rec["_meta"] = dict(kept_rec["_meta"])
        kept_rec["_meta"]["overlay_history"] = [
            {"dataset": ds, "source_type": src_of(r), "kept": True}
            for ds, r in entries_sorted[:1]
        ] + [
            {"dataset": ds, "source_type": st, "kept": False}
            for ds, st in dropped
        ]
        kept_rec["_meta"]["merge_priority"] = PRIORITY.get(src_of(kept_rec), 99)
        merged.append(kept_rec)
        audit_counts[f"kept_{src_of(kept_rec)}"] += 1
        if dropped:
            audit_counts["overlay_events"] += 1
            overlay_event_log.append({
                "key": list(k), "kept": src_of(kept_rec),
                "dropped": [{"dataset": d, "source_type": s} for d, s in dropped],
            })

    audit = {
        "generated_at":     datetime.now(timezone.utc).isoformat(),
        "n_total":          len(merged),
        "n_from_heuristic": len(heuristic_records),
        "n_from_llm":       len(llm_records),
        "kept_counts":      dict(audit_counts),
        "verified_ratio":   sum(1 for r in merged if src_of(r) in ("verified_llm", "verified_canonical")) / max(1, len(merged)),
        "n_overlay_events": len(overlay_event_log),
        "first_20_events":  overlay_event_log[:20],
    }
    return merged, audit


def write_outputs(merged: list[dict], audit: dict):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for r in merged:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # canonical lists from first record
    countries = sorted({r["_meta"]["country"] for r in merged})
    issues = sorted({r["_meta"]["issue"] for r in merged})
    cops = sorted({r["_meta"]["cop"] for r in merged})
    meta = {
        "dataset_version":  "5.2.0-merged",
        "prompt_version":   "stance_extract_v1.4_llm",
        "n_records":        len(merged),
        "n_countries":      len(countries),
        "n_issues":         len(issues),
        "n_cops":           len(cops),
        "countries":        countries,
        "issues":           issues,
        "cops":             cops,
        "verified_ratio":   audit["verified_ratio"],
        "kept_counts":      audit["kept_counts"],
        "generated_at":     audit["generated_at"],
        "overlay_policy":   "verified_llm > verified_canonical > llm_unverified_quote > heuristic_extension",
    }
    META.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    AUDIT.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except: pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    h = load_jsonl(HEURISTIC)
    l = load_jsonl(LLM)
    print(f"[v9.1 merge] heuristic={len(h)}  llm={len(l)}")
    if not h and not l:
        print(f"[v9.1 merge] no inputs — run build_v5_dataset / llm_stance_extractor first")
        sys.exit(1)

    merged, audit = merge_records(h, l)
    print(f"[v9.1 merge] result: {len(merged)} records")
    print(f"[v9.1 merge] verified_ratio: {audit['verified_ratio']*100:.1f}%")
    print(f"[v9.1 merge] overlay events: {audit['n_overlay_events']}")
    print(f"[v9.1 merge] kept counts:")
    for k, v in sorted(audit["kept_counts"].items()):
        print(f"   {k}: {v}")

    if args.dry_run:
        print("\n[v9.1 merge] --dry-run, not writing.")
        return

    write_outputs(merged, audit)
    print(f"\n[v9.1 merge] wrote {OUT.relative_to(ROOT)}")
    print(f"[v9.1 merge] wrote {META.relative_to(ROOT)}")
    print(f"[v9.1 merge] wrote {AUDIT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
