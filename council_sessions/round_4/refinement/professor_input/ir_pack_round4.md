# Round 4 — IR/Political Science Professor Input Package

> 발신: data-refinement-analyst
> 수신: ir-political-professor
> 작성일: 2026-04-26

---

## 1. P0-3: Realist B0 Baseline F1 결과

Round 3 권고 "realist baseline을 먼저 증명하라" 직접 충족.

### 핵심 결과

| 지표 | 값 | 해석 |
|---|---|---|
| 사용 변수 | CO2 per capita, share global CO2, log GDP | Realist 3-factor |
| Similarity metric | Cosine (z-score normalized) | |
| K (top-K prediction) | 75 | 동일 그룹 쌍 수 |
| Truth pairs | 75 (그룹 멤버십 pseudo-truth) | |
| **F1** | **0.560** | |
| Random baseline | ~0.44 | |
| 가설 F1 < 0.70 | **CONFIRMED** | realism insufficient |

### F1 = 0.560 해석

Random baseline 대비 +12pp로 realism이 전혀 무용하지는 않으나, 실용적 예측 모델로는 불충분.

대표적 예측 오류:
- **USA-SAU** (cosine=0.889): 대형 고배출 경제 유사 → realist 예측 협력
  → 실제: 다른 협상 그룹 (UMBRELLA vs ARAB/G77). 적응재원 입장 대립.
- **BRA-USA** (cosine=-0.863): 물질 차이 → realist 예측 비협력
  → 실제: BRA는 G77, USA는 UMBRELLA이나, 양자 diplomatic 협의 active (브라질-미국 기후협력)
- **BRA-KEN** (cosine=낮음): 경제 구조 이질 → realist 예측 비협력
  → 실제: G77 동일, AGN-G77 연대 strong

### 교수 검토 요청

1. **Pseudo-truth의 타당성**: 그룹 멤버십 기반 협력 ground truth의 이론적 근거 평가 바람. IR 이론에서 "동일 협상 그룹 = cooperative" 전제가 얼마나 강한가?
2. **ENB Castro 2025 대체**: 실제 협력 지표 (공동 제출서, co-sponsoring, joint statement)로 대체 시 F1이 어떻게 변할 것으로 예측? Round 5 collector에 ENB dataset 수집 우선순위 부여 필요한지?
3. **realist 변수 확장**: 예를 들어 vulnerability index (ND-GAIN), historical emissions, Annex I/non-Annex I status를 추가하면 realist baseline이 개선될지 이론적 판단 바람.

---

## 2. P0-4: L.25 Advance vs Final — Tallberg 가설 재해석

### 핵심 발견

**두 문서는 실질적으로 동일** (hot spots = 0, 텍스트 word diff = 0).

| 지표 | 값 |
|---|---|
| Advance 단락 | 121 |
| Final 단락 | 121 |
| Hot spots (cosine < 0.85) | **0** |
| 실질 변경 단락 | **0** |
| 차이 | 헤더 formatting + footnote 위치만 상이 |

### Tallberg 가설 재해석

**원래 가설**: L.25 advance → final 과정에서 GGA-IND specific 단락이 집중 변경 = formula control evidence.

**실제 관찰**: advance ≡ final → 의장의 formula control이 advance 배포 **이전** 단계에서 완성.

**수정된 인과 사슬**:
[비공식 협의 (informal consultations, contact groups)] → [formula crystallization] → [L.25 advance 배포] → [formal adoption without change]

이는 Tallberg (2006) formula control의 **더 강한 증거**:
의장단이 advance 배포 전에 이미 모든 이견을 해소한 "pre-crystallized formula" 제시.

### Para 7 언어 분석 (formula control의 언어적 흔적)

"voluntary, non-prescriptive, non-punitive, facilitative" (4개 hedging 연속)
+ "respectful of national sovereignty"
+ "shall not become a barrier"
+ "shall not be used under any circumstances as a condition...to access funding"

이 언어는 의장이 사전에 BASIC/G77 red line을 식별하고 선제 수용한 증거.

### 교수 검토 요청

1. **Tallberg 수정 해석의 이론적 타당성**: "advance ≡ final = stronger formula control" 논리가 Tallberg (2006) 원문과 정합하는지 평가 바람. 대안 해석 (예: advance가 이미 lowest common denominator = 의장 influence 없음)을 반론으로 제시할 수 있는가?
2. **비공식 협의 재구성**: COP30 contact group 회의록, ENB daily 요약, COP30 presidency closing statement에서 informal 채널 formula control 과정 재구성 가능한지? Round 5 collector 우선순위 제안 바람.
3. **COP28 → COP29 → COP30 trajectory**: advance/final 비교를 COP28 (UAE), COP29 (Azerbaijan)에도 적용하면 Tallberg 효과가 시계열적으로 증가하는지 분석 가능. 이 비교의 학술적 가치 평가 바람.

---

## 3. 이론 통합 이슈 — IR 교수 판단 필요

### 이슈 A: Putnam Level I vs Level II 분리

현재 CINA는 Level I (국제 협상) 결과물만 분석 (L.25E, ENB summaries).
브라질 Plano Clima는 Level II (국내 정치) 결과물.

교수 제안 사항: Plano Clima 채택 과정 (2024년 CIM 심의 과정)을 Level II win-set 증거로 사용하는 것이 타당한가? CIM의 20개 부처 구성이 win-set 폭을 좁혔는지 확인 방법?

### 이슈 B: Constructivist vs Realist 설명력

F1 비교 (Realist B0 = 0.560 vs CINA GNN 목표 ≥ 0.80)에서 ΔF1 = 0.24+를 "constructivist/framing 변수 기여"로 해석하는 것에 이론적 동의하는가?

아니면 ΔF1의 일부는 단순히 "more information" (더 많은 변수)의 효과일 수 있어, 이론적 주장을 약화시킬 수 있다는 반론을 선제적으로 다루는 방법을 조언 바람.

### 이슈 C: COP30 의장국 paradox의 논문 claim

현재 CINA의 핵심 claim:
"브라질은 국내 (Organization 67%, IRR 0.714)와 국제 (Nodality 49%, IRR 0.445)에서 다른 instrument-mix를 의도적으로 사용하는 '이중 게임'을 수행한다"

이 claim을 뒷받침하기 위해 추가로 필요한 IR 이론 기반 논거나 반증 테스트를 제안 바람.

---

## 4. Round 5 IR 교수 권고 요청

다음 라운드에서 IR 교수에게 다음 분석을 요청드릴 예정:
1. Tallberg formula control의 비공식 협의 채널 문헌 검토
2. BASIC 그룹 연대 압력 vs 브라질 단독 선호 분리 방법론
3. 19국 협상 그룹 멤버십의 ENB 기반 실증 자료 검토

이에 대한 사전 입력(선행 연구 추천 등)을 Round 5 task 전에 제공해주시면 감사하겠습니다.
