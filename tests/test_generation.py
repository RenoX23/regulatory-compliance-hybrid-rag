"""Unit tests for generation, prompt building, and citation verification."""

from src.generation.citations import CitationValidator
from src.generation.prompts import build_rag_prompt
from src.generation.llm import DeterministicComplianceGenerator
from src.schemas import ChunkMetadata, Regulator, RetrievalResult


def create_sample_retrieval():
    meta = ChunkMetadata(
        chunk_id="test-card-c001",
        doc_id="test-card",
        regulator=Regulator.RBI,
        title="Credit Card Directions",
        circular_number="RBI/2022-23/92",
        issue_date="2022-04-21",
        section_number="Chapter II",
        clause_number="Clause 6(a)",
        page_number=1,
        citation="RBI - [RBI/2022-23/92] - Chapter II - (Clause 6(a)) - Page 1"
    )
    return RetrievalResult(
        chunk_id="test-card-c001",
        content="Card-issuers shall not issue unsolicited credit cards. In case of unsolicited cards, the issuer shall pay a penalty of twice the credit limit.",
        metadata=meta,
        score=0.92,
        retrieval_type="reranked",
        rank=1
    )


def test_build_rag_prompt():
    """Verify prompt formatting includes verified context and structured directives."""
    chunk = create_sample_retrieval()
    prompt = build_rag_prompt("What is the penalty for unsolicited cards?", [chunk])
    assert "VERIFIED REGULATORY CONTEXT:" in prompt
    assert "RBI/2022-23/92" in prompt
    assert "Clause 6(a)" in prompt
    assert "AUDITOR QUERY:" in prompt


def test_citation_validator_valid():
    """Verify that matching citations are verified successfully."""
    validator = CitationValidator()
    chunk = create_sample_retrieval()
    answer_text = (
        "Under RBI directions, the penalty is twice the credit limit "
        "[Citation: RBI - [RBI/2022-23/92] - Chapter II - (Clause 6(a)) - Page 1]."
    )

    is_grounded, verified, ungrounded = validator.verify_citations(answer_text, [chunk])
    assert is_grounded is True
    assert len(verified) == 1
    assert len(ungrounded) == 0


def test_citation_validator_hallucinated():
    """Verify that fake or hallucinated citations are flagged."""
    validator = CitationValidator()
    chunk = create_sample_retrieval()
    hallucinated_text = (
        "The penalty is fixed at 1 lakh rupees "
        "[Citation: SEBI - [SEBI/FAKE/999] - Section 99 - Page 42]."
    )

    is_grounded, verified, ungrounded = validator.verify_citations(hallucinated_text, [chunk])
    assert is_grounded is False
    assert len(ungrounded) == 1
    assert "SEBI/FAKE/999" in ungrounded[0]


def test_deterministic_generator_fallback():
    """Verify fallback response when contexts are empty or score is below threshold."""
    gen = DeterministicComplianceGenerator()
    resp = gen.generate("Some out-of-domain question", [])
    assert "INSUFFICIENT_REGULATORY_EVIDENCE" in resp
