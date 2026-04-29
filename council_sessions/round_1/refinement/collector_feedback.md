# Data Refinement → Data Collector Feedback
# Round 1 → Round 2

작성: Data Refinement Analyst | 2026-04-25

---

## 발견된 Gap (수집 미비)

### Gap 1 — 각국 공식 UNFCCC 입장문 전무 [우선순위: Critical]

현재 corpus에 각국이 UNFCCC에 공식 제출한 SBI/SBSTA/CMA 문서가 없다. IPCC 과학 문서와 COP30 결과 선언은 있으나, 협상 과정에서 각국이 표명한 입장(position papers, opening statements, draft texts)이 없어 Stage 1 LLM 스탠스 추출을 수행할 수 없다.

**요청**: 아래 우선 수집 목록 참조. UNFCCC 제출 문서 포털(https://unfccc.int/documents)에서 COP30 및 SBI62/SBSTA62 관련 문서 수집.

**우선 수집 목록**:
| 국가/그룹 | 이슈 | 세션 | 문서 유형 |
|-----------|------|------|-----------|
| Brazil (BRA) | GGA-IND, ADAPT-FIN | COP30, SBI62 | Submission, Opening Statement |
| EU | GGA-IND, ADAPT-FIN, L&D-OP | COP30, SBI62 | Submission |
| AOSIS | GGA-IND, L&D-OP | COP30 | Group Statement |
| LDC Group | NAPs, ADAPT-FIN | SBI62 | Statement |
| LMDC | GGA-IND (opposition signals) | COP30 | Statement |
| African Group | GGA-IND, ADAPT-FIN | COP30 | Submission |
| India (IND) | GGA-IND | COP30, SBI62 | Statement |
| China (CHN) | GGA-IND, ADAPT-FIN | COP30 | Submission |
| AILAC | GGA-IND, L&D-OP | COP30 | Statement |
| USA | 모든 이슈 (부재 확인) | COP30 | — |

---

### Gap 2 — COP29 (Baku) 협상 문서 없음 [우선순위: High]

COP29→COP30 입장 변화 시계열 분석이 CINA의 핵심 검증 과제이나, Baku COP29(2024년 11월) 적응 협상 문서가 없다. GGA 지표 협상의 전사(前史)를 파악할 수 없다.

**요청**: COP29 GGA-IND 관련 SBI61/SBSTA61 문서 최소 10건 수집.

---

### Gap 3 — IISD ENB 일일 협상 요약 없음 [우선순위: High]

Castro et al. 2025 논문(방법론 설명)은 있으나, 실제 ENB 일일 요약(COP30 day-by-day) 문서가 없다. 협상 과정의 실시간 상호작용(agreement/opposition)을 파악할 수 없다.

**요청**: IISD ENB(https://enb.iisd.org/climate) COP30 일일 요약 HTML 수집. 특히 적응(adaptation) 세션 관련 호.

---

### Gap 4 — Saudi Arabia, LMDC 직접 발언 없음 [우선순위: Medium]

현재 corpus에서 SAU(사우디아라비아)는 2건 문서에서만 언급되며, 직접 발언 없음. LMDC 그룹의 저항 시그널 파악 불가.

**요청**: SAU, 이란, 알제리의 COP30 GGA 관련 발언 또는 제출문 수집.

---

### Gap 5 — NDC 적응 섹션 없음 [우선순위: Medium]

각국 NDC(Nationally Determined Contribution) 적응 섹션이 없다. 국가별 공식 적응 목표와 협상 입장을 연결하는 기준선 데이터가 부재.

**요청**: BRA, EU, CHN, IND, AOSIS 대표국 최신 NDC 적응 섹션 PDF 수집.

---

## 다음 라운드 수집 우선순위 요약

| 우선순위 | 갭 | 예상 문서 수 |
|---------|-----|------------|
| Critical | 각국 COP30 공식 제출문 (상위 10개국/그룹) | 20-30건 |
| High | COP29 GGA 관련 SBI61/SBSTA61 문서 | 10-15건 |
| High | IISD ENB COP30 일일 요약 | 15-20건 |
| Medium | LMDC/SAU COP30 발언 | 5-10건 |
| Medium | NDC 적응 섹션 (5개국) | 5건 |

**Round 2 수집 목표**: 총 50-80건 → Stage 1 LLM 추출 가동 조건 충족.
