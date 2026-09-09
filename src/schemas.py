"""Domain schemas and data contracts for Regulatory Compliance Hybrid RAG."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Regulator(str, Enum):
    """Regulatory Authority or Legal Jurisdiction."""
    RBI = "RBI"
    SEBI = "SEBI"
    STATUTORY = "STATUTORY"


class ChunkMetadata(BaseModel):
    """Granular metadata stored alongside each indexed chunk."""
    chunk_id: str = Field(..., description="Unique identifier: doc_id-cXXX")
    doc_id: str = Field(..., description="Base document ID")
    regulator: Regulator = Field(..., description="Regulatory body (RBI/SEBI/STATUTORY)")
    title: str = Field(..., description="Official title of the regulatory circular/act")
    circular_number: str = Field(..., description="Official circular reference code")
    issue_date: str = Field(..., description="Date of issuance YYYY-MM-DD")
    section_number: str = Field(default="N/A", description="Statutory or regulatory section/chapter")
    section_title: str = Field(default="", description="Descriptive title of section")
    clause_number: str = Field(default="", description="Specific clause or sub-clause")
    page_number: int = Field(default=1, description="Source PDF page number (1-indexed)")
    citation: str = Field(..., description="Standardized auditor-facing citation string")


class DocumentChunk(BaseModel):
    """A bounded, section-aware unit of regulatory text ready for indexing."""
    chunk_id: str
    content: str = Field(..., description="Text content including standardized context header")
    raw_text: str = Field(..., description="Raw text without context prefix")
    metadata: ChunkMetadata


class RegulatoryDocument(BaseModel):
    """Full regulatory document representation."""
    doc_id: str
    regulator: Regulator
    title: str
    circular_number: str
    issue_date: str
    subject: str
    pdf_filename: str
    total_pages: int = 1
    sections: List[Dict[str, Any]] = Field(default_factory=list)


class RetrievalResult(BaseModel):
    """A scored retrieval candidate produced by dense, sparse, RRF, or reranker layers."""
    chunk_id: str
    content: str
    metadata: ChunkMetadata
    score: float = Field(..., description="Similarity score, BM25 score, RRF score, or reranker probability")
    retrieval_type: str = Field(..., description="Type of retrieval: 'dense', 'sparse', 'rrf', 'reranked'")
    rank: int = Field(default=0, description="1-indexed rank within candidate list")


class QueryRequest(BaseModel):
    """Incoming user or auditor compliance query."""
    query: str = Field(..., min_length=3, description="Compliance query or legal question")
    top_k: int = Field(default=3, ge=1, le=20, description="Final number of context chunks")
    regulator_filter: Optional[Regulator] = Field(default=None, description="Optional regulator filter")
    enable_reranking: bool = Field(default=True, description="Whether to apply cross-encoder reranker")


class QueryResponse(BaseModel):
    """Final grounded answer with citations and verified context."""
    query: str
    answer: str
    grounded: bool = Field(..., description="True if query met confidence threshold and has citations")
    confidence_score: float = Field(..., description="Highest reranker score or composite confidence")
    citations: List[str] = Field(default_factory=list, description="Extracted official regulatory citations")
    retrieved_chunks: List[RetrievalResult] = Field(default_factory=list)
    latency_breakdown_ms: Dict[str, float] = Field(default_factory=dict)
