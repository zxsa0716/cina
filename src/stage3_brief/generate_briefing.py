"""Stage 3 ministerial briefing 자동 생성 — Groq Llama 3.3 70B.

Stage 1 stances_full_v1.jsonl + 정제 산출물 (chair_metadata, IRR_Korea/Brazil,
realist_b0, hedging_2d) 모두 종합해서 외교부 장관급 보고서 자동 작성.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("cina.stage3")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


def load_evidence_pack() -> dict:
    """모든 정량 evidence 종합."""
    pack = {}

    # Stage 1 stances
    p = ROOT / "data" / "processed" / "stances_full_v1.jsonl"
    if p.exists():
        pack["stances"] = []
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                pack["stances"].append(json.loads(line))

    # IRR_Brazil
    p = ROOT / "data" / "processed" / "irr_brazilian_translation_gap_v2.json"
    if p.exists():
        pack["irr_brazil"] = json.loads(p.read_text(encoding="utf-8"))

    # Realist B0
    p = ROOT / "data" / "processed" / "realist_b0_statistics.json"
    if p.exists():
        pack["realist_b0"] = json.loads(p.read_text(encoding="utf-8"))

    # Chair metadata stats
    p = ROOT / "data" / "processed" / "chair_metadata_stats_v2.json"
    if p.exists():
        pack["chair_stats"] = json.loads(p.read_text(encoding="utf-8"))

    # Frame distribution
    p = ROOT / "data" / "processed" / "frame_distribution_round3.json"
    if p.exists():
        pack["frame_dist"] = json.loads(p.read_text(encoding="utf-8"))

    return pack


SYSTEM_BRIEFING = """당신은 외교부 기후환경과학외교국에서 장관급 보고서를 작성하는 전문 분석가입니다.

CINA (Climate Issue-Network Analysis) 프레임워크의 정량 분석 결과를 받아서, 한국 기후대사가 COP31 (2026.11 Turkey) 협상에 활용할 전략 브리핑을 작성합니다.

브리핑 구조:
## §1. 경영진 요약 (5 bullets, 각 30단어)
## §2. 현황 평가
   - 6개 적응 하위 이슈별 협상 지형
## §3. 연합 지형 (Coalition Map)
   - 이슈별 실질 연합 분석
## §4. 레버리지 분석
   - 의장국 procedural authority + 브릿지 국가
## §5. 패키지 딜 기회
## §6. Red Lines 및 위험
   - 한국 측 red line + 합의 실패 위험
## §7. 권고 전략 자세
   - 우선순위 매트릭스 + 접촉 시퀀스
## §8. 결론

원칙:
- 모든 주장에 evidence (stance_score, frame_type, IRR 등) 인용
- 한국어 (외교부 보고 문체)
- 정량 수치 정확
- 할루시네이션 금지 — 데이터에 없는 사실 만들지 말 것
"""


def build_user_prompt(evidence: dict) -> str:
    stances_summary = []
    for s in evidence.get("stances", []):
        meta = s.get("_meta", {})
        stances_summary.append({
            "country": meta.get("country"),
            "issue": meta.get("issue"),
            "stance": s.get("stance_score"),
            "category": s.get("stance_category"),
            "frame": s.get("frame_type"),
            "is_chair": s.get("procedural_signals", {}).get("is_chair_role"),
            "is_pen_holder": s.get("procedural_signals", {}).get("is_pen_holder"),
            "key_demands": s.get("key_demands", [])[:2],
        })

    irr_brazil = evidence.get("irr_brazil", {})

    return f"""다음 CINA 정량 분석 결과를 바탕으로 한국 기후대사 장관급 브리핑 작성:

=== Stage 1 LLM 추출 stance 데이터 (16개 country×issue) ===
{json.dumps(stances_summary, ensure_ascii=False, indent=2)}

=== Brazilian IRR Translation Gap (R5 CONFIRMED) ===
- IRR 국내 (Plano Clima): 0.714
- IRR 국제 (COP30 GGA): 0.410 (negative Authority 분리 후)
- Δ = 0.304 (학술 가설 임계 0.30 돌파)
- 의의: Putnam Two-Level Games × Howlett instrument calibration 빈자리 정량화

=== Realist B0 통계 ===
- F1 = 0.560, p<0.0001 vs random 0.440
- 함의: realism alone insufficient → CINA constructivist+frame 변수 정당화

=== chair_metadata ===
- 총 56 records (COP21-30)
- Brazil GGA-IND에서 is_chair=True + is_pen_holder=True 직접 확인
- Tallberg formula control 4 channel 평가 가능

=== frame_distribution ===
- scientific 51, mixed 24, sovereignty 5, justice 9, development 5

각 §1-§8를 채우세요. 한국어로 작성. 외교부 공식 보고체."""


def generate_briefing() -> str:
    from src.stage1_extract.providers import get_provider

    evidence = load_evidence_pack()
    logger.info("Evidence pack: %d stances, IRR=%s, F1=%s",
                len(evidence.get("stances", [])),
                evidence.get("irr_brazil", {}).get("delta_revised", "?"),
                evidence.get("realist_b0", {}).get("f1", "?"))

    provider = get_provider("groq", temperature=0.3, max_tokens=8000)
    user = build_user_prompt(evidence)

    logger.info("Generating briefing (target ~5000 tokens)...")
    resp = provider.complete(
        system=SYSTEM_BRIEFING,
        user=user,
        json_schema=None,  # markdown output
    )

    return resp.content


def main() -> int:
    text = generate_briefing()

    out = ROOT / "deliverables" / "ministerial_briefing_ko_v1.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    header = f"""---
title: COP31 협상 전략 브리핑 (한국 기후대사)
generated_at: {datetime.utcnow().isoformat()}Z
generator: CINA Stage 3 (Groq Llama 3.3 70B, free)
evidence_base: data/processed/stances_full_v1.jsonl + 4 정량 산출물
language: ko
status: v1_draft
---

"""
    out.write_text(header + text, encoding="utf-8")
    logger.info("Briefing saved: %s (chars: %d)", out, len(text))
    print(f"\n=== Briefing 일부 미리보기 ===\n")
    print(text[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
