"""Paper draft v1 자동 생성 — Track A 한국어 수업 제출 + Track B 영문 학술.

Stage 1 stances + IRR + chair_metadata + realist B0 모두 통합.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.paper")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


def load_evidence() -> dict:
    pack = {}
    for name, path in [
        ("stances", "data/processed/stances_full_v1.jsonl"),
        ("irr_brazil", "data/processed/irr_brazilian_translation_gap_v2.json"),
        ("realist_b0", "data/processed/realist_b0_statistics.json"),
        ("chair_stats", "data/processed/chair_metadata_stats_v2.json"),
        ("frame_dist", "data/processed/frame_distribution_round3.json"),
    ]:
        p = ROOT / path
        if not p.exists():
            continue
        if name == "stances":
            pack[name] = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        else:
            pack[name] = json.loads(p.read_text(encoding="utf-8"))
    return pack


SYSTEM_PAPER_KO = """당신은 국민대학교 기후기술융합학과 대학원생 Heedo의 학술 논문 초안을 작성합니다.

대상: 글로벌기후리더십 수업 제출 (2026년 5월 마감)
형식: 학술 보고서 (한국어, 약 5000자, 인용 형식)
주제: COP30 Belém Adaptation Indicators 분석 — CINA Framework 기반

구조:
# 제목
## Abstract (150단어)
## 1. 서론 — 연구 동기 + 연구 질문
## 2. 이론적 배경 — Regime Complex, Two-Level Games, Issue Linkage, Epistemic Communities
## 3. 데이터 및 방법론 — CINA 3-Stage 파이프라인
## 4. 결과 — 4 핵심 발견
   4.1 GGA-IND Authority 6.1
   4.2 IRR_Brazil Δ=0.304 CONFIRMED
   4.3 L.25 pre-crystallized formula
   4.4 Realist F1=0.560
## 5. 논의 — 학술 기여 + 정책 함의
## 6. 한국 정책에의 시사점 — IRR_Korea 0.653
## 7. 결론 + 향후 연구

원칙:
- 모든 정량 수치 정확
- evidence 인용
- 학술적 어조
- 할루시네이션 금지"""


SYSTEM_PAPER_EN = """You are drafting an academic paper for Global Environmental Change journal.

Target audience: Climate diplomacy researchers, IR scholars, policy analysts.
Length: ~6000 words English.
Topic: COP30 Belém Adaptation Indicators — A Multi-LLM CINA Framework Analysis

Structure:
# Title
## Abstract (200 words)
## 1. Introduction — research motivation + research questions
## 2. Theoretical Framework — Regime Complex (Keohane-Victor 2011), Two-Level Games (Putnam 1988), Issue Linkage (Tollison-Willett 1979), Epistemic Communities (Haas 1992)
## 3. Methodology — Three-stage LLM-GNN-LLM pipeline
   3.1 Stage 1: Calibrated stance extraction (NATO 4-axis instruments + frame_type + procedural)
   3.2 Stage 2: Heterogeneous temporal graph + R-GAT
   3.3 Stage 3: Graph-Grounded Generation
## 4. Empirical Validation — COP30 retrospective
   4.1 GGA-IND Authority axis 6.1 (lowest among 6 issues)
   4.2 Brazilian IRR Translation Gap Δ=0.304 CONFIRMED
   4.3 L.25 pre-crystallized formula hypothesis (Tallberg ii+iv + Steinberg + Goh)
   4.4 Realist B0 F1=0.560 (p<0.0001) — constructivist+frame variables justified
## 5. Discussion — Putnam × Howlett research gap
## 6. Implications for South Korea — IRR_Korea 0.653 case study
## 7. Limitations + Future Research

Citations: Use APA format with full reference list."""


def generate_paper(language: str = "ko") -> str:
    from src.stage1_extract.providers import get_provider

    evidence = load_evidence()
    stances_summary = []
    for s in evidence.get("stances", []):
        meta = s.get("_meta", {})
        stances_summary.append({
            "country": meta.get("country"),
            "issue": meta.get("issue"),
            "stance_score": s.get("stance_score"),
            "frame_type": s.get("frame_type"),
            "is_chair_role": s.get("procedural_signals", {}).get("is_chair_role"),
            "is_pen_holder": s.get("procedural_signals", {}).get("is_pen_holder"),
        })

    user = f"""다음 정량 evidence로 논문 작성:

=== Stage 1 LLM 추출 16건 ===
{json.dumps(stances_summary, ensure_ascii=False, indent=2)}

=== Brazilian IRR Translation Gap (R5) ===
- 국내: 0.714, 국제: 0.410, Δ=0.304 (CONFIRMED, 가설 임계 0.30 돌파)
- Negative Authority 6 토큰 분리 (shall_not×3, should_not×1, nor_establish×2)

=== Realist B0 통계 ===
- F1=0.560, McNemar p<0.0001, Cohen κ=0.216 vs Random F1=0.440

=== chair_metadata ===
- 56 records (COP21-30 historical)
- Brazil GGA-IND: is_chair_role=True + is_pen_holder=True 직접 검증

=== frame_distribution ===
- scientific 51 / mixed 24 / sovereignty 5 / justice 9 / development 5

=== 회고 검증 핵심 사례 ===
- Brazil GGA-IND stance 1.00 + frame=development
- India GGA-IND stance 0.80 + frame=justice (CBDR-RC)
- AOSIS ADAPT-FIN stance 0.80 + frame=development
- South Korea NAPs 0.80 + is_pen_holder=True

논문 본문 작성 시작."""

    provider = get_provider("groq", temperature=0.4, max_tokens=8000)
    system = SYSTEM_PAPER_KO if language == "ko" else SYSTEM_PAPER_EN
    logger.info("Generating paper draft (%s)...", language)
    resp = provider.complete(system, user, json_schema=None)
    return resp.content


def main() -> int:
    # Korean
    text_ko = generate_paper("ko")
    out_ko = ROOT / "deliverables" / "paper_draft_v1_ko.md"
    out_ko.parent.mkdir(parents=True, exist_ok=True)
    header_ko = f"""---
title: COP30 Belém Adaptation Indicators — CINA Framework 분석
author: Heedo (국민대학교 기후기술융합학과)
generated_at: {datetime.utcnow().isoformat()}Z
generator: CINA Stage 3 (Groq Llama 3.3 70B, free)
target: 국민대 글로벌기후리더십 수업 제출 (2026.05)
language: ko
status: v1_draft
---

"""
    out_ko.write_text(header_ko + text_ko, encoding="utf-8")
    logger.info("Korean paper draft: %s (%d chars)", out_ko, len(text_ko))

    # English
    text_en = generate_paper("en")
    out_en = ROOT / "deliverables" / "paper_draft_v1_en.md"
    header_en = f"""---
title: "From Text to Strategy — A Multi-LLM CINA Pipeline for Climate Diplomacy, Validated on COP30 Adaptation Outcomes"
author: Heedo (Kookmin University, Department of Climate Technology Convergence)
generated_at: {datetime.utcnow().isoformat()}Z
generator: CINA Stage 3 (Groq Llama 3.3 70B, free)
target: Global Environmental Change / NeurIPS Climate Change AI Workshop 2026
language: en
status: v1_draft
---

"""
    out_en.write_text(header_en + text_en, encoding="utf-8")
    logger.info("English paper draft: %s (%d chars)", out_en, len(text_en))
    return 0


if __name__ == "__main__":
    sys.exit(main())
