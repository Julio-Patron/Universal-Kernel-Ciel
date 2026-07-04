import json
import logging
import re
from pathlib import Path
from typing import List, Optional

from ciel.schemas.purpose import PurposeObject, TaskInfo, PurposeCriteria
from ciel.inference.model_router import route_inference

logger = logging.getLogger(__name__)

# Predefined static fallback PurposeObjects
STATIC_FALLBACKS = {
    "repo_analysis": PurposeObject(
        schema_version="ciel.purpose.v1.0",
        task=TaskInfo(
            type="repo_analysis",
            decision_needed="what_to_do_first",
            output_mode="diagnostic_and_plan"
        ),
        purpose=PurposeCriteria(
            primary_question="What is the gap between project intention and current implementation reality?",
            success_criteria=[
                "identify project intention",
                "identify current implementation",
                "detect implementation gaps",
                "recommend next action"
            ]
        )
    ),
    "core_hardening": PurposeObject(
        schema_version="ciel.purpose.v1.0",
        task=TaskInfo(
            type="core_hardening",
            decision_needed="verify_security_and_stability",
            output_mode="hardening_checklist"
        ),
        purpose=PurposeCriteria(
            primary_question="Are the core components of the repository hardened against security and stability failures?",
            success_criteria=[
                "audit core configurations and imports",
                "detect potential security vulnerabilities or weak points",
                "evaluate edge cases and error handling",
                "recommend hardening fixes"
            ]
        )
    ),
    "api_integration_tests": PurposeObject(
        schema_version="ciel.purpose.v1.0",
        task=TaskInfo(
            type="api_integration_tests",
            decision_needed="validate_boundaries",
            output_mode="test_coverage_gap"
        ),
        purpose=PurposeCriteria(
            primary_question="Are the API endpoints and external integration boundaries properly verified?",
            success_criteria=[
                "identify all external/internal API boundary points",
                "assess existing test coverage for boundaries",
                "recommend integration test additions"
            ]
        )
    ),
    "refactoring": PurposeObject(
        schema_version="ciel.purpose.v1.0",
        task=TaskInfo(
            type="refactoring",
            decision_needed="reduce_technical_debt",
            output_mode="refactor_plan"
        ),
        purpose=PurposeCriteria(
            primary_question="How can the codebase structure be simplified and refactored to reduce technical debt?",
            success_criteria=[
                "identify code duplication or complexity hotspots",
                "design a simplified component hierarchy",
                "propose step-by-step refactoring stages"
            ]
        )
    )
}

def scan_documentation_context(repo_path: Path) -> str:
    """Scans the repository for documentation files (README.md, docs/*.md)
    and compiles a truncated context representation of the project's intent.
    """
    doc_context_parts = []
    
    # 1. Target README.md (case-insensitive) in the root
    readme_candidates = [
        repo_path / "README.md",
        repo_path / "readme.md",
        repo_path / "README.txt",
        repo_path / "readme.txt"
    ]
    
    for candidate in readme_candidates:
        if candidate.is_file():
            try:
                # Read up to 4000 characters to manage context size
                content = candidate.read_text(encoding="utf-8", errors="ignore")
                truncated = content[:4000]
                doc_context_parts.append(
                    f"--- DOCUMENT: {candidate.name} ---\n{truncated}\n"
                )
                break  # Stop after reading one README
            except Exception as e:
                logger.warning(f"Failed to read readme file {candidate}: {e}")
                
    # 2. Target docs/*.md files (max 3 files, 2000 chars each)
    docs_dir = repo_path / "docs"
    if docs_dir.is_dir():
        try:
            md_files = list(docs_dir.glob("*.md"))
            for file_path in sorted(md_files)[:3]:
                if file_path.is_file():
                    try:
                        # Read up to 2000 characters per doc file
                        content = file_path.read_text(encoding="utf-8", errors="ignore")
                        truncated = content[:2000]
                        rel_path = file_path.relative_to(repo_path)
                        doc_context_parts.append(
                            f"--- DOCUMENT: {rel_path} ---\n{truncated}\n"
                        )
                    except Exception as e:
                        logger.warning(f"Failed to read doc file {file_path}: {e}")
        except Exception as e:
            logger.warning(f"Failed to list docs directory: {e}")
            
    return "\n".join(doc_context_parts) if doc_context_parts else "No documentation found."

def extract_json_block(raw_text: str) -> str:
    """Extracts JSON block from markdown tags or returns raw string.
    Supports both JSON objects ({...}) and arrays ([...]).
    """
    match = re.search(r"```json\s*(.*?)\s*```", raw_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
        
    match = re.search(r"```\s*(.*?)\s*```", raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
        
    brace_start = raw_text.find('{')
    brace_end = raw_text.rfind('}')
    bracket_start = raw_text.find('[')
    bracket_end = raw_text.rfind(']')
    
    starts = []
    if brace_start != -1 and brace_end != -1 and brace_start < brace_end:
        starts.append((brace_start, brace_end))
    if bracket_start != -1 and bracket_end != -1 and bracket_start < bracket_end:
        starts.append((bracket_start, bracket_end))
        
    if starts:
        start_idx, end_idx = min(starts, key=lambda x: x[0])
        return raw_text[start_idx:end_idx+1].strip()
        
    return raw_text.strip()


def get_static_fallback(prompt: str) -> PurposeObject:
    """Selects a static PurposeObject based on keywords in the user prompt."""
    prompt_lower = prompt.lower()
    
    if any(k in prompt_lower for k in ["test", "api", "integration", "boundary"]):
        return STATIC_FALLBACKS["api_integration_tests"]
    elif any(k in prompt_lower for k in ["harden", "security", "protect", "vuln", "fortify"]):
        return STATIC_FALLBACKS["core_hardening"]
    elif any(k in prompt_lower for k in ["refactor", "clean", "debt", "simplify"]):
        return STATIC_FALLBACKS["refactoring"]
    else:
        return STATIC_FALLBACKS["repo_analysis"]

def resolve_purpose(prompt: str, repo_path: Optional[str] = None) -> PurposeObject:
    """Resolves a vague user prompt into a structured PurposeObject.
    Uses Ollama local inference to parse against documentation intent context,
    with a fallback to rule-based static matching if the LLM query fails or Pydantic validation fails.
    """
    # 1. Resolve repository path (default to current working directory)
    path_obj = Path(repo_path) if repo_path else Path.cwd()
    
    # 2. Extract documentation context
    doc_context = scan_documentation_context(path_obj)
    
    # 3. Formulate the LLM prompt
    llm_prompt = f"""You are the Ciel Kernel Purpose Resolver.
Your task is to convert a vague or ambiguous user prompt into a structured decision-making objective (PurposeObject) based on the provided repository context.

USER PROMPT:
{prompt}

REPOSITORY DOCUMENTATION CONTEXT:
{doc_context}

You must return a JSON object conforming exactly to the following Pydantic schema:

{{
  "schema_version": "ciel.purpose.v1.0",
  "task": {{
    "type": "The type of task. E.g., 'repo_analysis', 'core_hardening', 'refactoring', 'api_integration_tests', etc.",
    "decision_needed": "The main decision or question that needs resolution. E.g., 'what_to_do_first', 'verify_security', 'validate_apis'",
    "output_mode": "The format or style of the output report. E.g., 'diagnostic_and_plan', 'hardening_checklist', 'gap_matrix'"
  }},
  "purpose": {{
    "primary_question": "A specific, deep question that the execution must answer based on the prompt and repository content.",
    "success_criteria": [
      "A list of concrete criteria that must be met to consider this task complete (minimum 3 items)."
    ]
  }}
}}

Rules:
1. Analyze the USER PROMPT in the context of the REPOSITORY DOCUMENTATION CONTEXT.
2. Determine what the user is trying to accomplish and map it to a specific task type, decision, and success criteria.
3. Your output must be a single, valid JSON block wrapped in ```json ... ``` code tags. Do not include any other text before or after the JSON.
"""

    # 4. Attempt LLM Query
    try:
        response_text = route_inference(llm_prompt)
        
        # Check if route_inference returned an error string
        if response_text.startswith("Error connecting to"):
            logger.warning(f"Inference connection error: {response_text}. Falling back to static dictionary.")
            return get_static_fallback(prompt)
            
        # Parse JSON
        extracted_json = extract_json_block(response_text)
        data = json.loads(extracted_json)
        
        # Validate using Pydantic PurposeObject
        purpose_obj = PurposeObject.model_validate(data)
        return purpose_obj
        
    except Exception as e:
        logger.warning(f"Failed LLM-powered purpose resolution: {e}. Falling back to static dictionary.")
        return get_static_fallback(prompt)

