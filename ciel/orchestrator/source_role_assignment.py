from pathlib import Path
from typing import List, Optional
from ciel.schemas.evidence import SourceFile
from ciel.schemas.product_boundary import ProductBoundary

def assign_role(file_path: Path, relative_to: Path, boundaries: Optional[List[ProductBoundary]] = None) -> SourceFile:
    """Assigns a role to a file based on its path and name."""
    try:
        rel_path = file_path.relative_to(relative_to)
    except ValueError:
        rel_path = file_path
        
    path_str = str(rel_path).replace("\\", "/")
    filename = rel_path.name.lower()
    
    # Intention Rules
    if filename == "readme.md" or path_str.startswith("docs/"):
        role = "intention"
    # Behavior Rules
    elif "test" in path_str.lower():
        role = "behavior"
    # Operational Rules
    elif path_str.startswith(".github/workflows/") or filename in ("dockerfile", "docker-compose.yml"):
        role = "operational_maturity"
    # Structure Rules
    elif filename in ("cargo.toml", "pyproject.toml", "package.json"):
        role = "structure"
    # Reality Rules (Code files usually)
    elif rel_path.suffix in (".py", ".rs", ".js", ".ts", ".go", ".java", ".cpp", ".c"):
        role = "reality"
    else:
        role = "unknown"
        
    boundary_id = None
    if boundaries:
        best_match = None
        max_len = -1
        for b in boundaries:
            b_path = b.path if b.path != "/" else ""
            if path_str.startswith(b_path + "/") or b_path == "" or path_str == b_path:
                if len(b_path) > max_len:
                    best_match = b.id
                    max_len = len(b_path)
        boundary_id = best_match
        
    return SourceFile(
        id=path_str,
        path=path_str,
        role=role,
        confidence=0.9,
        boundary_id=boundary_id
    )
