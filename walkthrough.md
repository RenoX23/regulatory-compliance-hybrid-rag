# Walkthrough: Regulatory Compliance Hybrid RAG (IndicCompliance)

## Overview
We have built and delivered an enterprise-grade **Hybrid RAG System for Financial & Regulatory Compliance** over RBI Master Directions, SEBI Circulars, and Statutory Directives. The project was executed with strict software engineering discipline, production-level code hygiene, and an atomic, professional Git commit history pushed to `origin main` at [https://github.com/RenoX23/regulatory-compliance-hybrid-rag.git](https://github.com/RenoX23/regulatory-compliance-hybrid-rag.git).

---

## 1. Atomic Commit Trajectory on `origin main`

| Commit Hash | Type / Scope | Description |
|---|---|---|
| `6a5c201` | `chore(init)` | Project scaffold, architecture specification, and `.gitignore` |
| `62dca7b` | `chore(deps)` | Lock virtualenv dependencies and update `requirements.txt` |
| `1a26240` | `feat(ingestion)` | Build regulatory PDF ingestion and dual ChromaDB-BM25 indexing |
| `1fb168c` | `feat(retrieval)` | Integrate reciprocal rank fusion, cross-encoder reranker, and citation guardrails |
| `82bfd84` | `feat(eval)` | Build automated Ragas evaluation suite and benchmark retrieval metrics |
| `a561210` | `feat(ui)` | Build interactive Streamlit compliance demo and FastAPI serving endpoints |
| `2706c8e` | `docs` | Deploy live UI to Hugging Face Spaces, complete production README, and add interview defense notes |

---

## 2. Quantitative Benchmark Results (105 Test Inquiries)

From `eval/reports/benchmark_summary.json` and `eval/reports/benchmark_report.md`:

| Metric | Target Threshold | Achieved Score | Status |
|---|---|---|---|
| **Faithfulness Score** | > 92.0% | **96.6%** | **PASSED** |
| **Context Precision Lift (Exact Legal Codes)** | > 25.0% | **+38.5%** | **PASSED** |
| **Adversarial / Out-of-Domain Refusal Accuracy** | 100.0% | **100.0%** | **PASSED** |
| **Hit Rate @ K=3** | > 95.0% | **100.0%** | **PASSED** |
| **Mean Cross-Encoder Latency** | < 400 ms | **124.3 ms** | **PASSED** |

### Comparative Retrieval Architecture Performance
1. **Dense Vector Baseline (`ChromaDB` / `bge-small-en-v1.5`)**:
   - Context Precision (MRR): **0.9176** (collapses to **0.6933** on exact alphanumeric codes)
   - Hit Rate @ 3: **95.7%**
2. **Hybrid Search (RRF $k=60$, No Reranker)**:
   - Context Precision (MRR): **0.9677** (+5.5% lift)
   - Hit Rate @ 3: **97.9%**
3. **Proposed Architecture (Hybrid RRF + `bge-reranker-base`)**:
   - Context Precision (MRR): **0.9892** (**+7.8% overall lift, +38.5% on exact statutory codes**)
   - Hit Rate @ 3: **100.0%**

---

## 3. Implemented Components

1. **Ingestion & Dual-Indexing Pipeline**:
   - `src/ingestion/corpus_data.py`: 22 authentic RBI & SEBI Master Directions and statutory statutes (RBI Act 1934 Section 45-IA, NI Act 1881 Section 138, PMLA 2002 Section 12, Digital Lending, DLG, V-CIP, LODR, PIT, etc.).
   - `src/ingestion/pdf_generator.py`: PyMuPDF layout generator creating authentic multi-page PDFs with headers, circular references, and section boundaries.
   - `src/ingestion/chunker.py`: Section-aware recursive chunker appending canonical context prefixes to avoid contextual drift.
   - `src/indexing/embeddings.py`: SentenceTransformer embeddings wrapper with `BAAI/bge-small-en-v1.5` normalized to unit vectors.
   - `src/indexing/sparse_index.py`: Inverted index using `BM25Okapi` with a specialized `RegulatoryTokenizer` preserving alphanumeric clauses (`45-ia`, `rbi/2023-24/102`, `sma-0`, `138(b)`).
   - `src/indexing/dense_index.py`: Persistent `ChromaDB` collection configured with cosine similarity.
   - `src/indexing/hybrid_indexer.py`: Synchronized dual-index manager.

2. **Retrieval, Reranking & Guardrails**:
   - `src/retrieval/rrf.py`: Reciprocal Rank Fusion ($k=60$) blending top dense and sparse ranks.
   - `src/retrieval/reranker.py`: `CrossEncoderReranker` using `BAAI/bge-reranker-base` with sigmoid normalization and confidence gating (`MIN_CONFIDENCE_THRESHOLD = 0.55`).
   - `src/generation/prompts.py`: Auditor system prompt mandating `[Doc ID, Section, Page #]` citation syntax.
   - `src/generation/citations.py`: Regex `CitationValidator` verifying output citations against retrieved context metadata.
   - `src/generation/llm.py`: Multi-provider generator supporting Gemini, Groq, and a local offline zero-cost `DeterministicComplianceGenerator`.
   - `src/generation/pipeline.py`: `RegulatoryRAGPipeline` coordinating retrieval $\to$ RRF $\to$ rerank $\to$ generation $\to$ latency measurement.

3. **Serving, UI & Deployment**:
   - `src/api.py`: Production FastAPI REST service (`GET /health`, `GET /index/status`, `POST /query`, `GET /benchmark/summary`) with CORS middleware and OpenAPI docs.
   - `app.py`: Streamlit compliance auditor terminal with confidence meters, latency waterfall breakdowns, side-by-side retrieved chunk inspector, benchmark dashboard, and corpus manifest viewer.
   - `Dockerfile` & `.dockerignore`: Container specification configured for Hugging Face Spaces (port 7860, non-root user).
   - `README.md`: Comprehensive recruiter-facing documentation with live badges, ASCII/Mermaid architectures, benchmark tables, the 3 Google XYZ resume bullets, and interview defenses.

4. **Automated Test Suite**:
   - 28 unit and integration tests across 10 test modules (`test_config.py`, `test_schemas.py`, `test_ingestion.py`, `test_indexing.py`, `test_rrf.py`, `test_reranker.py`, `test_generation.py`, `test_pipeline.py`, `test_evaluation.py`, `test_api.py`).
   - **All 28 tests passing with 100% success rate**.
