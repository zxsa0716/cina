---
task_id: T01-Round4
assigned_to: policy-data-collector
agent_model: sonnet
round: 4
priority: P0 (chair_letters + Korean MOE) + P0 (realist baseline) + P1 (NSA + AGN)
depends_on:
  - council_sessions/round_3/synthesis/cross_review.md (§2 CR3 directives, §6 Round 4 핵심 방향)
  - council_sessions/round_3/refinement/collector_feedback_round3.md (placeholder 4건 재수집)
  - council_sessions/round_3/ir_political/critique.md §6 P0-1 (chair letters), §6 P0-2 (realist B0)
  - council_sessions/round_3/policy_science/critique.md §5 (Plano Clima Vol II + APIB + KOR MOE PDF)
deadline: Round 4 종료 전 (Phase A: 24시간 내, Phase B: 48시간 내)
---

# T01 Round 4 — policy-data-collector 작업 지시

## 0. 목적

Round 3에서 미충족된 CR3.1 (chair_metadata Bayer-Urpelainen N>100 panel threshold) + CR3.5 (realist baseline 4 datasets) + 미시작된 placeholder 재수집 4건을 Round 4 P0로 처리. NSA + AGN 확장은 P1.

## 1. 산출물 (Deliverables)

### 1.1 P0 — IR critique §6 P0-1 직접 응답: COP21~27 historical chair letters 12+건

**목표**: chair_metadata 32 → 80+ records, COP coverage 3 → 10. Bayer-Urpelainen (2013, *ISQ* 57) panel 분석 minimum threshold 도달.

**우선순위 12 records (8 시점)**:

| COP | 의장 | 국가 | 그룹 | 우선 수집 (각 1-3건) |
|-----|------|------|------|---------------------|
| COP21 (2015 Paris) | Laurent Fabius | FRA | EU/Umbrella | opening + closing letter, JL Marrakech transition note |
| COP22 (2016 Marrakech) | Salaheddine Mezouar | MAR | Africa | presidency vision + agenda guidance |
| COP23 (2017 Bonn/Fiji) | Frank Bainimarama | FJI | AOSIS | Talanoa Dialogue letter + presidency closing |
| COP24 (2018 Katowice) | Michał Kurtyka | POL | EU (coal exporter — hedge case) | Katowice rulebook letter + Solidarity Declaration |
| COP25 (2019 Madrid) | Carolina Schmidt | CHL | AILAC | Time for Action presidency letter |
| COP26 (2021 Glasgow) | Alok Sharma | UK | EU/Umbrella | Glasgow presidency programme + Reflections letter |
| COP27 (2022 Sharm el Sheikh) | Sameh Shoukry | EGY | Africa (gas exporter — hedge case) | Sharm presidency note + Cover decision letter |

**소스 URL pattern**:
- UNFCCC archive: `https://unfccc.int/cop21`, `/cop22`, ... `/cop27` → "Presidency / Letters" subsection
- COP26 specific: `https://ukcop26.org/` archive (UK gov)
- Fallback: UN Climate Change Conference archive `https://unfccc.int/process-and-meetings/conferences`
- Tertiary fallback: ENB COP21~27 daily reports에 인용된 presidency texts

**스크립트**: `src/collect/curated_round4_chairs.py` (CuratedRound4ChairsCollector) 신규 작성. WebSearch 4-6회로 URL 확보 → Playwright headless fallback → manifest append.

**검증 기준**:
- chair_metadata.jsonl 80+ records
- COP_coverage_distinct ≥ 10 (COP21~30)
- 비-BASIC 비-산유국 의장 (FRA, FJI, UK, CHL) baseline ≥ 6 records (counterfactual 가능)
- 산유국 의장 (UAE, AZE, EGY, POL — coal) baseline ≥ 8 records

### 1.2 P0 — Korean MOE 적응대책 PDF 직접 fetch (Playwright)

**현재 상태**: `Korean_MOE_adapt_plan_index 1 HTML`만 수집됨. PDF 본문 미수집.

**목표 산출물**:
- 환경부 「제3차 국가 기후위기 적응 강화대책 (2026-2030)」 PDF 본문
- KEI 정책보고서 2024-04 「제3차 국가기후위기적응강화대책 수립 지원 및 평가체계 구축」 PDF
- KEI WP 2024-08 (제2차 적응대책 92개 세부과제 모니터링) PDF (가능 시)

**소스**:
- 환경부 공식: `https://www.me.go.kr` 보도자료 검색 "제3차 국가 기후위기 적응 강화대책"
- KEI: `https://www.kei.re.kr/main.es?mid=a30201000000` 정책보고서 검색
- 비상 fallback: WebSearch 한국어 + Playwright dynamic

**왜 P0**: T02 Round 4의 `korean_nap_gga_crosswalk.csv` (5×6 매트릭스) 산출에 한국 5대 영역 분류 표준이 필수 입력 (Policy critique §4).

### 1.3 P0 — Realist baseline B0 country_features_v2 4 datasets

**현재 상태**: OWID CO2 2건 (BASELINE entries) 수집됨. 나머지 3 datasets 미수집.

**목표 4 datasets**:

| Dataset | 형식 | URL | 검증 |
|---------|------|-----|------|
| **WB GDP per capita (current US$)** | API JSON or bulk CSV | `https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD?format=json&date=2010:2024` | CINA 20국 + AOSIS·LDC 결측 < 5% |
| **SIPRI Military Expenditure 2024** | PDF + Excel | `https://www.sipri.org/databases/milex` (Trends in World Military Expenditure 2024 fact sheet) | CINA 20국 + AOSIS·LDC 결측 < 10% |
| **COW Alliances v4.1** | CSV | `https://correlatesofwar.org/data-sets/formal-alliances/` (V4.1 country-year) | 1816-2012 (시계열 길이만 보장) |
| **OWID CO2 cumulative** | 이미 있음 — 검증만 | 기존 BASELINE entries 2건 country-year 매핑 검증 |

**스크립트**: `src/collect/realist_baseline.py` (RealistBaselineCollector) 신규. API 호출 (WB) + Playwright PDF download (SIPRI) + HTTP CSV download (COW).

**검증 기준**:
- country_features_v2.csv 산출 (T02 Round 4가 통합) 시 CINA 20국 + AOSIS·LDC 36+ 국가 ISO3 join 정확도 > 99%
- 결측 셀 < 10%
- 4 features (GDP_pc + MILEX_pct_GDP + alliance_count + CO2_cumulative_per_capita)

**왜 P0**: IR critique §9 D2 "F1 ≥ 90%이면 CINA novelty 위협 — 빠른 검증 후 Discussion 대응 전략 설계 필요". Round 4 즉시 검증 필수.

### 1.4 P0 — Placeholder 4건 재수집

`refinement/collector_feedback_round3.md` HIGH 4건. Playwright headless로 직접 fetch.

| doc_id | URL | 사이즈 expected |
|--------|-----|----------------|
| round3_curated-a5df10d8f2fc | https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202509160100---AOSIS%20Submission%20-%20Climate%20Champions%20-%20FINAL.pdf | > 50 KB |
| round3_curated-407c6606eb8e | https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202406031611---AOSIS%20Joint%20Opening%20Statement%20SB60%20-%20FINAL%20for%20Upload%20-%203%20Jun%2024.pdf | > 50 KB |
| round3_curated-0cf9b5f4d8bf | https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202404031108---AOSIS%20adaptation_Submission%20text%20plus%20data%20gaps.pdf | > 50 KB |
| round4_curated-e3e9c0a8d5ba | https://www4.unfccc.int/sites/SubmissionsStaging/Documents/202009012224---Final_AIPP_IWGIA_Submission_1_September_2020.pdf | > 50 KB |

manifest에서 기존 entry update (sha256 재계산).

### 1.5 P1 — NSA observer submission 확장 (옵션 A+C 하이브리드 조건)

**목표**: NSA 20 records / 4 entity → **40+ records / 8+ entity** (IR critique §5.3 옵션 A 가능 조건)

**우선순위 4 entity 추가**:

| Entity | 약자 | 우선 문서 |
|--------|------|----------|
| Coordinadora de las Organizaciones Indígenas de la Cuenca Amazónica | COICA | COP30 Belém statement, COP28 fossil fuel statement |
| Articulação dos Povos Indígenas do Brasil | APIB | COP30 Aldeia Global statement, COP30 indigenous demands |
| Climate Action Network International | CAN | COP30 Joint NGO Statement, COP29 Eco newsletter |
| Women & Gender Constituency | WGC | COP30 opening statement, gender just transition submission |

**부수 (시간 허용 시)**:
- Trade Union NGOs (TUNGO) COP30 statement
- BINGO (Business and Industry NGO) COP30 statement (반대편 균형 ablation)

**소스**:
- UNFCCC observer submissions portal: `https://unfccc.int/process/parties-non-party-stakeholders/non-party-stakeholders/admitted-non-governmental-organizations`
- WebSearch + 단체 공식 site (climatenetwork.org, womengenderclimate.org)

### 1.6 P1 — Plano Clima Vol II + AGN African Group submissions

**Plano Clima Vol II** (Policy critique §5):
- 「Plano Clima Volume II — Plano Nacional de Adaptação」 실행 계획 본문
- 소스: `https://www.gov.br/casacivil/pt-br/assuntos/noticias/2025/junho/governo-federal-lanca-plano-clima` 또는 MMA portal
- 왜 필요: 섹터별 instrument-mix 정량 분해 (Putnam Two-Level Games 국내 트랙 evidence 강화)

**AGN African Group submissions** (지시문 명시):
- UNFCCC docs ID 629526, 63346 follow
- AGN GGA submission COP29/COP30, AGN L&D submission, AGN finance submission

**Saudi Arabia / Arab Group L&D** (collector_feedback_round3 HIGH):
- COP29 SAU adaptation submission
- COP29 Arab Group L&D joint submission
- SAU NDC 3.0 (있다면)

## 2. 품질 기준 (Acceptance Criteria)

- [ ] manifest.jsonl 132 → **170+** (chair 12 + KOR MOE 3 + realist 4 + placeholder 4 + NSA 20 + Plano Vol II 1 + AGN 5 + SAU 3 = +52 minimum)
- [ ] sha256_coverage_pct = 100%, license_coverage_pct = 100% 유지
- [ ] coverage_summary.json 갱신 — countries 35% → **45%+**, sessions 31.2% → **45%+**, issues 83.3% 유지
- [ ] chair_metadata 80+ records, COP_coverage ≥ 10 (T02 Round 4 정제 확인 후 검증)
- [ ] country_features_v2.csv 입력 4 datasets 모두 raw 디렉토리에 존재
- [ ] placeholder 4건 모두 정상 PDF (> 50 KB)
- [ ] NSA 8+ entity (LCIPP, AIPP, IWGIA, IIPFCC, COICA, APIB, CAN, WGC)
- [ ] Korean MOE 적응대책 PDF 본문 + KEI 정책보고서 1+건

## 3. 제공된 컨텍스트 (Provided Context)

### 3.1 Round 3 산출물 (필수 참조)
- `data/manifest/manifest.jsonl` — 132 entries
- `data/manifest/coverage_summary.json` — 현재 coverage
- `data/processed/chair_metadata.jsonl` — 32 records (확장 baseline)
- `data/processed/non_state_actor_signals.jsonl` — 20 records (확장 baseline)
- `council_sessions/round_3/refinement/collector_feedback_round3.md` — placeholder 4건 + SAU/COP29 GGA/Plano Vol II priorities

### 3.2 Round 3 IR critique 권고 (§6)
- P0-1: chair_metadata N=32 → N≥80+, COP_coverage ≥ 10
- P0-2: Realist B0 4 datasets country_features_v2 검증
- P0-3: Secretariat informational note (FCCC/.../INF) 시리즈 N≥15
- P1-1: NSA observer submission N≥80 (Round 5 R-GAT 옵션 A 가능 조건)

### 3.3 Round 3 Policy critique 권고 (§5)
- P0: Plano Clima Vol II
- P0: APIB COP30 statement
- P1: 환경부 「제3차 국가 기후위기 적응 강화대책」 본문 PDF
- P1: OECD CRS Adaptation Finance 2023-2024 bulk CSV (Treasure 축 ground truth)

## 4. 보고 (Reporting)

### 4.1 형식
`council_sessions/round_4/data_collection/REPORT.md` 작성:
- Phase 별 (P0 chairs / P0 KOR MOE / P0 realist / P0 placeholder / P1 NSA / P1 AGN+SAU+Plano Vol II) 수집 결과
- 실패한 fetch URL 별도 명시 (Round 5 fallback 후보)
- WebSearch 횟수 + Playwright 호출 횟수

### 4.2 기간
- Phase A (P0 4건): 24시간 내
- Phase B (P1 3건): 48시간 내

### 4.3 종료 시 인계
- T02 Round 4에 인계: realist baseline 4 datasets raw 디렉토리, chair letters 12+건 raw 디렉토리, KOR MOE PDF, NSA 추가 8 entity raw 디렉토리
- coverage_summary.json 갱신 후 manifest.jsonl 무결성 검증

---

*— team-lead, 2026-04-26*
