from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ProtectedPath(BaseModel):
    pattern: str
    action: str

class DenyRules(BaseModel):
    file_patterns: List[str] = Field(default_factory=list)
    commands: List[str] = Field(default_factory=list)

class Limits(BaseModel):
    changed_files: int = 100
    total_changed_lines: int = 5000

class Check(BaseModel):
    command: str
    args: List[str] = Field(default_factory=list)
    required: bool = False

class Ruleset(BaseModel):
    version: int = 1
    protected_paths: List[ProtectedPath] = Field(default_factory=list)
    deny: DenyRules = Field(default_factory=DenyRules)
    limits: Limits = Field(default_factory=Limits)
    checks: List[Check] = Field(default_factory=list)
    hash: Optional[str] = None
