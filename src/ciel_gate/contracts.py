from typing import Literal
from pydantic import BaseModel

class ChangeProposal(BaseModel):
    repository: str
    base_commit: str
    agent: str
    diff: str
    requested_commands: list[str] = []

class DiffFacts(BaseModel):
    files_added: list[str]
    files_modified: list[str]
    files_deleted: list[str]
    total_additions: int
    total_deletions: int
    sensitive_paths: list[str]

class PolicyViolation(BaseModel):
    rule_id: str
    severity: str
    path: str | None
    reason: str

class GateDecision(BaseModel):
    verdict: Literal["allow", "deny", "require_approval"]
    risk: Literal["low", "medium", "high", "critical"]
    violations: list[PolicyViolation]
    diff_hash: str
    policy_hash: str
