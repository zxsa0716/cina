---
assigned_to: ir-political-professor
agent_model: opus
round: 5
priority: P0
depends_on:
  - council_sessions/round_5/refinement/professor_input/ir_pack_round5.md
  - council_sessions/round_5/tasks/T02_refinement_task.md (P0-1, P0-3, P0-4 산출 필수)
  - council_sessions/round_5/tasks/T01_collector_task.md (P0-1 Castro matrix, P0-2 SBI/SBSTA notes)
  - council_sessions/round_4/ir_political/critique.md (R4 baseline 4.36)
deadline: Round 5 cross-review 작성 전
---

## 목적

Round 4 4 P0 권고 후속 검증. (1) Castro 2025 cooperation matrix 실데이터 후 Realist B0 F1 정량 통계로 재검증, (2) chair_metadata N=60+ 확장 후 Bayer-Urpelainen panel threshold N≥80 도달 가시화, (3) L.25 pre-crystallized formula 가설을 Tallberg(ii)+(iv) ⊕ Steinberg ⊕ Goh framing으로 정련 → NeurIPS CCAI signature finding 후보 정식화, (4) hedging density × group red line 2D plot 해석. Round 5에서 IR 4.36 → 4.55+ 도약 목표.

---

## 구체 산출물 (P0)

### P0-1. Castro 2025 cooperation matrix 후 Realist B0 F1 재검증 (IR R4 P0-3 후속)

- [ ] T01 R5 P0-1 산출 (`data/raw/round5/castro_2025_matrix/`) cooperation matrix CSV 정독
- [ ] T02 R5 P0-3 산출 (`data/processed/realist_b0_statistics.json`) 정독:
  - F1=0.560, McNemar p, Cohen κ, 95% CI [lower, upper]
- [ ] Castro 매트릭스로 cross-validation 가능 여부 평가:
  - Castro 그라운드 트루스 vs B0 prediction 직접 비교
  - Castro 매트릭스 차원이 CINA stance schema와 호환되는지
- [ ] 두 가능성 framing:
  - 시나리오 A: Castro 매트릭스 호환 가능 → B0 F1 cross-validated, IR §4.1 #3 권고 충족
  - 시나리오 B: 매트릭스 schema mismatch → R6 schema bridge 작업 필요 (P1)
- [ ] **결정적 판단**: Castro 데이터 활용으로 IR §4.1 권고 #3 (B0 cross-validation) 충족 여부

### P0-2. chair_metadata N=60+ 후 Bayer-Urpelainen panel threshold 가시화 (IR §3.1.A 후속)

- [ ] T02 R5 P0-1 산출 (`data/processed/chair_metadata.jsonl` ≥60 records) 정독
- [ ] Tallberg(2010) 4 채널 시계열 분석:
  - formula control 빈도 (COP21→COP30)
  - agenda shaping 빈도
  - brokerage 빈도
  - information asymmetry 빈도
- [ ] "energy exporter chair 3연속 (COP28 UAE / COP29 AZE / COP30 BRA)" 가설 검증 가능 여부
  - 3 chair의 frame_type 분포 비교
  - 화석연료 산업 보호 언어 빈도 (oil/gas/petroleum/transition fuel) 비교
- [ ] Bayer-Urpelainen N≥80 도달 estimation: R6 +20 records (총 80) 가능 여부
  - SBI/SBSTA informal notes (R5 P0-2) 추가 + 추가 GST/JT-WP letter 검토

### P0-3. L.25 pre-crystallized formula 가설 정련 (R4 §2.4 후속, NeurIPS CCAI signature 후보)

- [ ] T01 R5 P0-2 산출 (`data/raw/round5/sbi_sbsta_notes/EVIDENCE_NOTES.md`) 정독
- [ ] contact group informal notes 4건에서 pre-cooking signal 추출:
  - Co-Facilitator의 "synthesis text" 등장 시점 vs L.25 advance text 등장 시점
  - 사전협상 단계에서 합의 언어가 이미 존재했던 정황 (Goh 2008)
- [ ] 통합 framing 정식화 (NeurIPS CCAI signature finding 후보):
  - **Mechanism A (Tallberg ii)**: agenda shaping — 의장국이 사전 합의 텍스트로 옵션 공간 축소
  - **Mechanism B (Tallberg iv)**: brokerage — 의장국이 contact group facilitator를 통해 사전 합의 도출
  - **Mechanism C (Steinberg 2002)**: consensus shaping — 다수 합의의 환상 (illusion of multilateral consensus)
  - **Mechanism D (Goh 2008)**: informal pre-cooking — formal session 전 informal 트랙에서 합의 완성
- [ ] L.25 cosine hot_spots=0 evidence를 4 mechanism에 매핑
- [ ] **결정적 framing**: "L.25 hot_spots=0이 cosine baseline의 실패가 아닌 pre-crystallized formula의 첫 정량 검증" 학술 정당성 명시

### P0-4. hedging density × group red line 2D plot 해석 (R4 §4.1 #4 후속)

- [ ] T02 R5 P0-4 산출 (`data/processed/figures/hedging_vs_redline_2d.png`) 검토
- [ ] 협상그룹별 위치 IR 해석:
  - AILAC (high redline + low hedging) → norm entrepreneur 가설 적합
  - LDC (high redline + high hedging) → strategic 권력 약자 (Underdal 1980)
  - AOSIS (high redline + medium hedging) → moral authority + diplomatic skill
  - BRA (medium redline + high hedging) → chair-host paradox (Hochstetler)
  - KOR (low redline + high hedging) → middle power free-riding (Cooper et al. 1993)
- [ ] **결정적 판단**: 5 group의 visual separation이 충분한가? 통계적 유의 (Hotelling T² 또는 ANOVA) 추가 권고

### P0-5. 5-Dim 자기평가 + Round 6 권고

- [ ] 5-Dim 점수 self-rate (R4 4.36 baseline):
  - Theoretical (R4 4.6)
  - Methodological (R4 4.0)
  - Empirical (R4 4.4)
  - Policy strategic (R4 4.3)
  - Reproducibility (R4 4.5)
- [ ] mean ≥ 4.55 목표
- [ ] Round 6 권고 P0/P1 list (3-5건)
- [ ] team-lead 결정 필요 사안 (D-R6-x) 0-3건

---

## 품질 기준

- [ ] Castro 매트릭스 cross-validation 결과가 통계적으로 방어 가능
- [ ] Bayer-Urpelainen N≥80 도달 estimation이 정량 (R6 추가 수집 minimum N 명시)
- [ ] L.25 pre-crystallized formula 4-mechanism framing이 reviewer에게 학술 정당성 명시
- [ ] 2D plot 5 group 해석이 IR 이론 (Underdal/Cooper/Hochstetler) 정합
- [ ] 5-Dim 점수 변동 시 정량 근거 명시

---

## 제공된 컨텍스트

### Round 4 critique 자기 진술 (요약)
- Combined 5-Dim mean 4.36, theoretical/empirical 모두 +0.5 상승
- raw 24 PDF processed 통합 미완 결정적 한계 → R5 P0-1로 처리
- pre-crystallized formula 가설을 Tallberg(ii)+(iv) + Steinberg "consensus shaping" + Goh "informal pre-cooking" 통합 framing — NeurIPS CCAI signature finding 후보

### Policy critique cross-reference
- Policy C1 Brazilian negative Authority 분리 → IR §2.3 dual-role strategic ambiguity 보완
- Policy C2 KEI 가중치 외부 정합성 → IR §3.1.D internal validity 우선

### Round 4 cross-review §3 (CR4 list)
- CR4.4 Castro matrix → T01 P0-1 (R5)
- CR4.6 SBI/SBSTA notes → T01 P0-2 (R5)
- CR4.5 2D plot → T02 P0-4 (R5)
- CR4.2 B0 통계 → T02 P0-3 (R5)
- CR4.3 24 PDF processed → T02 P0-1 (R5)

### Round 4 cross-review §4 (team-lead 권고)
- D-R5-5: L.25 pre-crystallized formula 단일 signature finding 채택

---

## 출력 위치

- `council_sessions/round_5/ir_political/critique.md`
