---
task_id: T03-Round4
assigned_to: policy-science-professor
agent_model: opus
round: 4
priority: P0
depends_on:
  - T02 Round 4 산출물 (korean_nap_gga_crosswalk.csv, IRR_Korea_2025.json, realist_b0_eval.json, stage1_llm_trial)
  - council_sessions/round_3/policy_science/critique.md (anchor 4.08/5)
  - council_sessions/round_3/synthesis/cross_review.md (§1.2 D-R3-2 Plano Clima 분석 정점)
  - Heedo 결정 D-R4-1 (Plano Clima 챕터 분기 vs 통합)
deadline: T02 완료 후 48시간
---

# T03 Round 4 — policy-science-professor 작업 지시

## 0. 목적

Round 3에서 Policy 4.08/5 도달 (Major→Minor revision 진입). Round 4 목표 **4.20+** — Policy strategic 차원 3.5 → 4.2 (+0.7) 한 단계 도약. 결정 dimension은 **korean_nap_gga_crosswalk + IRR_Korea_2025 시범 정량화**.

## 1. 산출물 (Deliverables)

### 1.1 P0 — `korean_nap_gga_crosswalk.csv` 검증 + 한국정책학회보 단독 논문 1편 가능성 평가

**검증 대상**: T02 Round 4 §1.2 산출물 — 5×6 매트릭스 (한국 5대 영역 × GGA 6 영역, ●HIGH/◐MED/○LOW 30 셀)

**검증 기준**:
1. **셀 판정 신뢰성**: 30 셀 중 evidence_traceability 인용이 한국 적응대책 본문 또는 KEI 보고서에서 실제 추출되었는가?
2. **분류 일관성**: ●HIGH 5 / ◐MED 13 / ○LOW 12 분포가 정책학적으로 정합한가? (예: 한국 4. 보건 영역이 9d Eco ○LOW로 판정된 근거가 합리적인가)
3. **GGA 매핑 정확도**: UAE-Belém 9a-e의 실제 indicator (110건)와의 매칭 정확도

**산출물**:
- `council_sessions/round_4/policy_science/cross_walk_validation.md` (셀 30개별 1-2 문장 검증 의견 + 종합 평점)
- 평점: 5-point scale (1=reject, 5=accept-as-is)

### 1.2 P0 — IRR_Korea_2025 메트릭 정합성 평가

**검증 대상**: T02 Round 4 §1.3 — IRR_Korea_2025 ≈ 0.62-0.68

**검증 질문**:
1. **공식 정합성**: IRR = Σ[W_k × Realized_k] / Σ[W_k × Promised_k] 가 docs/07 §11 Task E 정의와 일치하는가?
2. **W_k 가중치 합리성**: cross-walk ●=1.0 / ◐=0.6 / ○=0.3 가중이 한국 적응대책 우선순위와 정합한가? (대안: KEI 정책중요도 점수)
3. **Realized 측정 단위**: 정량 0.5-1.0 / 정성 0.0-0.5 분류가 KEI 모니터링 보고서의 실제 평가 척도와 일치하는가?
4. **신뢰구간**: 0.62-0.68 범위가 통계적으로 robust한가? (bootstrap 권고)

**산출물**:
- `council_sessions/round_4/policy_science/irr_validation.md`
- 한국정책학회보 reviewer 입장에서 (i) major revision required, (ii) minor revision, (iii) accept-as-is 판정

### 1.3 P0 — 한국정책학회보 단독 논문 1편 가능성 평가

**평가 질문**:
- IRR_Korea_2025 ≈ 0.62-0.68이 한국 첫 NAP IRR 정량화 사례로서 한국정책학회보 단독 논문의 핵심 finding이 될 수 있는가?
- Track A (수업 브리핑)와 Track B (NeurIPS CCAI / GEC)에 더해 Track C (한국정책학회보 단독) 분리 추진 가치가 있는가?

**평가 dimension** (5-point scale):
1. **신규성**: KEI/KIEP가 산출하지 않은 영역인가? (Round 3 Policy critique §4 "한국 첫 NAP IRR 정량화 사례")
2. **이론 기여**: Putnam Two-Level Games × Howlett instrument translation 정식화가 한국정책학회보 학술 기여로 인정될 수준인가?
3. **데이터 충실성**: T01 Round 4 KOR MOE PDF 본문 + KEI 보고서로 N≥? 충분 evidence 확보 가능한가?
4. **정책 함의**: 한국 환경부 담당관의 GGA 59지표 우선 대응 23-25개 식별이 정책 brief로 전환 가능한가?
5. **저자 분담 가능성**: Heedo 단독 vs 공저자 (KEI 명수정 박사 + 학교 지도교수)

**산출물**:
- `council_sessions/round_4/policy_science/korea_paper_track_c_assessment.md`
- 권고: 추진 / 보류 / Round 5 재평가
- 추진 시: 핵심 thesis 1문장 + 목차 5장 + 예상 길이 + 마감 일정

### 1.4 P0 — Plano Clima 분석 docs/15 구조 결정 입력 (Heedo D-R4-1 응답)

**Heedo D-R4-1 옵션**:
- A. 분기 (`docs/15_two_level_instrument_translation.md` Policy + `docs/16_chair_brokerage_game.md` IR)
- B. 통합 (`docs/15_brazil_dual_role_analysis.md` 단일 챕터)
- C. Round 5 결정 연기

**Policy 입장 명확화**:
- 옵션 A 채택 시 Policy 챕터 (`docs/15_two_level_instrument_translation.md`) 목차 5절 초안
- 옵션 B 채택 시 Policy 분석 분량 (총 챕터의 ~50%)
- 옵션 C 채택 시 Round 5 결정 입력 데이터 (Plano Clima Vol II 분석 후)

**산출물**:
- `council_sessions/round_4/policy_science/plano_clima_chapter_input.md`
- 옵션별 deliverable structure 1-2 페이지

### 1.5 P0 — 5-Dimension Rubric 재평가 (Round 3 → Round 4)

**입력**:
- T02 Round 4 산출물 (1.1~1.9)
- T01 Round 4 산출물 (Korean MOE PDF, NSA 8+ entity, Plano Vol II)
- Stage 1 LLM trial 결과

**재평가 dimensions**:

| Dimension | R3 | R4 expected | 동인 |
|-----------|----|-------------|------|
| Theoretical | 4.2 | 4.4? | Plano Clima Vol II + Salamon (2002) tools 분류 도입? |
| Methodological | 3.8 | 4.2? | Stage 1 LLM 가동 + headline_indicator 3-way + ICR Cohen κ |
| Empirical | 4.3 | 4.5? | KOR MOE PDF + NSA 8+ entity + Plano Vol II = +N건 |
| Policy strategic | 3.5 | 4.4? | korean_nap_gga_crosswalk + IRR_Korea_2025 산출 |
| Reproducibility | 4.6 | 4.7? | cr4_compliance + Stage 1 LLM seed/temperature 기록 |

**산출물**: `council_sessions/round_4/policy_science/critique.md` 본문에 통합 (rubric_breakdown 표)

### 1.6 P1 — Round 4 결정적 비판 Top 3 (Round 5 권고)

Round 3 critique §8 5건 (D7~D11) 중 미해결 + Round 4 신규 발견을 합산하여 Round 5 P0 권고 Top 3 선정.

**산출물**: `council_sessions/round_4/policy_science/critique.md` §"Round 4 핵심 비판 Top 3" 절

## 2. 품질 기준

- [ ] 5 deliverable 모두 산출 (1.1 + 1.2 + 1.3 + 1.4 + 1.5)
- [ ] critique.md 5-Dim Rubric 재평가 (목표 4.20+)
- [ ] 한국정책학회보 Track C 추진/보류 명확 권고
- [ ] Plano Clima 챕터 옵션 A/B/C 응답
- [ ] D-R4-1 Heedo 결정 입력 명확

## 3. 제공된 컨텍스트

- `council_sessions/round_3/policy_science/critique.md` (4.08/5 anchor)
- `council_sessions/round_3/synthesis/cross_review.md` (§1.2 D-R3-2)
- `council_sessions/round_3/refinement/professor_input/policy_sci_pack_round3.md`
- `data/processed/refinement_round4_stats.json` (T02 산출 후)
- `data/processed/IRR_Korea_2025.json` (T02 §1.3 산출)
- `deliverables/korean_nap_gga_crosswalk.csv` (T02 §1.2 산출)

## 4. 보고

### 4.1 형식
`council_sessions/round_4/policy_science/critique.md` (Round 3와 동일 구조 + 1.1~1.6 통합)

### 4.2 IR 교수와의 합의·불일치 예측 (§7 절)
- D-R3-2 Plano Clima 분석 정점 — Round 4에서 어느 옵션 (분기/통합)으로 합의 가능?
- 한국정책학회보 Track C 분리 추진 — IR 교수도 동의?
- realist B0 F1 결과에 따른 Discussion 대응 (3 시나리오)

---

*— team-lead, 2026-04-26*
