---
agent: team-lead
round: 2
phase: synthesis
date: 2026-04-25
inputs:
  - council_sessions/round_2/policy_science/critique.md
  - council_sessions/round_2/ir_political/critique.md
  - data/processed/refinement_round2_stats.json (instrument_totals, frame_distribution, group_frequency)
  - data/manifest/manifest.jsonl (102 entries)
  - data/processed/{documents.jsonl 87, uae_belem_indicators.jsonl 149, ndc_adaptation_sections.jsonl 39, chair_metadata.jsonl 17, extraction_targets.jsonl 298}
  - council_sessions/round_1/synthesis/cross_review.md (anchor)
constitution_anchor: CINA_FRAMEWORK.md §1-§3 + Heedo 4 directives
---

# Round 2 — 두 교수 critique cross-review

## 0. 한 단락 종합

Round 1 권고 3건(NATO 4축 instrument_signals, frame_type 5분류, chair_status edge)이 Round 2에서 모두 schema v1.3로 hard-wire 되어 80건 신규 corpus·149 indicator·17 chair record·39 NDC 적응 섹션을 산출했고, **두 교수 모두 평점을 동시에 끌어올렸다(Policy 2.8→3.8, IR 3.3→3.9, combined 3.05→3.85)**. 가장 결정적 진전은 두 학파 모두 Empirical validity 차원에서 +1.0 이상 도약했다는 사실이다 — Round 1이 "데이터 0건 fail"로 끝났다면, Round 2는 1차 사료 17건 이상 확보 + Authority 6.1·sovereignty 5건의 정량 분포로 두 학파의 가설을 자체 입증할 수 있는 단계로 올라섰다. 그러나 두 교수가 **공통으로 지적한 결정적 한계 3건(C-shared)** 이 남아있다: (a) **샘플 사이즈 부족** — chair_metadata 17건은 인과 추론에 부족, 149 indicator 31% 노이즈 오염, (b) **discriminating power 부족** — NATO 4축 Nodality 표준편차 0.36, frame_type justice/development 0건, (c) **counterfactual 부재** — 비-BASIC 의장 baseline 없음. Round 3는 이 3개를 모두 잡아야 하며, 동시에 Heedo 헌법 4조항을 침해하지 않는다. 본 cross-review는 합의 5건 / 생산적 불일치 4건 / 처리 결정 8건을 명시한다.

---

## 1. 합의 (Convergent findings)

### A1 — Round 1 권고가 evidence를 자동 산출했음 (양 교수 공통)
- **Policy §1.1**: "Authority 414, Nodality 대비 70% — 적응 협상의 본질적 soft-law 성격을 NATO 4축이 식별. Howlett(2019) p.114 instrument calibration 가설 정합."
- **IR §1.1**: "Tallberg 4 채널 중 (ii) formula control 4건 + (iv) agenda-shaping 2건이 procedural_phrases 텍스트 패턴으로 자동 식별. UNFCCC 결정문 장르 규범의 학습이라는 점에서 reviewer 인정 가능."
- **합의 본질**: Round 1에서 두 교수가 권고한 schema 변형이 단순 "필드 추가"가 아니라 **이론적 가설을 텍스트 분포로 변환**시켰다. 이는 CINA의 LLM-GNN-LLM 파이프라인이 *이론 → 변수 → 데이터*의 정합 사슬을 갖추기 시작했다는 결정적 신호.

### A2 — Empirical validity 도약 (양 교수 공통, +1.0 이상)
- Policy: 2/5 → 4/5 (+2.0)
- IR: 2.5/5 → 3.5/5 (+1.0)
- 도약의 공동 근거: (i) UNFCCC curated 20건 (Belém Package L.24/L.25/L.25E + UAE-Belém 9a-e + Mutirao Decision + OECD/C2ES 분석), (ii) chair_metadata 17건, (iii) NDC 적응 섹션 39건, (iv) UAE-Belém indicators 149건. **Round 1의 fatal gap(0건)이 Round 2의 가장 큰 자산이 됨**.

### A3 — 샘플 사이즈가 인과 추론에 부족 (C-shared 1)
- **IR §3 C2.1**: "N=17 chair records로는 chairman power 4 채널 식별 불가. Bayer & Urpelainen 2013 ISQ는 N>100. R-GAT edge type sample 17은 attention overfitting 거의 확실."
- **Policy §1.2**: "6.1이 인과 메커니즘인지 단순 상관 패턴인지 불분명. counterfactual 부재."
- **합의**: 양 교수 모두 chair_metadata N=17이 "case study 수준"이지 "quantitative inference 수준"이 아니라고 진단. **Round 3에서 COP21~COP29 historical presidency letters/L-document 추가 수집 → 목표 N≥150**.

### A4 — Discriminating power 부족 (C-shared 2)
- **Policy §3 C3**: "Nodality 표준편차 0.36 — 6 이슈 전반에서 좁은 대역. 'report'·'data'·'information' 키워드가 거의 모든 UNFCCC 문서에서 매칭. 변별력 부족 시 정책수단 차이 주장이 통계적으로 약함."
- **IR §3 C2.2**: "frame_type justice 0건, development 0건. AOSIS의 norm entrepreneurship과 LDC의 historical-responsibility frame이 invisible. CINA가 IR 핵심 메커니즘을 측정하지 못한다는 reject 사유."
- **합의**: 양 교수 모두 키워드 사전이 너무 광범위하거나 너무 협소하여 **이론적 카테고리가 분포로 분리되지 못함**을 지적. **Round 3에서 (i) NATO 4축 discriminating keyword + TF-IDF 가중, (ii) frame_type rhetorical signature 키워드 확장, (iii) Stage 1 LLM 추출 활성화**.

### A5 — 149 indicator 노이즈 정제 필요 (C-shared 3)
- **Policy §3 C1**: "uae_belem_indicators.jsonl seq 1~13 (target 9a Water)이 'Introduction', 'Progress as of...', 'Definition of indicator types' 등 PDF 목차 텍스트. 41건 중 최소 13건 목차 추정 (31%). Krippendorff 2019 §11 unit definition 위반."
- **IR §1.1 / §7 합의 예상**: "정책학자도 reviewer 관점에서 동일 우려." (IR critique §7에서 명시 합의)
- **합의**: 두 교수 모두 reviewer가 즉시 발견할 결함으로 인정. **Round 3에서 `kind` 필드 분화(`indicator | toc | header | metadata`) + seq<14 또는 줄임표 패턴 자동 라벨링**.

---

## 2. 생산적 불일치 (Divergent emphases)

### D1 (Round 1 D1 재발) — Scope 확장 (협상 vs 이행)
- **Policy 입장**: Authority 6.1 = 이행 위험. Task E 없으면 CINA는 "협상 분석기"이지 "정책 도구"가 아님. *Global Environmental Change* 또는 *Climate Policy* 정책학 저널 reviewer는 "그래서 이행은?"을 반드시 묻는다.
- **IR 입장**: 양립 채택 옹호. Lipscy(2017) *Renegotiating the World Order* + Drezner(2007) *All Politics is Global*은 implementation politics가 IR의 정당한 영역임을 명시. **단 IR layer와 Policy layer를 분리 가능한 sub-graph로 설계 + ablation 가능 조건**.
- **처리**: Heedo가 Round 1 후 HEEDO-1로 이미 accept함 (state.json 참조). Round 2 closure 시점에서 재논의 불필요. **Task E (Implementation Realization Rate)**는 Round 4-5에서 본격 가동. Round 3는 Task E 평가 메트릭의 정밀화와 OECD CRS·NDC Registry 데이터 수집 시작에 집중.

### D2 — 정밀화 vs 확장 우선순위
- **Policy 입장(C3 강조)**: NATO 4축 키워드 사전 정밀화 + Stage 1 LLM 추출이 P0. 4축이 변별력 없으면 어떤 corpus 확장도 의미 없음.
- **IR 입장(C2.1 강조)**: chair_metadata N=17→150 historical 확장이 P0. counterfactual 없이는 어떤 정밀화도 인과 주장에 못 도달.
- **처리**: **양립 채택, Round 3에서 동시 진행**. T01 (collector)는 IR 권고대로 historical presidency letters 수집, T02 (refinement)는 Policy 권고대로 키워드 사전 정밀화 + Stage 1 LLM ready 상태. 두 작업은 독립적 — 동시 가능. 우선순위 충돌 없음.

### D3 — 149 indicator의 분석 단위
- **Policy 입장**: indicator-level (지표 채택률, KPI proliferation, design quality)
- **IR 입장**: indicator 협상의 procedural choice (누가 어떤 지표를 거부했는가, agenda control 흔적)
- **처리**: **양립 — 같은 데이터 다른 lens**. 149 indicator는 (i) 노이즈 정제 후 (ii) 정책학 lens (kind=indicator만)와 IR lens (procedural_phrases 동시 등장 여부) 둘 다 분석. Stage 2 GAT에서 indicator 노드는 두 attention head로 분리 학습 가능.

### D4 — counterfactual 설계
- **Policy 입장**: indicator 채택률 (지표 design quality 변화 — COP29→COP30 시계열)
- **IR 입장**: chair-level (의장 텍스트 보존도 — advance→final cosine, 비-BASIC 의장 baseline)
- **처리**: **양립 — 두 counterfactual 모두 수집/측정**. (a) IR: COP21 Paris (Fabius) / COP26 Glasgow (Sharma) / COP28 Dubai (Al Jaber) / COP29 Baku (Babayev) presidency letters 수집 → chair language 분포 비교. (b) Policy: COP29 → COP30 GGA 결정문 indicator 변화 시계열 + KEI 제3차 적응강화대책 cross-walk. 두 counterfactual은 분석 대상이 다르므로 충돌 없음.

---

## 3. 결정적 비판 (top critiques) — Round 3 P0 변환

| ID | 비판 출처 | 한 줄 진단 | Round 3 task |
|----|----------|----------|---------------|
| **CR3.1** | IR §3 C2.1 (P0) | N=17 chair records → 인과 추론 불가, R-GAT edge overfit | T01: COP21~COP29 11개 historical presidency letters/L-document 추가 수집 (목표 +50, 누적 N≥67) |
| **CR3.2** | IR §3 C2.2 (P0) | frame_type justice/development 0건 — AOSIS·LDC norm entrepreneurship invisible | T02: rhetorical signature 키워드 확장 + Stage 1 LLM v1.4 prompt에 frame logic instruction |
| **CR3.3** | Policy §3 C1 (P0) | 149 indicator 중 31% PDF 목차 노이즈 — unit definition 위반 | T02: `kind` 필드 분화 + seq<14 또는 "..." 패턴 toc 자동 라벨링 |
| **CR3.4** | Policy §3 C3 (P0) | Nodality SD 0.36 — 4축 변별력 부족, 키워드 사전 광범위 매칭 | T02: discriminating keyword 선별 + TF-IDF 가중 |
| **CR3.5** | Policy §3 C2 (P1) | JT-ADAPT 53건 비국가 행위자 0건 (COICA/APIB/ITUC/CAN invisible) | T01: ISD ENB 인용에서 비국가 행위자 입장문 5-10건 시범 추출 |
| **CR3.6** | IR §6 P0(3) | Realist baseline B0 데이터 부재 (GDP/CO2/Mil/Alliance) | T01: World Bank API + Our World in Data CO2 + SIPRI + COW 4개 데이터셋 |
| **CR3.7** | Policy §5 P1(3) | 한국 제3차 적응강화대책 PDF 인코딩 실패 + KEI 모니터링 보고서 미수집 | T01: Playwright 재시도 + KEI Working Paper 2024-08 수집 |
| **CR3.8** | 양 교수 공통 (P0) | Stage 1 LLM 추출 미가동 — 모든 점수가 규칙 기반 | T02 prep + Round 4 P0: ANTHROPIC_API_KEY 점검 + 5개 highest-value 문서 시범 추출 (~$5-10) |

---

## 4. Heedo 헌법 4조항 정합성 점검

| Heedo 지시 | Round 2 evidence | Round 3 plan 정합 | 위배 가능성 |
|-----------|----------------|---------------|-----------|
| ① 논문감 수준 (Global Env Change / NeurIPS CCAI) | Authority 6.1·sovereignty 5건·149 indicator·17 chair record는 reviewer가 인정할 정량 evidence | T01-T04 모두 reviewer 즉각 결함을 잡는 작업 (N 부족, 노이즈, 변별력) | 위배 0 |
| ② COP30 회고 검증 (Belém Package) | Belém Package L.24/L.25/L.25E 직접 확보, GGA-IND Authority 6.1, 의장국 procedural authority 17건 정량화 | Round 3 historical baseline 추가는 회고 검증의 외적 타당도 강화 | 위배 0 |
| ③ 수업·논문 투트랙 | Brazilian Plano Clima 3건 (브라질/논문) + Korean MOFA 3건·MOE NAP 1건 (수업/한국어) 양측 데이터 | T01에 한국 KEI 모니터링 + Brazilian Planalto 추가 수집 양립 | 위배 0 |
| ④ LLM-GNN-LLM 파이프라인 신규성 유지 | schema v1.3 + features v2 채택, GAT R-GAT edge type 추가는 Heedo XAI/GAT 전문성 활용 | Stage 1 LLM 활성화 (Round 4 P0), Stage 2 GAT 학습 준비 | 위배 0 |

→ **Constitution check: 4/4 PASS. Round 3 task 8건 모두 헌법 정합.**

---

## 5. 처리 결정 (Round 3 task assignment)

### 5.1 task 4종 매핑

| Task | 할당 | Round 3 P0 항목 | Round 3 P1 항목 | 예상 산출 |
|------|-----|-------------|-------------|---------|
| **T01 collector** (sonnet) | policy-data-collector | CR3.1 (historical presidency letters +50), CR3.6 (realist baseline 4 dataset), CR3.7 (KEI + 한국 NAP 재시도) | CR3.5 (JT-ADAPT 비국가 행위자 5-10건), Castro 2025 supp. 재시도 | manifest 102→150+, chair_metadata 17→67+, country_features 32-dim → 36-dim (CO2 cumulative + GDP + military + alliance overlap) |
| **T02 refinement** (sonnet) | data-refinement-analyst | CR3.2 (justice/development frame rhetorical signature), CR3.3 (kind 분화 + toc 라벨링), CR3.4 (discriminating keyword + TF-IDF), CR3.8 prep (extraction_targets 우선순위 부여) | 그룹별 frame distribution table + Pearson χ² | documents.jsonl 87→150+, uae_belem_indicators.jsonl kind 분화 후 indicator 카운트 정확화, frame_distribution 5범주 모두 nonzero |
| **T03 policy-sci** (opus) | policy-science-professor | Round 2 권고 정밀화 검증, Task E IRR 메트릭 구체화, 한국 제3차 적응강화대책 cross-walk | 4축 다양성 지수 (Shannon entropy) | critique_round3.md, IRR 평가 protocol 초안, KEI cross-walk matrix 5×6 |
| **T04 ir-political** (opus) | ir-political-professor | chair_metadata N≥67 후 인과 추론 검증, frame_type 5범주 분포 균형 검증, Tallberg 4 채널 모두 측정 가능 검증 | counterfactual baseline 1·2 산출 (cosine + KS-test) | critique_round3.md, R-GAT edge type ablation 가능성 평가 |

### 5.2 Stage 1 LLM 활성화 — Round 4 P0 권고 (Round 3에서 prep)

Round 3에서 T02가 Stage 1 LLM 호출 ready 상태가 되면 Round 4에서 실제 추출 가동.
- **점검 사항**: ANTHROPIC_API_KEY 환경 변수, prompt v1.4 (rhetorical signature instruction 포함), seed/temperature 기록 인프라, evidence_quote 출력 schema
- **첫 추출 대상 5건**: 
  1. FCCC/PA/CMA/2025/L.25E_final (`cop30_curated-f569...`) — GGA 최종 결정문
  2. AOSIS submission 1건 (Round 3 수집 후 highest-priority)
  3. LMDC submission 1건 (Round 3 수집 후 highest-priority)
  4. Plano Clima Sumário Executivo (`brazilian_gov-...`) — 브라질 적응정책
  5. ENB COP30 summary (`enb_curated-...`) — daily negotiation 흐름
- **비용 추정**: ~$5-10 per 5-doc trial run (Sonnet 4.5 input ~50K tokens × 5 docs + output ~10K tokens × 5 docs)
- **거버넌스**: Heedo 사전 승인 필요 — Round 3 종료 시점에 Heedo 결정 요청 (현재 cross-review는 Round 4 P0 권고로 명시)

### 5.3 양립 처리 (D1-D4 모두 양립)

D1 scope 확장은 HEEDO-1로 이미 accept. D2 정밀화/확장은 T01·T02가 독립 동시 진행. D3 indicator 분석 lens는 둘 다 적용 (kind 분화 후 정책학·IR 양측 lens 분석 가능). D4 counterfactual은 IR(chair-level) + Policy(indicator-level) 둘 다 수집/측정. **불일치는 우선순위 충돌이 아니라 분석 lens 차이 → 양립.**

### 5.4 Heedo 에스컬레이션 (Round 3 결정 필요 사안)

| ID | 사안 | 권고 | 결정자 |
|----|------|------|------|
| **HEEDO-4** | Stage 1 LLM 활성화 (Round 4 P0) — ANTHROPIC_API_KEY + ~$10 비용 + prompt v1.4 채택 | accept (Round 3 종료 시점에 prep 완료 검증 후) | Heedo |
| **HEEDO-5** | Task E 평가 protocol — KEI 모니터링 보고서·OECD CRS·NDC Registry 통합 (정책학 §4 권고) | accept (정책학 저널 투고 정당화 + Heedo 헌법 ① 정합) | Heedo |
| **HEEDO-6** | 한국 제3차 적응강화대책 KEI Working Paper 수집 — academic license 검토 | 직접 다운로드 가능 (KEI 공개 보고서) → automatic accept | 자동 |
| **HEEDO-7** | Castro 2025 supplementary 재시도 — 제1저자 academic email contact | accept (Round 1 D5 미해결, Heedo 학교 이메일 발송 권고) | Heedo |

→ Round 2 closing report에서 **HEEDO-4·HEEDO-5·HEEDO-7 3건 명시적 결정 요청**.

---

## 6. Rubric 변화 정량 분석

| Dimension | R1 Policy | R2 Policy | R1 IR | R2 IR | R2 Combined | 변화 동인 |
|-----------|---------:|---------:|------:|------:|-----------:|----------|
| Theoretical | 3.0 | **4.0** | 3.5 | **4.0** | 4.0 | NATO 4축 + frame_type 5범주 schema hard-wire |
| Methodological | 3.0 | **3.5** | 3.0 | **3.5** | 3.5 | procedural_signals 자동식별, 단 LLM 미가동 |
| Empirical | 2.0 | **4.0** | 2.5 | **3.5** | 3.75 | Belém Package 1차 사료 + 17 chair + 39 NDC + 149 indicator |
| Policy/strategic | 2.0 | **3.0** | 3.5 | **4.0** | 3.5 | 한국 정부 자료 일부, Track A 브리핑 textual grounding 강화 |
| Reproducibility | 4.0 | **4.5** | 4.0 | **4.5** | 4.5 | schema_pass_rate 95.2% + audit trail round2-v1.3 |
| **평균** | **2.8** | **3.8** | **3.3** | **3.9** | **3.85** | +0.80 (combined) |

→ G4 dual review combined 3.05 → **3.85** (target 3.0 명확히 통과). 두 교수 모두 R&R minor revision 단계 진입.

---

## 7. Round 2 closure 권고

**team-lead 권고: Round 2 공식 종결 (approved with Round 3 P0 remediation)**.

근거:
1. 두 교수 모두 +1.0 이상 평점 도약, combined 3.85 (target 3.0 명확히 초과)
2. Round 1 권고 3건 모두 evidence 산출 (Authority 6.1, frame distribution, chair_metadata)
3. C-shared 3건 (CR3.1·CR3.2·CR3.3·CR3.4)은 Round 3 task 4종으로 모두 처리 가능
4. Heedo 헌법 4조항 모두 위배 0건
5. 새 gap 8건 발견 (CR3.1~CR3.8) — 수렴 카운터 0/3 유지 (Round 5-6 수렴 예상 budget 내)

다음 라운드 진입 차원:
- **Round 3 (Phase A)**: T01 historical collection + T02 정밀화 (병렬) → 두 교수 critique → cross-review
- **Round 4 (Phase A)**: Stage 1 LLM 활성화 (조건부 Heedo 승인) → 첫 LLM 추출 → 정량 점수 → 두 교수 critique
- **Round 5-6 (Phase B)**: Stage 2 GAT 학습 + Task E IRR 측정 + 수렴 평가

---

## 8. Constitution check 최종

- 헌법 ① (논문감): G4 3.85 = R&R minor revision 진입 = 논문감 ✓
- 헌법 ② (COP30 검증): Belém Package 직접 확보 + 의장 procedural authority 정량화 ✓
- 헌법 ③ (투트랙): 한국·브라질 양측 데이터 수집 ✓
- 헌법 ④ (LLM-GNN-LLM 신규성): schema v1.3 + features v2 채택, Stage 1 LLM 활성화 prep, Stage 2 GAT R-GAT edge type ✓

→ **모두 PASS. Round 2 closure 승인 권고.**

---

*— team-lead, 2026-04-25 cross-review (Round 2 closure synthesis)*
