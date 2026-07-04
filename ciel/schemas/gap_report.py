from pydantic import BaseModel
from typing import List

class GapProjectInfo(BaseModel):
    name: str

class GapMatrixItem(BaseModel):
    claim_id: str
    claim: str
    status: str
    classification: str
    evidence: List[str]
    severity: str
    interpretation: str
    recommended_action: str

class MaturityScore(BaseModel):
    intention_clarity: float
    implementation_completeness: float
    behavior_confidence: float
    operational_readiness: float
    commercial_readiness: float

class Verdict(BaseModel):
    stage: str
    summary: str
    main_bottleneck: str

class NextAction(BaseModel):
    priority: int
    type: str
    description: str
    reason: str

class ImplementationGapReport(BaseModel):
    schema_version: str = "ciel.gap_report.v1.0"
    project: GapProjectInfo
    gap_matrix: List[GapMatrixItem]
    maturity_score: MaturityScore
    verdict: Verdict
    next_actions: List[NextAction]
