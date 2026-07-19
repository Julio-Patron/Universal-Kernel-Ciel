from ciel_gate.contracts import ChangeProposal, GateDecision, PolicyViolation, DiffFacts
from ciel_gate.policy.schema import Ruleset

def evaluate_proposal(proposal: ChangeProposal, policy: Ruleset, facts: DiffFacts, diff_hash: str, policy_hash: str) -> GateDecision:
    """Evaluates a change proposal against a policy."""
    violations = []
    
    # 1. Protected paths
    # (Simplified for now)
    
    # 2. Deny rules
    # (Simplified for now)
    
    # 3. Limits
    # (Simplified for now)
    
    verdict = "allow"
    risk = "low"
    
    if violations:
        verdict = "deny"
        risk = "high"
        
    return GateDecision(
        verdict=verdict,
        risk=risk,
        violations=violations,
        diff_hash=diff_hash,
        policy_hash=policy_hash
    )
