import json
import logging
from typing import List, Tuple

from ciel.inference.model_router import route_inference
from ciel.orchestrator.purpose_resolver import extract_json_block
from ciel.schemas.evidence import EvidenceBundle
from ciel.schemas.gap_report import GapMatrixItem, MaturityScore, NextAction, Verdict

logger = logging.getLogger(__name__)


def _ratio(part: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round(max(0.0, min(1.0, part / total)), 2)


def audit_maturity_fallback(bundle: EvidenceBundle, gaps: list[GapMatrixItem]) -> Tuple[MaturityScore, Verdict, List[NextAction]]:
    total_claims = len(bundle.intention_claims)
    implemented = sum(1 for gap in gaps if gap.status == "implemented")
    high_gaps = sum(1 for gap in gaps if gap.severity == "high")

    implementation_completeness = _ratio(implemented, total_claims) if total_claims else (0.4 if bundle.implementation_facts else 0.0)
    behavior_confidence = 0.75 if bundle.behavior_evidence else 0.15
    operational_readiness = 0.75 if bundle.operational_evidence else 0.2
    commercial_readiness = round(min(implementation_completeness, behavior_confidence, operational_readiness), 2)
    if high_gaps:
        commercial_readiness = max(0.0, round(commercial_readiness - 0.1, 2))

    score = MaturityScore(
        intention_clarity=0.85 if total_claims else 0.2,
        implementation_completeness=implementation_completeness,
        behavior_confidence=behavior_confidence,
        operational_readiness=operational_readiness,
        commercial_readiness=commercial_readiness,
    )

    if score.commercial_readiness >= 0.9 and high_gaps == 0:
        stage = "production"
    elif score.commercial_readiness >= 0.75 and high_gaps == 0:
        stage = "beta"
    elif bundle.implementation_facts and bundle.behavior_evidence:
        stage = "alpha"
    elif bundle.implementation_facts:
        stage = "technical_core_ready"
    else:
        stage = "ideation"

    if high_gaps:
        bottleneck = "implementation_gaps"
    elif not bundle.behavior_evidence:
        bottleneck = "test_coverage"
    elif not bundle.operational_evidence:
        bottleneck = "release_operations"
    else:
        bottleneck = "distribution"

    verdict = Verdict(
        stage=stage,
        summary=f"Detected {implemented}/{total_claims} documented claims with matching implementation evidence.",
        main_bottleneck=bottleneck,
    )

    actions: list[NextAction] = []
    if high_gaps:
        actions.append(NextAction(priority=1, type="coding", description="Close high-severity roadmap gaps.", reason="Documented claims need implementation evidence."))
    if not bundle.behavior_evidence:
        actions.append(NextAction(priority=2, type="testing", description="Add automated tests for CLI and fallback logic.", reason="Reports must be verified."))
    if not bundle.operational_evidence:
        actions.append(NextAction(priority=3, type="release", description="Add CI and build validation.", reason="Releases need repeatable checks."))
    if not actions:
        actions.append(NextAction(priority=1, type="release", description="Prepare a tagged release candidate.", reason="Core quality gates are present."))

    return score, verdict, actions


def audit_maturity(bundle: EvidenceBundle, gaps: list[GapMatrixItem]) -> Tuple[MaturityScore, Verdict, List[NextAction]]:
    gaps_summary = [{"claim": g.claim, "status": g.status, "severity": g.severity} for g in gaps]
    prompt = "Return JSON maturity_score, verdict and next_actions for this gap summary: " + json.dumps(gaps_summary)

    try:
        response_text = route_inference(prompt)
        if response_text.startswith("Error"):
            return audit_maturity_fallback(bundle, gaps)

        data = json.loads(extract_json_block(response_text))
        score = MaturityScore.model_validate(data["maturity_score"])
        verdict = Verdict.model_validate(data["verdict"])
        actions = [NextAction.model_validate(action) for action in data["next_actions"]]
        return score, verdict, actions
    except Exception as exc:
        logger.warning("LLM audit failed: %s", exc)
        return audit_maturity_fallback(bundle, gaps)
