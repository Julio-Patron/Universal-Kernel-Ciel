import logging
from ciel.inference.model_router import route_inference
from ciel.schemas.refactor_plan import RefactorStep
from pathlib import Path

logger = logging.getLogger(__name__)

def generate_diff(step: RefactorStep, repo_path: Path) -> str:
    """Generates a unified diff for a refactoring step using the LLM."""
    if step.action == "run_command":
        return f"# Command to run: {step.path}\n"
        
    file_path = repo_path / step.path
    current_content = "File does not exist."
    if file_path.exists() and file_path.is_file():
        try:
            current_content = file_path.read_text(encoding="utf-8")
        except Exception:
            current_content = "Binary or unreadable file."
            
    prompt = f"""
    You are an AI patch generator. Your job is to output ONLY a unified diff (.patch format)
    to fulfill the following refactoring step. Do not include markdown codeblocks (like ```diff), just the raw diff text.
    
    File path: {step.path}
    Action: {step.action}
    Reason: {step.reason}
    
    Current File Content:
    {current_content}
    
    Unified Diff (unified diff format, starting with --- and +++):
    """
    
    try:
        diff_output = route_inference(prompt)
        if diff_output.startswith("Error"):
            return f"--- a/{step.path}\n+++ b/{step.path}\n# Error: LLM inference failed. Could not generate diff for {step.action}."
        
        clean_diff = diff_output.strip()
        if clean_diff.startswith("```diff"):
            clean_diff = clean_diff[7:]
        elif clean_diff.startswith("```patch"):
            clean_diff = clean_diff[8:]
        elif clean_diff.startswith("```"):
            clean_diff = clean_diff[3:]
        if clean_diff.endswith("```"):
            clean_diff = clean_diff[:-3]
            
        return clean_diff.strip()
    except Exception as e:
        logger.warning("Failed to generate diff for %s: %s", step.path, e)
        return f"--- a/{step.path}\n+++ b/{step.path}\n# Warning: Diff generation failed."
