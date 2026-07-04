import pytest
from unittest.mock import patch
from ciel.skills.detect_implementation_gap import detect_gap
from ciel.skills.audit_repo_maturity import audit_maturity
from ciel.schemas.evidence import EvidenceBundle, ProjectInfo, IntentionClaim, ImplementationFact

@pytest.fixture
def dummy_bundle():
    return EvidenceBundle(
        project=ProjectInfo(name="Test"),
        intention_claims=[
            IntentionClaim(id="c1", source_id="s1", claim="Must do X")
        ],
        implementation_facts=[
            ImplementationFact(id="f1", source_id="s2", fact="Does X", fact_type="implemented_capability")
        ],
        behavior_evidence=[]
    )

@patch("ciel.skills.detect_implementation_gap.query_ollama")
def test_detect_gap_valid_json(mock_query, dummy_bundle):
    mock_query.return_value = """
    ```json
    [
      {
        "claim_id": "c1",
        "claim": "Must do X",
        "status": "implemented",
        "classification": "production_ready",
        "evidence": ["f1"],
        "severity": "low",
        "interpretation": "It is done.",
        "recommended_action": "None"
      }
    ]
    ```
    """
    gaps = detect_gap(dummy_bundle)
    assert len(gaps) == 1
    assert gaps[0].status == "implemented"
    assert gaps[0].interpretation == "It is done."

@patch("ciel.skills.detect_implementation_gap.query_ollama")
def test_detect_gap_invalid_json(mock_query, dummy_bundle):
    mock_query.return_value = "Not a json"
    gaps = detect_gap(dummy_bundle)
    assert len(gaps) == 1
    # Fallback behavior when words don't match
    assert gaps[0].interpretation == "The documented claim has no matching implementation."

@patch("ciel.skills.detect_implementation_gap.query_ollama")
def test_detect_gap_ollama_error(mock_query, dummy_bundle):
    mock_query.return_value = "Error connecting to local inference: Connection refused"
    gaps = detect_gap(dummy_bundle)
    assert len(gaps) == 1
    assert gaps[0].interpretation == "The documented claim has no matching implementation."

@patch("ciel.skills.audit_repo_maturity.query_ollama")
def test_audit_maturity_valid_json(mock_query, dummy_bundle):
    mock_query.return_value = """
    ```json
    {
      "maturity_score": {
        "intention_clarity": 0.9,
        "implementation_completeness": 0.5,
        "behavior_confidence": 0.0,
        "operational_readiness": 0.1,
        "commercial_readiness": 0.2
      },
      "verdict": {
        "stage": "alpha",
        "summary": "Sum",
        "main_bottleneck": "bottleneck"
      },
      "next_actions": [
        {
          "priority": 1,
          "type": "coding",
          "description": "desc",
          "reason": "reason"
        }
      ]
    }
    ```
    """
    from ciel.schemas.gap_report import GapMatrixItem
    gaps = [GapMatrixItem(claim_id="c1", claim="c", status="s", classification="c", evidence=[], severity="low", interpretation="i", recommended_action="r")]
    score, verdict, actions = audit_maturity(dummy_bundle, gaps)
    assert score.intention_clarity == 0.9
    assert verdict.stage == "alpha"
    assert actions[0].type == "coding"

@patch("ciel.skills.audit_repo_maturity.query_ollama")
def test_audit_maturity_ollama_error(mock_query, dummy_bundle):
    mock_query.return_value = "Error connecting to local inference: Connection refused"
    gaps = []
    score, verdict, actions = audit_maturity(dummy_bundle, gaps)
    # Fallback values when bundle has claims and facts
    assert score.intention_clarity == 0.9
    assert verdict.stage == "technical_core_ready"
