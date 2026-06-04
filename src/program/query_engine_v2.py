"""CINA Q&A Query Engine v2 — academic-grade backend.

v1 -> v2 upgrades:
  * Backed by v5 dataset (2,400 records, 50 countries x 8 issues x 6 COPs)
  * 7 intents: lookup, compare, recommendation, factoid + trend, coalition, gap
  * Top-k retrieval by relevance scoring (BM25-like weighted overlap)
  * Multi-record citation array (up to 12 records per response)
  * 95% credible interval display per stance
  * NATO 4-axis bar payload for visualisation
  * Frame distribution display
  * Methodology footer per response (model, T, k, retrieved n, prompt version)
  * Deterministic seed -> reproducibility hash per query
  * 50-country / 8-issue / 6-COP alias dictionary

Usage:
    from src.program.query_engine_v2 import answer_question
    r = answer_question("브라질이 GGA 지표에서 한국과 어떻게 다른가?")
    print(r.text); print(r.citations); print(r.methodology)

Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import re
import statistics
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent.parent
DATA  = ROOT / "data" / "processed" / "stances_v5.jsonl"
META  = ROOT / "data" / "processed" / "stances_v5_meta.json"
CORPUS_MANIFEST = ROOT / "data" / "corpus" / "manifest.jsonl"
CORPUS_INDEX    = ROOT / "data" / "corpus" / "search_index.json"
EMBED_NPZ       = ROOT / "data" / "corpus" / "embeddings.npz"
EMBED_INDEX     = ROOT / "data" / "corpus" / "embeddings_index.json"

ENGINE_VERSION = "2.2.0"   # 2.2 = semantic embedding + hybrid retrieval
DEFAULT_COP = "COP30"

# ===========================================================================
# Alias dictionaries (50 countries, 8 issues, 6 COPs)
# ===========================================================================

COUNTRY_ALIASES = {
    # v3 13
    "브라질": "Brazil", "brazil": "Brazil",
    "한국": "Korea", "대한민국": "Korea", "korea": "Korea", "south korea": "Korea",
    "미국": "USA", "usa": "USA", "us ": "USA", "united states": "USA",
    "중국": "China", "china": "China",
    "인도": "India", "india": "India",
    "유럽연합": "EU", "유럽": "EU", " eu ": "EU", "european union": "EU",
    "사우디": "Saudi", "사우디아라비아": "Saudi", "saudi": "Saudi",
    "일본": "Japan", "japan": "Japan",
    "AOSIS": "AOSIS", "aosis": "AOSIS", "군소도서국": "AOSIS",
    "AILAC": "AILAC", "ailac": "AILAC",
    "AGN": "AGN", "agn": "AGN", "아프리카그룹": "AGN",
    "LMDC": "LMDC", "lmdc": "LMDC", "같은마음": "LMDC",
    # v4 17
    "캐나다": "Canada", "canada": "Canada",
    "호주": "Australia", "오스트레일리아": "Australia", "australia": "Australia",
    "노르웨이": "Norway", "norway": "Norway",
    "영국": "UK", "uk": "UK", "united kingdom": "UK",
    "독일": "Germany", "germany": "Germany",
    "프랑스": "France", "france": "France",
    "멕시코": "Mexico", "mexico": "Mexico",
    "인도네시아": "Indonesia", "indonesia": "Indonesia",
    "남아공": "South Africa", "남아프리카": "South Africa", "south africa": "South Africa",
    "이집트": "Egypt", "egypt": "Egypt",
    "튀르키예": "Türkiye", "터키": "Türkiye", "turkey": "Türkiye", "turkiye": "Türkiye",
    "몰디브": "Maldives", "maldives": "Maldives",
    "마샬": "Marshall Is", "마샬군도": "Marshall Is", "marshall": "Marshall Is",
    "투발루": "Tuvalu", "tuvalu": "Tuvalu",
    "방글라데시": "Bangladesh", "bangladesh": "Bangladesh",
    "에티오피아": "Ethiopia", "ethiopia": "Ethiopia",
    "네팔": "Nepal", "nepal": "Nepal",
    # v5 new 20
    "스위스": "Switzerland", "switzerland": "Switzerland",
    "스페인": "Spain", "spain": "Spain", "에스파냐": "Spain",
    "이탈리아": "Italy", "italy": "Italy",
    "뉴질랜드": "New Zealand", "new zealand": "New Zealand", "nz": "New Zealand",
    "아르헨티나": "Argentina", "argentina": "Argentina",
    "콜롬비아": "Colombia", "colombia": "Colombia",
    "칠레": "Chile", "chile": "Chile",
    "페루": "Peru", "peru": "Peru",
    "코스타리카": "Costa Rica", "costa rica": "Costa Rica",
    "베트남": "Vietnam", "vietnam": "Vietnam",
    "태국": "Thailand", "thailand": "Thailand",
    "필리핀": "Philippines", "philippines": "Philippines",
    "파키스탄": "Pakistan", "pakistan": "Pakistan",
    "이란": "Iran", "iran": "Iran",
    "아랍에미리트": "UAE", "uae": "UAE", "emirates": "UAE",
    "카타르": "Qatar", "qatar": "Qatar",
    "케냐": "Kenya", "kenya": "Kenya",
    "가나": "Ghana", "ghana": "Ghana",
    "세네갈": "Senegal", "senegal": "Senegal",
    "모로코": "Morocco", "morocco": "Morocco",
}

ISSUE_ALIASES = {
    "GGA-IND": "GGA-IND", "글로벌 적응 목표 지표": "GGA-IND", "GGA 지표": "GGA-IND",
    "적응 지표": "GGA-IND", "indicator": "GGA-IND", "지표": "GGA-IND",
    "GGA-MOI": "GGA-MOI", "GGA 이행수단": "GGA-MOI", "이행수단": "GGA-MOI", "MoI": "GGA-MOI",
    "NAPs": "NAPs", "NAP": "NAPs", "국가적응계획": "NAPs", "적응계획": "NAPs",
    "JT-ADAPT": "JT-ADAPT", "정의로운 전환": "JT-ADAPT", "JT": "JT-ADAPT", "just transition": "JT-ADAPT",
    "L&D-OP": "L&D-OP", "손실 피해": "L&D-OP", "손실·피해": "L&D-OP", "loss damage": "L&D-OP",
    "FRLD": "L&D-OP", "손실 및 피해": "L&D-OP",
    "FINANCE-ADAPT": "FINANCE-ADAPT", "적응 재원": "FINANCE-ADAPT", "재원": "FINANCE-ADAPT",
    "adaptation finance": "FINANCE-ADAPT",
    "TRANS-FIN": "TRANS-FIN", "재원 투명성": "TRANS-FIN", "투명성": "TRANS-FIN", "transparency": "TRANS-FIN",
    "TECH-TRANS": "TECH-TRANS", "기술이전": "TECH-TRANS", "기술 이전": "TECH-TRANS",
    "technology transfer": "TECH-TRANS",
}

COP_ALIASES = {
    "COP25": "COP25", "cop25": "COP25", "마드리드": "COP25", "madrid": "COP25",
    "COP26": "COP26", "cop26": "COP26", "글래스고": "COP26", "glasgow": "COP26",
    "COP27": "COP27", "cop27": "COP27", "샤름": "COP27", "sharm": "COP27",
    "COP28": "COP28", "cop28": "COP28", "두바이": "COP28", "dubai": "COP28",
    "COP29": "COP29", "cop29": "COP29", "바쿠": "COP29", "baku": "COP29",
    "COP30": "COP30", "cop30": "COP30", "벨렘": "COP30", "belem": "COP30",
}

# ===========================================================================
# Data structures
# ===========================================================================

@dataclass
class QueryIntent:
    type: str
    countries: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    cop: Optional[str] = None
    raw_question: str = ""
    relevance_keywords: list[str] = field(default_factory=list)


@dataclass
class Citation:
    country: str
    issue: str
    cop: str
    quote: str
    score: float
    ci_lower: float = 0.0
    ci_upper: float = 0.0
    frame: str = ""
    location: str = ""
    source_type: str = ""


@dataclass
class Methodology:
    """Reproducibility footer attached to every response."""
    engine_version: str
    dataset_version: str
    prompt_version: str
    intent_type: str
    n_retrieved: int
    n_in_dataset: int
    retrieval_rule: str
    deterministic_seed: int
    response_hash: str


@dataclass
class Response:
    text: str
    citations: list[Citation] = field(default_factory=list)
    viz_payload: dict = field(default_factory=dict)
    intent: Optional[QueryIntent] = None
    matched_records: int = 0
    confidence: float = 0.0
    methodology: Optional[Methodology] = None

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "citations": [asdict(c) for c in self.citations],
            "viz_payload": self.viz_payload,
            "intent": asdict(self.intent) if self.intent else None,
            "matched_records": self.matched_records,
            "confidence": self.confidence,
            "methodology": asdict(self.methodology) if self.methodology else None,
        }


# ===========================================================================
# Data loader
# ===========================================================================

_RECORDS_CACHE: list[dict] = []
_META_CACHE: dict = {}


def load_records() -> list[dict]:
    global _RECORDS_CACHE
    if _RECORDS_CACHE:
        return _RECORDS_CACHE
    if not DATA.exists():
        raise FileNotFoundError(
            f"v5 dataset missing: {DATA}. Run `python -m src.data.build_v5_dataset`"
        )
    with open(DATA, "r", encoding="utf-8") as f:
        _RECORDS_CACHE = [json.loads(line) for line in f if line.strip()]
    return _RECORDS_CACHE


def load_meta() -> dict:
    global _META_CACHE
    if _META_CACHE:
        return _META_CACHE
    if META.exists():
        _META_CACHE = json.loads(META.read_text(encoding="utf-8"))
    return _META_CACHE


# ===========================================================================
# v6 Corpus loader + search (TF-IDF inverted index)
# ===========================================================================

_CORPUS_MANIFEST_CACHE: list[dict] = []
_CORPUS_INDEX_CACHE: dict = {}

STOP_WORDS = {
    "the","a","an","and","or","but","is","are","of","in","on","at","to","for","with","by",
    "as","that","this","it","its","not","no","from","into",
    "본","해","이","그","저","것","및","또","수","의","에","에서","으로","로","를","을","는","가",
    "있다","없다","한다","된다","것이다","위해","대한","대해","해서","하는","된","된다고","이는",
}

def _corpus_tokenize(text: str) -> list[str]:
    if not text: return []
    raw = re.findall(r"[가-힣]+|[A-Za-z0-9_\-\.&]+", text.lower())
    return [t for t in raw if len(t) > 1 and t not in STOP_WORDS]

def load_corpus_manifest() -> list[dict]:
    global _CORPUS_MANIFEST_CACHE
    if _CORPUS_MANIFEST_CACHE: return _CORPUS_MANIFEST_CACHE
    if not CORPUS_MANIFEST.exists(): return []
    with open(CORPUS_MANIFEST, "r", encoding="utf-8") as f:
        _CORPUS_MANIFEST_CACHE = [json.loads(line) for line in f if line.strip()]
    return _CORPUS_MANIFEST_CACHE

def load_corpus_index() -> dict:
    global _CORPUS_INDEX_CACHE
    if _CORPUS_INDEX_CACHE: return _CORPUS_INDEX_CACHE
    if not CORPUS_INDEX.exists(): return {}
    _CORPUS_INDEX_CACHE = json.loads(CORPUS_INDEX.read_text(encoding="utf-8"))
    return _CORPUS_INDEX_CACHE

def corpus_search(query: str, top_k: int = 5) -> list[dict]:
    """TF-IDF search returning [{doc_id, score, manifest_record}, ...]."""
    idx = load_corpus_index()
    if not idx: return []
    manifest = load_corpus_manifest()
    by_id = {r["doc_id"]: r for r in manifest}
    toks = _corpus_tokenize(query)
    scores = defaultdict(float)
    for t in toks:
        idf_w = idx.get("idf", {}).get(t, 0)
        if t not in idx.get("inverted", {}): continue
        for doc_id, w in idx["inverted"][t]:
            scores[doc_id] += w * idf_w
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
    return [{"doc_id": d, "score": round(s, 4),
             "manifest": by_id.get(d, {"doc_id": d, "path": "?", "title": d, "type": "?"})}
            for d, s in ranked]

# ===========================================================================
# v7 Semantic embedding search (sentence-transformers)
# ===========================================================================

_EMBED_MATRIX = None       # np.ndarray (N, 384)
_EMBED_INDEX_META = None   # dict with items list
_EMBED_MODEL = None        # SentenceTransformer (lazy)

def _load_embeddings():
    """Lazy load NPZ + index. Returns (matrix, index_meta) or (None, None)."""
    global _EMBED_MATRIX, _EMBED_INDEX_META
    if _EMBED_MATRIX is not None: return _EMBED_MATRIX, _EMBED_INDEX_META
    if not EMBED_NPZ.exists() or not EMBED_INDEX.exists():
        return None, None
    try:
        import numpy as np
        arr = np.load(EMBED_NPZ)
        _EMBED_MATRIX = arr["embeddings"].astype(np.float32)
        _EMBED_INDEX_META = json.loads(EMBED_INDEX.read_text(encoding="utf-8"))
        return _EMBED_MATRIX, _EMBED_INDEX_META
    except Exception as e:
        print(f"[v2.2] embedding load failed: {e}")
        return None, None

def _get_embed_model():
    """Lazy-load sentence-transformers model."""
    global _EMBED_MODEL
    if _EMBED_MODEL is not None: return _EMBED_MODEL
    try:
        from sentence_transformers import SentenceTransformer
        meta = _EMBED_INDEX_META or {}
        model_name = meta.get("model_name", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        _EMBED_MODEL = SentenceTransformer(model_name)
        return _EMBED_MODEL
    except Exception as e:
        print(f"[v2.2] sentence-transformers unavailable: {e}")
        return None

def semantic_search(query: str, top_k: int = 8, kinds: list[str] | None = None) -> list[dict]:
    """Cosine similarity search using v7 embeddings.

    Returns: [{doc_id, kind, title, score, text_preview, path, cop, country}, ...]
    Returns [] gracefully if embeddings or model unavailable."""
    matrix, meta = _load_embeddings()
    if matrix is None: return []
    model = _get_embed_model()
    if model is None: return []
    import numpy as np
    q_emb = model.encode([query], normalize_embeddings=True, convert_to_numpy=True)[0].astype(np.float32)
    sims = matrix @ q_emb        # since both L2-normalised, dot == cosine
    items = meta["items"]
    # Optional kind filter
    if kinds:
        idx_filter = [i for i, it in enumerate(items) if it["kind"] in kinds]
        sub_sims = sims[idx_filter]
        ranked = sorted(zip(idx_filter, sub_sims), key=lambda x: -x[1])[:top_k]
    else:
        ranked = sorted(enumerate(sims), key=lambda x: -x[1])[:top_k]
    out = []
    for i, s in ranked:
        it = items[i]
        out.append({
            "doc_id":       it.get("doc_id"),
            "kind":         it.get("kind"),
            "title":        it.get("title"),
            "type":         it.get("type"),
            "country":      it.get("country"),
            "cop":          it.get("cop"),
            "path":         it.get("path"),
            "text_preview": it.get("text_preview", ""),
            "chunk_idx":    it.get("chunk_idx"),
            "score":        float(s),
        })
    return out

def hybrid_search(query: str, top_k: int = 8,
                  alpha: float = 0.6, kinds: list[str] | None = None) -> list[dict]:
    """Hybrid keyword (TF-IDF) + semantic search.

    final_score = alpha * semantic_cosine + (1 - alpha) * tfidf_norm
    Defaults to 0.6 semantic + 0.4 keyword.
    Falls back to keyword-only if embeddings unavailable.
    """
    sem_hits = semantic_search(query, top_k=top_k * 3, kinds=kinds)
    kw_hits = corpus_search(query, top_k=top_k * 3)
    if not sem_hits:
        return [{"doc_id": h["doc_id"], "score": h["score"], "kind": "corpus_whole",
                 "title": h["manifest"].get("title"), "path": h["manifest"].get("path"),
                 "type": h["manifest"].get("type"), "text_preview": "",
                 "country": h["manifest"].get("country"), "cop": h["manifest"].get("cop"),
                 "method": "keyword"} for h in kw_hits[:top_k]]
    # Normalise scores to [0, 1]
    max_sem = max((h["score"] for h in sem_hits), default=1.0) or 1.0
    max_kw  = max((h["score"] for h in kw_hits), default=1.0) or 1.0
    by_doc = {}
    for h in sem_hits:
        d = h["doc_id"]
        s = h["score"] / max_sem
        by_doc[d] = {"semantic": s, "keyword": 0, "hit": h}
    for h in kw_hits:
        d = h["doc_id"]
        s = h["score"] / max_kw
        if d in by_doc:
            by_doc[d]["keyword"] = s
        else:
            by_doc[d] = {"semantic": 0, "keyword": s,
                         "hit": {"doc_id": d, "title": h["manifest"].get("title"),
                                 "path": h["manifest"].get("path"),
                                 "type": h["manifest"].get("type"),
                                 "country": h["manifest"].get("country"),
                                 "cop": h["manifest"].get("cop"),
                                 "kind": "corpus_whole",
                                 "text_preview": "",
                                 "chunk_idx": None,
                                }}
    ranked = sorted(by_doc.items(),
                    key=lambda x: -(alpha * x[1]["semantic"] + (1 - alpha) * x[1]["keyword"]))[:top_k]
    out = []
    for d, info in ranked:
        h = info["hit"]
        out.append({**h,
                    "score": round(alpha * info["semantic"] + (1 - alpha) * info["keyword"], 4),
                    "score_semantic": round(info["semantic"], 4),
                    "score_keyword":  round(info["keyword"], 4),
                    "method": "hybrid"})
    return out


def corpus_filter_by_context(intent) -> list[dict]:
    """Return manifest records whose country/issue/COP overlap with intent."""
    manifest = load_corpus_manifest()
    out = []
    for r in manifest:
        if intent.countries:
            if r.get("country") in intent.countries: out.append(r); continue
            if r.get("type") == "national_policy" and r.get("country") in intent.countries:
                out.append(r); continue
        if intent.issues:
            if any(i in (r.get("issues_addressed") or []) for i in intent.issues):
                out.append(r); continue
        if intent.cop and r.get("cop") == intent.cop:
            out.append(r); continue
    # dedupe
    seen = set(); uniq = []
    for r in out:
        k = r["doc_id"]
        if k not in seen: seen.add(k); uniq.append(r)
    return uniq


# ===========================================================================
# Intent parsing (v2 - extended)
# ===========================================================================

# Trigger words by intent
INTENT_TRIGGERS = {
    "search":         ["원문", "본문", "결정문", "L-document", "L문서", "조문", "조항", "where does it say",
                       "document says", "텍스트", "decision text", "policy document", "source"],
    "trend":          ["추이", "시계열", "흐름", "trajectory", "trend", "evolution", "over time", "변화 추이"],
    "coalition":      ["연합", "동맹", "비슷한 국가", "유사한 국가", "비슷", "coalition", "similar countries", "동조"],
    "gap":            ["translation gap", "국내국제", "국내 국제", "domestic international", "delta",
                       "Δ", "이중정체성", "이중 정체성", "괴리", "이행격차", "이행 격차"],
    "compare":        ["비교", " vs ", " versus ", "차이", "사이", "different from", "compared to"],
    "recommendation": ["권고", "전략", "어떻게 해야", "추천", "권장", "recommend", "수립", "방안", "strategy"],
    "factoid":        ["정확히 몇", "정확한 값", "정확히 얼마", "exact value", "정확히"],
}


def parse_intent(question: str) -> QueryIntent:
    q = question.strip()
    q_lower = " " + q.lower() + " "

    # Country detection
    countries = []
    for alias, canonical in COUNTRY_ALIASES.items():
        if alias.lower() in q_lower and canonical not in countries:
            countries.append(canonical)

    # Issue detection
    issues = []
    for alias, canonical in ISSUE_ALIASES.items():
        if alias.lower() in q_lower and canonical not in issues:
            issues.append(canonical)

    # COP detection (avoid 브라질 == COP30 confusion)
    cop = None
    for alias, canonical in COP_ALIASES.items():
        if alias.lower() in q_lower:
            cop = canonical
            break

    # Type detection - priority-ordered
    qtype = "unknown"
    for intent_name, triggers in INTENT_TRIGGERS.items():
        if any(t.lower() in q_lower for t in triggers):
            qtype = intent_name
            break
    # Refine: compare requires >=2 countries
    if qtype == "compare" and len(countries) < 2:
        qtype = "lookup"
    if qtype == "unknown":
        if countries and issues:        qtype = "lookup"
        elif countries:                  qtype = "lookup"
        elif issues:                     qtype = "lookup"

    # Keywords for relevance scoring (drop common words)
    stop = {"의", "에서", "어떻게", "왜", "는", "가", "을", "를", "is", "the", "a", "an", "and", "or"}
    kw = [w for w in re.split(r"\s+", q) if w and w.lower() not in stop and len(w) > 1]

    return QueryIntent(
        type=qtype, countries=countries, issues=issues,
        cop=cop or DEFAULT_COP, raw_question=q,
        relevance_keywords=kw,
    )


# ===========================================================================
# Retrieval (top-k relevance scoring)
# ===========================================================================

def _record_relevance(r: dict, intent: QueryIntent) -> float:
    """Score how relevant record r is to the parsed intent."""
    score = 0.0
    m = r["_meta"]
    if intent.countries:
        score += 1.5 if m["country"] in intent.countries else 0
    if intent.issues:
        score += 1.5 if m["issue"] in intent.issues else 0
    if intent.cop and m["cop"] == intent.cop:
        score += 1.0
    # mild boost for higher confidence / salience
    score += 0.3 * r.get("confidence", 0.85)
    score += 0.2 * r.get("salience_score", 0.65)
    # boost verified canonical records
    if m.get("source_type") == "verified_canonical":
        score += 0.5
    return score


def retrieve(intent: QueryIntent, k: int = 20) -> list[dict]:
    """Top-k retrieval against v5 dataset."""
    records = load_records()
    # Hard filter by country/issue/COP if specified
    pool = records
    if intent.countries:
        pool = [r for r in pool if r["_meta"]["country"] in intent.countries]
    if intent.issues:
        pool = [r for r in pool if r["_meta"]["issue"] in intent.issues]
    if intent.cop and intent.type not in ("trend", "coalition"):
        # For trend / coalition we want multiple COPs
        pool = [r for r in pool if r["_meta"]["cop"] == intent.cop]
    # Score and sort
    scored = [(r, _record_relevance(r, intent)) for r in pool]
    scored.sort(key=lambda x: -x[1])
    return [r for r, _ in scored[:k]]


# ===========================================================================
# Response formatters
# ===========================================================================

def _fmt_score(s: float) -> str:
    sign = "+" if s >= 0 else ""
    return f"{sign}{s:.2f}"


def _stance_label_ko(s: float) -> str:
    if s >= 0.7:  return "강한 지지"
    if s >= 0.3:  return "지지"
    if s >= -0.3: return "중립"
    if s >= -0.7: return "반대"
    return "강한 반대"


def _ci_str(r: dict) -> str:
    lo, hi = r.get("ci_lower_95"), r.get("ci_upper_95")
    if lo is None or hi is None: return ""
    return f" (95% CI [{lo:+.2f}, {hi:+.2f}])"


def _nato_summary(r: dict) -> str:
    nato = r.get("nato_4axis", {})
    if not nato: return ""
    n, a, t, o = nato.get("nodality", 0), nato.get("authority", 0), nato.get("treasure", 0), nato.get("organization", 0)
    return f"NATO 4축: N={n:.2f} A={a:.2f} T={t:.2f} O={o:.2f}"


def _record_to_citation(r: dict) -> Citation:
    m = r["_meta"]
    return Citation(
        country=m["country"], issue=m["issue"], cop=m["cop"],
        quote=r.get("evidence_quote", ""), score=r.get("stance_score", 0.0),
        ci_lower=r.get("ci_lower_95", 0.0), ci_upper=r.get("ci_upper_95", 0.0),
        frame=r.get("frame_type", ""), location=r.get("evidence_location", ""),
        source_type=m.get("source_type", ""),
    )


# ===========================================================================
# Per-intent builders
# ===========================================================================

def _build_lookup(intent: QueryIntent, records: list[dict]) -> Response:
    if not records:
        return _build_empty(intent)

    lines = []
    cit = []
    payload = {"type": "lookup_card", "items": []}

    if len(records) == 1:
        r = records[0]
        m = r["_meta"]
        s = r["stance_score"]
        lines.append(f"**{m['country']} -{m['issue']} ({m['cop']})**")
        lines.append(f"")
        lines.append(f"입장 점수: **{_fmt_score(s)}** ({_stance_label_ko(s)}){_ci_str(r)}")
        lines.append(f"우세 frame: {r.get('frame_type', '-')}")
        lines.append(f"{_nato_summary(r)}")
        if r.get("procedural_composite", 0) > 0.1:
            proc = r.get("procedural_signals", {})
            tags = []
            if proc.get("is_chair_role"):  tags.append("의장")
            if proc.get("is_pen_holder"):  tags.append("펜홀더")
            lines.append(f"절차권한: {', '.join(tags)} (composite={r.get('procedural_composite'):.2f})")
        delta = r.get("translation_gap_delta", 0)
        if abs(delta) > 0.15:
            lines.append(f"국내↔국제 translation gap Δ = {delta:+.2f}")
        cit.append(_record_to_citation(r))
    else:
        # Multi-record summary
        target = intent.countries[0] if intent.countries else "-"
        lines.append(f"**{target} -{len(records)}개 매칭 record**\n")
        for r in records[:8]:
            m = r["_meta"]
            s = r["stance_score"]
            lines.append(f"- {m['issue']} ({m['cop']}): {_fmt_score(s)} {_stance_label_ko(s)}{_ci_str(r)}")
            if len(cit) < 8:
                cit.append(_record_to_citation(r))
        payload["items"] = [
            {"label": f"{r['_meta']['issue']}@{r['_meta']['cop']}", "value": r["stance_score"]}
            for r in records[:8]
        ]

    conf = statistics.mean([r.get("confidence", 0.85) for r in records])
    r0 = records[0]
    return Response(
        text="\n".join(lines), citations=cit, viz_payload=payload,
        intent=intent, matched_records=len(records), confidence=round(conf, 3),
    )


def _build_compare(intent: QueryIntent, records: list[dict]) -> Response:
    if len(intent.countries) < 2:
        return _build_lookup(intent, records)

    target_issues = intent.issues or ["GGA-IND", "GGA-MOI", "NAPs", "JT-ADAPT", "L&D-OP",
                                       "FINANCE-ADAPT", "TRANS-FIN", "TECH-TRANS"]
    cop = intent.cop or DEFAULT_COP
    grouped = defaultdict(dict)
    for r in records:
        m = r["_meta"]
        if m["cop"] == cop:
            grouped[m["country"]][m["issue"]] = r

    lines = [f"**{' vs '.join(intent.countries)} 입장 비교 ({cop})**\n"]
    cit = []
    payload = {"type": "comparison_bar", "labels": target_issues, "series": []}

    for c in intent.countries:
        c_records = grouped.get(c, {})
        scores, cis = [], []
        for iss in target_issues:
            r = c_records.get(iss)
            if r:
                s = r["stance_score"]
                scores.append(s)
                cis.append({"lo": r.get("ci_lower_95"), "hi": r.get("ci_upper_95")})
                if r.get("evidence_quote") and len(cit) < 12:
                    cit.append(_record_to_citation(r))
            else:
                scores.append(None); cis.append(None)
        payload["series"].append({"name": c, "data": scores, "ci": cis})

        lines.append(f"\n**{c}**:")
        for iss, s in zip(target_issues, scores):
            if s is not None:
                lines.append(f"  - {iss}: {_fmt_score(s)} ({_stance_label_ko(s)})")

    # Compute pairwise gap
    if len(intent.countries) == 2:
        c1, c2 = intent.countries[:2]
        gaps = []
        for iss in target_issues:
            r1 = grouped.get(c1, {}).get(iss); r2 = grouped.get(c2, {}).get(iss)
            if r1 and r2:
                gaps.append((iss, r1["stance_score"] - r2["stance_score"]))
        if gaps:
            largest = max(gaps, key=lambda x: abs(x[1]))
            lines.append(f"\n📊 **최대 격차**: {largest[0]} (Δ = {largest[1]:+.2f})")

    conf = statistics.mean([r.get("confidence", 0.85) for r in records]) if records else 0.85
    return Response(
        text="\n".join(lines), citations=cit, viz_payload=payload, intent=intent,
        matched_records=len(records), confidence=round(conf, 3),
    )


def _build_trend(intent: QueryIntent, records: list[dict]) -> Response:
    """Time-series across COPs for given (country, issue)."""
    if not records:
        return _build_empty(intent)

    # Group by (country, issue) -> sorted by COP
    grouped = defaultdict(dict)
    for r in records:
        m = r["_meta"]
        grouped[(m["country"], m["issue"])][m["cop"]] = r

    cops_order = load_meta().get("cops", ["COP25","COP26","COP27","COP28","COP29","COP30"])

    lines = ["**시계열 추이 분석**\n"]
    cit = []
    payload = {"type": "timeseries", "x": cops_order, "series": []}

    for (country, issue), per_cop in list(grouped.items())[:8]:
        ys = [per_cop.get(c, {}).get("stance_score") for c in cops_order]
        valid_ys = [y for y in ys if y is not None]
        if not valid_ys: continue
        payload["series"].append({
            "name": f"{country} -{issue}",
            "data": ys,
        })
        # text summary
        first, last = valid_ys[0], valid_ys[-1]
        delta = last - first
        arrow = "↑" if delta > 0.05 else ("↓" if delta < -0.05 else "→")
        lines.append(f"- {country} {issue}: {_fmt_score(first)} → {_fmt_score(last)} {arrow} (Δ {delta:+.2f})")
        # Add 1 citation per series
        for c in reversed(cops_order):
            if c in per_cop and len(cit) < 8:
                cit.append(_record_to_citation(per_cop[c]))
                break

    if len(grouped) > 8:
        lines.append(f"\n(전체 {len(grouped)}개 series 중 8개만 표시)")

    conf = 0.82  # trend extraction inherently noisier
    return Response(
        text="\n".join(lines), citations=cit, viz_payload=payload, intent=intent,
        matched_records=len(records), confidence=conf,
    )


def _build_coalition(intent: QueryIntent, records: list[dict]) -> Response:
    """Find countries similar to the requested country at the given COP."""
    if not intent.countries:
        return _build_empty(intent)
    target = intent.countries[0]
    cop = intent.cop or DEFAULT_COP

    all_records = load_records()
    # Build full stance vector per country at this COP
    by_country = defaultdict(dict)
    for r in all_records:
        m = r["_meta"]
        if m["cop"] == cop:
            by_country[m["country"]][m["issue"]] = r["stance_score"]

    if target not in by_country:
        return _build_empty(intent)

    target_vec = by_country[target]
    issues = sorted(target_vec.keys())

    def pearson(v1, v2):
        """Mean-centred similarity; discriminates between countries whose
        overall positive bias would otherwise saturate cosine near 1."""
        common = [iss for iss in issues if iss in v1 and iss in v2]
        if len(common) < 2: return 0.0
        x = [v1[iss] for iss in common]
        y = [v2[iss] for iss in common]
        mx, my = sum(x)/len(x), sum(y)/len(y)
        num = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y))
        dx = (sum((xi-mx)**2 for xi in x))**0.5
        dy = (sum((yi-my)**2 for yi in y))**0.5
        if dx == 0 or dy == 0: return 0.0
        return num / (dx * dy)

    sims = []
    for c, vec in by_country.items():
        if c == target: continue
        sims.append((c, pearson(target_vec, vec)))
    sims.sort(key=lambda x: -x[1])

    lines = [f"**{target}와 가장 유사한 국가 ({cop}, 8-이슈 Pearson 상관계수)**\n"]
    payload = {"type": "coalition_bar", "labels": [], "values": []}
    cit = []
    for c, sim in sims[:10]:
        lines.append(f"- {c}: r = {sim:+.3f}")
        payload["labels"].append(c); payload["values"].append(round(sim, 3))
        # Pull 1 citation per neighbor for evidence
        for r in records:
            if r["_meta"]["country"] == c and r["_meta"]["cop"] == cop and len(cit) < 10:
                cit.append(_record_to_citation(r)); break

    # Also include target's own primary coalition
    coalition_meta = None
    for r in records:
        if r["_meta"]["country"] == target:
            coalition_meta = r.get("coalition_membership"); break
    if coalition_meta:
        lines.append(f"\n📍 **{target}의 공식 coalition**: primary = {coalition_meta.get('primary')}, all = {coalition_meta.get('all')}")

    return Response(
        text="\n".join(lines), citations=cit, viz_payload=payload, intent=intent,
        matched_records=len(records), confidence=0.85,
    )


def _build_gap(intent: QueryIntent, records: list[dict]) -> Response:
    """Translation gap analysis: domestic vs international stance."""
    if not records:
        return _build_empty(intent)

    target_country = intent.countries[0] if intent.countries else None
    # If 1 country, show its per-issue translation gap; else show top-10 gap leaders
    if target_country:
        target_records = [r for r in records if r["_meta"]["country"] == target_country]
        if not target_records:
            return _build_empty(intent)
        lines = [f"**{target_country} -국내↔국제 translation gap (Δ = 국내 stance - 국제 stance)**\n"]
        payload = {"type": "gap_bar", "labels": [], "values": []}
        cit = []
        # group by issue (most recent COP if not specified)
        by_issue = defaultdict(list)
        for r in target_records:
            by_issue[r["_meta"]["issue"]].append(r)
        for iss, rs in by_issue.items():
            # take most recent COP record
            rs.sort(key=lambda r: r["_meta"]["cop"])
            r = rs[-1]
            delta = r.get("translation_gap_delta", 0)
            lines.append(f"- {iss} ({r['_meta']['cop']}): Δ = {delta:+.2f}  (domestic≈{r.get('domestic_stance_proxy', 0):+.2f}, intl={r['stance_score']:+.2f})")
            payload["labels"].append(iss); payload["values"].append(round(delta, 3))
            if len(cit) < 8: cit.append(_record_to_citation(r))
        return Response(
            text="\n".join(lines), citations=cit, viz_payload=payload, intent=intent,
            matched_records=len(records), confidence=0.78,
        )
    else:
        # No country: show 10 largest |Δ| globally for the COP
        cop = intent.cop or DEFAULT_COP
        all_at_cop = [r for r in load_records() if r["_meta"]["cop"] == cop]
        # Per-country mean |Δ|
        by_country = defaultdict(list)
        for r in all_at_cop:
            by_country[r["_meta"]["country"]].append(abs(r.get("translation_gap_delta", 0)))
        rankings = [(c, statistics.mean(vs)) for c, vs in by_country.items()]
        rankings.sort(key=lambda x: -x[1])

        lines = [f"**{cop} -국가별 평균 |translation gap| 상위 10**\n"]
        payload = {"type": "gap_ranking", "labels": [], "values": []}
        for c, mean_d in rankings[:10]:
            lines.append(f"- {c}: |Δ_mean| = {mean_d:.3f}")
            payload["labels"].append(c); payload["values"].append(round(mean_d, 3))
        return Response(
            text="\n".join(lines), citations=[], viz_payload=payload, intent=intent,
            matched_records=len(all_at_cop), confidence=0.75,
        )


def _build_recommendation(intent: QueryIntent, records: list[dict]) -> Response:
    """Strategy recommendation for Korea (or specified country)."""
    target = intent.countries[0] if intent.countries else "Korea"
    cop = intent.cop or DEFAULT_COP

    target_records = [r for r in records if r["_meta"]["country"] == target and r["_meta"]["cop"] == cop]
    if not target_records:
        return _build_empty(intent)

    # Sort by stance — find weakest issues for the target
    target_records.sort(key=lambda r: r["stance_score"])
    weakest = target_records[:3]
    strongest = target_records[-3:][::-1]

    lines = [f"**{target} 전략 권고 ({cop})**\n"]
    lines.append("\n📉 약점 이슈 (낮은 stance, 보강 필요):")
    cit = []
    for r in weakest:
        m = r["_meta"]
        lines.append(f"  - {m['issue']}: {_fmt_score(r['stance_score'])}{_ci_str(r)}; 권장 — NATO {max(r.get('nato_4axis', {}), key=lambda k: r.get('nato_4axis', {}).get(k, 0))} 축 강화")
        if len(cit) < 6: cit.append(_record_to_citation(r))

    lines.append("\n📈 강점 이슈 (높은 stance, pen-holder potential):")
    for r in strongest:
        m = r["_meta"]
        proc = r.get("procedural_signals", {})
        pen = " 👑 펜홀더" if proc.get("is_pen_holder") else ""
        lines.append(f"  - {m['issue']}: {_fmt_score(r['stance_score'])}{pen}")
        if len(cit) < 8: cit.append(_record_to_citation(r))

    # Suggest coalition allies
    coalition_meta = target_records[0].get("coalition_membership", {})
    if coalition_meta.get("all"):
        lines.append(f"\n🤝 활용 가능 coalition: {', '.join(coalition_meta['all'])}")

    # Mean translation gap
    deltas = [abs(r.get("translation_gap_delta", 0)) for r in target_records]
    mean_d = statistics.mean(deltas) if deltas else 0
    lines.append(f"\n📐 평균 |translation gap| = {mean_d:.3f} ({'주의' if mean_d > 0.25 else '안정'})")

    payload = {
        "type": "recommendation_card",
        "weakest": [{"issue": r["_meta"]["issue"], "score": r["stance_score"]} for r in weakest],
        "strongest": [{"issue": r["_meta"]["issue"], "score": r["stance_score"]} for r in strongest],
    }
    return Response(
        text="\n".join(lines), citations=cit, viz_payload=payload, intent=intent,
        matched_records=len(records), confidence=0.82,
    )


def _build_factoid(intent: QueryIntent, records: list[dict]) -> Response:
    if not records:
        return _build_empty(intent)
    r = records[0]
    m = r["_meta"]
    s = r["stance_score"]
    return Response(
        text=f"{m['country']} -{m['issue']} ({m['cop']}): stance = **{_fmt_score(s)}**{_ci_str(r)}",
        citations=[_record_to_citation(r)],
        viz_payload={"type": "scalar", "value": s},
        intent=intent, matched_records=len(records), confidence=r.get("confidence", 0.85),
    )


def _build_search(intent: QueryIntent, records: list[dict]) -> Response:
    """Corpus-document search intent — hybrid (semantic + keyword) by default."""
    # Try hybrid; falls back to keyword if embeddings unavailable
    hybrid_hits = hybrid_search(intent.raw_question, top_k=8)
    method = hybrid_hits[0].get("method", "keyword") if hybrid_hits else "keyword"
    if not hybrid_hits:
        return Response(
            text="corpus에서 관련 문서를 찾지 못했습니다.",
            citations=[], viz_payload={"type":"empty"}, intent=intent,
            matched_records=0, confidence=0.0,
        )
    method_label = "semantic+keyword 하이브리드" if method == "hybrid" else "keyword (TF-IDF)"
    lines = [f"**'{intent.raw_question}' — corpus 문서 top-{len(hybrid_hits)} ({method_label})**\n"]
    for i, h in enumerate(hybrid_hits, 1):
        lines.append(f"{i}. **{h.get('title','?')}**  (score={h['score']:.3f})")
        meta_parts = []
        if h.get("type"): meta_parts.append(f"type: {h['type']}")
        if h.get("cop"): meta_parts.append(f"cop: {h['cop']}")
        if h.get("country"): meta_parts.append(f"country: {h['country']}")
        if h.get("chunk_idx") is not None: meta_parts.append(f"chunk #{h['chunk_idx']}")
        if method == "hybrid":
            meta_parts.append(f"semantic={h.get('score_semantic', 0):.2f}")
            meta_parts.append(f"keyword={h.get('score_keyword', 0):.2f}")
        if meta_parts: lines.append(f"   - {' · '.join(meta_parts)}")
        lines.append(f"   - path: `{h.get('path', '?')}`")
        if h.get("text_preview"):
            preview = h["text_preview"][:200].replace("\n", " ")
            lines.append(f'   - preview: "{preview}..."')
    payload = {"type": "search_results", "method": method,
               "items": [{"title": h.get("title"), "score": h["score"],
                          "path": h.get("path"), "type": h.get("type"),
                          "score_semantic": h.get("score_semantic"),
                          "score_keyword": h.get("score_keyword")}
                         for h in hybrid_hits]}
    return Response(
        text="\n".join(lines), citations=[], viz_payload=payload,
        intent=intent, matched_records=len(hybrid_hits), confidence=0.85,
    )


def _build_empty(intent: QueryIntent) -> Response:
    txt = "데이터베이스에서 매칭되는 record를 찾지 못했습니다.\n"
    txt += "- 지원: 50개국 × 8이슈 (GGA-IND, GGA-MOI, NAPs, JT-ADAPT, L&D-OP, FINANCE-ADAPT, TRANS-FIN, TECH-TRANS) × 6 COP (COP25-COP30)\n"
    txt += "- 질문에 국가명 + 이슈명을 명시하시면 더 정확한 결과를 얻습니다."
    return Response(
        text=txt, citations=[], viz_payload={"type": "empty"},
        intent=intent, matched_records=0, confidence=0.0,
    )


# ===========================================================================
# Main entry
# ===========================================================================

def _make_methodology(intent: QueryIntent, n_retrieved: int, seed: int = 42) -> Methodology:
    meta = load_meta()
    payload = json.dumps({
        "intent_type": intent.type,
        "countries":   intent.countries,
        "issues":      intent.issues,
        "cop":         intent.cop,
        "raw":         intent.raw_question,
        "seed":        seed,
    }, sort_keys=True)
    h = hashlib.sha256(payload.encode()).hexdigest()[:16]
    return Methodology(
        engine_version=ENGINE_VERSION,
        dataset_version=meta.get("dataset_version", "5.0.0"),
        prompt_version=meta.get("prompt_version", "stance_extract_v1.3"),
        intent_type=intent.type,
        n_retrieved=n_retrieved,
        n_in_dataset=meta.get("n_records", 2400),
        retrieval_rule="top-k by relevance (country/issue/COP filter + salience + confidence + verified bonus)",
        deterministic_seed=seed,
        response_hash=h,
    )


_INTENT_DISPATCH = {
    "lookup":         _build_lookup,
    "compare":        _build_compare,
    "trend":          _build_trend,
    "coalition":      _build_coalition,
    "gap":            _build_gap,
    "recommendation": _build_recommendation,
    "factoid":        _build_factoid,
    "search":         _build_search,
}


def answer_question(question: str, k: int = 24, seed: int = 42) -> Response:
    intent = parse_intent(question)
    # Choose retrieval k by intent
    retrieval_k = {
        "trend":      120,
        "coalition":  400,
        "gap":        80,
    }.get(intent.type, k)
    records = retrieve(intent, k=retrieval_k)
    builder = _INTENT_DISPATCH.get(intent.type, _build_lookup)
    response = builder(intent, records)

    # v2.2: auto-attach corpus references using hybrid search (semantic + keyword).
    if intent.type != "search":
        hyb_hits = hybrid_search(question, top_k=5)
        context_hits = corpus_filter_by_context(intent)
        # Build doc_id-keyed merged list, preserving hybrid order
        seen = set()
        merged = []
        for h in hyb_hits:
            if h.get("doc_id") and h["doc_id"] not in seen:
                seen.add(h["doc_id"])
                merged.append({"doc_id": h["doc_id"], "title": h.get("title"),
                               "short_title": h.get("title"), "path": h.get("path"),
                               "type": h.get("type"), "official_url": None,
                               "score": h.get("score"), "method": h.get("method")})
        for r in context_hits:
            if r["doc_id"] not in seen:
                seen.add(r["doc_id"]); merged.append(r)
        if merged:
            response.viz_payload["corpus_references"] = [
                {"doc_id": r["doc_id"], "title": r.get("short_title", r.get("title", "?")),
                 "path": r.get("path"), "type": r.get("type"),
                 "official_url": r.get("official_url"),
                 "score": r.get("score"), "method": r.get("method")}
                for r in merged[:3]
            ]
            response.text += "\n\n📚 **관련 corpus 문서** (hybrid 검색):\n"
            for r in merged[:3]:
                method_tag = f" [{r.get('method','keyword')}]" if r.get("method") else ""
                response.text += f"  - {r.get('short_title', r.get('title','?'))}{method_tag}  (`{r.get('path','?')}`)\n"

    response.methodology = _make_methodology(intent, n_retrieved=len(records), seed=seed)
    return response


# ===========================================================================
# CLI
# ===========================================================================

def _demo():
    import io, sys
    # Force utf-8 stdout for Windows cp949 consoles
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except Exception: pass
    demo_questions = [
        "브라질 GGA-IND COP30 입장은?",
        "브라질과 한국의 GGA 지표 입장 차이는?",
        "AOSIS GGA-IND 시계열 추이?",
        "한국과 비슷한 국가는?",
        "브라질의 translation gap 분석",
        "COP30 한국 외교 권고",
        "사우디 L&D-OP 정확한 점수는?",
        "L.25E 결정문 본문 어디서 voluntary 어구 사용?",   # new: search intent
        "FRLD 펀드 신설 결정문 원문",                      # new: search intent
    ]
    for q in demo_questions:
        print(f"\n{'='*72}\nQ: {q}\n{'='*72}")
        r = answer_question(q)
        print(r.text)
        if r.citations:
            print(f"\n[citations {len(r.citations)}]")
            for c in r.citations[:3]:
                print(f"  - {c.country}/{c.issue}@{c.cop}: {_fmt_score(c.score)} -- \"{c.quote[:90]}...\"")
        if r.methodology:
            print(f"\n[methodology] {r.methodology.intent_type} | retrieved={r.methodology.n_retrieved} / dataset={r.methodology.n_in_dataset} | hash={r.methodology.response_hash}")


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        try: sys.stdout.reconfigure(encoding="utf-8")
        except Exception: pass
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        _demo()
    elif len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        r = answer_question(q)
        print(json.dumps(r.to_dict(), indent=2, ensure_ascii=False))
    else:
        print("Usage: python -m src.program.query_engine_v2 --demo")
        print("       python -m src.program.query_engine_v2 '<your question>'")
