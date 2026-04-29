"""Manifest management — single source of truth for collected documents.

`data/manifest/manifest.jsonl` 에 모든 수집물 누적. Append-only + dedup by sha256.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from filelock import FileLock

MANIFEST_DIR = Path("data/manifest")
MANIFEST_FILE = MANIFEST_DIR / "manifest.jsonl"
LOCK_FILE = MANIFEST_DIR / ".manifest.lock"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def doc_id_from_url(source: str, url: str) -> str:
    """Stable doc_id from source+URL."""
    h = hashlib.sha1((source + "|" + url).encode()).hexdigest()[:12]
    return f"{source}-{h}"


def append_record(record: dict) -> None:
    """Append a manifest entry, dedupe-on-sha256 + dedupe-on-doc_id."""
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    record.setdefault("recorded_at", now_iso())
    with FileLock(str(LOCK_FILE)):
        existing = load_records()
        seen_sha = {r.get("sha256") for r in existing if r.get("sha256")}
        seen_id = {r.get("doc_id") for r in existing if r.get("doc_id")}
        if record.get("sha256") in seen_sha:
            return
        if record.get("doc_id") in seen_id:
            return
        with open(MANIFEST_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def load_records() -> list[dict]:
    if not MANIFEST_FILE.exists():
        return []
    with open(MANIFEST_FILE, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def find_by_url(url: str) -> Optional[dict]:
    for r in load_records():
        if r.get("source_url") == url:
            return r
    return None


def coverage_summary() -> dict:
    """Compute coverage: countries × issues × sessions."""
    from src.data.identifiers import (
        CINA_COUNTRIES, CINA_ISSUES, CINA_SESSIONS,
    )

    records = load_records()
    by_source: dict[str, int] = {}
    by_session: dict[str, int] = {}
    by_country: dict[str, int] = {}
    by_issue: dict[str, int] = {}

    for r in records:
        by_source[r.get("source_system", "?")] = by_source.get(r.get("source_system", "?"), 0) + 1
        s = r.get("session", "?")
        by_session[s] = by_session.get(s, 0) + 1
        for c in r.get("country_authors_initial", []):
            by_country[c] = by_country.get(c, 0) + 1
        for t in r.get("topic_tags_initial", []):
            by_issue[t] = by_issue.get(t, 0) + 1

    return {
        "total_documents": len(records),
        "by_source": by_source,
        "by_session": by_session,
        "by_country": by_country,
        "by_issue": by_issue,
        "coverage_pct": {
            "countries": round(
                100 * sum(1 for k in CINA_COUNTRIES if k in by_country)
                / max(len(CINA_COUNTRIES), 1),
                1,
            ),
            "issues": round(
                100 * sum(1 for k in CINA_ISSUES if k in by_issue)
                / max(len(CINA_ISSUES), 1),
                1,
            ),
            "sessions": round(
                100 * sum(1 for k in CINA_SESSIONS if k in by_session)
                / max(len(CINA_SESSIONS), 1),
                1,
            ),
        },
        "computed_at": now_iso(),
    }


def write_summary(out_path: Path = MANIFEST_DIR / "coverage_summary.json") -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(coverage_summary(), ensure_ascii=False, indent=2), encoding="utf-8")
