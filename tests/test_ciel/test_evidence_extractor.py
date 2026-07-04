import pytest
from pathlib import Path
from unittest.mock import patch
from ciel.rag.evidence_extractor import (
    extract_evidence,
    _python_facts,
    _llm_facts,
    _generic_code_facts
)
from ciel.schemas.evidence import SourceFile

def test_python_facts_ast_parsing():
    content = """
import os
from sys import argv

class MyClass:
    def method(self):
        pass

def my_func():
    pass
"""
    facts, count = _python_facts(content, "src_1", 1)
    
    assert len(facts) == 3
    assert facts[0].fact == "Imports dependencies: argv, os"
    assert "Defines class MyClass" in facts[1].fact
    assert "Defines function my_func" in facts[2].fact

def test_generic_code_facts():
    content = """
function jsFunc() {}
def py_func(): pass
class MyClass {}
"""
    facts, count = _generic_code_facts(content, "src_2", 1)
    
    assert len(facts) == 3
    assert "jsFunc" in facts[0].fact
    assert "MyClass" in facts[1].fact
    assert "py_func" in facts[2].fact

@patch("ciel.rag.evidence_extractor.route_inference")
def test_llm_facts_valid(mock_query):
    mock_query.return_value = """```json
[
  {"fact": "Does advanced stuff", "fact_type": "implemented_capability"}
]
```"""
    src = SourceFile(id="s1", path="test.py", role="reality", confidence=1.0)
    facts, count = _llm_facts("def advanced_func(): pass", src, 1)
    
    assert len(facts) == 1
    assert facts[0].fact == "Does advanced stuff"

@patch("ciel.rag.evidence_extractor.route_inference")
def test_llm_facts_fallback_on_error(mock_query, tmp_path):
    # Simulate a network error connecting to Ollama
    mock_query.return_value = "Error connecting to local inference: Connection refused"
    
    # Create a dummy python file in a temporary directory
    file_path = tmp_path / "test_fallback.py"
    file_path.write_text("def fallback_func(): pass", encoding="utf-8")
    
    src = SourceFile(id="s1", path=str(file_path.name), role="reality", confidence=1.0)
    
    # extract_evidence catches the ConnectionError and falls back to AST extraction (_static_facts)
    bundle = extract_evidence(tmp_path, [src])
    
    # Verify the fallback successfully extracted the python facts instead of failing
    assert len(bundle.implementation_facts) == 1
    assert "Defines function fallback_func" in bundle.implementation_facts[0].fact
