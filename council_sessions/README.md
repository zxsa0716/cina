# council_sessions/ — CINA 협의체 작업 공간

CINA 5-에이전트 협의체의 모든 라운드 산출물, 상태, 연대기가 이곳에 기록된다.

## 파일·디렉토리

- `state.json` — 현재 라운드, 품질 게이트, 진행 상태 (세션 간 지속성)
- `LEDGER.md` — append-only 라운드별 요약 연대기
- `README.md` — 이 문서
- `round_{N}/` — 각 라운드 산출물
  - `tasks/` — 팀장이 작성한 에이전트별 task
  - `data_collection/` — policy-data-collector 산출물
  - `refinement/` — data-refinement-analyst 산출물
  - `policy_science/` — policy-science-professor 산출물
  - `ir_political/` — ir-political-professor 산출물
  - `synthesis/` — 팀장 교차 검토
  - `LEAD_REPORT.md` — 팀장 라운드 보고

## 사용 흐름

### 첫 실행
```
/cina-council start
```
또는 자연어 "CINA 협의체 초기화"

### 라운드 실행
```
/cina-council-round next
```
약 85분 / $3-6.

### 상태 점검
```
/cina-council status
```

### 수렴 시
```
/cina-council finalize
```
→ `deliverables/FINAL_SYNTHESIS.md` + `docs/paper/draft_v1.md` 생성.

## 규약 문서

전체 운영 규약은 [`docs/10_council_protocol.md`](../docs/10_council_protocol.md) 참조.

## 재현성

모든 에이전트 호출은 `state.json.rounds_completed[*].llm_calls` 에 기록.
각 라운드 `LEAD_REPORT.md` 에 LLM 비용·소요 시간 표기.

## 주의

- `state.json`은 `session-state` skill 경유로만 수정 (lock 기반 atomic write).
- `LEDGER.md`는 append-only. 과거 entries 수정 금지.
- 실험적 라운드는 `round_{N}_draft/` 로 분리 후 테스트, 성공 시 공식 round로 승격.
