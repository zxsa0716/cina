---
assigned_to: policy-science-professor
model: opus
round: 2
priority: P0
issued_at: 2026-04-25
deadline: round_2_close (after T02 refinement completes)
depends_on:
  - council_sessions/round_2/refinement/professor_input/policy_sci_pack_v2.md
  - council_sessions/round_2/refinement/quality_report.md
  - council_sessions/round_1/policy_science/critique.md
  - council_sessions/round_1/synthesis/cross_review.md
---

# T03 (Round 2) — 정책학 교수: 권고 반영 검증 + 심화 비판

## 1. 목적
Round 1 정책학 critique에서 제기한 3대 비판(C1 MLG, C2 NATO 4축, C3 Implementation Gap)이 (a) team-lead의 처리 결정과 (b) Round 2 데이터·스키마에 어떻게 반영되었는지 검증한다. 동시에 신규 corpus(70-100건)에 대한 정책학 심화 비판을 수행한다.

## 2. 컨텍스트 — 너의 Round 1 비판이 어떻게 처리되었는지

team-lead가 cross_review.md에서 결정한 사항:

| Round 1 비판 | 처리 결정 | Round 2 반영 |
|------------|---------|-------------|
| C1 MLG (subnational/NSA 노드) | Round 3 검토 (P1 시퀀싱) | 이번 라운드 미반영. 데이터 부담 분산 결정 |
| C2 NATO 4축 (instrument_signals) | **즉시 채택** | Stage 1 prompt v1.3에 4-필드 dict 추가 |
| C3 Implementation Gap (Task E) | Heedo 결정 대기 (HEEDO-1) | Heedo 결정 후 Round 3 시행 |

**team-lead의 정합성 평가**: 너의 권고는 헌법(논문감 + 투트랙)과 정합. 다만 **D5 audience 갈등**(부처 실무 vs 협상단)은 deliverables/(Track A)와 docs/(Track B) 분리로 자연 해소.

## 3. P0 산출물

### 3.1 권고 반영 검증 (반드시)

`council_sessions/round_2/policy_science/verification.md` 작성:
- [ ] §"v1.3 instrument_signals 검증" — Round 2 정제 결과에서 NATO 4축이 실제로 추출되는가? Belém Package 정책 수단 분포 (Round 1 §4 표)와 일치하는가?
  - 6 이슈 × 4 수단 매트릭스의 실증 score 분포 비평
  - "Belém Package가 soft instruments(authority/treasure 약함, nodality 강함)에 집중"이라는 Round 1 가설의 검증 여부
- [ ] §"한국 부처 자료의 수집·정제 적정성" — T01 한국 자료 5-10건이 「녹색·기후외교 추진전략」, 환경부 NAP 3차, KEI/KIEP를 포괄하는가? 누락된 핵심 자료 (e.g. 기재부 GCF 분담률, 국회 기후특위 보고서) 지적
- [ ] §"MLG 미반영의 영향 평가" — C1 권고가 Round 2에 미반영되었는데, JT-ADAPT 이슈에서 비국가 행위자 부재가 분석에 어떤 한계를 만드는가? Round 3 P1 우선순위 확인

### 3.2 심화 비판 (Round 2 corpus 기반)

신규 70-100건 corpus를 본 후 새 비판:
- [ ] §"정책 수단 결합(policy instrument mix)의 빈약성" — 만약 GGA-IND 이슈에서 4축 모두 score < 0.3 이면, 이는 정책 수단의 부재인가 아니면 추출 한계인가? Howlett(2019) instrument calibration 이론 인용
- [ ] §"한국 적응정책 vs 브라질 적응정책 비교 가능성" — Round 2 corpus에 한국·브라질 자료가 모두 있다면, 두 국가의 정책 수단 분포 비교 분석
- [ ] §"Round 1에서 제기하지 못한 새 비판" — 정제 결과를 본 후 발견한 추가 결함 (예: COP29→COP30 자료가 들어왔다면 정책 학습(policy learning) cycle 분석 가능성)

### 3.3 Heedo 결정 사안에 대한 입장

- [ ] §"HEEDO-1 (Scope 확장) 지지 강도" — 너의 Round 1 C3 권고가 헌법 수준 결정으로 격상됨. 다음 질문에 답:
  - Q: 만약 Heedo가 scope 확장을 거부하면, CINA의 정책학적 기여는 어디까지 가능한가?
  - Q: 만약 수용하면, Task E Implementation Realization Rate의 ground truth는 어디서 (KEI 보고서? OECD 적응재원 통계? 국가별 NDC 갱신 데이터?)?

## 4. P1 산출물

- [ ] §"docs/09 브리핑 템플릿 v2 권고" — 너의 Round 1 §3.1 권고 (§0 정부 추진전략 정합성 추가, GGA cross-walk 부록)에 대한 구체적 textual 제안. Round 3에서 docs/09 업데이트 시 반영
- [ ] §"한국 정책학 추가 reference" — Round 1 §5에서 9건 인용. Round 2 corpus를 본 후 추가로 핵심 reference 2-3건

## 5. Rubric 재평가 (Round 1 → Round 2)

5-Dimension Rubric 재평가하여 표 작성:
| Dimension | Round 1 점수 | Round 2 점수 | 변화 근거 |
|-----------|-------------|-------------|----------|
| Theoretical grounding | 3/5 | ?/5 | (instrument_signals 도입 후) |
| Methodological rigor | 3/5 | ?/5 | |
| Empirical validity | 2/5 | ?/5 | (corpus 70-100건 확보 후) |
| Policy strategic relevance | 2/5 | ?/5 | (한국 부처 자료 후) |
| Clarity & reproducibility | 4/5 | ?/5 | |

목표: 평균 ≥ 3.5/5 (Round 1: 2.8/5).

## 6. 산출물 위치
- 메인 비평: `council_sessions/round_2/policy_science/critique.md`
- 권고 반영 검증: `council_sessions/round_2/policy_science/verification.md`
- (선택) docs/09 textual 제안: `council_sessions/round_2/policy_science/briefing_template_v2_proposal.md`

## 7. ir-political-professor와의 cross-review 예고
team-lead가 두 critique 모두 수령 후 합의·불일치 식별. 너의 입장이 IR과 충돌할 가능성 있는 항목:
- HEEDO-1 (scope 확장) — IR 교수는 이행이 model scope 밖이라고 주장할 수 있음
- AOSIS 변수 처리 — 너의 vulnerability metric vs IR의 norm entrepreneurship (cross_review §3 D2: 양 변수 병기로 결정됨)

이 두 항목에서 너의 입장을 강화하려면 어떤 추가 evidence·이론이 필요한가를 §"IR과의 합의·불일치" 절에 정리.

## 8. 본 task의 헌법 정합성
- ✓ 헌법 §1 논문감: 정책학 비판 통합으로 reviewer pool 확대 (PA, GEC 모두 reviewer 가능)
- ✓ 헌법 §2 COP30 회고: 정책 수단 분포가 Belém Package 사후 평가의 핵심
- ✓ 헌법 §3 투트랙: 한국 부처 자료 검증이 Track A 직접 강화
- ✓ 헌법 §4 LLM-GNN-LLM: 신규 변수가 파이프라인 입출력에 통합되었는지 검증

**작업은 T02 refinement (policy_sci_pack_v2.md) 완료 후 시작.**
