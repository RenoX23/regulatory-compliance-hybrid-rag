"""LLM Generation Layer with Grounding & Citation Guardrails."""

import os
from abc import ABC, abstractmethod
from typing import List, Optional
from rich.console import Console

from src.config import settings
from src.generation.prompts import SYSTEM_PROMPT, build_rag_prompt
from src.schemas import RetrievalResult

console = Console()


class BaseLLMGenerator(ABC):
    """Abstract interface for LLM answer generation."""

    @abstractmethod
    def generate(self, query: str, contexts: List[RetrievalResult]) -> str:
        """Generate compliance determination grounded in retrieved contexts."""
        pass


class GeminiGenerator(BaseLLMGenerator):
    """Gemini 1.5 Flash generator with strict system instructions."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        from google import genai
        from google.genai import types

        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model or settings.GEMINI_MODEL
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be set to use GeminiGenerator")

        self.client = genai.Client(api_key=self.api_key)
        self.types = types

    def generate(self, query: str, contexts: List[RetrievalResult]) -> str:
        prompt = build_rag_prompt(query, contexts)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=self.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.0,
                max_output_tokens=1024
            )
        )
        return response.text or ""


class GroqGenerator(BaseLLMGenerator):
    """Groq LLaMA 3.3 generator."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        from groq import Groq

        self.api_key = api_key or settings.GROQ_API_KEY
        self.model_name = model or settings.GROQ_MODEL
        if not self.api_key:
            raise ValueError("GROQ_API_KEY must be set to use GroqGenerator")

        self.client = Groq(api_key=self.api_key)

    def generate(self, query: str, contexts: List[RetrievalResult]) -> str:
        prompt = build_rag_prompt(query, contexts)
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=1024
        )
        return completion.choices[0].message.content or ""


class DeterministicComplianceGenerator(BaseLLMGenerator):
    """Deterministic local compliance synthesizer.

    Used when no external API key is active or during offline CI/unit testing.
    Extracts relevant legal sentences and formats strict citations without hallucination.
    """

    def generate(self, query: str, contexts: List[RetrievalResult]) -> str:
        if not contexts:
            return (
                "INSUFFICIENT_REGULATORY_EVIDENCE: The provided RBI/SEBI regulatory corpus "
                "does not contain sufficient authoritative grounds to answer this query with legal certainty."
            )

        top_chunk = contexts[0]
        # If the highest score is too low, invoke fallback
        if top_chunk.score < settings.MIN_CONFIDENCE_THRESHOLD:
            return (
                "INSUFFICIENT_REGULATORY_EVIDENCE: The provided RBI/SEBI regulatory corpus "
                "does not contain sufficient authoritative grounds to answer this query with legal certainty."
            )

        findings = []
        citations = []
        for idx, c in enumerate(contexts[:2], start=1):
            text_body = c.content.split("]\n", 1)[-1] if "]\n" in c.content else c.content
            findings.append(f"• Provision ({c.metadata.section_number} / {c.metadata.clause_number}): {text_body.strip()}")
            citations.append(f"[{c.metadata.citation}]")

        answer_lines = [
            "### COMPLIANCE AUDIT DETERMINATION",
            "",
            f"**Legal Finding**: The relevant regulatory provisions governing '{query}' are established under official directives as summarized below:",
            "",
            "\n\n".join(findings),
            "",
            "### MANDATORY AUDIT CITATIONS",
            " ".join(citations)
        ]
        return "\n".join(answer_lines)


def get_llm_generator() -> BaseLLMGenerator:
    """Factory selecting the best available LLM provider."""
    # Try Gemini if key is present
    if settings.GEMINI_API_KEY:
        try:
            return GeminiGenerator()
        except Exception as e:
            console.print(f"[yellow]Failed initializing GeminiGenerator ({e}), trying Groq...[/yellow]")

    # Try Groq if key is present
    if settings.GROQ_API_KEY:
        try:
            return GroqGenerator()
        except Exception as e:
            console.print(f"[yellow]Failed initializing GroqGenerator ({e}), using local deterministic synthesizer.[/yellow]")

    # Fallback to deterministic local generator
    console.print("[cyan]Using DeterministicComplianceGenerator (Local zero-cost / offline mode).[/cyan]")
    return DeterministicComplianceGenerator()


# Compatibility aliases
GeminiLLMGenerator = GeminiGenerator
GroqLLMGenerator = GroqGenerator
