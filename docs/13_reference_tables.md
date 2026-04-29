# 13. Reference Tables — 식별자 표준

> CINA가 사용하는 모든 국가·그룹·이슈·세션 식별자의 단일 정의처(single source of truth).
> 모든 collector·refinement·analysis 코드는 이 식별자를 참조한다.

---

## 1. 국가 코드 (Country Identifiers)

CINA는 **ISO 3166-1 alpha-3** (3자) 코드를 표준으로 사용. EU·연합체는 별도 코드.

### 1.1 CINA 핵심 20국 (Stage 1 우선 추출 대상)

| Slug | ISO3 | Full Name | UN Region | Climate Group |
|------|------|-----------|-----------|--------------|
| brazil | BRA | Brazil (federal republic of) | LAC | G77, BASIC, AILAC-observer |
| eu | EU | European Union | Europe | EU |
| usa | USA | United States of America | NA | Umbrella |
| china | CHN | China (People's Republic of) | Asia | G77, BASIC, LMDC |
| india | IND | India | Asia | G77, BASIC, LMDC |
| japan | JPN | Japan | Asia | Umbrella |
| south_korea | KOR | Korea (Republic of) | Asia | EIG |
| australia | AUS | Australia | Oceania | Umbrella |
| canada | CAN | Canada | NA | Umbrella |
| norway | NOR | Norway | Europe | Umbrella |
| switzerland | CHE | Switzerland | Europe | EIG |
| mexico | MEX | Mexico | LAC | EIG, AILAC |
| south_africa | ZAF | South Africa | Africa | G77, BASIC, African Group |
| saudi_arabia | SAU | Saudi Arabia | MENA | G77, Arab Group, LMDC |
| uae | ARE | United Arab Emirates | MENA | G77, Arab Group |
| egypt | EGY | Egypt | MENA | G77, Arab Group, African Group |
| colombia | COL | Colombia | LAC | G77, AILAC |
| chile | CHL | Chile | LAC | G77, AILAC |
| costa_rica | CRI | Costa Rica | LAC | G77, AILAC, HAC |
| kenya | KEN | Kenya | Africa | G77, African Group |

### 1.2 협상 그룹 (Negotiating Groups)

| Slug | Full Name | 멤버 수 | CINA 처리 |
|------|----------|---------|-----------|
| g77 | G77 + China | 134 | 그룹 노드 |
| eu_g | European Union | 27 | 그룹 노드 (EU와 동일 처리) |
| umbrella | Umbrella Group | ~10 | 그룹 노드 |
| eig | Environmental Integrity Group | 5 | 그룹 노드 |
| aosis | Alliance of Small Island States | 39 | 그룹 노드 |
| ldc | Least Developed Countries | 45 | 그룹 노드 |
| african | African Group | 54 | 그룹 노드 |
| arab | Arab Group | 22 | 그룹 노드 |
| ailac | AILAC | 8 | 그룹 노드 |
| basic | BASIC | 4 | 그룹 노드 |
| lmdc | Like-Minded Developing Countries | ~25 | 그룹 노드 |
| hac | High Ambition Coalition | ~70 (가변) | 그룹 노드 |
| amazon | Amazon Cooperation Treaty | 8 | 보조 그룹 노드 |

### 1.3 그룹 멤버십 매트릭스
구현: `src/data/group_membership.csv`
- Rows: country slug
- Cols: group slug
- Values: 0/1 (시간 invariant) 또는 가입연도 (시간 variant)

---

## 2. 이슈 코드 (Issue Identifiers — Adaptation Sector)

CINA Stage 1/2/3 모든 곳에서 **이 코드만** 사용.

| Code | Full Label | UNFCCC Topic ID | Paris Article | 우선순위 |
|------|-----------|------------------|--------------|---------|
| **GGA-IND** | Global Goal on Adaptation Indicators | (1136 + 별도) | Art. 7.1 | P0 |
| **ADAPT-FIN** | Adaptation Finance | — | Art. 9 | P0 |
| **L&D-OP** | Loss and Damage Fund Operations | 3558 | Art. 8 | P0 |
| **NAPs** | National Adaptation Plans | 3812 | Art. 7.9 | P1 |
| **MIT-ADAPT** | Mitigation-Adaptation Nexus | — | Art. 7.7 | P2 |
| **JT-ADAPT** | Just Transition with Adaptation | — | UAE JTWP | P2 |

### 2.1 Issue 분류 키워드 (1차 필터용)

```python
ISSUE_KEYWORDS = {
    "GGA-IND": [
        "Global Goal on Adaptation", "GGA", "UAE Framework",
        "adaptation indicator", "Belém Adaptation Indicators",
        "indicator framework", "global resilience",
    ],
    "ADAPT-FIN": [
        "adaptation finance", "adaptation funding", "NCQG",
        "doubling adaptation finance", "tripling adaptation finance",
        "adaptation gap", "GCF adaptation",
    ],
    "L&D-OP": [
        "Loss and Damage", "L&D Fund", "FRLD",
        "non-economic loss", "Santiago Network",
        "direct access", "Sharm el-Sheikh dialogue",
    ],
    "NAPs": [
        "National Adaptation Plan", "NAP", "LEG",
        "iterative submission", "NAP central",
    ],
    "MIT-ADAPT": [
        "mitigation-adaptation", "co-benefits", "synergies",
        "trade-offs", "integrated approach",
    ],
    "JT-ADAPT": [
        "Just Transition", "JTWP", "vulnerable populations",
        "indigenous", "gender-responsive adaptation",
        "labour rights",
    ],
}
```

### 2.2 Issue ↔ COP 결정 매핑

| Issue | 핵심 결정 | COP |
|-------|----------|-----|
| GGA-IND | 11/CMA.5 (UAE Framework), Belém indicators | COP28→COP30 |
| ADAPT-FIN | Glasgow doubling, Belém tripling | COP26→COP30 |
| L&D-OP | Loss and Damage Fund 설립 결정 | COP27→COP28 |
| NAPs | 4/CMA.3 NAP 가이드라인 | COP21→ |
| JT-ADAPT | UAE Just Transition Work Programme | COP28→ |

---

## 3. COP 회기 (Conference Sessions)

| Session | Year | Place | URL Slug | Key Outcome (적응 관련) |
|---------|------|-------|----------|-------------------------|
| COP21 / CMA1 | 2015 | Paris | cop21 | Paris Agreement, Art. 7 |
| COP22 / CMA1.bis | 2016 | Marrakech | cop22 | Marrakech Action Proclamation |
| COP23 / CMA1.bis2 | 2017 | Bonn | cop23 | Talanoa Dialogue 시작 |
| COP24 / CMA1.bis3 | 2018 | Katowice | cop24 | Paris Rulebook |
| COP25 | 2019 | Madrid | cop25 | (적응 진전 미진) |
| COP26 / CMA3 | 2021 | Glasgow | cop26 | Glasgow-Sharm el-Sheikh GGA WP |
| COP27 / CMA4 | 2022 | Sharm el-Sheikh | cop27 | L&D Fund 설립 |
| COP28 / CMA5 | 2023 | Dubai | cop28 | UAE Framework on GGA, GST |
| COP29 / CMA6 | 2024 | Baku | cop29 | NCQG (재원), 운영 결정 |
| **COP30 / CMA7** | 2025 | **Belém** | **cop30** | **Belém Adaptation Indicators (59), 재원 3배 공약** |

### 3.1 부속 기관 회의

| Body | Function | 연 2회 |
|------|----------|--------|
| SBI | Implementation 점검 | 5월 (Bonn), COP 동시 |
| SBSTA | Scientific advice | 5월, COP 동시 |
| AC | Adaptation Committee | 비정기 |
| LEG | LDC Expert Group | 비정기 |
| TEC | Technology Executive Committee | 비정기 |

---

## 4. UNFCCC 문서 분류 (Document Types)

| Type | 약어 | 의미 |
|------|------|------|
| Decision | DEC | CMA/COP 공식 결정 |
| Conclusions | CONC | 의장단 결론 (CP, CMA, SBI, SBSTA) |
| Submissions | SUBM | Party 입장 제출 (개별 또는 묶음 MISC) |
| Information note | INF | 사무국 정보 |
| Misc | MISC | Party submission 모음 |
| Technical paper | TP | 기술 분석 |
| Synthesis report | SYNTH | 종합 |
| Reports | RPT | 보고서 (회의록, 활동) |

CINA는 **DEC + SUBM + MISC + CONC** 우선 수집.

---

## 5. ENB Volume Convention

ENB는 Vol 12 = UNFCCC, 각 발행은 일련번호.

| Volume | Series | 일련번호 패턴 |
|--------|--------|--------------|
| Vol 12 | UNFCCC | enb12{NNN}e.pdf (e=English) |
| Vol 9 | CSD/HLPF | enb09... (CINA 미사용) |

### 5.1 COP30 ENB 시리즈 (예상)
- enb12880e ~ enb12895e 정도 (10-15개 발행, COP30 기간)
- Final summary report: enb12{LAST}e

---

## 6. 데이터 디렉토리 구조 (식별자 적용)

```
data/raw/
├── unfccc_submissions/
│   └── {cop_slug}/                      # cop30, cop29, ...
│       ├── {symbol_slug}.pdf            # FCCC_CP_2025_L19.pdf
│       └── {symbol_slug}.meta.json
├── ndcs/
│   └── {iso3}/
│       ├── {iso3}_NDC_v{N}_{YYYY-MM}.pdf
│       └── {iso3}_NDC_v{N}_{YYYY-MM}.meta.json
├── enb_summaries/
│   └── {cop_slug}/
│       ├── enb12{NNN}e.pdf
│       └── enb12{NNN}e.meta.json
├── ipcc_ar6/
│   └── wg{N}/
│       └── chapter_{NN}.pdf
├── castro_2025/
│   └── enb_interactions_1995_2023.csv
└── cop30_official/
    └── {date}_{slug}.html
```

---

## 7. Country Power Index (그래프 분석용)

CINA Stage 2의 epistemic divergence 계산에서 사용. 각 국가의 협상 영향력 가중치.

```python
COUNTRY_POWER_INDEX = {
    "BRA": 0.85,  # 의장국 + BASIC
    "EU":  0.95,
    "USA": 0.90,
    "CHN": 0.92,
    "IND": 0.78,
    "AOSIS": 0.62,  # 도덕적 권위
    "LDC":   0.55,
    "ZAF":   0.65,
    "SAU":   0.70,  # 석유 + Arab Group
    # ... 점수는 (a) GDP+CO2 score + (b) historical agenda-setting + (c) group leadership
    # 산출 근거는 src/data/power_index.py에 명시
}
```

---

## 8. ND-GAIN Vulnerability (노드 피처)

각 국가의 적응 취약성·준비도 점수 (0~1, 높을수록 취약):

```python
ND_GAIN_VULNERABILITY = {
    # 출처: https://gain.nd.edu/our-work/country-index/
    # 최신: 2024 Index
    "BRA": 0.443,
    "EU":  0.333,  # 27국 평균
    "USA": 0.353,
    "CHN": 0.422,
    "IND": 0.522,
    # ...
}
```

`src/data/nd_gain_vulnerability.csv` 에 전체 국가 표.

---

## 9. 식별자 검증 규칙

모든 collector·refinement 코드는 다음 검증을 통과해야 한다:

```python
def validate_identifiers(record: dict) -> list[str]:
    errors = []
    if record.get("country") and record["country"] not in CINA_COUNTRIES:
        errors.append(f"Unknown country: {record['country']}")
    if record.get("issue") and record["issue"] not in CINA_ISSUES:
        errors.append(f"Unknown issue code: {record['issue']}")
    if record.get("session") and record["session"] not in CINA_SESSIONS:
        errors.append(f"Unknown session: {record['session']}")
    return errors
```

`src/data/identifiers.py`에 단일 정의.

---

## 10. 다음 문서
- `src/data/identifiers.py` — Python에서 import 가능한 단일 식별자 모듈
- `src/collect/unfccc_submissions.py` 등 — 실제 collector 구현
