# Round 5 — Policy-Sci 교수 전달 패키지

> 작성: data-refinement-analyst | 날짜: 2026-04-26 | Round 5

---

## 1. C1 비평 후속: Negative Authority 분리 결과

### 1.1 교수 원문 비평 (Round 4)
> "Brazilian L.25E의 negative Authority ('shall NOT')가 Δ 산식에 포함되어 0.269가 inflate. negative Authority 분리 후 재계산 시 Δ>0.30 가능."

### 1.2 Round 5 처리 결과

**텍스트 증거 (L.25E 원문 직접 인용)**:

Para 7:
> "the indicators **should not** create additional reporting burdens... **shall not** become a barrier and **shall not** be used under any circumstances as a condition for developing country Parties to access funding."

Para 9:
> "**shall not** create new obligations... **nor establish** global standardized methodologies or data-collection processes, **nor establish** any compliance frameworks."

**수치 결과**:

| 시나리오 | 방법 | IRR_intl | Δ | 가설 Δ≥0.30 |
|---|---|---|---|---|
| A (Round 4) | Authority 합산 | 0.445 | 0.269 | PARTIAL |
| B (Round 5) | negative 분리 (6개 재분류) | 0.410 | **0.304** | **CONFIRMED** |

**교수의 가설 CONFIRMED**: negative Authority 6개(shall_not×3, should_not×1, nor_establish×2) 재분류 시 Δ = 0.304 > 0.30.

### 1.3 이론적 해석 요청

**교수께 질문**: Δ_revised = 0.304는 Putnam (1988) win-set 이론과 Howlett (2019) instrument calibration 이론이 각각 어떻게 해석해야 하는가?

구체적으로:
- Scenario B의 "Authority_negative가 실질적으로 Nodality로 기능한다"는 주장에 동의하시는가?
- 아니면 Authority_negative는 별도의 제3 범주(예: "constraint-authority")로 분류해야 하는가?
- Δ = 0.304 vs 0.269의 차이(0.035)가 Howlett calibration 이론 관점에서 의미 있는 수준인가?

---

## 2. 2D Plot에서 Policy 시사점

### 2.1 핵심 관찰

Hedging density × Red line salience 2D 분석 결과:
- AILAC: 헤징 밀도 최고 (0.009) + 레드라인 moderate → **"고 야망 + 전략적 헤징"** 패턴
- AOSIS: 레드라인 높음 (1.5°C survival language) → 타협 공간 제한
- LDC: 헤징 moderate + L&D/적응재원 레드라인 → G77 연대 내에서 자체 입장 유지
- G77_BRA: 헤징 낮음 + 레드라인 낮음 → 의장국으로서 **중립적 절차 언어** 채택

### 2.2 교수께 확인 요청

- Plano Clima 국내 정책에서 브라질이 Organization/Authority 축 지배(67%)를 보이면서 국제 협상에서는 절차 중립(낮은 레드라인)을 유지하는 패턴: 이것이 "의장국 이중 역할(Presidency Dual Role)" 현상으로 이론화 가능한가?
- Policy-Sci 이론에서 이 현상을 설명하는 기존 프레임이 있는가?

---

## 3. Round 6 준비: 추가 분석 요청

### 3.1 Stage 1 LLM 추출 검증

현재 Stage 1 추출은 rule-based fallback만 적용됨. 교수의 의견:
- Scenario A vs B 중 어느 것을 Stage 1 stance extraction의 "ground truth" 기준으로 사용해야 하는가?
- negative Authority (shall NOT)로 표현된 브라질의 입장을 stance score로 변환할 때: -1 (반대) vs +0.5 (조건부 지지) vs 0 (중립)?

### 3.2 Plano Clima 국내 negative Authority 분석

Round 5에서는 L.25E만 재분석했음. 교수 권고: Plano Clima에서도 "나쁜 것을 하지 말라" 류의 negative authority를 분리하면 IRR_domestic이 변하는가? 이것이 Δ를 더 크게 만드는가, 작게 만드는가?

---

## 4. 산출물 목록

| 파일 | 내용 |
|---|---|
| `deliverables/IRR_Brazil_2025_v2_negAuth.md` | Δ_revised 상세 보고서 |
| `data/processed/irr_brazilian_translation_gap_v2.json` | 정량 데이터 |
| `deliverables/hedging_density_2d_data.json` | 2D plot 수치 데이터 |
| `deliverables/hedging_density_2d_plot.png` | 2D scatter plot |
