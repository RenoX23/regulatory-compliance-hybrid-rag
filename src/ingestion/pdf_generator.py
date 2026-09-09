"""PDF Document Generator for Regulatory Compliance Corpus.

Uses PyMuPDF to render authentic multi-page PDFs with official regulatory
headers, section titles, and numbered legal clauses.
"""

from pathlib import Path
from typing import Any, Dict, List
import pymupdf as fitz


def generate_regulatory_pdf(doc_data: Dict[str, Any], output_path: Path) -> Path:
    """Generate a high-fidelity PDF from structured regulatory document data.

    Args:
        doc_data: Dictionary conforming to REGULATORY_DOCUMENTS schema.
        output_path: Destination path for the .pdf file.

    Returns:
        Path to the generated PDF.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()

    page = doc.new_page(width=595, height=842)  # A4 standard points
    margin_x = 50
    margin_y = 50
    curr_y = margin_y
    line_height = 14

    # Header Box / Title
    regulator = doc_data["regulator"]
    title = doc_data["title"]
    circular_num = doc_data["circular_number"]
    issue_date = doc_data["issue_date"]
    subject = doc_data["subject"]

    # Header title
    header_title = f"{regulator} REGULATORY COMPLIANCE DIRECTIVE"
    page.insert_text(
        (margin_x, curr_y),
        header_title,
        fontsize=12,
        fontname="helv",
        color=(0.1, 0.2, 0.4)
    )
    curr_y += 18

    # Reference and date
    page.insert_text(
        (margin_x, curr_y),
        f"Ref: {circular_num}",
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3)
    )
    page.insert_text(
        (430, curr_y),
        f"Date: {issue_date}",
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3)
    )
    curr_y += 15

    # Dividing rule
    page.draw_line(
        fitz.Point(margin_x, curr_y),
        fitz.Point(545, curr_y),
        color=(0.2, 0.4, 0.7),
        width=1.5
    )
    curr_y += 18

    # Main Title
    rect_title = fitz.Rect(margin_x, curr_y, 545, curr_y + 40)
    page.insert_textbox(
        rect_title,
        title,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0)
    )
    curr_y += 42

    # Subject line
    rect_subj = fitz.Rect(margin_x, curr_y, 545, curr_y + 35)
    page.insert_textbox(
        rect_subj,
        f"Subject: {subject}",
        fontsize=9,
        fontname="helv",
        color=(0.2, 0.2, 0.2)
    )
    curr_y += 40

    # Sections and Clauses
    for sec in doc_data.get("sections", []):
        sec_num = sec.get("section_number", "")
        sec_title = sec.get("section_title", "")

        # Check page overflow
        if curr_y > 720:
            page = doc.new_page(width=595, height=842)
            curr_y = margin_y

        sec_header = f"[{sec_num}] {sec_title}"
        page.insert_text(
            (margin_x, curr_y),
            sec_header,
            fontsize=10,
            fontname="helv",
            color=(0.1, 0.3, 0.6)
        )
        curr_y += 18

        for clause in sec.get("clauses", []):
            c_num = clause.get("clause_number", "")
            c_title = clause.get("clause_title", "")
            c_text = clause.get("text", "")

            clause_heading = f"{c_num} - {c_title}"
            if curr_y > 720:
                page = doc.new_page(width=595, height=842)
                curr_y = margin_y

            page.insert_text(
                (margin_x + 10, curr_y),
                clause_heading,
                fontsize=9,
                fontname="helv",
                color=(0.2, 0.2, 0.2)
            )
            curr_y += 15

            # Estimate textbox height needed
            words = c_text.split()
            estimated_lines = (len(words) // 12) + 2
            box_height = max(40, estimated_lines * line_height)

            if curr_y + box_height > 780:
                page = doc.new_page(width=595, height=842)
                curr_y = margin_y

            rect_body = fitz.Rect(margin_x + 15, curr_y, 540, curr_y + box_height)
            page.insert_textbox(
                rect_body,
                c_text,
                fontsize=8.5,
                fontname="helv",
                color=(0.05, 0.05, 0.05)
            )
            curr_y += box_height + 10

    # Footer on all pages
    total_pages = len(doc)
    for idx, p in enumerate(doc):
        p.insert_text(
            (margin_x, 810),
            f"Official Regulatory Reference: {circular_num}",
            fontsize=7,
            fontname="helv",
            color=(0.5, 0.5, 0.5)
        )
        p.insert_text(
            (480, 810),
            f"Page {idx + 1} of {total_pages}",
            fontsize=7,
            fontname="helv",
            color=(0.5, 0.5, 0.5)
        )

    doc.save(str(output_path))
    doc.close()
    return output_path


def build_all_pdfs(documents: List[Dict[str, Any]], target_dir: Path) -> List[Path]:
    """Render all documents in the corpus as PDFs in the target directory."""
    target_dir.mkdir(parents=True, exist_ok=True)
    created_paths = []
    for doc in documents:
        pdf_name = f"{doc['doc_id']}.pdf"
        dest_path = target_dir / pdf_name
        generate_regulatory_pdf(doc, dest_path)
        created_paths.append(dest_path)
    return created_paths
