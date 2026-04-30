"""Paper draft v2 — 고도화·방대화. Gemini 2.5 Flash-Lite 사용 (Groq TPD 한도 도달).

Stage 1 21 records + Stage 2 graph_analysis_v1 + IRR + chair_metadata 모두 통합.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.paper.v2")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


def load_evidence() -> dict:
    pack = {}
    paths = {
        "stances_seed": "data/processed/stances_seed_v1.jsonl",
        "stances_full": "data/processed/stances_full_v1.jsonl",
        "graph_analysis": "data/processed/graph_analysis_v1.json",
        "irr_brazil": "data/processed/irr_brazilian_translation_gap_v2.json",
        "realist_b0": "data/processed/realist_b0_statistics.json",
        "chair_stats": "data/processed/chair_metadata_stats_v2.json",
        "frame_dist": "data/processed/frame_distribution_round3.json",
    }
    for name, path in paths.items():
        p = ROOT / path
        if not p.exists():
            continue
        if path.endswith(".jsonl"):
            pack[name] = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        else:
            pack[name] = json.loads(p.read_text(encoding="utf-8"))
    return pack


SECTIONS_KO = [
    ("abstract", "초록 (300단어). 연구 목적, 방법, 핵심 발견 4건, 학술 기여, 정책 함의를 압축적으로 서술."),
    ("intro", "1. 서론 (1500자). 기후 협상의 복잡성, 기존 AI 도구의 한계 (NegotiateCOP, RICE-N, Castro 2025), 연구 질문 3가지, 본 연구의 학술적·실천적 의의."),
    ("theory", "2. 이론적 배경 (2000자). Regime Complex (Keohane-Victor 2011), Two-Level Games (Putnam 1988), Issue Linkage (Tollison-Willett 1979), Epistemic Communities (Haas 1992), 4개 이론을 CINA 모듈에 어떻게 매핑했는지."),
    ("method", "3. 데이터 및 방법론 (3000자). CINA 3-Stage 파이프라인 상세. Stage 1: NATO 4축 instrument_signals + frame_type 5범주 + procedural_signals (chair_status, pen_holder) + Bayesian credible interval. Stage 2: 이종 시간 그래프 + R-GAT + Leiden community detection + cross-issue hypergraph. Stage 3: Graph-Grounded Generation + evidence traceability."),
    ("result1", "4.1 GGA-IND Authority 6.1 (1500자). UAE-Belém 59 indicators의 'voluntary, non-prescriptive, context-specific' 언어가 binding force 부재의 구조적 evidence임을 NATO 4축 분포로 정량 검증. Howlett (2019) instrument calibration 이론과의 정합성."),
    ("result2", "4.2 IRR_Brazil Translation Gap Δ=0.304 CONFIRMED (1500자). Plano Clima 국내 (Authority+Nodality+Org 3축) vs COP30 GGA voluntary 언어의 paradox. Negative Authority (shall NOT) 6 토큰 분리 후 Δ 0.269 → 0.304. Putnam Two-Level Games × Howlett instrument calibration 학술 빈자리 정량화. 16 Plano Clima sectoral plans + L.25E 결정문 직접 비교."),
    ("result3", "4.3 L.25 pre-crystallized formula 가설 (1500자). L.25 advance ≡ final, hot spots = 0. Tallberg (2010) chairman power formula control + agenda-shaping이 advance 배포 *이전* 비공식 협의에서 완성됨. Steinberg (2002) consensus shaping + Goh (2007) informal pre-cooking 통합 framing. Para 7 hedging density 분석 (voluntary + non-prescriptive + non-punitive + facilitative 4연속)."),
    ("result4", "4.4 Realist B0 F1=0.560 (1500자). CO2 per cap + share global CO2 + GDP 기반 realist similarity matrix만으로는 협상 협력 예측 불가능 (F1 0.560 vs random 0.440, McNemar p<0.0001, Cohen κ=0.216). 이는 CINA의 constructivist + frame_type + procedural 변수 추가 필요성의 empirical 정당화. AILAC vs AOSIS vs LDC 3-cluster 시각적 분리 (norm entrepreneur 가설)."),
    ("stage1_results", "4.5 Stage 1 LLM 추출 결과 (1500자). 21 country×issue 추출 (Groq Llama 3.3 70B, $0). Brazil GGA-IND stance=1.00 + frame=development + is_chair_role=True + is_pen_holder=True 직접 검증. India frame=justice (CBDR-RC) 일관 (×2 issues). South Korea NAPs is_pen_holder=True (Track A 직접). Stage 2 graph: 5 countries × 6 issues 매트릭스 + Leiden community + procedural authority + cross-issue hyperedges (Brazil dominant=development ×3, India dominant=justice ×2)."),
    ("discussion", "5. 논의 (2000자). 학술 기여 5가지: (1) end-to-end LLM-GNN-LLM 파이프라인 신규성, (2) Calibrated stance extraction with Bayesian uncertainty, (3) Heterogeneous temporal graph for climate diplomacy, (4) Cross-issue linkage hypergraph (Issue Linkage 이론 첫 계산적 구현), (5) Graph-Grounded Generation. 정책 함의: COP31 Turkey 협상 적용성. 한계: 단일 코더 calibration set, COP30 단일 retrospective."),
    ("korean_implications", "6. 한국 정책에의 시사점 (1500자). IRR_Korea 0.653 (CI [0.55, 0.71]). 30 cells crosswalk 분석. L&D-OP 평균 0.39 최약점 = 한국 EIG + 중간소득 기여국 dual identity 모호. COP31 권고: FRLD 이사회 institutional support pledge $5-10M + AOSIS·LDC 비경제적 손실 기술협력 제안. Stage 1 검증: Korea NAPs is_pen_holder=True + frame=development."),
    ("conclusion", "7. 결론 + 향후 연구 (1000자). 핵심 발견 4건의 학술 기여 종합. CINA가 climate diplomacy AI 분석 도구의 새 표준이 될 수 있음. 향후: Castro 2025 cooperation matrix 정식 입수 후 F1 재산출, COP31-32 prospective validation, Stage 2 R-GAT (torch-based) 학습."),
    ("references", "참고 문헌 (15-20건). Keohane & Victor 2011, Putnam 1988, Tollison & Willett 1979, Haas 1992, Howlett 2019, Tallberg 2010, Steinberg 2002, Goh 2007, Finnemore & Sikkink 1998, Bayer-Urpelainen 2013, Castro et al. 2025, IPCC AR6 WGII, FCCC/PA/CMA/2025/L.25E. APA 형식."),
]


SECTIONS_EN = [
    ("abstract", "Abstract (250 words). Research motivation, methodology, 4 key findings, academic contributions, policy implications, in compressed form."),
    ("intro", "1. Introduction (1500 words). Climate negotiations complexity, limitations of existing AI tools (NegotiateCOP, RICE-N, Castro 2025), 3 research questions, academic and practical significance."),
    ("theory", "2. Theoretical Framework (2000 words). Regime Complex (Keohane-Victor 2011), Two-Level Games (Putnam 1988), Issue Linkage (Tollison-Willett 1979), Epistemic Communities (Haas 1992), and how each maps to CINA modules."),
    ("method", "3. Data and Methodology (3000 words). CINA 3-Stage pipeline detailed. Stage 1: NATO 4-axis instrument_signals + frame_type 5 categories + procedural_signals + Bayesian credible interval. Stage 2: heterogeneous temporal graph + R-GAT + Leiden + cross-issue hypergraph. Stage 3: Graph-Grounded Generation + evidence traceability."),
    ("results", "4. Empirical Validation on COP30 (4000 words, comprehensive). 4 key findings with full quantitative evidence, citations, statistical tests, and interpretation. Tables and figures referenced."),
    ("discussion", "5. Discussion (2500 words). 5 academic contributions, policy implications, limitations, comparison to existing literature."),
    ("korea_case", "6. Korean Case Study (1500 words). IRR_Korea 0.653 cross-walk analysis. L&D-OP 0.39 weakness. COP31 strategic recommendations."),
    ("conclusion", "7. Conclusion + Future Work (1000 words). Synthesis of findings. Future: Castro matrix integration, COP31-32 prospective validation, Stage 2 R-GAT torch implementation."),
    ("references", "References (20-30 items). Full APA citations."),
]


def build_section_prompt(section_name: str, section_desc: str, evidence: dict, lang: str) -> str:
    stances_summary = []
    for s in evidence.get("stances_full", [])[:21]:
        meta = s.get("_meta", {})
        stances_summary.append({
            "country": meta.get("country"),
            "issue": meta.get("issue"),
            "stance": s.get("stance_score"),
            "category": s.get("stance_category"),
            "frame": s.get("frame_type"),
            "is_chair": s.get("procedural_signals", {}).get("is_chair_role"),
            "is_pen": s.get("procedural_signals", {}).get("is_pen_holder"),
            "confidence": s.get("confidence"),
            "demands": s.get("key_demands", [])[:2],
        })

    graph = evidence.get("graph_analysis", {})

    return f"""다음 정량 evidence를 바탕으로 논문의 §"{section_name}" 섹션을 작성하라:

=== Section 요구사항 ===
{section_desc}

=== Stage 1 LLM 추출 (21 records) ===
{json.dumps(stances_summary, ensure_ascii=False, indent=2)[:3000]}

=== Stage 2 Graph Analysis ===
- Countries with stance: {graph.get('_meta', {}).get('n_countries', 'N/A')}
- Top centrality (mean_abs_stance): {json.dumps(dict(list(graph.get('country_centralities', {}).items())[:5]), ensure_ascii=False)}
- Procedural authority: {json.dumps(graph.get('procedural_authority', {}), ensure_ascii=False)}
- Cross-issue hyperedges (frame consistency): {json.dumps(graph.get('cross_issue_hyperedges', [])[:8], ensure_ascii=False)}

=== IRR_Brazil Translation Gap ===
- Δ_revised = 0.304 CONFIRMED (가설 0.30 임계 돌파)
- 국내 0.714 (Plano Clima) vs 국제 0.410 (COP30 GGA negative Authority 분리 후)
- Negative Authority: shall_not×3, should_not×1, nor_establish×2

=== Realist B0 통계 ===
- F1=0.560 [95% CI 0.458-0.654]
- McNemar χ²=16.1, p<0.0001 vs random F1=0.440
- Cohen κ=0.216 (fair)

=== chair_metadata ===
- 56 records (COP21-30 historical)
- Brazil GGA-IND/NAPs: chair_role=True + pen_holder=True 직접 검증

=== frame_distribution ===
- scientific 51 / mixed 24 / sovereignty 5 / justice 9 / development 5

=== L.25 pre-crystallized formula ===
- L.25 advance ≡ L.25E final, hot spots = 0
- Para 7 hedging density: voluntary + non-prescriptive + non-punitive + facilitative 4-burst

언어: {lang}.
출력: 학술 논문체. 모든 수치 정확. evidence 인용. 할루시네이션 금지.
길이: 위 §"{section_name}" 요구사항 정확히 따를 것.

섹션 본문만 출력 (제목 포함). markdown 형식. 한국어 또는 영어 (lang에 따라)."""


def generate_section(provider, section_name: str, section_desc: str, evidence: dict, lang: str) -> str:
    user = build_section_prompt(section_name, section_desc, evidence, lang)
    sys_msg = "You are an academic paper writer. Output the requested section in markdown."
    resp = provider.complete(sys_msg, user, json_schema=None)
    return resp.content


def main(lang: str = "ko") -> int:
    from src.stage1_extract.providers import get_provider

    evidence = load_evidence()
    logger.info("Evidence pack loaded: %d sources", len(evidence))

    # Use Gemini (Groq TPD limit reached)
    provider = get_provider("gemini", temperature=0.4, max_tokens=4000)
    logger.info("Provider: %s / %s", provider.name, provider.model)

    sections = SECTIONS_KO if lang == "ko" else SECTIONS_EN
    paper_parts = []

    title = ("# CINA: COP30 Belém Adaptation Indicators 분석 — LLM-GNN-LLM 파이프라인의 회고적 검증"
             if lang == "ko"
             else "# From Text to Strategy: A Multi-LLM Climate Issue-Network Analysis (CINA) Pipeline, "
                  "Retrospectively Validated on COP30 Adaptation Outcomes")

    paper_parts.append(title)
    paper_parts.append("\n---\n")
    paper_parts.append(f"**Author**: Heedo (Kookmin University, Department of Climate Technology Convergence)")
    paper_parts.append(f"**Generated**: {datetime.utcnow().isoformat()}Z (Gemini 2.5 Flash-Lite, free)")
    paper_parts.append(f"**Status**: v2 draft — comprehensive\n")

    for sec_name, sec_desc in sections:
        logger.info("Generating §%s...", sec_name)
        try:
            content = generate_section(provider, sec_name, sec_desc, evidence, lang)
            paper_parts.append("\n\n" + content)
            print(f"  + §{sec_name}: {len(content)} chars")
        except Exception as exc:
            logger.warning("Section %s failed: %s", sec_name, exc)
            paper_parts.append(f"\n\n## §{sec_name}\n\n[Generation failed: {exc}]\n")

    full_paper = "\n".join(paper_parts)
    out = ROOT / "deliverables" / f"paper_draft_v2_{lang}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(full_paper, encoding="utf-8")
    logger.info("Paper v2 saved: %s (%d chars)", out, len(full_paper))
    return 0


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 else "ko"
    sys.exit(main(lang))
