from pathlib import Path
from ciel.skills.auto_refactor_planner import generate_refactor_plan
from ciel.schemas.gap_report import ImplementationGapReport

def resolve_technical_debt(report: ImplementationGapReport, repo_path: Path):
    """Orchestrates the resolution of technical debt by executing the refactor plan."""
    plans = generate_refactor_plan(report.gap_matrix)
    
    if not plans:
        return "No technical debt detected."
        
    results = []
    for plan in plans:
        results.append(f"Plan ID: {plan.plan_id}")
        for step in plan.steps:
            # In a real scenario, this would use the executor with approval gate
            # For this scaffold, we just log the planned actions
            results.append(f"Step {step.order}: {step.action} on {step.path}")
            
    return "\n".join(results)
