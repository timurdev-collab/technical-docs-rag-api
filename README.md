# Technical Documentation Retrieval API

A Python **retrieval foundation for RAG applications**, using local Markdown technical documents.

## Current functionality
- Chunk Markdown files and build an in-memory weighted term index.
- Rank passages against user questions using cosine similarity.
- Serve `GET /health` and `GET /search?q=pressure` over a lightweight HTTP API.
- Automated unittest suite and CI.

**Important:** This project currently implements lexical retrieval, not embedding-based semantic retrieval, FastAPI, an LLM or answer generation. These are planned extensions, not completed features.

## Run
Python 3.10+ with no third-party dependencies.

```bash
python -m app.server
curl "http://127.0.0.1:8000/search?q=pressure%20loss&k=2"
python -m unittest discover -s tests -v
```

All included technical documents are sample demonstration content.

## Retrieval verification
Run `python scripts/evaluate.py` for a three-query sample relevance check and `python -m unittest discover -s tests -v` for ranking, input and source-attribution tests. See [architecture](docs/architecture.md). The current implementation performs lexical search, not embeddings or LLM answer generation.
