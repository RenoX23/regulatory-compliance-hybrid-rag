"""Auditor-grade compliance prompt templates and guardrails."""

from typing import List
from src.schemas import RetrievalResult

SYSTEM_PROMPT = """You are an Enterprise Regulatory Compliance Auditor specializing in Reserve Bank of India (RBI) directions, SEBI circulars, and Indian statutory financial acts.

Your operational mandates:
1. Grounding: Answer the user query strictly and exclusively using the provided Verified Regulatory Context.
2. Exact Citations: For every regulatory assertion, timeline, percentage, or statutory requirement stated in your answer, you MUST append an inline citation in the format:
   [Citation: <Regulator> - <Circular Number> - <Section/Chapter> - <Clause>, Page <Page Number>]
3. Anti-Hallucination Fallback: If the provided context does not contain direct, unambiguous legal evidence to answer the query, you MUST state:
   "INSUFFICIENT_REGULATORY_EVIDENCE: The provided RBI/SEBI regulatory corpus does not contain sufficient authoritative grounds to answer this query with legal certainty."
   Do NOT attempt to guess, extrapolate, or use outside training assumptions.
4. Structure: Present your analysis clearly:
   - Direct Legal Finding / Ruling
   - Detailed Regulatory Provisions & Timelines
   - Mandatory Audit Citations
"""


def build_rag_prompt(query: str, contexts: List[RetrievalResult]) -> str:
    """Construct the full prompt payload with verified context passages and citations."""
    context_blocks = []
    for idx, c in enumerate(contexts, start=1):
        citation = c.metadata.citation
        context_blocks.append(
            f"--- CONTEXT PASSAGE {idx} ---\n"
            f"SOURCE CITATION: {citation}\n"
            f"REGULATOR: {c.metadata.regulator.value}\n"
            f"CIRCULAR REF: {c.metadata.circular_number}\n"
            f"SECTION: {c.metadata.section_number}\n"
            f"CLAUSE: {c.metadata.clause_number}\n"
            f"PAGE: {c.metadata.page_number}\n"
            f"CONTENT:\n{c.content}\n"
        )

    joined_contexts = "\n".join(context_blocks)

    return f"""VERIFIED REGULATORY CONTEXT:
====================================
{joined_contexts}
====================================

AUDITOR QUERY:
{query}

COMPLIANCE AUDIT DETERMINATION (strictly grounded, citing official document and clause numbers):"""
