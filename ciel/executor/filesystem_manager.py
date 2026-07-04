from pathlib import Path
from ciel.executor.approval_gate import request_approval

def create_directory(path: Path, require_approval: bool = True) -> bool:
    """Creates a directory."""
    if require_approval:
        approved = request_approval(f"Create directory: {path}")
        if not approved:
            return False
            
    path.mkdir(parents=True, exist_ok=True)
    return True
    
def write_file(path: Path, content: str, require_approval: bool = True) -> bool:
    """Writes content to a file."""
    if require_approval:
        approved = request_approval(f"Write file: {path}")
        if not approved:
            return False
            
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True
