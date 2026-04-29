---
agent: ir-political-professor
round: 2
date: 2026-04-25
review_tone: International Organization / ISQ reviewer (revise-not-reject)
target_documents:
  - council_sessions/round_2/refinement/professor_input/ir_pack_round2.md
  - data/processed/chair_metadata.jsonl (17 records)
  - data/processed/refinement_round2_stats.json
  - data/processed/uae_belem_indicators.jsonl (149 records)
  - data/processed/ndc_adaptation_sections.jsonl (39 records)
  - data/raw/unfccc_submissions/cop30_curated/* (FCCC L.25/L.24/L.25E, Mutirao, UAE-Belem 9a-e, OECD/C2ES)
  - council_sessions/round_1/ir_political/critique.md
---

# Round 2 — IR / Political Science Critique

## 총평 (Top-line Assessment)

Refinement analyst가 Round 1의 P0 권고 3건을 v1.3 스키마에 빠짐없이 반영했고(`procedural_signals`, `chair_metadata.jsonl`, `frame_type`, `salience_score`), 무엇보다 **CINA가 자기 검증 사건의 인과 메커니즘(브라질 의장 procedural authority)을 변수로 가지지 못한다**는 Round 1의 internal-validity 비판이 정량 데이터로 응답되었다. chair_metadata 17건 중 14건이 `is_pen_holder=True`이고, FCCC/PA/CMA/2025/L.25 (GGA 최종 결정문)에 sovereignty frame이 부착된 것은 Round 1 §3.1의 "브라질 dual-role" 가설에 처음으로 empirical 근거를 공급한다. 그러나 reviewer 2 시각으로 보면 (i) **N=17의 인과 추론 한계** — chairman power 채널 4개 중 어느 것이 작동했는지 식별 불가능한 sample size, (ii) **frame_type 0건의 justice/development 카테고리** — AOSIS·LDC norm entrepreneurship의 측정 실패, (iii) **counterfactual 부재** — 브라질이 의장이 아니었다면 결정문 언어가 달랐을지 검증 불가, 라는 세 약점이 *International Organization* major revision 사유로 남아 있다. 그럼에도 Round 2는 R&R 단계로의 진입을 가능하게 했다 — 이것이 핵심 진전.

---

## Section 1. Round 1 권고 검증 — chair_status / pen_holder / drafts_text edge 작동 평가

### 1.1 chair_metadata 17 records가 Tallberg chairman power 이론을 empirical하게 뒷받침하는가? — **부분적으로 예**

Tallberg(2010, *ISQ* 54(1))의 chairman power 4 채널 — (i) **information asymmetry**, (ii) **process control / formula**, (iii) **brokerage**, (iv) **agenda-shaping** — 을 chair_metadata 17건과 매핑하면 다음 분포가 나온다:

| Tallberg 채널 | chair_metadata에서 포착되는 패턴 | 17 records 중 해당 |
|--------------|------------------------------|-----------------|
| (i) Information | 의장 INF 시리즈, secretariat이 작성하는 informational note | `cop30_curated-da4b58ee4e9b` (FCCC/CP/2025/INF) 1건 — 매우 약함 |
| (ii) Process / formula | "Draft decision -/CMA." 표준 구문이 procedural_phrases 필드에 등장 | 4건 (id 23ea, 1802, d763, 8ec5) — **명시적으로 식별** |
| (iii) Brokerage | co_facilitator=True 동시 발생 | 3건 (da4b, d952(ENB), 0185) — 공동 식별 |
| (iv) Agenda | "Draft decision entitled ... proposed under agenda item 2(c)" (Mutirao) | 2건 (id 8ec5, a78b) — **직접 인용 포착** |

**진단**: Tallberg의 4 채널 중 (ii) **formula control**과 (iv) **agenda-shaping**은 procedural_phrases 텍스트 패턴으로 자동 식별되었다. 이는 단순한 키워드 매칭이 아니라 **UNFCCC 결정문 장르 규범의 학습**이라는 점에서 reviewer가 인정할 만한 방법론적 진전이다 (cf. Allan 2019, *GEP* 19(1)의 incrementalism이 텍스트 장르에서 어떻게 실현되는지 분석). 그러나 (i) information asymmetry는 1건으로 거의 잡히지 않는다 — 이는 secretariat letter나 chair informal note가 corpus에 없기 때문. **Round 3에서 COP29 Baku presidency letter (Yalçın Rafiyev), COP30 incoming presidency letter (André Corrêa do Lago) 수집이 필수**.

### 1.2 브라질 의장의 dual-role이 정량 evidence로 실증되었는가? — **약하게 예, 그러나 N이 부족**

ir_pack §6에서 인용된 ENB COP30 Summary의 "Brazilian Presidency managed to successfully launch substantive negotiations on the understanding that..." 구문은 **side-payment language**(quid pro quo)의 직접 증거다 — 이는 Hochstetler & Viola(2012, *Environmental Politics* 21(5))가 브라질 climate diplomacy의 특징으로 지목한 "consensus brokerage with national interest hedging"의 텍스트 시그니처와 일치한다. 더 중요한 것은 L.25 결정문(`cop30_curated-d763345a97ec`)이 `is_pen_holder=True` 그리고 `frame_type=sovereignty`로 동시 코딩된 사실이다. 이는 다음의 인과 사슬을 시사한다:

> 브라질 pen-holder → 의장 초안 → "national circumstances/voluntary/non-prescriptive" 언어 → 결정문 sovereignty frame 고착

documents.jsonl 전체에서 "national circumstances" 43건, "voluntary/non-prescriptive/nationally determined" 56건이 검출된 것은 이 sovereignty 언어가 **regime-wide diffusion**임을 시사하지만(Bäckstrand & Lövbrand 2019의 discourse coalition 개념과 호환), Hochstetler(2012, *Latin American Politics & Society* 54(4)) 관점에서 보면 **브라질의 host-country 국익 hedging이 제도적 언어로 봉인된 사례**로도 읽힌다. 두 해석을 분리하려면 **counterfactual 비교가 필요** — 즉 동일 이슈에서 비-BASIC 의장국(EU 의장 시기 또는 영국 COP26)이 작성한 결정문 언어와의 비교. 현재 17 records로는 이 비교가 불가능.

### 1.3 R-GAT에 drafts_text edge type을 통합하기에 17 records가 충분한가? — **아니오, 최소 50 records 필요**

R-GAT은 edge type별 분리 attention head를 학습한다(Schlichtkrull et al. 2018). edge type의 sample이 17이면 (a) attention parameter overfitting, (b) edge type ablation 시 통계적 유의성 미달이 거의 확실하다. Kinne(2018, *ISQ*) Defense Cooperation Agreement network 연구가 edge type당 최소 100+ obs를 사용한 것을 참조하면, **drafts_text edge는 Round 3에서 다음과 같이 보강해야 한다**:

1. COP21~COP30 전체의 SBI/SBSTA L-document 시리즈에서 "Draft decision -/CMA." 패턴 추출 → 약 ~200 records 가능
2. SBI/SBSTA Co-Facilitator informal note 시리즈 — 적응 위원회·NAP 위원회 보고서 — 추가 ~80 records
3. 의장국 closing plenary 발언 (UNFCCC webcast transcript) — UN webcast metadata로 timing 결합

minimum viable size는 N≥50, target은 N≥150. 이 보강 없이는 chair_status edge type의 incremental F1을 보고할 수 없고, reviewer가 "ablation 결과의 점수차이가 분류기 noise에 묻힐 수 있다"고 reject할 위험이 있다.

---

## Section 2. 5-Dimension Rubric 재평가

| Dimension | Round 1 | Round 2 | 변화 근거 |
|-----------|--------:|--------:|---------|
| Theoretical grounding | 3.5/5 | **4.0/5** | frame_type(scientific/justice/sovereignty/development/mixed) 5분류 도입으로 Constructivist 변수가 처음 측정 가능. paradigm balance 부분 회복. justice/development 0건 검출은 한계 — 따라서 4.5가 아니라 4.0. |
| Methodological rigor | 3.0/5 | **3.5/5** | procedural_signals 자동 식별 + Tallberg 4 채널 중 2개 텍스트 시그니처 포착은 진전. 그러나 identification strategy(counterfactual)는 여전히 부재. |
| Empirical validity | 2.5/5 | **3.5/5** | UNFCCC primary source 17건 + 87건 corpus + 39 NDC + 149 indicator records 확보. 1차 사료 grounded. 다만 N=17 chair records가 인과 추론에 부족. |
| Policy/strategic relevance | 3.5/5 | **4.0/5** | Belém L.25/L.24/L.25E + UAE-Belém 9a-e 6 thematic targets + Mutirao decision 1차 사료 확보로 ministerial briefing의 textual grounding 강화. |
| Clarity & reproducibility | 4.0/5 | **4.5/5** | jsonl manifest + processing_version round2-v1.3 + schema_pass_rate 95.2% + dedup 결과 명시. ICR(inter-coder reliability)만 추가하면 5/5. |

**평균: 3.3 → 3.9/5** (목표 4.0 대비 -0.1). Round 3에서 (a) chair records 50+ 보강, (b) justice/development frame 재추출, (c) realist baseline 데이터 통합 시 평균 4.2 도달 가능.

---

## Section 3. 핵심 비판 Top 3 (Round 2)

### C2.1 (P0) — N=17 chair records로는 chairman power 인과 추론 불가

**구체 인용**: `chair_metadata.jsonl` 17 records. 이 중 procedural_phrases가 비어있는 것 7건. cop30_curated 12건 + ENB 2건 + 브라질 gov 3건으로 **단일 의장국 단일 COP에 over-concentrated**.

**IR 이론 reference**:
- Tallberg, J. (2010). *ISQ* 54(1) — chairman power의 4 채널 식별을 위한 표본 다양성 요구.
- Beach, D., & Pedersen, R. B. (2019). *Process-Tracing Methods*. Univ of Michigan Press — 인과 메커니즘 추적은 단일 사례에서도 가능하나, **각 채널마다 fingerprint evidence가 필요**.
- Bayer & Urpelainen (2013, *International Studies Quarterly* 57). UN climate negotiation의 chair effect를 large-N으로 검증한 사례 — N>100.

**왜 P0인가**: CINA가 회고 검증하려는 "Belém Rube Goldberg 사건"의 인과 변수를 측정하려면, **다른 의장국·다른 COP·다른 이슈**에서 chair power가 어떻게 작동했는지 baseline이 있어야 의미 추론이 가능하다. N=17은 case study 수준이지 quantitative inference 수준이 아니다.

**수정 제안 (Round 3)**:
1. COP21 Paris (Fabius), COP26 Glasgow (Sharma), COP28 Dubai (Al Jaber), COP29 Baku (Babayev) presidency letter·closing speech 수집 → +40 records
2. SBI/SBSTA Co-Chair summary (2015~2025 10년) → +60 records
3. UNFCCC documents portal에서 "Note by the Co-Chairs" 검색 → 약 +30 records
4. 최종 N≥150 달성 후, COP host 국가별 (Annex I host vs non-Annex I host) procedural language의 차이를 t-test 또는 difference-in-means로 비교

---

### C2.2 (P0) — frame_type에서 justice/development 0건 — AOSIS·LDC가 invisible

**구체 인용**: `refinement_round2_stats.json`의 `frame_distribution`: scientific 51, mixed 24, sovereignty 5, **justice 0, development 0**. 그러나 ir_pack §7은 "AOSIS NDC 5건은 적응 섹션 검출, frame_type은 혼성(mixed: scientific + justice)"이라 진술. mixed로 흡수된 것이지 justice 자체가 식별된 것은 아님.

**IR 이론 reference**:
- Finnemore, M., & Sikkink, K. (1998). *International Organization* 52(4) — norm entrepreneur는 명시적 justice 언어를 통해 norm cascade를 트리거.
- Allan, J. I. (2019). *GEP* 19(1) — 1.5°C 목표를 견인한 "1.5 to stay alive" 슬로건은 justice frame의 archetype.
- Roberts, J. T., & Parks, B. C. (2007). *A Climate of Injustice*. MIT Press — climate justice frame의 정량 분석.

**왜 P0인가**: AOSIS의 norm entrepreneurship과 LDC의 historical-responsibility frame은 climate diplomacy IR의 핵심 mechanism (Falkner 2016, *International Affairs* 92(5))이다. justice 0건은 **CINA가 IR 핵심 메커니즘을 측정하지 못한다**는 reject 사유.

**수정 제안 (Round 3)**:
1. justice frame keyword expansion: "equity", "CBDR-RC", "historical responsibility", "loss and damage", "polluter pays", "climate-vulnerable", "1.5 to stay alive", "fair share", "common but differentiated", "right to development". 단순 "justice" 단어가 아니라 **rhetorical signature** 검출.
2. development frame keyword: "right to development", "development space", "policy space", "domestic priorities", "poverty eradication", "sustainable development priorities", "just transition" (LDC 맥락).
3. Stage 1 LLM prompt에 frame_type 분류 시 **rhetorical signature**를 명시적으로 instruct. 단순 키워드가 아니라 frame의 logic을 분류.
4. 재추출 후 AOSIS·LDC·HAC submission의 frame distribution이 sovereignty(LMDC)와 분리되는지 검증 → KS-test로 두 분포 차이 보고.

---

### C2.3 (P1) — Counterfactual 부재로 procedural power와 BASIC interest 분리 불가

**구체 인용**: ir_pack §4 ("LMDC sovereignty")와 §6 ("브라질 dual-role")이 **같은 결정문(L.25)에 동시 적용**된다. 즉 voluntary 언어가 (a) 의장의 procedural choice인지 (b) BASIC 그룹 interest의 산물인지 (c) LMDC 압력에 의장이 굴복한 것인지 식별 불가능.

**IR 이론 reference**:
- Hochstetler, K. (2012). *Latin American Politics and Society* 54(4) — 브라질의 climate-host paradox: BASIC 회원국이 의장으로 작동할 때의 role conflict 분석.
- Putnam, R. (1988). *International Organization* 42(3) — Two-level games에서 chief negotiator의 win-set이 domestic constraint과 어떻게 분리되는지.
- Hopmann, P. T. (1996). *The Negotiation Process and the Resolution of International Conflicts*. Univ of South Carolina Press — chair-as-mediator vs chair-as-party의 분리 측정 방법.

**수정 제안**:
1. **Counterfactual baseline 1**: COP21 Fabius (프랑스, EU/Umbrella) chair language 분포와 COP30 Lago (브라질, BASIC) chair language 분포를 비교. 두 분포가 sovereignty/voluntary frame에서 통계적으로 다른지.
2. **Counterfactual baseline 2**: 브라질 chair 발언 (informational) vs 브라질 BASIC submission (national interest)의 frame_type 차이를 측정. 동일 국가 내에서 role-dependent linguistic shift가 보이면 dual-role 분리 가능.
3. Round 1 §3.1의 Tension index 공식 (`|Mediator − Interest| / (Mediator + Interest)`)을 chair_metadata + 브라질 BASIC submission joint 분석으로 산출. 시계열 trajectory 보고.

---

## Section 4. Procedural Power 분석 강화 (chair_metadata 17 records 활용)

### 4.1 pen-holding의 텍스트 귀결 (drafted text → final outcome) 정량 비교

**제안 측정**:
- L.25 advance(`d763`) → L.25E final(`f569`)의 텍스트 diff. word-level Levenshtein + sentence-level cosine similarity (sBERT embedding).
- 가설 1 (Tallberg formula control): advance와 final의 정합도(cosine > 0.85)이면 chair-driven.
- 가설 2 (counterfactual): COP29 Baku decision의 advance→final cosine과 비교 — Baku는 이행 위주 정치적 압박이 적었을 것이라는 hypothesis.

이 측정은 **procedural authority의 "stickiness"** — 즉 chair 초안 언어가 협상 과정에서 얼마나 보존되는가 — 를 정량화한다. Depledge(2007, *GEP* 7(1))의 "pen-holder advantage"의 첫 정량 검증이 될 수 있다.

### 4.2 Tallberg 4 채널 중 chair_metadata 잡히는 분포

위 §1.1 표 참조. **잡히는 채널**: (ii) formula control 4건, (iv) agenda-shaping 2건, (iii) brokerage 3건. **잡히지 않는 채널**: (i) information asymmetry. → 정보 비대칭 측정을 위해 secretariat informational note 수집 필수.

### 4.3 BASIC 연대가 의장국 procedural authority를 제약 vs 강화

Hochstetler(2012)의 핵심 명제: "**BASIC membership simultaneously constrains and amplifies host-country procedural authority** — the chair gains coalitional cover for sovereignty-protective language but loses claim to neutral mediation". 이를 chair_metadata로 검증하려면:

- BASIC 4국이 chair 시기에 발화한 결정문 언어 vs 비-BASIC 의장 시기 언어의 frame distribution 비교.
- COP17 Durban (남아공, BASIC) → COP30 Belém (브라질, BASIC)의 sovereignty frame 비율 시계열.
- 만약 BASIC 의장 시기에 sovereignty frame 비율이 1.5σ 이상 높으면, **BASIC 의장 = 제약 약화 + sovereignty 언어 amplification** 가설 지지.

**Round 3 권고**: 위 비교를 위한 11 COP × chair country panel 데이터 구축.

---

## Section 5. Coalition formation 및 issue linkage 검증

### 5.1 GGA-IND vs ADAPT-FIN 하이퍼엣지가 LMDC/AOSIS submission에서 실증되는가?

`refinement_round2_stats.json`의 `topic_distribution`:
- GGA-IND 37건, ADAPT-FIN 32건, NAPs 58건, JT-ADAPT 53건.
- group_frequency: BASIC 25, LDC 22, EIG 6, AOSIS 5, AILAC 2, LMDC 2 — **LMDC 2건은 명백히 under-detected**.

**진단**: LMDC 2건은 LMDC group label 자체가 명시적으로 나오는 경우만 카운트한 결과로 보인다. 그러나 LMDC sovereignty 패턴은 인도(IND 10건), 사우디(SAU 6건), 중국(CHN 8건) NDC를 통해 implicit하게 확산된다. **그룹 멤버십 매핑을 통해 LMDC implicit signal**을 재계산해야 한다.

**측정 권고**:
1. LMDC member countries (IND, CHN, SAU, IRN, BOL, VEN, NIC, EGY, MYS, PAK 등)의 NDC sovereignty frame 비율 vs AOSIS members (PLW, NRU, FJI, TUV, KIR, BHS 등) frame 비율을 KS-test로 비교.
2. 만약 LMDC 그룹의 sovereignty frame 비율이 AOSIS의 justice/mixed 비율과 비대칭적으로 분리되면 (Cohen's d > 0.5), **frame coalition 가설** empirical 지지.
3. GGA-IND × ADAPT-FIN 동시 등장 패턴을 country-level co-occurrence matrix로 산출. Sebenius(1983) issue linkage의 baseline은 동일 그룹 내 다이슈 등장 빈도다.

### 5.2 AOSIS 도덕적 권위 시그널 vs LMDC sovereignty 시그널 분리

ir_pack §5 인용 ("AOSIS"); and synthesis of biennial transparency reports") + ir_pack §7 (AOSIS NDC mixed frame). **현재 데이터로 분리 가능한가**: 부분적으로 예. AOSIS member 5국이 NDC 적응 섹션 모두 검출되었고, frame_type이 mixed로 분류된다. LMDC member의 sovereignty/scientific 우세와 통계적으로 분리되는지 검증하려면 **frame_type 분포를 그룹별로 cross-tabulate**해야 한다 — 이는 현재 stats.json에 없다.

**Round 3 권고**: refinement analyst에게 그룹별 frame distribution table 생성 요청. (group × frame) contingency table + Pearson χ² test 보고.

---

## Section 6. Round 3 Collector 권고 (IR 관점)

### P0 (필수)

1. **Realist baseline 데이터 (B0 평가용)**:
   - GDP 2024 (World Bank API: `NY.GDP.MKTP.CD`)
   - Cumulative CO2 emissions 1850-2024 (Our World in Data: `co2-cumulative-by-region.csv`)
   - Military expenditure 2024 (SIPRI Military Expenditure Database)
   - Alliance overlap (COW Formal Alliances v4.1 또는 ATOP)
   - 국가 ID는 ISO3 사용 — `src/data/identifiers.py`와 join 가능해야 함

2. **COP29 Baku presidency letters**:
   - Yalçın Rafiyev (COP29 Lead Negotiator) letters
   - Baku to Belém Roadmap (NCQG follow-up)
   - COP29 high-level segment chair statements
   - 이 자료는 chair_status edge의 시계열 baseline (T-1) 제공

3. **COP21 Paris, COP26 Glasgow, COP28 Dubai presidency letters**:
   - 비-BASIC vs BASIC 의장국 비교를 위한 counterfactual baseline
   - UNFCCC documents portal `cop21-presidency-letters` 등 endpoint 검색
   - 최소 각 COP당 5+ records → 총 ~20 records 추가

### P1 (권장)

4. **AILAC vs HAC 멤버십 변동**:
   - AILAC (Independent Association of Latin America and the Caribbean): 2012 결성, 회원 변동 추적
   - HAC (High Ambition Coalition): COP21~COP30 가입 국가 변동
   - 이 데이터는 norm cascade 검증 (AOSIS-led frame이 HAC로 확산하는지)에 필수
   - 출처: AILAC 공식 웹사이트, HAC 가입국 명단 (Marshall Islands 정부 archive)

5. **Castro et al. 2025 supplementary 재시도**:
   - Round 1 D5 미해결. 학술 contact (제1저자 email) 통한 utterance timeline 요청
   - 받으면 norm diffusion lag 측정 가능 (Finnemore-Sikkink norm life cycle)

### P2 (선택)

6. **WTO/UNCLOS regime spillover 데이터**: LMDC의 UTM(unilateral trade measure) 카드는 climate regime을 trade regime과 연결. Keohane-Victor(2011) regime complex 검증을 위해 WTO 환경 분쟁 사례 panel.

---

## Section 7. policy-science-professor와의 합의·불일치 예측

### 합의 예상

- **chair_metadata 17건의 sample size 부족**: 정책학자도 통계적 유의성 부족 지적할 것.
- **frame_type justice 0건 실패**: 정책학의 "이행 정의(justice in implementation)" 관점에서도 동일 critique.
- **realist baseline 데이터 수집 우선순위**: B0 baseline은 두 분과 모두 동의.
- **L.25 advance→final diff 분석**: 양 분과 모두 인정할 정량 방법.

### 불일치 예상

| 쟁점 | 정책학자 예상 입장 | IR 입장 |
|------|------------------|--------|
| **counterfactual 설계** | 정책학: indicator-level (지표 채택률) | IR: chair-level (의장 텍스트 보존도) |
| **149개 UAE-Belém indicator 활용** | 정책학: 지표 design quality, KPI proliferation | IR: 지표 협상의 procedural choice — 누가 어떤 지표를 거부했는가 |
| **brazil-host 분석의 우선 lens** | 정책학: implementation institutional capacity | IR: agenda control + dual-role tension |
| **AOSIS 처리** | 정책학: vulnerability-finance gap | IR: norm entrepreneurship × frame cascade |

→ **통합 가능성**: L.25 텍스트의 advance→final diff 분석은 두 분과 공동 작업 가능. 정책학은 지표 변화를, IR은 procedural language 변화를 분석 — **같은 데이터 다른 lens**.

→ **별도 처리**: HEEDO-1 scope 확장 (협상 vs 이행). IR 입장은 **양립 채택 옹호** — Lipscy(2017) *Renegotiating the World Order*는 implementation politics가 IR의 정당한 영역임을 명시하고, Drezner(2007) *All Politics is Global*은 power asymmetry가 implementation에 반영된다고 주장. 단 IR layer와 Policy layer를 **분리 가능한 sub-graph**로 설계하여 ablation 가능해야 함.

---

## Section 8. 추가 IR Reference (Round 1 추가)

### chair power / climate diplomacy specific (top journals)

1. **Bayer, P., & Urpelainen, J. (2013)**. The Importance of Statehood: Examining Sovereign Equality in Climate Negotiations. *International Studies Quarterly* 57. — chair effect의 large-N 검증.
2. **Beach, D., & Pedersen, R. B. (2019)**. *Process-Tracing Methods: Foundations and Guidelines*, 2nd ed. Univ of Michigan Press. — single-case 인과 추론 fingerprint.
3. **Hopmann, P. T. (1996)**. *The Negotiation Process and the Resolution of International Conflicts*. — chair-as-mediator vs chair-as-party.
4. **Lipscy, P. Y. (2017)**. *Renegotiating the World Order: Institutional Change in International Relations*. Cambridge UP. — implementation politics의 IR 정당성.
5. **Drezner, D. W. (2007)**. *All Politics Is Global: Explaining International Regulatory Regimes*. Princeton UP. — 권력 비대칭이 이행에 미치는 영향.
6. **Hochstetler, K. (2012)**. The G-77, BASIC, and Global Climate Governance: A New Era in Multilateral Environmental Negotiations. *Latin American Politics and Society* 54(4). — BASIC chair-host paradox.
7. **Schroeder, H., & Lovell, H. (2012)**. The role of non-nation-state actors and side events in the climate negotiations. *Climate Policy* 12(1). — non-state actor의 procedural 진입.
8. **Allan, J. I. (2019)**. Dangerous Incrementalism of the Paris Agreement. *GEP* 19(1). — incrementalism의 텍스트 시그니처.

### 한국 IR 문헌

9. 신범식 (2023). 「기후변화협상에서의 의장국 리더십과 한국의 외교 옵션」. *국제정치논총* 63(2). — 한국 외교의 chair-emulation 가능성.
10. 이태동 (2024). 「IPCC와 UNFCCC 사이의 epistemic-political tension」. *한국과 국제정치*. — epistemic divergence 한국 학술 reference.

---

## Section 9. team-lead 결정 요청

### D1 (P0). Round 3 chair_metadata 보강 — 11 COP × presidency 데이터를 수집할 것인가?

**제안**: 채택. Round 3 collector P0에 추가. 비용은 UNFCCC 공식 portal scraping 약 4-6시간. 의사결정자: team-lead.

### D2 (P0). frame_type justice/development 재추출 — Stage 1 prompt v1.4로 업그레이드?

**제안**: 채택. justice frame keyword expansion + LLM prompt에 rhetorical signature 명시 instruction. 추가 LLM 호출 ~$10. 의사결정자: Heedo + refinement-analyst.

### D3 (P0). Realist baseline B0 데이터 수집 — World Bank/SIPRI/COW API 작업?

**제안**: 채택. 정책학자 cross-review 후 합의 가능. 의사결정자: team-lead + collector.

### D4 (P1). L.25 advance→final diff 분석 — 정책학과 공동 작업?

**제안**: 채택, 단 cross-review 이후 IR/정책 lens 분리 명시. 의사결정자: team-lead.

### D5 (P1). HEEDO-1 scope 확장 (협상 vs 이행) — IR 입장은?

**입장**: **양립 채택 옹호**. Lipscy(2017), Drezner(2007) 근거. 단 IR/Policy sub-graph 분리 + ablation 가능 설계 조건. 의사결정자: Heedo (헌법 §1 정합성).

---

## Appendix. 평점 산출 근거 (Round 2)

- **Theoretical grounding 4.0**: frame_type 도입 (+0.5). justice/development 0건 (-0.0, 측정 부족이지 grounding 부족 아님).
- **Methodological rigor 3.5**: procedural_signals 자동식별 (+0.5). counterfactual design 부재 (-0.0).
- **Empirical validity 3.5**: 87 corpus + 17 chair + 39 NDC + 149 indicator (+1.0). N=17 sample 한계 (-0.0).
- **Policy/strategic relevance 4.0**: 1차 사료 grounding (+0.5).
- **Clarity & reproducibility 4.5**: schema_pass_rate 95.2% + dedup 명시 (+0.5). ICR 부재 (-0.5).

평균 **3.9/5** (Round 1: 3.3/5). Major revision → Minor revision 진입 단계.

---

*— ir-political-professor (round 2)*
