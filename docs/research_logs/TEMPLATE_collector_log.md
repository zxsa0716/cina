---
template_for: policy-data-collector
log_type: collection_session
round: 0
date: YYYY-MM-DD
---

# Collector Session Log — Round {N}

## 1. Mandate

(team-lead가 발급한 task 인용. tasks/round_{N}/T###_collection.md 경로)

## 2. Sources Targeted

| Source | URL | Priority | Result |
|--------|-----|----------|--------|
| ... | ... | P0/P1/P2 | OK / partial / blocked |

## 3. 발견 (Discoveries)

### 3.1 데이터 가용성
- ...

### 3.2 구조적 단서 (Structural cues)
- ENB Vol 12 일련번호 패턴: enb12888e ~ enb12{LAST}e
- UNFCCC topic ID 매핑 갱신: ...

### 3.3 차단·실패
- 사이트 403: ENB → User-Agent 헤더 필요
- ...

## 4. 수집 통계

- 다운로드 파일 수: N
- 총 용량: M MB
- 평균 다운로드 시간: T sec/file
- 중복 (sha256 hit): K

## 5. Manifest 변경

- 추가된 doc_id 수: N (`data/manifest/manifest.jsonl`)
- coverage % 변화: countries +X%, issues +Y%, sessions +Z%

## 6. 품질 점검 (5 게이트)

| 게이트 | 통과? | 메모 |
|--------|------|------|
| Q1 Coverage | ✓/✗ | ... |
| Q2 Integrity | ✓/✗ | ... |
| Q3 Metadata | ✓/✗ | ... |
| Q4 License | ✓/✗ | ... |
| Q5 Deduplication | ✓/✗ | ... |

## 7. 다음 라운드 권고

- (구체적, actionable)

## 8. team-lead에게 escalation

- (있으면 명시, 없으면 "없음")

## Appendix A. Environmental snapshot
- Python: 3.X
- requirements hash: ...
- Network: home/lab WiFi
- Run timestamp: ISO

## Appendix B. 원본 명령
```bash
python -m src.collect.orchestrate --sources ... --topic ... --max ...
```
