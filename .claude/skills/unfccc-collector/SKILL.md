---
name: unfccc-collector
description: UNFCCC 공식 문서, NDC, IISD ENB 요약을 수집·정규화하는 데이터 수집 skill. Rate-limiting·재시도·체크포인트 지원. Stage 0 담당.
---

# UNFCCC Collector Skill

## 언제 이 skill을 호출하는가

- "데이터 수집해줘"
- "UNFCCC 문서 가져와"
- `cina-orchestrator`가 Phase A에서 자동 위임

## 입력·출력

### Input
- `source`: {unfccc, ndc, enb, castro2025, all}
- `cop`: COP 세션 번호 (예: 30)
- `sector`: adaptation / mitigation / all
- `countries`: list of ISO3 codes 또는 group labels
- `date_range`: [start, end] (ISO 8601)

### Output
- `data/raw/{source}/{cop}/` 하위 원시 파일
- `data/processed/documents.jsonl` — [docs/03 §3] Document Schema
- `.cina_collect_state.json` — 재개용 체크포인트

## 소스별 수집 절차

### UNFCCC Submission Portal
- Base URL: `https://unfccc.int/documents`
- Query API (있으면) 또는 HTML parsing
- PDF 다운로드 + PyMuPDF로 text 추출
- Rate limit: 1 req/sec, exponential backoff on 429

### NDC Registry
- Base URL: `https://unfccc.int/NDCREG`
- 국가별 최신 NDC + 업데이트 이력
- 특히 적응 섹션 파싱

### IISD ENB
- Base URL: `https://enb.iisd.org/`
- 각 COP 세션의 daily bulletin + summary report
- robots.txt 준수
- CC BY-NC-SA 라이선스 명시

### Castro et al. 2025 Dataset
- Source: Nature Scientific Data supplement
- CSV 다운로드 후 local cache
- 별도 API 없음, 1회 수집

### NegotiateCOP API (선택)
- 공개 API가 있으면 활용
- 시맨틱 검색 supplement 역할 (primary source 아님)

## 재개 가능한 수집

체크포인트 파일 `.cina_collect_state.json`:
```json
{
  "started_at": "2026-04-24T14:00Z",
  "completed_docs": ["UNFCCC-SBI-2025-L3", ...],
  "pending_urls": [...],
  "failed_urls": [
    {"url": "...", "error": "timeout", "attempts": 2}
  ]
}
```

중단 후 재실행 시 자동 resume.

## 문서 정규화 (Document Schema)

수집된 각 문서를 [docs/03 §3] 스키마로 변환:
```json
{
  "doc_id": "UNFCCC-SBI-2025-L3",
  "source": "unfccc_submission",
  "cop_session": "COP30",
  "subsidiary_body": "SBI",
  "document_type": "draft_conclusions",
  "date": "2025-06-18",
  "authors": ["Brazil"],
  "topics": ["adaptation", "GGA"],
  ...
}
```

## 토픽 자동 분류

1차 필터: 키워드 기반 regex
- adaptation: `(adaptation|adaptive|GGA|Global Goal on Adaptation)`
- finance: `(finance|financing|NCQG|\$[0-9])`
- loss_damage: `(loss and damage|L&D|non-economic)`
- naps: `(National Adaptation Plan|NAP)`
- just_transition: `(just transition|JTWP)`

2차 확인: LLM (claude-haiku, 비용 효율적)
```
"Which of these issues does this document primarily address?
 Options: {adaptation, GGA-indicators, adaptation-finance, loss-damage, NAPs, just-transition}
 Return JSON: {primary: <one>, secondary: <list>}"
```

## 윤리·라이선스

- UNFCCC: 공개 UN 문서, 재이용 가능. 인용 시 공식 문서 번호.
- ENB: CC BY-NC-SA. 비영리 연구 목적 준수.
- NDC: 국가 주권 문서. 인용 가능.
- Castro 2025: 저자 허가 없이 재배포 X, 인용만.

모든 수집된 raw 파일에 라이선스 메타데이터 첨부.

## 품질 자동 점검

- 문서 수: 기대 범위 내인가 (보통 20국 × 6이슈 = 최소 50건)
- 중복 제거: sha256 기반
- 언어 감지: 영어 이외 문서 count (한국어 NDC 등)
- 빈 문서 감지: text length < 100 chars → 경고

## 의존성

Python:
- `requests`, `beautifulsoup4`, `PyMuPDF`
- `ratelimit`, `tenacity` (backoff)
- `langdetect`

MCP:
- `fetch` (HTTP 요청)
- `filesystem` (로컬 저장)

## 예상 소요

- 20국 × 6이슈 범위: 약 80~120 문서
- 수집 시간: 30분~1시간 (rate limit)
- 저장 용량: ~500 MB (PDF 포함)
