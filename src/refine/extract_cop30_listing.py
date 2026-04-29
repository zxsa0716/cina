"""Extract COP30 news listing page content from embedded JS window.__data."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
SRC  = BASE / "src"
sys.path.insert(0, str(SRC))
sys.stdout.reconfigure(encoding="utf-8")

from data.identifiers import ISSUE_KEYWORDS


def sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def tag_topics(text: str) -> list[str]:
    lower = text.lower()
    matched = []
    for issue_code, kws in ISSUE_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in lower:
                matched.append(issue_code)
                break
    return matched


def collect_texts(obj, results, depth=0):
    if depth > 15:
        return
    if isinstance(obj, dict):
        for key in ("title", "description", "text", "content", "summary", "body"):
            val = obj.get(key, "")
            if isinstance(val, str) and len(val) > 30:
                results.append(val.strip())
        for v in obj.values():
            collect_texts(v, results, depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            collect_texts(item, results, depth + 1)


def extract_cop30_listing(html_path: Path, doc_id: str, manifest_entry: dict) -> dict | None:
    html = html_path.read_bytes().decode("utf-8", errors="replace")

    m = re.search(r"window\.__data=(.*?);\s*</script>", html, re.DOTALL)
    if not m:
        return None

    raw_js = m.group(1)
    raw_js = re.sub(r"\bundefined\b", "null", raw_js)
    try:
        data = json.loads(raw_js)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse: {e}", file=sys.stderr)
        return None

    results = []
    collect_texts(data, results)

    # Deduplicate preserving order
    seen = set()
    unique = []
    for r in results:
        if r not in seen:
            seen.add(r)
            unique.append(r)

    full_text = "\n\n".join(unique)
    if len(full_text) < 200:
        return None

    paras = [{"para_id": i + 1, "text": t} for i, t in enumerate(unique)]
    topics = tag_topics(full_text)

    return {
        "doc_id": doc_id,
        "source": "cop30_official",
        "source_type": "cop30_official",
        "cop_session": "COP30",
        "subsidiary_body": None,
        "document_type": "web_news_listing",
        "date": "2026-04-25",
        "authors": ["Brazil (COP30 Presidency)"],
        "topics": topics if topics else ["adaptation"],
        "topic_tags": topics,
        "country_authors_initial": ["BRA"],
        "groups_referenced": [],
        "language": "en",
        "paragraphs": paras,
        "paragraphs_total_raw": len(paras),
        "paragraphs_selected": len(paras),
        "url": manifest_entry.get("source_url", ""),
        "retrieved_at": manifest_entry.get("retrieved_at", ""),
        "sha256": sha256_of_text(full_text),
        "sha256_raw_file": manifest_entry.get("sha256", ""),
        "filesize_bytes": manifest_entry.get("filesize_bytes", 0),
        "processing_version": "round1-v1.0",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "extraction_note": (
            f"Extracted {len(paras)} text pieces from window.__data JS object. "
            "Original page is a React SPA with minimal static HTML."
        ),
    }


if __name__ == "__main__":
    html_path = BASE / "data/raw/cop30_official/en_news_about_cop30.html"
    manifest_path = BASE / "data/manifest/manifest.jsonl"

    manifest = {}
    with open(manifest_path, encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            manifest[e["doc_id"]] = e

    doc_id = "cop30_official-48e357da95f6"
    entry = manifest.get(doc_id, {
        "doc_id": doc_id,
        "source_url": "https://cop30.br/en/news-about-cop30",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "sha256": "",
        "filesize_bytes": html_path.stat().st_size,
    })

    doc = extract_cop30_listing(html_path, doc_id, entry)
    if doc:
        print(f"[OK] {doc['doc_id']} | topics={doc['topic_tags']} | paras={doc['paragraphs_selected']}")
        # Append to documents.jsonl
        out_path = BASE / "data/processed/documents.jsonl"
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
        print(f"[OK] Appended to {out_path}")
    else:
        print("[FAIL] Extraction returned None")
