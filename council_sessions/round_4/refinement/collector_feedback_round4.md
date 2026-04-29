# Data Refinement → Data Collector Feedback (Round 4)

> 발신: data-refinement-analyst
> 수신: policy-data-collector
> 작성일: 2026-04-26
> 우선순위 지시: 팀장 Round 5 T01 반영 요청

---

## 발견된 Gap (Round 4 정제 과정)

### 1. ENB Castro 2025 실제 협력 matrix (최우선)
- **현황**: P0-3 F1 검증에서 pseudo-truth (그룹 멤버십) 사용. 실제 ENB co-sponsoring/joint statement 데이터 미수집.
- **필요 데이터**: Castro et al. 2025 (Nature Scientific Data) 협력 matrix 또는 IISD ENB COP30 요약에서 직접 추출 가능한 joint statement 목록
- **우선순위**: **HIGH** (F1 재검증에 직결)
- **소스**: https://www.nature.com/articles/s41597-025-06262-4 + enb.iisd.org/cop30

### 2. COP30 contact group 회의록 (Tallberg 비공식 협의 재구성)
- **현황**: L.25 advance ≡ L.25E final → formula control이 비공식 협의에서 완성. 그 과정 문서 미수집.
- **필요 데이터**: UNFCCC contact group informal notes, COP30 Presidency closing remarks, ENB COP30 Day 12 summary
- **우선순위**: **HIGH** (Tallberg 인과사슬 보강)
- **소스**: enb.iisd.org/cop30 + unfccc.int/cop30/sessions

### 3. Saudi Arabia L&D-OP 관련 제출서
- **현황**: Round 3 피드백에서도 지적됨. 여전히 0건.
- **필요 데이터**: Saudi Arabia UNFCCC submission on FRLD/L&D fund, SBI 2025 submissions
- **우선순위**: **HIGH**
- **소스**: unfccc.int/documents/629xxx (Saudi Arabia 2025)

### 4. 한국 GCF 기여 관련 외교부 공식 자료
- **현황**: ADAPT-FIN × 사회·경제 cell (0.38) LOW_CONFIDENCE. 한국의 GCF 기여 stance가 공식 문서로 미확인.
- **필요 데이터**: 외교부 GCF 이사회 참여 관련 보도자료, 기후재원 입장 문서
- **우선순위**: **MEDIUM**
- **소스**: mofa.go.kr + gcfund.org/about/governance/board-meeting

### 5. COP28/COP29 L.25 대응 advance/final 텍스트
- **현황**: Tallberg 시계열 분석을 위해 COP28 (UAE), COP29 (Azerbaijan) GGA 결정문 advance/final 쌍 필요
- **필요 데이터**: FCCC/PA/CMA/2023 + 2024 advance/final pairs
- **우선순위**: **MEDIUM**
- **소스**: unfccc.int/documents

### 6. AOSIS COP29 statement on GGA-IND
- **현황**: Round 3에서도 언급. GGA-IND 이슈에서 AOSIS의 입장 문서 미수집.
- **우선순위**: **MEDIUM**
- **소스**: aosis.org + unfccc COP29 AOSIS submissions

### 7. 한국 COP30 협상 입장 전문 (외교부)
- **현황**: seq_371781, seq_376685는 수집됨 (방어적 EIG 입장). COP30 실제 발언문 미수집.
- **필요 데이터**: 한국 COP30 국가대표단 발언문, EIG 공동성명
- **우선순위**: **LOW**
- **소스**: mofa.go.kr + unfccc.int/cop30

---

## 우선순위 요약

| 우선순위 | 항목 | 소요 라운드 |
|---|---|---|
| HIGH | ENB Castro 2025 협력 matrix | Round 5 |
| HIGH | COP30 contact group 회의록/ENB day summaries | Round 5 |
| HIGH | Saudi Arabia L&D-OP 제출서 | Round 5 |
| MEDIUM | 한국 GCF 기여 외교부 자료 | Round 5 |
| MEDIUM | COP28/29 advance/final 쌍 | Round 5-6 |
| MEDIUM | AOSIS COP29 GGA-IND 제출서 | Round 5-6 |
| LOW | 한국 COP30 발언문 | Round 6 |
