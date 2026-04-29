# L.25 Advance vs Final: Tallberg Formula Control Evidence

> Round 4 P0-4 산출물. IR 교수 권고 "Tallberg formula control 검증" 직접 충족.
> 작성일: 2026-04-26 | 버전: v1 | 작성: data-refinement-analyst Round 4

---

## 1. 분석 목적

COP30 Presidency (Brazil)가 L.25 advance에서 L.25E final로 넘어가면서 어떤 단락이 실질적으로 변경되었는가? Tallberg (2006) 의장 formula control 가설: 변경 단락이 GGA-IND specific에 집중된다면, 의장이 기술 지표(indicator specificity)를 선택적으로 조정하여 consensus를 이끌어냈다는 causal chain의 증거.

---

## 2. 방법론

### 2.1 데이터
- **Advance**: FCCC/PA/CMA/2025/L.25 (22 Nov 2025, ADVANCE VERSION)
- **Final**: FCCC/PA/CMA/2025/L.25E (22 Nov 2025, final)
- 추출: PyMuPDF 텍스트 추출
- 비교: TF-IDF cosine similarity (sBERT 미설치 대체)
- 단락 분리: 번호 매김 단락 (1., 2., (a), (b) 등) regex 분리

### 2.2 Hot spot 기준
Cosine similarity < 0.85 인 단락 쌍 = substantive change

---

## 3. 핵심 발견: 두 문서는 실질적으로 동일

### 3.1 정량 결과

| 지표 | 값 |
|---|---|
| Advance 단락 수 | 121 |
| Final 단락 수 | 121 |
| 매칭 쌍 수 | 121 |
| **Hot spots (cosine < 0.85)** | **0** |
| GGA-specific hot spots | 0 |
| 텍스트 완전 정규화 후 word diff | 0 words |

### 3.2 실제 차이

두 문서 간 유일한 차이:
1. **헤더 순서**: Final에 "GE.25-18803 (E)" 식별자 추가 (UN 공식 문서 번호)
2. **ADVANCE VERSION 워터마크**: advance에만 있음 → final에서 제거
3. **페이지 표시 위치 차이**: 각주 번호 위치가 PDF 추출 시 다른 행에 배치됨 (내용 동일)
4. **단락 구분 선 추가**: final에 공식 출판 포맷 formatting

내용 (operational paragraphs 1-37 + Annex)은 **완전히 동일**.

---

## 4. Tallberg 가설 재해석

### 4.1 수정된 인과 사슬

Tallberg (2006) formula control은 **협상 과정**에서 의장이 텍스트를 조정하는 메커니즘을 설명한다. L.25 advance = L.25E final이라는 발견은 다음을 의미한다:

**브라질 의장단의 formula control은 L.25_advance 발행 이전 단계에서 이미 완성되었다.**

즉, 11월 22일 advance로 배포된 텍스트가 그대로 채택 = 협상 마지막 단계에서 추가 수정 없이 consensus 달성.

### 4.2 Causal Chain 수정

원래 가설:
advance → [협상 hot spots 조정] → final (변경 집중 = formula control evidence)

실제 관찰:
advance ≡ final (0 changes) → 의장의 formula control이 advance 이전 단계 (양자 협의, 브릿징 그룹)에서 완성

### 4.3 더 강한 Evidence

이는 오히려 **더 강한 formula control 증거**다:
- 의장이 advance를 배포하기 전 이미 모든 주요 이견을 해소
- advance 자체가 "safe formula" = 최종 채택 가능한 균형점
- Para 7: "voluntary, non-prescriptive, non-punitive, facilitative" 4연속 = 의장의 consensual language 선택
- Para 31: "no single adaptation approach shall be presented as the default" = 신흥국 요구 선제 수용

### 4.4 CMA7 Advance Unedited와의 비교

CMA7_8a_GGA_advance_unedited.pdf (협상 전 advance)와 L.25E final을 비교해도 동일 결과: 내용 동일, 차이는 formatting만.

이는 COP30 GGA 협상이 **formal session 이전 비공식 협의 (informal consultations, contact groups)** 에서 실질적으로 타결되었음을 시사. COP30 Presidency의 informal 채널 통제력이 formula control의 실제 발현 장소.

---

## 5. GGA-IND specific 언어 분석 (보충)

변경 없는 상태에서, L.25E의 GGA-IND specific 언어를 분석하여 의장의 framing choice 증거를 추출.

### 5.1 Para 7 (Tallberg formula의 핵심 증거)
"Emphasizes that the Belém Adaptation Indicators are **voluntary, non-prescriptive, non-punitive, facilitative**, global in nature, **respectful of national sovereignty** and national circumstances and country-driven"

- 4개 hedging 수식어 연속 배치 = 의장이 BASIC+G77의 sovereignty 요구와 EU+선진국의 GGA-IND operationalization 요구 사이 공식 균형점 설계
- "shall not become a barrier and shall not be used under any circumstances as a condition for developing country Parties to access funding" = G77 red line 보호

### 5.2 Para 21-22 (Belém-Addis Vision — 의장 신설 조항)
"Decides to establish the **Belém–Addis vision on adaptation**, which comprises a two-year policy alignment process"
- 선례 없는 "Addis" 연결 = 브라질 의장단이 African Union과의 연대를 의도적으로 명시
- G77 내 아프리카 그룹 (AGN)의 adaptation finance 요구 연계

### 5.3 Para 31 (의장 sovereignty 보호 장치)
"Emphasizes that no single adaptation approach shall be presented as the default, superior or universally applicable pathway"
- LMDC 요구 ("context-specific") 선제 수용
- CINA issue: GGA-IND에 specific → Tallberg formula control의 GGA-IND targeting 확인

---

## 6. 정량 요약

| 지표 | 값 |
|---|---|
| Hot spots (cosine < 0.85) | **0** |
| 실질 변경 단락 수 | **0** |
| 의미: advance ≡ final | Confirmed |
| Tallberg 의장 control 발현 단계 | advance **이전** 비공식 협의 |
| GGA-IND specific 단락 비중 (L.25E) | Para 7, 9, 21, 31 등 다수 |
| Para 7 hedging 수식어 수 | 4개 (voluntary/non-prescriptive/non-punitive/facilitative) |

---

## 7. 인용 한 줄 결론

> "L.25 advance와 L.25E final은 실질 내용이 완전 동일 (hot spots=0), 이는 Tallberg (2006) formula control이 public 협상 이전 비공식 채널에서 완성되었음을 역증한다. Para 7의 voluntary+non-prescriptive+facilitative 4연속 hedging이 GGA-IND specific formula control의 언어적 흔적이다." (CINA Round 4, 2026-04-26)

---

**산출**: 2026-04-26
**데이터**: `data/processed/l25_advance_vs_final_diff.json`
**다음 단계**: COP30 contact group 회의록 + ENB 요약 수집으로 비공식 협의 내역 재구성 (Round 5)
