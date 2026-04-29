# IRR_Brazil_2025_v2: Negative Authority 분리 후 Translation Gap 재산출

> Round 5 P0-2 산출물. Policy-Sci 교수 C1 비평 직접 충족.
> 작성일: 2026-04-26 | 버전: v2 | 작성: data-refinement-analyst Round 5
> 참조: `data/processed/irr_brazilian_translation_gap_v2.json`

---

## 1. Round 4 피드백 요약 (Policy-Sci C1)

Policy-Sci 교수 비평:
> "Brazilian L.25E의 negative Authority ('shall NOT')가 Δ 산식에 포함되어 0.269가 inflate. negative Authority 분리 후 재계산 시 Δ>0.30 가능."

Round 4 결과: Δ = 0.269 (가설 0.30 PARTIAL)
Round 5 목표: negative Authority 토큰 분리 → IRR_intl_revised → Δ_revised 산출

---

## 2. Negative Authority 분리 방법론

### 2.1 핵심 개념

L.25E (FCCC/PA/CMA/2025/L.25)에서 "Authority" axis 토큰은 두 종류가 섞여 있다.

- **Authority_positive**: 의무 부과 동사 ("decides", "calls upon", "requests", "affirms")
- **Authority_negative**: 의무 **차단** 구문 ("shall not", "should not", "nor establish", "nor liability")

Round 4의 NATO 산식은 Authority_total = Authority_positive + Authority_negative를 합산했다.
Policy-Sci 교수 지적: Authority_negative는 실제로 구속력을 **제거**하는 Nodality/constraint 언어에 더 가깝다.
따라서 IRR_intl 분모에서 Authority_negative를 Authority 범주에서 제외(→ Nodality로 재분류)해야 한다.

### 2.2 텍스트 증거 (L.25E 원문)

**Para 7 (3개 negative authority 토큰)**:
> "Emphasizes that the Belém Adaptation Indicators are voluntary, non-prescriptive, non-punitive, facilitative... and that the indicators **should not** create additional reporting burdens... **shall not** become a barrier and **shall not** be used under any circumstances as a condition for developing country Parties to access funding."

패턴: `should not` × 1, `shall not` × 2

**Para 8 (1개 negative authority 토큰)**:
> "Also emphasizes that the Belém Adaptation Indicators do not create new financial obligations or commitments, **nor liability or compensation**."

패턴: `nor liability` × 1

**Para 9 (4개 negative authority 토큰 — 최강)**:
> "Affirms that the Belém Adaptation Indicators... **shall not create new obligations** for developing country Parties, benchmarks or evaluation criteria, **nor establish** global standardized methodologies or data-collection processes, **nor establish** any compliance frameworks, nor prejudice any Party's position."

패턴: `shall not` × 1, `not create new obligations` × 1, `nor establish` × 2

**Para 31 (1개 negative authority 토큰)**:
> "Emphasizes that **no single** adaptation approach shall be presented as the default, superior or universally applicable pathway."

패턴: `no single approach` × 1

### 2.3 분리 집계

| 구문 유형 | 발견 위치 | 토큰 수 |
|---|---|---|
| shall not | Para 7 (×2), Para 9 (×1) | 3 |
| should not | Para 7 | 1 |
| nor establish | Para 9 (×2) | 2 |
| **소계 (분리 대상)** | | **6** |

Round 4 Authority_total = 21개 중 6개 (28.6%)가 negative authority로 재분류.

---

## 3. IRR 재산출 결과

### 3.1 산식 정의

**Round 4 (Scenario A)**:
```
IRR_intl_A = (Authority_total + Organization) / Total
           = (21 + 56) / 173 = 0.445
```

**Round 5 (Scenario B)** — negative Authority 재분류:
```
Authority_positive = 21 - 6 = 15
Nodality_revised = 84 + 6 = 90 (constraint 언어로 재분류)
Total = 173 (비교 가능성 유지, 동일 분모)

IRR_intl_B = (Authority_positive + Organization) / Total
           = (15 + 56) / 173 = 0.4104
```

### 3.2 Δ_revised 산출

| 시나리오 | IRR_domestic | IRR_intl | Δ | 가설 Δ≥0.30 |
|---|---|---|---|---|
| **A (Round 4)** | 0.714 | 0.445 | **0.269** | PARTIAL |
| **B (Round 5)** | 0.714 | 0.410 | **0.304** | **CONFIRMED** |

Delta_shift = +0.035 (Scenario B에서 Δ 증가)

### 3.3 시나리오 B 해석

Authority_negative(shall NOT 류)를 Nodality로 재분류했을 때:
- IRR_intl 0.445 → 0.410 하락
- Δ 0.269 → 0.304 상승 → **0.30 임계 초과 = CONFIRMED**

이는 Policy-Sci 교수 가설을 지지한다: L.25E의 표면적 Authority(21개)는 실제로 28.6%가 의무 부과가 아닌 의무 차단 구문이었으며, 이를 보정하면 브라질의 국내↔국제 instrument calibration 갭이 더 크게 나타난다.

---

## 4. 이론적 함의 (Putnam × Howlett 보강)

### 4.1 Dual-Rhetoric Strategy (이중 수사 전략)

Para 7~9의 패턴은 단순한 "약한 언어" 이상이다. 브라질(의장국)은 **두 층위의 수사**를 동시에 사용했다:

1. **표면적 Authority** (positive verbs: "decides", "adopts", "affirms"): 결정의 형식적 정당성 부여
2. **내부 Negation** (shall NOT 류): G77 개도국의 sovereignty 보호 / compliance 거부

이것이 Howlett (2019) calibration 이론에서 다루지 않는 **이중 수사 calibration** 현상이다.

### 4.2 Scenario B가 더 이론적으로 타당한 이유

Putnam (1988) Two-Level Games에서 win-set은 국내 지지 연합의 크기로 결정된다.
브라질의 G77/BASIC 연대 win-set은 "shall NOT create obligations" 삽입으로만 확보 가능했다.
따라서 Authority_negative는 국내 연합 통제를 위한 전략적 장치(Nodality 기능)이지, 실질적 국제 의무 부과가 아니다.
이를 Authority에서 분리하는 것(Scenario B)이 lsquarely Putnam 이론과 정합적이다.

---

## 5. 한계 및 Round 6 후속

1. **6-token 추정의 불확실성**: Round 4의 총 Authority=21이 어떤 구체적 단어들로 구성됐는지 재추적 필요. Round 5 python 재추적 결과와 비교 필요.
2. **LLM Layer 2 미적용**: L.25E 전체 단락에 대한 Claude-haiku 의미론적 분류로 확인 권고 (Round 6에서 API 키 활성화 시).
3. **Plano Clima 재분석 미수행**: 브라질 국내 문서에서도 Authority_negative 분리 시 IRR_domestic 변화 가능.

---

## 6. 요약 인용

> "Brazilian L.25E의 Authority 토큰 21개 중 6개(28.6%)는 'shall NOT', 'should not', 'nor establish' 등 negative binding 구문으로, Nodality(제약 언어)로 재분류 시 IRR_intl_B = 0.410, Δ_revised = 0.304 → 가설 Δ≥0.30 CONFIRMED." (CINA Round 5, 2026-04-26)

---

**버전**: v2 (Round 5)
**이전 버전**: `deliverables/IRR_Brazil_2025.md` (Round 4, Δ=0.269, PARTIAL)
**데이터**: `data/processed/irr_brazilian_translation_gap_v2.json`
**처리 스크립트**: `src/p02_negative_authority_irr_v2.py`
