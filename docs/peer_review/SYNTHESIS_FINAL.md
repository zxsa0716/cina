# 📊 CINA Peer Review Synthesis — 10-Reviewer Final Verdict

> **Status**: ✅ Complete · 10/10 reviewers · simulated peer review
> **Synthesis date**: 2026-05-05
> **Decision gate**: ❌ **NEEDS REVISION** (D2 fail, D5 marginal fail)
> **Recommended path**: arXiv preprint + NeurIPS CCAI Workshop + 한국 KCI 별도 논문 (3-track 병행)

---

## 1. 한 페이지 요약 (Executive synthesis)

10명의 다학제 reviewer (기후학·국제정치·외교실무·정책학·SE·NLP·GNN·통계·한국 KCI·편집위원)가 paper.md, ministerial_briefing_ko.md, 코드, figures, RUN_REPORT 등을 검토한 결과, **현 단계 paper의 학술 투고 readiness는 평균 2.0/5 (10가지 차원 중 가장 낮음)**이다. 동시에 **정직성 (D4 = 4.05/5)과 재현성 (D5 = 3.95/5)은 학생 single-author 프로젝트로서 매우 우수**하다. 즉 **방법론적 결함을 정직히 인정한 reproducible 학생 프로젝트**라는 honest characterisation이 종합 진단이다.

3가지 P0 cross-cutting weakness (4명 이상 reviewer 동의):
1. **Small-sample over-reach** (N=3 contested, n=78 stance, n=13 노드 모두) — 5명 (R6/R7/R8/R10/R3)
2. **Single-case Δ를 이론적 contribution으로 over-claim** — 4명 (R2/R4/R7/R10)
3. **외부 expert validation 부재** (Task D LLM 시뮬레이션) — 5명 (R1/R3/R8/R9/R10)

전반적 결론: **현 형태로 Q1 학술지 (GEC IF 11.2)는 desk reject 가능성 95% 이상**. 그러나 **NeurIPS CCAI 2026 Workshop short paper + 한국정책학회보 별도 한국어 단저자 논문 + arXiv preprint**의 3-track 병행은 **75% 이상 가능성**으로 평가된다.

---

## 2. 점수 매트릭스 (10 reviewers × 10 dimensions)

| Reviewer | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | **Total** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 Climate Sci | 2.5 | 2.5 | 2.5 | 4.0 | 4.0 | 3.0 | 2.5 | 3.5 | 2.5 | 2.0 | 29.0 |
| R2 IR Theory | 3.0 | 2.0 | 2.0 | 4.5 | 4.0 | 2.5 | 2.5 | 3.5 | 2.5 | 1.5 | 28.0 |
| R3 Practitioner | 2.0 | 2.5 | 2.5 | 3.5 | 3.0 | 3.0 | 2.5 | 3.0 | 2.5 | 2.0 | 26.5 |
| R4 Policy Sci | 2.5 | 2.0 | 2.5 | 4.0 | 4.0 | 3.5 | 2.5 | 3.5 | 2.5 | 2.0 | 29.0 |
| R5 SE / DevOps | 1.5 | 2.0 | 2.0 | 3.5 | 4.0 | 4.0 | 3.0 | 3.5 | 3.0 | 2.5 | 29.0 |
| R6 ML / NLP | 2.5 | 2.5 | 2.0 | 4.5 | 4.5 | 2.0 | 2.0 | 3.5 | 3.0 | 2.0 | 28.5 |
| R7 GNN / Network | 2.0 | 1.5 | 1.5 | 4.0 | 4.0 | 1.5 | 2.0 | 3.0 | 2.5 | 1.5 | 23.5 |
| R8 Stats | 2.0 | 1.5 | 1.0 | 4.5 | 4.0 | 1.5 | 2.0 | 3.0 | 2.5 | 1.5 | 23.5 |
| R9 Korean KCI | 3.0 | 3.0 | 3.0 | 3.5 | 3.5 | 4.0 | 3.0 | 3.0 | 3.0 | 2.5 | 31.5 |
| R10 Editor | 2.5 | 2.5 | 2.0 | 4.5 | 4.5 | 3.0 | 3.0 | 4.0 | 3.0 | 2.5 | 31.5 |
| **평균** | **2.35** | **2.20** | **2.10** | **4.05** | **3.95** | **2.80** | **2.50** | **3.35** | **2.70** | **2.00** | **28.0** |
| **표준편차** | 0.47 | 0.48 | 0.57 | 0.44 | 0.44 | 0.92 | 0.41 | 0.34 | 0.26 | 0.41 | 2.7 |

**해석**:
- 가장 낮은 차원: **D10 Submission readiness (2.00)** — 모든 reviewer가 "현 상태 그대로는 투고 무리" 합의
- 두 번째 낮은 차원: **D3 Empirical robustness (2.10)** — small sample / N=3 / n=78 / single case가 cross-cutting issue
- 가장 높은 차원: **D4 Honesty (4.05)** — 자기 비판 일관성과 limitation 명시 우수
- 두 번째 높은 차원: **D5 Reproducibility (3.95)** — 코드 + 데이터 + 방법론 공개 우수 (단 0.05 차이로 임계치 미통과)
- 가장 disagreement 큰 차원: **D6 Practical/policy (σ = 0.92)** — 분과별 lens 차이 (R5 SE = 4.0 vs R7 GNN = 1.5)
- 가장 agreement 큰 차원: **D9 Novelty argument (σ = 0.26)** — 모든 reviewer가 "novelty가 분산되어 sharpening 필요" 일치

---

## 3. Decision gate 평가

| Gate | Threshold | Actual | Pass |
|------|-----------|--------|------|
| 평균 D2 (방법론 엄밀성) | ≥ 3.5 | **2.20** | ❌ 큰 폭 fail |
| 평균 D4 (정직성/framing) | ≥ 4.0 | **4.05** | ✅ 통과 |
| 평균 D5 (재현성) | ≥ 4.0 | **3.95** | ⚠️ 0.05 미달 |
| "Major reject" venue 추천 reviewer | ≤ 2명 | **0명** | ✅ 통과 |
| Krippendorff α (10 reviewers) | ≥ 0.5 | (계산 미실행) | — |

**Overall**: ❌ **NEEDS REVISION** — D2 큰 폭 미통과로 paper 본 투고 진행 불가.

D4·D5는 통과/근접이므로 **연구 자체는 정직성과 재현성 면에서 우수**하나, **방법론 엄밀성은 분과별 reviewer 표준에 미달**한다는 honest verdict.

---

## 4. Cross-cutting weaknesses (4+ reviewers 동의)

### W1. Small-sample over-reach — 5 reviewers (R6/R7/R8/R10/R3)
**Specific claims**: N=3 contested issue 예측, n=78 stance records, n=13 그래프 노드, single-case Brazil Δ.
**Why critical**: D3 (Empirical robustness) 평균 2.10의 직접 원인. random chance baseline (binomial p≈0.05) 또는 random graph permutation test 부재.

### W2. Single-case Δ를 이론적 contribution으로 over-claim — 4 reviewers (R2/R4/R7/R10)
**Specific claims**: paper.md §4.4 "Translation Gap Δ = 0.304 ... at the intersection of Two-Level Games and instrument calibration"; Abstract의 "novel single-case quantification".
**Why critical**: Bayer-Urpelainen 2014 등 양면게임 정량 선행 연구 부재 인정 + Howlett calibration의 frequency vs intensity 구별 부재.

### W3. 외부 expert validation 부재 (Task D simulated panel) — 5 reviewers (R1/R3/R8/R9/R10)
**Specific claims**: Task D 5-persona panel은 LLM 시뮬레이션. Krippendorff α=0.905는 shared-model bias inflation.
**Why critical**: 정직히 disclosure는 했으나, 실제 외부 expert (KEI/KAIST/MOFA/GEP) 섭외가 부재한 채 paper 본 투고는 reviewer pool에서 즉시 수용 거부.

### W4. Bayesian σ_regime vs Leiden modularity 충돌 미해결 — 3 reviewers (R2/R7/R10)
**Specific claims**: σ_regime = 1.4% vs Leiden modularity 0.31의 modeling assumption 차이를 paper에서 disentangle 안 함.
**Why critical**: 두 결과의 동시 보고가 inconsistent로 보임. Network science vs hierarchical regression의 무엇을 측정하는지 이론적 정리 필요.

### W5. 영-한 코드 스위칭 일관성 부족 — 3 reviewers (R3/R9/R10)
**Specific claims**: "regime complex", "norm entrepreneur", "Translation Gap Δ", "horizontal cleavage" 등 한국어 표기 미정착.
**Why critical**: 한국 KCI 학술지 reviewer가 즉시 수정 요구. 외교부 보고서 voice와도 분리.

---

## 5. Likely Reject Reasons (분과별)

| Source reviewer | Reject reason 요약 (1줄) | 영향 venue |
|-----------------|---------------------|------------|
| R1 Climate | UNFCCC 7-target과의 mapping 부재 + IPCC AR6 HEV framework 미적용 | Climate Policy / GEC |
| R2 IR | "First quantitative" over-claim + Bayesian-Leiden 충돌 | International Organization / GEP |
| R3 Practitioner | $5-10M pledge의 예산 절차 무시 + 1차 자료 인용 부족 | MOFA / KEI |
| R4 Policy | NATO 4축 supervised baseline 비교 부재 + frequency vs intensity 미구별 | Policy Sciences |
| R5 SE | pytest 0% + requirements 비-pinned + GitHub Actions 미설치 + subprocess hang | JOSS |
| R6 NLP | "Shared-model bias 분리" over-reach + Spearman 0.658 SOTA 비교 부재 | ACL / EMNLP |
| R7 GNN | n=13 modularity 통계 유의성 미입증 + R-GAT multi-task confounding 미통제 | NeurIPS / NetSci |
| R8 Stats | N=3 P@3=1.00의 random chance 대비 weak + DiD parallel-trends 미실행 | JASA |
| R9 Korean KCI | 영-한 코드 스위칭 + KCI 양식 미부합 + 단저자 학생 + 1차 자료 출처 부족 | 한국정책학회보 |
| R10 Editor | Novelty 분산 + 단저자 학생 + 영문/한국어 voice 분리 → desk reject 가능성 | 모든 venue |

**Cross-cutting reject reason** (4+ reviewers): **"Method은 야심차나 single-case retrospective + simulated panel + small N의 결합이 학술지 reviewer pool에서 즉시 reject 또는 major revision 사유"**.

---

## 6. Required Revisions Priority Matrix

### 🔴 P0 — must fix before any submission (4+ reviewers 또는 D2/D5 직접 원인)

| # | Revision item | 지지 reviewers | Effort |
|---|--------------|----------------|---------|
| 1 | Abstract와 §1에서 "to our knowledge first within climate negotiation domain", "novel single-case quantification" 등 first-claim 표현 모두 약화 또는 제거 + Bayer-Urpelainen 2014, Hochstetler-Milkoreit 2014 인용 추가 | R2, R4, R7, R10 | low (1일) |
| 2 | P@3=R@3=1.00 (N=3) 결과에 random chance baseline (binomial 또는 hypergeometric)과의 비교 + p-value 명시. Abstract에서 강조 약화 | R6, R8, R10 | low (반나절) |
| 3 | Bayesian σ_regime vs Leiden modularity 충돌의 modeling assumption disentangle 단락 (§4.2 확장) | R2, R7, R10 | medium (2일) |
| 4 | NATO 4축 LLM zero-shot vs supervised dictionary baseline 정량 비교 (precision/recall/F1) 또는 명시적 limitation으로 처리 | R4, R6 | medium (3-5일, 데이터 필요) |
| 5 | UNFCCC 공식 GGA 7-target ↔ 본 보고 6 이슈 mapping table 추가 | R1, R10 | low (1일) |
| 6 | 한국 NAP / MOFA 보도자료 1차 자료 직접 인용 (제목, 일자, 핵심 문장) | R3, R9 | low (반나절) |
| 7 | 외교부 권고 5가지 중 P3 (자발적 5–10백만 달러 약정)을 "검토를 시작할 것" 수준으로 약화 + 예산 절차 명시 | R3 | low (반나절) |

### 🟡 P1 — should fix before workshop submission (2-3 reviewers)

| # | Revision item | Reviewers | Effort |
|---|--------------|-----------|---------|
| 1 | R-GAT chair attention emergent claim의 multi-task ablation: stance-only / coalition-only / contested-only 학습 시 attention 분포 비교 | R7, R6 | medium (3일) |
| 2 | Cross-LLM α "shared-model bias 분리" → "per-LLM systematic offset 보정"으로 약화 + 5종 모두 transformer + RLHF임을 abstract에 disclose | R6 | low (반나절) |
| 3 | Spearman ρ=0.658의 동분야 SOTA (Burnham 2024 *Political Analysis*) 비교 표 추가 | R6 | low (1일) |
| 4 | n=13 노드 Leiden modularity 0.31의 random graph permutation test (1000 회) 추가, p-value 보고 | R7 | low (1일) |
| 5 | 영-한 코드 스위칭 정비: "regime complex" → "체제 복합", "norm entrepreneur" → "규범 기업가" 등 일관 표기 | R3, R9 | medium (3일) |
| 6 | CAUSAL_IDENTIFICATION_STRATEGY.md를 paper.md "future work" §7로 이전 또는 별도 strategy paper로 분리 | R8 | low (반나절) |
| 7 | Capano-Howlett-Pritoni 2025 NATO text-analysis review를 본 연구의 비교 baseline으로 직접 활용 | R4 | medium (2일) |
| 8 | 지도교수 acknowledgement 명시 (paper.md, README, CITATION.cff) | R9, R10 | trivial (10분) |
| 9 | 한국어 별도 KCI 단저자 논문 작성 시작 (paper.md를 KCI 양식으로 번역 + 한국 정책 강조) | R9, R10 | high (4-6주) |

### 🟢 P2 — nice to have

| # | Revision item | Reviewer | Effort |
|---|--------------|----------|---------|
| 1 | tests/ 폴더 + 5개 unit test (cross_llm, bayesian, rgat smoke, llm smoke, viz) | R5 | medium (1주) |
| 2 | pyproject.toml + pinned lockfile | R5 | low (1일) |
| 3 | GitHub Actions workflow 실제 설치 + 첫 CI run 통과 | R5 | low (1일) |
| 4 | run_all.py subprocess → 직접 import 구조 refactoring | R5 | medium (3일) |
| 5 | Pyg (PyTorch Geometric) standard library로 R-GAT 마이그레이션 | R7 | medium (1주) |
| 6 | OSF 실제 등록 (현재 GitHub만) | R8 | trivial (1일) |

---

## 7. Venue Recommendation 분포 (10 reviewers)

| Venue | 추천 reviewer 수 | 평균 평가 가능성 |
|-------|-----------------|----------------|
| **NeurIPS CCAI 2026 Workshop** | **6/10** ⭐ | 75% |
| 한국정책학회보 / 환경정책 (KCI) | **4/10** ⭐ | 50-60% (별도 한국어 논문 + 공동저자 후) |
| arXiv preprint | **3/10** ⭐ | always available, recommended first step |
| Workshop (Policy Sciences / ISA / ASA) | **3/10** | mid (분과별 workshop) |
| KEI 정책 보고서 | **1/10** | (외교부 실무자 권장) |
| GitHub release + Zenodo DOI | **1/10** | (SE 권장) |
| Q1 top-tier (GEC / Nature CC) | **0/10** | desk reject likely |
| Q2 mid-tier (Climate Policy / GEP / Policy Sciences) | **0/10** | 본 투고 무리 (P0 후) |
| Reject 단독 | **0/10** | — |

**Consensus venue**: **NeurIPS CCAI 2026 Workshop short paper (1st priority) + 한국정책학회보 KCI 별도 한국어 논문 (2nd priority) + arXiv preprint (always)** 의 3-track 병행.

---

## 8. 최종 권고 — 다음 단계 로드맵

### Path A — P0 항목 우선 수정 (약 1-2주)
- 위 P0 7개 항목 paper.md에 반영
- README, ALL_OUTPUTS_INDEX, ministerial_briefing 일관성 업데이트
- 지도교수 acknowledgement 즉시 추가

### Path B — arXiv preprint (P0 완료 후 1주)
- 4-page workshop format으로 paper.md 압축 + arXiv 업로드
- arXiv ID 발급 후 모든 GitHub 인용 업데이트
- Zenodo 연동으로 영구 DOI 발급

### Path C — NeurIPS CCAI 2026 Workshop short paper (deadline ~7월)
- arXiv 버전을 4-page short paper로 축약
- multi-axis extraction + R-GAT emergent attention 핵심
- Submission readiness: 75%

### Path D — 한국정책학회보 별도 한국어 단저자 논문 (2-3개월)
- 한국 적응정책 IRR 정량 평가 도구 + L&D-OP 약점 + COP31 권고 중심
- 지도교수 공동저자 (한국 학회 관례 + R10 편집위원 권고)
- KCI 양식 (국문 abstract 800자, 키워드, 참고문헌 형식)
- Submission readiness: 50-60%

### Path E — Future (6-12개월): longitudinal extension + real expert validation 후 Q2 학술지
- COP21-COP30 시계열 데이터 확보 + DiD 실제 추정 (R8 권고)
- 외부 expert 5인 패널 실제 코딩 + Krippendorff α 측정 (R1/R3/R10 권고)
- R-GAT multi-task confounding ablation (R7 권고)
- Climate Policy 또는 Global Environmental Politics 본 투고

---

## 9. Honest disclosure (mandatory)

본 synthesis는 **LLM 페르소나 시뮬레이션 기반 simulated peer review**의 결과이며, 실제 외부 학자 reviewer 섭외와 동등한 효력을 가지지 않는다. 본 결과는 (a) 자체 약점 발굴 도구, (b) 실제 reviewer 거절 사유 사전 시뮬레이션, (c) 실제 외부 reviewer 섭외 시 baseline으로만 활용된다. CRITICAL_REVIEW.md §3.2의 simulated panel 한계 진술이 본 synthesis에도 동등하게 적용된다.

향후 KEI / KAIST / MOFA / GEP 편집위원 등 실제 외부 학자에게 동일한 rubric을 보내 비교 검증할 것을 권고한다. 본 simulated synthesis의 가치는 **실제 reviewer가 잡을 가능성이 높은 reject 사유를 사전에 30가지 이상 식별**한 점에 있다.

---

## 10. Aggregated open questions for the author (10 reviewers 종합)

1. **R1**: UNFCCC 공식 GGA 7-target과 본 보고 6 이슈는 어떻게 매핑되는가?
2. **R2**: Bayer-Urpelainen 2014가 양면게임 정량화의 선행 연구로서 본 연구와 어떻게 차별화되는가?
3. **R3**: 외교부 권고 3 ($5-10M pledge)의 예산 절차상 실현 가능성은 어떻게 가정하는가?
4. **R4**: NATO 4축 LLM zero-shot 추출이 dictionary baseline 대비 어떤 정량적 우위를 갖는가?
5. **R5**: tests/ 폴더가 부재한 이유는? Master orchestrator subprocess hang의 reproducer minimal example을 issue로 등록할 수 있는가?
6. **R6**: 5종 LLM 모두 transformer + RLHF임을 인정한 상태에서 "shared-model bias 분리"는 어떻게 측정학적으로 정당화되는가?
7. **R7**: Leiden modularity 0.31의 random graph permutation p-value는 측정한 적 있는가?
8. **R8**: P@3=R@3=1.00의 random chance baseline은 무엇으로 정의하는가? Binomial vs hypergeometric?
9. **R9**: 한국정책학회보 투고를 위한 한국어 별도 논문 작성 계획이 있는가? 지도교수 공동저자 권고에 대한 입장은?
10. **R10**: arXiv preprint + NeurIPS CCAI Workshop + 한국 KCI 3-track 병행이 single-author 작업 분량으로 현실적인가?

---

## 11. 종합 진단 (Editor 시점 1-paragraph)

> CINA는 학생 single-author 프로젝트로서는 매우 우수한 reproducibility (D5 = 3.95) 와 정직성 (D4 = 4.05)을 보이는 야심찬 학제간 시도이다. 그러나 (i) 5-10개로 분산된 novelty argument의 sharpening 부족, (ii) N=3 / n=78 / n=13 의 small sample 위에 세워진 실증적 주장의 over-reach, (iii) 외부 expert validation의 부재, (iv) Bayesian-Leiden 결과 충돌의 미해결, (v) 단저자 학생 + 지도교수 미공동저자라는 학회 관례 위반이 결합되어, **현 형태로 어떤 분과 venue 본 투고도 desk reject 가능성이 매우 높다**. 그러나 P0 7가지 수정 후 (예상 1-2주) **arXiv preprint + NeurIPS CCAI 2026 Workshop short paper + 한국정책학회보 별도 한국어 단저자 논문 (지도교수 공동)**의 3-track 병행은 **75% 이상 가능성**으로 평가된다. 6-12개월 후 longitudinal extension + real expert validation이 완료되면 Climate Policy 또는 Global Environmental Politics Q2 본 투고도 가능하다.

---

*Synthesized by `scripts/run_peer_review.py --synthesize` + manual narrative analysis*
*Reviewer signature*: 10 simulated personas × structured rubric + adversarial mode
*Honesty disclosure*: This is simulated peer review (LLM personas), not externally-recruited expert review. See CRITICAL_REVIEW.md §3.2 for limitations.
*Author response*: pending (recommended action: address P0 items first, then submit author response document for second-round simulated review)
