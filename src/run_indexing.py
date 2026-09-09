"""CLI script to build corpus, execute dual-indexing, and verify test queries."""

import argparse
from rich.console import Console
from rich.table import Table

from src.indexing.hybrid_indexer import HybridIndexer

console = Console()


def run_pipeline(force: bool = False):
    """Run dual indexing and verify retrieval against key regulatory queries."""
    indexer = HybridIndexer()
    status = indexer.index_all(force_reindex=force)
    console.print(f"[bold green]Index Status:[/bold green] {status}")

    # Acceptance Test Queries: Exact regulatory codes + natural language queries
    test_queries = [
        # Exact statutory/circular codes (sparse test)
        "Section 138 Negotiable Instruments Act statutory demand notice",
        "Section 45-IA Reserve Bank of India Act Net Owned Fund",
        "RBI/2022-23/111 Digital Lending Guidelines cooling-off period",
        "Regulation 30 SEBI LODR material disclosure timelines",
        # Natural language / conceptual compliance queries (dense test)
        "What are the requirements for Video KYC and customer presence?",
        "What is the penalty for issuing unsolicited credit cards?",
        "Within how many hours must banks report severe cyber incidents to RBI?",
        "What is the maximum default loss guarantee percentage in digital lending?"
    ]

    for q in test_queries:
        table = Table(title=f"Retrieval Results for: '{q}'", show_lines=True)
        table.add_column("Type", style="cyan", width=10)
        table.add_column("Rank", style="magenta", width=6)
        table.add_column("Score", style="green", width=8)
        table.add_column("Citation", style="yellow", width=40)
        table.add_column("Content Preview", style="white")

        # Dense query
        dense_hits = indexer.search_dense(q, top_k=2)
        for h in dense_hits:
            table.add_row(
                "Dense",
                str(h.rank),
                f"{h.score:.3f}",
                h.metadata.citation,
                h.content[h.content.find(']') + 2:h.content.find(']') + 140] + "..."
            )

        # Sparse query
        sparse_hits = indexer.search_sparse(q, top_k=2)
        for h in sparse_hits:
            table.add_row(
                "Sparse",
                str(h.rank),
                f"{h.score:.3f}",
                h.metadata.citation,
                h.content[h.content.find(']') + 2:h.content.find(']') + 140] + "..."
            )

        console.print(table)
        console.print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and verify regulatory dual indices.")
    parser.add_argument("--force", action="store_true", help="Force rebuild of PDFs and indices.")
    args = parser.parse_args()
    run_pipeline(force=args.force)
