# ANTHROPIC_API_KEY 설정 완벽 가이드 (Heedo 전용 단계별)

> Stage 1 LLM 실행에 필요한 단 1개 외부 의존성. 이 가이드 따라 5분 안에 설정 완료.

---

## 1단계: API key 발급 (~3분, 1회만)

### 1.1 Anthropic Console 접속
브라우저에서: **https://console.anthropic.com**

### 1.2 회원가입 / 로그인
- 이메일 + 비밀번호 또는 Google 로그인
- 학교 이메일 (zxsa0716@kookmin.ac.kr) 사용 권장

### 1.3 결제 수단 등록 ($5 최소 충전)
- 우측 상단 → Settings → Billing
- "Add Credit" 클릭
- **최소 $5 (약 7,000원)** 충전 (CINA Stage 1 시드 5건은 $5-8 예상, 전체 corpus는 $30-40)
- 신용카드 또는 PayPal

### 1.4 API key 생성
- Settings → **API Keys** → "Create Key"
- 이름: `cina-stage1` (자유)
- 생성된 key 복사 (예: `sk-ant-api03-xxxxxxx...`)
- **⚠️ 이 화면을 닫으면 다시 못 봄. 안전한 곳에 메모.**

---

## 2단계: 환경변수 설정 (PowerShell)

### 옵션 A: 현재 세션에만 적용 (간단, 매번 다시)

PowerShell 창에서 입력:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-xxxxxxx..."
```

검증:
```powershell
echo $env:ANTHROPIC_API_KEY
```
→ key 일부 출력되면 성공.

### 옵션 B: 영구 설정 (권장)

PowerShell 관리자 권한으로 열기 → 입력:
```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-api03-xxxxxxx...", "User")
```

PowerShell 닫고 새로 열어서 검증:
```powershell
echo $env:ANTHROPIC_API_KEY
```

### 옵션 C: Git 저장소 안전 사용 (.env 파일)

CINA 폴더에:
```bash
cd C:\Users\admin\Desktop\대학원수업\1학기\리더쉽
echo "ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxx..." > .env
```

`.gitignore` 에 `.env` 이미 포함되어 있어 git에 안 올라감 (이미 작성됨).

Python에서:
```python
from dotenv import load_dotenv
load_dotenv()
import os
key = os.environ["ANTHROPIC_API_KEY"]
```

`python-dotenv` 설치 필요: `pip install python-dotenv`

---

## 3단계: CINA Stage 1 실행 (Heedo 입력 후 자동)

### 3.1 5 시드 추출 (최저 비용 시작)
```powershell
cd C:\Users\admin\Desktop\대학원수업\1학기\리더쉽
python -m src.pipeline --country Brazil --cop 30 --sector adaptation --language ko --raw-dir data/raw/unfccc_submissions/cop30_curated --output deliverables/ --stages 1
```

예상:
- 소요: 10분
- 비용: $5-8
- 출력: `data/processed/stances.jsonl` (5 시드 × 6 이슈 = 30 records)

### 3.2 전체 corpus 추출 (Stage 1 본격)
```powershell
python -m src.pipeline --country Brazil --cop 30 --sector adaptation --raw-dir data/raw --output deliverables/ --stages 1
```

예상:
- 소요: 1시간
- 비용: $30-40
- 출력: 전체 corpus stance 추출

---

## 4단계: 확인 — 모든 게 자동 흘러감

API key 설정 + Stage 1 실행 후:

| 단계 | 자동 진행 | 예상 시간 |
|------|---------|---------|
| Stage 1 stances.jsonl | 자동 (Heedo 작업 0) | 10분 ~ 1시간 |
| Calibration set 50건 확장 | 자동 | 30분 |
| R5 Phase B (Opus reset 후) | 자동 | 30분 |
| R6 종결 평가 | 자동 | 30분 |
| Stage 2 GNN 학습 setup | (`pip install torch` 권고) | Heedo 결정 |
| Stage 2 GNN 학습 실행 | 자동 (torch 설치 후) | 1-2시간 (RTX 4090) |
| Stage 3 ministerial briefing 생성 | 자동 | 10분 ($2-5) |
| 최종 paper draft v1 | 자동 | (텍스트 생성만) |

**Heedo 추가 입력**: 0회 (Stage 2 torch 설치만 결정)

---

## 5단계: 비용 관리 (안심)

### 비용 한도 설정 (권장)
Anthropic Console → Settings → Billing → **Usage Limits**:
- Hard limit: $50 (이 이상 자동 차단)
- Soft warning: $20 (알림만)

### Round별 예상 비용 (R5 Phase B 후 누적)

| 단계 | 비용 |
|------|------|
| 현재까지 누적 (R0-R5 Phase A) | ~$48-55 (council agents) |
| Stage 1 시드 5건 | $5-8 |
| Stage 1 전체 corpus | $30-40 |
| R5 Phase B + R6 (council) | $5-10 |
| Stage 3 ministerial briefing | $2-5 |
| **CINA 전체 완성 누적** | **~$90-120** |

학회 발표 1편 + Track A + Track B 동시 산출 비용으로는 합리적 수준.

---

## 6단계: 트러블슈팅

### Q1. "Invalid API key" 에러
- key 복사 시 따옴표 포함 또는 공백 포함 가능. 다시 복사.
- key 형식: `sk-ant-api03-` 로 시작 + 64자 무작위 문자

### Q2. "Insufficient credits" 에러
- Console → Billing → Add Credit. $5+ 충전.

### Q3. PowerShell에서 환경변수 안 읽힘
```powershell
# 현재 세션 다시 설정
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."

# 또는 영구 설정 후 PowerShell 재시작
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
# PowerShell 닫고 새로 열기
```

### Q4. Python에서 환경변수 못 읽음
```python
import os
print(os.environ.get('ANTHROPIC_API_KEY', 'NOT SET'))
```
NOT SET이면 PowerShell에서 변수 다시 설정 + Python 다시 실행.

### Q5. 비용 초과 우려
- Console → Billing → Usage Limits → Hard limit $50 설정 (안전 차단)
- Anthropic은 일일/월 초과 알림 보냄

---

## 7단계: 백업 — API key 분실 시

분실 시 Console → API Keys → 기존 key Revoke + 새 key 생성. CINA 코드는 환경변수만 보므로 키 교체에 영향 없음.

---

## 종합 요약 (5분 작업)

1. console.anthropic.com 회원가입 + $5 충전 (3분)
2. API Keys → Create Key → 복사 (1분)
3. PowerShell:
   ```powershell
   [Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
   ```
   (1분, 영구 설정)
4. PowerShell 새로 열기 → `echo $env:ANTHROPIC_API_KEY` 검증
5. 끝. 제게 "API key 설정 완료" 알려주시면 Stage 1 자동 실행.

---

**작성**: 2026-04-29
**유효성**: Anthropic Console 인터페이스 변경 시 부분 갱신 필요
