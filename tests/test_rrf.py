"""Unit tests for Reciprocal Rank Fusion (RRF)."""

from src.retrieval.rrf import reciprocal_rank_fusion
from src.schemas import ChunkMetadata, Regulator, RetrievalResult


def create_result(cid: str, rank: int, score: float, r_type: str) -> RetrievalResult:
    meta = ChunkMetadata(
        chunk_id=cid,
        doc_id=cid.split("-")[0],
        regulator=Regulator.RBI,
        title="Regulation",
        circular_number="RBI/2023/01",
        issue_date="2023-01-01",
        citation=f"RBI - [{cid}] - Page 1"
    )
    return RetrievalResult(
        chunk_id=cid,
        content=f"Content for {cid}",
        metadata=meta,
        score=score,
        retrieval_type=r_type,
        rank=rank
    )


def test_rrf_scoring_and_ordering():
    """Verify that a document appearing at rank 1 in both dense and sparse wins top RRF."""
    # doc A: rank 1 in dense, rank 1 in sparse
    # doc B: rank 2 in dense, missing in sparse
    # doc C: missing in dense, rank 2 in sparse
    dense = [
        create_result("doc-A", 1, 0.95, "dense"),
        create_result("doc-B", 2, 0.85, "dense"),
    ]
    sparse = [
        create_result("doc-A", 1, 15.0, "sparse"),
        create_result("doc-C", 2, 10.0, "sparse"),
    ]

    fused = reciprocal_rank_fusion(dense, sparse, k=60, top_n=3)
    assert len(fused) == 3
    assert fused[0].chunk_id == "doc-A"

    # doc-A score should be (1/61) + (1/61) = 2/61 ~= 0.03278
    expected_a = (1.0 / 61.0) + (1.0 / 61.0)
    assert abs(fused[0].score - expected_a) < 1e-5
    assert fused[0].rank == 1


def test_rrf_empty_inputs():
    """Verify RRF handles empty inputs gracefully."""
    res = reciprocal_rank_fusion([], [], k=60, top_n=5)
    assert res == []

    dense_only = [create_result("doc-1", 1, 0.9, "dense")]
    res2 = reciprocal_rank_fusion(dense_only, [], k=60, top_n=5)
    assert len(res2) == 1
    assert res2[0].chunk_id == "doc-1"
