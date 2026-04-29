---
assigned_to: data-refinement-analyst
agent_model: sonnet
round: 5
priority: P0
depends_on:
  - council_sessions/round_5/tasks/T01_collector_task.md (P0-1, P0-2)
  - council_sessions/round_4/refinement/collector_feedback_round4.md
  - council_sessions/round_4/synthesis/cross_review.md
deadline: Round 5 dual review 시작 전
---

## 목적

Round 4 4 P0 산출물의 후속 작업 4종을 P0로 처리한다.
(1) IR critique §4.1 권고 #1 — 24 historical chair PDF processed pipeline 통합으로 chair_metadata N=32→60+ 확장 (Bayer-Urpelainen panel threshold 80 도달 R6 가시화).
(2) Policy critique C1 — Brazilian L.25E negative Authority ("shall NOT") 분리 후 IRR_intl 재계산 → Δ_revised 산출 → Δ>0.30 가설 CONFIRMED 검증.
(3) IR critique §3.2.B — Realist baseline B0 F1=0.560 통계적 정량 (McNemar test + Cohen κ + 95%CI bootstrap).
(4) IR critique §4.1 권고 #4 — hedging density × group red line 2D plot (matplotlib).

---

## 구체 산출물 (P0)

### P0-1. 24 PDF processed pipeline 통합 (IR P0-1)

- [ ] T01 R4 산출 24 historical chair letters (COP21-27 + COP30 Troika) PDF 모두 정제
- [ ] 각 PDF에 대해 chair_metadata 추출 schema 적용 (chair_role, presidency, session, formula_control_signal, agenda_shaping_signal, brokerage_signal, information_signal)
- [ ] Stage 1 LLM (prompt v1.4) 활용 추출 권고 (LLM 미가동 시 rule-based fallback)
- [ ] `data/processed/chair_metadata.jsonl` 32 → ≥60 record 확장
- [ ] 출처 분포: cop30_curated 12 + iisd_enb 3 + brazilian_gov 1 + ndc 7 + round3_curated 3 + round4_curated 6 + **round4_t01_chair 24** + (R5 SBI/SBSTA 노트 4건 추가 가능)
- [ ] 산출 statistics: `data/processed/chair_metadata_stats_v2.json`
- [ ] Tallberg 4 채널 시계열 분석 (COP21~COP30, energy exporter chair 비율 등)

### P0-2. Brazilian negative Authority 분리 + IRR_intl 재계산 (Policy P0, CR4.1)

- [ ] L.25E (FCCC/PA/CMA/2025/L.25) 텍스트 재정독
- [ ] "shall NOT", "shall not", "without prejudice", "voluntary" 등 negative-binding 구문 식별
- [ ] negative Authority 카운트 분리:
  - `authority_positive` (binding "shall") vs `authority_negative` ("shall NOT" + voluntary opt-out)
- [ ] IRR_intl 재계산: `IRR_intl_revised = (Σ W_k × Realized_k_positive) / (Σ W_k × Promised_k)`
- [ ] Δ_revised = IRR_Korea_2025 - IRR_intl_revised 산출
- [ ] 두 시나리오 보고:
  - 시나리오 A (negative 미분리, 기존): Δ = 0.269 (PARTIAL, 가설 미달)
  - 시나리오 B (negative 분리, 신규): Δ = X.XXX (CONFIRMED 또는 PARTIAL)
- [ ] `data/processed/irr_brazilian_translation_gap_v2.json` 산출

### P0-3. Realist B0 F1 통계적 정량 (IR P0-2, CR4.2)

- [ ] B0 베이스라인 (chair_status + GDP + MILEX + alliances + CO2 emissions) F1=0.560 재현 코드 검증
- [ ] McNemar test (B0 vs CINA full pipeline 가상 비교 또는 B0 vs random) → p-value
- [ ] Cohen κ (B0 prediction vs ground-truth) → 효과 크기 (slight/fair/moderate)
- [ ] Bootstrap 95% CI (n_resamples=1000, seed=42) → [F1_lower, F1_upper]
- [ ] 결과 표:
  | Metric | Value | 95% CI | p-value | κ |
  |--------|-------|--------|---------|---|
  | B0 F1 | 0.560 | [X, Y] | Z | W |
- [ ] `data/processed/realist_b0_statistics.json` 산출
- [ ] N=32 chair 한계 명시 (R6 N≥80 후 재산출 권고)

### P0-4. hedging density × group red line 2D plot (IR P0-4, CR4.5)

- [ ] hedging density 정의: 문서당 hedging modal verb (may/might/could/should/可能/可) 빈도 / 총 단어 수
- [ ] group red line salience 정의: 협상그룹 핵심 입장(AOSIS 1.5°C / LDC L&D / AILAC GST quality) 명시 빈도 score [0, 1]
- [ ] `data/processed/documents.jsonl` 119 records 대상 두 metric 산출
- [ ] matplotlib scatter:
  - x = hedging density
  - y = group red line salience
  - color = 협상그룹 (AILAC=red, LDC=green, AOSIS=blue, BRA=purple, KOR=orange)
  - annotation = 각 group 위치 평균에 ellipse
- [ ] `data/processed/figures/hedging_vs_redline_2d.png` (300 dpi) + `.svg`
- [ ] caption draft (`data/processed/figures/CAPTIONS.md`)

---

## 품질 기준

- [ ] chair_metadata ≥ 60 records (32+24+ε), 100% schema-valid
- [ ] Brazilian Δ_revised 두 시나리오 모두 evidence-quote 첨부 (L.25E 원문 인용)
- [ ] B0 통계 3종 모두 산출 + bootstrap seed 명시
- [ ] 2D plot 300 dpi + SVG vector + caption
- [ ] 모든 산출물 reproducibility 보장 (seed=42, prompt version=v1.4)
- [ ] LLM 호출 시 cost <$5 유지 (Stage 1 추가 trial 시)

---

## 제공된 컨텍스트

### Round 4 4 P0 산출물 (요약)
- IRR_Korea_2025 = 0.653 (CI [0.543, 0.644]), L&D-OP 0.390 최약점
- IRR_Brazilian_Translation_Gap Δ = 0.269 (가설 0.30 PARTIAL)
- Realist B0 F1 = 0.560 (가설 F1<0.70 CONFIRMED)
- L.25 hot_spots = 0 (pre-crystallized formula 가설)

### Policy critique C1 (인용)
> "Brazilian L.25E의 negative Authority ('shall NOT')가 Δ 산식에 포함되어 0.269가 inflate. negative Authority 분리 후 재계산 시 Δ>0.30 가능."

### IR critique §3.2.B (인용)
> "F1=0.560 confirm은 헌법 §4 명제의 첫 정량 evidence. 단 N=32 기반이라 95%CI bootstrap 필수."

### IR critique §4.1 권고 #4 (인용)
> "hedging density × group red line 2D plot — AILAC/LDC/AOSIS 3 위치가 시각적으로 분리되면 norm entrepreneurship 정량 evidence."

---

## 출력 위치

- `data/processed/chair_metadata.jsonl` (overwrite, ≥60 records)
- `data/processed/chair_metadata_stats_v2.json`
- `data/processed/irr_brazilian_translation_gap_v2.json`
- `data/processed/realist_b0_statistics.json`
- `data/processed/figures/hedging_vs_redline_2d.png` (+ .svg)
- `data/processed/figures/CAPTIONS.md`
- `council_sessions/round_5/refinement/REPORT.md`
- `council_sessions/round_5/refinement/professor_input/policy_sci_pack_round5.md`
- `council_sessions/round_5/refinement/professor_input/ir_pack_round5.md`
