from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class RefactorStep(BaseModel):
    order: int = Field(description="Sequential order of the step")
    action: Literal["create_file", "modify_file", "delete_file", "add_tests", "run_command", "refactor_logic"] = Field(description="Action type")
    path: str = Field(description="File path or command target")
    reason: str = Field(description="Explanation of why this step is necessary")
    evidence_id: Optional[str] = Field(None, description="Related evidence or gap ID")

class RefactorPlan(BaseModel):
    plan_id: str = Field(description="Unique identifier for the plan")
    target_gap_id: str = Field(description="Gap ID this plan aims to resolve")
    risk: Literal["low", "medium", "high"] = Field(description="Risk level of the changes")
    steps: List[RefactorStep] = Field(description="Detailed execution steps")
    suggested_tests: List[str] = Field(default_factory=list, description="Tests to write to verify the changes")
