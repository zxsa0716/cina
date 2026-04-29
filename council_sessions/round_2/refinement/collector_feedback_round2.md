# Data Refinement → Data Collector Feedback (Round 2)

작성: Data Refinement Analyst | 2026-04-25 | CINA Round 2

---

## 1. 발견된 Gap

### Gap 1 (HIGH): Saudi Arabia GGA-IND 관련 문서 0건 (Round 1 지속 미해결)

Saudi Arabia의 GGA-IND 직접 입장 표명 문서가 여전히 없음. Round 2에서 SAU NDC 1건 추가됐지만 적응 지표 관련 발언 없음. Arab Group의 ENB 발언 4건 중 GGA-IND 관련 인용 0건. 수집 범위를 UNFCCC Party Submission Portal의 SAU 개별 submission으로 확장 요망.

**수집 목표**: `https://unfccc.int/documents/submissions` 에서 `Saudi Arabia + GGA OR adaptation` 필터

---

### Gap 2 (HIGH): AOSIS 그룹의 GGA 협상 입장 직접 발언 1건

AOSIS 소도서국 NDC 5건(Fiji, Nauru, Palau, Samoa, Bahamas) 있으나, 이들의 **협상 발언** 기록(intervention record)이 없음. ENB에서 AOSIS 언급은 3건이지만 GGA-IND 관련 직접 인용 없음. AOSIS의 GGA salience (생존과 직결)를 정량화하려면 AOSIS formal submission 또는 ENB 협상 기록 필요.

**수집 목표**: AOSIS COP30 formal submission to CMA7 (sbsta/sbi session records)

---

### Gap 3 (HIGH): Realist baseline 데이터 미수집

Stage 2 GAT에 필요한 국가 power 변수 (GDP, CO2, military, alliance) 미수집. CINA 20개국 × 4변수 = 80 data points 필요.

**수집 목표**:
- World Bank API: GDP (current USD, 2020-2025)
- Global Carbon Project: Cumulative CO2 (1850-2024)
- SIPRI: Military expenditure 2024
- `data/raw/country_power/` 에 저장

---

### Gap 4 (MEDIUM): 한국(KOR) 외교부 자료 — COP30 적응 관련 1건

수집된 한국 외교부 3건 중 2건은 한국어로 rendering 불량 (CP949 인코딩 이슈). COP30 적응 관련 한국 공식 입장은 GGA-IND에서 1건 태그됐으나 내용 접근 불가.

**수집 목표**: 
- 외교부 영문 보도자료 (`www.mofa.go.kr/eng` 기후 카테고리)
- 환경부 COP30 결과 보고서 영문판
- Korean MOFA 영문 NDC 3.0 제출 문서

---

### Gap 5 (MEDIUM): LMDC 공식 submission 미수집

ENB에서 LMDC 언급 2건이나 LMDC의 GGA 관련 formal position paper가 없음. LMDC(중국, 인도, 사우디, 이란 등)는 "voluntary, non-prescriptive" 언어의 주요 지지자로 추정되나 직접 증거 부재.

**수집 목표**: `https://unfccc.int/submissions/lmdc` 또는 LMDC joint statement COP30

---

### Gap 6 (MEDIUM): 9(e) Infrastructure 지표 8개 — 목표 미충족

UAE-Belém 9e Infrastructure 지표 8개 추출됨 (목표: 최소 5개 이상 → 통과이나 타겟 대비 부족). 9a(41), 9b(46), 9c(54) 대비 현저히 적음. PDF 구조 문제 또는 지표 텍스트가 표 형식으로 되어 있을 가능성.

**수집 목표**: UAE_Belem_9e_Infrastructure.pdf 페이지 별 텍스트 확인 (PyMuPDF page-by-page 재시도)

---

### Gap 7 (LOW): African Group 공식 입장 미수집

group_frequency에서 african 그룹 5건이나 African Group 공식 COP30 발언은 없음. 아프리카 국가 NDC 10건 있으나 그룹 position paper 부재.

---

## 2. 우선순위 요약

| 우선순위 | Gap | 이유 |
|--------|-----|-----|
| High | SAU GGA-IND 0건 | Stage 2 Arab Group 노드 공백 |
| High | AOSIS GGA formal position | AOSIS salience asymmetry 검증 핵심 |
| High | Realist baseline (GDP/CO2/military) | Stage 2 GNN 학습 불가 |
| Medium | KOR 영문 자료 | Track A 브리핑 직결 |
| Medium | LMDC formal submission | sovereignty 프레임 증거 강화 |
| Medium | 9e 지표 추가 추출 | UAE-Belém 완성도 |
| Low | African Group position | Stage 2 아프리카 노드 강화 |

---

## 3. 기술적 메모 (Collector 참고)

1. **한국어 HTML 인코딩**: `data/raw/korean_gov/` 파일들이 CP949로 저장되어 refinement 시 UTF-8 decode 실패. 수집 시 `requests.get(...).encoding = 'utf-8'` 강제 또는 BeautifulSoup에서 `html.parser` 대신 `lxml` 사용 권장.

2. **NDC PDF 암호화**: `ndc-522b0273dc4b`, `ndc-135da9f5bc3e`, `ndc-081d5ef69cdf` — 3건이 PyMuPDF 추출 실패 (빈 텍스트). 이 파일들은 스캔 PDF일 가능성. OCR 처리 또는 UNFCCC portal에서 텍스트 기반 버전 재수집 요망.

3. **Brazilian gov HTML**: `planalto_en_international_agenda_cop30.html` — 본문 200자 미만. React SPA 구조로 서버사이드 렌더링 없음. Playwright 또는 Selenium으로 재수집 필요.

---

## 4. Round 3 Collector task 자동 도출 요약

Round 3 collector가 우선적으로 수행해야 할 작업:

1. UNFCCC submission portal → SAU, AOSIS, LMDC party submissions (GGA/CMA7 관련)
2. World Bank/OECD API → CINA 20개국 GDP/CO2/military 시계열
3. KOR MOFA 영문 COP30 결과 보고서 재수집
4. 3건 encrypted NDC OCR 또는 텍스트버전 재수집
5. 9e Infrastructure PDF 구조 재검토 및 지표 재추출

예상 신규 문서: 20-30건 (realist baseline + party submissions)
