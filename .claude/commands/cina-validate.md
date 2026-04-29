---
description: 기존 브리핑 문서의 모든 주장을 evidence/structural fact 근거로 검증
argument-hint: [briefing-file-path]
---

`evidence-validator` skill로 브리핑의 각 문장이 (텍스트 인용, 구조적 근거)를 가지는지 검증합니다.

진행 순서:
1. $ARGUMENTS 의 파일 로딩 (기본: `deliverables/ministerial_briefing.md`)
2. 문장별 split → 7가지 rule 적용
3. Unverified / Warning 분류
4. `deliverables/verification_report.md` 생성
5. 최대 3회 재생성 후에도 통과 못한 claim은 자동 제거 + 경고

출력:
- `verified_count / total` 비율
- 할루시네이션 카테고리별 건수
- 수정 권고 리스트
