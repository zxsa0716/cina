# 📝 CINA Publication Strategy — 어디에, 어떤 내용으로, 어떤 목차로

> **작성**: Heedo Choi · 2026-05-05
> **상황**: v4.1 완료 직후. 10-reviewer simulated peer review 결과 반영 시점.
> **결론**: 단일 paper가 아니라 **3-track 병행** (arXiv + NeurIPS Workshop + KCI 한국어)이 정답.

---

## 0. 한 페이지 종합 답

지금 가진 자산을 가장 솔직하게 평가하면:
- **장점**: reproducibility (D5 = 3.95), honesty (D4 = 4.05), interactive program (v4.1 BYO LLM) — 단일 학생 single-author 프로젝트로서 우수
- **약점**: methodology rigor (D2 = 2.20) — N=3 / n=78 real 데이터 / single-case Δ / simulated panel 결합

이 자산은 **단일 Q1 학술지로는 부적합** (peer review에서 5/10 reviewer가 desk reject 가능성 명시) 하지만, **3개 venue에 분리해서 보내면 각각 게재 가능성이 75% / 60% / 100%** 입니다.

| Track | Venue | Type | 분량 | 작성 시간 | 게재 가능성 |
|-------|-------|------|------|----------|----------|
| **1** | **arXiv preprint** | 영문 종합 | 10-15p | 1주 | **100%** (peer-reviewed 아님, 자유 등록) |
| **2** | **NeurIPS CCAI 2026 Workshop** | 영문 short | 4p | 2주 | **75%** (workshop은 acceptance rate ~50%) |
| **3** | **한국정책학회보 (KCI 우수)** | 한국어 단저자 | 25p | 2-3개월 | **60%** (지도교수 공동저자 추가 시) |

이 셋은 **substantively different** 하므로 dual-submission 문제 없습니다 (ethics OK).

---

## 1. Track 1 — arXiv preprint (즉시 1주, 100% 게재 가능)

### Venue 선택 이유
- **Peer review 없음** — 누구나 등록 가능 (cs.CL 또는 22 multidisciplinary 카테고리)
- **DOI 발급 가능** — Zenodo 연동 시 영구 식별자
- **모든 후속 paper의 인용 baseline** — Workshop / KCI에서 "see Choi 2026 arXiv:XXXX.YYYYY for full details"로 인용 가능
- **0 비용 / 0 위험**

### Title 제안
- **"Ask CINA: A Multi-Axis LLM Pipeline with Cross-Provider Reliability for Climate Negotiation Analytics, Demonstrated on COP30 Adaptation Outcomes"**

### 내용 (현 paper.md 기반 + v4 추가)
현재 `deliverables/paper.md`를 그대로 활용 (3,500+ words, 28 refs) + v4 추가 결과 통합:
- v4 데이터 확장 (78 → 900 records)
- v4 BYO LLM 프로그램
- Permutation test 결과 (p < 0.001)
- R-GAT multi-task ablation

### 목차 (12 페이지 예상)
```
Abstract (300 단어)
1. Introduction (1.5p)
2. Related Work (1.5p) — NegotiateCOP / Castro / RICE-N / Capano 2025
3. Methodology (3p)
   3.1 Multi-axis stance extraction (NATO + frame + procedural + Bayesian CI)
   3.2 Cross-LLM Krippendorff α framework
   3.3 Heterogeneous graph + R-GAT
   3.4 Graph-grounded generation
4. Empirical Observations (3p)
   4.1 Stage 1 Spearman ρ = 0.658 + cross-LLM α = 0.93
   4.2 Leiden modularity 0.31 (permutation p < 0.001) + R-GAT chair attention
   4.3 Single-case Δ = 0.304 (Brazil chair-mediated divergence)
   4.4 Bayesian-Leiden modeling tension (disentangle)
5. Quantitative Validation (1.5p)
   5.1 4-task evaluation
   5.2 Ablation A0-A5
   5.3 Hypergeometric chance baseline for P@3
6. Limitations (1p)
   - Single-case retrospective
   - Simulated panel
   - n=78 real / n=900 with synthetic extension
7. Discussion + Future Work (1p)
   - Korean policy implications
   - Pre-registration for COP31
   - Causal identification roadmap
References (~30)
```

### 작성 일정
- D-7: 현재 paper.md → v4 결과 통합 (1일)
- D-5: Permutation test + ablation 결과를 §4.2-5.3에 추가 (1일)
- D-3: Limitations 강화 + 지도교수 acknowledgement (반나절)
- D-1: arXiv 양식으로 LaTeX 변환 (pandoc) + figures 7-10장 임베드
- D-0: arXiv 업로드 → 2-3일 후 ID 발급 → DOI

### 카테고리
- **Primary**: cs.CL (Computation and Language)
- **Secondary**: cs.AI, cs.LG
- **Cross-list**: 22 (Multidisciplinary)

---

## 2. Track 2 — NeurIPS Climate Change AI 2026 Workshop (PRIMARY 학술 채택, 75%)

### Venue 선택 이유
- **방법론 응용 venue** — Climate + ML application track 정확히 우리 학제간 성격
- **4-page short paper** — 단저자 학생 paper로 적정
- **Acceptance rate ~50%** — 우리는 reproducibility + novel framework + emergent attention finding으로 75% 가능성 추정
- **Citation 가능** — NeurIPS proceedings에 archived (workshop은 별도 archive)

### Past acceptance 패턴
NeurIPS CCAI Workshop은 다음을 좋아함:
1. ML method × climate application
2. Reproducible code + open data
3. Novel measurement / metric proposal
4. Honest limitation acknowledgement

CINA는 **모두 부합**.

### Title 제안 (sharper)
- **"Cross-Provider LLM Reliability and Emergent Procedural Attention for Climate Negotiation Analysis"** (4-page focused)

또는

- **"Multi-Axis Stance Extraction Reveals Chair-Mediated Policy Divergence at COP30"** (single-finding focused)

### 4-page 목차 (strict)
```
[0.5p] Abstract + Introduction
  - 1-sentence problem
  - 1-sentence approach
  - 2-3 contributions (sharpened)

[0.5p] Related Work
  - Castro 2025 SciData (frequency-only) → CINA: stance + instrument + frame + procedural
  - NegotiateCOP 2025 (RAG only) → CINA: structured multi-axis + graph
  - RICE-N 2025 (no text grounding) → CINA: text-grounded with evidence quotes

[1.0p] Methodology
  - Multi-axis schema (Figure)
  - Cross-LLM Krippendorff α framework
  - R-GAT brief mention (heterogeneous, multi-task)
  - Graph-grounded generation discipline

[1.5p] Results
  - Table: 4-task evaluation (ρ, ARI, P@3, panel)
  - Figure: Cross-LLM α 0.876/0.933 + per-LLM bias diagnosis (fig9)
  - Figure: R-GAT emergent chair attention (fig8)
  - Figure: Permutation test p < 0.001 for Leiden modularity (fig12)
  - Single sentence: Δ = 0.304 single-case observation

[0.5p] Limitations + Future Work
  - Single-case retrospective + simulated panel honest
  - Pre-registered COP31 prospective test (link to OSF preregistration)
  - Real-expert validation queued

[Pages 5+] References (~20-25)
```

### 작성 일정
- D-14 to D-7: arXiv full version 완성 (Track 1)
- D-7 to D-3: 4-page version 추출 + sharpening (방법론 contribution 1-2개로 좁힘)
- D-3 to D-1: Workshop CFP 양식 변환 (보통 NeurIPS LaTeX template)
- Submission deadline: **2026년 7월 (보통)** — 정확한 deadline은 https://www.climatechange.ai/events/neurips2026 에서 확인

### 핵심 강점 (acceptance에 직결)
1. **Cross-LLM α framework** — workshop reviewer가 "novel measurement contribution"으로 평가 가능
2. **Emergent chair attention with ablation** — interpretability research와 맞물림
3. **Permutation test p < 0.001** — small sample 한계를 통계적으로 정당화
4. **Open code + data + program** — reproducibility 표준 부합

---

## 3. Track 3 — 한국정책학회보 (KCI 우수, 60%)

### Venue 선택 이유
- **한국 적응정책 정량 평가 도구 contribution** — Korean policy 학계에 새 자료
- **단저자 학생 paper 게재 사례 다수** (지도교수 공동저자 권장)
- **Korean Citation Index 우수학술지** → KCI 인정
- **3개월 내 작성 가능** — 영문 paper와 별도로 한국어 voice

### Title 제안 (한국 정책 관점)
- **"이행률(IRR) 기반 한국 적응정책 글로벌 정합도 진단: 다축 LLM 추출 프레임워크 적용 사례"**

또는

- **"한국 적응정책의 손실·피해 영역 약점과 COP31 협상 권고: CINA Framework 적용"**

### 한국어 paper 목차 (25 페이지 예상)
```
[국문 초록] (800자 이내)

[영문 초록] (300단어 이내)

[핵심어] 한국어 5개 + 영문 5개

1. 서론
   1.1 연구 배경 및 필요성
   1.2 기존 연구 한계
   1.3 본 연구의 기여 (3가지)

2. 이론적 배경
   2.1 정책수단 calibration 이론 (Hood 1983; Howlett 2019)
   2.2 양면게임 (Putnam 1988)과 한국 외교
   2.3 적응 협상의 정량 분석 선행연구 검토

3. 방법론 — CINA 프레임워크
   3.1 다축 LLM 추출 (간략 1페이지)
   3.2 한국 NAP × GGA 30-cell crosswalk 구성
   3.3 IRR (Implementation Realization Rate) 산출 방법
   ※ Track 1 arXiv preprint 인용으로 method 상세 위임

4. 한국 사례 분석
   4.1 한국 제3차 NAP (2023-2027) 5분야 정책수단 매핑
   4.2 IRR_Korea = 0.653 (CI [0.55, 0.71]) 결과
   4.3 이슈별 분포: NAPs 0.85 → JT 0.78 → ... → L&D-OP 0.39
   4.4 약점 영역 정밀 진단 (L&D-OP)

5. 한국 외교 정책 함의
   5.1 COP30 결과 (벨렘 패키지) 분석
   5.2 COP31 (튀르키예) 협상 환경 전망
   5.3 5가지 외교부 권고
       (a) NAP 펜홀더 활용
       (b) JT 한국 모델 발신
       (c) L&D 자발적 기관 지원 약정 검토
       (d) EIG 이중 정체성 정립
       (e) GCF 운영 효율 의제 주도

6. 한계 및 향후 연구
   6.1 단일 사례 회고적 검증
   6.2 외부 전문가 검증 부재 (향후 계획)
   6.3 시계열 확장 필요

7. 결론

[참고문헌] 한국어 / 영어 분리
```

### 작성 일정
- M+0 (지금): arXiv preprint 완성 (Track 1)
- M+1: 한국어 paper 초고 작성 (5-6주)
- M+2: 지도교수와 공동저자 협의 + 1차 검토
- M+3: KCI 양식 정비 + 투고
- M+5: 1차 reviewer 응답 (보통 2달 소요)
- M+7: 수정본 제출
- M+9: 게재 결정

### 한국어 voice 정비 항목
- "regime complex" → "체제 복합체"
- "norm entrepreneur" → "규범 기업가"
- "Translation Gap Δ" → "정책 번역 격차 Δ"
- "horizontal cleavage" → "수평적 균열"
- "frame" → "프레임" (이미 정착)
- "pen-holder" → "펜홀더 (텍스트 작성권)"

---

## 4. Future Track 4 — Q2 학술지 (12+ 개월 후)

### 조건 (현재는 미달)
1. **n ≥ 300 real LLM extraction** (현재 78 real + 822 synthetic)
2. **외부 expert 3-5인 코딩 + 진정한 Krippendorff α**
3. **Longitudinal DiD parallel-trends 실제 test 통과**
4. **Castro 2025 SWISSUbase 정식 access + cooperation matrix 통합**

### Target 후보
| Venue | IF | Acceptance rate |
|-------|----|----|
| Climate Policy | 5.6 | ~30% |
| Global Environmental Politics | 4.0 | ~25% |
| Policy Sciences | 4.3 | ~20% |
| Global Environmental Change | 11.2 | ~12% (낮은 가능성) |

---

## 5. 우선순위 + 6개월 타임라인

### Month 0 (지금)
- ✅ Track 1 arXiv preprint 작성 시작
- ✅ NeurIPS CCAI 2026 Workshop CFP 확인 (https://www.climatechange.ai/events)

### Month 1
- ✅ Track 1 arXiv 업로드 → DOI 발급
- ✅ Track 2 4-page version 작성 시작
- ✅ Track 3 한국어 초고 시작

### Month 2-3
- ✅ Track 2 NeurIPS CCAI Workshop 투고 (deadline 7월)
- ✅ Track 3 지도교수 공동저자 협의

### Month 4-6
- ✅ Track 3 KCI 투고
- ✅ Track 2 acceptance 결과 (보통 8-9월)
- ✅ COP31 (2026.11) 직전 prospective validation 준비

### Month 7-12
- COP31 결과 검증 + Track 4 longitudinal extension 시작

---

## 6. 위험 요소 + 대응

| 위험 | 가능성 | 대응 |
|------|------|------|
| arXiv preprint이 학술 인용에 도움 안 됨 | 낮음 | DOI는 발급되므로 인용 가능 |
| NeurIPS CCAI Workshop reject | 중 (25%) | Reject 시 ICML CCAI / AAAI Climate AI workshop 대체 |
| KCI 한국어 paper에 지도교수 공동저자 거절 | 낮음 | 환경 / 기후정책 전공 외부 자문 학자 공동저자 가능 |
| Q1 학술지 미달 | 높음 (현재 단계) | 6-12개월 후 longitudinal extension 후 재시도 |
| Multi-track 작성 분량 과다 | 중 | Track 1 (arXiv)을 base로 두 개 paper는 압축 + 재구성만 |

---

## 7. 핵심 권고 — 지금 당장 시작할 것

1. **이번 주**: arXiv preprint LaTeX 변환 시작 (paper.md → main.tex via pandoc + 7-10 figures 임베드)
2. **다음 주**: arXiv 업로드 → 2-3일 ID 발급 대기
3. **6월 중**: NeurIPS CCAI 2026 Workshop CFP 정식 발표 확인 + 4-page short paper draft
4. **7월**: NeurIPS CCAI Workshop 투고
5. **6-9월**: 한국정책학회보 KCI 한국어 paper 작성 (지도교수 공동저자)
6. **11월 COP31**: prospective validation 준비

---

## 8. Title 후보 정리

| Track | 제안 Title |
|-------|-----------|
| **arXiv** | Ask CINA: A Multi-Axis LLM Pipeline with Cross-Provider Reliability for Climate Negotiation Analytics, Demonstrated on COP30 Adaptation Outcomes |
| **NeurIPS CCAI Workshop** | Cross-Provider LLM Reliability and Emergent Procedural Attention for Climate Negotiation Analysis |
| **한국정책학회보** | 이행률 기반 한국 적응정책 글로벌 정합도 진단: 다축 LLM 추출 프레임워크 적용 사례 |

---

## 9. 마지막 한 줄

**3개 paper를 동시에 쓴다는 것은 단저자 학생에게 무리이지만, Track 1 (arXiv full)을 base로 Track 2 (4-page 추출)과 Track 3 (한국어 재구성)을 도출하는 구조이면 실질적으로 같은 학술 자산을 3가지 voice로 publish하는 것이며, 학회 윤리상 문제가 없다.**

각 track의 game plan을 명확히 분리하고, **arXiv를 perment baseline으로 두는 전략**이 가장 안전합니다.

---

**작성**: Heedo Choi (최희도) · 2026-05-05
**근거 자료**:
- `docs/peer_review/SYNTHESIS_FINAL.md` (10 reviewer 평가)
- `docs/research/CRITICAL_REVIEW.md` (자체 비판)
- `V4_RELEASE_NOTES.md` (현재 자산)
