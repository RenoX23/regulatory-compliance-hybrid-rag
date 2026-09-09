"""Full Hybrid RAG Pipeline for Regulatory Compliance & Audit Intelligence."""

import time
from typing import Dict, List, Optional
from rich.console import Console

from src.config import settings
from src.indexing.hybrid_indexer import HybridIndexer
from src.retrieval.rrf import reciprocal_rank_fusion
from src.retrieval.reranker import CrossEncoderReranker
from src.generation.llm import BaseLLMGenerator, get_llm_generator
from src.generation.citations import CitationValidator
from src.schemas import QueryRequest, QueryResponse, Regulator, RetrievalResult

console = Console()


class RegulatoryRAGPipeline:
    """End-to-end Enterprise Compliance Hybrid RAG Pipeline."""

    def __init__(
        self,
        indexer: Optional[HybridIndexer] = None,
        reranker: Optional[CrossEncoderReranker] = None,
        generator: Optional[BaseLLMGenerator] = None,
        validator: Optional[CitationValidator] = None
    ):
        self.indexer = indexer or HybridIndexer()
        self.reranker = reranker or CrossEncoderReranker()
        self.generator = generator or get_llm_generator()
        self.validator = validator or CitationValidator()

    def query(self, request: QueryRequest) -> QueryResponse:
        """Execute the complete Hybrid RAG workflow."""
        start_total = time.perf_counter()
        latencies: Dict[str, float] = {}

        # 1. Dense Retrieval
        t0 = time.perf_counter()
        dense_results = self.indexer.search_dense(
            query=request.query,
            top_k=settings.RETRIEVAL_DENSE_TOP_K,
            regulator_filter=request.regulator_filter
        )
        latencies["dense_retrieval_ms"] = (time.perf_counter() - t0) * 1000.0

        # 2. Sparse Retrieval
        t0 = time.perf_counter()
        sparse_results = self.indexer.search_sparse(
            query=request.query,
            top_k=settings.RETRIEVAL_SPARSE_TOP_K
        )
        # Apply regulator filter on sparse results if requested
        if request.regulator_filter:
            sparse_results = [
                s for s in sparse_results
                if s.metadata.regulator == request.regulator_filter
            ]
        latencies["sparse_retrieval_ms"] = (time.perf_counter() - t0) * 1000.0

        # 3. Reciprocal Rank Fusion (RRF)
        t0 = time.perf_counter()
        fused_candidates = reciprocal_rank_fusion(
            dense_results=dense_results,
            sparse_results=sparse_results,
            k=settings.RRF_K,
            top_n=15
        )
        latencies["rrf_fusion_ms"] = (time.perf_counter() - t0) * 1000.0

        # 4. Cross-Encoder Reranking
        t0 = time.perf_counter()
        if request.enable_reranking and fused_candidates:
            reranked_chunks = self.reranker.rerank(
                query=request.query,
                candidates=fused_candidates,
                top_n=request.top_k
            )
        else:
            reranked_chunks = fused_candidates[:request.top_k]
        latencies["reranking_ms"] = (time.perf_counter() - t0) * 1000.0

        # Check confidence threshold
        max_score = reranked_chunks[0].score if reranked_chunks else 0.0
        is_low_confidence = (
            not reranked_chunks or
            max_score < settings.MIN_CONFIDENCE_THRESHOLD or
            (len(sparse_results) == 0 and max_score < 0.62)
        )
        if is_low_confidence:
            answer = (
                "INSUFFICIENT_REGULATORY_EVIDENCE: The provided RBI/SEBI regulatory corpus "
                "does not contain sufficient authoritative grounds to answer this query with legal certainty."
            )
            latencies["generation_ms"] = 0.0
            latencies["total_pipeline_ms"] = (time.perf_counter() - start_total) * 1000.0
            return QueryResponse(
                query=request.query,
                answer=answer,
                grounded=False,
                confidence_score=max_score,
                citations=[],
                retrieved_chunks=reranked_chunks,
                latency_breakdown_ms=latencies
            )

        # 5. Grounded Generation
        t0 = time.perf_counter()
        answer = self.generator.generate(request.query, reranked_chunks)
        latencies["generation_ms"] = (time.perf_counter() - t0) * 1000.0

        # 6. Citation Extraction & Verification
        is_grounded, verified_cites, ungrounded_cites = self.validator.verify_citations(
            answer=answer,
            retrieved_contexts=reranked_chunks
        )

        # If answer says INSUFFICIENT_REGULATORY_EVIDENCE, mark not grounded
        if "INSUFFICIENT_REGULATORY_EVIDENCE" in answer:
            is_grounded = False

        latencies["total_pipeline_ms"] = (time.perf_counter() - start_total) * 1000.0

        return QueryResponse(
            query=request.query,
            answer=answer,
            grounded=is_grounded,
            confidence_score=max_score,
            citations=verified_cites,
            retrieved_chunks=reranked_chunks,
            latency_breakdown_ms=latencies
        )
