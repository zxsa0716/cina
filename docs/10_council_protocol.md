# 10. Council Protocol — 5-에이전트 협의체 운영 규약

> CINA의 "AI 모델 설계 협의체" 운영 규약.
> 4개 작업 에이전트가 서로 피드백하며 방법론을 다듬고, 1명의 팀장 에이전트가 감독한다.
> 세션 간 지속성·라운드 구조·의사결정 규칙을 명시.

---

## 1. 구성원

| Role | Agent ID | Model | 주 책임 |
|------|----------|-------|---------|
| 팀장 | `team-lead` | opus | 감독, 교차검토, 품질 게이트, Heedo 보고 |
| 데이터 수집 | `policy-data-collector` | sonnet | UNFCCC·ENB·NDC 문서 수집 |
| 데이터 정제 | `data-refinement-analyst` | sonnet | raw → 구조화, 토픽 태깅, 품질 점검 |
| 정책학 교수 | `policy-science-professor` | opus | 정책 이론·실무 적용성 비판 |
| 외교·정치학 교수 | `ir-political-professor` | opus | IR 이론·권력 분석·역사 맥락 비판 |

## 2. 라운드 구조 (1 round ≈ 1 작업 세션)

### 2.1 Phase A — 분배 (팀장, 약 10분)
1. `council_sessions/state.json` 로드
2. 이전 라운드 산출물 요약 (팀장이 4개 에이전트 리포트 읽음)
3. 5가지 gap 체크 (data/theory/method/eval/narrative)
4. `council_sessions/round_N/tasks/*.md` 작성 (에이전트별)

### 2.2 Phase B — 병렬 수집·정제 (sonnet 에이전트, 약 20분)
- `policy-data-collector` → 새 문서 수집
- `data-refinement-analyst` → 신규 + 기존 문서 정제
- 가능하면 병렬 실행 (`Agent` 도구 multi-spawn)
- 산출물: `council_sessions/round_N/data_collection/`, `.../refinement/`

### 2.3 Phase C — 병렬 비판 (opus 교수, 약 30분)
- `policy-science-professor` → Phase B 산출물 + 전체 프레임워크 비판
- `ir-political-professor` → 동일 자료 독립 비판
- 두 교수는 서로의 이전 라운드 critique를 읽지만 **동시 작성**
- 산출물: `.../policy_science/critique.md`, `.../ir_political/critique.md`

### 2.4 Phase D — 상호 검토 (팀장, 약 15분)
- 팀장이 두 교수의 critique 병합
- 합의 지점 / 불일치 지점 식별
- 데이터 에이전트에게 feedback 전달 (`collector_feedback.md`, `refinement_feedback.md`)
- 5 품질 게이트 판정

### 2.5 Phase E — 보고 (팀장, 약 10분)
- `council_sessions/round_N/LEAD_REPORT.md` 작성
- `council_sessions/LEDGER.md` append
- `council_sessions/state.json` 업데이트 (round += 1)
- Heedo에게 요약 제시

**총 소요**: 약 85분 / round. 비용: sonnet $1-2 + opus $2-4 ≈ $3-6 / round.

---

## 3. 세션 간 지속성 (Session Persistence)

CINA pipeline 세션은 재시작되므로, 협의체 상태는 파일 기반 저장.

### 3.1 중심 파일 — `council_sessions/state.json`
```json
{
  "project": "CINA",
  "framework_version": "2.0",
  "current_round": 3,
  "rounds_completed": [
    {"round": 1, "date": "2026-04-25", "outcome": "baseline_established"},
    {"round": 2, "date": "2026-04-26", "outcome": "data_gaps_filled"}
  ],
  "active_tasks": {
    "policy-data-collector": "round_3/tasks/collector_task.md",
    "data-refinement-analyst": "round_3/tasks/refinement_task.md"
  },
  "quality_gates": {
    "G1_data_coverage": {"status": "pass", "value": 0.87},
    "G2_evidence_grounding": {"status": "pending"},
    "G3_theory_grounding": {"status": "partial"},
    "G4_dual_review": {"status": "pending"},
    "G5_heedo_alignment": {"status": "pass"}
  },
  "blocked_on": null,
  "next_action": "Collector → refine missing Saudi Arabia L&D docs",
  "updated_at": "2026-04-26T18:00:00Z"
}
```

### 3.2 연대기 — `council_sessions/LEDGER.md`
Append-only 기록. 각 라운드 한 블록:
```markdown
## Round N — 2026-MM-DD
- Lead summary: ...
- Key decisions: ...
- Gaps identified: ...
- Professor ratings: policy-sci 4.2/5, ir-political 3.8/5
- Next round focus: ...
```

### 3.3 라운드별 디렉토리 — `council_sessions/round_N/`
```
round_N/
├── tasks/
│   ├── collector_task.md
│   ├── refinement_task.md
│   ├── policy_prof_task.md
│   └── ir_prof_task.md
├── data_collection/
│   ├── REPORT.md
│   ├── manifest.jsonl
│   └── collector_feedback.md
├── refinement/
│   ├── REPORT.md
│   ├── collector_feedback.md
│   └── corpus_stats.json
├── policy_science/
│   ├── critique.md
│   └── vs_ir_dialogue.md
├── ir_political/
│   ├── critique.md
│   └── vs_policy_dialogue.md
├── synthesis/
│   └── cross_review.md
└── LEAD_REPORT.md
```

---

## 4. 의사결정 규칙

### 4.1 합의 (Consensus)
두 교수가 같은 권고를 내면 → 팀장 자동 승인 → 다음 라운드 task로 변환.

### 4.2 불일치 (Disagreement)
두 교수가 반대 권고:
1. 팀장이 각 관점의 논리를 분석
2. 3가지 결과 중 하나 선택:
   - **양립**: 두 관점 모두 CINA에 반영
   - **우선순위**: 이번 라운드 한 관점만 구현, 다음 라운드 다른 관점
   - **Heedo 에스컬레이션**: 결정 불가, Heedo 판단 필요
3. 선택 이유를 `synthesis/cross_review.md`에 기록

### 4.3 Quality Gate 실패
5개 게이트 중 하나라도 fail:
- G1 (데이터) fail → collector가 추가 수집
- G2 (evidence) fail → refinement가 evidence link 강화
- G3 (이론) fail → 해당 교수 에이전트가 추가 references
- G4 (dual review) fail → 해당 차원 재검토 라운드
- G5 (Heedo alignment) fail → 즉시 Heedo 에스컬레이션

### 4.4 종료 조건
- 5 게이트 모두 pass + 2회 연속 새 gap 없음 → 수렴 권고
- 최대 10 라운드 한도 (비용 제어)
- Heedo 명시적 종료

---

## 5. 에이전트 간 통신 프로토콜

### 5.1 Direct feedback 채널
| From → To | 채널 파일 |
|----------|----------|
| refinement → collector | `round_N/refinement/collector_feedback.md` |
| policy-prof → refinement | `round_N/policy_science/refinement_feedback.md` |
| ir-prof → refinement | `round_N/ir_political/refinement_feedback.md` |
| prof ↔ prof | `round_N/{policy_science|ir_political}/vs_*_dialogue.md` |

모든 채널은 팀장이 읽고 통합.

### 5.2 수직 통신 (팀장 ↔ 에이전트)
- Down: `round_N/tasks/{agent}_task.md`
- Up: `round_N/{agent}/REPORT.md` 또는 `critique.md`

### 5.3 프로토콜 위반
에이전트가 프로토콜 벗어난 행동 시:
1. 팀장이 `synthesis/protocol_violations.md`에 기록
2. 3회 누적 시 해당 에이전트 재교육 prompt (팀장이 task 재작성)

---

## 6. 컨텍스트 관리

### 6.1 에이전트별 context budget
- sonnet 에이전트: 최대 80K tokens input (비용 효율)
- opus 교수: 최대 150K tokens input (깊이 우선)
- 팀장: 최대 200K tokens (전체 상태 파악)

### 6.2 Context 우선순위 (에이전트 소환 시)
1. 자기 에이전트 정의 (`.claude/agents/{name}.md`) — 항상
2. 팀장 task (`round_N/tasks/{agent}_task.md`) — 항상
3. 직전 라운드 자기 산출물 — 항상
4. CINA_FRAMEWORK.md + 관련 docs/ — 선택적
5. 다른 에이전트 최근 산출물 — task에서 명시한 것만
6. `council_sessions/state.json` — 요약만

### 6.3 장기 기억 (Long-term memory)
- 프로젝트 Memory (`memory/*.md`) — 모든 에이전트 읽기
- 라운드 간 변화는 `LEDGER.md`에 요약 → 새 라운드 에이전트가 빠르게 이전 상태 파악

---

## 7. 모델 선택 근거

| 작업 | 모델 | 근거 |
|------|------|------|
| 데이터 수집 | sonnet | 반복 작업, 비용 효율 |
| 데이터 정제 | sonnet | 규칙 기반 + 간단 LLM 확인 |
| 정책학 비판 | opus | 이론적 깊이 필요 |
| IR 비판 | opus | 이론적 깊이 필요 |
| 팀장 | opus | 전체 조율, 통합 판단 |

## 8. 운영 Checklist (Heedo 용)

협의체 시작 전:
- [ ] `.claude/agents/` 5개 파일 존재
- [ ] `.mcp.json` memory/fetch 서버 설정
- [ ] `council_sessions/` 디렉토리 초기화
- [ ] `CINA_FRAMEWORK.md` 최신판
- [ ] ANTHROPIC_API_KEY 환경변수 (실제 LLM 호출용, 아닐 경우 skill-only mode)

협의체 진행 중:
- [ ] 매 라운드 시작 시 `state.json` 확인
- [ ] 팀장 `LEAD_REPORT.md` 읽기
- [ ] 불일치·블록 시 Heedo 개입
- [ ] 라운드 종료 시 `LEDGER.md` 업데이트 확인

협의체 종료 후:
- [ ] `deliverables/FINAL_SYNTHESIS.md` 생성
- [ ] 논문 draft `docs/paper/draft_v1.md` 생성
- [ ] 데이터셋 공개 준비 (Zenodo)

---

## 9. 시작 방법

### 옵션 A — Slash command
```
/cina-council start
```

### 옵션 B — CINA pipeline 세션에서 자연어
"팀장 에이전트 소환해서 라운드 1 시작"

### 옵션 C — Python 스크립트 (Anthropic API 직접)
```bash
python -m src.council.run --round 1
```

3가지 방법 모두 `council_sessions/state.json`을 기준점으로 사용.

---

## 10. 실패 시나리오 & 복구

| 실패 | 증상 | 복구 |
|------|------|------|
| 에이전트가 task를 무시 | 산출물 없음 | 팀장이 task 재작성, 구체성 강화 |
| 두 교수가 끊임없이 반대 | 수렴 안 됨 (3라운드) | Heedo 에스컬레이션, 메타 질문 |
| Collector가 같은 소스만 긁음 | 중복률 높음 | Refinement가 gap feedback 강화 |
| Context overflow | 에이전트 응답 깨짐 | `session-state` skill로 축약 요약 생성 |
| 비용 폭주 | $50 초과 | Heedo에게 alert, 중단 대기 |

---

## 11. 다음 문서
- [.claude/skills/council-orchestrator/SKILL.md](../.claude/skills/council-orchestrator/SKILL.md) — 실제 orchestration 지침
- [.claude/skills/session-state/SKILL.md](../.claude/skills/session-state/SKILL.md) — state.json 관리
- [council_sessions/README.md](../council_sessions/README.md) — 디렉토리 초기화 가이드
