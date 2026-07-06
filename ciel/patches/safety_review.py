from ciel.schemas.refactor_plan import RefactorStep

def review_step_safety(step: RefactorStep) -> dict:
    """Evaluates if a refactor step is safe or destructive."""
    
    reason = step.reason.lower()
    path = step.path.lower()
    combined = f"{path} {reason}"
    
    if step.action == "delete_file":
        return {"safe": False, "reason": "Deleting files is inherently destructive and requires manual execution."}
        
    if any(keyword in combined for keyword in ("rm -rf", "drop table", "delete from")):
        return {"safe": False, "reason": "Destructive keywords found (rm, drop, delete)."}
        
    if "auth" in path and step.action == "modify_file":
        if any(keyword in combined for keyword in ("disable", "remove", "bypass")):
            return {"safe": False, "reason": "Potentially modifying authentication logic in an unsafe way."}
            
    if step.action == "run_command":
        if "curl" in combined or "wget" in combined:
            return {"safe": False, "reason": "Network requests in commands are blocked by default."}
            
    return {"safe": True, "reason": "Approved by basic static analysis."}
