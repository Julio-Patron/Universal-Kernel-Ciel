from typing import List
from ciel.schemas.evidence import EvidenceBundle
from ciel.schemas.gap_report import GapMatrixItem

import json
import logging
from ciel.inference.local_inference_adapter import query_ollama
from ciel.orchestrator.purpose_resolver import extract_json_block

logger = logging.getLogger(__name__)

def detect_gap_fallback(bundle: EvidenceBundle) -> List[GapMatrixItem]:
    """Fallback: Compares intention claims with reality facts using simple word count."""
    gaps = []
    facts_str = " ".join([f.fact.lower() for f in bundle.implementation_facts])
    
    for claim in bundle.intention_claims:
        claim_text = claim.claim.lower()
        if any(word in facts_str for word in claim_text.split() if len(word) > 4):
            status, classification, severity = "implemented", "production_ready", "low"
            interpretation = "The documented core claim is backed by implementation."
            recommended_action = "Package this capability."
        else:
            status, classification, severity = "roadmap_gap", "missing_feature", "high"
            interpretation = "The documented claim has no matching implementation."
            recommended_action = "Evaluate if this needs to be built."
            
        gaps.append(GapMatrixItem(
            claim_id=claim.id,
            claim=claim.claim,
            status=status,
            classification=classification,
            evidence=[f.id for f in bundle.implementation_facts],
            severity=severity,
            interpretation=interpretation,
            recommended_action=recommended_action
        ))
    return gaps

def detect_gap(bundle: EvidenceBundle) -> List[GapMatrixItem]:
    """Compares intention claims with reality facts to produce gap matrix using semantic LLM evaluation."""
    claims = [{"id": c.id, "claim": c.claim} for c in bundle.intention_claims]
    facts = [{"id": f.id, "fact": f.fact} for f in bundle.implementation_facts]
    
    if not claims:
        return []
        
    llm_prompt = f"""You are the Ciel Kernel Implementation Gap Detector.
Compare the following Intention Claims (what the project wants to do) against the Implementation Facts (what is actually built).

Intention Claims:
{json.dumps(claims, indent=2)}

Implementation Facts:
{json.dumps(facts, indent=2)}

Your task is to output a single valid JSON array of gap objects exactly matching this schema:
[
  {{
    "claim_id": "c1",
    "claim": "The exact text of the claim",
    "status": "implemented" OR "roadmap_gap" OR "technical_debt" OR "architecture_drift",
    "classification": "production_ready" OR "missing_feature" OR "bug" OR "partial",
    "evidence": ["f1", "f2"], 
    "severity": "low", "medium", or "high",
    "interpretation": "A 1-2 sentence semantic explanation of why this gap status was chosen.",
    "recommended_action": "A 1 sentence recommendation."
  }}
]
Rules:
1. "evidence" must be a list of matching fact IDs. Empty list if none.
2. Output must be a single valid JSON array wrapped in ```json ``` tags.
"""
    try:
        response_text = query_ollama(llm_prompt, model="llama3")
        if response_text.startswith("Error"):
            logger.warning(f"Ollama error in gap detection: {response_text}. Using fallback.")
            return detect_gap_fallback(bundle)
            
        json_str = extract_json_block(response_text)
        data = json.loads(json_str)
        
        if isinstance(data, dict):
            data = data.get("gaps", data.get("gap_matrix", []))
            
        if not isinstance(data, list):
            raise ValueError("Expected a list of gaps from LLM.")
            
        gaps = []
        for item in data:
            if "claim_id" not in item:
                continue
            item["evidence"] = [str(x) for x in item.get("evidence", [])]
            gaps.append(GapMatrixItem.model_validate(item))
            
        if not gaps:
            return detect_gap_fallback(bundle)
            
        return gaps
    except Exception as e:
        logger.warning(f"LLM gap detection failed: {e}. Using fallback.")
        return detect_gap_fallback(bundle)
