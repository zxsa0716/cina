# Contributing to CINA

Thanks for your interest in contributing to CINA — a graduate research project on
LLM-driven climate-negotiation analysis at Kookmin University. We welcome:

- 🐞 **Bug reports** — see `.github/ISSUE_TEMPLATE/bug_report.yml`
- 🎓 **Academic critique** — see `.github/ISSUE_TEMPLATE/academic_question.yml`
- 🔬 **Methodology extensions** — particularly the 8 paths laid out in [`METHODOLOGY_ADVANCEMENT_ROADMAP.md`](METHODOLOGY_ADVANCEMENT_ROADMAP.md)
- 📊 **Replication** — running `python -m src.run_all` on your hardware and reporting deviations
- 🌐 **Multi-lingual extension** — Stage 1 extraction in PT/ES/FR/AR (advancement E8)
- ✍️ **Real expert validation** — if you are a climate-diplomacy practitioner (KEI / KAIST / MOFA / GEP / etc.) willing to do blind coding, please email `zxsa0716@kookmin.ac.kr` directly.

---

## Quick start for contributors

### 1. Fork + clone + set up

```bash
git clone https://github.com/YOUR_USERNAME/cina
cd cina
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Verify the pipeline runs

```bash
python -m src.stage1_extract.llm_smoke_test --offline    # < 5 sec, exit 0
python -m src.run_all --skip-rgat                         # full pipeline minus R-GAT
```

If both succeed, your environment is good.

### 3. Make your change in a feature branch

```bash
git checkout -b feat/my-extension
# ... edit code ...
python -m src.run_all   # verify nothing broke
git add . && git commit -m "feat: short description"
git push origin feat/my-extension
```

### 4. Open a Pull Request

Use the template at `.github/PULL_REQUEST_TEMPLATE.md`. Tick the relevant boxes (stage, type, reproducibility, honesty checklist).

---

## Coding conventions

### Python

- **Python 3.11+**.
- Format with `black` (line length 100), lint with `ruff`. CI runs both.
- Type hints on all public functions; encouraged elsewhere.
- Module docstrings should describe (a) what the module does, (b) which advancement (E1-E8) or paper section it implements, (c) author + license.

### Filenames & versioning

- **No version-numbered filenames** (no `_v2`, `_v3`, `_final`, `_FINAL_v3`). Git is the version control system. New analyses get new descriptive names; the old name is removed in the same commit.
- One canonical artefact per concept. If you produce a new variant, replace, do not duplicate.

### Figures

- 300 dpi, white background, A4-friendly aspect ratio.
- Use the CINA palette in `src/viz/publication_figures.py::CINA_PALETTE`.
- DejaVu Sans typography.
- Spines top/right off; light grid (alpha 0.3).
- New figures should integrate into `src/viz/publication_figures.py` — do not create one-off scripts.

### Commits

- Imperative mood ("Add X", not "Added X" or "Adds X")
- First line ≤ 72 chars
- Body wrapped at 80 chars, separated by blank line
- One logical change per commit
- Reference issues with `Closes #N` / `Refs #N`

### Honesty / academic standards

This project follows the principles documented in [`CRITICAL_REVIEW.md`](CRITICAL_REVIEW.md):

- **No "first quantitative measurement" claims** without literature search to back them up.
- **Distinguish simulated from real expert validation** in any reported metric.
- **Disclose N (sample size)** explicitly for any new statistic.
- **Accurately describe baseline tools** (NegotiateCOP has Position Comparison; Castro 2025 includes a dynamic-network paper).
- **Frame contributions as "preliminary observations" or "single-case findings"** unless replication has been done.

PRs that introduce overclaims will be asked to revise.

---

## Reproducibility checklist (for empirical PRs)

- [ ] Random seed fixed (default 42) and documented
- [ ] Exact deps listed in `requirements.txt`
- [ ] `python -m src.run_all` produces the new numbers reproducibly
- [ ] If LLM call required, also include a deterministic fallback (cached response or synthetic dataset)
- [ ] Update `RUN_REPORT.md` template and `paper.md` numerical claims simultaneously

---

## Code of Conduct

By participating you agree to abide by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

---

## License

By contributing, you agree that your contributions will be licensed under:
- **MIT** for code (`src/`, `*.py`)
- **CC BY 4.0** for documentation, briefings, deliverables

---

## Contact

**Heedo Choi (최희도)** — zxsa0716@kookmin.ac.kr
Department of Climate Technology Convergence (기후기술융합학과), Kookmin University
GitHub: [@zxsa0716](https://github.com/zxsa0716)
