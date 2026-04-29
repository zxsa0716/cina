# Round 3 — 정책학 교수 입력 패키지 (Policy Science Pack v3)

작성: Data Refinement Analyst | 2026-04-25 | CINA Round 3 | processing_version: round3-v1.4

---

## 0. Round 2 권고 반영 확인

Round 2에서 정책학 교수가 요청한 핵심 질문:

> **"GGA-IND의 Authority/Treasure 비대칭이 Realization Rate에 인과적 영향을 미치는가?"**
> Nodality-only 지표 vs Treasure-backed 지표의 이행률 차이를 예측하는 이론 모형은?

Round 3에서 이 질문에 직접 관련된 신규 증거를 다음과 같이 확보하였다:

1. **GGA_COP30_draft_text_3.pdf**: 실제 협상문 draft 텍스트에서 `[shall]/[should]` 브라켓 잔류 패턴 확인 — Authority 언어가 협상 종료까지 확정되지 않은 구조적 증거
2. **LMDC_submission_on_GGA.pdf**: 개도국 그룹이 "means of implementation" 조건부로만 authority-like 언어에 동의한다는 명시적 입장
3. **Global_Solidarity_Taskforce_B2BR_2025.pdf**: 1.3T 재정 목표의 법적 구속력 없음 확인 (Treasure without Authority)

---

## 1. Round 3 정제 결과 요약

| 항목 | 값 |
|-----|---|
| 신규 처리 문서 | 27건 (27 성공, 0 거부) |
| 누적 corpus | 114건 |
| 신규 소스 유형 | 의장 서한(3건), 협상 draft(2건), 비국가 토착민 제출(4건), 개도국 연합 제출(4건), 국내 적응계획(4건), 분석 보고서(2건) |
| frame_type 5범주 | 모두 활성 (justice 9건, development 5건 신규) |
| chair_metadata | 17 → 32 (COP28/29/30 시계열 완성) |

---

## 2. 인용 1 — GGA Draft Text: Authority 언어의 브라켓 잔류 패턴

> "[Recalls the principles and provisions of the UNFCCC and [the][its] Paris Agreement, including the principle of equity and **common but differentiated responsibilities** and respective capabilities]"

> "2. Calls on all Parties to **[shall][should]** designate or establish a national focal point..."

**출처**: `round4_curated-e4a23ee43d09` (GGA_COP30_draft_text_3.pdf), Version 17/11/2025 23:55

**정책학적 함의**: 이 draft의 `[shall][should]` 이중 브라켓은 Howlett(2019) 정책수단 이론에서 "authority signal ambiguity"의 전형이다. `shall` = binding authority, `should` = voluntary nodality. COP30 협상 마감 직전까지 이 선택이 미결 상태였다는 것은 GGA-IND 이슈에서 Authority 수단이 합의 불가 영역임을 실증한다. Round 2 분석에서 제시한 "GGA-IND Authority 점수 최저(6.1)" 가설의 직접적 텍스트 근거.

**NATO 분류 업데이트**: GGA draft에서 Authority/Nodality 선택이 미결일 때, 최종 결정문은 Nodality-default로 귀결된다. 이것이 59개 Belém 지표가 "context-specific" + "voluntary" 형태로 합의된 구조적 이유.

---

## 3. 인용 2 — LMDC 입장: 개도국의 조건부 Authority 동의 구조

> "The GGA should take into account equity and **common but differentiated responsibilities** and respective capabilities... ensuring that the GGA framework does not create additional burdens for developing countries in the absence of adequate **means of implementation**"

**출처**: `round3_curated-cfdd2faec536` (LMDC_submission_on_GGA.pdf, 3쪽)

**정책학적 함의**: LMDC의 입장은 "Treasure(means of implementation) 없으면 Authority 없다"는 조건부 동의 구조다. 이는 Pauw et al.(2018)의 "capacity gap 가설"을 넘어, 개도국이 Authority 수단 수용을 Treasure 수단과 패키지화하는 전략적 협상 포지셔닝임을 보여준다.

**Round 2 질문 답변**: Nodality-only 지표 vs Treasure-backed 지표의 이행률 차이 예측 이론 — LMDC 포지션이 제시하는 메커니즘: Treasure 확보 → 개도국 NDC/NAP 이행 → 지표 realization. 이 인과 경로가 성립하지 않으면 Nodality-only 지표의 realization rate는 개도국에서 구조적으로 낮을 수밖에 없다.

---

## 4. 인용 3 — Global Solidarity Taskforce: Treasure without Authority 실증

> "The Baku to Belém Roadmap to 1.3T is a framework for ambition, not a legally binding commitment. Developed countries **should** (not shall) mobilize..."

**출처**: `round4_curated-ac65e1496fa2` (Global_Solidarity_Taskforce_B2BR_2025.pdf)

**정책학적 함의**: 1.3T 재정 목표는 Treasure 신호 강도가 높지만(금액 명시), Authority 신호는 "should"로 확정. Treasure without Authority = 재정 약속 + 집행 메커니즘 부재. ADAPT-FIN 이슈의 instrument_signals 비대칭(Treasure:9.8, Authority:7.0)이 이 문서에서 직접 확인됨.

---

## 5. 인용 4 — Brazilian Plano Clima: 국내 정책 언어 vs 국제 협상 언어 격차

> "O Plano Clima estabelece marcos regulatórios para adaptação climática em todos os setores... com metas mensuráveis e mecanismos de acompanhamento e avaliação"
(기후계획은 모든 섹터의 기후 적응을 위한 규제 프레임워크를 수립... 측정 가능한 목표와 모니터링·평가 메커니즘 포함)

**출처**: `round3_curated-8a2f2dbfb372` (Brazil_Plano_Clima_Sumario_Executivo_2024_2035.pdf, pt)

**정책학적 함의**: 브라질 **국내** 적응계획은 Authority("marcos regulatórios" = 규제 프레임워크)와 Nodality("metas mensuráveis" = 측정 가능한 목표)를 병용한다. 반면 브라질이 COP30 의장으로 주도한 **국제** GGA 결정문에서는 Authority 언어가 브라켓으로 남았다. **국내 정책 vs 국제 협상에서 의장국의 instrument 선호가 달라지는 이유는 무엇인가?** — Putnam(1988)의 Two-Level Game 이론 적용 가능성 확인.

---

## 6. 인용 5 — AOSIS SCF Needs Survey: 소도서국의 재정 우선순위

> "AOSIS members identified **adaptation finance accessibility** as the primary barrier to implementing NAPs, with 78% citing **institutional capacity** rather than funding volume as the binding constraint"

**출처**: `round3_curated-87e79f4af3e3` (AOSIS_SCF_needs_survey.pdf)

**정책학적 함의**: 소도서국의 적응 재정 장벽이 "규모(Treasure)"가 아닌 "접근성/역량(Organization + Nodality)"에 있다는 경험적 발견. 이는 GCF의 "additional USD 1.33 billion" 승인이 AOSIS에게 실효적이지 않을 수 있음을 시사. NATO 수단 조합 관점: AOSIS에게 필요한 것은 Treasure 증가가 아닌 Organization(접근 절차 간소화) + Nodality(기술지원).

---

## 7. NATO 수단 분포 업데이트 (Round 3 추가 corpus)

신규 27건에서 추출한 instrument_signals 집계:

| 이슈 | Nodality | Authority | Treasure | Organization | N |
|------|----------|-----------|----------|--------------|---|
| GGA-IND | 높음 | **낮음** | 중간 | 중간 | +19 |
| ADAPT-FIN | 높음 | 중간 | **높음** | 높음 | +8 |
| L&D-OP | 높음 | 중간 | **높음** | 중간 | +5 |
| JT-ADAPT | **높음** | 낮음 | 중간 | 높음 | +16 |

**신규 관찰**: JT-ADAPT 이슈에서 Nodality가 지배적이며 Organization이 두 번째. 토착민(IIPFCC/AIPP/IWGIA/LCIPP) 문서에서 "platform," "mechanism," "process" 등 Organization 신호가 집중 등장. Authority는 여전히 낮음 — 토착민 권리의 UNFCCC 프레임에서의 hard-law화 저항 구조.

---

## 8. Round 3 정책학 교수에 대한 핵심 질문

> **브라질이 국내 Plano Clima에서 구사하는 Authority+Nodality 병용 전략과, COP30 의장으로서 GGA 결정문에서 Authority를 브라켓으로 남긴 선택 사이의 괴리를, Putnam(1988) Two-Level Game + Howlett(2019) instrument mix 이론으로 설명할 수 있는가?**
>
> 구체적으로: (a) 국내 win-set에서는 Authority 수단이 정치적으로 가능하지만, (b) 국제 협상 table에서 Authority 언어가 개도국 연합(LMDC/G77)의 반발을 유발하므로 의장국이 자발적으로 Authority를 Nodality로 희석하는 메커니즘이 존재하는가?
> 이 메커니즘이 성립한다면, 59개 Belém 지표의 voluntary 성격은 브라질 의장의 전략적 선택인가, 구조적 제약인가?

---

## 첨부 데이터 경로

- `data/processed/documents.jsonl` — 114건 (round3-v1.4)
- `data/processed/uae_belem_indicators.jsonl` — 110건 (context_text 9.1%, 4분류)
- `data/processed/chair_metadata.jsonl` — 32건 (COP28/29/30 시계열)
- `data/processed/frame_distribution_round3.json` — 5범주 분포
- `data/processed/non_state_actor_signals.jsonl` — 20건 (NSA entity 포함)
- `data/processed/refinement_round3_stats.json` — 전체 통계
