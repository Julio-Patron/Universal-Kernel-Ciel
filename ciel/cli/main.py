import typer
from pathlib import Path

app = typer.Typer(help="Ciel Kernel V0 CLI")

@app.command()
def analyze(path: Path = typer.Argument(..., help="Path to the repository to analyze")):
    """Ejecuta el análisis completo del repositorio."""
    from ciel.rag.file_scanner import scan_repository
    from ciel.orchestrator.source_role_assignment import assign_role
    from ciel.rag.evidence_extractor import extract_evidence
    from ciel.orchestrator.reasoning_orchestrator import orchestrate_reasoning
    from ciel.cli.render import render_terminal
    
    files = scan_repository(path)
    roles = [assign_role(f, path) for f in files]
    bundle = extract_evidence(path, roles)
    
    report = orchestrate_reasoning(bundle)
    render_terminal(report)

@app.command()
def purpose(prompt: str = typer.Argument(..., help="Prompt para resolver el propósito")):
    """Devuelve el PurposeObject resolviendo una petición ambigua."""
    from ciel.orchestrator.purpose_resolver import resolve_purpose
    
    purpose_obj = resolve_purpose(prompt)
    typer.echo(purpose_obj.model_dump_json(indent=2))

@app.command()
def sources(path: Path = typer.Argument(..., help="Path to the repository")):
    """Muestra el Source Role Assignment para el repositorio."""
    from ciel.rag.file_scanner import scan_repository
    from ciel.orchestrator.source_role_assignment import assign_role
    import json
    
    files = scan_repository(path)
    roles = [assign_role(f, path) for f in files]
    output = [r.model_dump() for r in roles]
    
    typer.echo(json.dumps(output, indent=2))

@app.command()
def gap(path: Path = typer.Argument(..., help="Path to the repository")):
    """Ejecuta solo la detección de brecha entre intención y realidad."""
    from ciel.rag.file_scanner import scan_repository
    from ciel.orchestrator.source_role_assignment import assign_role
    from ciel.rag.evidence_extractor import extract_evidence
    from ciel.skills.detect_implementation_gap import detect_gap
    import json
    
    files = scan_repository(path)
    roles = [assign_role(f, path) for f in files]
    bundle = extract_evidence(path, roles)
    
    gap_matrix = detect_gap(bundle)
    output = [g.model_dump() for g in gap_matrix]
    
    typer.echo(json.dumps(output, indent=2))

@app.command()
def report(
    path: Path = typer.Argument(..., help="Path to the repository"),
    format: str = typer.Option("markdown", "--format", help="Formato de salida (json o markdown)")
):
    """Exporta el reporte del análisis."""
    from ciel.rag.file_scanner import scan_repository
    from ciel.orchestrator.source_role_assignment import assign_role
    from ciel.rag.evidence_extractor import extract_evidence
    from ciel.orchestrator.reasoning_orchestrator import orchestrate_reasoning
    from ciel.cli.render import render_json, render_markdown
    
    files = scan_repository(path)
    roles = [assign_role(f, path) for f in files]
    bundle = extract_evidence(path, roles)
    
    report_obj = orchestrate_reasoning(bundle)
    
    if format.lower() == "json":
        typer.echo(render_json(report_obj))
    else:
        typer.echo(render_markdown(report_obj))

if __name__ == "__main__":
    app()
