---
assigned_to: policy-data-collector
agent_model: sonnet
round: 5
priority: P0
depends_on:
  - council_sessions/round_4/ir_political/critique.md
  - council_sessions/round_4/policy_science/critique.md
  - council_sessions/round_4/synthesis/cross_review.md
deadline: Round 5 Phase A (T02 시작 전)
---

## 목적

Round 4 두 교수 critique CR4.4·CR4.6 + Policy C2 직접 대응. (a) Castro 2025 ENB cooperation matrix 실제 raw data 다운로드로 Stage 2 baseline ground-truth 확보, (b) UNFCCC SBI/SBSTA contact group informal notes 수집으로 Tallberg pre-cooking evidence 확보 (L.25 pre-crystallized formula 가설 검증), (c) KEI WP 시리즈 5건으로 IRR_Korea 가중치 외부 정합성 reference 확인.

---

## 구체 산출물 (P0)

### P0-1. Castro 2025 ENB cooperation matrix 실제 다운로드 (CR4.4)

- [ ] Nature Sci Data 논문(`https://www.nature.com/articles/s41597-025-06262-4`) supplementary materials 섹션 정독
- [ ] figshare 또는 zenodo 링크 추적 (DOI 명시 추적)
- [ ] cooperation_matrix.csv (또는 .json/.parquet) 실제 다운로드 → `data/raw/round5/castro_2025_matrix/`
- [ ] manifest 등록 (sha256 + license 명시)
- [ ] schema 첫 5행 sample → `data/raw/round5/castro_2025_matrix/SAMPLE.md`
- 실패 시: corresponding author email 확인 + Heedo 학교 메일 발송 권고 (manifest에 placeholder)

### P0-2. UNFCCC SBI/SBSTA contact group informal notes ≥4건 (CR4.6)

- [ ] UNFCCC documents portal에서 다음 검색:
  - `https://unfccc.int/documents` → "informal note" + "contact group" + "GGA" + "2025"
  - 대상 세션: SB62 (June 2025) + SB63 (Nov 2025 in Belém)
- [ ] L.25 사전협상 추적용 ≥4건 informal notes 다운로드 (Co-Facilitator notes 우선)
- [ ] 추가 후보: SBI co-facilitators' summary, GGA contact group facilitators' note, JT-WP technical paper draft
- [ ] manifest 등록 (chair_role=facilitator 라벨 첨부)
- [ ] 각 PDF에 대해 1-line "Tallberg pre-cooking signal" 메모 (`data/raw/round5/sbi_sbsta_notes/EVIDENCE_NOTES.md`)

### P0-3. KEI WP 시리즈 5건 (Policy C2)

- [ ] 한국환경연구원(KEI) 웹사이트 (`https://www.kei.re.kr/`) Working Paper 시리즈 검색
- [ ] 키워드: "국가적응대책", "GGA", "적응 지표", "기후변화 적응", "Authority Treasure" (Hood 1983 instrument 한국어 번역)
- [ ] 명수정 박사 저작 우선 검색 (한국 NAP IRR 권위자)
- [ ] 5건 PDF 다운로드 → `data/raw/round5/kei_wp_series/`
- [ ] 각 PDF에 대해 가중치 reference 발췌 (Authority/Treasure/Nodality/Organization 비율 추출)
- [ ] `data/raw/round5/kei_wp_series/WEIGHTING_REFERENCE.md` 작성 (5건 weight schema 비교 표)

---

## 품질 기준

- [ ] manifest 156 → ≥165 (+9 minimum: 1 + 4 + 4 KEI partial)
- [ ] sha256 100% 추적
- [ ] license 100% 명시 (Castro figshare CC license, UNFCCC CC-BY-NC, KEI 학술목적 활용)
- [ ] Castro 매트릭스 schema 검증 (행렬 차원, 결측 비율, 키 컬럼명) — 실패 시 즉시 보고
- [ ] SBI/SBSTA 노트 4건 모두 chair_role 라벨 정확
- [ ] KEI WP 5건의 가중치 reference 표가 비교 가능한 정형 (Markdown table)

---

## 제공된 컨텍스트

### Round 4 Policy critique (C2 인용)
> "IRR_Korea 가중치 (Authority 0.35 / Treasure 0.25 / Nodality 0.20 / Organization 0.20)가 외부 정합성 검증 없음. KEI 명수정 박사 (한국 NAP IRR 권위자) email 협의 권고. 단 R6 외부 협의 전 internal validity 우선 확보."

### Round 4 IR critique (§4.1 권고 #3 + #4 인용)
> "Castro 2025 ENB cooperation matrix를 실제 데이터로 확보해야 R-GAT cross-validation 가능. supplementary materials 추적 필수.
> contact group informal notes (Tallberg pre-cooking evidence)는 L.25 pre-crystallized formula 가설의 결정적 검증."

### Round 4 cross-review §3 (CR4 list)
- CR4.4 Castro 2025 매트릭스 → T01 P0
- CR4.6 contact group notes ≥4건 → T01 P0

### 기존 manifest 156 entries (chair letters 24 신규 포함)
- COP21~30 분포: 8 sessions × ~2건 = chair_metadata seed 강화
- Round 5 P0-1 처리 후 chair_metadata 32 → 60+ 확장 가능 (T02 R5 P0-1로 이전)

---

## 비non-blocking 사항

- 다음 항목은 Round 5에서 수집 못해도 P1 (Round 6 가능):
  - APEC/G20 climate side-event statement (Hochstetler "BASIC chair-host paradox" 보강)
  - COICA/APIB/CAN/WGC 추가 NSA 4 entity (현 4 → 8)

---

## 출력 위치

- `data/raw/round5/castro_2025_matrix/`
- `data/raw/round5/sbi_sbsta_notes/`
- `data/raw/round5/kei_wp_series/`
- `council_sessions/round_5/data_collection/manifest.jsonl` (cumulative)
- `council_sessions/round_5/data_collection/REPORT.md` (Round 5 collection 요약)
