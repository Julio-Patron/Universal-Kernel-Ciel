from pathlib import Path
from typing import List, Dict

def identify_boundaries(repo_path: Path) -> List[Dict]:
    """Identifies potential product boundaries or sub-projects within a monorepo."""
    boundaries = []
    
    if not repo_path.is_dir():
        return boundaries
        
    # Scaffold logic: Look for common markers of sub-projects
    markers = {"package.json", "Cargo.toml", "pyproject.toml", "go.mod", "pom.xml", "build.gradle"}
    
    for path in repo_path.rglob("*"):
        if path.is_file() and path.name in markers:
            # Avoid the root project acting as a sub-boundary if we only want nested ones
            if path.parent != repo_path:
                try:
                    rel_path = str(path.parent.relative_to(repo_path)).replace("\\", "/")
                    boundaries.append({
                        "boundary_path": rel_path,
                        "marker": path.name,
                        "type": "sub_project"
                    })
                except ValueError:
                    pass
                
    return boundaries
