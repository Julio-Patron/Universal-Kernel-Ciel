import os
from pathlib import Path
from typing import List

# Default ignore patterns
IGNORE_DIRS = {".git", ".venv", "node_modules", "__pycache__", "venv", "env", ".pytest_cache"}
IGNORE_EXTS = {".pyc", ".pyo", ".pyd", ".so", ".dll", ".exe", ".bin"}

def scan_repository(repo_path: Path) -> List[Path]:
    """Scans the repository and returns a list of valid files."""
    valid_files = []
    if not repo_path.is_dir():
        return valid_files
    
    for root, dirs, files in os.walk(repo_path):
        # Mutate dirs in-place to avoid traversing ignored directories
        dirs[:] = [
            d for d in dirs 
            if d not in IGNORE_DIRS and (not d.startswith(".") or d == ".github")
        ]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix not in IGNORE_EXTS and not file.startswith("."):
                valid_files.append(file_path)
    
    return valid_files
