import typer
from pathlib import Path

app = typer.Typer(help="Ciel Kernel V0 CLI")

@app.command()
def analyze(
    path: Path = typer.Argument(..., help="Path to the repository to analyze"),
    scope: str = typer.Option(None, "--scope", help="Filtrar por ID de boundary (ej. frontend, backend)"),
    ruleset: str = typer.Option(None, "--ruleset", help="ID del ruleset a aplicar (ej. agent-safe-repo)")
):
    """Ejecuta el análisis completo del repositorio a través del ciclo cognitivo V2."""
    from ciel.rag.file_scanner import scan_repository
    from ciel.orchestrator.source_role_assignment import assign_role
    from ciel.rag.evidence_extractor import extract_evidence
    from ciel.orchestrator.reasoning_orchestrator import orchestrate_reasoning
    from ciel.cli.render import render_terminal
    from ciel.orchestrator.purpose_resolver import resolve_purpose
    from ciel.memory.decision_ledger import DecisionLedger
    from ciel.skills.detect_product_boundaries import identify_boundaries
    from ciel.skills.load_rulesets import load_ruleset
    import time
    
    ledger = DecisionLedger(path)
    
    active_ruleset = None
    if ruleset:
        typer.echo(f"\n>> Phase -1: Loading Policy Ruleset '{ruleset}'...")
        try:
            active_ruleset = load_ruleset(ruleset, search_paths=[path / "rulesets", Path.cwd() / "rulesets"])
            typer.secho(f"   [OK] Loaded {active_ruleset.id} (hash: {active_ruleset.hash[:8]})", fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"   [ERROR] {e}", fg=typer.colors.RED)
            raise typer.Exit(1)
            
    typer.secho("\n[COGNITIVE CYCLE START] Initializing Ciel V2 Intelligence Layer...", fg=typer.colors.CYAN, bold=True)
    
    typer.echo("\n>> Phase 0: Map Product Boundaries...")
    boundaries = identify_boundaries(path)
    ledger.record_decision(
        "boundary_detection",
        context={"repo_path": str(path)},
        decision={"boundaries": [b.model_dump() for b in boundaries]}
    )
    
    # Phase 11: Purpose Resolution
    typer.echo("\n>> Phase 11: Resolving Project Purpose from Documentation...")
    start_time = time.time()
    purpose_obj = resolve_purpose(
        "Analyze this repository and identify gaps between documentation intent and code reality.", 
        repo_path=str(path)
    )
    ledger.record_decision(
        "purpose_resolution", 
        context="Analyze this repository and identify gaps between documentation intent and code reality.",
        decision={"task": purpose_obj.task.type, "question": purpose_obj.purpose.primary_question}
    )
    typer.secho(f"   [OK] Identified Task: {purpose_obj.task.type} | {purpose_obj.purpose.primary_question}", fg=typer.colors.GREEN)
    
    # Phase 12: Evidence Extraction
    typer.echo("\n>> Phase 12: Extracting Implementation Facts from Reality...")
    files = scan_repository(path)
    roles = [assign_role(f, path, boundaries) for f in files]
    
    if scope:
        roles = [r for r in roles if r.boundary_id == scope or (scope in (r.boundary_id or ""))]
        typer.secho(f"   [!] Scope filtering applied: '{scope}'. Kept {len(roles)} files.", fg=typer.colors.YELLOW)
        
    bundle = extract_evidence(path, roles)
    ledger.record_decision(
        "evidence_extraction",
        context={"files_scanned": len(files), "path": str(path)},
        decision={"facts": len(bundle.implementation_facts), "claims": len(bundle.intention_claims)}
    )
    typer.secho(f"   [OK] Extracted {len(bundle.implementation_facts)} Implementation Facts & {len(bundle.intention_claims)} Intention Claims.", fg=typer.colors.GREEN)
    
    # Phase 13 & 14: Gap Detection & Maturity Audit
    typer.echo("\n>> Phase 13 & 14: Semantic Reasoning & Gap Auditing...")
    report = orchestrate_reasoning(bundle, ruleset=active_ruleset)
    ledger.record_decision(
        "maturity_audit",
        context={"bundle_size": len(bundle.implementation_facts), "ruleset": active_ruleset.id if active_ruleset else None},
        decision={"maturity_score": report.maturity_score.model_dump(), "verdict": report.verdict.model_dump()}
    )
    
    elapsed = time.time() - start_time
    typer.secho(f"\n[COGNITIVE CYCLE COMPLETE] Finished in {elapsed:.2f}s.\n", fg=typer.colors.CYAN, bold=True)
    
    render_terminal(report)

@app.command()
def boundaries(path: Path = typer.Argument(..., help="Path to the repository")):
    """Muestra el mapa de fronteras de producto (boundaries) del repositorio."""
    from ciel.skills.detect_product_boundaries import identify_boundaries
    from ciel.memory.decision_ledger import DecisionLedger
    import json
    
    ledger = DecisionLedger(path)
    typer.secho("\n[COGNITIVE CYCLE START] Detecting Product Boundaries...", fg=typer.colors.CYAN, bold=True)
    
    boundaries = identify_boundaries(path)
    
    ledger.record_decision(
        "boundary_detection",
        context={"repo_path": str(path)},
        decision={"boundaries": [b.model_dump() for b in boundaries]}
    )
    
    typer.secho(f"   [OK] Detected {len(boundaries)} boundaries.", fg=typer.colors.GREEN)
    output = [b.model_dump() for b in boundaries]
    typer.echo(json.dumps(output, indent=2))

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
    format: str = typer.Option("markdown", "--format", help="Formato de salida (json o markdown)"),
    ruleset: str = typer.Option(None, "--ruleset", help="ID del ruleset a aplicar")
):
    """Exporta el reporte del análisis."""
    from ciel.rag.file_scanner import scan_repository
    from ciel.orchestrator.source_role_assignment import assign_role
    from ciel.rag.evidence_extractor import extract_evidence
    from ciel.orchestrator.reasoning_orchestrator import orchestrate_reasoning
    from ciel.cli.render import render_json, render_markdown
    from ciel.skills.load_rulesets import load_ruleset
    
    active_ruleset = None
    if ruleset:
        active_ruleset = load_ruleset(ruleset, search_paths=[path / "rulesets", Path.cwd() / "rulesets"])

    
    files = scan_repository(path)
    roles = [assign_role(f, path) for f in files]
    bundle = extract_evidence(path, roles)
    
    report_obj = orchestrate_reasoning(bundle, ruleset=active_ruleset)
    
    if format.lower() == "json":
        typer.echo(render_json(report_obj))
    else:
        typer.echo(render_markdown(report_obj))

memory_app = typer.Typer(help="Manage Ciel Kernel memory and decision ledger")
app.add_typer(memory_app, name="memory")

@memory_app.command("init")
def memory_init(path: Path = typer.Argument(..., help="Path to the repository")):
    """Inicializa la memoria local."""
    from ciel.memory.decision_ledger import DecisionLedger
    ledger = DecisionLedger(path)
    ledger._ensure_dir()
    typer.secho("Memory ledger initialized.", fg=typer.colors.GREEN)

@memory_app.command("status")
def memory_status(path: Path = typer.Argument(..., help="Path to the repository")):
    """Revisa el estado de la cadena criptográfica de memoria."""
    from ciel.memory.decision_ledger import DecisionLedger
    ledger = DecisionLedger(path)
    if not ledger.log_path.exists():
        typer.secho("No memory ledger found.", fg=typer.colors.YELLOW)
        return
    if ledger.verify_chain():
        typer.secho("Ledger status: OK (Chain verified)", fg=typer.colors.GREEN)
    else:
        typer.secho("Ledger status: CORRUPTED (Hash mismatch detected)", fg=typer.colors.RED)

@memory_app.command("verify")
def memory_verify(path: Path = typer.Argument(..., help="Path to the repository")):
    """Verifica estrictamente el ledger y sale con error si está corrupto."""
    import sys
    from ciel.memory.decision_ledger import DecisionLedger
    ledger = DecisionLedger(path)
    if ledger.verify_chain():
        typer.secho("Ledger verified successfully.", fg=typer.colors.GREEN)
    else:
        typer.secho("Ledger verification failed!", fg=typer.colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    app()
