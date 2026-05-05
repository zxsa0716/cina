# 🖱️ 남은 3가지 GitHub UI 클릭 — 정확한 단계별 가이드

> **Pages는 이미 활성화됨** ✅ (`https://zxsa0716.github.io/cina/` 작동 중)
>
> 남은 3가지: ① About 입력 → ② Social preview 업로드 → ③ Release 발행
> 총 소요 시간: **약 3분**

---

## ① About 입력 (1분)

**왜**: GitHub 검색 가능성 + repo 첫인상. 우측 상단 사이드바에 description, website, topics가 나타납니다.

### Step-by-step

1. 브라우저 열고 → **https://github.com/zxsa0716/cina** 접속

2. **repo 메인 페이지 우측 상단**에 다음과 같은 영역이 보입니다:
   ```
   About                                    ⚙️
   ┌───────────────────────────────────┐
   │ No description, website, or       │
   │ topics provided.                  │
   └───────────────────────────────────┘
   ```

3. 그 옆의 **⚙️ (톱니바퀴 아이콘)** 클릭

4. "Edit repository details" 모달이 뜸. 다음 3개 필드 입력:

   **🔵 Description** (이걸 그대로 복사)
   ```
   Multi-axis LLM stance extraction + heterogeneous R-GAT + graph-grounded briefing for climate negotiation intelligence (COP30 retrospective)
   ```

   **🔵 Website**
   ```
   https://zxsa0716.github.io/cina/
   ```

   **🔵 Topics** (밑의 박스에 클릭하고 하나씩 입력하거나 한 번에 붙여넣기 — 공백으로 구분, 자동으로 chip이 됨)
   ```
   climate-negotiations cop30 cop31 unfccc adaptation large-language-models graph-neural-networks graph-attention-network leiden-algorithm regime-complex two-level-games norm-entrepreneur policy-instruments korea brazil
   ```

   ※ 각 단어 입력 후 **스페이스 또는 엔터** 누르면 chip으로 변환됨. 15개 모두 chip으로 보여야 함.

5. **체크박스** (선택):
   - ☑️ Releases
   - ☐ Packages (사용 안 함)
   - ☐ Deployments
   - ☐ Environments

6. 모달 하단 **[Save changes]** 버튼 클릭

7. **확인**: repo 메인 페이지로 돌아가면 우측 About 섹션에:
   ```
   About                                    ⚙️
   ┌───────────────────────────────────────┐
   │ Multi-axis LLM stance extraction +    │
   │ heterogeneous R-GAT + graph-grounded  │
   │ briefing for climate negotiation...   │
   │                                       │
   │ 🔗 zxsa0716.github.io/cina/           │
   │                                       │
   │ 🏷️ climate-negotiations  cop30        │
   │   cop31  unfccc  adaptation  ...      │
   └───────────────────────────────────────┘
   ```
   이렇게 보이면 완료.

---

## ② Social preview 업로드 (30초)

**왜**: 슬랙/카카오톡/트위터/링크드인에 GitHub URL을 붙이면 카드 형태 미리보기가 뜨는데, 이게 그 카드 이미지입니다.

**파일 위치 (정확한 경로)**:
```
C:\Users\admin\Desktop\대학원수업\1학기\리더쉽\docs\social_preview.png
```
- 크기: 1280 × 640 PNG (160 KB)
- 내용: CINA 로고 (그라디언트) + 4개 핵심 메트릭 chip (Spearman 0.658 / P@3 1.00 / Cross-LLM α 0.93 / R-GAT chair 1.00) + 우측 Leiden 2 communities 네트워크 다이어그램 (Brazil chair = gold glow) + URL pill

### Step-by-step

1. https://github.com/zxsa0716/cina 접속

2. 상단 탭에서 **[Settings]** 클릭 (가장 우측, 톱니바퀴 모양 옆)

3. 좌측 사이드바 → **General** (가장 위, 기본 선택돼 있음)

4. 페이지를 아래로 스크롤하면 **"Social preview"** 섹션이 보임:
   ```
   Social preview
   ──────────────────────────────────────────
   Upload an image to customize your
   repository's social media preview.
   Images should be at least 640×320px
   (1280×640px for best display).

   ┌──────────────────┐
   │  No preview       │
   │  uploaded.        │
   └──────────────────┘

   [Edit]  [Remove]
   ```

5. **[Edit]** 버튼 클릭 → 파일 선택 다이얼로그

6. 다음 경로로 이동:
   ```
   C:\Users\admin\Desktop\대학원수업\1학기\리더쉽\docs\
   ```
   (탐색기에서 위 경로를 주소창에 붙여넣고 엔터)

7. **`social_preview.png`** 선택 → **[열기]**

8. 자동 업로드. 미리보기가 즉시 표시됨.

9. **확인**: 트위터/슬랙에 `https://github.com/zxsa0716/cina`를 붙이면 그 카드가 뜸.

---

## ③ Release 발행 (1분)

**왜**: `v3.0.0` 태그는 이미 push되어 있지만, GitHub Releases 페이지에는 아직 보이지 않습니다. Release를 publish해야 사용자가 다운로드 가능한 zip + release notes가 표시됩니다.

### Step-by-step

1. 다음 URL로 직접 접속:
   ```
   https://github.com/zxsa0716/cina/releases/new
   ```
   또는 repo 메인 페이지 우측 사이드바의 **Releases** 섹션 클릭 → **[Draft a new release]**

2. **"Choose a tag"** 드롭다운 클릭 → 검색창에 `v3.0` 입력 → **`v3.0.0`** 선택
   (이미 존재하는 태그라 "Existing tag" 표시가 떠야 함)

3. **Release title** 입력:
   ```
   v3.0.0 — Methodology Advancement Release
   ```

4. **Describe this release** 큰 텍스트 박스에 아래 내용을 그대로 복사 → 붙여넣기:

   ```markdown
   # v3.0.0 — Methodology Advancement Release

   End-to-end re-execution + production-grade upgrade of CINA. Single
   command runs the full pipeline (`python -m src.run_all`); LLM
   provider stack is production-ready (`python -m
   src.stage1_extract.llm_smoke_test`); all 10 figures regenerated
   under unified visual identity.

   ## ✨ Highlights

   - **Real Heterogeneous R-GAT** (PyTorch, 200 ep) — val Spearman ρ
     = 0.708, **emergent chair-edge attention 1.00** (vs similarity
     0.28), supervision-free recovery of Tallberg (2010) procedural
     authority
   - **Cross-LLM Krippendorff α** — 0.876 raw / **0.933
     bias-corrected** over 5 providers, decoupled from shared-model
     bias
   - **Bayesian 3-level variance decomposition** — σ_country 54%,
     σ_group 37%, σ_regime 1.4% (transparent tension reporting)
   - **OSF-style pre-registration** for COP31 — 4 falsifiable
     hypotheses, Bonferroni α = 0.0125, code freeze 2026-09-01
   - **Causal identification strategy** — DiD + synthetic control + IV
     for generalising the Brazil Δ = 0.304 single-case finding
   - **Master orchestrator** `src/run_all.py` — 8 steps, generates
     `RUN_REPORT.md`
   - **Production figure suite** — 10 figures, 300 dpi, CINA palette
   - **5-page interactive web demo** — index / methodology /
     visualizations / outputs / sitemap

   ## 📚 Citation

   ```
   Choi, Heedo (2026). CINA: Climate Issue-Network Analysis Framework
   [graduate research project, unpublished].
   Department of Climate Technology Convergence, Kookmin University.
   https://github.com/zxsa0716/cina
   ```

   ## 📂 Key files

   - `deliverables/paper.md` — academic paper draft (3,500+ words, 28 references)
   - `deliverables/ministerial_briefing_ko.md` / `_en.md` — ministerial briefing
   - `RUN_REPORT.md` — auto-generated by master pipeline
   - `docs/research/CRITICAL_REVIEW.md` — self-critical literature review
   - `docs/research/METHODOLOGY_ADVANCEMENT_ROADMAP.md` — 8 extension paths
   - `docs/research/PREREGISTRATION_COP31.md` — prospective hypotheses

   ## 🔗 Web demo

   https://zxsa0716.github.io/cina/

   ## 🙋 Author

   **Heedo Choi (최희도)** · Kookmin University, Department of Climate
   Technology Convergence (기후기술융합학과) · zxsa0716@kookmin.ac.kr
   ```

5. 그 아래 옵션:
   - ☑️ **Set as the latest release** (이미 체크돼 있어야 함)
   - ☐ Set as a pre-release (체크 안 함)
   - ☐ Create a discussion for this release (선택, 체크해도 OK)

6. 우측 하단 **[Publish release]** 버튼 클릭 (또는 Save draft은 미공개)

7. **확인**: https://github.com/zxsa0716/cina/releases 에 v3.0.0이 표시됨

---

## ✅ 완료 후 결과

위 3가지가 끝나면 **https://github.com/zxsa0716/cina** 메인 페이지가 다음과 같이 보입니다:

```
┌───────────────────────────────────────────────────────────────┐
│  zxsa0716/cina  ⭐  ⑂                                           │
│                                                                │
│  [README 본문]                                                  │
│                                                                │
│  ─────────────────────────────────────────────                  │
│                          About                          ⚙️       │
│  Multi-axis LLM stance extraction + heterogeneous R-GAT...     │
│  🔗 zxsa0716.github.io/cina/                                   │
│  🏷️ climate-negotiations  cop30  cop31  unfccc  ...           │
│                                                                │
│  📜 Cite this repository                  ← CITATION.cff에서 자동 │
│                                                                │
│  📦 Releases                                                    │
│   ⭐ v3.0.0 — Methodology Advancement Release  Latest          │
│                                                                │
│  📦 Packages                                                    │
│   No packages published                                         │
│                                                                │
│  💻 Languages                                                   │
│   ████████████ Python  92%                                     │
│   ████ HTML  6%                                                │
│   ▏ JavaScript  2%                                             │
└───────────────────────────────────────────────────────────────┘
```

그리고 슬랙/카카오에 `github.com/zxsa0716/cina` 링크 붙이면:

```
┌─────────────────────────────────────────────────┐
│ 📷 [Social preview 이미지 — CINA 로고 + 메트릭 + 네트워크]  │
├─────────────────────────────────────────────────┤
│ zxsa0716/cina                                    │
│ Multi-axis LLM stance extraction + heterogeneous │
│ R-GAT + graph-grounded briefing for climate...  │
│ 🐍 Python  📅 Updated today                       │
└─────────────────────────────────────────────────┘
```

처럼 표시됩니다.

---

## 🤖 자동화된 (작업 불필요) 항목

위 3가지 외에는 모두 자동:

- ✅ **CITATION.cff** → repo 사이드바 "Cite this repository" 버튼 자동
- ✅ **Issue templates** → "New issue" 클릭 시 Bug / Academic 폼 자동
- ✅ **PR template** → PR 작성 시 체크박스 자동
- ✅ **CHANGELOG.md** → "Insights → Community Standards"에서 100% 표시
- ✅ **CODE_OF_CONDUCT, CONTRIBUTING, SECURITY** → 같이 100%
- ✅ **`.github/FUNDING.yml`** → "Sponsor" 버튼 (선택)
- ✅ **`.zenodo.json` + `codemeta.json`** → Zenodo 연동 시 자동 메타데이터
- ✅ **`Dockerfile` + `Makefile`** → 사용자가 `make help`로 즉시 확인

---

**작성**: 2026-05-05 · Heedo Choi (최희도)
**소요 시간**: 정확히 3분 (About 1분 + Social preview 30초 + Release 1분 30초)
