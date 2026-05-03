# CINA: Climate Issue-Network Analysis Framework

[![License](https://img.shields.io/badge/License-MIT%20%2B%20CC%20BY%204.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Phase%205%20Complete-brightgreen.svg)](deliverables/evaluation_report_v2.md)
[![Combined Rubric](https://img.shields.io/badge/Combined%20Rubric-4.76%2F5-success.svg)](deliverables/evaluation_report_v2.md)
[![Manifest](https://img.shields.io/badge/Manifest-225%20docs-blue.svg)](data/manifest/coverage_summary.json)

> **"From Text to Strategy: An LLM–GNN Pipeline for Climate Negotiation Intelligence, Retrospectively Validated on COP30 Adaptation Outcomes"**
>
> An academic research project extending Kookmin University's Graduate Global Climate Leadership coursework into a publishable AI methodology study.
> **Track A** (class submission — ministerial-grade adaptation briefing) + **Track B** (academic submission — *Global Environmental Change* / NeurIPS Climate Change AI 2026).

---

> 📦 **모든 산출물 보기**: [ALL_OUTPUTS_INDEX.md](ALL_OUTPUTS_INDEX.md) — 학술 페이퍼 · 장관급 브리핑 · 정량 검증 보고서 8종 · Stage 2 figures 7종 · 방법론 문서 15종 · 데이터/코드 인덱스
> 🌐 **웹 데모**: [docs/web/index.html](docs/web/index.html) (deploy 후: https://zxsa0716.github.io/cina/web/)

---

## TL;DR

CINA fills three gaps left by existing climate negotiation AI tools:

| Existing Tool | Limitation | CINA Contribution |
|---------------|-----------|-------------------|
| NegotiateCOP (Germany 2024) | Text QA only | Structured stance + per-issue separation |
| RICE-N (Salesforce 2022) | Theoretical simulation | Document-grounded |
| Castro et al. 2025 | Frequency aggregation | Strategic decision-making + automated briefing |

```
UNFCCC Submissions + ENB + NDC + IPCC + OWID + IMF + PRIMAP
         │
         ▼ Stage 1: LLM Stance Extraction (Bayesian uncertainty + NATO 4-axis + 5 frame types)
Country × Issue Stance Tensor (98 records)
         │
         ▼ Stage 2: Heterogeneous Temporal Graph + Leiden (chair_status + drafts_text edge)
Coalition clusters · Bridge nodes · Cross-issue hyperedges · Procedural authority
         │
         ▼ Stage 3: Graph-Grounded Generation (evidence + structural fact required)
Ministerial Strategic Briefing (Korean + English) + Academic Paper Drafts
```

---

## Phase 5 Evaluation Results (4-task) ⭐

| Task | Metric | Value | Threshold | Status |
|------|--------|-------|-----------|--------|
| **A. Stance Accuracy** | Spearman ρ | **0.658** | ≥ 0.6 | ✅ PASS |
| | MAE | **0.183** | ≤ 0.25 | ✅ PASS |
| **B. Coalition Detection** | ARI proxy | **0.42** | ≥ 0.4 | ✅ PASS |
| **C. Outcome Prediction** | P@3 / R@3 | **1.00 / 1.00** ⭐ | ≥ 0.6 | ✅ PASS |
| **D. Briefing Quality** | Mean panel | **4.53/5** | ≥ 4.0 | ✅ PASS |
| | Krippendorff α | **0.905** | ≥ 0.7 | ✅ PASS |

8 publishable-grade findings (see [evaluation_report_v2.md](deliverables/evaluation_report_v2.md)).

---

## Key Academic Findings (8)

1. **GGA-IND Authority axis = 6.1** (lowest of 6 issues) — voluntary language as binding-force absence (Howlett 2019 instrument calibration evidence)
2. **IRR_Brazil Translation Gap Δ = 0.304 CONFIRMED** — Putnam × Howlett research gap quantification ⭐
3. **L.25 pre-crystallized formula hypothesis** — NeurIPS CCAI signature finding candidate (Tallberg 2010 + Steinberg 2002 + Goh 2007 integration)
4. **Realist B0 F1 = 0.560 (p<0.0001)** — constructivist+frame variables empirically justified
5. **Leiden 2 communities** — Regime Complex 'horizontal cleavage' (Keohane-Victor 2011) quantitatively verified ⭐
6. **Task A Spearman 0.658** (CINA vs expert agreement)
7. **Task C P@3=R@3=1.00** (3/3 contested issues correctly predicted from stance variance alone)
8. **Korean IRR = 0.653, L&D-OP = 0.39 weakness** — actionable COP31 negotiation recommendation

---

## Project Structure

```
cina/
├── README.md                    # (this document)
├── LICENSE                      # MIT (code) + CC BY 4.0 (docs/data)
├── CINA_FRAMEWORK.md            # Core framework v2.0 definition
│
├── docs/                        # Academic methodology (15 documents)
│   ├── 01_theoretical_foundations.md   # Regime Complex, Two-Level Games, Issue Linkage, Epistemic Communities
│   ├── 02_methodology.md               # Three-stage pipeline specification
│   ├── 03_data_architecture.md         # Schema definitions
│   ├── 04_stage1_stance_extraction.md  # LLM + Bayesian CI + Platt calibration
│   ├── 05_stage2_graph_analysis.md     # R-GAT + Leiden + hypergraph
│   ├── 06_stage3_briefing_generation.md # Graph-Grounded Generation
│   ├── 07_evaluation_protocol.md       # 4-task validation
│   ├── 08_novelty_positioning.md       # Academic contributions C1-C10
│   ├── 09_ministerial_briefing_template.md
│   ├── 10_council_protocol.md          # 5-agent council architecture
│   ├── 11_source_catalog.md            # Tier 1-4 sources
│   ├── 12_data_collection_master_plan.md
│   ├── 13_reference_tables.md          # 20 countries × 12 groups × 6 issues
│   ├── 14_schema_v1_3_changes.md       # NATO 4-axis + frame + procedural
│   └── 15_stage2_features_v2.md        # chair_status + drafts_text edge
│
├── deliverables/                # Final outputs (12 documents)
│   ├── country_selection.md            # Brazil selection rationale
│   ├── sector_focus.md                 # Adaptation sector justification
│   ├── agenda_matrix.md                # COP30 6-issue matrix
│   ├── korean_nap_gga_crosswalk_v3.csv # 30 cells (Korean NAP × GGA targets)
│   ├── IRR_Korea_2025_v2.md           # IRR_Korea = 0.653 (CI [0.55, 0.71])
│   ├── IRR_Brazil_2025_v2_negAuth.md  # Δ = 0.304 CONFIRMED ⭐
│   ├── realist_b0_statistics.md        # F1 = 0.560, p<0.0001
│   ├── L25_formula_control_evidence.md # Pre-crystallized formula hypothesis
│   ├── hedging_density_2d_plot.png     # AILAC vs AOSIS vs LDC clusters
│   ├── AILAC_norm_entrepreneur_quantification.md  # Finnemore-Sikkink test
│   ├── evaluation_report_v2.md         # Phase 5 4-task quantitative validation
│   ├── ministerial_briefing_v3_ko.md   # Korean ministerial brief (Track A)
│   └── ministerial_briefing_v3_en.md   # English version (Track B)
│
├── src/                         # Python implementation
│   ├── data/identifiers.py             # 20 countries × 12 groups × 6 issues × 16 sessions
│   ├── collect/                        # 26 collectors (UNFCCC, NDC, ENB, IPCC, IMF, PRIMAP, WRI, etc.)
│   ├── stage1_extract/                 # LLM stance extraction
│   │   ├── extract.py / extract_v2.py  # Multi-LLM provider abstraction
│   │   └── providers/                  # Gemini, Groq, Ollama, OpenRouter, Anthropic
│   ├── stage2_graph/                   # R-GAT model + NetworkX advanced + Leiden
│   ├── stage3_brief/                   # Graph-Grounded Generation
│   ├── evaluation/                     # 4-task evaluation (Task A/B/C/D + ablations)
│   ├── validate/                       # Evidence validator
│   └── pipeline.py                     # End-to-end CLI
│
└── data/
    └── manifest/manifest.jsonl         # 225 entries (license/sha256 100% tracked)
```

---

## Quickstart (Free LLM)

### 1. Clone + environment
```bash
git clone https://github.com/zxsa0716/cina.git
cd cina
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# or .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2. Choose a free LLM provider

#### Option A: Gemini 2.5 Flash-Lite (recommended ⭐)
```bash
# Get free key at https://aistudio.google.com/apikey
export GEMINI_API_KEY="your_key"
export CINA_LLM_PROVIDER="gemini"
pip install google-generativeai
```

#### Option B: Groq Llama 3.3 70B (fastest)
```bash
# Get free key at https://console.groq.com/keys
export GROQ_API_KEY="your_key"
export CINA_LLM_PROVIDER="groq"
pip install groq
```

#### Option C: Ollama local (zero cost, unlimited)
```bash
# Install at https://ollama.com/download
ollama pull qwen2.5:3b
export CINA_LLM_PROVIDER="ollama"
pip install ollama
```

### 3. Run the CINA pipeline
```bash
# Stage 1 — stance extraction
python -m src.pipeline --country Brazil --cop 30 --sector adaptation --stages 1

# Stage 2 — graph analysis (NetworkX + Leiden)
python -m src.stage2_graph.advanced_analysis

# Stage 3 — ministerial briefing generation
python -m src.stage3_brief.generate_briefing

# Evaluation 4-task
python -m src.evaluation.run_full_evaluation
```

---

## Author

**Heedo Choi** (최희도)
Graduate Student, Department of Climate Technology Convergence (기후기술융합학과)
Kookmin University, Seoul, Republic of Korea
✉️  zxsa0716@kookmin.ac.kr  ·  GitHub: [@zxsa0716](https://github.com/zxsa0716)

Research focus: Graph Attention Networks (GAT) · Explainable AI (XAI) · Urban climate analytics · Climate justice quantification

## Citation

```bibtex
@misc{choi2026cina,
  author       = {Choi, Heedo},
  title        = {{CINA}: Climate Issue-Network Analysis --- An LLM-GNN Pipeline for Climate Negotiation Intelligence, Retrospectively Validated on COP30 Adaptation Outcomes},
  year         = {2026},
  institution  = {Kookmin University, Department of Climate Technology Convergence},
  howpublished = {\url{https://github.com/zxsa0716/cina}},
  note         = {Graduate research project, Global Climate Leadership programme (2026 Spring)}
}
```

**APA**: Choi, H. (2026). *CINA: Climate Issue-Network Analysis — An LLM-GNN pipeline for climate negotiation intelligence, retrospectively validated on COP30 adaptation outcomes* [Computer software]. Kookmin University, Department of Climate Technology Convergence. https://github.com/zxsa0716/cina

---

## Target venues

- **Primary**: *Global Environmental Change*, *Climate Policy*, *Global Environmental Politics*
- **Technical**: NeurIPS Climate Change AI Workshop 2026, AAAI AI for Social Good
- **Dataset track**: Nature Scientific Data
- **Class submission**: Kookmin University Graduate Global Climate Leadership (May 2026)

---

## License

- **Code**: MIT
- **Documentation, briefs, deliverables**: CC BY 4.0
- **Third-party data** in `data/raw/`: Per-source licenses (manifest.jsonl tracked)

---

## Acknowledgments

- IPCC AR6 Working Group II authors
- IISD Earth Negotiations Bulletin reporting team
- Castro, Kristof, Kammerer, Cogne (2025) — ENB cooperation/conflict dataset
- Brazilian MMA (Plano Clima 16 sectoral plans publication)
- Multi-LLM provider stack (Google Gemini, Groq, Ollama)

---

**Status**: Phase 5 Evaluation complete. Track A (class) ready, Track B (academic) draft-ready.
**Last update**: 2026-04-30
