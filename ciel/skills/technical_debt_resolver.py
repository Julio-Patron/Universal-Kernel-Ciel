from pathlib import Path
from ciel.skills.auto_refactor_planner import generate_refactor_plan
from ciel.executor.shell_executor import execute_command
from ciel.schemas.gap_report import ImplementationGapReport

def resolve_technical_debt(report: ImplementationGapReport, repo_path: Path):
    """Orchestrates the resolution of technical debt by executing the refactor plan."""
    plan = generate_refactor_plan(report.gap_matrix)
    
    if not plan:
        return "No technical debt detected."
        
    results = []
    for step in plan:
        # In a real scenario, this would use the executor with approval gate
        # For this scaffold, we just log the planned actions
        results.append(f"Step {step['step']}: Action planned -> {step['action']}")
        
    return "\n".join(results)
