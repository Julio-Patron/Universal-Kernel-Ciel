import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from ciel.schemas.gap_report import ImplementationGapReport

console = Console()

def render_json(report: ImplementationGapReport) -> str:
    """Returns the JSON string representation of the report."""
    return report.model_dump_json(indent=2)

def render_markdown(report: ImplementationGapReport) -> str:
    """Returns a nicely formatted Markdown representation of the report."""
    md = f"# Ciel Analysis Report: {report.project.name}\n\n"
    
    md += "## Verdict\n"
    md += f"**Stage:** {report.verdict.stage}\n\n"
    md += f"{report.verdict.summary}\n\n"
    md += f"**Main Bottleneck:** {report.verdict.main_bottleneck}\n\n"
    
    md += "## Maturity Score\n"
    md += f"- **Intention Clarity:** {report.maturity_score.intention_clarity}\n"
    md += f"- **Implementation Completeness:** {report.maturity_score.implementation_completeness}\n"
    md += f"- **Behavior Confidence:** {report.maturity_score.behavior_confidence}\n"
    md += f"- **Operational Readiness:** {report.maturity_score.operational_readiness}\n"
    md += f"- **Commercial Readiness:** {report.maturity_score.commercial_readiness}\n\n"
    
    md += "## Implementation Gap Matrix\n"
    md += "| Claim | Status | Severity | Recommended Action |\n"
    md += "|-------|--------|----------|--------------------|\n"
    for item in report.gap_matrix:
        md += f"| {item.claim} | {item.status} | {item.severity} | {item.recommended_action} |\n"
    
    md += "\n## Next Actions\n"
    for action in sorted(report.next_actions, key=lambda a: a.priority):
        md += f"{action.priority}. **{action.type.capitalize()}**: {action.description}\n"
        md += f"   *Reason*: {action.reason}\n"
        
    return md

def render_terminal(report: ImplementationGapReport):
    """Prints a rich terminal representation of the report."""
    
    console.print(Panel(f"[bold blue]Ciel Analysis Report:[/bold blue] {report.project.name}"))
    
    console.print(f"\n[bold]Verdict:[/bold] {report.verdict.stage} - {report.verdict.summary}")
    console.print(f"[bold red]Bottleneck:[/bold red] {report.verdict.main_bottleneck}\n")
    
    table = Table(title="Implementation Gap Matrix", show_header=True, header_style="bold magenta")
    table.add_column("Claim")
    table.add_column("Status")
    table.add_column("Severity")
    table.add_column("Action")
    
    for item in report.gap_matrix:
        status_color = "green" if item.status == "implemented" else "yellow"
        table.add_row(
            item.claim,
            f"[{status_color}]{item.status}[/{status_color}]",
            item.severity,
            item.recommended_action
        )
        
    console.print(table)
    
    console.print("\n[bold]Next Actions:[/bold]")
    for action in sorted(report.next_actions, key=lambda a: a.priority):
        console.print(f"  [bold cyan]{action.priority}. {action.type.upper()}[/bold cyan]: {action.description}")
        console.print(f"     [dim]Reason: {action.reason}[/dim]")
