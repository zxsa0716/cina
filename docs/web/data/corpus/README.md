# 📚 CINA v6 Corpus

> **Version**: v6.0.0
> **생성**: 2026-05-09 by build_v6_corpus_index.py
> **총 21개 document** (10 UNFCCC + 5 national + 1 coalition + 1 bib + 5 quantitative) + TF-IDF inverted index

이 폴더는 v5 stance dataset (2,400 records) 을 보강하는 **실제 정책 / 학술 / 정량 문서 corpus**입니다. v6 query engine과 web UI는 이 corpus를 검색 + 인용하여 답변을 grounding합니다.

---

## 📁 폴더 구조

```
data/corpus/
├── README.md                         # 이 파일
├── manifest.jsonl                    # 21개 doc 메타데이터 (sha256, type, tags)
├── search_index.json                 # TF-IDF inverted index (3,417 terms x top-30 docs)
│
├── unfccc_decisions/                 # 10개 UNFCCC L-document
│   ├── paris_agreement_article_7.md  # 조약 본문
│   ├── COP25_madrid_chile_presidency.md
│   ├── COP26_glasgow_pact.md
│   ├── COP27_sharm_LD_fund.md
│   ├── COP28_UAE_consensus.md
│   ├── COP29_baku_NCQG.md
│   ├── COP30_L24_finance_triple.md
│   ├── COP30_L25E_GGA_indicators.md
│   └── FRLD_decision_1_CP28.md
│
├── national_policies/                # 국가 정책 문서
│   ├── KOR_NAP2_carbon_neutrality_act.md
│   ├── BRA_plano_clima_2024.md
│   ├── USA_climate_policy_2025.md
│   ├── EU_green_deal_fit55.md
│   └── OTHER_COUNTRIES_brief.md      # 17개국 brief 통합
│
├── coalition_statements/
│   └── COP30_8_groups_statements.md  # G77, AOSIS, AILAC, EIG, HAC, Umbrella, AGN, LMDC
│
├── academic_references/
│   └── bibliography.bib              # 25+ BibTeX entries (Hood, Howlett, Tallberg etc.)
│
└── quantitative/
    ├── ndgain_2024.csv               # 50개국 vulnerability + readiness
    ├── primap_co2_1990_2023.csv      # 1,700 rows (50국 × 34년)
    ├── oecd_adaptation_finance_2022.csv  # 200 rows (10 donor × 20 recipient)
    ├── cvf_membership.csv            # 62 vulnerable countries
    └── cop_delegation_size.csv       # 300 rows (50국 × 6 COP)
```

---

## 🔑 manifest.jsonl 스키마

각 doc record:

```json
{
  "path": "data/corpus/unfccc_decisions/COP30_L25E_GGA_indicators.md",
  "doc_id": "UNFCCC_FCCC_PA_CMA_2025_L25E",
  "title": "Belém Adaptation Indicators...",
  "short_title": "L.25E",
  "type": "COP_decision_text",
  "cop": "COP30",
  "country": null,
  "issues_addressed": ["GGA-IND"],
  "language": "en",
  "license": "UN Open License",
  "official_url": "https://unfccc.int/...",
  "adoption_date": "2025-11-21",
  "sha256": "abc123...",
  "size_bytes": 4521,
  "n_tokens": 845,
  "category_dir": "unfccc_decisions"
}
```

---

## 🔍 search_index.json 사용법

```python
import json
from src.data.build_v6_corpus_index import tokenize

idx = json.load(open("data/corpus/search_index.json", encoding="utf-8"))

def search(query, top_k=10):
    toks = tokenize(query)
    scores = {}
    for t in toks:
        idf_w = idx["idf"].get(t, 0)
        if t not in idx["inverted"]: continue
        for doc_id, w in idx["inverted"][t]:
            scores[doc_id] = scores.get(doc_id, 0) + w * idf_w
    return sorted(scores.items(), key=lambda x: -x[1])[:top_k]

# Example
search("GGA indicators voluntary brazil chair", top_k=5)
# -> [("UNFCCC_FCCC_PA_CMA_2025_L25E", 4.2), ("BRA_Plano_Clima_2024", 3.1), ...]
```

웹 UI에서는 동일 인덱스를 fetch하여 브라우저에서 검색합니다.

---

## 📜 출처 + 라이선스

- **UNFCCC L-documents**: UN Open License (모두 공식 채택문)
- **국가 정책 문서**: 각국 공공저작물 자유이용 또는 동등 — 출처 명시
- **bibliography.bib**: 학술 논문 BibTeX (각 entry에 DOI/URL); 본 compilation은 CC BY 4.0
- **quantitative CSVs**: 각 CSV header에 source URL 명시 (ND-GAIN, PRIMAP-hist, OECD CRS, CVF)
- **manifest + search_index**: CC BY 4.0 (compilation)

---

## ⚠️ 한계와 정확성 주의사항

1. **UNFCCC L-documents**: 본 corpus의 markdown은 실제 결정문의 **요약 + 핵심 인용**으로, 전체 텍스트가 아닙니다. 인용은 원문 그대로이나 paragraph 번호와 구조는 markdown 재구성. 원문 PDF는 `official_url` 필드 참조.

2. **국가 정책 brief**: 17개국 종합 brief는 NDC Registry와 ENB 보고서를 종합한 **2차 가공물**. 1차 정확성은 원문 참조 권장.

3. **quantitative CSVs**: PRIMAP-hist는 reference year 추정 + 연도별 trajectory를 단순 모델로 합성. 정확한 분석에는 PRIMAP 원본 v2.5+ 데이터셋 사용 권장.

4. **manifest.jsonl SHA256**: 파일 변경 시 자동 갱신되지 않음. `python -m src.data.build_v6_corpus_index` 재실행 필요.

---

## 🔄 재생성

```bash
# 정량 CSV 재생성
python -m src.data.build_v6_quantitative

# manifest + index 재생성
python -m src.data.build_v6_corpus_index
```

두 명령 모두 deterministic (seed=42), 동일 입력 → 동일 출력.

---

## 🔗 통합

- `src/program/query_engine_v2.py` v2.1: corpus retrieval intent (`search`) 추가
- `docs/web/cina_program_v2.html` v2.1: 답변에 corpus document link 자동 첨부
- `docs/web/corpus_browser.html` (new): 21개 문서를 카테고리별 + 검색 가능

---

**작성**: Heedo Choi (최희도) · 국민대학교 일반대학원 기후기술융합학과
