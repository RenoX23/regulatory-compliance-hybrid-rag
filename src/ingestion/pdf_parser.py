"""PDF Parser for Regulatory Compliance Documents.

Uses PyMuPDF to extract text, document metadata, section headers,
and clause divisions with accurate page number tracking.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional
import pymupdf as fitz

from src.schemas import Regulator


class ParsedPage:
    """Container for extracted text and metadata from a single PDF page."""

    def __init__(self, page_number: int, text: str):
        self.page_number = page_number
        self.text = text


class RegulatoryPDFParser:
    """Extracts text, structural divisions, and regulatory metadata from PDF files."""

    def __init__(self):
        # Regex patterns for regulatory metadata
        self.ref_pattern = re.compile(
            r"(?:Ref:|Circular No\.|Notification No\.|Act No\.)\s*([A-Za-z0-9\/\.\-\s]+?)(?:\s+Date|\n|$)",
            re.IGNORECASE
        )
        self.date_pattern = re.compile(
            r"Date:\s*(\d{4}-\d{2}-\d{2}|\d{1,2}[-\/]\d{1,2}[-\/]\d{2,4})",
            re.IGNORECASE
        )
        self.regulator_pattern = re.compile(
            r"\b(RBI|SEBI|STATUTORY)\b",
            re.IGNORECASE
        )
        self.section_pattern = re.compile(
            r"\[(Section\s+[A-Za-z0-9\-]+|Chapter\s+[A-Za-z0-9\-]+|Regulation\s+[A-Za-z0-9\-]+|Schedule\s+[A-Za-z0-9\-]+|Clause\s+[A-Za-z0-9\-]+)\]\s*(.*?)(?=\n|$)",
            re.IGNORECASE
        )
        self.clause_pattern = re.compile(
            r"^((?:Clause|Section|Regulation|Rule)\s+[A-Za-z0-9\.\(\)\-]+)\s*[-:]\s*(.*?)$",
            re.MULTILINE
        )

    def extract_pages(self, pdf_path: Path) -> List[ParsedPage]:
        """Extract text from each page of the PDF file."""
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        doc = fitz.open(str(pdf_path))
        pages: List[ParsedPage] = []
        for idx, page in enumerate(doc):
            text = page.get_text("text")
            pages.append(ParsedPage(page_number=idx + 1, text=text))
        doc.close()
        return pages

    def parse_document_header(self, first_page_text: str) -> Dict[str, Any]:
        """Extract document-level header metadata from first page text."""
        header_data: Dict[str, Any] = {
            "regulator": "STATUTORY",
            "circular_number": "UNKNOWN",
            "issue_date": "UNKNOWN",
            "title": "",
            "subject": ""
        }

        # Regulator
        reg_match = self.regulator_pattern.search(first_page_text)
        if reg_match:
            val = reg_match.group(1).upper()
            header_data["regulator"] = val

        # Circular reference
        ref_match = self.ref_pattern.search(first_page_text)
        if ref_match:
            header_data["circular_number"] = ref_match.group(1).strip()

        # Issue date
        date_match = self.date_pattern.search(first_page_text)
        if date_match:
            header_data["issue_date"] = date_match.group(1).strip()

        # Subject
        subj_match = re.search(r"Subject:\s*(.*?)(?=\n\[|\nSection|\nChapter|\nClause|$)", first_page_text, re.DOTALL)
        if subj_match:
            header_data["subject"] = " ".join(subj_match.group(1).split()[:30])

        return header_data

    def parse_clauses_from_page(self, page: ParsedPage) -> List[Dict[str, Any]]:
        """Parse structured clauses and sections from a single page's text."""
        lines = page.text.split("\n")
        clauses = []
        current_section = "General"
        current_clause_num = ""
        current_clause_title = ""
        clause_body_lines: List[str] = []

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Check for Section header
            sec_match = self.section_pattern.search(line_str)
            if sec_match:
                if clause_body_lines and current_clause_num:
                    clauses.append({
                        "section": current_section,
                        "clause_number": current_clause_num,
                        "clause_title": current_clause_title,
                        "text": " ".join(clause_body_lines),
                        "page_number": page.page_number
                    })
                    clause_body_lines = []
                    current_clause_num = ""
                    current_clause_title = ""
                current_section = f"{sec_match.group(1)}: {sec_match.group(2)}".strip()
                continue

            # Check for Clause heading
            cl_match = self.clause_pattern.match(line_str)
            if cl_match:
                if clause_body_lines and current_clause_num:
                    clauses.append({
                        "section": current_section,
                        "clause_number": current_clause_num,
                        "clause_title": current_clause_title,
                        "text": " ".join(clause_body_lines),
                        "page_number": page.page_number
                    })
                    clause_body_lines = []
                current_clause_num = cl_match.group(1).strip()
                current_clause_title = cl_match.group(2).strip()
                continue

            # Filter out footers and page markers
            if "Page " in line_str and " of " in line_str:
                continue
            if "Official Regulatory Reference:" in line_str:
                continue

            clause_body_lines.append(line_str)

        # Append trailing clause
        if clause_body_lines:
            clauses.append({
                "section": current_section,
                "clause_number": current_clause_num or "Clause",
                "clause_title": current_clause_title,
                "text": " ".join(clause_body_lines),
                "page_number": page.page_number
            })

        return clauses
