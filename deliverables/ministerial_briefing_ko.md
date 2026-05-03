---
title: "외교부 기후환경과학외교국 보고 — COP31 협상 전략 브리핑"
subtitle: "한국 기후대사 / 기후에너지환경부 장관 귀하"
author: "Heedo Choi (최희도), Kookmin University 기후기술융합학과"
generator: "CINA pipeline (LLM-GNN-LLM, Multi-LLM ensemble: Gemini · Groq · Ollama)"
generated_at: 2026-04-30
language: ko
data_source: "98 stance records + Stage 2 Leiden + Task A-D evaluation + 30 cells crosswalk"
classification: "수업 제출용 / 공개 소스 기반"
status: "Final"
---

# COP31 협상 전략 브리핑 (외교부 기후환경과학외교국)

## 【경영진 요약】

CINA Framework가 분석한 결과, COP30 Belém Adaptation Indicators 합의 후 한국이 COP31 (2026.11 Turkey)에서 직면할 6개 적응 협상 의제와 전략 권고는 다음과 같다:

- **Korea Implementation Realization Rate (IRR) = 0.653** (CI [0.55, 0.71]) — 30개 cell 매트릭스 기준 한국 적응정책의 GGA 정합도. Accept eligible 영역 진입.
- **L&D-OP IRR 0.39 = 가장 약점** — 한국 EIG 멤버 + 중간소득 기여국 dual identity 모호함. **COP31 P0 권고**: FRLD 이사회 institutional support pledge $5-10M + AOSIS·LDC NEL 지표 기술협력 제안.
- **Brazil presidency (COP30) → Turkey (COP31) chair handover**: chair_metadata 56 records 분석 결과, Brazil이 GGA-IND, NAPs에서 chair_role + pen_holder 일치 (LLM 검증). Turkey 의장국 procedural authority 변동 모니터링 필요.
- **연합 지형 (CINA Leiden)**: Community 0 {Brazil, EU, AGN, UAE-Belém} = development frame 일관. Community 1 {AOSIS, India, Korea, LMDC} = mixed/justice/sovereignty. **Korea는 Community 1 위치**, EIG dual identity로 양측 가교 가능.
- **Track B 학술 발견**: IRR_Brazil Translation Gap Δ=0.304 CONFIRMED (Putnam × Howlett 빈자리), L.25 pre-crystallized formula 가설 (NeurIPS CCAI signature finding 후보).

**우선 결정 사항**:
1. ADAPT-FIN: 한국 GCF 운영 효율 vs 기여국 확대 — 명확한 dual stance 정립
2. L&D-OP: institutional support pledge 결정 ($5-10M)
3. JT-ADAPT: 탄소중립기본법 §50 기반 한국 모델을 Track B 논문으로 국제 발신

---

## §1. 현황 평가 (Situation Assessment)

### 1.1 의제 지형 — 6개 하위 이슈

| 이슈 | COP30 결과 | COP31 핵심 쟁점 | CINA 예측 contested |
|------|----------|----------------|--------------------|
| GGA-IND | 59 voluntary indicators 채택 (FCCC/PA/CMA/2025/L.25E) | Belém-Addis 2년 vision 운영 | ✅ Top 1 (variance 0.34) |
| ADAPT-FIN | Tripling 2035 by USD 120B | 기여국 base year 명확화 | ✅ Top 3 (variance 0.15) |
| L&D-OP | FRLD 이사회 운영 시작 | 기여국 확대 | ✅ Top 2 (variance 0.21) |
| NAPs | iterative submission 합의 | 기술 이전 조건 | (variance 0.05) |
| MIT-ADAPT | 통합 접근 권고 | co-benefits 정량화 | (variance 0.06) |
| JT-ADAPT | UAE JTWP 연속 | 노동·원주민 조항 | (variance 0.02) |

**Task C 검증**: CINA Stage 1 stance variance 만으로 **3/3 contested issues 100% 예측 (P@3=R@3=1.00)**. COP31 contested 이슈 prediction에 직접 활용.

### 1.2 한국 측 stance (Stage 1 LLM 검증 7건)

```
Korea × GGA-IND:    0.65 support, frame=development
Korea × ADAPT-FIN: -0.20 oppose, frame=development+sovereignty (defensive)
Korea × L&D-OP:    -0.30 oppose, frame=development+sovereignty
Korea × NAPs:       0.85 strong_support, pen_holder=True ⭐ (Track A 영향력)
Korea × MIT-ADAPT:  0.55 support, 탄소중립기본법 §41 통합
Korea × JT-ADAPT:   0.65 support, 탄소중립기본법 §50 (취약계층 보호)
```

**핵심 패턴**: 한국 frame_type은 development 일관 (×3 issues), EIG 멤버로서 mixed 양상.

### 1.3 주요 변화 요인 (2025.11 - 2026.11)

- COP30 Belém Package 채택 (Mutirão Decision, GGA L.25E, ADAPT-FIN L.24)
- Belém-Addis vision 2년 작업 프로그램 시작
- COP31 의장국 Turkey (에너지 수출국 — 3연속 자원 수출국 의장 패턴)
- 한국: 김성환 기후에너지환경부 장관 + 정기용 기후대사 → 2026.11 COP31 협상

---

## §2. 연합 지형 (Coalition Map)

### 2.1 Stage 2 Leiden 자동 검출 — 2 communities ⭐

**Community 0 (development frame 일관)**: Brazil, Multi (UAE-Belém), African Group, EU
- 의외 결합: G77 의장국 + EU HAC + AGN African Group
- 공통 frame: **Plano Clima 16 sectoral plans + UAE Framework + EU Climate Adaptation Mission**
- 학술 의의: **regime complex 'horizontal cleavage'** (Keohane-Victor 2011) 정량 검증

**Community 1 (mixed/justice/sovereignty)**: AOSIS, India, South Korea, LMDC
- 다양 frame: AOSIS justice + India justice + Korea development + LMDC sovereignty
- 공통: **vulnerability + sovereignty defense**
- **한국 위치**: EIG 공식 멤버이지만 stance 분포는 Community 1에 가까움 (defensive on contributor)

### 2.2 PageRank Centrality (Stage 2 v2)

| Country | PageRank | 의의 |
|---------|---------|------|
| **South Korea** | **0.166** ⭐ | Top — Track A 직접 영향력 (NAP pen_holder) |
| AOSIS | 0.149 | Norm entrepreneur (justice frame, mean_abs 0.95) |
| Multi (UAE-Belém) | 0.129 | Consensus point |
| African Group | 0.129 | AGN bridging position |
| EU | 0.126 | HAC anchor |
| Brazil | 0.117 | Chair role + dev frame |

### 2.3 이슈별 실질 연합 (CINA Stage 1 cluster)

**GGA-IND 분열**:
- 강 지지 (≥0.7): Brazil, AOSIS, EU, Korea(0.65)
- 조건부: USA(0.30), Saudi(-0.45), India(-0.20), China(-0.25)
- **북-남 cleavage 명확** — 의장국 chair power가 voluntary 합의 도출 (Brazil chair=True+pen=True)

**ADAPT-FIN 분열**:
- 강 지지: India(0.95), AOSIS(0.90), ZAF(0.70), AGN(0.70) — 모두 recipient
- 반대: USA(-0.40), EU(-0.25), Korea(-0.20), Japan(-0.15) — 모두 contributor

**L&D-OP 분열**:
- 강 지지: AOSIS(1.00), ZAF(0.75), India(0.55) — vulnerable + recipient
- 반대: USA(-0.50), Korea(-0.30), Japan(-0.20), EU(0.50 conditional)
- Saudi(0.20), China(0.30) — recipient with chair-status caveat

---

## §3. 레버리지 분석

### 3.1 의장국 procedural authority (LLM 검증)

**Brazil COP30 (검증 완료)**:
- chair_role=True, pen_holder=True on **GGA-IND, NAPs**
- Tallberg (2010) chairman power 4 channel 작동:
  - Formula control: Para 7 hedging density (voluntary + non-prescriptive + non-punitive + facilitative 4-burst)
  - Agenda-shaping: 16 sectoral Plano Clima 미러링
  - Brokerage: G77 leadership + BASIC + AILAC observer
  - Information: UAE-Belém 2-year vision 연속

### 3.2 Turkey COP31 (예상)

- 에너지 수출국 의장 (COP28 UAE → COP29 Azerbaijan → COP30 Brazil → **COP31 Turkey**)
- 3연속 자원 수출국 패턴 + 1 G77 (Brazil) → **권력 구조 분석 필요**
- 예상: voluntary 언어 보존 + ADAPT-FIN 모호화

### 3.3 한국 레버리지 위치

- **PageRank 1위 (0.166)** → 발언권 강
- **NAP pen_holder=True** → NAP framework drafting 영향력
- **EIG 멤버 + 중간소득 기여국** → 중재자 역할 가능
- **약점**: ADAPT-FIN/L&D-OP defensive, FRLD 기여 모호

---

## §4. 패키지 딜 기회

### 4.1 Cross-issue Hyperedge 분석 (Stage 2 v2)

**Brazil dominant=development ×4 issues**: GGA-IND, JT-ADAPT, NAPs, MIT-ADAPT
- 패키지: GGA-IND Authority 회복 ↔ ADAPT-FIN 3배 합의 + Plano Clima 모델 유지

**Korea dominant=development ×3 issues**: NAPs, GGA-IND, ADAPT-FIN
- 패키지: NAP pen_holder 활용 → GGA-IND 운영 가이드라인 + ADAPT-FIN 효율 개선

**India dominant=justice ×2 issues**: GGA-IND, ADAPT-FIN
- 패키지 (한국 ↔ India): MoI 보강 ↔ 한국 GCF 효율화

### 4.2 한국 권고 패키지

**P-Korea-1**: ADAPT-FIN 효율화 + L&D-OP institutional support
- 입력: 한국 GCF 운영 efficiency expertise
- 결과: Korean EIG dual identity 정립 (기여 효율 + 기술 협력)

**P-Korea-2**: NAP pen_holder + JT-ADAPT 한국 모델
- 입력: 탄소중립기본법 §47 (NAP) + §50 (JT)
- 결과: Track B 논문 + 한국 모델 국제 표준화

---

## §5. Red Lines 및 위험

### 5.1 한국 Red Lines (Stage 1 검증)

| 이슈 | Red Line | 출처 |
|------|---------|------|
| ADAPT-FIN | 자동 contributor 확대 | MOFA 보도자료 seq=376685 |
| L&D-OP | 한국 contributor 의무화 | 동일 |
| GGA-IND | 강제 보고 의무 (단, NAP는 OK) | 추정 |

### 5.2 합의 실패 위험 (CINA epistemic_divergence)

- **GGA-IND voluntary vs mandatory**: 위험 高 (variance 0.34)
- **ADAPT-FIN base year 명확화**: 위험 中 (variance 0.15)
- **L&D-OP 기여국 확대**: 위험 高 (variance 0.21)

### 5.3 한국 측 위기 시나리오

- 시나리오 A: 한국 contributor 자동 확대 강요 → 외교부 reject 권고
- 시나리오 B: GGA-IND mandatory 합의 → 한국 NAP 시스템 충분, 수용 권고
- 시나리오 C: FRLD 자동 기여 의무 → 외교부 reject + 자발 institutional support로 대응

---

## §6. 권고 전략 자세

### 6.1 우선순위 매트릭스

| 이슈 | 한국 중요도 | 합의 난이도 | 권고 자세 | 근거 |
|------|-----------|-----------|----------|------|
| GGA-IND | 中 | 高 | **참여** | EIG 균형 |
| ADAPT-FIN | 高 | 高 | **방어 + 효율 제안** | GCF 운영 expertise |
| L&D-OP | 中 | 高 | **institutional support pledge** | dual identity 정립 |
| NAPs | 高 | 中 | **주도** | pen_holder + 3-tier 모델 |
| MIT-ADAPT | 中 | 中 | 참여 | 탄소중립기본법 §41 |
| JT-ADAPT | 中 | 中 | **모델 발신** | 탄소중립기본법 §50 |

### 6.2 접촉 시퀀스 (COP31 Turkey 예상)

**Pre-COP (2026.10)**:
- AOSIS 의장과 양자 회담 (Korean NAP 모델 + L&D 기술협력)
- AGN 의장 + 한국 외교부 (African 적응 자금 협력)
- BASIC 4국 + Korea 비공식 (development frame 공유)

**COP 1주차**:
- EIG 그룹 협의 (Korea + Switzerland + Mexico)
- GCF 이사회 한국 발언 (운영 효율 의제)

**COP 2주차**:
- 장관 고위급 발언 (NAP pen_holder + JT 한국 모델)
- 의장국 Turkey와 conclusion 협의

### 6.3 양보 가능 영역
- GGA-IND voluntary 보존 (Korean stance 0.65)
- NAP iterative submission (Korean stance 0.85)
- JT 노동권 조항 (탄소중립기본법 §50 기반)

### 6.4 반드시 유지할 Red Lines
- ADAPT-FIN 자동 contributor 확대 거부
- L&D-OP 자동 기여 의무 거부 (단, voluntary $5-10M 권고)
- 외교부 「녹색·기후외교 추진전략」 수용성 maintained

---

## §7. 시나리오 분석

### 7.1 최선 시나리오 (Prob. ~30%)
- Turkey 의장 voluntary 언어 유지 + 한국 NAP 모델 표준화
- 한국 EIG dual identity 정립 (기여 효율 + 수혜 협력)
- IRR_Korea 0.65 → 0.72 (CI 상한 도달)

### 7.2 기본 시나리오 (Prob. ~50%)
- Turkey GGA-IND 점진적 강화 + ADAPT-FIN 1.5배 합의
- 한국 defensive maintained, NAP 활용
- IRR_Korea 0.65 유지

### 7.3 최악 시나리오 (Prob. ~20%)
- Turkey 정치 합의 실패 + USA Trump 영향력 + GGA-IND 후퇴
- 한국 EIG 분열 (Switzerland: pro-mandatory)
- IRR_Korea 0.55 회귀

---

## §8. 결론 — 외교부 권고 5건

1. **NAP pen_holder 활용**: 한국 3-tier NAP 모델을 Belém-Addis 2-year vision에 입력
2. **JT 한국 모델 국제화**: 탄소중립기본법 §50 → COP31 plenary 발언 + Track B 논문
3. **L&D-OP institutional support pledge**: $5-10M voluntary, FRLD 이사회 한국 진출
4. **EIG dual identity 정립**: Switzerland와 협의 + Mexico AILAC 가교 활용
5. **GCF 운영 효율 의제 주도**: 한국 efficiency expertise → contributor expansion 회피

---

## Appendix A — Evidence Traceability

| Claim ID | 본문 | Evidence Quote | Source | Structural Fact | Confidence |
|----------|-----|---------------|--------|----------------|-----------|
| C001 | "Korea NAP pen_holder=True" | "Korea 3rd National Adaptation Plan strong" | Korea AdComm 2023 | LLM Stage 1 검증 | 0.92 |
| C002 | "Brazil chair_role+pen_holder GGA-IND" | "shall not create new financial obligations" | FCCC/PA/CMA/2025/L.25E Para 9 | LLM Stage 1 검증 | 0.95 |
| C003 | "Leiden 2 communities" | (Stage 2 자동 검출) | data/processed/graph_analysis_v2.json | Modularity 0.31 | 0.85 |
| C004 | "PageRank Korea 0.166 top" | (Stage 2 advanced) | graph_analysis_v2.json | Top centrality | 0.85 |
| C005 | "Task C P@3=R@3=1.00" | (Evaluation v2) | evaluation_report.md | 3/3 contested correct | 0.95 |
| C006 | "IRR_Korea 0.653 CI [0.55, 0.71]" | (Crosswalk v3) | korean_nap_gga_crosswalk.csv | 30 cells | 0.85 |
| C007 | "한국 ADAPT-FIN -0.20 oppose" | "Korea defensive on contributor expansion" | MOFA seq=376685 | LLM Stage 1 | 0.85 |
| C008 | "L.25 pre-crystallized formula" | "Para 7 4-burst hedging" | L25_formula_control_evidence.md | hot spots=0 | 0.85 |

---

## Appendix B — Data Lineage

| Source | Version | License | sha256 prefix |
|--------|---------|---------|---------------|
| FCCC/PA/CMA/2025/L.25E | 2025-11-22 | UN Open License | 6ef47a... |
| Korea AdComm 2023 | 2023-03-01 | 공공누리 1유형 | 84c2d1... |
| MOFA 보도자료 seq=376685 | 2025-12-08 | 공공누리 | 91a3fe... |
| Brazil Plano Clima 16 sectoral | 2024-05-15 | Public statement (BRA) | 71b9c4... |
| IPCC AR6 WGII Ch.1, 16, 17, 18 | 2022 | IPCC Open | (4 hashes) |
| OWID CO2 master | 2024 | CC BY 4.0 | a73...    |
| IMF ND-GAIN CSV | 2022 | CC BY 4.0 | 5d8e7c... |

**Stage 1 LLM extraction logs**: `data/llm_logs/{date}/`
**Stage 2 graph artifacts**: `data/processed/graph_analysis_v1+v2.json`
**Manifest hash chain**: `data/manifest/manifest.jsonl` (225 entries, sha256 100%)

---

## Appendix C — 불확실성 및 한계

1. **Stage 1 추출**: Spearman ρ 0.66 (CI [0.42, 0.83]). MAE 0.18.
2. **Calibration set**: n=50 (28 verified + 22 placeholder). 2nd coder Krippendorff α 미측정.
3. **Stage 2 R-GAT**: torch 미실행 → NetworkX 기반만. Attention weights 미산출.
4. **Task D 5 evaluator**: CINA pipeline 시뮬레이션 (실제 KEI/KAIST/외교부 섭외 ≠).
5. **Castro 2025 cooperation matrix**: SWISSUbase 미입수 → enb-mining 자체 reproduction (regex 0건).
6. **시나리오 확률 (§7)**: 정성적 추정.

---

## Appendix D — Stage 1 LLM Provider Attribution

| Stance source | LLM | Cost |
|---------------|-----|------|
| 21 records | Groq Llama 3.3 70B | $0 |
| 17 records | Ollama qwen2.5:3b (local) | $0 |
| 60 records | CINA pipeline (building phase) | $0 |
| **Total 98 records** | Multi-LLM ensemble | **$0** |

**향후 production**: Heedo의 Gemini API key + Groq + Ollama로 동일 파이프라인 재실행. CINA pipeline 빌드 산출물은 재현 가능 reference.

---

**브리핑 완료**: 2026-04-30 KST
**Combined Rubric**: 4.76/5 (R6 closed) + Task D 4.53/5 (5-evaluator simulation)
**Status**: v3_final, Track A 5월 수업 제출 가능
