"""Unit tests for Cross-Encoder Reranker."""

from src.retrieval.reranker import CrossEncoderReranker
from src.schemas import ChunkMetadata, Regulator, RetrievalResult


def test_cross_encoder_reranking():
    """Verify cross-encoder reranker scores pairs and returns top_n."""
    reranker = CrossEncoderReranker()

    c1 = RetrievalResult(
        chunk_id="c1",
        content="Section 138 of Negotiable Instruments Act deals with cheque dishonour and 30 days statutory notice.",
        metadata=ChunkMetadata(
            chunk_id="c1",
            doc_id="ni-act",
            regulator=Regulator.STATUTORY,
            title="NI Act",
            circular_number="Act 26",
            issue_date="1881-12-09",
            citation="STATUTORY - NI Act - Page 1"
        ),
        score=0.01,
        retrieval_type="rrf",
        rank=1
    )
    c2 = RetrievalResult(
        chunk_id="c2",
        content="SEBI Mutual Fund regulations dictate Total Expense Ratio (TER) limits for equity schemes.",
        metadata=ChunkMetadata(
            chunk_id="c2",
            doc_id="sebi-mf",
            regulator=Regulator.SEBI,
            title="Mutual Funds",
            circular_number="SEBI/MF/01",
            issue_date="2019-06-05",
            citation="SEBI - Mutual Funds - Page 1"
        ),
        score=0.01,
        retrieval_type="rrf",
        rank=2
    )

    query = "What is the statutory notice period for cheque dishonour under Section 138?"
    reranked = reranker.rerank(query, [c2, c1], top_n=2)

    assert len(reranked) == 2
    # c1 is directly relevant to Section 138, c2 is about mutual fund expenses
    assert reranked[0].chunk_id == "c1"
    assert reranked[0].score > reranked[1].score
    assert reranked[0].rank == 1
    assert reranked[1].rank == 2
