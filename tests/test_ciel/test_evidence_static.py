from pathlib import Path
from unittest.mock import patch

from ciel.rag.evidence_extractor import extract_evidence
from ciel.schemas.evidence import SourceFile


def test_static_python_parser_extracts_function():
    repo_path = Path("repo")
    sources = [SourceFile(id="main.py", path="main.py", role="reality", confidence=1.0)]
    with patch("ciel.rag.evidence_extractor.route_inference", return_value="not-json"), patch.object(Path, "exists", return_value=True), patch.object(Path, "read_text", return_value="def hello():\n    pass"):
        bundle = extract_evidence(repo_path, sources)
    assert bundle.implementation_facts[0].fact == "Defines function hello"


def test_static_structure_parser_extracts_pyproject_sections():
    repo_path = Path("repo")
    sources = [SourceFile(id="pyproject.toml", path="pyproject.toml", role="structure", confidence=1.0)]
    content = '[project]\nname = "sample"\n\n[project.scripts]\nsample = "sample.cli:app"'
    with patch.object(Path, "exists", return_value=True), patch.object(Path, "read_text", return_value=content):
        bundle = extract_evidence(repo_path, sources)
    assert len(bundle.implementation_facts) == 2
