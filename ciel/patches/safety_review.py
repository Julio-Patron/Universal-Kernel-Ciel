from ciel.schemas.refactor_plan import RefactorStep

def review_step_safety(step: RefactorStep) -> dict:
    """Evaluates if a refactor step is safe or destructive."""
    
    reason = step.reason.lower()
    path = step.path.lower()
    
    if step.action == "delete_file":
        return {"safe": False, "reason": "Deleting files is inherently destructive and requires manual execution."}
        
    if "rm -rf" in path or "drop table" in reason or "delete from" in reason:
        return {"safe": False, "reason": "Destructive keywords found (rm, drop, delete)."}
        
    if "auth" in path and step.action == "modify_file":
        if "disable" in reason or "remove" in reason or "bypass" in reason:
            return {"safe": False, "reason": "Potentially modifying authentication logic in an unsafe way."}
            
    if step.action == "run_command":
        if "curl" in path or "wget" in path:
            return {"safe": False, "reason": "Network requests in commands are blocked by default."}
            
    return {"safe": True, "reason": "Approved by basic static analysis."}
