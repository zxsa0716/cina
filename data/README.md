# data/ — CINA 데이터 디렉토리

이 디렉토리는 CINA 파이프라인의 모든 데이터를 담는다. `.gitignore`에 의해 대부분 버전 관리에서 제외되며, 공개는 Zenodo를 통해 논문 수락 후 진행한다.

## 구조

```
data/
├── raw/                          # 외부 소스 원본
│   ├── unfccc_submissions/
│   │   └── cop30/
│   ├── ndcs/
│   ├── enb_summaries/
│   └── castro_2025/
├── processed/                    # 파이프라인 중간·최종 산출물
│   ├── documents.jsonl
│   ├── stances.jsonl
│   ├── graph.pkl
│   ├── graph_analysis.json
│   └── embeddings.npy
├── calibration/
│   ├── expert_coded_stances_sample.csv
│   └── platt.pkl
├── llm_logs/                     # 날짜별 LLM 호출 기록
└── runs/                         # 실행 스냅샷 (config, seeds)
```

## 데이터 소스별 라이선스

| 소스 | 라이선스 | 재이용 |
|------|---------|--------|
| UNFCCC submissions | UN 공개 문서 | 자유 재이용, 출처 명시 |
| NDC Registry | 국가 주권 문서 | 인용 가능, 재배포 주의 |
| IISD ENB | CC BY-NC-SA 4.0 | 비영리 연구 재이용 OK |
| Castro et al. 2025 | Nature Sci Data | 인용 필수, 재배포 저자 허가 |

## 초기 세팅

```bash
# 1. 디렉토리 생성
mkdir -p data/{raw/unfccc_submissions/cop30,raw/ndcs,raw/enb_summaries,raw/castro_2025,processed,calibration,llm_logs,runs}

# 2. 수집 실행
python -m src.collect.run --source unfccc --cop 30 --sector adaptation

# 3. Calibration 세트 수동 작성
# data/calibration/expert_coded_stances_sample.csv에 n=50 coding 추가
```

## 재현성 원칙

- 모든 `data/processed/*` 는 `src/` 스크립트로 재생성 가능해야 함
- `data/raw/*` 는 public source에서 수집 스크립트로 재획득 가능해야 함
- `data/runs/{timestamp}/` 에 매 실행의 config/seed/prompt 스냅샷

## 확보된 데이터 현황

(아직 수집 전 — 이 섹션은 파이프라인 실행 후 자동 업데이트 예정)
