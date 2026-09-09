"""Quantitative Evaluation Metrics for Regulatory Compliance RAG.

Implements Information Retrieval and Ragas-style evaluation metrics:
- Context Precision / Mean Reciprocal Rank (MRR)
- Context Recall / Hit Rate @ K
- Faithfulness (Anti-hallucination fidelity)
- Answer Relevancy (Semantic similarity to ground truth)
- Citation Precision (Accuracy of cited circulars)
- Refusal Accuracy (Out-of-domain defense)
"""

import re
from typing import Dict, List, Set, Tuple
import numpy as np
from src.schemas import RetrievalResult


def compute_reciprocal_rank(
    retrieved_chunks: List[RetrievalResult],
    target_doc_id: str,
    target_section: str = "",
    target_clause: str = ""
) -> float:
    """Calculate reciprocal rank (1 / rank) for the target document and section/clause."""
    if not retrieved_chunks or target_doc_id == "none":
        return 0.0

    target_clean = target_doc_id.lower().replace("-", "")
    sec_clean = target_section.lower().replace(" ", "")
    clause_clean = target_clause.lower().replace(" ", "")

    for idx, c in enumerate(retrieved_chunks, start=1):
        doc_clean = c.metadata.doc_id.lower().replace("-", "")
        chunk_sec = c.metadata.section_number.lower().replace(" ", "")
        chunk_clause = c.metadata.clause_number.lower().replace(" ", "")
        chunk_content = c.content.lower()

        # Check document match
        if target_clean in doc_clean or doc_clean in target_clean:
            clause_match = clause_clean and (clause_clean in chunk_clause or clause_clean in chunk_content)
            sec_match = sec_clean and (sec_clean in chunk_sec or sec_clean in chunk_content)
            if clause_match or sec_match:
                return 1.0 / idx
            # If doc matches but wrong section/clause, penalize partial match
            return 0.35 / idx
    return 0.0


def compute_hit_at_k(
    retrieved_chunks: List[RetrievalResult],
    target_doc_id: str,
    k: int = 3
) -> float:
    """Check if target document appears in top-K retrieved candidates."""
    if target_doc_id == "none":
        return 1.0 if not retrieved_chunks else 0.0

    target_clean = target_doc_id.lower().replace("-", "")
    for c in retrieved_chunks[:k]:
        doc_clean = c.metadata.doc_id.lower().replace("-", "")
        if target_clean in doc_clean or doc_clean in target_clean:
            return 1.0
    return 0.0


def compute_citation_precision(
    extracted_citations: List[str],
    expected_citation: str
) -> float:
    """Evaluate whether generated citations correctly reference the expected circular."""
    if expected_citation == "NONE":
        return 1.0 if not extracted_citations else 0.0

    if not extracted_citations:
        return 0.0

    expected_tokens = set(re.findall(r"[A-Za-z0-9]+", expected_citation.lower()))
    matches = 0
    for cite in extracted_citations:
        cite_tokens = set(re.findall(r"[A-Za-z0-9]+", cite.lower()))
        common = expected_tokens.intersection(cite_tokens)
        if len(common) >= 2:
            matches += 1

    return float(matches) / max(1.0, float(len(extracted_citations)))


def compute_faithfulness_score(
    answer: str,
    retrieved_chunks: List[RetrievalResult]
) -> float:
    """Compute faithfulness score: proportion of answer content entailed by context."""
    if "INSUFFICIENT_REGULATORY_EVIDENCE" in answer:
        return 1.0

    if not retrieved_chunks:
        return 0.0

    # Combine context text
    context_text = " ".join([c.content.lower() for c in retrieved_chunks])
    context_words = set(re.findall(r"\b[a-z0-9]{3,}\b", context_text))

    # Extract informative content words from answer
    answer_words = re.findall(r"\b[a-z0-9]{3,}\b", answer.lower())
    # Exclude common boilerplate words
    boilerplate = {
        "the", "and", "under", "for", "with", "this", "that", "shall",
        "compliance", "audit", "determination", "finding", "findings",
        "relevant", "provisions", "governing", "official", "directives",
        "below", "mandatory", "citations", "established", "summarized"
    }
    content_words = [w for w in answer_words if w not in boilerplate]
    if not content_words:
        return 1.0

    grounded_count = sum(1 for w in content_words if w in context_words)
    return float(grounded_count) / float(len(content_words))


def compute_refusal_accuracy(
    query_category: str,
    answer: str
) -> float:
    """Evaluate whether adversarial out-of-domain queries are correctly declined."""
    if query_category != "adversarial_negative":
        return 1.0

    declined = "INSUFFICIENT_REGULATORY_EVIDENCE" in answer
    return 1.0 if declined else 0.0
