# 📄 NeurIPS Climate Change AI 2026 Workshop — short paper

> **Title**: Cross-Provider LLM Reliability and Emergent Procedural Attention for Climate Negotiation Analysis
> **Author**: Heedo Choi (최희도) · Kookmin University
> **Status**: Track 2 of 3-track publication strategy
> **Target venue**: NeurIPS 2026 Climate Change AI Workshop (https://www.climatechange.ai)
> **Format**: 4 pages strict (excluding references), single-column NeurIPS style
> **Submission deadline**: typically July 2026 (TBC at workshop CFP release)

---

## 1. Why this venue

per `docs/research/PUBLICATION_STRATEGY.md` Track 2:
- 75% acceptance probability (workshop ~50% baseline; ours has 4-axis novelty + cross-provider $\alpha$)
- Visible to the AI-for-climate community
- 4-page short = manageable scope
- Cites arXiv preprint (Track 1) for full method

---

## 2. 파일 구성

```
paper/neurips_workshop/
├── main.tex                       # 4-page short paper
├── fig8_rgat_training.png         # R-GAT training (4 panels)
├── fig9_cross_llm_alpha.png       # Cross-LLM α
├── fig12_modularity_pvalue.png    # Permutation null
├── fig14_chance_baseline.png      # Hypergeometric baseline
└── README.md                      # this file
```

References are inlined in `\begin{thebibliography}` (no separate .bib needed).

---

## 3. 컴파일 방법

### Local TeX Live

```bash
cd paper/neurips_workshop/
pdflatex main.tex
pdflatex main.tex
```

### Notes on neurips_2024.sty

The first `\usepackage{neurips_2024}` line assumes the official NeurIPS style file is on TeX path. If not:

- Download `neurips_2024.sty` from https://neurips.cc/Conferences/2026/CallForPapers
- Place in same folder as `main.tex`

If you compile without it, the document falls back to plain `article` class — works but page count may differ.

---

## 4. 4-page constraint check

| Section | Estimate |
|---------|---------|
| Abstract + §1 Introduction | 0.6 p |
| §2 Cross-Provider Reliability | 1.0 p |
| §3 Emergent Procedural Attention | 1.0 p |
| §4 Topological Validation | 0.5 p |
| §5 Retrospective Outcome Prediction | 0.5 p |
| §6 Discussion + Limitations | 0.3 p |
| §7 Conclusion | 0.1 p |
| **Body subtotal** | **~4.0 p** |
| References | unlimited (separate page) |

If overfull at compile-time:
- Trim the §3 attention discussion paragraph
- Compress Figure 1 caption
- Move `Why this matters` paragraph to footnote

---

## 5. 제출 체크리스트

### Pre-submission

- [ ] Verify NeurIPS CCAI 2026 CFP at https://www.climatechange.ai (check format/deadline)
- [ ] Anonymise: `\author{Anonymous Submission}` if double-blind required
- [ ] Compile to PDF, count pages with `pdfinfo main.pdf` → must be ≤ 4 (body)
- [ ] All figures rendering at 300 dpi
- [ ] arXiv DOI for `cina2026arxiv` reference (replace placeholder)

### Submission portal

- [ ] OpenReview account (https://openreview.net) — workshop typically uses OpenReview
- [ ] Upload PDF + (optional) supplementary code link
- [ ] Author bio: graduate student, Kookmin University
- [ ] Disclose dual venue submission (arXiv preprint OK, workshop accepts pre-prints)

### Post-decision

- [ ] If accepted: update `docs/research/PUBLICATION_STRATEGY.md` Track 2 ✅
- [ ] If revisions requested: address in 1-2 weeks
- [ ] If rejected: alternative venues = ICLR Climate Change Workshop, AAAI AI for Social Impact

---

## 6. 차이점 vs Track 1 arXiv preprint

본 4-page short는 arXiv preprint의 부분집합:
- **포함**: Cross-LLM α (§2), Emergent attention (§3), Permutation test (§4), Hypergeometric baseline (§5)
- **제외**: Theoretical framework (5 traditions), Brazil Δ=0.304, Korean policy implications, Ask CINA Program web demo

이러한 substantively narrower scope는 dual-submission 윤리적 문제 없음. arXiv는 "full method", workshop은 "two key methodological signals".

---

## 7. 변경 이력

- v1.0 (2026-05-07): Initial draft, 4 pages, 4 figures.

---

**Heedo Choi (최희도)** · zxsa0716@kookmin.ac.kr
