from typing import List
from ciel.schemas.evidence import SourceFile

def separate_context(sources: List[SourceFile], boundary: str) -> List[SourceFile]:
    """Filters sources to only include those belonging to a specific boundary."""
    separated = []
    
    for src in sources:
        # If the file path starts with the boundary path, it belongs to this context
        if src.path.startswith(boundary + "/") or src.path == boundary:
            separated.append(src)
            
    return separated
