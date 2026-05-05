# 📋 Pre-Registration: CINA Prospective Validation on COP31

> **Pre-registered**: 2026-05-04
> **Author**: Heedo Choi (최희도) · Kookmin University, Department of Climate Technology Convergence
> **Project**: CINA (Climate Issue-Network Analysis)
> **Code freeze (planned)**: GitHub release tag `v3.0-prereg-cop31` at commit hash to be assigned 2026-09-01
> **Validation event**: COP31 (Türkiye, 9–22 November 2026)
> **Validation source**: IISD Earth Negotiations Bulletin final report (released ~2026-12-01)
> **Storage**: This document, hashed and committed to GitHub, serves as the immutable pre-registration. A copy will be uploaded to OSF with the same content.

---

## 1. Background and rationale

The retrospective validation reported in Choi (2026, working paper) showed that CINA's Stage 1 multi-axis stance extraction, applied to the pre-COP30 corpus, identified the three contested issues at COP30 (GGA-IND, ADAPT-FIN, L&D-OP) with P@3 = R@3 = 1.00. Because retrospective tests cannot rule out post-hoc fitting, this pre-registration commits CINA to specific predictions on COP31 *before the negotiation begins*, with falsification criteria fixed in advance.

This pre-registration follows the spirit of the Open Science Framework (OSF) protocol but is hosted on the project's GitHub repository for permanence and version control.

---

## 2. Hypotheses

Each hypothesis is paired with a falsification criterion. All thresholds are set in advance and will not be adjusted after data collection. We use a Bonferroni-corrected α level of 0.05 / 4 = **0.0125** for the four hypotheses.

### H1 — Contested-issue prediction continuity
> **The three issues with the highest CINA-extracted stance variance among the COP31 adaptation agenda will overlap with at least 2 of the 3 issues reported as contested in the IISD ENB COP31 final report.**

- **Test statistic**: |predicted top-3 ∩ ENB contested set| ≥ 2
- **Falsification**: |overlap| ≤ 1
- **Significance**: Under H₀ that CINA carries no signal, the probability of at least 2/3 overlap by chance (assuming 6 candidate issues) is C(3,2)·C(3,1)/C(6,3) + C(3,3)/C(6,3) = 9/20 + 1/20 = 0.50. We require ≥ 2/3 overlap as a one-sided test; the joint probability of H1 + H2 + H3 + H4 holding by chance is ≪ 0.0125.

### H2 — Chair Translation Gap persistence
> **Türkiye's domestic-international policy-instrument divergence Δ_Türkiye, computed from a Türkiye national adaptation plan (or equivalent climate policy document published before 2026-09-01) versus the COP31 adopted decision text, will be ≥ 0.20.**

- **Lower bound**: Δ ≥ 0.20 (looser than Brazil's measured Δ = 0.30 to allow for cross-country baseline differences)
- **Falsification**: Δ < 0.20 — would suggest chair-mediated divergence is Brazil-specific rather than a general chair pattern
- **Robustness check**: Replicate the Δ measurement using both the LLM-extracted instrument signals and a manual NATO 4-axis coding of the same texts; both must independently meet the threshold.

### H3 — Korean NAP pen-holder signal stability
> **The CINA-extracted Korean stance on the NAPs issue at COP31 (using documents published 2025-12-01 to 2026-09-01) will be ≥ 0.65 with `is_pen_holder = true` in at least 60 % of multi-sample runs (k = 5).**

- **Falsification**: stance < 0.50 OR is_pen_holder rate < 40 %
- **Interpretation**: Tests whether procedural-authority signals are stable over a one-year horizon, separate from issue-level stance shifts.

### H4 — AILAC norm-entrepreneur metric stability
> **AILAC's NES (Norm Entrepreneur Score, Choi 2026 §4.5) at COP31, computed using the same four criteria (frame consistency, stance strength, tipping-point evidence, norm transfer), will be ≥ 0.80.**

- **Falsification**: NES < 0.70
- **Interpretation**: Tests whether the small-state norm-entrepreneur position is a stable structural feature or a Brazil-presidency artefact.

---

## 3. Data and code freeze

### 3.1 Code freeze

- **Commit hash**: To be added at 2026-09-01 (two months before COP31). All analysis code (Stage 1 extraction prompts, Stage 2 graph analysis, Δ computation, NES computation) will be frozen at this commit and tagged `v3.0-prereg-cop31`.
- **No post-hoc edits**: Any code change after the freeze must be (a) clearly documented in a separate commit, (b) marked as "post-registration analysis", and (c) not mixed with the primary H1–H4 evaluation.

### 3.2 Data freeze (input)

- **Pre-COP31 corpus**: All UNFCCC documents, NDCs, ENB summaries, and government publications dated **before 2026-09-01** (cut-off date).
- **Manifest snapshot**: A manifest.jsonl snapshot will be committed at the freeze date with sha256 for each input document.
- **Excluded**: Any document published 2026-09-02 onwards, even if available before COP31, will not be used for prediction (to prevent data leakage).

### 3.3 Validation source (output)

- **Primary**: IISD Earth Negotiations Bulletin final COP31 report (~2026-12-01).
- **Secondary**: UNFCCC L-document final adopted texts (FCCC/PA/CMA/2026/L.x).
- **Tie-breaker**: If contested-issue identification differs between IISD ENB and UNFCCC text, both will be reported and the more conservative (lower P@3) used as primary.

---

## 4. Pre-specified analysis plan

### 4.1 Primary analysis (H1)

1. Run frozen CINA Stage 1 on the pre-COP31 corpus.
2. Compute stance variance σ²_i for each of the 6 adaptation issues.
3. Rank issues by σ² and select top-3.
4. After IISD ENB COP31 publication, identify the contested-issue set per their reporting.
5. Compute |overlap|.
6. Report the one-sided test result with the pre-specified threshold.

### 4.2 Secondary analyses (H2, H3, H4)

H2: Compute Δ_Türkiye using the same NATO 4-axis extraction protocol as Brazil. Report 95 % bootstrap CI.

H3: Run k = 5 multi-sample on Korean stance for NAPs over the pre-freeze corpus. Report mean stance and `is_pen_holder` rate.

H4: Re-evaluate AILAC's four norm-entrepreneur criteria using the post-COP30 corpus. Report NES with weighted sum (weights: 0.25, 0.25, 0.30, 0.20 as in Choi 2026).

### 4.3 Sensitivity analyses (post-registered)

- Vary Stage 1 LLM provider (Gemini vs. Groq vs. Anthropic) and report cross-LLM consistency Krippendorff α on H1's predicted top-3.
- Vary the cut-off date (2026-09-01 ↔ 2026-08-15) and report whether top-3 ranking changes.

---

## 5. Multiple-comparison correction

- Family-wise α = 0.05.
- Number of hypotheses: 4 (H1, H2, H3, H4).
- Bonferroni-corrected α per hypothesis: 0.05 / 4 = **0.0125**.
- All four hypotheses must independently meet their thresholds for the registration to be reported as "fully confirmed". Partial confirmation will be reported transparently.

---

## 6. Deviations and stopping rules

- **No optional stopping**: The analysis will be run exactly as specified above on exactly one date (after IISD ENB final report publication).
- **No HARKing**: Hypotheses will not be modified after looking at the data. Any post-hoc analyses will be clearly labelled as exploratory.
- **Deviations**: If any deviation from this plan becomes necessary (e.g., COP31 cancellation, ENB report unavailable), the deviation and reason will be documented in `PREREGISTRATION_COP31_DEVIATIONS.md` with a timestamp.

---

## 7. Reporting format

The validation result will be reported in:

1. A short technical report (`COP31_VALIDATION_REPORT.md`) within 4 weeks of ENB publication.
2. A revised section of the working paper (Choi 2026, working paper) under §7.2 "Prospective validation".
3. A submission to the NeurIPS Climate Change AI 2026 Workshop (post-COP31) or a subsequent venue.

If H1 fails, the working paper title will be updated to "Preliminary methodology with negative prospective validation" and the methodology section revised accordingly. Negative results will not be hidden.

---

## 8. Conflicts of interest

The author declares no conflicts of interest. This is a single-author graduate-research project with no industry funding.

---

## 9. Ethics

This research uses only publicly available textual data (UNFCCC documents, government publications, IISD ENB). No human subjects are involved. Per Korean institutional review standards, IRB review is not required.

---

## 10. Cryptographic commitment

The SHA-256 hash of this file as committed to GitHub at the freeze date will serve as the immutable pre-registration timestamp. Hash will be recorded here at freeze:

```
SHA-256: <to be filled at 2026-09-01 freeze>
GitHub commit: <to be filled>
GitHub release tag: v3.0-prereg-cop31
```

---

**Pre-registration prepared by**: Heedo Choi (최희도)
**Email**: zxsa0716@kookmin.ac.kr
**ORCID**: (pending registration)
**Date**: 2026-05-04 (pre-freeze draft)
**Final freeze planned**: 2026-09-01
