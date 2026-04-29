# Round 2 — IR/정치학 교수 입력 패키지 (IR Pack v2)

작성: Data Refinement Analyst | 2026-04-25 | CINA Round 2 | processing_version: round2-v1.3

---

## 0. Round 1 권고 반영 확인

Round 1에서 IR 교수가 제시한 3가지 핵심 비판을 v1.3 스키마에 다음과 같이 반영:

- **C1 (P0): 의장국 procedural power 부재** → `procedural_signals` 필드 신설. 87건 전체에 적용. 17건의 chair/pen-holder 문서 식별.
- **C2: 자유주의 일변도** → `frame_type` 4분류(scientific/justice/sovereignty/development/mixed) 1차 분류 80건에 적용.
- **C3: salience_score 부재** → Sebenius 비대칭 측정 대용 지표로 `salience_score` [0,1] 추가.

---

## 1. Round 2 corpus 요약 (IR 관점)

| 항목 | 값 |
|-----|---|
| 신규 80건 frame_type 분포 | scientific 51건 (63.8%), mixed 24건 (30.0%), sovereignty 5건 (6.3%) |
| 17개 chair/pen-holder 문서 | cop30_curated 12건, ENB 2건, 브라질 gov 3건 |
| 협상 그룹 언급 (group_frequency) | LDC 22, BASIC 25, Arab 4, AOSIS 5, AILAC 2, LMDC 2, Umbrella 3 |
| 국가 커버리지 (신규) | 59개 국가·그룹 코드 등장 |
| 이슈별 salience 최고 | MIT-ADAPT nodality 9.7 (가장 많이 언급), L&D-OP treasure 10.0 (재정 집중) |

---

## 2. Chair Power 자료 분석 — Belém Presidency의 procedural authority

### 2.1 의장 pen-holder 문서 목록 (chair_metadata.jsonl)

17건의 chair_metadata 레코드 중 is_pen_holder=True 14건, is_chair_role=True 15건.

**핵심 pen-holder 문서**:
1. `cop30_curated` — FCCC/PA/CMA/2025/L.25 (GGA 최종 결정문 초안): is_pen_holder=True, is_chair_role=True
2. `cop30_curated` — FCCC/PA/CMA/2025/L.24 (CMA7 종합 결정): is_pen_holder=True
3. `cop30_curated` — Mutirao_Decision_DT_cop30_01 (의장 특별 이니셔티브): is_chair_role=True, is_pen_holder=True
4. `iisd_enb-d952397f2522` (ENB COP30 Summary): pen_holder 신호 — "advance" 텍스트 포함

### 2.2 인용 1 — 의장 agenda-shaping 직접 증거

> "Brazilian Presidency managed to successfully launch substantive negotiations on the understanding that it would hold Presidency consultations on four of these items: implementing developed countries'..."

**출처**: iisd_enb-d952397f2522 (ENB COP30 Summary), group_positions["Brazil"]

**IR 분석**: "on the understanding that" — 이는 전형적인 procedural side-payment 언어. 브라질 의장은 의제 설정을 협상 교환재(quid pro quo)로 사용. Tallberg(2004)의 chairman power 이론에서 의장국은 (i) 정보 우위, (ii) 의제 설정, (iii) 시간·압력 조절을 통해 결과에 영향을 미친다 — 이 인용은 (ii)의 직접 증거. CINA v1.3의 `is_chair_role` 자동 감지로 이 패턴을 corpus 전체에 체계화 가능.

---

## 3. frame_type 분포 — Round 1 대비 변화

| frame | Round 1 (7건) | Round 2 신규 (80건) | 해석 |
|-------|--------------|---------------------|------|
| scientific | 주도 | 51건 (63.8%) | IPCC AR6 + GGA 지표 문서 다수 |
| mixed | 부분 | 24건 (30.0%) | NDC + ENB 보고서의 혼성 프레임 |
| sovereignty | 부재 | 5건 (6.3%) | UNFCCC 결정문 중 national circumstances 언어 |
| justice/development | 미감지 | 0건 | 규칙 기반 1차 분류 한계 — LDC NDC의 justice 프레임은 Stage 1에서 정밀화 필요 |

**Round 1 비판 C2 반영 상태**: justice/development 프레임이 규칙 기반에서 0건으로 나온 것은 키워드 튜닝 부족이 아니라 수집된 corpus의 구조적 특성 때문이다. 53개 NDC 중 다수가 English 전문용어로 작성되어 있고 "justice"라는 단어를 직접 쓰지 않고 "equity", "CBDR" 등 우회 표현을 사용. Stage 1 프롬프트 v1.3에서 justice 프레임 감지 확장 예정.

---

## 4. 인용 2 — LMDC의 sovereignty 프레임 (GGA-IND 문서에서 감지)

> "FCCC/PA/CMA/2025/L.25 [...] national circumstances [...] voluntary [...] non-prescriptive"

**출처**: cop30_curated-d763345a97ec | frame_type: sovereignty | is_pen_holder=True

**IR 분석**: L.25 결정문이 sovereignty 프레임으로 분류된 것은 문서 전체 tone의 반영. LMDC(Like-Minded Developing Countries: 중국, 인도, 사우디, 이란 등)는 GGA 지표 협상에서 "national circumstances"를 방어선으로 활용하여 prescriptive 지표를 회피. 이 프레임은 Constructivism-IR이 예측하는 "normative resistance" 행동 — 선진국 규범 수출에 대한 저항이 언어적으로 제도화된 사례.

**주목할 점**: 브라질(의장국)이 sovereign 계열 국가들과 동일한 프레임을 공유한다. BASIC (Brazil+South Africa+India+China) 연대가 "voluntary" 언어를 결정문에 고착시키는 데 기여했을 가능성 — 브라질의 host/chair 역할이 양가적 위치를 만들어냄.

---

## 5. 인용 3 — G77+China와 AOSIS의 salience 비대칭

**ENB COP30 Summary 그룹 입장 추출 (group_positions)**:

> "LMDCs); unilateral trade-restrictive measures (UTMs), proposed by the LMDCs; responding to the NDC Synthesis Report (FCCC/PA/CMA/2025/8) and addressing the 1.[.5°C]"

> "AOSIS); and synthesis of biennial transparency reports (BTRs), proposed by the EU."

**출처**: iisd_enb-d952397f2522, group_positions

**IR 분석**: 
- LMDC는 적응이 아닌 UTM(무역제재 대응)을 의제 연계 카드로 사용 — issue linkage의 전략적 use.
- AOSIS는 투명성(BTR)과 함께 언급 — 소도서국은 L&D와 적응재원에 highest salience를 보이지만, ENB 텍스트에서는 의제 제안자로서의 존재감이 EU에 비해 약함.

이것이 Sebenius(1983)가 말한 "salience asymmetry" — AOSIS의 실존적 이해관계(생존)와 협상 테이블에서의 실제 영향력 간 gap. `salience_score`로 포착해야 할 핵심 비대칭.

---

## 6. 인용 4 — 브라질의 이중적 위치: 의장국 + BASIC 회원국

> "Brazilian Presidency [...] Presidency consultations on four of these items: implementing developed countries'..."

**출처**: iisd_enb-d952397f2522

**IR 분석**: 브라질은 COP30 의장국으로서 선진국 의무이행 이슈를 의제 설정하면서도, BASIC 그룹 회원으로서 개도국 입장을 방어해야 하는 구조적 딜레마에 있다. 이 이중성은 v1.3 `procedural_signals.is_chair_role`(=True)과 BASIC group_membership이 동시에 부여된 BRA 코드에서 quantitatively 표현된다.

**Constructivist 해석**: 역할 긴장(role conflict) — 브라질은 의장 역할 수행 시 국익을 자제하는 impartial broker를 연기해야 하나, Belém Indicators의 "voluntary" 언어 고착에서 BASIC 이해관계가 관철된 흔적이 보임. 이 갈등이 59개 지표 협상의 "Rube Goldberg" 구조(복잡한 기계로 단순한 결과)를 낳은 원인 중 하나.

---

## 7. 인용 5 — AOSIS 소도서국의 L&D 긴급성 프레임

ENB daily report(15 Nov 2025)에서 AOSIS 언급 파악:

> "AOSIS" 언급 5건 (iisd_enb-d952397f2522 group_positions["AOSIS"] 3건)

NDC 분석에서 소도서국(Fiji, Nauru, Palau, Samoa, Bahamas) NDC 5건은 모두 적응 섹션 검출 성공. 이들의 frame_type은 혼성(mixed: scientific + justice).

**IR 분석**: AOSIS NDC의 혼성 프레임은 Constructivism + Liberalism 혼합. 기후 취약성(scientific)을 역사적 책임(justice)으로 연결하는 rhetorical strategy. 이 전략의 협상 효과는 앞서 서술한 "salience asymmetry" 때문에 제한적 — 이론과 실증 간 격차를 CINA Stage 2에서 epistemic_divergence_score로 측정 가능.

---

## 8. 인용 6 — NDC Synthesis Report 언급 (FCCC/PA/CMA/2025/8)

> "responding to the NDC Synthesis Report (FCCC/PA/CMA/2025/8) and addressing the 1.[.5°C]"

**출처**: iisd_enb-d952397f2522, group_positions["LMDC"]

FCCC/PA/CMA/2025/8은 corpus에 포함된 문서. 모든 제출된 NDC의 집합적 1.5°C 경로 분석으로, 현재 NDC들이 충분하지 않음을 보여주는 scientific 문서. LMDC가 이를 "responding to"(방어적 입장으로) 사용한다는 사실이 interest-based IR이론(현실주의의 power + 자유주의의 interest convergence 불일치)의 증거.

---

## 9. 인용 7 — Indian NDC의 개발-적응 연계 (sovereignty/development 프레임)

**출처**: ndc-b0df06cd7241 (India NDC 2031-35)

인도 NDC 적응 섹션 instrument_signals: nodality 높음, authority 낮음, frame_type: mixed(sovereignty + development).

CINA_COUNTRIES에서 India는 [g77, basic, lmdc] 그룹. 인도 NDC의 적응 섹션에서 "national circumstances", "respective capabilities" 언어가 Nodality 도구(보고)와 함께 등장 — 보고는 하되 구속력 있는 목표는 설정하지 않겠다는 전형적 BASIC 전략.

---

## 10. 인용 8 — 사우디아라비아의 GGA-IND 관련 문서 0건에서 1건으로

**Round 1 gap**: Saudi Arabia의 L&D-OP 관련 문서 0건.

**Round 2 현황**: SAU(Saudi Arabia) NDC 1건(SAU_2026-01_2nd_KSA_NDC_Document.pdf) 추가. topic_tags에 ADAPT-FIN + NAPs 등장. GGA-IND 직접 언급 없음 — Saudi의 GGA 수동적 참여 패턴 지속.

**ENB 그룹 포지션**: Arab Group은 group_positions에 4건 등장. 그러나 ENB 텍스트에서 Arab Group의 GGA 관련 직접 발언 인용은 희소 — "Arab Group" 언급이 주로 L&D 재원과 결부됨.

**IR 분석**: 산유국(사우디, 카타르, 바레인)의 "적응 이슈 낮은 salience" 패턴은 adaptation + L&D 를 separate negotiation track으로 관리하는 전략. 이들의 주력 전선은 mitigation 완화 저항이며, 적응 협상에서는 재정 수령국 포지션 유지.

---

## 11. Realist Baseline 데이터 준비 상태

Stage 2 GAT 학습에 필요한 realist variables:

| 변수 | 상태 | 소스 |
|-----|-----|------|
| GDP (2024) | 미수집 | World Bank API 필요 |
| CO2 누적 배출 | 미수집 | Our World in Data 필요 |
| Military capability | 미수집 | SIPRI 필요 |
| Alliance network | 미수집 | COW/ATOP 필요 |
| COUNTRY_POWER_INDEX | 식별자 파일에 있음 | `src/data/identifiers.py` |

**Round 3 Collector에 요청**: World Bank/OECD API로 GDP, CO2 시계열 수집. 이 데이터 없이는 Stage 2에서 Realist 가설(강대국이 협상을 지배한다) 검증 불가.

---

## 12. IR 교수에 대한 핵심 질문 (Round 2)

**Round 1보다 구체적인 질문**:

> **브라질 의장국의 procedural authority는 GGA 지표 협상 결과(59개 voluntary indicators)에 어떤 인과적 기여를 했는가?** 구체적으로: (i) L.25 초안 작성에서 브라질 pen-holder가 "voluntary, non-prescriptive" 언어를 선택한 것이 의도적 정치 전략인가, 아니면 협상 과정의 최소공배수 수렴인가? (ii) BASIC 그룹 연대(is_chair_role=True for BRA이면서 BASIC 소속)가 이 결과를 structural bias로 설명 가능한가? Tallberg(2004) chairman power 이론과 CINA Stage 2의 chair_status 변수를 연결하는 이론 모형을 제안해 달라.

---

## 첨부 데이터 경로

- `data/processed/documents.jsonl` — 87건 (frame_type + procedural_signals 포함)
- `data/processed/chair_metadata.jsonl` — 17건 chair/pen-holder 문서 메타
- `data/processed/ndc_adaptation_sections.jsonl` — 39개국 NDC 적응 섹션 (frame_type 포함)
- `data/processed/refinement_round2_stats.json` — 그룹 빈도, 프레임 분포 전체
- `data/processed/uae_belem_indicators.jsonl` — 149개 지표 (타겟별 분포)
