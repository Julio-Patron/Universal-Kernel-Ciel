from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RulesetThresholds(BaseModel):
    maturity_score_min: float = Field(0.0, description="Puntuación mínima de madurez (0.0 a 1.0)")

class Ruleset(BaseModel):
    id: str = Field(description="Identificador único del policy pack")
    version: str = Field(description="Versión del ruleset")
    required: List[str] = Field(default_factory=list, description="Lista de verificaciones requeridas")
    thresholds: Optional[RulesetThresholds] = Field(default_factory=RulesetThresholds)
    hash: Optional[str] = Field(None, description="SHA-256 hash del archivo YAML")
