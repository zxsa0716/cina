---
agent: ir-political-professor
round: 3
date: 2026-04-25
review_tone: International Organization / ISQ / GEP reviewer (revise-not-reject)
target_documents:
  - council_sessions/round_3/refinement/professor_input/ir_pack_round3.md
  - data/processed/chair_metadata.jsonl (32 records)
  - data/processed/frame_distribution_round3.json (5 frames active)
  - data/processed/non_state_actor_signals.jsonl (20 records, 4 entities)
  - data/processed/refinement_round3_stats.json
  - council_sessions/round_2/ir_political/critique.md (Round 2 anchor)
processing_version: round3-v1.4
---

# Round 3 — IR / Political Science Critique

## 총평 (Top-line Assessment)

Round 2의 P0 권고 3건 가운데 **CR3.4 (frame 5범주 활성화)는 완전 충족** — justice 9건 / development 5건이 새로 식별되었고, AOSIS·IIPFCC·AILAC가 명시적 norm entrepreneur 노드로 부상했다. 이는 Round 2가 "AOSIS·LDC가 invisible"이라 진단한 *Constructivist 변수의 측정 실패*를 정성적으로 해소한 진전이다 (Finnemore-Sikkink 1998 기준 "norm emergence" stage 측정 가능). 그러나 **CR3.1 (chair_metadata N≥150)은 32건으로 미달**이며, 더 심각하게는 32건 중 **24건이 COP30 단일 회기에 집중**되고 historical chair letter는 COP28 UAE / COP29 AZE / COP30 BRA 단 3건뿐이다. Bayer & Urpelainen(2013, *ISQ* 57)의 large-N chair effect 검증 기준선(N>100, ≥10 COP)에 비추면 여전히 *case study* 수준이다. 핵심적으로, **"에너지 수출국 의장 3연속" 가설은 시계열 데이터로 처음 가시화되었으나 N=3으로는 가설 *생성*은 가능해도 가설 *검증*은 불가능**하다. Reviewer 2 입장에서 보면 (i) chair 시계열 N의 양적 부족, (ii) frame_type이 *causal mechanism*이 아니라 *descriptive label*로 머물 위험, (iii) realist baseline B0 데이터가 task에 명시되었으나 실제 country_features_v2에서 검증되지 않은 점이 *International Organization* major→minor revision 전환의 잔여 장애물이다. 그럼에도 Round 3는 "epistemic-political tension" 가설(이태동 2024)을 정량 검증할 수 있는 minimal viable corpus를 처음 구성했다는 점에서 R&R 진입을 공고히 했다.

---

## Section 1. Round 2 권고 검증 — CR3.1 + CR3.4 응답 평가

### 1.1 CR3.1 (chair_metadata N≥150) — **부분 미달, 그러나 시계열 prior 형성**

`chair_metadata.jsonl`은 17 → **32**로 88% 증가했으나 Round 2 §1.3이 명시한 minimum viable size N≥50 / target N≥150에 모두 미달이다. 분포를 정밀 분해하면:

| 출처 | N | COP 분포 |
|------|---|----------|
| cop30_curated | 12 | COP21 1, COP26 1, COP28 0, COP29 1, COP30 9 |
| iisd_enb | 3 | COP22 1, COP28 2 |
| brazilian_gov | 1 | COP28 1 |
| ndc | 7 | COP28 5, COP30 2 |
| round3_curated | 3 | COP30 3 |
| round4_curated (신규) | 6 | COP28 1 (UAE letter), COP29 1 (AZE letter), COP30 4 (BRA letter + GGA drafts) |

**진단**: 32건 중 24건(75%)이 COP30, 즉 단일 회기에 집중된다. 시계열 prior(Tallberg 2010 chairman power 채널의 cross-COP variation 검증)는 사실상 **3 records (UAE/AZE/BRA presidency letter)**에 의존한다. 이는 다음 두 가지 상반된 해석을 가능케 한다:

- **긍정적 해석**: Round 2 §6 P0-2에 명시된 "COP29 Baku presidency letter (Yalçın Rafiyev), COP30 incoming presidency letter (André Corrêa do Lago) 수집 필수"는 충족되었다. Tallberg 4 채널 가운데 (i) **information asymmetry**는 historical chair letter 3건이 secretariat note + presidency vision + agenda guidance를 포함하므로, COP30 단일 INF note 1건만 존재했던 Round 2 대비 가시성이 3배 증가했다.
- **부정적 해석**: Bayer & Urpelainen (2013, *ISQ* 57(4))의 panel data 분석은 chair 효과 식별에 단일 COP의 multiple records가 아니라 **다수 COP × 다수 chair**의 cross-sectional + temporal variation을 요구한다. N_COP=3 (UAE/AZE/BRA)으로는 chair country fixed effect를 추정할 수 없고, presidency rotation과 outcome 사이의 인과 추론은 *spurious correlation* 위험이 명백하다 (자유도 사실상 0).

**Tallberg 4 채널 자동 매핑 가능성**:

| 채널 | Round 2 (N=17) | Round 3 (N=32) | 변화 |
|------|----------------|----------------|------|
| (i) Information asymmetry | 1건 (COP30 INF) | **4건** (COP30 INF + UAE/AZE/BRA presidency letter) | **+300%** |
| (ii) Process / formula control | 4건 | **6건** (GGA drafts 2건 추가) | +50% |
| (iii) Brokerage (co_facilitator) | 3건 | **4건** (GGA draft 3 co-facilitator 추가) | +33% |
| (iv) Agenda-shaping | 2건 | **2건** (Mutirao decisions만) | 0% |

결론: 채널 (i)·(ii)·(iii)는 Round 3에서 자동 식별 가능 수준에 처음 도달했으나, (iv) **agenda-shaping**은 추가 데이터(SBI/SBSTA opening plenary, in-session scenario notes) 없이는 측정 불가다. 이는 *causal mechanism evidence*로서 Tallberg(2010) 4 채널을 fully measure하려는 야심에는 1/4가 미달함을 뜻한다.

### 1.2 CR3.4 (frame 5범주 활성화) — **완전 충족, 다만 인과 추론에는 유의수준 미달**

`frame_distribution_round3.json`이 보고하는 분포 — scientific 58 / mixed 37 / sovereignty 5 / justice 9 / development 5 — 는 5범주 모두 nonzero라는 **Round 2 P0-2의 요건을 충족**한다. Frame source 추적이 가장 인상적이다:

- **justice 9건**: AOSIS_SCF, IIPFCC_TK / SBM014, LCIPP_COP30, AILAC GST(COP27), Korean NAP — Indigenous + SIDS + LDC + AILAC 동시 포착. 이는 Allan(2019, *GEP* 19(1))이 "1.5 to stay alive"를 norm emergence archetype으로 지목한 prediction을 **다중 entity로 확장** 검증할 수 있는 prior다.
- **development 5건**: BRA Plano Clima 3건 + LMDC GGA + LMDC DEA — Brazil이 host로서 development frame을 채택하는 동시에 LMDC가 sovereignty가 아닌 development frame으로 분류된다. 이는 Hochstetler (2012, *Latin American Politics & Society* 54(4)) "BASIC chair-host paradox"의 **첫 텍스트 시그너처**이다.

**그러나 인과 추론에는 부족**: justice 9건 / development 5건의 effect size 산출은 통계적으로 불안정하다. Cohen's d 산출 시 분모가 되는 표본 표준편차가 N=5에서 매우 노이즈에 민감하며, χ² test의 expected count는 일부 셀에서 5 미만이 되어 Fisher's exact test로 회피해야 한다. **AOSIS frame_type=justice 또는 mixed(justice 우세) ≥ 60%** 라는 T04 task §2 검증 기준은, AOSIS 5건 중 justice 4건 + mixed 1건 = 80%로 **수치상 충족**되나 N=5라는 자유도가 reviewer에게 *anecdotal* 비판을 부른다. **Round 4 권고**: justice 5+5+5(IIPFCC/AOSIS/LDC), development 5+5(LMDC/BASIC) 추가 수집 후 χ² 또는 Fisher's exact로 검증.

### 1.3 Tallberg 4 채널 매핑 자동화

**자동화 가능 (Round 3 시점)**:
- (ii) formula control: `procedural_phrases` regex matching ("Draft decision -/CMA.")로 95% precision 달성 추정
- (iii) brokerage: `is_co_facilitator=True` boolean으로 100% recall

**자동화 어려움 (Round 4 필요)**:
- (i) information asymmetry: `doc_kind=presidency_letter OR cop30_curated INF series`로 결합 식별 가능, 단 secretariat scenario note 별도 수집 필요
- (iv) agenda-shaping: "proposed under agenda item N(c)" 패턴 외에 in-session pre-sessional scenario note 필요. Round 4 SBI/SBSTA opening plenary minutes 추가 수집 권고.

---

## Section 2. 5-Dimension Rubric 재평가

| Dimension | Round 1 | Round 2 | **Round 3** | 변화 동인 |
|-----------|--------:|--------:|--------:|---------|
| Theoretical grounding | 3.5 | 4.0 | **4.3** | frame 5범주 모두 nonzero (+0.3). justice/development source 9+5건이 Constructivist 변수를 측정 가능 수준으로 끌어올림. Finnemore-Sikkink norm emergence 단계 매핑 가능. |
| Methodological rigor | 3.0 | 3.5 | **3.7** | Tallberg 4 채널 중 3개 자동 식별 (+0.2). 그러나 counterfactual baseline (비-BASIC vs BASIC chair)이 N_COP=3으로 산출 불가 — 0.5 진전이 아니라 0.2에 그침. |
| Empirical validity | 2.5 | 3.5 | **3.8** | chair_metadata 17 → 32 (+0.2). non_state_actor signals 20건 + 4 entities 신규 (+0.1). 단 N=32가 Bayer-Urpelainen 2013 N>100 기준 미달이라 0.5 진전 아닌 0.3. |
| Policy strategic relevance | 3.5 | 4.0 | **4.3** | "에너지 수출국 의장 3연속" 가설이 정책적으로 high-impact narrative. development frame이 BRA presidency에 부착됨으로써 host-country dual-role 분석이 정책 함의 강화. |
| Clarity & reproducibility | 4.0 | 4.5 | **4.5** | processing_version round3-v1.4 + cr3_compliance JSON로 audit trail 완비. ICR(inter-coder reliability)이 여전히 부재 (0 진전). |

**평균: 3.3 → 3.9 → 4.13/5** (목표 4.3 대비 -0.17). Round 4에서 (a) chair 시계열 COP21/26/27 letter 추가, (b) realist baseline B0 country_features_v2 검증 통과, (c) ICR 코더 2인 실시 시 평균 4.4 도달 가능.

---

## Section 3. "에너지 수출국 의장 3연속" 가설 검증

data-refinement-analyst가 ir_pack §1 말미에 제기한 핵심 질문: **COP28(UAE) → COP29(AZE) → COP30(BRA)의 연속 3개 의장국이 모두 에너지 수출국(UAE, AZE) 또는 자원 보유국(BRA)이라는 사실이 GGA의 voluntary + soft-law 귀결에 구조적 영향을 주었는가?**

### 3.1 IR 이론 framing의 4가지 옵션

| 이론 | 가설 | CINA 측정 변수 | Round 3 데이터로 검증 가능? |
|------|-----|----------------|---------------------------|
| **Sebenius (1983) negotiation arithmetic** | 산유국 의장은 "fossil fuel veto coalition"의 가용성을 협상 산출에 prior로 주입; Pareto frontier가 산유국 ideal point 쪽으로 이동 | UAE/AZE letter의 mitigation:adaptation 비율 vs BRA letter의 동일 비율 | **부분적**. 텍스트 ratio 산출은 가능, 단 N_chair=3으로 Sebenius "BATNA shifting" 검증 불충분 |
| **Steinberg (2002, *IO* 56) presidency as agenda-setter** | 의장의 procedural authority가 outcome distribution을 비대칭적으로 shift; 의장 국익이 outcome에 *systematic bias*로 반영 | chair_metadata.is_pen_holder=True의 frame_type 분포 vs party_submission frame 분포의 KS-test | **불가**. counterfactual로 비-BASIC/비-산유국 의장 (UK COP26, EGY COP27, GER COP23)의 동일 기간 letter 필요. Round 4 필수. |
| **Hochstetler (2012, *LAPS* 54(4)) BASIC chair-host paradox** | BASIC 의장은 sovereignty 언어를 강화하면서도 mediator 정당성을 동시 주장; dual-role tension 측정 가능 | BRA presidency letter의 development frame + L.25 결정문 sovereignty frame 동시 코딩 | **가능 (Round 3 가시화)**. development 5건 가운데 BRA 3건이 직접 evidence. |
| **Falkner (2016, *Int'l Affairs* 92(5)) climate hegemon thesis** | 의장국의 *energy/resource portfolio*가 regime의 mitigation ambition ceiling을 결정; agenda-setting이 단순 절차적이 아니라 구조적 | UAE/AZE letter의 "fossil fuel" 언어 명시 빈도 vs BRA letter의 "Amazon protection" 동시 담론 | **부분적**. 텍스트 N=3이라 ceiling 가설 검증은 Glasgow→Sharm el Sheikh→Dubai→Baku→Belém 5 COP letter panel 필요. |

### 3.2 N_chair=3에서 무엇이 가능하고 무엇이 불가능한가

**가능 (가설 *생성*)**:
1. UAE letter "energy transition" + AZE letter "Finance COP" + BRA letter "adaptation as heart" → **의제 회전 (agenda rotation)** 패턴이 host country interest와 정합한다는 정성 가설.
2. 3 letter 모두 "[shall][should]" 미해결 브라켓을 보존하는 텍스트 전략을 보임 — Allan(2019) incrementalism 관찰의 chair-letter level 확인.

**불가능 (가설 *검증*)**:
1. presidency rotation effect를 시계열 panel regression으로 추정 — 자유도 부족.
2. "에너지 수출국 vs 비-수출국" t-test 또는 Cohen's d — N_treatment=2 (UAE+AZE), N_control=0 (없음). 비-산유국 의장 baseline 부재.
3. Steinberg (2002) "agenda-setter shift" hypothesis 검증 — outcome shift 측정에 필요한 pre-presidency expected outcome (counterfactual) 부재.

### 3.3 권고 — chair_metadata 시계열 확장 우선순위

Round 4에서 다음 12 records 우선 수집 시 가설 *검증* 단계로 전이 가능:
- COP21 Fabius (FRA, EU/Umbrella, 비-산유국) opening + closing letter 2건
- COP22 Trabelsi (MAR, Africa, 비-주요 산유국) 1건
- COP23 Bainimarama (FJI, AOSIS, 비-산유국) presidency letter 2건
- COP24 Kurtyka (POL, EU but coal exporter — 흥미로운 hedge case) 2건
- COP25 Carolina Schmidt (CHL, AILAC, 비-산유국) 1건
- COP26 Sharma (UK, EU/Umbrella, 비-산유국) 2건
- COP27 Shoukry (EGY, Africa, gas exporter — 또 다른 산유국 case) 2건

총 12 records 추가 시 **N_chair=15, COP coverage=9**로 확장. Bayer-Urpelainen (2013) panel 분석의 minimal threshold (N>10 COP)에 처음 도달.

---

## Section 4. frame_type 5범주 활성화 후 norm entrepreneurship 분석

### 4.1 justice 9건의 IR 함의 — Indigenous epistemic community의 부상

justice frame source 9건 중 **6건이 Indigenous 관련**(IIPFCC 2건, LCIPP 1건, AIPP/IWGIA joint 1건, AOSIS-LCIPP joint 2건)이다. 이는 Round 2가 미식별한 핵심 행위자 클래스 — **Indigenous epistemic community** — 가 처음으로 측정 가능 노드가 되었음을 뜻한다. Haas (1992, *IO* 46(1))의 epistemic community 이론은 본래 *과학자 네트워크*에 한정되었으나, Witter et al. (2015) 및 Comberti et al. (2019) 후속 연구는 Indigenous knowledge holder가 climate adaptation 영역에서 "전통생태지식 (Traditional Ecological Knowledge, TEK)" 기반의 별도 epistemic community를 형성한다고 주장한다. CINA의 justice frame이 IIPFCC SBM014 ("Parties should... respect, promote, and consider their respective obligations on human rights... the rights of indigenous peoples")를 포착한 것은 이 후속 이론의 *operationalization*이다.

**합의 결과 형성 메커니즘 가설**: AOSIS-LCIPP joint submission (round3 a5df, 407c, 0cf9 등 다중)은 단일 entity가 아닌 **AOSIS × Indigenous 연합** 노드로 해석되어야 한다. 이는 Allan & Hadden (2017, *Environmental Politics* 26(4))의 "transnational coalition" 개념의 직접 적용 사례로, COP30 GGA 결정문에서 토착민 권리 명시 (preamble paragraph 인용)가 이 연합의 norm entrepreneurship 산물이라는 가설을 정량 검증할 수 있다.

### 4.2 development 5건의 IR 함의 — sovereignty와의 결합/분리

development frame 5건의 source 분포:
- BRA Plano Clima 3건 (host country)
- LMDC GGA + LMDC DEA 2건

**핵심 관찰**: LMDC가 sovereignty가 아닌 development frame으로 분류된 것은 Round 2의 "LMDC sovereignty 우세" 가정에 대한 **부분적 반증**이다. 이는 두 가지 해석을 허용한다:
1. **방법론적 해석**: justice/development keyword expansion (Round 2 §3 권고 §C2.2-2)이 너무 inclusive하여 LMDC의 sovereignty 언어가 development로 흡수되었을 가능성. → ICR 검증 필수.
2. **실질적 해석**: LMDC의 협상 수사가 2024-25 시점에서 sovereignty (Westphalian) → development (Bandung-style right to development) 로 *strategic reframing* 했을 가능성. 이는 Roberts & Parks (2007) "climate of injustice"의 development-as-justice 통합 명제와 정합.

**검증 권고**: Round 4에서 LMDC 같은 entity의 시계열(COP21~30) frame_type 변천을 추적하면 strategic reframing 가설을 검증할 수 있다.

### 4.3 mixed 37건의 IR 함의 — brokerage 신호인가, 측정 노이즈인가

mixed frame이 24 → 37로 53% 증가한 것은 양가적이다. **brokerage 가설**: mixed frame은 의장국이나 broker 국가가 다중 그룹의 frame을 텍스트에 동시 봉합한 시그니처일 가능성. 그러나 **노이즈 가설**: LLM 분류기가 단일 frame 결정에 실패한 reject pile일 가능성. 두 가설 분리에는 mixed로 분류된 37건 중 *internal frame composition* (예: justice 60% + sovereignty 40%) 보고가 필요하다. **Round 4 권고**: refinement-analyst에게 mixed frame의 component breakdown 요청.

---

## Section 5. Non-state actor (IIPFCC/AIPP/IWGIA/LCIPP) IR 위치

### 5.1 Hooghe-Marks Type II governance 부합성

Hooghe & Marks (2003, *American Political Science Review* 97(2))의 Type II governance는 task-specific, overlapping, non-territorial 행위자가 다층 거버넌스에 참여하는 구조다. UNFCCC 내 Indigenous 4 entity는 정확히 Type II 특성을 보인다:
- **Task-specific**: TEK/biocultural heritage 영역 한정
- **Overlapping**: IIPFCC (global), AIPP (Asia regional), LCIPP (UNFCCC institutional), IWGIA (international NGO)는 mandate가 중첩
- **Non-territorial**: 국가 영토에 정박되지 않음 (cross-border indigenous nation)

**CINA 함의**: 이 4 entity를 Stage 2 R-GAT의 **별도 노드 type**으로 모델링하는 것이 이론적으로 정당화된다. Type I (territorial state) 노드와 Type II (non-territorial functional) 노드를 분리하면 hybrid governance의 영향력 (예: Indigenous → AOSIS → COP30 preamble) 경로 추적이 attention weight으로 가시화 가능하다.

### 5.2 Indigenous epistemic community (Haas 1992 연장)

Haas (1992)의 epistemic community 4 조건 — (i) shared causal beliefs, (ii) shared normative principles, (iii) shared notions of validity, (iv) common policy enterprise — 을 Indigenous 4 entity에 적용:
- (i) Causal beliefs: TEK이 climate adaptation에 valid knowledge라는 epistemic claim ✓
- (ii) Normative: UNDRIP (UN Declaration on Rights of Indigenous Peoples) 기반 자기결정 원칙 ✓
- (iii) Validity: peer-validated indigenous-led research methodology ✓
- (iv) Common policy enterprise: COP 결정문에 토착민 권리 명시 + LCIPP 제도화 ✓

4 조건 모두 충족 → **Indigenous epistemic community 노드 모델링이 Haas 이론의 정당한 확장**.

### 5.3 Stage 2 R-GAT 통합 옵션

| 옵션 | 설명 | 장점 | 단점 |
|------|------|------|------|
| **A. 별도 노드 type** | Country/Group/Issue + 신규 NSA-Indigenous 노드 type | Type II governance 이론 정합 | R-GAT meta-path 복잡도 증가, ablation 비용 |
| **B. JT-ADAPT 한정 노드** | Just Transition 이슈 sub-graph 한정 | 데이터 효율 (NSA 20건 모두 JT-ADAPT 포함) | Indigenous 영향력이 NAPs/MIT-ADAPT에도 작동하므로 under-modeling |
| **C. edge 가중치 부착** | Country ↔ Issue edge에 NSA endorsement weight 추가 | 모델 수정 최소 | NSA 자체 행위자성 (norm entrepreneur) 손실 |

**IR 권고**: **옵션 A가 이론적으로 정당하나 데이터 N=20으로는 R-GAT attention head 학습이 불안정**. Round 4-5에서 NSA observer submission 추가 수집 (target N≥80) 후 옵션 A 채택. 단기적으로는 **옵션 A + C 하이브리드** — NSA 노드 추가하되 edge 가중치를 Indigenous endorsement intensity로 augment.

---

## Section 6. Round 4 collector 권고 (IR 관점)

### P0 (필수)

1. **COP21~COP27 historical chair letters (시계열 N≥80 달성)**:
   - COP21 Fabius (FRA), COP22 Trabelsi (MAR), COP23 Bainimarama (FJI), COP24 Kurtyka (POL), COP25 Schmidt (CHL), COP26 Sharma (UK), COP27 Shoukry (EGY) 각 2-3건씩 → 최소 +14, target +40 records
   - UNFCCC documents portal: `https://unfccc.int/process-and-meetings/the-paris-agreement/the-paris-agreement` archive section
   - 각 의장의 opening letter, scenario note, closing remarks 3종 우선
   - **목표**: chair_metadata 32 → 80+, COP coverage 3 → 10

2. **Realist baseline B0 country_features_v2 검증 (지연된 P0)**:
   - T01 P0-B에 명시된 4 datasets (WB GDP, OWID CO2 cumulative, SIPRI MILEX, COW alliances v4.1) 통합 country_features_v2.csv가 **CINA 20국 모두 결측 없는지** 확인
   - ISO3 join 정확도 > 99%
   - **realist baseline B0 (4 features만) F1 < 80%**라는 hypothesis 검증. 만약 ≥ 90%이면 CINA novelty 위협 → Discussion section에서 명시적 처리 필요 (Drezner 2007 권력비대칭 가설로 frame).

3. **Secretariat informational note (FCCC/.../INF) 시리즈**:
   - Tallberg 4 채널 중 (i) information asymmetry 측정의 핵심 source
   - 현재 chair_metadata에 INF series 1건 (cop30 da4b) → target N≥15
   - SBI/SBSTA scenario note 추가 수집

### P1 (권장)

4. **NSA observer submission 확장 (Round 5 R-GAT 옵션 A 가능 조건)**:
   - IIPFCC/AIPP/IWGIA/LCIPP 외에 Climate Action Network (CAN), Women & Gender Constituency (WGC), Trade Union NGOs (TUNGO) 추가
   - 현재 20건 → target 80+

5. **Castro et al. 2025 supplementary 학술 contact (Round 1 D5 미해결)**:
   - 제1저자 zxsa0716@kookmin.ac.kr가 아닌 별도 academic email로 contact
   - utterance timeline 확보 시 norm diffusion lag (Finnemore-Sikkink life cycle) 정량화

### P2 (선택)

6. **WTO/UNCLOS spillover 데이터** — Keohane-Victor (2011) regime complex 검증용. 우선순위 낮음.

---

## Section 7. policy-science-professor와의 합의·불일치 예측

### 합의 예상

- **chair_metadata N=32의 시계열 부족**: 정책학자도 소수 의장 corpus에서 implementation politics 추론 불가 지적 가능
- **frame 5범주 활성화의 가치**: justice frame 9건이 climate justice / vulnerability lens 정책학에서도 환영
- **realist baseline B0 country_features_v2 검증 미완**: 양 분과 모두 즉각 진행 권고
- **Indigenous 4 entity 노드 모델링**: 정책학의 distributive justice 관점에서도 정당화 가능
- **L.25 advance→final cosine diff 미완료**: Round 2 §4.1에서 양 분과 합의했으나 Round 3에서 산출 안 됨 — 양측 공동 권고

### 불일치 예상

| 쟁점 | 정책학자 예상 입장 | IR 입장 |
|------|------------------|--------|
| **에너지 수출국 의장 가설** | 정책학: implementation capacity gap에 가깝게 해석 (UAE/AZE는 능력 있는 host였는가) | IR: agenda-setting bias 가설 우선 (Steinberg 2002) |
| **NSA Indigenous 노드 모델링** | 정책학: vulnerability index와 결합한 capability framing | IR: norm entrepreneurship + epistemic community framing |
| **mixed frame 37건의 해석** | 정책학: implementation의 multi-stakeholder 정합성 신호 | IR: brokerage 신호 또는 측정 노이즈 |
| **N=32 부족 진단의 정도** | 정책학: 정책 brief 작성에는 충분 (Track A 우선) | IR: Track B 논문에는 미달, Round 4 추가 수집 요구 |

→ **통합 가능성**: "에너지 수출국 의장 가설"은 정책학의 implementation capacity와 IR의 agenda-setting bias 양 lens에서 *동일 데이터를 다르게 해석*하는 productive disagreement. 두 lens 모두 critique에 명시하고 Discussion section에서 alternative framing으로 제시.

→ **별도 처리**: NSA 노드 모델링은 IR이 옵션 A (별도 노드 type) 옹호 vs 정책학이 옵션 C (edge 가중치) 선호 가능. 두 모델을 ablation으로 비교하는 것이 합리적 — Round 5 GAT 학습에서 두 모델 F1 차이 보고.

---

## Section 8. 추가 IR Reference (Round 1·2 18개 + Round 3 신규 5개 = 누적 23개)

### Round 3 신규 reference (5개)

19. **Steinberg, R. H. (2002)**. In the Shadow of Law or Power? Consensus-Based Bargaining and Outcomes in the GATT/WTO. *International Organization* 56(2). — Chair as agenda-setter의 outcome bias 정량 검증 모델. CINA의 "에너지 수출국 의장" 가설 framing에 직접 적용.
20. **Hooghe, L., & Marks, G. (2003)**. Unraveling the Central State, but How? Types of Multi-Level Governance. *American Political Science Review* 97(2). — Type I/Type II governance 구분. NSA Indigenous 4 entity의 Type II 정당화.
21. **Witter, R., Marion Suiseeya, K. R., Gruby, R. L., et al. (2015)**. Moments of influence in global environmental governance. *Environmental Politics* 24(6). — Indigenous epistemic community 부상의 GEG 분석.
22. **Allan, J. I., & Hadden, J. (2017)**. Exploring the framing power of NGOs in global climate politics. *Environmental Politics* 26(4). — Transnational coalition framing power. AOSIS-LCIPP joint submission 분석에 직접 적용.
23. **Falkner, R. (2016)**. The Paris Agreement and the new logic of international climate politics. *International Affairs* 92(5). — Climate hegemon vs pledge-and-review. "에너지 수출국 의장" 가설의 climate hegemon ceiling 모델.

### 한국 IR 문헌 보강

- 신범식 (2023). 「기후변화협상에서의 의장국 리더십과 한국의 외교 옵션」. *국제정치논총* 63(2). — Round 2 인용, Round 3에서 BRA-host development frame 분석에 재적용.
- 이태동 (2024). 「IPCC와 UNFCCC 사이의 epistemic-political tension」. *한국과 국제정치*. — Round 3의 IIPFCC + LCIPP traditional knowledge 정치화 분석에 직접 적용.

---

## Section 9. team-lead 결정 요청

### D1 (P0). chair_metadata 시계열 확장 — COP21~27 letter 14+건 Round 4 수집할 것인가?

**제안**: 채택. Bayer-Urpelainen (2013) panel 분석 minimum threshold (N>10 COP) 도달 위해 필수. UNFCCC portal scraping 약 6-8시간. 실패 시 Round 5에서 ICR 검증으로 보완 가능하나 대체 불가.

### D2 (P0). Realist baseline B0 country_features_v2 검증 — Round 4 collector 우선 task인가?

**제안**: 채택. T01 P0-B에 이미 명시되었음에도 검증 보고가 누락 (cr3_compliance에 항목 없음). 만약 realist 4 변수만으로 F1 ≥ 90%이면 CINA novelty 위협 — 빠른 검증 후 Discussion 대응 전략 설계 필요.

### D3 (P0). L.25 advance→final cosine diff 산출 — Round 4 즉시 실행?

**제안**: 채택. Round 2 §4.1과 Round 3 cross-review 양측 합의 사항. sBERT embedding cosine similarity 계산은 4시간 작업. Tallberg formula control 가설의 첫 정량 검증.

### D4 (P1). NSA Indigenous 4 entity의 R-GAT 노드 모델링 옵션 — A/B/C 결정?

**제안**: **옵션 A + C 하이브리드** 채택. Round 4 NSA 추가 수집 후 옵션 A 가능. 단기적으로 옵션 C 시작.

### D5 (P1). frame_type ICR (inter-coder reliability) 코딩 검증 — Round 4 시작?

**제안**: 채택. mixed 37건 / justice 9건 / development 5건의 신뢰도 검증을 위해 코더 2인 (외부 정치학 대학원생) 무작위 30건 더블 코딩. Krippendorff α ≥ 0.7 목표.

### D6 (P2). HEEDO-1 scope 확장 (협상 vs 이행) — Round 2 미해결 결정 재요청

**입장**: **양립 채택 옹호 (Round 2 입장 유지)**. Lipscy (2017), Drezner (2007) 근거. IR/Policy sub-graph 분리 + ablation 가능 설계 조건. 

---

## Appendix. 평점 산출 근거 (Round 3)

- **Theoretical grounding 4.3**: 5범주 frame 활성화 (+0.3). justice/development source 14건 식별 (Constructivist 변수 측정 가능). Indigenous epistemic community 노드 정당화 (Haas 1992 + Hooghe-Marks 2003 확장). Round 4에서 BRA dual-role 정량 검증 시 4.5 도달.
- **Methodological rigor 3.7**: Tallberg 4 채널 중 3개 자동 식별 (+0.2). counterfactual baseline 1 (비-BASIC chair) N_COP=3으로 산출 불가 — 만점 진전 못 함.
- **Empirical validity 3.8**: chair 17 → 32 + NSA 20건 + 4 entity 추가 (+0.3). Bayer-Urpelainen N>100 미달 (-0.0, 단계적 도달 가능).
- **Policy strategic relevance 4.3**: 에너지 수출국 의장 narrative + BRA development frame 가시화 (+0.3). Track A 정책 brief grounding 강화.
- **Clarity & reproducibility 4.5**: cr3_compliance JSON + processing_version 명시 (+0.0, 유지). ICR 부재 (-0.5).

평균 **4.13/5** (Round 1: 3.3, Round 2: 3.9, Round 3: 4.13). Major revision → Minor revision 진입 공고화.

---

## Round 3 핵심 비판 Top 3

### C3.1 (P0) — chair_metadata N=32, COP coverage=3으로는 시계열 인과 추론 불가

**구체 인용**: 32 records 중 24건 (75%)이 COP30. historical chair letter는 UAE/AZE/BRA 3건뿐. Bayer-Urpelainen (2013, *ISQ* 57) panel 분석 N>100 / N_COP≥10 기준선 미달.

**왜 P0인가**: "에너지 수출국 의장 3연속" 가설 검증의 자유도가 0. Steinberg (2002) agenda-setter shift 모델 검증 시 비-산유국 의장 baseline 부재.

**수정 제안**: Round 4 COP21~27 letter 12+건 수집 (위 §6 P0-1).

### C3.2 (P0) — frame_type 5범주 활성화는 *descriptive*이지 *causal mechanism* 아님

**구체 인용**: justice 9건 / development 5건이 Indigenous + AOSIS + AILAC + LMDC + BRA에 분포되어 있으나, **frame_type 차이가 협상 outcome (L.25 결정문 언어, 59 indicator 채택률)에 인과적으로 어떤 경로로 작용했는지** 측정 변수가 없음. Beach & Pedersen (2019) process tracing의 fingerprint evidence가 미수집.

**왜 P0인가**: frame_type을 단지 group 특성의 *label*로 처리하면 Wendt (1999) constructivism의 "ideas have causal power" 명제가 검증 불가능. CINA의 IR contribution이 약화.

**수정 제안**: Round 4-5에서 frame_type → outcome (sovereignty frame 비율 vs final decision의 voluntary 언어 비율) 회귀 분석. Process tracing fingerprint로 (a) AOSIS justice frame 등장 → (b) chair drafts 채택 → (c) preamble 토착민 권리 명시 사슬 검증.

### C3.3 (P0) — Realist baseline B0 country_features_v2 검증 미수행

**구체 인용**: T01 P0-B 명시에도 cr3_compliance에 country_features_v2 검증 항목 없음. CINA 20국 결측, ISO3 join 정확도, realist 4 변수 단독 F1 미보고.

**왜 P0인가**: 만약 realist 4 변수만으로 F1 ≥ 90%이면 CINA의 정교한 GAT + frame_type 변수의 incremental contribution이 통계적으로 미달. Discussion section에서 reviewer 2가 즉시 reject 사유로 사용 가능.

**수정 제안**: Round 4 collector 즉시 실행. 결과에 따라 (a) F1 < 80%: CINA novelty 강화 (b) F1 80-90%: incremental 위치 (c) F1 ≥ 90%: Drezner (2007) "power asymmetry explains all" 가설로 Discussion 재구성.

---

*— ir-political-professor (round 3)*
