"""Corpus Builder for Regulatory Compliance Hybrid RAG.

Coordinates corpus generation, manifest tracking, and end-to-end PDF ingestion.
"""

import json
from pathlib import Path
from typing import List, Optional
from rich.console import Console

from src.config import settings
from src.ingestion.corpus_data import REGULATORY_DOCUMENTS
from src.ingestion.pdf_generator import build_all_pdfs
from src.ingestion.pdf_parser import RegulatoryPDFParser
from src.ingestion.chunker import SectionAwareChunker
from src.schemas import DocumentChunk, Regulator

console = Console()


class CorpusBuilder:
    """Manages raw PDF generation, manifest tracking, and chunk ingestion."""

    def __init__(
        self,
        raw_dir: Optional[Path] = None,
        processed_dir: Optional[Path] = None,
        chunk_size: int = settings.CHUNK_SIZE,
        chunk_overlap: int = settings.CHUNK_OVERLAP
    ):
        self.raw_dir = raw_dir or settings.RAW_DATA_DIR
        self.processed_dir = processed_dir or settings.PROCESSED_DATA_DIR
        self.parser = RegulatoryPDFParser()
        self.chunker = SectionAwareChunker(target_chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def prepare_raw_corpus(self, force_regenerate: bool = False) -> List[Path]:
        """Generate official PDFs from structured corpus data if not present."""
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = self.raw_dir / "manifest.json"

        pdf_files = list(self.raw_dir.glob("*.pdf"))
        if len(pdf_files) >= len(REGULATORY_DOCUMENTS) and not force_regenerate and manifest_path.exists():
            console.print(f"[green]Raw PDF corpus already exists ({len(pdf_files)} documents). Skipping generation.[/green]")
            return pdf_files

        console.print(f"[bold blue]Rendering {len(REGULATORY_DOCUMENTS)} official regulatory PDFs into {self.raw_dir}...[/bold blue]")
        generated = build_all_pdfs(REGULATORY_DOCUMENTS, self.raw_dir)

        manifest = [
            {
                "doc_id": d["doc_id"],
                "regulator": d["regulator"],
                "title": d["title"],
                "circular_number": d["circular_number"],
                "issue_date": d["issue_date"],
                "subject": d["subject"],
                "filename": f"{d['doc_id']}.pdf"
            }
            for d in REGULATORY_DOCUMENTS
        ]
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        console.print(f"[green]Successfully rendered {len(generated)} regulatory PDFs and manifest.[/green]")
        return generated

    def ingest_corpus(self, force_reparse: bool = False) -> List[DocumentChunk]:
        """Ingest all raw PDFs and produce section-aware DocumentChunks."""
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        chunks_cache_path = self.processed_dir / "chunks.json"

        if chunks_cache_path.exists() and not force_reparse:
            console.print("[cyan]Loading cached DocumentChunks from disk...[/cyan]")
            with open(chunks_cache_path, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
            chunks = [DocumentChunk.model_validate(c) for c in raw_list]
            console.print(f"[green]Loaded {len(chunks)} DocumentChunks from cache.[/green]")
            return chunks

        # Ensure PDFs exist
        self.prepare_raw_corpus()

        # Build document lookup from corpus definition
        doc_meta_map = {d["doc_id"]: d for d in REGULATORY_DOCUMENTS}

        all_chunks: List[DocumentChunk] = []
        pdf_paths = sorted(list(self.raw_dir.glob("*.pdf")))

        console.print(f"[bold blue]Parsing and chunking {len(pdf_paths)} regulatory PDFs...[/bold blue]")
        for pdf_path in pdf_paths:
            doc_id = pdf_path.stem
            doc_info = doc_meta_map.get(doc_id, {})
            regulator = Regulator(doc_info.get("regulator", "STATUTORY"))
            title = doc_info.get("title", pdf_path.stem)
            circular_number = doc_info.get("circular_number", "UNKNOWN")
            issue_date = doc_info.get("issue_date", "UNKNOWN")

            pages = self.parser.extract_pages(pdf_path)
            all_clause_records = []
            for p in pages:
                clauses = self.parser.parse_clauses_from_page(p)
                all_clause_records.extend(clauses)

            doc_chunks = self.chunker.chunk_document(
                doc_id=doc_id,
                regulator=regulator,
                title=title,
                circular_number=circular_number,
                issue_date=issue_date,
                clause_records=all_clause_records
            )
            all_chunks.extend(doc_chunks)

        # Save to cache
        with open(chunks_cache_path, "w", encoding="utf-8") as f:
            json.dump([c.model_dump() for c in all_chunks], f, indent=2)

        console.print(f"[bold green]Total DocumentChunks generated: {len(all_chunks)} across {len(pdf_paths)} documents.[/bold green]")
        return all_chunks
