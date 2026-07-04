from ciel.schemas.evidence import EvidenceBundle
from ciel.schemas.gap_report import MaturityScore, Verdict, NextAction
import json
import logging
from typing import Tuple, List
from ciel.inference.local_inference_adapter import query_ollama
from ciel.orchestrator.purpose_resolver import extract_json_block

logger = logging.getLogger(__name__)

def audit_maturity_fallback(bundle: EvidenceBundle, gaps: list) -> Tuple[MaturityScore, Verdict, List[NextAction]]:
    """Fallback: Calculates maturity scores and final verdicts based on simple counts."""
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

def audit_maturity(bundle: EvidenceBundle, gaps: list) -> Tuple[MaturityScore, Verdict, List[NextAction]]:
    """Calculates maturity scores and final verdicts based on the gap matrix using semantic LLM evaluation."""
    gaps_summary = [{"claim": g.claim, "status": g.status} for g in gaps]
    
    llm_prompt = f"""You are the Ciel Kernel Repo Maturity Auditor.
Based on the following Gap Matrix of this repository, generate a maturity score, a verdict, and next actions.

Gap Matrix:
{json.dumps(gaps_summary, indent=2)}

Output a single valid JSON object exactly matching this schema:
{{
  "maturity_score": {{
    "intention_clarity": 0.9,
    "implementation_completeness": 0.5,
    "behavior_confidence": 0.0,
    "operational_readiness": 0.1,
    "commercial_readiness": 0.2
  }},
  "verdict": {{
    "stage": "ideation" OR "technical_core_ready" OR "alpha" OR "beta" OR "production",
    "summary": "1 sentence summary",
    "main_bottleneck": "1-3 words identifying the bottleneck"
  }},
  "next_actions": [
    {{
      "priority": 1,
      "type": "coding" OR "packaging" OR "testing" OR "docs",
      "description": "What to do next",
      "reason": "Why do it"
    }}
  ]
}}
Rules:
1. All scores must be floats between 0.0 and 1.0.
2. Return only the valid JSON object within ```json ``` tags.
"""
    try:
        response_text = query_ollama(llm_prompt, model="llama3")
        if response_text.startswith("Error"):
            logger.warning(f"Ollama error in audit: {response_text}. Using fallback.")
            return audit_maturity_fallback(bundle, gaps)
            
        json_str = extract_json_block(response_text)
        data = json.loads(json_str)
        
        score = MaturityScore.model_validate(data["maturity_score"])
        verdict = Verdict.model_validate(data["verdict"])
        actions = [NextAction.model_validate(a) for a in data["next_actions"]]
        
        return score, verdict, actions
    except Exception as e:
        logger.warning(f"LLM audit failed: {e}. Using fallback.")
        return audit_maturity_fallback(bundle, gaps)
