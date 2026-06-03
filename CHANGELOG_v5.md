# CINA v5 / Program v2 — CHANGELOG

> **Release**: 2026-05-08
> **작성**: Heedo Choi (최희도) · zxsa0716@kookmin.ac.kr

이번 릴리스는 **데이터 / 백엔드 / 프론트엔드 / LLM 모드** 4영역을 동시에 학술 등급으로 끌어올린 메이저 업그레이드입니다. v4.1 → v5+v2.

---

## TL;DR

| 영역 | v4.1 (이전) | v5 / v2 (현재) | 증가 |
|------|-----------|----------------|------|
| 데이터 records | 900 | **2,400** | +166% |
| 국가 | 30 | **50** | +20 |
| 이슈 | 6 | **8** (TRANS-FIN, TECH-TRANS 추가) | +2 |
| COP | 5 (26-30) | **6** (25-30) | +1 |
| Schema 필드/record | 13 | **22** | +9 |
| Query intents | 4 (lookup, compare, recommendation, factoid) | **7** (+ trend, coalition, gap) | +3 |
| 시각화 | 정적 5개 | 정적 + **inline SVG mini chart** (sparkline, NATO 4축, CI bar, gap bar) | dynamic |
| LLM 모드 | 단일 턴 | **multi-turn** (최근 5턴 컨텍스트) | + 메모리 |
| Export | 없음 | **Markdown · JSON · BibTeX** 3종 | + 3 |
| 인용 | 1건 / answer | **최대 12건** + expandable panel | +11 |
| 방법론 footer | 없음 | engine v · dataset v · intent · retrieved n · hash | 재현성 |

---

## 1. 데이터 v4 → v5 (`data/processed/stances_v5.jsonl`)

### Coverage 확장

- **50개국** = v3 13 + v4 17 + **v5 신규 20**
  - 신규 20국: Switzerland, Spain, Italy, New Zealand, Argentina, Colombia, Chile, Peru, Costa Rica, Vietnam, Thailand, Philippines, Pakistan, Iran, UAE, Qatar, Kenya, Ghana, Senegal, Morocco
- **8개 이슈** = v4 6개 + **v5 신규 2개**
  - 신규: `TRANS-FIN` (재원 투명성), `TECH-TRANS` (기술이전)
- **6개 COP** = COP25 (Madrid 2019) 추가 → COP30 (Belém 2025)

### Schema 강화 (record당 22개 필드, 이전 13개)

신규 필드:

| 필드 | 의미 |
|------|------|
| `ci_lower_95`, `ci_upper_95` | Bayesian 95% credible interval |
| `nato_4axis.{nodality,authority,treasure,organization}` | NATO 4축 개별 점수 (Hood 1983; Howlett 2019) |
| `nato_axis_sum` | 4축 합 (NATO 강도) |
| `frame_distribution` | 5-class frame 확률 분포 (단일 라벨 X) |
| `procedural_composite` | chair + pen + drafts 종합 권한 점수 (0-1) |
| `coalition_membership.{primary, all}` | 공식 협상 그룹 |
| `translation_gap_delta` | 국내↔국제 stance 격차 (Δ) |
| `domestic_stance_proxy` | 국내 정책 stance 추정치 |
| `evidence_location` | 인용 출처 (verified / placeholder) |
| `_meta.prompt_version`, `dataset_version` | 재현성 메타데이터 |

### 재현성

- 결정론적 seed=42
- Schema hash: `7c3434c77d0865ad` (record 0의 key 배열 SHA-256)
- 메타데이터 파일: `data/processed/stances_v5_meta.json`

### 한계 명시

v5 dataset의 v3 13국 + v4 17국 패턴은 **v3 verified records의 stance pattern을 보존**하고, 신규 20국은 **ND-GAIN, GDP, 협상 블록 휴리스틱**으로 산출됨. v3 78개 record는 실제 LLM 추출 + 외부 코더 검증을 거쳤으나, 그 외는 **분석/시각화/탐색용 합성 corpus**임을 명시. 실제 LLM 추출로 대체는 `python -m src.pipeline --country ... --cop ...`으로 가능.

---

## 2. Query Engine v2 (`src/program/query_engine_v2.py`)

### 7개 intent

| intent | trigger 키워드 | 출력 |
|--------|--------------|------|
| `lookup` | "입장", "스탠스", "position" | 단일 또는 다중 record 카드 |
| `compare` | "비교", "vs", "차이" | 교차 비교 표 + 최대 격차 |
| `trend` | "추이", "시계열", "trajectory" | COP25-30 sparkline |
| `coalition` | "비슷한", "유사한", "동맹" | Pearson 상관 top-10 |
| `gap` | "translation gap", "국내국제", "Δ" | 이슈별 / 글로벌 |
| `recommendation` | "권고", "전략", "방안" | 약점/강점 + 정책 권고 |
| `factoid` | "정확히 몇", "exact" | 단일 스칼라 |

### Top-k retrieval

- relevance score = country 매치 (+1.5) + issue 매치 (+1.5) + COP 매치 (+1.0) + 0.3 × confidence + 0.2 × salience + 0.5 × verified bonus
- intent별 k: trend=120, coalition=400, gap=80, 그 외=24

### Pearson similarity for coalition

이전 cosine 방식은 모든 국가가 양의 stance를 가져 r≈1로 수렴 → mean-centered Pearson으로 변경. Korea와 가장 가까운 국가: Mexico (r=+0.97), Canada (+0.91), Australia (+0.89) — EIG 회원국 + Umbrella 일관성 확인.

### 방법론 footer (재현성)

모든 응답 끝에 첨부:
```
engine v2.0.0 · dataset v5.0.0 · intent compare · retrieved n=2 · source rule-based · hash 868c80f1303787de
```

`hash`는 (intent_type, countries, issues, cop, seed) SHA-256 prefix로, 동일 질문은 항상 동일 hash.

### CLI

```bash
python -m src.program.query_engine_v2 --demo
python -m src.program.query_engine_v2 "AOSIS GGA-IND 시계열 추이?"
```

---

## 3. Web UI v2 (`docs/web/cina_program_v2.html` + `assets/cina_program_v2.js`)

### inline SVG 시각화 (외부 라이브러리 없음)

- **`svgCIBar`**: stance + 95% CI 시각화 (양/음 색구분, mid-line)
- **`svgNatoBar`**: NATO 4축 컬러 막대 (N=cyan, A=violet, T=amber, O=emerald)
- **`svgSparkline`**: COP25-30 stance trajectory
- **`svgHBars`**: 양음 분리 horizontal bar (gap ranking, coalition similarity)

### Multi-turn LLM memory

최근 5턴이 LLM prompt에 `## 최근 대화 (참고용)` section으로 자동 포함됨. localStorage `cina_v2_history`에 50턴 유지.

### Export

3종 export 버튼:
- `.md` — Markdown 대화 로그
- `.json` — 전체 history (intent, citations, timestamp 포함)
- `.bib` — BibTeX (CINA + arXiv 인용)

### 인용 panel

응답마다 `📎 근거 N건 (펼치기)` expandable. 각 인용에는:
- 국가/이슈/COP
- stance + CI
- frame
- verified ✅ 마커
- evidence quote (italic)

### 방법론 footer (HTML)

모든 답변 끝에 회색 dashed 박스:
```
📐 methodology · engine v2.0.0 · dataset v5.0.0 · intent compare · retrieved n=24 · source LLM (gemini) · hash 868c80f1303787de
```

---

## 4. LLM Mode v2

### IR 이론 grounding이 강제된 시스템 프롬프트

```
당신은 CINA (Climate Issue-Network Analysis) Q&A 전문가다.
이론적 기반: Hood 1983 NATO 4축 정책수단, Howlett 2019 정책 도구 calibration,
Tallberg 2010 chair 절차권한, Putnam 1988 Two-Level Games,
Keohane & Victor 2011 regime complex.

## 엄격한 출력 규칙
1. CINA database lookup 결과만을 사실 근거로 사용
2. stance score 부호 + 소수점 2자리
3. 95% CI 표기
4. IR 이론 한 번 이상 인용
5. "📎 근거 N건" 명시
6. 데이터 없는 정보는 "데이터베이스에 명시되지 않음" 표기
7. 한국어 자연 단락
```

### Top-k retrieval to LLM context

LLM에는 최상위 24 records만 전달 (이전: 모든 records). 각 record는:
```
[Record 1] country=Brazil | issue=GGA-IND | cop=COP30
  stance=+1.00 (95% CI [+0.92, +1.00])
  frame=sovereignty | NATO: N=0.55 A=0.24 T=0.16 O=0.30
  proc_composite=1.00 | coalition=G77+China
  translation_gap_delta=+0.00
  evidence: [COP30, Brazil] 59 voluntary, non-prescriptive...
  source: verified_canonical
```

### Multi-turn 메모리

최근 5턴이 prompt에 포함되어 LLM이 대화 흐름을 인지함.

### Fallback

LLM 호출 실패 시 자동으로 rule-based 결과로 fallback + 에러 메시지 표시.

---

## 5. 사용법

### 로컬 실행

```bash
# 1. v5 dataset 생성
python -m src.data.build_v5_dataset

# 2. CLI Q&A
python -m src.program.query_engine_v2 --demo
python -m src.program.query_engine_v2 "사우디 L&D-OP 점수?"

# 3. 웹 인터페이스 (정적 호스팅)
python -m http.server 8000
# → http://localhost:8000/docs/web/cina_program_v2.html
```

### 라이브 배포

- v4.1 (legacy): `https://zxsa0716.github.io/cina/web/cina_program.html`
- v2 (NEW): `https://zxsa0716.github.io/cina/web/cina_program_v2.html`

두 페이지는 병렬 운영 (v4.1은 deprecation 예정).

---

## 6. 마이그레이션 가이드 (v4.1 사용자)

1. v4.1 dataset (stances_v4.jsonl)은 그대로 유지 — v5는 별도 파일
2. v4.1 query engine (`src/program/query_engine.py`)도 그대로 사용 가능
3. **새 기능 사용은 v5/v2 엔트리포인트로 전환**:
   - `from src.program.query_engine_v2 import answer_question`
   - URL은 `cina_program_v2.html`
4. BYO LLM 키는 동일 localStorage namespace (`cina_byo_key_*`) 사용 → 재입력 불필요

---

## 7. 알려진 한계

- v5 record 2,400 중 **검증된 verified_canonical은 v3 78개 + 일부 강화 인용 = 약 30건**. 나머지는 휴리스틱 합성으로, COP31 prospective validation 전까지 신뢰도 라벨이 보수적.
- 신규 20국의 stance pattern은 외부 문헌 인용보다는 ND-GAIN/GDP/block 휴리스틱에 의존.
- TRANS-FIN, TECH-TRANS 두 신규 이슈는 v3 검증 데이터가 없으므로 stance score는 전체적으로 합성.
- Multi-turn LLM 메모리는 단순 5턴 sliding window. semantic compression은 미구현.
- Export functions는 클라이언트 사이드만 (서버 저장 X).

---

## 8. 다음 단계

- v5 dataset의 verified 비율 확대 (현재 ~30 → 목표 200, 실 LLM 추출 + 외부 코더)
- COP31 prospective validation (2026.11)
- export PDF (matplotlib 또는 jspdf 통합)
- 다국어 (영어 UI 옵션)

---

**커밋 추적**:
- `data/processed/stances_v5.jsonl` (2,400 records)
- `data/processed/stances_v5_meta.json`
- `src/data/build_v5_dataset.py`
- `src/program/query_engine_v2.py`
- `docs/web/cina_program_v2.html`
- `docs/web/assets/cina_program_v2.js`
- `CHANGELOG_v5.md` (this file)
