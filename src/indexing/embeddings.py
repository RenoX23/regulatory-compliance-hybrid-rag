"""Embedding Providers for Dense Vector Retrieval."""

from abc import ABC, abstractmethod
from typing import List, Optional
import numpy as np
from rich.console import Console

from src.config import settings

console = Console()


class BaseEmbeddings(ABC):
    """Abstract interface for document and query embedding generators."""

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Compute embeddings for a list of document chunks."""
        pass

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Compute embedding for a single query."""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Vector dimensionality."""
        pass


class SentenceTransformerEmbeddings(BaseEmbeddings):
    """Local SentenceTransformer embedding model."""

    def __init__(self, model_name: Optional[str] = None, device: Optional[str] = None):
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self.device = device or settings.EMBEDDING_DEVICE
        console.print(f"[cyan]Loading SentenceTransformer embedding model: {self.model_name} on {self.device}...[/cyan]")
        self.model = SentenceTransformer(self.model_name, device=self.device)
        if hasattr(self.model, "get_embedding_dimension"):
            self._dimension = self.model.get_embedding_dimension()
        else:
            self._dimension = self.model.get_sentence_embedding_dimension()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Batch embed document strings with normalization."""
        if not texts:
            return []
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            normalize_embeddings=True
        )
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string with normalization."""
        emb = self.model.encode(
            [text],
            show_progress_bar=False,
            normalize_embeddings=True
        )[0]
        return emb.tolist()

    @property
    def dimension(self) -> int:
        return self._dimension


class GeminiEmbeddings(BaseEmbeddings):
    """Gemini Cloud API embedding generator using text-embedding-004."""

    def __init__(self, api_key: Optional[str] = None, model: str = "models/text-embedding-004"):
        from google import genai

        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be provided for GeminiEmbeddings")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model
        self._dimension = 768

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []
        for text in texts:
            res = self.client.models.embed_content(
                model=self.model,
                contents=text
            )
            embeddings.append(res.embedding.values)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        res = self.client.models.embed_content(
            model=self.model,
            contents=text
        )
        return res.embedding.values

    @property
    def dimension(self) -> int:
        return self._dimension


_EMBEDDING_INSTANCE: Optional[BaseEmbeddings] = None


def get_embedding_provider() -> BaseEmbeddings:
    """Singleton factory for embedding provider."""
    global _EMBEDDING_INSTANCE
    if _EMBEDDING_INSTANCE is not None:
        return _EMBEDDING_INSTANCE

    if settings.EMBEDDING_PROVIDER.lower() == "gemini" and settings.GEMINI_API_KEY:
        try:
            _EMBEDDING_INSTANCE = GeminiEmbeddings()
            return _EMBEDDING_INSTANCE
        except Exception as e:
            console.print(f"[yellow]Failed initializing Gemini embeddings ({e}), falling back to local SentenceTransformer.[/yellow]")

    _EMBEDDING_INSTANCE = SentenceTransformerEmbeddings()
    return _EMBEDDING_INSTANCE
