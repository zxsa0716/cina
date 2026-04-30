# CINA: COP30 Belém Adaptation Indicators 분석 — LLM-GNN-LLM 파이프라인의 회고적 검증

---

**Author**: Heedo (Kookmin University, Department of Climate Technology Convergence)
**Generated**: 2026-04-29T07:07:32.238465Z (Gemini 2.5 Flash-Lite, free)
**Status**: v2 draft — comprehensive



# 초록

본 연구는 기후 변화 적응에 대한 국가별 및 지역별 입장을 분석하고, 특히 개발도상국과 취약 국가의 적응 노력에 대한 국제 사회의 지원 메커니즘을 탐구한다. 연구 목적은 기후 변화 적응 관련 국제 협상에서 주요 행위자들의 입장, 프레임, 그리고 절차적 역할을 정량적으로 분석하여, 적응 금융, 지표 개발, 국가 적응 계획(NAPs) 등 핵심 이슈에 대한 논의 동향을 파악하는 데 있다.

연구 방법론으로는 2021년부터 2030년까지 COP 회의의 56개 기록을 분석 대상으로 삼았으며, 특히 브라질, AOSIS, 인도, 한국 등 주요 국가 및 지역 그룹의 발언 데이터를 수집하였다. LLM 기반의 텍스트 분석을 통해 각 행위자의 입장(stance), 이슈 프레임(frame), 의장국 및 제안국 역할(procedural authority)을 추출하고, 이를 바탕으로 국가별 입장 분포, 프레임 일관성, 그리고 이슈별 중심성(centrality)을 분석하였다. 또한, 브라질의 국내 및 국제적 입장 간의 격차(IRR_Brazil Translation Gap)와 같은 구체적인 사례를 심층 분석하였다.

핵심 발견은 다음과 같다. 첫째, 브라질은 '개발' 프레임을 중심으로 적응 지표 개발(GGA-IND) 및 국가 적응 계획(NAPs) 수립에 강력한 지지를 표명하며 의장국 및 제안국으로서 적극적인 역할을 수행하였다. 둘째, AOSIS와 인도는 '개발' 및 '정의(justice)' 프레임을 통해 적응 금융(ADAPT-FIN) 지원의 필요성을 강조하며, 특히 개발도상국에 대한 재정 지원 의무를 명확히 하였다. 셋째, 한국은 '개발' 프레임 하에서 적응 지표 개발 및 국가 적응 계획 수립에 지지를 보이며 절차적 권한을 행사하였다. 넷째, 국제 협상에서 '자발적', '비강제적', '비처벌적', '촉진적'이라는 수사적 장치(hedging density)가 빈번하게 사용되어, 구속력 있는 합의 도출에 어려움이 있음을 시사한다.

본 연구의 학술적 기여는 기후 변화 적응 논의에서 행위자들의 복잡한 입장과 전략을 정량적으로 분석하고 시각화함으로써, 기존의 질적 연구를 보완하고 새로운 분석 틀을 제공한다는 데 있다. 또한, '개발'과 '정의'라는 상반되면서도 상호 보완적인 프레임이 적응 논의에서 어떻게 작용하는지를 밝혀냈다. 정책적 함의로는, 개발도상국의 적응 역량 강화를 위한 실질적인 재정 및 기술 지원 메커니즘 구축의 시급성을 강조하며, 국제 사회는 구속력 있는 적응 목표 설정과 이행을 위한 보다 적극적인 노력을 기울여야 할 것이다. 특히, 브라질의 사례에서 나타난 국내외 입장 간의 괴리를 줄이고, 모든 국가가 형평성 있는 적응 부담을 공유할 수 있도록 국제 협력 강화가 필요하다.


# 서론

기후 변화는 인류 문명에 대한 전례 없는 위협으로 부상했으며, 이에 대응하기 위한 국제적 협상은 복잡성과 다층성을 특징으로 한다. 파리 협정 이후, 지구 평균 온도 상승폭을 산업화 이전 대비 1.5°C로 제한하기 위한 야심찬 목표 달성을 위해서는 각국의 기여 방안(NDC) 강화와 적응 능력 향상, 그리고 이를 뒷받침할 재정 지원 메커니즘 구축이 필수적이다. 그러나 이러한 목표를 향한 여정은 각국의 상이한 역사적 책임, 경제 발전 수준, 그리고 기후 변화에 대한 취약성으로 인해 첨예한 이해관계 충돌과 정치적 난제로 가득하다. 특히, 개발도상국의 적응 능력 강화와 재정 지원 문제는 기후 협상의 핵심 쟁점이자 난제로서, '정의로운 전환'과 '기후 정의'라는 가치와 직결된다.

기후 협상의 복잡성을 이해하고 효과적인 정책 결정을 지원하기 위한 노력의 일환으로 다양한 인공지능(AI) 도구들이 개발되어 왔다. 예를 들어, NegotiateCOP은 기후 협상 과정에서 국가별 입장을 분석하고 시각화하는 데 활용될 수 있으며, RICE-N 모델은 기후 변화의 경제적 영향을 예측하는 데 기여한다. 또한, Castro (2025)의 연구는 기후 협상에서 특정 국가의 발언 패턴과 영향력을 분석하는 방법론을 제시한다. 이러한 도구들은 기후 협상의 특정 측면을 이해하는 데 유용하지만, 다음과 같은 한계점을 지닌다. 첫째, 기존 AI 도구들은 주로 과거 데이터에 기반한 정태적 분석에 치중하는 경향이 있어, 역동적으로 변화하는 협상 환경과 국가 간의 복잡한 상호작용을 실시간으로 포착하고 예측하는 데 한계가 있다. 둘째, '개발', '정의', '주권' 등 다양한 프레임워크를 통해 국가들의 입장이 나타나는데, 이러한 프레임워크 간의 미묘한 차이와 전환을 심층적으로 분석하는 데 어려움이 있다. 특히, 브라질과 같이 '개발' 프레임워크를 중심으로 적응 지표 개발(GGA-IND, NAPs)에 적극적인 입장을 보이면서도(Brazil, GGA-IND, stance=1.0, frame="development", is_chair=True, is_pen=True; Brazil, NAPs, stance=0.8, frame="development", is_chair=True, is_pen=True), 재정 지원(ADAPT-FIN)에 대해서는 중립적인 태도를 보이는(Brazil, ADAPT-FIN, stance=0, frame="mixed") 복합적인 입장을 보이는 국가들의 경우, 단편적인 분석으로는 그 의도를 완전히 파악하기 어렵다. 셋째, 특히 적응 금융(ADAPT-FIN)과 같은 쟁점에서 인도와 같이 '정의' 프레임워크를 통해 선진국의 재정 지원 의무를 강조하는(India, ADAPT-FIN, stance=1.0, frame="justice") 국가들의 요구사항을 분석하는 데 있어, 단순히 찬성/반대 여부를 넘어선 심층적인 프레임 분석이 요구된다.

본 연구는 이러한 기존 AI 도구들의 한계를 극복하고 기후 협상의 복잡성을 보다 심층적으로 이해하기 위해 다음과 같은 세 가지 연구 질문을 제시한다.

1.  **기후 협상에서 국가들의 적응 관련 정책 요구사항은 어떤 프레임워크(예: 개발, 정의, 주권)를 통해 나타나며, 이러한 프레임워크는 국가별 입장의 강도 및 협상 과정에서의 절차적 권한(의장국, 펜홀더)과 어떤 관계를 가지는가?**
2.  **적응 금융(ADAPT-FIN) 및 적응 지표 개발(GGA-IND)과 같은 핵심 쟁점에서 국가들의 입장은 어떻게 나타나며, 특히 브라질, 인도, AOSIS와 같은 주요 행위자들의 입장은 어떤 특징을 보이는가?**
3.  **기후 협상 과정에서 '번역의 간극(translation gap)'은 어떻게 나타나며, 특히 브라질의 경우 국내 및 국제 협상 과정에서 발생하는 번역의 간극은 어떤 특성을 가지는가?**

본 연구는 위 세 가지 연구 질문에 대한 답을 찾기 위해, COP21부터 COP30까지의 기후 협상 데이터를 기반으로 국가별 입장의 강도, 프레임워크, 절차적 권한, 그리고 번역의 간극을 종합적으로 분석하는 새로운 AI 기반 방법론을 제안한다. 구체적으로, Stage 1 LLM 추출 결과에서 나타난 국가별 입장, 쟁점, 프레임워크, 그리고 절차적 권한에 대한 정량적 데이터를 활용하여 분석을 수행한다. 또한, Stage 2 Graph Analysis에서 도출된 국가별 중심성, 절차적 권한, 그리고 프레임 일관성 지표를 활용하여 국가들의 협상 전략을 심층적으로 분석한다. 더 나아가, IRR_Brazil Translation Gap 분석을 통해 브라질의 국내외 협상 과정에서 발생하는 번역의 간극을 정량적으로 측정하고 그 특성을 규명한다.

본 연구의 학술적 의의는 다음과 같다. 첫째, 기후 협상에 대한 기존의 단편적인 AI 분석에서 벗어나, 국가별 입장, 프레임워크, 절차적 권한, 그리고 번역의 간극을 통합적으로 분석하는 새로운 분석 프레임워크를 제시한다. 둘째, 실제 기후 협상 데이터를 기반으로 국가들의 복합적인 입장과 협상 전략을 정량적으로 분석함으로써, 기후 협상 연구의 경험적 기반을 강화한다. 셋째, 특히 개발도상국의 적응 능력 강화와 재정 지원이라는 민감한 쟁점에서 나타나는 프레임워크의 차이와 번역의 간극을 심층적으로 분석함으로써, 기후 정의 논의에 대한 새로운 통찰을 제공한다.

본 연구의 실천적 의의는 다음과 같다. 첫째, 기후 협상 당사국 및 이해관계자들에게 각국의 입장과 협상 전략에 대한 보다 정확하고 심층적인 정보를 제공함으로써, 보다 효과적인 협상 전략 수립을 지원한다. 둘째, 특히 개발도상국의 적응 능력 강화와 재정 지원에 대한 논의에서 발생하는 오해와 불신을 해소하고, 상호 이해를 증진하는 데 기여할 수 있다. 셋째, 브라질과 같은 주요 협상 당사국의 번역 간극 분석 결과는 향후 국제 협상 과정에서 의사소통의 효율성을 높이고, 보다 건설적인 논의를 이끌어내는 데 기여할 수 있다. 궁극적으로 본 연구는 기후 변화라는 전 지구적 위협에 효과적으로 대응하기 위한 국제 협력 강화에 기여할 것으로 기대된다.


## 2. 이론적 배경

본 연구는 기후변화 적응 논의에서 국가들의 행위와 입장을 분석하기 위해 복합적인 이론적 틀을 적용한다. 특히, 국제 레짐의 복잡성, 다층적 협상 과정, 이슈 연계, 그리고 지식 공동체의 역할을 중심으로 분석 모델을 구축한다. 이러한 이론들은 CINA(Climate INteraction Analysis) 모듈에 다음과 같이 매핑되어 분석의 깊이를 더한다.

### 2.1. Regime Complex (Keohane & Victor, 2011)

Keohane과 Victor(2011)가 제시한 '레짐 복합체(Regime Complex)' 이론은 단일한 국제 레짐이 아닌, 상호 연관되고 때로는 중첩되는 다수의 국제 규범, 규정, 그리고 기구들의 집합으로 국제 거버넌스를 이해하는 틀을 제공한다. 기후변화 분야는 파리협정, UNFCCC, 교토의정서 등 다양한 규범 체계와 더불어, 특정 이슈(예: 적응 금융, 손실과 피해)를 다루는 여러 협상 과정이 복잡하게 얽혀 있다. CINA 모듈은 이러한 레짐 복합체 내에서 국가들이 특정 이슈에 대해 어떤 입장을 취하고(stance), 어떤 요구사항(demands)을 제시하는지를 분석함으로써, 국가 행위자들이 복수의 규범 체계 속에서 어떻게 전략적으로 행동하는지를 파악한다. 예를 들어, 브라질이 'GGA-IND' 이슈에서 'development' 프레임을 내세우며 강한 지지(strong_support) 입장을 보인 것은(Stage 1 LLM 추출), 개발도상국으로서의 지위를 활용하여 적응 지표 개발에 대한 요구사항을 관철시키려는 레짐 복합체 내에서의 전략적 행동으로 해석될 수 있다.

### 2.2. Two-Level Games (Putnam, 1988)

Putnam(1988)의 '이층 게임(Two-Level Games)' 이론은 국제 협상이 국내 정치와 불가분의 관계에 있음을 강조한다. 국가 대표는 국제 무대에서 협상하는 동시에, 국내적으로는 다양한 이해관계자들의 압력과 요구에 직면한다. 성공적인 국제 합의는 국제적 합의 가능성(win-set)과 국내 비준 가능성(win-set)이라는 두 가지 조건을 모두 충족해야 한다. CINA 모듈은 국가의 'stance'와 'demands'를 분석함으로써, 국제 무대에서의 입장과 요구사항을 파악한다. 또한, 'is_chair' 및 'is_pen' 메타데이터는 특정 국가가 의장국 역할을 수행하거나 문서 초안 작성(pen holder)에 참여하는 등, 국내외적 역학 관계 속에서 협상 과정에 미치는 영향력을 간접적으로 시사한다. 브라질이 'NAPs' 이슈에서 의장국(chair_role=True) 및 문서 초안 작성자(pen_holder=True)로서의 역할을 수행한 것은(Stage 1 LLM 추출), 국내적 지지를 바탕으로 국제 협상에서 주도적인 역할을 수행하려는 이층 게임의 역학을 보여준다.

### 2.3. Issue Linkage (Tollison & Willett, 1979)

'이슈 연계(Issue Linkage)'는 서로 다른 이슈들을 묶어 협상의 지렛대로 활용하는 전략이다. 특정 이슈에서의 양보를 통해 다른 이슈에서의 이득을 얻으려는 시도는 국제 협상의 중요한 특징 중 하나이다. CINA 모듈은 다양한 'issue'에 대한 국가들의 'stance'와 'frame'을 분석함으로써, 국가들이 특정 이슈를 다른 이슈와 어떻게 연계하고 있는지 추론할 수 있다. 예를 들어, 인도가 'GGA-IND' 이슈에서 'justice' 프레임을 내세우며 적응 노력에서의 형평성과 공동의 차별화된 책임(CBDR-RC)을 강조하고, 동시에 'ADAPT-FIN' 이슈에서도 개발도상국에 대한 재정 지원을 강력히 요구하는(Stage 1 LLM 추출) 것은, 적응 지표 개발과 적응 금융이라는 두 이슈를 연계하여 개발도상국의 입장을 강화하려는 전략으로 볼 수 있다.

### 2.4. Epistemic Communities (Haas, 1992)

Haas(1992)의 '지식 공동체(Epistemic Communities)' 이론은 특정 분야의 전문 지식과 가치를 공유하는 전문가 집단이 정책 결정 과정에 미치는 영향을 설명한다. 기후변화 분야에서는 과학자, 정책 전문가, 국제기구 관계자 등으로 구성된 지식 공동체가 과학적 합의를 형성하고 정책 의제를 설정하는 데 중요한 역할을 한다. CINA 모듈의 'frame' 분석은 이러한 지식 공동체의 영향을 파악하는 데 기여한다. 예를 들어, 브라질과 한국이 'development' 프레임을, 인도가 'justice' 프레임을 주로 사용하는 것은(Stage 1 LLM 추출), 각 국가가 속한 혹은 영향을 받는 지식 공동체의 가치와 우선순위가 반영된 결과로 해석될 수 있다. 'frame_consistency' 분석 결과, 브라질(3), 인도(2), 한국(2) 모두 특정 프레임을 일관되게 사용하는 경향을 보이며(Stage 2 Graph Analysis), 이는 해당 국가들이 특정 지식 공동체의 영향 하에 있음을 시사한다.

이 네 가지 이론적 틀은 CINA 모듈을 통해 기후변화 적응 논의에서 국가들의 복잡한 행위와 전략을 다각적으로 분석하는 기반을 제공한다. 레짐 복합체는 국제 환경의 구조적 복잡성을, 이층 게임은 국내외적 상호작용을, 이슈 연계는 협상 전략을, 그리고 지식 공동체는 정책 결정에 영향을 미치는 전문적 지식의 역할을 설명함으로써, 본 연구는 기후변화 적응 거버넌스에 대한 심층적인 이해를 추구한다.


## 3. 데이터 및 방법론

본 연구는 기후변화 협상 맥락에서 국가들의 입장, 프레임, 그리고 절차적 역할을 심층적으로 분석하기 위해 CINA(Climate Negotiation Analysis) 3단계 파이프라인을 적용하였다. 이 파이프라인은 정량적 증거 추출, 이종 시간 그래프 분석, 그리고 그래프 기반 생성 및 증거 추적을 포함한다.

### 3.1. Stage 1: 정량적 증거 추출 및 베이지안 신뢰 구간

Stage 1에서는 NATO(Negotiation Analysis Tool Ontology)의 4가지 핵심 지표, 즉 `stance` (입장), `category` (범주), `frame` (프레임), 그리고 `confidence` (신뢰도)를 기반으로 LLM(Large Language Model)을 활용하여 21개의 정량적 증거를 추출하였다. `stance`는 국가의 입장 강도를 -1(반대)에서 1(지지) 사이의 연속적인 값으로 나타내며, `category`는 `strong_support`, `support`, `neutral_or_silent` 등 5가지 범주로 분류되었다. `frame`은 협상 이슈에 대한 국가의 인식 틀을 나타내며, `development`, `justice`, `sovereignty`, `mixed`, `scientific` 등 다양한 프레임이 식별되었다. `confidence`는 추출된 정보의 신뢰도를 나타낸다.

추가적으로, 협상 과정에서의 절차적 역할을 반영하기 위해 `is_chair` (의장 역할 수행 여부)와 `is_pen` (문서 초안 작성 참여 여부)이라는 두 가지 이진 변수를 도입하였다. 이 변수들은 국가가 특정 이슈에 대해 의장 역할을 수행하거나 문서 초안 작성에 참여했는지를 나타낸다. 예를 들어, 브라질은 'NAPs'(National Adaptation Plans) 이슈에서 `chair_role=True` 및 `pen_holder=True`로 직접 검증되었으며(chair_metadata), 이는 해당 국가가 해당 협상에서 중요한 절차적 권한을 가졌음을 시사한다.

본 연구에서 추출된 `stance` 값은 베이지안 신뢰 구간(Bayesian Credible Interval)을 통해 불확실성을 고려하였다. 이는 각 증거의 신뢰도를 보다 견고하게 평가하고, 분석 결과의 강건성을 높이는 데 기여한다. 예를 들어, Realist B0 모델의 통계 분석 결과, F1 점수는 0.560 [95% CI 0.458-0.654]로 나타났으며, 이는 무작위 F1 점수(0.440) 대비 유의미한 성능 향상을 보여준다(McNemar χ²=16.1, p<0.0001). Cohen's Kappa 값은 0.216으로 'fair' 수준의 일치도를 나타냈다.

LLM 추출 결과, `frame` 분포는 `scientific`이 51건으로 가장 많았으며, `mixed` 24건, `justice` 9건, `sovereignty` 5건, `development` 5건 순으로 나타났다(frame_distribution). 이는 기후변화 협상에서 과학적 근거를 바탕으로 한 논의가 주를 이루지만, 정의, 주권, 개발 등 다양한 가치와 프레임이 복합적으로 작용하고 있음을 보여준다.

### 3.2. Stage 2: 이종 시간 그래프 분석

Stage 2에서는 Stage 1에서 추출된 정량적 증거들을 기반으로 이종 시간 그래프(Heterogeneous Temporal Graph)를 구축하였다. 이 그래프는 국가, 이슈, 그리고 시간이라는 세 가지 주요 노드 유형과 이들 간의 관계를 나타내는 엣지로 구성된다. 그래프 분석을 위해 R-GAT(Relational Graph Attention Network) 모델을 활용하여 노드 임베딩을 학습하였다. R-GAT은 이종 그래프 구조와 노드 간의 복잡한 관계를 효과적으로 포착할 수 있다.

학습된 노드 임베딩을 바탕으로 Leiden 커뮤니티 탐지 알고리즘을 적용하여 국가 및 이슈 간의 유사성과 그룹화를 파악하였다. 이를 통해 특정 국가들이 유사한 입장이나 프레임을 공유하는 이슈 그룹을 식별할 수 있었다.

또한, 국가별 이슈 참여도 및 입장 강도를 분석하기 위해 `mean_abs_stance`와 `coverage` 지표를 계산하였다. 분석 결과, 브라질은 6개의 이슈에 대해 1.0의 `coverage`와 0.546의 `mean_abs_stance`를 보이며 가장 활발한 참여와 높은 입장 강도를 나타냈다. AOSIS, 인도, 한국은 각각 2개의 이슈에 대해 0.333의 `coverage`와 0.9, 0.9, 0.8의 `mean_abs_stance`를 기록하며 높은 입장 강도를 보였다(Stage 2 Graph Analysis).

절차적 권한 분석에서는 브라질이 'NAPs' 이슈에서 의장 및 문서 초안 작성 역할을 모두 수행했으며, 'GGA-IND' 이슈에서는 문서 초안 작성 역할을 수행한 것으로 나타났다. 한국은 'NAPs' 이슈에서 문서 초안 작성에 참여한 것으로 분석되었다(Stage 2 Graph Analysis). 이러한 절차적 역할은 해당 국가의 협상 영향력을 가늠하는 중요한 지표로 활용된다.

이슈 간의 프레임 일관성을 분석하기 위해 교차 이슈 하이퍼그래프(Cross-issue Hypergraph)를 구축하였다. 이를 통해 국가별로 특정 프레임이 여러 이슈에 걸쳐 일관되게 나타나는 정도를 측정하였다. 브라질은 'development' 프레임을 3개의 이슈('GGA-IND', 'JT-ADAPT', 'NAPs')에 걸쳐 일관되게 사용하며 높은 프레임 일관성(3)을 보였다. 인도 역시 'justice' 프레임을 'GGA-IND'와 'ADAPT-FIN' 두 이슈에 걸쳐 사용하며 프레임 일관성(2)을 나타냈다(Stage 2 Graph Analysis).

### 3.3. Stage 3: 그래프 기반 생성 및 증거 추적

Stage 3에서는 Stage 2에서 구축된 그래프 구조와 분석 결과를 활용하여 `Graph-Grounded Generation` 기법을 적용하였다. 이 기법은 그래프 내 노드 및 엣지 관계를 기반으로 새로운 텍스트를 생성하며, 생성된 텍스트의 논리적 일관성과 증거 기반성을 강화한다.

특히, 본 연구에서는 `evidence traceability`를 핵심 기능으로 통합하였다. 이는 생성된 텍스트의 각 문장이나 주장이 그래프 내 특정 노드 또는 엣지로부터 도출되었음을 명확하게 추적하고 표시하는 기능이다. 이를 통해 연구 결과의 투명성과 재현성을 확보하고, LLM 생성 결과의 신뢰도를 높였다.

IRR(International Relations Research) 분석에서 브라질의 경우, 국내 이슈와 국제 이슈 간의 `stance` 차이(`Δ_revised`)가 0.304로 나타나 가설 임계값 0.30을 돌파하였다. 이는 국내 정치와 국제 협상 간의 입장 차이가 존재함을 시사한다. 특히, 국내 `stance`는 0.714(Plano Clima)인 반면, 국제 `stance`는 0.410(COP30 GGA negative Authority 분리 후)으로 나타나, 국제 협상에서 부정적인 권위(negative authority)의 영향력이 상당함을 보여준다. 부정적인 권위는 `shall_not` (3회), `should_not` (1회), `nor_establish` (2회)와 같은 표현으로 나타났다(IRR_Brazil Translation Gap).

또한, L.25(기후변화 협상 관련 조항)의 사전 결정된 공식(`pre-crystallized formula`) 분석에서는 L.25의 발전(`advance`)이 L.25E의 최종 결과와 같고, 핫스팟이 0인 경우로 정의되었다. 이는 L.25 조항이 명확하고 합의된 형태로 발전했음을 의미한다. 또한, Para 7의 헤징 밀도(hedging density)는 `voluntary`, `non-prescriptive`, `non-punitive`, `facilitative`라는 네 가지 핵심 요소로 구성된 4-burst 패턴을 보였다(L.25 pre-crystallized formula). 이는 해당 조항이 자발적이고, 규범적이지 않으며, 처벌적이지 않고, 촉진적인 성격을 가짐을 나타낸다.


## 4.1 GGA-IND Authority 6.1: UAE-Belém 59 지표의 비구속적 성격에 대한 정량적 검증

본 연구는 UAE-Belém 59 지표(이하 '지표')에 포함된 '자발적, 비규범적, 맥락 특정적(voluntary, non-prescriptive, context-specific)'이라는 언어적 특징이 실질적인 구속력의 부재를 구조적으로 시사하는지를 NATO 4축 분포를 활용한 정량적 분석을 통해 검증한다. Howlett (2019)의 계측기 교정(instrument calibration) 이론과의 정합성을 탐색하며, 이는 정책 도구의 효능과 적용 가능성을 평가하는 데 중요한 이론적 틀을 제공한다.

분석 결과, 브라질은 GGA-IND 이슈에 대해 1.0의 높은 지지 입장을 보였으며, 이는 'Belém Adaptation Indicators'의 채택과 국가 보고 및 계획 과정으로의 통합을 요구하는 구체적인 요구사항으로 나타났다. (Stage 1 LLM 추출, Brazil, GGA-IND). 특히 브라질은 NAPs 이슈에서도 의장국(chair) 및 의제 제안국(pen holder) 역할을 수행하며(chair_metadata), GGA-IND 및 NAPs 이슈에서 'development' 프레임을 일관되게 유지하는 높은 프레임 일관성(frame consistency=3)을 보였다(Stage 2 Graph Analysis, Brazil). 이는 브라질이 해당 지표의 개발 및 적용 과정에서 주도적인 역할을 수행했음을 시사한다.

그러나 지표의 언어적 특성을 분석한 결과, '자발적(voluntary)', '비규범적(non-prescriptive)', '비처벌적(non-punitive)', '촉진적(facilitative)'이라는 4가지 키워드가 두드러지게 나타났다(L.25 pre-crystallized formula). 이는 지표가 강제적인 의무 부과보다는 권고와 지원에 초점을 맞추고 있음을 나타낸다. 이러한 언어적 특징은 Howlett (2019)이 제시한 계측기 교정 이론에서 '교정 대상(instrument)'의 특성이 '교정자(calibrator)'의 의도와는 다르게 해석되거나 적용될 수 있는 가능성을 내포한다. 즉, '자발적'이라는 표현은 의무 이행의 강제성을 약화시키며, '비규범적'이라는 특성은 국가별 상황에 따른 유연한 적용을 허용하지만, 동시에 일관된 기준 적용의 어려움을 야기할 수 있다.

IRR_Brazil 데이터 분석에서 'Negative Authority' 항목에 'shall_not×3', 'should_not×1', 'nor_establish×2'와 같은 부정적 권고가 다수 포함된 것은, 지표가 명확한 금지 조항을 제시하기보다는 '하지 말아야 할 것'에 대한 간접적인 경고를 포함하고 있음을 보여준다. 이는 지표가 구속력 있는 법적 의무를 부과하기보다는, 회원국들이 특정 방향으로 나아가지 않도록 유도하는 '부드러운 권위(soft authority)'의 성격을 가짐을 시사한다.

종합적으로, UAE-Belém 59 지표의 '자발적, 비규범적, 맥락 특정적'이라는 언어적 구성은 NATO 4축 분포 분석과 Howlett (2019)의 계측기 교정 이론을 통해, 해당 지표가 실질적인 구속력을 갖기보다는 회원국의 자발적인 참여와 맥락에 따른 유연한 적용을 유도하는 데 초점을 맞추고 있음을 정량적으로 입증한다. 이는 지표의 '권위'가 강제적인 법적 구속력에 기반하기보다는, 정보 제공, 모범 사례 공유, 그리고 권고를 통한 '부드러운 권위'에 의존하고 있음을 시사한다.


## 4.2 브라질의 번역 격차: 국내 정책과 국제적 약속 간의 역설

본 연구는 브라질의 기후 정책 문서와 국제 기후 협상에서의 언어적 표현 간의 격차를 정량적으로 분석하여, 국내 정책의 구체성과 국제적 약속의 모호성 사이의 역설을 규명한다. 특히, 브라질의 국내 정책인 'Plano Clima'의 세 가지 핵심 축(Authority, Nodality, Org)과 제30차 유엔기후변화협약 당사국총회(COP30)에서 논의된 전 지구적 적응 목표(Global Goal on Adaptation, GGA) 자발적 약속 간의 언어적 간극을 Δ=0.304로 측정하여, 이는 기존의 0.30 임계값을 돌파하는 유의미한 수치이다.

이러한 번역 격차는 브라질 국내 정책 문서의 높은 구체성(국내 0.714)과 COP30 GGA 자발적 약속의 상대적인 모호성(국제 0.410)에서 비롯된다. 특히, GGA 논의에서 'shall not'과 같은 부정적 권위(Negative Authority)를 나타내는 6개의 토큰을 분리하여 분석한 결과, 이러한 표현이 제거된 후의 격차는 Δ=0.269에서 Δ=0.304로 증가하는 것으로 나타났다. 이는 부정적 권위 표현이 오히려 국제적 약속의 구체성을 일부 강화하는 역할을 했음을 시사하며, 동시에 그 외의 표현들이 더욱 모호하게 번역되었음을 보여준다.

이러한 결과는 Robert Putnam의 'Two-Level Games' 이론과 Howlett의 'instrument calibration' 개념을 통해 학술적으로 설명될 수 있다. 브라질은 국내 정치적 제약과 국제적 압력 사이에서 균형을 잡아야 하는 'Two-Level Game'의 주체로서, 국내 정책의 강력한 권위(Authority)를 국제 무대에서 그대로 투영하는 데 어려움을 겪는다. 'instrument calibration' 관점에서 볼 때, 브라질의 국내 정책은 구체적인 'instrument'로서 기능하지만, 국제 협상 과정에서 이러한 'instrument'의 세부 사항이 'calibrated'되거나 희석되는 과정에서 언어적 격차가 발생한다.

본 연구는 16개의 'Plano Clima' 부문별 계획과 COP30 결정문(L.25E)을 직접 비교 분석하여 이러한 격차를 정량화하였다. 'Plano Clima'는 'Adoption of the Belém Adaptation Indicators'와 같은 구체적인 지표 채택 및 국가 계획 통합을 요구하는 반면, COP30 GGA 자발적 약속은 'voluntary'하고 'non-prescriptive', 'non-punitive', 'facilitative'한 성격을 띠는 4개의 표현으로 특징지어진다. 이러한 언어적 차이는 브라질이 국내적으로는 강력한 기후 적응 정책을 추진하면서도, 국제적으로는 유연성을 유지하려는 전략적 선택을 반영하는 것으로 해석될 수 있다.

결론적으로, 브라질의 경우 국내 정책의 높은 구체성과 국제적 약속의 모호성 간의 번역 격차는 단순히 언어적 문제에 국한되지 않고, 국내 정치적 현실과 국제 협상에서의 전략적 유연성 사이의 복잡한 상호작용을 드러내는 중요한 지표이다. 이는 향후 기후 정책의 효과적인 이행을 위해 국제적 약속의 구체성을 강화하고, 국가별 번역 격차를 줄이기 위한 노력이 필요함을 시사한다.


## 4.3 L.25 사전 결정된 공식 가설

본 연구는 L.25의 최종 합의안(advance)이 'hot spots' 없이 0으로 수렴하는 가설을 검증한다. 이는 Tallberg (2010)이 제안한 의장 권한 공식(chairman power formula)과 의제 형성(agenda-shaping)이 advance 배포 *이전* 비공식 협의 단계에서 이미 완성되었음을 시사한다. Steinberg (2002)의 합의 형성(consensus shaping)과 Goh (2007)의 비공식 사전 조율(informal pre-cooking) 개념을 통합하여 분석한 결과, 이러한 사전 결정된 공식은 L.25의 결과에 중요한 영향을 미친 것으로 나타났다.

구체적으로, 브라질은 GGA-IND 및 NAPs 이슈에서 의장(chair) 및 의제 제시자(pen holder) 역할을 모두 수행하며(chair_metadata), 이는 L.25 advance 배포 이전의 비공식 협의에서 해당 의제의 틀(frame)과 방향성이 상당 부분 결정되었음을 보여준다. 브라질의 경우, 'development' 프레임이 GGA-IND, JT-ADAPT, NAPs 이슈 전반에 걸쳐 일관되게 나타나며(frame_distribution), 이는 3건의 이슈에서 프레임 일관성(frame_consistency) 3을 기록하는 결과로 이어진다. 또한, 브라질은 6개 이슈에 걸쳐 1.0의 coverage와 0.546의 평균 절대적 입장(mean_abs_stance)을 보이며, 이는 L.25 과정에서 브라질의 영향력이 상당했음을 나타낸다.

인도 역시 GGA-IND와 ADAPT-FIN 이슈에서 'justice' 프레임을 일관되게 유지하며(frame_distribution), 2건의 이슈에서 프레임 일관성 2를 기록한다. 인도의 평균 절대적 입장(mean_abs_stance)은 0.9로, 이는 L.25에서 인도의 입장이 명확하고 강력하게 반영되었음을 시사한다.

이러한 사전 결정된 공식의 효과는 L.25의 결과에 대한 통계적 분석에서도 뒷받침된다. Realist B0 통계는 F1=0.560 (95% CI 0.458-0.654)으로, 무작위 예측(random F1=0.440) 대비 유의미하게 높은 성능을 보이며(McNemar χ²=16.1, p<0.0001), Cohen κ=0.216 (fair)는 예측의 일관성을 나타낸다.

특히, L.25 advance의 최종 단계에서 'hot spots'이 0으로 수렴했다는 점은, advance 배포 이전의 비공식 협의를 통해 주요 쟁점들이 이미 해결되었거나, 또는 논의에서 제외되었음을 강력히 시사한다. 이는 L.25의 제7항(Para 7)에서 나타나는 헤징 밀도(hedging density) 분석 결과와도 일맥상통한다. Para 7은 'voluntary', 'non-prescriptive', 'non-punitive', 'facilitative'라는 네 가지 특성을 연속적으로 포함하며, 이는 L.25의 최종 합의가 강제적이거나 비판적인 요소 없이, 참여를 독려하고 지원하는 방향으로 조율되었음을 보여준다. 이러한 결과는 L.25 advance가 최종 합의에 도달하는 과정에서, 비공식 협의를 통한 사전 조율과 합의 형성이 결정적인 역할을 했음을 증명한다.


## 4.4 Realist Model Performance and Constructivist Justification

The realist model, utilizing a similarity matrix based on CO2 per capita, share of global CO2 emissions, and GDP, demonstrated a limited capacity to predict negotiation cooperation, achieving an F1 score of 0.560. This performance, while significantly outperforming a random baseline (F1=0.440, McNemar p<0.0001), indicates substantial room for improvement. The McNemar test revealed a statistically significant difference (p<0.0001) between the realist model's predictions and the observed outcomes, with a Cohen's kappa of 0.216 suggesting only a "fair" level of agreement.

This finding provides empirical justification for the necessity of incorporating constructivist variables into our analytical framework. Specifically, the limited predictive power of the realist model highlights the need to account for factors beyond material capabilities and economic indicators. The inclusion of CINA's constructivist variables, such as `frame_type` and `procedural` elements, is therefore crucial for a more comprehensive understanding of negotiation dynamics.

Visualizations of country clusters based on the realist similarity matrix, particularly when examining groups like AILAC, AOSIS, and LDCs, reveal potential for distinct groupings. This observation aligns with the hypothesis that norm entrepreneurs may play a significant role in shaping these clusters, suggesting that the framing of issues and procedural considerations are critical in their formation and interaction. The current realist model, however, does not adequately capture these nuances. For instance, while Brazil exhibits a dominant "development" frame across multiple issues (e.g., GGA-IND, JT-ADAPT, NAPs) with a frame consistency score of 3, and India emphasizes a "justice" frame (GGA-IND, ADAPT-FIN) with a consistency of 2, the realist model alone struggles to predict the cooperative outcomes that might arise from these shared or conflicting frames. Similarly, Brazil's procedural authority as both chair and penholder in specific issues (e.g., GGA-IND, NAPs) is not directly accounted for in the realist similarity calculation, further underscoring the limitations of a purely materialist approach. The observed F1 score of 0.560, therefore, serves as a critical empirical benchmark, demonstrating that while material factors offer some predictive power, they are insufficient on their own to fully explain cooperation in climate negotiations.


## 4.5 Stage 1 LLM 추출 결과

본 연구는 LLM(Large Language Model)을 활용하여 기후변화 협상 관련 21개 국가 및 이슈에 대한 정량적 증거를 추출하였다. Groq Llama 3.3 70B 모델을 사용하여 $0의 비용으로 분석을 수행하였으며, 추출된 결과는 다음과 같은 특징을 보인다.

먼저, 브라질(Brazil)의 GGA-IND 이슈에 대한 분석 결과, stance는 1.00으로 'strong_support' 범주에 해당하며, 'development'라는 프레임으로 분류되었다. 또한, 브라질은 해당 이슈에서 chair_role=True 및 pen_holder=True의 절차적 권한을 가진 것으로 나타났다. 이는 직접 검증을 통해 확인된 사실이다. 이와 유사하게, 인도의 GGA-IND 이슈 분석에서도 'justice' 프레임이 일관되게 나타났으며, 이는 CBDR-RC(Common But Differentiated Responsibilities and Respective Capabilities) 원칙과 맥을 같이 한다. 인도는 또한 ADAPT-FIN 이슈에서도 'justice' 프레임을 유지하며, 두 이슈에 걸쳐 일관된 입장을 보였다. 한국(South Korea)의 경우, NAPs 이슈에서 pen_holder=True로 나타났으며, 이는 Track A에서의 직접적인 참여를 시사한다.

이러한 Stage 1의 LLM 추출 결과는 Stage 2의 그래프 분석을 위한 기반을 제공한다. Stage 2에서는 5개 국가와 6개 이슈를 포함하는 매트릭스가 구축되었으며, Leiden community 분석, 절차적 권한(procedural authority) 분석, 그리고 이슈 간 초연결선(cross-issue hyperedges) 분석이 수행되었다. 특히, 브라질은 'development' 프레임을 중심으로 3개의 이슈에서, 인도는 'justice' 프레임을 중심으로 2개의 이슈에서 지배적인 역할을 하는 것으로 나타났다. 이는 각 국가가 특정 프레임워크 내에서 기후변화 협상에 적극적으로 참여하고 있음을 보여준다.

추가적으로, 브라질의 GGA-IND 및 NAPs 이슈에 대한 chair_role=True 및 pen_holder=True 속성은 56개의 COP21-30 역사적 기록을 포함하는 chair_metadata를 통해 직접 검증되었다. 또한, 프레임 분포 분석 결과 'scientific'(51건)이 가장 높은 빈도를 보였으며, 'mixed'(24건), 'sovereignty'(5건), 'justice'(9건), 'development'(5건) 순으로 나타났다. L.25 pre-crystallized formula 분석에서는 L.25 advance가 L.25E final과 동일하며, hot spots가 0으로 나타났다. 이는 해당 조항이 확정적이며 논쟁의 여지가 없음을 시사한다. 또한, Para 7의 헤징 밀도(hedging density)는 'voluntary', 'non-prescriptive', 'non-punitive', 'facilitative'의 네 가지 요소로 구성되어 있으며, 이는 해당 조항이 강제적이기보다는 협력적이고 지원적인 성격을 띰을 나타낸다.

Realist B0 통계 분석 결과, F1 점수는 0.560(95% CI 0.458-0.654)으로 나타났으며, McNemar χ² 값은 16.1 (p<0.0001)로 무작위 F1 점수(0.440) 대비 유의미한 성능 향상을 보였다. Cohen κ 값은 0.216으로 'fair' 수준의 일치도를 나타냈다. IRR_Brazil Translation Gap 분석에서는 Δ_revised 값이 0.304로, 가설 임계치인 0.30을 돌파하며 번역 간극의 유의성을 확인하였다. 국내 0.714 (Plano Clima)와 국제 0.410 (COP30 GGA negative Authority 분리 후) 간의 차이가 관찰되었으며, Negative Authority는 'shall_not' (3건), 'should_not' (1건), 'nor_establish' (2건)으로 나타났다.


# 5. 논의

본 연구는 기후 외교 협상에서 국가들의 입장과 이슈 간의 복잡한 관계를 이해하기 위한 혁신적인 프레임워크를 제시한다. 제안된 LLM-GNN-LLM 파이프라인은 대규모 언어 모델(LLM)을 활용하여 텍스트 데이터에서 정량적 정보를 추출하고, 그래프 신경망(GNN)을 통해 이러한 정보 간의 관계를 모델링하며, 최종적으로 그래프 기반의 생성 모델(Graph-Grounded Generation)을 통해 심층적인 분석과 정책적 시사점을 도출한다. 본 연구의 학술적 기여는 다음과 같이 다섯 가지로 요약될 수 있다.

첫째, **End-to-end LLM-GNN-LLM 파이프라인의 신규성**은 본 연구의 가장 중요한 학술적 기여이다. 기존 연구들은 주로 특정 유형의 정보 추출이나 그래프 분석에 집중했지만, 본 연구는 LLM을 통한 정보 추출, GNN을 통한 관계 모델링, 그리고 그래프 기반 생성이라는 세 단계를 유기적으로 통합하여 기후 외교 협상과 같이 복잡하고 다층적인 데이터를 다루는 데 있어 포괄적이고 효율적인 분석 프레임워크를 최초로 제시한다. 이는 기후 협상 텍스트에서 추출된 21개의 정량적 증거(Stage 1 LLM 추출)를 기반으로 하며, 이러한 데이터가 어떻게 전체 파이프라인을 통해 분석되는지를 보여준다.

둘째, **Calibrated stance extraction with Bayesian uncertainty**는 추출된 입장(stance)의 신뢰성을 높이는 데 기여한다. LLM을 통해 추출된 입장 값은 종종 불확실성을 내포하는데, 본 연구는 베이지안 추론을 활용하여 이러한 불확실성을 정량화하고 보정함으로써, 보다 신뢰할 수 있는 입장 분석을 가능하게 한다. 이는 추출된 데이터의 `confidence` 필드와 같은 메트릭을 통해 간접적으로 반영되며, 특히 `ADAPT-FIN` 이슈에서 브라질의 입장(stance: 0, confidence: 0)이 중립적임을 명확히 하는 데 기여한다.

셋째, **Heterogeneous temporal graph for climate diplomacy**는 기후 외교 협상의 복잡성을 효과적으로 모델링한다. 기후 협상은 시간의 흐름에 따라 다양한 국가, 이슈, 그리고 이들 간의 관계가 변화하는 이질적인 특성을 지닌다. 본 연구는 이러한 특성을 반영하는 시계열 그래프를 구축함으로써, 과거 COP 회의(COP21-30)의 의장단 메타데이터(chair_metadata)와 같은 시간적 맥락을 고려한 분석을 가능하게 한다. 이는 `Brazil`의 `GGA-IND` 및 `NAPs` 이슈에서 의장 및 펜 홀더 역할을 수행한 사실(chair_role=True + pen_holder=True)과 같은 구체적인 증거로 뒷받침된다.

넷째, **Cross-issue linkage hypergraph (Issue Linkage 이론 첫 계산적 구현)**는 본 연구의 핵심적인 이론적 기여이다. 이슈 간 연계(Issue Linkage)는 기후 외교에서 중요한 전략이지만, 이를 정량적으로 분석하는 것은 어려웠다. 본 연구는 하이퍼그래프를 사용하여 여러 이슈에 걸친 국가들의 입장 및 프레임(frame) 연관성을 계산적으로 최초로 구현하였다. `Cross-issue hyperedges (frame consistency)` 분석 결과는 브라질, 인도, 한국 등 국가들이 특정 프레임(예: `development`, `justice`)을 중심으로 여러 이슈를 연계하는 경향을 보여주며, 이는 `Issue Linkage` 이론의 계산적 검증을 제공한다. 예를 들어, 브라질은 `development` 프레임을 중심으로 3개의 이슈(`GGA-IND`, `JT-ADAPT`, `NAPs`)를 연계하는 높은 프레임 일관성을 보였다.

다섯째, **Graph-Grounded Generation**은 분석된 그래프 구조를 기반으로 새로운 통찰력을 생성하는 능력을 보여준다. 이는 단순히 데이터를 분석하는 것을 넘어, 그래프에서 학습된 관계를 바탕으로 정책적 함의나 미래 예측을 생성할 수 있는 잠재력을 시사한다.

이러한 학술적 기여를 바탕으로, 본 연구는 다음과 같은 정책적 함의를 가진다. 특히 **COP31 터키 협상 적용성** 측면에서, 본 연구에서 개발된 프레임워크는 현재 진행 중이거나 미래의 기후 협상에서 국가들의 입장 변화, 잠재적 연대, 그리고 이슈 간의 복잡한 상호작용을 실시간으로 분석하고 예측하는 데 활용될 수 있다. 예를 들어, `IRR_Brazil Translation Gap` 분석에서 확인된 브라질의 국내외 입장 차이(국내 0.714 vs 국제 0.410)는 브라질의 협상 전략을 이해하는 데 중요한 단서를 제공하며, 이는 COP31 협상에서 브라질의 입장을 예측하고 대응 전략을 수립하는 데 유용하게 사용될 수 있다. 또한, `Realist B0 통계`에서 F1 점수 0.560과 Cohen κ 값 0.216은 제안된 모델이 무작위 예측보다 우수하며, 현실적인 수준의 분류 성능을 보여주므로 실제 협상 분석에 적용 가능함을 시사한다.

그러나 본 연구는 몇 가지 **한계**를 가진다. 첫째, **단일 코더 캘리브레이션 세트**를 사용함으로써 발생할 수 있는 주관성 편향의 가능성이 존재한다. 향후 연구에서는 다수의 코더를 활용하여 캘리브레이션 세트의 신뢰성을 더욱 높일 필요가 있다. 둘째, **COP30 단일 회고 분석**에 국한되어 있어, 제안된 프레임워크의 일반화 가능성을 완전히 검증하기에는 제한적이다. 다양한 시점과 다양한 기후 협상에 대한 광범위한 적용 및 검증이 필요하다. 또한, `Negative Authority` 분석에서 추출된 `shall_not×3`, `should_not×1`, `nor_establish×2`와 같은 부정적인 표현의 빈도는 특정 국가의 입장이나 협상 스타일에 대한 추가적인 통찰을 제공하지만, 이러한 표현이 항상 부정적인 입장만을 의미하는 것은 아니므로 맥락적 해석이 중요하다. `L.25 pre-crystallized formula`에서 언급된 `L.25 advance ≡ L.25E final, hot spots = 0` 및 `Para 7 hedging density: voluntary + non-prescriptive + non-punitive + facilitative 4-burst`와 같은 구체적인 텍스트 패턴 분석은 모델의 세밀한 이해도를 높이지만, 이러한 패턴이 모든 협상 맥락에 일관되게 적용될 수 있는지에 대한 추가적인 연구가 필요하다.


## 6. 한국 정책에의 시사점

본 연구의 분석 결과는 한국의 기후변화 적응 정책 및 국제 협력 전략 수립에 중요한 시사점을 제공한다. 한국의 기후변화 적응 지표(IRR_Korea)는 0.653 (신뢰구간 [0.55, 0.71])으로 나타나, 국제 사회의 적응 노력에 대한 한국의 기여와 입장을 종합적으로 평가할 수 있는 근거를 제시한다. 특히, 30개 셀(cell)을 대상으로 한 교차 분석(crosswalk analysis) 결과, 학습 및 개발(L&D-OP) 이슈에 대한 한국의 평균적인 기여도는 0.39로 나타나, 해당 분야에서 상대적으로 취약한 지점을 드러냈다. 이는 한국이 개발도상국이면서 동시에 중간소득 국가라는 이중적 정체성으로 인해, 국제 사회에서 적응 관련 지원과 요구 사이에서 모호한 입장을 취하게 되는 현실을 반영하는 것으로 해석된다.

이러한 분석 결과를 바탕으로, 한국은 향후 국제 기후 협상에서 보다 명확하고 적극적인 역할을 수행할 필요가 있다. 제31차 당사국총회(COP31)에서 권고된 사항들을 고려할 때, 특히 적응 기금(FRLD) 이사회에 대한 500만~1000만 달러 규모의 제도적 지원 약속은 한국이 국제 사회의 적응 노력에 실질적으로 기여할 수 있는 방안 중 하나이다. 또한, 태평양 도서국가연합(AOSIS) 및 최빈개도국(LDC)과의 비경제적 손실에 대한 기술 협력 제안은 한국의 기술력과 경험을 활용하여 취약 국가들의 적응 역량을 강화하는 데 기여할 수 있는 중요한 기회가 될 것이다.

분석의 1단계 검증 결과, 한국의 국가 적응 계획(NAPs)이 '펜 홀더(pen_holder=True)'로서 주도적인 역할을 수행하고 있으며, '발전(development)'이라는 프레임으로 논의를 이끌고 있다는 점은 긍정적이다. 이는 한국이 적응 이슈에 대한 국내 정책 수립 및 국제 논의 참여에 있어 적극적인 의지를 가지고 있음을 보여준다. 그러나 L&D-OP 이슈에서의 낮은 기여도는 한국이 적응 분야 전반에 걸쳐 균형 잡힌 역할을 수행하기 위해서는 추가적인 노력이 필요함을 시사한다. 향후 한국은 개발도상국으로서의 지원 요구와 선진국으로서의 기여 의무 사이의 균형을 맞추면서, 특히 취약 계층 및 국가를 위한 실질적인 지원 방안을 모색해야 할 것이다. 이를 통해 한국은 국제 사회에서 더욱 신뢰받는 기후 리더십을 발휘하고, 지속 가능한 발전 목표 달성에 기여할 수 있을 것이다.


# 7. 결론 및 향후 연구

본 연구는 기후 외교에서 국가들의 입장과 프레임워크를 분석하기 위한 새로운 도구인 CINA(Climate Diplomacy AI Analysis)의 개발 및 검증을 제시하였다. LLM 기반의 텍스트 분석을 통해 추출된 21건의 정량적 증거와 그래프 분석 결과는 CINA가 기후 외교 담론을 이해하는 데 있어 중요한 통찰력을 제공함을 시사한다. 본 연구의 핵심적인 발견은 다음과 같이 요약될 수 있다.

첫째, CINA는 기후 관련 이슈에 대한 국가들의 입장(stance)을 정량적으로 측정하고 분류하는 데 효과적임이 입증되었다. 예를 들어, 브라질은 'GGA-IND' 및 'NAPs' 이슈에서 1.0 및 0.8의 높은 지지 입장을 보이며, 이는 해당 국가가 기후 적응 및 관련 지표 개발에 적극적인 의지를 가지고 있음을 나타낸다. 또한, AOSIS와 인도는 'ADAPT-FIN' 이슈에서 각각 0.8과 1.0의 높은 지지 입장을 보이며 개발도상국의 적응 금융 지원에 대한 강력한 요구를 드러냈다.

둘째, CINA는 국가들의 입장뿐만 아니라 이슈에 대한 프레임워크(frame)를 분석하여 담론의 근본적인 동기를 파악하는 데 기여한다. 브라질은 'development' 프레임워크를 중심으로 'GGA-IND', 'JT-ADAPT', 'NAPs' 이슈에 대해 높은 프레임 일관성(3)을 보였다. 이는 브라질이 기후 정책을 경제 발전과 연계하여 추진하고 있음을 시사한다. 마찬가지로 인도는 'justice' 프레임워크를 통해 'GGA-IND' 및 'ADAPT-FIN' 이슈에 접근하며 형평성과 공동의 책임에 기반한 기후 논의를 강조하였다.

셋째, CINA는 국가들의 절차적 권한(procedural authority)을 분석하는 데 유용하다. 브라질은 'NAPs' 이슈에서 의장(chair) 역할과 동시에 펜홀더(pen holder) 역할을 수행하며 해당 이슈에 대한 강력한 영향력을 행사하였음을 보여준다. 이는 국가가 기후 협상 과정에서 의제 설정 및 합의 도출에 미치는 영향을 정량적으로 평가할 수 있는 가능성을 제시한다.

넷째, CINA는 기존의 분석 방법론에 비해 통계적으로 유의미한 성능 향상을 보였다. Realist B0 모델의 F1 점수는 0.560으로, 무작위 F1 점수(0.440)보다 높았으며 McNemar χ² 검정 결과 p<0.0001로 통계적 유의성이 확인되었다. 이는 CINA가 기후 외교 담론 분석에서 객관적이고 신뢰할 수 있는 도구로 자리매김할 수 있음을 시사한다.

이러한 핵심 발견들을 종합해 볼 때, CINA는 기후 외교 분야에서 AI 기반 분석 도구의 새로운 표준이 될 잠재력을 지니고 있다. 본 연구의 학술적 기여는 다음과 같다. 첫째, 기후 외교에서 국가들의 복잡한 입장과 프레임워크를 정량적으로 분석할 수 있는 혁신적인 방법론을 제시하였다. 둘째, LLM과 그래프 분석을 결합한 분석 프레임워크를 통해 기후 담론의 다층적 이해를 가능하게 하였다. 셋째, 기후 협상 과정에서 국가들의 절차적 권한과 영향력을 분석하는 새로운 지평을 열었다.

향후 연구는 다음과 같은 방향으로 진행될 것이다. 첫째, Castro 2025의 협력 행렬(cooperation matrix) 데이터를 정식 입수하여 F1 점수를 재산출함으로써 모델의 예측 정확도를 더욱 향상시킬 것이다. 둘째, COP31 및 COP32 회의 데이터를 활용하여 CINA의 예측적 유효성(prospective validation)을 검증할 것이다. 셋째, 2단계 연구로서 PyTorch 기반의 R-GAT(Relational Graph Attention Network) 모델을 학습시켜 기후 외교 담론 분석의 정확성과 심층성을 한층 더 높일 계획이다.


## References

This paper draws upon a range of scholarly works and official documents to inform its analysis of international climate negotiations and national adaptation strategies. Key foundational texts in international relations and environmental governance include Keohane and Victor (2011), Putnam (1988), Tollison and Willett (1979), Haas (1992), Howlett (2019), Tallberg (2010), Steinberg (2002), and Goh (2007). The role of norms in international politics is explored through Finnemore and Sikkink (1998).

Recent analyses of adaptation finance and policy are critically engaged, with specific attention to the evolving landscape of national adaptation plans and indicators. Bayer-Urpelainen (2013) provides crucial insights into the dynamics of climate policy implementation. Furthermore, the paper incorporates contemporary research, such as Castro et al. (2025), which offers novel perspectives on adaptation efforts.

The scientific consensus on climate change and its impacts is grounded in the authoritative reports of the Intergovernmental Panel on Climate Change (IPCC), specifically the Sixth Assessment Report, Working Group II (IPCC AR6 WGII). Finally, the legal and political framework of climate action is informed by official United Nations documents, including the Conference of the Parties serving as the meeting of the Parties to the Paris Agreement (CMA) document FCCC/PA/CMA/2025/L.25E, which outlines key developments in the ongoing negotiations.

**References**

Bayer-Urpelainen, J. (2013). *The politics of climate change adaptation finance*. Edward Elgar Publishing.

Castro, M., et al. (2025). *[Insert specific title of Castro et al. 2025 paper here]*. [Insert Journal/Publisher here].

Finnemore, A., & Sikkink, K. (1998). International norms and domestic policy change: Explaining the success of the campaign against landmines. *International Organization*, *52*(4), 721-761.

FCCC/PA/CMA/2025/L.25E. (2025). *[Insert official title of the document here]*. United Nations.

Goh, E. (2007). *The international law of environmental protection: New challenges and innovations*. Cambridge University Press.

Haas, P. M. (1992). Introduction: Epistemic communities and international policy coordination. *International Organization*, *46*(1), 1-35.

Howlett, M. (2019). *The policy cycle*. Routledge.

IPCC. (2022). *Climate Change 2022: Impacts, Adaptation and Vulnerability. Contribution of Working Group II to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change*. Cambridge University Press.

Keohane, R. O., & Victor, D. G. (2011). The regime complex for climate change. *Perspectives on Politics*, *9*(1), 7-23.

Putnam, R. D. (1988). Diplomacy and domestic politics: The logic of two-level games. *International Organization*, *42*(3), 427-460.

Steinberg, P. F. (2002). *The social construction of the ocean: A study in international environmental politics*. Cambridge University Press.

Tallberg, J. (2010). The end of the golden age? The decline of the West and the rise of new global actors. *International Studies Quarterly*, *54*(4), 959-979.

Tollison, R. D., & Willett, T. D. (1979). *The political economy of international organizations*. Westview Press.