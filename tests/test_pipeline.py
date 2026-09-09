"""Integration tests for the complete RegulatoryRAGPipeline."""

from src.generation.pipeline import RegulatoryRAGPipeline
from src.schemas import QueryRequest, Regulator


def test_regulatory_pipeline_query():
    """Verify end-to-end pipeline execution on real indexed regulatory corpus."""
    pipeline = RegulatoryRAGPipeline()

    # Query with exact statutory code
    req = QueryRequest(
        query="What is the statutory notice period for cheque dishonour under Section 138 of NI Act?",
        top_k=3,
        regulator_filter=Regulator.STATUTORY
    )
    resp = pipeline.query(req)

    assert resp.query == req.query
    assert len(resp.retrieved_chunks) > 0
    assert resp.confidence_score > 0.0
    # Top chunk should cite Section 138
    top_chunk = resp.retrieved_chunks[0]
    assert "138" in top_chunk.metadata.section_number or "138" in top_chunk.content
    assert "total_pipeline_ms" in resp.latency_breakdown_ms
    assert resp.latency_breakdown_ms["total_pipeline_ms"] > 0.0


def test_regulatory_pipeline_ungrounded_fallback():
    """Verify that an out-of-domain query is declined by confidence guardrail."""
    pipeline = RegulatoryRAGPipeline()

    req = QueryRequest(
        query="How do I cook Italian carbonara pasta with egg yolks?",
        top_k=3
    )
    resp = pipeline.query(req)

    # Out of domain query should fail confidence threshold or fallback
    assert (
        "INSUFFICIENT_REGULATORY_EVIDENCE" in resp.answer or
        resp.confidence_score < 0.45 or
        not resp.grounded
    )
