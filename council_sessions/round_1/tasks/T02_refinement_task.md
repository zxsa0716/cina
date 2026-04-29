---
assigned_to: data-refinement-analyst
round: 1
issued_by: team-lead
issued_at: 2026-04-25
priority: P0
deadline: round_1 종료 전
depends_on: [T01_collector_task.md]
---

# Task T02 — Round 1 Refinement (raw → CINA Document Schema)

## 목적
Round 1 collector가 수집한 raw 파일들을 CINA Document Schema (`docs/03_data_architecture.md §3`)에 맞게 정제하고, 토픽·국가·세션 자동 태깅을 수행한다. 두 교수가 즉시 비판할 수 있는 입력 패키지를 만든다.

## 구체 산출물

- [ ] `data/processed/documents.jsonl` — 모든 raw 파일의 정규화 레코드
  - 스키마: `docs/03_data_architecture.md §3` 준수
  - 모든 레코드에 `paragraphs[]`, `topic_tags[]`, `country_authors[]`, `sha256`
- [ ] `data/processed/refinement_stats.json` — 정제 통계
- [ ] `council_sessions/round_1/refinement/REPORT.md` — 1-2 pages 결과 보고
- [ ] `council_sessions/round_1/refinement/professor_input/policy_sci_pack.md`
- [ ] `council_sessions/round_1/refinement/professor_input/ir_pack.md`
- [ ] `council_sessions/round_1/refinement/collector_feedback.md` — 다음 라운드 collector에게

## 처리 단계

### 단계 1. PDF/HTML → 텍스트
- PyMuPDF (PDF) / BeautifulSoup (HTML)
- 단락 분할 (paragraph_id 부여)
- 추출 실패 케이스 별도 로그

### 단계 2. 토픽 자동 태깅
- `src/data/identifiers.py` 의 `ISSUE_KEYWORDS` 1차 필터
- 키워드 매치 시 `topic_tags_initial` 에 issue code 추가 (GGA-IND, ADAPT-FIN 등)
- 매치 0건 또는 ≥ 3건 인 경우 LLM (claude-haiku) 2차 확인
- 모든 LLM 호출 비용은 `data/llm_logs/` 에 기록

### 단계 3. 국가/그룹 인식
- 1차: 정규식 + `CINA_COUNTRIES` 사전 매칭
- 2차: 약어·별칭 (e.g., "USA"→"USA", "EU-27"→"EU") 정규화
- 그룹 라벨 (G77, AOSIS, LDC) 별도 식별 → `groups_referenced[]`

### 단계 4. 세션 매핑
- 문서 내 "COP X", "SBI XX" 추출 → `session` 필드
- 문서 발행일이 있으면 `date_context` 채움

### 단계 5. 품질 게이트
- 텍스트 길이 ≥ 200 chars (그 미만은 별도 quarantine)
- topic_tags ≥ 1
- country_authors_initial 또는 groups_referenced ≥ 1

## 두 교수 입력 패키지 (전달용)

각 패키지에 다음 포함:

### `policy_sci_pack.md` (정책학 교수에게)
- Round 1 정제 결과 1단락 요약
- 정책학 관점에서 흥미로운 인용 5-10개 (정책 수단, 다층 거버넌스 시그널)
- 명시적 질문:
  - "GGA 지표 합의의 정책 이행 단계에서 다층 거버넌스 함의는?"
  - "MoI(Means of Implementation) 조항이 결과적으로 binding force를 약화시킨 정책수단 이론적 함의?"
  - 외 2-3개

### `ir_pack.md` (외교학 교수에게)
- Round 1 정제 결과 1단락 요약
- IR 관점 흥미로운 인용 5-10개 (연합 형성, 권력 역학, 패권 서사)
- 명시적 질문:
  - "브라질 의장국이 BASIC과 G77 사이에서 어떤 lobby balancing을 했는가?"
  - "AOSIS의 도덕적 권위 vs LMDC의 거부권 행사 구조적 비교?"
  - 외 2-3개

## 품질 기준

- [ ] documents.jsonl 의 ≥ 95% 가 schema 검증 통과
- [ ] 토픽 태그 분포 stat (각 이슈에 ≥ 5건)
- [ ] LLM 비용 ≤ $1
- [ ] 두 교수 입력 패키지 각 1-2 pages

## 제공된 컨텍스트
- [docs/03_data_architecture.md](../../../docs/03_data_architecture.md) §3 (Document Schema)
- [docs/13_reference_tables.md](../../../docs/13_reference_tables.md) §2 (이슈 키워드)
- 코드: `src/data/identifiers.py`, `src/refine/` (없으면 생성)
- 입력: `data/raw/` + `data/manifest/manifest.jsonl`
