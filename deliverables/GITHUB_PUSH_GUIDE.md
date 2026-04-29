# GitHub Push 완벽 가이드 (Heedo 단계별)

> 2026-04-29 작성. CINA 95%+ 구축 후 GitHub 공개 준비.

---

## 0. 사전 점검 (5초)

```powershell
cd C:\Users\admin\Desktop\대학원수업\1학기\리더쉽
ls
```

다음 파일들이 있어야 함:
- `LICENSE` ✓
- `README.md` ✓ (badges + 5분 quickstart)
- `.gitignore` ✓ (104 lines, secrets/.env/raw data 차단)
- `requirements.txt` ✓
- `CINA_FRAMEWORK.md` ✓
- `docs/`, `src/`, `deliverables/`, `council_sessions/`, `.claude/` ✓

---

## 1. Secrets 재검증 (반드시 — push 전 필수)

### 1.1 .env 파일 + key 누락 확인
```powershell
# .env 또는 키 패턴 검색
git ls-files | findstr /i "env key secret token credential"
```
출력이 비어있어야 함. 있으면 `.gitignore`에 추가.

### 1.2 코드 안 hardcoded key 검색
```powershell
findstr /R /S /M "sk-ant- AIza gsk_ sk-or-" src docs deliverables 2>nul
```
출력이 비어있어야 함.

### 1.3 council session memory 점검
```powershell
ls council_sessions/.memory_graph.json council_sessions/.council_memory.json 2>nul
# 있으면 .gitignore가 차단해야 함 (이미 추가됨)
```

---

## 2. GitHub 저장소 생성 (5분)

### 2.1 GitHub 계정 (이미 있으면 skip)
- https://github.com/signup → 학교 이메일 (zxsa0716@kookmin.ac.kr) 권장
- 인증 (이메일 확인)

### 2.2 새 repository 생성
- 우측 상단 + → "New repository"
- Repository name: `cina` 또는 `cina-research` 또는 `climate-issue-network-analysis`
- Description: `Climate Issue-Network Analysis — LLM-GNN pipeline for climate diplomacy, validated on COP30 Belém Adaptation Indicators`
- Visibility: **Public** (논문 투고 + 공개 학술 기여 목적) 또는 **Private** (수업 제출 후 공개)
- **체크하지 말 것**:
  - ❌ Add a README file (이미 있음)
  - ❌ Add .gitignore (이미 있음)
  - ❌ Choose a license (이미 있음)
- "Create repository" 클릭

생성 후 URL: `https://github.com/[USERNAME]/cina`

---

## 3. Git 초기화 + 첫 commit (10분)

### 3.1 Git 설치 확인
```powershell
git --version
```
없으면: https://git-scm.com/download/win 설치.

### 3.2 사용자 정보 설정 (1회만)
```powershell
git config --global user.name "Heedo"
git config --global user.email "zxsa0716@kookmin.ac.kr"
```

### 3.3 로컬 git 저장소 초기화
```powershell
cd C:\Users\admin\Desktop\대학원수업\1학기\리더쉽

# 이미 .git이 있으면 skip
git init

# .gitignore 적용 확인
git status

# 의도하지 않은 파일이 보이면 .gitignore 추가
```

### 3.4 첫 commit
```powershell
git add .
git status                    # 추가된 파일 확인 — secrets 없는지 한 번 더
git commit -m "Initial CINA v2.0 release: LLM-GNN pipeline + 5-agent council + 225 manifest entries

- 15 docs/ academic methodology files (Theoretical foundations, methodology, evaluation)
- 25 src/collect/ collectors (UNFCCC, NDC, ENB, IPCC, IMF, PRIMAP, Plano Clima, etc.)
- 5-agent council architecture (R0-R5 Phase A complete, Combined Rubric 4.37/5)
- Stage 1/2/3 pipeline code with provider abstraction (Gemini/Groq/Ollama/Anthropic)
- 225 manifest entries with license/sha256 tracking
- Key academic findings: GGA-IND Authority 6.1, Brazil Δ=0.304 CONFIRMED, L.25 pre-crystallized formula, Realist F1=0.560

Constitution 4 directives all PASS-eligible after free LLM provider integration."
```

### 3.5 GitHub remote 연결
```powershell
git remote add origin https://github.com/[USERNAME]/cina.git
git branch -M main
git push -u origin main
```

처음 push 시 GitHub 인증 (브라우저 popup 또는 PAT):
- Personal Access Token 권장 — https://github.com/settings/tokens
  - "Generate new token (classic)" → repo scope → 토큰 복사
  - PowerShell에서 username + token 입력 (token이 password 자리)

---

## 4. 첫 push 후 확인

### 4.1 GitHub 웹에서 확인
브라우저에서 `https://github.com/[USERNAME]/cina` 접속.

확인:
- README.md badge 모두 표시되는지
- LICENSE 자동 인식 (MIT + CC BY 4.0)
- 폴더 구조 (docs/, src/, deliverables/) 보이는지
- secrets 누출 없는지 (`.env`, API key)

### 4.2 size 확인
```powershell
git count-objects -vH
```
1 GB 미만이어야 정상. 초과 시 `data/raw/` 가 commit 됐을 가능성 — `.gitignore` 재점검.

---

## 5. 후속 push (라운드 진행 후)

### 5.1 변경 사항 확인
```powershell
git status
git diff
```

### 5.2 commit + push
```powershell
git add deliverables/IRR_Brazil_2025_v3.md     # 특정 파일만
# 또는
git add -u                                       # 추적 중 변경
git commit -m "Round 6: Stage 1 LLM extraction + IRR_Brazil v3"
git push
```

---

## 6. 학술 공개 옵션

### 6.1 Zenodo DOI (권장 — 인용 가능)
- https://zenodo.org/account/settings/github/ 에서 GitHub repo 연결
- GitHub repo 우측 "Releases" → "Create a new release" → tag `v0.1.0`
- Zenodo가 자동으로 DOI 부여 (예: 10.5281/zenodo.XXXXXXX)
- 논문 인용에 사용

### 6.2 Hugging Face Datasets (데이터 공개)
- `data/processed/*.jsonl` (license-clean) 만 별도 HF Datasets에 공개
- raw 데이터는 Zenodo 또는 SWISSUbase 모방 (학술 승인 후)

### 6.3 arXiv preprint
- 논문 draft 완성 후 https://arxiv.org/submit
- CC BY 4.0 라이선스로 공개

---

## 7. CI/CD (선택, 향후)

### 7.1 GitHub Actions (테스트 자동화)
`.github/workflows/test.yml`:
```yaml
name: CINA Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -c "from src.data.identifiers import CINA_COUNTRIES; print(len(CINA_COUNTRIES))"
      - run: python -m pytest tests/ -v
```

### 7.2 README badges 자동 갱신
- Manifest entries 카운트 자동 업데이트
- Quality gates 점수 자동 표시

---

## 8. 트러블슈팅

### Q1. push가 거부됨 (large files)
- `data/raw/` 가 staged 됐을 가능성. 
  ```powershell
  git rm -r --cached data/raw/
  git commit -m "Remove raw data from tracking (already in .gitignore)"
  git push
  ```

### Q2. 인증 실패
- HTTPS → PAT 필요. https://github.com/settings/tokens 에서 PAT 생성.
- 또는 SSH 키: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Q3. README badge 안 보임
- shields.io 도메인 차단 가능. 광역 차단 환경에서만 발생.
- 일반 환경에서는 자동 작동.

### Q4. LICENSE 자동 인식 안 됨
- LICENSE 파일이 reportPos에 있어야 함 (✓ 이미 root)
- GitHub가 detect하기까지 push 후 1-2분 소요

### Q5. .git 폴더 size 너무 큼
- `data/raw/` 가 history에 들어감. `git filter-repo` 로 정리:
  ```powershell
  pip install git-filter-repo
  git filter-repo --path data/raw --invert-paths
  git push --force
  ```

---

## 9. 권장 push 워크플로우

```powershell
# 매 라운드 종료 시
cd C:\Users\admin\Desktop\대학원수업\1학기\리더쉽
git status
git diff council_sessions/LEDGER.md          # 라운드 진척 확인
git add council_sessions/LEDGER.md council_sessions/round_*/LEAD_REPORT_FINAL.md \
        deliverables/*.md data/manifest/coverage_summary.json
git commit -m "Round N: [핵심 변화 한 줄]"
git push
```

---

## 10. Heedo가 해야 할 단계 요약 (15분)

| # | 단계 | 시간 | 핵심 |
|---|------|------|------|
| 1 | GitHub 회원가입 (이미 있으면 skip) | 3분 | 학교 이메일 |
| 2 | 새 repo 생성 (`cina`) | 2분 | Public 권장, README/license 체크 X |
| 3 | PAT 생성 (Settings → Tokens) | 2분 | repo scope |
| 4 | Git config + init + commit + push | 5분 | 위 §3 명령 그대로 |
| 5 | Zenodo 연결 (선택) | 3분 | 인용 가능한 DOI |

총 **15분 후 GitHub 공개 완료** + 인용 가능한 학술 산출물 등록.

---

## 11. 자율 보강 — 제가 수행 가능 (Heedo 입력 0)

다음 작업은 git push 전에 제가 자동으로 마무리 가능:
- ✅ secrets 재검증 (가까운 미래 자동 실행)
- ✅ README badge 정확도 확인
- ✅ docs/ 모든 cross-reference 검증
- ✅ .gitignore 추가 보강 (이미 104 lines)
- ⏸️ 첫 commit message draft 작성 (위 §3.4 그대로 사용 가능)

Heedo가 명시적으로 `git push` 후 알려주면, 제가 후속 라운드 진행 + 매 라운드별 commit을 자동 push 가능 (단, GitHub 인증은 Heedo 단계).

---

**작성**: 2026-04-29
**버전**: v1
**다음 갱신**: 첫 push 후 후속 워크플로우 정밀화
