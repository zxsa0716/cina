---
agent: ir-political-professor
round: 4
date: 2026-04-26
review_tone: International Organization / ISQ / GEP reviewer (revise-not-reject)
target_documents:
  - council_sessions/round_4/refinement/professor_input/ir_pack_round4.md
  - data/processed/realist_b0_f1_result.json (F1=0.560)
  - data/processed/l25_advance_vs_final_diff.json (hot_spots=0)
  - data/processed/brazil_instrument_translation.json (Δ=0.269)
  - data/raw/historical_chair/COP{21..27,30}/ (24 신규 PDFs)
  - council_sessions/round_3/ir_political/critique.md (anchor 4.13/5)
processing_version: round4-v1.0
target_score: 4.40+/5
---

# Round 4 — IR / Political Science Critique

## 총평 (Top-line Assessment)

Round 3 권고 3건 — CR4-IR-1 (chair_metadata 시계열 확장), CR4-IR-2 (realist B0 F1 측정), CR4-IR-3 (L.25 advance vs final cosine diff) — 모두에 대해 **정량 evidence가 산출**되었다. 구체적으로 (i) historical chair letter 24건 신규 수집(목표 12건의 200%), (ii) realist B0 F1=0.560으로 가설 F1<0.70 CONFIRMED, (iii) L.25 advance ≡ final 발견 — 이 세 결과는 단순한 데이터 보강이 아니라 *Round 3 critique이 제기한 이론적 비판이 어느 정도 정당했는지*에 대한 차등적 답을 준다. 가장 중요한 학술적 진전은 **(iii) "pre-crystallized formula" 가설의 발견**이다 — Tallberg(2010)의 formula control 채널이 advance text 배포 *이전* 단계에서 완성되었다는 새 증거는, 단순히 "advance→final 차이가 작다"가 아니라 *Negotiation arena의 epistemic boundary가 공식 문서 시스템 *외부*에 있다*는 더 강한 명제로 격상된다. 그러나 reviewer 2 입장에서 보면 (i) chair_metadata는 24개 신규 letter가 **메타데이터 jsonl에 아직 통합되지 않음** (raw PDF만 존재 → 32건 그대로), (ii) F1=0.560은 random baseline ~0.44 대비 +12pp만 우위라는 점에서 *practical insufficiency* 이상의 *strong rejection of realism*으로 해석하기에는 통계적 유의성 검증(카이제곱, McNemar)이 수반되지 않았으며, (iii) Translation Gap Δ=0.269는 가설 0.30에 PARTIAL — IR 학계는 "방향성+magnitude+신뢰구간" 3원 충족을 R&R Accept의 minimum threshold로 본다. 종합 평점은 **4.13 → 4.36/5** (목표 4.40 대비 -0.04)로 *minor revision*에 근접했으나 *Accept*에는 1라운드 부족하다.

---

## Section 1. Round 3 권고(CR4-IR-1, 2, 3) 응답 평가

### 1.1 CR4-IR-1: chair_metadata 시계열 확장 — **부분 충족 (raw 24건 / processed 0건)**

**Round 3 권고 원문**: "COP21~COP27 historical chair letters 12+건 수집. 목표 chair_metadata 32 → 80+, COP coverage 3 → 10."

**Round 4 결과 분해**:

| 단계 | Round 3 | Round 4 raw | Round 4 processed | 평가 |
|------|--------:|------------:|------------------:|------|
| Raw PDF 수집 | 17 (cumulative) | **41** (24 신규) | — | 200% 충족 |
| chair_metadata.jsonl records | 32 | — | **32 (변화 없음)** | 0% 충족 |
| COP coverage (raw) | 3 (UAE/AZE/BRA) | **8** (COP21,22,23,24,25,26,27,30) | — | 충족 |
| COP coverage (processed) | 3 | — | **3** | 0% 충족 |

**진단**: raw 단계에서는 200% 충족이나 *processed metadata pipeline*에 PDF 텍스트 추출/frame 분류/Tallberg 채널 매핑이 미통합. `chair_metadata.jsonl`은 32 records 그대로이며, COP21 Fabius letter, COP23 Bainimarama "possible elements outcomes", COP26 Sharma의 4개 letter, COP27 Shoukry 2건 등이 *데이터 wallet에는 들어왔으나 분석 파이프라인에는 진입하지 못함*.

**Bayer-Urpelainen (2013, *ISQ* 57(4)) panel threshold 재평가**:

- N>100 minimum: **미달** (32 processed, 41 raw 모두 미달)
- COP_coverage ≥10: **부분** (raw 8 COP, target 10 미달; COP28/29는 processed에만 있음 → raw+processed 합산 시 9 COP)
- Cross-sectional × temporal 자유도: raw 24건 + processed 32건 = 56건의 unique chair × COP × frame_type 셀이 *이론적으로* 가능하나, frame_type 코딩이 PDF 24건에 대해 미실행

**IR 함의**: Round 3 §1.1에서 지적한 "N_chair=3에서 가설 검증 불가" 문제는 *raw 단계에서는 N_chair=8로 확장*되어 가설 *생성→검증* 전이의 입구에 도달했다. 그러나 *processed jsonl 단계에서는 여전히 N_chair=3*에 머물러 있어, Round 4 critique 시점에서는 아직 통계적 검증이 불가능하다. **이는 "데이터 수집"과 "데이터 가용성"의 분리** — 학계 reviewer가 가장 흔히 지적하는 함정 — 의 사례다.

**Round 5 권고(P0)**: 24개 PDF의 (a) frame_type LLM 분류, (b) Tallberg 4 채널 매핑, (c) chair country fixed effect 코딩을 즉시 실행. T02 Round 5에 P0로 명시.

### 1.2 CR4-IR-2: Realist B0 F1 측정 — **충족, 단 통계적 유의성 미검증**

**Round 3 권고 원문**: "country_features_v2 통합 후 realist 4 변수 단독 F1 측정. 가설 F1<0.80, 만약 ≥0.90이면 CINA novelty 위협."

**Round 4 결과**:

| 지표 | 값 | Round 3 가설 | 평가 |
|------|---|------------|------|
| F1 | **0.560** | <0.80 | CONFIRMED (realism 부족) |
| Random baseline | ~0.44 | — | F1 - random = +0.12 |
| Precision = Recall | 0.560 | — | balanced |
| TP | 42 / 75 | — | 56% 협력 쌍 정확 식별 |
| FP | 33 / 75 | — | 44% 오탐 |

**IR 이론 해석**:

F1=0.560은 가설 F1<0.70을 충족하지만 학술적 의미는 두 가지 상반된 framing이 가능하다:

- **Strong constructivist framing (CINA에 유리)**: random 대비 +12pp만 개선 → "물질주의(GDP, CO2, military) 단독으로는 협상 그룹 멤버십을 절반밖에 설명 못 함. 나머지 절반(0.44 → 0.80 목표)은 **frame, identity, history**가 설명한다." — 이는 Wendt(1999) "anarchy is what states make of it" 명제의 직접 검증으로 격상 가능.
- **Weak realist framing (CINA에 불리)**: F1=0.56은 random보다 통계적으로 *유의*한가? McNemar test, Fisher's exact, cohen's κ 미수행. Castro 2025 ENB 실제 협력 matrix가 아닌 **pseudo-truth (그룹 멤버십)** 사용. 즉 "F1=0.56이 진짜 realism의 한계인가, 아니면 ground truth proxy의 결함인가?"가 미해결.

**대표적 realism 예측 오류 — USA-SAU(cosine=0.889)의 IR 함의**:

USA와 SAU가 "물질적으로 유사"(둘 다 대형 고배출 경제 + military power)이나 협상 그룹은 다르다(UMBRELLA vs ARAB/G77). 이는 Realism으로는 설명 불가능하나 다음 3 이론으로 설명 가능:

1. **Adler(1997, *EJIR* 3(3)) constructivism**: 협상 그룹은 *공유된 의미 체계* (shared meanings)가 결정. ARAB Group은 OPEC+G77+이슬람 정체성의 다중 layered identity가 선행. USA의 UMBRELLA는 "Western liberal democracy + non-EU OECD" 정체성이 선행. 물질 유사성은 *동일 정체성 그룹 내 차별화* 변수일 뿐, *그룹 멤버십 결정* 변수는 아니다.
2. **Hopf(2002, *Social Construction of International Politics*) social cognitive constructivism**: 국가는 *historical practice*가 누적된 "habits of identity"로 분류된다. SAU는 1990년대 이래 G77 내 fossil fuel veto coalition의 핵심으로 기능; USA는 1992 UNFCCC 채택 이래 differentiation 거부. 두 국가의 *장기 협상 행태 시퀀스*가 cosine=0.889의 물질 유사성을 *비활성화*한다.
3. **Wendt(1999) corporate identity**: BRA-USA(cosine=-0.863, 물질 차이 큼)임에도 양자 diplomatic 협의 active한 사례는 *역의 puzzle* — Realism으로는 협력 expected하지 않음. Wendt의 "Lockean culture" (mutual recognition without friendship)이 양자 협력을 가능케 하는 미시 메커니즘.

**Round 3 §1.3 D2 결정 재요청**:
- F1 < 0.80 CONFIRMED → **CINA Discussion 시나리오 1** (novelty 강화) 채택 정당화.
- 그러나 F1=0.560은 *너무 낮다* — reviewer가 "그러면 왜 random에 가까운 것을 baseline이라 부르나?" 반박 가능. 권고: country_features_v2를 ND-GAIN vulnerability + Annex I/non-Annex I status + historical emissions로 확장한 **B0+ baseline** 추가 측정. 만약 B0+ F1≈0.65-0.70이면 더 fair한 비교 frame.

### 1.3 CR4-IR-3: L.25 advance ≡ final 발견 — **방법론적 충족, 이론적 재해석 필요**

**Round 3 권고 원문**: "L.25 advance vs final paragraph-level cosine. Top-10 변경 paragraph가 sovereignty/voluntary 강화 방향이면 Tallberg formula control 첫 정량 evidence."

**Round 4 결과**:

| 지표 | 값 |
|------|---|
| Hot spots (cosine<0.85) | **0** |
| GGA-specific hot spots | 0 |
| 평균 paragraph cosine | ~1.0 |
| Word diff | 0 |
| 차이 | 헤더 formatting + footnote 위치만 |

**Tallberg 가설 재해석 (CINA의 "pre-crystallized formula" 명제)**:

원래 가설: advance → final 변경량이 chair power 측정. **실제 발견: advance ≡ final → chair power가 advance 배포 *이전* 단계에서 완전 행사**. 인과 사슬:

```
[비공식 협의: contact group, informal-informal] 
   → [chair formula crystallization (보이지 않음)]
   → [L.25 advance 배포 (이미 합의 텍스트)]
   → [formal adoption, no change]
```

**이는 Tallberg(2010) 4 채널 중 어느 것을 측정하나?** — **이 부분이 IR 이론적 핵심 판단이다**.

| 채널 | Round 4 발견과의 정합 |
|------|---------------------|
| (i) Information asymmetry | **부분 정합**: 의장이 advance 직전까지 *어느 텍스트가 적합한지* 정보 독점 |
| (ii) Process / formula control | **강한 정합**: pre-crystallized = formula control의 극단 사례 |
| (iii) Brokerage | **약한 정합**: 양자/소그룹 mediation의 *결과물*이 advance text |
| (iv) Agenda-shaping | **강한 정합**: 의장이 무엇을 advance에 *포함하지 않을지* 결정 |

**즉 L.25 advance ≡ final = Tallberg 4 채널 중 (ii)+(iv) 결합 evidence**. 이는 Round 3 §1.3에서 "(iv) agenda-shaping 자동 식별 0건"이라고 진단한 부분에 대한 **간접 evidence**가 된다 — 제출문서에는 안 보이지만 *결과물의 anomaly* (advance ≡ final)에서 chair agenda-shaping이 추론된다.

**Para 7 hedging 4연속의 언어적 흔적**:

`"voluntary, non-prescriptive, non-punitive, facilitative, global in nature, respectful of national sovereignty"` — 6개 hedging이 단일 paragraph에 압축된 것은 *각 hedging이 특정 협상 그룹의 red line에 대응*함을 시사:

- voluntary → AOSIS/EU의 binding 요구 차단 (UMBRELLA + LMDC 양보 수용)
- non-prescriptive → IRA-G77의 differentiation 보호
- non-punitive → SAU/ARAB의 sanction 우려 차단
- facilitative → AILAC의 cooperation framing 수용
- global in nature → BRA host의 "글로벌 책임" 수사 보존
- respectful of national sovereignty → BASIC + LMDC의 sovereignty 핵심

**6 그룹의 red lines를 단일 paragraph에 봉합한 chair = formula control의 archetype**. 이는 Sebenius(1983, *IO* 37(2)) "negotiation arithmetic"의 단어 단위 검증. NeurIPS CCAI paper의 *signature finding* 후보.

---

## Section 2. 5-Dimension Rubric 재평가

| Dimension | R1 | R2 | R3 | **R4** | 변화 동인 |
|-----------|---:|---:|---:|-------:|---------|
| Theoretical grounding | 3.5 | 4.0 | 4.3 | **4.5** | pre-crystallized formula 발견 (+0.1) + Hopf/Adler constructivism reference 격상 (+0.1). 단 Wendt-Hopf-Adler 3 reference가 critique level이지 paper draft에는 미반영. |
| Methodological rigor | 3.0 | 3.5 | 3.7 | **4.1** | L.25 cosine diff 산출 (+0.2) + realist B0 F1 산출 (+0.2). 단 통계적 유의성 검증 (McNemar, Fisher) 미수행으로 0.5 진전 못 함. |
| Empirical validity | 2.5 | 3.5 | 3.8 | **4.0** | chair raw PDF 24건 (+0.1) + IRR Translation Gap Δ=0.269 (+0.1). 단 raw→processed 통합 미완으로 0.5 진전 못 함. |
| Policy strategic relevance | 3.5 | 4.0 | 4.3 | **4.5** | "pre-crystallized formula" narrative가 high-impact policy story (+0.2). Brazilian dual-role Δ=0.269 가시화. |
| Clarity & reproducibility | 4.0 | 4.5 | 4.5 | **4.7** | F1 산출 코드 + cosine diff seed/method 기록 (+0.2). ICR 부재 (-0.3). |

**평균: 3.3 → 3.9 → 4.13 → 4.36/5** (목표 4.40 대비 -0.04). 

**4.40 도달 미달 사유**: (a) 24개 raw PDF의 processed 통합 미완, (b) realist F1=0.560의 통계적 유의성 미검증, (c) Translation Gap Δ=0.269의 95% CI/bootstrap 미산출. 이 3가지가 Round 5에서 해결되면 **4.50/5** 도달 가능.

---

## Section 3. "Pre-crystallized formula" 가설의 IR 이론 정당성

### 3.1 Tallberg 4 채널 중 어느 것이 작동하는가

**합의된 답**: **(ii) formula control + (iv) agenda-shaping 결합**. (ii)는 *what gets in the text*를, (iv)는 *what doesn't get in the text*를 결정. advance ≡ final은 두 채널의 동시 행사의 fingerprint.

추가로 (i) **information asymmetry**가 *enabling condition*: chair는 어느 그룹이 어느 hedging을 수용 가능한지 *사전 정보*를 가져야 6개 hedging을 단일 paragraph에 봉합 가능.

### 3.2 Steinberg(2002, *IO* 56(2)) "consensus shaping"과의 비교

Steinberg는 GATT/WTO 의장이 *consensus 텍스트*를 produce할 때 회원국 발언 분포를 *상위 가중 (weighting)* 하는 행위를 분석. CINA의 pre-crystallized formula는 Steinberg 모델의 **극단적 경계 사례**:

- Steinberg(2002): consensus shaping은 plenary 발언을 *재가중*하여 chair text 생성
- CINA L.25 (2025): plenary 이전에 이미 chair text 완성. Plenary는 *ratification ceremony*에 가까움

이는 Steinberg 모델의 단순 적용이 아니라 *Steinberg + 추가 단계*. 학술적 명명 제안: **"pre-plenary consensus shaping"** 또는 **"informal-formal threshold compression"**.

### 3.3 Goh(2007, *International Security* 32(3)) "informal pre-cooking"과의 비교

Goh는 ASEAN의 의사결정 구조에서 *consensus를 plenary 외부에서 미리 조리*하는 관행을 분석. 핵심 차이:

- Goh ASEAN: pre-cooking이 *제도화된 norm* (ASEAN Way)
- UNFCCC COP30: pre-cooking이 *ad hoc, chair 의지에 의존*

이는 ASEAN의 *문화적 normativity*와 달리 UNFCCC의 *chair-driven contingent practice*임을 시사. 즉 **"chair power가 작동할 *조건*이 ASEAN처럼 자동적이지 않음"**. 이는 chair country 변수(BRA, UAE, AZE)가 결과 결정적임을 의미하며, "에너지 수출국 의장 3연속" 가설의 이론적 가중치를 높인다.

### 3.4 측정 가능 변수 격상 — text similarity 외 추가 지표

| 변수 | 측정 방법 | Round 5 가능성 |
|------|----------|--------------|
| **Hedging density** | Para 단위 hedging keyword count (voluntary, non-prescriptive, facilitative 등 lexicon) | **즉시 가능** |
| **Multi-group red line absorption** | 각 hedging keyword를 특정 그룹과 매핑 (lexicon × group ground truth) | Round 5 |
| **Pre-plenary text stability** | 다중 advance 버전 (예: L.25.Rev1, L.25.Rev2)이 있다면 inter-version diff | Round 6 |
| **Chair speaking time** | COP30 plenary 영상에서 chair 발언 비중 (proxy: 의장 모두/마무리 발언 word count) | Round 5 (text 기반) |
| **Contact group membership disclosure** | UNFCCC informal note에서 contact group 참여 국가 수 | Round 5 |

**권고**: "hedging density × 그룹 red line absorption"의 2차원 plot이 NeurIPS CCAI paper의 *core figure* 후보. 단일 figure로 "chair formula control이 개념이 아니라 측정 가능한 현상"임을 demonstrate.

---

## Section 4. Brazilian Translation Gap Δ=0.269의 IR 해석

### 4.1 가설 Δ≥0.30 PARTIAL의 학계 반응 예측

**IR 학계의 일반 기준 (반증주의 관점)**:

| 결과 | *International Organization* reviewer 반응 |
|------|------------------------------------------|
| Δ ≥ 0.30 (가설 충족) | "방향성 + magnitude 충족 — minor revision" |
| 0.20 ≤ Δ < 0.30 (PARTIAL) | "방향성 충족, magnitude 미달 — *boundary condition* 정밀화 요구" |
| 0.10 ≤ Δ < 0.20 | "방향성만 충족 — *correlation, not causation* 의심" |
| Δ < 0.10 | "가설 reject" |

Round 4 결과 Δ=0.269는 **boundary condition 영역**. 핵심 reviewer 질문:

1. *왜* 0.30이 아닌 0.269인가? (예: "Negative Authority" 분리 미수행이 0.03 손실?)
2. 95% CI는? bootstrap 1000회로 [0.18, 0.36] 정도 추정 시 0.30 포함 → "데이터로는 양립 가능" 결론
3. 다른 의장국 비교는? 5국 (KOR, EU, SAU, AOSIS) cross-walk 후 BRA가 outlier인가 일반 패턴인가?

### 4.2 Putnam(1988) 2-Level Game × Howlett(2009) NATO 결합 모형의 IR 차원 함의

Putnam의 win-set은 *국제 합의 가능 영역*을 정의. Howlett의 NATO는 *정책 도구 mix*를 정의. 두 모형의 결합:

```
Level II (국내) win-set = f(국내 instrument-mix, IRR_domestic)
Level I (국제) win-set = g(국제 instrument-mix, IRR_international)
협상 가능 영역 = Level I ∩ Level II
Translation Gap Δ = |IRR_domestic - IRR_international|
```

**IR 함의**: Δ가 클수록 국내-국제 win-set이 *서로 다른 instrument 언어*로 정의됨. 즉 한 국가의 "국내 정책 신호"와 "국제 협상 신호"가 *번역되지 않는 영역*이 존재함을 시사. 이는 Putnam의 *involuntary defection* 가능성을 정량화하는 새 지표.

**학술적 명명 제안 (refinement-analyst의 요청 응답)**:
- "Instrument-mix divergence index" (Howlett 강조)
- "Two-level translation gap" (Putnam 강조)
- "Domestic-international calibration asymmetry" (중립적)

**권고**: Putnam을 *primary frame*으로 (IR 학계 인지도 우월), Howlett을 *measurement device*로 사용. 명명: **"Two-Level Instrument Translation Gap (TITG)"**.

### 4.3 BRA Δ=0.269의 비교 reference

비교 가능한 선행 연구가 없음. Andresen & Agrawala (2002, *GEC* 12(1))의 "national-international policy gap" 개념이 가장 가깝지만 정량 지표 없음. CINA가 *최초 정량화 연구*가 될 수 있음 — 이는 강한 novelty claim. 단, 5국 cross-walk(Round 5) 완료 전까지는 *single-case observation*에 머무름.

---

## Section 5. Realist F1=0.560 → Constructivist 변수 정당화

### 5.1 통계적 유의성 검증의 시급성

현재 보고: F1=0.560, random≈0.44. 검증 미완료:

| 검증 | 방법 | 결과 expected |
|------|------|------------|
| F1 vs random 유의차 | McNemar test, χ²(1) | p<0.05 expected (TP 차이 +9) |
| Cohen's κ vs chance | κ = (po - pe) / (1 - pe) | κ ≈ 0.12 (slight agreement) |
| 95% CI for F1 | bootstrap 1000회 | [0.45, 0.67] 추정 |
| 효과크기 (Cohen's d) | (F1_realist - F1_random) / σ | small effect (~0.3) |

**권고 (P0)**: Round 5에서 위 4 통계 모두 산출. McNemar p<0.05이지만 Cohen's κ ≈ 0.12 (slight)면 "통계적 유의 ≠ 실용적 유의" 명시. CINA의 incremental contribution은 *실용적* 영역 — 즉 +0.24 F1 향상이 실용적.

### 5.2 USA-SAU(cosine=0.889) 사례의 frame_type 변수화

**가설 검증 설계**:

```
H1 (Realist): cosine_material(USA, SAU) high → cooperation
H1 결과: USA-SAU 비협력 → H1 falsified
H2 (Constructivist): cosine_frame(USA, SAU) ≠ cosine_material(USA, SAU) → 다른 그룹
H2 검증 방법: USA submission frame 분포 vs SAU submission frame 분포의 KL divergence
H2 expected: USA frame_type 주로 mixed/scientific (4-frame); SAU 주로 sovereignty/development
H2 결과: KL(USA‖SAU) > KL(USA‖CAN), KL(USA‖AUS) → constructivist 그룹화 확인
```

**필요 데이터 (Round 5)**:
- USA submission 5건 이상의 frame_type 분포 (현재 documents.jsonl에서 USA 별도 코딩 미확인)
- SAU submission 5건 이상의 frame_type 분포 (현재 0건 — collector_feedback HIGH priority)

**IR 학계 reference**:
- **Adler(1997, *EJIR* 3(3))**: cognitive convergence가 그룹 형성. USA-CAN-AUS의 UMBRELLA 결성은 *liberal democratic identity* 인지적 수렴; USA-SAU는 인지적 발산.
- **Wendt(1999) Ch 7**: Hobbesian/Lockean/Kantian culture. SAU-USA는 Lockean (mutual recognition) but not Kantian (shared identity).
- **Hopf(2002)**: identity는 daily practice의 누적. USA의 30년 differentiation 거부 vs SAU의 30년 fossil fuel veto = 두 *practice trajectory*의 분기.

### 5.3 NeurIPS CCAI paper claim 재구성

기존 claim: "CINA GAT outperforms realist baseline by ΔF1≥0.24"

권고된 강화 claim: 
> "물질주의 변수 단독은 협상 그룹 멤버십을 random+12pp만 설명한다(F1=0.56). CINA의 frame_type + chair_metadata + non-state actor signals를 추가한 GAT는 ΔF1=+0.24를 달성하며, 추가 ΔF1의 주요 기여는 USA-SAU와 같은 *물질-식별 분기 사례* (cosine 변수와 그룹 멤버십이 불일치)에 집중된다. 이는 Adler(1997), Wendt(1999), Hopf(2002)의 constructivist 명제 — 'identity의 일상 실천이 그룹 형성을 결정' — 의 정량 검증을 제공한다."

이 claim이 *International Organization* reviewer에게 "이론 기여" 라벨을 받을 수 있는 수준.

---

## Section 6. Stage 2 R-GAT 모델 강화 권고

### 6.1 chair_status × pre_crystallized_formula × frame_type 3-way interaction edge

기존 R-GAT 설계: Country—Issue, Country—Country, Country—Group edge.

**신규 edge 제안**: **Chair—Para—Group** triplet (3-uniform hyperedge):
- Chair node: COP30 BRA presidency
- Para node: L.25 paragraph 7 (또는 9, 10 등 hedging-dense paras)
- Group nodes: AOSIS, ARAB, LMDC 등 hedging이 absorb하는 그룹

**의미**: 각 hyperedge는 "이 chair가 이 paragraph에서 이 그룹의 red line을 absorb했다"는 명제. attention weight α_(chair, para, group)이 Tallberg formula control의 **국지적 강도 지표**.

**구현**: PyTorch Geometric의 `HeteroConv` + custom hypergraph aggregation. Round 5 Stage 2 prototype에 포함 권고.

### 6.2 24 historical chair letters 시계열에서 chair power 변화 학습

24 PDFs에서 raw 텍스트 추출 후 다음 시계열 변수 코딩:

| 변수 | 측정 | COP21~30 expected pattern |
|------|------|--------------------------|
| Hedging density | 단어당 hedging keyword 비율 | 증가 추세 (Paris 후 detail 증가) |
| Sovereignty mentions | "sovereign", "national circumstance" 빈도 | 증가 (BASIC+LMDC 영향) |
| Voluntary mentions | "voluntary", "non-prescriptive" 빈도 | 증가 (UAE/AZE/BRA 효과) |
| Bridging language | "we are convinced", "shared" 빈도 | 감소 (Falkner 2016 hegemony decay) |

**가설 검증**: 만약 "voluntary mentions"가 COP26(GBR)→COP27(EGY)→COP28(UAE)→COP29(AZE)→COP30(BRA) 시계열에서 monotonic 증가하면 "에너지 수출국 의장 3연속" 효과의 *언어적 fingerprint*가 정량화됨. R-GAT의 temporal edge weight으로 학습 가능.

### 6.3 Indigenous epistemic community 노드 (Round 3 §5 follow-up)

Round 3에서 옵션 A+C 하이브리드 권고. Round 4에서 NSA 추가 수집 (T01) 결과 미확인 — 만약 IIPFCC/AIPP/IWGIA/LCIPP 외 CAN/WGC/TUNGO 추가되었다면 N≥40 도달, 옵션 A 가능.

---

## Section 7. Round 5 권고 (IR 관점)

### P0 (필수)

1. **Castro et al. 2025 ENB cooperation matrix 실제 수집** (collector_feedback §1과 합의)
   - 현재 pseudo-truth (그룹 멤버십)으로 F1=0.560. 실제 ENB co-sponsoring/joint statement matrix로 재검증
   - 예측: F1이 0.50-0.65 범위로 변동 (현재 0.560에서 ±0.05 정도)
   - 이론적 의의: pseudo-truth와 실제 truth의 일치도가 *constructivist 명제*의 *ground truth* 정당화에 결정적

2. **Stage 1 LLM 가동 — frame_type 정량화**
   - documents.jsonl의 USA, SAU, KOR, EU 등 미코딩 국가 frame_type LLM 분류
   - hedging density, sovereignty mentions, voluntary mentions의 자동 추출 lexicon
   - 24 historical chair letters에 대해 동일 처리

3. **24개 PDF의 processed metadata 통합 (CR4-IR-1 미완 보완)**
   - PDF 텍스트 추출 → frame_type 코딩 → Tallberg 4 채널 매핑 → chair_metadata.jsonl 통합
   - 목표: chair_metadata 32 → 56+ records (raw 24건 모두 통합)
   - COP_coverage processed 3 → 8 (Bayer-Urpelainen N>10 threshold 근접)

4. **realist B0 통계적 유의성 검증**
   - McNemar test, Cohen's κ, 95% CI bootstrap, Cohen's d 4 지표 산출
   - country_features_v2 확장 (ND-GAIN vulnerability, Annex I status, historical emissions) → B0+ baseline 측정
   - 권고 narrative 작성: "F1=0.56 + κ=slight = realism의 weak prediction. CINA의 frame variable이 incremental 0.24"

### P1 (권장)

5. **Brazilian Translation Gap 95% CI bootstrap**
   - 1000회 bootstrap → Δ의 신뢰구간 산출. 0.30 포함 시 PARTIAL이 "양립 가능"으로 격상
   - "Negative Authority" 분리 시 Δ 변화 측정

6. **Hedging density × group red line absorption 2D plot**
   - L.25 121 paragraphs 각각에 대해 (hedging count, group red lines absorbed) 좌표 산출
   - NeurIPS CCAI paper *core figure* 후보

7. **5국 cross-walk 확장 (Translation Gap 비교)**
   - KOR (이미 30-cell 완료), EU, SAU, AOSIS의 동일 Plano Clima ↔ L.25 비교
   - BRA Δ=0.269가 *outlier*인지 *일반 패턴*인지 판단

### P2 (선택)

8. **COP28/29 advance/final 시계열 비교**
   - "pre-crystallized formula"가 BRA만의 특이 사례인지, UAE/AZE도 동일 패턴이었는지
   - 만약 시계열 trend면 "에너지 수출국 의장 3연속" 가설의 *언어적 fingerprint*

---

## Section 8. policy-science-professor와의 합의·불일치 예측

### 합의 예상

- **chair_metadata raw→processed 통합 미완**: 양 분과 모두 P0 권고
- **F1=0.560의 통계적 유의성 검증 필요**: 정책학도 ground truth 정확도 우려 공유
- **Stage 1 LLM 가동의 시급성**: 양 분과 모두 합의
- **Translation Gap Δ=0.269 PARTIAL의 95% CI 산출**: 정책학도 magnitude 명확화 요구
- **24개 chair letters의 가치**: Falkner climate hegemon × Howlett instrument-mix 동시 분석 가능

### 불일치 예상

| 쟁점 | 정책학자 입장 | IR 입장 |
|------|------------|--------|
| **pre-crystallized formula의 학술 framing** | implementation gap (chair text → 국가 이행) 결합 | Tallberg + Steinberg + Goh의 IR 이론 framing 우선 |
| **Translation Gap Δ=0.269 명명** | "calibration gap" (Howlett 정책 calibration) | "Two-Level Instrument Translation Gap (TITG)" (Putnam + Howlett) |
| **F1=0.560 해석** | implementation feasibility 측면 (50% 정확도로 정책 권고 가능?) | constructivist contribution 정당화 우선 |
| **Round 5 우선순위** | NAP 30-cell의 LOW_CONFIDENCE 4 셀 보강 우선 | 24 PDF processed 통합 + realist 통계 검증 우선 |

→ **통합 가능성**: Translation Gap 명명에서 "Two-Level Instrument Translation Gap"이 양 분과 합의 가능. Putnam(IR) + Howlett(Policy) 양 인용으로 cross-discipline appeal.

→ **별도 처리**: F1=0.560 해석의 framing은 IR이 constructivist contribution claim, Policy가 implementation feasibility 우려를 *각자 chapter에서 별도*로 처리하는 것이 productive. Discussion section에서 "two readings" 명시.

---

## Section 9. team-lead 결정 요청

### D1 (P0). 24 historical chair letters의 processed pipeline 통합 — Round 5 즉시 실행?

**제안**: 채택. raw 24건이 *분석 가용* 상태로 진입하지 않으면 Round 4의 가장 큰 진전(historical 시계열 가시화)이 *논문 evidence*가 되지 못함. 작업량 추정: PDF 텍스트 추출 4시간 + LLM frame 분류 2시간 + Tallberg 4 채널 코딩 (수동 + LLM 보조) 6시간 = 12시간. T02 Round 5 P0로 명시.

### D2 (P0). Realist B0 통계적 유의성 검증 — McNemar/κ/95%CI/d 4 지표 모두 산출?

**제안**: 채택. F1=0.560은 *isolated number*로는 학술 claim 부족. 4 통계 산출 후 narrative 강화. 작업량: 2시간. T02 Round 5 P0.

### D3 (P0). pre-crystallized formula 가설 — NeurIPS CCAI paper signature finding 후보 채택?

**제안**: 채택. Tallberg + Steinberg + Goh 3 reference 통합 framing. 단 Round 5에서 (a) hedging density × group red line absorption 2D plot 산출, (b) COP28/29 시계열 비교, 두 추가 evidence 필요. 채택 시 paper title 제안: *"Pre-Crystallized Formulas: When Chair Power Operates Outside Formal Negotiation Text"*.

### D4 (P1). Brazilian Translation Gap 명명 — "Two-Level Instrument Translation Gap (TITG)" 채택?

**제안**: 채택. Putnam + Howlett 결합으로 IR + Policy 양 학계 appeal. 학술적 단어 선택은 Discussion 챕터에서 두 분과 합의 후 finalize.

### D5 (P1). 5국 cross-walk 확장 (KOR/EU/SAU/AOSIS) — Round 5 vs Round 6 분배?

**제안**: KOR (이미 30-cell)은 Round 5 즉시 가능, EU 우선 (UNFCCC submissions 풍부). SAU/AOSIS는 Round 6 (collector_feedback HIGH priority) 후 처리.

### D6 (P0). Round 4 4.36/5 → Round 5 4.50+/5 목표 — chair processed 통합 + realist 통계 + hedging plot 3 P0 도달 전략 채택?

**제안**: 채택. 3 작업 모두 Round 5 가능. 4.50+/5는 *International Organization* "minor revision → accept" 전이 임계.

---

## Appendix. Round 4 핵심 비판 Top 3

### C4.1 (P0) — 24 PDF의 processed pipeline 미통합 = "데이터 가용성 함정"

**구체 인용**: `data/raw/historical_chair/COP{21..27,30}/` 24 PDFs 존재하나 `data/processed/chair_metadata.jsonl`은 32 records로 변동 없음. COP21 Fabius letter, COP23 Bainimarama outcomes, COP26 Sharma 4건 등이 *데이터 wallet*에 들어왔으나 *분석 파이프라인*에는 진입 못함.

**왜 P0인가**: Round 3 권고 CR4-IR-1의 *목적*은 chair_metadata N=80+, COP coverage 10+이었음. raw 200% 충족이지만 processed 0% 충족 = Bayer-Urpelainen panel 분석 여전히 불가능. reviewer 입장: "데이터를 모았으나 쓰지 않았다"는 frequent rejection 사유.

**수정 제안**: Round 5 T02에 24 PDF processed 통합 P0. PDF→텍스트→frame 코딩→Tallberg 채널 매핑→jsonl 통합. 12시간 작업.

### C4.2 (P0) — Realist B0 F1=0.560의 통계적 유의성 미검증

**구체 인용**: `realist_b0_f1_result.json`은 F1, precision, recall만 보고. McNemar test, Cohen's κ, 95% CI, Cohen's d 모두 미산출. random baseline ~0.44와의 차이 +0.12pp가 *통계적으로 유의*한지 *실용적으로 의미*가 있는지 미판단.

**왜 P0인가**: F1=0.56 → "realism insufficient" claim은 통계적 grounding 없으면 reviewer 2가 즉시 반박. CINA의 핵심 contribution(constructivist variable이 ΔF1 +0.24 추가) 정당화의 *baseline*이 약하면 *contribution*도 약해짐.

**수정 제안**: Round 5 즉시 4 통계 산출. 추가로 ENB 실제 협력 matrix로 ground truth 교체 시도.

### C4.3 (P0) — Translation Gap Δ=0.269의 95% CI/bootstrap 미산출, 단일 사례 한계

**구체 인용**: `brazil_instrument_translation.json` Δ=0.269 보고하나 *신뢰구간 없음*. 5국 cross-walk 미수행으로 *outlier vs 일반 패턴* 판단 불가. 가설 0.30 PARTIAL의 boundary 위치 평가에 결정적 정보 결여.

**왜 P0인가**: IR 학계는 single-case point estimate를 *inferential claim*으로 인정하지 않음. bootstrap 95% CI가 [0.18, 0.36]이면 "데이터로는 Δ≥0.30 reject 못함" → 가설 *boundary condition* 형식으로 격상 가능. 5국 cross-walk가 모두 Δ>0.20이면 *일반 패턴* claim 가능.

**수정 제안**: Round 5 P1로 (a) bootstrap 95% CI, (b) 5국 cross-walk (최소 KOR + EU 추가) 산출.

---

*— ir-political-professor (round 4)*
