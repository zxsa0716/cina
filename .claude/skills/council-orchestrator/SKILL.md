---
name: council-orchestrator
description: 5-에이전트 CINA 협의체의 1 라운드를 오케스트레이션. Phase A(분배) → B(수집/정제 병렬) → C(두 교수 비판 병렬) → D(상호검토) → E(보고)를 순차 실행. 세션 간 재개 지원. Heedo가 "라운드 N 시작" 또는 /cina-council-round 호출 시 자동 트리거.
---

# Council Orchestrator Skill

## 언제 호출되는가

- "협의체 라운드 N 돌려"
- "팀장 소환" / "에이전트 모아서 회의"
- `/cina-council-round` slash command
- `/cina-council start`

## 전체 흐름

### Pre-flight
1. `council_sessions/state.json` 존재 확인. 없으면 `session-state` skill로 초기화.
2. 현재 라운드 번호 결정: `state.json.current_round + 1`
3. `council_sessions/round_{N}/` 디렉토리 생성
4. `.claude/agents/` 5개 파일 존재 확인

### Phase A — 팀장 분배 (약 10분)
**Agent 호출**: `team-lead` (opus)

Prompt context:
- `CINA_FRAMEWORK.md`, `docs/10_council_protocol.md`
- `council_sessions/state.json`
- 이전 라운드 LEAD_REPORT.md 및 에이전트 산출물 (있으면)
- Heedo의 이번 라운드 특별 지시 (있으면)

Task to team-lead:
```
You are starting Round {N}. Read state.json and previous round outputs.
Identify 5 gaps (data/theory/method/eval/narrative) and assign tasks to:
  - policy-data-collector
  - data-refinement-analyst
  - policy-science-professor
  - ir-political-professor

Write task files under council_sessions/round_{N}/tasks/*.md using the template.
Return a list of 4 task paths.
```

### Phase B — 데이터 에이전트 병렬 실행 (약 20분)
**Parallel Agent 호출**:
- `policy-data-collector` (sonnet) — Task: `tasks/collector_task.md`
- `data-refinement-analyst` (sonnet) — Task: `tasks/refinement_task.md`

두 에이전트는 서로 독립 실행 (병렬). 둘 다 완료될 때까지 대기.

산출물 점검:
- `round_{N}/data_collection/REPORT.md` 존재
- `round_{N}/refinement/REPORT.md` 존재
- 둘 중 하나 실패 시 팀장에게 블록 에스컬레이션

### Phase C — 교수 에이전트 병렬 실행 (약 30분)
**Parallel Agent 호출**:
- `policy-science-professor` (opus) — Task: `tasks/policy_prof_task.md`
- `ir-political-professor` (opus) — Task: `tasks/ir_prof_task.md`

두 교수는 Phase B 산출물과 CINA 전체 문서를 읽고 독립 비판. 둘이 서로의 critique 초안을 보지 않음 (편향 방지).

산출물:
- `round_{N}/policy_science/critique.md`
- `round_{N}/ir_political/critique.md`
- 두 교수 모두 1~5 평점 Rubric 작성

### Phase D — 팀장 교차 검토 (약 15분)
**Agent 호출**: `team-lead` (opus)

Task:
```
Phase B, C outputs are in council_sessions/round_{N}/.
Your tasks:
1. Read both professors' critiques. Identify agreements and productive disagreements.
2. Write round_{N}/synthesis/cross_review.md with consensus / disagreement / decisions.
3. Derive feedback for data agents (if critiques imply data gaps):
   → round_{N}/synthesis/collector_feedback.md (if applicable)
   → round_{N}/synthesis/refinement_feedback.md (if applicable)
4. Evaluate 5 quality gates (G1-G5). Write results to round_{N}/synthesis/quality_gates.json.
5. Update council_sessions/state.json (current_round=N, quality_gates=...).
```

### Phase E — 보고 (약 10분)
**Agent 호출**: `team-lead` (opus)

Task:
```
Write round_{N}/LEAD_REPORT.md following the template in docs/10 §2.5.
Append a block to council_sessions/LEDGER.md.
Suggest next round focus or convergence.
```

### Post-round
- Heedo에게 LEAD_REPORT.md 핵심 요약 제시 (2-3 문장)
- 종료 조건 체크:
  - 5 gate 모두 pass?
  - 2회 연속 새 gap 없음?
  - Round ≥ 10?
- 종료 조건 충족 시 "수렴 권고" 메시지 + `deliverables/FINAL_SYNTHESIS.md` 생성 제안

## 에이전트 소환 실제 호출 방법

이 skill이 실행될 때, 주 세션은 다음과 같이 각 에이전트를 Agent tool로 호출한다:

```
Agent(
  description="Team lead kicks off round N",
  subagent_type="team-lead",
  prompt="""
  You are orchestrating Round {N}. Current state.json attached below.
  [contents of state.json]
  Previous LEAD_REPORT:
  [contents if exists]
  Heedo's latest guidance:
  [any new user message relevant]
  
  Produce:
  1. Task files at council_sessions/round_{N}/tasks/*.md
  2. Round kickoff summary (≤150 words) as your final message
  """
)
```

병렬 실행 시 단일 메시지에 여러 Agent tool call 포함 (공식 Claude Code 지침).

## State 파일 조작

라운드 중 state 갱신:
```
state.json.current_round = N (Phase E 후)
state.json.rounds_completed.append({round: N, date, outcome})
state.json.quality_gates 업데이트
state.json.updated_at = now()
```

모든 state 수정은 `session-state` skill을 경유하여 atomic write (tmp file → rename).

## 에러 처리

- Agent 호출 실패: 3회 retry (exponential backoff), 실패 시 해당 Phase abort, 팀장에게 리포트
- Context overflow: 팀장이 state.json에 `blocked_on: "context_overflow_{phase}"` 기록, `session-state` skill로 축약 생성
- 비용 임계치 초과 ($10/round): Heedo alert, 다음 Phase 대기

## 의존성

- `session-state` skill — state.json 관리
- `cina-orchestrator` skill — Stage 1/2/3 파이프라인 (협의체 결과 반영 후 실행)
- 5개 에이전트 정의 (`.claude/agents/`)
- `.mcp.json` — filesystem, fetch, memory 서버

## 성공 지표

- 각 라운드 종료 시 5개 게이트 중 ≥ 3개 pass
- 라운드 간 genuine progress (단순 재진술 금지)
- Heedo가 LEAD_REPORT를 읽고 "이건 내 의도대로 가고 있다" 확신
