# Round 5 — IR 교수 전달 패키지

> 작성: data-refinement-analyst | 날짜: 2026-04-26 | Round 5

---

## 1. §3.2.B 비평 후속: B0 F1 통계적 정량 완료

### 1.1 교수 원문 비평 (Round 4)
> "F1=0.560 confirm은 헌법 §4 명제의 첫 정량 evidence. 단 N=32 기반이라 95%CI bootstrap 필수."

### 1.2 Round 5 통계 결과

| Metric | Value | 95% CI (bootstrap) | p-value | Cohen κ |
|---|---|---|---|---|
| B0 F1 | **0.560** | **[0.458, 0.654]** | **< 0.0001** | **0.216 (fair)** |
| Random F1 | 0.440 | N/A | baseline | N/A |

**방법**: Bootstrap n=1000, seed=42 / McNemar chi²=16.1 (vs Random) / Cohen κ Landis&Koch 기준

### 1.3 해석

1. **통계적 유의성 CONFIRMED** (p < 0.0001): B0는 우연보다 유의하게 협력 쌍 예측
2. **실용적 한계 CONFIRMED** (F1=0.560 < 0.70, κ=0.216 = fair): realism alone insufficient
3. **CI 폭 넓음** [0.458, 0.654]: N=32 기반의 불안정성 노출 → 교수 지적 정확

**N=32 한계**: Round 5 후 chair_metadata = 56 records (56/80 = 70.0%).
Bayer-Urpelainen (2021) panel threshold 80 도달을 위해 Round 6에서 24개 추가 수집 필요.

---

## 2. §4.1 권고 #1 후속: chair_metadata 확장

### 2.1 교수 권고 (Round 4)
> "24 historical chair PDF processed pipeline 통합 → chair_metadata N=32→60+ 확장"

### 2.2 Round 5 처리 결과

| 소스 | 건수 | 비고 |
|---|---|---|
| cop30_curated | 13 | Round 1-3 |
| iisd_enb | 3 | Round 1-3 |
| brazilian_gov | 1 | Round 1-3 |
| ndc | 7 | Round 3 |
| round3_curated | 3 | Round 3 |
| round4_curated | 5 | Round 4 |
| **round4_t01_chair (신규)** | **24** | Round 5 (P0-1) |
| **합계** | **56** | 32 → **56 (+24)** |

**Bayer-Urpelainen 진도**: 56/80 = **70%** (Round 6에서 80 도달 가시)

### 2.3 Tallberg 4채널 분포 (신규 24개 기준)

| 채널 | 건수 | 주요 문서 유형 |
|---|---|---|
| formula_control | 3 | COP21 Paris statement, COP22 session report, COP23 elements of outcome |
| brokerage | 19 | 대부분의 pre-COP letters, COP30 CPD letters |
| agenda_shaping | 1 | COP30 CPD 5th letter (Aug 2025) |
| information | 1 | COP21 scanned info note |

### 2.4 에너지 수출국 의장 패턴

COP21-COP30 중 에너지 수출국 의장:
- COP24: Poland (석탄)
- COP28: UAE (석유)
- COP29: Azerbaijan (가스)

비중: 3/10 = **30%** (2015-2025 기간)

**교수께 질문**: Tallberg (2006) 이론에서 energy exporter 의장은 formula_control 채널보다 information/agenda_shaping 채널을 선호한다는 가설이 있는가? 현재 데이터에서 UAE(COP28) 문서가 brokerage 채널로 분류됨 — 이것이 예상과 일치하는가?

---

## 3. §4.1 권고 #4 후속: Hedging Density × Red Line 2D Plot

### 3.1 교수 권고 (Round 4)
> "hedging density × group red line 2D plot — AILAC/LDC/AOSIS 3 위치가 시각적으로 분리되면 norm entrepreneurship 정량 evidence."

### 3.2 Round 5 시각화 결과

**Group 중심점 요약**:

| Group | Hedging Density (mean) | Red Line Salience (mean) | 해석 |
|---|---|---|---|
| AILAC | 0.0088 | 0.200 | High hedge + Moderate RL: norm entrepreneurship 전형 |
| AOSIS | 0.0018 | 0.224 | Low hedge + High RL: survival framing (compromise 불가) |
| LDC | 0.0056 | 0.130 | Moderate both: strategic ambiguity |
| G77_BRA | 0.0015 | 0.000 | Low both: presidency neutral language |
| EIG_KOR | 0.0002 | 0.000 | Very low: technical reporting documents |
| EU | 0.0024 | 1.000 | Single doc (outlier) |

**교수 가설 검증**:
- "AILAC/LDC/AOSIS 3 위치가 시각적으로 분리되면 norm entrepreneurship 정량 evidence"
- 결과: AILAC(최고 헤징) vs AOSIS(최고 레드라인) vs LDC(중간) **분리 확인**
- AILAC의 "high hedge + moderate red line" 위치는 Finnemore & Sikkink (1998) norm entrepreneur 패턴과 일치: 야망적 목표를 diplomatic language로 포장

### 3.3 교수께 해석 요청

1. AILAC의 높은 hedging density가 "전략적 모호성(strategic ambiguity)"인가, 아니면 "규범 구성(norm framing)"인가? IR 이론에서 이 둘을 어떻게 구분하는가?

2. AOSIS의 낮은 hedging + 높은 red line salience는 "강경 포지셔닝(hard positioning)"으로 해석 가능한가? Putnam Two-Level Games에서 이것이 win-set을 좁히는가, 넓히는가?

3. G77_BRA의 낮은 hedging + 낮은 red line: 이것이 브라질 의장국의 "procedural neutrality" 전략인가? Chayes & Chayes (1995) managerial compliance 이론과 연결 가능한가?

---

## 4. Round 6 IR 교수 요청사항

1. **N=80 chair_metadata 도달 후 B0 F1 재산출**: 현재 56개 → 추가 24개 필요. 어느 COP 세션 문서를 우선 수집해야 하는가?

2. **Tallberg 채널 × 에너지 수출국 교차 분석**: COP24/28/29 (에너지 수출국 의장)에서 brokerage/formula_control 비율이 비에너지 의장국과 다른가?

3. **Castro ENB 2025 co-sponsorship 데이터**: B0 pseudo-truth를 대체하기 위해 실제 협력 데이터가 필요. R6 Collector task에 포함 요청.

---

## 5. 산출물 목록

| 파일 | 내용 |
|---|---|
| `data/processed/chair_metadata.jsonl` | 56 records (32→56 확장) |
| `data/processed/chair_metadata_stats_v2.json` | 통계 |
| `data/processed/realist_b0_statistics.json` | F1 + bootstrap + McNemar + kappa |
| `deliverables/realist_b0_statistics.md` | 보고서 |
| `data/processed/figures/hedging_vs_redline_2d.png` | 2D scatter (300 dpi) |
| `data/processed/figures/hedging_vs_redline_2d.svg` | SVG vector |
| `data/processed/figures/CAPTIONS.md` | Figure captions (EN+KR) |
