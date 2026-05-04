# 📋 교수님께 제출 가이드 (Track A — 글로벌기후리더십 2026-1)

> **저자**: Heedo Choi (최희도) · 기후기술융합학과 · zxsa0716@kookmin.ac.kr
> **수업**: 글로벌기후리더십 (2026-1학기)
> **과제**: 특정 국가/섹터 선정 → 주무부처 장관급 COP 협상 브리핑 작성
> **선정 국가**: 브라질 (COP30 의장국) + 한국 (관전국)
> **선정 섹터**: 적응 (Adaptation)
> **검증 사건**: COP30 Belém Adaptation Indicators (FCCC/PA/CMA/2025/L.25E)

---

## 🎯 제출 권장 구성 (3가지 옵션)

### 옵션 A — 미니멀 제출 (수업 요건 충족) ⭐ 추천

**1. 메인 산출물 (필수)**
- **`deliverables/ministerial_briefing_ko.md`** → PDF 변환 후 제출
  - 9 섹션 + 4 부록 (증거 추적성 / 데이터 lineage / 불확실성 / LLM provider attribution)
  - 길이: 약 8,500 단어
  - 외교부 기후환경과학외교국 보고 형식으로 작성됨

**2. 수업 과제 사전 분석 (필수)**
- `deliverables/country_selection.md` → 브라질 선정 근거
- `deliverables/sector_focus.md` → Adaptation 섹터 정당성
- `deliverables/agenda_matrix.md` → COP30 6-issue 매트릭스

→ **총 4개 markdown → PDF로 변환해 1개 압축 폴더로 제출**

---

### 옵션 B — 표준 제출 (논문감 학술 정성 어필)

옵션 A + 다음 정량 검증 보고서 추가:

- `deliverables/IRR_Korea.md` — 한국 적응정책 GGA 이행률 (IRR=0.653, 30 cells)
- `deliverables/IRR_Brazil.md` — Brazil Translation Gap Δ=0.304 정량
- `deliverables/AILAC_norm_entrepreneur_quantification.md` — Norm entrepreneur 검증 (NES=0.86)
- `deliverables/evaluation_report.md` — 4-task 정량 평가 (Spearman 0.658, P@3=R@3=1.00, α=0.905)
- `deliverables/korean_nap_gga_crosswalk.csv` — 30-cell 매핑 원본 데이터

**제출 시 첨부 메시지 예시**:
> 본 과제는 단일 브리핑이 아닌, 재현 가능한 LLM-GNN-LLM 파이프라인(CINA Framework)을 구축하여 COP30 적응 협상 결과(Belém Adaptation Indicators, 2025.11)에 회고적으로 검증한 학술 연구입니다. 수업 요건인 장관급 브리핑 외에, 정량 검증 보고서 5종과 인터랙티브 웹 데모를 함께 제출합니다.

---

### 옵션 C — 풀 패키지 (논문감 + 실재성 시연)

옵션 B + 다음 자료 추가:

- **`deliverables/paper.md`** — 학술 논문 draft (3,428 words, 23 references)
- **`docs/web/figures/` 7장 PNG** — Stage 2 시각화 (heatmap, network, hedging, centrality 등)
- **GitHub repository URL**: https://github.com/zxsa0716/cina (코드 + 데이터 + 산출물 일체)
- **인터랙티브 웹 데모 URL**: https://zxsa0716.github.io/cina/ (4 페이지 — 메인/methodology/visualizations/outputs)
- **15개 방법론 문서**: `docs/01_*.md` ~ `docs/15_*.md`

---

## 📑 PDF 변환 방법 (3가지)

### 방법 1 — VS Code (가장 쉬움, 추천)
1. VS Code 확장 "Markdown PDF" 설치 (yzane.markdown-pdf)
2. .md 파일 열기 → 우클릭 → "Markdown PDF: Export (pdf)"
3. 같은 폴더에 .pdf 생성됨

### 방법 2 — Pandoc (학술 품질 최고)
```bash
# Windows에서 Pandoc 설치 (https://pandoc.org/installing.html)
pandoc deliverables/ministerial_briefing_ko.md \
  -o ministerial_briefing_ko.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Malgun Gothic" \
  -V geometry:margin=2.5cm
```

### 방법 3 — GitHub 렌더링 → 브라우저 인쇄 (가장 빠름)
1. GitHub repo의 .md 파일 클릭 (예: https://github.com/zxsa0716/cina/blob/main/deliverables/ministerial_briefing_ko.md)
2. 브라우저에서 `Ctrl+P` (인쇄)
3. "PDF로 저장" 선택

### 방법 4 — Hancom Office / Word 사용
1. Typora, Obsidian, MarkText 등으로 .md 열기 → 복사
2. Hancom/Word에 붙여넣기 → 서식 정리 후 저장

---

## 📁 제출 폴더 구조 (권장)

로컬에 새 폴더를 만들어서 다음 구조로 정리:

```
HeedoChoi_GlobalClimateLeadership_2026Spring_Submission/
├── 00_제출개요.md                          ← (간략 README, 제출자/과제명/구성)
├── 01_장관급브리핑_KO.pdf                   ← ministerial_briefing_ko.md → PDF
├── 02_장관급브리핑_EN.pdf                   ← ministerial_briefing_en.md → PDF
├── 03_사전분석/
│   ├── 01_brazil_country_selection.pdf
│   ├── 02_adaptation_sector_focus.pdf
│   └── 03_cop30_agenda_matrix.pdf
├── 04_정량검증보고서/
│   ├── 01_IRR_Korea_0.653.pdf
│   ├── 02_IRR_Brazil_translation_gap_0.304.pdf
│   ├── 03_AILAC_norm_entrepreneur.pdf
│   ├── 04_L25_formula_evidence.pdf
│   ├── 05_realist_baseline_F1_0.560.pdf
│   └── 06_evaluation_report_4task.pdf
├── 05_시각화_figures/
│   ├── fig1_country_issue_heatmap.png
│   ├── fig2_procedural_authority.png
│   ├── fig3_frame_consistency.png
│   ├── fig4_centrality.png
│   ├── fig5_similarity_network.png
│   ├── fig6_hedging_density_2d.png
│   └── fig7_translation_gap_brazil.png
├── 06_방법론_논문/
│   ├── paper_draft.pdf                     ← deliverables/paper.md → PDF
│   └── 15_methodology_docs.pdf             ← docs/01-15 합본
├── 07_원시데이터샘플/
│   ├── stances_sample_10.jsonl
│   ├── graph_analysis.json
│   ├── irr_brazilian_translation_gap.json
│   └── README.md
└── 99_링크.md                               ← GitHub + Web demo URL
```

---

## 📝 제출 메시지 (이메일/LMS) 템플릿

```
안녕하세요 교수님,

기후기술융합학과 대학원생 최희도입니다. 글로벌기후리더십 (2026-1학기)
과제 제출드립니다.

【제출 개요】
- 선정 국가: 브라질 (COP30 의장국)
- 선정 섹터: 적응 (Adaptation)
- 검증 사건: COP30 Belém Adaptation Indicators (2025.11 합의,
  FCCC/PA/CMA/2025/L.25E)

【핵심 산출물】
1. 장관급 협상 브리핑 (한국 외교부 기후환경과학외교국 형식)
   — 9 섹션 + 4 부록 (증거 추적성/데이터 lineage/불확실성/LLM 출처)

2. CINA Framework — LLM → 그래프 분석 → LLM 3단계 파이프라인
   — UNFCCC 텍스트를 외교 전략 인텔리전스로 자동 변환
   — 회고적 검증: contested issue 3/3 정확 예측 (P@3=R@3=1.00)

【논문감 정량 검증 (선택)】
- Brazil Translation Gap Δ=0.304 (Putnam × Howlett 정량화)
- 한국 IRR=0.653, L&D-OP=0.39 약점 식별 → COP31 actionable 권고
- AILAC norm entrepreneur 4-criteria 3.5/4 PASS (NES=0.86)
- Phase 5 4-task 평가: Spearman ρ=0.658, Mean 4.53/5, Krippendorff α=0.905

【추가 자료 (선택)】
- 공개 GitHub repository: https://github.com/zxsa0716/cina
- 인터랙티브 웹 데모: https://zxsa0716.github.io/cina/
  (메인 + Methodology 인터랙티브 파이프라인 + D3 시각화 + 산출물 카탈로그)

감사합니다.
최희도 드림
zxsa0716@kookmin.ac.kr
```

---

## ⚡ 빠른 변환 명령 (한 번에 PDF 만들기)

VS Code Markdown PDF 확장 설치 후, 한 번에 변환:

```bash
# Windows PowerShell 또는 bash
cd "C:/Users/admin/Desktop/대학원수업/1학기/리더쉽"

# 핵심 4개 파일 PDF 변환 (VS Code에서 각 파일 열고 우클릭)
# 또는 Pandoc 일괄:
for f in deliverables/ministerial_briefing_ko.md \
         deliverables/country_selection.md \
         deliverables/sector_focus.md \
         deliverables/agenda_matrix.md; do
  pandoc "$f" -o "${f%.md}.pdf" --pdf-engine=xelatex \
    -V mainfont="Malgun Gothic" -V geometry:margin=2.5cm
done
```

---

## 🎓 교수님께 어필할 포인트 3가지

1. **수업 요건 100% 충족 + 논문감 확장**
   장관급 브리핑은 수업 과제 요건을 정확히 충족하면서, 그 뒤에 재현 가능한 학술 방법론(CINA)을 구축해 *Global Environmental Change* / NeurIPS Climate Change AI Workshop 2026 투고 후보로 발전시켰습니다.

2. **회고적 검증의 학술적 가치**
   2025년 11월 COP30 Belém Adaptation Indicators(L.25E) 합의 결과를 입력해, CINA가 contested issue 3/3을 정확 예측함을 정량 검증했습니다. 이는 단순 AI 활용을 넘어선 **AI 방법론 평가 연구**입니다.

3. **5개 학술 이론 정량화**
   Keohane-Victor (Regime Complex), Putnam (Two-Level Games), Howlett (instrument calibration), Tallberg (procedural authority), Finnemore-Sikkink (norm entrepreneur)를 각각 정량 검증 — IR/정책학 이론 quantification으로 readable.

---

## ❓ 자주 묻는 질문

**Q. 한 파일만 내야 한다면?**
→ `deliverables/ministerial_briefing_ko.md` (PDF 변환 후 제출). 이것만으로 수업 요건은 충족됩니다.

**Q. 영문도 같이 내야 하나요?**
→ 수업이 한국어 진행이면 KO만, 국제 회람이면 EN도 추가. 일반적으로 KO 메인 + EN 보조.

**Q. CSV / JSON 같은 raw 데이터도 같이 내나요?**
→ 옵션. 학술 정성 어필용으로 `data/sample/` 의 7개 JSON 첨부 가능. PDF 본문에서 GitHub 링크로 대체해도 무방.

**Q. 페이지 분량 제한이 있다면?**
→ 브리핑 본문(9 섹션) + 부록 1개(증거 추적성)만 추출하여 약 5,000 단어로 줄일 수 있습니다.

**Q. 발표(PT) 자료도 필요?**
→ 본 가이드는 텍스트 보고서 기준입니다. 발표용 슬라이드 필요 시 별도 요청 가능 (PPTX 자동 생성 skill 보유).

---

**최종 점검 체크리스트** ✅

- [ ] `ministerial_briefing_ko.md` PDF 변환 완료
- [ ] 사전 분석 3개 파일 PDF 변환
- [ ] 정량 검증 보고서 선택 + 변환 (옵션 B 이상)
- [ ] 제출 메시지(이메일/LMS) 작성
- [ ] GitHub URL + Web demo URL 포함
- [ ] 폴더 구조 정리 후 ZIP 압축
- [ ] 제출 마감일 (2026.05) 확인

**작성**: 2026-05-04
**저자**: Heedo Choi (최희도), 기후기술융합학과, Kookmin University
