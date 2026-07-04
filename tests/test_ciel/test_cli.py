from typer.testing import CliRunner
from ciel.cli.main import app

runner = CliRunner()

def test_analyze_command():
    result = runner.invoke(app, ["analyze", "./"])
    assert result.exit_code == 0
    assert "Verdict" in result.stdout
    assert "Implementation Gap Matrix" in result.stdout

def test_purpose_command():
    result = runner.invoke(app, ["purpose", "what to do"])
    assert result.exit_code == 0
    assert "repo_analysis" in result.stdout
    assert "what_to_do_first" in result.stdout

def test_sources_command():
    result = runner.invoke(app, ["sources", "./"])
    assert result.exit_code == 0
    assert "intention" in result.stdout
    assert "reality" in result.stdout

def test_gap_command():
    result = runner.invoke(app, ["gap", "./"])
    assert result.exit_code == 0
    assert "claim_id" in result.stdout
    assert "classification" in result.stdout

def test_report_command():
    result_json = runner.invoke(app, ["report", "./", "--format", "json"])
    assert result_json.exit_code == 0
    assert "schema_version" in result_json.stdout
    assert "ciel.gap_report.v1.0" in result_json.stdout

    result_md = runner.invoke(app, ["report", "./", "--format", "markdown"])
    assert result_md.exit_code == 0
    assert "# Ciel Analysis Report:" in result_md.stdout
    assert "## Implementation Gap Matrix" in result_md.stdout

from unittest.mock import patch

@patch("ciel.orchestrator.purpose_resolver.route_inference")
@patch("ciel.rag.evidence_extractor.route_inference")
@patch("ciel.skills.detect_implementation_gap.route_inference")
@patch("ciel.skills.audit_repo_maturity.route_inference")
def test_analyze_command_offline_fallback(mock_audit, mock_detect, mock_extract, mock_purpose):
    error_msg = "Error connecting to local inference: connection refused"
    mock_purpose.return_value = error_msg
    mock_extract.return_value = error_msg
    mock_detect.return_value = error_msg
    mock_audit.return_value = error_msg
    
    result = runner.invoke(app, ["analyze", "./"])
    assert result.exit_code == 0
    assert "Verdict" in result.stdout
    assert "Implementation Gap Matrix" in result.stdout
