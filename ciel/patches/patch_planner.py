from typing import List, Dict
from pathlib import Path
from ciel.schemas.refactor_plan import RefactorPlan
from ciel.patches.diff_generator import generate_diff
from ciel.patches.safety_review import review_step_safety

def propose_patches(plan: RefactorPlan, repo_path: Path) -> List[Dict]:
    """Orchestrates generation of patches and safety reviews for a plan."""
    proposed_patches = []
    
    for step in plan.steps:
        safety = review_step_safety(step)
        
        diff = ""
        if safety["safe"]:
            diff = generate_diff(step, repo_path)
            
        proposed_patches.append({
            "step": step.model_dump(),
            "safety": safety,
            "diff": diff
        })
        
    return proposed_patches
