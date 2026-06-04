"""CINA v9.6 — Reproducibility certificate generator.

Computes a hash chain across all CINA build artefacts:
  - v5 dataset (stances_v5.jsonl + stances_v5_meta.json)
  - v6 corpus (manifest.jsonl + 21 markdown + 5 CSVs + search_index.json)
  - v7 embeddings (embeddings.npz + embeddings_index.json)
  - Build scripts (build_v5_dataset, build_v6_corpus_index, build_v7_embeddings,
                   merge_v5_llm, llm_stance_extractor, etc.)
  - Source code (query_engine_v2, llm_cache, evaluator modules)

Output:
  data/reproducibility_certificate.json   — structured hash list + chain hash
  data/reproducibility_certificate.md     — human-readable summary

The "chain hash" is SHA-256 of the sorted (path, sha256) pairs concatenated.
External validators can run this script on a fresh clone and compare chain hashes.

Usage:
  python -m src.data.build_reproducibility_certificate
  python -m src.data.build_reproducibility_certificate --verify  # compare to stored chain

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_JSON = ROOT / "data" / "reproducibility_certificate.json"
OUT_MD   = ROOT / "data" / "reproducibility_certificate.md"

# Categorised list of artefacts/source files
CATEGORIES = {
    "v5_dataset": [
        "data/processed/stances_v5.jsonl",
        "data/processed/stances_v5_meta.json",
    ],
    "v5_merged": [
        "data/processed/stances_v5_merged.jsonl",
        "data/processed/stances_v5_merged_meta.json",
        "data/processed/stances_v5_merged_audit.json",
    ],
    "v6_corpus_index": [
        "data/corpus/manifest.jsonl",
        "data/corpus/search_index.json",
        "data/corpus/README.md",
    ],
    "v6_corpus_documents": "data/corpus/**/*.md",     # glob
    "v6_corpus_csvs":      "data/corpus/quantitative/*.csv",
    "v6_corpus_bib":      ["data/corpus/academic_references/bibliography.bib"],
    "v7_embeddings": [
        "data/corpus/embeddings.npz",
        "data/corpus/embeddings_index.json",
        "data/corpus/embeddings_gemini.npz",
        "data/corpus/embeddings_gemini_index.json",
    ],
    "build_scripts": [
        "src/data/build_v5_dataset.py",
        "src/data/v5_evidence_quotes_expanded.py",
        "src/data/build_v6_corpus_index.py",
        "src/data/build_v6_quantitative.py",
        "src/data/build_v7_embeddings.py",
        "src/data/build_v7_embeddings_gemini.py",
        "src/data/merge_v5_llm.py",
        "src/data/rebuild_if_stale.py",
    ],
    "engine_scripts": [
        "src/program/query_engine_v2.py",
        "src/program/llm_stance_extractor.py",
        "src/program/llm_cache.py",
    ],
    "eval_scripts": [
        "src/eval/cross_llm_alpha.py",
        "src/eval/external_coder_alpha.py",
    ],
    "test_suite": "tests/test_*.py",
    "changelogs": "CHANGELOG_v*.md",
    "documentation": [
        "CLAUDE.md", "README.md", "data/corpus/README.md",
        "docs/research/PUBLICATION_STRATEGY.md",
    ],
}


def file_sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
    return h.hexdigest()


def collect_files(spec) -> list[Path]:
    """Resolve spec (list of paths or single glob string) to actual file list."""
    if isinstance(spec, list):
        return [ROOT / p for p in spec]
    elif isinstance(spec, str):
        # glob
        if "**" in spec:
            base = ROOT / spec.split("**")[0]
            pattern = spec.split("**")[1].lstrip("/")
            return sorted(base.rglob(pattern))
        else:
            base = ROOT / Path(spec).parent
            return sorted(base.glob(Path(spec).name))
    return []


def build_certificate() -> dict:
    entries = []
    per_category_counts = {}
    for category, spec in CATEGORIES.items():
        files = collect_files(spec)
        present = [p for p in files if p.exists()]
        per_category_counts[category] = {"requested": len(files), "present": len(present)}
        for p in sorted(present):
            entries.append({
                "category":  category,
                "path":      str(p.relative_to(ROOT)).replace("\\", "/"),
                "sha256":    file_sha(p),
                "size_bytes": p.stat().st_size,
            })

    # Chain hash = sha256 of sorted (path, sha) pairs
    chain_h = hashlib.sha256()
    for e in sorted(entries, key=lambda x: x["path"]):
        chain_h.update((e["path"] + "|" + e["sha256"]).encode())
    chain = chain_h.hexdigest()

    cert = {
        "version":         "v9.6.0",
        "generated_at":    datetime.now(timezone.utc).isoformat(),
        "n_entries":       len(entries),
        "chain_hash":      chain,
        "per_category":    per_category_counts,
        "entries":         entries,
    }
    return cert


def write_certificate(cert: dict):
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(cert, indent=2, ensure_ascii=False), encoding="utf-8")

    # MD report
    lines = [
        f"# CINA Reproducibility Certificate",
        f"",
        f"- **Version**: {cert['version']}",
        f"- **Generated**: {cert['generated_at']}",
        f"- **Total entries**: {cert['n_entries']}",
        f"- **Chain hash**: `{cert['chain_hash']}`",
        f"",
        f"## Categories",
        f"",
        f"| Category | Requested | Present |",
        f"|---|---|---|",
    ]
    for cat, counts in cert["per_category"].items():
        lines.append(f"| {cat} | {counts['requested']} | {counts['present']} |")
    lines.append("")
    lines.append("## How to verify")
    lines.append("")
    lines.append("```bash")
    lines.append("git clone https://github.com/zxsa0716/cina")
    lines.append("cd cina")
    lines.append("python -m src.data.build_reproducibility_certificate")
    lines.append("# Compare chain_hash with the one in this file above")
    lines.append("```")
    lines.append("")
    lines.append("If chain hashes match, the entire CINA build chain (data + scripts + tests + docs)")
    lines.append("is bit-identical to the certified state.")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def verify_against_stored() -> bool:
    if not OUT_JSON.exists():
        print(f"❌ no stored certificate at {OUT_JSON}")
        return False
    stored = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    fresh = build_certificate()
    match = stored.get("chain_hash") == fresh["chain_hash"]
    print(f"stored chain : {stored.get('chain_hash')}")
    print(f"fresh chain  : {fresh['chain_hash']}")
    print(f"match: {'✅ YES' if match else '❌ NO'}")
    if not match:
        # Diff entries
        stored_set = {(e["path"], e["sha256"]) for e in stored.get("entries", [])}
        fresh_set  = {(e["path"], e["sha256"]) for e in fresh["entries"]}
        added = fresh_set - stored_set
        removed = stored_set - fresh_set
        if added:
            print(f"\nAdded/changed ({len(added)}):")
            for p, _ in sorted(added)[:10]: print(f"  + {p}")
        if removed:
            print(f"\nRemoved/changed ({len(removed)}):")
            for p, _ in sorted(removed)[:10]: print(f"  - {p}")
    return match


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except: pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true",
                    help="compare current state to stored certificate")
    args = ap.parse_args()

    if args.verify:
        ok = verify_against_stored()
        sys.exit(0 if ok else 1)

    cert = build_certificate()
    write_certificate(cert)
    print(f"[v9.6 cert] {cert['n_entries']} entries certified")
    print(f"[v9.6 cert] chain hash: {cert['chain_hash']}")
    print(f"[v9.6 cert] wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"[v9.6 cert] wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
