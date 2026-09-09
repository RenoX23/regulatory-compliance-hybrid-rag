"""Unit tests for benchmark metrics and evaluation engine."""

from eval.benchmark_data import ALL_BENCHMARK_QA
from eval.metrics import (
    compute_reciprocal_rank,
    compute_hit_at_k,
    compute_citation_precision,
    compute_faithfulness_score,
    compute_refusal_accuracy
)
from eval.evaluator import RegulatoryRAGEvaluator
from src.schemas import ChunkMetadata, Regulator, RetrievalResult


def test_benchmark_dataset_integrity():
    """Verify that the benchmark dataset contains at least 100 queries with complete fields."""
    assert len(ALL_BENCHMARK_QA) >= 100
    categories = {qa["category"] for qa in ALL_BENCHMARK_QA}
    assert "exact_code" in categories
    assert "quantitative_threshold" in categories
    assert "conceptual_compliance" in categories
    assert "adversarial_negative" in categories

    for qa in ALL_BENCHMARK_QA:
        assert "id" in qa
        assert "query" in qa and len(qa["query"]) >= 3
        assert "ground_truth_answer" in qa
        assert "target_doc_id" in qa


def test_metric_computations():
    """Verify accuracy of core IR evaluation metrics."""
    meta = ChunkMetadata(
        chunk_id="test-doc-c001",
        doc_id="test-doc",
        regulator=Regulator.RBI,
        title="Test Regulation",
        circular_number="RBI/2023/01",
        issue_date="2023-01-01",
        section_number="Section 10",
        clause_number="Clause 1",
        page_number=1,
        citation="RBI - [RBI/2023/01] - Section 10 - Page 1"
    )
    hit_result = RetrievalResult(
        chunk_id="test-doc-c001",
        content="Under Section 10, capital requirements are mandatory.",
        metadata=meta,
        score=0.9,
        retrieval_type="reranked",
        rank=1
    )

    # MRR calculation
    mrr = compute_reciprocal_rank([hit_result], target_doc_id="test-doc", target_section="Section 10")
    assert mrr == 1.0

    # Hit@3 calculation
    hit = compute_hit_at_k([hit_result], target_doc_id="test-doc", k=3)
    assert hit == 1.0

    # Citation precision
    cite_prec = compute_citation_precision(
        ["RBI - [RBI/2023/01] - Section 10 - Page 1"],
        expected_citation="RBI - [RBI/2023/01] - Section 10"
    )
    assert cite_prec == 1.0

    # Refusal accuracy
    refusal = compute_refusal_accuracy(
        query_category="adversarial_negative",
        answer="INSUFFICIENT_REGULATORY_EVIDENCE: not found."
    )
    assert refusal == 1.0


def test_evaluator_quick_run():
    """Verify that evaluator runs across sample QA queries without error."""
    evaluator = RegulatoryRAGEvaluator()
    sample_dataset = ALL_BENCHMARK_QA[:3]
    summary = evaluator.evaluate_all(qa_dataset=sample_dataset)

    assert summary["total_queries_evaluated"] == 3
    assert "dense_baseline" in summary
    assert "hybrid_rrf_plus_reranker" in summary
    assert summary["hybrid_rrf_plus_reranker"]["faithfulness"] > 0.8
