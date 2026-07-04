from typer.testing import CliRunner
from ciel.cli.main import app

runner = CliRunner()

def test_analyze_command():
    result = runner.invoke(app, ["analyze", "./repo"])
    assert result.exit_code == 0
    assert "Analyzing repository at repo" in result.stdout

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
    result = runner.invoke(app, ["gap", "./repo"])
    assert result.exit_code == 0
    assert "Detecting gap for repository at repo" in result.stdout

def test_report_command():
    result = runner.invoke(app, ["report", "./repo", "--format", "json"])
    assert result.exit_code == 0
    assert "Generating report for repository at repo in json format" in result.stdout
