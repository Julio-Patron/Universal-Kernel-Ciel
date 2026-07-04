from pydantic import BaseModel
from typing import List, Literal

class GapProjectInfo(BaseModel):
    name: str

class GapMatrixItem(BaseModel):
    claim_id: str
    claim: str
    status: Literal["implemented", "roadmap_gap", "technical_debt", "architecture_drift"]
    classification: Literal["production_ready", "missing_feature", "bug", "partial"]
    evidence: List[str]
    severity: Literal["low", "medium", "high"]
    interpretation: str
    recommended_action: str

class MaturityScore(BaseModel):
    intention_clarity: float
    implementation_completeness: float
    behavior_confidence: float
    operational_readiness: float
    commercial_readiness: float

class Verdict(BaseModel):
    stage: Literal["ideation", "technical_core_ready", "alpha", "beta", "production"]
    summary: str
    main_bottleneck: str

class NextAction(BaseModel):
    priority: int
    type: Literal["coding", "packaging", "testing", "docs", "release", "configuration"]
    description: str
    reason: str

class ImplementationGapReport(BaseModel):
    schema_version: str = "ciel.gap_report.v1.0"
    project: GapProjectInfo
    gap_matrix: List[GapMatrixItem]
    maturity_score: MaturityScore
    verdict: Verdict
    next_actions: List[NextAction]
