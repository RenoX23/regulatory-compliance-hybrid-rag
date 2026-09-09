"""ChromaDB Dense Vector Index for Semantic Retrieval."""

from pathlib import Path
from typing import Any, Dict, List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from rich.console import Console

from src.config import settings
from src.indexing.embeddings import BaseEmbeddings, get_embedding_provider
from src.schemas import ChunkMetadata, DocumentChunk, Regulator, RetrievalResult

console = Console()


class ChromaDenseIndex:
    """ChromaDB persistent vector store for regulatory document chunks."""

    def __init__(
        self,
        persist_dir: Optional[Path] = None,
        collection_name: Optional[str] = None,
        embedding_provider: Optional[BaseEmbeddings] = None
    ):
        self.persist_dir = str(persist_dir or settings.CHROMA_PERSIST_DIRECTORY)
        self.collection_name = collection_name or settings.CHROMA_COLLECTION_NAME
        self.embedding_provider = embedding_provider or get_embedding_provider()

        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def count(self) -> int:
        """Return the number of stored vectors in the collection."""
        return self.collection.count()

    def add_chunks(self, chunks: List[DocumentChunk], batch_size: int = 64) -> None:
        """Embed and upsert document chunks into the Chroma collection."""
        if not chunks:
            return

        console.print(f"[cyan]Adding {len(chunks)} chunks to ChromaDB collection '{self.collection_name}'...[/cyan]")

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            ids = [c.chunk_id for c in batch]
            documents = [c.content for c in batch]

            # Serialize metadata ensuring all values are str, int, float, or bool
            metadatas = []
            for c in batch:
                meta_dict = c.metadata.model_dump()
                flat_meta: Dict[str, Any] = {}
                for k, v in meta_dict.items():
                    if isinstance(v, (str, int, float, bool)):
                        flat_meta[k] = v
                    else:
                        flat_meta[k] = str(v)
                metadatas.append(flat_meta)

            # Compute embeddings
            embeddings = self.embedding_provider.embed_documents(documents)

            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )

        console.print(f"[green]Successfully indexed {len(chunks)} chunks in ChromaDB. Total count: {self.count()}[/green]")

    def query(
        self,
        query_text: str,
        top_k: int = 20,
        regulator_filter: Optional[Regulator] = None
    ) -> List[RetrievalResult]:
        """Query ChromaDB for top_k semantically nearest chunks."""
        if self.count() == 0:
            return []

        query_embedding = self.embedding_provider.embed_query(query_text)

        where_clause = None
        if regulator_filter:
            where_clause = {"regulator": regulator_filter.value}

        res = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.count()),
            where=where_clause,
            include=["documents", "metadatas", "distances"]
        )

        results: List[RetrievalResult] = []
        if not res["ids"] or not res["ids"][0]:
            return results

        ids = res["ids"][0]
        docs = res["documents"][0]
        metadatas = res["metadatas"][0]
        distances = res["distances"][0]

        for rank_idx, (cid, doc, meta, dist) in enumerate(zip(ids, docs, metadatas, distances), start=1):
            # Cosine distance in Chroma: dist = 1 - cosine_similarity. Similarity = 1 - dist.
            similarity = max(0.0, min(1.0, 1.0 - float(dist)))
            chunk_meta = ChunkMetadata(
                chunk_id=meta.get("chunk_id", cid),
                doc_id=meta.get("doc_id", "unknown"),
                regulator=Regulator(meta.get("regulator", "STATUTORY")),
                title=meta.get("title", ""),
                circular_number=meta.get("circular_number", ""),
                issue_date=meta.get("issue_date", ""),
                section_number=meta.get("section_number", ""),
                section_title=meta.get("section_title", ""),
                clause_number=meta.get("clause_number", ""),
                page_number=int(meta.get("page_number", 1)),
                citation=meta.get("citation", "")
            )

            results.append(
                RetrievalResult(
                    chunk_id=cid,
                    content=doc,
                    metadata=chunk_meta,
                    score=similarity,
                    retrieval_type="dense",
                    rank=rank_idx
                )
            )

        return results

    def clear(self) -> None:
        """Clear all entries from collection."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
