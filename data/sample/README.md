# 📊 Public Sample Data

> 이 폴더는 CINA 파이프라인이 실제로 생성한 산출물의 **공개 샘플**입니다.
> 전체 데이터(225 raw 문서, 60 stance records, 1.3GB)는 license 제약으로 Zenodo에 별도 공개 예정입니다.

## 파일 목록

| 파일 | 설명 | 출처 |
|------|------|------|
| `stances_sample_10.jsonl` | Stage 1 LLM 추출 stance 10개 샘플 (전체 60개 중) | `src/stage1_extract/extract_v2.py` 산출 |
| `graph_analysis.json` | Stage 2 country×issue matrix + Leiden 2 communities + centralities | `src/stage2_graph/advanced_analysis.py` 산출 |
| `realist_b0_statistics.json` | Realist baseline F1 = 0.560 통계 (McNemar p<0.0001) | `src/p03_realist_b0_statistics.py` 산출 |
| `irr_brazilian_translation_gap.json` | Brazil Translation Gap Δ=0.304 정량 결과 | `src/p02_negative_authority_irr_v2.py` 산출 |
| `chair_metadata_stats.json` | COP1-COP29 chair 통계 (regional rotation, presidency type) | `src/p01_merge_chair_metadata.py` 산출 |
| `rgat_training_results.json` | R-GAT GNN 학습 결과 (proxy via NetworkX) | Stage 2 advanced analysis |
| `frame_distribution.json` | 5-frame typology 분포 (scientific/justice/sovereignty/security/development) | Refinement Round 3 산출 |

## Stage 1 Stance Record 스키마 (v1.3)

각 stance record는 다음 필드를 포함:

```json
{
  "_meta": {
    "doc_id": "FCCC_PA_CMA_2025_L25E_BRA_GGA",
    "country": "Brazil",
    "iso3": "BRA",
    "issue": "GGA-IND",
    "cop": "COP30",
    "extracted_at": "2026-04-30T13:30:00Z",
    "provider": "cina_pipeline",
    "k_samples": 5
  },
  "stance_score": 0.95,                    // -1 (oppose) ~ +1 (strong support)
  "stance_score_samples": [1.0, 0.95, ...], // multi-sample k=5
  "ci_lower_95": 0.86,                     // Bayesian credible interval
  "ci_upper_95": 1.0,
  "stance_category": "strong_support",
  "key_demands": [...],                    // 핵심 요구사항
  "red_lines": [...],                      // 절대 양보 불가
  "flexibility_signals": [...],            // 협상 여지
  "evidence_quotes": [{"quote": "...", "location": "Para 7"}],
  "frame_type": "development",             // scientific/justice/sovereignty/security/development/mixed
  "frame_components": ["development", "sovereignty"],
  "salience_score": 1.0,
  "instrument_signals": {                  // NATO 4-axis (Hood 1983, Howlett 2019)
    "nodality": [...],
    "authority": [...],
    "treasure": [...],
    "organization": [...]
  },
  "procedural_signals": {                  // Tallberg 2010
    "is_chair_role": true,
    "is_pen_holder": true,
    "drafts_text_for_issue": "GGA-IND"
  },
  "confidence": 0.95
}
```

## 재현 방법

샘플 데이터를 생성하는 전체 파이프라인:

```bash
# Stage 1 — stance 추출 (Brazil, COP30, adaptation)
python -m src.pipeline --country Brazil --cop 30 --sector adaptation --stages 1

# Stage 2 — 그래프 분석 (Leiden + centrality)
python -m src.stage2_graph.advanced_analysis

# Stage 3 — 장관급 브리핑 생성
python -m src.stage3_brief.generate_briefing

# Phase 5 평가 (4-task)
python -m src.evaluation.run_full_evaluation
```

## 데이터 추적성

모든 raw 문서는 `data/manifest/manifest.jsonl`에 license + sha256 + source URL이 추적되어 있습니다 (225 entries). 본 sample은 그 중 일부의 후처리 결과입니다.
