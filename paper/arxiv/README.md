# 📄 arXiv preprint package — Ask CINA

> **Title**: Ask CINA: A Multi-Axis LLM Pipeline with Cross-Provider Reliability for Climate Negotiation Analytics, Demonstrated on COP30 Adaptation Outcomes
> **Author**: Heedo Choi (최희도) · Kookmin University Department of Climate Technology Convergence
> **Status**: Track 1 of 3-track publication strategy (see `docs/research/PUBLICATION_STRATEGY.md`)
> **License**: paper CC BY 4.0 · code MIT
> **Target arXiv category**: cs.CL (primary) · cs.SI · physics.soc-ph (cross-list)

---

## 1. Why arXiv first

per `docs/research/PUBLICATION_STRATEGY.md` Track 1:
- 0 비용 / 0 risk / 100% 게재 가능
- DOI via Zenodo 연동 가능
- NeurIPS Workshop · KCI 한국어 paper의 인용 baseline

---

## 2. 파일 구성

```
paper/arxiv/
├── main.tex                  # main document (single .tex)
├── references.bib            # 25 BibTeX entries (natbib + plainnat)
├── figures/                  # 14 PNG figures (300 dpi)
│   ├── fig1_country_issue_heatmap.png
│   ├── fig2_procedural_authority.png
│   ├── fig3_frame_consistency.png
│   ├── fig4_centrality.png
│   ├── fig5_similarity_network.png
│   ├── fig6_hedging_density_2d.png
│   ├── fig7_translation_gap_brazil.png
│   ├── fig8_rgat_training.png
│   ├── fig9_cross_llm_alpha.png
│   ├── fig10_bayesian_decomposition.png
│   ├── fig11_stance_timeseries.png
│   ├── fig12_modularity_pvalue.png
│   ├── fig13_rgat_ablation.png
│   └── fig14_chance_baseline.png
└── README.md                 # this file
```

Embedded figures: 9 of 14 (fig1, 5, 7, 8, 9, 10, 11, 12, 13, 14). fig2/3/4/6 are released in the GitHub repo for further inspection but not embedded here for length.

---

## 3. 컴파일 방법

### Local TeX Live (recommended)

```bash
cd paper/arxiv/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Result: `main.pdf` (~12 pages)

### Overleaf (web)

1. Create new project → Upload `paper/arxiv/` folder zipped
2. Set compiler to **pdfLaTeX**
3. Set bibliography to **natbib**
4. Press Recompile

---

## 4. arXiv 제출 체크리스트

### Pre-submission

- [ ] Compile locally to verify PDF renders correctly
- [ ] Spell-check (LaTeX `aspell --check main.tex` or Overleaf integrated)
- [ ] All citations in `references.bib` resolved (no `[?]` in PDF)
- [ ] All figures in `figures/` referenced and rendering at 300 dpi
- [ ] Author email · ORCID (apply at https://orcid.org if not yet)
- [ ] Affiliation matches Kookmin official English name

### arXiv submission

- [ ] Account at https://arxiv.org (requires endorsement for cs.CL first time)
- [ ] If endorsement needed: contact Kookmin advisor or co-author from cs.CL with arXiv account
- [ ] Submit page: https://arxiv.org/submit
- [ ] Upload as **single .tar.gz** containing `main.tex`, `references.bib`, `figures/`
- [ ] Primary category: cs.CL · Cross-list: cs.SI, physics.soc-ph
- [ ] License: CC BY 4.0
- [ ] After processing: arXiv ID assigned (e.g., 2606.XXXXX)

### Post-submission (within 24h)

- [ ] DOI via Zenodo: link arXiv → Zenodo via https://zenodo.org/account/settings/github
- [ ] Update GitHub README badge with arXiv link + DOI
- [ ] Update `docs/research/PUBLICATION_STRATEGY.md` Track 1 status to ✅ COMPLETED
- [ ] Add arXiv link to CINA web (`docs/web/index.html` and `cina_program.html` footer)

---

## 5. 향후 후속 paper들과 관계

### Track 2 — NeurIPS CCAI Workshop (4-page short)
- 같은 데이터, 같은 method
- focus: cross-provider reliability + emergent chair-attention 두 가지만
- 본 arXiv preprint를 ``Choi 2026 [arXiv:2606.XXXXX] for full details''로 인용
- 작성: `paper/neurips_workshop/main.tex`

### Track 3 — KCI 한국어 (단저자, 25p)
- 다른 데이터: Korea NAP × GGA crosswalk 30-cell IRR
- 다른 framing: 한국 적응정책 글로벌 정합도 진단
- 본 arXiv를 영문 method reference로 인용
- 작성: `paper/kci_korean/manuscript.docx`

이 셋은 substantively different하므로 dual-submission 문제 없음 (ethics OK).

---

## 6. 알려진 한계 (이 preprint에서 명시한 것들)

§5.6 Limitations에 6가지 명시:
1. Sample size n=98 (98 < 300, 일반화 불가)
2. Single retrospective case (N=3 contested issues)
3. Single-case Δ=0.304 (Brazil only)
4. Simulated expert panel (α=0.905는 upper bound)
5. n=50 supervised pairs (부분 placeholder)
6. Confirmation drift (multi-LLM reviewer protocol)

이 한계들은 peer review에서 **언급될 것이지만 사전에 명시했으므로 reject 이유가 아닌 future work로 정리됨**.

---

## 7. 변경 이력

- v1.0 (2026-05-07): Initial arXiv-ready package, 12 pages, 14 figures total / 10 embedded.

---

**Heedo Choi (최희도)** · zxsa0716@kookmin.ac.kr · Kookmin University
