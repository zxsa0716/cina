# GitHub Repository — Production-Grade Setup Guide

> **Repository**: https://github.com/zxsa0716/cina
> **Author**: Heedo Choi (최희도) · Kookmin University
> **Last polish**: 2026-05-05

이 문서는 cina repository를 학술 표준으로 보이게 하는 **GitHub UI 설정** 권장사항입니다. 코드/파일이 아니라 GitHub 사이트의 클릭 한 번으로 적용 가능한 항목들입니다.

---

## 1. About 섹션 (repo 우측 상단)

**Description** (140자 제한):
```
Multi-axis LLM stance extraction + heterogeneous R-GAT + graph-grounded briefing for climate negotiation intelligence (COP30 retrospective)
```

**Website**:
```
https://zxsa0716.github.io/cina/
```

**Topics** (권장 15개):
```
climate-negotiations
cop30
cop31
unfccc
adaptation
large-language-models
graph-neural-networks
graph-attention-network
leiden-algorithm
regime-complex
two-level-games
norm-entrepreneur
policy-instruments
korea
brazil
```

→ Repo 메인 → 우측 ⚙️ Settings 옆 톱니바퀴 → topics/description 입력.

---

## 2. Social preview (Open Graph image)

**무엇**: Repo URL을 트위터/카카오/슬랙/링크드인에 붙였을 때 보이는 미리보기 이미지.

**권장 이미지**: `docs/web/figures/fig5_similarity_network.png` (Leiden 2 communities 네트워크) 또는 새 social_card.png 제작.

**적용 경로**:
1. Repo Settings → General → Social preview
2. "Edit" → Upload image
3. 권장 사이즈: 1280 × 640 px

만약 Open Graph 이미지 별도 제작 시 `docs/social_preview.png` 권장 위치.

---

## 3. README badges 정상화

현 README.md 상단의 badge들:

```markdown
![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab.svg?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.11-ee4c2c.svg?logo=pytorch&logoColor=white)
![License](https://img.shields.io/badge/License-MIT%20%2B%20CC%20BY%204.0-blue.svg)
![Spearman](https://img.shields.io/badge/Task%20A%20Spearman%20%CF%81-0.658-success)
![P@3](https://img.shields.io/badge/Task%20C%20P%403-1.00-success)
![Cross-LLM](https://img.shields.io/badge/Cross--LLM%20%CE%B1-0.93-success)
```

이미 readme.md 상단에 통합 적용됨. ✅

---

## 4. Releases & Tags

```bash
# 학술 버전 v3.0 release 예시
git tag -a v3.0.0 -m "Methodology advancement: R-GAT + Cross-LLM + Bayesian + Pre-registration"
git push origin v3.0.0
```

GitHub Releases 페이지 → "Draft a new release" → Tag v3.0.0 → Release notes:

```markdown
# v3.0.0 — Methodology Advancement Release

## What's new
- Real Heterogeneous R-GAT (PyTorch): val ρ = 0.708, emergent chair attention 1.00
- Cross-LLM Krippendorff α = 0.876 raw / 0.933 bias-corrected (5 providers)
- Bayesian 3-level variance decomposition
- OSF-style pre-registration for COP31 prospective validation
- Causal identification strategy (DiD/SC/IV)
- Master end-to-end orchestrator (src/run_all.py)
- Publication-grade figure suite under unified visual identity

## Citation
Choi, Heedo (2026). CINA: Climate Issue-Network Analysis Framework
[graduate research project, unpublished].
Department of Climate Technology Convergence, Kookmin University.
```

---

## 5. Pinned issues (선택)

Repo에 이슈 트래커가 있으면 다음 3개를 pin:

1. "🚀 Future work: COP31 prospective validation" — 2026-09-01 freeze
2. "🤝 Looking for external expert coders" — KEI/KAIST/MOFA
3. "📊 Open call for COP25-COP30 longitudinal data" — Castro et al. 2025 SWISSUbase access

---

## 6. GitHub Pages

```
Settings → Pages
  Source: Deploy from a branch
  Branch: main / docs
  Save
```

URL: `https://zxsa0716.github.io/cina/`

위 설정 후 1-3분 대기. CINA 메인 페이지가 docs/index.html을 통해 표시됨.

---

## 7. Discussions (선택)

```
Settings → Features → Discussions: Enable
```

카테고리 권장:
- 📢 Announcements (release 공지)
- 💡 Ideas (학술 확장 제안)
- 🙋 Q&A (사용법 질문)
- 🎓 Academic discussion (논문 비판)

---

## 8. Branch protection (선택)

```
Settings → Branches → Branch protection rules → Add rule
  Branch name pattern: main
  ☑ Require pull request reviews before merging
  ☑ Require status checks to pass
```

---

## 9. CodeQL / Dependabot (선택)

```
Settings → Code security & analysis
  ☑ Dependency graph
  ☑ Dependabot alerts
  ☑ Dependabot security updates
```

Python repo이므로 자동 보안 alert + version PR 자동 생성.

---

## 10. Profile README link (개인 GitHub)

자기 GitHub `@zxsa0716` profile에 cina를 pinned repo로 추가:

```
github.com/zxsa0716 → 우측 "Customize your pins" → cina 선택 → Save
```

---

## 11. arXiv preprint upload (학술용)

준비 완료 시:

```bash
# 1. Convert paper.md → LaTeX with pandoc
pandoc deliverables/paper.md -o paper.tex --bibliography=refs.bib

# 2. arXiv submit:
#    Account: arxiv.org
#    Category: cs.AI (primary), cs.CL (secondary), 22 IR (cross-list)
#    Submit arXiv → wait 1-2 days → arXiv ID assigned

# 3. Add arXiv badge to README
echo '[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)' >> README.md
```

---

## 12. Permanent identifiers

| Identifier | 용도 | 등록 방법 |
|-----------|-----|--------|
| **GitHub Release tag v3.0.0** | 코드 freeze 시점 | git tag |
| **Zenodo DOI** | 데이터셋 영구 보관 | github → zenodo 연동, release하면 자동 DOI |
| **arXiv preprint** | 학술 인용 가능 | 위 11번 |
| **ORCID** | 저자 영구 ID | https://orcid.org/register |

---

**작성**: 2026-05-05 · Heedo Choi (최희도)
