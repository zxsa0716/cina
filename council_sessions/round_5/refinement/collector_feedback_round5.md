# Data Refinement → Data Collector Feedback (Round 5)

> 작성: data-refinement-analyst | 날짜: 2026-04-26

---

## 1. P0-1 처리 중 발견된 Gap

### Gap 1 (High): COP28 UAE 의장 문서 부족 [P0]
- 현재 round4_t01_chair에 COP28 대상 문서 없음 (round4_curated에 1건만)
- UAE (에너지 수출국 의장)의 Tallberg 채널 분석을 위해 COP28 COP/CMA 의장 서한 필요
- **수집 요청**: UNFCCC 공식 포털에서 COP28 Presidency letters (Sultan Al Jaber 서명)

### Gap 2 (High): COP29 Azerbaijan 의장 문서 1건만 존재 [P0]
- round4_curated에 COP29 1건 (Azerbaijan)
- 에너지 수출국 의장 비교 분석을 위해 최소 3건 필요
- **수집 요청**: COP29 Presidency communications (Mukhtar Babayev)

### Gap 3 (High): COP28 UAE-Belem Work Programme 최종 보고서 [P0]
- UAE-Belem indicators 합의 과정 문서 (SBI/SBSTA 공동 의장 보고서) 미수집
- **수집 요청**: FCCC/SBSTA/2024/7 + FCCC/SBI/2024/13 관련 섹션

### Gap 4 (Medium): LMDC 그룹 제출 문서 [P1]
- documents.jsonl에서 LMDC 태그 독립 문서 0건 (G77 합산 처리 중)
- 2D plot에서 LMDC 위치 별도 표시 불가
- **수집 요청**: LMDC (Like-Minded Developing Countries) 2025 GGA submissions

### Gap 5 (Medium): ENB Castro 2025 co-sponsorship data [P1]
- B0 pseudo-truth를 실제 협력 데이터로 대체해야 함
- **수집 요청**: IISD ENB 2025 데이터셋에서 joint-submission 및 co-sponsorship 쌍 추출
- 참조: Castro et al. 2025 (https://www.nature.com/articles/s41597-025-06262-4)

### Gap 6 (Medium): SBI/SBSTA 62nd session (June 2026) 문서 [P1]
- Round 6 분석을 위한 COP30 후속 문서
- **수집 요청**: SB 62 (2026년 6월) 적응 의제 관련 문서

---

## 2. P0-2 처리 중 발견된 Gap

### Gap 7 (High): Plano Clima negative authority 분석용 포르투갈어 negation 패턴 [P0]
- L.25E에서 negative authority 분리 완료 → Plano Clima에도 동일 적용 필요
- "não deverá", "não obrigatório", "vedado" 등 포르투갈어 negation 수집
- **분석 요청**: Plano Clima 3개 PDF에서 negative authority 한국어 포르투갈어 재분석

### Gap 8 (Medium): L.25 advance vs L.25E final 비교 문서 [P1]
- FCCC/PA/CMA/2025/L.25_advance.pdf가 이미 수집됨
- L.25 → L.25E 변화에서 negative authority 토큰이 추가됐는지 추적 가능
- **분석 요청**: L.25_advance와 L.25E_final을 diff 비교 (협상 압력 흔적 추적)

---

## 3. 우선순위 요약

| 우선순위 | Gap | 요청 대상 |
|---|---|---|
| P0 (즉시) | Gap 1: COP28 UAE 의장 서한 | Collector |
| P0 (즉시) | Gap 2: COP29 AZE 의장 서한 | Collector |
| P0 (즉시) | Gap 3: FCCC/SBSTA/2024/7 | Collector |
| P0 (즉시) | Gap 7: Plano Clima neg auth 분석 | Collector/Refinement |
| P1 | Gap 4: LMDC submissions | Collector |
| P1 | Gap 5: ENB Castro 2025 co-sponsorship | Collector |
| P1 | Gap 6: SB 62 문서 | Collector |
| P1 | Gap 8: L.25 vs L.25E diff | Refinement |

---

## 4. Round 6 Collector Task 권고

Round 6 Collector task에 다음을 반영 요청:

1. COP28/COP29 Presidency letters 우선 수집 (Tallberg 분석 완성)
2. LMDC 2025 GGA submissions (hedging density group 분리)
3. Castro ENB 2025 co-sponsorship dataset (B0 ground truth 대체)
4. Bayer-Urpelainen threshold 80 도달을 위해 총 24개 chair docs 추가 목표

---

**chair_metadata 진도**: 56/80 (70%) — R6에서 80 목표
**2D plot group coverage**: 7/7 groups 표시 중 (LMDC 독립 분류 미완)
