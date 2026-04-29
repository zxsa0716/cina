"""CINA Round 1 — Data Refinement Pipeline (rules-based, no LLM).

입력  : data/raw/ 하위 7개 파일 (4 PDF + 3 HTML)
출력  : data/processed/documents.jsonl
        data/processed/refinement_stats.json
로그  : stderr
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# 경로 설정
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parents[2]
SRC  = BASE / "src"
sys.path.insert(0, str(SRC))

from data.identifiers import (
    CINA_COUNTRIES,
    CINA_GROUPS,
    CINA_SESSIONS,
    ISSUE_KEYWORDS,
)

RAW_IPCC   = BASE / "data/raw/ipcc_ar6/wg2"
RAW_COP30  = BASE / "data/raw/cop30_official"
RAW_CASTRO = BASE / "data/raw/castro_2025"
MANIFEST   = BASE / "data/manifest/manifest.jsonl"
OUT_DIR    = BASE / "data/processed"
REJECTED   = OUT_DIR / "rejected"

OUT_DIR.mkdir(parents=True, exist_ok=True)
REJECTED.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 헬퍼: SHA-256 (내용 기반)
# ---------------------------------------------------------------------------
def sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# ---------------------------------------------------------------------------
# 헬퍼: 단락 분할
# ---------------------------------------------------------------------------
_PARA_SPLIT = re.compile(r"\n{2,}")

def split_paragraphs(text: str, min_len: int = 40) -> list[dict]:
    """개행 2회 이상으로 1차 분할, 최소 길이 미만 단락은 이전 단락에 병합."""
    raw = _PARA_SPLIT.split(text)
    result = []
    buf = ""
    for chunk in raw:
        chunk = chunk.strip()
        if not chunk:
            continue
        buf = (buf + " " + chunk).strip() if buf else chunk
        if len(buf) >= min_len:
            result.append(buf)
            buf = ""
    if buf:
        result.append(buf)
    return [{"para_id": i + 1, "text": p} for i, p in enumerate(result)]

# ---------------------------------------------------------------------------
# 헬퍼: 토픽 태깅
# ---------------------------------------------------------------------------
def tag_topics(text: str) -> list[str]:
    """ISSUE_KEYWORDS 기반 규칙 태깅. 대소문자 무시."""
    lower = text.lower()
    matched = []
    for issue_code, kws in ISSUE_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in lower:
                matched.append(issue_code)
                break
    return matched

# ---------------------------------------------------------------------------
# 헬퍼: 국가 인식
# ---------------------------------------------------------------------------
_COUNTRY_ALIASES: dict[str, str] = {
    # 약어 → ISO3
    "eu":              "EU",
    "european union":  "EU",
    "united states":   "USA",
    "united states of america": "USA",
    "u.s.":            "USA",
    "u.s.a.":          "USA",
    "brazil":          "BRA",
    "brasil":          "BRA",
    "china":           "CHN",
    "india":           "IND",
    "japan":           "JPN",
    "korea":           "KOR",
    "republic of korea": "KOR",
    "australia":       "AUS",
    "canada":          "CAN",
    "norway":          "NOR",
    "switzerland":     "CHE",
    "mexico":          "MEX",
    "south africa":    "ZAF",
    "saudi arabia":    "SAU",
    "united arab emirates": "ARE",
    "uae":             "ARE",
    "egypt":           "EGY",
    "colombia":        "COL",
    "chile":           "CHL",
    "costa rica":      "CRI",
    "kenya":           "KEN",
}

_GROUP_ALIASES: dict[str, str] = {
    "g77":          "g77",
    "g77+china":    "g77",
    "aosis":        "aosis",
    "ldc":          "ldc",
    "least developed countries": "ldc",
    "african group": "african",
    "arab group":   "arab",
    "ailac":        "ailac",
    "basic":        "basic",
    "lmdc":         "lmdc",
    "like-minded developing countries": "lmdc",
    "umbrella":     "umbrella",
    "umbrella group": "umbrella",
    "high ambition coalition": "hac",
    "eig":          "eig",
    "environmental integrity group": "eig",
}

def identify_countries(text: str) -> list[str]:
    lower = text.lower()
    found = set()
    for alias, iso3 in _COUNTRY_ALIASES.items():
        if re.search(r"\b" + re.escape(alias) + r"\b", lower):
            found.add(iso3)
    return sorted(found)

def identify_groups(text: str) -> list[str]:
    lower = text.lower()
    found = set()
    for alias, slug in _GROUP_ALIASES.items():
        if re.search(r"\b" + re.escape(alias) + r"\b", lower):
            found.add(slug)
    return sorted(found)

# ---------------------------------------------------------------------------
# 헬퍼: 세션 추출
# ---------------------------------------------------------------------------
_SESSION_RE = re.compile(
    r"\b(COP\s*\d+|SBI\s*\d+|SBSTA\s*\d+|CMA\s*\d+)\b", re.IGNORECASE
)

def extract_sessions(text: str) -> list[str]:
    raw = _SESSION_RE.findall(text)
    normalized = [re.sub(r"\s+", "", s.upper()) for s in raw]
    valid = [s for s in normalized if s in CINA_SESSIONS]
    return sorted(set(valid))

# ---------------------------------------------------------------------------
# PDF 추출 (PyMuPDF) — 첫 50 단락 + 마지막 30 단락 + 키워드 매치
# ---------------------------------------------------------------------------
import fitz  # PyMuPDF

def extract_pdf(path: Path, manifest_entry: dict) -> dict | None:
    """PDF → CINA Document Schema dict. 실패 시 None."""
    try:
        doc = fitz.open(str(path))
    except Exception as e:
        print(f"[ERROR] PDF open failed: {path.name}: {e}", file=sys.stderr)
        return None

    pages_text = []
    for page in doc:
        pages_text.append(page.get_text("text"))
    doc.close()

    full_text = "\n\n".join(pages_text).strip()
    if len(full_text) < 200:
        print(f"[WARN] PDF too short (<200 chars): {path.name}", file=sys.stderr)
        return None

    all_paras = split_paragraphs(full_text)
    total = len(all_paras)

    # 헤드 50 + 테일 30 + 키워드 매치 단락
    head_set  = set(range(0, min(50, total)))
    tail_set  = set(range(max(0, total - 30), total))
    kw_all    = [kw.lower() for kws in ISSUE_KEYWORDS.values() for kw in kws]
    kw_set    = set()
    for i, p in enumerate(all_paras):
        t = p["text"].lower()
        if any(kw in t for kw in kw_all):
            kw_set.add(i)

    selected_idx = sorted(head_set | tail_set | kw_set)
    selected_paras = []
    for new_id, old_idx in enumerate(selected_idx, start=1):
        selected_paras.append({"para_id": new_id, "text": all_paras[old_idx]["text"]})

    extracted_text = " ".join(p["text"] for p in selected_paras)
    topics   = tag_topics(extracted_text)
    countries = identify_countries(extracted_text)
    groups   = identify_groups(extracted_text)
    sessions = extract_sessions(extracted_text)

    chapter_num   = manifest_entry.get("chapter_number", "")
    chapter_title = manifest_entry.get("chapter_title", "")

    return {
        "doc_id":           manifest_entry["doc_id"],
        "source":           "ipcc_ar6_wg2",
        "source_type":      "ipcc_ar6_wg2",
        "cop_session":      sessions[0] if sessions else "COP30",
        "subsidiary_body":  None,
        "document_type":    "ipcc_chapter",
        "date":             "2022-02-28",   # AR6 WG2 SPM approval date
        "authors":          ["IPCC WG2"],
        "topics":           topics if topics else ["adaptation"],
        "topic_tags":       topics,
        "country_authors_initial": countries,
        "groups_referenced": groups,
        "language":         "en",
        "paragraphs":       selected_paras,
        "paragraphs_total_raw": total,
        "paragraphs_selected":  len(selected_paras),
        "chapter_number":   chapter_num,
        "chapter_title":    chapter_title,
        "url":              manifest_entry.get("source_url", ""),
        "retrieved_at":     manifest_entry.get("retrieved_at", ""),
        "sha256":           sha256_of_text(full_text),
        "sha256_raw_file":  manifest_entry.get("sha256", ""),
        "filesize_bytes":   manifest_entry.get("filesize_bytes", 0),
        "processing_version": "round1-v1.0",
        "processed_at":     datetime.now(timezone.utc).isoformat(),
        "extraction_note":  (
            f"Selected {len(selected_paras)}/{total} paragraphs "
            f"(head50+tail30+keyword_match). "
            f"Keyword match para count: {len(kw_set)}."
        ),
    }

# ---------------------------------------------------------------------------
# HTML 추출 (BeautifulSoup)
# ---------------------------------------------------------------------------
from bs4 import BeautifulSoup

_BOILERPLATE_RE = re.compile(
    r"(javascript|cookie|privacy policy|terms of use|subscribe|follow us|"
    r"newsletter|copyright ©|all rights reserved|skip to (main )?content|"
    r"menu|search|login|sign up|share this)",
    re.IGNORECASE,
)

def extract_html(path: Path, manifest_entry: dict) -> dict | None:
    try:
        raw_bytes = path.read_bytes()
        html = raw_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"[ERROR] HTML read failed: {path.name}: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(html, "html.parser")

    # 불필요 태그 제거
    for tag in soup(["script", "style", "nav", "footer", "header",
                     "aside", "form", "button", "iframe"]):
        tag.decompose()

    # 본문 우선순위: <main> > <article> > <body>
    body = soup.find("main") or soup.find("article") or soup.find("body")
    if body is None:
        print(f"[WARN] No body found: {path.name}", file=sys.stderr)
        return None

    # 텍스트 추출 (블록 요소 → 개행)
    texts = []
    for elem in body.find_all(["p", "h1", "h2", "h3", "h4", "li", "blockquote", "td"]):
        t = elem.get_text(separator=" ", strip=True)
        if t and len(t) > 20 and not _BOILERPLATE_RE.search(t):
            texts.append(t)

    full_text = "\n\n".join(texts).strip()
    if len(full_text) < 200:
        print(f"[WARN] HTML too short (<200 chars): {path.name}", file=sys.stderr)
        return None

    paras    = split_paragraphs(full_text)
    topics   = tag_topics(full_text)
    countries = identify_countries(full_text)
    groups   = identify_groups(full_text)
    sessions = extract_sessions(full_text)

    source_type = manifest_entry.get("source_type", "unknown")

    return {
        "doc_id":           manifest_entry["doc_id"],
        "source":           source_type,
        "source_type":      source_type,
        "cop_session":      sessions[0] if sessions else "COP30",
        "subsidiary_body":  None,
        "document_type":    "web_article",
        "date":             manifest_entry.get("retrieved_at", "")[:10] or "2026-04-25",
        "authors":          _infer_authors(source_type),
        "topics":           topics if topics else ["adaptation"],
        "topic_tags":       topics,
        "country_authors_initial": countries,
        "groups_referenced": groups,
        "language":         "en",
        "paragraphs":       paras,
        "paragraphs_total_raw": len(paras),
        "paragraphs_selected":  len(paras),
        "url":              manifest_entry.get("source_url", ""),
        "retrieved_at":     manifest_entry.get("retrieved_at", ""),
        "sha256":           sha256_of_text(full_text),
        "sha256_raw_file":  manifest_entry.get("sha256", ""),
        "filesize_bytes":   manifest_entry.get("filesize_bytes", 0),
        "processing_version": "round1-v1.0",
        "processed_at":     datetime.now(timezone.utc).isoformat(),
        "extraction_note":  f"{len(paras)} paragraphs extracted from HTML.",
    }

def _infer_authors(source_type: str) -> list[str]:
    if source_type == "cop30_official":
        return ["Brazil (COP30 Presidency)"]
    if source_type == "castro_2025":
        return ["Castro et al. 2025"]
    return ["Unknown"]

# ---------------------------------------------------------------------------
# 품질 게이트
# ---------------------------------------------------------------------------
_MIN_PARA_TEXT_LEN = 200

def passes_quality_gate(doc: dict) -> tuple[bool, str]:
    text_len = sum(len(p["text"]) for p in doc.get("paragraphs", []))
    if text_len < _MIN_PARA_TEXT_LEN:
        return False, f"total paragraph text {text_len} < {_MIN_PARA_TEXT_LEN}"
    if not doc.get("topic_tags"):
        return False, "no topic_tags"
    return True, "ok"

# ---------------------------------------------------------------------------
# 메인 실행
# ---------------------------------------------------------------------------
def load_manifest() -> dict[str, dict]:
    entries = {}
    with open(MANIFEST, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entry = json.loads(line)
                entries[entry["doc_id"]] = entry
    return entries

def main():
    manifest = load_manifest()
    records     = []
    rejected    = []
    stats = {
        "input_total": 7,
        "pdf_attempted": 0,
        "html_attempted": 0,
        "success": 0,
        "rejected": 0,
        "rejected_reasons": [],
        "topic_distribution": defaultdict(int),
        "country_frequency": defaultdict(int),
        "group_frequency": defaultdict(int),
        "by_source": defaultdict(int),
        "avg_para_count": 0,
        "processing_version": "round1-v1.0",
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }

    # ------ PDF 처리 ------
    pdf_files = sorted(RAW_IPCC.glob("*.pdf"))
    print(f"[INFO] Found {len(pdf_files)} PDFs", file=sys.stderr)
    for pdf_path in pdf_files:
        stats["pdf_attempted"] += 1
        # manifest entry 찾기 (raw_file_path 매칭)
        entry = next(
            (e for e in manifest.values()
             if Path(e.get("raw_file_path", "")).name == pdf_path.name),
            None,
        )
        if entry is None:
            print(f"[WARN] No manifest entry for {pdf_path.name}", file=sys.stderr)
            entry = {
                "doc_id": f"ipcc_ar6_wg2-{pdf_path.stem}",
                "source_url": "",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "sha256": "",
                "filesize_bytes": pdf_path.stat().st_size,
            }

        doc = extract_pdf(pdf_path, entry)
        if doc is None:
            stats["rejected"] += 1
            stats["rejected_reasons"].append(
                {"doc_id": entry["doc_id"], "reason": "extraction_failed"}
            )
            continue

        ok, reason = passes_quality_gate(doc)
        if not ok:
            stats["rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": doc["doc_id"], "reason": reason})
            rejected.append(doc)
            (REJECTED / f"{doc['doc_id']}.json").write_text(
                json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            continue

        records.append(doc)
        stats["success"] += 1
        stats["by_source"]["ipcc_ar6_wg2"] += 1
        for t in doc["topic_tags"]:
            stats["topic_distribution"][t] += 1
        for c in doc["country_authors_initial"]:
            stats["country_frequency"][c] += 1
        for g in doc["groups_referenced"]:
            stats["group_frequency"][g] += 1
        print(f"[OK] {doc['doc_id']} | topics={doc['topic_tags']} | paras={doc['paragraphs_selected']}", file=sys.stderr)

    # ------ HTML 처리 ------
    html_sources = [
        (RAW_COP30 / "en_news_about_cop30.html", "cop30_official-48e357da95f6"),
        (RAW_COP30 / "en_news_about_cop30_cop30_approves_belem_package1.html", "cop30_official-3312641d06a8"),
        (RAW_CASTRO / "castro_2025_article.html", "castro_2025-8e8f9da2cd34"),
    ]

    for html_path, doc_id in html_sources:
        stats["html_attempted"] += 1
        entry = manifest.get(doc_id, {
            "doc_id": doc_id,
            "source_url": "",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "sha256": "",
            "filesize_bytes": html_path.stat().st_size if html_path.exists() else 0,
            "source_type": "unknown",
        })

        doc = extract_html(html_path, entry)
        if doc is None:
            stats["rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": doc_id, "reason": "extraction_failed"})
            continue

        ok, reason = passes_quality_gate(doc)
        if not ok:
            stats["rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": doc["doc_id"], "reason": reason})
            rejected.append(doc)
            (REJECTED / f"{doc['doc_id']}.json").write_text(
                json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            continue

        records.append(doc)
        stats["success"] += 1
        stats["by_source"][doc["source_type"]] += 1
        for t in doc["topic_tags"]:
            stats["topic_distribution"][t] += 1
        for c in doc["country_authors_initial"]:
            stats["country_frequency"][c] += 1
        for g in doc["groups_referenced"]:
            stats["group_frequency"][g] += 1
        print(f"[OK] {doc['doc_id']} | topics={doc['topic_tags']} | paras={len(doc['paragraphs'])}", file=sys.stderr)

    # ------ documents.jsonl 저장 ------
    out_path = OUT_DIR / "documents.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[INFO] Written {len(records)} records to {out_path}", file=sys.stderr)

    # ------ 통계 계산 ------
    if records:
        stats["avg_para_count"] = round(
            sum(r["paragraphs_selected"] for r in records) / len(records), 1
        )

    stats["topic_distribution"] = dict(stats["topic_distribution"])
    stats["country_frequency"]  = dict(stats["country_frequency"])
    stats["group_frequency"]    = dict(stats["group_frequency"])
    stats["by_source"]          = dict(stats["by_source"])

    # coverage gap
    all_issues = list(ISSUE_KEYWORDS.keys())
    stats["coverage_gap"] = [
        issue for issue in all_issues
        if stats["topic_distribution"].get(issue, 0) == 0
    ]

    stats_path = OUT_DIR / "refinement_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Stats written to {stats_path}", file=sys.stderr)

    # ------ 결과 출력 ------
    print("\n=== Round 1 Refinement Summary ===", file=sys.stderr)
    print(f"  Input files   : {stats['input_total']}", file=sys.stderr)
    print(f"  Success       : {stats['success']}", file=sys.stderr)
    print(f"  Rejected      : {stats['rejected']}", file=sys.stderr)
    print(f"  Topic dist    : {stats['topic_distribution']}", file=sys.stderr)
    print(f"  Coverage gaps : {stats['coverage_gap']}", file=sys.stderr)

    # return stats for report generation
    return records, stats

if __name__ == "__main__":
    main()
