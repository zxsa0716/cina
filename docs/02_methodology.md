# 02. Methodology — 전체 방법론

> 본 문서는 CINA의 3단계 파이프라인을 방법론적 엄밀성 수준에서 서술한다. 각 단계의 상세 구현은 `04_*.md`, `05_*.md`, `06_*.md`에 있다.

## 1. Problem Formulation

### 1.1 입력
- 문서 집합 $\mathcal{D} = \{d_1, \ldots, d_M\}$: UNFCCC 공식 submission, NDC, ENB 요약
- 국가 집합 $\mathcal{N} = \{n_1, \ldots, n_N\}$, $N \approx 195$
- 이슈 집합 $\mathcal{I} = \{i_1, \ldots, i_I\}$, $I = 6$ (adaptation sub-issues)
- 협상 그룹 집합 $\mathcal{G} = \{g_1, \ldots, g_K\}$, $K \approx 12$
- 시간 인덱스 $t \in \{t_1, \ldots, t_T\}$ (COP21 … COP30)

### 1.2 목표
다음 네 가지 출력을 생성한다:
1. **스탠스 텐서** $S \in \mathbb{R}^{N \times I \times T \times 3}$: 각 (국가, 이슈, 시점)에 대해 스탠스 점수의 posterior mean과 95% credible interval.
2. **연합 클러스터** $C_i(t)$: 이슈 $i$, 시점 $t$에서의 국가 그룹핑.
3. **핵심 행위자 순위** $R_i(t)$: 이슈 $i$에서의 betweenness/eigenvector centrality 기반 중요 국가 리스트.
4. **전략 브리핑** $B$: 선정 국가(브라질)의 장관에게 올리는 구조화 문서.

---

## 2. Stage 1: Calibrated Stance Extraction

### 2.1 추출 스키마
각 (국가 $n$, 이슈 $i$, 문서 $d$) 조합에 대해 LLM에 다음 JSON 스키마를 강제한다:

```json
{
  "country": "Brazil",
  "issue": "GGA-IND",
  "stance_score_raw": 0.65,
  "stance_score_calibrated": 0.58,
  "ci_lower_95": 0.42,
  "ci_upper_95": 0.74,
  "key_demands": ["Quantitative indicators with capacity context"],
  "red_lines": ["No universal metrics without MoI"],
  "flexibility_signals": ["phased implementation acceptable"],
  "evidence_quotes": [
    {
      "quote": "Brazil calls for measurable indicators that reflect...",
      "source": "UNFCCC/SBI/2025/L.3",
      "paragraph": "12"
    }
  ],
  "extraction_metadata": {
    "model": "claude-opus-4-7",
    "temperature": 0.3,
    "samples": 5,
    "prompt_version": "v1.2"
  }
}
```

### 2.2 다중 샘플링과 불확실성 정량화
각 (국가, 이슈) 조합에 대해 동일 프롬프트로 $k=5$회 LLM 호출 (temperature=0.3). 얻은 $k$ 개의 stance score에 대해:
- Posterior mean $\hat{\mu}$, 표준편차 $\hat{\sigma}$ 계산
- **Beta-binomial 모델**로 95% credible interval 도출: stance score를 $[−1,+1]$에서 $[0,1]$로 rescale 후 Beta prior $\text{Beta}(\alpha_0, \beta_0)$ 가정, $k$ 샘플로 사후 분포 갱신

### 2.3 Calibration
LLM의 raw score는 체계적 편향이 있을 수 있다 (친환경 편향 등). **Platt scaling**으로 보정:
- 훈련 데이터: ENB-coded interaction 중 이슈별로 명확히 dissent/concurrence로 분류 가능한 (국가, 이슈) 쌍 $n_{\text{cal}} \approx 200$
- Sigmoid 함수 $\sigma(a \cdot s + b)$의 $(a, b)$를 MLE로 추정
- 보정된 score $s_{\text{cal}} = \sigma(a \hat{\mu} + b)$

### 2.4 Prompt Engineering
Stage 1 프롬프트는 다음을 **반드시 포함**:
1. 이론적 정의 (Two-Level Games의 win-set 설명)
2. 출력 JSON schema 엄격 강제
3. Evidence quote 필수 (빈 quote 금지)
4. "확신이 없으면 stance_score=0, ci_lower/upper를 넓게" 지시
5. Few-shot examples (2개: 명확한 지지, 조건부 지지)

상세 프롬프트는 `docs/04_stage1_stance_extraction.md` 부록.

---

## 3. Stage 2: Heterogeneous Temporal Graph Analysis

### 3.1 그래프 정의
$G(t) = (V, E(t))$, $V = V_N \cup V_I \cup V_G$
- $V_N$: 국가 노드 ($|V_N| = N$)
- $V_I$: 이슈 노드 ($|V_I| = I$)
- $V_G$: 협상 그룹 노드 ($|V_G| = K$)

엣지 유형:
- $e_{\text{stance}}(n, i, t)$: 국가→이슈, weight = $S_{n,i,t}$
- $e_{\text{sim}}(n_1, n_2, i, t)$: 이슈 $i$에서 두 국가 스탠스 간 cosine similarity
- $e_{\text{coop}}(n_1, n_2, t)$: ENB 기반 과거 협력 빈도 (Castro et al. 2025)
- $e_{\text{mem}}(n, g)$: 국가-그룹 멤버십 (시간 불변)

### 3.2 Heterogeneous Graph Attention Network (R-GAT)
노드 임베딩 학습:
$$h_v^{(l+1)} = \sigma\left(\sum_{r \in R} \sum_{u \in \mathcal{N}_r(v)} \alpha_{vu}^{(r,l)} W_r^{(l)} h_u^{(l)}\right)$$

여기서 $\alpha_{vu}^{(r,l)}$는 edge type $r$에 대한 attention weight (LeakyReLU + softmax).

**학습 목표**: 두 가지 auxiliary task로 self-supervised:
1. **Link prediction**: 무작위로 mask한 stance edge의 weight 예측
2. **Coalition consistency**: 같은 그룹 내 국가 쌍의 임베딩 거리 < 다른 그룹 쌍

### 3.3 커뮤니티 탐지
학습된 임베딩 공간에서 이슈별로 **Leiden algorithm** (Traag et al. 2019) 적용:
- 이슈 $i$에 대해 국가 노드들의 임베딩 $\{h_n^{i}\}$ 추출
- $k$-NN 그래프 구축 ($k=5$)
- Leiden으로 커뮤니티 탐지 (resolution $\gamma=1.0$)
- 결과: 이슈별 클러스터 labeling $C_i(t)$

### 3.4 Centrality 분석
- **Betweenness centrality**: 브릿지 국가 식별
- **Eigenvector centrality**: 영향력 큰 국가
- **Attention-based centrality**: R-GAT의 incoming attention weight 합 → 모델이 중요하다 판단한 노드

### 3.5 Cross-Issue Hypergraph
Issue linkage theory 구현:
- 각 국가의 이슈별 flexibility_signal 벡터 $f_n \in \{0,1\}^I$ 추출
- Apriori-like algorithm으로 support $\geq \tau$ 이상인 이슈 부분집합 탐지
- 결과: hyperedge $\{i_a, i_b, i_c\}$ = 국가들이 공통으로 flexibility 또는 rigidity를 보이는 이슈 묶음

### 3.6 출력 아티팩트
```json
{
  "issue_communities": {
    "GGA-IND": [
      {"cluster_id": 0, "countries": ["EU", "Norway", ...], "centroid_stance": 0.8},
      {"cluster_id": 1, "countries": ["India", "Saudi Arabia", ...], "centroid_stance": -0.4}
    ],
    ...
  },
  "bridge_countries": {
    "GGA-IND": [{"country": "South Africa", "betweenness": 0.34}, ...]
  },
  "cross_issue_hyperedges": [
    {"issues": ["GGA-IND", "ADAPT-FIN"], "countries": ["India", "LDC-group"], "pattern": "linked_concession"}
  ]
}
```

---

## 4. Stage 3: Graph-Grounded Briefing Generation

### 4.1 입력
- Stage 2 출력 JSON
- 원시 evidence quotes (Stage 1에서 수집)
- 브라질의 공식 입장 (focal country)

### 4.2 생성 제약
각 생성된 문장 $s$는 다음을 만족:
- $s$가 팩트 주장이면 → 반드시 (evidence_quote, structural_fact) 쌍 인용
- $s$가 전략 권고이면 → 최소 한 개의 이슈/국가 구조적 근거 필요
- 할루시네이션 필터: 학습된 evidence base에 없는 국가/이슈/수치 등장 시 rejection

### 4.3 브리핑 템플릿 (고정 구조)
```markdown
# [Minister] 보고 — [COP] [Sector] 협상 전략 브리핑

## 1. Situation Assessment
[이슈 i별 현재 stance 분포 요약]

## 2. Coalition Map
[Stage 2 community detection 결과 서술]

## 3. Leverage Analysis
[브릿지 국가, 고centrality 행위자]

## 4. Package Deal Opportunities
[Cross-issue hypergraph에서 도출된 묶음 제안]

## 5. Red Lines and Risks
[epistemic divergence 가능성, 합의 실패 위험]

## 6. Recommended Strategic Posture
[우선 접촉 순서, 양보 영역, 유지 영역]

## Appendix A. Evidence Table
[주장–근거 매핑 테이블]
```

### 4.4 생성 프로토콜
1. Stage 2 JSON을 섹션별 prompt context로 decomposition
2. 각 섹션을 독립적으로 생성 (temperature=0.2)
3. 생성 후 자동 검증: 모든 claim에 evidence citation 있는가?
4. 검증 실패 시 재생성 (최대 3회), 여전히 실패하면 해당 claim 제거 후 경고

---

## 5. 전체 파이프라인 의사코드

```python
# CINA Pipeline v2.0
def run_cina(focal_country, sector, cop):
    # Stage 0: Data collection
    docs = collect_documents(source=["unfccc", "ndcs", "enb"], cop=cop, sector=sector)
    
    # Stage 1: Stance extraction
    stances = []
    for doc in docs:
        for country in extract_mentioned_countries(doc):
            for issue in sector.issues:
                samples = [llm_extract(doc, country, issue, temp=0.3) for _ in range(5)]
                stance = calibrate(aggregate(samples))
                stances.append(stance)
    
    S_tensor = build_stance_tensor(stances)  # [N, I, T, 3]
    
    # Stage 2: Graph analysis
    G = build_heterogeneous_graph(S_tensor, coop_data=castro_2025_enb())
    rgat_model = train_rgat(G, tasks=["link_pred", "coalition_consistency"])
    embeddings = rgat_model.get_embeddings()
    
    communities = {i: leiden(embeddings[:, i]) for i in sector.issues}
    centralities = compute_centralities(G, embeddings)
    hyperedges = detect_cross_issue_linkages(S_tensor)
    
    analysis = {
        "communities": communities,
        "centralities": centralities,
        "hyperedges": hyperedges,
    }
    
    # Stage 3: Briefing generation
    brief = generate_briefing(
        focal=focal_country,
        analysis=analysis,
        evidence=stances,  # contains quotes
        template=MINISTERIAL_BRIEF_TEMPLATE,
    )
    verify_evidence_grounding(brief)
    
    return brief, analysis, S_tensor
```

---

## 6. 재현성 (Reproducibility)

- 모든 LLM 호출의 (prompt, temperature, seed, model_version, timestamp)를 로깅 → `data/llm_logs/`
- GNN 학습의 hyperparameter seed 고정 (`PYTHONHASHSEED=42`, `torch.manual_seed(42)`)
- 모든 스크립트는 `--config config.yaml --seed N --output-dir X` 인터페이스 통일
- Docker 컨테이너 제공 (향후)

---

## 7. 계산 자원 추산

- Stage 1: 약 20 국가 × 6 이슈 × 5 샘플 = 600 LLM calls. Claude API 기준 약 $20–40.
- Stage 2: R-GAT 학습 1–2시간 (RTX 4090 or equivalent). NetworkX/PyG로 CPU-only도 가능 (그래프가 작으므로).
- Stage 3: 브리핑 1회 생성 시 LLM call 30–50회 (섹션별). 약 $2–5.
- Total: **약 $30–50, 학습 시간 1–2시간** per 실험.

---

## 다음 문서
- [03_data_architecture.md](03_data_architecture.md) — 데이터 수집·스키마 상세
- [04_stage1_stance_extraction.md](04_stage1_stance_extraction.md) — Stage 1 프롬프트·calibration 상세
- [05_stage2_graph_analysis.md](05_stage2_graph_analysis.md) — R-GAT 구현 상세
- [06_stage3_briefing_generation.md](06_stage3_briefing_generation.md) — 브리핑 생성 상세
- [07_evaluation_protocol.md](07_evaluation_protocol.md) — 평가 설계
