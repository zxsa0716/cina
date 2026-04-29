# 06. Stage 3 — Graph-Grounded Briefing Generation

> Stage 3의 목표: Stage 2 분석 결과를 장관급 전략 브리핑 문서로 변환. 모든 주장은 (텍스트 인용 + 구조적 근거) 쌍으로 grounding.

## 1. 설계 원칙

### 1.1 Graph-Grounded Generation (GGG)
이 프로젝트의 **방법론적 신규성 핵심**. 일반 RAG는 텍스트 인용으로 할루시네이션을 줄이지만, 전략적 주장("X가 핵심 중재국이다")은 텍스트에 명시되지 않는다. GGG는 생성 시:
- **Factual claims** → 반드시 evidence_quote 인용
- **Structural claims** → 반드시 network metric 인용
- **Strategic claims** → 반드시 (evidence + structure) 쌍

### 1.2 Non-hallucination 제약
- 모든 생성 문장을 post-hoc verifier가 검사. 인용 누락 시 재생성 또는 제거.
- 수치(예: "3개국이 반대", "38%의 support")는 Stage 1/2 출력에서 직접 조회한 값만 허용.

### 1.3 어조와 포맷
- 장관급 보고: 간결, 직설, 전문용어 정제.
- 권고는 **actionable verb**로 시작 ("우선 접촉하라", "양보 검토하라", "red line 유지하라").
- 불확실성 명시: credible interval을 자연어로 풀어씀 ("78–85% 신뢰 수준").

---

## 2. 브리핑 템플릿 (고정 구조)

```markdown
# 브리핑: [장관직] — [COP 세션] [섹터] 협상 전략

**기밀분류**: 수업 제출용 (공개 소스만 사용)  
**작성**: CINA Framework v2.0, [날짜]  
**대상**: [장관/기후대사 직책]  
**주제**: [Sector]  
**세션**: [COP session, 장소, 기간]

---

## 경영진 요약 (Executive Summary, 1 page)
[3~5 bullet, 각 bullet은 §2~§6의 핵심]

---

## §1. 현황 평가 (Situation Assessment)
### 1.1 의제 지형
[6개 하위 이슈별 현재 국제 협상 상태]

### 1.2 [자국] 공식 입장 요약
[Stage 1 출력에서 자국 스탠스 벡터]

### 1.3 주요 변화 요인
[최근 6개월 내 이슈별 모멘텀 변화]

---

## §2. 연합 지형 (Coalition Map)
### 2.1 이슈별 연합 구조
[Stage 2 community detection, 각 이슈별 최대 4개 블록]

### 2.2 공식 그룹 vs 실질 연합
[G77, EU 같은 공식 그룹이 실제 이슈별 클러스터와 얼마나 일치/불일치하는지]

### 2.3 시간에 따른 연합 재편
[Stage 2의 temporal snapshot 비교]

---

## §3. 레버리지 분석 (Leverage Analysis)
### 3.1 브릿지 국가 (Bridge Actors)
[betweenness centrality 상위, 양쪽 블록 연결 가능성]

### 3.2 영향력 허브 (Hubs)
[eigenvector + attention centrality 상위]

### 3.3 [자국]의 구조적 위치
[자국이 어떤 다리를 놓을 수 있는지]

---

## §4. 패키지 딜 기회 (Package Deal Opportunities)
[Cross-issue hypergraph에서 도출된 묶음 제안, 예상 파트너, 교환 조건]

---

## §5. Red Lines와 위험 (Red Lines and Risks)
### 5.1 합의 실패 가능성이 높은 이슈
[epistemic divergence score 높은 이슈들]

### 5.2 예상 반대 블록
[Stage 2 opposing cluster]

### 5.3 [자국] red line과 상충 지점
[자국 red_lines와 다른 국가 key_demands의 교집합]

---

## §6. 권고 전략 자세 (Recommended Strategic Posture)

### 6.1 우선 순위 (Priority Matrix)
| 이슈 | 자국 중요도 | 합의 난이도 | 권고 자세 |
|------|-------------|-------------|-----------|
| ... | ... | ... | 주도 / 참여 / 관망 |

### 6.2 접촉 시퀀스 (Engagement Sequence)
1. [1주차] ...국과 양자 회담
2. [2주차] ...그룹과 조율
...

### 6.3 양보 가능 영역
[red line 이 아닌, flexibility signal 공유하는 이슈]

### 6.4 반드시 유지할 영역
[자국 red_lines, 선거/국내정치 고려]

---

## §7. 시나리오 분석 (Scenario Analysis)
### 7.1 최선 시나리오
[핵심 브릿지 국가 설득 성공 시]

### 7.2 기본 시나리오
[현재 궤적]

### 7.3 최악 시나리오
[epistemic divergence 현실화 시]

---

## Appendix A — 주장-근거 추적 테이블 (Evidence Traceability)

| Claim ID | 문장 | Evidence Quote | Source Doc | Structural Fact | Confidence |
|----------|------|----------------|-----------|-----------------|------------|
| C001 | ... | "..." | ... | betweenness=0.34 | 0.87 |

## Appendix B — 데이터 계보 (Data Lineage)
- 문서 수: [N]
- 스탠스 추출 수: [M]
- LLM 호출: [K] (model, temperature, prompt_version)
- GNN 학습 설정: [...]

## Appendix C — 불확실성 및 한계
[회고적 검증에서 드러난 오차 경향, expert eval 점수, 한계]
```

---

## 3. 생성 프로토콜

### 3.1 섹션별 분리 생성
전체 브리핑을 한 번에 생성하지 않고 섹션별로 독립 생성. 각 섹션 프롬프트:

```text
[SYSTEM]
You are drafting a ministerial briefing for [country]'s [minister title].
You are writing Section {section_id}: {section_title}.

Available structured analysis:
{analysis_json_relevant_to_this_section}

Available evidence quotes (only cite from this list):
{evidence_quotes_list}

Constraints:
1. Every factual claim must cite at least one evidence_quote by source_doc_id.
2. Every structural claim (coalition, centrality, linkage) must cite the analysis JSON field.
3. Format: concise, official report tone in Korean.
4. Maximum length: {max_words} words.
5. Do not invent numbers. Copy directly from provided data.

Output the section in Markdown.
```

### 3.2 Post-Generation Verification

```python
def verify_briefing_claims(section_text, evidence_base, analysis_json):
    """
    Parse section_text. For each sentence:
      - If contains numeric claim → regex match against analysis_json / evidence_base
      - If contains country X assertion → check evidence list mentions X
      - Return list of unverified claims.
    """
    unverified = []
    for sent in split_sentences(section_text):
        if is_claim(sent):
            citations = extract_citations(sent)
            if not any(verify(cite, evidence_base, analysis_json) for cite in citations):
                unverified.append(sent)
    return unverified
```

검증 실패 시 3회 regenerate. 여전히 실패하는 claim은 경고와 함께 자동 제거.

### 3.3 Executive Summary 생성
모든 §1~§7 섹션 생성 후, 마지막 단계에서 Executive Summary 생성:
- 입력: 각 섹션의 첫 단락 + 권고 섹션의 bullet
- 출력: 5개 bullet, 각 30단어 이내

---

## 4. 언어 스타일 가이드

### 4.1 추천 어휘
- "협상 지형" (landscape) > "상황"
- "구조적 레버리지" > "영향력"
- "연합 재편 가능성" > "편들이 바뀔 수"
- "교환 가능한 양보" > "타협"

### 4.2 피할 어휘
- 감정 표현 ("우려스럽다", "다행히")
- 과도한 확신 ("반드시", "명백히") — 불확실성 수준에 맞춰 사용
- 수사적 질문 ("과연 ~할 수 있을까?")

### 4.3 숫자 표현
- 원 스탠스 점수 → 자연어: "0.78 (강한 지지)"
- Credible interval → "신뢰구간 [0.42, 0.74], 불확실성 중등"
- Coalition size → "이 블록은 N개국으로 구성"

---

## 5. Evidence Traceability Table 자동 생성

섹션 생성 완료 후, 모든 인용을 수집하여 Appendix A 테이블을 자동 빌드:

```python
def build_evidence_table(all_sections: dict[str, str], citations_log: list) -> pd.DataFrame:
    rows = []
    for cid, cite in enumerate(citations_log):
        rows.append({
            "Claim ID": f"C{cid:03d}",
            "Sentence": cite["sentence"],
            "Evidence Quote": cite["evidence_quote"][:200],
            "Source Doc": cite["source_doc_id"],
            "Structural Fact": cite.get("structural_fact", "-"),
            "Confidence": cite["confidence"],
        })
    return pd.DataFrame(rows)
```

이 테이블이 **reviewer가 CINA의 주장을 검증할 수 있는 핵심 산출물**이다.

---

## 6. 다국어 출력
논문용은 영어, 수업 제출용은 한국어. 프롬프트의 `language` 변수만 바꾸면 동일 분석에서 두 버전 생성 가능.

---

## 7. 예시 문단 (자동생성 예상 출력)

> §3. 레버리지 분석
> 
> 남아프리카공화국은 GGA 지표 이슈에서 가장 높은 구조적 중재 가능성을 보유한다 (betweenness centrality = 0.34, BASIC과 African Group을 가교하는 위치). 실제 남아공의 SBI 2025 제출문은 "indicators must respect differentiated capacity" (UNFCCC/SBI/2025/INF.2, para 8) 를 강조하면서도 "we welcome the expert-proposed framework as a starting basis" (ibid. para 11) 라는 이중 신호를 보낸다. 이는 Two-Level Games 관점에서 win-set 확장의 여지를 시사한다. **권고**: 남아공 협상팀장과 1주차 양자 회담을 통해 "역량 맥락 조항" 추가 시 EU·AOSIS와의 다리 역할을 요청.

각 주장이 (정량 네트워크 지표 + 인용문 + 이론적 언어)로 뒷받침되는 것이 Graph-Grounded Generation의 특징.

---

## 다음 문서
- [07_evaluation_protocol.md](07_evaluation_protocol.md)
