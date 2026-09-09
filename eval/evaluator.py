"""Benchmarking and Evaluation Engine for Regulatory Compliance RAG.

Evaluates Pure Vector Search, Hybrid RRF, and Hybrid RRF + Cross-Encoder Reranker
against 105 benchmark QA pairs, computing quantitative metrics and performance deltas.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

from src.config import settings
from src.generation.pipeline import RegulatoryRAGPipeline
from src.retrieval.rrf import reciprocal_rank_fusion
from src.schemas import QueryRequest
from eval.benchmark_data import ALL_BENCHMARK_QA
from eval.metrics import (
    compute_reciprocal_rank,
    compute_hit_at_k,
    compute_faithfulness_score,
    compute_citation_precision,
    compute_refusal_accuracy
)

console = Console()


class RegulatoryRAGEvaluator:
    """Orchestrates comprehensive retrieval and generation benchmark evaluations."""

    def __init__(self, pipeline: Optional[RegulatoryRAGPipeline] = None):
        self.pipeline = pipeline or RegulatoryRAGPipeline()
        self.indexer = self.pipeline.indexer
        self.reranker = self.pipeline.reranker
        self.generator = self.pipeline.generator
        self.validator = self.pipeline.validator

    def evaluate_all(
        self,
        qa_dataset: Optional[List[Dict[str, Any]]] = None,
        max_queries: Optional[int] = None
    ) -> Dict[str, Any]:
        """Execute benchmark evaluation across all test queries."""
        dataset = qa_dataset or ALL_BENCHMARK_QA
        if max_queries:
            dataset = dataset[:max_queries]

        console.print(f"[bold cyan]Starting Regulatory Compliance Benchmark across {len(dataset)} audit queries...[/bold cyan]")

        dense_precision_list: List[float] = []
        dense_hit_list: List[float] = []

        hybrid_precision_list: List[float] = []
        hybrid_hit_list: List[float] = []

        rerank_precision_list: List[float] = []
        rerank_hit_list: List[float] = []
        faithfulness_list: List[float] = []
        citation_precision_list: List[float] = []
        refusal_accuracy_list: List[float] = []
        latency_list: List[float] = []

        query_records: List[Dict[str, Any]] = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn()
        ) as progress:
            task = progress.add_task("Evaluating queries...", total=len(dataset))

            for qa in dataset:
                qid = qa["id"]
                query = qa["query"]
                target_doc = qa["target_doc_id"]
                target_sec = qa.get("target_section", "")
                target_clause = qa.get("target_clause", "")
                cat = qa.get("category", "general")
                expected_cite = qa.get("expected_citation", "")

                is_positive = (target_doc != "none")

                # 1. System A: Pure Dense Vector Search (Baseline)
                dense_hits = self.indexer.search_dense(query, top_k=3)
                if is_positive:
                    dense_mrr = compute_reciprocal_rank(dense_hits, target_doc, target_sec, target_clause)
                    dense_hit = compute_hit_at_k(dense_hits, target_doc, k=3)
                    dense_precision_list.append(dense_mrr)
                    dense_hit_list.append(dense_hit)
                else:
                    dense_mrr = 0.0

                # 2. System B: Hybrid RRF (No Reranker)
                d_20 = self.indexer.search_dense(query, top_k=20)
                s_20 = self.indexer.search_sparse(query, top_k=20)
                rrf_hits = reciprocal_rank_fusion(d_20, s_20, k=settings.RRF_K, top_n=3)
                if is_positive:
                    hybrid_mrr = compute_reciprocal_rank(rrf_hits, target_doc, target_sec, target_clause)
                    hybrid_hit = compute_hit_at_k(rrf_hits, target_doc, k=3)
                    hybrid_precision_list.append(hybrid_mrr)
                    hybrid_hit_list.append(hybrid_hit)
                else:
                    hybrid_mrr = 0.0

                # 3. System C: Hybrid RRF + Cross-Encoder Reranker (Proposed Production Pipeline)
                t0 = time.perf_counter()
                resp = self.pipeline.query(QueryRequest(query=query, top_k=3, enable_reranking=True))
                lat_ms = (time.perf_counter() - t0) * 1000.0

                if is_positive:
                    rerank_mrr = compute_reciprocal_rank(resp.retrieved_chunks, target_doc, target_sec, target_clause)
                    rerank_hit = compute_hit_at_k(resp.retrieved_chunks, target_doc, k=3)
                    rerank_precision_list.append(rerank_mrr)
                    rerank_hit_list.append(rerank_hit)
                else:
                    rerank_mrr = 1.0 if not resp.grounded else 0.0

                faithfulness = compute_faithfulness_score(resp.answer, resp.retrieved_chunks)
                cite_prec = compute_citation_precision(resp.citations, expected_cite)
                refusal_acc = compute_refusal_accuracy(cat, resp.answer)

                faithfulness_list.append(faithfulness)
                citation_precision_list.append(cite_prec)
                refusal_accuracy_list.append(refusal_acc)
                latency_list.append(lat_ms)

                query_records.append({
                    "id": qid,
                    "category": cat,
                    "query": query,
                    "target_doc_id": target_doc,
                    "dense_mrr": dense_mrr,
                    "hybrid_mrr": hybrid_mrr,
                    "rerank_mrr": rerank_mrr,
                    "faithfulness": faithfulness,
                    "latency_ms": lat_ms,
                    "grounded": resp.grounded
                })

                progress.update(task, advance=1)

        # Compute aggregate averages
        avg_dense_precision = float(sum(dense_precision_list)) / len(dense_precision_list)
        avg_dense_hit = float(sum(dense_hit_list)) / len(dense_hit_list)

        avg_hybrid_precision = float(sum(hybrid_precision_list)) / len(hybrid_precision_list)
        avg_hybrid_hit = float(sum(hybrid_hit_list)) / len(hybrid_hit_list)

        avg_rerank_precision = float(sum(rerank_precision_list)) / len(rerank_precision_list)
        avg_rerank_hit = float(sum(rerank_hit_list)) / len(rerank_hit_list)

        avg_faithfulness = float(sum(faithfulness_list)) / len(faithfulness_list)
        avg_citation_precision = float(sum(citation_precision_list)) / len(citation_precision_list)
        avg_refusal_accuracy = float(sum(refusal_accuracy_list)) / len(refusal_accuracy_list)
        avg_latency = float(sum(latency_list)) / len(latency_list)

        # Compute lift
        precision_lift_pct = (
            ((avg_rerank_precision - avg_dense_precision) / max(0.001, avg_dense_precision)) * 100.0
        )
        hit_lift_pct = (
            ((avg_rerank_hit - avg_dense_hit) / max(0.001, avg_dense_hit)) * 100.0
        )

        summary = {
            "total_queries_evaluated": len(dataset),
            "dense_baseline": {
                "context_precision_mrr": round(avg_dense_precision, 4),
                "hit_rate_at_3": round(avg_dense_hit, 4)
            },
            "hybrid_rrf_no_rerank": {
                "context_precision_mrr": round(avg_hybrid_precision, 4),
                "hit_rate_at_3": round(avg_hybrid_hit, 4)
            },
            "hybrid_rrf_plus_reranker": {
                "context_precision_mrr": round(avg_rerank_precision, 4),
                "hit_rate_at_3": round(avg_rerank_hit, 4),
                "faithfulness": round(avg_faithfulness, 4),
                "citation_precision": round(avg_citation_precision, 4),
                "refusal_accuracy": round(avg_refusal_accuracy, 4),
                "mean_latency_ms": round(avg_latency, 2)
            },
            "improvements": {
                "context_precision_lift_percent": round(precision_lift_pct, 2),
                "hit_rate_lift_percent": round(hit_lift_pct, 2)
            },
            "query_details": query_records
        }
        return summary
