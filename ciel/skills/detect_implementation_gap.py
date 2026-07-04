import json
import logging
import re
from typing import List

from ciel.inference.local_inference_adapter import query_ollama
from ciel.orchestrator.purpose_resolver import extract_json_block
from ciel.schemas.evidence import EvidenceBundle
from ciel.schemas.gap_report import GapMatrixItem

logger = logging.getLogger(__name__)

STOPWORDS = {
    "the", "and", "for", "with", "from", "this", "that", "into", "must", "should",
    "project", "kernel", "ciel", "using", "based", "your", "you", "are", "what",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_]{2,}", text.lower())
        if token not in STOPWORDS and len(token) > 3
    }


def _match_fact_ids(claim: str, facts: list[dict]) -> list[str]:
    claim_tokens = _tokens(claim)
    if not claim_tokens:
        return []

    scored: list[tuple[float, str]] = []
    for fact in facts:
        fact_tokens = _tokens(fact["fact"])
        if not fact_tokens:
            continue
        overlap = claim_tokens & fact_tokens
        score = len(overlap) / max(len(claim_tokens), 1)
        if score >= 0.25:
            scored.append((score, fact["id"]))

    scored.sort(reverse=True)
    return [fact_id for _, fact_id in scored[:5]]


def detect_gap_fallback(bundle: EvidenceBundle) -> List[GapMatrixItem]:
    gaps: list[GapMatrixItem] = []
    facts = [{"id": f.id, "fact": f.fact} for f in bundle.implementation_facts]

    for claim in bundle.intention_claims:
        evidence = _match_fact_ids(claim.claim, facts)
        if evidence:
            status = "implemented"
            classification = "partial" if len(evidence) == 1 else "production_ready"
            severity = "low" if classification == "production_ready" else "medium"
            interpretation = "The claim has matching implementation evidence, but deeper behavioral validation may still be needed."
            recommended_action = "Back this claim with focused tests and keep it in the release scope."
        else:
            status = "roadmap_gap"
            classification = "missing_feature"
            severity = "high"
            interpretation = "No concrete implementation evidence matched this documented claim."
            recommended_action = "Either implement this claim or remove it from release-facing documentation."

        gaps.append(
            GapMatrixItem(
                claim_id=claim.id,
                claim=claim.claim,
                status=status,
                classification=classification,
                evidence=evidence,
                severity=severity,
                interpretation=interpretation,
                recommended_action=recommended_action,
            )
        )
    return gaps


def detect_gap(bundle: EvidenceBundle) -> List[GapMatrixItem]:
    claims = [{"id": c.id, "claim": c.claim} for c in bundle.intention_claims]
    facts = [{"id": f.id, "fact": f.fact} for f in bundle.implementation_facts]

    if not claims:
        return []

    prompt = (
        "Compare documented claims to implementation facts. Return JSON only as an array. "
        "Allowed status: implemented, roadmap_gap, technical_debt, architecture_drift. "
        "Allowed classification: production_ready, missing_feature, bug, partial. "
        "Allowed severity: low, medium, high.\n"
        f"Claims: {json.dumps(claims)}\nFacts: {json.dumps(facts)}"
    )

    try:
        response_text = query_ollama(prompt)
        if response_text.startswith("Error"):
            return detect_gap_fallback(bundle)

        data = json.loads(extract_json_block(response_text))
        if isinstance(data, dict):
            data = data.get("gaps", data.get("gap_matrix", []))
        if not isinstance(data, list):
            raise ValueError("expected a list of gaps")

        gaps = []
        for item in data:
            if not isinstance(item, dict) or "claim_id" not in item:
                continue
            item["evidence"] = [str(x) for x in item.get("evidence", [])]
            gaps.append(GapMatrixItem.model_validate(item))

        return gaps or detect_gap_fallback(bundle)
    except Exception as exc:
        logger.warning("LLM gap detection failed: %s", exc)
        return detect_gap_fallback(bundle)
