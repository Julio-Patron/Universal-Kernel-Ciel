from pydantic import BaseModel
from typing import List

class TaskInfo(BaseModel):
    type: str
    decision_needed: str
    output_mode: str

class PurposeCriteria(BaseModel):
    primary_question: str
    success_criteria: List[str]

class PurposeObject(BaseModel):
    schema_version: str = "ciel.purpose.v1.0"
    task: TaskInfo
    purpose: PurposeCriteria
