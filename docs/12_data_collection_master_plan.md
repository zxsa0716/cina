# 12. Data Collection Master Plan — 수집 마스터 플랜

> 누가, 무엇을, 언제, 어디서, 어떻게, 왜 수집하는지를 한 문서에 명시.
> `policy-data-collector` agent가 매 라운드 시작 시 이 문서를 reference로 task를 수행.

---

## 1. 5W1H 요약

| 항목 | 답 |
|------|---|
| **What** | UNFCCC submissions, NDCs, ENB summaries, IPCC AR6, Castro 2025 dataset, COP30 결정문 |
| **Why** | CINA Stage 1 학습/추론 + Stage 2 prior + Stage 3 evidence + 4-task 평가 ground truth |
| **Who** | `policy-data-collector` agent (sonnet) — task는 team-lead가 발급 |
| **Where** | docs/11_source_catalog.md 의 11개 소스 |
| **When** | Round 1: 우선 코어 → Round 2-3: gap 보강 |
| **How** | `src/collect/*.py` Python collector + `src/collect/orchestrate.py` 통합 |

---

## 2. 우선순위 (Priority Tiers)

### Tier P0 — Round 1 필수 (수업 제출에도 필요)
1. **브라질 COP30 적응 관련 submission** (focal country)
2. **COP30 Belém Package 결정문** (실제 결과)
3. **ENB COP30 종합 요약** (협상 일지)
4. **Castro 2025 dataset** (calibration ground truth)
5. **20개국 NDC 적응 섹션** (스탠스 추출 input)

### Tier P1 — Round 2 보강
6. **UNFCCC SBI/SBSTA 적응 의제 submission** (COP30 이전 6개월)
7. **20개국 COP29 입장문** (시계열 비교용)
8. **IPCC AR6 WGII Ch.16, 17, 18** (이론 접지)

### Tier P2 — Round 3 정밀화
9. **AOSIS, LDC, AILAC group 공동 입장문**
10. **Climate Action Tracker country profiles**
11. **ND-GAIN vulnerability 데이터** (그래프 노드 피처)

---

## 3. 수집 시퀀스 (Round 1 상세)

### Step 1.1 — Castro 2025 dataset (10분)
```bash
python -m src.collect.castro_2025
```
- Nature Sci Data 페이지에서 supplement CSV 다운로드
- `data/raw/castro_2025/enb_interactions.csv` 저장
- SHA256 기록

### Step 1.2 — COP30 공식 결정문 (15분)
```bash
python -m src.collect.cop30_official --documents belem-package,gga-decisions
```
- Belém Package 전체 텍스트
- GGA 지표 결정문
- 의장단 letter

### Step 1.3 — ENB COP30 요약 (20분)
```bash
python -m src.collect.iisd_enb --event cop30 --type summary,daily
```
- COP30 일일 발행 (12-15건)
- COP30 종합 summary
- 협상 그룹 위치 분석

### Step 1.4 — UNFCCC 브라질 + 핵심 5개국 submission (30분)
```bash
python -m src.collect.unfccc_submissions \
    --topic adaptation \
    --conference cop30,sbi62,sbsta62 \
    --countries Brazil,EU,US,China,India,AOSIS \
    --type submissions,decisions
```
- 약 30-50개 PDF
- 각 PDF에 메타데이터 첨부

### Step 1.5 — 20국 NDC 적응 섹션 (40분)
```bash
python -m src.collect.ndc_registry \
    --countries Brazil,EU27,US,China,India,Norway,Switzerland,Canada,Australia,Japan,SouthKorea,Saudi,UAE,Egypt,SouthAfrica,Mexico,Colombia,Chile,CostaRica,Kenya
```
- 최신 NDC PDF 다운로드
- 적응 섹션 PDF 페이지 식별 (목차 분석)

### Step 1.6 — 정제 단계 핸드오프
- 모든 raw 파일 `data/raw/` 트리에 정착
- `data/manifest/round_1.jsonl` 생성
- `data-refinement-analyst`로 핸드오프

**Round 1 예상 총 소요**: 약 2시간 (네트워크), 약 200-300 문서.

---

## 4. 메타데이터 표준

모든 수집 파일에 `*.meta.json` 동봉:

```json
{
  "doc_id": "UNFCCC-FCCC-CP-2025-L19",
  "source_system": "unfccc.int",
  "source_url": "https://unfccc.int/sites/default/files/resource/cp2025_L19_E.pdf",
  "retrieved_at": "2026-04-25T15:30:00Z",
  "retrieved_by": "policy-data-collector/round_1",
  "license": "UN Open License",
  "license_attribution": "© UNFCCC",
  "sha256": "...",
  "filesize_bytes": 245612,
  "language": "en",
  "page_count": 12,
  "topic_tags_initial": ["adaptation", "GGA"],
  "country_authors_initial": ["Brazil"],
  "session": "COP30",
  "document_type": "decision",
  "symbol": "FCCC/CP/2025/L.19",
  "raw_file_path": "data/raw/unfccc_submissions/cop30/FCCC_CP_2025_L19.pdf",
  "extraction_status": "pending",
  "verification_status": "pending"
}
```

---

## 5. 품질 게이트 (수집 단계)

| 게이트 | 기준 | 통과 못하면 |
|--------|------|-----------|
| **Q1 Coverage** | 20국 × 6이슈 ≥ 80% 문서 확보 | 추가 수집 task |
| **Q2 Integrity** | sha256 검증 100% | 재다운로드 |
| **Q3 Metadata** | 모든 파일 .meta.json 존재 | metadata 보강 |
| **Q4 License** | 라이선스 정보 100% 명시 | 재수집 (소스 재확인) |
| **Q5 Deduplication** | 중복률 < 5% | dedupe 수행 |

---

## 6. 수집 데이터의 이동 경로

```
[외부 소스]
    │ collector
    ▼
council_sessions/data_collection/raw/    ← 임시 (라운드별)
    │ orchestrate.py 검증
    ▼
data/raw/{source_type}/{conference}/     ← 영구 저장
    │ data-refinement-analyst
    ▼
data/processed/documents.jsonl           ← Stage 1 입력
    │ Stage 1 LLM
    ▼
data/processed/stances.jsonl             ← Stage 2 입력
    │ Stage 2 GNN
    ▼
data/processed/graph_analysis.json       ← Stage 3 입력
    │ Stage 3 LLM
    ▼
deliverables/ministerial_briefing.md     ← 최종
```

---

## 7. 라운드별 수집 목표

### Round 1 (현재) — Foundation
- Tier P0 (1.1 ~ 1.5)
- 산출물: `data/raw/`에 약 250 문서, manifest

### Round 2 — Gap-filling
- 두 교수의 critique에서 식별된 gap
- 누락 국가/이슈/시점 보강
- COP25-29 시계열 확장

### Round 3 — Calibration
- Calibration set 50개 expert coding
- 추가 ENB 데이터로 Castro와 cross-validation

### Round 4-N — Refinement
- 라운드별 발견된 specific gap만 수집

---

## 8. 비용·자원 추정

### Round 1
- 네트워크: ~2 GB 다운로드, ~2시간
- 저장: ~3 GB (raw + 메타)
- LLM (수집 자체에는 거의 안 씀): ~$0.50 (토픽 분류 보조)

### 전체 프로젝트
- 모든 라운드 합계: ~5-10 GB
- 저장 위치: 로컬 + Zenodo (논문 acceptance 후)

---

## 9. 실패 시나리오 대응

| 시나리오 | 대응 |
|---------|-----|
| UNFCCC 사이트 장애 | 24시간 후 재시도, NegotiateCOP API 우회 |
| ENB 403 차단 | User-Agent 변경, IISD 직접 contact (학술 사용) |
| NDC PDF 인덱스 변경 | HTML 파싱 로직 업데이트, fallback to 검색 |
| Castro 데이터 접근 불가 | 저자 직접 contact (논문 contact email) |
| Rate limit 초과 | exponential backoff, 다음 라운드로 분할 |

---

## 10. 다음 문서
- [docs/13_reference_tables.md](13_reference_tables.md) — 국가/그룹/이슈 식별자 표
- `src/collect/*.py` — 실제 collector 코드
