"""Unit tests for dense vector indexing and sparse BM25 indexing."""

from src.indexing.sparse_index import RegulatoryTokenizer, BM25Index
from src.indexing.dense_index import ChromaDenseIndex
from src.schemas import ChunkMetadata, DocumentChunk, Regulator


def create_sample_chunks():
    """Helper to build representative regulatory test chunks."""
    c1 = DocumentChunk(
        chunk_id="test-nbfc-c001",
        content="[REGULATOR: RBI | SECTION: Section 45-IA] In terms of Section 45-IA of the RBI Act 1934, no NBFC shall operate without Certificate of Registration and Net Owned Fund of 10 crore.",
        raw_text="In terms of Section 45-IA of the RBI Act 1934, no NBFC shall operate without Certificate of Registration and Net Owned Fund of 10 crore.",
        metadata=ChunkMetadata(
            chunk_id="test-nbfc-c001",
            doc_id="test-nbfc",
            regulator=Regulator.RBI,
            title="NBFC Directions",
            circular_number="RBI/2023-24/102",
            issue_date="2023-10-19",
            section_number="Section 45-IA",
            citation="RBI - [RBI/2023-24/102] - Section 45-IA - Page 1"
        )
    )
    c2 = DocumentChunk(
        chunk_id="test-ni-c001",
        content="[REGULATOR: STATUTORY | SECTION: Section 138] Section 138 of Negotiable Instruments Act: Dishonour of cheque for insufficiency of funds requires statutory demand notice within 30 days.",
        raw_text="Section 138 of Negotiable Instruments Act: Dishonour of cheque for insufficiency of funds requires statutory demand notice within 30 days.",
        metadata=ChunkMetadata(
            chunk_id="test-ni-c001",
            doc_id="test-ni",
            regulator=Regulator.STATUTORY,
            title="Negotiable Instruments Act",
            circular_number="Act 26 of 1881",
            issue_date="1881-12-09",
            section_number="Section 138",
            citation="STATUTORY - [Act 26 of 1881] - Section 138 - Page 1"
        )
    )
    c3 = DocumentChunk(
        chunk_id="test-digi-c001",
        content="[REGULATOR: RBI | SECTION: Digital Lending] Digital lending guidelines require mandatory cooling-off period of minimum 3 days for borrowers to exit loan without penalty.",
        raw_text="Digital lending guidelines require mandatory cooling-off period of minimum 3 days for borrowers to exit loan without penalty.",
        metadata=ChunkMetadata(
            chunk_id="test-digi-c001",
            doc_id="test-digi",
            regulator=Regulator.RBI,
            title="Digital Lending Guidelines",
            circular_number="RBI/2022-23/111",
            issue_date="2022-09-02",
            section_number="Section B",
            citation="RBI - [RBI/2022-23/111] - Section B - Page 1"
        )
    )
    return [c1, c2, c3]


def test_regulatory_tokenizer():
    """Verify domain-specific tokenization preserves legal codes."""
    tok = RegulatoryTokenizer()
    tokens = tok.tokenize("Section 45-IA and RBI/2023-24/102 with SMA-0")
    assert "section" in tokens
    assert "45-ia" in tokens
    assert "45" in tokens
    assert "ia" in tokens
    assert "rbi/2023-24/102" in tokens
    assert "sma-0" in tokens


def test_bm25_exact_code_matching():
    """Verify BM25 returns top hit for exact alphanumeric regulatory codes."""
    chunks = create_sample_chunks()
    bm25_idx = BM25Index()
    bm25_idx.build(chunks)

    # Test exact query for Section 138
    res_138 = bm25_idx.query("Section 138 demand notice", top_k=2)
    assert len(res_138) > 0
    assert res_138[0].chunk_id == "test-ni-c001"

    # Test exact query for Section 45-IA
    res_45ia = bm25_idx.query("Section 45-IA Net Owned Fund", top_k=2)
    assert len(res_45ia) > 0
    assert res_45ia[0].chunk_id == "test-nbfc-c001"


def test_dense_semantic_matching(tmp_path):
    """Verify ChromaDenseIndex stores embeddings and retrieves semantically relevant text."""
    chunks = create_sample_chunks()
    dense_idx = ChromaDenseIndex(
        persist_dir=tmp_path / "chroma_test",
        collection_name="test_collection"
    )
    dense_idx.add_chunks(chunks)
    assert dense_idx.count() == 3

    # Natural language query without using the exact phrase 'cooling-off period'
    nl_query = "What is the look-up window for borrowers to cancel an online loan without fees?"
    res = dense_idx.query(nl_query, top_k=1)
    assert len(res) == 1
    assert res[0].chunk_id == "test-digi-c001"
    assert res[0].score > 0.4
