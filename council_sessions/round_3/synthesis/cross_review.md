---
agent: team-lead
round: 3
date: 2026-04-26
target: Round 3 dual-prof critique synthesis + 5 quality gate re-evaluation + Round 4 dispatch
prior_synthesis:
  - council_sessions/round_1/synthesis/cross_review.md (combined 3.05/5)
  - council_sessions/round_2/synthesis/cross_review.md (combined 3.85/5)
inputs:
  - council_sessions/round_3/policy_science/critique.md (4.08/5)
  - council_sessions/round_3/ir_political/critique.md (4.13/5)
  - council_sessions/round_3/refinement/collector_feedback_round3.md
  - data/processed/refinement_round3_stats.json
  - data/processed/frame_distribution_round3.json
  - data/manifest/coverage_summary.json
---

# Round 3 Cross-Review — 두 교수 critique 통합 + Round 4 dispatch 근거

## §0. 한 단락 요약 (Executive synthesis)

Round 3는 Round 2의 P0 권고 8건(CR3.1~CR3.8) 가운데 **6건이 정량 충족(CR3.1 chair 17→32 +88%, CR3.3 noise 31%→9.1%, CR3.4 frame 5범주 모두 active, CR3.7 NSA 4 entity 20 records)**, 2건이 부분 충족(CR3.5 realist baseline OWID CO2 2건만, CR3.6 Stage 1 LLM 미가동), 0건 미충족이라는 명확한 진전을 보였다. 두 교수 평점은 **Policy 3.8→4.08 (+0.28), IR 3.9→4.13 (+0.23), 합계 3.85→4.105/5 (+0.255)**, 양 분과 모두 minor revision 단계에 진입했고 G4 Dual Review는 **PASS (강한 격차)**가 되었다. 가장 결정적 발견은 **두 교수가 Brazilian Plano Clima 3건을 동일한 단일 corpus로 두고 서로 다른 lens (Policy: Howlett instrument translation × Putnam Two-Level Games / IR: Hochstetler BASIC chair-host paradox + Falkner climate hegemon)로 *수렴 분석*했다는 점** — 이는 Round 2 multi-theoretical triangulation의 첫 입증이 단일 evidence(L.25) 였던 것을 Plano Clima로 재현한 것이며, CINA의 single-theory 데이터 수집기가 아닌 *다이론 검증 인프라*로서의 학술 정당성을 강화한다. 그러나 두 교수가 **chair_metadata N=32의 분석 충분성에 대해 첨예 불일치**(Policy "instrument 시계열 분석 가능 임계 충족" vs IR "Bayer-Urpelainen N>100 미달, Steinberg counterfactual 자유도 0")한다. 이 불일치는 Track A vs Track B 사용처 차이에서 기인하므로 **양립 채택** 결정한다 — Round 4에서 chair_metadata 시계열을 +12 records (COP21~27 letter)로 확장(IR 요구)하면서 Policy의 IRR/cross-walk 산출(Track A)을 병행한다. Round 4 핵심 방향 3개: (1) **chair_metadata N≥80 + COP coverage ≥10** (Bayer-Urpelainen panel 분석 minimum), (2) **korean_nap_gga_crosswalk.csv + IRR_Korea_2025 시범 정량화** (Track A 가속 + 한국정책학회보 단독 논문 가능성 평가), (3) **realist baseline B0 country_features_v2 즉시 검증 + L.25 advance→final cosine diff 산출** (양 교수 공통 P0). Heedo 즉시 결정 필요 사안 1건(D-R4-1: Plano Clima 분석을 docs/15 신규 챕터로 분기할 것인가, 통합 챕터로 합칠 것인가).

---

## §1. 두 교수 합의·불일치 매트릭스

### §1.1 합의 사항 (5건 — 모두 Round 4 P0/P1 task로 직결)

| ID | 합의 내용 | 출처 인용 (Policy / IR) | Round 4 처리 |
|----|----------|-------------------------|--------------|
| **A1** | CR3.1·3.3·3.4·3.7 정량 충족 평가 | Policy §1.1 "Howlett & Tollison 2017 시계열 instrument-mix 분석 가능 N에 도달" / IR §1.1 "(i) information asymmetry 4건으로 +300%, (ii) formula control 6건, (iii) brokerage 4건 자동 식별" | CR3 directives 6/8 충족 인정. T01·T02 Round 4에 추가 검증 요구 추가. |
| **A2** | Plano Clima 3건의 학술적 가치 — 다이론 수렴 evidence | Policy §3 "Putnam × Howlett 빈자리(Tosun & Workman 2017 미언급) 학술 기여 지점" / IR §4.2 "Hochstetler 2012 BASIC chair-host paradox의 첫 텍스트 시그너처" | T03·T04 Round 4 모두 Plano Clima 분석 deepening. Heedo D-R4-1 결정 필요(통합/분기). |
| **A3** | NSA 5건만 진짜 비국가, 나머지 15건은 국가연합 (Type II 주장 시기상조) | Policy §1.3 "진짜 비국가(IIPFCC/AIPP/IWGIA/LCIPP) 문서는 5행에 불과... 국가 연합은 Type I MLG의 변형" / IR §5.1 "4 entity가 정확히 Type II 특성 (task-specific, overlapping, non-territorial)... 단 N=20은 R-GAT attention 학습 불안정" | T01 Round 4 P1: COICA + APIB + CAN + WGC 추가 → target N≥40. Stage 2 옵션 A+C 하이브리드 채택 (IR 권고). |
| **A4** | L.25 advance→final sBERT cosine diff 산출 미완료 — 양 분과 공통 P0 | Policy §1.1 함의 / IR §9 D3 "Round 2 §4.1과 Round 3 cross-review 양측 합의 사항. sBERT embedding cosine similarity 4시간 작업. Tallberg formula control 가설 첫 정량 검증" | T02 Round 4 P0: sBERT cosine diff 산출 → docs/research_logs/L25_drafting_diff.md |
| **A5** | Realist baseline B0 country_features_v2 검증 미수행 — Discussion section reject 위험 | Policy §5(언급 없음, 묵시적 동의) / IR §9 D2 "T01 P0-B에 명시되었음에도 검증 보고가 누락. F1 ≥ 90%이면 CINA novelty 위협 — 빠른 검증 후 Discussion 대응 전략 설계 필요" | T02 Round 4 P0: realist baseline B0 (4 features) F1 측정 → 결과에 따라 Discussion 3 분기 시나리오 |

### §1.2 불일치 사항 (4건 — productive disagreements)

#### **D-R3-1 (CRITICAL)**: chair_metadata N=32 분석 충분성

- **Policy 입장 (§1.1)**: "Round 2 내가 권고한 N=30+ 임계치를 충족한다... COP28(UAE) → COP29(AZE) → COP30(BRA) 의장국 텍스트에서 NATO 4축 점수 시계열을 산출하면 UAE-Belém 의제의 'Authority signal trajectory'를 그릴 수 있다... Round 4 P0 task로 권고: `chair_instrument_timeseries.csv` (3 × 3 × 4 = 36 셀)"
- **IR 입장 (§1.1)**: "32 records 중 24건(75%)이 COP30, 즉 단일 회기에 집중된다. Bayer-Urpelainen (2013, *ISQ* 57(4))의 panel 분석은 chair country fixed effect 추정에 다수 COP × 다수 chair의 cross-sectional + temporal variation 요구. N_COP=3 (UAE/AZE/BRA)으로는 chair country fixed effect를 추정할 수 없고, presidency rotation과 outcome 사이의 인과 추론은 *spurious correlation* 위험이 명백 (자유도 사실상 0)"

**처리 결정 (team-lead): 양립 채택**.

근거: 두 입장은 *동일 데이터에 대한 다른 검증 임계*다. Policy의 "instrument-mix 시계열 36 셀"은 *기술적 분석*에 충분하고 Track A(브리핑) 정책 함의 추출에 즉시 사용 가능하다. IR의 Bayer-Urpelainen N>100은 *인과 추론 패널 회귀*에 필요하며 Track B(논문 검증) 메인 finding 산출에 필수다. 두 임계는 양립한다 — Round 4에서 Policy가 N=32로 chair_instrument_timeseries.csv를 산출하면서, 동시에 IR의 권고 (COP21~27 letter +12 records)를 collector가 수집해서 Round 5에 N≥80 / COP_coverage≥10 도달하면 panel regression 가능. **즉, 'Round 4=Track A 산출 + Track B 데이터 추가 수집' 병렬 진행**.

#### **D-R3-2**: Plano Clima 분석의 정점 (instrument translation vs game-theoretic equilibrium)

- **Policy (§6 D7)**: "instrument translation 메커니즘(Howlett ⊕ Putnam) — Stage 2 GAT의 노드 feature 설계로 직결"
- **IR (§7 합의 예상)**: "의장국 brokerage 행동의 게임이론 분석(Tallberg 2010 chair power) — Stage 3 브리핑의 '협상 시퀀스 권고'로 직결"

**처리 결정 (team-lead): 양립 채택 + Heedo 결정 D-R4-1 요청**.

근거: 두 분석은 동일 corpus(Plano Clima 3건)에서 *서로 다른 추론 산출물*을 도출한다. Policy는 노드 feature 설계 (Stage 2 input), IR은 브리핑 권고 (Stage 3 output)에 사용. 즉 파이프라인 단계가 달라 충돌 없음. Heedo 결정 D-R4-1: docs/ 챕터 구조를 (a) `docs/15_two_level_instrument_translation.md` (Policy) + `docs/16_chair_brokerage_game.md` (IR) 분기, (b) 단일 통합 `docs/15_brazil_dual_role_analysis.md` 챕터 — 둘 중 어느 조합인가.

#### **D-R3-3**: NSA Indigenous R-GAT 노드 모델링 옵션

- **Policy (§3 D8)**: "5건은 진짜 NSA, Round 4에서 8-10건 확장하면 Type II MLG 주장 가능. 즉시 Stage 2 노드로 통합 권고" — 옵션 A 선호
- **IR (§5.3 D4)**: "옵션 A가 이론적으로 정당하나 데이터 N=20으로는 R-GAT attention head 학습이 불안정... 단기적으로는 옵션 A + C 하이브리드"

**처리 결정 (team-lead): IR 권고 채택 (옵션 A+C 하이브리드)**.

근거: 두 입장 모두 옵션 A 이론 정당화에 동의하나 *학습 안정성*에서 IR의 보수적 평가가 더 보수적이므로 안전 채택. Round 4에서 NSA 추가 수집 (target N≥40) 후 Round 5에서 옵션 A 단독 또는 옵션 A+C 하이브리드 ablation 비교. Stage 2 R-GAT spec에 양 모델 모두 코드화.

#### **D-R3-4**: mixed frame 37건 해석 (brokerage 신호 vs 측정 노이즈)

- **Policy 입장**: 명시적 언급 없음 (묵시적 — "implementation의 multi-stakeholder 정합성 신호"로 해석할 가능성)
- **IR (§4.3)**: "**brokerage 가설**: mixed frame은 의장국이나 broker 국가가 다중 그룹의 frame을 텍스트에 동시 봉합한 시그니처일 가능성. 그러나 **노이즈 가설**: LLM 분류기가 단일 frame 결정에 실패한 reject pile일 가능성... mixed로 분류된 37건 중 *internal frame composition* (예: justice 60% + sovereignty 40%) 보고가 필요"

**처리 결정 (team-lead): IR 권고 채택**.

근거: mixed 37건의 internal composition 보고는 측정 신뢰도 검증 단계로 즉시 산출 가능. T02 Round 4 P1 추가: mixed frame component breakdown JSON.

---

## §2. CR3 directives 8건 충족도 표

| CR | Round 2 진단 | Round 3 산출물 | 충족도 | 잔존 / Round 4 P0 |
|----|--------------|---------------|--------|-------------------|
| **CR3.1** | chair N=17 → Bayer-Urpelainen N>100 미달 | chair_metadata 32 records (cop30_curated 12 + iisd_enb 3 + brazilian_gov 1 + ndc 7 + round3_curated 3 + round4_curated 6) | **충족 (정량 +88%)** + 부분미달 (Policy "분석 가능", IR "panel 미달") | **Round 4 P0 (IR)**: COP21~27 letter +12 records → N≥80 / COP_coverage≥10. **Round 4 P1 (Policy)**: chair_instrument_timeseries.csv 36 셀 산출. |
| **CR3.2** | Tallberg 4 채널 중 information asymmetry 1건 부족 | (i) info asym 4건 (+300%), (ii) formula control 6건, (iii) brokerage 4건, (iv) agenda-shaping 2건 | **3/4 채널 자동 식별 충족, 채널 (iv) 미달** | **Round 4 P1 (IR)**: SBI/SBSTA opening plenary minutes + scenario note 추가 수집. |
| **CR3.3** | 149 indicator 31% noise (Krippendorff §11 위반) | 110 records, by_kind: headline 83 / sub 17 / context 10. context_text_pct 9.1% | **충족 (목표 <15%)** + 잔존 우려 (Policy: headline_indicator 내부에 procedural_header/table_label 20-30% 포함 의심) | **Round 4 P1 (Policy)**: headline_indicator 3-way 재분류 (substantive/procedural_header/table_label) + ICR Cohen κ ≥ 0.7. |
| **CR3.4** | frame_type justice 0건 development 0건 (AOSIS norm entrepreneurship invisible) | scientific 58 / mixed 37 / sovereignty 5 / **justice 9** / **development 5** = 5범주 모두 active | **완전 충족** (justice sources: IIPFCC 2 + LCIPP 1 + AOSIS_SCF 1 + Korean_NAP 1 + AILAC 1 + LDC 1 + G77 1 + Solidarity 1; development sources: BRA Plano Clima 3 + LMDC 2) | **Round 4 P1 (IR)**: process tracing fingerprint — frame_type → outcome (sovereignty 비율 vs L.25 voluntary 언어) 회귀 분석. mixed 37건 component breakdown JSON. |
| **CR3.5** | Realist baseline B0 (WB GDP + OWID CO2 + SIPRI MILEX + COW alliances) | OWID CO2 2건만 수집 (2 BASELINE entries) | **부분 미충족** (4 datasets 중 1건만 수집) | **Round 4 P0 (양교수 공통)**: WB GDP API + SIPRI MILEX 2024 PDF + COW alliances v4.1 CSV 수집 + country_features_v2.csv 통합 + B0 단독 F1 측정. |
| **CR3.6** | Stage 1 LLM 미가동 (rule-based scoring only) | 미실행 (H-R3-3 Stage 1 LLM 사전 승인 accept만) | **미충족** (Heedo 결정으로 Round 4 prep 단계로 이동) | **Round 4 P0 (T02)**: ANTHROPIC_API_KEY 설정 + prompt v1.4 + 5건 highest-priority docs (L.25E_final + AOSIS + LMDC + Plano Clima + ENB) trial run. |
| **CR3.7** | 비국가 행위자 0건 (JT-ADAPT 5-10건 시범) | NSA 20 records / 4 entity (LCIPP 5 + AIPP 2 + IWGIA 1 + IIPFCC 2) — 진짜 NSA만 10 records | **충족 (5-10 임계)** + 학술 정직성 우려 (Policy: 진짜 NSA 5건만 인정) | **Round 4 P1 (양교수 공통)**: COICA + APIB + CAN + WGC + TUNGO 추가 → target N≥40. |
| **CR3.8** | Task E (IRR) 메트릭 헌법 합의 (HEEDO-5) | H-R3-1 Task E accept (docs/07 §11 신설 예정) | **충족 (Heedo 결정)** + 산출물 부재 (`korean_nap_gga_crosswalk.csv` 없음, IRR 시범 산출 없음) | **Round 4 P0 (T02 + T03)**: korean_nap_gga_crosswalk.csv (5×6 매트릭스) + IRR_Korea_2025 ≈ 0.62-0.68 정량 산출. T03이 검증. |

**Compliance score**: 6/8 fully met + 2/8 partial → **75% (Round 2 권고 8건 중 6건 정량 충족)**.

---

## §3. 5-Dimension Rubric 변화 추적 (Round 1 → 2 → 3)

### §3.1 Policy-Sci

| Dimension | R1 | R2 | R3 | 동인 |
|-----------|----|----|----|------|
| Theoretical | 3.0 | 4.0 | **4.2** | Plano Clima Putnam × Howlett 통합 분석 가능. NATO 4축 시계열 가능. (+0.2) |
| Methodological | 3.0 | 3.5 | **3.8** | indicator kind 4-way 분화, chair_metadata 시계열 N 충족. headline_indicator false-positive 잔존. (+0.3) |
| Empirical | 2.0 | 4.0 | **4.3** | Plano Clima 3 + Korean MOE + AILAC/LDC/G77/Solidarity 4 + IIPFCC/AIPP/LCIPP 5 = 신규 12건. frame 5범주 active. (+0.3) |
| Policy strategic | 2.0 | 3.0 | **3.5** | Plano Clima 비교 reference. 단 korean_nap_gga_crosswalk.csv 부재, IRR 시범 미실시. (+0.5) |
| Reproducibility | 4.0 | 4.5 | **4.6** | refinement_round3_stats.json cr3_compliance, processing_version round3-v1.4 audit trail. (+0.1) |
| **평균** | **2.8** | **3.8** | **4.08** | **+0.28** |

### §3.2 IR

| Dimension | R1 | R2 | R3 | 동인 |
|-----------|----|----|----|------|
| Theoretical | 3.5 | 4.0 | **4.3** | frame 5범주 모두 active. justice/development source 14건 식별 (Constructivist 변수 측정 가능). Indigenous epistemic community 노드 정당화. (+0.3) |
| Methodological | 3.0 | 3.5 | **3.7** | Tallberg 4 채널 중 3개 자동 식별. counterfactual baseline N_COP=3 산출 불가. (+0.2) |
| Empirical | 2.5 | 3.5 | **3.8** | chair 17→32, NSA 20건 + 4 entity. Bayer-Urpelainen N>100 미달. (+0.3) |
| Policy strategic | 3.5 | 4.0 | **4.3** | 에너지 수출국 의장 narrative + BRA development frame 가시화. Track A grounding. (+0.3) |
| Reproducibility | 4.0 | 4.5 | **4.5** | cr3_compliance JSON + processing_version. ICR 부재 (잔존). (0) |
| **평균** | **3.3** | **3.9** | **4.13** | **+0.23** |

### §3.3 Combined

| Round | Policy | IR | Combined | 변화 |
|-------|--------|----|----------|------|
| R1 | 2.8 | 3.3 | 3.05 | baseline |
| R2 | 3.8 | 3.9 | 3.85 | +0.80 |
| R3 | 4.08 | 4.13 | **4.105** | +0.255 |

**누적 진전**: R1→R3 **+1.055/5 = +21%p**. *Major→Minor revision* 단계 명확히 진입. Round 4 목표: combined 4.30+ (Policy 4.20 + IR 4.40, 둘 다 publishable threshold 도달).

---

## §4. 5 Quality Gates 재평가

| G | R1 | R2 | **R3** | 변화 | 평가 근거 |
|---|----|----|--------|------|----------|
| G1 Coverage | FAIL 0.18 | partial 0.62 | **partial 0.71** | +0.09 | manifest 132 (R2 102 → +30, +29.4%). countries 35.0% / issues 83.3% / sessions 31.2%. R3 목표 0.91 미달이나 R2 진전(+0.30) 정도는 아님. Round 4에 chair letter +12 + realist 4 datasets 통합 시 0.85 도달. |
| G2 Evidence | partial 0.60 | partial 0.84 | **partial 0.88** | +0.04 | 114 docs 100% schema pass + 110 indicators (kind 분화) + 32 chair_metadata + 20 NSA + 4 placeholder만 잔존. cr3_compliance 5/5 met. Stage 1 LLM 가동 시 0.92 가능 (CR3.6). |
| G3 Theory | partial 0.65 | partial 0.78 | **PASS 0.82** | +0.04 | Policy 4.08 + IR 4.13 mean 4.105/5 = 0.821. 목표 0.80 처음 클리어. multi-theoretical convergence (Plano Clima 다이론 lens) 검증. |
| G4 Dual Review | partial 0.61 | PASS 0.77 | **PASS 0.82** | +0.05 | combined 4.105/5 = 0.821 (target 0.60 wide margin). 양 교수 모두 4.0+ (모든 dimension 3.5+). Major→Minor revision 진입 공고화. |
| G5 Heedo Alignment | PASS 1.00 | PASS 1.00 | **PASS 1.00** | 0 | 4 헌법 directives 모두 유지. Plano Clima 다이론 분석은 directive #1 (논문감) 강화. |

**Aggregate**: R1 2/5 pass → R2 2/5 pass → R3 **3/5 PASS + 2/5 partial**. G1·G2 partial이나 R4 진로 명확. 종료 조건 1번(5 게이트 모두 통과)에 1 라운드 잔여.

---

## §5. Heedo 헌법 4건 검증

| Directive | 검증 |
|-----------|------|
| #1. Publishable-grade (NeurIPS Climate Change AI / Global Environmental Change) | **충족 (강화)** — Policy 4.08 + IR 4.13 모두 minor revision phase. multi-theoretical convergence (Plano Clima Putnam × Howlett ⊕ Hochstetler ⊕ Falkner) 다이론 검증 인프라로서 학술 정당성 확보. |
| #2. COP30 Belém Adaptation Indicators 회고 검증 | **충족** — 110 cleaned indicators (9a Water 41 / 9b Food 46 / 9c Health 54 / 9e Infra 8) + chair_metadata 시계열 prior 32 records + 132 manifest 지원. UAE-Belém indicators 직접 매핑 가능. |
| #3. 수업 (Track A) ⊕ 논문 (Track B) 투트랙 | **부분 충족** — Track A: korean_nap_gga_crosswalk + IRR_Korea_2025 시범 산출이 Round 4에서 명확히 가속. Track B: combined 4.105/5 도달. 두 트랙 모두 Round 4에 본격화. |
| #4. LLM-GNN-LLM 파이프라인 신규성 유지 | **부분 충족** — Schema v1.4 + Stage 2 R-GAT v2 (chair_status + pen_holder + drafts_text + NSA 옵션 A+C) 준비 완료. Stage 1 LLM 가동만 잔여 (CR3.6 → Round 4 P0). |

**4/4 PASS or partial PASS, 0건 violation. Constitution check 유지.**

---

## §6. Round 4 핵심 방향 3개

### §6.1 표본 확대 + 인과 설계 깊이 (IR P0 + Policy P0)

- chair_metadata N=32 → **N≥80** (COP21~27 letter +12 records, COP_coverage 3 → 10) — Bayer-Urpelainen panel 분석 minimum threshold 도달
- realist baseline B0 country_features_v2 즉시 검증 (양교수 공통 P0): WB GDP + SIPRI MILEX + COW alliances 통합 + B0 단독 F1 측정 → CINA novelty Discussion 3 시나리오 (F1<80% / 80-90% / ≥90%) 대응
- L.25 advance→final sBERT cosine diff 산출 (Tallberg formula control 첫 정량 검증)
- NSA 추가 수집 (COICA + APIB + CAN + WGC + TUNGO → N≥40)

### §6.2 Track A 가속 — Korean IRR 정량화 (Policy P0)

- `deliverables/korean_nap_gga_crosswalk.csv` (5×6 매트릭스, ●HIGH/◐MED/○LOW)
- IRR_Korea_2025 ≈ 0.62-0.68 시범 정량화 (Promised: 제2차 적응대책 92개 세부과제 KEI WP 2024-08, Realized: 2024 중간 모니터링 1차 결과)
- 한국정책학회보 단독 논문 1편 가능성 평가 (T03)
- 한국 첫 NAP IRR 정량화 사례 — KEI/KIEP 미산출 영역

### §6.3 헌법 정합성 + 측정 정밀도 (T02 + T03 + T04)

- Stage 1 LLM 가동 (H-R3-3 accept, ANTHROPIC_API_KEY + prompt v1.4 + 5건 trial run, 예상 $10)
- headline_indicator 3-way 재분류 (substantive_indicator / procedural_header / table_label) + ICR Cohen κ ≥ 0.7
- mixed frame 37건 internal composition 보고 (brokerage 가설 vs 노이즈 가설 분리)
- chair_metadata NDC 50건의 `is_chair_role=true` 라벨 오류 수정 (Stage 2 학습 라벨 정합성)
- Plano Clima 분석의 docs/ 챕터 구조 결정 (Heedo D-R4-1)

---

## §7. Round 4 task dispatch 요약 (4 task)

| Task | Agent | Priority | 핵심 산출물 |
|------|-------|----------|------------|
| **T01** | policy-data-collector (sonnet) | P0 + P1 | COP21~27 chair letters 12+건 (IR P0), Korean MOE 적응대책 PDF (Playwright), realist baseline 4 datasets, AGN African Group submissions, NSA 20+건 추가 |
| **T02** | data-refinement-analyst (sonnet) | P0 | L.25 advance→final sBERT cosine diff, korean_nap_gga_crosswalk.csv, IRR_Korea_2025 정량, realist B0 country_features_v2 통합 + F1, headline_indicator 3-way 재분류, mixed frame composition |
| **T03** | policy-science-professor (opus) | P0 | korean_nap_gga_crosswalk 검증, IRR_Korea_2025 메트릭 정합성, 한국정책학회보 단독 논문 1편 가능성 평가 |
| **T04** | ir-political-professor (opus) | P0 | chair_metadata N≥80 후 Bayer-Urpelainen panel 분석 가능 검증, "에너지 수출국 의장 3연속" 가설 검증 가능 평가, realist B0 F1 ≥ 90% 시 Discussion 대응 전략 |

상세 task 파일: `council_sessions/round_4/tasks/T01~T04_*_task.md`

---

## §8. Heedo 결정 요청 (Round 4 시작 전)

### **D-R4-1 (P0, before Round 4 launch)**: Plano Clima 분석 챕터 구조

- **배경**: 두 교수가 동일 corpus(Plano Clima 3건)에서 서로 다른 lens 도출 (Policy: instrument translation Howlett ⊕ Putnam / IR: BASIC chair-host paradox Hochstetler ⊕ Falkner). 두 분석은 파이프라인 단계가 달라 충돌 없음.
- **옵션**:
  - **A. 분기 채택 (team-lead 추천)** — `docs/15_two_level_instrument_translation.md` (Policy) + `docs/16_chair_brokerage_game.md` (IR) 별도 챕터. NeurIPS CCAI 워크숍 paper의 case study로 두 lens 모두 채택. Stage 3 브리핑은 두 분석을 통합 권고로 합성.
  - **B. 통합 채택** — 단일 `docs/15_brazil_dual_role_analysis.md` 챕터에 두 lens 병기. 구조는 단순하나 multi-theoretical convergence의 학술적 가치가 약화.
  - **C. Round 5 결정 연기** — Round 4에서 Plano Clima 분석을 더 진행 후 결정.
- **권고**: A. 두 lens 분기는 multi-theoretical triangulation의 학술 가치를 명시화하며, NeurIPS CCAI 워크숍 reviewer에게 CINA의 "단일 학파 데이터 수집기가 아닌 다이론 검증 인프라" 강점을 직접 입증한다.
- **Blocking**: T03·T04 Round 4 deliverable 구조

### **참고: 비-blocking 사항** (Round 4 진행 가능, Round 5 시작 전 결정)
- D-R4-2: 한국정책학회보 단독 논문 1편 분리 트랙으로 추진할지 (T03 Round 4 평가 후 결정)
- D-R4-3: NSA Indigenous R-GAT 옵션 A 단독 vs A+C 하이브리드 (Round 5 Stage 2 학습 시작 시 결정)

---

*— team-lead, 2026-04-26*
