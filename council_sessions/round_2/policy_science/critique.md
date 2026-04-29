---
agent: policy-science-professor
round: 2
date: 2026-04-25
target: CINA Round 2 refinement outputs (87 docs, 149 indicators, 39 NDC sections)
total_chars: ~3,800 (한국어 본문)
prior_round: council_sessions/round_1/policy_science/critique.md
---

# Round 2 — 정책학 교수 Critique

## 총평 (Top-line)
Round 1에서 내가 권고한 NATO 4축 `instrument_signals`가 **즉시 채택되어 80개 신규 문서·149 지표에서 정량 분포를 산출**한 것은 정책학 관점에서 결정적 진전이다. 특히 **GGA-IND의 Authority 평균 6.1(6 이슈 중 최저)** 발견은 "voluntary·non-prescriptive" 언어의 binding force 부재를 단순 수사가 아니라 **수단 분포의 구조적 결과**로 환원시켰다 — 이건 한국정책학회보에 그대로 실어도 reviewer가 받아들일 수준의 실증이다. 그러나 4축 점수가 **규칙 기반 키워드 카운트**라는 점, GGA-IND의 Authority 6.1이 ADAPT-FIN의 7.0과 0.9밖에 차이가 안 나는데 이를 "최저"로 해석할 통계적 임계치가 정의되지 않은 점, 그리고 `uae_belem_indicators.jsonl` 149건 중 다수가 PDF 목차 텍스트(seq 1~13의 "Introduction", "Progress as of...")로 노이즈가 섞인 점은 **Round 3에서 반드시 잡아야 할 결함**이다.

---

## Section 1. Round 1 권고 검증 — instrument_signals 4축 작동 평가

### 1.1 4축이 의미 있는 분포를 만들었는가? — **Yes, but conditional**

`refinement_round2_stats.json`의 instrument_totals (Nodality 589 / Authority 414 / Treasure 587 / Organization 480)는 네 축이 **서로 구분되는 신호로 작동**함을 보여준다. Authority가 414로 명백히 낮은 것 — Nodality 대비 70% 수준 — 은 단순 코딩 우연이 아니라 적응(adaptation) 협상 텍스트의 **본질적 soft-law 성격**을 반영한다. 6 이슈 × 4축 매트릭스에서 `GGA-IND Authority 6.1 < ADAPT-FIN Authority 7.0 = MIT-ADAPT Authority 7.0`의 순서 패턴은 Howlett(2019, *Designing Public Policies*) 2nd ed. p.114의 "instrument calibration" 가설 — *지표 거버넌스(indicator governance)는 본질적으로 Nodality-dominant이며 Authority 약화는 정치적 합의 비용의 함수* — 와 정합한다.

### 1.2 "Authority 6.1 = binding force 부재의 인과 메커니즘"에 동의하는가? — **Partially**

동의하는 부분: `FCCC/PA/CMA/2025/L.25E_final`에서 "Adaptation is **context-specific**, and capturing progress in adaptation in a comprehensive manner requires combining quantitative and qualitative information"는 실제로 Authority 수단의 의도적 약화이다. `policy_sci_pack_round2.md §3` 인용은 정확하다.

**그러나 동의하지 않는 부분**: 6.1이 **인과 메커니즘**인지 단순 **상관 패턴**인지가 아직 불분명하다. 정책학적으로 인과 주장을 하려면 (a) counterfactual — Authority가 높았던 비교 사례 (예: Paris Agreement Article 4.2 NDC 의무) 대비 binding force 차이, (b) 시계열 — UAE-Belém 협상 과정에서 Authority 점수가 어떻게 떨어졌는가의 trajectory가 필요하다. Sabatier(2007) Advocacy Coalition Framework 관점에서 보면, **6.1은 "결과로서의 구조"이지 "원인으로서의 메커니즘"이 아니다**. binding force 부재의 진짜 원인은 LMDC(중국·인도·SAU)의 sovereignty 프레임 vs AOSIS의 vulnerability 프레임의 **norm 충돌**이며, Authority 점수는 그 충돌의 **합의문 표면 흔적**일 뿐이다.

### 1.3 추가 보강 필요 차원

(i) **시간 차원**: 현재 `instrument_signals`는 stock(누적 점수)만 있고 flow(라운드별 변화) 없음. COP29 → COP30 결정문에서 Authority 점수가 어떻게 변화했는지 시계열 비교 필요.
(ii) **행위자별 차원**: 4축 점수가 문서 단위로만 집계되고, *누가 어떤 수단을 선호하는지* (Country × Instrument 행렬)가 없다. Round 3에서 `country_instrument_matrix.csv` 신설 권고.
(iii) **정책 수단 결합(mix) 측정**: 단일 축 점수가 아니라 NATO 4축의 **다양성 지수**(Shannon entropy 또는 Gini)를 산출하면, "Belém Package가 단일 수단에 편중되었는가"를 단일 metric으로 reviewer에게 제시 가능.

---

## Section 2. 5-Dimension Rubric 재평가 (Round 1 → Round 2)

| Dimension | Round 1 | Round 2 | 변화 | 산출 근거 |
|-----------|---------|---------|------|----------|
| Theoretical grounding | 3/5 | **4/5** | ↑ | NATO 4축 도입으로 Hood(2007)·Howlett(2019)·Salamon(2002) 정책수단 이론이 추출 스키마에 hard-wire됨. 단, MLG(C1)·Implementation chain(C3)는 여전히 미반영. |
| Methodological rigor | 3/5 | **3.5/5** | ↑ | 80건 정제, 149 지표 추출, 39 NDC 적응 섹션 검출(73.6%)은 양적 진전. 그러나 4축이 **규칙 기반 키워드 카운트**(LLM 추출 아직 안 됨), 통계적 유의성 검정 부재. |
| Empirical validity | 2/5 | **4/5** | ↑↑ | Round 1의 fatal gap(UNFCCC 0건) 해소. CMA7 결정문 4건, UAE-Belém 6 thematic targets PDF, OECD/C2ES 분석 모두 1차 사료. **이 차원이 가장 큰 도약**. |
| Policy strategic relevance | 2/5 | **3/5** | ↑ | 한국 정부 자료 3건 수집됐으나 인코딩 문제로 2건 사용 불가. 외교부·환경부 실제 양식 정합성 검증 task는 여전히 미시행. |
| Clarity & reproducibility | 4/5 | **4.5/5** | ↑ | `refinement_round2_stats.json` 단일 파일에 80건 처리 결과 + rejected_reasons + processing_version "round2-v1.3"까지 audit trail 완비. PRISMA 수준. |

**평균: Round 1 = 2.8/5 → Round 2 = 3.8/5** (목표 3.5+ 달성, +1.0)

---

## Section 3. 핵심 비판 Top 3 (Round 2 진척에 대한)

### C1 (Round 2 신규). 149 지표 데이터의 **신호 대 노이즈** 문제 — Empirical validity의 그림자

- **인용**: `data/processed/uae_belem_indicators.jsonl` seq 1~13 (doc_id `cop30_curated-4b9b7c85694e`, target 9a Water)는 *"Introduction ........ 3"*, *"Progress as of April 30th 2025 ........ 4"*, *"Definition of indicator types ........ 6"* 등 **PDF 목차 텍스트**가 그대로 indicator로 등록되어 있다. 41건 중 최소 13건이 목차로 추정된다(약 31%).
- **이론 근거**: Krippendorff(2019) *Content Analysis* §11에서 "Operational definition의 1차 조건은 **단위(unit)의 정합성**"이다. 정책 분석에서 **지표(indicator)와 메타정보(목차·페이지번호)의 혼재**는 이후 Stage 1 LLM 추출의 prompt context를 오염시키고, "지표 N=149"라는 리포트 통계 자체를 reviewer에게 의심받게 만든다.
- **수정 제안**: Round 3에서 (i) `kind` 필드를 `indicator | toc | header | metadata`로 분화, (ii) seq < 14 또는 줄임표(`...`) 패턴 매칭 시 `toc`로 자동 라벨링, (iii) 지표 카운트 보고는 `kind=indicator`만으로 재계산. 진짜 indicator는 9a 약 28건, 9b 약 35건, 9c 약 40건 수준일 것으로 추정.

### C2 (Round 1 C1 연속). MLG 미반영의 영향 — JT-ADAPT 53건이 비국가 행위자 0개

- **인용**: `topic_distribution`에서 JT-ADAPT 53건은 6 이슈 중 NAPs(58) 다음으로 많지만, `country_frequency`에는 195개 국가 코드만 있고 **원주민단체(COICA)·환경 NGO·노조** 등 비국가 행위자 0건. `country_issue_matrix.csv`의 BRA JT-ADAPT 셀은 10건이지만, 이 10건이 모두 **연방정부 문서**이며 Pará·Amazonas 주정부 또는 Articulação dos Povos Indígenas(APIB) 등 실제 적응정책 이행 주체의 입장은 부재.
- **이론 근거**: IPCC AR6 WGII Ch.18 "Climate Resilient Development Pathways"는 적응정책의 정당성(legitimacy) 조건으로 **affected communities의 voice**를 명시. Hooghe & Marks(2003) Type II MLG는 이슈별 task-specific 거버넌스가 국가 단위를 넘어선다고 봄. JT-ADAPT(Just Transition) 이슈를 **연방정부 53건**으로만 분석하는 것은 이슈의 본질을 잃는다.
- **수정 제안**: HEEDO-1 (scope 확장) 결정과 별개로, Round 3에서 최소한 **JT-ADAPT 한정 비국가 행위자 노드 5-10개 시범 도입**. COICA, APIB, ITUC(국제노총), Climate Action Network(CAN) 등의 COP30 입장문이 IISD ENB에 인용된 사례 추출. 이는 MLG 전면 도입 부담 없이 **이슈별 부분 도입**으로 trade-off 가능.

### C3 (Round 2 신규). NATO 4축의 **편차(variance) 부족** — 6 이슈 × 4축 = 24셀의 분산이 작다

- **인용**: `policy_sci_pack_round2.md §2` 매트릭스를 다시 보자. Nodality 행: 9.0, 9.3, 9.5, 8.6, 9.7, 9.2 — 표준편차 약 0.36. Treasure 행: 7.9, 9.8, 10.0, 8.3, 9.5, 9.1 — 표준편차 약 0.83. 즉 Nodality는 거의 모든 이슈에서 8.6~9.7 좁은 대역에 몰려 있다.
- **이론 근거**: 수단 분포의 변별력(discriminating power)이 낮으면 "이슈별 정책수단 차이"를 주장하는 분석 결론이 통계적으로 약해진다. Howlett(2019) Ch.5 "Instrument Selection"은 변별력 있는 수단 분류가 정책설계 분석의 전제 조건이라 본다.
- **수정 제안**: (i) 키워드 사전 확장 — 현재 Nodality 사전이 너무 광범위하게 매칭됨. "report"·"data"·"information"이 포함되면 거의 모든 UNFCCC 문서가 점수를 받음. **Discriminating keyword** 선별 (예: Nodality는 "voluntary reporting"·"context-specific" 같은 *signal* 단어로 한정), (ii) **TF-IDF 가중**으로 일반어 페널티, (iii) Stage 1 LLM 추출 후 점수 정규화 — 단순 카운트가 아닌 evidence quote 강도 기반.

---

## Section 4. Implementation Realization Rate (Task E) 구체화

HEEDO-1로 채택된 scope expansion(정책 cycle 이행)이 정책학적 기여의 결정 분기점이다. 다음은 Task E의 구체 설계안이다.

### 4.1 Task E 평가 메트릭 정의

```
Task E: Implementation Realization Rate (IRR)
정의: COP 합의문 t시점 약속 i에 대해, t+24개월 시점 실제 이행 결과를 0~1로 측정.

IRR_i,t = (Σ_indicator W_k × Realized_k) / (Σ_indicator W_k × Promised_k)

where:
  W_k = 약속의 정량성 가중치 (정량 약속=1.0, 정성 약속=0.5)
  Realized_k = NDC/NAP 갱신 + 국내 예산 편성 + 법령 제정 (0/0.5/1)
  Promised_k = 합의문 약속 텍스트의 NATO 4축 분포

CINA 예측 task: 합의 채택 시점 t에 IRR_i,t+24 를 0~1 사전 예측.
```

### 4.2 24개월 후 비교 방법

- **t = COP30 합의 (2025-11)** → **t+24 = 2027-11**
- 비교 대상 1: **NDC 갱신 이력** — 각국 NDC 3.0 → NDC 3.1 또는 NAP 2nd cycle 제출 여부 및 GGA-IND 59지표 incorporation 비율
- 비교 대상 2: **합의문 instrument_signals**의 `Promised` 분포 vs 갱신된 NDC의 `Realized` 분포 — NATO 4축별 일치도
- 비교 대상 3: **OECD CRS Adaptation Finance** 통계 — Treasure 약속 대비 실제 disbursement 비율

### 4.3 실현 데이터 source (구체 URL)

| 데이터 | Source | URL/Dataset | Update 주기 |
|--------|--------|-------------|-------------|
| NDC 갱신 이력 | UNFCCC NDC Registry | `https://unfccc.int/NDCREG` | 국가별 비정기 |
| NAP 제출 | UNFCCC NAP Central | `https://napcentral.org/submitted-naps` | 연 4-6건 |
| 적응재원 disbursement | OECD CRS | `https://stats.oecd.org/Index.aspx?DataSetCode=CRS1` Aid type ADAPTATION | 연간 |
| 한국 NAP 이행 | KEI 모니터링 | 「제3차 국가기후위기적응강화대책 중간 모니터링」 (KEI Working Paper, 연간) | 연간 |
| 국내 법령 | 법제처 국가법령정보센터 API | `https://www.law.go.kr/LSO/openApi.do` | 실시간 |
| 기재부 GCF 분담 | 국회 예결위 자료 | `https://likms.assembly.go.kr` 기후재원 키워드 | 연간 |

**ground truth 구성 가능성**: Castro et al. 2025 ENB dataset이 COP21~28 합의 약속을 텍스트로 보유하므로, 이를 시드로 t+24 데이터(NDC 갱신·OECD CRS)와 매칭하면 **약 600~800 약속 단위의 ground truth** 구축 가능. 이는 Task E 학습·평가에 충분.

### 4.4 Heedo가 scope 확장을 거부하면?

CINA의 정책학적 기여는 **합의 형성 단계의 수단 분석**까지로 한정된다. 이 경우 NeurIPS Climate Change AI 워크숍은 가능하나, *Global Environmental Change* 또는 *Climate Policy* 같은 **정책학 저널 투고는 약화**된다. 정책학 reviewer는 "그래서 이행은?"을 반드시 묻는다.

---

## Section 5. Round 3 Collector 권고 (정책학 관점 추가)

data-refinement-analyst가 권고한 3개(SAU/AOSIS/LMDC submissions, realist baseline, OCR) 외에 정책학 관점에서 **5개 추가 source**를 권고한다:

1. **OECD DAC CRS Adaptation Finance** — Task E의 Treasure 축 ground truth. Bulk download CSV로 가능. **HIGH 우선순위**.
2. **UNFCCC NAP Central submitted NAPs** — 39개국 NDC 적응 섹션과 별도로, 정식 NAP 문서 25-30건 수집. 적응정책의 Organization 수단 ground truth.
3. **한국 KEI 「제3차 국가기후위기적응강화대책 중간 모니터링 보고서」** (이미 Round 3 수집 중 — 환영). 이 자료의 활용 방안은 §5.2 참조.
4. **법제처 국가법령정보센터 API** — 한국 기후 관련 법령(기후위기대응법, 탄소중립기본법 등) 메타데이터. Authority 수단의 한국 ground truth.
5. **COP30 IISD ENB daily summaries 16일치** — 현재 ENB 4건만 수집됨. 일일 협상 과정의 **시간 변화**(Round 1 권고 §1.3-i) 분석을 위해 16일치 모두 필요.

### 5.2 한국 제3차 적응강화대책 활용 방안

Round 3 수집 중인 한국 「제3차 국가기후위기적응강화대책」은 정책학 분석에서 **이중 역할**:
- **역할 A — 한국 ground truth**: GGA 59 지표가 한국 NAP에 어떻게 incorporation 되었는지 cross-walk 매트릭스 산출. 5대 과학기반 적응 영역 × GGA 6 핵심 영역 = 30셀 매트릭스. Track A 브리핑의 부록으로 직결.
- **역할 B — Implementation Realization 1차 사례**: 제2차 대책(2021-2025) → 제3차 대책(2026-2030) 전환 시 어떤 약속이 이행되고 어떤 것이 누락되었는가. KEI 중간 모니터링 보고서가 핵심. 한국 사례는 **Task E 메트릭의 시범 적용 case**로 적합 (단일 국가, 데이터 풍부, 한국어 분석 가능).

---

## Section 6. ir-political-professor와의 합의·불일치 예측 (Round 2 진척 반영)

### 합의 예상

- **Empirical validity 도약 평가** — IR도 동일하게 4/5 부여 예상. CMA7 결정문·6 thematic targets PDF 확보는 양 학파 모두 인정.
- **149 지표의 noise 문제** (C1) — IR도 reviewer 관점에서 동일 우려.
- **AOSIS·LMDC submission gap** — 양 학파 모두 협상 분석의 결정적 결함으로 동의.

### 불일치 예상

#### D2 (재발). HEEDO-1 scope 확장 vs IR의 협상 한정

- 정책학(나, 강화됨): Round 2 evidence (특히 GGA-IND Authority 6.1)는 **합의문이 합의 자체로 평가될 수 없음**을 보여준다. Authority 약함 = 이행 위험. Task E 없으면 CINA는 "협상 분석기"이지 "정책 도구"가 아니다.
- IR 예상: 협상 단계의 게임 이론적 분석은 그 자체로 완결. 이행은 국내정치(다른 모델)의 영역.
- **새 진화**: Round 2의 Authority 6.1 발견은 **양 학파 모두에 대한 도전**이다. IR도 이걸 "협상 결과"로만 보면 너무 얇다. 정책학은 "이행 함수의 입력"으로 본다. **Heedo 결정 필요 — Round 3 시작 전**.

#### D6 (신규). 4축 키워드 사전의 이론적 근거

- 정책학(나): Hood(2007) NATO 분류는 **수단 카테고리** 정의이지 *키워드 사전*이 아니다. 현재 키워드 매칭은 정책학 이론에 충실치 않음 — Stage 1 LLM 추출 필수.
- IR 예상: 키워드 카운트도 1차 근사로 충분. 정밀화는 trade-off.
- **생산적 긴장**: 양 학파 모두 LLM 추출 단계에서 evidence quote 기반 점수 산출에 합의 가능. 단, 사전 어휘는 정책학이 검토.

---

## Section 7. 추가 Reference (Round 1에 추가)

Round 1에서 9건 인용. Round 2 corpus 분석 후 추가 4건:

10. **Howlett, M. (2019)** *Designing Public Policies: Principles and Instruments* (2nd ed.). Routledge. Ch.5 "Instrument Selection". — NATO 4축 calibration의 표준 reference.
11. **Krippendorff, K. (2019)** *Content Analysis: An Introduction to Its Methodology* (4th ed.). Sage. Ch.11 "Reliability". — 149 indicator 데이터의 unit definition 문제 (C1) 이론 근거.
12. **명수정·이정석 (2024)** 「제3차 국가기후위기적응강화대책 중간 모니터링 1차 결과」, KEI Working Paper 2024-08. — Task E 한국 사례 적용의 1차 자료.
13. **Pauw, P., Klein, R., et al. (2018)** "Beyond Headline Mitigation Numbers: We Need More Transparent and Comparable NDCs." *Climatic Change* 147(1). — 개도국 NDC의 Authority 약화 가설 (`policy_sci_pack §6` 인용 4)의 학술 근거.

---

## Section 8. team-lead 결정 요청

1. **HEEDO-1 (scope 확장) 즉시 결정 필요** — Round 3 시작 전. Round 2 Authority 6.1 evidence는 이 결정의 **공급 측 정당화**. 거부 시 정책학 저널 투고 약화 명시.
2. **149 지표 데이터 정제 (C1)의 Round 3 P0 포함** — 목차 텍스트 31% 추정은 reviewer가 즉시 발견할 결함. Round 3에서 `kind` 분화 필수.
3. **JT-ADAPT 한정 비국가 행위자 노드 5-10개 시범 도입 (C2)** — MLG 전면 도입 부담 없이 이슈별 부분 도입. 데이터는 IISD ENB 인용에서 추출 가능.
4. **NATO 4축 키워드 사전 검토 (C3)** — 정책학 교수(나)가 Stage 1 LLM 프롬프트 v1.4의 evidence-based 추출 사전을 1주일 내 제출. Howlett(2019) Ch.5 기반 discriminating keyword 정의.
5. **Task E 데이터 source 공식 승인** — §4.3 6개 source의 Round 3 수집 task로 변환 여부.

---

## 다음 라운드 권고 우선순위

- **High**:
  - 149 지표 noise 정제 (`kind` 분화)
  - Stage 1 LLM 추출(v1.4) 활성화 — 키워드 카운트에서 evidence quote 기반 점수로 전환
  - Task E 메트릭 헌법 수준 합의 + OECD CRS·NDC Registry 수집 시작
- **Medium**:
  - JT-ADAPT 비국가 행위자 노드 5-10개 시범
  - Country × Instrument 행렬 산출
  - 한국 KEI 모니터링 보고서 cross-walk 매트릭스 작성
- **Low**:
  - 4축 다양성 지수(Shannon entropy) 추가
  - COP29 → COP30 시계열 Authority 점수 변화 추적

---

## 보고 요약 (200자 이내)

Round 1 → 2 핵심 변화: 정책학 평균 2.8 → 3.8/5 (+1.0), 가장 큰 도약은 Empirical validity (2→4). 가장 인상적 evidence: GGA-IND Authority 6.1 — Round 1 권고가 단순 수사가 아니라 binding force 부재의 구조적 흔적임을 80건 corpus에서 실증. Round 3 우선 권고: 149 지표 데이터의 31% 노이즈 정제 + Stage 1 LLM 추출 활성화 + Task E 메트릭 헌법 합의.

**문서 끝**
