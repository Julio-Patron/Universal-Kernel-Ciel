from typing import List
from pathlib import Path
from ciel.schemas.evidence import (
    SourceFile, 
    EvidenceBundle, 
    ProjectInfo,
    IntentionClaim,
    ImplementationFact,
    BehaviorEvidence
)
import re

def extract_evidence(repo_path: Path, sources: List[SourceFile]) -> EvidenceBundle:
    """Extracts evidence from sources into a bundle."""
    claims = []
    facts = []
    behaviors = []
    
    claim_counter = 1
    fact_counter = 1
    
    for src in sources:
        abs_path = repo_path / src.path
        if not abs_path.exists():
            continue
            
        try:
            content = abs_path.read_text(encoding="utf-8")
        except Exception:
            continue
            
        if src.role == "intention":
            # Very basic markdown heading extraction as a placeholder for LLM extraction
            for line in content.splitlines():
                if line.startswith("# ") or line.startswith("## "):
                    claims.append(IntentionClaim(
                        id=f"c{claim_counter}",
                        source_id=src.id,
                        claim=line.strip("# ").strip(),
                        claim_type="capability"
                    ))
                    claim_counter += 1
                    
        elif src.role == "reality":
            # Extract basic function/class definitions
            for line in content.splitlines():
                if line.strip().startswith("def ") or line.strip().startswith("class "):
                    name = line.replace("def ", "").replace("class ", "").split("(")[0].split(":")[0].strip()
                    facts.append(ImplementationFact(
                        id=f"f{fact_counter}",
                        source_id=src.id,
                        fact=f"Implemented {name}",
                        fact_type="implemented_capability"
                    ))
                    fact_counter += 1
                    
        elif src.role == "behavior":
            behaviors.append(BehaviorEvidence(
                id=f"b{len(behaviors)+1}",
                source_id=src.id,
                evidence="Found test definitions",
                evidence_type="test_suite"
            ))

    project_info = ProjectInfo(
        name=repo_path.name,
        primary_language="Python" # Hardcoded for now
    )
    
    return EvidenceBundle(
        project=project_info,
        sources=sources,
        intention_claims=claims,
        implementation_facts=facts,
        behavior_evidence=behaviors
    )
