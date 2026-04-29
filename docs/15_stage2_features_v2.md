# 15. Stage 2 Features v2 — Procedural Authority Encoding

> Round 1 IR 교수 결정적 권고 (CR2) 반영. R-GAT 모델에 의장국·co-facilitator·pen-holder 변수를 노드/엣지 수준에서 추가한다.
>
> **결정**: Heedo 2026-04-25 accept. 적용 시점: Round 2-3 그래프 학습.

---

## 1. 동기

`docs/05_stage2_graph_analysis.md §3.6` 의 `epistemic_divergence_score` 는 Belém Adaptation Indicators "Rube Goldberg" 사건의 회고 검증을 약속하지만, 현 v1 모델에는 **의장국 procedural authority (텍스트 초안권 + 의제 통제)** 가 없다. 이 변수 없이는 다음을 설명 못함:

- 왜 브라질이 전문가 안을 재작성할 수 있었는가? → procedural pen-hold
- 왜 다른 G77 국가는 그 결과에 묶였는가? → text-control diffuses through chair
- 왜 EU 같은 협상력 1위 국가가 결과적으로 따랐는가? → de facto consent under chair drafting

IR 표준 reference: **Tallberg 2010** *International Studies Quarterly* "Explaining the institutional foundations of European Union negotiations" — chair power as independent variable. **Depledge 2007** *Global Environmental Politics* — UNFCCC presidency studies.

---

## 2. 추가 변수 (3 layer)

### 2.1 Country Node Feature (`d_country` 32 → 35)

```python
country_features = {
    # v1 — 그대로 유지
    "gdp_per_capita_log": float,
    "co2_per_capita": float,
    # ... 기존 32-dim ...

    # v2 NEW
    "chair_status": int,                 # 0=not, 1=co-facilitator, 2=presidency, 3=consecutive presidency (e.g., COP29→30)
    "pen_holder_score": float,           # [0,1], 평균 회기 내 텍스트 초안권 비율
    "agenda_setting_history": float,     # [0,1], 지난 5년 의제 도입 빈도
}
```

값 산출:
- `chair_status`: UNFCCC 공식 의장단 명단에서 자동 추출
- `pen_holder_score`: SBI/SBSTA L-document 헤더의 "Submitted by" 카운트
- `agenda_setting_history`: ENB 종합 요약에서 "X proposed", "X introduced" 빈도

### 2.2 Issue Node Feature (`d_issue` 16 → 19)

```python
issue_features = {
    # v1 그대로
    ...,
    # v2 NEW
    "pen_holder_country_id": int,       # ISO3 → integer mapping; 이 이슈의 현 의장국
    "co_facilitator_country_ids": list, # SBI/SBSTA 공동 진행자
    "agenda_volatility": float,         # [0,1], 직전 회기 대비 텍스트 변화율
}
```

### 2.3 NEW Edge Type — `drafts_text`

```python
data['country', 'drafts_text', 'issue'].edge_index = ...
data['country', 'drafts_text', 'issue'].edge_attr = ...  # [num_edges, 3]
# edge_attr columns: [drafts_count, last_draft_date_offset_days, contentious_flag]
```

이 엣지가 있으면:
- `Country A — drafts_text → Issue I`: 국가 A가 이슈 I의 텍스트 초안 작성
- 가중치: 빈도 + 최근성 + 논쟁 여부

R-GAT은 이 엣지에 별도 weight matrix 학습 → procedural channel을 stance / cooperation channel과 분리하여 모델링.

---

## 3. 데이터 수집 요구사항 (Round 2 collector 의무)

CR2 채택으로 Round 2 collector는 다음을 추가 수집해야 한다:

1. **COP29 Baku presidency letters** — 의장단의 공식 communication
2. **COP30 Belém presidency letters** (이미 일부 수집됨)
3. **SBI/SBSTA L-document headers** — "Submitted by [chair]" 메타데이터
4. **Co-facilitator nominations** — SBI/SBSTA 의장 announcement (sessions 의제 4번)

이는 `council_sessions/round_2/tasks/T01_collector_task.md`에 명시됨.

---

## 4. 정제 단계 변경 (T02 Round 2)

`data-refinement-analyst`는 다음 자동 채움:

```python
def detect_procedural_role(doc_meta: dict) -> dict:
    """
    L-document, presidency letter 헤더에서 chair_status / pen_holder 자동 추출.
    """
    role = {"is_chair": False, "is_pen_holder": False, "drafts_for": None}
    title = doc_meta.get("title", "")
    if re.search(r"presidency|chair", title, re.IGNORECASE):
        role["is_chair"] = True
    if re.search(r"draft\s+conclusions|prepared\s+by", title, re.IGNORECASE):
        role["is_pen_holder"] = True
    # ...
    return role
```

각 문서의 `procedural_signals` 가 미리 채워진 상태로 Stage 1 LLM에 전달 → LLM은 검증/확장만.

---

## 5. R-GAT 학습 변경

### 5.1 새로운 task: Chair-driven Outcome Prediction
```python
def chair_outcome_loss(emb_country, emb_issue, chair_drafted_text, observed_outcome):
    """
    의장국이 초안 작성한 이슈의 합의 결과를 emb로 예측.
    Belém Indicators 사례에서 'Rube Goldberg' 결과를 모델이 사전 예측하는지 검증.
    """
    chair_emb = emb_country[chair_status_idx]
    issue_emb = emb_issue
    pred = (chair_emb * issue_emb).sum(-1)
    return F.mse_loss(pred, observed_outcome)
```

### 5.2 Joint loss 갱신
$$\mathcal{L} = \lambda_1 \mathcal{L}_{link} + \lambda_2 \mathcal{L}_{coal} + \lambda_3 \mathcal{L}_{outcome} + \lambda_4 \mathcal{L}_{chair}$$

초기값: $\lambda = (0.4, 0.25, 0.20, 0.15)$.

---

## 6. 평가 영향

`docs/07_evaluation_protocol.md`:
- Task A (스탠스 정확도): 영향 없음
- Task B (연합 탐지): chair edge 포함이 NMI/ARI 개선하는지 ablation
- **Task C (결과 예측)**: 핵심 검증 — 의장국 dependence를 모델이 포착하면 contested issue prediction P@10 / R@10 개선되어야 함
- Task D (브리핑 품질): Stage 3 브리핑이 procedural authority 인식 → "남아공이 bridge이지만 의장국 브라질의 pen-hold가 결정적"

### 6.1 Ablation 추가
- A6: drafts_text edge 제거 → Task C 성능 저하 측정
- A7: chair_status feature 제거 → 동일

CR2 적용 후 A6/A7가 실제로 성능 저하한다면 → IR 교수 비판이 옳았음을 empirical 증명.

---

## 7. 위험과 대응

| 위험 | 대응 |
|------|------|
| Procedural metadata 수집 누락 | Round 2 collector T01에서 P0 task로 명시 |
| chair_status 매핑 오류 | UNFCCC 공식 의장단 명단 (`docs/13` §3 별도 표) cross-validate |
| edge type 추가로 학습 불안정 | $\lambda_4$ warm-up: 첫 50 epoch는 0, 이후 0.15로 ramp |
| 모델 복잡도 증가 → 과적합 | Validation set held-out + early stopping patience=30 유지 |

---

## 8. 변경 이력

- 2026-04-25: Round 1 IR 교수 critique CR2 반영. Heedo accept. Round 2-3 학습 시 적용.
