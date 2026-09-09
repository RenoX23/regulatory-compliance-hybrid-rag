"""Section-Aware Recursive Chunker for Regulatory Compliance Documents.

Splits legal regulatory text while preserving clause integrity and prepending
contextual citation headers to maximize dense and sparse retrieval precision.
"""

from typing import Any, Dict, List
from src.schemas import ChunkMetadata, DocumentChunk, Regulator


class SectionAwareChunker:
    """Chunker that preserves section boundaries and appends canonical regulatory headers."""

    def __init__(self, target_chunk_size: int = 450, chunk_overlap: int = 50):
        self.target_chunk_size = target_chunk_size
        self.chunk_overlap = chunk_overlap

    def format_citation(
        self,
        regulator: Regulator,
        circular_number: str,
        section_number: str,
        clause_number: str,
        page_number: int
    ) -> str:
        """Format an auditor-grade compliance citation string."""
        parts = [f"{regulator.value}"]
        if circular_number and circular_number != "UNKNOWN":
            parts.append(f"[{circular_number}]")
        if section_number and section_number != "General":
            parts.append(f"{section_number}")
        if clause_number and clause_number != "Clause":
            parts.append(f"({clause_number})")
        parts.append(f"Page {page_number}")
        return " - ".join(parts)

    def create_context_header(
        self,
        regulator: Regulator,
        circular_number: str,
        title: str,
        section_number: str,
        clause_number: str,
        page_number: int
    ) -> str:
        """Generate standardized context header prepended to chunk content."""
        return (
            f"[REGULATOR: {regulator.value} | CIRCULAR: {circular_number} | "
            f"SECTION: {section_number} | CLAUSE: {clause_number} | PAGE: {page_number}]\n"
        )

    def _split_text_into_windows(self, text: str) -> List[str]:
        """Split text into word-bounded windows with overlap."""
        words = text.split()
        if len(words) <= self.target_chunk_size:
            return [text]

        windows = []
        start = 0
        step = max(1, self.target_chunk_size - self.chunk_overlap)
        while start < len(words):
            end = min(len(words), start + self.target_chunk_size)
            chunk_words = words[start:end]
            windows.append(" ".join(chunk_words))
            if end >= len(words):
                break
            start += step
        return windows

    def chunk_document(
        self,
        doc_id: str,
        regulator: Regulator,
        title: str,
        circular_number: str,
        issue_date: str,
        clause_records: List[Dict[str, Any]]
    ) -> List[DocumentChunk]:
        """Convert a list of parsed clause records into indexed DocumentChunk objects."""
        chunks: List[DocumentChunk] = []
        chunk_idx = 1

        for rec in clause_records:
            sec_name = rec.get("section", "General")
            clause_num = rec.get("clause_number", "")
            clause_title = rec.get("clause_title", "")
            raw_text = rec.get("text", "").strip()
            page_num = rec.get("page_number", 1)

            if not raw_text or len(raw_text.split()) < 5:
                continue

            # Section number extraction
            sec_num = sec_name.split(":")[0] if ":" in sec_name else sec_name

            # Sub-split long clauses if necessary
            text_segments = self._split_text_into_windows(raw_text)

            for seg in text_segments:
                chunk_id = f"{doc_id}-c{chunk_idx:03d}"
                citation = self.format_citation(
                    regulator=regulator,
                    circular_number=circular_number,
                    section_number=sec_num,
                    clause_number=clause_num,
                    page_number=page_num
                )
                header = self.create_context_header(
                    regulator=regulator,
                    circular_number=circular_number,
                    title=title,
                    section_number=sec_num,
                    clause_number=f"{clause_num} {clause_title}".strip(),
                    page_number=page_num
                )
                full_content = f"{header}{seg}"

                metadata = ChunkMetadata(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    regulator=regulator,
                    title=title,
                    circular_number=circular_number,
                    issue_date=issue_date,
                    section_number=sec_num,
                    section_title=sec_name,
                    clause_number=clause_num,
                    page_number=page_num,
                    citation=citation
                )

                chunk = DocumentChunk(
                    chunk_id=chunk_id,
                    content=full_content,
                    raw_text=seg,
                    metadata=metadata
                )
                chunks.append(chunk)
                chunk_idx += 1

        return chunks
