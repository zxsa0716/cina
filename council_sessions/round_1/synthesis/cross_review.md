---
agent: team-lead
round: 1
date: 2026-04-25
status: round_1_closing_synthesis
inputs:
  - council_sessions/round_1/data_collection/REPORT.md
  - council_sessions/round_1/refinement/collector_feedback.md
  - council_sessions/round_1/refinement/professor_input/policy_sci_pack.md
  - council_sessions/round_1/refinement/professor_input/ir_pack.md
  - council_sessions/round_1/policy_science/critique.md
  - council_sessions/round_1/ir_political/critique.md
---

# Round 1 — Cross-Review Synthesis (Team-Lead)

두 교수 critique과 두 데이터 에이전트의 산출물을 종합하여, 합의 지점·결정적 비판·처리 결정을 정리한다.

---

## 1. Two-Professor Rubric 비교

| Dimension | Policy-Sci | IR-Political | Mean | Δ | 비고 |
|-----------|-----------|--------------|------|---|------|
| Theoretical grounding | 3.0 | 3.5 | 3.25 | 0.5 | 정책학 코어 부재(정책학자) vs IR canon 충실하나 paradigm balance 결여(IR) — 두 비판이 상호보완 |
| Methodological rigor | 3.0 | 3.0 | 3.00 | 0.0 | 두 교수 모두 "구조는 합리적이나 식별/이행 메소드 부재"로 일치 |
| Empirical validity | 2.0 | 2.5 | 2.25 | 0.5 | UNFCCC/NDC/ENB 0건이라는 Round 1 결정적 fail에 두 교수 모두 동의 |
| Policy/strategic relevance | 2.0 | 3.5 | 2.75 | 1.5 | **최대 불일치**. 정책학자는 한국 부처 적용성 결함을 강하게, IR은 외교실무 부합 평가. 같은 docs/09를 다른 audience 시각에서 읽음 |
| Clarity & reproducibility | 4.0 | 4.0 | 4.00 | 0.0 | 두 교수 모두 인프라·표준은 합격선 |

**평균**: Policy-Sci 2.8 / IR 3.3 → **두 교수 합산 평균 3.05/5**, 두 교수 모두 ≥ 3.0 미달이거나 경계선이지만 IR은 통과, Policy-Sci는 2.8로 경계 미달. → **G4 Dual Review는 partial pass** (다음 절 참조).

---

## 2. 합의 지점 (high confidence agreement)

| # | 합의 항목 | Policy-Sci 인용 | IR 인용 | 처리 |
|---|----------|---------------|---------|------|
| A1 | Round 1 Empirical fail (UNFCCC/NDC/ENB 0건) | §Section 2 C-empirical, "정책 분석의 1차 사료가 부재한 상태" | §Section 1 Empirical 2.5, "Round 2 Playwright 도입 전엔 empirical claim 일체 보류" | **Round 2 P0**: Playwright 도입 강행 |
| A2 | Reproducibility/표준은 합격선 | §1 Rubric 4/5 | §1 Rubric 4/5 | 유지. 추가 작업 불필요 |
| A3 | COP30 회고 검증 framing 자체는 타당 | §총평 함의적 | §Section 4 합의예상 1번 | 유지. CINA 헌법 변경 불필요 |
| A4 | 의장국 브라질 + Belém Indicators 사례선택 정당 | §총평 (간접) | §Section 4 합의예상 4번 | 유지 |
| A5 | Castro 2025 데이터의 ground truth 활용 | §3 한국 정책학 §3.3 (간접 인정) | §Section 4 합의예상 (단, ENB editor framing bias 단서) | Round 2/3에서 calibration 시 활용. 단서 기록 |
| A6 | 4-task 평가 protocol에 dependent variable 추가 필요 | C3 Implementation Realization Rate (Task E) | Section 3.1 dual-role tension index 측정 | Round 3에서 통합 평가 protocol 재설계 |

---

## 3. 불일치 지점 (productive disagreement)

| # | 쟁점 | Policy-Sci 입장 | IR 입장 | 결정 |
|---|------|----------------|--------|------|
| D1 | **CINA scope** | 정책 cycle 전체 (합의→이행 t+24m)로 확장. Implementation Gap을 평가 변수로. | 협상 그래프 모델링 자체 강화 (chair power, frame, salience). 이행은 별도 layer. | **양립 (Round 2부터 양 layer 병기 시작)**. Heedo 헌법 (논문감 + COP30 회고)과 정합. 단 데이터 부담 조기 평가 필요. → 헌법 §scope 확장 권고를 Heedo에 에스컬레이션 |
| D2 | **AOSIS 모델링** | 취약성 지표(ND-GAIN)로 vulnerability metric | norm entrepreneurship × moral authority × frame diffusion | **양 변수 병기** (별개 노드 피처). 후속 ablation에서 incremental validity 측정. IR이 정책학에 양보 권고 (단일화 거부) |
| D3 | **노드 추가 우선순위** | Subnational(브라질 9개 Amazon 주, 한국 광역시도)·NonStateActor(원주민·NGO) P1 | Country-Group 단위 강화 (chair_status, pen_holder)가 P0 | **시퀀싱**: Round 2에 IR의 P0(chair/pen) 먼저 → Round 3에 정책학의 P1(subnational/NSA) 검토. 데이터 부담 분산 |
| D4 | **Belém Rube Goldberg 해석** | KPI proliferation, policy design failure | Chairmanship procedural power × epistemic-political tension | **둘 다 채택**. CINA가 두 메커니즘 모두 회고적으로 식별 가능해야 함. Stage 2 motif 분석에서 명시적 hypothesis 두 개 |
| D5 | **브리핑 audience** | 부처 실무 (한국 외교부·환경부 cross-walk) | 외교부 협상단 (red line, leverage) | **deliverables/ 트랙은 정책학, docs/ 트랙은 IR**. Track A(수업)·Track B(논문) 분리가 이를 자연스럽게 해소 |

---

## 4. 결정적 비판 (Critical findings, must-act)

각 비판에 대한 처리 결정. team-lead가 단독 처리할 사안은 [T-LEAD], Heedo 결정 필요는 [HEEDO].

### CR1. [T-LEAD] **Stage 1 추출 스키마 확장 — instrument_signals + frame_type + salience_score**

- **출처**: Policy-Sci C2 (NATO 4축), IR C2 (frame_type), IR C3 (salience asymmetry).
- **결정**: **양 교수 권고를 통합한 v1.3 prompt 스키마** Round 2에서 시행.
  - 추가 필드:
    1. `instrument_signals: {nodality, authority, treasure, organization}` (각 0-1 score + evidence quote) — 정책학자
    2. `frame_type ∈ {scientific, justice, sovereignty, security, development}` — IR 교수
    3. `salience_score ∈ [0, 1]` — IR 교수 (issue linkage)
  - 기존 스키마 유지: `key_demands, red_lines, flexibility_signals, coalition_alignment`
- **비용**: Stage 1 prompt token ~30% 증가 → Round 2 추출 LLM 호출 비용 +20-30%.
- **처리 위치**: Round 2 T02 refinement task에 prompt v1.3 명세 포함.

### CR2. [T-LEAD] **country_features에 chair_status + procedural variables 추가**

- **출처**: IR C1 (P0).
- **결정**: **즉시 채택**. CINA가 자기 검증 사건(Belém Rube Goldberg)의 인과 메커니즘을 변수로 갖지 못하는 것은 internal validity 결함.
  - 추가 변수:
    1. `chair_status ∈ {0=일반, 1=incoming, 2=current, 3=outgoing troika}`
    2. `pen_holder_country_id` (issue_features) — 각 이슈별 텍스트 초안권 보유국
    3. R-GAT edge type `drafts_text(Country, Issue, t)` 신설
- **데이터 요구**: COP29 Baku 의장단 letter, COP30 Belém presidency letter, SBI/SBSTA L-document(의장 초안)
- **처리 위치**: Round 2 T01 collector (의장 letter·L-doc 수집), T02 refinement (스키마 반영), `docs/05` 업데이트는 Round 3.

### CR3. [HEEDO] **CINA scope 확장 결정 — 정책 cycle 이행까지 포함할 것인가**

- **출처**: Policy-Sci C3 (Implementation Realization Rate, Task E 신설).
- **결정안**: **권고: 양립 채택**. 이유:
  1. Heedo 헌법 "논문감 수준"과 정합. *Global Environmental Change* reviewer가 implementation gap 부재 시 reject 가능성 있음.
  2. Track A 수업 브리핑은 본질적으로 한국 부처 이행을 다루므로 정책학 변수가 deliverable에 직접 기여.
- **trade-off**: 데이터 수집 부담 +40% (NDC 갱신, 국내 법령, 예산 편성 outcome edge). Round 4 마감과 충돌 가능.
- **처리 위치**: Round 2 LEAD_REPORT에서 Heedo 결정 요청. 결정 시 Round 3에서 평가 Task E 정식 추가.

### CR4. [T-LEAD] **Realist baseline B0 추가 (incremental validity check)**

- **출처**: IR C2.
- **결정**: 채택 (low cost). GDP/CO2 데이터 이미 인프라에 존재.
- **처리 위치**: Round 3 평가 protocol 재설계 시. Round 2에서는 데이터만 준비.

### CR5. [T-LEAD] **데이터 에이전트 피드백 통합**

데이터 에이전트의 collector_feedback.md(5 Gap)와 두 교수의 권고를 통합하여 Round 2 T01 수집 매트릭스 발급:

| 우선순위 | 출처 | 항목 | Round 2 수집 목표 |
|---------|------|------|-----------------|
| Critical | Refinement Gap1 + IR C1 | 각국 UNFCCC submission + 의장 letter + L-document | 30-40건 |
| Critical | Refinement Gap2 | COP29 (Baku) GGA SBI61/SBSTA61 문서 | 10-15건 |
| High | Refinement Gap3 + IR Section 3 | IISD ENB COP30 일일 요약 + utterance timeline | 15-20건 |
| High | Policy-Sci 한국 §3 | 한국 정부 NAP·NDC·외교부 추진전략 문서 | 5-10건 |
| Medium | Refinement Gap4 | LMDC/SAU 직접 발언 | 5-10건 |
| Medium | Refinement Gap5 | NDC 적응 섹션 (BRA, EU, CHN, IND, AOSIS 대표국) | 5건 |

**총 목표: 70-100건** → Stage 1 LLM 추출 가동 + Stage 2 그래프 학습 충족 임계.

---

## 5. 두 교수의 권고 vs Heedo 헌법 정합성 검토

| 권고 | 헌법 §1 논문감 | 헌법 §2 COP30 회고 | 헌법 §3 투트랙 | 헌법 §4 LLM-GNN-LLM | 결론 |
|------|--------------|-------------------|---------------|-------------------|------|
| Policy-Sci scope 확장 (이행 cycle) | ✓ 강화 | △ 직접 영향 없음 | ✓ Track A 강화 | ✓ Stage 3 출력에 새 차원 | **채택 권고 (Heedo 결정)** |
| Policy-Sci NATO 4축 (instrument_signals) | ✓ 강화 | ✓ 회고 정확도 향상 | ✓ 양 트랙 | ✓ Stage 1 enrich | **즉시 채택** |
| Policy-Sci MLG 노드 (subnational/NSA) | ✓ 강화 | △ 데이터 부담 | △ Track A 보너스 | ✓ Stage 2 enrich | **Round 3 검토** |
| IR chair_status + pen_holder | ✓ 강화 | ✓✓ 핵심 사건 인과변수 | ✓ 양 트랙 | ✓ Stage 2 핵심 | **즉시 채택 (P0)** |
| IR realist baseline B0 | ✓ 강화 (rigour) | ✓ ablation에 필요 | ✓ | ✓ 평가 단계 | **즉시 채택** |
| IR frame_type | ✓ 강화 | ✓ AOSIS 정량화 | ✓ | ✓ Stage 1 enrich | **즉시 채택** |

→ **모든 즉시·핵심 권고가 헌법과 정합**. 정합 불일치 없음. Heedo 결정 필요는 D1 (scope 확장) 한 건.

---

## 6. 데이터 에이전트 피드백 (Round 2 collector·refinement에 전달)

### 6.1 To: policy-data-collector (Round 2)

**P0 작업** (반드시 Round 2 종료 전):
1. **Playwright 도입** — `requirements.txt: playwright>=1.45`, `pyproject.toml` 의존성 추가, `python -m playwright install chromium`. UNFCCC/NDC/ENB 동적 페이지 우회.
2. **수집 매트릭스 (위 §4 CR5 표)** 80건 목표.
3. **두 교수 권고 신규 자료**:
   - COP29 Baku presidency letter (의장단 letter, "Baku to Belém Roadmap" 포함)
   - COP30 Belém presidency letter (브라질 의장 6월 letter, presidency text 초안 노트)
   - SBI62/SBSTA62 L-document 시리즈 (의장 텍스트 초안권 추적)
   - NDC 적응 섹션 (BRA, EU, CHN, IND, AOSIS 대표국 — 5건)
4. **Castro 2025 supplements** — DOI page 재분석 또는 figshare 직접 검색.
5. **한국 부처 자료** — gov.kr 외교부/환경부 NAP·NDC, KEI 보고서.

**P1 작업** (가능한 만큼):
6. ENB Volume 12 brute force (`enb12880e` ~ `enb12895e`) — CC BY-NC-SA 명시.
7. AOSIS, LDC, AILAC 그룹 statement 검색.

**산출물 형식**:
- `data/manifest/manifest.jsonl` 추가 항목 (sha256, license, 메타 100% 유지)
- `council_sessions/round_2/data_collection/REPORT.md` (T01 결과)
- `data/runs/collect_*` summary

### 6.2 To: data-refinement-analyst (Round 2)

**P0 작업**:
1. **Stage 1 추출 스키마 v1.3 구현** — Round 1 v1.2 + 신규 필드 3종:
   - `instrument_signals: {nodality, authority, treasure, organization}` (Policy-Sci)
   - `frame_type ∈ {scientific, justice, sovereignty, security, development}` (IR)
   - `salience_score ∈ [0, 1]` (IR)
2. **chair-status 자동 인식** — 문서 메타에서 의장국·co-facilitator·pen-holder 식별 로직.
3. Round 2 collector가 가져온 70-100건 raw → CINA Document Schema 변환.
4. 정제 결과를 두 교수 input pack(`policy_sci_pack_v2.md`, `ir_pack_v2.md`)에 반영.

**P1 작업**:
5. Round 1 정제 결과(7건)에 대한 v1.3 스키마 backfill (overhead 적음).

---

## 7. team-lead 결정 sheet (요약)

| 결정 ID | 항목 | 결정자 | 결정 |
|--------|------|-------|------|
| T-LEAD-1 | Stage 1 prompt v1.3 (instrument + frame + salience) | team-lead | **채택**. Round 2 적용 |
| T-LEAD-2 | chair_status / pen_holder / drafts_text | team-lead | **채택**. Round 2 데이터 수집 + 스키마 반영 |
| T-LEAD-3 | Realist baseline B0 | team-lead | **채택**. Round 3 평가 통합 |
| T-LEAD-4 | AOSIS 변수 병기 (vulnerability + norm-entrepreneurship) | team-lead | **채택** |
| T-LEAD-5 | 노드 추가 시퀀싱 (chair P0 R2, subnational/NSA P1 R3) | team-lead | **채택** |
| HEEDO-1 | CINA scope 확장 (이행 cycle 포함, Task E 신설) | Heedo | **권고: 채택. R2 LEAD_REPORT에서 결정 요청** |
| HEEDO-2 | Playwright 도입 200MB binary 승인 | Heedo | **권고: 채택. 사실상 필수** |
| HEEDO-3 | IISD ENB 학술 contact email 발송 | Heedo | **권고: 채택. 학교 이메일로 사전 통지** |

---

## 8. 종합 — Round 1 종료 권고

- **두 교수 비판은 헌법과 정합한 enrichment**. 어느 권고도 CINA의 핵심(LLM-GNN-LLM, 회고 검증, 투트랙)과 충돌하지 않는다.
- **Round 1은 인프라 + 첫 수집 + 첫 비판**의 라운드로 완수. 결정적 fail은 G1 Empirical (0.18)만, 이는 동적 사이트 차단점이라는 명확한 원인이 있고 Round 2에서 해소 가능.
- **Round 2 진입 권고**: Playwright 도입 + 수집 매트릭스 + 스키마 v1.3 + 의장 power 변수.

**문서 끝**
