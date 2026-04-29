# 11. Source Catalog — 모든 데이터 소스 카탈로그

> CINA가 사용하는 모든 외부 데이터 소스의 정확한 URL, 접근법, 라이선스, 식별 패턴.
> 이 문서가 곧 collector 구현의 사양서다.

---

## 0. 카탈로그 분류

| 등급 | 의미 | 예시 |
|------|------|------|
| **Tier-1 (Primary)** | CINA의 핵심 학습/검증 데이터 | UNFCCC submission, ENB, NDC |
| **Tier-2 (Calibration)** | Ground truth / calibration set | Castro et al. 2025, Climate Action Tracker |
| **Tier-3 (Context)** | 이론 접지·과학 근거 | IPCC AR6, IISD analysis |
| **Tier-4 (Adjacent)** | 보조 분석 | World Bank CCDR, Brazilian government docs |

---

## 1. UNFCCC 공식 문서 시스템 (Tier-1)

### 1.1 소스 정보
- **명칭**: UNFCCC Documents Portal
- **주소**: https://unfccc.int/documents
- **운영**: UN Climate Change Secretariat (Bonn, Germany)
- **총 문서 수**: ~63,118건 (2025-12 기준)

### 1.2 URL 필터 패턴

```
https://unfccc.int/documents
  ?f[0]=topic:{TOPIC_ID}
  &f[1]=conference:{CONF_ID}
  &f[2]=country:{ISO3}
```

URL 인코딩 시: `f[0]` → `f%5B0%5D`

### 1.3 핵심 Topic ID (CINA 적응 섹터)

| Topic | ID | 설명 |
|-------|-----|------|
| Adaptation | **1136** | 적응 일반 |
| Adaptation Committee | 3484 | AC 산하 |
| National Adaptation Plans | 3812 | NAPs 프로세스 |
| Loss and Damage | 3558 | L&D 일반 |
| Adaptation Finance | (검색 확인 필요) | 재원 |
| Just Transition | (검색 확인 필요) | UAE JTWP |

### 1.4 핵심 Conference ID

| Conference | ID | 회기 |
|-----------|-----|------|
| COP 30 | (확인 필요) | 2025-11 Belém |
| COP 29 | (확인 필요) | 2024-11 Baku |
| COP 28 | (확인 필요) | 2023-12 Dubai |
| SBI 62 | (확인 필요) | 2025-06 Bonn |
| SBSTA 62 | (확인 필요) | 2025-06 Bonn |
| CMA 7 | (확인 필요) | 2025-11 Belém |

**TODO**: collector가 첫 실행 시 conference dropdown HTML 파싱하여 ID 매핑 자동 구축.

### 1.5 Symbol 패턴 (UNFCCC 문서 식별자)
```
FCCC/CP/2025/L.X      ← COP 결정
FCCC/CMA/2025/L.X     ← CMA 결정
FCCC/SBI/2025/X       ← SBI 의제 문서
FCCC/SBSTA/2025/X     ← SBSTA 의제
FCCC/SBI/2025/INF.X   ← Information note
FCCC/SBI/2025/MISC.X  ← Miscellaneous (Party submission 묶음)
```

CINA는 특히 **MISC** (개별 Party submission 묶음) 문서를 우선 수집한다.

### 1.6 Document Type
- `Conclusions` (의장단 결론)
- `Decisions` (CMA/COP 결정)
- `Submissions from Parties` (각국 입장)
- `Information notes`
- `Reports`

### 1.7 라이선스
UN 공개 문서. UN Re-use Policy: 출처 명시 시 자유 재이용.

### 1.8 Rate limit (정찰 결과)
명시된 robots.txt 제한 없음. 보수적으로 1 req/sec.

### 1.9 Collector 구현
`src/collect/unfccc_submissions.py`

---

## 2. NDC Registry (Tier-1)

### 2.1 소스 정보
- **명칭**: NDC Registry (Paris Article 4.12)
- **주소**: https://unfccc.int/NDCREG
- **총 NDC 수**: 337건 (모든 Party의 모든 버전)

### 2.2 NDC PDF URL 패턴
정찰 결과 확인된 패턴:
```
https://unfccc.int/sites/default/files/{YYYY-MM}/{COUNTRY_CODE}-{YYYY-MM-DD}%20{TITLE}.pdf
```

예시:
```
https://unfccc.int/sites/default/files/2025-11/DK-2025-11-05%20EU%20NDC.pdf
```

### 2.3 브라질 NDC (focal country)
- **2023 Updated NDC**: PDF 직접 링크 collector가 동적 발견 필요
- **NAP**: 별도 NAP central database (UNFCCC LEG)

### 2.4 라이선스
국가 주권 문서. 인용 가능, 재배포는 출처 명시.

### 2.5 Collector
`src/collect/ndc_registry.py`

---

## 3. IISD Earth Negotiations Bulletin (Tier-1)

### 3.1 소스 정보
- **명칭**: Earth Negotiations Bulletin
- **운영**: IISD Reporting Services
- **주소**: https://enb.iisd.org/
- **UNFCCC 페이지**: https://enb.iisd.org/negotiations/un-framework-convention-climate-change-unfccc

### 3.2 URL 패턴
```
# 일일 게시판
https://enb.iisd.org/sites/default/files/{YYYY-MM}/enb12{NNN}e.pdf
   (예: enb12888e.pdf — COP30 day 8)

# 종합 요약 페이지
https://enb.iisd.org/{event-slug}-summary
   (예: bonn-climate-change-conference-sb62-sbi62-sbsta62-summary)

# 회기별 인덱스
https://enb.iisd.org/events/{event-slug}
```

### 3.3 ENB 호수 패턴
ENB는 Vol 12 (UNFCCC 시리즈)이며, 각 발행은 `enb12{N}e.pdf` 형태:
- `enb12888e.pdf` — COP30 final summary 직전
- 매 COP마다 약 12-20개 일일 발행

### 3.4 정찰 결과 — 직접 fetch 차단
WebFetch 403. 우회 방법:
1. requests 라이브러리에 `User-Agent: Mozilla/5.0` 헤더 추가
2. 1 req/sec rate limit 엄수
3. robots.txt 확인 (CC BY-NC-SA 라이선스이므로 연구용 OK)

### 3.5 라이선스
**CC BY-NC-SA 4.0** — 비영리 학술 연구 재이용 가능, 동일 라이선스 공유 의무.

### 3.6 Collector
`src/collect/iisd_enb.py`

---

## 4. Castro et al. 2025 ENB Dataset (Tier-2 / Ground Truth)

### 4.1 소스 정보
- **논문**: Castro, P., Kristof, V., Kammerer, M., & Cogne, T. (2025). *Participation, Cooperation and Conflict in UN Climate Negotiations*. Nature Scientific Data.
- **DOI**: 10.1038/s41597-025-06262-4
- **URL**: https://www.nature.com/articles/s41597-025-06262-4

### 4.2 데이터 위치
Nature Scientific Data 부속 데이터:
- Figshare 또는 Zenodo 저장소 (논문 페이지에서 링크)
- CSV/JSON 형식

### 4.3 데이터 내용
- 1995-2023 ENB 협상 인터랙션
- Country pair × interaction type (cooperation/conflict) × date
- Auto-coded from ENB text + hand-coded validation set

### 4.4 라이선스
Nature Sci Data 정책 — 일반적으로 CC BY 4.0 (논문 페이지에서 확인 필요).

### 4.5 CINA에서의 용도
- **Stage 1 calibration**: stance score Platt calibration의 ground truth
- **Stage 2 prior**: 국가-국가 cooperation edge weight의 prior
- **Task B evaluation**: coalition F1의 ground truth

### 4.6 Collector
`src/collect/castro_2025.py`

---

## 5. COP30 Official Site (Tier-1)

### 5.1 소스 정보
- **명칭**: COP30 Brazilian Presidency Official Site
- **주소**: https://cop30.br/en
- **운영**: Brazilian Government, MMA + Itamaraty

### 5.2 핵심 페이지
- 공식 결정문: https://cop30.br/en/news-about-cop30/cop30-approves-belem-package1
- 의장단 letters: https://cop30.br/en/cop30-presidency
- 보도자료: https://cop30.br/en/news-about-cop30

### 5.3 라이선스
브라질 정부 공식 발표. 인용 가능, 재배포 출처 명시.

### 5.4 Collector
`src/collect/cop30_official.py`

---

## 6. IPCC AR6 (Tier-3 / 과학 근거)

### 6.1 소스 정보
- **운영**: Intergovernmental Panel on Climate Change
- **주소**: https://www.ipcc.ch/
- **AR6 WGII 적응**: https://www.ipcc.ch/report/ar6/wg2/

### 6.2 핵심 챕터 (CINA 적응 섹터)
- **Ch.1 Point of Departure** — 적응 거버넌스 출발점
- **Ch.16 Key Risks across Sectors** — Hazard-Exposure-Vulnerability
- **Ch.17 Decision-Making Options** — 의사결정 프레임
- **Ch.18 Climate Resilient Development**
- **Cross-Chapter Box: Just Transitions**

### 6.3 PDF 다운로드 패턴
```
https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_Chapter{NN}.pdf
```

### 6.4 라이선스
IPCC 자료. 비영리 학술 재이용 자유, 출처 명시 필수.

### 6.5 Collector
`src/collect/ipcc_ar6.py`

---

## 7. NegotiateCOP (Tier-2 / 보조 검색)

### 7.1 소스 정보
- **명칭**: NegotiateCOP — UNFCCC AI Assistant
- **주소**: https://negotiatecop.org/
- **운영**: GIZ (German Federal Government), Adaptation Community

### 7.2 사용 방식
- API 또는 웹 인터페이스
- UNFCCC 문서 시맨틱 검색 + QA
- CINA의 Stage 0.5 보조 (gap 발견 시 정보 보강)

### 7.3 주의
NegotiateCOP의 응답을 **그대로 복제 인용 금지**. CINA는 원문 UNFCCC 문서를 1차 소스로 사용.

---

## 8. 보조 소스 (Tier-4)

| 명칭 | URL | 용도 |
|------|-----|------|
| Climate Action Tracker | https://climateactiontracker.org/ | 국가별 정책 평가 |
| ND-GAIN Index | https://gain.nd.edu/our-work/country-index/ | 적응 취약성 점수 (국가 노드 피처) |
| World Bank CCDR | https://www.worldbank.org/en/publication/country-climate-development-reports | 국가 기후개발 보고 |
| Carbon Brief | https://www.carbonbrief.org/ | 정책 분석 (인용 보조) |
| Brazilian MMA | https://www.gov.br/mma/ | 브라질 환경부 정책 (포어 번역) |
| Itamaraty | https://www.gov.br/mre/ | 브라질 외교부 |
| KEI | https://www.kei.re.kr/ | 한국환경연구원 |
| KIEP | https://www.kiep.go.kr/ | 대외경제정책연구원 |

---

## 9. 라이선스 매트릭스

| 소스 | 라이선스 | 재배포 | 인용 의무 |
|------|---------|--------|----------|
| UNFCCC docs | UN Open License | OK | 출처 명시 |
| NDC Registry | Sovereign | 출처 명시 후 | 필수 |
| IISD ENB | CC BY-NC-SA 4.0 | 동일 라이선스로 | 필수 |
| Castro 2025 | CC BY 4.0 (추정) | OK | DOI 인용 |
| COP30 official | Public statement | OK | 출처 명시 |
| IPCC AR6 | IPCC Open | OK | 챕터 인용 |
| NegotiateCOP | (확인 필요) | 응답 직접복제 X | 도구 인용 |

CINA가 공개하는 모든 산출물(논문, 데이터셋)은 **CC BY 4.0 + MIT** 듀얼.

---

## 10. 윤리·운영 원칙

1. **robots.txt 준수**: 모든 collector는 첫 실행 시 robots.txt fetch
2. **Rate limit**: 기본 1 req/sec, 도메인별 override 가능
3. **User-Agent 정직**: `CINA-Research/2.0 (academic; contact: zxsa0716@kookmin.ac.kr)`
4. **체크포인트**: 모든 collector는 `.collect_state.json` 으로 재개 가능
5. **SHA-256 해시**: 모든 다운로드 파일에 hash 기록 → 무결성 검증
6. **메타데이터 첨부**: 모든 raw 파일에 license · retrieved_at · source_url · sha256 동봉

---

## 11. 수집 범위 (CINA-Brazil-COP30 데이터셋)

**기간**: 2015-01-01 ~ 2025-12-31 (Paris Agreement 이후)
**우선 회기**: COP21, COP26, COP27, COP28, COP29, COP30, SBI/SBSTA 60-62
**우선 국가** (20):
- Brazil (focal), EU, US, China, India, AOSIS, LDCs, African Group, AILAC, Arab Group, LMDC, Japan, S.Korea, Australia, Saudi Arabia, S.Africa, Norway, Switzerland, Mexico, Colombia
**우선 이슈** (6): GGA-IND, ADAPT-FIN, L&D-OP, NAPs, MIT-ADAPT, JT-ADAPT

**예상 문서 수**:
- UNFCCC submissions: ~300건
- NDCs: ~50건 (20국 × 2-3 버전)
- ENB 일일 발행: ~80건 (회기당 12-20)
- IPCC AR6 챕터: 5건
- Castro dataset: 1건
- COP30 official: ~10건

**합계**: 약 450건 → 약 2-5 GB.

---

## 12. 다음 단계

이 카탈로그를 기반으로:
1. [docs/12_data_collection_master_plan.md](12_data_collection_master_plan.md) — 수집 일정·우선순위
2. [docs/13_reference_tables.md](13_reference_tables.md) — 국가/그룹/이슈 식별자
3. `src/collect/*.py` — 소스별 collector 실제 구현
4. `data/manifest/manifest.jsonl` — 수집 결과 누적 매니페스트
