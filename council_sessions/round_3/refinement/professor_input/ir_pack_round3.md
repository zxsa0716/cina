# Round 3 — IR·국제정치 교수 입력 패키지 (IR Pack v3)

작성: Data Refinement Analyst | 2026-04-25 | CINA Round 3 | processing_version: round3-v1.4

---

## 0. Round 2 권고 반영 확인

Round 2에서 IR 교수에 전달한 주요 발견:
- chair_metadata 17건: ENB 기반 의장 역할 탐지
- 브라켓 언어 잔류("[Notes][Welcomes]")의 의미 미결 상태

Round 3 신규 증거:
- COP28/UAE → COP29/AZE → COP30/BRA 의장 서한 시계열 3건 확보
- GGA draft text 2건: 협상문 버전 진화 추적 가능
- G77/China, LDC, AILAC, Global Solidarity Taskforce 개도국 연합 4개 제출 문서

---

## 1. 의장국 시계열 분석 (COP28→COP30)

### COP28 UAE 의장 (2023)

**핵심 프레이밍**:
> "Fast-tracking the just, equitable and orderly energy transition and slashing emissions before 2030"
> "Transforming climate finance... address the dual challenges of climate and development in a just and equitable way"

**출처**: `round4_curated-ee51d1ac3f31` (COP28_UAE_presidency_letter_oct2023.pdf)

**IR 분석**: UAE(OPEC 산유국) 의장이 "energy transition"을 의제 전면에 배치 — 에너지 생산국의 에너지 안보 담론을 기후 협상 프레임에 통합. 적응보다 완화(mitigation) 중심. 아랍 그룹/OPEC 이익과 UNFCCC 의무 사이의 긴장을 "orderly transition"으로 봉합하는 수사적 전략.

### COP29 AZE 의장 (2024)

**핵심 프레이밍**:
> "COP29 will be the Finance COP... The New Collective Quantified Goal (NCQG) must be our defining achievement"
> "Baku to Belém Roadmap — bridge between COP29 and COP30"

**출처**: `round4_curated-308187ec6e3f` (COP29_AZE_president_designate_first_letter.pdf)

**IR 분석**: AZE(또 다른 산유국)가 "Finance COP" 프레이밍으로 의제를 재정으로 집중. NCQG=$1.3T는 이 프레임의 산물. "Baku to Belém" 브랜딩은 COP29-30 연속성 narrative 구축 — 의장국이 자국 성과를 다음 의장국에 위임하는 비공식 합의의 제도화.

### COP30 BRA 의장 (2025)

**핵심 프레이밍**:
> "COP30 is the People's COP... The Amazon and the oceans are watching us"
> "Adaptation is not a peripheral issue — it is the very heart of what we must achieve"
> "National Adaptation Plans must be the anchor of every country's climate strategy"

**출처**: `round4_curated-05f300fd9c3f` (COP30_BRA_first_letter_from_president_html.html)

**IR 분석**: BRA가 adaptation을 "심장(heart)"으로 프레임화 — COP28(UAE/에너지전환) → COP29(AZE/재정) → COP30(BRA/적응) 의제 순환 구조. "People's COP"는 시민사회·개도국 연합의 정당성 동원 전략. Amazon 언급은 BRA의 협상력 원천(생태 서비스 공급국)을 의제에 투영.

**시계열 핵심 발견**: 연속 3개 의장국이 모두 에너지 수출국(UAE/AZE) 또는 천연자원 보유국(BRA)이라는 사실은 UNFCCC 의장국 선출 메커니즘의 지역 순환 규칙과 대국 이익 사이의 구조적 관계를 노출.

---

## 2. 개도국 연합 네트워크 (G77/AILAC/LDC/LMDC) 포지션 맵

### 연합 간 공통점과 분열선

**공통 입장** (모든 4개 그룹):
- CBDR-RC 원칙 유지 (differentiating historical responsibility)
- 재정 충족 전제 하의 지표 수용
- "context-specific" 지표 접근 선호

**분열선 탐지**:

| 이슈 | G77/China | LDC | AILAC | LMDC |
|------|-----------|-----|-------|------|
| 지표 binding force | 반대 | 반대 | 약한 지지 | 강한 반대 |
| 재정 목표 수준 | $1.3T+ | $1.3T (최소선) | "transformative" | 비명시 |
| 전통 지식 포함 | 찬성 | 찬성 | 찬성 | 유보 |
| 적응 정량화 | 조건부 | 조건부 | 지지 | 유보 |

**출처**: 
- `round4_curated-ba2adb95eb28` (G77_China_Baku_Belem_1_3T_submission.pdf)
- `round4_curated-a3dd05346bd4` (LDC_Baku_Belem_1_3T_roadmap_views.pdf)
- `round4_curated-006d89325646` (AILAC_GST_TD1_2_submission_2022.pdf)
- `round3_curated-cfdd2faec536` (LMDC_submission_on_GGA.pdf)

**IR 분석**: G77(134개국) 내부 분열이 가시화 — LDC는 강한 재정 요구 + 지표 수용, AILAC은 ambitious climate action + developing country protection 병립, LMDC는 development 우선 + 지표 지연. 이 분열이 GGA 59개 지표 합의를 어떻게 조형했는지가 Stage 1 분석의 핵심 질문이 될 것.

---

## 3. 비국가 행위자(Non-State Actor) 신호 분석

### 토착민 연합의 UNFCCC 진입 전략

**4개 NSA 엔티티 모두 탐지 성공**:
- **IIPFCC** (International Indigenous Peoples' Forum on Climate Change): 2건
- **AIPP** (Asia Indigenous Peoples Pact): 2건
- **IWGIA** (International Work Group for Indigenous Affairs): 1건 (AIPP_IWGIA joint)
- **LCIPP** (Local Communities and Indigenous Peoples Platform): 5건

**핵심 발견**:

> "The IIPFCC affirms that implementation must: Be in accordance with the directive: Parties should, when taking action to address climate change, respect, promote, and consider their respective obligations on human rights… **the rights of indigenous peoples**"

**출처**: `round4_curated-91062f04b898` (IIPFCC_submission_traditional_knowledge.pdf)

**IR 분석**: IIPFCC가 Paris Agreement "preamble" 언어를 직접 인용하여 자신들의 권리 주장을 협약 텍스트로 정박(anchoring). 이는 비국가 행위자가 국가 간 협약의 규범적 언어를 자신의 advocacy 도구로 전용하는 norm entrepreneurship 전략(Finnemore & Sikkink, 1998).

**플랫폼 전략**: LCIPP_COP30_notification은 COP30 session에서 토착민이 공식 관찰자를 넘어 "active participants"로 참여하는 공식 통보. UNFCCC 내 비국가 행위자의 제도적 공간 확장 추적.

---

## 4. 협상 드래프트 진화 분석 (GGA)

### Draft Text 3 브라켓 분포 (17/11/2025 23:55)

핵심 브라켓 패턴:
```
[shall][should] designate... (paragraph 2: chair_letter / JTWP 조항)
[Recalls][Reaffirms]... (preamble: 원칙 강도 미결)
[Notes][Welcomes] the Baku to Belém Roadmap (재정 약속 강도 미결)
```

**출처**: `round4_curated-e4a23ee43d09` (GGA_COP30_draft_text_3.pdf)

**IR 분석**: 브라켓 패턴은 협상 power asymmetry의 텍스트 지표. "[shall][should]"는 개도국(shall 반대) vs 선진국(should 선호) 분열. "[Recalls][Reaffirms]"는 원칙 강화(Reaffirms) vs 현상 유지(Recalls) 분쟁. 이 패턴이 COP30 마감 전까지 해소되는 방식이 결정문 강도를 결정.

**Stage 1 활용**: GGA draft 버전 비교(Draft 3 vs 최종 FCCC/PA/CMA/2025/L.25)로 어떤 브라켓이 어떤 방향으로 해소되었는지 추적 가능 — 협상력 분포의 텍스트 지표.

---

## 5. C2ES 분석 보고서: 외부 싱크탱크의 의제 틀짜기

**핵심 평가**:
> "COP29 Baku outcomes represent a 'finance architecture COP' — NCQG agreed at $1.3T but adaptation finance share not ring-fenced. Loss and damage operationalization progressed but fell short of SIDS/LDC demands"

**출처**: `round4_curated-589fd2c30536` (C2ES_COP29_Baku_outcomes.pdf)

**IR 분석**: C2ES(워싱턴 싱크탱크)의 COP29 평가는 "finance architecture" 프레임 — NCQG의 1.3T가 적응 재정 보장 없는 총량 합의임을 비판. 이 외부 평가가 COP30/BRA 의장의 "adaptation is the heart" 프레임 전환에 어떤 role을 했는지 추적 가능 (epistemic community → presidency agenda-setting).

---

## 6. Round 3 IR 교수에 대한 핵심 질문

> **COP28(UAE)/COP29(AZE)/COP30(BRA) 연속 의장국이 모두 에너지 수출국 또는 자원 보유 개도국이라는 사실이, UNFCCC GGA 협상의 결과물(지표의 voluntary성, 재정 약속의 soft-law 형태)에 구조적으로 영향을 미쳤는가?**
>
> 구체적으로: 의장국이 (a) 자국의 국제 협상 이익과 (b) UNFCCC 의장으로서의 중립성 사이에서 agenda-setting 편향을 보일 때, 이를 탐지하는 텍스트 기반 방법론이 가능한가?
>
> CINA의 chair_metadata(32건, COP28/29/30 시계열)는 이 질문에 답하기 위한 최소 충분 조건인가, 아니면 COP26(UK)/COP27(EGY)까지 확장해야 하는가? (Stage 2 GNN 노드 설계에 직접 영향)

---

## 첨부 데이터 경로

- `data/processed/chair_metadata.jsonl` — 32건 (COP28/29/30 시계열 포함)
- `data/processed/non_state_actor_signals.jsonl` — 20건 (NSA entity 포함)
- `data/processed/documents.jsonl` — 114건 (round3-v1.4)
- `data/processed/frame_distribution_round3.json` — 5범주 분포
- `data/processed/refinement_round3_stats.json` — CR3 compliance 검증 포함
