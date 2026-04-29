# 03. Data Architecture — 데이터 수집·스키마

> 본 문서는 CINA의 데이터 파이프라인: 어디서, 무엇을, 어떻게 수집하고, 어떤 스키마로 저장하는지를 서술한다.

## 1. 데이터 소스

### 1.1 Primary Sources (1차 데이터)

| ID | Source | Format | Access | 용도 |
|----|--------|--------|--------|------|
| S1 | **UNFCCC Submission Portal** | PDF, HTML | https://unfccc.int/documents | 각국 공식 입장문 (SBI, SBSTA, CMA 제출 문서) |
| S2 | **NDC Registry** | PDF | https://unfccc.int/NDCREG | 국가 NDC 적응 섹션 |
| S3 | **IISD ENB (Earth Negotiations Bulletin)** | HTML, PDF | https://enb.iisd.org/ | 협상 일일 요약, 협력/대립 인터랙션 |
| S4 | **NegotiateCOP** | API (RAG) | https://negotiatecop.org/ | 문서 시맨틱 검색 보조 |
| S5 | **Castro et al. 2025 ENB Dataset** | CSV, JSON | Nature Scientific Data supplement | 협력/대립 ground truth |

### 1.2 Secondary Sources (참조)
- IPCC AR6 WG2 (적응 과학 근거)
- World Bank CCDR (Country Climate and Development Reports)
- Climate Action Tracker (국가별 정책 평가)

### 1.3 데이터 수집 윤리 및 라이선스
- UNFCCC 공식 문서: 공개, UN 재이용 정책 준수
- ENB: IISD의 CC BY-NC-SA 라이선스. 연구 목적 재이용 가능.
- 개별 국가 기밀 문서는 수집하지 않음.

---

## 2. 원시 데이터 디렉토리 구조

```
data/
├── raw/
│   ├── unfccc_submissions/
│   │   └── cop30/
│   │       ├── sbi_2025/
│   │       │   ├── brazil_sbi_2025_adaptation.pdf
│   │       │   └── ...
│   │       └── sbsta_2025/
│   ├── ndcs/
│   │   ├── brazil_ndc_2023_updated.pdf
│   │   └── ...
│   ├── enb_summaries/
│   │   ├── cop30_day1.html
│   │   └── ...
│   └── castro_2025/
│       └── enb_interactions_1995_2023.csv
├── processed/
│   ├── documents.jsonl       # 문서 전체 텍스트 + 메타
│   ├── stances.jsonl         # Stage 1 출력
│   ├── graph.pkl             # Stage 2 그래프 객체
│   └── embeddings.npy        # R-GAT 학습 결과
├── calibration/
│   └── expert_coded_stances_sample.csv  # 50개 전문가 코딩 샘플
└── llm_logs/
    └── 2026-04-24/
        └── stage1_extraction.jsonl
```

---

## 3. 문서 스키마 (Document Schema)

수집 후 모든 문서는 다음 JSON 스키마로 정규화 (`documents.jsonl`):

```json
{
  "doc_id": "UNFCCC-SBI-2025-L3",
  "source": "unfccc_submission",
  "cop_session": "COP30",
  "subsidiary_body": "SBI",
  "document_type": "draft_conclusions",
  "date": "2025-06-18",
  "authors": ["Brazil"],
  "topics": ["adaptation", "GGA"],
  "language": "en",
  "full_text": "...",
  "paragraphs": [
    {"para_id": 1, "text": "..."},
    {"para_id": 2, "text": "..."}
  ],
  "url": "https://unfccc.int/documents/...",
  "retrieved_at": "2026-04-24T14:30:00Z",
  "sha256": "abc123..."
}
```

### 3.1 필수 필드
- `doc_id`: 전역 고유 ID (UNFCCC 공식 번호 우선)
- `date`: ISO 8601
- `authors`: 문서의 국가·그룹 저자 (UNFCCC 공식 목록)
- `sha256`: 재현성을 위한 hash

### 3.2 토픽 레이블링
이슈 레이블(`topics`)은 두 단계로:
1. 키워드 기반 1차 필터 (adaptation, GGA, finance, L&D, NAP, just transition)
2. LLM 2차 확인 (프롬프트: "이 문서는 다음 이슈 중 어느 것을 주로 다루나?")

---

## 4. 스탠스 스키마 (Stance Schema)

`stances.jsonl`의 각 레코드:

```json
{
  "stance_id": "brazil-gga_ind-cop30-001",
  "country": "Brazil",
  "iso3": "BRA",
  "issue": "GGA-IND",
  "issue_description": "Global Goal on Adaptation indicators",
  "cop_session": "COP30",
  "date_context": "2025-11-10",
  
  "stance_score_raw_samples": [0.65, 0.58, 0.70, 0.62, 0.68],
  "stance_score_mean": 0.646,
  "stance_score_std": 0.045,
  "stance_score_calibrated": 0.58,
  "ci_lower_95": 0.48,
  "ci_upper_95": 0.74,
  
  "stance_category": "conditional_support",
  "key_demands": [
    "Quantitative indicators with capacity context",
    "Regional flexibility"
  ],
  "red_lines": [
    "No universal metrics without means of implementation"
  ],
  "flexibility_signals": [
    "phased implementation acceptable",
    "open to sectoral customization"
  ],
  
  "evidence_quotes": [
    {
      "quote": "Brazil calls for measurable indicators that reflect national capacities...",
      "source_doc_id": "UNFCCC-SBI-2025-L3",
      "paragraph": 12,
      "confidence": 0.9
    }
  ],
  
  "epistemic_alignment": {
    "cites_ipcc": true,
    "cites_leg_technical": false,
    "aligns_with_expert_proposal": "partial"
  },
  
  "extraction_metadata": {
    "model": "claude-opus-4-7",
    "model_id": "claude-opus-4-7",
    "temperature": 0.3,
    "samples": 5,
    "prompt_version": "v1.2",
    "prompt_hash": "sha256:...",
    "extracted_at": "2026-04-24T15:00:00Z",
    "extraction_latency_sec": 42.1
  }
}
```

### 4.1 `stance_category` 분류 체계
- `strong_support` ($s \geq 0.7$)
- `support` ($0.3 \leq s < 0.7$)
- `conditional_support` ($0.1 \leq s < 0.3$ with flexibility_signals ≥ 1)
- `neutral_or_silent` ($-0.1 < s < 0.1$)
- `oppose` ($-0.7 < s \leq -0.1$)
- `strong_oppose` ($s \leq -0.7$)

### 4.2 `epistemic_alignment` — 이 필드의 의의
Epistemic Communities 이론을 구현하는 핵심 필드. 국가의 입장이:
- 과학 문헌(IPCC) 기반인가
- 기술 body (LEG, TEC) 제안과 정렬되는가
- 전문가 원안과 얼마나 일치하는가

COP30의 "Rube Goldberg" 사례에서 브라질의 `epistemic_alignment.aligns_with_expert_proposal` 값이 "partial"에서 "divergent"로 이동하는 패턴을 회고적으로 식별할 수 있는가가 핵심 검증 과제.

---

## 5. 그래프 스키마 (Graph Schema)

PyTorch Geometric HeteroData 객체로 저장:

```python
from torch_geometric.data import HeteroData

data = HeteroData()

# 노드 피처
data['country'].x = torch.tensor(...)  # [N, d_country]
data['issue'].x = torch.tensor(...)    # [I, d_issue]
data['group'].x = torch.tensor(...)    # [K, d_group]

# 엣지 (예시)
data['country', 'has_stance', 'issue'].edge_index = ...  # [2, E_ci]
data['country', 'has_stance', 'issue'].edge_attr = ...   # [E_ci, d_stance]

data['country', 'cooperates_with', 'country'].edge_index = ...
data['country', 'cooperates_with', 'country'].edge_attr = ... # weight, temporal

data['country', 'member_of', 'group'].edge_index = ...
```

### 5.1 국가 노드 피처 (d_country=32)
- GDP per capita (normalized)
- CO2 emissions per capita
- Adaptation vulnerability index (ND-GAIN)
- Climate finance contributor/recipient flag
- Regional one-hot (Africa, Asia, Europe, ...)

### 5.2 이슈 노드 피처 (d_issue=16)
- Issue category (감축/적응/재원/...)
- Technical complexity (전문가 의존도)
- Historical contention level
- Paris Agreement Article reference

### 5.3 엣지 가중치
- `has_stance`: stance_score ∈ [−1, +1]
- `cooperates_with`: 과거 공동 발언 빈도 (Castro 2025 데이터)
- `member_of`: 1/0 binary

---

## 6. 데이터 수집 스크립트 명세

`src/collect/run.py` 인터페이스:

```bash
python src/collect/run.py \
  --source unfccc \
  --cop 30 \
  --sector adaptation \
  --countries Brazil,EU,US,China,India,AOSIS,LDCs,African_Group,AILAC,Arab,LMDC,Japan,Korea,Australia,Saudi \
  --output data/raw/unfccc_submissions/cop30/ \
  --retry 3 \
  --rate-limit 1.0
```

### 6.1 Rate limiting
UNFCCC/IISD에 대한 부하 최소화:
- 기본 delay: 1초/요청
- User-Agent: `CINA-Research/2.0 (academic; contact: zxsa0716@kookmin.ac.kr)`
- robots.txt 준수

### 6.2 재시도·체크포인트
모든 수집은 state file (`.cina_collect_state.json`) 기록. 중단 후 재개 가능.

---

## 7. 데이터 품질 검증

### 7.1 자동 검증 (Stage 0.5)
- **완결성**: 모든 주요 국가(20개)에 대해 이슈당 최소 1개 문서 확보 여부
- **일관성**: 동일 국가의 상충 스탠스 flag (ci_upper < 0 while stance_score > 0)
- **evidence grounding**: 모든 stance에 evidence_quote 1개 이상

### 7.2 수동 검증 (Calibration set)
- $n=50$ (국가, 이슈) 쌍을 무작위 샘플링
- Heedo + (가능하면) 지도교수 또는 기후 전공자가 독립 코딩
- Krippendorff's α ≥ 0.7 이 목표

---

## 8. 데이터 공개 정책

CINA의 재현성을 위해 다음을 공개:
- 전처리된 `documents.jsonl` (원문 저작권 문제 없는 인용 길이만)
- `stances.jsonl` 전체 (LLM 추출 결과)
- Calibration set (익명화된 expert codings)
- 모든 프롬프트 버전

공개 대상: Zenodo DOI + GitHub repo (논문 acceptance 이후).

---

## 다음 문서
- [04_stage1_stance_extraction.md](04_stage1_stance_extraction.md): Stage 1 프롬프트·calibration 상세
