# R7 — 그래프 / 네트워크 모델링 교수 (GNN / Network Science) — Review Brief

> **Persona**: ETH Zürich Network Lab / 서울대 산업공학과 GNN 그룹
> **분과 기여 영역**: Leiden, R-GAT 아키텍처, attention 해석, modularity
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ☐ Pending · ☐ In progress · ☐ Complete

## 핵심 평가 관점
n=13 노드의 작은 그래프에서 도출된 Leiden modularity 0.31과 R-GAT chair attention 1.00이 통계적으로 견고한지, attention의 emergent 해석이 정당한지를 본다. 작은 그래프에서의 statistical fluctuation을 결과로 over-interpret 하지 않았는지가 핵심.

## Reading list
| 우선순위 | 파일 |
|---------|------|
| ⭐ P0 | `src/stage2_graph/rgat.py`, `src/stage2_graph/advanced_analysis.py` |
| ⭐ P0 | `docs/web/figures/fig5_similarity_network.png`, `fig8_rgat_training.png` |
| ⭐ P0 | `docs/05_stage2_graph_analysis.md`, `docs/15_stage2_features_v2.md` |
| ⭐ P0 | `data/sample/graph_analysis.json`, `rgat_training_results.json` |
| P1 | `data/processed/bayesian_decomposition.json` (regime σ = 0.04 vs Leiden) |

## Adversarial 검토 8가지
1. **n=13 노드의 Leiden modularity 0.31 — random graph permutation test 부재** — 통계적 유의성 입증 없이 "stable communities" 주장
2. **R-GAT chair attention 1.00의 multi-task loss confounding** — coalition + contested label에 chair가 포함되어 있어 attention이 high할 수밖에 없는 데이터 누설 가능성
3. **Edge type imbalance 미통제** — co_chairs 엣지는 6개 (Brazil → 6 issues), similar_to는 N×3, has_stance는 ~78. attention의 비대칭은 데이터 imbalance 때문일 수 있음
4. **R-GAT vs vanilla GAT vs MLP baseline 미비교** — heterogeneous attention의 marginal contribution 미입증
5. **Bayesian σ_regime = 1.4%와 Leiden modularity 0.31의 정면 충돌이 paper에서 충분히 다루어지지 않음** — 두 결과가 동시에 의미 있다는 주장은 modeling 모순
6. **Attention 해석의 알려진 한계 (Jain & Wallace 2019, Wiegreffe & Pinter 2019)에 대한 인용 부재** — "attention is not explanation" 논쟁
7. **Resolution sweep γ ∈ [0.7, 1.3]만으로 stability claim 부족** — 더 넓은 sweep + 다른 community algorithm (Louvain, SBM) 비교 필요
8. **n=13에서 8 train + 5 val split은 R-GAT validation으로 의미 있는가** — overfitting 거의 보장된 setting

## Rubric (D2 Methodological rigor + D3 Empirical robustness가 핵심)

| Dim | Score | Justification |
|-----|-------|---------------|
| D1 Theoretical contribution (Network Science) | __/5 | |
| D2 Methodological rigor ⭐ | __/5 | |
| D3 Empirical robustness ⭐ | __/5 | |
| D4 Honesty / framing | __/5 | |
| D5 Reproducibility | __/5 | |
| D6 Practical / policy | __/5 | |
| D7 Literature integration (GNN literature) | __/5 | |
| D8 Writing quality | __/5 | |
| D9 Novelty argument | __/5 | |
| D10 Submission readiness (Network venue) | __/5 | |
| **Total** | **__/50** | |

## 작성 시
### Top 3 strengths / weaknesses
### Most likely reject reason at NeurIPS / ICML / NetSci
### Worst over-interpretation
### Required revisions (P0/P1/P2)
### Venue recommendation
☐ NeurIPS / ICML main ☐ NetSci ☐ NeurIPS CCAI Workshop ☐ arXiv preprint ☐ Reject
**Reasoning**:
### Open questions

---
*Reviewer signature*: R7 GNN Persona · Simulated peer review.
