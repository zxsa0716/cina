---
assigned_to: policy-data-collector
round: 3
priority: P0
depends_on:
  - council_sessions/round_2/synthesis/cross_review.md
  - council_sessions/round_2/synthesis/quality_gates.json
  - council_sessions/round_2/policy_science/critique.md (CR3.5, CR3.7)
  - council_sessions/round_2/ir_political/critique.md (CR3.1, CR3.6)
inputs:
  - data/manifest/manifest.jsonl (102 entries — Round 2 cumulative)
  - src/collect/{curated_cop30,korean_gov,brazilian_gov,enb_curated,unfccc_submissions,ndc_registry,iisd_enb}.py
  - src/collect/dynamic_browser.py (Playwright, validated)
deadline: Round 3 P0 — 24h target / P1 — 48h target
---

# T01 — Collector Round 3

## 목적

두 교수가 Round 2 critique에서 합의한 **샘플 사이즈 부족(C-shared 1)** 과 **counterfactual 부재(D4)** 를 데이터 측면에서 해결한다. 동시에 Round 1에서 미해결된 한국 적응정책 이행 추적 데이터(KEI 모니터링 보고서)를 수집한다.

## 구체 산출물

### P0-A. Historical presidency letters / L-document (CR3.1) — 목표 +50 records

UNFCCC 공식 portal에서 COP21~COP29 의장국 procedural 자료 수집:

- [ ] **COP21 Paris** (Fabius, France/EU): presidency letters + closing speech + L-document `FCCC/CP/2015/L.9/Rev.1` 계열
- [ ] **COP22 Marrakech** (Mezouar, Morocco): SBI/SBSTA L-document
- [ ] **COP23 Bonn** (Bainimarama, Fiji/AOSIS): Talanoa Dialogue 시작 letters
- [ ] **COP24 Katowice** (Kurtyka, Poland/EU): Paris Rulebook 결정문 advance/final
- [ ] **COP25 Madrid** (Schmidt, Chile-Spain): "Time for Action" 의장 messaging
- [ ] **COP26 Glasgow** (Sharma, UK/Umbrella): Glasgow Climate Pact L-document advance/final 비교
- [ ] **COP27 Sharm el-Sheikh** (Shoukry, Egypt/G77+China): Loss & Damage Fund 결정문 procedural records
- [ ] **COP28 Dubai** (Al Jaber, UAE/LMDC-adjacent): UAE Consensus L-document advance/final + presidency letters
- [ ] **COP29 Baku** (Babayev, Azerbaijan): Baku to Belém Roadmap + NCQG decision text + Yalçın Rafiyev (Lead Negotiator) letters

수집 방법:
- UNFCCC documents portal: `https://unfccc.int/documents` Playwright dynamic scraping
- 검색 endpoint: `?session=COPNN&type=L-document` 및 `?session=COPNN&type=Presidency`
- 추가: UNFCCC NAP Central, SBI/SBSTA Co-Chair note (`Note by the Co-Chairs`)

품질 기준:
- [ ] 각 COP당 최소 5 records → 9 COP × 5 = **45 records** + Baku Roadmap 추가 → 누적 N≥67 (Round 2 17 + Round 3 50)
- [ ] License/sha256 100% 추적
- [ ] manifest entry에 `session_id` 정확 부착 (cop21~cop29)
- [ ] "Draft decision -/CMA." 패턴 자동 검출 가능한 PDF 텍스트 layer 보유

### P0-B. Realist baseline B0 — 4 datasets (CR3.6)

Round 4-5에서 baseline B0 (realist GAT) 평가용 country features:

- [ ] **GDP 2024 (current USD)**: World Bank API
  - URL: `https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2024&format=json`
  - 출력: `data/raw/baseline/wb_gdp_2024.json` + 정규화 CSV (ISO3 join key)
- [ ] **CO2 cumulative 1850-2024**: Our World in Data
  - URL: `https://github.com/owid/co2-data/raw/master/owid-co2-data.csv`
  - 필터: country level only, `cumulative_co2` 컬럼 추출
  - 출력: `data/raw/baseline/owid_co2_cumulative.csv`
- [ ] **Military expenditure 2024**: SIPRI Military Expenditure Database
  - URL: `https://www.sipri.org/databases/milex` (Excel download)
  - 출력: `data/raw/baseline/sipri_milex_2024.xlsx`
  - 정규화: `current_usd`, `share_of_gdp` 컬럼 ISO3로 변환
- [ ] **Alliance overlap**: COW Formal Alliances v4.1 또는 ATOP
  - URL: `https://correlatesofwar.org/data-sets/formal-alliances/`
  - 출력: `data/raw/baseline/cow_alliances_v4_1.csv`
  - 처리: pairwise alliance dyad matrix → CINA 20국 sub-matrix

품질 기준:
- [ ] ISO3 코드로 `src/data/identifiers.py`와 100% join 가능
- [ ] License 명시 (World Bank CC BY-4.0 / OWID CC BY / SIPRI 학술용 / COW academic)
- [ ] `country_features` 32-dim → **36-dim** 확장 (GDP_log + CO2_cum_log + milex_pct_gdp + alliance_count)
- [ ] manifest entry per dataset

### P0-C. Korean MOE 적응대책 + KEI 모니터링 보고서 (CR3.7)

Round 2 인코딩 실패한 한국 정부 자료 재수집:

- [ ] **제3차 국가기후위기적응강화대책 (2026-2030)** PDF
  - 환경부 보도자료: `https://www.me.go.kr/home/web/board/read.do?boardMasterId=1&boardId=1592836`
  - Playwright headless로 PDF download (Round 2 timeout 발생 → User-Agent 변경 + 30s timeout 재시도)
  - 출력: `data/raw/korean_gov/me_3rd_adaptation_plan_2026.pdf`
- [ ] **KEI Working Paper 2024-08** 「제3차 국가기후위기적응강화대책 중간 모니터링 1차 결과」
  - 저자: 명수정·이정석
  - URL: `https://www.kei.re.kr/board.es?mid=a10101000000&bid=0049&list_no=...` (검색 후 PDF 다운로드)
  - 출력: `data/raw/korean_gov/kei_2024_08_adaptation_monitoring.pdf`
- [ ] **국가법령정보센터 API** — 기후위기대응법, 탄소중립기본법 메타데이터
  - URL: `https://www.law.go.kr/LSO/openApi.do` (API key 필요 시 Heedo 학교 계정)
  - 출력: `data/raw/korean_gov/law_metadata.json`

품질 기준:
- [ ] PDF text layer 추출 가능 (한글 OCR 필요 시 `pymupdf` 한국어 OCR 옵션)
- [ ] KEI 보고서는 정책학 §5.2 cross-walk 매트릭스의 핵심 입력
- [ ] License: KEI CC BY-NC, 환경부 KOGL Type-1, 법제처 KOGL Type-1

### P1-A. JT-ADAPT 비국가 행위자 시범 5-10건 (CR3.5)

IISD ENB COP30 daily summaries 16일치에서 비국가 행위자 입장문 추출:

- [ ] **COICA** (Coordinator of Indigenous Organizations of the Amazon Basin)
- [ ] **APIB** (Articulação dos Povos Indígenas do Brasil)
- [ ] **ITUC** (International Trade Union Confederation)
- [ ] **CAN** (Climate Action Network)
- [ ] **WWF / IUCN / IIED** (관찰자 NGO)

수집 방법:
- ENB COP30 daily summaries 16일치 (현재 4건만 수집 → 12건 추가) - HTML/PDF
- "side event", "non-state actor", "civil society", "indigenous peoples" 키워드 페이지
- 비국가 행위자 입장문 인용 paragraph 추출
- 출력: manifest entry `enb_curated-{daily_NN}` + `data/raw/iisd_enb/cop30_daily_NN.{html|pdf}`

품질 기준:
- [ ] ENB CC BY-NC-SA 라이센스 명시
- [ ] 최소 5 records (10 ideal)
- [ ] paragraph-level extraction 가능한 텍스트 layer

### P1-B. SAU/AOSIS/LMDC formal submissions (Round 2 refinement 권고 잔여)

UNFCCC SBI/SBSTA submissions portal에서 그룹별 formal submission:

- [ ] **AOSIS** submissions (COP30 NCQG / GGA / Loss & Damage 관련) — 최소 3건
- [ ] **LMDC** submissions (sovereignty / CBDR / NCQG) — 최소 3건
- [ ] **SAU** national submission (LMDC member, fossil fuel transition 관련) — 최소 2건

품질 기준:
- [ ] manifest entry에 `group_id` 정확 부착 (aosis/lmdc/saudi)
- [ ] License 명시 (UNFCCC CC BY-NC-ND)

### P2 (선택). Castro 2025 supplementary 재시도 (Round 1 D5 미해결)

- [ ] 제1저자 academic email contact (Heedo 학교 이메일 발송 — `zxsa0716@kookmin.ac.kr`)
- [ ] 받으면 utterance-level timeline → norm diffusion lag 측정 (Finnemore-Sikkink norm life cycle)
- [ ] HEEDO-7 결정 후 진행

## 품질 기준 (전체)

- [ ] 모든 신규 entry license + sha256 + retrieval timestamp 기록
- [ ] manifest 102 → **목표 165+** (Round 2 102 + P0 ~63 + P1 ~10-15)
- [ ] Coverage 0.62 → 0.91+ 도달
- [ ] 모든 PDF text layer 검증 (스캔 PDF는 OCR 라벨)
- [ ] CINA 20국 중 미수집 국가 (TUV·KIR) 보강 — AOSIS submission에서 보충 가능

## 제공된 컨텍스트

- Round 2 cross-review 핵심 결정 (council_sessions/round_2/synthesis/cross_review.md):
  - "CR3.1 (P0): COP21~COP29 11개 historical presidency letters → 목표 N≥67"
  - "CR3.6 (P0): Realist baseline B0 4 dataset"
  - "CR3.7 (P0): KEI Working Paper 2024-08"
- IR 교수 §6 P0(1)(2)(3) realist baseline + presidency letters 권고
- Policy 교수 §5 한국 KEI 모니터링 + §3 C2 비국가 행위자 시범
- 기존 인프라: Playwright + Chromium 검증 완료, dynamic_browser.py 작동

## 출력 위치

- Raw data: `data/raw/{source}/...`
- Manifest: `data/manifest/manifest.jsonl` (append-only)
- 수집 리포트: `council_sessions/round_3/data_collection/REPORT.md`
- 정제 인계서: `council_sessions/round_3/refinement/collector_feedback_round3.md`
