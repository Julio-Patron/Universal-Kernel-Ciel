import json
import uuid
import logging
import re
from typing import List, Optional

from ciel.schemas.gap_report import GapMatrixItem
from ciel.schemas.refactor_plan import RefactorPlan, RefactorStep
from ciel.inference.model_router import route_inference
from ciel.orchestrator.purpose_resolver import extract_json_block

logger = logging.getLogger(__name__)

_PATH_PATTERN = re.compile(
    r"(?<![\w.-])(?:[\w.-]+/)+[\w.-]+\.[A-Za-z0-9]+|"
    r"(?<![\w.-])[\w.-]+\.(?:py|toml|yaml|yml|json|md|js|ts|tsx|go|rs|java)"
)


def _infer_target_path(gap: GapMatrixItem) -> str:
    """Use concrete gap evidence before falling back to the repository root."""
    candidates = [*gap.evidence, gap.recommended_action, gap.claim]
    for candidate in candidates:
        match = _PATH_PATTERN.search(candidate)
        if match:
            return match.group(0)

    combined = " ".join(candidates).lower()
    if "memory" in combined and "ledger" in combined:
        return "ciel/memory/decision_ledger.py"
    if "test" in combined:
        return "tests/"
    return "."

def generate_refactor_plan(gaps: List[GapMatrixItem], target_gap_id: Optional[str] = None) -> List[RefactorPlan]:
    """Generates a step-by-step refactoring plan based on technical debt gaps."""
    plans = []
    
    # Filtrar gaps que requieren refactorización
    debt_items = [g for g in gaps if g.status in ("technical_debt", "roadmap_gap") or g.classification == "missing_feature"]
    
    for gap in debt_items:
        if target_gap_id and gap.claim_id != target_gap_id:
            continue
            
        prompt = f"""
        You are an expert software architect.
        Generate a detailed, step-by-step refactoring plan to resolve this implementation gap.
        
        Gap ID: {gap.claim_id}
        Gap Claim: {gap.claim}
        Current Status: {gap.status}
        Severity: {gap.severity}
        Interpretation: {gap.interpretation}
        Recommended Action: {gap.recommended_action}
        
        Return ONLY a JSON object matching this exact structure:
        {{
            "plan_id": "refactor_xxx",
            "target_gap_id": "{gap.claim_id}",
            "risk": "low" (or "medium" or "high"),
            "steps": [
                {{
                    "order": 1,
                    "action": "modify_file",
                    "path": "path/to/file",
                    "reason": "why this step is needed",
                    "evidence_id": "optional evidence or gap id"
                }}
            ],
            "suggested_tests": ["test case description"]
        }}
        """
        
        try:
            resp = route_inference(prompt)
            if resp.startswith("Error"):
                raise ValueError("LLM inference failed or disabled.")
                
            data = json.loads(extract_json_block(resp))
            if "plan_id" not in data:
                data["plan_id"] = f"refactor_{uuid.uuid4().hex[:8]}"
            if "target_gap_id" not in data:
                data["target_gap_id"] = gap.claim_id
                
            plan = RefactorPlan(**data)
            plans.append(plan)
        except Exception as e:
            logger.warning("LLM planning failed for gap %s: %s", gap.claim_id, e)
            fallback_plan = RefactorPlan(
                plan_id=f"refactor_fallback_{uuid.uuid4().hex[:8]}",
                target_gap_id=gap.claim_id,
                risk=gap.severity,
                steps=[
                    RefactorStep(
                        order=1,
                        action="modify_file",
                        path=_infer_target_path(gap),
                        reason=f"Fallback: {gap.recommended_action}",
                        evidence_id=gap.claim_id
                    )
                ],
                suggested_tests=[f"Verify {gap.claim}"]
            )
            plans.append(fallback_plan)
            
    return plans
