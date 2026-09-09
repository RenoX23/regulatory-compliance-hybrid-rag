"""Unit tests for configuration management."""

from pathlib import Path
from src.config import Settings


def test_settings_initialization():
    """Verify settings defaults and directory properties."""
    settings = Settings()
    assert settings.BASE_DIR.exists()
    assert isinstance(settings.DATA_DIR, Path)
    assert isinstance(settings.RAW_DATA_DIR, Path)
    assert settings.CHUNK_SIZE > 0
    assert settings.CHUNK_OVERLAP >= 0
    assert settings.RRF_K > 0
    assert settings.RETRIEVAL_DENSE_TOP_K > 0
    assert settings.RETRIEVAL_SPARSE_TOP_K > 0


def test_settings_directories_creation(tmp_path):
    """Verify ensure_directories creates nested folders."""
    settings = Settings(DATA_DIR=tmp_path / "data")
    settings.RAW_DATA_DIR = settings.DATA_DIR / "raw"
    settings.PROCESSED_DATA_DIR = settings.DATA_DIR / "processed"
    settings.CHROMA_PERSIST_DIRECTORY = settings.DATA_DIR / "chroma"
    settings.ensure_directories()

    assert settings.RAW_DATA_DIR.exists()
    assert settings.PROCESSED_DATA_DIR.exists()
    assert settings.CHROMA_PERSIST_DIRECTORY.exists()
