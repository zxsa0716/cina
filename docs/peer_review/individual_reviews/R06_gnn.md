# R6 — GNN / Graph Learning Reviewer 슬롯

```yaml
reviewer_id: R6
reviewer_field: Heterogeneous Graph Neural Networks / R-GAT / GAT interpretability
reviewer_proxy_affiliation: 가상 — NeurIPS / ICLR 평가 위원
review_date: <to be filled>
status: ⬜ EMPTY
```

## 책임 영역

- Schlichtkrull (2018) R-GCN과 Veličković (2018) GAT 인용 정확성
- Heterogeneous R-GAT 구현의 architecture 정합성
- "Emergent chair attention 1.00" 주장의 robustness
- Multi-task loss design (stance + coalition + contested)
- Leiden vs R-GAT 결과 비교의 적절성

## 예상 강점

- Relation-specific attention (chair / member / similar / has_stance)는 표준 R-GCN+GAT 결합으로 적절
- Multi-task 학습으로 procedural authority signal이 emergent하게 학습된다는 결과는 흥미

## 예상 약점

- **결정적**: 13 노드 그래프에서 학습된 attention의 robustness는 매우 약함. Random seed 1개로 측정한 attention 1.00은 "emergent recovery"라기보다 "small-graph artefact" 가능성
- Attention weight의 절대값(1.00)은 softmax 정규화 결과. 노드 i가 chair edge가 1개뿐이면 softmax(single edge) = 1.00은 자명. "1.00" 자체보다 "다른 edge를 가진 노드들의 chair edge attention rank"가 더 의미 있는 측정
- 13 노드는 GAT 학습으로는 너무 작음. Transductive setting에서 train/val 분할 어떻게 했는지 명시 부재 (사실상 over-fit 가능)
- Coalition accuracy 0.77은 Leiden community label에 대한 다수결 분류이지 unsupervised learning이 아님. 이미 라벨이 graph structure에 implicit
- Schlichtkrull 2018 R-GCN의 "basis decomposition" 또는 "block diagonal decomposition"이 본 구현에 적용되지 않음. Standard hetero-GAT에 그쳤는데, R-GCN의 기여인 weight sharing trick의 부재가 명시되지 않음

## 예상 점수

```yaml
A1_scientific_accuracy: 3
A2_methodological_rigor: 2     # n 작음, single seed
A3_theoretical_grounding: 3
A4_honesty_self_criticism: 4
A5_practicality_impact: 3
A6_RGAT_architecture_correctness: 3
A7_attention_interpretability: 2     # "1.00" claim의 robustness 부족
```

## 예상 top-3 action items

```yaml
- priority: high
  item: |
    R-GAT 학습을 5+ random seeds × 200 epochs로 재실행. Attention weight
    분포의 mean ± std 보고. "Chair edge attention 1.00"을 "0.94 ± 0.03"
    같은 statistically valid 표현으로 변경.
  estimated_effort: 1 week

- priority: high
  item: |
    13 노드 transductive over-fit 우려에 대응. (a) 더 큰 그래프 (n ≥ 50)
    구축, 또는 (b) leave-one-country-out cross validation으로 
    generalization 검증.
  estimated_effort: 4 weeks

- priority: medium
  item: |
    Schlichtkrull R-GCN basis decomposition을 적용하거나, 적용하지
    않는 이유를 명시. "Standard hetero-GAT"가 R-GCN+GAT의 어느 부분을
    구현했는지 architecture diagram 추가.
  estimated_effort: 1 week
```

## 예상 의사결정

```yaml
recommendation:
  decision: Reject (현 형태) / Major Revision
  target_venue_assessment: |
    NeurIPS CCAI Workshop 2026 (poster, preliminary OK). ICLR / NeurIPS
    main track 무리 (n 작음). GraphML at NeurIPS 가능 if n 확장.
  conditions_for_acceptance: |
    1. Multi-seed attention robustness
    2. n ≥ 50 또는 cross-validation
    3. Architecture details 명시
```

---

**Status**: ⬜ Empty template.
