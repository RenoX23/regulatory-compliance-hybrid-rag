"""FastAPI production service for Regulatory Compliance Hybrid RAG."""

import json
import time
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.generation.pipeline import RegulatoryRAGPipeline
from src.schemas import QueryRequest, QueryResponse, Regulator

app = FastAPI(
    title="Regulatory Compliance Hybrid RAG API",
    description=(
        "Enterprise-grade financial and regulatory compliance audit intelligence engine "
        "covering RBI Master Directions, SEBI Circulars, and Statutory Directives."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for cross-domain UI or client integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pipeline Singleton
_pipeline: Optional[RegulatoryRAGPipeline] = None


def get_pipeline() -> RegulatoryRAGPipeline:
    """Retrieve or initialize the singleton RAG pipeline."""
    global _pipeline
    if _pipeline is None:
        _pipeline = RegulatoryRAGPipeline()
    return _pipeline


@app.get("/health", tags=["System"])
def health_check() -> Dict[str, Any]:
    """Health check endpoint confirming index readiness and component availability."""
    try:
        pipeline = get_pipeline()
        dense_count = pipeline.indexer.dense_index.count()
        sparse_count = pipeline.indexer.sparse_index.count()
        return {
            "status": "healthy",
            "service": "regulatory-compliance-hybrid-rag",
            "version": "1.0.0",
            "timestamp": time.time(),
            "indices": {
                "dense_chunks_indexed": dense_count,
                "sparse_chunks_indexed": sparse_count,
                "ready": dense_count > 0 and sparse_count > 0,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service initialization error: {str(e)}",
        )


@app.get("/index/status", tags=["Indexing"])
def index_status() -> Dict[str, Any]:
    """Get metadata on the indexed regulatory corpus and configured ML models."""
    pipeline = get_pipeline()
    return {
        "status": "ready",
        "dense_count": pipeline.indexer.dense_index.count(),
        "sparse_count": pipeline.indexer.sparse_index.count(),
        "embedding_model": settings.EMBEDDING_MODEL_NAME,
        "reranker_model": settings.RERANKER_MODEL_NAME,
        "dense_top_k": settings.RETRIEVAL_DENSE_TOP_K,
        "sparse_top_k": settings.RETRIEVAL_SPARSE_TOP_K,
        "rrf_k": settings.RRF_K,
        "min_confidence_threshold": settings.MIN_CONFIDENCE_THRESHOLD,
        "supported_regulators": [r.value for r in Regulator],
    }


@app.post("/query", response_model=QueryResponse, tags=["RAG"])
def query_regulatory_corpus(request: QueryRequest) -> QueryResponse:
    """Execute end-to-end regulatory compliance retrieval, reranking, and generation.

    Accepts a user query, applies hybrid search (dense ChromaDB + sparse BM25),
    fuses candidate lists via Reciprocal Rank Fusion (RRF), computes cross-encoder
    reranking scores, enforces citation guardrails, and returns a verified auditor response.
    """
    if not request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query string cannot be empty.",
        )

    try:
        pipeline = get_pipeline()
        response = pipeline.query(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retrieval or generation pipeline error: {str(e)}",
        )


@app.get("/benchmark/summary", tags=["Evaluation"])
def get_benchmark_summary() -> Dict[str, Any]:
    """Retrieve quantitative Ragas-aligned evaluation metrics and benchmark summaries."""
    report_path = settings.BASE_DIR / "eval" / "reports" / "benchmark_summary.json"
    if not report_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benchmark report has not been generated yet.",
        )
    with open(report_path, "r", encoding="utf-8") as f:
        return json.load(f)
