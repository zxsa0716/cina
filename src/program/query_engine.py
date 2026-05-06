"""CINA Q&A Query Engine — backend logic for the interactive program.

Routes user natural-language questions about climate negotiation positions
to (a) data lookup, (b) optional LLM response generation, (c) citation
attachment, (d) visualization payload.

Usage:
    from src.program.query_engine import answer_question
    response = answer_question("브라질이 GGA 지표에서 한국과 어떻게 다른가?")
    print(response.text)
    print(response.citations)
    print(response.viz_payload)

Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
License: MIT
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data" / "processed" / "stances_v4.jsonl"

# ---------------------------------------------------------------------------
# Country / issue alias dictionaries (Korean and English)
# ---------------------------------------------------------------------------

COUNTRY_ALIASES = {
    "브라질": "Brazil", "brazil": "Brazil",
    "한국": "Korea", "대한민국": "Korea", "korea": "Korea", "south korea": "Korea",
    "미국": "USA", "usa": "USA", "us": "USA", "united states": "USA",
    "중국": "China", "china": "China",
    "인도": "India", "india": "India",
    "유럽연합": "EU", "유럽": "EU", "eu": "EU",
    "사우디": "Saudi", "사우디아라비아": "Saudi", "saudi": "Saudi",
    "일본": "Japan", "japan": "Japan",
    "튀르키예": "Türkiye", "터키": "Türkiye", "turkey": "Türkiye",
    "AOSIS": "AOSIS", "aosis": "AOSIS", "군소도서국연합": "AOSIS", "군소도서국": "AOSIS",
    "AILAC": "AILAC", "ailac": "AILAC",
    "AGN": "AGN", "agn": "AGN", "아프리카그룹": "AGN", "아프리카": "AGN",
    "LMDC": "LMDC", "lmdc": "LMDC", "같은마음개도국": "LMDC",
    "캐나다": "Canada", "canada": "Canada",
    "호주": "Australia", "오스트레일리아": "Australia",
    "노르웨이": "Norway",
    "영국": "UK", "uk": "UK",
    "독일": "Germany", "germany": "Germany",
    "프랑스": "France", "france": "France",
    "멕시코": "Mexico", "mexico": "Mexico",
    "인도네시아": "Indonesia",
    "남아공": "South Africa", "남아프리카": "South Africa", "south africa": "South Africa",
    "이집트": "Egypt", "egypt": "Egypt",
    "몰디브": "Maldives",
    "투발루": "Tuvalu",
    "방글라데시": "Bangladesh",
    "에티오피아": "Ethiopia",
    "네팔": "Nepal",
}

ISSUE_ALIASES = {
    "GGA-IND": "GGA-IND", "글로벌 적응 목표 지표": "GGA-IND", "GGA 지표": "GGA-IND", "지표": "GGA-IND",
    "GGA-MOI": "GGA-MOI", "GGA 이행수단": "GGA-MOI", "이행수단": "GGA-MOI",
    "NAPs": "NAPs", "NAP": "NAPs", "국가적응계획": "NAPs", "적응계획": "NAPs",
    "JT-ADAPT": "JT-ADAPT", "정의로운 전환": "JT-ADAPT", "JT": "JT-ADAPT",
    "L&D-OP": "L&D-OP", "손실 피해": "L&D-OP", "손실·피해": "L&D-OP", "loss damage": "L&D-OP",
    "FINANCE-ADAPT": "FINANCE-ADAPT", "적응 재원": "FINANCE-ADAPT", "재원": "FINANCE-ADAPT", "finance": "FINANCE-ADAPT",
}

COP_ALIASES = {
    "COP26": "COP26", "cop26": "COP26", "글래스고": "COP26",
    "COP27": "COP27", "cop27": "COP27", "샤름": "COP27",
    "COP28": "COP28", "cop28": "COP28", "두바이": "COP28", "uae": "COP28",
    "COP29": "COP29", "cop29": "COP29", "바쿠": "COP29",
    "COP30": "COP30", "cop30": "COP30", "벨렘": "COP30", "브라질": "COP30",  # ambiguous
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class QueryIntent:
    """Parsed intent of a user question."""
    type: str                                # "compare" | "lookup" | "recommendation" | "factoid" | "unknown"
    countries: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    cop: Optional[str] = None
    raw_question: str = ""


@dataclass
class Citation:
    """Evidence citation attached to an answer."""
    country: str
    issue: str
    cop: str
    quote: str
    score: float


@dataclass
class Response:
    """Full Q&A response."""
    text: str                                # human-readable answer
    citations: list[Citation] = field(default_factory=list)
    viz_payload: dict = field(default_factory=dict)
    intent: Optional[QueryIntent] = None
    matched_records: int = 0
    confidence: float = 0.0

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "citations": [asdict(c) for c in self.citations],
            "viz_payload": self.viz_payload,
            "intent": asdict(self.intent) if self.intent else None,
            "matched_records": self.matched_records,
            "confidence": self.confidence
        }


# ---------------------------------------------------------------------------
# Data loader (in-memory)
# ---------------------------------------------------------------------------

_RECORDS_CACHE: list[dict] = []


def load_records() -> list[dict]:
    global _RECORDS_CACHE
    if _RECORDS_CACHE:
        return _RECORDS_CACHE
    if not DATA.exists():
        raise FileNotFoundError(f"v4 dataset missing: {DATA}. Run `python -m src.data.build_v4_dataset`")
    with open(DATA, "r", encoding="utf-8") as f:
        _RECORDS_CACHE = [json.loads(line) for line in f if line.strip()]
    return _RECORDS_CACHE


# ---------------------------------------------------------------------------
# Intent parsing
# ---------------------------------------------------------------------------

def parse_intent(question: str) -> QueryIntent:
    """Heuristic intent parser — identifies country, issue, COP, query type."""
    q = question.strip()
    q_lower = q.lower()

    # Country detection
    countries = []
    for alias, canonical in COUNTRY_ALIASES.items():
        if alias.lower() in q_lower and canonical not in countries:
            # Special case: "브라질" can mean either country or COP30 venue
            if alias == "브라질" and any(t in q for t in ["COP30", "cop30", "벨렘"]):
                continue
            countries.append(canonical)

    # Issue detection
    issues = []
    for alias, canonical in ISSUE_ALIASES.items():
        if alias.lower() in q_lower and canonical not in issues:
            issues.append(canonical)

    # COP detection
    cop = None
    for alias, canonical in COP_ALIASES.items():
        if alias.lower() in q_lower:
            cop = canonical
            break

    # Type detection
    qtype = "unknown"
    if any(w in q for w in ["비교", "차이", "다른", "vs", "versus"]) and len(countries) >= 2:
        qtype = "compare"
    elif any(w in q for w in ["권고", "전략", "어떻게", "추천", "recommend"]):
        qtype = "recommendation"
    elif any(w in q for w in ["입장", "위치", "스탠스", "stance", "position"]):
        qtype = "lookup"
    elif any(w in q for w in ["몇", "얼마", "how much", "what is the value"]):
        qtype = "factoid"
    elif countries and issues:
        qtype = "lookup"
    elif issues and not countries:
        qtype = "lookup"

    return QueryIntent(
        type=qtype,
        countries=countries,
        issues=issues,
        cop=cop or "COP30",  # default to COP30 (focal year)
        raw_question=q
    )


# ---------------------------------------------------------------------------
# Data lookup
# ---------------------------------------------------------------------------

def lookup(countries: list[str], issues: list[str], cop: Optional[str] = None) -> list[dict]:
    """Filter records by country/issue/COP."""
    records = load_records()
    result = []
    for r in records:
        meta = r["_meta"]
        if countries and meta["country"] not in countries:
            continue
        if issues and meta["issue"] not in issues:
            continue
        if cop and meta["cop"] != cop:
            continue
        result.append(r)
    return result


# ---------------------------------------------------------------------------
# Response generation (rule-based, with structured output)
# ---------------------------------------------------------------------------

def _format_score(s: float) -> str:
    sign = "+" if s >= 0 else ""
    return f"{sign}{s:.2f}"


def _stance_label_ko(s: float) -> str:
    if s >= 0.7: return "강한 지지"
    if s >= 0.3: return "지지"
    if s >= -0.3: return "중립"
    if s >= -0.7: return "반대"
    return "강한 반대"


def _build_compare_response(intent: QueryIntent, records: list[dict]) -> Response:
    if len(intent.countries) < 2:
        return _build_unknown_response(intent)

    # Group records by (country, issue) → take the COP-specific or most recent
    grouped = defaultdict(dict)
    for r in records:
        m = r["_meta"]
        grouped[m["country"]][m["issue"]] = r

    # If issues specified, restrict; else use all 6
    target_issues = intent.issues if intent.issues else ["GGA-IND", "GGA-MOI", "NAPs", "JT-ADAPT", "L&D-OP", "FINANCE-ADAPT"]

    # Build response text
    lines = []
    cop_display = intent.cop or "COP30"
    lines.append(f"**{' vs '.join(intent.countries)} 입장 비교 ({cop_display})**\n")

    citations = []
    payload = {"type": "comparison_bar", "labels": target_issues, "series": []}

    for c in intent.countries:
        c_records = grouped.get(c, {})
        scores = []
        for iss in target_issues:
            r = c_records.get(iss)
            if r:
                s = r["stance_score"]
                scores.append(s)
                if r.get("evidence_quote") and len(citations) < 6:
                    citations.append(Citation(
                        country=c, issue=iss, cop=r["_meta"]["cop"],
                        quote=r["evidence_quote"], score=s
                    ))
            else:
                scores.append(None)
        payload["series"].append({"name": c, "data": scores})
        lines.append(f"\n**{c}**:")
        for iss, s in zip(target_issues, scores):
            if s is not None:
                lines.append(f"  - {iss}: {_format_score(s)} ({_stance_label_ko(s)})")

    # Summary line
    if len(intent.countries) == 2 and len(target_issues) >= 1:
        c1, c2 = intent.countries[0], intent.countries[1]
        if c1 in grouped and c2 in grouped:
            iss = target_issues[0]
            r1 = grouped[c1].get(iss)
            r2 = grouped[c2].get(iss)
            if r1 and r2:
                diff = r1["stance_score"] - r2["stance_score"]
                lines.append(f"\n**핵심 차이 ({iss})**: {c1} {_format_score(r1['stance_score'])} 와 "
                             f"{c2} {_format_score(r2['stance_score'])} 사이의 차이는 {_format_score(diff)}로, "
                             f"{'유사한 입장' if abs(diff) < 0.2 else '뚜렷한 입장 차이'}을 보인다.")

    return Response(
        text="\n".join(lines),
        citations=citations,
        viz_payload=payload,
        intent=intent,
        matched_records=sum(len(grouped[c]) for c in intent.countries),
        confidence=0.85
    )


def _build_lookup_response(intent: QueryIntent, records: list[dict]) -> Response:
    """Single country, single (or multiple) issue lookup."""
    if not records:
        return Response(
            text="해당 조건에 부합하는 입장 데이터를 찾지 못했습니다. 국가명·이슈명을 다시 확인해 주세요.",
            intent=intent, confidence=0.0
        )

    lines = []
    citations = []
    payload = {"type": "stance_table", "rows": []}

    # Group by country for cleaner display
    by_country = defaultdict(list)
    for r in records:
        by_country[r["_meta"]["country"]].append(r)

    for country, recs in by_country.items():
        lines.append(f"\n**{country}** ({intent.cop or 'COP30'})")
        for r in recs:
            iss = r["_meta"]["issue"]
            s = r["stance_score"]
            frame = r.get("frame_type", "")
            chair = "👑 의장" if r["procedural_signals"]["is_chair_role"] else ""
            pen = " · 펜홀더" if r["procedural_signals"]["is_pen_holder"] else ""
            lines.append(f"  - {iss}: {_format_score(s)} ({_stance_label_ko(s)}) "
                         f"· frame={frame} {chair}{pen}")
            payload["rows"].append({
                "country": country, "issue": iss, "score": s,
                "frame": frame, "chair": r["procedural_signals"]["is_chair_role"]
            })
            if r.get("evidence_quote") and len(citations) < 6:
                citations.append(Citation(
                    country=country, issue=iss, cop=r["_meta"]["cop"],
                    quote=r["evidence_quote"], score=s
                ))

    return Response(
        text="\n".join(lines),
        citations=citations,
        viz_payload=payload,
        intent=intent,
        matched_records=len(records),
        confidence=0.85
    )


def _build_recommendation_response(intent: QueryIntent, records: list[dict]) -> Response:
    """Korean foreign policy recommendation."""
    # If Korea is in countries, give Korean recommendations
    target_country = "Korea" if "Korea" in intent.countries else (intent.countries[0] if intent.countries else "Korea")
    target_issues = intent.issues if intent.issues else ["GGA-IND", "L&D-OP"]

    # Look up target country's stance
    own_records = [r for r in records if r["_meta"]["country"] == target_country]
    own_by_issue = {r["_meta"]["issue"]: r for r in own_records}

    lines = [f"**{target_country} 외교부 권고 ({intent.cop or 'COP31 prospective'})**\n"]

    recommendations_db = {
        "GGA-IND": (
            "한국형 NAP 거버넌스 모델을 벨렘–아디스 작업 프로그램의 참조 모형으로 입력. "
            "탄소중립기본법 §47에 근거한 3단계 구조(중앙·지방·부문)를 활용하여 "
            "운영 가이드라인 표준 사례 위치 확보."
        ),
        "GGA-MOI": (
            "GCF 운영 효율성 지표 제안을 통해 자동 공여국 확대 논의를 측면에서 우회. "
            "GCF 호스트 국가의 운영 경험을 의제화."
        ),
        "NAPs": (
            "NAP 펜홀더 권한을 활용하여 한국형 적응 모델을 국제 표준 사례로 정착. "
            "다른 행위자(브라질 +0.88, AOSIS +0.78, EU +0.72)와 협력 가능한 영역."
        ),
        "JT-ADAPT": (
            "탄소중립기본법 §50의 취약계층·노동자 보호 조항을 COP31 본회의 장관 발언에서 "
            "명시적으로 언급하고 학술 논문으로 영문 발신을 동시 진행."
        ),
        "L&D-OP": (
            "한국 IRR 0.39로 6 이슈 중 최저 약점 영역. 손실·피해 기금 이사회에 대한 "
            "**자발적 기관 지원 약정 (연 5–10백만 달러 규모) 검토 시작**을 권고. "
            "단, 예산 편성 절차(환경부/외교부 → 기획재정부 → 국무회의 → 국회 의결)상 사전 검토 필수."
        ),
        "FINANCE-ADAPT": (
            "GCF 운영 효율 의제 주도로 협상 가시성 확보. 자동 공여국 base year 확대 "
            "논의를 측면에서 우회."
        ),
    }

    for iss in target_issues:
        rec_text = recommendations_db.get(iss)
        if rec_text:
            own_score = own_by_issue.get(iss, {}).get("stance_score", "?")
            lines.append(f"\n**{iss}** (현 입장: {_format_score(own_score) if isinstance(own_score, float) else own_score})")
            lines.append(f"  {rec_text}")

    citations = [
        Citation(country=target_country, issue=iss, cop=intent.cop or "COP30",
                 quote=own_by_issue[iss].get("evidence_quote", ""),
                 score=own_by_issue[iss]["stance_score"])
        for iss in target_issues if iss in own_by_issue
    ][:4]

    payload = {"type": "recommendation_list", "country": target_country,
               "issues": target_issues}

    return Response(
        text="\n".join(lines),
        citations=citations,
        viz_payload=payload,
        intent=intent,
        matched_records=len(own_records),
        confidence=0.8
    )


def _build_factoid_response(intent: QueryIntent, records: list[dict]) -> Response:
    """Specific number / fact lookup."""
    facts = {
        "delta": ("브라질 Translation Gap **Δ = 0.304** — Plano Clima 국내 정책 NATO 4축 사용률 67% 와 "
                   "L.25E 국제 voluntary 텍스트 사용률 23%의 차이. Putnam(1988) × Howlett(2019) 정책수단 분기 정량화."),
        "irr": ("한국 적응정책 종합 이행률 **IRR = 0.653** (95% 신뢰구간 [0.55, 0.71]). "
                "L&D-OP 영역의 0.39가 6 이슈 중 최저로 약점."),
        "nes": ("AILAC 8개국 규범 기업가 점수 **NES = 0.86** (4 criteria 중 3.5개 충족). "
                "Finnemore-Sikkink (1998) 4 criteria 적용."),
        "spearman": ("CINA Stage 1 입장 추출 정확도 **Spearman ρ = 0.658** (전문가 reference 대비). "
                      "MAE = 0.183. Phase 5 Task A 결과."),
        "cross_llm": ("5개 LLM 제공자 간 일치도 **Krippendorff α = 0.876 (원시) / 0.933 (편향 보정)**. "
                       "단, 5종 모두 transformer + RLHF 기반이므로 same-paradigm agreement이지 "
                       "shared-model bias 완전 분리는 아님."),
    }
    q = intent.raw_question.lower()
    matched = []
    if any(t in q for t in ["delta", "δ", "translation gap", "번역 격차", "0.304"]):
        matched.append(facts["delta"])
    if any(t in q for t in ["irr", "이행률", "0.653"]):
        matched.append(facts["irr"])
    if any(t in q for t in ["nes", "norm entrepreneur", "규범 기업가", "ailac"]):
        matched.append(facts["nes"])
    if any(t in q for t in ["spearman", "정확도", "task a"]):
        matched.append(facts["spearman"])
    if any(t in q for t in ["cross-llm", "krippendorff", "alpha", "α"]):
        matched.append(facts["cross_llm"])

    if not matched:
        return _build_lookup_response(intent, records)

    return Response(
        text="\n\n".join(matched),
        intent=intent,
        confidence=0.95
    )


def _build_unknown_response(intent: QueryIntent) -> Response:
    return Response(
        text=(
            "질문 의도를 명확히 파악하지 못했습니다. 다음과 같은 형식으로 다시 질문해 주세요:\n\n"
            "- **국가 비교**: '브라질과 한국의 GGA 지표 입장 차이는?'\n"
            "- **입장 조회**: 'AOSIS의 손실·피해 입장은?'\n"
            "- **권고 요청**: '한국이 COP31 L&D 이슈에서 어떻게 해야 하나?'\n"
            "- **사실 확인**: 'Translation Gap Δ 값은 얼마인가?'\n\n"
            "지원 국가 (30): Brazil, EU, USA, China, India, AOSIS, Korea, Saudi, Japan, AILAC, AGN, LMDC, "
            "Multi, Canada, Australia, Norway, UK, Germany, France, Mexico, Indonesia, South Africa, Egypt, "
            "Türkiye, Maldives, Marshall Is, Tuvalu, Bangladesh, Ethiopia, Nepal\n"
            "지원 이슈 (6): GGA-IND, GGA-MOI, NAPs, JT-ADAPT, L&D-OP, FINANCE-ADAPT\n"
            "지원 COP: COP26, COP27, COP28, COP29, COP30"
        ),
        intent=intent,
        confidence=0.0
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def answer_question(question: str) -> Response:
    """Answer a natural-language question about CINA stance data."""
    intent = parse_intent(question)
    records = lookup(intent.countries, intent.issues, intent.cop)

    if intent.type == "compare":
        return _build_compare_response(intent, records)
    elif intent.type == "lookup":
        return _build_lookup_response(intent, records)
    elif intent.type == "recommendation":
        return _build_recommendation_response(intent, records)
    elif intent.type == "factoid":
        return _build_factoid_response(intent, records)
    else:
        return _build_unknown_response(intent)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import sys

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    ap = argparse.ArgumentParser(description="CINA Q&A query engine CLI")
    ap.add_argument("question", nargs="?",
                    help="Natural-language question about CINA stance data")
    ap.add_argument("--demo", action="store_true",
                    help="Run 4 demo queries")
    args = ap.parse_args()

    if args.demo:
        queries = [
            "브라질과 한국의 GGA 지표 입장 차이는?",
            "AOSIS의 손실·피해 입장은?",
            "한국이 COP31 L&D 이슈에서 어떻게 해야 하나?",
            "Translation Gap Δ 값은 얼마인가?",
        ]
        for q in queries:
            print(f"\n{'=' * 70}")
            print(f"Q: {q}")
            print('=' * 70)
            r = answer_question(q)
            print(r.text)
            if r.citations:
                print(f"\n[인용 {len(r.citations)}건]")
                for c in r.citations[:2]:
                    print(f"  - {c.country} {c.issue} ({c.cop}): {c.quote[:100]}")
            print(f"\n신뢰도: {r.confidence:.2f}, 매칭 records: {r.matched_records}")
    elif args.question:
        r = answer_question(args.question)
        print(r.text)
        if r.citations:
            print(f"\n[인용 {len(r.citations)}건]")
            for c in r.citations:
                print(f"  - {c.country} {c.issue} ({c.cop}): {c.quote[:120]}")
    else:
        ap.print_help()
