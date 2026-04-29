# Castro et al. 2025 ENB Cooperation Matrix Data Access Request

> **Action required**: Heedo가 학교 이메일 (zxsa0716@kookmin.ac.kr)로 직접 발송.
> **Why**: Stage 2 R-GAT의 cooperation ground-truth (현재 pseudo-truth로 F1=0.560 측정 중). 실제 Castro matrix 입수 시 F1 재산출로 *IO* / NeurIPS CCAI reviewer 만족 가능.

---

## 발송 대상 (multiple)

**Primary**:
- Paula Castro (corresponding author): paula.castro@zhaw.ch
- Victor Kristof (data lead): victor.kristof@epfl.ch (또는 GitHub: @vkristof)

**Secondary** (data repository):
- SWISSUbase contact: contact@swissubase.ch
- DOI: 10.48573/8VQM-7Z98

---

## 영문 이메일 템플릿

```
Subject: Academic data access request — CINA project (Kookmin University, Korea)

Dear Dr. Castro,

I am writing to request academic access to the ENB negotiation interactions
dataset published in your 2025 Nature Scientific Data paper:

  Castro, P., Kristof, V., Kammerer, M., & Cogne, T. (2025).
  "Participation, Cooperation and Conflict in UN Climate Negotiations."
  Scientific Data, 12, 06262.
  DOI: 10.1038/s41597-025-06262-4
  Data DOI: 10.48573/8VQM-7Z98

I am a researcher at the Department of Climate Technology Convergence,
Kookmin University, Republic of Korea, working on a project called CINA
(Climate Issue-Network Analysis). CINA is a three-stage LLM → GNN → LLM
pipeline that retrospectively validates AI-driven negotiation analysis
against COP30 (Belém, November 2025) Adaptation Indicator outcomes.

Your interactions.csv file is critical for our Stage 2 ground-truth
validation. Specifically, we need to:
  1. Replace the current pseudo-truth (group membership similarity) with
     your actual ENB-coded cooperation/conflict pair frequencies
  2. Re-compute realist baseline F1 on actual coalition predictions
  3. Validate our chair_metadata pre-crystallized formula hypothesis
     against your 1995-2023 procedural authority signals

We will:
  - Acknowledge your work fully (DOI citation in all derivative outputs)
  - Comply with the CC BY-NC-SA 4.0 license (academic, non-commercial)
  - Share back our derivative analysis if useful to your future work

Could you advise on the most efficient way to obtain access to
interactions.csv (or the equivalent cooperation matrix file from the 8-file
SWISSUbase bundle)? We have already attempted automated download via the
SWISSUbase landing page but received a "contact us" prompt rather than a
direct download.

I am happy to provide:
  - Institutional verification (Kookmin University, Korea)
  - Project description (CINA whitepaper, ~5 pages)
  - Brief data use plan and timeline

Thank you for sharing this remarkable dataset with the climate diplomacy
research community. Your work has already informed our methodological
design, and direct access would significantly strengthen our retrospective
validation of the COP30 Belém Adaptation Indicators outcome.

Best regards,

Heedo [Last Name]
Researcher, Department of Climate Technology Convergence
Kookmin University
Seoul, Republic of Korea
zxsa0716@kookmin.ac.kr

CC: paula.castro@zhaw.ch, victor.kristof@epfl.ch
```

---

## 한국어 발송 노트 (Heedo용)

- **타이밍**: COP30 종료 (2025.11) + Stage 2 가동 시점 (2026.05) 사이가 적정
- **승인율 추정**: 70-80% (Nature Sci Data 데이터는 학술 사용 표준 승인)
- **리스크**: 1-2주 응답 대기. fallback으로 GitHub `victorkristof/enb-mining` 코드 저장소 활용 (raw ENB 텍스트 자체 코딩 가능)
- **CINA 프로젝트 설명서 (1 page)**: 별도 첨부 가능 — `docs/CINA_overview_for_data_request.md` 작성 권고

---

## fallback 시나리오

응답 1주 미달 시:
1. GitHub `victorkristof/enb-mining` 코드 저장소 clone
2. ENB 1995-2023 raw bulletins (이미 IISD 공개) 직접 코딩 재현
3. 또는 Kammerer (Kammerer & Hickmann 2024) HLS dataset로 cross-validation

응답 안내 시:
1. SWISSUbase 계정 생성
2. 8 file bundle (interventions.csv, interactions.csv, issues, parties, groupings, interventions+issues, interactions+issues, codebook) 다운로드
3. `data/raw/round5/castro_2025_matrix/` 에 저장
4. `src/collect/manifest.py:append_record` 로 manifest 등록 (license CC BY-NC-SA 4.0)

---

**작성**: 2026-04-28 (Round 5 T01 collector_feedback 보강)
**상태**: Heedo 발송 대기
