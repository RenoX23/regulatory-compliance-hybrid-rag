"""Sparse BM25 Index for Regulatory Exact-Token Matching.

Implements domain-aware tokenization to preserve regulatory clauses,
circular reference numbers, and statutory sections without token loss.
"""

import pickle
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from rank_bm25 import BM25Okapi
from rich.console import Console

from src.config import settings
from src.schemas import ChunkMetadata, DocumentChunk, RetrievalResult

console = Console()


class RegulatoryTokenizer:
    """Tokenizer tailored for Indian financial regulatory and legal nomenclature."""

    def __init__(self):
        # Matches alphanumeric tokens, hyphens, and slashes: e.g. "45-IA", "RBI/2023-24/102", "SMA-0"
        self.token_regex = re.compile(r"\b[A-Za-z0-9]+(?:[-/.][A-Za-z0-9]+)*\b")

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercased terms preserving legal alphanumeric compounds."""
        if not text:
            return []
        raw_tokens = self.token_regex.findall(text.lower())
        tokens = []
        for t in raw_tokens:
            tokens.append(t)
            # If compound token (e.g. '45-ia' or 'rbi/2023-24/102'), also include split sub-tokens
            if "-" in t or "/" in t or "." in t:
                sub_parts = re.split(r"[-/.]", t)
                for part in sub_parts:
                    if len(part) > 1:
                        tokens.append(part)
        return tokens


class BM25Index:
    """BM25 Okapi sparse index over regulatory document chunks."""

    def __init__(self, tokenizer: Optional[RegulatoryTokenizer] = None):
        self.tokenizer = tokenizer or RegulatoryTokenizer()
        self.bm25: Optional[BM25Okapi] = None
        self.chunks: List[DocumentChunk] = []
        self.chunk_map: Dict[str, DocumentChunk] = {}

    def build(self, chunks: List[DocumentChunk]) -> None:
        """Construct BM25 inverted index from a list of DocumentChunks."""
        if not chunks:
            raise ValueError("Cannot build BM25 index with empty chunk list")

        self.chunks = chunks
        self.chunk_map = {c.chunk_id: c for c in chunks}

        console.print(f"[cyan]Tokenizing {len(chunks)} chunks for BM25 sparse index...[/cyan]")
        tokenized_corpus = [self.tokenizer.tokenize(c.content) for c in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)
        console.print("[green]BM25 sparse index built successfully.[/green]")

    def count(self) -> int:
        """Return number of indexed chunks."""
        return len(self.chunks)

    def query(self, query_text: str, top_k: int = 20) -> List[RetrievalResult]:
        """Search BM25 index and return scored RetrievalResult list."""
        if self.bm25 is None or not self.chunks:
            raise RuntimeError("BM25 index is not initialized or built.")

        query_tokens = self.tokenizer.tokenize(query_text)
        if not query_tokens:
            return []

        doc_scores = self.bm25.get_scores(query_tokens)
        top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]

        results: List[RetrievalResult] = []
        for rank_idx, idx in enumerate(top_indices, start=1):
            score = float(doc_scores[idx])
            if score <= 0.0:
                continue
            chunk = self.chunks[idx]
            results.append(
                RetrievalResult(
                    chunk_id=chunk.chunk_id,
                    content=chunk.content,
                    metadata=chunk.metadata,
                    score=score,
                    retrieval_type="sparse",
                    rank=rank_idx
                )
            )
        return results

    def save(self, file_path: Optional[Path] = None) -> Path:
        """Serialize BM25 index and chunks to disk."""
        target_path = file_path or settings.BM25_PERSIST_PATH
        target_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "bm25": self.bm25,
            "chunks": [c.model_dump() for c in self.chunks]
        }
        with open(target_path, "wb") as f:
            pickle.dump(payload, f)
        console.print(f"[green]Saved BM25 sparse index to {target_path}[/green]")
        return target_path

    def load(self, file_path: Optional[Path] = None) -> bool:
        """Load serialized BM25 index from disk."""
        target_path = file_path or settings.BM25_PERSIST_PATH
        if not target_path.exists():
            return False

        with open(target_path, "rb") as f:
            payload = pickle.load(f)

        self.bm25 = payload["bm25"]
        raw_chunks = payload["chunks"]
        self.chunks = [DocumentChunk.model_validate(c) for c in raw_chunks]
        self.chunk_map = {c.chunk_id: c for c in self.chunks}
        console.print(f"[green]Loaded BM25 index with {len(self.chunks)} chunks from {target_path}[/green]")
        return True
