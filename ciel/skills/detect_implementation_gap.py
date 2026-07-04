from typing import List
from ciel.schemas.evidence import EvidenceBundle
from ciel.schemas.gap_report import GapMatrixItem

def detect_gap(bundle: EvidenceBundle) -> List[GapMatrixItem]:
    """Compares intention claims with reality facts to produce gap matrix."""
    gaps = []
    
    # PROVISIONAL SCAFFOLD: Very naive semantic matching simulation via word count.
    # This is NOT production-grade reasoning and serves only as a Phase 4 placeholder.
    facts_str = " ".join([f.fact.lower() for f in bundle.implementation_facts])
    
    for claim in bundle.intention_claims:
        claim_text = claim.claim.lower()
        
        # Naive keyword intersection
        if any(word in facts_str for word in claim_text.split() if len(word) > 4):
            status = "implemented"
            classification = "production_ready"
            severity = "low"
            interpretation = "The documented core claim is backed by implementation."
            recommended_action = "Package this capability."
        else:
            status = "roadmap_gap"
            classification = "missing_feature"
            severity = "high"
            interpretation = "The documented claim has no matching implementation."
            recommended_action = "Evaluate if this needs to be built."
            
        gaps.append(GapMatrixItem(
            claim_id=claim.id,
            claim=claim.claim,
            status=status,
            classification=classification,
            evidence=[f.id for f in bundle.implementation_facts], # Simplification
            severity=severity,
            interpretation=interpretation,
            recommended_action=recommended_action
        ))
        
    return gaps
