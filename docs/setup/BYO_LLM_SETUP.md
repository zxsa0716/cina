# 🔑 BYO LLM Key Setup — Ask CINA Program 자연어 답변 활성화

> **위치**: `docs/web/cina_program.html` (배포: https://zxsa0716.github.io/cina/web/cina_program.html)
> **모드**: rule-based (기본, 즉시) ↔ **LLM (BYO key, 자연어 답변)** ⭐
> **저장**: 본인 브라우저 localStorage에만 저장. CINA 서버로 전송되지 않습니다.

---

## 1. 왜 BYO key인가

CINA Program에는 두 가지 답변 모드가 있다.

| 모드 | 특징 | 비용 | 답변 품질 |
|------|------|------|---------|
| 🧮 **Rule-based** (기본) | 사전 정의된 매칭 + 템플릿 | 무료 / 즉시 | 정확한 사실 + 정형화된 표 |
| 🤖 **LLM (BYO key)** | 사용자 본인 API 키로 LLM 호출 | 본인 부담 (무료 tier 가능) | 자연어 흐름 + 맥락 이해 |

LLM 모드는 사용자가 자기 API 키를 입력해야 작동한다. 이는 다음을 의미한다:
- ✅ CINA가 사용자 데이터를 저장하지 않음 (키는 브라우저에만)
- ✅ CINA 운영 비용 0
- ✅ 사용자가 모델 선택 가능
- ⚠️ 키 노출 위험은 사용자 본인 책임

---

## 2. 지원 LLM provider 3종

| Provider | 모델 | 무료 가능? | 키 발급 |
|----------|------|----------|---------|
| **Gemini** ⭐ | gemini-2.5-flash-lite | 무료 1,000 req/day | https://aistudio.google.com/apikey |
| **Anthropic** | claude-sonnet-4-5 | 유료 (5달러 free credit 이후) | https://console.anthropic.com/settings/keys |
| **Groq** | llama-3.3-70b-versatile | 무료 (rate-limited) | https://console.groq.com/keys |

권장 시작점: **Gemini** (무료 + 빠른 발급)

---

## 3. 단계별 사용법 (3분)

### 1️⃣ Gemini API 키 발급 (1분)

1. **https://aistudio.google.com/apikey** 접속 (Google 계정 로그인)
2. **"Create API key"** 클릭
3. 프로젝트 선택 또는 새로 생성 → key 복사 (`AIzaSy...`로 시작, 약 39자)

> 💡 무료 tier: 1,000 requests/day, 분당 15 requests, 모델 컨텍스트 1M tokens. CINA Q&A 수십 건은 충분.

### 2️⃣ CINA Program에 키 입력 (30초)

1. **https://zxsa0716.github.io/cina/web/cina_program.html** 열기
2. 입력란 옆 **🔑 API Key** 버튼 클릭 → 모달 열림
3. **Gemini 2.5 Flash-Lite** 행에 복사한 키 붙여넣기 → **저장**
4. 상태 표시가 ✅ 저장됨으로 변경되면 완료

### 3️⃣ LLM 모드 활성화 (10초)

1. 입력란 위 모드 토글에서 **🤖 LLM (BYO key)** 클릭
2. provider 선택 prompt가 뜨면 **gemini** 입력
3. 이제 모드 badge가 🟢 **LLM 사용 가능: gemini**로 변경됨

### 4️⃣ 자연어 질문 (15초)

```
예시 질문:
- "브라질이 COP30에서 GGA 지표를 어떻게 통제했는지 단계별로 설명해 줘"
- "한국이 손실·피해 영역에서 약점인데, EIG 회원국으로서 가장 외교적으로 우아한 해결책은?"
- "AILAC 8개국이 norm entrepreneur 위치를 강화하려면 어떤 협력이 필요한가?"
```

이러한 질문은 rule-based 모드에서는 정형 답변만 가능하지만, LLM 모드에서는 **CINA 데이터베이스 조회 결과를 grounding으로 사용**하면서 자연스러운 단락 답변을 생성한다.

---

## 4. 답변 구조 (LLM 모드)

LLM 모드에서 모든 답변은 다음을 포함한다:

```
[자연어 답변 본문]
- CINA 데이터베이스 조회 결과만을 사실 근거로 사용
- "데이터에 명시되지 않음" 정직 표시
- stance score 부호 + 소수점 2자리 (예: +0.65)

📎 인용 N건
- 각 인용은 (국가, 이슈, COP, stance score, evidence quote)
- LLM에 제공된 동일한 lookup 결과에서 추출

신뢰도 / 매칭 records / intent / source 메타데이터
```

LLM은 CINA 데이터에 없는 사실은 추측하지 않도록 prompt 되어 있다 (할루시네이션 방지).

---

## 5. 프라이버시 및 보안

### CINA가 절대 하지 않는 것
- ❌ 사용자 API 키를 CINA 서버로 전송
- ❌ 키를 백엔드 데이터베이스에 저장
- ❌ 사용자 질문/답변을 추적하거나 로깅

### CINA가 하는 것
- ✅ 키를 브라우저 `localStorage`에만 저장 (`cina_byo_key_*`)
- ✅ LLM API 호출은 사용자 브라우저에서 직접 provider로
- ✅ "🔑 API Key" 모달에서 언제든 키 제거 가능

### 권장 보안 조치
- 공용 PC에서는 키 입력 후 사용 끝나면 **즉시 제거**
- 키가 의심스러우면 즉시 provider 콘솔에서 **rotate** (새 키 발급 + 기존 키 폐기)
- Production 환경에서는 별도 무료 키를 발급받아 limited scope로 사용

---

## 6. 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| "API key not set" 에러 | 키 미저장 | 🔑 API Key 모달에서 저장 |
| HTTP 401 / 403 | 키 무효 또는 만료 | provider 콘솔에서 키 재발급 |
| HTTP 429 (Too Many Requests) | rate limit 도달 | 1분 대기 후 재시도 또는 다른 provider 사용 |
| CORS error (Anthropic) | browser direct call 차단 | `anthropic-dangerous-direct-browser-access: true` 헤더 (이미 적용됨) |
| HTTP 500 / 503 | provider 서버 일시 장애 | 다른 provider로 자동 fallback 또는 잠시 후 재시도 |
| 응답이 비어있음 | content filter 트리거 | 질문 표현 변경 |

---

## 7. 예시 비교 (Rule-based vs LLM)

### 질문: "브라질이 COP30에서 GGA 지표 협상을 어떻게 주도했나?"

**Rule-based 모드 (기본)**:
```
Brazil (COP30)
  - GGA-IND: +0.95 (강한 지지) · frame=development 👑 의장 · 펜홀더

📎 인용 1건
- Brazil GGA-IND (COP30, 점수 +0.95):
  [COP30, Brazil] 59 voluntary, non-prescriptive, non-punitive,
  facilitative indicators across seven thematic targets

신뢰도 85% · 매칭 records 1 · intent: lookup · source: rule-based
```

**LLM 모드 (Gemini)**:
```
브라질은 COP30 의장국으로서 GGA 지표 협상을 주도하면서, 합의는
형식적으로 채택하되 운영적으로는 의무를 발생시키지 않는 정교한
텍스트 설계를 구현했습니다.

stance score +0.95(강한 지지)는 지표 채택 자체에 대한 지지를
나타내지만, 데이터베이스의 evidence quote는 "59 voluntary,
non-prescriptive, non-punitive, facilitative indicators"이라는
4중 헷지 어휘 배치를 보여줍니다. 이는 자발적 성격을 한 차례
명시한 것이 아니라 네 차례 반복한 결과로, 의장국 권한을 활용한
formula control의 텍스트 수준 evidence입니다.

브라질은 chair_role + pen_holder 신호를 모두 보유하여 결정문
작성권을 행사한 것으로 데이터에 기록되어 있습니다.

📎 인용 1건 (LLM에 제공된 동일 데이터)
- Brazil GGA-IND (COP30, 점수 +0.95): ...

신뢰도 92% · 매칭 records 1 · intent: lookup · source: GEMINI (BYO key)
```

LLM 모드는 **데이터의 의미를 자연스럽게 풀어주는** 효과가 있다.

---

## 8. 비용 추정 (대략)

### Gemini 2.5 Flash-Lite (free tier)
- 1 query ≈ 800 input tokens + 400 output tokens
- 무료 quota: 1,000 RPD = 하루 1,000 query
- **일반 사용자에게는 사실상 무료**

### Anthropic Claude Sonnet 4.5
- 1 query ≈ $0.003 (input + output 합산)
- $5 free credit = 약 1,600 query
- 무료 credit 소진 후 본인 부담

### Groq Llama 3.3 70B
- 무료 (rate-limited): 분당 30 req, 일당 14,400 req
- **fastest response time** (대부분 1초 이내)

권장: **Gemini for daily use, Groq for fast batch**

---

## 9. CLI 모드 (advanced)

브라우저 없이 Python CLI로 동일한 Q&A:

```bash
# Rule-based (즉시, 무료)
python -m src.program.query_engine --demo
python -m src.program.query_engine "브라질과 한국의 GGA 지표 입장 차이는?"

# LLM 모드는 향후 src/program/query_engine.py에 추가 예정
# 현재는 src/stage1_extract/llm_smoke_test.py로 provider 연결 확인 가능:
export GEMINI_API_KEY=AIzaSy...
python -m src.stage1_extract.llm_smoke_test --providers gemini
```

---

**작성**: 2026-05-05 · Heedo Choi (최희도) · zxsa0716@kookmin.ac.kr
**관련**: [`cina_program.html`](../web/cina_program.html) · [`assets/cina_program.js`](../web/assets/cina_program.js)
