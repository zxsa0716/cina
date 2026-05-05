# 🔍 CINA 비판적 검토 — 실제 논문 비교 + 학술 가치 평가

> 작성: 2026-05-04 · 저자 자체 검토
> 목적: "이게 정말 논문감인가?"를 정직하게 평가하고, 어떻게 고도화/포지셔닝해야 할지 결정

---

## 1. 결론 한 줄 요약

**CINA는 현 상태로는 워크숍 단신/포스터 + 정책 분야 KCI 논문 수준이며, *Global Environmental Change* (IF 11.2) 같은 1차 학술지 투고는 아직 무리이다.** 대신 **NeurIPS Climate Change AI 2026 Workshop short paper + 한국정책학회보**의 두 트랙으로 가는 것이 가장 현실적이고, 이 경로를 위해서는 다음의 정직성 보강 + 한 가지 핵심 기여 sharpening이 필요하다.

---

## 2. 실제 경쟁 논문 매핑 (2024-2025 최신)

### 2.1 우리가 baseline으로 제시한 도구의 실제 모습

#### ❌ NegotiateCOP — 우리가 strawman 했음
**우리의 주장**: "Text RAG QA만 가능, 연합 구조 추론 불가"
**실제 (negotiatecop.org/about + GIZ 자료)**:
- Submission Explorer (메타데이터 + 인터랙티브 필터로 issue 탐색)
- **Position Comparison Feature (국가 간 입장 체계적 비교, overlap/disagreement 표시)** ← 우리가 빠뜨림
- Portal Chat (RAG)
- 2025년 11월 COP30에 맞춰 정식 launch (독일 GIZ + 3개 부처 데이터랩 공동)
- 무료 공개 디지털 공공재

**시사점**: NegotiateCOP은 "Position Comparison"이라는 핵심 기능을 이미 가지고 있다. 우리 paper §1에서 "기존 도구는 stance 비교를 못한다"라고 한 것은 사실과 다르다. **우리의 차별점은 "stance 비교가 가능하다"가 아니라 "(a) Bayesian CI + NATO 4축 + 5 frame을 동시 추출, (b) 그래프 구조로 community 자동 검출, (c) graph-grounded generation으로 hallucination 방지"** 세 가지의 결합이다. 이걸 명확히 해야 한다.

#### ✅ Castro et al. 2025 (Nature Scientific Data) — 인용 정확
**실제**: ENB 보고서를 기반으로 한 cooperation/conflict 빈도 데이터셋. 1995-2024 COP 전 회기 코딩. DOI: 10.1038/s41597-025-06262-4.
**우리의 차별점**: Castro는 **빈도 집계** (A-B 국가가 N번 협력 언급됨). CINA는 **stance 정량화** (A 국가가 X 이슈에 ±0.95 강도). 이는 보완적 데이터이지 대체 관계가 아니다. **paper에서 "Castro 한계 = 빈도만"이라고 비판하는 톤을 부드럽게**, "Castro와 CINA를 결합하면 양면 분석 가능"으로 전환해야 한다.

#### 🆕 Castro et al. 2025 (Tandfonline) "Dynamic networks of negotiation" — 직접 경쟁
**URL**: https://www.tandfonline.com/doi/full/10.1080/23251042.2025.2507287
**실제**: Castro 데이터셋을 사용해 **dynamic network analysis**로 실질적 alliance를 추출. "공식 negotiating bloc(AOSIS, G77+China, LDC)는 안정적이지만 협상 결과를 완전히 설명 못한다"가 핵심 주장.
**시사점**: 우리 Stage 2와 **목적이 동일**하다 (실질적 연합 검출). 다만 우리는 (a) ENB 빈도가 아닌 stance score 기반, (b) 단일 시점(2025) 분석. Castro Tandfonline은 1995-2024 시계열. **우리가 우위인 점**: stance score는 빈도보다 풍부한 신호이며, NATO 4축 + frame까지 같이 봄. **우리가 열위인 점**: 단일 시점, n 작음, 시계열 분석 부재.

#### 🆕 "Applying Hood's NATO framework to quantitative text analysis" 2025 — 직접 경쟁
**URL**: ResearchGate 400309939
**실제**: NATO 4축의 **text analysis 적용 방법론 review + research agenda**. dictionary methods, supervised learning, topic models, span-level annotation 등 다양한 방법 포괄. **construct validity, multi-label coding, calibration intensity** 등 challenge 명시.
**시사점**: 우리 NATO 4축 추출은 이 review의 framework 안에 포함된다. **우리 차별점**: LLM zero-shot extraction (이 review가 다루는 supervised/dictionary와 다름) + procedural authority 신호 통합. 이걸 명시하고 review를 직접 인용해야 한다.

#### ✅ RICE-N 2025 (PMLR) — 우리가 강조한 baseline 차이 정확
**실제**: Multi-agent RL 기반 시뮬레이션. 실제 텍스트 grounding 없음.
**우리 차별점**: 정확함. 단, "RICE-N은 시뮬레이션이라 한계"라기보다 "RICE-N과 CINA는 상보적 — 시뮬레이션 + 실측"이라고 표현하는 게 학술적 매너.

#### 🆕 "Tracing inclusivity at UNFCCC conferences" 2025 (Nature Climate Change)
**실제**: COP side event 2003-2023을 ML topic modeling + 사회연결망 분석으로 분석.
**시사점**: 우리와 인접 분야이지만 (a) 공식 결정문이 아닌 side event, (b) topic modeling 위주, (c) inclusivity 관점. **paper에서 Related Work에 인용 필수**.

### 2.2 우리가 인용한 stance detection benchmark — 정상적 위치

stance detection 벤치마크 영역에서 LLM 기반 방법이 전통적 방법과 동등 수준 도달 (Cambridge "Stay Tuned" 2024). 정치 텍스트 stance detection이 활발한 분야이고, 우리 Spearman ρ=0.658은 이 분야 **중간 수준**이다 (top 결과는 0.75+).

---

## 3. CINA의 진짜 강점과 약점 (정직 평가)

### 3.1 진짜 강점 (논문에서 강조해야 할 것)

1. **다축 추출의 결합** (NATO + frame + procedural + Bayesian CI). 개별 요소는 다 선행연구가 있지만, **이 4가지를 단일 LLM 추출 파이프라인으로 결합한 것은 새롭다**. 이게 ablation A2/A3/A1에서 각 -7%/-4%/-5% 기여로 입증됨.
2. **Graph-grounded generation 검증기**. 모든 brief 문장에 (text quote + structural fact) 이중 grounding 강제 + 7-rule post-hoc verifier. Ablation A4의 -15% impact가 가장 크고, 이는 hallucination 방지의 효과를 보여주는 **검증 가능한 정량 결과**.
3. **회고적 검증 framework**. COP30 결과(L.25E, 2025.11)를 회고적으로 입력해 contested 이슈 예측 정확도 측정. 이 design이 정량 IR 분야에서 흔치 않다.
4. **개방형 재현성**. 코드 MIT, 데이터 manifest 225 entries with sha256, sample data 공개, 5개 LLM provider 추상화. 동급 논문 중 reproducibility 상위.
5. **단일 케이스 정밀 분석**: Brazil Translation Gap Δ=0.304는 **양면게임 × 정책수단 calibration**이 만나는 빈자리에 대한 **정량 측정**. 일반화는 어렵지만 단일 케이스로서는 가치 있음.

### 3.2 진짜 약점 (정직히 인정해야 할 것)

| 약점 | 심각도 | 어떻게 처리할지 |
|------|------|---------------|
| n=98 stance records (≤ NLP 평균) | 중 | "pilot study" 또는 "preliminary" 표현 사용 |
| 13 countries (전체 196 UNFCCC 중) | 중 | 명시적 제한, 향후 확장 계획 |
| Task D 5 평가자 = LLM 시뮬레이션 | **고** | Task D를 **별도 task로 분리**, 본문에서는 Task A/B/C만 강조 |
| Krippendorff α=0.905 from simulated panel | **고** | "simulated panel"임을 abstract부터 명시 |
| Single Brazil case (Δ=0.304) | 중 | "single case study"임을 §4에서 자명하게 표시 |
| Stage 2 R-GAT 미구현 (NetworkX only) | **고** | "Future work: GAT-based learned weights" — paper §2에서 RGAT는 design level만 |
| "First quantitative measurement of Putnam × Howlett gap" 주장 | **고** | "**A** novel quantitative measurement" 또는 "first reported within climate domain" |
| P@3=R@3=1.00 from N=3 | 중 | 신뢰구간 또는 "small sample, encouraging signal" 표현 |
| NegotiateCOP straw man | 중 | 정확한 비교로 수정 |

### 3.3 잘못된 또는 과장된 주장 (수정 필수)

1. **"NegotiateCOP은 stance 비교 불가"** ← **틀림**. NegotiateCOP은 Position Comparison Feature를 가지고 있다. 수정: "NegotiateCOP은 individual stance를 보여주지만 (a) Bayesian uncertainty, (b) 정책수단 calibration, (c) 자동 community 검출은 제공하지 않는다."

2. **"First quantitative measurement of Putnam × Howlett intersection"** ← **검증 불가능한 over-claim**. 수정: "A novel quantitative measurement of domestic-international policy instrument divergence in climate negotiations" — "first" 빼고 "novel"로.

3. **"Combined Rubric 4.76/5"** — 이건 **내부 평가 도구**이므로 외부 reviewer에게는 의미 없음. paper에서 빼고 "Phase 5 evaluation completed across 4 tasks"로 표현.

4. **"5 expert evaluators"** — 시뮬레이션이므로 "5 expert *personas* simulated by Claude"로 명시.

5. **"R-GAT model"** — 실제로는 NetworkX 기반. paper에서 "heterogeneous graph analysis with NetworkX + Leiden + igraph"로 정확히. R-GAT는 Future Work.

---

## 4. 가능한 투고 경로 (현실 평가)

### 4.1 지금 상태로 가능한 투고

| 매체 | 가능성 | 무엇이 필요한가 |
|------|------|-------------|
| **NeurIPS Climate Change AI 2026 Workshop (포스터)** | **높음 (60-70%)** | 4-page short paper. 현 분량 충분. 위 5가지 과장 수정 필수 |
| **한국정책학회보 (KCI)** | **높음 (60-70%)** | 한국 정책 함의 분량 확장 (현 §6 → 1편 분량). 적응정책 학계와 직접 대화 |
| **Climate Policy (Q1)** | **중간 (30-40%)** | n 확장 + 시계열 추가 + 실제 외교 전문가 인터뷰 추가 |

### 4.2 6-12개월 후 가능 (확장 후)

| 매체 | 무엇을 추가해야 하나 |
|------|--------------------|
| **Global Environmental Politics** | (a) n=300+ stance records (전 196개국 일부), (b) 실제 외교 전문가 5인 패널 코딩, (c) 시계열 (COP21-30) 분석 |
| **Nature Scientific Data** | 데이터셋 자체를 peer review. CINA-stance-2026 dataset 발표용 별도 논문 |
| **Global Environmental Change (IF 11.2)** | 위 모두 + 정책 함의 깊이 (실제 외교부 협업 후 도출) |

### 4.3 최우선 권고 트랙

**A 트랙 (학술)**: NeurIPS CCAI 2026 Workshop short paper (4-page) + arXiv preprint
- 강점: 회고적 검증 + graph-grounded generation 결합
- 위험: Workshop은 종종 정식 publication으로 인정되지 않음

**B 트랙 (정책)**: 한국정책학회보 또는 *Korean Journal of International Studies*
- 강점: 한국 NAP IRR + L&D 약점 + 정책 권고 구체성
- 위험: 학술 IR 동료들이 "AI 도구 활용"으로만 평가할 위험

**두 트랙을 병행**하는 것이 가장 안전.

---

## 5. 학술 contribution 재정의

기존 우리는 "8 publishable findings"라고 주장했지만, 실제 학술 기여는 **2-3개로 sharpening**해야 한다:

### Primary Contribution (1개로 좁히기)

> **A multi-axis stance extraction pipeline that combines NATO 4-axis policy instruments, frame typology, procedural authority signals, and Bayesian credible intervals from UNFCCC negotiation texts using LLM ensemble, demonstrated to recover regime complex 'horizontal cleavage' (Keohane & Victor 2011) via downstream Leiden community detection.**

이게 **method paper**로서의 contribution이다. 한 문장에 다 담아야 한다.

### Secondary Contributions (2개)

1. **Translation Gap Δ as a metric**: Domestic vs international policy instrument usage divergence를 NATO 4축 frequency 차이로 측정한 단일 metric. Brazil COP30 case에서 Δ=0.304 측정. Two-Level Games (Putnam 1988) × Instrument Calibration (Howlett 2019) 교차점에 위치.
2. **Graph-grounded generation for diplomatic briefing**: 모든 LLM 출력 문장에 (text quote + structural fact) 이중 grounding 강제. 7-rule post-hoc verifier. Ablation에서 evidence grounding 제거 시 -15% impact (가장 큰 단일 컴포넌트).

### "Findings" → "Empirical observations"

기존 "8 publishable findings" 대신 본문에 다음과 같이:

- "We observe a horizontal cleavage in adaptation negotiations consistent with regime complex theory (Keohane & Victor, 2011; Leiden modularity = 0.31, n=13)."
- "We measure Brazil's domestic-international policy instrument divergence at Δ=0.304 (single case study)."
- "Among 6 GGA issues, GGA-IND shows lowest Authority axis usage (6.1), consistent with chair-controlled pre-crystallization."

각각 단순 "발견"이 아니라 "관찰 + 이론 연결 + 한계"의 단락으로.

---

## 6. 즉시 수행해야 할 paper.md 수정 사항

1. **Abstract**: "first" → "novel" 또는 "to our knowledge first within climate negotiation domain"
2. **§1 Introduction**: NegotiateCOP을 정확히 묘사 (Position Comparison 인정)
3. **§2 Related Work** (신설 또는 확장): Castro Tandfonline 2025 + NATO 2025 review + Tracing Inclusivity 2025 + RICE-N 2025 + stance detection benchmark literature 인용
4. **§3 Methodology**: R-GAT는 design level로만, 구현은 NetworkX임을 명시
5. **§4 Results**: P@3=R@3=1.00 옆에 "(N=3 contested issues, encouraging signal but small sample)" 추가
6. **§5 Discussion**: §5.2에 5가지 limitation을 한 단락으로 정리, simulated panel 명시
7. **§6 Conclusion**: "8 findings" → "Three primary observations + framework contribution"
8. **References**: Castro Tandfonline 2025, NATO text analysis 2025, Tracing inclusivity 2025 추가

---

## 7. 학술 매너 (놓치면 reviewer가 화내는 것들)

1. ✅ **Open code, open data sample** — 잘 함
2. ❌ **No real expert validation** — Task D 시뮬레이션 명시 누락
3. ❌ **No pre-registration** — 회고적 검증의 신뢰성 약화. 차후 OSF preregistration 권고
4. ❌ **Single LLM ablation 미실시** — "Multi-LLM ensemble"이라고 했는데 각 LLM 단독 성능 비교 없음. ablation A5는 ensemble 제거인데 각 모델 단독 제거 안 함
5. ❌ **Compute reporting 부재** — 총 LLM API 비용, 실행 시간, GPU 사용량 등
6. ✅ **Manifest tracking** — 좋음
7. ❌ **IRB / Ethics 언급 없음** — 인간 데이터 없으니 면제이지만 "no human subjects" 명시 권고
8. ❌ **Cherry-picking 위험** — 8 findings가 모두 "성공" 패턴. 어떤 가설이 검증 실패했는지 보고 없음

---

## 8. 다음 단계 우선순위

### 즉시 (오늘-내일)
1. paper.md를 위 수정 사항대로 honest version으로 재작성
2. README citation에서 "Combined Rubric 4.76/5" 같은 내부 메트릭 제거
3. ALL_OUTPUTS_INDEX의 "8 findings" → "3 primary observations + framework"로 수정
4. NegotiateCOP 정확한 묘사로 모든 곳 수정 (paper, README, briefing)

### 1-2주
1. 실제 외교부/환경부 1인이라도 비공식 의견 받기 (제출 전)
2. 한국정책학회보 투고 양식에 맞춰 한국어 single-author 논문 별도 작성
3. NeurIPS CCAI 2026 workshop CFP 확인 (대개 6-7월 deadline)
4. arXiv preprint 업로드

### 1-2개월
1. Single LLM ablation 추가 실행
2. Compute reporting 추가
3. 시계열 데이터 (COP25-30) 추가 (가능 시)

### 6-12개월 (장기)
1. 실제 외교 전문가 5인 코딩 패널 섭외 → Krippendorff α 정식 측정
2. n 확장 (98 → 300+)
3. R-GAT 실제 학습 (PyTorch)
4. Q1 학술지 투고

---

## 9. 결론

**현 상태의 CINA는 "야심찬 학생 프로젝트로서 우수"하나 "Q1 IR 학술지 투고는 시기상조"이다.** 그러나 (a) 회고적 검증 design + (b) graph-grounded generation 검증기 + (c) 다축 stance 추출의 결합은 **연구 가치가 충분**하며, 정직한 수정 후 NeurIPS Climate Change AI Workshop + 한국정책학회보 더블 트랙으로 갈 수 있다.

**가장 위험한 것은 "이게 Global Environmental Change에 갈 수 있다"는 자기 기만이다.** 학술 reviewer는 위 약점을 즉시 잡아내며, "promising but not yet ready" 평가를 받게 된다. 솔직하게 "preliminary methodology paper with single case retrospective validation"로 포지셔닝하면 학회 채택 + 차후 확장 경로가 안전하다.

수업 제출용으로는 현 상태로 충분하다 (교수님이 놀랄 수준). 다만 "Track B 학술 투고"라고 할 때는 위 정직성 수정이 필수이다.

---

**작성**: Heedo Choi (최희도) · 2026-05-04 · 자체 비판적 검토
**참고 논문**:
- Castro et al. 2025 (Nature SciData): https://www.nature.com/articles/s41597-025-06262-4
- Castro et al. 2025 (Tandfonline): https://www.tandfonline.com/doi/full/10.1080/23251042.2025.2507287
- NATO Framework Text Analysis 2025: ResearchGate 400309939
- NegotiateCOP: https://negotiatecop.org/
- Tracing Inclusivity at UNFCCC 2025: https://www.nature.com/articles/s41558-025-02254-9
