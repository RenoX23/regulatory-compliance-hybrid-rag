"""Cross-Encoder Reranking Layer for Regulatory Precision.

Applies deep cross-attention over query-chunk pairs using BAAI/bge-reranker-base
to filter top RRF candidates down to high-density context passages.
"""

import time
from typing import List, Optional
import numpy as np
from rich.console import Console

from src.config import settings
from src.schemas import RetrievalResult

console = Console()


class CrossEncoderReranker:
    """Cross-Encoder reranker evaluating full attention between query and chunk."""

    def __init__(
        self,
        model_name: Optional[str] = None,
        device: Optional[str] = None
    ):
        from sentence_transformers import CrossEncoder

        self.model_name = model_name or settings.RERANKER_MODEL_NAME
        self.device = device or settings.RERANKER_DEVICE
        console.print(f"[cyan]Loading Cross-Encoder reranker: {self.model_name} on {self.device}...[/cyan]")
        try:
            self.model = CrossEncoder(self.model_name, device=self.device)
        except Exception as e:
            fallback = "cross-encoder/ms-marco-MiniLM-L-6-v2"
            console.print(f"[yellow]Failed loading {self.model_name} ({e}), falling back to {fallback}...[/yellow]")
            self.model = CrossEncoder(fallback, device=self.device)

    def _sigmoid(self, x: float) -> float:
        """Sigmoid activation to convert raw logit to probability in [0, 1]."""
        return float(1.0 / (1.0 + np.exp(-x)))

    def rerank(
        self,
        query: str,
        candidates: List[RetrievalResult],
        top_n: int = settings.RERANK_TOP_N
    ) -> List[RetrievalResult]:
        """Rerank candidate chunks using cross-encoder attention scoring.

        Args:
            query: User or auditor query.
            candidates: Top candidates from RRF.
            top_n: Number of top chunks to retain (default 3).

        Returns:
            Reranked list of RetrievalResult sorted by cross-encoder score.
        """
        if not candidates:
            return []

        start_time = time.perf_counter()
        pairs = [[query, c.content] for c in candidates]

        raw_scores = self.model.predict(pairs, show_progress_bar=False)

        scored_results: List[RetrievalResult] = []
        for c, raw_score in zip(candidates, raw_scores):
            prob_score = self._sigmoid(float(raw_score))
            scored_results.append(
                RetrievalResult(
                    chunk_id=c.chunk_id,
                    content=c.content,
                    metadata=c.metadata,
                    score=prob_score,
                    retrieval_type="reranked"
                )
            )

        scored_results.sort(key=lambda x: x.score, reverse=True)
        top_results = scored_results[:top_n]
        for rank_idx, item in enumerate(top_results, start=1):
            item.rank = rank_idx

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        console.print(f"[green]Reranked {len(candidates)} candidates -> top {len(top_results)} in {latency_ms:.1f}ms.[/green]")
        return top_results
