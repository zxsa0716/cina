# 📚 CINA Paper Drafts — 3-Track Publication Strategy

> **Strategic plan**: `docs/research/PUBLICATION_STRATEGY.md`
> **Author**: Heedo Choi (최희도) · Kookmin University · zxsa0716@kookmin.ac.kr
> **Status**: All 3 tracks drafted (2026-05-07), pending compile + review + submission

---

## Why 3 papers from 1 project?

The peer review session (D2 = 2.20 fail) honestly diagnosed that single Q1 journal submission is infeasible from current data ($n=98$ verified, single retrospective case). But the same assets support 3 substantively different papers in 3 different venues. This avoids overclaiming while maximising research output.

---

## Track 1 — arXiv Preprint (Full English Methodology)

| Field | Value |
|------|------|
| **Folder** | `paper/arxiv/` |
| **Title** | Ask CINA: A Multi-Axis LLM Pipeline with Cross-Provider Reliability for Climate Negotiation Analytics, Demonstrated on COP30 Adaptation Outcomes |
| **Length** | 12 pages, 10 figures embedded, 25 BibTeX entries |
| **Compile** | `pdflatex main && bibtex main && pdflatex main && pdflatex main` |
| **Venue** | arXiv (cs.CL primary) — peer-reviewed: NO |
| **Acceptance** | 100% (registration only) |
| **Time to upload** | 1 week |
| **Status** | ✅ Drafted, awaiting endorsement + submission |

---

## Track 2 — NeurIPS CCAI 2026 Workshop (English Short Paper)

| Field | Value |
|------|------|
| **Folder** | `paper/neurips_workshop/` |
| **Title** | Cross-Provider LLM Reliability and Emergent Procedural Attention for Climate Negotiation Analysis |
| **Length** | 4 pages strict (body) + unlimited refs, 4 figures |
| **Compile** | `pdflatex main && pdflatex main` |
| **Venue** | NeurIPS 2026 Climate Change AI Workshop — peer-reviewed: YES (single-blind) |
| **Acceptance** | 75% (workshop ~50% baseline; ours has differentiation) |
| **Deadline** | TBD (typically July 2026 for December workshop) |
| **Status** | ✅ Drafted, awaiting CFP open + submission |

---

## Track 3 — KCI 한국어 Paper (Korean Policy-Diagnostic Application)

| Field | Value |
|------|------|
| **Folder** | `paper/kci_korean/` |
| **Title** | 이행률 기반 한국 적응정책의 글로벌 정합도 진단 — 다축 LLM 추출 프레임워크 적용 사례 |
| **Length** | 25 pages markdown (→ docx via pandoc), 4 figures |
| **Author** | 단저자 또는 지도교수 공저 |
| **Venue** | 한국정책학회보 (KCI 우수등재) — peer-reviewed: YES |
| **Acceptance** | 60% (단저자) / 75% (공저) |
| **Submission** | 2026년 7-8월 |
| **Status** | ✅ Drafted, awaiting 한글화 검토 + .docx 변환 |

---

## Future Track 4 (12+ months out)

Q2 journal submission (Climate Policy or Global Environmental Politics) requires:
- $n \geq 300$ stance records (real, not heuristic)
- COP31 prospective validation (Nov 2026)
- 3+ external coder Krippendorff α
- Longitudinal dataset COP21–COP31

Folder placeholder: `paper/q2_journal/` (not yet created; awaits 12-month data extension).

---

## Why this is ethical

These 3 papers share a methodological foundation but differ substantively:
- **arXiv**: full method + 4 contributions across IR/policy/ML
- **Workshop**: 2 contributions (cross-provider α, emergent attention) — narrower
- **KCI**: different data (Korea NAP × GGA), different framing (정책 정합도), different recommendations (COP31 외교 전략)

All three explicitly cite each other, with arXiv as the canonical full reference. This pattern matches contemporary multidisciplinary research norms (cf. Lin et al. 2023; Stiennon et al. 2020).

---

## Compile Instructions Summary

```bash
# arXiv (full)
cd paper/arxiv && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

# Workshop (short)
cd paper/neurips_workshop && pdflatex main.tex && pdflatex main.tex

# KCI (markdown → docx)
cd paper/kci_korean && pandoc manuscript.md -o manuscript.docx
```

---

**Heedo Choi (최희도)** · 2026-05-07
