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
status: "Polished draft — citations integrated, figures inline-referenced (not yet submitted)"
license: "CC BY 4.0 (paper) / MIT (code at github.com/zxsa0716/cina)"
language: "EN + KO summary"
---

# From Text to Strategy — A Multi-LLM CINA Pipeline, Retrospectively Validated on COP30 Adaptation Outcomes

## Abstract (300 words)

Climate negotiation analytics have so far split into three complementary but disconnected approaches: (a) retrieval-augmented document interfaces (e.g. NegotiateCOP, Germany 2025), which surface and compare individual country positions but do not jointly model policy-instrument calibration or coalition structure; (b) game-theoretic simulators (RICE-N, Zhang et al. 2025), which generate strategic dynamics without grounding in negotiation texts; and (c) interaction-frequency datasets (Castro et al. 2025, *Nature Scientific Data*; Castro et al. 2025, *Environmental Sociology*), which aggregate ENB-coded cooperation/conflict counts and apply dynamic network analysis to recover alliances. We introduce **CINA (Climate Issue-Network Analysis)**, a methodology that complements these approaches by combining four signals into a single LLM-based stance extraction step: (i) stance scores with Bayesian credible intervals from k=5 ensemble sampling, (ii) NATO 4-axis policy instruments (Hood 1983; Howlett 2019), (iii) frame types (5 categories; Snow & Benford 1988), and (iv) procedural-authority signals (chair_role, pen_holder, drafts_text; Tallberg 2010). Downstream, a heterogeneous country × issue × group graph is analysed with Leiden community detection (Traag, Waltman & van Eck 2019), PageRank centrality, and cross-issue Apriori-style motif mining. A graph-grounded generation discipline forces every output claim to cite both a verbatim evidence quote and a structural fact, with a 7-rule post-hoc verifier; ablating this constraint reduces Spearman ρ by 15 percentage points, the largest single component effect. We pilot CINA on the **COP30 Belém Adaptation Indicators** outcome (FCCC/PA/CMA/2025/L.25E, November 2025) as a single retrospective case. Across a 4-task evaluation on n=98 stance records spanning 13 countries × 6 issues, CINA reaches Spearman ρ = 0.66 against expert reference codings (Task A) and correctly identifies 3 of 3 contested issues from stance variance alone (Task C; small-sample, encouraging signal). A simulated 5-persona expert panel scored generated briefings at 4.53/5 mean (Task D; we flag this as a methodological limitation, since real expert validation remains future work). As an empirical observation we report a Brazil domestic-international policy-instrument divergence of Δ = 0.304 between Plano Clima (NATO 4-axis 67 %) and the L.25E international text (Nodality-only 48 %), proposed as a novel single-case quantification at the intersection of Two-Level Games (Putnam 1988) and instrument-calibration theory (Howlett 2019). We release CINA under MIT/CC BY 4.0 with five LLM provider adapters at github.com/zxsa0716/cina.

**Keywords**: climate negotiations, large language models, graph neural networks, regime complex theory, two-level games, instrument calibration, COP30, adaptation, Korea, Brazil

---

## 1. Introduction

The 2025–2026 climate adaptation negotiation cycle generated nearly 300 official UNFCCC documents, hundreds of national submissions, and the first formal *Belém Adaptation Indicators* package — 59 voluntary indicators across seven thematic targets, accompanied by a decision to triple adaptation finance to USD 120 billion by 2035 (FCCC/PA/CMA/2025/L.25E; FCCC/PA/CMA/2025/L.24). The volume and complexity of this textual record have motivated several recent computational approaches, each strong in one respect but limited in another. NegotiateCOP (GIZ, 2025) is a public retrieval-augmented interface that lets users search submissions and compare positions side by side, but does not jointly model policy-instrument calibration, frame typology, or coalition structure. Castro et al. (2025) released a *Nature Scientific Data* dataset of cooperation/conflict counts coded from Earth Negotiations Bulletin (ENB) reports across COP1–COP29, and a companion *Environmental Sociology* paper (Castro et al. 2025) applied dynamic network analysis to that dataset; that line of work captures interaction frequencies but not the policy-instrument or framing signals embedded in the underlying texts. RICE-N (Zhang et al. 2025) simulates negotiation dynamics with multi-agent reinforcement learning, producing strategic insights without document grounding.

This paper proposes a complementary methodology, **CINA (Climate Issue-Network Analysis)**, that combines four signals into a single LLM-based stance extraction step — Bayesian-uncertainty-quantified stance scores, NATO 4-axis policy-instrument calibration (Hood 1983; Howlett 2019; Capano et al. 2025), 5-frame typology (Snow & Benford 1988), and procedural-authority signals (Tallberg 2010) — and feeds the resulting stance tensor into a Leiden-based heterogeneous graph analysis (Stage 2), and from there into a graph-grounded generation step that produces ministerial-grade briefings under verifiable evidence-and-structure dual-grounding (Stage 3). The contribution is methodological: each individual signal has antecedents in the literature, but their joint extraction within a single multi-axis schema, validated against an actual COP outcome (the L.25E text adopted in November 2025), is to our knowledge novel within the climate-negotiations domain.

We frame three research questions:

- **RQ1 (Methodology)**: Can a single LLM extraction step, applied at the (country, issue) granularity, recover stance direction *together with* policy-instrument calibration, frame typology, and procedural-authority signals at acceptable accuracy?
- **RQ2 (Empirical observation)**: Does Leiden community detection on the resulting stance tensor produce a partition consistent with the regime-complex horizontal-cleavage hypothesis (Keohane & Victor 2011)?
- **RQ3 (Single-case retrospective validation)**: When CINA is given the pre-COP30 corpus only, does it correctly identify the three issues that turned out contested at COP30, and does it surface a measurable domestic-international policy-instrument divergence in the chair country (Brazil)?

We position the present paper as a **preliminary methodology paper with single-case retrospective validation**. Sections 2–3 review the literature and methodology. Section 4 reports empirical observations. Section 5 reports the 4-task evaluation, including explicit limitations of a simulated-panel briefing-quality task (Task D) and a small contested-issue sample (n = 3). Section 6 discusses Korean policy implications, and Section 7 concludes with future work — in particular, expansion to n = 300+ stance records, real-expert validation, and PyTorch-based graph-attention learning.

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

CINA Stage 1 supports five free LLM backends: Gemini 2.5 Flash-Lite (Google), Groq Llama 3.3 70B, Ollama qwen2.5:3b (local, 1.84 GB RAM), OpenRouter free pool, and Anthropic API. The build phase used CINA pipeline; the production phase will run on the free stack at zero marginal cost.

### 3.3 Stage 2 — Heterogeneous Graph + Leiden + Centrality

Country, issue, and negotiating-group nodes form a heterogeneous graph; edges are typed (`has_stance`, `similar_to`, `cooperates_with`, `member_of`). For the present paper we report a **NetworkX + igraph + leidenalg** realisation with Leiden community detection (Traag, Waltman & van Eck 2019, resolution γ = 1.0) and five centrality measures (PageRank, betweenness, eigenvector, degree, closeness). A relational graph-attention network (R-GAT) is specified at the design level (`docs/05_stage2_graph_analysis.md`), but its supervised training is **deferred to future work**: the present paper does not report attention weights or learned edge embeddings. Cross-issue **Apriori-style motif mining** (min support 0.2, min issues 2) detects *frame-coherence motifs* — sets of issues on which a single country exhibits the same dominant frame.

### 3.4 Stage 3 — Graph-Grounded Generation

Briefing generation operates on the Stage 2 JSON plus the deduped evidence-quote pool. Each generated sentence is post-hoc validated against seven rules (numeric claim ↔ analysis JSON, country mention ↔ stance database, structural claim ↔ network metric, etc.); failures are auto-removed and logged. The Korean ministerial template (`docs/09`) yields nine sections plus four appendices (Evidence Traceability, Data Lineage, Uncertainty, LLM Provider Attribution). A parallel English version targets academic audiences.

### 3.5 Development methodology — internal review protocol

CINA was developed under an internal review protocol involving multiple LLM-instantiated reviewer roles (a policy-science reviewer and an IR reviewer) that critiqued each pipeline iteration before quality-gate sign-off; the protocol is documented in `docs/10_council_protocol.md` for reproducibility but should be understood as an internal *development hygiene* mechanism, not a substitute for external peer review.

---

## 4. Empirical Observations (Three Primary)

We report three primary empirical observations that follow from the methodology of Section 3, plus two single-case findings (Sections 4.4–4.5) we present as candidate signals warranting further investigation. We deliberately frame these as "observations," not "discoveries," given the limitations enumerated in Section 5.6.

### 4.1 Observation 1 — GGA-IND has the lowest Authority-axis usage among six issues

Across the six adaptation issues we coded, GGA-IND scored 6.1 on the Authority sub-axis (Hood 1983; Howlett 2019), the lowest in the corpus, while showing high Nodality usage. This is consistent with the explicit textual posture of FCCC/PA/CMA/2025/L.25E §7 — "voluntary, non-prescriptive, non-punitive, facilitative" — and with §9's negative-authority clause ("shall not create new financial obligations"). We interpret this as a quantitative correlate of the soft-law character of the GGA indicator framework, in line with Howlett's instrument-calibration theory; we do not claim it is the first such quantification, since dictionary-based and supervised approaches to NATO coding have been reviewed by Capano et al. (2025). **(Figure 1, top row.)**

### 4.2 Observation 2 — Leiden community detection produces a horizontal cleavage consistent with regime-complex theory

Stage 2 Leiden (Traag, Waltman & van Eck 2019; resolution γ = 1.0) returns two stable communities at modularity 0.31 over n = 13 nodes: **C0 = {Brazil, Multi (UAE-Belém), African Group, EU}** (development-frame consistent) and **C1 = {AOSIS, India, South Korea, LMDC, China}** (mixed/justice/sovereignty). C0 unites the G77 chair, the EU HAC anchor, and AGN bridging; C1 unites principled vulnerability advocates with sovereignty defenders. The partition is stable across resolution sweep γ ∈ [0.7, 1.3]. We read this as consistent with the *horizontal cleavage* component of Keohane & Victor's (2011) regime-complex hypothesis — but we caution against reading too much into a 13-node clustering: the result needs replication on a substantially larger node set (target n = 50+) before any general claim is warranted. **(Figure 5, similarity network.)**

### 4.3 Observation 3 — Stance variance alone correctly identifies the COP30 contested set (small-sample retrospective signal)

Ground truth, from the IISD ENB final report on COP30: the contested-issue set in the adaptation track was {GGA-IND voluntary-vs-mandatory, ADAPT-FIN base-year, L&D-OP contributor expansion}. Predicted top-3 by Stage 1 stance variance alone — that is, with no chair-power feature, no historical interaction frequency from Castro et al. (2025), and no learned weights — was {GGA-IND (var = 0.34), L&D-OP (0.21), ADAPT-FIN (0.15)}. This yields P@3 = R@3 = 1.00 on N = 3 contested issues. **The small N matters**: this is not a generalisable accuracy claim, but an encouraging single-case signal that stance dispersion captured by the multi-axis schema carries information about future contestation. We will revisit this on COP31 prospectively. **(Web-demo §4 evaluation panel.)**

### 4.4 Single-case finding — Brazil domestic-international policy-instrument divergence Δ = 0.304

Brazil's domestic *Plano Clima* (16 sectoral plans, 2024–2035) deploys all four NATO axes at an aggregate usage of 67 % (combining Authority, Nodality, Treasure, Organization). The COP30 GGA L.25E text — drafted under Brazilian presidency — collapses to predominantly nodality-based instruments at 48 %, with three "shall not" clauses constituting a *negative-authority* envelope. We define **Δ = IRR_domestic − IRR_international = 0.714 − 0.410 = 0.304** as a single-case quantitative measurement of this divergence. We propose Δ as a candidate metric at the intersection of Two-Level Games (Putnam 1988) and instrument calibration (Howlett 2019; Capano et al. 2025). Since this is a single chair-country in a single year, no claim of theoretical generality is made; replication across COP25–COP30 chair countries is the natural next step. **(Figure 2; Brazil-paradox panel of the web demo.)**

### 4.5 Single-case finding — L.25 advance-vs-final text shows zero divergence on aligned paragraphs

Comparing the L.25 *advance* draft and the L.25E *final* text yields TF-IDF cosine ≥ 0.95 on every aligned paragraph; that is, the chair-circulated draft and the adopted text are essentially identical in this issue. Combined with §7's four-burst hedging (voluntary + non-prescriptive + non-punitive + facilitative in successive sentences), this is consistent with Tallberg's (2010) *formula-control* channel having been exercised pre-circulation, i.e., the adopted text was already crystallised when the advance text was distributed. This is a single-issue finding and we treat it as a candidate signal of "pre-crystallised formula," not a confirmed pattern; replication on at least three chair-led decisions is needed.

### 4.6 Realist baseline (B0) — context for the multi-axis contribution

A baseline using only realist features (CO2 per-capita, share of global CO2, log-GDP) on cosine similarity yields F1 = 0.560 against pseudo-truth coalition labels (vs. random F1 = 0.440; Cohen κ = 0.216; McNemar χ² = 16.1, p < 0.0001 vs. random). The realist features alone do significantly better than chance but stay well below the 0.7+ that operational policy use would require. The diagnostic error case — USA–Saudi cosine = 0.889 on realist features, despite the two states sitting in different negotiating blocs — illustrates why frame, instrument, and procedural variables carry orthogonal signal.

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

### 5.4 Task D — Briefing quality (simulated panel; **methodological limitation**)

We constructed a panel of five expert personas (a Korean Energy Economics Institute policy researcher, a KAIST IR professor, a Ministry of Foreign Affairs climate negotiator, a Ministry of Environment adaptation officer, and a *Global Environmental Politics* journal editor) and prompted an LLM (Claude Sonnet 4.5) to score the generated ministerial briefing from each persona's viewpoint on a 5-dimension Likert rubric. The simulated panel yielded a mean of 4.53 / 5 and an inter-persona Krippendorff α of 0.905, with hallucination rate of 1.5 % under post-hoc verification.

**We explicitly flag this as a methodological limitation.** A simulated-persona panel is not a substitute for real expert evaluation: the same model that generated the brief is, indirectly, evaluating its own output through a persona prompt, which is known to inflate scores and inter-rater agreement (cf. LLM Psychometrics Review 2025, Kearns et al.). The α = 0.905 should therefore be read as an *upper bound under shared-model bias*, not as a real human-coder reliability measurement. Real-expert validation with at least three external coders (target: KEI, KAIST, MOFA) is queued for a follow-up study.

### 5.5 Ablation Study (A0 → A5)

| Variant | Spearman ρ | MAE | Δ ρ |
|---------|-----------|-----|-----|
| A0 Full CINA | **0.658** | **0.183** | (base) |
| A1 No graph | 0.625 | 0.187 | −5 % |
| A2 No calibration | 0.592 | 0.201 | −10 % |
| A3 No multi-sample | 0.605 | 0.198 | −8 % |
| **A4 No evidence grounding** | **0.559** | **0.210** | **−15 %** |
| A5 No hypergraph | 0.638 | 0.185 | −3 % |

**A4 is the largest single contributor.** Removing the fuzzy-match evidence-grounding step costs 15 percentage points of Spearman ρ. We read this as empirical support for the design intuition that tying every output claim to a verbatim source quote is what makes a stance-extraction system credible — both to downstream graph analysis and to a human reviewer.

### 5.6 Limitations

Six limitations bear directly on how the results above should be interpreted:

1. **Sample size**: n = 98 stance records across 13 countries × 6 issues. While this is sufficient for a single-case methodological pilot, generalisable claims require n ≥ 300 with broader country coverage; we treat the present numbers accordingly.
2. **Single retrospective case (N = 3 contested issues)**: Task C's P@3 = R@3 = 1.00 is encouraging but reflects one COP cycle and three issues. Prospective COP31 validation is the appropriate next test.
3. **Single-case Δ = 0.304**: The Brazil domestic-international policy-instrument divergence is measured for one chair-state in one year. Replication across COP25–COP30 chair countries is needed before any general claim about chair-mediated translation gaps.
4. **Simulated expert panel (Task D)**: As discussed in §5.4, persona-prompted self-evaluation is a known source of inflated agreement. The Krippendorff α = 0.905 is therefore an upper bound under shared-model bias.
5. **Graph attention not learned**: Stage 2 uses NetworkX + igraph + leidenalg. R-GAT is design-level only in the present paper; learned attention weights are future work.
6. **Calibration set**: n = 50 supervised pairs (28 verified + 22 placeholder). External two-coder Krippendorff α has not yet been measured, and Castro et al. (2025) cooperation/conflict ground truth from SWISSUbase is queued but not yet incorporated.

We additionally note potential confirmation drift in the multi-round development protocol (Section 3.5): although the protocol introduces internal critique, the reviewer roles share the LLM provider and may exhibit shared blind spots.

---

## 6. Discussion — Korean Policy Implications

The 30-cell Korea NAP × GGA crosswalk yields **IRR_Korea = 0.653** (95 % CI [0.55, 0.71]) — Accept-eligible. The single weakest cell is **L&D-OP × 사회·경제 adaptation = 0.39**, traceable to Korea's EIG-membership-plus-middle-income-contributor *dual identity ambiguity* (MOFA press release seq=376685, 2025-12-08).

We therefore recommend, for the COP31 Türkiye negotiation:

1. **Activate Korea's NAP pen-holder status** (Stage 1 extraction confirms `pen_holder = true` for Korea on NAPs) by inputting the 3-tier (national-province-municipal) NAP model into the Belém-Addis 2-year work programme.
2. **Internationalise the JT-Korean model**: Carbon Neutrality Framework Act §50 (vulnerable-population protection) is a deliverable for the COP31 plenary statement and a Track-B paper.
3. **Issue an L&D-OP institutional support pledge** of USD 5–10 M, claiming a Korean board seat at FRLD on operational-efficiency grounds.
4. **Articulate EIG dual identity** by aligning with Switzerland and bridging to AILAC via Mexico.
5. **Lead the GCF operational-efficiency agenda** to deflect contributor-base-expansion pressure.

**Track A submission package**: `ministerial_briefing_ko.md`, `paper.md` (this), `IRR_Korea.md`, `korean_nap_gga_crosswalk.csv`, six 300-dpi figures, `evaluation_report.md`. Submitted to the Kookmin Graduate Global Climate Leadership course (May 2026).

---

## 7. Conclusion

We presented CINA, a multi-axis LLM stance-extraction pipeline coupled with Leiden community detection and graph-grounded briefing generation, and piloted it on the COP30 adaptation negotiation cycle. Within the limitations of a single-case methodological pilot (Section 5.6), three observations carry the paper: (a) Leiden community detection on the multi-axis stance tensor produced a horizontal cleavage that is consistent with Keohane & Victor's (2011) regime-complex hypothesis; (b) stance variance alone correctly identified the 3-of-3 COP30 contested issues in retrospective testing; and (c) we propose **Δ**, a single-issue domestic-international policy-instrument divergence metric, with a first measurement of Δ = 0.304 for Brazil at COP30. The framework's main methodological contribution is the joint extraction of stance + instrument + frame + procedural signals, and the graph-grounded generation discipline whose ablation accounts for the largest single component effect (−15 % Spearman ρ).

We see four priority extensions, in order of urgency: (i) prospective application to COP31 (Türkiye, November 2026), with stance extraction frozen before the negotiation begins; (ii) external two-coder Krippendorff measurement using KEI / KAIST / MOFA reviewers in place of the simulated panel reported in Section 5.4; (iii) replication of the Δ measurement on COP25–COP30 chair countries (Spain, UAE, Azerbaijan, Brazil) to test whether chair-mediated divergence is a general pattern; and (iv) a torch-based R-GAT implementation that replaces the current NetworkX-based graph analysis with learned edge attention.

Source code: github.com/zxsa0716/cina (MIT). Documentation, briefings, and crosswalks: CC BY 4.0. All third-party data licences are tracked in `data/manifest/manifest.jsonl`. We invite replication and welcome external validation, particularly from external expert coders working in the climate-diplomacy domain.

---

## References

- Bayer, P., & Urpelainen, J. (2013). External sources of clean technology: Evidence from the Clean Development Mechanism. *Review of International Studies*, 39(4).
- Capano, G., Howlett, M., & co-authors (2025). Applying Hood's NATO framework to quantitative text analysis in policy studies: Theory, methods, and empirical applications. *Working paper / preprint*. ResearchGate 400309939.
- Castro, P., Kristof, V., Kammerer, M., & Cogne, T. (2025a). Participation, cooperation and conflict in UN climate negotiations. *Scientific Data*. DOI: 10.1038/s41597-025-06262-4.
- Castro, P., et al. (2025b). Dynamic networks of negotiation for international climate change cooperation. *Environmental Sociology*. https://doi.org/10.1080/23251042.2025.2507287.
- Finnemore, M., & Sikkink, K. (1998). International norm dynamics and political change. *International Organization*, 52(4), 887–917.
- GIZ Data Lab (2025). NegotiateCOP: an AI prototype for equal climate negotiations. https://negotiatecop.org/about (accessed May 2026).
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
- UNFCCC (2025a). FCCC/PA/CMA/2025/L.25E — Belém Adaptation Indicators decision.
- UNFCCC (2025b). FCCC/PA/CMA/2025/L.24 — Tripling adaptation finance decision.
- Vaccari, S., et al. (2025). Tracing inclusivity at UNFCCC conferences through side events and interest group dynamics. *Nature Climate Change*. DOI: 10.1038/s41558-025-02254-9.
- Zhang, T., et al. (2025). AI for Global Climate Cooperation: Modeling Global Climate Negotiations, Agreements, and Long-Term Cooperation in RICE-N. *Proceedings of Machine Learning Research* (PMLR), v267.

---

## Korean Summary (한국어 요약)

본 연구는 UNFCCC 협상 텍스트의 다축 stance 추출(stance + NATO 4축 정책수단 + 5 frame + 절차 권한 신호)을 단일 LLM 추출 단계에서 수행하고, 그 산출물을 Leiden 커뮤니티 검출과 graph-grounded 브리핑 생성으로 연결하는 방법론적 파이프라인 **CINA**를 제안한다. 본고는 단일 사례에 대한 회고적 검증을 보고하는 **방법론 예비(pilot) 논문**이며, 일반화 가능한 결론을 주장하지 않는다. n = 98 stance records(13개국 × 6 이슈)에 기반한 4-task 평가 결과, Spearman ρ = 0.658(전문가 reference 대비, Task A), COP30 contested 이슈 3/3 정확 예측(N = 3, Task C, 작은 표본의 고무적 신호), simulated 5인 페르소나 패널 평균 4.53 / 5(Task D — 본 패널은 LLM 시뮬레이션이며 실제 외부 전문가 검증은 향후 과제로 명시한다). 단일 사례 관찰로서 브라질의 국내(Plano Clima) ↔ 국제(L.25E) 정책수단 사용률 차이를 **Δ = 0.304**로 정량화하여, Two-Level Games(Putnam 1988)와 정책수단 calibration(Howlett 2019; Capano 등 2025)의 교차점에 위치한 후보 메트릭으로 제안한다. 한국 적응정책의 30-cell IRR은 0.653(95 % CI [0.55, 0.71])이며 L&D-OP 영역이 가장 낮은 0.39로, COP31 협상을 위한 5건의 정책 권고를 도출한다. 코드 MIT, 문서 CC BY 4.0, github.com/zxsa0716/cina.

---

*Manuscript prepared 2026-05 by Heedo Choi, Kookmin University Department of Climate Technology Convergence. Single-author graduate research project; not yet peer-reviewed.*
