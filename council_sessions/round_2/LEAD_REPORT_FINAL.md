# Round 2 — Team-Lead Final Report

**To**: Heedo (zxsa0716@kookmin.ac.kr) | **From**: team-lead | **Date**: 2026-04-25 | **Round**: 2 (closing)

---

## 한 줄 요약 (30 words)

Round 2 종결 권고. Round 1 권고가 evidence를 산출(GGA-IND Authority 6.1, chair 17건, indicator 149개), 두 교수 평점 +0.80(combined 3.05→3.85). G4·G5 PASS, G1·G2·G3 partial, Round 3 P0 8건 발급.

---

## 이번 라운드 핵심 발견 (5)

1. **Empirical 도약** — 두 교수 모두 Empirical validity +1.0 이상 상향 (Policy 2→4, IR 2.5→3.5). Round 1 fatal gap (UNFCCC 0건)이 가장 큰 자산으로 전환됨 — Belém Package L.24/L.25/L.25E + UAE-Belém 9a-e + chair_metadata 17건 + NDC 39건 + indicator 149개.

2. **Authority 6.1 의 multi-theoretical convergence** — GGA-IND Authority 평균 6.1(6 이슈 중 최저)이 두 교수의 인과 사슬을 동시에 지지: 정책학(Howlett 2019 instrument calibration의 soft-law 흔적) + IR(L.25 `is_pen_holder=True` + frame_type sovereignty의 브라질 dual-role 봉인). CINA가 multi-theoretical triangulation 도구로 작동함을 입증한 첫 사례.

3. **두 교수 공통 reject risk 4건 (모두 Round 3 P0로 매핑)**:
   - chair_metadata N=17 → 인과 추론 불가 (CR3.1)
   - frame_type justice/development 0건 → AOSIS·LDC norm entrepreneurship invisible (CR3.4)
   - 149 indicator 중 31% PDF 목차 노이즈 → Krippendorff unit definition 위반 (CR3.3)
   - Stage 1 LLM 미가동, 모든 점수 규칙 기반 → CINA 헌법 §4 partial (CR3.6)

4. **Round 3 Phase A 11건 PDF 사전 확보** — AOSIS 6 (FCCC/SBI/2025/17 + Climate Champions + MAHWP3 + SB60 opening + adaptation submission + SCF needs survey), LMDC 2 (GGA submission + supplementary 9.1 DEA), Brazilian Plano Clima 3 (13MB), World Bank Brazil CCDR 1 (3.9MB). CR3.4(justice frame)와 Task E(브라질 적응 이행 ground truth)의 evidence base 미리 확보.

5. **헌법 정합성 4/4** (단 §4는 partial — Stage 1 LLM 미가동) — Round 3 CR3.6이 §4 PASS의 임계 task.

---

## 5 Quality Gates 최종 평가

| Gate | Round 1 | Round 2 | Round 3 목표 | 상태 |
|------|--------:|--------:|-----------:|------|
| **G1 Coverage** | 0.18 (FAIL) | **0.62** | 0.91 | partial_pass (manifest 102/165, source 다양성 8개, schema_pass 95.2%) |
| **G2 Evidence Grounding** | 0.60 (PARTIAL) | **0.84** | 0.92 | partial_pass (87 docs paragraph-level + 149 indicator + 17 chair source-traceable; 31% noise 차감) |
| **G3 Theory Grounding** | 0.65 (PARTIAL) | **0.78** | 0.85 | partial_pass (두 교수 평균 4.0/5; MLG 미흡수, ACF 미매핑) |
| **G4 Dual Review** | 0.61 (PARTIAL) | **0.77** | 0.82 | **PASS** (target 0.60 wide margin clear; 두 교수 모두 ≥3.5; R&R minor revision 진입) |
| **G5 Heedo Alignment** | 1.00 (PASS) | **1.00** | 1.00 | **PASS** (4 directives 모두 정합) |

**판정**: **approved with Round 3 P0 remediation**. G4·G5 PASS, G1-G3 partial_pass with clear remediation paths.

---

## 다음 라운드 방향 (Round 3 Phase B + 후속)

### 방향 1 — 표본 확대 + 인과 설계
- **T01 (collector)**: COP21~COP29 11개 historical presidency letters → chair_metadata N≥67 (목표 150). Realist baseline 4 dataset (WB GDP + OWID CO2 + SIPRI MILEX + COW alliances) → Stage 2 GNN 학습 unblock. 한국 MOE 제3차 적응대책 PDF Playwright 보강. 비국가 행위자 5-10건 (COICA/APIB/ITUC) JT-ADAPT 한정.

### 방향 2 — 측정 정밀화
- **T02 (refinement)**: 149 indicator → `kind` 분화 (indicator/toc/header/metadata) → 진짜 indicator 약 100건. NATO 4축 discriminating keyword + TF-IDF 가중. frame_type rhetorical signature 키워드 확장 (Stage 1 prompt v1.4 — equity, CBDR-RC, 1.5-to-stay-alive 등). Stage 1 LLM ready 상태.

### 방향 3 — 헌법 정합성 + Track A 가속
- **T03 (policy-sci)**: Task E (IRR) 메트릭 헌법 합의 검토. KEI 모니터링 보고서 cross-walk (5×6 matrix). 비국가 행위자 평가 모듈 (Hooghe-Marks Type II).
- **T04 (ir-political)**: chair_metadata N≥67 후 Tallberg 4채널 분류 + counterfactual 검증 (비-BASIC 의장 baseline). frame_type 5범주 모두 활성화 검증. Stage 2 R-GAT drafts_text edge 학습 준비도 평가.

---

## Heedo 결정 필요 사안 (3건)

### H-R3-1 (P0, before T03 launch). Task E (IRR) 메트릭 헌법 합의

Policy-Sci §4 권고: `IRR_i,t = (Σ W_k × Realized_k) / (Σ W_k × Promised_k)` 공식이 CINA 4번째 평가 task로 공식 채택될 것인가.

- **(A) 채택 [team-lead 추천]** — docs/07에 §5 신설. Round 3에서 OECD CRS + NDC Registry + KEI 데이터 수집. 정책학 저널 투고 정당화. Round 4-5에서 평가 가동.
- (B) 부분 채택 (Track A 한정).
- (C) 거부 (정책학 저널 약화).

### H-R3-2 (P0, before T01 launch). 비국가 행위자 노드 채택 범위

Policy-Sci C2 권고: JT-ADAPT 한정 5-10개 비국가 행위자 노드 시범 도입.

- **(A) 채택 (JT-ADAPT 한정) [team-lead 추천]** — COICA, APIB, ITUC, IIPFCC 5-7 노드. R-GAT heterogeneous node type 추가. IPCC AR6 WGII Ch.18 정당성 조건 부합.
- (B) 거부.
- (C) Round 4 연기.

### H-R3-3 (P0, end of Round 3). Stage 1 LLM 활성화 (Round 4 P0)

Round 3 종료 시점에서 prep 완료 후 Stage 1 LLM 첫 추출 (~$10/trial, 5건 highest-priority docs).

- **(A) 사전 승인 [team-lead 추천]** — Round 3 prep 완료 검증 후 자동 진행. ANTHROPIC_API_KEY + prompt v1.4 + seed 기록 인프라.
- (B) Round 3 종료 후 결정.

**보조 결정** (자동 진행):
- HEEDO-6 KEI Working Paper 수집 — 공개 보고서 → 자동 accept
- HEEDO-7 Castro 2025 supp. academic email — Heedo 학교 이메일 발송 권고

---

## 비용·시간 (Round 2 cumulative)

| 항목 | 값 |
|------|---|
| LLM 호출 | ~3 (data-refinement-analyst sonnet 1 + policy-prof opus 1 + ir-prof opus 1) |
| 비용 추정 | ~$8-12 (sonnet + 2× opus critique) |
| 라운드 소요 시간 | ~6시간 (Phase A 인프라 90분 + Phase B 정제 90분 + 두 교수 critique 90분 + synthesis 90분) |
| 누적 LLM 호출 (R0+R1+R2) | ~16 |
| 누적 비용 | ~$20-26 |
| 누적 storage | ~500 MB raw + ~22 MB processed |
| 누적 manifest | 102 entries |

---

## 산출물 인벤토리 (Round 2)

### 데이터
- `data/manifest/manifest.jsonl` — 102 entries (Round 1: 7, Round 2 Phase A: +84, Phase B 추가: +11)
- `data/processed/documents.jsonl` — 87 records (schema v1.3)
- `data/processed/uae_belem_indicators.jsonl` — 149 records (9a:41, 9b:46, 9c:54, 9e:8 — 31% noise 추정)
- `data/processed/ndc_adaptation_sections.jsonl` — 39 records (39/53 = 73.6% 검출)
- `data/processed/chair_metadata.jsonl` — 17 records (Tallberg formula 4 + agenda-shaping 2 + brokerage 3)
- `data/processed/extraction_targets.jsonl` — 298 records
- `data/processed/refinement_round2_stats.json` — 처리 통계 + topic_distribution + frame_distribution + instrument_totals
- `data/processed/country_issue_matrix.csv` — 국가×이슈 사전 매트릭스

### Round 3 Phase A 사전 수집 (data/raw/round3/)
- `AOSIS_GGA_submission/` — 6 PDFs (FCCC/SBI/2025/17 + 5 supplementary)
- `LMDC_AILAC_submission/` — 2 PDFs (GGA submission + 9.1 DEA)
- `Brazilian_Plano_Clima/` — 3 PDFs (13MB total)
- `WorldBank_CCDR/` — 1 PDF (3.9MB)
- `Korean_MOE_adapt_plan/` — 1 HTML (PDF Round 4 보강 필요)

### 협의체 산출물
- `council_sessions/round_2/refinement/REPORT.md`
- `council_sessions/round_2/refinement/collector_feedback_round2.md` (7 gaps for collector)
- `council_sessions/round_2/refinement/professor_input/policy_sci_pack_round2.md`
- `council_sessions/round_2/refinement/professor_input/ir_pack_round2.md`
- `council_sessions/round_2/policy_science/critique.md` (Rubric 3.8/5)
- `council_sessions/round_2/ir_political/critique.md` (Rubric 3.9/5)
- `council_sessions/round_2/synthesis/cross_review.md`
- `council_sessions/round_2/synthesis/quality_gates.json`
- `council_sessions/round_2/LEAD_REPORT_FINAL.md` (이 문서)

### Round 3 Tasks 발급 (council_sessions/round_3/tasks/)
- `T01_collector_task.md` — historical chair (CR3.1) + realist baseline (CR3.5) + 한국 MOE (CR3.7) + 비국가 행위자 (CR3.5/CR3.7)
- `T02_refinement_task.md` — kind 분화 (CR3.3) + frame justice/dev 재추출 (CR3.4) + TF-IDF 가중 (CR3.6) + Stage 1 prompt v1.4 prep
- `T03_policy_prof_task.md` — Task E (IRR) 메트릭 (CR3.8) + 비국가 행위자 평가 + Round 3 정제 검증
- `T04_ir_prof_task.md` — chair N≥67 후 Tallberg 4채널 검증 + frame 5범주 활성 + Stage 2 R-GAT 준비도

---

## Convergence Tracker

| 라운드 | 새 gap | 누적 closed | 헌법 정합 | 수렴 카운터 |
|------|------:|----------:|---------|----------:|
| Round 0 | - | - | 100% | - |
| Round 1 | 11 | 0 | 100% | 0/3 |
| Round 2 | **8** | 5 (Round 1 P0 권고 모두 evidence 산출) | 75% (§4 partial) | **0/3** |
| Round 3 (예상) | 4-6 | +6 (CR3.1~CR3.6) | 100% (CR3.6 §4 회복) | 0/3 또는 1/3 |

**예상 수렴 시점**: Round 5-6 (chair N≥150 + Stage 1 LLM 활성화 + Stage 2 GAT 학습 후).

---

## team-lead 종합 진단

Round 2는 **방법론적 도약 라운드**다. Round 1의 정성적 골격(NATO 4축, procedural_signals, frame_type, salience_score)이 80건 신규 정제로 처음 정량 evidence를 산출했고, 두 교수가 동일한 인과 사슬(브라질 pen-holder → voluntary 언어 → sovereignty frame 고착)을 GGA-IND Authority 6.1 + L.25 sovereignty frame로 동시 지지했다. 이는 CINA가 multi-theoretical triangulation 도구로 작동함을 첫 입증한 결과로, NeurIPS CCAI / GEC 투고 시 차별화 지점이다.

그러나 두 교수는 동일한 4가지 reject risk를 지적했다 — sample size 부족, frame 측정 실패, indicator 노이즈, LLM 미가동. Round 3는 이 4가지 + Realist baseline + Task E + 비국가 행위자 노드를 8 P0 task로 처리한다. Round 3 Phase A 11건 PDF가 이미 도착해 있으므로 collector 작업의 50%가 사전 완료된 셈이다.

Heedo의 즉시 결정 3건(H-R3-1 Task E, H-R3-2 비국가 행위자, H-R3-3 Stage 1 LLM)은 모두 헌법과 정합되며 (A) 옵션 채택을 추천한다. Round 2는 **공식 종결 권고** — Round 3 진입 시 active_tasks를 T01-T04 Round 3로 갱신, current_round를 3으로 update.

---

*— team-lead, 2026-04-25T10:00:00Z, Round 2 closure final*
