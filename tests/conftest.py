import pytest
from ciel.schemas.evidence import EvidenceBundle, ProjectInfo, IntentionClaim, ImplementationFact

@pytest.fixture
def dummy_bundle():
    """Returns a minimal valid EvidenceBundle for testing."""
    return EvidenceBundle(
        project=ProjectInfo(name="TestProject", primary_language="python"),
        intention_claims=[
            IntentionClaim(
                id="claim_test_1",
                source_id="doc_1",
                claim="The system must support offline CI mode.",
                claim_type="architectural_decision"
            )
        ],
        implementation_facts=[
            ImplementationFact(
                id="fact_test_1",
                source_id="code_1",
                fact="The CLI skips LLM queries when CIEL_DISABLE_LLM=1.",
                fact_type="implemented_capability"
            )
        ],
        behavior_evidence=[],
        sources=[]
    )
