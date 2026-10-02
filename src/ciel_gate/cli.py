import typer
import sys
import hashlib
from pathlib import Path
from pydantic import ValidationError

from ciel_gate.contracts import ChangeProposal
from ciel_gate.policy.loader import load_policy
from ciel_gate.diff.parser import parse_diff
from ciel_gate.policy.evaluator import evaluate_proposal
from ciel_gate.ledger.writer import DecisionLedger

app = typer.Typer(help="Ciel Gate: Agent Change Control")

@app.command()
def init():
    """Initialize Ciel Gate in the current repository."""
    typer.echo("Initialized Ciel Gate")

@app.command()
def check(policy: str = typer.Option(..., help="Path to policy YAML"),
          agent: str = typer.Option(..., help="Identity of the agent"),
          format: str = typer.Option("json", help="Output format")):
    """Check a proposed diff against policies."""
    diff_text = sys.stdin.read()
    if not diff_text.strip():
        typer.echo("Error: Empty diff provided.", err=True)
        raise typer.Exit(code=4)
        
    try:
        ruleset = load_policy(policy)
    except Exception as e:
        typer.echo(f"Policy Error: {e}", err=True)
        raise typer.Exit(code=5)
        
    facts = parse_diff(diff_text)
    diff_hash = hashlib.sha256(diff_text.encode()).hexdigest()
    
    proposal = ChangeProposal(
        repository=Path.cwd().name,
        base_commit="HEAD",
        agent=agent,
        diff=diff_text,
        requested_commands=[]
    )
    
    decision = evaluate_proposal(proposal, ruleset, facts, diff_hash, ruleset.hash or "unknown")
    
    try:
        ledger = DecisionLedger(Path.cwd())
        ledger.record_decision(event_type="policy_check", context=proposal.model_dump(), decision=decision.model_dump())
    except Exception as e:
        # Silently fail ledger or log to stderr
        print(f"Warning: ledger failure {e}", file=sys.stderr)
    
    if format == "json":
        typer.echo(decision.model_dump_json())
    else:
        typer.echo(f"Verdict: {decision.verdict} (Risk: {decision.risk})")
        for v in decision.violations:
            typer.echo(f"- {v.rule_id} [{v.severity}]: {v.reason} ({v.path})")
            
    # Exit codes: 0 (allow), 2 (require_approval), 3 (deny), 4 (input error), 5 (check failed)
    if decision.verdict == "allow":
        raise typer.Exit(code=0)
    elif decision.verdict == "require_approval":
        raise typer.Exit(code=2)
    else:
        raise typer.Exit(code=3)

@app.command()
def verify():
    """Verify the decision ledger for integrity."""
    ledger = DecisionLedger(Path.cwd())
    valid = ledger.verify_chain()
    if valid:
        typer.echo("Ledger verified. Chain is intact.")
        raise typer.Exit(code=0)
    else:
        typer.echo("Ledger verification failed! Chain is broken or tampered.", err=True)
        raise typer.Exit(code=1)

@app.command()
def validate(policy: str = typer.Argument(..., help="Path to policy YAML")):
    """Validate a policy YAML file."""
    try:
        load_policy(policy)
        typer.echo("Policy is valid")
    except Exception as e:
        typer.echo(f"Policy invalid: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
