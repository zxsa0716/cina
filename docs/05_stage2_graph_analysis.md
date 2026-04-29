# 05. Stage 2 — Heterogeneous Temporal Graph Analysis

> Stage 2의 목표: Stage 1의 스탠스 텐서를 이종·시간 그래프로 구축하고, R-GAT 학습·커뮤니티 탐지·centrality 분석으로 연합 구조를 추출.

## 1. 그래프 구성 상세

### 1.1 노드 유형과 피처

**Country Nodes** ($|V_N| \approx 195$, 실제 적극 참여국 ~60)
```python
country_features = {
    "gdp_per_capita_log": float,          # World Bank
    "co2_per_capita": float,              # Global Carbon Atlas
    "nd_gain_vulnerability": float,       # ND-GAIN Index 2024
    "climate_finance_role": int,          # 0=recipient, 1=contributor, 2=both
    "region_onehot": [float] * 7,         # Africa, Asia, Europe, LAC, NA, Oceania, MENA
    "annex1_status": int,                 # 0=non-Annex I, 1=Annex I, 2=Annex II
    "ldc_status": int,                    # 0/1
    "sids_status": int,                   # 0/1 (Small Island Developing State)
    "oil_exporter": int,                  # 0/1
    "cop_attendance_rate": float,         # 지난 5년 COP 참석률
}
# 총 d_country = 32
```

**Issue Nodes** ($|V_I| = 6$)
```python
issue_features = {
    "issue_category_onehot": [float] * 6,  # 적응/감축/재원/기술/손실&피해/공정전환
    "technical_complexity": float,         # 전문가 의존도 (0~1)
    "historical_contention": float,        # ENB 기반 대립 빈도 (지난 5년)
    "cop30_priority": float,               # 의장국 공식 우선순위 (0~1)
    "paris_art_reference": int,            # 해당 Paris Art. 번호
    "time_horizon": int,                   # 단기/중기/장기 (1/2/3)
}
# 총 d_issue = 16
```

**Group Nodes** ($|V_G| = 12$)
- G77+China, LDCs, AOSIS, AILAC, Arab Group, African Group, EU, Umbrella Group, EIG, LMDC, BASIC, HAC
```python
group_features = {
    "size_log": float,                   # log(member count)
    "developing_share": float,           # 개도국 비중
    "climate_vulnerability_mean": float, # 회원국 ND-GAIN 평균
    "historical_cohesion": float,       # ENB 기반 그룹 응집도
}
# 총 d_group = 8
```

### 1.2 엣지 유형

| Type | (src, tgt) | Weight Semantics | Direction |
|------|-----------|------------------|-----------|
| `has_stance` | (Country, Issue) | $S_{n,i,t} \in [−1,+1]$ | directed |
| `similar_to` | (Country, Country) | cosine sim of stance vectors | undirected |
| `cooperates_with` | (Country, Country) | ENB-coded cooperation freq (log) | undirected |
| `member_of` | (Country, Group) | 1.0 | directed |
| `related_issue` | (Issue, Issue) | linkage potential (from `flexibility_signals`) | undirected |

### 1.3 시간 차원
각 엣지는 연도별 `edge_attr`. 주요 시점: COP21 (Paris), COP26 (Glasgow), COP27 (L&D fund 결정), COP28 (UAE GST), COP29 (Baku NCQG), COP30 (Belém).

짧은 시계열(T=6)이므로 GRU-based temporal encoder보다는 **시점별 그래프 snapshot의 sequence**로 모델링하고, Stage 2.5에서 시점 간 변화 패턴을 계산.

---

## 2. R-GAT 모델 구현

### 2.1 아키텍처

```python
import torch
import torch.nn as nn
from torch_geometric.nn import HeteroConv, GATv2Conv, Linear

class CINAHeteroGAT(nn.Module):
    def __init__(self, metadata, hidden_dim=64, num_layers=3, heads=4):
        super().__init__()
        self.node_embed = nn.ModuleDict({
            nt: Linear(-1, hidden_dim)  # -1 means infer input size
            for nt in metadata[0]  # node types
        })
        
        self.convs = nn.ModuleList()
        for _ in range(num_layers):
            conv = HeteroConv({
                et: GATv2Conv(
                    (-1, -1), hidden_dim, heads=heads,
                    concat=False, add_self_loops=False,
                )
                for et in metadata[1]  # edge types
            }, aggr='sum')
            self.convs.append(conv)
        
        self.readout = nn.ModuleDict({
            nt: Linear(hidden_dim, hidden_dim)
            for nt in metadata[0]
        })
    
    def forward(self, x_dict, edge_index_dict, return_attention=False):
        # Initial embedding
        x_dict = {k: self.node_embed[k](v).relu() for k, v in x_dict.items()}
        
        attention_weights = []
        for conv in self.convs:
            if return_attention:
                x_dict, att = conv(x_dict, edge_index_dict, return_attention_weights=True)
                attention_weights.append(att)
            else:
                x_dict = conv(x_dict, edge_index_dict)
            x_dict = {k: v.relu() for k, v in x_dict.items()}
        
        out = {k: self.readout[k](v) for k, v in x_dict.items()}
        if return_attention:
            return out, attention_weights
        return out
```

### 2.2 학습 목표 (Multi-task)

**Task 1 — Stance Edge Prediction (Link Prediction)**
무작위로 20% `has_stance` 엣지를 masking. 나머지로 학습하고, masked 엣지의 weight 예측.
Loss: MSE between predicted and actual stance weight.

**Task 2 — Coalition Consistency (Contrastive)**
동일 그룹 국가 쌍은 임베딩 거리 < 다른 그룹 쌍.
Triplet loss: $\mathcal{L} = \max(0, d(a,p) - d(a,n) + \text{margin})$

**Task 3 — Outcome Prediction (Supervised; 선택적)**
Castro et al. 2025에서 "COP 결과에서 국가 X가 최종 합의문에 찬성했는지" 라벨을 활용.

**Joint loss**:
$$\mathcal{L} = \lambda_1 \mathcal{L}_{\text{link}} + \lambda_2 \mathcal{L}_{\text{coal}} + \lambda_3 \mathcal{L}_{\text{outcome}}$$

초기값: $\lambda = (0.5, 0.3, 0.2)$.

### 2.3 학습 설정
- Optimizer: AdamW, lr=1e-3, weight_decay=1e-5
- Batch: 전체 그래프 (transductive 학습)
- Epochs: 200, early stopping patience=30
- 검증: 10% 엣지 holdout
- 하드웨어: RTX 4090 or Colab A100

---

## 3. Analysis Pipeline

### 3.1 커뮤니티 탐지 (Leiden)

```python
import igraph as ig
import leidenalg

def detect_communities(embeddings, issue_id, k=5, gamma=1.0):
    # k-NN graph from embeddings
    from sklearn.neighbors import kneighbors_graph
    sparse_knn = kneighbors_graph(embeddings, n_neighbors=k, mode='distance')
    
    # iGraph + Leiden
    g = ig.Graph.Weighted_Adjacency(
        1 / (sparse_knn.toarray() + 1e-6),
        mode='undirected'
    )
    partition = leidenalg.find_partition(
        g, leidenalg.RBConfigurationVertexPartition,
        resolution_parameter=gamma,
    )
    return partition.membership
```

**이슈별 분리 실행**: 6개 이슈 각각에 대해 countries 임베딩을 issue 노드에 대한 attention-weighted projection으로 추출 후 Leiden.

### 3.2 Centrality 집합

```python
import networkx as nx

def compute_centralities(G_nx, embeddings):
    return {
        "betweenness": nx.betweenness_centrality(G_nx, weight='weight'),
        "eigenvector": nx.eigenvector_centrality(G_nx, weight='weight', max_iter=1000),
        "attention_in": compute_attention_in_centrality(embeddings),  # R-GAT attention sum
    }
```

### 3.3 Cross-Issue Hypergraph

```python
from itertools import combinations

def detect_linkage_hyperedges(stances, min_support=0.2, min_issues=2, max_issues=4):
    """
    Apriori-style detection of linked flexibility patterns.
    
    For each country, build a flexibility vector f_n ∈ {0,1}^I:
      f_n[i] = 1 if country n shows flexibility_signals on issue i.
    
    Hyperedge (i1, i2, ..., ik) = set of issues where a nontrivial group of
    countries jointly show flexibility (support ≥ min_support).
    """
    flex_matrix = build_flex_matrix(stances)  # [N, I]
    
    hyperedges = []
    for size in range(min_issues, max_issues + 1):
        for issue_combo in combinations(range(I), size):
            jointly_flexible = flex_matrix[:, list(issue_combo)].all(axis=1).mean()
            if jointly_flexible >= min_support:
                countries = flex_matrix[:, list(issue_combo)].all(axis=1).nonzero()[0]
                hyperedges.append({
                    "issues": [issue_labels[i] for i in issue_combo],
                    "countries": [country_labels[c] for c in countries],
                    "support": float(jointly_flexible),
                    "pattern": classify_linkage_pattern(stances, countries, issue_combo),
                })
    return hyperedges
```

`classify_linkage_pattern` 는 다음 셋 중 하나 리턴:
- `linked_concession`: 국가들이 여러 이슈에서 동시에 양보 의사
- `package_demand`: 여러 이슈에서 동시에 강경, 묶음 타결 의도
- `divergent`: 이슈에 따라 입장 상반 (잠재적 거래 기회)

### 3.4 Epistemic Divergence Detection
COP30 Rube Goldberg 사례를 설명하는 핵심 진단:

```python
def epistemic_divergence_score(stances_per_country, expert_proposal, political_decision):
    """
    전문가 제안과 정치 합의 간 거리를, 국가별 epistemic_alignment 필드 분포로 설명.
    """
    aligned = sum(s.epistemic_alignment.aligns_with_expert_proposal == "full" for s in stances_per_country)
    divergent = sum(s.epistemic_alignment.aligns_with_expert_proposal == "divergent" for s in stances_per_country)
    political_weight = sum(country_power[s.country] for s in stances_per_country if s.epistemic_alignment.aligns == "divergent")
    
    return {
        "epistemic_alignment_ratio": aligned / len(stances_per_country),
        "political_weight_of_divergent": political_weight,
        "predicted_divergence_risk": political_weight / (aligned + political_weight + 1e-6),
    }
```

---

## 4. Attention-based XAI

R-GAT의 attention weights는 모델이 "어떤 엣지가 의사결정에 중요했는지"를 drop-in으로 제공.

### 4.1 해석 아티팩트
1. **Edge attention heatmap**: 국가×국가 행렬, 값=inbound attention. 시각화 시 상위 5% hub로 highlight.
2. **Attention-ranked evidence**: 어떤 stance edge가 모델의 coalition 판단에 가장 기여했는지, 그 엣지의 evidence_quote를 Stage 3 브리핑에서 우선 인용.

### 4.2 SHAP 보조
노드 피처 중요도는 SHAP로 추가 분석 (선택적):
```python
import shap
explainer = shap.DeepExplainer(model, background_data)
shap_values = explainer.shap_values(instance)
```

---

## 5. 출력 아티팩트 예시

```json
{
  "timestamp": "2026-05-15T10:00:00Z",
  "model_version": "CINA-RGAT-v2.0",
  "issue_analyses": {
    "GGA-IND": {
      "communities": [
        {
          "cluster_id": 0,
          "label": "pro-quantitative_bloc",
          "countries": ["EU","UK","Norway","Switzerland","Canada","Australia"],
          "centroid_stance": 0.78,
          "within_cluster_agreement": 0.89
        },
        {
          "cluster_id": 1,
          "label": "MoI-conditional_bloc",
          "countries": ["India","China","Saudi Arabia","Bolivia","Cuba","Pakistan"],
          "centroid_stance": -0.22,
          "within_cluster_agreement": 0.76
        },
        {
          "cluster_id": 2,
          "label": "vulnerability-first_bloc",
          "countries": ["AOSIS","LDCs","Kenya","Costa Rica"],
          "centroid_stance": 0.45,
          "within_cluster_agreement": 0.81
        }
      ],
      "bridge_countries": [
        {"country":"South Africa","betweenness":0.34,"rationale":"connects BASIC to African Group"},
        {"country":"Brazil","betweenness":0.31,"rationale":"chair role, spans G77 and BASIC"}
      ],
      "top_attention_nodes": [
        {"country":"EU","attention_sum":0.87,"role":"agenda_setter"},
        {"country":"Brazil","attention_sum":0.71,"role":"bridge"}
      ]
    }
  },
  "cross_issue_hyperedges": [
    {
      "issues": ["GGA-IND","ADAPT-FIN"],
      "countries": ["India","LMDC_core"],
      "support": 0.31,
      "pattern": "package_demand",
      "interpretation": "Indicators acceptable IFF finance tripled — package deal opportunity."
    }
  ],
  "epistemic_divergence": {
    "GGA-IND": {
      "predicted_divergence_risk": 0.62,
      "high_political_weight_dissenters": ["Brazil","China","India","Saudi Arabia"],
      "interpretation": "High risk that chair-driven compromise deviates from expert proposal."
    }
  }
}
```

---

## 6. 해석 가이드 (Stage 3로 전달)

각 출력 필드는 브리핑의 어느 섹션으로 흐르는지 매핑:

| Stage 2 출력 | Stage 3 브리핑 섹션 |
|-------------|---------------------|
| `communities` | §2. Coalition Map |
| `bridge_countries` | §3. Leverage Analysis |
| `cross_issue_hyperedges` | §4. Package Deal Opportunities |
| `epistemic_divergence` | §5. Red Lines and Risks |
| `top_attention_nodes` | §3. Leverage Analysis (보강) |

---

## 다음 문서
- [06_stage3_briefing_generation.md](06_stage3_briefing_generation.md)
