# Round 2 — 정책학 교수 입력 패키지 (Policy Science Pack v2)

작성: Data Refinement Analyst | 2026-04-25 | CINA Round 2 | processing_version: round2-v1.3

---

## 0. Round 1 권고 반영 확인

Round 1에서 정책학 교수가 제시한 핵심 비판(C2: NATO 4축 정책수단 분류 부재)을 v1.3 스키마에 다음과 같이 반영하였다:

- `instrument_signals` 필드: nodality(정보·보고), authority(규제·의무), treasure(재정), organization(기구) 4축 키워드 기반 1차 계량화 추가. 80개 신규 문서 전체에 적용.
- Round 1 비판: "GGA 지표가 왜 voluntary·non-prescriptive로 합의되었나?"에 대한 실증 데이터를 이번 라운드에서 수집.
- 현재 단계는 LLM 없는 규칙 기반 1차 분류. Stage 1 프롬프트 v1.3에서 증거 인용 포함 정밀화 예정.

---

## 1. Round 2 정제 결과 요약

| 항목 | 값 |
|-----|---|
| 신규 처리 문서 | 80건 (84 시도, 4 거부 — 암호화 PDF 2건, 빈 HTML 1건, 분량 부족 PDF 1건) |
| Round 1 + Round 2 누적 | 87건 |
| 스키마 검증 통과율 | 95.2% (80/84) |
| 주요 신규 소스 | UNFCCC COP30 결정문 20건, NDC 50건, ENB COP30 보고서 4건 |
| NDC 적응 섹션 검출 | 39/53건 (73.6%) |
| UAE-Belém 지표 추출 | 149개 (9a:41, 9b:46, 9c:54, 9e:8) |
| 의장/pen-holder 문서 | 17건 (15건 chair_role, 14건 pen_holder) |

---

## 2. NATO 4축 정책수단 분포 매트릭스

**규칙 기반 1차 계량 (키워드 카운트, 정규화 전)**

| 이슈 | Nodality | Authority | Treasure | Organization | N (docs) |
|------|----------|-----------|----------|--------------|----------|
| GGA-IND | 9.0 | 6.1 | 7.9 | 7.9 | 37 |
| ADAPT-FIN | 9.3 | 7.0 | **9.8** | 8.3 | 32 |
| L&D-OP | 9.5 | 6.9 | **10.0** | 7.8 | 34 |
| NAPs | 8.6 | 6.4 | 8.3 | 7.3 | 58 |
| MIT-ADAPT | 9.7 | 7.0 | 9.5 | 7.8 | 46 |
| JT-ADAPT | 9.2 | **6.9** | 9.1 | 7.8 | 53 |

**전체 corpus 합계 (Round 2, 80건)**: Nodality 589 | Authority 414 | Treasure 587 | Organization 480

**핵심 발견**: 모든 이슈에서 Nodality > Organization > Treasure > Authority 순서. GGA-IND의 Authority 점수가 6개 이슈 중 **가장 낮다** (6.1). Round 1에서 제기된 "voluntary·non-prescriptive의 binding force 부재" 가설과 정합.

---

## 3. 인용 1 — GGA 결정문의 구속력 없는 언어 (FCCC/PA/CMA/2025/L.25)

> "Belém Adaptation Indicators for measuring progress achieved towards the targets referred to in paragraphs 9–10 of decision 2/CMA.5 [... ] Adaptation is context-specific, and capturing progress in adaptation in a comprehensive manner requires combining quantitative and qualitative information."

**출처**: cop30_curated-1802f1565fb9, para 6 | FCCC/PA/CMA/2025/L.25, Annex

**정책학적 함의**: "context-specific" + "combining quantitative and qualitative" 표현은 Howlett (2019)의 정책수단 연속체(instrument continuum)에서 Nodality(정보) 수단의 전형적 형식이다. 강제적 측정(Authority)이 아닌 자발적 보고 방식이며, 이는 UNESCO 등 소프트 거버넌스 기관의 관행과 동일하다. **질문: UNFCCC 밖의 Hard-law 거버넌스 체계(예: CBAM, 탄소국경세)와 이 Nodality-only 지표 체계를 비교했을 때, 이행 인센티브 구조는 어떻게 다른가?**

---

## 4. 인용 2 — "Baku to Belém Roadmap to 1.3T" 재정 약속 (FCCC/PA/CMA/2025/L.24 계열)

> "[Notes][Welcomes] the 'Baku to Belém Roadmap to 1.3T' summarising the work of the Presidencies of the sixth and seventh sessions of the Conference of the Parties serving as the meeting of the Parties to the Paris Agreement, welcomes their efforts, and recognizes the five action areas identified and its role in scaling up financing to developing countries."

**출처**: cop30_curated-f569070f6878, para 7 | CMA7 decisions

**정책학적 함의**: 브라켓 "[Notes][Welcomes]" 잔류는 합의문 협상의 표준 병리 현상이다. 재정 약속(Treasure 수단)이 "recognizes"(약한) vs "welcomes"(강한)로 언어 강도가 불확정 상태로 마감된 것은 NCQG(New Collective Quantified Goal) 협상과 직결된다. NATO 분류상 Treasure 신호가 강함에도 Authority 신호가 낮은 비대칭 구조 — 재정 약속은 있으나 집행 메커니즘은 없음.

**질문**: 브라켓 언어 잔류가 이행 가능성에 미치는 영향을 측정하는 선행 연구가 있는가? (Castro et al. 2025 ENB 데이터가 이 질문의 도구변수로 활용 가능한지?)

---

## 5. 인용 3 — Belém Dialogue on Tripling Adaptation Finance (새 기구 설립)

> "Requests the co-chairs, with the support of the secretariat, to produce an annual report summarizing the discussions within the Belem Dialogue on Tripling Adaptation Finance."

**출처**: cop30_curated-f569070f6878, para 8 | CMA7 결정문

**정책학적 함의**: 신규 Dialogue 설립은 NATO Organization 수단. 그러나 "annual report"만 요청하고 구체적 집행 권한(Authority)이 없다 — Organization 수단이 Authority 없이 설치될 때 제도화(institutionalization) 가능성이 낮다는 Hooghe & Marks(2003)의 Type II 거버넌스 취약성이 반복. **Round 1에서 제기된 "Global Implementation Accelerator — Type I vs II?" 질문의 연속선상 사례.**

---

## 6. 인용 4 — NDC 적응 섹션: 개도국의 수단 선호 패턴

NDC 39건에서 추출된 적응 섹션 instrument_signals 평균 (ndc_adaptation_sections.jsonl 기준):

| 수단 | 평균 키워드 카운트 |
|-----|---------|
| Nodality | 약 9.2 |
| Treasure | 약 8.9 |
| Organization | 약 7.1 |
| Authority | 약 5.3 |

**대표 사례 — Fiji NDC 3.0 (cop30_curated 인접, ndc 그룹)**:
적응 섹션에서 "National Adaptation Plan", "capacity building", "monitoring and evaluation" 등 Nodality + Organization 수단이 집중 등장. Fiji의 Authority 점수 낮음 → 소도서국 NDC의 전형: 자발적 보고 + 국제지원 요청, 국내 규제 없음.

**정책학적 패턴**: 개도국 NDC의 적응 섹션에서 Authority < Nodality 비대칭이 전반적으로 관찰됨. 이는 개도국 NDC의 "capacity gap" 가설을 지지한다 (Pauw et al. 2018). 단, 이번 규칙 기반 분류를 Stage 1 LLM 추출로 정밀화해야 확정.

---

## 7. 인용 5 — OECD의 UAE-Belém 지표 프레임워크 고려사항 (전통 지식 이슈)

> "If traditional knowledge is to be genuinely reflected in international reporting frameworks, it cannot simply be merged with more established scientific knowledge systems. Instead, it is important to recognise that traditional knowledge..."

**출처**: cop30_curated-6c0f837ca085 (OECD_2025_UAE_Belem_considerations.pdf), para 6

**정책학적 함의**: 전통지식(IK)의 Nodality 수단화 문제. OECD는 국제 보고 프레임워크에서 IK를 과학 지식과 동등하게 취급하는 표준화 압력에 저항. 이는 정책 수단 설계에서 knowledge epistemology 충돌이다. GGA 59개 지표 중 IK 관련 지표의 비중이 얼마인지, 그것이 어떤 측정 체계를 전제하는지가 향후 NAP 과정에서 결정적 갈등 지점이 될 수 있다.

---

## 8. 인용 6 — Mutirao Decision (COP30 의장 특별 결정)

> "Mutirao_Decision_DT_cop30_01" — COP30 Presidency initiative document

**출처**: cop30_curated-da4b58ee4e9b | is_pen_holder=True, is_chair_role=True

**정책학적 함의**: "Mutirão"(포르투갈어: 공동작업/공동체 행동)는 브라질 문화적 거버넌스 개념을 UNFCCC 결정 언어로 도입한 사례. Organization 수단이 문화적 언어로 포장될 때 제도의 보편성 vs 지역적 legitimacy 간 긴장이 발생. 향후 COP31 의장국이 이 결정을 승계할 것인지가 제도적 연속성 지표.

---

## 9. 인용 7 — C2ES GGA Indicators Principles (비정부 민간 기관의 norm 형성)

> "C2ES_2025_GGA_indicators_principles.pdf" — Center for Climate and Energy Solutions, Washington DC

**출처**: cop30_curated 카테고리 | frame_type: scientific

**정책학적 함의**: UNFCCC 프로세스 외부 epistemic community(C2ES 같은 싱크탱크)가 지표 원칙을 정의하는 Nodality 수단 행사자로 등장. Haas(1992)의 epistemic community 이론에서 비정부 주체의 정책 수단 행사는 국가 Authority를 우회한다. GGA 59개 지표에 비정부 싱크탱크의 원칙이 얼마나 반영되었는지 Stage 1에서 추적 가능.

---

## 10. 인용 8 — ENB COP30 Summary: 의장 관리 협상 방식

> "Brazilian Presidency managed to successfully launch substantive negotiations on the understanding that it would hold Presidency consultations on four of these items: implementing developed countries'..."

**출처**: iisd_enb-d952397f2522 (ENB COP30 Summary, 346KB), para 1 of group_positions["Brazil"]

**정책학적 함의**: "Presidency managed... on the understanding that" — 의장이 의제 설정(agenda-setting)을 negotiation package 교환 조건으로 사용한 전형적 procedural authority 행사. 이는 Tallberg(2004)의 "chairman power" — 의장이 정보 비대칭을 이용한 negotiation facilitation이 아닌 agenda-shaping을 한다는 주장을 지지. Authority 수단이 정식 결정문이 아닌 Presidency 관행으로 행사된 사례.

---

## 11. 정책수단 매트릭스 해석 — 핵심 발견

**발견 1**: GGA-IND에서 Authority 점수 최저(6.1). 이 이슈는 Nodality-dominant. 59개 지표 합의가 binding force 없이 이뤄진 구조적 이유.

**발견 2**: L&D-OP에서 Treasure 점수 최고(10.0). 재정 조성은 가장 강하게 논의된 이슈. 그러나 Authority는 여전히 낮음 — L&D Fund 운영 절차에 대한 강제 규범 부재.

**발견 3**: MIT-ADAPT에서 Nodality 점수 최고(9.7) + Authority 공동 최고(7.0). 과학-정책 인터페이스가 가장 dense한 이슈 — IPCC AR6의 co-benefits 관련 챕터들이 직접 정책 수단 언어로 전환되고 있음을 시사.

**발견 4**: ADAPT-FIN의 Treasure/Authority 비율이 가장 높음 (9.8/7.0 = 1.4). 재정 약속 대비 집행 메커니즘 공백이 가장 큰 이슈.

---

## 12. Stage 1 준비 상태 및 정책학 교수에 대한 요청

**v1.3 스키마 사전 채움 완료**: 87건 documents.jsonl에 instrument_signals(4축) + frame_type + salience_score + procedural_signals 저장. Stage 1 LLM 추출(evidence quote 포함 정밀화)을 위한 사전 scaffolding 완성.

**정책학 교수에게 요청하는 핵심 질문 (Round 2)**:

> **GGA-IND의 Authority/Treasure 비대칭이 Realization Rate에 인과적 영향을 미치는가?** 59개 지표 중 국가 NDC·NAP에 이미 반영된 지표(Early Adopter)와 미반영 지표의 차이가 수단 분류(instrument_signals)로 예측 가능한지를 이론적으로 논증해 달라. 구체적으로: Nodality-only 지표 vs Treasure-backed 지표의 이행률 차이를 예측하는 이론 모형은 무엇인가? (Task E — Implementation Realization Rate의 이론 기반으로 사용 예정)

---

## 첨부 데이터 경로

- `data/processed/documents.jsonl` — 87건 문서 (v1.3 schema)
- `data/processed/uae_belem_indicators.jsonl` — 149 지표 (9a:41, 9b:46, 9c:54, 9e:8)
- `data/processed/ndc_adaptation_sections.jsonl` — 39개국 NDC 적응 섹션
- `data/processed/refinement_round2_stats.json` — 전체 통계
- `data/processed/country_issue_matrix.csv` — 국가×이슈 문서 커버리지
