import ast
import json
import logging
import re
from collections import Counter
from pathlib import Path
from typing import List

from ciel.inference.local_inference_adapter import query_ollama
from ciel.orchestrator.purpose_resolver import extract_json_block
from ciel.schemas.evidence import (
    BehaviorEvidence,
    EvidenceBundle,
    ImplementationFact,
    IntentionClaim,
    OperationalEvidence,
    ProjectInfo,
    SourceFile,
)

logger = logging.getLogger(__name__)

CLAIM_KEYWORDS = (
    "must ",
    "should ",
    "provides ",
    "supports ",
    "enforces ",
    "detects ",
    "validates ",
    "prevents ",
    "generates ",
)


def _clean_markdown_text(line: str) -> str:
    return line.strip().strip("#-*`> ").strip()


def _extract_intention_claims(content: str, source_id: str, start_index: int) -> tuple[list[IntentionClaim], int]:
    claims: list[IntentionClaim] = []
    claim_counter = start_index
    seen: set[str] = set()

    for raw_line in content.splitlines():
        line = _clean_markdown_text(raw_line)
        if not line or line in seen:
            continue

        lower = line.lower()
        is_heading = raw_line.startswith("# ") or raw_line.startswith("## ")
        is_claim_sentence = any(keyword in lower for keyword in CLAIM_KEYWORDS) and len(line) <= 220

        if is_heading or is_claim_sentence:
            seen.add(line)
            claims.append(
                IntentionClaim(
                    id=f"c{claim_counter}",
                    source_id=source_id,
                    claim=line,
                    claim_type="capability" if is_heading else "behavioral_expectation",
                )
            )
            claim_counter += 1

    return claims[:25], claim_counter


def _python_facts(content: str, source_id: str, start_index: int) -> tuple[list[ImplementationFact], int]:
    facts: list[ImplementationFact] = []
    fact_counter = start_index

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return facts, fact_counter

    imports = sorted(
        {
            alias.name.split(".")[0]
            for node in tree.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in getattr(node, "names", [])
            if alias.name
        }
    )
    if imports:
        facts.append(
            ImplementationFact(
                id=f"f{fact_counter}",
                source_id=source_id,
                fact=f"Imports dependencies: {', '.join(imports[:10])}",
                fact_type="dependency_usage",
            )
        )
        fact_counter += 1

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = [item.name for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))]
            suffix = f" with methods {', '.join(methods[:8])}" if methods else ""
            facts.append(
                ImplementationFact(
                    id=f"f{fact_counter}",
                    source_id=source_id,
                    fact=f"Defines class {node.name}{suffix}",
                    fact_type="implemented_capability",
                )
            )
            fact_counter += 1
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            decorators = [getattr(dec, "id", "") for dec in node.decorator_list]
            decorated = " CLI command" if "command" in decorators else " function"
            facts.append(
                ImplementationFact(
                    id=f"f{fact_counter}",
                    source_id=source_id,
                    fact=f"Defines{decorated} {node.name}",
                    fact_type="implemented_capability",
                )
            )
            fact_counter += 1

    return facts, fact_counter


def _generic_code_facts(content: str, source_id: str, start_index: int) -> tuple[list[ImplementationFact], int]:
    facts: list[ImplementationFact] = []
    fact_counter = start_index
    patterns = [
        r"\bfunction\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\bdef\s+([A-Za-z_][A-Za-z0-9_]*)",
    ]
    seen: set[str] = set()
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            name = match.group(1)
            if name in seen:
                continue
            seen.add(name)
            facts.append(
                ImplementationFact(
                    id=f"f{fact_counter}",
                    source_id=source_id,
                    fact=f"Defines code symbol {name}",
                    fact_type="implemented_capability",
                )
            )
            fact_counter += 1
    return facts, fact_counter


def _structure_facts(content: str, source: SourceFile, start_index: int) -> tuple[list[ImplementationFact], int]:
    facts: list[ImplementationFact] = []
    fact_counter = start_index
    filename = Path(source.path).name.lower()

    if filename == "pyproject.toml":
        for marker in ("[project]", "[project.scripts]", "[project.optional-dependencies]"):
            if marker in content:
                facts.append(
                    ImplementationFact(
                        id=f"f{fact_counter}",
                        source_id=source.id,
                        fact=f"Configures Python packaging section {marker}",
                        fact_type="packaging_metadata",
                    )
                )
                fact_counter += 1
    elif filename == "package.json":
        try:
            data = json.loads(content)
            scripts = sorted((data.get("scripts") or {}).keys())
            if scripts:
                facts.append(
                    ImplementationFact(
                        id=f"f{fact_counter}",
                        source_id=source.id,
                        fact=f"Defines package scripts: {', '.join(scripts[:10])}",
                        fact_type="packaging_metadata",
                    )
                )
                fact_counter += 1
        except json.JSONDecodeError:
            pass

    return facts, fact_counter


def _static_facts(content: str, source: SourceFile, start_index: int) -> tuple[list[ImplementationFact], int]:
    suffix = Path(source.path).suffix.lower()
    if source.role == "structure":
        return _structure_facts(content, source, start_index)
    if suffix == ".py":
        return _python_facts(content, source.id, start_index)
    return _generic_code_facts(content, source.id, start_index)


def _llm_facts(content: str, source: SourceFile, fact_counter: int) -> tuple[list[ImplementationFact], int]:
    prompt = (
        "Extract 1 to 5 concrete implementation facts from the file below. "
        "Return only JSON: [{\"fact\": \"...\", \"fact_type\": \"implemented_capability\"}].\n\n"
        f"File: {source.path}\n"
        f"Content:\n{content[:8000]}"
    )
    response_text = query_ollama(prompt)
    if response_text.startswith("Error connecting to local inference:"):
        raise ConnectionError(response_text)
    if not response_text.strip():
        raise ValueError("empty response received from local inference")

    data = json.loads(extract_json_block(response_text))
    if isinstance(data, dict):
        data = data.get("facts", [data])
    if not isinstance(data, list):
        raise ValueError("expected a JSON list of facts")

    facts: list[ImplementationFact] = []
    for item in data:
        if isinstance(item, dict) and item.get("fact"):
            facts.append(
                ImplementationFact(
                    id=f"f{fact_counter}",
                    source_id=source.id,
                    fact=str(item["fact"]).strip(),
                    fact_type=str(item.get("fact_type", "implemented_capability")).strip(),
                )
            )
            fact_counter += 1
    if not facts:
        raise ValueError("no valid facts returned")
    return facts, fact_counter


def extract_evidence(repo_path: Path, sources: List[SourceFile]) -> EvidenceBundle:
    claims: list[IntentionClaim] = []
    facts: list[ImplementationFact] = []
    behaviors: list[BehaviorEvidence] = []
    operations: list[OperationalEvidence] = []

    claim_counter = 1
    fact_counter = 1
    llm_disabled = False

    for src in sources:
        abs_path = repo_path / src.path
        if not abs_path.exists():
            continue

        try:
            content = abs_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if src.role == "intention":
            new_claims, claim_counter = _extract_intention_claims(content, src.id, claim_counter)
            claims.extend(new_claims)

        elif src.role in {"reality", "structure"}:
            extracted_via_llm = False
            if src.role == "reality" and not llm_disabled:
                try:
                    new_facts, fact_counter = _llm_facts(content, src, fact_counter)
                    facts.extend(new_facts)
                    extracted_via_llm = True
                except ConnectionError as exc:
                    logger.warning("LLM unavailable for %s: %s", src.path, exc)
                    llm_disabled = True
                except Exception as exc:
                    logger.warning("LLM extraction failed for %s: %s", src.path, exc)

            if not extracted_via_llm:
                new_facts, fact_counter = _static_facts(content, src, fact_counter)
                facts.extend(new_facts)

        elif src.role == "behavior":
            behaviors.append(
                BehaviorEvidence(
                    id=f"b{len(behaviors)+1}",
                    source_id=src.id,
                    evidence="Found test definitions",
                    evidence_type="test_suite",
                )
            )

        elif src.role == "operational_maturity":
            operations.append(
                OperationalEvidence(
                    id=f"o{len(operations)+1}",
                    source_id=src.id,
                    evidence=f"Found operational manifest: {abs_path.name}",
                    evidence_type="manifest",
                )
            )

    exts = [Path(src.path).suffix.lower() for src in sources if src.role == "reality" and Path(src.path).suffix]
    lang_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
    }
    primary_language = lang_map.get(Counter(exts).most_common(1)[0][0], "Unknown") if exts else "Unknown"

    return EvidenceBundle(
        project=ProjectInfo(name=repo_path.name, primary_language=primary_language),
        sources=sources,
        intention_claims=claims,
        implementation_facts=facts,
        behavior_evidence=behaviors,
        operational_evidence=operations,
    )
