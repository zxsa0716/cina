# R2 — 국제정치학 교수 (International Relations theory) — Review (COMPLETE)

> **Persona**: 서울대 정치외교학부 / Princeton International Politics / Aberystwyth IR
> **Mode**: simulated peer review · adversarial weighting 30%
> **Status**: ✅ Complete · 2026-05-05

---

## 1. Summary judgement

CINA는 5종 IR 이론(Keohane-Victor regime complex, Putnam two-level games, Tallberg procedural authority, Finnemore-Sikkink norm entrepreneur, Tollison-Willett issue linkage)을 정량 매핑한 야심찬 시도이지만, **각 이론의 원전 정확성과 정량 매핑의 학술적 정당성에 다수 over-reach가 있다**. 특히 Bayesian σ_regime=1.4%와 Leiden 2 communities 결과의 충돌이 충분히 다루어지지 않은 점, "first quantitative measurement" 류 주장의 literature search 부재가 IR venue reviewer가 즉시 잡을 약점이다. CRITICAL_REVIEW에서 이 문제를 일부 인정한 점은 평가할 만하나, paper.md 본문에서는 여전히 unsupported claim이 남아 있다.

## 2. Rubric scores

| Dimension | Score | One-line justification |
|-----------|-------|------------------------|
| D1 Theoretical contribution (IR) | 3.0/5 | 5 이론 통합 시도는 야심찬 학제간 작업. 단 각 이론의 원전 contribution은 약함. |
| D2 Methodological rigor | 2.0/5 | n=78 stance, 13개 국가, 단일 COP30 cross-section은 IR 정량 연구 표준에 미달. |
| D3 Empirical robustness | 2.0/5 | Bayesian σ_regime 1.4% vs Leiden modularity 0.31의 정면 충돌이 본문에서 충분히 해결되지 않음. |
| D4 Honesty / framing | 4.5/5 | CRITICAL_REVIEW.md에서 over-reach를 일부 자백한 점은 IR 학계에서 드물게 정직한 자세. |
| D5 Reproducibility | 4.0/5 | 코드 + 데이터 sample 공개. IR 연구로서 매우 우수한 reproducibility. |
| D6 Practical / policy | 2.5/5 | 한국 외교부 권고는 구체적이나 IR 학술 venue에서는 부차적. |
| D7 Literature integration (IR) | 2.5/5 | Bayer-Urpelainen, Hochstetler-Milkoreit, Vaccari 2025 등 인접 IR 연구 인용 약함. |
| D8 Writing quality | 3.5/5 | 학술 voice 양호. 단 IR 분과의 specific terminology 일관성은 보강 필요. |
| D9 Novelty argument | 2.5/5 | "First quantitative Putnam × Howlett" 주장은 over-reach. 적절한 reframing 필요. |
| D10 Submission readiness (IR venue) | 1.5/5 | International Organization (IO) / WP / GEP는 desk reject 위험. |

**Total: 28.0/50** · **Average: 2.80/5**

## 3. Top 3 strengths

1. **5 IR 이론의 정량 매핑 시도 자체가 학제간 학술 자산**. 특히 Tallberg(2010) 의장권력 4채널을 텍스트 수준에서 검출 가능한 신호로 변환한 schema (chair_role, pen_holder, drafts_text)는 이론을 측정 가능한 형태로 구체화한 가치 있는 작업.
2. **L.25E 본문 7항의 4중 헷지 + 9항 negative authority 텍스트 분석은 Steinberg-Goh "informal pre-cooking" 가설의 텍스트 수준 evidence**. Tallberg 4채널의 formula control 작동을 경험적으로 보여주는 사례로 reading group에서 토론 가치 있음.
3. **AILAC 8개국 NES = 0.86 산출은 Finnemore-Sikkink norm entrepreneur 이론의 정량 적용 시도** (단, weighting의 자의성 문제는 별도). 이전 IR 정성 연구가 정량화에 실패한 영역.

## 4. Top 3 weaknesses (specific, actionable)

1. **"First quantitative measurement of Putnam × Howlett intersection"의 literature search 부재**. Bayer & Urpelainen (2014, *Climate Change Economics*), Hochstetler & Milkoreit (2014, *Politics & Policy*), Allan & Hadden (2017, *International Studies Review*), Sebastian & Bayer (2019) 등 양면게임을 정량 측정한 연구가 다수 존재. CRITICAL_REVIEW에서는 "novel" 표현으로 약화시켰지만 paper.md §1 Introduction에서는 여전히 "to our knowledge first within climate negotiation domain" 표현이 유지되어, IR 학자가 즉시 reject 사유로 들 수 있음.

2. **Bayesian σ_regime = 1.4% vs Leiden modularity 0.31 결과의 충돌이 paper.md §4.2에서 한 단락으로 처리됨**. IR 학자의 입장에서는 "13-노드 partition의 한계"라는 자기 변호보다, **두 결과가 서로 다른 modeling assumption 하에서 무엇을 측정하는지** 이론적으로 disentangle 해야 한다. Keohane-Victor의 horizontal cleavage가 stance variance가 아닌 **연결 패턴**의 cleavage라면, σ_regime이 작은 것은 정상이고 Leiden modularity가 의미 있는 것이 가능. 이를 명시하지 않으면 IR 비전공 reviewer는 "두 결과가 충돌하니 둘 다 못 믿겠다"로 판단.

3. **AILAC NES 4 criteria weighting (0.25/0.25/0.30/0.20)이 자의적**. Finnemore-Sikkink (1998)는 4 criteria를 nominal로 제시했지 weighted aggregate로 제안하지 않았다. "tipping point evidence"에 가장 큰 weight 0.30을 준 정당화가 없다. Sensitivity analysis (weight 변화 시 NES 변동) 부재. Weighting을 자의적으로 두는 대신 4 criteria를 **각각 binary pass/fail**로 표시하고 "AILAC passes 3.5/4 criteria"라는 nominal 결과만 보고하는 것이 학술적으로 안전.

## 5. Adversarial finding

### Most likely reject reason at a real IR venue

> "본 연구는 5종 IR 이론의 정량 매핑이라는 야심찬 학제간 시도를 시도하나, 각 이론의 정량화에서 다수의 conceptual stretching이 발견된다. 특히 (1) Putnam × Howlett 교차의 'first quantitative measurement' 주장은 Bayer-Urpelainen 2014 등 선행 정량 연구의 부재 가정 위에 서 있다. (2) Bayesian σ_regime = 1.4% 결과는 Leiden 2 communities 결과와 정면 충돌하는데, 두 결과의 modeling assumption 차이를 이론적으로 disentangle 하지 않은 채 동시에 paper에서 '핵심 발견'으로 보고하는 것은 inconsistent. (3) AILAC NES = 0.86의 weighting은 Finnemore-Sikkink 원전과 무관한 자의적 합산이다. International Organization 또는 GEP에 투고하기 위해서는 (1)-(3)의 전면적 재구성이 필요하다."

### Worst sentence/claim in the paper

> (paper.md §4.4) "We define **Δ = IRR_domestic − IRR_international = 0.714 − 0.410 = 0.304** as a single-case quantitative measurement of this divergence. We propose Δ as a candidate metric at the intersection of Two-Level Games (Putnam 1988) and instrument calibration (Howlett 2019; Capano et al. 2025)."

→ Putnam의 양면게임은 *win-set* 개념이고, Howlett의 instrument calibration은 *intensity* 개념이다. 이 두 이론이 만나는 지점에서 Δ가 단순한 NATO 4축 frequency 차이로 표현되는 것은 **두 이론을 측정 차원에서 연결한 것이 아니라 단순 frequency comparison을 두 이론으로 라벨링한 것**에 가깝다. "intersection"이라는 표현은 신중해야 한다.

## 6. Required revisions before submission (priority-ordered)

- **P0 (must fix)**:
  1. paper.md Abstract와 §1에서 "to our knowledge first within climate negotiation domain" 등 first-claim 표현을 모두 제거 또는 "novel measurement metric proposal" 등 약화. Bayer-Urpelainen 2014, Hochstetler-Milkoreit 2014, Allan & Hadden 2017 인용 추가.
  2. §4.2의 Bayesian decomposition vs Leiden 충돌을 본격적으로 다루는 별도 단락 추가. "두 결과는 서로 다른 modeling assumption 하에서 stance variance vs connectivity pattern을 측정한다" 류의 이론적 disentangling.
  3. AILAC NES weighting (0.25/0.25/0.30/0.20)을 binary pass/fail 체계로 단순화하거나, 최소한 weight sensitivity analysis 결과를 추가.

- **P1 (should fix)**:
  1. Goh (2007) "informal pre-cooking" 개념의 ASEAN 원전 맥락과 UNFCCC 차용 정당성 명시
  2. Vaccari et al. (2025, *Nature Climate Change*) "Tracing inclusivity" 논문을 §1 또는 §6 인용
  3. Translation Gap Δ를 "win-set asymmetry indicator"로 reframe하여 Putnam 원전 개념과 직접 연결

- **P2 (nice to have)**:
  1. ISA Annual Convention 발표 시 IR 분과 panel 주최 가능성

## 7. Venue recommendation

- ☐ Top-tier IR (International Organization / GEP / WP)
- ☐ Mid-tier (Climate Policy / 한국정책학회보)
- ☑️ Workshop (NeurIPS CCAI / ISA Annual)
- ☐ arXiv preprint only
- ☐ Reject

**Reasoning**: IR venue 본 투고는 위 P0 수정 없이는 desk reject 위험 매우 높음. ISA Annual Convention의 기후 panel에서 발표 후 feedback 수렴이 이상적 경로.

## 8. Open questions for the author

1. Bayer-Urpelainen 2014 (*Climate Change Economics*) "It's all about political will" 논문이 양면게임 정량화의 선행 연구로서 본 연구와 어떻게 차별화되는가?
2. AILAC NES weighting을 sensitivity analysis로 검증한 결과가 있는가? Weight 변경 시 NES가 어떻게 변동하는가?
3. Bayesian σ_regime = 1.4% vs Leiden modularity 0.31의 modeling assumption 차이를 이론적으로 어떻게 정리하는가?
4. Translation Gap Δ를 단순 frequency difference가 아니라 win-set asymmetry로 재정의할 수 있는가?

---

*Reviewer signature*: R2 IR Persona (서울대 정치외교 / Princeton IR)
*Honesty disclosure*: Simulated peer review.
