---
assigned_to: policy-data-collector
round: 6
priority: P0
issued_by: team-lead
issued_at: 2026-04-30
---

# Task T01 — Round 6 Collection Boost

## 목적
R5 Phase B 두 교수 권고 직접 대응. AILAC submission, LDC B2BR, COP21-27 historical chair letters 추가, Castro matrix enb-mining script 4 자동 실행.

## 산출물
- [ ] AILAC GST submission 정제 (frame_type=justice 검증)
- [ ] LDC B2BR submission 정제 (CBDR-RC 보강)
- [ ] COP21-27 historical chair letters 12+ 추가 (chair_metadata 56→80+)
- [ ] enb-mining script 4 자동 실행 → Castro cooperation matrix 자체 생성
- [ ] Ollama qwen2.5:3b (1.6 GB) 설치 권고 → Multi-LLM ensemble 정상화

## 품질 기준
- chair_metadata N≥80 (Bayer-Urpelainen panel threshold)
- AILAC frame_type=justice CINA Stage 1로 직접 추출
- Castro auto-reproduction precision ≥ 70% vs manual coding sample

## 권장 명령
```powershell
cd data/raw/round7/castro_reproduction_repo/enb-mining-main
pip install -r requirements.txt
python scripts/1-list-issues.py data/issues.csv
python scripts/2-download-html.py data/issues.csv data/html
python scripts/3-scrape-interventions.py data/html data/issues.csv data/parties.txt data/groupings.txt data/interventions.csv
python scripts/4-scrape-interactions.py data/interventions.csv data/parties.txt data/groupings.txt data/interactions.csv
```

## 상태 업데이트
- 2026-04-30: 발급 완료. Heedo 결정 D-R6-1~4 후 실행 또는 자동 진행.
