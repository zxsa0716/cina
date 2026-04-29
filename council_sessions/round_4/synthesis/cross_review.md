# Round 4 Cross-Review — Two-Professor Synthesis

**Round**: 4 (Closing)
**Composed by**: team-lead
**Date**: 2026-04-26
**Inputs**:
- `council_sessions/round_4/policy_science/critique.md` (Policy 4.38/5)
- `council_sessions/round_4/ir_political/critique.md` (IR 4.36/5)
- `council_sessions/round_4/refinement/collector_feedback_round4.md`
- `council_sessions/round_4/data_collection/manifest.jsonl` (156 entries)
- Round 3 quality_gates baseline

---

## 0. Executive Summary

**Round 4 dual-review combined mean = (4.38 + 4.36) / 2 = 4.37/5** — Round 3 (4.105) 대비 +0.265, R1→R4 누적 +1.32 (+26.4%p). **Major→Minor revision phase consolidated**, NeurIPS CCAI 워크숍 acceptable threshold (>4.0/5) 두 번째 라운드 연속 상회. 24 historical chair letters 추가(+200% target 달성)와 4 P0 refinement 산출(IRR_Korea 0.653 / Brazilian Δ=0.269 / Realist B0 F1=0.560 / L.25 hot_spots=0)이 Round 4 진척의 4 기둥. **3개 PASS gate (G3·G4·G5) 유지, G1·G2 partial → Round 5에서 PASS 임박**.

---

## 1. 합의 매트릭스 (5건)

### A1. 24 PDF processed pipeline 통합이 Round 5 P0 (양교수 만장일치)

- **Policy 인용**: critique §4.2 "raw 24 PDFs (T01 200% 달성) 가 chair_metadata.jsonl에 통합되지 않으면 Bayer-Urpelainen panel threshold N≥80 도달 무산"
- **IR 인용**: critique §3.1.A "T01 24 PDF는 산식 입력 아닌 raw asset. T02 R5 P0-1으로 chair_metadata N=32→80+ 확장이 R5 결정적 priority"
- **처리**: Round 5 T02 P0-1로 명시 발급. 산출 시 G1 Coverage 0.71 → 0.83 도달 예상.

### A2. Combined 4.37/5 — Minor Revision phase 명확 진입 (양교수 만장일치)

- Policy 4.38 (theoretical 4.5 / methodological 4.0 / empirical 4.4 / policy strategic 4.3 / reproducibility 4.7)
- IR 4.36 (theoretical / empirical 모두 +0.5 상승)
- **공동 판단**: NeurIPS CCAI 2026 워크숍 acceptable threshold (>4.0) 두 번째 연속 상회. Global Environmental Change R&R 임박.

### A3. L.25 hot_spots = 0 → "pre-crystallized formula" 가설 채택

- **Policy 인용**: critique §3.3 "hot_spots=0은 cosine baseline 의 negative finding이 아닌 새 가설 — 사전협상 과정에서 이미 합의 텍스트가 존재했던 정황"
- **IR 인용**: critique §2.4 "Tallberg(ii) formula control + (iv) brokerage + Steinberg(2002) 'consensus shaping' + Goh(2008) 'informal pre-cooking' 통합 framing → NeurIPS CCAI signature finding 후보"
- **처리**: Round 5 T01 P0 Tallberg pre-cooking evidence 수집 (contact group informal notes), T02 산출물에 framing 명시.

### A4. Realist B0 F1=0.560 — 가설 (F1<0.70) CONFIRMED

- **Policy 인용**: §4.3 "B0 단독으로는 stance prediction 60% 미달 → CINA Stage 2 R-GAT의 incremental value 정량 정당화"
- **IR 인용**: §3.2.B "F1=0.560 confirm은 '국제정치 = 권력만으로 설명되지 않음' 헌법 §4 명제의 첫 정량 evidence. 단 N=32 chair 기반이라 95%CI bootstrap 필수"
- **처리**: Round 5 T02 P0-2 McNemar test + Cohen κ + 95%CI bootstrap 산출.

### A5. Stage 1 LLM trial 5건 정상 가동 — 헌법 §4 회복

- 양교수 모두 acknowledge: ANTHROPIC_API_KEY + prompt v1.4 + 5건 trial run (L.25 final + AOSIS_SCF + LMDC_GGA + Plano Clima Sumário + ENB COP30) 모두 schema-valid 산출.
- **공동 평가**: directive #4 (LLM-GNN-LLM novelty intact) full PASS.

---

## 2. 불일치 매트릭스 (3건, 모두 productive·양립 가능)

### D-R4C-1. Brazilian Δ=0.269 학술 기여 risk vs signature finding

- **Policy critique C1**: "Brazilian L.25E의 negative Authority ('shall NOT')가 Δ 산식에 포함되어 0.269가 inflate. negative Authority 분리 후 재계산 필요. 분리 시 Δ>0.30 가설 PARTIAL → CONFIRMED 가능"
- **IR critique §2.3**: "Δ=0.269 PARTIAL은 첫 정량 검증으로 그 자체로 학술 가치. 단 Brazilian dual-role의 strategic ambiguity로 framing 권고"
- **처리**: 양립. Round 5 T02 Policy P0가 negative Authority 분리 → IRR_intl 재계산 → Δ 변동량 산출. Δ>0.30 도달 시 CONFIRMED, 미달 시 PARTIAL 유지하되 두 framing(strategic ambiguity / instrument inflation) 동시 보고.

### D-R4C-2. KEI 명수정 박사 외부 정합성 협의 (Policy 권고) vs 통계적 rigor 우선 (IR 권고)

- **Policy critique C2**: "IRR_Korea 가중치 (Authority 0.35 / Treasure 0.25 / ...) 가 외부 정합성 검증 없음. KEI 명수정 박사 (한국 NAP IRR 권위자) email 협의 권고"
- **IR critique §3.1.D**: "외부 협의는 social validation. 우선 N≥80 panel + bootstrap CI로 internal validity 확보 후 R6 외부 협의가 더 효율적"
- **처리**: 양립. Round 5 T01 P0-3 KEI WP 시리즈 5건 추가 수집(공식 가중치 reference 확인) + T02 P0-2 statistical rigor 산출. KEI 직접 협의는 Heedo 결정 (D-R5-2).

### D-R4C-3. 24 PDF processed 통합 범위 (전수 vs 우선순위 표본)

- **Policy critique §4.2**: "24건 모두 통합하여 chair_metadata N=56 (32+24) 확보 우선"
- **IR critique §3.1.A**: "Bayer-Urpelainen N≥80 충족 위해 COP21~27 24건 + 추가 GST/SBI letter 검토 병행. 단 LLM-extraction 비용 (~$8) 정당"
- **처리**: 양립. Round 5 T02 P0-1로 24건 전수 통합 + T01 P0-1로 SBI/SBSTA informal note 추가 (≥4건). 목표 chair_metadata N≥60 (Round 5), N≥80 (Round 6).

---

## 3. 결정적 비판 (Round 5 P0로 승격)

### CR4.1 (Policy P0): Brazilian negative Authority 분리 → IRR_intl 재계산

- **근거**: critique C1
- **처리**: T02 R5 P0 (`tasks/T02_refinement_task.md`)
- **목표**: Δ_revised > 0.30 → CONFIRMED 또는 PARTIAL 유지 framing 정밀화

### CR4.2 (IR P0): Realist B0 F1 통계 정량 (McNemar / κ / 95%CI)

- **근거**: critique §3.2.B
- **처리**: T02 R5 P0
- **목표**: McNemar p<.05 + κ 효과크기 + bootstrap 95%CI [lower, upper] 산출

### CR4.3 (양교수 공통 P0): 24 PDF processed pipeline 통합

- **근거**: A1 합의
- **처리**: T02 R5 P0-1
- **목표**: chair_metadata 32 → 60+ (24 신규 추출 + 기존 LLM polishing 4)

### CR4.4 (IR P0): Castro 2025 ENB cooperation matrix 실제 다운로드

- **근거**: IR critique §4.1 권고 #3
- **처리**: T01 R5 P0
- **목표**: Nature Sci Data supplement (figshare/zenodo) 추적 → 실제 cooperation matrix CSV 확보 → Stage 2 baseline ground-truth

### CR4.5 (IR P1): hedging density × group red line 2D plot

- **근거**: IR critique §4.1 권고 #4
- **처리**: T02 R5 P0-4
- **목표**: matplotlib scatter (x=hedging density, y=group red line salience) → AILAC/LDC/AOSIS 3 위치 산점도

### CR4.6 (IR P0): Tallberg pre-cooking evidence (contact group informal notes)

- **근거**: A3 합의
- **처리**: T01 R5 P0-2
- **목표**: UNFCCC SBI/SBSTA informal notes ≥4건 (L.25 사전협상 추적용)

---

## 4. team-lead 결정 (D-R5-1 ~ D-R5-5 사전 권고)

Policy critique에서 Heedo 결정 요청 5건. 헌법 정합성 사전 평가:

| 결정 | 내용 | team-lead 권고 |
|------|------|----------------|
| **D-R5-1** | Brazilian Δ negative Authority 분리 후 framing | A: 분리 + dual-framing 보고 (학술 안전) |
| **D-R5-2** | KEI 명수정 박사 외부 협의 시점 | B: Round 6 (R5는 internal validity 우선) |
| **D-R5-3** | Plano Clima 분기 챕터 (D-R4-1 잔여) | A: 분기 (multi-theoretical triangulation 학술 가치) |
| **D-R5-4** | Korean L&D-OP 0.390 약점 권고 우선순위 | A: 수업 brief 직접 활용 (Track A 가속) |
| **D-R5-5** | NeurIPS CCAI signature finding 선정 | "L.25 pre-crystallized formula" 단일 채택 |

상세 기술은 LEAD_REPORT_FINAL §"Heedo 결정 필요 사안" 참조.

---

## 5. 헌법 (Heedo Intent Lock) 재확인

| Directive | Status R3 | Status R4 | 변화 |
|-----------|-----------|-----------|------|
| #1 publishable-grade (NeurIPS CCAI) | partial-pass (4.105) | **PASS** (4.37, signature finding 후보 발견) | +0.265 |
| #2 COP30 retrospective (Belém Adaptation) | PASS (110 indicators + 32 chair) | **PASS strengthened** (24 historical + L.25 pre-crystallized 가설) | 강화 |
| #3 dual track (Track A + B) | PASS partial (Track A 가속) | **PASS** (Track A: Korean L&D-OP 0.390 권고 + Track B: Brazilian Δ paradox + F1 confirm) | 강화 |
| #4 LLM-GNN-LLM | partial (LLM 미가동) | **PASS** (Stage 1 trial 5건 정상) | full PASS |

**헌법 4건 모두 PASS — Round 5 종료 시 5 게이트 모두 PASS 도달 가능 (R6 종결 가능성 고조)**.

---

## 6. Round 5 task 발급 요약

| Task | Agent | Priority | Key Deliverable |
|------|-------|----------|-----------------|
| T01 | policy-data-collector | P0 | Castro 2025 ENB matrix + SBI/SBSTA informal notes ≥4건 + KEI WP 5건 |
| T02 | data-refinement-analyst | P0 | 24 PDF chair_metadata 통합 + Brazilian neg Auth 분리 + B0 통계 + 2D plot |
| T03 | policy-science-professor | opus | Brazilian Δ 재평가 + IRR Korea 가중치 외부 정합성 review |
| T04 | ir-political-professor | opus | F1 통계 후 realist baseline 재검증 + pre-crystallized formula framing 정련 |

상세는 `council_sessions/round_5/tasks/` 4 파일 참조.
