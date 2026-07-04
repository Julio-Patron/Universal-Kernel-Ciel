from typing import List, Dict
from ciel.schemas.gap_report import GapMatrixItem

def generate_refactor_plan(gaps: List[GapMatrixItem]) -> List[Dict]:
    """Generates a step-by-step refactoring plan based on technical debt gaps."""
    plan = []
    
    debt_items = [g for g in gaps if g.status in ("technical_debt", "roadmap_gap") or g.classification == "missing_feature"]
    
    for i, item in enumerate(debt_items):
        plan.append({
            "step": i + 1,
            "target_claim": item.claim,
            "action": f"Implement or fix {item.claim}",
            "command": f"echo 'Scaffold command to resolve: {item.claim}'"  # Scaffold
        })
        
    return plan
