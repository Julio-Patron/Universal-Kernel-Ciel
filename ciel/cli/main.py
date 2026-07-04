import typer
from pathlib import Path

app = typer.Typer(help="Ciel Kernel V0 CLI")

@app.command()
def analyze(path: Path = typer.Argument(..., help="Path to the repository to analyze")):
    """Ejecuta el análisis completo del repositorio."""
    typer.echo(f"Analyzing repository at {path}")

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
    typer.echo(f"Detecting gap for repository at {path}")

@app.command()
def report(
    path: Path = typer.Argument(..., help="Path to the repository"),
    format: str = typer.Option("markdown", "--format", help="Formato de salida (json o markdown)")
):
    """Exporta el reporte del análisis."""
    typer.echo(f"Generating report for repository at {path} in {format} format")

if __name__ == "__main__":
    app()
