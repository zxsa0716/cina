---
agent: policy-science-professor
round: 1
date: 2026-04-25
target: CINA Framework v2.0 + Round 1 산출물
total_chars: ~3,200 (한국어 본문 기준)
---

# Round 1 — 정책학 교수 Critique

## 총평 (Top-line)
CINA는 국제정치(IR) 이론(regime complex, two-level games, issue linkage)을 grounding으로 잘 깔았지만, **정책학(policy science)의 코어 — 정책 수단(instrument), 정책 이행(implementation), 다층 거버넌스(MLG), 정책 학습(policy transfer) — 은 거의 다루지 않는다**. Round 1 데이터 수집은 Q1 Coverage 0.18로 결정적 fail이며, 정책학 관점에서 보면 "Stage 1을 돌릴 정책 텍스트 자체가 없는" 상태다. 또한 장관급 브리핑 템플릿(`docs/09`)은 "외교부 기후환경과학외교국"을 수신처로 명기하면서도 한국 외교부·환경부 실제 보고 서식·이행체계와의 정합성이 한 줄도 검증되지 않았다.

---

## Section 1. 5-Dimension Rubric

| Dimension | Score | 산출 근거 |
|-----------|-------|----------|
| Theoretical grounding | **3/5** | IR 이론 4종은 명시적이지만 정책학 이론 0건. `docs/01 §5`의 "Supporting"에도 Howlett·Salamon·Pressman-Wildavsky·Hooghe&Marks 모두 부재. Climate Justice만 짧게 언급. |
| Methodological rigor | **3/5** | LLM→GNN→LLM 파이프라인의 quant rigor는 좋으나, 정책 이행 평가(implementation tracking) 메소드 0건. 평가 4-task(`docs/07`)는 모두 협상 산출물(스탠스·연합·합의·브리핑 품질) 기준이며, 합의 후 국내 이행은 측정 변수가 없음. |
| Empirical validity | **2/5** | Round 1 REPORT.md 기준 UNFCCC submission 0건, NDC 0건, ENB 0건. 정책 분석의 1차 사료가 부재한 상태에서 모든 후속 정책 함의는 invalid. IPCC AR6 4 챕터·Castro article·COP30 news 페이지만으로는 "국가 이슈별 스탠스" 추출 불가. |
| Policy strategic relevance | **2/5** | `docs/09` 템플릿은 외교부 보고 형식을 표방하나, (i) 한국 외교부 「외교문서 작성 표준」 문서번호 체계 KR-CLI-… 의 출처 미명시, (ii) 환경부 「국가기후위기적응대책(2026~2030)」 연계 모듈 없음, (iii) 의장국=브라질 fixed로 한국 실무자 직접 사용 어려움. 권고도 "양자 접촉 시퀀스" 위주로 정책 수단(NATO 프레임)이 한쪽으로 치우침. |
| Clarity & reproducibility | **4/5** | `docs/12 §4` 메타데이터 표준, `docs/13` 식별자 단일 정의처, sha256·license 100% 추적 등은 정책 reviewer도 재현 가능. 단, "정책 권고가 어느 단계에서 어떻게 만들어졌는가"의 audit trail은 evidence_quote+structural_fact까지만이고, **이론→권고**의 trace는 끊긴다. |

**평균 2.8/5** — 인프라·이론(IR)·재현성은 합격선, 정책학 코어·실증 자료·한국 적용성은 결정적 결함.

---

## Section 2. 핵심 비판 Top 3

### C1. 다층 거버넌스(MLG) 부재 — Country-Group-Issue만으로는 적응정책을 설명할 수 없다
- **인용**: `docs/05 §1.1`은 노드 유형을 Country(195)·Issue(6)·Group(12)로 한정. `CINA_FRAMEWORK.md §2`의 그래프 다이어그램도 동일. `docs/09 §6.2` 접촉 시퀀스도 "남아공 협상팀장 → EU 집행위 → AOSIS 의장" 등 **국가/그룹 단일 층위**.
- **이론 근거**: Hooghe & Marks(2003) Type I/II MLG, Bache & Flinders(2004)는 적응정책이 본질적으로 supranational ↔ national ↔ subnational ↔ local의 4-layer로 작동한다고 본다. 특히 적응(adaptation)은 mitigation과 달리 **지역(locality) 단위 이행**이 핵심이며(IPCC AR6 WGII Ch.17, 이미 수집됨), JT-ADAPT 이슈는 원주민·취약 커뮤니티 등 **비국가 행위자**가 정책 산출의 결정 요인이다. 브라질 의장국의 Amazon 정책은 연방-州(Pará, Amazonas)-원주민 단체 3-layer 분쟁이 핵심인데 CINA는 이를 단일 국가 노드 "BRA"로 압축한다.
- **수정 제안**:
  1. 노드 유형에 `Subnational`(브라질 9개 Amazon 주, 한국 17개 광역시도), `NonStateActor`(원주민조직 COICA, 환경 NGO, 산업협회) 추가.
  2. `docs/05 §1.2` 엣지 표에 `implements_at(National→Subnational)`, `lobbies(NonState→Country×Issue)` 두 type 추가.
  3. JT-ADAPT 이슈에 한해 비국가 행위자 노드 강제(이슈가 본질적으로 비국가 행위자 권리 이슈이므로). 단, 데이터 가용성 문제로 Round 2의 P1 task로 제안.

### C2. 정책 수단(Policy Instrument) 균형 검토 부재 — 권고가 "Authority"에 편중
- **인용**: `docs/09 §6.2 접촉 시퀀스`는 "양자 회담→지지 성명→내부 조율" 등 모두 외교적 권위(authority) 수단. `docs/02 §2.1` 추출 스키마의 `key_demands`·`red_lines`·`flexibility_signals` 셋 다 **협상 입장 시그널**이고, 재정·제도·정보 수단은 추출 필드 없음.
- **이론 근거**: Hood(2007) NATO 프레임 — Nodality(정보), Authority(규제·권한), Treasure(재정), Organization(제도·기구) — 으로 정책 수단을 분류하면, 적응정책의 핵심은 ADAPT-FIN(Treasure)·NAPs(Organization)·GGA-IND(Nodality, 지표 자체가 정보 수단)이다. Salamon(2002)도 "규제 일변도 정책은 실패한다"고 경고. 그런데 CINA는 추출 단계부터 협상 시그널만 본다 → 재원 약속의 strength·실행 메커니즘의 신뢰도가 빠진다. 한국 환경정책학에서 정회성(2014, 한국환경정책학회 학술대회) 「적응정책의 정책수단 결합」도 동일 지적.
- **수정 제안**:
  1. Stage 1 추출 스키마에 `instrument_signals: {nodality, authority, treasure, organization}` 4-필드 dict 추가. 각 필드는 해당 수단을 시사하는 quote/score.
  2. Stage 3 §6 "권고 전략 자세"를 **NATO 4축 매트릭스**로 재구성. "정보 수단(GGA 지표 형식 제안) × 재정 수단(KR 적응협력 분담률 명시) × 권위 수단(접촉 시퀀스) × 조직 수단(NAPs 기술 지원 거버넌스 신설)" 4셀.
  3. 평가 Task A에 instrument_balance 메트릭 추가 — "권고가 4 수단에 얼마나 분포하는가."

### C3. 정책 이행 격차(Implementation Gap) 변수 부재 — 합의→이행 chain 추적 안 함
- **인용**: `docs/07` 4-task 어디에도 합의문 채택 이후의 국내 이행 결과(NDC 갱신·예산 편성·법령 제정)을 측정하는 dependent variable 없음. `docs/09` 브리핑은 "최선/기본/최악 시나리오"가 모두 협상 결과 기준이고, 한국 정부 환경부 NAP·재정부 GCF 분담·법무부 기후소송 대응 등 **이행 단계 risk**가 비어 있음.
- **이론 근거**: Pressman & Wildavsky(1973)는 "합의는 이행이 아니다, 이행은 결정 지점이 늘어날수록 지수적으로 실패한다"고 주장. Sabatier(2007) Advocacy Coalition Framework도 정책 학습이 합의 후 5-10년 cycle에서 일어난다고 봄. 적응정책은 특히 finance pledge → actual disbursement gap이 60% 이상(OECD 2024). CINA가 "COP30 합의 99% 예측"해도 그 합의의 80%가 이행 안 되면, 정책학적으로는 무용하다.
- **수정 제안**:
  1. Stage 2 그래프에 시간 차원 t를 COP21~30(현재)뿐 아니라 t+1~t+3(post-COP 12~36개월)까지 확장. NDC 갱신·국내 법령 제정·예산 편성 데이터를 outcome edge로 추가.
  2. 평가에 **Task E — Implementation Realization Rate** 신설. 과거 COP21~28의 합의 약속 중 t+24m 시점 실제 이행률을 ground truth로, CINA가 어떤 약속이 이행 가능성 높은지 사전 예측하는가.
  3. 브리핑 §5 Red Lines 에 "이행 위험(implementation risk)" 별도 subsection — 한국에서 GCF 기여 약속이 기재부 예산편성 → 국회 비준 통과 가능성을 0~1 score로.

---

## Section 3. 한국 정책학 관점 추가 권고

### 3.1 외교부 기후환경과학외교국 실무 모듈
- 현 템플릿은 보고 양식만 있고 외교부 「녹색·기후외교 추진전략(2024.9)」의 4대 추진과제(다자협력 주도·아시아태평양 연대·기후재원 외교·녹색기술 외교)와의 매핑 없음. **수정**: §1 "현황 평가" 앞에 §0 "정부 추진전략 정합성" 추가, 4대 과제 각각에 CINA 분석이 어떻게 기여하는지 명시.

### 3.2 환경부 적응정책과 연계
- 「제3차 국가기후위기적응강화대책(2023~2025)」 5대 과학기반 기후재난 대응 전략과 GGA-IND 6개 핵심 영역(food/water/health/ecosystem/infrastructure/poverty)의 cross-walk를 부록에 첨부. 환경부가 외교부 브리핑을 받았을 때 "어느 환경부 과제가 영향받는가" 즉시 식별 가능.

### 3.3 국가기후위기적응대책 정합성
- 한국 적응 거버넌스의 부처 간 조율(환경부·해수부·산림청·기상청·재난안전관리본부) 매트릭스가 CINA 분석에 반영되지 않음. 한국행정학보의 부처 간 조율 모델(임도빈·정정길 계열)을 적용하여, 6개 적응 이슈별 국내 주관 부처 mapping을 §3 "레버리지 분석"의 한국 sub-section에 추가.

---

## Section 4. ir-political-professor와의 합의·불일치 예측

### 합의 예상
- **방법론 신규성·재현성**은 양 교수 모두 합격 평가할 것. Castro 2025 dataset의 ground truth 활용·Bayesian calibration·sha256 메타 표준 등.
- **Round 1 Q1 Coverage fail**은 양쪽 모두 결정적 결함으로 동의. UNFCCC/NDC/ENB 0건이면 IR이든 정책학이든 분석 불가.

### 불일치 예상
- **이행 가능성 vs 협상 권력의 강조점 차이**:
  - 정책학(나): "합의가 이행으로 안 가면 무의미하다 → Implementation Realization Rate를 평가에 추가하라."
  - IR 정치학(예상): "협상 권력 분포·블록 동학·hegemonic stability가 본질이다 → 이행은 국내정치의 영역이고 모델 scope 밖이다."
- **노드 추가의 우선순위**:
  - 정책학(나): Subnational·NonStateActor 추가가 적응정책의 본질 (특히 JT-ADAPT).
  - IR(예상): Country-Group이 협상 단위이므로 추가는 model complexity만 늘리고 식별 어려움.
- **생산적 긴장**: team-lead가 "CINA의 scope를 협상 분석(IR)에 한정할지, 정책 cycle 전체로 확장할지" 헌법 수준 결정 필요. 현 v2.0은 전자에 가까움. Heedo의 의도(논문감 + 수업 활용)와 정렬 필요.

---

## Section 5. 추가 Reference (한국 정책학 우선)

### 한국 학술 (≥3)
1. **명수정·이정석 (2023)** 「국가기후위기적응대책 이행평가체계 개선방안」, 한국환경연구원 KEI Working Paper 2023-12. — 이행평가 변수 설계의 한국적 표준.
2. **고재경 (2022)** 「지방자치단체 기후위기 적응대책의 다층 거버넌스 분석」, 한국정책학회보 31(4). — MLG의 한국 적용 사례, 광역시도 노드 추가 근거.
3. **윤순진 외 (2024)** 「기후재원 외교의 국내 정치경제: NDC와 예산편성의 정합성」, 한국행정학보 58(2). — Implementation Gap의 한국 사례.

### 정책기관 보고서 (≥2)
4. **KEI (2024)** 『제3차 국가기후위기적응대책 중간 모니터링 보고서』 — 5대 과학기반 적응 영역과 GGA cross-walk의 1차 자료.
5. **KIEP (2024)** 「COP29 기후재원 NCQG 협상 분석과 한국의 대응방안」, 대외경제정책연구원 KIEP 오늘의 세계경제 24-32. — ADAPT-FIN 이슈의 한국적 분석 모델.

### 국제 정책학 (보강)
6. Howlett, M., & Ramesh, M. (2003). *Studying Public Policy: Policy Cycles and Policy Subsystems* (2nd ed.). Oxford UP. — NATO 프레임 운용.
7. Pressman, J., & Wildavsky, A. (1973). *Implementation*. UC Press. — Implementation chain 이론.
8. Hooghe, L., & Marks, G. (2003). Unraveling the Central State, but How? Types of Multi-level Governance. *American Political Science Review*, 97(2). — MLG Type I/II.
9. Dolowitz, D., & Marsh, D. (2000). Learning from Abroad: The Role of Policy Transfer in Contemporary Policy-Making. *Governance*, 13(1). — 정책 학습/이전.

---

## Section 6. team-lead 결정 요청

1. **CINA scope 결정 (헌법 수준)**: 협상 분석(COP30까지)으로 한정할지, 정책 cycle 전체(합의→이행 t+24m)로 확장할지. 후자라면 평가 Task E 신설·outcome edge 데이터 추가 수집 필요. Heedo의 "논문감" 의도에는 후자가 더 부합하나 Round 4까지의 마감 압박과 trade-off.
2. **MLG 노드 확장의 Round 2 P1 포함 여부**: Subnational(브라질 Amazon 주·한국 광역시도)·NonStateActor(원주민·NGO) 노드 추가가 Round 2 task에 들어갈지. 데이터 수집 부담 큼(브라질 주 단위 적응계획·COICA 입장문 등).
3. **한국 정부 보고 양식 정합성 검증 task 신설**: 외교부 「외교문서 작성 표준」·환경부 NAP 보고 양식과 `docs/09` 템플릿의 cross-walk를 외부 자문(KEI 또는 한국정책학회 적응정책 분과 contact)으로 검증할지.

---

## 다음 라운드 권고 우선순위

- **High**: Round 2에 (a) UNFCCC/NDC/ENB Playwright 우회로 정책 텍스트 확보, (b) Stage 1 스키마에 `instrument_signals` 4-필드 추가, (c) Implementation Gap 평가 Task E 헌법 수준 합의.
- **Medium**: MLG Subnational/NonStateActor 노드 추가, 한국 정부 양식 정합성 검증.
- **Low**: 한국 학술 ref 추가 인용은 docs/01 §5 보강 시 일괄 반영.

**문서 끝**
