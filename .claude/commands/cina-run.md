---
description: CINA 파이프라인 전체를 실행한다 (Stage 1→2→3)
argument-hint: [stages: all|1,2,3|2,3] [--language ko|en]
---

CINA 파이프라인을 실행합니다. `cina-orchestrator` skill을 사용하여 사전 검증, Stage 실행, 품질 게이트, 사후 리포트까지 자동 처리합니다.

인자:
- `$ARGUMENTS` — 실행할 stage (예: `2,3` 으로 Stage 1 스킵) 및 옵션

진행 순서:
1. `.claude/skills/cina-orchestrator/SKILL.md` 참조
2. 사전 점검: `data/raw/` 문서 유무, `data/calibration/` 세트 확인
3. Stage 1 → 2 → 3 순차 실행 (각 스킬 위임)
4. `deliverables/` 에 최종 브리핑 생성
5. 실행 리포트 `deliverables/run_report_{timestamp}.md`

에러 시 stage별 산출물은 유지, 실패 지점 명시.
