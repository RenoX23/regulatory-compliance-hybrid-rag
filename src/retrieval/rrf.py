"""Reciprocal Rank Fusion (RRF) for Hybrid Dense-Sparse Search.

Combines disjoint or overlapping rank lists from dense vector search (ChromaDB)
and sparse keyword search (BM25) using reciprocal rank scoring:
Score(d) = sum(1 / (k + rank(d)))
"""

from typing import Dict, List, Optional
from rich.console import Console

from src.config import settings
from src.schemas import ChunkMetadata, RetrievalResult

console = Console()


def reciprocal_rank_fusion(
    dense_results: List[RetrievalResult],
    sparse_results: List[RetrievalResult],
    k: int = settings.RRF_K,
    top_n: int = 15
) -> List[RetrievalResult]:
    """Merge and re-score dense and sparse retrieval results using RRF.

    Args:
        dense_results: Ranked results from dense vector index.
        sparse_results: Ranked results from sparse BM25 index.
        k: Smoothing constant (default 60). Mitigates the impact of high ranks.
        top_n: Number of fused candidates to return.

    Returns:
        Fused list of RetrievalResult objects ordered by composite RRF score.
    """
    rrf_scores: Dict[str, float] = {}
    chunk_meta_map: Dict[str, ChunkMetadata] = {}
    chunk_content_map: Dict[str, str] = {}
    dense_ranks: Dict[str, int] = {}
    sparse_ranks: Dict[str, int] = {}

    # Accumulate dense ranks
    for rank_idx, r in enumerate(dense_results, start=1):
        cid = r.chunk_id
        rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank_idx))
        chunk_meta_map[cid] = r.metadata
        chunk_content_map[cid] = r.content
        dense_ranks[cid] = rank_idx

    # Accumulate sparse ranks
    for rank_idx, r in enumerate(sparse_results, start=1):
        cid = r.chunk_id
        rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank_idx))
        if cid not in chunk_meta_map:
            chunk_meta_map[cid] = r.metadata
            chunk_content_map[cid] = r.content
        sparse_ranks[cid] = rank_idx

    # Sort descending by RRF score
    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    fused_results: List[RetrievalResult] = []
    for new_rank, (cid, score) in enumerate(sorted_items, start=1):
        fused_results.append(
            RetrievalResult(
                chunk_id=cid,
                content=chunk_content_map[cid],
                metadata=chunk_meta_map[cid],
                score=score,
                retrieval_type="rrf",
                rank=new_rank
            )
        )

    return fused_results
