"""Citation extractor and hallucination guardrail validator."""

import re
from typing import List, Set, Tuple
from src.schemas import RetrievalResult


class CitationValidator:
    """Validates citations in generated answers against provided context."""

    def __init__(self):
        # Matches [Citation: ...] or standard citation strings
        self.citation_tag_regex = re.compile(
            r"\[(?:Citation:\s*)?([^\]]+)\]",
            re.IGNORECASE
        )

    def extract_citations(self, text: str) -> List[str]:
        """Extract all citation brackets from answer text."""
        matches = self.citation_tag_regex.findall(text)
        citations = []
        for m in matches:
            clean_m = m.strip()
            # Filter out non-citation brackets like [1] or [REGULATOR: ...]
            if any(k in clean_m for k in ["RBI", "SEBI", "STATUTORY", "Act", "Page", "Section", "Clause"]):
                citations.append(clean_m)
        return list(dict.fromkeys(citations))  # Deduplicate preserving order

    def verify_citations(
        self,
        answer: str,
        retrieved_contexts: List[RetrievalResult]
    ) -> Tuple[bool, List[str], List[str]]:
        """Verify extracted citations against retrieved chunks.

        Returns:
            (is_grounded, verified_citations, ungrounded_citations)
        """
        extracted = self.extract_citations(answer)
        valid_citations: Set[str] = {c.metadata.citation.lower() for c in retrieved_contexts}
        valid_circs: Set[str] = {c.metadata.circular_number.lower() for c in retrieved_contexts if c.metadata.circular_number}

        verified: List[str] = []
        ungrounded: List[str] = []

        for cite in extracted:
            cite_lower = cite.lower()
            # Check direct match or substring circular match
            is_valid = (
                any(vc in cite_lower or cite_lower in vc for vc in valid_citations) or
                any(circ in cite_lower for circ in valid_circs)
            )
            if is_valid:
                verified.append(cite)
            else:
                ungrounded.append(cite)

        # Answer is grounded if it has at least one verified citation and no hallucinated circulars
        is_grounded = len(verified) > 0 and len(ungrounded) == 0
        return is_grounded, verified, ungrounded
