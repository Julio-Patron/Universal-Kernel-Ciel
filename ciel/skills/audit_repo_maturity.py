from ciel.schemas.evidence import EvidenceBundle
from ciel.schemas.gap_report import MaturityScore, Verdict, NextAction
from typing import Tuple, List

def audit_maturity(bundle: EvidenceBundle, gaps: list) -> Tuple[MaturityScore, Verdict, List[NextAction]]:
    """Calculates maturity scores and final verdicts based on the gap matrix."""
    
    # Dummy calculation for V0 based on counts
    has_intention = len(bundle.intention_claims) > 0
    has_reality = len(bundle.implementation_facts) > 0
    has_behavior = len(bundle.behavior_evidence) > 0
    
    score = MaturityScore(
        intention_clarity=0.9 if has_intention else 0.2,
        implementation_completeness=0.75 if has_reality else 0.1,
        behavior_confidence=0.8 if has_behavior else 0.0,
        operational_readiness=0.5,
        commercial_readiness=0.6 if has_reality else 0.1
    )
    
    verdict = Verdict(
        stage="technical_core_ready" if has_reality else "ideation",
        summary="The core engine appears valuable, but distribution is incomplete." if has_reality else "No code found.",
        main_bottleneck="commercial_distribution_layer" if has_reality else "implementation"
    )
    
    actions = [
        NextAction(
            priority=1,
            type="packaging" if has_reality else "coding",
            description="Package the working core as the first sellable unit." if has_reality else "Start coding.",
            reason="Commercial value depends on distribution."
        )
    ]
    
    return score, verdict, actions
