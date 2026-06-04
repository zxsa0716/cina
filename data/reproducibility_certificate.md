# CINA Reproducibility Certificate

- **Version**: v9.6.0
- **Generated**: 2026-06-04T03:10:16.004152+00:00
- **Total entries**: 58
- **Chain hash**: `b869015d5f88625263796daf21db3d486f0eae5468fb0a1a6be22e8d8a199a4d`

## Categories

| Category | Requested | Present |
|---|---|---|
| v5_dataset | 2 | 2 |
| v5_merged | 3 | 3 |
| v6_corpus_index | 3 | 3 |
| v6_corpus_documents | 16 | 16 |
| v6_corpus_csvs | 5 | 5 |
| v6_corpus_bib | 1 | 1 |
| v7_embeddings | 4 | 2 |
| build_scripts | 8 | 8 |
| engine_scripts | 3 | 3 |
| eval_scripts | 2 | 2 |
| test_suite | 5 | 5 |
| changelogs | 4 | 4 |
| documentation | 4 | 4 |

## How to verify

```bash
git clone https://github.com/zxsa0716/cina
cd cina
python -m src.data.build_reproducibility_certificate
# Compare chain_hash with the one in this file above
```

If chain hashes match, the entire CINA build chain (data + scripts + tests + docs)
is bit-identical to the certified state.