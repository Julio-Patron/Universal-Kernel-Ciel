from typing import List
from pydantic import BaseModel

class DiffFacts(BaseModel):
    files_added: List[str] = []
    files_modified: List[str] = []
    files_deleted: List[str] = []
    total_additions: int = 0
    total_deletions: int = 0
    sensitive_paths: List[str] = []
