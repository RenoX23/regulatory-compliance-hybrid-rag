"""Unit and integration tests for FastAPI compliance endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.api import app, get_pipeline
from src.generation.pipeline import RegulatoryRAGPipeline
from src.generation.llm import DeterministicComplianceGenerator


@pytest.fixture(scope="module")
def test_client():
    """Create a test client with deterministic generator for fast, reliable CI execution."""
    pipeline = get_pipeline()
    pipeline.generator = DeterministicComplianceGenerator()
    with TestClient(app) as client:
        yield client


def test_health_endpoint(test_client):
    """Verify /health returns 200 and indicates healthy indices."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "regulatory-compliance-hybrid-rag"
    assert data["indices"]["ready"] is True
    assert data["indices"]["dense_chunks_indexed"] > 0
    assert data["indices"]["sparse_chunks_indexed"] > 0


def test_index_status_endpoint(test_client):
    """Verify /index/status returns corpus metadata and configuration."""
    response = test_client.get("/index/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "RBI" in data["supported_regulators"]
    assert "SEBI" in data["supported_regulators"]
    assert "STATUTORY" in data["supported_regulators"]
    assert data["dense_count"] > 0
    assert data["sparse_count"] > 0


def test_benchmark_summary_endpoint(test_client):
    """Verify /benchmark/summary returns 200 and contains benchmark metrics."""
    response = test_client.get("/benchmark/summary")
    assert response.status_code == 200
    data = response.json()
    assert "hybrid_rrf_plus_reranker" in data
    assert "total_queries_evaluated" in data


def test_query_empty_string_fails(test_client):
    """Verify empty query raises 400 Bad Request."""
    response = test_client.post("/query", json={"query": "   "})
    assert response.status_code == 400


def test_query_valid_statutory_directive(test_client):
    """Verify valid regulatory query executes end-to-end and returns grounded response."""
    payload = {
        "query": "What is the Net Owned Fund (NOF) requirement for NBFC under Section 45-IA?",
        "top_k": 3,
        "enable_reranking": True,
        "regulator_filter": "RBI",
    }
    response = test_client.post("/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "answer" in data
    assert data["grounded"] is True
    assert data["confidence_score"] > 0.5
    assert len(data["retrieved_chunks"]) > 0
    assert "total_pipeline_ms" in data["latency_breakdown_ms"]


def test_query_out_of_domain_refusal(test_client):
    """Verify ungrounded out-of-domain query is refused by guardrails."""
    payload = {
        "query": "How to make a delicious margherita pizza with mozzarella?",
        "top_k": 3,
        "enable_reranking": True,
    }
    response = test_client.post("/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "INSUFFICIENT_REGULATORY_EVIDENCE" in data["answer"]
    assert data["grounded"] is False
