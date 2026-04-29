---
agent: ir-political-professor
round: 1
date: 2026-04-25
target_documents:
  - CINA_FRAMEWORK.md
  - docs/01_theoretical_foundations.md
  - docs/02_methodology.md
  - docs/05_stage2_graph_analysis.md
  - docs/06_stage3_briefing_generation.md
  - docs/08_novelty_positioning.md
  - docs/13_reference_tables.md
  - council_sessions/round_1/data_collection/REPORT.md
review_tone: International Organization / ISQ reviewer (revise-not-reject)
---

# Round 1 — IR / Political Science Critique

## 총평 (Top-line Assessment)

CINA는 IR canon (Keohane-Victor 2011, Putnam 1988, Haas 1980/1992, Tollison-Willett 1979, Sebenius 1983, Hafner-Burton-Kahler-Montgomery 2009)을 명시적으로 인용하고 각 이론을 구체적 파이프라인 모듈에 매핑(`docs/01_theoretical_foundations.md` Table 6)했다는 점에서 **이론 접지 의도(intent of theoretical grounding)**는 명확하다. 그러나 현 단계에서 (i) **이론적 비대칭(theoretical asymmetry)** — 자유주의·제도주의 일변도이며 현실주의·구성주의가 명시적으로 배제(`01_theoretical_foundations.md` §7), (ii) **권력 변수의 외생성(exogeneity of power)** — `COUNTRY_POWER_INDEX`가 GDP/CO2/그룹리더십 가중합 hard-coded(`13_reference_tables.md` §7), (iii) **의장국 권력의 내생화 부재(unmodeled chairmanship power)** — Belém Rube Goldberg 사건의 핵심 메커니즘인 procedural power가 그래프 구조 변수로 들어가 있지 않음, 이라는 세 가지 구조적 약점이 있다. *International Organization*이나 *Global Environmental Politics* reviewer가 첫 round에서 reject 사유로 들 만한 것은 (iii)이며, (i)/(ii)는 major revision 사유다.

---

## Section 1. 5-Dimension Rubric

| Dimension | Score | 핵심 평가 |
|-----------|-------|----------|
| Theoretical grounding | **3.5/5** | IR canon 인용·매핑은 충실하나 paradigm balance 결여(현실주의·구성주의 배제 명시). Network IR 흐름과의 연결이 SNA 한 줄(`§5.2`)로 압축되어 약함. |
| Methodological rigor | **3/5** | R-GAT + Leiden + Apriori-style hypergraph 조합은 합리적이나, **identification strategy**가 없음. coalition consistency triplet loss는 group membership을 label로 사용하므로 그룹 자체를 예측한다는 것은 tautology에 가까움. |
| Empirical validity | **2.5/5** | Round 1 데이터 수집 결과 UNFCCC submission 0, NDC 0, ENB 0(`data_collection/REPORT.md` Q1 fail). 현재 시점에서 회고 검증의 ground truth 자체가 미확보. Round 2 Playwright 도입 전엔 empirical claim 일체 보류. |
| Policy / strategic relevance | **3.5/5** | 장관급 브리핑 템플릿(`06_stage3`)과 Engagement Sequence·Priority Matrix 항목은 외교 실무에 부합. 다만 한국 외교의 비-Annex I 모호 위치, BASIC-vs-EIG 동시참여 등 **focal country를 한국으로 swap했을 때의 robustness**가 검증되지 않음. |
| Clarity & reproducibility | **4/5** | identifier 표준(`13_reference_tables.md`), license 추적, sha256, run summary 모두 우수. IR 학술지 reviewer 기준의 **prompt versioning + seed**까지 약속(`02_methodology.md` §6). 다만 power_index.py가 **black-box 가중합**으로 남으면 reproducibility는 형식적임. |

평균 **3.3/5** — Major revision 권고. IR theoretical contribution(C9, C10)을 진짜 contribution으로 승격하려면 이번 라운드에서 power 모델링 보강이 필수다.

---

## Section 2. 핵심 비판 Top 3

### C1. Procedural / Chairmanship Power가 그래프 변수로 모델링되지 않음 (P0)

**구체 인용**:
- `CINA_FRAMEWORK.md` §3.1: "의장국은 이슈별로 포지션이 달라지므로 CINA의 이슈별 스탠스 분리 능력을 가장 강하게 테스트"
- `docs/05_stage2_graph_analysis.md` §1.1 country_features 32차원 중 **chair_status / procedural_role / pen_holder 변수 부재**
- `docs/01_theoretical_foundations.md` §2.2: "의장국으로서 Level I 역할(중재자)과 Level II 역할(자국 이해)이 동시에 작용한다. CINA는 이를 두 개의 분리된 stance vector로 포착할 수 있는가?" — 질문만 남기고 답이 없음

**IR 이론 근거**:
- Tallberg, J. (2010). *The Power of the Chair: Formal Leadership in International Cooperation*. *International Studies Quarterly*, 54(1), 241–265. 의장국이 (a) agenda-shaping, (b) brokerage, (c) representation의 세 가지 procedural resource를 통해 결과를 형성함을 보임.
- Depledge, J. (2007). A Special Relationship: Chairpersons and the Secretariat in the Climate Change Negotiations. *Global Environmental Politics*, 7(1), 45–68. UNFCCC 특수성에서 의장권의 텍스트 초안권(pen-holder power)이 결정적임을 사례로 제시.
- Bäckstrand, K., & Lövbrand, E. (2019). The Road to Paris. *Journal of Environmental Policy & Planning*, 21(5). Paris Agreement 텍스트 초안 메커니즘이 의장국·co-facilitator의 procedural authority에 의존함을 분석.

**왜 P0인가**: COP30 Belém Adaptation Indicators 59개 사건은 **정확히 chairmanship power의 사례**다. 브라질 의장국이 expert proposal을 정치적으로 재작성한 것을 CINA의 `epistemic_divergence_score`(`05_stage2_graph_analysis.md` §3.4)는 *국가별 power_index의 가중합으로* 계산한다. 그러나 이 가중합에는 의장국의 procedural seat가 들어가 있지 않다. 즉 **CINA는 자기가 검증하겠다고 약속한 사건의 인과 메커니즘을 변수로 갖고 있지 않다**. 이것은 *International Organization* reviewer가 "the model cannot, in principle, recover the explanandum"이라고 reject할 사유다.

**수정 제안 (실행 가능)**:
1. `country_features`에 **chair_status** (0=일반, 1=incoming presidency, 2=current presidency, 3=outgoing troika) 카테고리 변수 추가.
2. `issue_features`에 **pen_holder_country_id** 추가 — 각 이슈별 텍스트 초안권 보유국. UNFCCC informal note에서 식별 가능.
3. R-GAT의 추가 edge type `drafts_text(Country, Issue, t)`을 정의하여 의장국·co-facilitator의 procedural 연결을 그래프에 직접 인코딩.
4. `epistemic_divergence_score` 산식에 `chair_proximity_to_political_outcome` 항 추가: 의장국 stance와 최종 텍스트의 cosine similarity가 expert proposal-텍스트 유사도보다 높으면 chair-driven divergence로 분류.

---

### C2. 자유주의 일변도 — Realist baseline과 Constructivist mechanism이 설계상 배제됨 (P0)

**구체 인용**:
- `docs/01_theoretical_foundations.md` §7: "Realist IR (Waltz, Mearsheimer): 국가를 단일 이성적 행위자로 보는 관점은 Stage 1의 flexibility signal 추출과 충돌. 이슈별 선호 변이를 설명 못함." / "Constructivism (Wendt): 단기 COP 협상에서 정량화가 어려움. 향후 확장 대상."
- `docs/08_novelty_positioning.md` §2.3 C9, C10이 모두 **Two-Level Games + Regime Complex** (자유주의-제도주의 canon)에만 의존.

**IR 이론 근거**:
- Mearsheimer, J. J. (1994/95). The False Promise of International Institutions. *International Security*, 19(3). 제도가 권력 분포의 epiphenomenon이라는 명제. CINA가 stance score만 보고 coalition을 추론한다면 이 비판에 노출됨.
- Wendt, A. (1999). *Social Theory of International Politics*. Cambridge UP. 이익은 정체성에 의해 구성된다는 명제. AOSIS의 "moral authority" / "climate-vulnerable identity"는 정확히 이 메커니즘.
- Hopf, T. (1998). The Promise of Constructivism in International Relations Theory. *International Security*, 23(1). 정체성 변수의 정량화 가능성.
- Falkner, R. (2016). The Paris Agreement and the new logic of international climate politics. *International Affairs*, 92(5), 1107–1125. Paris 이후 climate diplomacy가 "pledge-and-review"로 옮겨가면서 norm-based legitimacy의 중요성이 증가.

**왜 P0인가**: 자유주의 일변도는 두 개의 구체적 실증 약점으로 이어진다.
1. **Realist null model 부재**: CINA의 coalition prediction이 "단순히 GDP-similar 국가들이 같은 cluster"에 떨어지는 것 이상의 정보를 주는지 baseline test가 없음. Material capability null model에 대한 incremental validity 입증 필요.
2. **AOSIS의 도덕적 권위 모델링 불가**: AOSIS는 GDP·인구·CO2 어느 측면에서도 약하지만 climate-vulnerable identity로 협상 결과(Paris 1.5°C 목표, L&D Fund 설립)를 공동 견인했다. CINA의 `ND_GAIN_VULNERABILITY`가 노드 피처로 있긴 하나, 이것은 **취약성 자체**일 뿐 **취약성을 활용한 norm entrepreneurship**의 측정이 아니다.

**수정 제안**:
1. **Realist baseline B0**: stance score 사용 없이 `(GDP, CO2, military, alliance overlap)`만으로 coalition을 예측하는 logistic 모델 추가. CINA의 incremental F1을 보고.
2. **Constructivist 변수 도입**: 각 (국가, 이슈) 추출에 `frame_type ∈ {scientific, justice, sovereignty, security, development}` 카테고리를 추가 코딩. Stage 1 prompt에 "어떤 normative frame을 동원하는가" 항목 신설. AOSIS의 frame이 LDC·HAC와 align되는지 추적 가능.
3. `docs/01_theoretical_foundations.md` §7을 "limitation"에서 "additional theoretical lens"로 격상하고, baseline이자 robustness check로 명시.

---

### C3. Hypergraph가 Issue Linkage 이론의 *형식적* 구현이지만 *전략적* 구현은 아님 (P1)

**구체 인용**:
- `docs/02_methodology.md` §3.5와 `docs/05_stage2_graph_analysis.md` §3.3: hyperedge = "여러 이슈에서 동시에 flexibility 또는 rigidity를 보이는 이슈 묶음" — Apriori support ≥ τ.
- `docs/01_theoretical_foundations.md` §3.2: Issue linkage = "교환 가능한 concession 창출 / 취약 이슈를 강력 이슈에 편승".

**IR 이론 근거**:
- Sebenius, J. K. (1983). Negotiation Arithmetic. *International Organization*, 37(2). Issue linkage의 핵심은 **선호 강도의 비대칭(asymmetric salience)** — A에게 사소한 이슈가 B에게 중대하면 cross-issue trade가 가능. **단순한 "공통 flexibility 패턴"이 아님**.
- Tollison & Willett (1979): linkage gain은 reservation values의 차이에 비례.
- Davis, C. L. (2004). International Institutions and Issue Linkage: Building Support for Agricultural Trade Liberalization. *American Political Science Review*, 98(1), 153–169. Linkage가 작동하려면 institutional binding이 필요.

**왜 P1인가**: 현재 CINA의 hyperedge 정의는 *공통 flexibility의 motif*이지 *상호 보완적 trade의 motif*가 아니다. Apriori는 "함께 발생하는 패턴"을 찾는 알고리즘이지 **"한쪽이 양보하고 다른 쪽이 강경한 보완 패턴"**을 찾지 않는다. Sebenius적 linkage는 **반대 방향 stance + 비대칭 salience**가 핵심인데, 현 구현은 같은 방향 flexibility만 본다. 그 결과 `classify_linkage_pattern`의 세 카테고리(`linked_concession`, `package_demand`, `divergent`) 중 진짜 linkage 기회는 마지막 `divergent`뿐이지만 detection은 앞 두 케이스 위주다.

**수정 제안**:
1. Hyperedge 정의를 **complementary motif**로 확장: 국가 그룹 G가 이슈 i에서는 강경(stance > τ_high)이고 이슈 j에서는 유연(flex_signal=1)일 때 (i, j, G)를 candidate package edge로 등록.
2. **Salience 변수 추가**: Stage 1에서 `salience_score ∈ [0,1]` (이슈 우선순위)을 별도 추출. linkage gain potential = stance_gap × salience_asymmetry.
3. Castro et al. 2025 데이터의 cross-issue cooperation pair를 retrospective ground truth로 사용하여 linkage detection의 precision/recall 측정.

---

## Section 3. Power 분석 강화 권고

CINA의 `COUNTRY_POWER_INDEX`(`13_reference_tables.md` §7)는 hard-coded 가중합이고 *시간 불변*이며 *이슈 불변*이다. 이는 climate diplomacy 권력의 핵심 동학을 놓친다.

### 3.1 의장국 브라질의 dual-role 정량화

브라질은 (a) **Level I**: COP30 의장국으로서 합의 도출 책임 (mediator), (b) **Level II**: 자국 Amazon·석유(Petrobras pre-salt) 이해 (interest-holder)의 두 역할이 충돌. 이를 측정하려면:

- **Mediator-score**: 브라질 발화 중 *procedural* 단어 비율 ("Parties may wish to consider", "as a way forward", "the chair proposes") + 양 진영 발화 빈도와의 균형. Yamin & Depledge (2004) *The International Climate Change Regime* 부록에서 의장 발언 코딩 사례.
- **Interest-score**: 브라질 NDC와 BASIC submission에서 자국 이해를 명시적으로 옹호하는 빈도.
- **Tension index**: |Mediator - Interest| / (Mediator + Interest). COP30 6주차 동안의 시계열로 plot.

### 3.2 BASIC 내부 분열 vs LMDC 결속

`13_reference_tables.md` §1.2는 BASIC(4국)·LMDC(~25국)을 같은 그룹 노드 유형으로 처리하지만 **결속 메커니즘이 다르다**:
- BASIC: 1) 거대 emitters만의 club (Hurrell & Sengupta 2012, *International Affairs* 88(3)), 2) 내부 이질성(중국 vs 인도 vs 브라질) 큼.
- LMDC: 1) 사우디·이란·볼리비아 등 normative coherence (개도국 권리 옹호), 2) Saudi의 financial subsidy로 cohesion 유지 (Blaxekjær & Nielsen 2015, *Climate Policy* 15(6)).

**측정 권고**: 그룹 노드 피처 `historical_cohesion`(`05_stage2_graph_analysis.md` §1.1)을 단일 스칼라가 아니라 **(within-group stance variance, leader-driven vs distributed cohesion type)** 두 차원으로 분해. BASIC은 high variance / leader-distributed, LMDC는 low variance / Saudi-anchored.

### 3.3 AOSIS 도덕적 권위 vs 실질 협상력 격차

AOSIS는 GDP·인구·이산화탄소 어느 면에서도 약하지만 1.5°C 목표 (Paris) · L&D Fund (COP27)를 견인. 이 **moral entrepreneurship**은 현재 CINA에서 측정 불가:
- 노드 피처에 `sids_status` 0/1만 있을 뿐.
- `COUNTRY_POWER_INDEX`에서 AOSIS = 0.62로 단일값.

**측정 권고**:
- **Norm entrepreneurship score**: AOSIS·LDC가 *처음* 도입한 frame ("loss and damage", "1.5 to stay alive")이 다른 그룹 발화에 cascade되는 비율 (Finnemore & Sikkink 1998 *International Organization* 52(4)의 norm life cycle). Castro et al. 2025의 utterance timeline에서 frame diffusion lag로 계산.
- **Coalition multiplier**: AOSIS 단독 power × HAC 합류 시 effective power. Stage 2 attention weight의 그룹 간 합산으로 추정.

### 3.4 Hegemonic Stability / G-X 외교 관점

US-China-EU의 trilateral configuration이 climate regime의 *underlying power structure*. Falkner (2005) *International Affairs* 81(1)는 EU의 "환경적 hegemonic stability" 가설을 검증하고, Hochstetler & Milkoreit (2014) *Global Environmental Politics* 14(1)는 emerging powers (BASIC)의 등장으로 hegemonic 모델이 **distributed leadership** 모델로 이행했다고 분석. CINA가 "bridge countries"를 betweenness centrality로 식별할 때, 이 거시 구조 변동이 변수로 들어가야 한다.

**권고**: `temporal snapshot`에 (US-China-EU triangle distance) 시계열 covariate 추가. 미-중 climate cooperation 발표(2014 Sunnylands, 2021 Glasgow) 전후의 graph topology shift를 event-study로 검증.

---

## Section 4. policy-science-professor와의 합의·불일치 예측

### 합의 예상 (high confidence)

- **Empirical validity 점수가 낮다**: 두 교수 모두 Round 1 데이터 부재(UNFCCC/NDC/ENB 0건)를 P0 blocker로 지적할 것.
- **Reproducibility 표준은 우수**: identifier 표준·sha256·license·prompt versioning 모두 정책학자도 인정할 강점.
- **회고적 검증의 framing 자체는 타당**: COP30 종료 직후라는 timing은 Track A(수업)·Track B(논문) 모두에 부합.
- **Brazil-Adaptation focus의 정당화**: 의장국 + Belém indicators ground truth는 양 분과 모두 강력 case study로 인정.

### 불일치 예상 (productive disagreement)

| 쟁점 | 정책학자 예상 입장 | IR 입장 |
|------|------------------|--------|
| **이행(implementation) vs 권력(power)** | NAP 이행률, finance gap 메트릭 강조; output→outcome→impact 사슬 | power asymmetry, agenda control, frame contestation 강조; 누가 이행을 정의하는가 |
| **Belém Rube Goldberg 사건의 해석** | 정책학: 정책 design failure (지표 과부하, KPI proliferation) | IR: chairmanship procedural power × epistemic-political tension의 산물 |
| **AOSIS 처리** | 취약성 지표 (ND-GAIN, GDP-pc) 기반 vulnerability metric | norm entrepreneurship × moral authority × coalition leadership |
| **브리핑 audience** | 부처 실무 (ministerial action plan) | 외교부 협상단 (red line, leverage) — 단, `06_stage3` 템플릿은 후자에 가까움 |
| **Castro 2025 활용** | ground truth로 calibration용 | ground truth지만 **그것 자체가 ENB editor의 framing bias를 가짐 (constructivist critique)** |

→ **통합 가능성**: 정책학자가 "implementation outcome"을 추가 노드 유형으로 제안할 가능성. IR은 그것을 받되 *implementation에 대한 권력 분포*를 edge weight로 인코딩하라고 제안. 두 관점 모두 CINA에 통합되어야 한다.

→ **별도 처리 권고**: AOSIS 처리에서 "vulnerability index (정책)"와 "norm entrepreneurship (IR)"은 통합하지 말고 **별개의 노드 피처**로 병기. 후속 ablation에서 각 변수의 incremental validity 측정.

---

## Section 5. 추가 Reference (영어 IR literature)

### Top journals — climate diplomacy 최근 5년 (≥3)

1. **Allan, J. I., & Hadden, J. (2017)**. Exploring the framing power of NGOs in global climate politics. *Environmental Politics*, 26(4), 600–620. — Frame analysis 정량화 가능성.
2. **Falkner, R. (2016)**. The Paris Agreement and the new logic of international climate politics. *International Affairs*, 92(5), 1107–1125. — Pledge-and-review의 IR 함의.
3. **Hochstetler, K., & Viola, E. (2012)**. Brazil and the politics of climate change. *Environmental Politics*, 21(5), 753–771. — 브라질 dual-role의 직접 사례.
4. **Bäckstrand, K., et al. (2017)**. Non-state actors in global climate governance. *Environmental Politics*, 26(4). — Non-state actor 통합 시 그래프 확장 방향.
5. **Aklin, M., & Mildenberger, M. (2020)**. Prisoners of the Wrong Dilemma: Why Distributive Conflict, Not Collective Action, Characterizes the Politics of Climate Change. *Global Environmental Politics*, 20(4), 4–27. — Realist redistributive framing의 climate 적용.
6. **Allan, J. I. (2019)**. Dangerous Incrementalism of the Paris Agreement. *Global Environmental Politics*, 19(1). — 합의의 incrementalism이 negotiation graph에 어떻게 나타나는가.

### Network IR 최근 5년 (≥2)

7. **Greenhill, B., & Lupu, Y. (2017)**. Clubs of Clubs: Fragmentation in the Network of Intergovernmental Organizations. *International Studies Quarterly*, 61(1), 181–195. — Regime complex의 network operationalization.
8. **Kinne, B. J. (2013, 2018)**. Network Dynamics and the Evolution of International Cooperation. *American Political Science Review* 107(4) / **Kinne, B. J. (2018)** Defense Cooperation Agreements. *International Studies Quarterly*. — Temporal network IR의 표준 방법론.
9. **Manger, M. S., & Pickup, M. A. (2016)**. The Coevolution of Trade Agreement Networks and Democracy. *Journal of Conflict Resolution*, 60(1). — co-evolution 모델링이 CINA의 stance-network coupling에 시사점.

### Climate diplomacy specific (Bäckstrand·Falkner·Hochstetler 등) (≥2)

10. **Bäckstrand, K., & Lövbrand, E. (2019)**. The Road to Paris: Contending Climate Governance Discourses. *Journal of Environmental Policy & Planning*, 21(5), 519–532. — Discourse coalition 개념을 CINA의 frame 변수에 직접 적용 가능.
11. **Hochstetler, K., & Milkoreit, M. (2014)**. Emerging Powers in Global Climate Governance. *Global Environmental Politics*, 14(1), 22–40. — BASIC의 distributed leadership.
12. **Tallberg, J. (2010)**. The Power of the Chair. *International Studies Quarterly*, 54(1). — C1 procedural power 비판의 1차 source.
13. **Depledge, J. (2007)**. A Special Relationship: Chairpersons and Secretariat in Climate Negotiations. *Global Environmental Politics*, 7(1). — UNFCCC chair power의 climate 특화 source.

---

## Section 6. team-lead 결정 요청

### D1. C1 (Chairmanship Power)을 Round 2 P0로 격상할 것인가?
**제안**: 격상 권고. 그렇지 않으면 epistemic_divergence 회고 검증의 internal validity가 무너짐. `country_features`에 `chair_status` + `pen_holder` 추가는 데이터 수집(B1 차단 해소 후 informal note)으로 즉시 가능. 의사결정자: Heedo + team-lead.

### D2. Realist baseline B0와 Constructivist frame 변수를 evaluation protocol에 추가할 것인가?
**제안**: B0는 추가(low cost — GDP/CO2 데이터 이미 있음). Frame 변수는 Stage 1 prompt 확장 필요(prompt v1.2 → v1.3). 추가 LLM 호출 비용 ~$5-10. 의사결정자: Heedo.

### D3. `COUNTRY_POWER_INDEX`를 hard-coded에서 learnable로 전환할 것인가?
**제안**: 부분 전환. (a) 기본 score는 hard-coded 유지(투명성), (b) issue-specific power adjustment를 R-GAT의 attention weight 합으로 endogenously 산출. 두 값의 차이를 "structural power surprise"로 보고.

### D4. policy-science-professor critique와 cross-review 시기?
**제안**: 양 critique이 모두 도착하면 team-lead가 unified critique matrix를 작성하여 Round 2 task로 분배. 합의 항목은 즉시 implementation, 불일치 항목은 두 교수 + Heedo의 round-table 결정.

### D5. AOSIS / norm entrepreneurship 측정을 위해 Castro 2025 utterance timeline 접근이 가능한가?
**제안**: Castro et al. 2025 supplementary 차단(B4) 해소가 선결. 학술 contact (Round 2 collector task)에 norm diffusion 분석용 utterance timestamp 요청 포함.

---

## Appendix. 평점 산출 근거 요약

- **Theoretical grounding 3.5**: canonical citation 충실 + mapping table 우수 (+1.5), 그러나 paradigm balance 결여 (-1).
- **Methodological rigor 3**: pipeline 합리성 (+2), identification strategy 부재·triplet loss tautology 위험 (-1).
- **Empirical validity 2.5**: design은 회고검증 가능 (+1.5), 실 데이터 부재 (-1).
- **Policy / strategic relevance 3.5**: 브리핑 템플릿 외교 실무성 (+2), focal country swap robustness 미검증 (-0.5).
- **Clarity & reproducibility 4**: identifier 표준·license·sha256·prompt versioning (+2), power_index black-box (-0.5).

---

*— ir-political-professor (round 1)*
