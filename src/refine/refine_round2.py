"""CINA Round 2 — Data Refinement Pipeline (rules-based, no LLM).

입력  : data/manifest/manifest.jsonl (91 entries)
       data/raw/**  (84 new files: ndcs, unfccc_curated, ipcc_ar6, cop30, enb, korean_gov, etc.)
출력  : data/processed/documents.jsonl          (appended: 84 new + 7 existing = 91)
       data/processed/refinement_round2_stats.json
       data/processed/uae_belem_indicators.jsonl
       data/processed/ndc_adaptation_sections.jsonl
       data/processed/chair_metadata.jsonl
       data/processed/extraction_targets.jsonl
       data/processed/country_issue_matrix.csv
로그  : stderr
버전  : round2-v1.3
"""
from __future__ import annotations

import csv
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
    GROUP_MEMBERSHIP,
)

MANIFEST      = BASE / "data/manifest/manifest.jsonl"
OUT_DIR       = BASE / "data/processed"
REJECTED_DIR  = OUT_DIR / "rejected"
EXISTING_DOCS = OUT_DIR / "documents.jsonl"

OUT_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)

PROCESSING_VERSION = "round2-v1.3"

# ---------------------------------------------------------------------------
# 헬퍼: SHA-256 (내용 기반)
# ---------------------------------------------------------------------------
def sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# ---------------------------------------------------------------------------
# 헬퍼: 단락 분할
# ---------------------------------------------------------------------------
_PARA_SPLIT = re.compile(r"\n{2,}")
_NUMBERED_PARA = re.compile(r"\n\s*(?:\d+\.|\([a-z]+\)|\([ivxlcdm]+\))\s+")

def split_paragraphs(text: str, min_len: int = 40) -> list[dict]:
    """2-blank-line split + numbered-paragraph pattern split."""
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
# v1.3 Schema: instrument_signals (NATO keywords)
# ---------------------------------------------------------------------------
_NODALITY_KW  = ["report", "indicator", "data", "transparency", "MRV",
                 "information", "track", "monitor", "scientific", "evidence",
                 "database", "registry", "communication"]
_AUTHORITY_KW = ["mandatory", "shall", "obligation", "binding", "agreement",
                 "decision", "require", "compliance", "protocol", "regulation",
                 "legally binding", "commit"]
_TREASURE_KW  = ["finance", "fund", "billion", "USD", "million", "tripling",
                 "doubling", "GCF", "NCQG", "resources", "investment",
                 "contribution", "budget", "grant", "loan"]
_ORG_KW       = ["committee", "expert group", "secretariat", "establish",
                 "operationalize", "working group", "body", "taskforce",
                 "institution", "mechanism", "LEG", "PCCB", "AC"]

def count_instrument_signals(text: str) -> dict:
    lower = text.lower()
    return {
        "nodality":    sum(1 for kw in _NODALITY_KW  if kw.lower() in lower),
        "authority":   sum(1 for kw in _AUTHORITY_KW if kw.lower() in lower),
        "treasure":    sum(1 for kw in _TREASURE_KW  if kw.lower() in lower),
        "organization":sum(1 for kw in _ORG_KW       if kw.lower() in lower),
    }

def classify_frame(text: str) -> str:
    lower = text.lower()
    scores = {
        "scientific":  sum(1 for kw in ["ipcc", "science", "evidence", "temperature", "1.5", "scenario", "model", "assessment"]
                           if kw in lower),
        "justice":     sum(1 for kw in ["common but differentiated", "historical responsibility", "vulnerability", "equity",
                                         "loss and damage", "climate justice", "developing countries should not"]
                           if kw in lower),
        "sovereignty": sum(1 for kw in ["national circumstances", "respective capabilities", "subject to", "voluntary",
                                         "non-prescriptive", "national determination", "sovereign"]
                           if kw in lower),
        "development": sum(1 for kw in ["developing countries", "poverty", "industrialization", "development pathway",
                                         "sustainable development", "economic growth", "livelihood"]
                           if kw in lower),
    }
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if top[0][1] == 0:
        return "mixed"
    if top[0][1] > 0 and top[1][1] > 0 and (top[0][1] - top[1][1]) <= 1:
        return "mixed"
    return top[0][0]

def detect_procedural_signals(text: str, meta: dict) -> dict:
    lower = text.lower()
    fname = meta.get("raw_file_path", "").replace("\\", "/")
    fname_lower = fname.lower()

    is_chair = any(kw in lower for kw in [
        "presidency", "belem letter", "cop30 presidency", "presiding officer",
        "chair proposes", "co-facilitator", "the chair", "co-chair"
    ])
    is_pen_holder = any(kw in lower for kw in [
        "draft decision", "draft text", "l-document", "advance unedited",
        "parties may wish to consider", "informal note"
    ]) or "_L" in fname or "advance" in fname_lower

    procedural_phrases = []
    patterns = [
        r"parties may wish to consider[^.]*\.",
        r"the chair proposes[^.]*\.",
        r"co-facilitator[^.]*\.",
        r"draft decision[^.]*\.",
        r"belem[^.]*presidency[^.]*\.",
    ]
    for pat in patterns:
        m = re.search(pat, lower)
        if m:
            procedural_phrases.append(text[m.start():m.end()].strip()[:200])

    return {
        "is_chair_role":     is_chair,
        "is_co_facilitator": "co-facilitator" in lower,
        "is_pen_holder":     is_pen_holder,
        "procedural_phrases": procedural_phrases[:3],
    }

# ---------------------------------------------------------------------------
# 헬퍼: 토픽 태깅
# ---------------------------------------------------------------------------
def tag_topics(text: str) -> list[str]:
    lower = text.lower()
    matched = []
    for issue_code, kws in ISSUE_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in lower:
                matched.append(issue_code)
                break
    return matched

# ---------------------------------------------------------------------------
# 헬퍼: 국가·그룹 인식
# ---------------------------------------------------------------------------
_COUNTRY_ALIASES: dict[str, str] = {
    "eu": "EU", "european union": "EU",
    "united states": "USA", "united states of america": "USA", "u.s.": "USA",
    "brazil": "BRA", "brasil": "BRA",
    "china": "CHN",
    "india": "IND",
    "japan": "JPN",
    "korea": "KOR", "republic of korea": "KOR", "south korea": "KOR",
    "australia": "AUS",
    "canada": "CAN",
    "norway": "NOR",
    "switzerland": "CHE",
    "mexico": "MEX",
    "south africa": "ZAF",
    "saudi arabia": "SAU",
    "united arab emirates": "ARE", "uae": "ARE",
    "egypt": "EGY",
    "colombia": "COL",
    "chile": "CHL",
    "costa rica": "CRI",
    "kenya": "KEN",
    "turkey": "TUR", "türkiye": "TUR",
    "bahamas": "BHS",
    "sierra leone": "SLE",
    "rwanda": "RWA",
    "bahrain": "BHR",
    "kazakhstan": "KAZ",
    "qatar": "QAT",
    "yemen": "YEM",
    "fiji": "FJI",
    "georgia": "GEO",
    "mauritania": "MRT",
    "mozambique": "MOZ",
    "ukraine": "UKR",
    "burundi": "BDI",
    "guinea": "GIN",
    "djibouti": "DJI",
    "gabon": "GAB",
    "suriname": "SUR",
    "uzbekistan": "UZB",
    "azerbaijan": "AZE",
    "comoros": "COM",
    "belarus": "BLR",
    "armenia": "ARM",
    "honduras": "HND",
    "nauru": "NRU",
    "palau": "PLW",
    "samoa": "WSM",
    "thailand": "THA",
    "trinidad and tobago": "TTO",
    "zambia": "ZMB",
    "congo": "COG",
    "eritrea": "ERI",
    "el salvador": "SLV",
    "cabo verde": "CPV",
    "paraguay": "PRY",
    "burkina faso": "BFA",
    "cote d'ivoire": "CIV", "côte d'ivoire": "CIV",
}

_GROUP_ALIASES: dict[str, str] = {
    "g77": "g77", "g77+china": "g77",
    "aosis": "aosis",
    "ldc": "ldc", "least developed countries": "ldc",
    "african group": "african",
    "arab group": "arab",
    "ailac": "ailac",
    "basic": "basic",
    "lmdc": "lmdc", "like-minded developing countries": "lmdc",
    "umbrella": "umbrella", "umbrella group": "umbrella",
    "high ambition coalition": "hac",
    "eig": "eig", "environmental integrity group": "eig",
    "amazon": "amazon",
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

def extract_sessions(text: str) -> list[str]:
    _SESSION_RE = re.compile(r"\b(COP\s*\d+|SBI\s*\d+|SBSTA\s*\d+|CMA\s*\d+)\b", re.IGNORECASE)
    raw = _SESSION_RE.findall(text)
    normalized = [re.sub(r"\s+", "", s.upper()) for s in raw]
    valid = [s for s in normalized if s in CINA_SESSIONS]
    return sorted(set(valid))

# ---------------------------------------------------------------------------
# PDF 추출 (PyMuPDF)
# ---------------------------------------------------------------------------
import fitz

def extract_pdf_text(path: Path) -> tuple[str, int]:
    """Returns (full_text, page_count). full_text may be empty."""
    try:
        doc = fitz.open(str(path))
        pages = [page.get_text("text") for page in doc]
        doc.close()
        full = "\n\n".join(pages).strip()
        return full, len(pages)
    except Exception as e:
        print(f"[ERROR] PDF open failed: {path.name}: {e}", file=sys.stderr)
        return "", 0

def make_pdf_document(path: Path, entry: dict, source_type: str,
                      document_type: str = "unfccc_decision",
                      date: str = "2025-11-01") -> dict | None:
    full_text, page_count = extract_pdf_text(path)
    if len(full_text) < 200:
        print(f"[WARN] PDF too short (<200 chars): {path.name}", file=sys.stderr)
        return None

    all_paras = split_paragraphs(full_text)
    total = len(all_paras)

    # Select: head50 + tail30 + keyword-match
    kw_all   = [kw.lower() for kws in ISSUE_KEYWORDS.values() for kw in kws]
    kw_set   = set()
    for i, p in enumerate(all_paras):
        t = p["text"].lower()
        if any(kw in t for kw in kw_all):
            kw_set.add(i)

    head_set = set(range(0, min(50, total)))
    tail_set = set(range(max(0, total - 30), total))
    selected_idx = sorted(head_set | tail_set | kw_set)
    selected_paras = [{"para_id": new_id, "text": all_paras[old_idx]["text"]}
                      for new_id, old_idx in enumerate(selected_idx, start=1)]

    extracted_text = " ".join(p["text"] for p in selected_paras)
    topics   = tag_topics(extracted_text)
    countries = identify_countries(extracted_text)
    groups   = identify_groups(extracted_text)
    sessions = extract_sessions(extracted_text)

    # v1.3 fields
    instr = count_instrument_signals(extracted_text)
    frame = classify_frame(extracted_text)
    proc  = detect_procedural_signals(extracted_text, entry)

    # Infer country from manifest
    manifest_iso3 = entry.get("iso3", "")
    if manifest_iso3 and manifest_iso3 not in ("UNK", "") and manifest_iso3 not in countries:
        countries = sorted(set(countries) | {manifest_iso3})

    authors = _infer_authors_from_entry(entry, source_type)

    return {
        "doc_id":          entry["doc_id"],
        "source":          source_type,
        "source_type":     source_type,
        "cop_session":     sessions[0] if sessions else entry.get("session", "COP30"),
        "subsidiary_body": _infer_subsidiary_body(entry.get("raw_file_path", "")),
        "document_type":   document_type,
        "date":            _infer_date(entry, date),
        "authors":         authors,
        "topics":          topics if topics else ["adaptation"],
        "topic_tags":      topics,
        "country_authors_initial": countries,
        "groups_referenced":       groups,
        "language":        _infer_language(path.name, full_text),
        "paragraphs":      selected_paras,
        "paragraphs_total_raw":   total,
        "paragraphs_selected":    len(selected_paras),
        "page_count":      page_count,
        "url":             entry.get("source_url", ""),
        "retrieved_at":    entry.get("retrieved_at", ""),
        "sha256":          sha256_of_text(full_text),
        "sha256_raw_file": entry.get("sha256", ""),
        "filesize_bytes":  entry.get("filesize_bytes", 0),
        # v1.3 Stage 1 pre-fill
        "instrument_signals": instr,
        "frame_type":         frame,
        "salience_score":     _estimate_salience(topics, selected_paras, kw_set, total),
        "procedural_signals": proc,
        "processing_version": PROCESSING_VERSION,
        "processed_at":       datetime.now(timezone.utc).isoformat(),
        "extraction_note":    (
            f"Selected {len(selected_paras)}/{total} paras "
            f"(head50+tail30+kw_match={len(kw_set)}). pages={page_count}."
        ),
    }

def _infer_subsidiary_body(raw_path: str) -> str | None:
    r = raw_path.upper()
    if "SBI" in r: return "SBI"
    if "SBSTA" in r: return "SBSTA"
    if "CMA" in r: return "CMA"
    if "COP" in r: return "COP"
    return None

def _infer_date(entry: dict, default: str) -> str:
    ret = entry.get("retrieved_at", "")[:10]
    sub = entry.get("submission_year_month", "")
    if sub:
        return sub + "-01"
    return ret or default

def _infer_language(filename: str, text: str) -> str:
    # Heuristic: check for common French/Spanish/Arabic words in first 500 chars
    sample = text[:500].lower()
    if any(w in sample for w in ["les ", "des ", "est ", "dans ", "pour "]):
        return "fr"
    if any(w in sample for w in [" los ", " las ", " del ", " para ", " que "]):
        return "es"
    # Korean
    if any('가' <= c <= '힣' for c in sample):
        return "ko"
    # Arabic (rough: any Arabic script)
    if any('؀' <= c <= 'ۿ' for c in sample):
        return "ar"
    # Cyrillic
    if any('Ѐ' <= c <= 'ӿ' for c in sample):
        return "ru"
    return "en"

def _estimate_salience(topics: list[str], paras: list[dict],
                       kw_set: set, total: int) -> float:
    """Rough salience: keyword paragraph density."""
    if total == 0:
        return 0.0
    return round(min(1.0, len(kw_set) / max(1, total)), 3)

def _infer_authors_from_entry(entry: dict, source_type: str) -> list[str]:
    iso3 = entry.get("iso3", "")
    if iso3 and iso3 not in ("UNK", ""):
        name = CINA_COUNTRIES.get(iso3, {}).get("name", iso3)
        return [name]
    title = entry.get("title", "")
    if source_type == "cop30_curated":
        return ["UNFCCC / COP30 Presidency"]
    if source_type == "ipcc_ar6_wg2":
        return ["IPCC WG2"]
    if source_type in ("cop30_official", "brazilian_gov"):
        return ["Brazil (COP30 Presidency)"]
    if source_type == "castro_2025":
        return ["Castro et al. 2025"]
    if source_type == "enb":
        return ["IISD ENB"]
    if source_type == "korean_gov":
        return ["Republic of Korea MOFA"]
    if title:
        return [title[:60]]
    return ["Unknown"]

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

def make_html_document(path: Path, entry: dict, source_type: str) -> dict | None:
    try:
        raw_bytes = path.read_bytes()
        html = raw_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"[ERROR] HTML read: {path.name}: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header",
                     "aside", "form", "button", "iframe"]):
        tag.decompose()

    body = soup.find("main") or soup.find("article") or soup.find("body")
    if body is None:
        print(f"[WARN] No body: {path.name}", file=sys.stderr)
        return None

    texts = []
    for elem in body.find_all(["p", "h1", "h2", "h3", "h4", "li", "blockquote", "td"]):
        t = elem.get_text(separator=" ", strip=True)
        if t and len(t) > 20 and not _BOILERPLATE_RE.search(t):
            texts.append(t)

    full_text = "\n\n".join(texts).strip()
    if len(full_text) < 200:
        print(f"[WARN] HTML too short: {path.name}", file=sys.stderr)
        return None

    paras    = split_paragraphs(full_text)
    topics   = tag_topics(full_text)
    countries = identify_countries(full_text)
    groups   = identify_groups(full_text)
    sessions = extract_sessions(full_text)

    kw_all = [kw.lower() for kws in ISSUE_KEYWORDS.values() for kw in kws]
    kw_count = sum(1 for p in paras if any(kw in p["text"].lower() for kw in kw_all))
    instr = count_instrument_signals(full_text)
    frame = classify_frame(full_text)
    proc  = detect_procedural_signals(full_text, entry)

    return {
        "doc_id":          entry["doc_id"],
        "source":          source_type,
        "source_type":     source_type,
        "cop_session":     sessions[0] if sessions else "COP30",
        "subsidiary_body": None,
        "document_type":   "web_article",
        "date":            entry.get("retrieved_at", "")[:10] or "2026-04-25",
        "authors":         _infer_authors_from_entry(entry, source_type),
        "topics":          topics if topics else ["adaptation"],
        "topic_tags":      topics,
        "country_authors_initial": countries,
        "groups_referenced":       groups,
        "language":        "en",
        "paragraphs":      paras,
        "paragraphs_total_raw":   len(paras),
        "paragraphs_selected":    len(paras),
        "url":             entry.get("source_url", ""),
        "retrieved_at":    entry.get("retrieved_at", ""),
        "sha256":          sha256_of_text(full_text),
        "sha256_raw_file": entry.get("sha256", ""),
        "filesize_bytes":  entry.get("filesize_bytes", 0),
        # v1.3
        "instrument_signals": instr,
        "frame_type":         frame,
        "salience_score":     round(min(1.0, kw_count / max(1, len(paras))), 3),
        "procedural_signals": proc,
        "processing_version": PROCESSING_VERSION,
        "processed_at":       datetime.now(timezone.utc).isoformat(),
        "extraction_note":    f"{len(paras)} paras from HTML.",
    }

# ---------------------------------------------------------------------------
# 품질 게이트
# ---------------------------------------------------------------------------
def passes_quality_gate(doc: dict) -> tuple[bool, str]:
    text_len = sum(len(p["text"]) for p in doc.get("paragraphs", []))
    if text_len < 200:
        return False, f"total_text {text_len} < 200"
    return True, "ok"

# ---------------------------------------------------------------------------
# UAE-Belém 지표 추출 (9a/9b/9c/9e)
# ---------------------------------------------------------------------------
# Pattern: lines that look like indicator rows — numbered or bullet items
_INDICATOR_BULLET = re.compile(
    r"(?:^|\n)\s*(?:\d+\.\d+|\d+\.|[•\-\*]|\([a-z]\))\s+(.{20,200})",
    re.MULTILINE
)
_HEADLINE_RE = re.compile(
    r"(?:headline|key|primary|core)\s+indicator[s]?\s*[:\-]?\s*(.{10,200})",
    re.IGNORECASE
)
_SUB_INDICATOR_RE = re.compile(
    r"(?:sub|supporting|secondary)\s*[\-\s]?indicator[s]?\s*[:\-]?\s*(.{10,200})",
    re.IGNORECASE
)

def extract_uae_belem_indicators(path: Path, target_code: str, doc_id: str) -> list[dict]:
    """Extract indicator entries from a UAE-Belém thematic PDF."""
    full_text, _ = extract_pdf_text(path)
    if not full_text:
        return []

    indicators = []
    # Strategy: find numbered / bullet items in the text
    bullets = _INDICATOR_BULLET.findall(full_text)
    for i, b in enumerate(bullets):
        b = b.strip()
        if len(b) < 20:
            continue
        # Classify as headline or sub-indicator
        kind = "indicator"
        if any(w in b.lower() for w in ["headline", "primary", "core"]):
            kind = "headline"
        elif any(w in b.lower() for w in ["sub", "secondary", "supporting"]):
            kind = "sub_indicator"
        indicators.append({
            "target":      target_code,
            "doc_id":      doc_id,
            "seq":         i + 1,
            "kind":        kind,
            "text":        b[:300],
            "sector":      _target_sector(target_code),
        })

    # De-dup by text prefix
    seen = set()
    unique = []
    for ind in indicators:
        key = ind["text"][:60]
        if key not in seen:
            seen.add(key)
            unique.append(ind)

    print(f"[UAE-Belém] {target_code}: {len(unique)} indicators from {path.name}",
          file=sys.stderr)
    return unique

def _target_sector(code: str) -> str:
    return {
        "9a": "Water supply and sanitation",
        "9b": "Food and agriculture",
        "9c": "Health",
        "9d": "Ecosystems and biodiversity",
        "9e": "Infrastructure and human settlements",
    }.get(code, "Unknown")

# ---------------------------------------------------------------------------
# NDC 적응 섹션 추출
# ---------------------------------------------------------------------------
_ADAPT_HEADER = re.compile(
    r"(?:^|\n)\s*(?:\d+\.?\s+)?(?:ADAPTATION|Adaptation|adaptation)\b.*(?:\n|$)",
    re.MULTILINE
)
_SECTION_BREAK = re.compile(
    r"(?:^|\n)\s*(?:\d+\.?\s+)?(?:MITIGATION|FINANCE|TRANSPARENCY|LOSS AND DAMAGE|APPENDIX|ANNEX)\b",
    re.IGNORECASE | re.MULTILINE
)

def extract_ndc_adaptation(path: Path, entry: dict) -> dict | None:
    """Extract adaptation section from an NDC PDF. Returns jsonl record or None."""
    full_text, page_count = extract_pdf_text(path)
    if not full_text:
        return None

    # Find start of adaptation section
    m = _ADAPT_HEADER.search(full_text)
    if not m:
        # Try softer search
        idx = full_text.lower().find("adaptation")
        if idx == -1:
            return None
        m_start = max(0, idx - 20)
    else:
        m_start = m.start()

    adapt_text_raw = full_text[m_start:]

    # Find end: next major section break after adaptation start
    m_end = _SECTION_BREAK.search(adapt_text_raw, 1)
    if m_end:
        adapt_text = adapt_text_raw[:m_end.start()]
    else:
        # Take up to 8000 chars (adaptation section shouldn't be the whole doc)
        adapt_text = adapt_text_raw[:8000]

    adapt_text = adapt_text.strip()
    if len(adapt_text) < 150:
        return None

    paras = split_paragraphs(adapt_text)
    topics = tag_topics(adapt_text)
    instr  = count_instrument_signals(adapt_text)
    frame  = classify_frame(adapt_text)

    iso3 = entry.get("iso3", "UNK")
    country_name = CINA_COUNTRIES.get(iso3, {}).get("name", iso3)

    return {
        "doc_id":          entry["doc_id"],
        "iso3":            iso3,
        "country":         country_name,
        "title":           entry.get("title", path.stem),
        "submission_year_month": entry.get("submission_year_month", ""),
        "language":        _infer_language(path.name, adapt_text),
        "adaptation_section_length_chars": len(adapt_text),
        "paragraphs":      paras[:30],   # cap at 30 paras for jsonl size
        "topics":          topics,
        "instrument_signals_adapt": instr,
        "frame_type_adapt": frame,
        "source_url":      entry.get("source_url", ""),
        "processed_at":    datetime.now(timezone.utc).isoformat(),
    }

# ---------------------------------------------------------------------------
# ENB 협상 그룹 입장 추출
# ---------------------------------------------------------------------------
_GROUP_SECTION = re.compile(
    r"(?:G77|AOSIS|EU|European Union|AILAC|LMDC|LDC|Arab Group|Umbrella|African Group|"
    r"High Ambition|Brazil|India|China|United States)[^.]{0,300}\.",
    re.IGNORECASE
)

def extract_enb_sections(path: Path, entry: dict) -> dict | None:
    """For large ENB HTML: extract sections by keyword headings."""
    try:
        raw_bytes = path.read_bytes()
        html = raw_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"[ERROR] ENB HTML: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    full_text = soup.get_text(separator="\n")

    # Find adaptation-related sections
    sections = {}
    section_patterns = {
        "adaptation":        r"(?:^|\n)([^\n]*\bAdaptation\b[^\n]*\n(?:[^\n]+\n){1,50})",
        "global_goal":       r"(?:^|\n)([^\n]*\bGlobal Goal\b[^\n]*\n(?:[^\n]+\n){1,50})",
        "belem_indicators":  r"(?:^|\n)([^\n]*\bBelém Indicators?\b[^\n]*\n(?:[^\n]+\n){1,50})",
        "loss_and_damage":   r"(?:^|\n)([^\n]*\bLoss and Damage\b[^\n]*\n(?:[^\n]+\n){1,50})",
    }
    for sec_name, pat in section_patterns.items():
        m = re.search(pat, full_text, re.IGNORECASE | re.MULTILINE)
        if m:
            sections[sec_name] = m.group(0).strip()[:2000]

    # Extract group positions
    group_mentions = {}
    for grp_pat in _GROUP_SECTION.finditer(full_text):
        sentence = grp_pat.group(0).strip()
        for alias in ["G77", "AOSIS", "EU", "AILAC", "LMDC", "LDC",
                       "Arab Group", "African Group", "Umbrella Group",
                       "High Ambition", "Brazil", "India", "China"]:
            if alias.lower() in sentence.lower():
                if alias not in group_mentions:
                    group_mentions[alias] = []
                if len(group_mentions[alias]) < 5:
                    group_mentions[alias].append(sentence[:300])

    paras = split_paragraphs(full_text)
    topics = tag_topics(full_text)
    countries = identify_countries(full_text)
    groups = identify_groups(full_text)
    sessions = extract_sessions(full_text)
    instr = count_instrument_signals(full_text)
    frame = classify_frame(full_text)
    proc  = detect_procedural_signals(full_text, entry)

    # build full doc record
    doc = {
        "doc_id":          entry["doc_id"],
        "source":          "enb",
        "source_type":     "enb",
        "cop_session":     sessions[0] if sessions else "COP30",
        "subsidiary_body": None,
        "document_type":   "enb_report",
        "date":            entry.get("retrieved_at", "")[:10] or "2025-11-22",
        "authors":         ["IISD ENB"],
        "topics":          topics if topics else ["adaptation"],
        "topic_tags":      topics,
        "country_authors_initial": countries,
        "groups_referenced":       groups,
        "language":        "en",
        "paragraphs":      paras[:100],
        "paragraphs_total_raw":   len(paras),
        "paragraphs_selected":    min(100, len(paras)),
        "url":             entry.get("source_url", ""),
        "retrieved_at":    entry.get("retrieved_at", ""),
        "sha256":          sha256_of_text(full_text),
        "sha256_raw_file": entry.get("sha256", ""),
        "filesize_bytes":  entry.get("filesize_bytes", 0),
        # ENB-specific
        "enb_sections":    sections,
        "group_positions": group_mentions,
        # v1.3
        "instrument_signals": instr,
        "frame_type":         frame,
        "salience_score":     round(min(1.0, len(topics) / 6.0), 3),
        "procedural_signals": proc,
        "processing_version": PROCESSING_VERSION,
        "processed_at":       datetime.now(timezone.utc).isoformat(),
        "extraction_note":    f"ENB report. {len(paras)} paras. {len(sections)} thematic sections. {len(group_mentions)} groups w/ positions.",
    }
    return doc

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

def load_existing_doc_ids() -> set[str]:
    """Load doc_ids already processed in Round 1."""
    ids = set()
    if EXISTING_DOCS.exists():
        with open(EXISTING_DOCS, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        d = json.loads(line)
                        ids.add(d["doc_id"])
                    except Exception:
                        pass
    return ids


def main():
    manifest = load_manifest()
    existing_ids = load_existing_doc_ids()
    print(f"[INFO] Manifest: {len(manifest)} entries. Already processed: {len(existing_ids)}",
          file=sys.stderr)

    new_records     = []
    rejected        = []
    ndc_sections    = []
    uae_indicators  = []
    chair_metadata  = []

    stats = {
        "round": 2,
        "input_manifest": len(manifest),
        "existing_round1": len(existing_ids),
        "new_attempted": 0,
        "new_success": 0,
        "new_rejected": 0,
        "rejected_reasons": [],
        "topic_distribution": defaultdict(int),
        "country_frequency": defaultdict(int),
        "group_frequency": defaultdict(int),
        "by_source": defaultdict(int),
        "frame_distribution": defaultdict(int),
        "instrument_totals": {"nodality": 0, "authority": 0, "treasure": 0, "organization": 0},
        "ndc_adaptation_detected": 0,
        "ndc_attempted": 0,
        "uae_belem_indicators_total": 0,
        "chair_docs_detected": 0,
        "processing_version": PROCESSING_VERSION,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }

    # ---- Group manifest entries by source type ----
    unfccc_entries  = []
    ndc_entries     = []
    ipcc_entries    = []
    html_entries    = []

    for doc_id, entry in manifest.items():
        if doc_id in existing_ids:
            continue  # skip Round 1 already-done
        st = entry.get("source_type", "")
        fp = entry.get("raw_file_path", "").replace("\\", "/")
        fmt = entry.get("file_format", "")
        suffix = Path(fp).suffix.lower() if fp else ""

        if suffix == ".pdf" or fmt == "pdf":
            if st == "cop30_curated":
                unfccc_entries.append(entry)
            elif st in ("ndc",):
                ndc_entries.append(entry)
            elif st == "ipcc_ar6_wg2":
                ipcc_entries.append(entry)
            else:
                # Generic PDF (brazilian_gov, korean_gov with PDF etc.)
                unfccc_entries.append(entry)
        elif suffix == ".html" or fmt == "html" or ".html" in fp:
            html_entries.append(entry)
        else:
            # Unknown — try to guess
            if fp.endswith(".pdf"):
                unfccc_entries.append(entry)
            else:
                html_entries.append(entry)

    print(f"[INFO] To process: {len(unfccc_entries)} UNFCCC PDFs, {len(ndc_entries)} NDCs, "
          f"{len(ipcc_entries)} IPCC, {len(html_entries)} HTMLs", file=sys.stderr)

    # ---- Process UNFCCC curated + other PDFs ----
    uae_targets = {"9a": "UAE_Belem_9a_Water.pdf",
                   "9b": "UAE_Belem_9b_Food.pdf",
                   "9c": "UAE_Belem_9c_Health.pdf",
                   "9e": "UAE_Belem_9e_Infrastructure.pdf"}
    uae_target_filenames = set(uae_targets.values())

    for entry in unfccc_entries + ipcc_entries:
        fp = Path(entry.get("raw_file_path", "").replace("\\", "/"))
        if not fp.exists():
            print(f"[WARN] File not found: {fp}", file=sys.stderr)
            stats["new_rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": entry["doc_id"], "reason": "file_not_found"})
            continue

        stats["new_attempted"] += 1
        st = entry.get("source_type", "unknown")
        doc_type = _guess_doc_type(fp.name, st)

        doc = make_pdf_document(fp, entry, st, document_type=doc_type)
        if doc is None:
            stats["new_rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": entry["doc_id"], "reason": "extraction_failed_or_too_short"})
            (REJECTED_DIR / f"{entry['doc_id']}.json").write_text(
                json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            continue

        ok, reason = passes_quality_gate(doc)
        if not ok:
            stats["new_rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": doc["doc_id"], "reason": reason})
            (REJECTED_DIR / f"{doc['doc_id']}.json").write_text(
                json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            continue

        new_records.append(doc)
        stats["new_success"] += 1
        stats["by_source"][st] += 1
        _update_stats(stats, doc)

        # Chair metadata
        if doc["procedural_signals"]["is_chair_role"] or doc["procedural_signals"]["is_pen_holder"]:
            stats["chair_docs_detected"] += 1
            chair_metadata.append({
                "doc_id":    doc["doc_id"],
                "source":    st,
                "is_chair_role":     doc["procedural_signals"]["is_chair_role"],
                "is_pen_holder":     doc["procedural_signals"]["is_pen_holder"],
                "is_co_facilitator": doc["procedural_signals"]["is_co_facilitator"],
                "procedural_phrases": doc["procedural_signals"]["procedural_phrases"],
                "cop_session": doc["cop_session"],
            })

        # UAE-Belém special extraction
        if fp.name in uae_target_filenames:
            for code, fname in uae_targets.items():
                if fp.name == fname:
                    inds = extract_uae_belem_indicators(fp, code, doc["doc_id"])
                    uae_indicators.extend(inds)
                    stats["uae_belem_indicators_total"] += len(inds)
                    break

        print(f"[OK] {doc['doc_id']} | {st} | topics={doc['topic_tags']} | "
              f"paras={doc['paragraphs_selected']} | frame={doc['frame_type']}",
              file=sys.stderr)

    # ---- Process NDC PDFs ----
    for entry in ndc_entries:
        fp = Path(entry.get("raw_file_path", "").replace("\\", "/"))
        if not fp.exists():
            print(f"[WARN] NDC not found: {fp}", file=sys.stderr)
            stats["new_rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": entry["doc_id"], "reason": "file_not_found"})
            continue

        stats["new_attempted"] += 1
        stats["ndc_attempted"] += 1

        doc = make_pdf_document(fp, entry, "ndc", document_type="ndc", date="2025-11-01")
        if doc is None:
            stats["new_rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": entry["doc_id"], "reason": "ndc_extraction_failed"})
            continue

        ok, reason = passes_quality_gate(doc)
        if not ok:
            stats["new_rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": doc["doc_id"], "reason": reason})
            continue

        new_records.append(doc)
        stats["new_success"] += 1
        stats["by_source"]["ndc"] += 1
        _update_stats(stats, doc)

        # NDC adaptation section
        adapt = extract_ndc_adaptation(fp, entry)
        if adapt:
            ndc_sections.append(adapt)
            stats["ndc_adaptation_detected"] += 1

        print(f"[OK-NDC] {doc['doc_id']} | iso3={entry.get('iso3')} | "
              f"adapt={'yes' if adapt else 'no'} | topics={doc['topic_tags']}", file=sys.stderr)

    # ---- Process HTML files ----
    enb_filenames = {
        "enb_belem-un-climate-change-conference-cop30-summary.html",
        "enb_belem-un-climate-change-conference-cop30.html",
        "enb_belem-un-climate-change-conference-cop30-daily-report-15nov2025.html",
        "enb_belem-un-climate-change-conference-cop30-daily-report-21nov2025.html",
    }

    for entry in html_entries:
        fp = Path(entry.get("raw_file_path", "").replace("\\", "/"))
        if not fp.exists():
            print(f"[WARN] HTML not found: {fp}", file=sys.stderr)
            stats["new_rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": entry["doc_id"], "reason": "file_not_found"})
            continue

        stats["new_attempted"] += 1
        st = entry.get("source_type", "unknown")

        if fp.name in enb_filenames or st == "enb":
            doc = extract_enb_sections(fp, entry)
        else:
            doc = make_html_document(fp, entry, st)

        if doc is None:
            stats["new_rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": entry["doc_id"], "reason": "html_extraction_failed"})
            continue

        ok, reason = passes_quality_gate(doc)
        if not ok:
            stats["new_rejected"] += 1
            stats["rejected_reasons"].append({"doc_id": doc["doc_id"], "reason": reason})
            continue

        new_records.append(doc)
        stats["new_success"] += 1
        stats["by_source"][st] += 1
        _update_stats(stats, doc)

        if doc["procedural_signals"]["is_chair_role"] or doc["procedural_signals"]["is_pen_holder"]:
            stats["chair_docs_detected"] += 1
            chair_metadata.append({
                "doc_id":    doc["doc_id"],
                "source":    st,
                "is_chair_role":     doc["procedural_signals"]["is_chair_role"],
                "is_pen_holder":     doc["procedural_signals"]["is_pen_holder"],
                "is_co_facilitator": doc["procedural_signals"]["is_co_facilitator"],
                "procedural_phrases": doc["procedural_signals"]["procedural_phrases"],
                "cop_session": doc["cop_session"],
            })

        print(f"[OK-HTML] {doc['doc_id']} | {st} | topics={doc['topic_tags']} | "
              f"paras={doc['paragraphs_selected']}", file=sys.stderr)

    # ---- Deduplication across new_records ----
    sha_seen: dict[str, str] = {}
    deduped = []
    exact_dups = 0
    for doc in new_records:
        h = doc["sha256"]
        if h in sha_seen:
            exact_dups += 1
            print(f"[DEDUP] {doc['doc_id']} exact dup of {sha_seen[h]}", file=sys.stderr)
        else:
            sha_seen[h] = doc["doc_id"]
            deduped.append(doc)
    stats["deduplication"] = {"exact_duplicates": exact_dups, "after_dedup": len(deduped)}
    new_records = deduped

    # ---- Append to documents.jsonl ----
    with open(EXISTING_DOCS, "a", encoding="utf-8") as f:
        for rec in new_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[INFO] Appended {len(new_records)} new records to {EXISTING_DOCS}", file=sys.stderr)

    # ---- UAE-Belém indicators ----
    uae_out = OUT_DIR / "uae_belem_indicators.jsonl"
    with open(uae_out, "w", encoding="utf-8") as f:
        for ind in uae_indicators:
            f.write(json.dumps(ind, ensure_ascii=False) + "\n")
    print(f"[INFO] UAE-Belém indicators: {len(uae_indicators)} → {uae_out}", file=sys.stderr)

    # ---- NDC adaptation sections ----
    ndc_out = OUT_DIR / "ndc_adaptation_sections.jsonl"
    with open(ndc_out, "w", encoding="utf-8") as f:
        for sec in ndc_sections:
            f.write(json.dumps(sec, ensure_ascii=False) + "\n")
    print(f"[INFO] NDC adaptation sections: {len(ndc_sections)} → {ndc_out}", file=sys.stderr)

    # ---- Chair metadata ----
    chair_out = OUT_DIR / "chair_metadata.jsonl"
    with open(chair_out, "w", encoding="utf-8") as f:
        for cm in chair_metadata:
            f.write(json.dumps(cm, ensure_ascii=False) + "\n")
    print(f"[INFO] Chair metadata: {len(chair_metadata)} → {chair_out}", file=sys.stderr)

    # ---- Country × Issue matrix ----
    country_issue: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    all_records_for_matrix = new_records  # only new — round1 already counted
    for doc in all_records_for_matrix:
        for country in doc.get("country_authors_initial", []):
            for topic in doc.get("topic_tags", []):
                country_issue[country][topic] += 1

    issues = list(ISSUE_KEYWORDS.keys())
    matrix_path = OUT_DIR / "country_issue_matrix.csv"
    with open(matrix_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["country"] + issues)
        for country in sorted(country_issue.keys()):
            row = [country] + [country_issue[country].get(iss, 0) for iss in issues]
            writer.writerow(row)
    print(f"[INFO] Country-issue matrix → {matrix_path}", file=sys.stderr)

    # ---- Extraction targets for Stage 1 ----
    targets: dict[tuple, list[str]] = defaultdict(list)
    for doc in new_records:
        for country in doc.get("country_authors_initial", []):
            for topic in doc.get("topic_tags", []):
                targets[(country, topic)].append(doc["doc_id"])

    targets_path = OUT_DIR / "extraction_targets.jsonl"
    with open(targets_path, "w", encoding="utf-8") as f:
        for (country, issue), doc_ids in sorted(targets.items()):
            f.write(json.dumps({"country": country, "issue": issue,
                                "doc_ids": doc_ids}, ensure_ascii=False) + "\n")
    print(f"[INFO] Extraction targets → {targets_path}", file=sys.stderr)

    # ---- Coverage gap ----
    all_issues = list(ISSUE_KEYWORDS.keys())
    stats["coverage_gap"] = [
        iss for iss in all_issues
        if stats["topic_distribution"].get(iss, 0) == 0
    ]

    # Serialize defaultdicts
    stats["topic_distribution"] = dict(stats["topic_distribution"])
    stats["country_frequency"]  = dict(stats["country_frequency"])
    stats["group_frequency"]    = dict(stats["group_frequency"])
    stats["by_source"]          = dict(stats["by_source"])
    stats["frame_distribution"] = dict(stats["frame_distribution"])

    total_docs = stats["new_success"]
    pass_rate = round(total_docs / max(1, stats["new_attempted"]) * 100, 1)
    stats["schema_pass_rate"] = f"{total_docs}/{stats['new_attempted']} ({pass_rate}%)"
    stats["ndc_adaptation_coverage"] = (
        f"{stats['ndc_adaptation_detected']}/{stats['ndc_attempted']}"
    )
    if new_records:
        stats["avg_para_count"] = round(
            sum(r["paragraphs_selected"] for r in new_records) / len(new_records), 1
        )

    # Write stats
    stats_path = OUT_DIR / "refinement_round2_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Stats → {stats_path}", file=sys.stderr)

    # ---- Summary ----
    print("\n=== Round 2 Refinement Summary ===", file=sys.stderr)
    print(f"  New attempted   : {stats['new_attempted']}", file=sys.stderr)
    print(f"  New success     : {stats['new_success']}", file=sys.stderr)
    print(f"  New rejected    : {stats['new_rejected']}", file=sys.stderr)
    print(f"  Schema pass     : {stats['schema_pass_rate']}", file=sys.stderr)
    print(f"  Topic dist      : {stats['topic_distribution']}", file=sys.stderr)
    print(f"  Frame dist      : {stats['frame_distribution']}", file=sys.stderr)
    print(f"  NDC adapt cover : {stats['ndc_adaptation_coverage']}", file=sys.stderr)
    print(f"  UAE-Belém inds  : {stats['uae_belem_indicators_total']}", file=sys.stderr)
    print(f"  Chair docs      : {stats['chair_docs_detected']}", file=sys.stderr)
    print(f"  Dedup exact     : {stats['deduplication']['exact_duplicates']}", file=sys.stderr)

    return new_records, stats, ndc_sections, uae_indicators


def _guess_doc_type(fname: str, source_type: str) -> str:
    f = fname.lower()
    if source_type == "ipcc_ar6_wg2":
        return "ipcc_chapter"
    if source_type == "ndc":
        return "ndc"
    if "decision" in f or "_l" in f or "cma" in f or "cop" in f:
        return "unfccc_decision"
    if "synthesis" in f or "submission" in f:
        return "synthesis_report"
    if "indicator" in f or "9a" in f or "9b" in f or "9c" in f or "9e" in f or "9d" in f:
        return "indicator_framework"
    return "policy_document"


def _update_stats(stats: dict, doc: dict):
    for t in doc.get("topic_tags", []):
        stats["topic_distribution"][t] += 1
    for c in doc.get("country_authors_initial", []):
        stats["country_frequency"][c] += 1
    for g in doc.get("groups_referenced", []):
        stats["group_frequency"][g] += 1
    stats["frame_distribution"][doc.get("frame_type", "unknown")] += 1
    instr = doc.get("instrument_signals", {})
    for axis in ["nodality", "authority", "treasure", "organization"]:
        stats["instrument_totals"][axis] += instr.get(axis, 0)


if __name__ == "__main__":
    main()
