# 무료 LLM 백엔드 완벽 설정 가이드 (Anthropic 대체)

> Heedo 지시: "Anthropic은 너무 비싸. 무료 API/데이터로 전환."
>
> **답**: CINA Stage 1을 4가지 무료 backend 중 선택 가능 (Gemini / Groq / Ollama / OpenRouter).
> 추천 순위 (작업량과 한국어 품질 기준):
>
> 1. **Gemini 2.5 Flash-Lite** ⭐ — 1000 RPD 무료, JSON 강함, 한국어 OK
> 2. **Groq Llama 3.3 70B** — 30 RPM 무료, 초고속
> 3. **Ollama Qwen 2.5 (local)** — 완전 무료, 오프라인, 16GB RAM 권장
> 4. **OpenRouter free pool** — DeepSeek/Llama free models

---

## 0. 즉시 결정 매트릭스

| 시나리오 | 추천 |
|---------|------|
| 가장 쉽게 시작 (5분 설정) | **Gemini Flash-Lite** |
| 가장 빠른 응답 (실시간 demo) | **Groq Llama 3.3 70B** |
| 외부 통신 차단 / 보안 / 무한 사용 | **Ollama 로컬** |
| 다양한 모델 실험 | **OpenRouter free pool** |
| 비용 무관, 최고 품질 | Anthropic Claude Haiku 4 (~$0.50/run) |

---

## 1. 옵션 A: Gemini 2.5 Flash-Lite (추천 ⭐)

### 1.1 무료 한도 (2026 기준)
- **15 RPM** (Requests Per Minute)
- **1,000 RPD** (Requests Per Day) — CINA Stage 1 150 calls 충분
- **250,000 TPM** (Tokens Per Minute)
- **1M context window**
- 한국어/포어/영어 모두 OK
- JSON structured output 지원

### 1.2 5분 설정

1. **API key 발급** (3분):
   - 브라우저: https://aistudio.google.com/apikey
   - Google 계정 로그인 (학교 zxsa0716@kookmin.ac.kr 권장)
   - "Create API Key" 클릭 → key 복사 (예: `AIzaSyXXX...`)
   - **무료, 결제 정보 불필요**

2. **PowerShell에 영구 설정** (1분):
   ```powershell
   [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AIzaSyXXX...", "User")
   [Environment]::SetEnvironmentVariable("CINA_LLM_PROVIDER", "gemini", "User")
   ```

3. **PowerShell 새로 열기 + 검증** (1분):
   ```powershell
   echo $env:GEMINI_API_KEY    # AIza... 출력 확인
   pip install google-generativeai
   ```

4. **Stage 1 실행 테스트**:
   ```powershell
   cd C:\Users\admin\Desktop\대학원수업\1학기\리더쉽
   python -c "from src.stage1_extract.providers import get_provider; p = get_provider('gemini'); print(p.complete('You are CINA test.', 'Say OK in JSON: {\"status\":\"ok\"}', {'type':'object'}).content)"
   ```

   기대 출력: `{"status":"ok"}` 또는 유사.

### 1.3 비용
- **$0** (free tier 안에서)
- CINA Stage 1 (150 calls × ~2.5K tokens) = 375K tokens
- 무료 1M tokens/day 한도 안에 충족

### 1.4 한계
- 12월 2025에 Google이 free tier 50-80% 축소함. 향후 변동 가능.
- 가용성 SLA 없음 (간헐적 429 에러 가능 → 자동 retry로 처리)

---

## 2. 옵션 B: Groq Llama 3.3 70B (초고속)

### 2.1 무료 한도
- **30 RPM**
- **6,000 TPM** (Tokens Per Minute)
- **1,000 RPD** (Requests Per Day)
- 280+ tok/sec inference (지구상 가장 빠름)
- JSON mode 지원
- 한국어/포어/영어 OK

### 2.2 5분 설정

1. https://console.groq.com/keys 접속 → 회원가입
2. "Create API Key" → 복사 (예: `gsk_XXX...`)
3. PowerShell:
   ```powershell
   [Environment]::SetEnvironmentVariable("GROQ_API_KEY", "gsk_...", "User")
   [Environment]::SetEnvironmentVariable("CINA_LLM_PROVIDER", "groq", "User")
   pip install groq
   ```

### 2.3 비용
- $0 free tier (개발 충분)
- 한도 초과 시 development 단가 (가격은 console에서 확인)

### 2.4 한계
- TPM 6K가 빡빡 — 큰 문서 처리 시 분할 필요
- Production SLA 없음

---

## 3. 옵션 C: Ollama 로컬 LLM (완전 무료, 무제한)

### 3.1 장점
- **$0 영구**
- 무제한 사용
- 오프라인 작동
- 데이터 프라이버시 100%

### 3.2 시스템 요구
- **Qwen 2.5 7B** (4.4 GB): 8 GB RAM 노트북 OK (느림), 16 GB 빠름
- **Qwen 2.5 14B** (9 GB): 16 GB RAM 권장
- M1/M2/M3 Mac 또는 GPU 있으면 빠름

### 3.3 설치 (10분, 1회만)

1. https://ollama.com/download 에서 Windows installer 다운로드
2. 설치 (자동 실행 background service)
3. PowerShell:
   ```powershell
   ollama pull qwen2.5:7b-instruct      # 4.4 GB, 추천
   ollama list                           # 설치 확인
   ```

4. CINA 설정:
   ```powershell
   [Environment]::SetEnvironmentVariable("CINA_LLM_PROVIDER", "ollama", "User")
   [Environment]::SetEnvironmentVariable("OLLAMA_MODEL", "qwen2.5:7b-instruct", "User")
   pip install ollama
   ```

5. 검증:
   ```powershell
   python -c "from src.stage1_extract.providers import get_provider; p = get_provider('ollama'); print(p.complete('You are CINA test.', 'Say OK in JSON.', {}).content)"
   ```

### 3.4 한계
- 노트북 사양에 따라 느림 (CPU only는 1 추출에 30-60초)
- 7B는 14B/Claude/Gemini 대비 품질 미세하게 낮음 (calibration 권장)

---

## 4. 옵션 D: OpenRouter free pool (다양한 모델)

OpenRouter는 100+ LLM provider를 통합. Free pool 포함.

### 4.1 가용 free 모델
- `meta-llama/llama-3.3-70b-instruct:free`
- `google/gemini-2.0-flash-exp:free`
- `deepseek/deepseek-chat-v3.1:free`
- `qwen/qwen-2.5-72b-instruct:free`

### 4.2 설정
```powershell
# https://openrouter.ai/keys 회원가입 + API key 생성
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-...", "User")
[Environment]::SetEnvironmentVariable("CINA_LLM_PROVIDER", "openrouter", "User")
[Environment]::SetEnvironmentVariable("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free", "User")
pip install openai
```

### 4.3 한계
- Free pool 가용성 변동 (혼잡 시 거부)
- Rate limit가 변동적

---

## 5. CINA 권장 운영 시나리오

### 시나리오 1: 가장 무료 + 안정 (권장)
```
1순위: Gemini 2.5 Flash-Lite        (default)
2순위: Groq Llama 3.3 70B            (Gemini 거부 시 fallback)
3순위: Ollama Qwen 2.5 7B local      (외부 거부 시 zero-cost local)
```

CINA 코드 (자동 fallback chain):
```python
from src.stage1_extract.providers import get_provider
for backend in ['gemini', 'groq', 'ollama']:
    try:
        provider = get_provider(backend)
        # 시도
        break
    except RuntimeError:
        continue
```

### 시나리오 2: 학술 발표용 최고 품질
- Anthropic Claude Sonnet 4 (~$3-5)
- 또는 Gemini 2.5 Pro (Tier 1 paid, $0.10-0.30/run)

---

## 6. CINA Stage 1 실행 (provider 선택 후)

### 6.1 시드 5건 추출 (~10분, $0)
```powershell
cd C:\Users\admin\Desktop\대학원수업\1학기\리더쉽
python -m src.pipeline --country Brazil --cop 30 --sector adaptation --language ko --raw-dir data/raw/unfccc_submissions/cop30_curated --output deliverables/ --stages 1
```

### 6.2 전체 corpus 추출 (~1시간, $0)
```powershell
python -m src.pipeline --country Brazil --cop 30 --sector adaptation --raw-dir data/raw --output deliverables/ --stages 1
```

---

## 7. 비교 표 (한눈에)

| Provider | 비용 | 속도 | 품질 | 한국어 | JSON | RPD | 추천 |
|----------|-----|-----|-----|-------|------|-----|------|
| **Gemini 2.5 Flash-Lite** | **$0** | 빠름 | A | ✅ | ✅ | 1000 | ⭐⭐⭐⭐⭐ |
| **Groq Llama 3.3 70B** | **$0** | 매우 빠름 | A | ✅ | ✅ | 1000 | ⭐⭐⭐⭐ |
| **Ollama Qwen 2.5 7B** | **$0** | 느림 (CPU) | B+ | ✅ | ✅ | ∞ | ⭐⭐⭐⭐ (privacy) |
| **OpenRouter free** | **$0** | 변동 | A | ✅ | ✅ | 변동 | ⭐⭐⭐ |
| Anthropic Sonnet 4 | $3-5 | 빠름 | A+ | ✅ | ✅ | ∞ | ⭐⭐⭐ (cost) |

---

## 8. 트러블슈팅 FAQ

### Q1. Gemini 429 "Too Many Requests"
- Free tier RPD 한도 (1000) 도달. 다음날 reset.
- 또는 `time.sleep(4)` retry로 처리 (자동 구현됨).

### Q2. Ollama "model not found"
- `ollama pull qwen2.5:7b-instruct` 다시 실행.
- `ollama list` 로 설치 확인.

### Q3. Groq TPM 6K 초과
- 큰 문서를 여러 호출로 분할. CINA `aggregate_samples`가 자동 처리.

### Q4. Provider switch
- 환경변수만 변경 + PowerShell 재시작:
  ```powershell
  [Environment]::SetEnvironmentVariable("CINA_LLM_PROVIDER", "ollama", "User")
  ```

### Q5. 모든 backend 실패
- Anthropic Haiku 4 fallback (~$0.50/run, 매우 저렴):
  ```powershell
  [Environment]::SetEnvironmentVariable("CINA_LLM_PROVIDER", "anthropic", "User")
  [Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
  ```

---

## 9. 자율 fallback chain (CINA 자동 처리)

CINA `extract_stance_v2`는 다음 순서로 자동 시도:
1. `CINA_LLM_PROVIDER` env 값 (default: `gemini`)
2. 실패 시 `groq` 시도
3. 실패 시 `ollama` 시도
4. 실패 시 `anthropic` 시도 (paid fallback)
5. 모두 실패 시 placeholder + warning

---

## 10. 한 줄 결론

**Gemini API key 발급 (5분, $0) → CINA 100% 도달**.

Heedo가 해야 할 단 한 가지:
```
https://aistudio.google.com/apikey 에서 key 받기
```

그 후:
```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AIza...", "User")
```

PowerShell 재시작 → 자동으로 모든 단계 진행.

---

**작성**: 2026-04-29
**버전**: v1 (Anthropic → Free LLM pivot)
**다음 갱신**: Stage 1 실행 후 실측 비용 + 속도 보고
