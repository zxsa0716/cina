# 📄 KCI 한국어 단저자 논문 — Track 3

> **제목**: 이행률 기반 한국 적응정책의 글로벌 정합도 진단 — 다축 LLM 추출 프레임워크 적용 사례
> **저자**: 최희도(Heedo Choi) · 국민대학교 일반대학원 기후기술융합학과
> **상태**: 3-track publication strategy의 Track 3
> **목표 게재지**: 한국정책학회보 (Korean Policy Studies Review) — KCI 우수등재
> **분량**: 25 pages 본문 + 5p 부록
> **제출 예상**: 2026년 7-8월

---

## 1. 본 venue 선택 이유

per `docs/research/PUBLICATION_STRATEGY.md` Track 3:
- **단저자 가능**: 영문 저널은 단저자 학생 게재 어려움, 한국어 KCI는 가능
- **외교부 재인용 잠재력**: 한국 적응정책 연구로 직접 활용 가능
- **방법론 + 정책 진단 + 권고**의 3가지를 모두 다루는 KCI 양식 부합
- 60% 게재 확률 (지도교수 공동저자 시 75%로 증가)

---

## 2. 차별화 포인트 vs Track 1 (영문 arXiv)

영문 arXiv가 **방법론 + COP30 일반 적용**이라면, 본 KCI 논문은:
- **다른 데이터**: 한국 NAP × GGA 30-cell crosswalk (영문 paper에 없는 새 데이터)
- **다른 framing**: 정책 정합도 + 정책수단 calibration 이론 적용
- **한국 정책 권고**: COP31 협상을 위한 5개 구체적 권고
- **한국학자 인용 가능 형식**: KCI 양식 + 한국어 우선

따라서 substantively different하므로 dual-submission 윤리적 문제 없음.

---

## 3. 파일 구성

```
paper/kci_korean/
├── manuscript.md              # 25-page 본문 (markdown)
├── fig1_country_issue_heatmap.png    # 30-cell IRR heatmap base
├── fig7_translation_gap_brazil.png   # 정책수단 calibration 예시
├── fig9_cross_llm_alpha.png          # Cross-LLM 신뢰도
├── fig11_stance_timeseries.png       # COP26-COP30 추이
└── README.md                  # this file
```

---

## 4. 한글 .docx 변환

KCI 제출은 .docx 또는 .hwp 형식이 표준. markdown → docx 변환:

```bash
pandoc paper/kci_korean/manuscript.md \
  -o paper/kci_korean/manuscript.docx \
  --reference-doc=docs/templates/kci_template.docx \
  --citeproc \
  --bibliography=paper/arxiv/references.bib \
  --csl=docs/templates/kci_apa.csl
```

(템플릿 파일은 한국정책학회 홈페이지에서 다운로드)

또는 hwp 변환:
- 한글 2024 또는 LibreOffice + .hwp filter 사용
- 한국정책학회 KCI 양식: 신명조 11pt, 1.6 줄간격, A4 여백 30/25/30/25mm

---

## 5. KCI 제출 체크리스트

### Pre-submission

- [ ] 지도교수와 공동저자 여부 결정 (단저자 vs 1저자/교신저자)
- [ ] 영문 초록(200 words) 검토 (영문 native speaker proofreading 권장)
- [ ] 한국정책학회 회원 가입 (회비: 학생 5만원/년)
- [ ] KCI 학술지 정보(https://www.kips.or.kr) 확인 — 투고 일정 확인
- [ ] References APA 7판 한국어 변형 형식 검증
- [ ] Plagiarism check (KCI는 turnitin 또는 카피킬러 결과 첨부 요구)
- [ ] 표·그림 캡션 한국어 + 영문 병기

### Submission

- [ ] 한국정책학회 온라인 투고 시스템 (https://kips.or.kr/sms)
- [ ] 투고비: 5만원 (학생 회원), 게재료: 별도 기준
- [ ] Cover letter: 한국 정책학적 contribution 강조
- [ ] 권장 심사위원 3인 명단 (KCI는 2-3인 심사 + 편집위원장 결정)

### After acceptance

- [ ] 한국정책학회보 issue에 게재 (semi-annual: 6월 / 12월)
- [ ] arXiv preprint 본문에 KCI 게재 정보 추가
- [ ] CINA GitHub README에 한국어 paper 링크 추가
- [ ] 외교부 기후환경과학외교국에 본문 사본 송부 (optional, courtesy)

---

## 6. 한국어 문체 점검사항

논문체 한자어 위주, 평어체 사용. 점검 항목:
- "~할 것이다" → "~한다" / "~할 수 있다"
- "본 연구는 ~을 주장하고자 한다" → "본 연구는 ~을 주장한다"
- "~라고 사료된다" → "~라고 판단된다" / "~로 평가된다"
- 영-한 코드스위칭 금지 — "implementation readiness" → "이행률(IRR)"
- 첫 등장 시에만 영문 병기, 이후 한자/한글
- 출처 표기: (Hood, 1983) → KCI 양식은 (Hood 1983) 띄어쓰기 없음

---

## 7. 변경 이력

- v1.0 (2026-05-07): Initial draft, 25 pages, 4 figures, 25+ references.

---

**최희도(Heedo Choi)** · zxsa0716@kookmin.ac.kr · 국민대학교 일반대학원 기후기술융합학과
