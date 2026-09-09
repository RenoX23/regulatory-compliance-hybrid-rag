"""Unit tests for PDF parsing and section-aware chunking."""

from pathlib import Path
from src.ingestion.corpus_data import REGULATORY_DOCUMENTS
from src.ingestion.pdf_generator import generate_regulatory_pdf
from src.ingestion.pdf_parser import RegulatoryPDFParser
from src.ingestion.chunker import SectionAwareChunker
from src.schemas import Regulator


def test_pdf_generation_and_parsing(tmp_path):
    """Test generating a regulatory PDF and parsing it with PyMuPDF."""
    doc_sample = REGULATORY_DOCUMENTS[0]  # NBFC SBR
    pdf_path = tmp_path / f"{doc_sample['doc_id']}.pdf"

    generated = generate_regulatory_pdf(doc_sample, pdf_path)
    assert generated.exists()
    assert generated.stat().st_size > 1000

    parser = RegulatoryPDFParser()
    pages = parser.extract_pages(generated)
    assert len(pages) >= 1

    first_page_text = pages[0].text
    header = parser.parse_document_header(first_page_text)
    assert header["regulator"] == "RBI"
    assert "RBI/2023-24/102" in header["circular_number"]

    clauses = parser.parse_clauses_from_page(pages[0])
    assert len(clauses) >= 1
    assert any("45-IA" in c.get("section", "") or "45-IA" in c.get("clause_number", "") or "45-IA" in c.get("text", "") for c in clauses)


def test_section_aware_chunker():
    """Test that SectionAwareChunker prepends canonical context headers and builds valid chunks."""
    chunker = SectionAwareChunker(target_chunk_size=100, chunk_overlap=20)

    sample_clauses = [
        {
            "section": "Section 138: Cheque Dishonour",
            "clause_number": "Clause 138(b)",
            "clause_title": "Notice Requirement",
            "text": "The payee shall issue a statutory demand notice within thirty days of receiving memo of dishonour from the bank.",
            "page_number": 1
        }
    ]

    chunks = chunker.chunk_document(
        doc_id="ni-act-138",
        regulator=Regulator.STATUTORY,
        title="Negotiable Instruments Act",
        circular_number="Act 26 of 1881",
        issue_date="1881-12-09",
        clause_records=sample_clauses
    )

    assert len(chunks) == 1
    chunk = chunks[0]
    assert chunk.chunk_id == "ni-act-138-c001"
    assert "[REGULATOR: STATUTORY" in chunk.content
    assert "CIRCULAR: Act 26 of 1881" in chunk.content
    assert "SECTION: Section 138" in chunk.content
    assert "Page 1" in chunk.metadata.citation
    assert "thirty days" in chunk.raw_text
