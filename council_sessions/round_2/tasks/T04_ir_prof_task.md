---
assigned_to: ir-political-professor
model: opus
round: 2
priority: P0
issued_at: 2026-04-25
deadline: round_2_close (after T02 refinement completes)
depends_on:
  - council_sessions/round_2/refinement/professor_input/ir_pack_v2.md
  - council_sessions/round_2/refinement/quality_report.md
  - council_sessions/round_1/ir_political/critique.md
  - council_sessions/round_1/synthesis/cross_review.md
---

# T04 (Round 2) — IR/외교학 교수: 권고 반영 검증 + 심화 비판

## 1. 목적
Round 1 IR critique에서 제기한 3대 비판(C1 chairmanship power, C2 paradigm balance, C3 hypergraph linkage)이 (a) team-lead의 처리 결정과 (b) Round 2 데이터·스키마에 어떻게 반영되었는지 검증한다. 동시에 신규 corpus(70-100건)에 대한 IR 심화 비판을 수행한다.

## 2. 컨텍스트 — 너의 Round 1 비판이 어떻게 처리되었는지

team-lead가 cross_review.md에서 결정한 사항:

| Round 1 비판 | 처리 결정 | Round 2 반영 |
|------------|---------|-------------|
| C1 Chairmanship power (P0) | **즉시 채택** | (a) T01 collector가 COP29 Baku presidency letter, COP30 Belém presidency letter, SBI/SBSTA L-document 수집 (b) T02 refinement의 v1.3 스키마에 procedural_signals + chair_metadata 추가 (c) Stage 2 country_features에 chair_status 추가 — Round 3 시행 |
| C2 Paradigm balance (Realist B0 + Constructivist frame) | **즉시 채택** | (a) v1.3 스키마에 frame_type ∈ {scientific, justice, sovereignty, security, development} 추가 (b) Realist B0 평가는 Round 3 평가 protocol에 통합 |
| C3 Hypergraph complementary motif | 시사 채택 (Round 3 Stage 2 구현 시) | salience_score 추출은 v1.3에 포함. complementary motif detection 알고리즘은 Round 3 |

**team-lead의 정합성 평가**: 너의 권고는 헌법(논문감 + COP30 회고)과 가장 강하게 정합. 특히 C1은 **CINA가 자기 검증 사건의 인과 메커니즘을 변수로 가져야 한다**는 internal validity 문제를 정확히 짚었으며 P0로 격상됨.

## 3. P0 산출물

### 3.1 권고 반영 검증 (반드시)

`council_sessions/round_2/ir_political/verification.md` 작성:

- [ ] §"Chair-power 데이터 수집 검증 (C1)" — T01이 가져온 의장 letter·L-document가 충분한가?
  - COP29 Baku presidency letter (Yalçın Rafiyev)와 Baku to Belém Roadmap 수집 여부
  - COP30 Belém presidency letter (André Corrêa do Lago)와 presidency text 초안 노트 수집 여부
  - SBI/SBSTA L-document 시리즈에서 pen_holder 식별 가능성
  - 필요시 Round 3 collector에 추가 권고
- [ ] §"v1.3 스키마의 frame_type/salience/procedural 검증 (C2, C3)" — 정제 결과에서 변수가 의미 있게 추출되는가?
  - frame_type 분포: AOSIS는 justice frame? LMDC는 sovereignty frame? 가설 검증
  - salience_score: 이슈 간 비대칭성이 통계적으로 식별되는가
  - procedural_signals: 의장 발화의 procedural phrase가 자동 인식되는가
- [ ] §"Realist baseline B0 데이터 준비 검증" — Round 3 평가에서 GDP/CO2/military/alliance 데이터로 coalition 예측 baseline 가능 여부

### 3.2 심화 비판 (Round 2 corpus 기반)

신규 70-100건 corpus를 본 후 새 비판:
- [ ] §"Section 3 Power 분석 강화 권고의 실증 검증" — Round 1 §3.1-3.4의 4가지 권고가 데이터로 가능한가?
  - 3.1 브라질 dual-role: Mediator-score / Interest-score / Tension index 측정 가능성
  - 3.2 BASIC vs LMDC 결속 메커니즘: within-group stance variance 측정 가능성
  - 3.3 AOSIS norm entrepreneurship: frame diffusion lag 측정 가능성 (Castro 2025 utterance timeline 필요)
  - 3.4 US-China-EU triangle distance: 실증 가능성
- [ ] §"COP29→COP30 시계열 분석" — 만약 COP29 Baku 자료가 들어왔다면, GGA 협상의 시간적 진화(Bayesian update) 분석 가능성
- [ ] §"Round 1에서 제기하지 못한 새 비판" — 정제 결과를 본 후 발견한 추가 결함

### 3.3 Heedo 결정 사안에 대한 입장

- [ ] §"HEEDO-1 (Scope 확장) 입장" — 너는 Round 1에서 "이행은 별도 layer"라는 함의적 입장이었음. 이제 정책학자의 Implementation Gap 권고가 Heedo 결정 사안으로 격상됨. 다음에 답:
  - Q: scope 확장이 IR 분석의 internal validity에 영향을 주는가?
  - Q: 만약 양립한다면, IR layer(협상 그래프)와 Policy layer(이행 outcome)의 인터페이스는 어떻게 설계되어야 하는가?
  - Q: AOSIS의 norm entrepreneurship과 implementation realization은 어떤 관계인가? (norm cascade가 이행 압박을 만드는가)

## 4. P1 산출물

- [ ] §"Stage 2 R-GAT 추가 edge type 권고" — 너의 Round 1 C1 권고에서 `drafts_text(Country, Issue, t)` edge type 제안. Round 2 데이터로 이 edge가 실제로 생성 가능한지 점검
- [ ] §"Castro 2025 supplements 접근 상태" — Round 1 D5 결정 (학술 contact)에 대한 진행 상황 확인 (T01 best-effort 결과 기반)

## 5. Rubric 재평가 (Round 1 → Round 2)

| Dimension | Round 1 점수 | Round 2 점수 | 변화 근거 |
|-----------|-------------|-------------|----------|
| Theoretical grounding | 3.5/5 | ?/5 | (frame_type, procedural 변수 도입 후) |
| Methodological rigor | 3/5 | ?/5 | |
| Empirical validity | 2.5/5 | ?/5 | (corpus 70-100건 + chair 자료 후) |
| Policy/strategic relevance | 3.5/5 | ?/5 | |
| Clarity & reproducibility | 4/5 | ?/5 | |

목표: 평균 ≥ 4.0/5 (Round 1: 3.3/5).

## 6. 산출물 위치
- 메인 비평: `council_sessions/round_2/ir_political/critique.md`
- 권고 반영 검증: `council_sessions/round_2/ir_political/verification.md`
- (선택) Stage 2 R-GAT 권고: `council_sessions/round_2/ir_political/rgat_edge_proposal.md`

## 7. policy-science-professor와의 cross-review 예고
team-lead가 두 critique 모두 수령 후 합의·불일치 식별. 너의 입장이 정책학과 충돌할 가능성:
- HEEDO-1 (scope 확장) — 너는 협상 분석 중심, 정책학자는 이행 cycle 포함 (cross_review §3 D1)
- 노드 추가 우선순위 — 너의 P0 (chair/pen) vs 정책학의 P1 (subnational/NSA) (cross_review §3 D3)

특히 D1에서 너의 입장 명확화 필요. **권고**: scope 확장이 헌법 §1 논문감과 정합한다면 양립 채택을 IR 관점에서도 옹호할 수 있는 근거 제시 (e.g. Lipscy 2017, *Renegotiating the World Order*에서 implementation politics가 IR의 정당한 영역임을 시사).

## 8. 본 task의 헌법 정합성
- ✓ 헌법 §1 논문감: International Organization / Global Environmental Politics reviewer 기준에서 chair power 변수는 reject 사유 해소
- ✓ 헌법 §2 COP30 회고: chair power가 Belém Rube Goldberg 인과변수의 핵심
- ✓ 헌법 §3 투트랙: 외교부 협상단 audience(Track A)·논문 reviewer audience(Track B) 모두 강화
- ✓ 헌법 §4 LLM-GNN-LLM: Stage 1 procedural_signals + Stage 2 chair_status + drafts_text edge 가 파이프라인 신규성 강화

**작업은 T02 refinement (ir_pack_v2.md) 완료 후 시작.**
