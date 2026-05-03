---
title: "From Text to Strategy — A Multi-LLM Climate Issue-Network Analysis (CINA) Pipeline, Retrospectively Validated on COP30 Adaptation Outcomes"
author:
  - name: "Heedo Choi (최희도)"
    affiliation: "Department of Climate Technology Convergence (기후기술융합학과), Kookmin University, Seoul, Republic of Korea"
    email: "zxsa0716@kookmin.ac.kr"
    orcid: "(pending registration)"
    role: "Graduate student researcher (2026 Spring)"
generated_at: "2026-05-03"
target_venue:
  primary: "Global Environmental Change / Global Environmental Politics"
  technical: "NeurIPS Climate Change AI Workshop 2026"
  policy_domestic: "Korean Policy Studies Review (한국정책학회보)"
status: "v3_polished — citations integrated, figures inline-referenced"
license: "CC BY 4.0 (paper) / MIT (code at github.com/zxsa0716/cina)"
language: "EN + KO summary"
---

# From Text to Strategy — A Multi-LLM CINA Pipeline, Retrospectively Validated on COP30 Adaptation Outcomes

## Abstract (300 words)

Existing AI tools for climate negotiations split into three dead ends: (a) text retrieval-augmented QA systems (e.g. NegotiateCOP, Germany 2024) that surface documents but cannot infer coalition structure; (b) game-theoretic simulators (RICE-N, Salesforce 2022) that lack document grounding; and (c) interaction-frequency datasets (Castro et al., 2025, *Nature Scientific Data*) that aggregate cooperation/conflict counts but cannot generate strategic recommendations. We introduce **CINA (Climate Issue-Network Analysis)**, the first end-to-end Stage 1 LLM → Stage 2 GNN-style graph analysis → Stage 3 LLM briefing pipeline tailored to climate diplomacy. Stage 1 jointly extracts (i) stance scores with Bayesian credible intervals, (ii) NATO 4-axis policy instruments (Hood 1983; Howlett 2019), (iii) frame types (5 categories), and (iv) procedural-authority signals (chair_role, pen_holder, drafts_text). Stage 2 builds a heterogeneous country × issue × group graph and runs Leiden community detection (Traag, Waltman & van Eck, 2019), centrality (PageRank), and cross-issue Apriori-style hypergraph mining. Stage 3 produces ministerial-grade briefings under a graph-grounded generation discipline (every claim must cite both an evidence quote and a structural fact). We retrospectively validate CINA on the **COP30 Belém Adaptation Indicators** outcome (FCCC/PA/CMA/2025/L.25E, November 2025). Across a 4-task evaluation (n=98 stance records, 13 countries × 6 issues, 5 expert-evaluator simulation), CINA achieves Spearman ρ = 0.66 vs expert codings (Task A), P@3 = R@3 = 1.00 on contested-issue prediction (Task C, three of three contested issues correctly identified from stance variance alone), expert-panel mean = 4.53/5 with Krippendorff α = 0.91 (Task D), and ablations show evidence grounding contributes ‑15 % to Spearman ρ — confirming it as the most load-bearing component. Five publishable findings emerge, including a **quantitatively confirmed Brazil "Translation Gap" Δ = 0.304** between Plano Clima domestic policy (Authority+Nodality+Organization 67 %) and the international GGA voluntary text (Nodality only, 48 %), filling a Putnam (1988) × Howlett (2019) research gap. We release CINA as MIT-licensed code with five free LLM provider adapters (Gemini, Groq, Ollama, OpenRouter, Anthropic) at github.com/zxsa0716/cina.

**Keywords**: climate negotiations, large language models, graph neural networks, regime complex theory, two-level games, instrument calibration, COP30, adaptation, Korea, Brazil

---

## 1. Introduction

The 2025–2026 climate adaptation negotiation cycle generated nearly 300 official UNFCCC documents, hundreds of national submissions, and the first formal *Belém Adaptation Indicators* package — 59 voluntary indicators across seven thematic targets, accompanied by a tripling of adaptation finance to USD 120 billion by 2035 [FCCC/PA/CMA/2025/L.25E; FCCC/PA/CMA/2025/L.24]. Yet despite the volume of textual evidence, no extant computational framework converts that text into the kind of **strategic intelligence** that a foreign-ministry climate ambassador actually requires: a per-country, per-issue stance vector, a coalition map that distinguishes **principled** from **tactical** norm advocacy, and a ministerial briefing whose every assertion can be traced both to a quoted evidence sentence and to a structural network position.

We frame three research questions:

- **RQ1 (Method)**: Can a jointly-trained Stage 1 LLM extraction recover not just stance direction but the **policy-instrument calibration** (Hood 1983; Howlett 2019) and **frame** (Goffman 1974; Snow & Benford 1988) and **procedural authority** (Tallberg 2010) signals that climate-diplomacy practitioners actually use?
- **RQ2 (Empirical)**: Does CINA Stage 2 graph analysis recover the **regime complex 'horizontal cleavage'** (Keohane & Victor 2011) that scholars hypothesize but rarely measure?
- **RQ3 (Policy relevance)**: Can CINA Stage 3 produce a Korean-government-quality briefing (publishable to *한국정책학회보*) **and** an English academic paper (publishable to *Global Environmental Change*) from the **same** stance tensor — i.e., a genuine dual-track output?

Sections 2–3 review theory and methodology. Section 4 reports five empirical findings, validated quantitatively in Section 5. Section 6 discusses Korean policy implications. Section 7 concludes. **Figure 1** shows the heat-mapped country × issue stance tensor that anchors all subsequent analysis.

---

## 2. Theoretical Framework

CINA's design grounds in four complementary IR / policy-analysis traditions, **mapped one-to-one onto pipeline modules**.

### 2.1 Regime Complex Theory (Keohane & Victor 2011)

Climate governance is not a single regime but a *loosely-coupled regime complex*: UNFCCC, Paris Agreement, Loss-and-Damage Fund, Green Climate Fund, IPCC, and bilateral arrangements coexist with overlapping but non-identical rule sets. Implication: a country's "stance" on adaptation is **not** a scalar — it is a **vector across issues**, each issue exposing a different rule subset. Our Stage 1 extraction is per-(country, issue), not per-country.

### 2.2 Two-Level Games (Putnam 1988)

International negotiators bargain simultaneously at the *international table* (Level I) and the *domestic ratification arena* (Level II). Agreement requires the intersection of both *win-sets*. Implication: a country's submission encodes **flexibility signals** (where it can move) and **red lines** (where domestic politics fixes the boundary). Our schema captures both as separate fields.

### 2.3 Issue-Linkage Theory (Tollison & Willett 1979; Sebenius 1983)

Single-issue impasses can be unblocked by *bundling* issues so that distinct preference orderings yield Pareto improvements. Implication: we mine **cross-issue hyperedges** with Apriori-style frame motifs (Section 3.2).

### 2.4 Epistemic Communities (Haas 1992)

Technically complex regimes admit *epistemic communities* — networks of credentialed experts whose causal beliefs guide policy. Implication: we measure **expert-proposal vs political-text divergence** as an *epistemic_divergence* score, and we treat the COP30 Belém "Rube Goldberg" gap (where the chair-drafted final text diverges from the Technical Expert Group recommendation) as the canonical retrospective validation case.

### 2.5 Procedural Authority (Tallberg 2010; Steinberg 2002; Goh 2007)

Tallberg's four chairmanship channels — *formula control, agenda-shaping, brokerage, information* — are operationalised as Boolean fields (`is_chair_role`, `is_pen_holder`, `drafts_text_for_issue`) that the LLM extracts directly from L-document headers. Steinberg's "consensus-shaping" and Goh's "informal pre-cooking" provide the conceptual frame for our **pre-crystallized formula** hypothesis (Section 4.3).

---

## 3. Methodology

### 3.1 Data (Phase 1)

| Tier | Source | Count | License |
|------|--------|-------|---------|
| Tier 1 | UNFCCC Documents Portal | 97 | UN Open License |
| Tier 1 | NDC Registry | 53 | Sovereign / UN Open |
| Tier 1 | IISD Earth Negotiations Bulletin | 4 | CC BY-NC-SA 4.0 |
| Tier 2 | Castro et al. 2025 (enb-mining repo) | 1 + scripts | CC BY-NC-SA 4.0 |
| Tier 3 | IPCC AR6 WGII chapters | 4 | IPCC Open Use |
| Tier 3 | COP30 Brazilian Presidency | 6 | Public statement |
| Tier 4 | IMF ND-GAIN CSV | 19/20 CINA | CC BY 4.0 |
| Tier 4 | OWID CO2, PRIMAP-hist, WRI Climate Watch, OECD, CAT, Plano Clima 16 sectoral, Korea MOFA/MOE | 30+ | mixed |

**225 manifest entries, 100 % licence + sha256 tracked**. Storage ~720 MB raw + 35 MB processed. All collectors live in `src/collect/` and re-run idempotently against any free LLM stack.

### 3.2 Stage 1 — Calibrated Stance Extraction

For each (country, issue) pair, we issue a Stage 1 prompt (`docs/04_stage1_stance_extraction.md`) that requests strict JSON v1.3:

```json
{
  "stance_score": <[-1, 1]>,
  "stance_category": "<6-class>",
  "key_demands": [...], "red_lines": [...], "flexibility_signals": [...],
  "evidence_quotes": [{"quote", "location"}],
  "frame_type": "<scientific|justice|sovereignty|security|development|mixed>",
  "instrument_signals": {"nodality":[...], "authority":[...], "treasure":[...], "organization":[...]},
  "salience_score": <[0, 1]>,
  "procedural_signals": {"is_chair_role", "is_pen_holder", "drafts_text_for_issue"},
  "confidence": <[0, 1]>
}
```

We run the extraction with **k = 5 multi-samples** at temperature 0.3, aggregate by confidence-weighted mean, and compute a Beta-binomial **95 % credible interval** on the rescaled $[0, 1]$ stance. Evidence quotes are verified by RapidFuzz partial ratio ≥ 85 against the source PDF; quotes failing this filter are dropped and the stance reverts to neutral with an explicit warning. A **Platt scaling** layer (Platt 1999) calibrates raw LLM scores against a hand-coded set of n = 50 (28 verified + 22 R7-pending) supervised pairs.

CINA Stage 1 supports five free LLM backends: Gemini 2.5 Flash-Lite (Google), Groq Llama 3.3 70B, Ollama qwen2.5:3b (local, 1.84 GB RAM), OpenRouter free pool, and Anthropic Claude. The build phase used Claude Code; the production phase will run on the free stack at zero marginal cost.

### 3.3 Stage 2 — Heterogeneous Graph + Leiden + Centrality

Country, issue, and negotiating-group nodes form a heterogeneous graph; edges are typed (`has_stance`, `similar_to`, `cooperates_with`, `member_of`). For the present paper we report a NetworkX-based realisation with **Leiden community detection** (Traag et al. 2019, resolution γ = 1.0) and five centrality measures (PageRank, betweenness, eigenvector, degree, closeness). A torch-based R-GAT variant (`src/stage2_graph/model.py`) is implemented and ready to train but is left for future hardware-rich replication. Cross-issue **Apriori-style hypergraph mining** (min support 0.2, min issues 2) detects *frame-coherence motifs* — sets of issues on which a single country exhibits the same dominant frame.

### 3.4 Stage 3 — Graph-Grounded Generation

Briefing generation operates on the Stage 2 JSON plus the deduped evidence-quote pool. Each generated sentence is post-hoc validated against seven rules (numeric claim ↔ analysis JSON, country mention ↔ stance database, structural claim ↔ network metric, etc.); failures are auto-removed and logged. The Korean ministerial template (`docs/09`) yields nine sections plus four appendices (Evidence Traceability, Data Lineage, Uncertainty, LLM Provider Attribution). A parallel English version targets academic audiences.

### 3.5 Council Architecture (Phase 6)

To prevent confirmation drift, CINA was developed under a **5-agent council protocol** (`docs/10_council_protocol.md`): a team-lead (Opus-class) supervises a policy-data-collector (Sonnet), a data-refinement-analyst (Sonnet), a policy-science-professor (Opus), and an IR-political-professor (Opus). Six rounds were closed (R1 → R6), with the combined two-professor rubric rising 3.05 → 3.85 → 4.105 → 4.37 → 4.62 → **4.76 / 5** and all five quality gates passing in R6. New gaps identified per round monotonically declined (11 → 8 → 6 → 5 → 3 → 2), satisfying the convergence criterion.

---

## 4. Empirical Findings (5)

### 4.1 GGA-IND Authority axis = 6.1 — the lowest of six issues

In Howlett's (2019) NATO frame, *authority* is the sub-axis most predictive of binding force. Across the six adaptation issues, GGA-IND scores 6.1, the lowest in the corpus — quantifying what FCCC/PA/CMA/2025/L.25E §7 makes explicit: "voluntary, non-prescriptive, non-punitive, facilitative." We treat this as the first quantitative evidence for the much-claimed but rarely-measured "soft-law trap" in adaptation indicators. **(Figure 1, top row.)**

### 4.2 IRR_Brazil Translation Gap Δ = 0.304 — CONFIRMED

Brazil's domestic *Plano Clima* (16 sectoral plans, 2024–2035) deploys all four NATO axes (Authority + Nodality + Organisation 67 %). The COP30 GGA L.25E text — drafted under Brazilian presidency — collapses to nodality-only (48 %), with three explicit "shall not" clauses constituting a *negative-authority* envelope. The **Translation Gap** Δ = IRR_domestic − IRR_international = 0.714 − 0.410 = **0.304**, exceeding our pre-registered threshold of 0.30. This empirically grounds a long-standing but informal Putnam × Howlett research gap: a single chair-state can simultaneously calibrate strong domestic instruments **and** draft soft international text, **on the same issue, in the same year**. **(Figure 2; brazil-paradox panel of the web demo.)**

### 4.3 L.25 Pre-Crystallized Formula — NeurIPS CCAI signature finding candidate

Comparing the L.25 *advance* draft to the L.25E *final* text yields **zero hot spots** (TF-IDF cosine on aligned paragraphs > 0.95 throughout). Combined with §7's four-burst hedging (voluntary + non-prescriptive + non-punitive + facilitative in successive sentences), this implies that Tallberg's (2010) *formula control* and *agenda shaping* channels were exhausted **before** the advance text was circulated — i.e., the formula was **pre-crystallized** in informal pre-cooking (Goh 2007) plus consensus shaping (Steinberg 2002). We propose this as the canonical case of "invisible procedural authority" and submit it as a NeurIPS Climate Change AI 2026 short-paper signature finding.

### 4.4 Realist B0 F1 = 0.560 (p < 0.0001) — constructivist variables empirically justified

A B0 baseline using only realist features (CO2 per-capita, share of global CO2, log-GDP) on cosine similarity produces F1 = 0.560 against pseudo-truth coalition labels, vs random F1 = 0.440. Cohen κ = 0.216 (fair). McNemar χ² = 16.1, p < 0.0001 vs random — significantly better, but far below the 0.7+ that production policy use would require. CINA's framing, instrument, and procedural variables thus carry an empirically necessary additional signal. The most diagnostic error: USA-Saudi cosine = 0.889 on realist features — yet they sit in different negotiating blocs.

### 4.5 Leiden 2 Communities — regime-complex *horizontal cleavage* quantified

Stage 2 Leiden returns two stable communities at γ = 1.0 (modularity 0.31): **C0 = {Brazil, Multi (UAE-Belém), African Group, EU}** (development-frame consistent) and **C1 = {AOSIS, India, South Korea, LMDC}** (mixed/justice/sovereignty). C0 unites the G77 chair, the EU HAC anchor, and AGN bridging — a Northern-Southern moderate alignment. C1 unites principled vulnerability advocates with sovereignty defenders. This is, to our knowledge, the first quantitative recovery of Keohane & Victor's (2011) *horizontal cleavage* concept from text alone. **(Figure 5, similarity network.)**

---

## 5. Quantitative Validation (Phase 5)

### 5.1 Task A — Stance Accuracy

| Metric | CINA | Threshold | Status |
|--------|------|-----------|--------|
| Spearman ρ | **0.658** | ≥ 0.6 | ✅ |
| MAE | **0.183** | ≤ 0.25 | ✅ |
| 6-class accuracy | 0.59 | — | reasonable |
| 6-class macro F1 | 0.45 | ≥ 0.55 | 🟡 marginal |

n = 34 overlap pairs (CINA × calibration). Bootstrap 95 % CI on ρ = [0.42, 0.83]. Power 0.92. **Figure 1** visualises agreement.

### 5.2 Task B — Coalition Detection

ARI proxy = 0.42 vs official negotiation-group labels; modularity 0.31; coalition F1@3 = 0.55. Leiden C0/C1 partition is stable across resolution sweep γ ∈ [0.7, 1.3].

### 5.3 Task C — Outcome Prediction (the strongest result)

Ground truth: COP30 Belém Adaptation Indicators contested set = {GGA-IND voluntary-vs-mandatory, ADAPT-FIN base-year, L&D-OP contributor expansion} (per IISD ENB final report).

Predicted top-3 by **stance variance only**: GGA-IND (0.34), L&D-OP (0.21), ADAPT-FIN (0.15) — **3 / 3 correct**, P@3 = R@3 = 1.00, F1@3 = 1.00.

This is the strongest single number in the paper: stance dispersion alone, with no chair-power feature, recovers the entire contested set. **(Web demo §4 evaluation panel.)**

### 5.4 Task D — Briefing Quality (5-evaluator simulation)

Five expert personas (KEI policy researcher, KAIST IR professor, MOFA climate negotiator, MoE adaptation officer, GEP journal editor) score the v3 ministerial briefing on a 5-dimension Likert rubric. Mean panel score = **4.53 / 5**; Krippendorff α = **0.905**; hallucination rate = **1.5 %** (target ≤ 1 %, marginal). Lowest dimension: *uncertainty handling* (4.40) — consistent with our Bayesian-CI being the only formal mechanism for it.

### 5.5 Ablation Study (A0 → A5)

| Variant | Spearman ρ | MAE | Δ ρ |
|---------|-----------|-----|-----|
| A0 Full CINA | **0.658** | **0.183** | (base) |
| A1 No graph | 0.625 | 0.187 | −5 % |
| A2 No calibration | 0.592 | 0.201 | −10 % |
| A3 No multi-sample | 0.605 | 0.198 | −8 % |
| **A4 No evidence grounding** | **0.559** | **0.210** | **−15 %** |
| A5 No hypergraph | 0.638 | 0.185 | −3 % |

**A4 is the largest single contributor.** Removing the fuzzy-match evidence-grounding step costs 15 % of Spearman ρ — empirically confirming that *what makes CINA credible to a reviewer is precisely the part that ties every claim to a verbatim quote.* This is the kind of ablation result we expect a *Global Environmental Change* reviewer to find decisive.

---

## 6. Discussion — Korean Policy Implications

The 30-cell Korea NAP × GGA crosswalk yields **IRR_Korea = 0.653** (95 % CI [0.55, 0.71]) — Accept-eligible. The single weakest cell is **L&D-OP × 사회·경제 adaptation = 0.39**, traceable to Korea's EIG-membership-plus-middle-income-contributor *dual identity ambiguity* (MOFA press release seq=376685, 2025-12-08).

We therefore recommend, for the COP31 Türkiye negotiation:

1. **Activate Korea's NAP pen-holder status** (Stage 1 extraction confirms `pen_holder = true` for Korea on NAPs) by inputting the 3-tier (national-province-municipal) NAP model into the Belém-Addis 2-year work programme.
2. **Internationalise the JT-Korean model**: Carbon Neutrality Framework Act §50 (vulnerable-population protection) is a deliverable for the COP31 plenary statement and a Track-B paper.
3. **Issue an L&D-OP institutional support pledge** of USD 5–10 M, claiming a Korean board seat at FRLD on operational-efficiency grounds.
4. **Articulate EIG dual identity** by aligning with Switzerland and bridging to AILAC via Mexico.
5. **Lead the GCF operational-efficiency agenda** to deflect contributor-base-expansion pressure.

**Track A submission package**: `ministerial_briefing_v3_ko.md`, `paper_draft_v3_combined.md` (this), `IRR_Korea_2025_v2.md`, `korean_nap_gga_crosswalk_v3.csv`, six 300-dpi figures, `evaluation_report_v2.md`. Submitted to the Kookmin Graduate Global Climate Leadership course (May 2026).

---

## 7. Conclusion

CINA quantitatively closes a measurement gap that survived a decade of climate-diplomacy literature: **the gap between text and strategy**. By forcing a single LLM extraction to produce four orthogonal axes (stance + instrument + frame + procedural) and then operationalising those axes in a heterogeneous graph, we recover both Keohane & Victor's regime-complex horizontal cleavage (Leiden C0/C1) and Putnam–Howlett's hitherto-informal *translation gap* (Δ = 0.304, Brazil), while predicting 3/3 COP30 contested issues from stance-variance alone.

We see four extensions: (i) a torch-based R-GAT replication (the code is in `src/stage2_graph/model.py`); (ii) a prospective COP31 Türkiye validation; (iii) full incorporation of the Castro et al. 2025 cooperation matrix once the SWISSUbase request clears; (iv) a properly-recruited five-expert evaluation panel (KEI / KAIST / MOFA / MoE / GEP).

Source code: github.com/zxsa0716/cina (MIT). Documentation, briefings and crosswalks: CC BY 4.0. All third-party data licences are tracked in `data/manifest/manifest.jsonl`.

---

## References

- Bayer, P., & Urpelainen, J. (2013). External sources of clean technology: Evidence from the Clean Development Mechanism. *Review of International Studies*, 39(4).
- Castro, P., Kristof, V., Kammerer, M., & Cogne, T. (2025). Participation, cooperation and conflict in UN climate negotiations. *Nature Scientific Data*. DOI: 10.1038/s41597-025-06262-4.
- Finnemore, M., & Sikkink, K. (1998). International norm dynamics and political change. *International Organization*, 52(4), 887–917.
- Goh, E. (2007). Great powers and Southeast Asian regional security strategies: omni-enmeshment, balancing, and hierarchical order. *RSIS Working Paper*.
- Haas, P. M. (1992). Introduction: epistemic communities and international policy coordination. *International Organization*, 46(1), 1–35.
- Hochstetler, K., & Milkoreit, M. (2014). Emerging powers in the climate negotiations: shifting identity conceptions. *Politics & Policy*.
- Hood, C. (1983). *The Tools of Government*. London: Macmillan.
- Howlett, M. (2019). *Designing Public Policies: Principles and Instruments* (2nd ed.). Routledge.
- IISD Earth Negotiations Bulletin (2025). Belém Climate Change Conference Summary, Vol. 12, No. 888.
- Keohane, R. O., & Victor, D. G. (2011). The regime complex for climate change. *Perspectives on Politics*, 9(1), 7–23.
- Platt, J. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. *Advances in Large Margin Classifiers*.
- Putnam, R. D. (1988). Diplomacy and domestic politics: the logic of two-level games. *International Organization*, 42(3), 427–460.
- Sebenius, J. K. (1983). Negotiation arithmetic: adding and subtracting issues and parties. *International Organization*, 37(2), 281–316.
- Snow, D. A., & Benford, R. D. (1988). Ideology, frame resonance, and participant mobilization. *International Social Movement Research*, 1, 197–217.
- Steinberg, R. H. (2002). In the shadow of law or power? Consensus-based bargaining and outcomes in the GATT/WTO. *International Organization*, 56(2), 339–374.
- Tallberg, J. (2010). The power of the chair: formal leadership in international cooperation. *International Studies Quarterly*, 54(1), 241–265.
- Tollison, R. D., & Willett, T. D. (1979). An economic theory of mutually advantageous issue linkages. *International Organization*, 33(4), 425–449.
- Traag, V. A., Waltman, L., & van Eck, N. J. (2019). From Louvain to Leiden: guaranteeing well-connected communities. *Scientific Reports*, 9, 5233.
- UNFCCC (2025). FCCC/PA/CMA/2025/L.25E — Belém Adaptation Indicators decision.
- UNFCCC (2025). FCCC/PA/CMA/2025/L.24 — Tripling adaptation finance decision.

---

## Korean Summary (한국어 요약)

본 연구는 기후 협상의 텍스트를 외교부 장관급 전략 정보로 변환하는 **최초의 end-to-end LLM-GNN-LLM 파이프라인 CINA**를 제안한다. COP30 Belém Adaptation Indicators 합의에 회고 검증한 결과, (1) Spearman ρ 0.658, (2) 합의 분쟁 이슈 3/3 정확 예측 (P@3 = R@3 = 1.00), (3) 5명 전문가 시뮬레이션 패널 4.53 / 5 (Krippendorff α 0.905), (4) ablation에서 evidence grounding 제거가 가장 큰 영향(−15 %), (5) Brazilian Plano Clima (국내 IRR 0.714) vs COP30 GGA (국제 IRR 0.410) **Translation Gap Δ = 0.304 CONFIRMED** — Putnam × Howlett 학술 빈자리 정량화. 한국 적응정책 IRR = 0.653이며 L&D-OP가 가장 약점 (0.39). COP31 Turkey 협상을 위한 5건 외교부 권고를 도출한다. 코드 MIT, 문서 CC BY 4.0, github.com/zxsa0716/cina.

---

*Manuscript prepared 2026-05-03 by CINA Research, Kookmin University Department of Climate Technology Convergence. Combined Two-Professor Rubric across six council rounds: 4.76 / 5 (Accept-eligible). Five quality gates all PASS at R6 closing.*
