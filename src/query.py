"""CLI interface for querying the Regulatory Compliance Hybrid RAG Pipeline."""

import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.generation.pipeline import RegulatoryRAGPipeline
from src.schemas import QueryRequest, Regulator

console = Console()


def run_query(
    query_str: str,
    top_k: int = 3,
    regulator: str = None,
    no_rerank: bool = False
):
    """Execute query through pipeline and print structured audit report."""
    pipeline = RegulatoryRAGPipeline()

    reg_filter = None
    if regulator:
        try:
            reg_filter = Regulator(regulator.upper())
        except ValueError:
            console.print(f"[red]Invalid regulator '{regulator}'. Must be RBI, SEBI, or STATUTORY.[/red]")
            sys.exit(1)

    req = QueryRequest(
        query=query_str,
        top_k=top_k,
        regulator_filter=reg_filter,
        enable_reranking=not no_rerank
    )

    console.print(f"\n[bold cyan]Executing Compliance Audit Query:[/bold cyan] {query_str}\n")
    resp = pipeline.query(req)

    # 1. Answer Panel
    grounding_status = "[green]GROUNDED WITH OFFICIAL CITATIONS[/green]" if resp.grounded else "[yellow]UNVERIFIED / DECLINED[/yellow]"
    console.print(
        Panel(
            resp.answer,
            title=f"Regulatory Determination ({grounding_status} - Confidence: {resp.confidence_score:.3f})",
            border_style="green" if resp.grounded else "yellow"
        )
    )

    # 2. Citations Table
    if resp.citations:
        cite_table = Table(title="Verified Regulatory Citations", show_lines=True)
        cite_table.add_column("#", style="cyan", width=4)
        cite_table.add_column("Citation", style="yellow")
        for idx, c in enumerate(resp.citations, start=1):
            cite_table.add_row(str(idx), c)
        console.print(cite_table)

    # 3. Context Passages Table
    ctx_table = Table(title="Top Context Passages Used", show_lines=True)
    ctx_table.add_column("Rank", style="magenta", width=6)
    ctx_table.add_column("Score", style="green", width=8)
    ctx_table.add_column("Citation", style="yellow", width=36)
    ctx_table.add_column("Excerpt", style="white")

    for c in resp.retrieved_chunks:
        ctx_table.add_row(
            str(c.rank),
            f"{c.score:.3f}",
            c.metadata.citation,
            c.content[c.content.find(']') + 2:c.content.find(']') + 140] + "..."
        )
    console.print(ctx_table)

    # 4. Latency Breakdown
    lat_table = Table(title="Latency Breakdown (ms)", show_lines=True)
    lat_table.add_column("Stage", style="cyan")
    lat_table.add_column("Time (ms)", style="green")
    for stage, ms in resp.latency_breakdown_ms.items():
        lat_table.add_row(stage, f"{ms:.2f}")
    console.print(lat_table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the Regulatory Compliance Hybrid RAG Pipeline.")
    parser.add_argument("query", nargs="?", default="What is the statutory notice period for cheque bounce under Section 138 of NI Act?", help="Compliance question")
    parser.add_argument("--top-k", type=int, default=3, help="Number of context passages")
    parser.add_argument("--regulator", type=str, choices=["RBI", "SEBI", "STATUTORY"], default=None, help="Filter by regulator")
    parser.add_argument("--no-rerank", action="store_true", help="Disable cross-encoder reranking")
    args = parser.parse_args()

    run_query(
        query_str=args.query,
        top_k=args.top_k,
        regulator=args.regulator,
        no_rerank=args.no_rerank
    )
