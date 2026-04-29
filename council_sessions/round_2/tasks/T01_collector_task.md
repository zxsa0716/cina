---
assigned_to: policy-data-collector
model: sonnet
round: 2
priority: P0
issued_at: 2026-04-25
deadline: round_2_close
depends_on:
  - council_sessions/round_1/data_collection/REPORT.md
  - council_sessions/round_1/refinement/collector_feedback.md
  - council_sessions/round_1/synthesis/cross_review.md
  - council_sessions/round_1/synthesis/quality_gates.json
related_critiques:
  - council_sessions/round_1/policy_science/critique.md (C1, C2; §3.2 한국 부처 자료)
  - council_sessions/round_1/ir_political/critique.md (C1 procedural power; §3.1 chair power)
---

# T01 (Round 2) — Dynamic-Source Collection with Playwright

## 1. 목적
Round 1의 결정적 차단점(G1=0.18; UNFCCC/NDC/ENB 0건)을 해소한다. 헤드리스 브라우저(Playwright) 도입으로 동적 JS 사이트를 수집하고, 두 교수 권고 반영을 위한 신규 자료(의장 letter, L-document, 한국 부처 자료, NDC 적응 섹션)를 추가 확보한다. **목표: manifest 70-100 신규 entries**.

## 2. 컨텍스트 (Round 1 산출물에서)

- **두 교수 합의**: UNFCCC/NDC/ENB 0건은 Stage 1 LLM 추출을 가동할 수 없는 결정적 결함 (cross_review §2 A1).
- **IR 교수 P0 비판**: CINA가 Belém Rube Goldberg 사건의 인과 메커니즘(chairmanship procedural power)을 변수로 갖지 못함. 이를 해소하려면 의장 letter, SBI/SBSTA L-document(의장 텍스트 초안) 수집 필수 (cross_review §4 CR2).
- **정책학 교수 권고**: 한국 외교부 「녹색·기후외교 추진전략(2024.9)」, 환경부 「제3차 국가기후위기적응강화대책(2023~2025)」, KEI/KIEP 보고서 (cross_review §6.1 P0 항목 4).

## 3. P0 산출물 (반드시)

### 3.1 인프라
- [ ] `requirements.txt` 또는 `pyproject.toml`에 `playwright>=1.45` 추가
- [ ] `python -m playwright install chromium` 1회 실행 (Heedo 환경에)
- [ ] `src/collect/dynamic_browser.py` — Playwright 래퍼 (page.goto + wait_for_selector + content() 또는 PDF download)
- [ ] 기존 `unfccc_submissions.py`, `ndc_registry.py`, `iisd_enb.py` 3개 collector를 dynamic_browser 사용으로 재구현

### 3.2 데이터 수집 매트릭스 (Round 1 cross_review §4 CR5 기준)

| 우선순위 | 카테고리 | 목표 건수 | 상세 |
|---------|---------|---------|------|
| Critical | UNFCCC submission (COP30) | 25-30 | BRA, EU, AOSIS, LDC, LMDC, African Group, AILAC, IND, CHN, USA(부재 확인), Umbrella, EIG, Arab Group — GGA-IND/ADAPT-FIN/L&D-OP/NAPs 이슈 |
| Critical | UNFCCC submission (COP29 SBI61/SBSTA61) | 10-15 | GGA 지표 협상 전사 |
| Critical | **의장 letter** (신규) | 4-6 | COP29 Baku presidency letter (Yalçın Rafiyev), COP30 Belém presidency letter (André Corrêa do Lago), Baku to Belém Roadmap |
| Critical | **SBI/SBSTA L-document** (신규) | 8-12 | 의장 텍스트 초안 시리즈 — pen_holder 식별용. Adaptation 관련 L.1 ~ L.N |
| High | IISD ENB COP30 일일 요약 | 12-15 | enb12880e ~ enb12895e brute force 시도, fail 시 학술 contact |
| High | **한국 부처 자료** (신규) | 5-10 | 외교부 「녹색·기후외교 추진전략(2024.9)」, 환경부 NAP 3차, KEI 2023-12, KEI 2024 NAP 중간모니터링, KIEP 24-32 |
| High | **NDC 적응 섹션** (신규) | 5 | BRA, EU, CHN, IND, AOSIS 대표국(Maldives 또는 Marshall Islands) |
| Medium | LMDC/SAU 직접 발언 | 5-10 | SAU, IRN, DZA의 COP30 GGA 발언 또는 제출문 |
| Medium | Castro 2025 supplements | best-effort | Nature DOI 페이지 재분석, figshare/zenodo 검색 |

**총 목표: 70-100건** (= G1 0.80+ 도달).

### 3.3 무결성·메타 표준 (유지)
- [ ] 모든 항목 sha256 검증
- [ ] 모든 항목 `.meta.json` 동봉 (license, download_url, retrieved_at, source_id)
- [ ] manifest.append_record 자동 dedup
- [ ] 라이선스 100% 추적 (UNFCCC: UN open / NDC: government / ENB: CC BY-NC-SA / Korean ministries: public)
- [ ] ENB 사용 시 license="CC BY-NC-SA" 명시

## 4. P1 산출물 (가능한 만큼)
- [ ] AOSIS, LDC, AILAC 그룹 statement 추가 검색
- [ ] Brazilian gov.br/mma, gov.br/mre 공식 statement (포어→영어 번역 메타)
- [ ] 미국 USA 공식 발화 부재 확인 (negative confirmation을 manifest에 별도 기록)

## 5. 제한·주의

### 5.1 ENB 학술 contact
- **HEEDO-3 결정 대기**: IISD에 사전 통지 필요한지 Heedo 결정 후 진행. 결정 전에는 brute force 시도하되 단일 IP rate-limit (1 req / 3 sec) 엄수.
- 모든 ENB 항목은 license="CC BY-NC-SA" + non-commercial-academic-use 명시.

### 5.2 Playwright robots
- `--no-robots` 옵션 유지 (Round 1과 동일). 단 user-agent에 `CINA-Research (zxsa0716@kookmin.ac.kr)` 명시.
- rate-limit: 1 req / 2 sec, max-concurrent 2.

### 5.3 데이터 부담 견적
- 70-100 docs × 평균 2MB = 140-200MB 추가 raw storage.
- LLM 호출 0회 (수집 단계).
- 시간: 추정 4-6시간 (Playwright 페이지 로딩 + 다운로드).

## 6. 산출물 위치
- 신규 raw 파일: `data/raw/{source}/...`
- manifest 추가: `data/manifest/manifest.jsonl`
- run summary: `data/runs/collect_20260425T*Z/summary.json`
- **REPORT**: `council_sessions/round_2/data_collection/REPORT.md` (구조: Round 1 REPORT.md 형식 따라)
- **두 교수 권고 반영 확인**: REPORT §"교수 권고 반영" 절에서 chair letter / L-doc / 한국 자료 수집 결과 명시

## 7. 품질 게이트 자체 점검
완료 시 REPORT.md §끝에 다음 표 작성:

| 게이트 | 결과 | 측정값 |
|--------|------|--------|
| Q1 Coverage (G1) | pass(≥0.80)/partial/fail | (수집/목표 비율) |
| Q2 Integrity | sha256 100%? | |
| Q3 Metadata | .meta.json 100%? | |
| Q4 License | 100% 추적? | |
| Q5 Deduplication | dedup 적용? | |
| **Q6 Chair-power 자료** (신규) | letter+L-doc 수집? | |
| **Q7 한국 부처 자료** (신규) | 5건 이상? | |

## 8. team-lead 에스컬레이션 트리거
- Playwright 도입 시 Heedo 환경에 chromium binary 200MB 다운로드 필요 → Heedo 승인(HEEDO-2) 확인.
- ENB 수집 시 IISD contact (HEEDO-3) 확인.
- 70건 미달 시 즉시 escalate (수집 매트릭스 재조정 필요).

## 9. 재현성 명령 이력 기록
모든 collector 실행 명령을 REPORT §Appendix A에 기록 (Round 1 형식 따라):
```bash
python -m src.collect.orchestrate --sources unfccc --topic adaptation --max 30 --countries "..." --no-robots --use-playwright
python -m src.collect.orchestrate --sources ndc --countries "Brazil,EU,China,India,Maldives" --no-robots --use-playwright
python -m src.collect.orchestrate --sources enb --event cop30 --max 15 --no-robots --use-playwright
python -m src.collect.orchestrate --sources korean-ministries --max 10 --no-robots
...
```

## 10. 본 task의 헌법 정합성 (자체 확인)
- ✓ 헌법 §1 논문감: G1 0.80+ 달성으로 empirical validity 회복
- ✓ 헌법 §2 COP30 회고: Belém + Baku letter, L-doc로 회고 인과변수 확보
- ✓ 헌법 §3 투트랙: 한국 부처 자료가 Track A 직접 기여
- ✓ 헌법 §4 LLM-GNN-LLM: Stage 1 입력 corpus 임계 도달

**작업 시작.**
