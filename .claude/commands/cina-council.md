---
description: CINA 5-에이전트 협의체를 시작하거나 현재 상태를 점검
argument-hint: [start|status|resume|finalize]
---

CINA 협의체(Council) 세션을 관리합니다.

**서브 명령**:
- `start` — 협의체 초기화 (첫 실행 시). `session-state` skill의 init 호출.
- `status` — 현재 state.json, LEDGER.md, 활성 task 요약 출력.
- `resume` — 마지막 라운드 이어서. `state.json` 읽어 `current_round + 1` 로 다음 라운드 트리거.
- `finalize` — 수렴 판정 후 `deliverables/FINAL_SYNTHESIS.md` + 논문 draft 생성.

$ARGUMENTS 가 없으면 `status`.

진행 순서 (start 예시):
1. `session-state` skill의 `init` 호출 → `council_sessions/` 구조 생성
2. `docs/10_council_protocol.md` 읽고 운영 규약 확인
3. 팀장 에이전트 소환하여 "Round 1" task 분배 준비
4. Heedo에게 다음 단계 확인 요청 (`/cina-council-round 1` 실행 여부)

자세한 규약: [docs/10_council_protocol.md](../../docs/10_council_protocol.md)
