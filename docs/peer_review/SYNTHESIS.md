# CINA Peer Review Synthesis (auto-generated)

> 10 / 10 reviewers complete · simulated peer review

## Score matrix

| Reviewer | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Total |
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
| **avg** | **2.35** | **2.2** | **2.1** | **4.05** | **3.95** | **2.8** | **2.5** | **3.35** | **2.7** | **2.0** | — |
| **σ** | 0.47 | 0.48 | 0.57 | 0.44 | 0.44 | 0.92 | 0.41 | 0.34 | 0.26 | 0.41 | — |

## Decision gate

- D2 ≥ 3.5: ❌ fail
- D4 ≥ 4.0: ✅ pass
- D5 ≥ 4.0: ❌ fail

**Overall**: ❌ NEEDS revision

## Aggregated weaknesses (all reviewers)

1. **GGA 7개 thematic targets와 본 보고서 6개 이슈 간 공식 mapping 부재**. UNFCCC 공식 7-target framework은 (i) water, (ii) food and agriculture, (iii) health, (iv) ecosystems and biodiversity, (v) infrastructure and human settlements, (vi) poverty eradication and livelihoods, (vii) cultural heritage이다. 본 보고의 6 이슈(GGA-IND, GGA-MOI, NAPs, JT-ADAPT, L&D-OP, FINANCE-ADAPT)는 다른 차원의 분류(meta-issue)이며, 두 분류 체계의 mapping table이 paper.md 또는 ministerial_briefing에 없다. 외교 실무에는 둘 다 필요.
2. **"적응 재원 3배 증액 2035년 1,200억 달러"의 baseline 명시 부재**. UNFCCC L.24 결정문은 명확한 baseline (2019 데이터 기준)을 제시하는데, 본 보고서는 단순히 "3배"라고만 표기. 2019 baseline 값 + 2035 target 값 + 그 사이 trajectory 명시 권장.
3. **IPCC AR6 WGII Hazard-Exposure-Vulnerability framework의 직접 적용 부재** — 저자 본인의 학문적 배경(GAT 기반 도시기후 / 기후정의·XAI)이 IPCC HEV framework와 매우 부합하는데, 본 분석에서는 적응 정책의 NATO 4축만 측정하고 climate hazard exposure 또는 vulnerability dimension은 입력으로 활용되지 않았음. ND-GAIN vulnerability index는 manifest에는 수집되었으나 분석에 들어가지 않음.
4. **"First quantitative measurement of Putnam × Howlett intersection"의 literature search 부재**. Bayer & Urpelainen (2014, *Climate Change Economics*), Hochstetler & Milkoreit (2014, *Politics & Policy*), Allan & Hadden (2017, *International Studies Review*), Sebastian & Bayer (2019) 등 양면게임을 정량 측정한 연구가 다수 존재. CRITICAL_REVIEW에서는 "novel" 표현으로 약화시켰지만 paper.md §1 Introduction에서는 여전히 "to our knowledge first within climate negotiation domain" 표현이 유지되어, IR 학자가 즉시 reject 사유로 들 수 있음.
5. **Bayesian σ_regime = 1.4% vs Leiden modularity 0.31 결과의 충돌이 paper.md §4.2에서 한 단락으로 처리됨**. IR 학자의 입장에서는 "13-노드 partition의 한계"라는 자기 변호보다, **두 결과가 서로 다른 modeling assumption 하에서 무엇을 측정하는지** 이론적으로 disentangle 해야 한다. Keohane-Victor의 horizontal cleavage가 stance variance가 아닌 **연결 패턴**의 cleavage라면, σ_regime이 작은 것은 정상이고 Leiden modularity가 의미 있는 것이 가능. 이를 명시하지 않으면 IR 비전공 reviewer는 "두 결과가 충돌하니 둘 다 못 믿겠다"로 판단.
6. **AILAC NES 4 criteria weighting (0.25/0.25/0.30/0.20)이 자의적**. Finnemore-Sikkink (1998)는 4 criteria를 nominal로 제시했지 weighted aggregate로 제안하지 않았다. "tipping point evidence"에 가장 큰 weight 0.30을 준 정당화가 없다. Sensitivity analysis (weight 변화 시 NES 변동) 부재. Weighting을 자의적으로 두는 대신 4 criteria를 **각각 binary pass/fail**로 표시하고 "AILAC passes 3.5/4 criteria"라는 nominal 결과만 보고하는 것이 학술적으로 안전.
7. **"자발적 5–10백만 달러 손실·피해 기관 지원 약정"의 예산 절차 무시**. 한국 정부 예산 편성은 (i) 환경부 또는 외교부 부처 요구 → (ii) 기획재정부 심의 → (iii) 국무회의 의결 → (iv) 국회 예산결산특별위원회 심의 → (v) 본회의 의결의 5단계를 거친다. 외교부 단독으로 "발표"할 수 있는 규모가 아니다. 또한 GCF 출연금(한국은 2021-2023 1억 5천만 달러 약정)과의 관계, 손실·피해 기금(FRLD)과의 분리 회계 처리, ODA 통계 인정 여부 등 정책 절차상 사전 검토가 필수. 권고 3은 "검토를 시작할 것" 수준으로 약화 권장.
8. **"한국이 NAP 펜홀더" 주장의 1차 자료 확인 부족**. CINA Stage 1이 추출한 `drafts_text_for_issue: NAPs` 신호의 근거 문서가 무엇인가? `appendix A`의 "MOFA 보도자료 seq=376685, 2025-12-08"은 외교부 보도자료 일련번호 형식으로 보이는데, 실제 그 보도자료를 직접 인용해야 한다 (보도자료 제목, 발표 일자, 핵심 문장). 외교부 reviewer는 본인이 작성하지 않은 보도자료를 근거로 한 외부 분석에 의문을 제기할 가능성이 높다.
9. **"EIG 위치 재배치" 표현의 외교 매너 부적합**. EIG는 협상 그룹이며, "위치"는 학술적 metaphor이다. 외교부 보고서에서는 "환경건전성그룹 내 한국 입장의 일관성 강화" 또는 "선진국·개도국 가교 정체성의 명료화" 같은 표현이 표준. "그래프적 위치를 발전 프레임 진영으로 재배치한다"는 외부 학자의 분석 언어이며, 외교부 권고로 그대로 인용하기는 어색.
10. **NATO 4축 LLM 추출의 supervised baseline 대비 정량 비교 부재**. Capano et al. (2025) NATO text-analysis review는 dictionary methods, supervised learning, topic models, scaling models 등 다양한 NATO 측정 방법론을 비교하는 메타논문이다. 본 연구는 Capano et al. 2025를 reference 추가했으나, **본인의 LLM zero-shot 방법이 dictionary baseline 대비 (a) precision/recall, (b) coding 일관성, (c) 시간/비용 면에서 어떤 정량적 우위를 갖는지** 측정하지 않았다. 정책학 reviewer는 "왜 dictionary 대신 LLM을 써야 하는가"를 직접 묻는다.
11. **Instrument calibration의 frequency vs intensity 구별 부재**. Howlett (2019) calibration은 instrument의 *intensity* (강도) 측정이고, NATO 4축의 단순 사용 여부 (binary) 또는 frequency (빈도)와 다르다. 예를 들어 Brazil의 Authority axis "shall not create new financial obligations"는 단 1회 등장하지만 그 강도는 매우 강하다. 본 연구의 Δ=0.304는 NATO 축의 frequency 차이를 측정한 것이지 calibration intensity 차이를 측정한 것이 아닐 수 있다. Howlett의 calibration 개념과 본 연구의 측정 사이에 conceptual gap이 있다.
12. **Negative authority "shall NOT" 측정 방법론 정당화 부재**. IRR_Brazil.md는 "negative authority 분리 후 Δ 재산출"이라 명시하지만, **negative authority를 어떻게 자동 검출했는지 (dictionary? LLM zero-shot? manual?)** 본문에 명시되지 않는다. 만일 LLM이 "shall not"의 negative authority를 단순 keyword matching으로 처리했다면, Δ=0.304는 단순 keyword frequency 효과일 가능성을 배제할 수 없다.
13. **`tests/` 폴더 자체가 없음 (pytest coverage 0%)**. 191개 tracked file 중 단일 unit test 파일도 없음. `requirements.txt`에 pytest는 listed되어 있으나 사용 흔적이 없다. 최소한 (a) `cross_llm_consistency` Krippendorff α 계산의 unit test, (b) `bayesian_hierarchical` variance decomposition의 numerical regression test, (c) `rgat` model forward pass smoke test는 필수. JOSS 투고는 test coverage ≥ 80% 권장하므로 desk reject 위험.
14. **`requirements.txt`가 `>=X.Y.Z` 표기 + `pyproject.toml` 없음 + lockfile 부재**. PyTorch가 다음 minor version에서 R-GAT API breaking change 시 빌드 실패. 권장: `poetry init` + `poetry.lock` 또는 `pip-tools`로 `requirements-lock.txt` 생성. 현재 `Dockerfile`도 unpinned dep로 빌드되므로 시간 지나면 같은 Dockerfile에서 다른 결과 발생 가능.
15. **`src/run_all.py` subprocess-based orchestration의 fragility**. 이전 세션에서 master pipeline이 hang한 사례가 두 차례 관찰됨 (b1z9ldp8p, by6dbm8ks 백그라운드 task). subprocess.run() + capture_output=True 구조는 stdout/stderr 버퍼 deadlock 가능성. 권장: subprocess 대신 직접 import + function call 구조로 재작성 (대부분의 step은 같은 Python process 내에서 실행 가능).
16. **"Cross-LLM α의 shared-model bias 분리" 주장의 over-reach**. 5종 LLM (Gemini 2.5 Flash-Lite, Groq Llama 3.3 70B, Anthropic Claude, Ollama Qwen 2.5, OpenRouter pool)은 모두 (a) transformer architecture, (b) RLHF / DPO / preference tuning 패러다임, (c) 영어 web text 위주의 사전 학습 corpus를 공유한다. 이들 사이의 α=0.93은 **same-paradigm agreement**이지 **shared-model bias로부터 분리된 reliability**가 아니다. 진정한 분리를 위해서는 (i) non-transformer baseline (예: BERT classifier on supervised stance dataset), (ii) human coder 1-2인의 동일 데이터 ground truth가 필요. 이 한계를 paper.md §3.2 또는 abstract에서 명시하지 않으면 NLP reviewer가 즉시 reject 사유로 삼는다.
17. **Multi-sample k=5의 통계적 정당화 부재**. 왜 k=5인가? k=3, k=10, k=20과의 marginal contribution 비교 없음. 대형 LLM API 비용 제약이라면 그 trade-off를 명시. 또한 k=5 sample이 i.i.d.인지 (temperature=0.3에서 LLM은 sampling correlation 가질 수 있음) 검증 부재. NLP 분야 표준은 k=10 이상 + bootstrap CI.
18. **Spearman ρ=0.658의 SOTA 대비 위치 미명시**. 정치 텍스트 stance detection 분야 최근 벤치마크: Cambridge "Stay Tuned" (Burnham 2024, *Political Analysis*) 등은 LLM stance detection에서 ρ=0.7-0.85 범위를 보고. 본 연구의 0.658이 동분야 어디에 위치하는지 비교 표 부재. NLP reviewer는 항상 SOTA 비교를 요구.
19. **n=13 노드 Leiden modularity 0.31의 통계적 유의성 검증 부재**. 13개 노드 그래프에서 modularity 0.31은 random graph (Erdős–Rényi 또는 configuration model)에서도 충분히 발생 가능한 수준이다. 권장: 1000회 random graph permutation 후 modularity 분포의 95th percentile과 비교. 만일 통계적으로 유의하지 않다면 "stable communities" 주장 자체가 약화된다.
20. **R-GAT chair attention 1.00의 confounding 통제 부재**. 본 setup에서 (a) `co_chairs` edge는 6개 (Brazil → 6 issues) 단일 source-from, (b) coalition label에 chair 정보가 부분적으로 포함, (c) contested label도 chair-relevant issue에 편중. Multi-task supervision이 chair edge에 의존하는 것이 자연스러운 결과일 수 있다. 권장: ablation study (i) coalition + contested supervision 제거 후 stance-only 학습 시 attention 분포, (ii) co_chairs edge type 자체 제거 후 stance prediction performance 비교, (iii) chair-edge data augmentation balance 변화 시 attention 변화.
21. **Bayesian σ_regime = 1.4% vs Leiden modularity 0.31 결과의 modeling 의미 disentangle 부재**. paper.md §4.2는 이 충돌을 "n=13 partition의 한계"로 처리하나, network science 관점에서는 (a) Leiden은 *connectivity pattern* (edge 존재 여부 + weight)을 분석하고, (b) Bayesian 3-level은 *stance variance* (node attribute의 분산)을 분해하는 별도 modeling이다. 두 결과는 서로 다른 데이터 generating process를 가정한 측정이므로 직접 비교 부적절. 이 점을 §4.2에 추가하지 않으면 GNN reviewer는 "두 결과가 충돌하니 둘 다 못 믿겠다"로 판단.
22. **P@3=R@3=1.00 (N=3)의 통계적 의미 불충분 정당화**. 6개 issue 중 3개 contested 정확 예측은 random chance (binomial test) 하에서도 C(3,3)/C(6,3) = 1/20 = 0.05 확률로 발생한다. paper.md는 "small-sample, encouraging signal"로 약화는 했지만, **N=3에서 power 분석이 사실상 불가능하다는 점, 그리고 random chance 대비 p=0.05 정도라는 점**을 명시해야 한다. 현재는 abstract에서 P@3=1.00이 강조되는데, 이는 mid-tier reviewer에게는 "왜 이렇게 약한 evidence를 abstract에 강조하는가" 의문을 제기한다.
23. **DiD parallel-trends test 명시 부재**. CAUSAL_IDENTIFICATION_STRATEGY.md는 "Pre-trend test: COP25-COP28 동안 Δ_Brazil 추세가 control 그룹과 평행한지 검증 필요"라고 언급하지만, 실제 시계열 데이터가 없어 미실행. DiD의 핵심 가정 (parallel pre-trends)이 미검증인 상태에서 hypothetical $\hat{\beta}$ 추정치를 제시하는 것은 method paper 표준에 미달. 권장: longitudinal data 확보 후 실제 parallel-trends test 결과를 paper에 포함하거나, 또는 본 strategy 문서는 paper에서 future work로 분리.
24. **Bonferroni α=0.0125의 multiple testing scope 불명확**. 4 hypothesis (H1-H4) 모두 family-wise error 통제 필요인지, 아니면 H1 (contested set continuity)만 primary endpoint이고 H2-H4는 secondary인지 명시 부재. Primary/secondary 구별이 있다면 α 분배가 다르다 (예: Hochberg, Holm-Bonferroni). 또한 H1의 |overlap| ≥ 2 임계치는 binomial 분포상 p ≈ 0.5인데 (chance가 충분히 가능), 이는 strong test가 아님.
25. **영-한 코드 스위칭의 일관성 부족**. 한국 학술지는 한국어 표기 일관성을 중시한다. 본 보고서 (ministerial_briefing_ko.md, 01_AgentAI를 활용한 장관급브리핑.docx)는 일부 영어 용어가 한국어 표기로 통합되었으나(예: "기준연도(base year)", "참조 모형(reference framework)") 다음 용어들이 여전히 영어로만 표기됨:
26. **한국 NAP 사실관계의 1차 자료 직접 인용 부족**. 한국 환경부 「제3차 국가기후변화적응대책 (2023-2027)」, 외교부 「녹색·기후외교 추진전략」, 탄소중립기본법 §47, §50 등이 본문에서 직접 인용되지만 정확한 출처 (문서명, 출간 일자, 페이지/조항)가 명시되지 않은 곳이 다수. 한국 학회 reviewer는 1차 자료 정확성에 매우 민감.
27. **KCI 투고 양식 미부합**. 한국정책학회보는 (a) 국문 초록 (800자 이내) + 영문 초록 (300단어 이내), (b) 핵심어 (국문 5개 + 영문 5개), (c) 참고문헌 한국어/영어 분리 표기, (d) 표/그림 한글 캡션, (e) 학술지명 이탤릭 등 양식 요구가 있다. 본 paper.md는 영문 abstract만 있고 한국어 표준 학술 양식이 아니다. 한국정책학회보 게재를 위해서는 별도 한국어 단저자 논문 작성 권장.
28. **Novelty argument의 분산**. 다른 reviewer들이 평가한 contribution을 종합하면: (i) Multi-axis stance extraction, (ii) Cross-LLM α framework, (iii) R-GAT chair attention emergent, (iv) Translation Gap Δ metric, (v) graph-grounded generation, (vi) pre-registration framework, (vii) causal identification strategy, (viii) Bayesian decomposition tension, (ix) AILAC NES quantification, (x) Korean IRR 도구... **너무 많다**. Editor 시점에서는 "이 paper의 1-2개 핵심 contribution이 무엇인가?"가 abstract 첫 문장에서 명확해야 한다. 여러 분과 reviewer가 각자 다른 contribution을 보는 것은 paper의 sharpening 부족 신호.
29. **단저자 학생 + 지도교수 미공동저자**. 한국 학회 관례 (R9 지적)와 동시에, 영문 학술지 reviewer도 단저자 학생 paper에 (a) 지도교수 unstated 영향 가능성, (b) thesis-from-scratch reviewing 부담을 의심한다. 최소한 acknowledgement에 advising professor 명시 권장.
30. **적합 venue가 paper voice와 분리됨**. 본 paper.md는 영문 + 학제간 + 학술 voice이고, ministerial_briefing_ko.md는 한국어 + 정책 voice이다. 단일 paper로 양 venue (영문 학술지 + 한국어 KCI) 모두 투고는 academic standards상 어렵다. 2개 별도 paper 작성 권장 (이미 구분되어 있으나, Track B 영문 paper.md도 분과별 1개로 sharpening 필요).

## Venue recommendation distribution

- NeurIPS Climate Change AI 2026 Workshop short paper: 1/10
- Workshop (NeurIPS CCAI / ISA Annual): 1/10
- KEI 정책 보고서 형식으로 발전 가능 (전면 수정 후): 1/10
- 외교부 실무자 인터뷰 후 재작성 권장: 1/10
- Workshop (Policy Sciences Conference, Carleton SPPA workshop): 1/10
- GitHub release + Zenodo DOI (가장 현실적 first step): 1/10
- NeurIPS CCAI 2026 Workshop (short paper): 1/10
- NeurIPS CCAI 2026 Workshop (climate application track): 1/10
- Workshop (NeurIPS CCAI / ASA Government Statistics): 1/10
- arXiv preprint: 1/10
- 한국정책학회보 (KCI 우수) — 한국어 별도 논문 작성 후: 1/10
- 환경정책 (KCI) — 적응정책 분야 적합: 1/10
- 정책분석평가학회보 (KCI) — 정책 평가 도구 측면 적합: 1/10
- Send to review @ Workshop (NeurIPS CCAI 2026) — **75%**: 1/10
- KCI domestic (한국정책학회보, 환경정책) — **50-60%** (별도 한국어 논문 + 공동저자 필요): 1/10
- arXiv preprint only — **always available, recommended first step**: 1/10

---

*Auto-generated by `scripts/run_peer_review.py --synthesize`. Simulated peer review — see CRITICAL_REVIEW.md §3.2 for limitations.*