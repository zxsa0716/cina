# R6 — 머신러닝 / NLP 교수 (LLM evaluation) — Review Brief

> **Persona**: Stanford NLP / KAIST AI 대학원 / Allen AI
> **분과 기여 영역**: LLM-기반 측정의 validity, prompt engineering, calibration
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ☐ Pending · ☐ In progress · ☐ Complete

## 핵심 평가 관점
이 reviewer는 LLM stance extraction의 측정학적 validity를 본다. Cross-LLM α = 0.93의 "shared-model bias 분리" 주장이 학술적으로 정당한가, prompt engineering 표준에 부합하는가, multi-sample k=5의 통계적 의미가 정당화되었는가.

## Reading list
| 우선순위 | 파일 |
|---------|------|
| ⭐ P0 | `src/stage1_extract/extract_v2.py`, `src/stage1_extract/cross_llm_consistency.py` |
| ⭐ P0 | `docs/04_stage1_stance_extraction.md` |
| ⭐ P0 | `deliverables/evaluation_report.md` (Phase 5) |
| P1 | `data/sample/stances_sample_10.jsonl` (실제 출력 품질) |
| P1 | `RUN_REPORT.md` (per-LLM bias 결과) |

## Adversarial 검토 8가지
1. **Cross-LLM α의 "shared-model bias 분리" 주장 over-reach** — Gemini, Groq Llama, Anthropic, Ollama Qwen, OpenRouter 5종 모두 transformer + RLHF 기반. 진정한 paradigm 분리 아님
2. **Multi-sample k=5의 통계적 정당화 부재** — k=10, k=20 vs k=5의 marginal contribution 미측정
3. **Beta-binomial 95% CI의 prior 정당화 부재** — uninformative prior 가정의 적정성
4. **Platt scaling calibration set n=50의 statistical power 미입증**
5. **Stance score를 -1~+1 continuous로 추출하면서 "stance_category" 6-class도 함께 출력 — 두 출력의 consistency 미검증**
6. **Evidence quote의 RapidFuzz threshold 85가 자의적** — 임계치 sensitivity analysis 부재
7. **LLM-as-judge in Task D는 self-evaluation circular** — 같은 LLM family가 생성하고 평가하는 구조의 inflation
8. **Recent LLM stance benchmarks (Cambridge 2024 Stay Tuned)에 대한 비교 부재** — Spearman ρ = 0.658이 동분야 SOTA 대비 어디 위치인지

## Rubric (D2 Methodological rigor + D3 Empirical robustness + D4 Honesty가 핵심)

| Dim | Score | Justification |
|-----|-------|---------------|
| D1 Theoretical contribution (NLP / ML) | __/5 | |
| D2 Methodological rigor ⭐ | __/5 | |
| D3 Empirical robustness ⭐ | __/5 | |
| D4 Honesty / framing ⭐ | __/5 | |
| D5 Reproducibility | __/5 | |
| D6 Practical / policy | __/5 | |
| D7 Literature integration (NLP benchmarks) | __/5 | |
| D8 Writing quality | __/5 | |
| D9 Novelty argument | __/5 | |
| D10 Submission readiness (NLP venue) | __/5 | |
| **Total** | **__/50** | |

## 작성 시
### Top 3 strengths / weaknesses
### Most likely reject reason at NLP venue (ACL / EMNLP / Findings)
### Worst measurement claim
### Required revisions (P0/P1/P2)
### Venue recommendation
☐ ACL / EMNLP main ☐ Findings ☐ NeurIPS CCAI Workshop ☐ arXiv preprint ☐ Reject
**Reasoning**:
### Open questions

---
*Reviewer signature*: R6 NLP Persona · Simulated peer review.
