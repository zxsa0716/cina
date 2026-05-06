# R6 — 머신러닝 / NLP 교수 (LLM evaluation) — Review (COMPLETE)

> **Persona**: Stanford NLP / KAIST AI 대학원 / Allen AI
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ✅ Complete · 2026-05-05

---

## 1. Summary judgement

LLM stance extraction의 측정학적 자기 검증 시도(Cross-LLM α, ablation)는 NLP 분야 표준에 부합하나, **"shared-model bias 분리" 주장이 5종 LLM 모두 transformer + RLHF 패러다임 공유의 사실을 무시한 over-reach**이고, **multi-sample k=5의 통계적 정당화 부재**, **Beta-binomial CI prior 정당화 부재**, **Spearman ρ=0.658이 동분야 SOTA (Cambridge "Stay Tuned" 2024 등) 대비 어디 위치인지 비교 부재**가 NLP venue reviewer의 즉시 reject 사유. NeurIPS CCAI Workshop short paper는 가능하지만 ACL/EMNLP main은 무리.

## 2. Rubric scores

| Dimension | Score | One-line justification |
|-----------|-------|------------------------|
| D1 Theoretical contribution (NLP / ML) | 2.5/5 | Multi-axis joint extraction은 적용 영역 기여, 새 method 자체는 아님. |
| D2 Methodological rigor ⭐ | 2.5/5 | k=5, Beta-binomial CI, Platt scaling 등 기술 stack은 표준이나 정당화 약함. |
| D3 Empirical robustness ⭐ | 2.0/5 | Spearman 0.658이 동분야 SOTA 대비 어디 위치인지 미비교 + Task D self-eval 문제. |
| D4 Honesty / framing ⭐ | 4.5/5 | Simulated panel 명시 + CRITICAL_REVIEW의 자기 비판은 NLP 분야에서 매우 정직한 자세. |
| D5 Reproducibility | 4.5/5 | 5-LLM provider abstraction + offline mock + sample data 우수. |
| D6 Practical / policy | 2.0/5 | NLP 분과 reviewer는 정책 응용을 부차적으로 봄. |
| D7 Literature integration (NLP benchmarks) | 2.0/5 | Stance detection benchmark literature 부족. Cambridge 2024 인용 부재. |
| D8 Writing quality | 3.5/5 | NLP 표준 voice 양호. |
| D9 Novelty argument | 3.0/5 | Cross-LLM α + emergent attention은 분명한 contribution 후보. |
| D10 Submission readiness (NLP venue) | 2.0/5 | ACL/EMNLP main 무리. Findings or workshop 적정. |

**Total: 28.5/50** · **Average: 2.85/5**

## 3. Top 3 strengths

1. **Cross-LLM Krippendorff α framework은 LLM-as-measurement 분야의 우수 자기 검증 시도**. raw 0.876 → bias-corrected 0.933의 per-LLM mean centering 보정 + per-LLM bias diagnosis (anthropic +0.118, ollama_qwen -0.158)는 measurement validity 입증의 좋은 실천.

2. **R-GAT chair-edge attention 1.00의 emergent finding은 attention interpretability 분야와 직접 대화 가능**. Multi-task supervision (stance + coalition + contested) 없이 chair signal이 학습된 결과는 (한계를 인정하더라도) NLP 분과에서 흥미로운 case.

3. **Offline mock LLM smoke test (`--offline` mode) + per-provider exit code는 production NLP 시스템의 모범**. 학술 paper에 production-readiness check 항목이 포함된 사례는 드물다.

## 4. Top 3 weaknesses (specific, actionable)

1. **"Cross-LLM α의 shared-model bias 분리" 주장의 over-reach**. 5종 LLM (Gemini 2.5 Flash-Lite, Groq Llama 3.3 70B, Anthropic Claude, Ollama Qwen 2.5, OpenRouter pool)은 모두 (a) transformer architecture, (b) RLHF / DPO / preference tuning 패러다임, (c) 영어 web text 위주의 사전 학습 corpus를 공유한다. 이들 사이의 α=0.93은 **same-paradigm agreement**이지 **shared-model bias로부터 분리된 reliability**가 아니다. 진정한 분리를 위해서는 (i) non-transformer baseline (예: BERT classifier on supervised stance dataset), (ii) human coder 1-2인의 동일 데이터 ground truth가 필요. 이 한계를 paper.md §3.2 또는 abstract에서 명시하지 않으면 NLP reviewer가 즉시 reject 사유로 삼는다.

2. **Multi-sample k=5의 통계적 정당화 부재**. 왜 k=5인가? k=3, k=10, k=20과의 marginal contribution 비교 없음. 대형 LLM API 비용 제약이라면 그 trade-off를 명시. 또한 k=5 sample이 i.i.d.인지 (temperature=0.3에서 LLM은 sampling correlation 가질 수 있음) 검증 부재. NLP 분야 표준은 k=10 이상 + bootstrap CI.

3. **Spearman ρ=0.658의 SOTA 대비 위치 미명시**. 정치 텍스트 stance detection 분야 최근 벤치마크: Cambridge "Stay Tuned" (Burnham 2024, *Political Analysis*) 등은 LLM stance detection에서 ρ=0.7-0.85 범위를 보고. 본 연구의 0.658이 동분야 어디에 위치하는지 비교 표 부재. NLP reviewer는 항상 SOTA 비교를 요구.

## 5. Adversarial finding

### Most likely reject reason at NLP venue (ACL / EMNLP / Findings)

> "본 연구의 cross-LLM α framework은 흥미로우나, 'shared-model bias 분리' 주장은 5종 LLM 모두 transformer + RLHF 패러다임 공유의 사실과 충돌한다. Same-paradigm agreement는 paradigm-independent reliability와 본질적으로 다르며, NLP 측정학에서는 non-transformer baseline 또는 human coder ground truth와의 비교가 표준이다. 또한 Spearman ρ=0.658는 정치 텍스트 stance detection 분야 최근 벤치마크 (Burnham 2024)의 0.7-0.85 대비 mid-low이며, 이를 명시하지 않은 채 'reasonable accuracy'로 표현한 것은 over-claim이다. R-GAT chair-edge attention 1.00의 emergent 해석은 multi-task loss와 chair-edge 데이터 imbalance를 통제하지 않은 결과이다. ACL main 투고는 무리이며, Findings 또는 workshop 단계에서 multi-task ablation + non-transformer baseline 추가 후 재고려."

### Worst measurement claim

> (paper.md Abstract) "We compute a cross-LLM Krippendorff α = 0.876 (raw) / 0.933 (bias-corrected, after per-LLM mean-centering) across five providers, providing a reliability bound that is partially decoupled from shared-model bias."

→ "decoupled from shared-model bias"는 5종 모두 transformer + RLHF인 사실 앞에서 measurement-theoretic claim으로 부적절. "partially decoupled from per-LLM systematic offset" 정도가 정확.

## 6. Required revisions before submission (priority-ordered)

- **P0 (must fix)**:
  1. "Shared-model bias 분리" 주장을 "per-LLM systematic offset 보정"으로 약화 또는 정확히 reframe. 5종 모두 transformer + RLHF임을 abstract에 disclose
  2. k=5 sample size의 정당화 + sampling correlation 검증 추가 (또는 limitation으로 명시)
  3. Spearman ρ 0.658의 동분야 SOTA (Burnham 2024 *Political Analysis*, Pavan & Mishra 2025 등) 비교 표 추가
  4. R-GAT emergent attention의 multi-task loss confounding ablation: stance-only, coalition-only, contested-only 학습 시 attention 분포 비교
- **P1 (should fix)**:
  1. Beta-binomial CI prior 정당화 (uninformative prior 가정 적정성)
  2. Evidence quote RapidFuzz threshold 85의 sensitivity analysis
  3. Non-transformer baseline (BERT classifier on existing stance dataset) 1개 추가
- **P2 (nice to have)**:
  1. Allen AI ai2-eval framework 또는 lm-eval-harness에 본 stance task 등록
  2. Hugging Face Hub에 fine-tuned 모델 (있으면) 또는 prompt template 공개

## 7. Venue recommendation

- ☐ ACL / EMNLP main
- ☐ Findings of ACL / EMNLP
- ☑️ NeurIPS CCAI 2026 Workshop (short paper)
- ☐ arXiv preprint
- ☐ Reject

**Reasoning**: NLP 분과 contribution은 method 자체보다 application + measurement validity check이므로 application workshop이 적합. ACL Findings는 P0 수정 후 재고려.

## 8. Open questions for the author

1. 5종 LLM이 모두 transformer + RLHF임을 인정한 상태에서, "shared-model bias 분리"는 어떻게 측정학적으로 정당화되는가?
2. k=5 sample size 결정의 prior 비용/정확도 trade-off 분석이 있는가?
3. Spearman ρ=0.658이 정치 텍스트 stance detection 분야에서 어떤 percentile에 해당하는가? Burnham 2024 등 최근 벤치마크 비교는?
4. R-GAT chair attention 1.00을 multi-task ablation으로 확인한 결과가 있는가? Single-task 학습 시 attention 분포는?

---

*Reviewer signature*: R6 NLP Persona (Stanford NLP / KAIST AI)
*Honesty disclosure*: Simulated peer review.
