import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from ciel.schemas.evidence import SourceFile, ImplementationFact
from ciel.rag.evidence_extractor import extract_evidence

def test_extract_evidence_llm_success():
    """Test successful LLM fact extraction mapping to ImplementationFact."""
    # Setup mock LLM response returning list
    mock_response = """
    Here is the JSON list:
    ```json
    [
      {
        "fact": "Provides a local inference adapter to query Ollama",
        "fact_type": "implemented_capability"
      },
      {
        "fact": "Supports custom model routing",
        "fact_type": "custom_type"
      }
    ]
    ```
    """
    
    repo_path = Path("fake_repo")
    sources = [
        SourceFile(id="s1", path="main.py", role="reality", confidence=1.0)
    ]
    
    with patch("ciel.rag.evidence_extractor.query_ollama") as mock_query, \
         patch.object(Path, "exists", return_value=True), \
         patch.object(Path, "read_text", return_value="def hello():\n    pass"):
         
        mock_query.return_value = mock_response
        
        bundle = extract_evidence(repo_path, sources)
        
        # Verify mocked query was called
        mock_query.assert_called_once()
        
        # Assert facts are extracted by LLM
        assert len(bundle.implementation_facts) == 2
        assert bundle.implementation_facts[0].id == "f1"
        assert bundle.implementation_facts[0].source_id == "s1"
        assert bundle.implementation_facts[0].fact == "Provides a local inference adapter to query Ollama"
        assert bundle.implementation_facts[0].fact_type == "implemented_capability"
        
        assert bundle.implementation_facts[1].id == "f2"
        assert bundle.implementation_facts[1].source_id == "s1"
        assert bundle.implementation_facts[1].fact == "Supports custom model routing"
        assert bundle.implementation_facts[1].fact_type == "custom_type"

def test_extract_evidence_llm_dict_wrapped_success():
    """Test successful LLM fact extraction when wrapped in a dict object."""
    mock_response = """
    {
      "facts": [
        {
          "fact": "Wrapped in a dictionary facts key"
        }
      ]
    }
    """
    
    repo_path = Path("fake_repo")
    sources = [
        SourceFile(id="s1", path="main.py", role="reality", confidence=1.0)
    ]
    
    with patch("ciel.rag.evidence_extractor.query_ollama") as mock_query, \
         patch.object(Path, "exists", return_value=True), \
         patch.object(Path, "read_text", return_value="def hello():\n    pass"):
         
        mock_query.return_value = mock_response
        
        bundle = extract_evidence(repo_path, sources)
        
        mock_query.assert_called_once()
        assert len(bundle.implementation_facts) == 1
        assert bundle.implementation_facts[0].fact == "Wrapped in a dictionary facts key"
        assert bundle.implementation_facts[0].fact_type == "implemented_capability"

def test_extract_evidence_llm_single_object_success():
    """Test successful LLM fact extraction when returning a single object instead of a list."""
    mock_response = """
    {
      "fact": "Single object fact extraction",
      "fact_type": "implemented_capability"
    }
    """
    
    repo_path = Path("fake_repo")
    sources = [
        SourceFile(id="s1", path="main.py", role="reality", confidence=1.0)
    ]
    
    with patch("ciel.rag.evidence_extractor.query_ollama") as mock_query, \
         patch.object(Path, "exists", return_value=True), \
         patch.object(Path, "read_text", return_value="def hello():\n    pass"):
         
        mock_query.return_value = mock_response
        
        bundle = extract_evidence(repo_path, sources)
        
        mock_query.assert_called_once()
        assert len(bundle.implementation_facts) == 1
        assert bundle.implementation_facts[0].fact == "Single object fact extraction"

def test_extract_evidence_connection_fallback_and_disable():
    """Test fallback on connection error and setting llm_disabled to True."""
    repo_path = Path("fake_repo")
    sources = [
        SourceFile(id="s1", path="main.py", role="reality", confidence=1.0),
        SourceFile(id="s2", path="other.py", role="reality", confidence=1.0)
    ]
    
    # We want s1 to cause connection error, which disables LLM.
    # Therefore, s2 should NOT trigger query_ollama at all.
    with patch("ciel.rag.evidence_extractor.query_ollama") as mock_query, \
         patch.object(Path, "exists", return_value=True), \
         patch.object(Path, "read_text", side_effect=["def hello():\n    pass", "class Goodbye:\n    pass"]):
         
        mock_query.return_value = "Error connecting to local inference: Connection refused"
        
        bundle = extract_evidence(repo_path, sources)
        
        # query_ollama should only be called once (for the first file)
        mock_query.assert_called_once()
        
        # Check that both files fell back to static parsing
        assert len(bundle.implementation_facts) == 2
        assert bundle.implementation_facts[0].source_id == "s1"
        assert bundle.implementation_facts[0].fact == "Implemented hello"
        
        assert bundle.implementation_facts[1].source_id == "s2"
        assert bundle.implementation_facts[1].fact == "Implemented Goodbye"

def test_extract_evidence_parsing_fallback():
    """Test fallback to static parser on parsing failures (invalid JSON, empty response, empty list)."""
    repo_path = Path("fake_repo")
    sources = [
        SourceFile(id="s1", path="main.py", role="reality", confidence=1.0)
    ]
    
    # Test case 1: invalid JSON
    with patch("ciel.rag.evidence_extractor.query_ollama", return_value="invalid json") as mock_query, \
         patch.object(Path, "exists", return_value=True), \
         patch.object(Path, "read_text", return_value="def hello():\n    pass"):
         
        bundle = extract_evidence(repo_path, sources)
        mock_query.assert_called_once()
        assert len(bundle.implementation_facts) == 1
        assert bundle.implementation_facts[0].fact == "Implemented hello"

    # Test case 2: empty list from LLM
    with patch("ciel.rag.evidence_extractor.query_ollama", return_value="[]") as mock_query, \
         patch.object(Path, "exists", return_value=True), \
         patch.object(Path, "read_text", return_value="def hello():\n    pass"):
         
        bundle = extract_evidence(repo_path, sources)
        mock_query.assert_called_once()
        assert len(bundle.implementation_facts) == 1
        assert bundle.implementation_facts[0].fact == "Implemented hello"
