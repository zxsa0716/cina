---
name: graph-analyst
description: Stage 1 스탠스 텐서를 이종 시간 그래프로 구축하고, Heterogeneous Graph Attention Network(R-GAT)로 학습 후 커뮤니티 탐지·centrality·cross-issue hypergraph 분석을 수행. Heedo의 GAT 전문성과 직결. Stage 2 파이프라인 담당.
---

# Graph Analyst Skill

## 언제 이 skill을 호출하는가

- "그래프 분석 돌려"
- "연합 지도 그려줘"
- "브릿지 국가 찾아"
- `cina-orchestrator`가 Phase C에서 자동 위임

## 입력·출력

### Input
- `data/processed/stances.jsonl` — Stage 1 출력
- `data/raw/castro_2025/enb_interactions_1995_2023.csv` — cooperation ground truth
- Config:
```yaml
hidden_dim: 64
num_layers: 3
heads: 4
learning_rate: 1e-3
epochs: 200
patience: 30
leiden_gamma: 1.0
hypergraph_min_support: 0.2
seed: 42
```

### Output
- `data/processed/graph.pkl` — PyG HeteroData 객체
- `data/processed/graph_analysis.json` — 분석 결과 (커뮤니티, centrality, hyperedges)
- `data/processed/embeddings.npy` — 노드 임베딩
- `data/processed/attention_weights.npy` — R-GAT attention (XAI용)

## 작업 절차

### 1. 그래프 구축 (`src/stage2_graph/build.py`)
- 3-type 노드: Country (20+), Issue (6), Group (12)
- 5-type 엣지: has_stance, similar_to, cooperates_with, member_of, related_issue
- 시간 축: COP21–COP30 (6 snapshot)

자세한 스키마 → `docs/05_stage2_graph_analysis.md §1`

### 2. R-GAT 학습
- 모델: `CINAHeteroGAT` (docs/05 §2.1)
- Multi-task loss: link prediction + coalition consistency + (optional) outcome
- 20% holdout for validation
- 학습 완료 후 전체 그래프 임베딩 생성

### 3. 커뮤니티 탐지 (이슈별)
이슈마다:
1. 임베딩 → 이슈 노드에 대한 attention-weighted projection
2. k-NN 그래프 (k=5)
3. Leiden algorithm (resolution γ=1.0)
4. 결과 후처리: 클러스터 라벨링 (자동: "pro-quantitative_bloc" 등)

### 4. Centrality 계산
```python
import networkx as nx
G_nx = to_networkx(heterograph_country_country)
centralities = {
    "betweenness": nx.betweenness_centrality(G_nx, weight='weight', normalized=True),
    "eigenvector": nx.eigenvector_centrality(G_nx, weight='weight', max_iter=1000),
    "attention_in": compute_attention_in_centrality(model_attention_weights),
}
```

### 5. Cross-Issue Hypergraph
- 각 국가의 flexibility_signal 벡터 `f_n ∈ {0,1}^6` 구축
- Apriori-like mining: min_support=0.2, size 2~4
- 결과를 {linked_concession, package_demand, divergent} 세 패턴으로 분류

### 6. Epistemic Divergence
각 이슈에 대해:
```python
aligned = sum(s.epistemic_alignment.aligns_with_expert_proposal == "full")
divergent = sum(... == "divergent")
political_weight = sum(country_power[s.country] for s in divergent_stances)
divergence_risk = political_weight / (aligned + political_weight + 1e-6)
```

### 7. 출력 JSON 작성
[docs/05 §5 출력 아티팩트] 형식. 각 필드를 Stage 3 섹션에 매핑.

## Attention XAI 산출물

모델 attention을 기반으로:
1. Edge attention heatmap (matplotlib + seaborn)
2. Top-K attention paths (어떤 엣지가 특정 예측에 기여했는지)
3. Per-claim attention tracing (Stage 3 evidence grounding에 사용)

저장: `data/processed/xai/` 하위 PNG + JSON

## 재현성

- 모든 random source (numpy, torch, python hash) seed 고정
- 학습 로그: TensorBoard (`runs/cina/`)
- 하이퍼파라미터 전체 저장: `config.yaml`

## 의존성

- `torch`, `torch_geometric`, `torch_geometric.nn.HeteroConv`
- `networkx`, `python-igraph`, `leidenalg`
- `scikit-learn`, `numpy`, `pandas`
- GPU 권장 (CPU도 가능, 그래프 작음)

## 실행 시간

- 그래프 구축: 5분
- R-GAT 학습: 1–2시간 (RTX 4090), 8시간 (CPU)
- 분석: 10분

## 품질 자동 점검

- Graph statistics: nodes, edges per type, average degree
- Training curves: loss plateau, validation metric convergence
- Community quality: modularity, coverage
- Centrality sanity check: EU/US의 eigenvector가 상위권인지

기준 미달:
- Modularity < 0.3 → "커뮤니티 구조 약함, 임베딩 차원 조정"
- 학습 loss diverge → "learning rate 하향 조정"

## Heedo의 전문성 활용 포인트

- GAT attention weight를 XAI 근거로 사용하는 패턴은 Heedo의 Urban Climate 논문 연장선
- IPCC Hazard-Exposure-Vulnerability 프레임이 국가 노드 피처 (nd_gain_vulnerability 등)에 반영
