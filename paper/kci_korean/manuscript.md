---
title: "이행률 기반 한국 적응정책의 글로벌 정합도 진단 — 다축 LLM 추출 프레임워크 적용 사례"
running_title: "한국 적응정책의 글로벌 정합도 진단"
author:
  - name: "최희도 (Heedo Choi)"
    affiliation: "국민대학교 일반대학원 기후기술융합학과"
    email: "zxsa0716@kookmin.ac.kr"
    orcid: "(등록 예정)"
target_journal: "한국정책학회보 (Korean Policy Studies Review)"
journal_grade: "KCI 우수등재"
manuscript_type: "단저자 일반논문"
expected_pages: 25
language: "한국어 (영문 초록 병기)"
status: "draft v1.0 — 2026-05-07"
license: "CC BY 4.0 (manuscript) / MIT (code)"
---

# 이행률 기반 한국 적응정책의 글로벌 정합도 진단 — 다축 LLM 추출 프레임워크 적용 사례

## 국문 초록 (300자 이내)

본 연구는 LLM(대규모 언어모델) 기반 다축 stance 추출 프레임워크 CINA(Climate Issue-Network Analysis)를 활용하여, 한국의 국가적응계획(NAP)과 COP30 채택 글로벌적응목표(Global Goal on Adaptation, GGA)의 7개 thematic targets 사이의 정합도를 30-cell crosswalk로 정량 진단하였다. 분석 결과 한국의 종합 이행률(Implementation Readiness Ratio, IRR)은 0.653(95% 신뢰구간 [0.55, 0.71])로 채택 가능 수준에 해당하나, 손실·피해 영역(L&D-OP × 사회·경제 적응)은 0.39로 가장 낮으며 이는 환경건전성그룹(EIG) 회원국이자 중상위 소득기여국이라는 한국의 이중 정체성 모호성에 기인한다. 본 연구는 (1) 30-cell crosswalk 구축 절차, (2) NATO 4-axis 정책수단(Hood 1983; Howlett 2019) 자동 분류 결과, (3) COP31(튀르키예, 2026.11) 협상을 위한 5개 정책 권고를 제시한다.

**주제어**: 기후변화 적응정책, 국가적응계획, 글로벌적응목표, 이행률, 정책수단, COP30, COP31, LLM, 한국

---

## 1. 서론

### 1.1 연구 배경

2025년 11월 브라질 벨렘에서 개최된 제30차 유엔기후변화협약 당사국총회(COP30)는 적응 영역에서 두 건의 역사적 결정문을 채택하였다. 첫째, FCCC/PA/CMA/2025/L.25E는 글로벌적응목표(GGA)의 7개 thematic targets에 대한 59개 자발적·비강제적·비처벌적·촉진적(voluntary, non-prescriptive, non-punitive, facilitative) 지표 패키지를 합의하였다. 둘째, FCCC/PA/CMA/2025/L.24는 2035년까지 적응재원을 1,200억 달러로 3배 확대(triple)할 것을 결정하였다. 이 두 문서는 향후 5-10년간 한국 적응정책의 외교적·재정적 환경을 규정하는 기준점이 된다.

한국은 환경건전성그룹(EIG) 회원국으로서 스위스, 멕시코, 모나코, 리히텐슈타인, 조지아와 함께 중간자적 입장을 견지해 왔으나, GDP 기준 세계 12위·1인당 CO₂ 배출 상위국이라는 정체성이 동시에 작용하여 협상장에서 일관된 위치 선언이 어려운 구조적 모호성에 직면하고 있다. 이 모호성은 단순히 외교 현장의 문제가 아니라, 국내 적응정책 설계와 국제 협상 입장 사이의 정합도(coherence)를 체계적으로 진단해야 해소될 수 있는 정책학적 문제이다.

### 1.2 연구 문제와 기여

기존 한국 적응정책 연구는 (a) 국내 NAP의 부문별 이행성과를 평가하거나 (Korea Environment Institute 2024), (b) UNFCCC 협상장에서 한국의 발화 내용을 정성적으로 분석하는 (이태동 외 2024) 방식으로 이원화되어 있었다. 본 연구는 두 흐름을 결합하여, (i) 한국 NAP의 11개 부문 정책수단을 다축 LLM 추출로 정량 코딩하고, (ii) 동일한 다축 schema로 GGA 7개 targets의 정책수단 요구사항을 코딩한 후, (iii) 30-cell crosswalk(NAP 11 sectors × GGA 7 thematic targets, 적용 가능한 30개 cell)로 양자의 정합도를 측정하는 새로운 방법론을 제안한다.

본 연구의 정책학적 기여는 세 가지이다. 첫째, **이행률(IRR, Implementation Readiness Ratio)**이라는 단일 지표로 국내 정책과 국제 합의 사이의 정합도를 정량화한다. 둘째, NATO 4-axis 정책수단 분류(Hood 1983; Howlett 2019; Capano 외 2025) 위에서 한국의 약점 영역을 cell-level로 식별한다. 셋째, COP31 협상(튀르키예, 2026년 11월)을 위한 5개 구체적 정책 권고를 도출한다.

### 1.3 논문 구성

제2장은 정합도와 정책수단 calibration의 이론적 배경을 정리한다. 제3장은 CINA 다축 추출 프레임워크와 cross-LLM 신뢰도 측정 방법을 기술한다. 제4장은 30-cell crosswalk 구축과 IRR 측정 결과를 제시한다. 제5장은 가장 약한 cell(L&D-OP × 사회·경제 적응)의 진단과 EIG 회원국으로서의 외교 입지 분석을 제공한다. 제6장은 COP31을 위한 5개 정책 권고를 제시한다. 제7장은 한계와 향후 과제를 논한다.

---

## 2. 이론적 배경

### 2.1 정책 정합도(Policy Coherence) 개념

정책 정합도는 OECD(2019)가 "다층 거버넌스 환경에서 다양한 수준의 정부와 부문이 일관된 목표를 추구하도록 보장하는 체계적 노력"으로 정의한 개념이다. 기후 적응정책에서의 정합도는 (i) 국내 부처 간 정합도(horizontal), (ii) 중앙-지방 정합도(vertical), (iii) 국내-국제 정합도(international)의 3차원으로 분해되며 (Nilsson 외 2012), 본 연구는 세 번째 차원인 국내-국제 정합도에 초점을 둔다.

한국은 2050 탄소중립·녹색성장 기본법(2021) 제50조에 적응 의무를, 동법 시행령에 5개년 NAP 수립 의무를 명시하였다. 1차 NAP(2021-2025)와 2차 NAP(2026-2030, 환경부 2025년 12월 확정)는 11개 부문(농업, 산림, 해양·수산, 물관리, 보건, 산업·에너지, 국토·도시, 인프라, 생태계, 통합관리, 국제협력)으로 구성된다. 그러나 NAP의 부문 구성과 GGA의 7개 targets(물·위생, 식량·농업, 보건, 생태계·생물다양성, 인프라·정주, 빈곤·생계, 문화유산) 사이의 정합 관계는 공식 문서로 매핑된 적이 없다.

### 2.2 정책수단 calibration: NATO 4-axis 프레임워크

Hood(1983)는 정부가 정책 목표를 달성하기 위해 사용 가능한 자원을 4개 축으로 범주화하였다: **Nodality(정보·신호)**, **Authority(법적·규제 권한)**, **Treasure(재정·인센티브)**, **Organization(조직·인력·기관)**. Howlett(2019, 2nd ed.)은 이 프레임워크를 정책수단 calibration의 일반 이론으로 발전시켰으며, Capano 외(2025)는 이를 정량적 텍스트 분석에 적용하기 위한 코딩 프로토콜을 제시하였다.

본 연구는 이 4축 위에서 한국 NAP 텍스트와 GGA 결정문 텍스트를 동일한 LLM 프롬프트로 코딩하여, 양자의 정책수단 사용 패턴이 어느 정도 일치하는지 정량 측정한다. 이는 단순히 "정책 목표가 일치한다"는 진술을 넘어, "정책 목표 달성을 위해 어떤 도구를 어느 정도 비중으로 동원하고 있는가"의 calibration 차원에서의 정합도 진단을 가능하게 한다.

### 2.3 이중 정체성과 EIG의 외교적 위치

한국은 1996년 OECD 가입 이후 비부속서I 국가에서 부속서I 국가로 사실상 이행 중인 unique한 외교적 위치에 있다. EIG(Environmental Integrity Group) 6개국 중 한국과 멕시코는 G20 회원국이며, 스위스·리히텐슈타인·모나코는 유럽 강소국, 조지아는 신흥 경제국이다. 이 이질적 구성은 EIG의 협상력을 약화시키는 동시에 (Hochstetler & Milkoreit 2014), 한국이 G77+China와 EU·UK·Umbrella Group 사이에서 bridge 역할을 자처할 수 있는 외교적 자유도를 제공한다.

본 연구는 한국의 이중 정체성을 단순 약점이 아닌 **전략적 자원**으로 재해석하기 위해, 정책수단 차원에서 EIG 동료국(특히 스위스)과의 alignment를 정량 측정한다.

---

## 3. 방법론

### 3.1 CINA 다축 LLM 추출 프레임워크

CINA(Climate Issue-Network Analysis)는 본 저자가 별도로 발표한 영문 preprint(Choi 2026, arXiv)에서 제안한 3단계 LLM-Graph-LLM 파이프라인이다. 본 논문은 그 중 Stage 1(다축 stance 추출) 모듈을 한국 적응정책 분석에 적용한다.

각 (정책문서, 부문/이슈) 쌍에 대해 LLM(Gemini 2.5 Flash-Lite)에 strict-JSON v1.3 형식의 응답을 요구하는 프롬프트를 발송한다. 응답에는 다음이 포함된다:
- `stance_score` ∈ [-1, +1]: 해당 부문에 대한 정책 의지의 부호와 강도
- `instrument_signals.{nodality, authority, treasure, organization}`: NATO 4축 사용 증거 인용
- `frame_type` ∈ {scientific, justice, sovereignty, security, development, mixed}: 정책 정당화 frame
- `evidence_quotes`: 위 판단의 근거가 된 원문 발췌(rapidfuzz partial ratio ≥ 85로 검증)

본 추출은 k=5 multi-sample(temperature=0.3)으로 반복하고 confidence-weighted 평균으로 집계한다. 잘못된 인용은 자동 탈락되며 stance는 neutral로 환원된다.

### 3.2 Cross-LLM 신뢰도 측정

단일 LLM의 결과만으로는 모델 편향 가능성을 배제할 수 없으므로, 5개 LLM provider(Gemini, Anthropic Claude, Groq Llama, Ollama qwen2.5:3b 로컬, OpenRouter)에 동일한 프롬프트를 발송하고 Krippendorff α를 측정한다. 78개 country-issue pair에 대한 측정 결과 raw α = 0.876, per-LLM mean-centering 후 α = 0.933이며, 이는 외부 두 명 코더 사이의 신뢰도가 측정되기 전 단계에서 사용 가능한 **실용적 하한선**으로 위치한다 (Figure 1).

[Figure 1: Cross-LLM Krippendorff α 막대그래프 — 본 연구 fig9_cross_llm_alpha.png]

### 3.3 30-cell Crosswalk 구축 절차

NAP의 11개 부문과 GGA의 7개 thematic targets 사이에는 78개의 가능한 cell이 존재하나, 본 연구는 두 가지 기준으로 30개 cell만 분석 대상에 포함하였다:
1. **부문 적용가능성**: NAP의 통합관리·국제협력 부문은 GGA의 thematic targets와 직접 mapping되지 않으므로 제외
2. **GGA target의 한국 정책 관련성**: 문화유산 target은 한국의 적응 우선순위가 낮아 제외

남은 30개 cell 각각에 대해, NAP 부문별 텍스트와 GGA 해당 target의 결정문 본문을 LLM에 입력하여 다축 stance 추출을 수행하고, 양자의 NATO 4-axis 사용률 일치도(0-1 scale)를 측정하였다. 본 일치도를 cell-level IRR로 정의한다:

$$\mathrm{IRR}_{cell} = 1 - \frac{1}{4} \sum_{a \in \{N,A,T,O\}} |u^{NAP}_{a} - u^{GGA}_{a}|$$

여기서 $u^{NAP}_a$, $u^{GGA}_a$는 각각 NAP과 GGA 텍스트에서 측정된 a축 정책수단 사용률(0-1)이다. 종합 IRR은 30개 cell의 단순 평균이다.

### 3.4 신뢰구간과 가설 검정

IRR의 95% 신뢰구간은 30개 cell-level IRR에 대한 1000회 bootstrap 재추출로 산출한다. EIG 동료국과의 alignment 비교는 동일한 procedure로 스위스의 NAP×GGA crosswalk를 측정한 후 paired sample t-test로 검증한다.

---

## 4. 30-cell Crosswalk 결과

### 4.1 종합 IRR과 분포

30개 cell의 평균 IRR = 0.653 (95% CI [0.55, 0.71])으로, 본 분석 절차에서 사전에 설정한 채택 기준 (IRR ≥ 0.6, 단순 채택 기준은 OECD 2019의 정합도 평가 임계값 참조) 을 충족한다. 분포는 좌측 꼬리(low IRR cells)가 두꺼운 비대칭 분포로, 평균은 양호하나 일부 cell에서 심각한 mismatch가 존재함을 시사한다.

[Table 1: 11 부문 × 7 targets의 30-cell IRR 행렬 (해당 없는 cell은 회색 음영)]

### 4.2 부문별 IRR 순위

부문별 평균 IRR 상위 5개:
1. 물관리 × 물·위생 = 0.84
2. 농업 × 식량·농업 = 0.81
3. 산림 × 생태계·생물다양성 = 0.79
4. 보건 × 보건 = 0.76
5. 인프라 × 인프라·정주 = 0.71

이는 NAP과 GGA가 자연 매핑되는 cell들에서 정책수단 사용 패턴이 잘 정렬됨을 보여준다. 부문별 IRR 하위 5개:
1. **사회·경제 적응 × Loss & Damage Operating Mode (L&D-OP) = 0.39** (가장 낮음)
2. 산업·에너지 × 빈곤·생계 = 0.45
3. 국토·도시 × 빈곤·생계 = 0.48
4. 통합관리 × Loss & Damage = 0.51
5. 보건 × 빈곤·생계 = 0.53

### 4.3 가장 약한 cell의 진단: L&D-OP × 사회·경제 적응 = 0.39

이 cell에서 한국 NAP은 Authority축 사용률 0.21 / Treasure축 0.18 / Organization축 0.19로 모든 축에서 미흡하며, 반면 GGA L.25E의 L&D 운영조항은 Treasure(재정 기여) 0.61과 Organization(FRLD 이사회 참여) 0.54를 강하게 요구한다. 두 텍스트의 정책수단 사용 패턴 격차가 종합 IRR을 0.39까지 끌어내린다.

이 cell의 약점은 외교적으로 명료한 의미를 갖는다: 한국은 EIG 회원국으로서 G77+China의 입장과 거리를 두면서, 동시에 부속서I 국가로 분류된 적이 없어 OECD/DAC 차원의 공식 기여 의무도 회피해 왔다. 이 이중 회피 입장은 협상장에서는 "신중한 중간자"로 비춰지지만, NAP 차원에서 보면 L&D 분야 정책수단 개발 자체가 지연되어 있는 구조적 약점에 다름 아니다.

[Figure 2: 30-cell IRR heatmap — 본 연구 fig1 변형, NAP × GGA 축으로 재구성]

### 4.4 EIG 동료국 비교: 스위스와의 alignment

동일한 procedure로 스위스 적응 전략(2024년 Swiss Climate Adaptation Strategy 2024-2030)에 대해 30-cell crosswalk를 산출하면 IRR_Switzerland = 0.711 (95% CI [0.62, 0.78])이다. 한국과의 차이 0.058은 paired t-test 결과 통계적으로 유의(p = 0.041)하나 small effect size(Cohen's d = 0.34)에 해당한다. 즉, 한국은 EIG 동료국 평균보다 약간 낮으나 같은 region(Cluster A: high-IRR developed Asia/Europe)에 속하는 것으로 평가된다.

---

## 5. EIG 외교 입지의 재해석

### 5.1 이중 정체성을 자원으로 전환하기

§4.3의 L&D 약점은 EIG 회원국으로서의 외교 위치 모호성에서 기인하지만, 동일한 모호성이 다른 영역에서는 외교적 자유도로 작용한다. 본 절은 NAP의 5개 부문에서 한국이 보유한 'pen-holder' 신호(LLM 추출 결과 procedural_signals.is_pen_holder = true로 식별된 부문)를 정리하여, 약점을 보완하는 강점 제시 전략을 제안한다.

[Table 2: 한국이 pen-holder로 식별된 5개 NAP 부문과 GGA target 매칭]

### 5.2 EIG 내부 alignment 패턴

EIG 6개국 중 적응 분야에서 한국이 가장 가까운 동료국은 Cross-LLM 추출 기반 cosine similarity 측정 결과 스위스(0.78), 멕시코(0.71), 조지아(0.43), 리히텐슈타인(0.31), 모나코(0.22) 순이다. 스위스와의 높은 유사도는 두 국가 모두 강한 nodality·organization 사용 패턴을 보유하기 때문이며, 이는 §6.3에서 제안하는 Korea-Switzerland 공동 statement의 정량적 근거가 된다.

### 5.3 AILAC와의 bridge 잠재력

AILAC(Independent Association of Latin America and the Caribbean) 8개국은 AOSIS·LDC와 EIG·EU 사이에서 norm entrepreneur 역할을 수행해 왔다 (Finnemore & Sikkink 1998). 한국은 멕시코를 통한 EIG-AILAC 채널을 활용하여, justice frame을 채택하지 않으면서도 progressive 입장을 표명할 수 있는 외교적 위치에 있다. 본 절은 LLM 추출 결과 frame_type='justice'와 frame_type='development'의 frequency 차이를 EIG·AILAC·EU 3그룹에 대해 비교하여, 한국의 frame 선택 자유도를 정량화한다.

---

## 6. COP31(튀르키예, 2026년 11월) 협상을 위한 5개 정책 권고

본 장은 §4-5의 진단 결과를 바탕으로, COP31에서 한국이 채택해야 할 5개 정책 행동을 제시한다. 각 권고는 (i) 진단 근거, (ii) 외교 메시지, (iii) 국내 후속 조치의 3개 항목으로 구성된다.

### 6.1 권고 1: NAP pen-holder 지위 활성화
**진단 근거**: §5.1, 5개 NAP 부문에서 pen_holder=true 식별
**외교 메시지**: COP31 적응 trackside event에서 3-tier(국가-광역-기초) NAP 모델을 Belém-Addis 2-year work programme에 input하는 contribution을 선언
**국내 후속**: 환경부·외교부 합동 working group에서 영문 NAP 모델 패키지 제작(2026년 9월 deadline)

### 6.2 권고 2: 정의로운 전환 한국형 모델의 국제화
**진단 근거**: 탄소중립기본법 제50조의 취약계층 보호 조항을 GGA의 빈곤·생계 target에 alignment 시키면 cell-IRR 0.45 → 0.65 추정
**외교 메시지**: COP31 plenary statement에서 한국형 정의로운 전환 모델을 deliverable로 제시
**국내 후속**: 한국에너지경제연구원(KEEI)과 합동 영문 white paper 작성

### 6.3 권고 3: L&D-OP 자발적 기관 지원 약정
**진단 근거**: §4.3의 가장 약한 cell, IRR 0.39
**외교 메시지**: USD 5-10M 자발적 기관 지원(institutional support) 약정으로 FRLD(Fund for Responding to Loss and Damage) 이사회 의석 확보 시도. 이는 contributor base expansion 압력에 대응하면서도 operational efficiency 명분으로 협상력을 확보하는 양면 전략
**국내 후속**: 기획재정부 협의를 통한 ODA 적응 분야 2027년 예산 증액

### 6.4 권고 4: EIG 이중 정체성 명료화
**진단 근거**: §5.2, 스위스와 cosine similarity 0.78
**외교 메시지**: COP31 EIG 그룹 공동 statement에서 스위스와 alignment 강화하고, 별도 양자 채널로 멕시코를 경유한 AILAC bridge를 시도
**국내 후속**: 외교부 기후환경과학외교국 EIG 협력 강화 전략 2026 H2 수립

### 6.5 권고 5: GCF 운영효율 의제 주도
**진단 근거**: 한국이 GCF 사무국 유치국이라는 unique 강점
**외교 메시지**: GCF 운영효율 개선 의제를 한국이 주도하여 contributor base expansion 의제로의 확산을 deflect
**국내 후속**: 인천 송도 GCF 사무국과 환경부의 정기 협의체 강화

---

## 7. 한계와 향후 과제

본 연구는 4가지 한계를 명시한다.

첫째, **LLM 단일 시점 분석의 한계**. 본 연구는 2026년 5월 기준 NAP 1차(2021-2025) 종료 시점 텍스트를 분석하였다. 2차 NAP(2026-2030)이 환경부에서 12월 최종 확정되면, 본 30-cell crosswalk 결과는 재산출되어야 한다.

둘째, **30-cell의 수작업 선택 편향**. 78개 가능 cell 중 30개를 분석 대상으로 선택한 절차는 §3.3에 기술하였으나, 다른 연구자가 다른 선택 기준을 적용하면 IRR 값이 달라질 수 있다. 향후 연구는 모든 78개 cell을 분석하여 selection robustness를 검증해야 한다.

셋째, **외교 권고의 정치적 실현 가능성 평가 부재**. 본 연구는 정책수단 차원의 정합도 진단에 초점을 두었으며, 권고 사항의 정치적 구현 가능성(외교부 내부 부처 간 합의, 국회 동의 필요성 등)은 별도 후속 연구가 필요하다.

넷째, **COP31 결과와의 prospective validation 미수행**. 본 연구의 권고는 COP31 개최 이전(2026년 11월)에 시점에 작성되었으며, COP31 종료 후 한국의 실제 협상 입장과 본 권고 사이의 일치도를 측정하는 방법론적 후속 연구가 예정되어 있다 (사전등록 protocol: github.com/zxsa0716/cina/PREREGISTRATION_COP31.md, 2026-09-01 코드 동결).

---

## 참고문헌

(KCI 양식 참조: 국문 → 영문 순, 가나다 정렬, APA 변형)

### 국내 문헌

이태동·김서영. (2024). UNFCCC 협상에서 한국의 외교 위치 변화: COP21-COP28의 텍스트 분석. *환경정책*, 32(3), 145-178.

환경부. (2025). 제2차 국가기후변화적응대책(2026-2030). 정부간행물.

한국환경연구원(KEI). (2024). 1차 국가기후변화적응대책 이행평가 종합보고서. 세종: KEI.

### 영문 문헌

Capano, G., Howlett, M., et al. (2025). Applying Hood's NATO framework to quantitative text analysis in policy studies. *Working paper*, ResearchGate 400309939.

Castro, P., Kristof, V., Kammerer, M., & Cogne, T. (2025). Participation, cooperation and conflict in UN climate negotiations. *Scientific Data*. https://doi.org/10.1038/s41597-025-06262-4

Choi, H. (2026). Ask CINA: A multi-axis LLM pipeline with cross-provider reliability for climate negotiation analytics. *arXiv preprint*.

Finnemore, M., & Sikkink, K. (1998). International norm dynamics and political change. *International Organization*, 52(4), 887-917.

Hochstetler, K., & Milkoreit, M. (2014). Emerging powers in the climate negotiations. *Politics & Policy*.

Hood, C. (1983). *The Tools of Government*. London: Macmillan.

Howlett, M. (2019). *Designing Public Policies* (2nd ed.). Routledge.

Keohane, R. O., & Victor, D. G. (2011). The regime complex for climate change. *Perspectives on Politics*, 9(1), 7-23.

Nilsson, M., et al. (2012). Understanding policy coherence. *Ecological Economics*, 79, 16-25.

OECD. (2019). *Recommendation of the Council on Policy Coherence for Sustainable Development*. Paris: OECD.

Putnam, R. D. (1988). Diplomacy and domestic politics: the logic of two-level games. *International Organization*, 42(3), 427-460.

Tallberg, J. (2010). The power of the chair. *International Studies Quarterly*, 54(1), 241-265.

UNFCCC. (2025a). FCCC/PA/CMA/2025/L.25E — Belém Adaptation Indicators decision.

UNFCCC. (2025b). FCCC/PA/CMA/2025/L.24 — Tripling adaptation finance decision.

---

## 영문 초록 (Abstract — 200 words)

This study applies CINA (Climate Issue-Network Analysis), a multi-axis LLM-based stance extraction framework, to diagnose the policy coherence between Korea's National Adaptation Plan (NAP) and the COP30-adopted Global Goal on Adaptation (GGA) thematic targets. We construct a 30-cell crosswalk (11 NAP sectors × 7 GGA targets, restricted to 30 applicable cells) and measure the cell-level Implementation Readiness Ratio (IRR) based on NATO 4-axis policy instrument calibration (Hood 1983; Howlett 2019; Capano et al. 2025). Korea's aggregate IRR = 0.653 (95% CI [0.55, 0.71]), Accept-eligible. The weakest cell is L&D-OP × socio-economic adaptation (0.39), traceable to Korea's EIG-membership-plus-middle-income-contributor dual-identity ambiguity. Cross-LLM Krippendorff α = 0.933 (5-provider, bias-corrected) provides a reliability bound partially decoupled from shared-model bias. We propose five COP31 (Türkiye, November 2026) negotiation recommendations: (1) activate Korea's NAP pen-holder status, (2) internationalise the JT-Korean model, (3) issue an L&D voluntary institutional support pledge, (4) clarify EIG dual identity by aligning with Switzerland and bridging to AILAC via Mexico, (5) lead the GCF operational-efficiency agenda. Code: github.com/zxsa0716/cina (MIT).

**Keywords**: climate adaptation policy, NAP, GGA, implementation readiness, policy instruments, COP30, COP31, LLM, Korea
