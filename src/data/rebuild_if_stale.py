"""Smart rebuild dispatcher — runs build steps only when source files changed.

Checks source hashes for v5/v6/v7 build artefacts; rebuilds only stale ones.

Usage:
  python -m src.data.rebuild_if_stale            # check + rebuild as needed
  python -m src.data.rebuild_if_stale --check    # report only, no rebuild
  python -m src.data.rebuild_if_stale --force    # rebuild everything

Author: Heedo Choi (Kookmin University)
License: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"


def file_sha(p: Path) -> str | None:
    if not p.exists(): return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_v5_dataset(force: bool = False) -> bool:
    """Check if stances_v5.jsonl needs rebuild."""
    out = DATA / "processed" / "stances_v5.jsonl"
    meta = DATA / "processed" / "stances_v5_meta.json"
    if force: return True
    if not out.exists() or not meta.exists(): return True
    try:
        m = json.loads(meta.read_text(encoding="utf-8"))
        # Source-hash for v5: builder file + expanded quotes file
        builder = ROOT / "src" / "data" / "build_v5_dataset.py"
        expanded = ROOT / "src" / "data" / "v5_evidence_quotes_expanded.py"
        cur_h = hashlib.sha256()
        if builder.exists(): cur_h.update(builder.read_bytes())
        if expanded.exists(): cur_h.update(expanded.read_bytes())
        return m.get("builder_hash") != cur_h.hexdigest()
    except: return True


def check_v6_corpus(force: bool = False) -> bool:
    """Check if corpus index needs rebuild."""
    if force: return True
    manifest = DATA / "corpus" / "manifest.jsonl"
    index = DATA / "corpus" / "search_index.json"
    if not manifest.exists() or not index.exists(): return True
    # any md/csv newer than index?
    idx_mtime = index.stat().st_mtime
    for p in (DATA / "corpus").rglob("*.md"):
        if p.stat().st_mtime > idx_mtime: return True
    for p in (DATA / "corpus" / "quantitative").glob("*.csv"):
        if p.stat().st_mtime > idx_mtime: return True
    return False


def check_v7_embeddings(force: bool = False) -> bool:
    """Use build_v7_embeddings own --check-stale logic."""
    if force: return True
    # Call the build script in check-stale mode (exit 1 = stale, 0 = fresh)
    result = subprocess.run(
        [sys.executable, "-m", "src.data.build_v7_embeddings", "--check-stale"],
        capture_output=True, cwd=ROOT, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )
    return result.returncode != 0


def run_step(cmd: list[str], desc: str) -> bool:
    print(f"\n[rebuild] {desc}")
    print(f"[rebuild] cmd: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    return result.returncode == 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except Exception: pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Report status only")
    ap.add_argument("--force", action="store_true", help="Rebuild everything")
    args = ap.parse_args()

    print(f"[rebuild] CINA build cache check\n{'='*60}")

    steps = [
        ("v5 dataset",        check_v5_dataset, ["src.data.build_v5_dataset"]),
        ("v6 corpus index",   check_v6_corpus,  ["src.data.build_v6_corpus_index"]),
        ("v7 embeddings",     check_v7_embeddings, ["src.data.build_v7_embeddings"]),
    ]

    needs = []
    for name, checker, _ in steps:
        stale = checker(force=args.force)
        sym = "🔴 STALE" if stale else "🟢 FRESH"
        print(f"[rebuild] {sym}  {name}")
        needs.append((name, stale))

    if args.check:
        any_stale = any(s for _, s in needs)
        sys.exit(1 if any_stale else 0)

    rebuilt = 0
    for (name, stale), (_, _, cmd) in zip(needs, steps):
        if stale:
            ok = run_step([sys.executable, "-m"] + cmd, f"rebuilding {name}")
            rebuilt += 1 if ok else 0
            if not ok:
                print(f"[rebuild] ❌ {name} FAILED")
                sys.exit(2)
    print(f"\n[rebuild] DONE. {rebuilt}/{len(steps)} rebuilt.")


if __name__ == "__main__":
    main()
