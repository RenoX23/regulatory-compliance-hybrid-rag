"""Hybrid Indexer Coordinator for Regulatory Compliance RAG.

Orchestrates dense vector indexing (ChromaDB) and sparse inverted indexing (BM25)
to ensure synchronized indexing across both representations.
"""

from typing import Any, Dict, List, Optional
from rich.console import Console

from src.config import settings
from src.ingestion.corpus_builder import CorpusBuilder
from src.indexing.dense_index import ChromaDenseIndex
from src.indexing.sparse_index import BM25Index
from src.schemas import DocumentChunk, Regulator, RetrievalResult

console = Console()


class HybridIndexer:
    """Manages dual indexing into ChromaDB and BM25."""

    def __init__(
        self,
        dense_index: Optional[ChromaDenseIndex] = None,
        sparse_index: Optional[BM25Index] = None,
        corpus_builder: Optional[CorpusBuilder] = None
    ):
        self.dense_index = dense_index or ChromaDenseIndex()
        self.sparse_index = sparse_index or BM25Index()
        self.corpus_builder = corpus_builder or CorpusBuilder()
        self.chunks: List[DocumentChunk] = []

    def index_all(self, force_reindex: bool = False) -> Dict[str, Any]:
        """Perform end-to-end ingestion and dual-indexing of the regulatory corpus."""
        console.print("[bold yellow]Starting Dual Ingestion & Indexing Pipeline...[/bold yellow]")

        # 1. Ingest/parse corpus chunks
        self.chunks = self.corpus_builder.ingest_corpus(force_reparse=force_reindex)
        if not self.chunks:
            raise RuntimeError("No chunks were produced by the CorpusBuilder.")

        # 2. Build or verify BM25 sparse index
        need_sparse_build = force_reindex or not self.sparse_index.load()
        if need_sparse_build:
            self.sparse_index.build(self.chunks)
            self.sparse_index.save()

        # 3. Build or verify ChromaDB dense index
        chroma_count = self.dense_index.count()
        need_dense_build = force_reindex or (chroma_count != len(self.chunks))
        if need_dense_build:
            if force_reindex:
                self.dense_index.clear()
            self.dense_index.add_chunks(self.chunks)

        status = {
            "total_chunks": len(self.chunks),
            "chroma_count": self.dense_index.count(),
            "bm25_count": len(self.sparse_index.chunks),
            "status": "synchronized" if self.dense_index.count() == len(self.sparse_index.chunks) else "mismatched"
        }
        console.print(f"[bold green]Dual indexing complete. Status: {status}[/bold green]")
        return status

    def search_dense(
        self,
        query: str,
        top_k: int = 20,
        regulator_filter: Optional[Regulator] = None
    ) -> List[RetrievalResult]:
        """Search dense vector index."""
        return self.dense_index.query(query, top_k=top_k, regulator_filter=regulator_filter)

    def search_sparse(
        self,
        query: str,
        top_k: int = 20
    ) -> List[RetrievalResult]:
        """Search BM25 sparse index."""
        return self.sparse_index.query(query, top_k=top_k)
