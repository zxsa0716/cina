---
assigned_to: data-refinement-analyst
model: sonnet
round: 2
priority: P0
issued_at: 2026-04-25
deadline: round_2_close (after T01 collector completes)
depends_on:
  - council_sessions/round_2/data_collection/REPORT.md (T01 output)
  - council_sessions/round_1/synthesis/cross_review.md
related_critiques:
  - council_sessions/round_1/policy_science/critique.md (C2 NATO 4-axis instrument_signals)
  - council_sessions/round_1/ir_political/critique.md (C2 frame_type, C3 salience asymmetry, C1 chair_status)
---

# T02 (Round 2) — Schema v1.3 Refinement (Instrument + Frame + Salience + Chair)

## 1. 목적
Round 1 v1.2 Stage 1 추출 스키마를 두 교수의 권고를 통합한 **v1.3**로 확장하고, Round 2 collector(T01)가 가져온 70-100건 raw → CINA Document Schema로 정제한다. 신규 변수 3종(instrument_signals, frame_type, salience_score) + chair-status 자동 인식 로직을 구현한다.

## 2. 컨텍스트 (cross_review §4 CR1, CR2)

두 교수가 제기한 핵심 비판:
- **Policy-Sci C2**: 정책 수단 균형 부재. Hood NATO 프레임(Nodality·Authority·Treasure·Organization)을 추출 단계에 도입.
- **IR C2**: 자유주의 일변도. Constructivist frame_type을 추가 코딩.
- **IR C3**: Issue linkage가 형식적 구현. salience_score로 Sebenius 비대칭 salience 측정 가능.
- **IR C1 (P0)**: 의장국 procedural power가 country_features에 부재. chair_status 자동 추출 로직 필요.

## 3. P0 산출물

### 3.1 Stage 1 Prompt v1.3 명세

**기존 v1.2 필드 (유지)**:
```yaml
- country_id: str
- issue_id: str
- session_id: str
- stance_score: float [-1, 1]
- key_demands: list[str]
- red_lines: list[str]
- flexibility_signals: list[str]
- coalition_alignment: list[group_id]
- evidence_quotes: list[{quote, paragraph_id}]
```

**v1.3 신규 필드**:
```yaml
- instrument_signals:               # Policy-Sci C2 (Hood NATO)
    nodality:        {score: float [0,1], evidence: str|null}  # 정보·지표 수단
    authority:       {score: float [0,1], evidence: str|null}  # 규제·권한 수단
    treasure:        {score: float [0,1], evidence: str|null}  # 재정·재원 수단
    organization:    {score: float [0,1], evidence: str|null}  # 제도·기구 수단
- frame_type:                        # IR C2 (Constructivist)
    primary: enum {scientific, justice, sovereignty, security, development, none}
    secondary: enum (same) | null
    evidence: str
- salience_score: float [0,1]        # IR C3 (Sebenius linkage)
- procedural_signals:                # IR C1 chair power (신규 보조 필드)
    is_chair_speaking: bool
    pen_holder_signal: bool          # 텍스트 초안 제안권 행사
    procedural_phrases: list[str]    # "Parties may wish to consider", "the chair proposes"
```

### 3.2 Chair-Status 자동 인식 로직

문서 메타에서 chair·co-facilitator·pen-holder 식별:
- [ ] 문서 source가 `unfccc.int/.../presidency/...` 또는 filename pattern `*L.<n>*` (L-document = 의장 텍스트 초안) 인 경우 `is_pen_holder_doc=True` 메타 추가
- [ ] 문서 발행자 메타에서 "COP30 Presidency", "Co-facilitator", "Chair" 키워드 자동 추출 → `chair_status` 추정
- [ ] 한국·EU 등 비-의장국 문서는 `chair_status=0` 기본값
- [ ] 결과를 `data/processed/chair_metadata.jsonl` 별도 파일로 저장 (Stage 2에서 country_features 생성 시 사용)

### 3.3 Round 2 corpus 정제

T01 collector가 완료되면:
- [ ] 70-100건 raw → CINA Document Schema 변환
- [ ] 단락 단위 정규화 (Round 1 754 단락 형식 따라)
- [ ] 6 적응 이슈(GGA-IND, ADAPT-FIN, L&D-OP, NAPs, MIT-ADAPT, JT-ADAPT) 키워드 매칭
- [ ] 20국·12그룹·6이슈 ID로 매핑
- [ ] 중복·결측·품질 점검 보고서 (`council_sessions/round_2/refinement/quality_report.md`)

### 3.4 Round 1 backfill (P1 → P0로 격상)
- [ ] Round 1 7건도 v1.3 스키마로 재처리. instrument_signals/frame_type/salience 추출. (overhead 적음, +cost ~$0.5)
- [ ] backfill 결과는 동일 corpus에 통합

### 3.5 두 교수 입력 패키지 v2 갱신

`council_sessions/round_2/refinement/professor_input/policy_sci_pack_v2.md`:
- [ ] §"Round 2 정제 결과 요약" — 신규 corpus 규모, NATO 4축 추출 통계
- [ ] §"정책 수단 분포 매트릭스" — 6 이슈 × 4 수단의 평균 score (Belém Package 패턴 식별)
- [ ] §"한국 부처 자료 분석" — 외교부·환경부 자료에서 추출한 정책 수단 분포
- [ ] §"Round 1 권고 반영 검증" — 정책학자가 Round 1에 제시한 C1/C2/C3 비판이 v1.3 스키마에 어떻게 반영되었는지

`council_sessions/round_2/refinement/professor_input/ir_pack_v2.md`:
- [ ] §"Round 2 정제 결과 요약" — frame_type 분포, salience asymmetry 통계
- [ ] §"Chair Power 자료 분석" — 의장 letter, L-document에서 추출한 chair_status / pen_holder 신호
- [ ] §"Realist baseline 데이터 준비 상태" — GDP/CO2/military/alliance 데이터 가용성
- [ ] §"Round 1 권고 반영 검증" — IR 교수의 C1/C2/C3 비판이 v1.3 스키마와 chair metadata에 어떻게 반영되었는지

## 4. P1 산출물

- [ ] `collector_feedback_v2.md` — Round 3 collector에 전달할 Round 2 새 gap (정제 과정에서 발견된 누락)
- [ ] Stage 1 prompt v1.3 텍스트 자체를 `prompts/stage1_v1.3.yaml`에 commit (재현성)
- [ ] Round 1 v1.2 → v1.3 변경점 변경로그 `prompts/CHANGELOG.md`

## 5. 품질 기준

### 5.1 추출 정확도 자체 평가
- [ ] 무작위 sampling 20개 (각 이슈별 3-4개) → 수동 검증 또는 LLM-as-judge로 v1.3 신규 필드 정확도 측정
- [ ] instrument_signals 4축의 evidence quote 100% (없으면 score=0)
- [ ] frame_type primary 분류 일관성 (같은 문서 다른 단락에서 동일 frame인가)

### 5.2 메타 표준 (유지)
- [ ] CINA Document Schema 100% 준수
- [ ] 모든 추출 결과에 source_id, paragraph_id, evidence_quote 동봉
- [ ] LLM 호출 메타: 모델, prompt_version=v1.3, temperature, seed, timestamp 기록

## 6. 비용 견적
- 70-100 docs × 평균 200 단락/doc × prompt v1.3 token = 추정 LLM 호출 비용 $15-25 (sonnet 기준)
- Round 1 7건 backfill +$1-2
- 총 ~$20-30

## 7. 산출물 위치
- 정제 데이터: `data/processed/documents.jsonl`, `data/processed/stances.jsonl` (각 stance triple)
- chair 메타: `data/processed/chair_metadata.jsonl`
- 두 교수 packs: `council_sessions/round_2/refinement/professor_input/{policy_sci,ir}_pack_v2.md`
- 품질 리포트: `council_sessions/round_2/refinement/quality_report.md`
- collector feedback: `council_sessions/round_2/refinement/collector_feedback_v2.md`
- prompts: `prompts/stage1_v1.3.yaml`, `prompts/CHANGELOG.md`

## 8. team-lead 에스컬레이션 트리거
- v1.3 추출 정확도가 무작위 sampling에서 70% 미달 시 escalate (prompt 개선 또는 calibration 필요)
- 한국 부처 자료가 5건 미만 정제 가능 시 escalate (수집·번역 추가 필요)

## 9. 본 task의 헌법 정합성
- ✓ 헌법 §1 논문감: NATO + frame + salience 추가가 reviewer-quality 강화
- ✓ 헌법 §2 COP30 회고: chair metadata가 Belém Rube Goldberg 사건의 인과변수 제공
- ✓ 헌법 §3 투트랙: instrument_signals가 Track A 한국 부처 정책 수단 분석에 직접 활용
- ✓ 헌법 §4 LLM-GNN-LLM: Stage 1 출력이 Stage 2 country_features 입력으로 직접 연결

**작업은 T01 collector 완료 후 시작.**
