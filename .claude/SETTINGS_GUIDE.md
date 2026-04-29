# .claude/settings.json 구성 가이드

> 보안상 Claude가 직접 생성하지 못하므로, Heedo가 직접 만들어야 한다.
> 아래 템플릿을 복사하여 `.claude/settings.json` 으로 저장.

## 권장 설정 템플릿

```json
{
  "permissions": {
    "allow": [
      "Read(//C/Users/admin/Desktop/대학원수업/1학기/리더쉽/**)",
      "Write(//C/Users/admin/Desktop/대학원수업/1학기/리더쉽/data/**)",
      "Write(//C/Users/admin/Desktop/대학원수업/1학기/리더쉽/deliverables/**)",
      "Write(//C/Users/admin/Desktop/대학원수업/1학기/리더쉽/docs/**)",
      "Write(//C/Users/admin/Desktop/대학원수업/1학기/리더쉽/src/**)",
      "Bash(python src/*)",
      "Bash(python -m pytest *)",
      "Bash(pip install *)",
      "Bash(ls *)",
      "Bash(pwd)",
      "Bash(git status)",
      "Bash(git diff)",
      "Bash(git log *)",
      "WebFetch(domain:unfccc.int)",
      "WebFetch(domain:enb.iisd.org)",
      "WebFetch(domain:cop30.br)",
      "WebFetch(domain:iddri.org)",
      "WebFetch(domain:iisd.org)",
      "WebFetch(domain:wri.org)",
      "WebFetch(domain:unu.edu)",
      "WebFetch(domain:nature.com)",
      "WebSearch",
      "Grep",
      "Glob"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)",
      "Bash(git reset --hard *)",
      "Write(//C/Users/admin/Desktop/대학원수업/1학기/리더쉽/.env)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo [$(date +%H:%M:%S)] CINA modified file >> .claude/logs/file_changes.log"
          }
        ]
      }
    ]
  }
}
```

## 해설

### permissions.allow
- **Read**: 프로젝트 전체 읽기 허용
- **Write**: 중요 아티팩트 디렉토리만 허용 (data, deliverables, docs, src)
- **Bash**: Python 실행, 패키지 설치, git 조회만 허용 (push는 수동)
- **WebFetch**: 공식 기후외교 도메인만 자동 허용
- **WebSearch/Grep/Glob**: 연구 탐색 허용

### permissions.deny
- `rm -rf`: 파일 삭제 차단
- `git push --force` / `reset --hard`: 파괴적 작업 차단
- `.env` 쓰기 차단: API key 보호

### hooks
- 파일 변경 시 자동 로그 (감사용)

## API Key 관리

Claude API key는 `.env` 파일에 저장하고, `.gitignore`에 추가:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...
```

```gitignore
# .gitignore
.env
data/raw/
data/processed/
data/llm_logs/
*.pkl
*.npy
__pycache__/
.venv/
```

## 적용 방법

1. 이 파일 내용 참고하여 `.claude/settings.json` 수동 생성
2. Claude Code 재시작 (`/restart`) — 설정 반영
3. `.gitignore` 동시 생성 권장

## 추가 customization

Heedo가 원하는 경우:
- **Model preference**: `"model": "claude-opus-4-7"` 추가
- **Environment vars**: `"env": {"PYTHONPATH": "./src"}` 추가
- **Slash commands**: `.claude/commands/` 아래 `.md` 파일 생성
