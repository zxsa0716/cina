# 📊 CINA Peer Review Synthesis (10 Reviewers · Pre-Submission)

> **Status**: ☐ Pending all reviewers · ☐ Synthesis in progress · ☐ Complete
> **Reviewers complete**: __ / 10
> **Synthesis date**: ____-__-__
> **Decision gate result**: ☐ Pass — ready for arXiv + Workshop submission · ☐ Fail — P0 fixes required

---

## 1. Decision gate 결과 (자동 판정)

다음 5개 임계치를 모두 통과해야 paper 투고 진행 가능 (PROTOCOL §2.4):

| Gate | Threshold | Actual | Pass |
|------|-----------|--------|------|
| 평균 D2 (방법론 엄밀성) | ≥ 3.5 | __ | ☐ |
| 평균 D4 (정직성/framing) | ≥ 4.0 | __ | ☐ |
| 평균 D5 (재현성) | ≥ 4.0 | __ | ☐ |
| "Major reject" venue 추천 reviewer | ≤ 2명 | __ | ☐ |
| Krippendorff α (10 reviewers) | ≥ 0.5 | __ | ☐ |

**Overall decision**: ☐ READY for arXiv + Workshop · ☐ NEEDS P0 revision · ☐ NEEDS major rework

---

## 2. 점수 행렬 (10 reviewers × 10 dimensions)

| Reviewer | D1 Theory | D2 Method | D3 Empirics | D4 Honesty | D5 Reprod | D6 Policy | D7 Literature | D8 Writing | D9 Novelty | D10 Ready | **Total/50** |
|----------|-----------|-----------|-------------|------------|-----------|-----------|---------------|------------|------------|-----------|--------------|
| R1 Climate Sci  | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| R2 IR Theory    | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| R3 Practitioner | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| R4 Policy Sci   | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| R5 SE / DevOps  | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| R6 ML / NLP     | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| R7 GNN / Network| __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| R8 Stats        | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| R9 Korean KCI   | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| R10 Editor      | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |
| **평균**        | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | **__** |
| **표준편차**    | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ | __ |

**해석**:
- 가장 낮은 평균 차원: D__ (___)
- Reviewer 간 가장 큰 disagreement (highest σ): D__ (분야별 lens 차이가 큰 영역)
- 가장 높은 평균 차원: D__ (___)

---

## 3. Krippendorff α (Inter-reviewer agreement)

10 reviewers × 10 dimensions interval-level data 기반.

- **α (raw)** = ___
- **α (excluding D6 Practical/Policy)** = ___ (분야별 lens 차이가 큰 차원 제외)
- **α (per dimension)**:

| Dim | α | Interpretation |
|-----|---|---------------|
| D1 | __ | |
| D2 | __ | |
| D3 | __ | |
| ... | __ | |

α ≥ 0.7 = high agreement (관찰 신뢰), 0.5-0.7 = moderate, < 0.5 = disagreement (분야별 lens 충돌)

---

## 4. Top 5 가장 자주 언급된 weakness

각 reviewer가 지적한 weakness를 통합하여 가장 자주 언급된 5가지를 추출:

| 순위 | Weakness 요약 | 언급 reviewer 수 | Adversarial 가중치 |
|------|--------------|------------------|------------------|
| 1 | | __/10 | × 1.5 = __ |
| 2 | | __/10 | × 1.5 = __ |
| 3 | | __/10 | × 1.5 = __ |
| 4 | | __/10 | × 1.5 = __ |
| 5 | | __/10 | × 1.5 = __ |

**Top weakness 분류** (cross-cutting vs single-discipline):
- Cross-cutting (3+ reviewers): ...
- Single-discipline (1-2 reviewers): ...

---

## 5. Likely Reject Reasons 통합

각 reviewer의 "Most likely reject reason"을 종합:

| Source reviewer | Reject reason 요약 | 영향 venue |
|-----------------|---------------------|------------|
| R1 Climate | | Climate venue |
| R2 IR | | IR venue |
| R3 Practitioner | | Policy practitioner |
| R4 Policy Sci | | Policy Sciences |
| R5 SE | | SE venue / JOSS |
| R6 NLP | | ACL/EMNLP |
| R7 GNN | | NeurIPS/NetSci |
| R8 Stats | | JASA |
| R9 Korean KCI | | 한국정책학회보 |
| R10 Editor | | 모든 venue |

**Cross-cutting reject reason** (3+ reviewers 동의): ...

---

## 6. Required Revisions Priority Matrix

10 reviewers의 required revisions를 통합:

### P0 (must fix before any submission)
- ≥ 4 reviewers + adversarial weight 통과
- 또는 D2/D4/D5 임계치 미달의 직접 원인

| # | Revision item | 지지 reviewers | Effort estimate |
|---|--------------|----------------|-----------------|
| 1 | | | low / med / high |
| 2 | | | |
| 3 | | | |

### P1 (should fix before workshop submission)
- ≥ 2 reviewers

| # | Revision item | 지지 reviewers | Effort estimate |
|---|--------------|----------------|-----------------|
| 1 | | | |
| 2 | | | |

### P2 (nice to have)
- 1 reviewer

| # | Revision item | Source | Effort |
|---|--------------|--------|--------|
| 1 | | | |

---

## 7. Venue Recommendation 집계

| Venue | 추천 reviewer 수 | Confidence |
|-------|-----------------|------------|
| Q1 top-tier (GEC, Nature Climate Change) | __ / 10 | low / med / high |
| Q2 mid-tier (Climate Policy, GEP, Policy Sciences) | __ / 10 | |
| Workshop (NeurIPS CCAI 2026) | __ / 10 | |
| KCI domestic (한국정책학회보) | __ / 10 | |
| arXiv preprint only | __ / 10 | |
| Reject | __ / 10 | |

**Consensus venue**: ___
**Reasoning**: ...

---

## 8. 최종 권고 — 다음 단계

### Path A — P0 통과 시 (recommended path)
1. P0 항목 우선 수정 (예상 소요: __ 일)
2. arXiv preprint 업로드 (1주)
3. NeurIPS CCAI 2026 Workshop short paper 작성 (4-page, 2주)
4. 한국정책학회보 별도 한국어 단저자 논문 작성 (2-3개월)
5. 6-12개월 longitudinal extension + real expert validation 후 GEC/GEP 본 투고

### Path B — P0 미통과 시 (rework required)
1. P0 + P1 항목 모두 수정 (예상 소요: __ 주)
2. 동일 protocol로 재검토 (synthesis v2)
3. 통과 시 Path A로 진행

### Path C — Major reject (3+ reviewers reject)
1. METHODOLOGY_ADVANCEMENT_ROADMAP의 E5-E8 (longitudinal + expert + multi-lingual + causal) 우선 실행
2. 6-12개월 후 paper 전면 재작성
3. 새로운 synthesis 세션 진행

---

## 9. Honesty disclosure (must remain)

본 synthesis는 **LLM 페르소나 시뮬레이션 기반 simulated peer review**의 결과이며, 실제 외부 학자 reviewer 섭외와 동등한 효력을 가지지 않는다. 본 결과는 (a) 자체 약점 발굴 도구, (b) 실제 reviewer 거절 사유 사전 시뮬레이션, (c) 실제 외부 reviewer 섭외 시 baseline으로만 활용된다. CRITICAL_REVIEW.md §3.2의 simulated panel 한계 진술이 본 synthesis에도 동등하게 적용된다.

향후 KEI / KAIST / MOFA / GEP 편집위원 등 실제 외부 학자에게 동일한 rubric을 보내 비교 검증할 것을 권고한다.

---

## 10. Aggregated open questions for the author

10 reviewers의 "Open questions for the author"를 통합:

1. ...
2. ...
3. ...
4. ...
5. ...
6. ...
7. ...
8. ...

---

**작성**: 자동 (orchestrator 스크립트가 10개 review.md 파싱 후 채움)
**검토자**: Heedo Choi (최희도)
**다음 commit**: synthesis 완료 시점에서 paper.md를 P0 사항에 따라 수정한 commit
