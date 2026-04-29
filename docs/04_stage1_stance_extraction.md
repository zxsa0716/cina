# 04. Stage 1 — Calibrated Stance Extraction

> Stage 1의 목표: 비구조화 협상 문서에서 국가 × 이슈별 스탠스를 불확실성 정량화와 함께 추출.

## 1. 프롬프트 설계 원칙

### 1.1 이론적 접지
프롬프트 자체에 Two-Level Games와 Win-Set 개념을 **시스템 프롬프트**로 포함하여, 모델이 단순 찬반이 아닌 "국내 제약 + 국제 협상" 양면을 고려하도록 유도.

### 1.2 구조화 출력 강제
`response_format=json_schema`로 다음 스키마 강제:

```json
{
  "type": "object",
  "required": ["country","issue","stance_score","evidence_quotes"],
  "properties": {
    "country": {"type": "string"},
    "issue": {"type": "string"},
    "stance_score": {"type": "number", "minimum": -1, "maximum": 1},
    "stance_category": {"enum": ["strong_support","support","conditional_support","neutral_or_silent","oppose","strong_oppose"]},
    "key_demands": {"type": "array", "items": {"type":"string"}, "maxItems": 5},
    "red_lines": {"type": "array", "items": {"type":"string"}, "maxItems": 3},
    "flexibility_signals": {"type": "array", "items": {"type":"string"}, "maxItems": 5},
    "evidence_quotes": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["quote","source_doc_id"],
        "properties": {
          "quote": {"type":"string","minLength":20},
          "source_doc_id": {"type":"string"},
          "paragraph": {"type":"integer"}
        }
      }
    },
    "confidence": {"type":"number","minimum":0,"maximum":1},
    "reasoning": {"type":"string","maxLength":800}
  }
}
```

### 1.3 Few-shot Examples
프롬프트에 2개 예시 포함:

**Example A — 명확한 지지**
```
Input: "The European Union strongly supports the adoption of quantitative indicators under the GGA framework, with measurable targets aligned with UAE Framework on Global Climate Resilience."
Output: {
  "country": "EU",
  "issue": "GGA-IND",
  "stance_score": 0.85,
  "stance_category": "strong_support",
  "key_demands": ["Quantitative indicators", "Alignment with UAE framework"],
  "red_lines": [],
  "flexibility_signals": [],
  "evidence_quotes": [{"quote":"strongly supports... quantitative indicators","source_doc_id":"EU-SBI-2025-01","paragraph":3}],
  "confidence": 0.95,
  "reasoning": "Direct affirmative language with specific technical demands indicates strong support."
}
```

**Example B — 조건부 지지**
```
Input: "India welcomes progress on the GGA but emphasizes that indicator selection must be guided by national circumstances and supported by adequate means of implementation, including finance and technology transfer."
Output: {
  "country": "India",
  "issue": "GGA-IND",
  "stance_score": 0.35,
  "stance_category": "conditional_support",
  "key_demands": ["Means of implementation", "National circumstances respected"],
  "red_lines": ["No mandatory indicators without MoI"],
  "flexibility_signals": ["welcomes progress"],
  "evidence_quotes": [{"quote":"welcomes progress... must be guided by national circumstances","source_doc_id":"IND-SBI-2025-02","paragraph":7}],
  "confidence": 0.85,
  "reasoning": "Positive framing coupled with explicit MoI demand — classic conditional support pattern of Like-Minded Developing Countries (LMDC)."
}
```

---

## 2. 전체 프롬프트 (v1.2)

```text
[SYSTEM]
You are a specialized climate diplomacy analyst. Your task is to extract a country's
stance on a specific climate negotiation issue from official UNFCCC documents.

Theoretical framework:
- A country's stance reflects its "win-set" — the intersection of international and
  domestic political feasibility (Putnam 1988, Two-Level Games).
- Within a stance, distinguish:
  * key_demands: what the country actively seeks
  * red_lines: hard constraints imposed by domestic politics
  * flexibility_signals: language suggesting the country could move

Analyst discipline:
1. Cite only direct quotes from the provided document. No paraphrasing.
2. If the document does not address the issue, return stance_score=0, confidence=0.
3. Use the full [-1, +1] range. Do NOT default to ±0.5.
4. If a country's statement is ambiguous, lower confidence and widen your mental uncertainty.

Output: strict JSON per the provided schema.

[USER]
Country: {country}
Issue: {issue_label} — {issue_description}

Document excerpt:
=== DOC START ===
{paragraphs_joined}
=== DOC END ===
Source document ID: {doc_id}

Extract the country's stance on this specific issue. If the document speaks about other
issues, do NOT invent a stance — return stance_score=0, confidence=0, and empty arrays.

Respond with JSON only.
```

---

## 3. Multi-Sample Aggregation

### 3.1 왜 단일 샘플이 아니라 5회 샘플인가
LLM의 출력은 decode 노이즈를 가진다. 특히 이분법적(지지/반대) 경계 케이스에서 점수가 ±0.1 수준 흔들린다. 5회 샘플로:
- Posterior mean $\hat{\mu}$ 추정 정확도 상승
- Posterior 분산으로 **Bayesian credible interval** 산출 가능
- 이 불확실성이 Stage 3 브리핑의 "확신 수준" 표기에 직접 쓰임

### 3.2 집계 알고리즘
```python
def aggregate_samples(samples: list[dict]) -> dict:
    scores = [s["stance_score"] for s in samples]
    confidences = [s["confidence"] for s in samples]
    
    # 1. Weighted mean (confidence-weighted)
    weights = np.array(confidences) / sum(confidences)
    weighted_mean = np.sum(np.array(scores) * weights)
    
    # 2. Beta-binomial credible interval
    # Rescale [-1,1] -> [0,1]
    rescaled = [(s + 1) / 2 for s in scores]
    alpha_post = 1 + sum(rescaled) * 5
    beta_post = 1 + (5 - sum(rescaled)) * 5  # 5 = k samples
    ci_low_01, ci_up_01 = beta.ppf([0.025, 0.975], alpha_post, beta_post)
    ci_low = ci_low_01 * 2 - 1
    ci_up = ci_up_01 * 2 - 1
    
    # 3. Merge textual outputs (union of demands/red_lines/flex_signals)
    merged_demands = list(set().union(*[s["key_demands"] for s in samples]))
    merged_red_lines = list(set().union(*[s["red_lines"] for s in samples]))
    merged_flex = list(set().union(*[s["flexibility_signals"] for s in samples]))
    
    # 4. Evidence quotes: preserve all, dedupe by text hash
    all_quotes = [q for s in samples for q in s["evidence_quotes"]]
    unique_quotes = dedupe_quotes(all_quotes)
    
    return {
        "stance_score_mean": weighted_mean,
        "ci_lower_95": ci_low,
        "ci_upper_95": ci_up,
        "stance_score_std": np.std(scores),
        "key_demands": merged_demands,
        "red_lines": merged_red_lines,
        "flexibility_signals": merged_flex,
        "evidence_quotes": unique_quotes,
        "sample_stance_scores": scores,
    }
```

---

## 4. Calibration

### 4.1 문제
LLM의 raw stance score는 체계적 편향을 가질 수 있다:
- 친환경 편향: 애매한 statement를 지지로 해석하는 경향
- 규범적 선호: 개도국의 "justice" 언어를 강한 지지로 해석하는 경향

### 4.2 해결: Platt Scaling
**훈련 데이터**:
- Castro et al. 2025 ENB 인터랙션 데이터에서, COP 25–29 기간 **명확한 지지/반대** 케이스 $n_{\text{cal}} \approx 200$ 추출
- 각 케이스에 대해 CINA Stage 1을 동일 문서로 돌려 raw score 생성
- 이진 라벨 $y \in \{0, 1\}$ (반대/지지) 설정

**보정**:
$$P(y=1 | s_{\text{raw}}) = \frac{1}{1 + \exp(a \cdot s_{\text{raw}} + b)}$$

$(a, b)$를 MLE로 추정하여, 보정된 score $s_{\text{cal}} = 2 \cdot P(y=1 | s_{\text{raw}}) - 1$.

### 4.3 Calibration 검증
- Reliability diagram (예측 확률 vs 실제 빈도)
- Expected Calibration Error (ECE): 목표 < 0.1
- Brier score

---

## 5. Issue-Specific 추출 고려사항

각 이슈는 고유한 특성이 있으므로, 이슈별로 prompt hint를 추가:

### GGA-IND (Global Goal on Adaptation Indicators)
- **Hint**: "Watch for positioning on (a) quantitative vs qualitative, (b) mandatory vs voluntary, (c) capacity context clauses."

### ADAPT-FIN (Adaptation Finance)
- **Hint**: "Watch for: (a) multiplier proposals (double/triple/quadruple), (b) contributor base (developed only vs expanded), (c) delivery channels (GCF vs bilateral)."

### L&D-OP (Loss and Damage Fund Operations)
- **Hint**: "Watch for: (a) direct access modalities, (b) eligibility criteria, (c) contribution obligations for large emerging economies."

### NAPs (National Adaptation Plans)
- **Hint**: "Watch for: (a) reporting cycles, (b) technical support mechanisms, (c) iterative vs one-time submission."

### MIT-ADAPT (Mitigation–Adaptation Nexus)
- **Hint**: "Watch for: (a) co-benefits framing, (b) trade-off acknowledgment, (c) integrated vs separate treatment."

### JT-ADAPT (Just Transition with Adaptation)
- **Hint**: "Watch for: (a) protection of vulnerable populations, (b) indigenous rights, (c) gender-responsive adaptation."

---

## 6. Failure Modes and Mitigations

| Failure | Symptom | Mitigation |
|---------|---------|-----------|
| Hallucinated evidence | Quote not in document | Post-hoc regex check against original doc |
| Over-confident extraction | confidence=1 but ambiguous text | Require confidence calibration against expert set |
| Missed subtle opposition | stance_score positive but actually passive resistance | Separate prompt for "passive resistance" pattern |
| Language barrier | Non-English submissions | Translate via DeepL first, annotate `translated: true` |

---

## 7. 실행 시 로그 예시

```jsonl
{"timestamp":"2026-04-24T15:02:14Z","country":"Brazil","issue":"GGA-IND","sample":1,"latency_sec":8.3,"tokens":1247,"cost_usd":0.0412}
{"timestamp":"2026-04-24T15:02:23Z","country":"Brazil","issue":"GGA-IND","sample":2,"latency_sec":7.9,"tokens":1201,"cost_usd":0.0398}
...
```

---

## 다음 문서
- [05_stage2_graph_analysis.md](05_stage2_graph_analysis.md) — R-GAT 구현
