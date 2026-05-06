# 📋 CINA Pre-Submission Peer Review Protocol (10-Reviewer Session)

> **Purpose**: 논문 투고 *이전*에, CINA 프로젝트의 GitHub 저장소·연구 방식·결과물·중간 산출물·전 과정을 10개 분과 학자 시점에서 다각 검토함으로써 약점을 사전에 발굴하고 실제 외부 reviewer 섭외의 baseline을 마련한다.
>
> **저자 (Subject)**: Heedo Choi (최희도) · Kookmin University, Department of Climate Technology Convergence
> **Session designed**: 2026-05-05
> **Format**: 10 simulated reviewers × structured rubric + adversarial mode + synthesis

---

## ⚠️ Critical disclosure (must remain in any downstream report)

본 세션은 **LLM 페르소나 시뮬레이션을 통한 simulated peer review**이며, 실제 외부 학자 섭외 review와 동등한 효력을 가지지 않는다. 평가 결과는 (a) 자체 약점 발굴 도구, (b) 실제 reviewer가 잡을 가능성이 높은 이슈의 사전 식별, (c) 향후 실제 외부 reviewer 섭외 시의 baseline으로만 사용된다. CRITICAL_REVIEW.md §3.2의 simulated panel 한계 진술이 본 세션에도 동등하게 적용된다.

---

## 1. Session 목표

| # | 목표 | 측정 가능 산출물 |
|---|------|--------------|
| G1 | 10개 분과별 약점 발굴 | 10개 review 보고서 (각 1-2 페이지) |
| G2 | 실제 reviewer 거절 사유 사전 시뮬레이션 | "Likely reject reasons" 통합 목록 |
| G3 | 투고 전 필수 수정 사항의 우선순위화 | Synthesis priority matrix |
| G4 | 분과별 적합 venue 매칭 | Per-reviewer venue recommendation |
| G5 | 다학제 일치도(inter-reviewer agreement) 측정 | Krippendorff α across 10 reviewers |

---

## 2. 10 Reviewer 페르소나 (분과별)

각 페르소나는 (a) 분과 정체성, (b) 핵심 evaluation lens, (c) 우선 검토 자료, (d) 평가에 영향을 주는 학술 기준의 4가지로 정의된다.

### R1. 기후학 교수 (Climate Science / IPCC track)
- **Lens**: COP30 결정문 해석의 기후과학적 정확도, IPCC AR6 정합성, 적응 의제(GGA) 기술적 정확도
- **Reading list**: paper.md §4 / ministerial_briefing_ko / IRR_Korea / IRR_Brazil / agenda_matrix / 02_사전분석/사전분석 PDF
- **Standards**: IPCC AR6 WGII Ch.16-18, Adaptation Gap Report, Belém Adaptation Indicators 공식 텍스트
- **Reject sensitivity**: 적응 ≠ 완화 혼동, GGA 7개 주제별 목표 범주화 오류, 한국 적응대책 사실관계 오류
- **Affiliation persona**: KAIST 환경공학 교수 / 국립기상과학원 / IPCC AR7 lead author

### R2. 국제정치학 교수 (International Relations theory)
- **Lens**: Regime complex theory, hegemony, alliance dynamics, 양면게임의 학술적 엄밀성
- **Reading list**: paper.md §2-4 / docs/research/CRITICAL_REVIEW / Translation Gap Δ 도출 과정 / Leiden 결과 해석
- **Standards**: Keohane-Victor 2011, Putnam 1988, Tallberg 2010, Finnemore-Sikkink 1998 원전 정확성
- **Reject sensitivity**: Putnam × Howlett 교차 “first quantitative measurement” 과대주장, regime complex의 horizontal cleavage를 단일 13-노드 graph로 입증한다는 over-reach
- **Affiliation persona**: 서울대 정치외교학부 / Princeton International Politics / Aberystwyth IR

### R3. 외교 실무자 (Practitioner — MOFA / 협상 실무)
- **Lens**: 권고의 실행 가능성, 협상 현장 정합성, 한국 외교부 매너
- **Reading list**: 01_AgentAI를 활용한 장관급브리핑.docx / SUBMISSION_GUIDE / 99_링크
- **Standards**: 외교부 공식 보고서 양식, 실제 COP 협상관 시점, EIG/AILAC 그룹 동학
- **Reject sensitivity**: "자발적 5–10백만 달러 약정"의 정치적 실현성 미검증, "EIG 위치 재배치" 주장의 외교적 비현실성, 한국 NAP pen-holder 주장의 사실 확인 가능성
- **Affiliation persona**: 외교부 기후변화환경외교국 전직 협상관 / KEI 정책연구원

### R4. 정책학 교수 (Policy Science — Howlett school)
- **Lens**: NATO 4축 정책수단 calibration의 이론적 정확성, instrument mix 분석
- **Reading list**: docs/04_stage1_stance_extraction / docs/14_schema_v1_3_changes / korean_nap_gga_crosswalk.csv / 02_IRR_Brazil / 03_AILAC
- **Standards**: Hood 1983, Howlett 2019, Capano-Howlett-Pritoni 2020/2025, instrument calibration 메타이론
- **Reject sensitivity**: NATO 축의 LLM 자동 추출이 supervised dictionary 방식 대비 어떤 정량적 우위를 갖는지 미입증, "first calibration measurement" 주장의 literature search 부재 가능성
- **Affiliation persona**: 서울대 행정대학원 / Simon Fraser School of Public Policy / Carleton SPPA

### R5. 소프트웨어 공학 / DevOps 교수
- **Lens**: 코드 품질, 재현성, CI/CD, 모듈성, 의존성 관리, 보안
- **Reading list**: src/run_all.py / src/stage1_extract/llm_smoke_test.py / src/stage2_graph/rgat.py / Makefile / Dockerfile / .github/workflows/ / requirements.txt / pytest 커버리지
- **Standards**: PEP 8, type hint coverage, test coverage ≥ 80%, 재현 가능 환경 (Docker/poetry/lockfile)
- **Reject sensitivity**: pytest 실제 테스트 부재, type hint 일관성 결여, requirements.txt 비-pinned, master orchestrator subprocess 구조의 fragility (이전 세션에서 hang 관찰)
- **Affiliation persona**: Google ML Engineer / KAIST 전산학부 / Apache 프로젝트 maintainer

### R6. 머신러닝 / NLP 교수 (LLM evaluation)
- **Lens**: LLM 기반 측정의 validity, prompt engineering, calibration, hallucination 통제
- **Reading list**: src/stage1_extract/extract_v2.py / src/stage1_extract/cross_llm_consistency.py / docs/04_stage1_stance_extraction / Phase 5 evaluation_report
- **Standards**: 최근 LLM stance detection 벤치마크 (Cambridge Stay Tuned 2024), Krippendorff α 적정 레벨, LLM-as-judge bias literature
- **Reject sensitivity**: Cross-LLM α = 0.93의 "shared-model bias 분리" 주장 — 5개 모델이 같은 RLHF 패러다임을 공유하므로 진정한 분리 아님. Multi-sample k=5의 통계적 의미 미정당화. Beta-binomial CI의 사전 분포 정당화 부재.
- **Affiliation persona**: Stanford NLP / KAIST AI 대학원 / Allen AI

### R7. 그래프 / 네트워크 모델링 교수 (GNN / Network Science)
- **Lens**: Leiden, R-GAT 아키텍처, attention 해석, modularity 의미
- **Reading list**: src/stage2_graph/rgat.py / src/stage2_graph/advanced_analysis.py / fig5_similarity_network / fig8_rgat_training / Bayesian decomposition
- **Standards**: Schlichtkrull 2018 R-GCN, Veličković 2018 GAT, Traag-Waltman-van Eck 2019 Leiden, recent attention interpretability literature
- **Reject sensitivity**: n=13 노드의 Leiden modularity 0.31이 통계적으로 유의미한가? (random graph 대비 permutation test 부재). R-GAT chair attention 1.00이 “emergent recovery”라는 주장은 multi-task loss와 chair-edge 자체의 데이터 양 imbalance를 통제하지 않은 over-interpretation. Bayesian σ_regime = 1.4%가 Leiden cleavage와 정면 충돌하는 점을 paper에서 충분히 다루지 않음.
- **Affiliation persona**: ETH Zürich Network Lab / 서울대 산업공학과 GNN 그룹

### R8. 계량 사회과학 / 통계 교수 (Causal inference / preregistration)
- **Lens**: 인과 식별 전략의 엄밀성, sample size justification, pre-registration 표준 부합도
- **Reading list**: docs/research/CAUSAL_IDENTIFICATION_STRATEGY / docs/research/PREREGISTRATION_COP31 / paper.md §5 / src/analysis/bayesian_hierarchical.py
- **Standards**: Imbens-Rubin causal inference, OSF preregistration template, Abadie synthetic control 2010, sample size power analysis
- **Reject sensitivity**: P@3 = R@3 = 1.00 (N=3) — power 분석이 사실상 불가능한 N. parallel-trends test가 명시되지 않은 DiD 설계. IV exclusion restriction의 정당화 부재. Bonferroni α = 0.0125가 4-가설 multiple testing에 충분한지 미입증.
- **Affiliation persona**: MIT Economics / Harvard Statistics / 연세대 응용통계

### R9. 한국 정책 / KCI 학자 (한국정책학회보 시점)
- **Lens**: 한국 적응정책의 사실관계, 한국어 학술 글쓰기 표준, KCI 게재 가능성
- **Reading list**: ministerial_briefing_ko / 01_AgentAI를 활용한 장관급브리핑.docx / IRR_Korea / SUBMISSION_GUIDE
- **Standards**: 한국정책학회보 투고 양식, 한국 NAP 제3차 (2023-2027) 사실관계, MOFA 보도자료 인용 정확도
- **Reject sensitivity**: 영-한 코드 스위칭이 한국 학술지 reviewer에게는 거슬릴 수 있음 ("regime complex", "norm entrepreneur" 등 한국어 학계 정착 용어로 일관 표기 필요). 한국 NAP 펜홀더 주장의 1차 자료(외교부 보도자료) 사실 확인.
- **Affiliation persona**: 한국정책학회보 편집위원 / 환경부 정책관

### R10. 학술 출판 편집위원 (Editor — venue fit)
- **Lens**: 전체 publishability, 적합 venue 매칭, novelty argument의 설득력, 분량/구조
- **Reading list**: README + paper.md 전체 + CRITICAL_REVIEW + METHODOLOGY_ADVANCEMENT_ROADMAP + RUN_REPORT
- **Standards**: Global Environmental Change / Climate Policy / NeurIPS CCAI Workshop / 한국정책학회보 가이드라인
- **Reject sensitivity**: GEC IF 11.2 투고는 현 단계에서 "premature" 평가 가능성. NeurIPS CCAI Workshop poster 단계가 적절. arXiv preprint 우선 권고. Single-case retrospective + simulated panel은 Q1 venue에서는 약점.
- **Affiliation persona**: GEP Senior Editor / Climate Policy Associate Editor / NeurIPS CCAI Workshop chair

---

## 3. 평가 Rubric (10 차원, 0-5 척도)

각 reviewer는 다음 10차원에서 0-5점을 매기고 short justification을 작성한다.

| # | 차원 | 정의 | 0점 의미 | 5점 의미 |
|---|------|------|---------|---------|
| D1 | **Theoretical contribution** | 본 분과 이론에 대한 기여 | 기여 없음 | 분과 주요 학술지 게재 가능 수준 |
| D2 | **Methodological rigor** | 방법론의 학술적 정확성 | 심각한 결함 | 방법론 자체가 contribution이 됨 |
| D3 | **Empirical robustness** | 결과의 통계적·실증적 견고성 | 통계 오류 | 다중 robustness check 모두 통과 |
| D4 | **Honesty / framing** | 한계 인정·과대주장 회피 | 만연한 over-claim | 모든 한계 정직히 명시 |
| D5 | **Reproducibility / openness** | 재현 가능성·자료 공개 | 재현 불가능 | 1-command 완전 재현 |
| D6 | **Practical / policy impact** | 실무 활용성 | 학술 자위 수준 | 외교부/현장 즉시 활용 가능 |
| D7 | **Literature integration** | 선행 연구 검토와 위치 | 주요 선행 누락 | 분야 동향 정확히 매핑 |
| D8 | **Writing quality** | 논증 구조·언어 명료성 | 가독성 낮음 | 학술지 수준 |
| D9 | **Novelty argument** | 기여 sharpening | 기여 모호 | 명확한 1-2개 기여 |
| D10 | **Submission readiness** | 현 상태 그대로 투고 가능성 | major revision | accept-ready |

**서술형 항목** (각 reviewer 필수):
- **Top 3 strengths**
- **Top 3 weaknesses (specific, actionable)**
- **Likely reject reason** (실제 reviewer가 reject 추천할 가장 가능성 높은 이유 1개)
- **Required revisions before submission** (priority-ordered)
- **Recommended venue**: Accept / Workshop / Domestic KCI / arXiv preprint only / Reject

---

## 4. Session 운영 방식

### 4.1 Phase A — 자료 준비 (이미 완료)
모든 reviewer가 access 가능한 자료는 GitHub repo의 다음과 같다:
- README, ALL_OUTPUTS_INDEX, CHANGELOG
- deliverables/paper.md (메인 검토 대상)
- deliverables/ministerial_briefing_ko.md / _en.md
- deliverables/{IRR_Korea, IRR_Brazil, AILAC_norm_entrepreneur, evaluation_report, L25_formula_control_evidence, realist_b0_statistics}.md
- docs/research/{CRITICAL_REVIEW, METHODOLOGY_ADVANCEMENT_ROADMAP, PREREGISTRATION_COP31, CAUSAL_IDENTIFICATION_STRATEGY}.md
- docs/01-15_*.md (방법론 문서)
- docs/web/figures/fig{1..10}*.png
- src/ (전 코드)
- RUN_REPORT.md (최신 실행 결과)
- data/sample/* (sanitized 데이터)

### 4.2 Phase B — 개별 review 실행

각 reviewer는 다음 4단계를 따른다:

1. **자료 1차 통독** — 자기 분과 reading list (15-30분)
2. **Rubric 채점** — 10차원 × 0-5 (5분)
3. **서술형 작성** — Strengths/Weaknesses/Reject reason/Revisions/Venue (15분)
4. **Adversarial 라운드** — "이 논문이 reviewer 2 모드에서 거절될 시나리오 1개를 가장 그럴듯하게 작성하라" (5분)

총 review당 약 45-60분 소요.

### 4.3 Phase C — Synthesis

**Per-reviewer 출력**: `docs/peer_review/R{1-10}_{discipline}_review.md`

**Aggregate 출력**: `docs/peer_review/SYNTHESIS.md`
- 평균 점수 매트릭스 (10 reviewers × 10 dimensions)
- Krippendorff α (10 reviewers 간 일치도) — 0.7 이상 = 관찰 신뢰
- 각 차원별 가장 낮은 점수 + 그 reviewer의 정당화
- "Likely reject reasons" 통합 목록 (중복 제거 후 빈도순)
- "Required revisions" priority matrix (P0 / P1 / P2)
- Venue recommendation 분포

### 4.4 Phase D — Decision gate

다음 임계치를 모두 통과해야 paper 투고 진행:

- 평균 D2 (방법론 엄밀성) ≥ 3.5
- 평균 D4 (정직성/framing) ≥ 4.0
- 평균 D5 (재현성) ≥ 4.0
- "Major reject" venue 추천 reviewer ≤ 2명
- Krippendorff α ≥ 0.5 (분과별 합리적 disagreement는 허용)

임계치 미달 시 priority matrix의 P0 항목 수정 후 재검토.

---

## 5. Adversarial Mode 가이드

각 reviewer는 다음 두 sub-mode 사이를 오간다.

### 5.1 Constructive mode (전체 review의 70%)
- 강점 진단
- 일반적 improvement 제안
- Venue fit 평가

### 5.2 Adversarial mode (전체 review의 30%)
- "이 논문에서 가장 weak한 1문장을 찾아라"
- "선행 연구가 이미 한 일을 'novel'이라 주장하지 않았는지 확인하라"
- "n=78, N=3 등 small sample 결과를 generalisable claim으로 over-reach 하지 않았는지 확인하라"
- "경쟁 도구(NegotiateCOP, Castro 2025, RICE-N)의 강점을 부당하게 축소하지 않았는지 확인하라"
- "Simulated panel 결과를 실제 expert panel과 동등하게 표시하지 않았는지 확인하라"

Adversarial 발견은 weight 1.5로 가중되어 priority matrix에 반영된다.

---

## 6. 출력 양식 (per-reviewer template)

각 reviewer는 다음 8개 섹션의 markdown 보고서를 작성한다:

```markdown
# Review by R{N} — {Discipline}

> **Reviewer**: {Persona affiliation}
> **Date**: 2026-MM-DD
> **Mode**: simulated peer review (LLM persona)
> **Reading time**: {hours}

## 1. Summary judgement
{1-3 sentences on overall assessment}

## 2. Rubric scores
| Dimension | Score | One-line justification |
|-----------|-------|------------------------|
| D1 Theoretical contribution | X/5 | ... |
| D2 Methodological rigor     | X/5 | ... |
| D3 Empirical robustness     | X/5 | ... |
| D4 Honesty / framing        | X/5 | ... |
| D5 Reproducibility          | X/5 | ... |
| D6 Practical / policy       | X/5 | ... |
| D7 Literature integration   | X/5 | ... |
| D8 Writing quality          | X/5 | ... |
| D9 Novelty argument         | X/5 | ... |
| D10 Submission readiness    | X/5 | ... |

**Total**: X/50 · **Average**: X.X/5

## 3. Top 3 strengths
1. ...
2. ...
3. ...

## 4. Top 3 weaknesses (specific, actionable)
1. ...
2. ...
3. ...

## 5. Adversarial finding
**Most likely reject reason at a real venue**:
...

**Specific worst sentence/claim in the paper**:
...

## 6. Required revisions before submission (priority-ordered)
- **P0 (must fix)**: ...
- **P1 (should fix)**: ...
- **P2 (nice to have)**: ...

## 7. Venue recommendation
☐ Accept at top-tier (GEC / Nature / NeurIPS proceedings)
☐ Accept at workshop / domestic (NeurIPS CCAI / 한국정책학회보)
☐ arXiv preprint only — not yet ready for venue
☐ Major revision required before any submission
☐ Reject

**Reasoning**: ...

## 8. Open questions / things I'd ask the author
1. ...
2. ...
3. ...

---
*Reviewer signature*: {persona}
*Honesty disclosure*: This is a simulated peer review by an LLM-instantiated persona, not an externally-recruited expert.
```

---

## 7. Aggregation 자동화 (synthesis 단계)

10개 review가 모두 작성된 후, `docs/peer_review/SYNTHESIS.md`에 다음을 자동 산출:

1. **점수 행렬**: 10 × 10 표
2. **Krippendorff α**: 10 reviewer 간 일치도 (R 또는 Python 산출)
3. **분과별 평균 vs 표준편차**: 어떤 차원에서 reviewer 간 큰 disagreement가 있는지
4. **Top 5 가장 자주 언급된 weakness**: 최소 3명 이상 reviewer가 지적한 항목
5. **Priority matrix**:
   - **P0** (≥ 4 reviewers + adversarial weight): 투고 전 필수
   - **P1** (≥ 2 reviewers): 강력 권고
   - **P2** (1 reviewer): 선택
6. **Venue recommendation 집계**: 각 venue별 추천 수
7. **Decision gate 결과**: 임계치 통과 여부

---

## 8. 다음 단계

본 protocol에 따라 10 reviewers를 순차 실행한다. 각 review는 별도 markdown 파일로 저장되며, 모두 완료 후 SYNTHESIS.md가 작성된다. 본 단계가 완료되면, 그 결과는:

- (a) **paper.md를 P0 사항에 따라 수정** → arXiv preprint 업로드 가능 상태
- (b) **target venue를 synthesis 결과에 따라 재선택** → 가장 적합한 venue로 투고
- (c) **실제 외부 expert reviewer 섭외 시 baseline** → 동일한 rubric을 외부 학자에게 보내 비교 가능

---

**작성**: Heedo Choi (최희도) · 2026-05-05
**관련**: docs/research/CRITICAL_REVIEW.md (이미 작성된 자체 비판 평가는 본 세션의 sibling 문서)
**다음 commit**: 10개 reviewer brief 템플릿 + synthesis 함석 추가
