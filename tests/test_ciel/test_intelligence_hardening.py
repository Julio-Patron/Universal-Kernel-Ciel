from unittest.mock import patch

from ciel.schemas.evidence import EvidenceBundle, ImplementationFact, IntentionClaim, ProjectInfo
from ciel.schemas.gap_report import GapMatrixItem
from ciel.skills.audit_repo_maturity import audit_maturity
from ciel.skills.detect_implementation_gap import detect_gap


def sample_bundle():
    return EvidenceBundle(
        project=ProjectInfo(name="Test", primary_language="python"),
        intention_claims=[IntentionClaim(id="c1", source_id="s1", claim="local inference adapter", claim_type="capability")],
        implementation_facts=[ImplementationFact(id="f1", source_id="s2", fact="Provides a local inference adapter", fact_type="implemented_capability")],
        behavior_evidence=[],
        sources=[],
    )


def test_gap_fallback_uses_matching_evidence():
    with patch("ciel.skills.detect_implementation_gap.query_ollama", return_value="not-json"):
        gaps = detect_gap(sample_bundle())
    assert gaps[0].status == "implemented"
    assert gaps[0].evidence == ["f1"]


def test_maturity_fallback_uses_evidence_counts():
    gap = GapMatrixItem(claim_id="c1", claim="c", status="implemented", classification="production_ready", evidence=["f1"], severity="low", interpretation="i", recommended_action="r")
    with patch("ciel.skills.audit_repo_maturity.query_ollama", return_value="Error"):
        score, verdict, actions = audit_maturity(sample_bundle(), [gap])
    assert score.implementation_completeness == 1.0
    assert verdict.stage == "technical_core_ready"
    assert actions
