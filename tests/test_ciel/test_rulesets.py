import pytest
from pathlib import Path
from ciel.schemas.ruleset import Ruleset
from ciel.skills.load_rulesets import load_ruleset
from ciel.schemas.evidence import EvidenceBundle, ProjectInfo
from ciel.schemas.gap_report import GapMatrixItem
from ciel.skills.audit_repo_maturity import audit_maturity_fallback

@pytest.fixture
def mock_rulesets_dir(tmp_path):
    rulesets_dir = tmp_path / "rulesets"
    rulesets_dir.mkdir()
    
    # Create a mock agent-safe-repo.yaml
    content = """
id: agent-safe-repo
version: 0.1.0
required:
  - tests_present
  - ci_present
thresholds:
  maturity_score_min: 0.80
"""
    (rulesets_dir / "agent-safe-repo.yaml").write_text(content)
    return rulesets_dir

def test_load_ruleset(mock_rulesets_dir):
    ruleset = load_ruleset("agent-safe-repo", search_paths=[mock_rulesets_dir])
    
    assert ruleset.id == "agent-safe-repo"
    assert ruleset.version == "0.1.0"
    assert "tests_present" in ruleset.required
    assert ruleset.thresholds.maturity_score_min == 0.80
    assert ruleset.hash is not None

def test_load_ruleset_not_found(mock_rulesets_dir):
    with pytest.raises(FileNotFoundError):
        load_ruleset("non-existent-ruleset", search_paths=[mock_rulesets_dir])


def test_load_invalid_ruleset_fails_clearly(mock_rulesets_dir):
    (mock_rulesets_dir / "invalid.yaml").write_text("- not\n- a\n- mapping\n")

    with pytest.raises(ValueError, match="Formato YAML inválido"):
        load_ruleset("invalid", search_paths=[mock_rulesets_dir])

def test_audit_maturity_with_ruleset(mock_rulesets_dir):
    ruleset = load_ruleset("agent-safe-repo", search_paths=[mock_rulesets_dir])
    
    bundle = EvidenceBundle(
        project=ProjectInfo(name="test", primary_language="python"),
        sources=[],
        intention_claims=[],
        implementation_facts=[],
        behavior_evidence=[], # Missing tests!
        operational_evidence=[] # Missing CI!
    )
    
    score, verdict, actions = audit_maturity_fallback(bundle, gaps=[], ruleset=ruleset)
    
    assert score.commercial_readiness == 0.0
    assert verdict.stage == "ideation"
    assert "missing_required_policy_checks" in verdict.main_bottleneck
    assert "tests_present" in verdict.main_bottleneck
