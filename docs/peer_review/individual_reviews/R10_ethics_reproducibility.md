# R10 — Research Ethics / Reproducibility Reviewer 슬롯

```yaml
reviewer_id: R10
reviewer_field: Research Ethics / Computational Reproducibility / Honest Reporting
reviewer_proxy_affiliation: 가상 — *Computational Communication Research* / FORRT (Framework for Open and Reproducible Research Training)
review_date: <to be filled>
status: ⬜ EMPTY
```

## 책임 영역

- 데이터 license 추적 (manifest.jsonl SHA-256 sha256 hash chain)
- LLM provider 사용의 윤리 (개인정보 처리, 비용 disclosure)
- 시뮬레이션 패널 vs 실제 평가의 명료한 분리
- 자체 비판 평가의 자기 일관성
- 코드 + 데이터 + 결과의 재현성 검증
- IRB / human subjects 처리 적절성

## 예상 강점

- 225-entry manifest with SHA-256 + license tracking은 computational social science 분야에서 표준 상위 수준
- LICENSE 파일 명료 (MIT for code + CC BY 4.0 for docs + per-source for raw data)
- CITATION.cff + .zenodo.json + codemeta.json 모두 갖춤. Permanent identifier 인프라 우수
- CRITICAL_REVIEW.md에서 "first quantitative measurement" → "novel"로 reframing한 점은 over-claim 회피의 명확한 증거
- Pre-registration with code freeze date는 prospective falsification의 표준
- `make smoke-offline` 같은 zero-network reproducibility test 제공

## 예상 약점

- **결정적**: Task D simulated panel의 self-evaluation bias는 abstract와 본문 §5.4에서 disclosed되지만, *결과 reporting* 단계에서는 여전히 "panel mean 4.53/5"가 prominent 위치. Honest reporting 표준에서는 시뮬레이션 결과를 *별도 섹션 또는 부록*으로 분리하고 본문 main results에는 포함하지 않는 것이 권장
- "Cross-LLM Krippendorff α = 0.933" 결과는 5개 *모두* OpenAI/Google/Anthropic/Meta/Alibaba 계열 LLM이며 모두 RLHF + transformer 아키텍처. "shared-model bias decoupling" 표현은 일부만 정확. 진정한 decoupling은 non-RLHF 모델 또는 non-transformer 모델이 필요
- LLM API 호출 비용 disclosure 부재. Gemini는 free tier이지만 5 provider × 78 pairs × k=5 = 1,950 calls의 환경 비용 (compute carbon footprint)이 보고되지 않음. Climate research paper에서 ironic
- `data/processed/`는 .gitignore되어 있어 RUN_REPORT.md의 numbers를 외부 사용자가 직접 재현하려면 raw data가 필요하지만 그것은 raw data 폴더가 비공개이므로 *전체 재현은 불가*. Sample data로는 paper 결과의 *근사* 재현만 가능. 이 한계의 명시 필요
- Simulated panel persona의 "외교부 climate negotiator" 등은 실제 외교관에게 contact했다면 informed consent 필요하지만, 시뮬레이션이므로 IRB 면제임을 명시 필요. SECURITY.md에 "no human subjects"가 있지만 paper 본문에는 부재

## 예상 점수

```yaml
A1_scientific_accuracy: 4
A2_methodological_rigor: 4
A3_theoretical_grounding: 4
A4_honesty_self_criticism: 5     # 본 분야에서 가장 우수
A5_practicality_impact: 4
A6_reproducibility: 4
A7_honest_reporting: 4            # disclosed but still featured
A8_data_ethics_IRB: 4
```

## 예상 top-3 action items

```yaml
- priority: high
  item: |
    Task D simulated panel 결과를 본문 main results에서 부록으로 이동.
    Abstract에는 "Cross-LLM α = 0.93 (real reliability bound)"만 남기고
    "simulated panel mean = 4.53/5"는 부록에서 한계와 함께만 보고.
  estimated_effort: 0.5 weeks

- priority: medium
  item: |
    LLM compute carbon footprint 추정 보고. 1,950 API calls × 평균
    토큰 = 약 X kWh ≈ Y g CO2eq. 기후 연구 paper의 환경 자기 인식
    표준 부합.
  estimated_effort: 0.3 weeks

- priority: medium
  item: |
    "Cross-LLM decoupling"의 한계 명시. 5 LLM 모두 RLHF + transformer
    이므로 진정한 architecture-decoupled measurement는 future work.
  estimated_effort: 0.3 weeks
```

## 예상 의사결정

```yaml
recommendation:
  decision: Minor Revision
  target_venue_assessment: |
    Reproducibility / honest reporting 측면에서는 GEC, Climate Policy,
    Computational Communication Research 모두 적합. 본 분야에서는
    저자가 most rigorous한 그룹에 속함.
  conditions_for_acceptance: |
    1. Simulated panel 결과를 main에서 부록으로
    2. Compute carbon footprint
    3. Cross-LLM decoupling의 architectural 한계
```

---

**Status**: ⬜ Empty template.
