---
description: 기존 Stage 1/2 결과로 장관급 브리핑만 생성 (Stage 3 단독)
argument-hint: [--language ko|en]
---

`briefing-composer` skill로 장관급 전략 브리핑을 생성합니다. Stage 1과 2는 이미 실행됐다고 가정합니다.

진행 순서:
1. `data/processed/stances.jsonl`, `data/processed/graph_analysis.json` 로딩
2. `docs/09_ministerial_briefing_template.md` 템플릿 기반 섹션별 생성
3. 각 섹션에 대해 `evidence-validator` skill로 검증
4. Evidence Traceability Table 자동 생성
5. `deliverables/ministerial_briefing.md` (또는 `_en.md`) 저장

$ARGUMENTS 에 `--language en` 이 있으면 영어 논문용 버전 생성.
