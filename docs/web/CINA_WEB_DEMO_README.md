# CINA Web Demo (`docs/web/`)

> Single-page interactive demo of the CINA framework + Korea/Brazil case studies.

## 🌐 Live Preview

Open `docs/web/index.html` in any browser, or deploy via GitHub Pages.

### GitHub Pages Setup
1. Repo Settings → Pages
2. Source: Deploy from branch
3. Branch: `main`, Folder: `/docs`
4. Save → site URL: `https://zxsa0716.github.io/cina/web/`

## 📂 Files

| File | Description |
|------|-------------|
| `index.html` | Main landing (10 sections) |
| `assets/style.css` | Modern dark theme + responsive |
| `assets/script.js` | Counters, scroll, data loader |
| `assets/data.json` | Real CINA data (98 stances + Leiden + IRR) |
| `figures/` | 6 PNG figures (300 dpi) |

## 📊 Sections

1. **Hero** — 4 key metrics (Combined Rubric 4.76, 5/5 PASS, 98 stances, 8 findings)
2. **Overview** — Existing tools vs CINA comparison (NegotiateCOP/RICE-N/Castro)
3. **Methodology** — 3-Stage pipeline + 5 LLM provider stack
4. **🇰🇷 Korea Case** — IRR 0.653, 30-cell crosswalk, 7 stance cards, 5 recommendations
5. **🇧🇷 Brazil Case** — Translation Gap Δ=0.304, chair power, pre-crystallized formula
6. **Coalition Map** — Leiden 2 communities, PageRank, frame motifs
7. **Findings** — 8 publishable-grade cards (5 venues)
8. **Evaluation** — Task A/B/C/D + Ablations A0-A5
9. **Figures** — 6 stage 2 visualizations
10. **Council Process** — R0→R6 progression, 5 agents
11. **Data** — 225 manifest, 14 sources, license tracking

## 🎨 Design

- Dark theme (matches academic GitHub Pages aesthetic)
- Responsive (mobile / tablet / desktop)
- Smooth scrolling, animated counters
- Real data embedded (no external API needed)
- Vanilla JS — no framework dependencies

## 🔁 Re-generate data

```bash
python -c "
import json
from pathlib import Path
# (see script in commit message — embeds latest stances + graph + IRR + eval)
"
```

## 📜 License

CC BY 4.0 (content), MIT (code structure).
