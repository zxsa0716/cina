# 01. Theoretical Foundations — 이론적 근거

> CINA의 모든 방법론 선택은 국제관계·환경정치 이론에서 유도된다. 본 문서는 그 연결을 명시적으로 추적한다.

## 1. Regime Complex Theory

**Reference**: Keohane, R. O., & Victor, D. G. (2011). *The Regime Complex for Climate Change*. Perspectives on Politics, 9(1), 7–23.

### 1.1 핵심 명제
기후 거버넌스는 단일 통합 regime이 아니라, 서로 부분적으로 중첩하는 여러 제도·조약·이니셔티브의 **느슨하게 결합된 복합체(loosely coupled regime complex)**다. UNFCCC(감축·적응), Paris Agreement(NDC), Loss and Damage Fund(재원), Kyoto CDM/SBSTA(탄소시장), IPCC(과학), GCF(기금) 등이 각기 다른 참여자·다른 의사결정 규칙·다른 권력 구조를 가진다.

### 1.2 CINA에서의 함의
- **이슈별 분리 모델링**: 국가의 "기후 정책 입장"은 단일 벡터가 아니라, 이슈마다 독립적으로 결정되는 고차원 구조다.
- **Stage 1 스탠스 추출의 정당화**: 동일 국가라도 이슈별 stance_score를 분리 추출하는 것은 이 이론의 직접적 구현이다.
- **Stage 2 이종 그래프의 정당화**: 단일 유형 노드가 아닌 Country × Issue 이종 그래프는 regime complex의 구조적 다중성을 반영한다.

---

## 2. Two-Level Games (Putnam, 1988)

**Reference**: Putnam, R. D. (1988). Diplomacy and Domestic Politics: The Logic of Two-Level Games. *International Organization*, 42(3), 427–460.

### 2.1 핵심 명제
국제 협상가는 두 개의 게임을 동시에 한다:
- **Level I**: 국제 협상 테이블에서의 합의 모색
- **Level II**: 국내 비준 획득을 위한 정치적 타협

합의는 Level I과 Level II의 교집합인 **"win-set"** 안에서만 가능하다. 국가의 공식 입장(submission)은 win-set의 경계를 드러내는 시그널이다.

### 2.2 CINA에서의 함의
- **`flexibility_signals` 추출**: 공식 입장 내부에 숨은 유연성 시그널("subject to capacity", "in accordance with national circumstances", "welcome further discussion")은 win-set의 확장 여지를 나타낸다. Stage 1의 LLM 프롬프트에서 이를 명시적으로 추출한다.
- **`red_lines` 추출**: 반대로 국내 정치가 허락하지 않는 절대적 한계선("no new obligations without means of implementation")은 win-set의 바깥 경계다.
- **브라질 사례**: 의장국으로서 Level I 역할(중재자)과 Level II 역할(자국 이해, 특히 Amazon 보호와 개발 권리 사이의 긴장)이 동시에 작용한다. CINA는 이를 두 개의 분리된 stance vector로 포착할 수 있는가?

---

## 3. Issue Linkage Theory

**References**:
- Tollison, R. D., & Willett, T. D. (1979). An Economic Theory of Mutually Advantageous Issue Linkages in International Negotiations. *International Organization*, 33(4), 425–449.
- Haas, E. B. (1980). Why Collaborate? Issue-Linkage and International Regimes. *World Politics*, 32(3), 357–405.
- Sebenius, J. K. (1983). Negotiation Arithmetic: Adding and Subtracting Issues and Parties. *International Organization*, 37(2), 281–316.

### 3.1 핵심 명제
단일 이슈로는 합의 불가능한 상황에서도, 서로 다른 선호를 가진 여러 이슈를 **묶으면(link)** 파레토 개선적 합의가 가능하다. 이슈 연계는 (a) 교환 가능한 concession을 창출하거나, (b) 취약 이슈를 더 강력한 이슈에 편승시키는 방식으로 작동한다.

### 3.2 CINA에서의 함의
- **Cross-Issue Hypergraph**: 일반 그래프는 pairwise edge만 표현하지만, 3개 이상 이슈 연계는 hyperedge로 표현해야 정확하다. Stage 2의 hypergraph 모듈은 이 이론의 직접 구현이다.
- **Package Deal 탐지**: 동일 국가가 "이슈 X 양보 + 이슈 Y 강경" 패턴을 보일 때, 그 국가는 X↔Y 패키지를 원한다는 시그널이다. CINA는 이 패턴을 hypergraph motif로 자동 탐지한다.
- **COP30 사례**: Belém Package는 (a) 적응 지표 합의 + (b) 적응 재원 3배 확대 commitment + (c) loss and damage fund 접근성을 **한 묶음**으로 처리한 전형적 issue-linkage다. CINA는 사전에 이 묶음 가능성을 예측할 수 있는가?

---

## 4. Epistemic Communities (Haas, 1992)

**Reference**: Haas, P. M. (1992). Introduction: Epistemic Communities and International Policy Coordination. *International Organization*, 46(1), 1–35.

### 4.1 핵심 명제
기술적으로 복잡한 이슈에서는 과학자·전문가 네트워크가 (a) 인과적 지식의 수렴, (b) 정책 권고의 합의, (c) 정부 대표단에 대한 조언을 통해 정책 결과를 실질적으로 형성한다.

### 4.2 CINA에서의 함의
- **전문가 원안 vs 정치적 재작성**: COP30 Belém Adaptation Indicators의 "Rube Goldberg" 사건 — 전문가 그룹이 제안한 지표 체계를 브라질 의장국이 정치적 고려로 크게 재작성한 — 은 epistemic community와 정치 블록 간 긴장의 전형이다.
- **CINA의 예측 과제**: 어떤 이슈에서 epistemic divergence가 발생할 가능성이 높은가? Stage 2 그래프에서 (a) 과학 기반 노드(SBSTA, IPCC 인용)와 (b) 정치 블록 노드 간 attention weight 차이가 큰 이슈를 flagging할 수 있는가?
- **NAPs 섹터 함의**: 국가 적응계획 방법론은 UNFCCC LEG(Least Developed Countries Expert Group) 같은 epistemic body의 영향이 크다. 이 영향력을 그래프 구조로 정량화한다.

---

## 5. 보조 이론 (Supporting)

### 5.1 Negotiation Analysis (Raiffa, 1982; Sebenius)
Raiffa의 분석적 협상이론은 BATNA, ZOPA, reservation value 같은 개념으로 개별 협상자의 이성적 행위를 모델링한다. CINA는 이를 직접 구현하지 않지만, Stage 3 브리핑에서 "X 이슈의 ZOPA는 [...]", "brazil의 BATNA는 [...]" 같은 언어로 전략 분석을 제공한다.

### 5.2 Social Network Analysis in IR (Hafner-Burton, Kahler, Montgomery 2009)
*Network Analysis for International Relations*, International Organization. 국제관계 네트워크 분석의 방법론적 기초. CINA의 centrality·community detection 해석의 기반.

### 5.3 Climate Justice (Schlosberg 2007; Heedo의 Urban Climate 논문)
적응 협상의 규범적 차원 — 누가 기후 영향을 가장 많이 받으며 누가 대응 능력이 가장 부족한가. CINA의 이슈 하나인 JT-ADAPT(Just Transition)는 이 규범적 프레임을 직접 반영한다. Heedo의 기존 climate justice XAI 연구와 연결점.

---

## 6. 이론 → 방법론 매핑 (한눈에)

| 이론 | CINA 구현 요소 | 위치 |
|------|---------------|------|
| Regime Complex | 이종 Country × Issue 그래프 | Stage 2 |
| Two-Level Games | `flexibility_signals`, `red_lines` 추출 | Stage 1 |
| Issue Linkage | Cross-issue hypergraph, package deal motif | Stage 2.3 |
| Epistemic Communities | Expert–political divergence detection | Stage 2.4 |
| Negotiation Analysis | ZOPA/BATNA 언어 브리핑 | Stage 3 |
| SNA for IR | Centrality·community 해석 | Stage 2.2 |
| Climate Justice | JT-ADAPT 이슈 전용 처리 | 하위 이슈 |

---

## 7. 이론적 limitation

CINA가 채택하지 **않은** 이론들과 그 이유:
- **Realist IR (Waltz, Mearsheimer)**: 국가를 단일 이성적 행위자로 보는 관점은 Stage 1의 flexibility signal 추출과 충돌. 이슈별 선호 변이를 설명 못함.
- **Constructivism (Wendt)**: 규범·정체성이 이익을 형성한다는 관점은 맞지만, 단기 COP 협상에서 정량화가 어려움. 향후 확장 대상.
- **Game-Theoretic Equilibrium (RICE-N)**: 균형 해석은 매력적이나 실제 문서 데이터가 부족하고, 회고적 검증 시 과적합 위험.

---

## 참고 문헌

1. Keohane, R. O., & Victor, D. G. (2011). The Regime Complex for Climate Change. *Perspectives on Politics*, 9(1).
2. Putnam, R. D. (1988). Diplomacy and Domestic Politics: The Logic of Two-Level Games. *International Organization*, 42(3).
3. Tollison, R. D., & Willett, T. D. (1979). An Economic Theory of Mutually Advantageous Issue Linkages. *International Organization*, 33(4).
4. Haas, E. B. (1980). Why Collaborate? Issue-Linkage and International Regimes. *World Politics*, 32(3).
5. Haas, P. M. (1992). Introduction: Epistemic Communities. *International Organization*, 46(1).
6. Sebenius, J. K. (1983). Negotiation Arithmetic. *International Organization*, 37(2).
7. Raiffa, H. (1982). *The Art and Science of Negotiation*. Harvard UP.
8. Hafner-Burton, E. M., Kahler, M., & Montgomery, A. H. (2009). Network Analysis for International Relations. *International Organization*, 63(3).
9. Schlosberg, D. (2007). *Defining Environmental Justice*. Oxford UP.
