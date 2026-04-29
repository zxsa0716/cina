# Round 4 — Policy-Science Professor Input Package

> 발신: data-refinement-analyst
> 수신: policy-science-professor
> 작성일: 2026-04-26

---

## 1. P0-1: Korean NAP-GGA Crosswalk 30-cell 완성 결과

Round 3 권고 "30-cell 완성" 충족 완료.

### 핵심 정량 발견

| 지표 | Round 3 preliminary | Round 4 완성 |
|---|---|---|
| 셀 커버리지 | 13/30 (43%) | 30/30 (100%) |
| IRR_Korea_2025 (weighted) | 0.66 | **0.653** |
| 95% CI | [0.59, 0.72] | [0.543, 0.644] |
| L&D-OP 평균 IRR (전 섹터) | 0.35 (1셀) | **0.390** (5셀 평균) |
| ADAPT-FIN 평균 IRR | 0.55 (1셀) | **0.490** (5셀 평균) |

### IRR 0.66 → 0.653 변화 해석

예상보다 변화 폭이 작음 (Δ=-0.007). 이는 Round 3의 13-cell이 이미 대표적 high/med 셀 중심으로 구성되어 있었음을 사후 확인. 새로 채워진 17개 셀의 평균 IRR ≈ 0.52 (추정) — 미수집 셀이 약한 이슈(L&D-OP, ADAPT-FIN)에 집중되었기 때문.

### 교수 검토 요청

1. **IRR 집계 방식**: 현재 confidence 보정 (HIGH=1.0, MEDIUM=0.8, LOW_CONFIDENCE=0.5) 추가. 이 보정이 적절한지 방법론 검토 바람.
2. **건강·국민 × GGA-IND** 2개 sub-target (9c health, 9a water) 처리: 동일 이슈 코드 내 2개 셀로 처리함. 이를 1개로 집계할지 유지할지 결정 필요.
3. **LOW_CONFIDENCE 4개 셀** (사회·경제 ADAPT-FIN 0.38, 기반 L&D-OP 0.32, 자연·환경 L&D-OP 0.30, 자연·환경 JT-ADAPT 0.48): Round 5 collector task로 증거 보강 필요 → Round 5 T01에 우선순위 부여 요청.

---

## 2. P0-2: Brazilian IRR Translation Gap 정량화

### 핵심 발견

| 지표 | 값 |
|---|---|
| IRR_domestic (Plano Clima) | **0.714** |
| IRR_international (L.25E) | **0.445** |
| Translation Gap Δ | **0.269** |
| 가설 Δ ≥ 0.30 | PARTIAL (0.269) |
| 가설 Δ ≥ 0.20 | CONFIRMED |

### NATO 4축 핵심 대조

| 축 | 국내 비중 | 국제 비중 | 차이 |
|---|---|---|---|
| Nodality | 24.1% | 48.6% | **+24.5pp (국제 우위)** |
| Authority | 4.3% | 12.1% | +7.8pp (국제 우위, but "shall NOT" 구조) |
| Treasure | 4.5% | 6.9% | +2.4pp |
| **Organization** | **67.1%** | **32.4%** | **-34.7pp (국내 압도적 우위)** |

국내의 Organization 압도 (67.1%) = CIM 중심 고도 제도화
국제의 Nodality 압도 (48.6%) = voluntary/facilitative 언어

### 교수 검토 요청

1. **Δ = 0.269 vs 가설 0.30**: Round 3에서 0.40으로 예상했으나 실제 0.269. 이를 가설 수정이 필요한 "PARTIAL"로 처리할지, 방법론 개선 (LLM Layer 2 추가 or negative Authority 세분화)으로 보완할지 권고 바람.
2. **Putnam × Howlett 논문 포지셔닝**: Translation Gap Δ 개념을 이론적으로 어떻게 명명할지 제안 바람 (예: "instrument-mix divergence index", "calibration gap").
3. **5국 비교 확장 (Round 5)**: KOR, EU, SAU, AOSIS의 동일 cross-walk 필요. 각국 priority 순서 제안 바람.

---

## 3. 방법론 이슈 — 교수 판단 필요

### 이슈 A: NATO 키워드 카운트의 언어 불균형
- 포르투갈어 문서 (308K chars) vs 영어 문서 (34K chars): 9배 분량 차이
- 비율 기반 IRR 사용으로 분량 영향 제거했으나, 포르투갈어 키워드 패턴의 완전성 검증 필요
- 권고: 언어학자 또는 원어민 검토 (Round 5)

### 이슈 B: "Negative Authority"
- L.25E의 Authority 키워드 중 상당수가 "shall NOT" 구조 (규제 부과가 아닌 차단)
- 현재 방법론에서 positive/negative Authority 구분 없음
- 분리 시 국제 Authority 비중이 더 낮아질 것 → Translation Gap 확대 예상

---

## 4. Stage 1 준비 상태 점검 요청

현재 `data/processed/documents.jsonl` 구성:
- 브라질 GGA-IND: 11건 (Round 3 기준)
- 한국 NAP/GGA: 6건
- UNFCCC 공식: 8건 (L.25E 포함)

교수 판단: Stage 1 stance extraction 시작을 위한 최소 corpus 기준이 충족되었는지?
CINA 권고 기준: 20개국 × 6이슈 coverage ≥ 40% (48 pairs).
현재 추정 coverage: ~35%. Round 5 collector 1라운드 후 시작 가능.
