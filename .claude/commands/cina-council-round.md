---
description: CINA 협의체의 한 라운드(Phase A~E)를 실행
argument-hint: [round-number 또는 "next"]
---

CINA 협의체의 한 라운드를 실행합니다. `council-orchestrator` skill을 사용합니다.

$ARGUMENTS:
- 특정 번호 (예: `3`) → 해당 라운드 실행
- `next` 또는 미지정 → `state.json.current_round + 1`

라운드 구조 (약 85분):
1. **Phase A** — 팀장 분배 (10분)
   - `team-lead` 에이전트가 gap 식별 및 task 작성
2. **Phase B** — 데이터 작업 병렬 (20분)
   - `policy-data-collector` + `data-refinement-analyst` (sonnet)
3. **Phase C** — 교수 비판 병렬 (30분)
   - `policy-science-professor` + `ir-political-professor` (opus)
4. **Phase D** — 팀장 교차검토 (15분)
5. **Phase E** — 팀장 보고 + state 업데이트 (10분)

산출물: `council_sessions/round_N/` 전체 + `LEDGER.md` 새 블록 + `LEAD_REPORT.md`

실행 후 Heedo에게 2~3 문장 요약 제시. 5개 품질 게이트 상태 표기.

**수렴 판정**: 5 gate 모두 pass + 2회 연속 gap 없음 → 자동으로 `/cina-council finalize` 권고.

자세한 규약: [docs/10_council_protocol.md](../../docs/10_council_protocol.md)
