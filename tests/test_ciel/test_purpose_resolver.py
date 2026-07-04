import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from ciel.orchestrator.purpose_resolver import (
    scan_documentation_context,
    extract_json_block,
    get_static_fallback,
    resolve_purpose,
    STATIC_FALLBACKS
)
from ciel.schemas.purpose import PurposeObject

def test_extract_json_block():
    # 1. JSON block wrapped in ```json
    raw_1 = "Some introduction\n```json\n{\n  \"schema_version\": \"ciel.purpose.v1.0\"\n}\n```\nSome outro."
    assert extract_json_block(raw_1) == "{\n  \"schema_version\": \"ciel.purpose.v1.0\"\n}"
    
    # 2. JSON block wrapped in general ```
    raw_2 = "```\n{\n  \"schema_version\": \"ciel.purpose.v1.0\"\n}\n```"
    assert extract_json_block(raw_2) == "{\n  \"schema_version\": \"ciel.purpose.v1.0\"\n}"
    
    # 3. Raw JSON object (braces)
    raw_3 = "  {\n  \"schema_version\": \"ciel.purpose.v1.0\"\n}  "
    assert extract_json_block(raw_3) == "{\n  \"schema_version\": \"ciel.purpose.v1.0\"\n}"
    
    # 4. No braces or markdown tags
    raw_4 = "invalid raw text"
    assert extract_json_block(raw_4) == "invalid raw text"

def test_get_static_fallback():
    # Test mapping keywords to correct fallbacks
    assert get_static_fallback("Please run api boundary tests").task.type == "api_integration_tests"
    assert get_static_fallback("harden the core components").task.type == "core_hardening"
    assert get_static_fallback("we need to refactor and clean technical debt").task.type == "refactoring"
    assert get_static_fallback("what to do first").task.type == "repo_analysis"
    assert get_static_fallback("unrelated prompt").task.type == "repo_analysis"

def test_scan_documentation_context(tmp_path):
    # Setup mock repo path
    readme = tmp_path / "README.md"
    readme.write_text("Hello README " * 500, encoding="utf-8") # 6500 chars
    
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    
    doc1 = docs_dir / "doc1.md"
    doc1.write_text("Doc 1 " * 400, encoding="utf-8") # 2400 chars
    
    doc2 = docs_dir / "doc2.md"
    doc2.write_text("Doc 2 " * 400, encoding="utf-8")
    
    doc3 = docs_dir / "doc3.md"
    doc3.write_text("Doc 3 " * 400, encoding="utf-8")
    
    doc4 = docs_dir / "doc4.md"
    doc4.write_text("Doc 4 " * 400, encoding="utf-8")
    
    context = scan_documentation_context(tmp_path)
    
    # Verify README is present and truncated to 4000 characters
    assert "--- DOCUMENT: README.md ---" in context
    assert len("Hello README " * 500) > 4000
    # The README segment should be truncated
    readme_part = context.split("--- DOCUMENT: docs")[0]
    assert len(readme_part.replace("--- DOCUMENT: README.md ---\n", "").strip()) <= 4000
    
    # Verify at most 3 documents from docs/ are scanned
    # doc1.md, doc2.md, doc3.md should be sorted alphabetically and processed, doc4.md ignored
    assert "doc1.md" in context
    assert "doc2.md" in context
    assert "doc3.md" in context
    assert "doc4.md" not in context

@patch("ciel.orchestrator.purpose_resolver.query_ollama")
def test_resolve_purpose_llm_success(mock_query):
    # Mock successful LLM response conforming to schema
    mock_query.return_value = """
    Here is your requested JSON object:
    ```json
    {
      "schema_version": "ciel.purpose.v1.0",
      "task": {
        "type": "custom_task",
        "decision_needed": "custom_decision",
        "output_mode": "custom_mode"
      },
      "purpose": {
        "primary_question": "What is the custom question?",
        "success_criteria": [
          "criterion 1",
          "criterion 2",
          "criterion 3"
        ]
      }
    }
    ```
    """
    
    result = resolve_purpose("some prompt")
    assert isinstance(result, PurposeObject)
    assert result.task.type == "custom_task"
    assert result.task.decision_needed == "custom_decision"
    assert result.purpose.primary_question == "What is the custom question?"
    assert len(result.purpose.success_criteria) == 3

@patch("ciel.orchestrator.purpose_resolver.query_ollama")
def test_resolve_purpose_ollama_error_fallback(mock_query):
    # query_ollama returning error message
    mock_query.return_value = "Error connecting to local inference: Connection refused"
    
    result = resolve_purpose("harden security")
    assert result.task.type == "core_hardening"

@patch("ciel.orchestrator.purpose_resolver.query_ollama")
def test_resolve_purpose_invalid_json_fallback(mock_query):
    # query_ollama returning malformed JSON
    mock_query.return_value = "```json\n{ malformed: json }\n```"
    
    result = resolve_purpose("refactor codebase")
    assert result.task.type == "refactoring"
