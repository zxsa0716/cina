"""Ministerial briefing v2 — 한국 기후대사 COP31 협상 전략 (고품질).

Gemini 2.5 Flash-Lite. 9 sections, comprehensive, 외교부 보고체.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.briefing.v2")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


def load_evidence() -> dict:
    pack = {}
    for name, path in [
        ("stances", "data/processed/stances_full_v1.jsonl"),
        ("seed_stances", "data/processed/stances_seed_v1.jsonl"),
        ("graph", "data/processed/graph_analysis_v1.json"),
        ("irr_brazil", "data/processed/irr_brazilian_translation_gap_v2.json"),
        ("realist", "data/processed/realist_b0_statistics.json"),
        ("chair", "data/processed/chair_metadata_stats_v2.json"),
    ]:
        p = ROOT / path
        if not p.exists():
            continue
        if path.endswith(".jsonl"):
            pack[name] = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        else:
            pack[name] = json.loads(p.read_text(encoding="utf-8"))
    return pack


SECTIONS = [
    ("exec_summary", """경영진 요약 (Executive Summary, 1 page).
5 bullets, 각 30단어 이내. 핵심 메시지 우선순위:
1) COP30 결과 핵심 (Belém Adaptation Indicators 59개, 'voluntary, non-prescriptive')
2) 한국 IRR_Korea_2025 = 0.653 (CI [0.55, 0.71]), L&D-OP 평균 0.39 최약점
3) 브라질 의장국 procedural authority (chair=NAPs, pen=GGA-IND+NAPs) 정량 검증
4) AOSIS norm entrepreneur 가설 CONFIRMED (mean_abs=0.90)
5) COP31 (Turkey) 협상 우선순위
"""),
    ("situation", """§1. 현황 평가 (1500자).
1-1. COP30 (벨렘, 2025.11) 결과 종합
1-2. UAE-Belém Indicators 9 thematic targets 5개 수집 (water/food/health/infrastructure/ecosystems)
1-3. Belém-Addis vision 두 트랙 (정치 + 기술)
1-4. 한국 측 입장 (외교부 보도자료 seq=376685): 방어적·외교적 stance
"""),
    ("coalition_map", """§2. 연합 지형 (Coalition Map, 1500자).
이슈별 실질 연합 (Stage 2 graph_analysis_v1.json 기반):
- GGA-IND: strong_support 5국 (Brazil, AOSIS, India, Korea, Multi)
- ADAPT-FIN: strong_support 2국 (AOSIS, India), neutral 1국 (Brazil)
- L&D-OP: neutral 1국 (Brazil)
- NAPs: strong_support 2국 (Brazil, Korea)
- MIT-ADAPT: strong_support 1국 (Brazil)
- JT-ADAPT: strong_support 1국 (Brazil)

frame consistency (cross-issue hyperedges):
- Brazil dominant=development (×3 issues)
- India dominant=justice (×2 issues, CBDR-RC)
- Korea dominant=development (×2 issues)
"""),
    ("leverage", """§3. 레버리지 분석 (1500자).
3-1. 의장국 procedural authority (Tallberg 4 channel):
- Brazil: chair_role on NAPs + pen_holder on GGA-IND/NAPs (Stage 1 LLM 직접 검증)
- 한국: pen_holder on NAPs (Track A 경쟁 우위 가능)
3-2. 브릿지 국가:
- South Africa (BASIC + African Group)
- Brazil (의장국 + G77 리더)
- Mexico (AILAC + EIG)
3-3. 영향력 허브 (mean_abs_stance):
- AOSIS 0.90 (norm entrepreneur)
- India 0.90 (CBDR-RC 일관)
- Korea 0.80 (sovereign development)
"""),
    ("packages", """§4. 패키지 딜 기회 (1500자).
4-1. GGA-IND × ADAPT-FIN 연계 (높은 hyperedge 가능성):
- 제안 블록: AOSIS + LDC + EU
- 한국 참여 가치: 중진국 위치 (EIG 멤버), brokerage 가능성
4-2. NAPs × 기술 이전:
- 한국 강점 (5년 주기, 17개 부문, 시도 NAP 의무, IRR 0.78)
- Korea pen_holder = 외교적 영향력 활용 가능
4-3. JT-ADAPT × 원주민 권리:
- Brazilian Plano Clima 16 sectoral plans (Igualdade Racial, Povos Indígenas)
- 한국 참여 제한적 (취약 분야)
"""),
    ("red_lines", """§5. Red Lines 및 위험 (1500자).
5-1. 한국 측 red lines (외교부 보도자료 기반):
- 기여국 의무 확대 회피 (NCQG)
- 기존 GCF 출연 외 추가 부담 거부
5-2. 합의 실패 위험 영역:
- ADAPT-FIN: '3배 확대' 공약 vs 실제 출연 격차
- L&D-OP: 한국이 EIG + 중간소득 dual identity 모호 (IRR 0.39 최약점)
- GGA-IND: 'voluntary' 언어로 binding force 부재 (Howlett instrument calibration)
5-3. 한국 IRR cross-walk 결과:
- HIGH: NAPs (0.78), GGA-IND health 9c (0.80), 인프라 9e (0.78)
- LOW: L&D-OP (0.39 평균)
"""),
    ("recommendations", """§6. 권고 전략 자세 (Strategic Posture, 2000자).
6-1. 우선순위 매트릭스:
| 이슈 | 한국 중요도 | 합의 난이도 | 권고 자세 | 근거 |
|------|------------|-------------|-----------|------|
| GGA-IND | 高 | 高 | 주도 | pen_holder 가능, EIG 위치 |
| NAPs | 高 | 中 | 주도 | IRR 0.78, 5년 주기 강점 |
| ADAPT-FIN | 中 | 中 | 참여 | 기여 부담 우려 |
| L&D-OP | 高 | 高 | 참여 | IRR 0.39 최약점 — 정체성 정립 필요 |
| MIT-ADAPT | 中 | 中 | 관망 | Brazilian framing 따라가기 |
| JT-ADAPT | 中 | 中 | 참여 | 국내 정치 조율 필요 |

6-2. 접촉 시퀀스:
주차 1: 남아프리카 (BASIC + AGN bridge), Mexico (AILAC + EIG), Brazil chair team
주차 2: AOSIS 의장 (vulnerability framing 공유), EU 환경총국, LDC 협상팀
주차 3: 일본 (Umbrella + EIG 협력), 노르웨이 (HAC), 사우디 (Arab Group bridge)

6-3. 양보 가능 영역 vs 유지 영역:
- 양보 가능: GGA-IND voluntary 지지 (이미 합의), NAPs 표준화 협력
- 유지: NCQG 한도 안 늘림, GCF 출연 한도 유지
"""),
    ("scenarios", """§7. 시나리오 분석 (1500자).
7-1. 최선 시나리오 (Prob ~25%):
- GGA-IND 정량 지표 채택 + 기술 이전 의무화
- 한국 EIG 리더십 확보 + 한국 NAP 모범 사례 채택
- IRR_Korea 0.65 → 0.75 도약 가능

7-2. 기본 시나리오 (Prob ~50%):
- GGA-IND voluntary 유지, 점진적 강화
- ADAPT-FIN 3배 확대 부분 실현
- 한국 stance 안정 유지

7-3. 최악 시나리오 (Prob ~25%):
- Belém-Addis vision 정체
- L&D 기금 운영 지연
- 한국 dual identity 모호함 노출
- 외교부 권고: 사전 명확화
"""),
    ("conclusion", """§8. 결론 (1000자).
한국 기후대사 COP31 협상의 핵심 메시지:
1) NAPs + GGA-IND 9c health 9e infrastructure 강점 활용 — 'best practice' 전파자 역할
2) L&D-OP 정체성 명확화 — '기여+수혜 dual' 또는 '중진국 brokerage' 선택
3) 의장국 브라질의 procedural authority 인식 + EIG 차원 사전 협상
4) Belém Adaptation Indicators 측정 표준화에 한국 기술력 (IPCC AR6 적응) 기여
"""),
    ("appendix", """## Appendix A. Evidence Traceability Table.
| Claim ID | 본문 발췌 | Evidence | Source | Confidence |
|----------|----------|----------|--------|-----------|
- 본 브리핑의 모든 정량 주장 (IRR_Korea 0.653, IRR_Brazil Δ 0.304, F1 0.560 등)에 대해 추적 테이블 작성.

## Appendix B. 데이터 계보.
- Manifest 225 entries
- Stage 1 21 LLM extractions ($0 Groq Llama 3.3 70B)
- Stage 2 graph_analysis_v1 (5 countries × 6 issues + procedural authority + cross-issue hyperedges)
- 16 Brazilian Plano Clima sectoral plans (정합성 검증)

## Appendix C. 불확실성 및 한계.
- 단일 LLM (Groq) 추출, ensemble validation 부분 (Gemini scanner + Ollama RAM 부족)
- Calibration set n=20 (목표 50)
- COP30 단일 retrospective
- 한국 측 정보는 공개 자료 기반 (외교부 보도자료)
"""),
]


def main() -> int:
    from src.stage1_extract.providers import get_provider

    evidence = load_evidence()
    logger.info("Evidence: %d Stage 1 records", len(evidence.get("stances", [])))

    provider = get_provider("gemini", temperature=0.3, max_tokens=4000)
    logger.info("Provider: %s / %s", provider.name, provider.model)

    parts = [
        "# 외교부 기후환경과학외교국 보고",
        "",
        f"**문서번호**: KR-CLI-2026-CINA-001",
        f"**등급**: CINA Framework v2.0 자동생성 (Gemini 2.5 Flash-Lite, free)",
        f"**작성일**: {datetime.utcnow().strftime('%Y-%m-%d')}",
        f"**작성자**: CINA Stage 3 Briefing Composer",
        f"**수신**: 김성환 기후에너지환경부 장관 (또는 정기용 외교부 기후변화대사) 귀하",
        f"**제목**: COP31 (Turkey, 2026.11) 협상 전략 브리핑 — CINA Framework 기반 정량 분석",
        "",
        "---",
        "",
    ]

    sys_msg = "You are an expert briefing writer for South Korean Ministry of Foreign Affairs. Write in formal Korean diplomatic style."

    for sec_name, sec_desc in SECTIONS:
        logger.info("Generating §%s...", sec_name)
        # context size 보호
        evidence_brief = {
            "stances_count": len(evidence.get("stances", [])) + len(evidence.get("seed_stances", [])),
            "graph_summary": {
                "n_countries": evidence.get("graph", {}).get("_meta", {}).get("n_countries"),
                "procedural_authority": evidence.get("graph", {}).get("procedural_authority"),
                "cross_issue_hyperedges": evidence.get("graph", {}).get("cross_issue_hyperedges", [])[:5],
            },
            "irr_brazil_delta": 0.304,
            "irr_korea": 0.653,
            "realist_f1": 0.560,
            "chair_metadata_n": 56,
        }
        user = f"""{sec_desc}

=== 정량 evidence ===
{json.dumps(evidence_brief, ensure_ascii=False, indent=2)}

언어: 한국어. 외교부 공식 보고체. 모든 수치 정확. evidence 인용. 위 §" 요구사항 정확히 따를 것."""
        try:
            resp = provider.complete(sys_msg, user, json_schema=None)
            parts.append(resp.content)
            parts.append("")
            print(f"  + §{sec_name}: {len(resp.content)} chars")
        except Exception as exc:
            logger.warning("Section %s failed: %s", sec_name, exc)
            parts.append(f"\n## §{sec_name}\n\n[Generation failed: {exc}]\n")

    full_briefing = "\n".join(parts)
    out = ROOT / "deliverables" / "ministerial_briefing_v2_ko.md"
    out.write_text(full_briefing, encoding="utf-8")
    logger.info("Briefing v2 saved: %s (%d chars)", out, len(full_briefing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
