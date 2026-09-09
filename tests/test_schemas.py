"""Unit tests for Pydantic data schemas."""

import pytest
from pydantic import ValidationError
from src.schemas import ChunkMetadata, DocumentChunk, Regulator, RetrievalResult


def test_chunk_metadata_valid():
    """Verify ChunkMetadata instantiates with all required fields."""
    meta = ChunkMetadata(
        chunk_id="test-doc-c001",
        doc_id="test-doc",
        regulator=Regulator.RBI,
        title="Test Regulation",
        circular_number="RBI/2023-24/10",
        issue_date="2023-05-10",
        section_number="Section 10",
        section_title="Capital Requirements",
        clause_number="Clause 1.1",
        page_number=2,
        citation="RBI - [RBI/2023-24/10] - Section 10 - Page 2"
    )
    assert meta.regulator == Regulator.RBI
    assert meta.page_number == 2


def test_chunk_metadata_invalid_regulator():
    """Verify validation error when unsupported regulator is provided."""
    with pytest.raises(ValidationError):
        ChunkMetadata(
            chunk_id="test-c001",
            doc_id="test",
            regulator="INVALID_REGULATOR",  # type: ignore
            title="Test",
            circular_number="CIRC/01",
            issue_date="2023-01-01",
            citation="Test Citation"
        )


def test_retrieval_result_creation():
    """Verify RetrievalResult schema."""
    meta = ChunkMetadata(
        chunk_id="doc1-c001",
        doc_id="doc1",
        regulator=Regulator.SEBI,
        title="SEBI LODR",
        circular_number="SEBI/2015/01",
        issue_date="2015-09-02",
        citation="SEBI - LODR - Page 1"
    )
    res = RetrievalResult(
        chunk_id="doc1-c001",
        content="Regulation 30 disclosure rules",
        metadata=meta,
        score=0.92,
        retrieval_type="dense",
        rank=1
    )
    assert res.score == 0.92
    assert res.retrieval_type == "dense"
