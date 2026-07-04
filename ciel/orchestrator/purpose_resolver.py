from ciel.schemas.purpose import PurposeObject, TaskInfo, PurposeCriteria

def resolve_purpose(prompt: str) -> PurposeObject:
    """Resolves a vague user prompt into a structured PurposeObject."""
    # Dummy static logic for V0
    task_info = TaskInfo(
        type="repo_analysis",
        decision_needed="what_to_do_first",
        output_mode="diagnostic_and_plan"
    )
    criteria = PurposeCriteria(
        primary_question="What is the gap between project intention and current implementation reality?",
        success_criteria=[
            "identify project intention",
            "identify current implementation",
            "detect implementation gaps",
            "recommend next action"
        ]
    )
    return PurposeObject(task=task_info, purpose=criteria)
