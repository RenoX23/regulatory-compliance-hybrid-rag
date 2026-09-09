# Hybrid RAG System for Financial & Regulatory Compliance (RBI / SEBI)

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![RAG Architecture](https://img.shields.io/badge/RAG-Hybrid_RRF_%2B_Cross--Encoder-orange.svg)]()

> **Domain**: Financial Technology / Regulatory Compliance & Audit Intelligence  
> **Target Role**: AI/ML Engineer / LLM Engineer / Applied Data Scientist  
> **Core Tech Stack**: Python, ChromaDB, rank-bm25, Cross-Encoder (BAAI/bge-reranker-base), Gemini 1.5 Flash / Groq LLaMA 3.3, Ragas, FastAPI, Streamlit, Hugging Face Spaces  

---

## 1. Executive Summary & Problem Framing

Financial institutions and fintechs operating in India face strict regulatory mandates enforced by the Reserve Bank of India (RBI) and Securities and Exchange Board of India (SEBI). Non-compliance results in multi-crore penalties, operational license revocations, and severe reputational damage.

Traditional dense-only vector RAG fails in regulatory and legal domains because dense embeddings hallucinate semantic equivalents while completely missing exact regulatory identifiers, circular numbers, and alphanumeric clause references (e.g., *Section 45-IA*, *Master Direction RBI/2024-25/18*, or *SEBI/HO/MIRSD/CIR/P/2023/112*).

This project implements an **enterprise-grade, hybrid compliance retrieval system**:
1. **Hybrid Retrieval (RRF)**: Merges dense semantic embeddings with sparse exact-token matching (BM25) via **Reciprocal Rank Fusion (RRF)**.
2. **Cross-Encoder Reranking**: Re-scores top candidates using `BAAI/bge-reranker-base` to maximize context density.
3. **Strict Citation & Hallucination Guard**: Constrains the LLM to output answers strictly quoting official document identifiers and clause numbers.
4. **Quantitative Evaluation via Ragas**: Benchmarks retrieval and generation against auditor-style test queries.
5. **Production Deployment**: Publicly deployable on **Hugging Face Spaces**.

---

## 2. System Architecture

```
[Official Regulatory PDFs: RBI Master Directions & SEBI Circulars]
                                │
                                ▼
[Document Ingestion & Section-Aware Chunking]
    ├── Hierarchical section & clause splitting
    └── Metadata Tagging (Circular ID, Section, Issue Date, Clause Ref)
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
[Dense Vector Embeddings]                     [Sparse Inverted Index]
    ├── ChromaDB Vector Store                     └── BM25 Okapi Index
    └── bge-small / text-embedding-004                (rank-bm25)
        │                                               │
        └───────────────────────┬───────────────────────┘
                                ▼
[Reciprocal Rank Fusion (RRF)]
    └── Combines dense & sparse rankings (k=60)
                                │
                                ▼
[Cross-Encoder Reranker: BAAI/bge-reranker-base]
    └── Joint attention scoring; filters top-15 down to top-3
                                │
                                ▼
[Grounded Generation & Citation Enforcement Layer]
    ├── Gemini 1.5 Flash / Groq LLaMA 3.3
    ├── Mandatory Clause Citation Template [Doc ID, Section, Page #]
    └── Fallback Guard: Declines ungrounded queries
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
[Interactive UI / API]                         [Ragas Quantitative Evaluation]
    ├── FastAPI / Streamlit Web App                ├── Faithfulness Score (>92%)
    └── Side-by-Side Source Clause Inspector       └── Context Precision vs Dense Baseline
```

---

## 3. Project Roadmap

- [x] **Scaffold & Architecture Specification**
- [ ] **Phase 1**: Real Regulatory Document Ingestion & Hybrid Indexing
- [ ] **Phase 2**: Reciprocal Rank Fusion & Cross-Encoder Reranking
- [ ] **Phase 3**: Quantitative Evaluation via Ragas
- [ ] **Phase 4**: Hugging Face Spaces Deployment & Documentation
