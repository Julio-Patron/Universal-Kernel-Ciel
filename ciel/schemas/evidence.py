from pydantic import BaseModel
from typing import List, Optional

class ProjectInfo(BaseModel):
    name: str
    primary_language: str

class SourceFile(BaseModel):
    id: str
    path: str
    role: str
    confidence: float
    boundary_id: Optional[str] = None

class IntentionClaim(BaseModel):
    id: str
    source_id: str
    claim: str
    claim_type: str

class ImplementationFact(BaseModel):
    id: str
    source_id: str
    fact: str
    fact_type: str

class BehaviorEvidence(BaseModel):
    id: str
    source_id: str
    evidence: str
    evidence_type: str

class OperationalEvidence(BaseModel):
    id: str
    source_id: str
    evidence: str
    evidence_type: str

class EvidenceBundle(BaseModel):
    schema_version: str = "ciel.evidence.v1.0"
    project: ProjectInfo
    sources: List[SourceFile]
    intention_claims: List[IntentionClaim]
    implementation_facts: List[ImplementationFact]
    behavior_evidence: List[BehaviorEvidence]
    operational_evidence: List[OperationalEvidence] = []
