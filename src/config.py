"""Configuration settings for Regulatory Compliance Hybrid RAG System."""

from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration class loaded from environment and defaults."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Base Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data")
    RAW_DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data" / "raw")
    PROCESSED_DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data" / "processed")
    CHROMA_PERSIST_DIRECTORY: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent / "data" / "chroma_db"
    )
    BM25_PERSIST_PATH: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent / "data" / "processed" / "bm25_index.pkl"
    )

    # API Keys
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    # Embedding Settings
    EMBEDDING_PROVIDER: str = "sentence_transformers"  # "sentence_transformers" or "gemini"
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DEVICE: str = "cpu"  # "cpu", "cuda", or "mps"

    # Reranker Settings
    RERANKER_MODEL_NAME: str = "BAAI/bge-reranker-base"
    RERANKER_DEVICE: str = "cpu"

    # Vector Store Settings
    CHROMA_COLLECTION_NAME: str = "regulatory_compliance_rbi_sebi"

    # Generation Settings
    DEFAULT_LLM_PROVIDER: str = "gemini"  # "gemini" or "groq"
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Chunking Hyperparameters
    CHUNK_SIZE: int = 450  # Words/tokens target
    CHUNK_OVERLAP: int = 50

    # Retrieval Hyperparameters
    RETRIEVAL_DENSE_TOP_K: int = 20
    RETRIEVAL_SPARSE_TOP_K: int = 20
    RRF_K: int = 60
    RERANK_TOP_N: int = 3
    MIN_CONFIDENCE_THRESHOLD: float = 0.30

    # Server Settings
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    def ensure_directories(self) -> None:
        """Ensure all storage directories exist."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.CHROMA_PERSIST_DIRECTORY.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
