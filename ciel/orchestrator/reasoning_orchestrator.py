from ciel.schemas.evidence import EvidenceBundle
from ciel.schemas.gap_report import ImplementationGapReport, GapProjectInfo
from ciel.skills.detect_implementation_gap import detect_gap
from ciel.skills.audit_repo_maturity import audit_maturity

def orchestrate_reasoning(bundle: EvidenceBundle) -> ImplementationGapReport:
    """Fuses evidence bundle with skills to produce final gap report."""
    
    gap_matrix = detect_gap(bundle)
    score, verdict, actions = audit_maturity(bundle, gap_matrix)
    
    return ImplementationGapReport(
        project=GapProjectInfo(name=bundle.project.name),
        gap_matrix=gap_matrix,
        maturity_score=score,
        verdict=verdict,
        next_actions=actions
    )
