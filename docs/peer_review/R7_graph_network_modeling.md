# R7 — 그래프 / 네트워크 모델링 교수 (GNN / Network Science) — Review (COMPLETE)

> **Persona**: ETH Zürich Network Lab / 서울대 산업공학과 GNN 그룹
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ✅ Complete · 2026-05-05

---

## 1. Summary judgement

n=13 노드의 작은 그래프에서 도출된 Leiden modularity 0.31과 R-GAT chair attention 1.00은 **통계적 유의성 검증 부재 + multi-task confounding 통제 부재**로 over-interpretation 위험이 매우 크다. Bayesian σ_regime=1.4%와 Leiden 결과의 정면 충돌이 paper에서 충분히 다루어지지 않은 것이 가장 심각한 문제. NeurIPS / ICML / NetSci 본 투고는 무리이며, NeurIPS CCAI Workshop 또는 application track이 적정. 그래프 분석의 production grade를 위해서는 (a) random graph permutation test, (b) multi-task ablation, (c) 더 큰 노드 set replication이 P0 필수.

## 2. Rubric scores

| Dimension | Score | One-line justification |
|-----------|-------|------------------------|
| D1 Theoretical contribution (Network Science) | 2.0/5 | n=13 그래프에서 새로운 network science 발견 부재. |
| D2 Methodological rigor ⭐ | 1.5/5 | Random graph permutation test 부재, edge type imbalance 통제 부재, GNN baseline 비교 부재. |
| D3 Empirical robustness ⭐ | 1.5/5 | n=13 Leiden + 8 train/5 val R-GAT는 과적합 거의 보장된 setup. |
| D4 Honesty / framing | 4.0/5 | CRITICAL_REVIEW에서 limitation 인정 자세 양호. |
| D5 Reproducibility | 4.0/5 | 코드 + figure 재생성 가능. |
| D6 Practical / policy | 1.5/5 | Network science 분과 reviewer는 정책 응용 부차적. |
| D7 Literature integration (GNN literature) | 2.0/5 | Schlichtkrull 2018, Veličković 2018 인용은 했으나 attention interpretability 논쟁 (Jain & Wallace 2019) 미언급. |
| D8 Writing quality | 3.0/5 | 그래프 분석 voice 표준. |
| D9 Novelty argument | 2.5/5 | "Emergent chair attention"은 흥미롭지만 over-interpretation 위험. |
| D10 Submission readiness (Network venue) | 1.5/5 | NeurIPS / NetSci 본 투고는 desk reject 가능성 높음. |

**Total: 23.5/50** · **Average: 2.35/5**

## 3. Top 3 strengths

1. **Heterogeneous R-GAT의 4 relation type 분리 (has_stance, member_of, similar_to, co_chairs) + per-relation attention 학습은 도메인 specific GNN 설계의 좋은 사례**. Multi-task loss 구조도 well-motivated.

2. **NetworkX 기반 numpy power-iteration centrality (PageRank, eigenvector)는 networkx 의존성 없이도 작동하도록 한 robust engineering 결정**. 이전 fig4 hang issue를 해결한 사례.

3. **Bayesian variance decomposition으로 Leiden 결과를 자기 검증한 시도는 학제간 honest reporting**. σ_regime=1.4% vs Leiden modularity 0.31의 충돌을 숨기지 않고 paper에 명시한 것은 학술적 정직성으로 평가 가능 (단, 이 충돌의 modeling 의미를 추가로 해석해야 함).

## 4. Top 3 weaknesses (specific, actionable)

1. **n=13 노드 Leiden modularity 0.31의 통계적 유의성 검증 부재**. 13개 노드 그래프에서 modularity 0.31은 random graph (Erdős–Rényi 또는 configuration model)에서도 충분히 발생 가능한 수준이다. 권장: 1000회 random graph permutation 후 modularity 분포의 95th percentile과 비교. 만일 통계적으로 유의하지 않다면 "stable communities" 주장 자체가 약화된다.

2. **R-GAT chair attention 1.00의 confounding 통제 부재**. 본 setup에서 (a) `co_chairs` edge는 6개 (Brazil → 6 issues) 단일 source-from, (b) coalition label에 chair 정보가 부분적으로 포함, (c) contested label도 chair-relevant issue에 편중. Multi-task supervision이 chair edge에 의존하는 것이 자연스러운 결과일 수 있다. 권장: ablation study (i) coalition + contested supervision 제거 후 stance-only 학습 시 attention 분포, (ii) co_chairs edge type 자체 제거 후 stance prediction performance 비교, (iii) chair-edge data augmentation balance 변화 시 attention 변화.

3. **Bayesian σ_regime = 1.4% vs Leiden modularity 0.31 결과의 modeling 의미 disentangle 부재**. paper.md §4.2는 이 충돌을 "n=13 partition의 한계"로 처리하나, network science 관점에서는 (a) Leiden은 *connectivity pattern* (edge 존재 여부 + weight)을 분석하고, (b) Bayesian 3-level은 *stance variance* (node attribute의 분산)을 분해하는 별도 modeling이다. 두 결과는 서로 다른 데이터 generating process를 가정한 측정이므로 직접 비교 부적절. 이 점을 §4.2에 추가하지 않으면 GNN reviewer는 "두 결과가 충돌하니 둘 다 못 믿겠다"로 판단.

## 5. Adversarial finding

### Most likely reject reason at NeurIPS / ICML / NetSci

> "본 연구의 R-GAT 결과는 n=13 노드 / 8 train + 5 val 분할의 small-data setup에서 도출되어, GNN 분과 standard (n ≥ 100, 보통 n ≥ 1000)의 statistical power 요구를 충족하지 않는다. Leiden modularity 0.31의 random graph permutation test 부재는 'stable communities' 주장을 정당화하지 못한다. Chair-edge attention 1.00의 'emergent recovery' 해석은 multi-task supervision의 coalition/contested label에 chair-relevant 정보가 누설되어 있을 가능성을 통제하지 않은 단순 association이다. NeurIPS / ICML / NetSci main track 투고는 무리이며, application workshop (NeurIPS CCAI) 또는 climate-policy 학제간 venue가 적정. Multi-task confounding ablation + larger node set replication이 P0 필수."

### Worst over-interpretation

> (paper.md §4.2) "Crucially, the learned attention weights — without explicit supervision on procedural authority — are dominated by the `co_chairs` relation (mean attention 1.00) over `member_of` (0.35), `similar_to` (0.28), and `has_stance` (0.08). Because the model receives no procedural-authority supervision, this represents an **emergent recovery** of Tallberg's (2010) chair-channel hypothesis."

→ "Emergent recovery without supervision"은 정확하지 않다. 모델은 (i) coalition label, (ii) contested label에 supervised되어 있고, 두 label 모두 chair-relevant 정보를 부분 포함한다. "Without explicit supervision on procedural authority"는 직접 procedural authority label은 부재하나, indirect supervision은 존재한다. "Emergent" 표현은 강한 인과 주장이며, multi-task confounding ablation 결과가 같이 제시되어야만 정당화 가능.

## 6. Required revisions before submission (priority-ordered)

- **P0 (must fix)**:
  1. Leiden modularity 0.31의 random graph permutation test (1000 회) 추가, p-value 보고
  2. R-GAT multi-task confounding ablation: stance-only, coalition-only, contested-only 학습 시 attention 분포 비교 표
  3. Bayesian σ_regime vs Leiden modularity 충돌의 modeling 의미 disentangle 단락 (§4.2 확장)
  4. n=13의 small graph limitation을 paper.md abstract와 §1에 명시. METHODOLOGY_ADVANCEMENT_ROADMAP의 E5 longitudinal extension을 paper.md §7로 이전
- **P1 (should fix)**:
  1. Vanilla GAT (no relation type) baseline 비교 추가
  2. Jain & Wallace (2019) "Attention is not Explanation" 인용 추가 + 본 연구가 어떻게 그 비판에 응답하는지
  3. Edge type imbalance (co_chairs 6 vs has_stance 78) 통제 ablation
- **P2 (nice to have)**:
  1. Pyg (PyTorch Geometric) standard implementation으로 마이그레이션 (현재 from-scratch)
  2. Wu et al. 2024 또는 최근 GNN climate 응용 인용

## 7. Venue recommendation

- ☐ NeurIPS / ICML main
- ☐ NetSci (Network Science Society)
- ☑️ NeurIPS CCAI 2026 Workshop (climate application track)
- ☐ arXiv preprint
- ☐ Reject

**Reasoning**: GNN 분과 표준에서 small-graph limitation이 본 투고를 막는다. Application workshop에서 method paper로 발표한 후, longitudinal extension (E5) 완료 후 본 venue 재고려.

## 8. Open questions for the author

1. Leiden modularity 0.31의 random graph permutation p-value는 측정한 적 있는가?
2. R-GAT 학습이 stance-only label에서 (coalition + contested 제거) chair attention을 동일하게 학습하는가? 이는 confounding 통제의 핵심 ablation.
3. Bayesian σ_regime과 Leiden modularity가 서로 다른 modeling assumption 하에서 무엇을 측정하는지 이론적 disentangle이 paper에 명시되었는가?
4. Pyg (PyTorch Geometric) standard library 대신 from-scratch 구현을 선택한 이유는?

---

*Reviewer signature*: R7 GNN Persona (ETH Zürich / 서울대 산업공학)
*Honesty disclosure*: Simulated peer review.
