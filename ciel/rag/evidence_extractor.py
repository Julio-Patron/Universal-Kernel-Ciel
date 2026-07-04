from typing import List
from pathlib import Path
import json
import logging
import re
from collections import Counter
from ciel.schemas.evidence import (
    SourceFile, 
    EvidenceBundle, 
    ProjectInfo,
    IntentionClaim,
    ImplementationFact,
    BehaviorEvidence,
    OperationalEvidence
)
from ciel.inference.local_inference_adapter import query_ollama
from ciel.orchestrator.purpose_resolver import extract_json_block

logger = logging.getLogger(__name__)


def extract_evidence(repo_path: Path, sources: List[SourceFile]) -> EvidenceBundle:
    """Extracts evidence from sources into a bundle."""
    claims = []
    facts = []
    behaviors = []
    operations = []
    
    claim_counter = 1
    fact_counter = 1
    llm_disabled = False
    
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
            extracted_via_llm = False
            if not llm_disabled:
                try:
                    # Truncate content to the first 8000 characters to prevent timeouts/context overflow
                    truncated_content = content[:8000]
                    if len(content) > 8000:
                        truncated_content += "\n\n... [Content Truncated due to size limits] ..."
                    
                    llm_prompt = f"""You are the Ciel Kernel Evidence Extractor.
Analyze the source code of the file '{src.path}' and extract key semantic implementation facts.

An implementation fact represents a concrete feature, logic component, architecture decision, helper capability, or library integration that is implemented in this file. Ignore trivial helper details, focus on key capabilities.

Your output must be a single, valid JSON array of objects conforming to the following schema:
[
  {{
    "fact": "A concise, clear sentence describing what is implemented (e.g. 'Provides a local inference adapter to query Ollama')",
    "fact_type": "implemented_capability"
  }}
]

Rules:
1. Rely only on the provided source code content. Do not hallucinate capabilities that do not exist.
2. The "fact" field must be a short, clear sentence.
3. Keep the number of facts between 1 and 5.
4. If there are no clear capabilities, return an empty array: []
5. Your output must be a single, valid JSON block wrapped in ```json ... ``` code tags. Do not include any other text before or after.

Source code of '{src.path}':
```
{truncated_content}
```
"""
                    response_text = query_ollama(llm_prompt, model="llama3")
                    
                    if response_text.startswith("Error connecting to local inference:"):
                        logger.warning(
                            f"Ollama connection error for {src.path}: {response_text}. "
                            "Disabling LLM and falling back to static parser."
                        )
                        llm_disabled = True
                        raise ConnectionError(f"Ollama connection error: {response_text}")
                        
                    if not response_text.strip():
                        raise ValueError("Empty response received from local inference.")
                        
                    extracted_json = extract_json_block(response_text)
                    data = json.loads(extracted_json)
                    
                    # Handle if LLM returned a single object instead of a list
                    if isinstance(data, dict):
                        if "facts" in data and isinstance(data["facts"], list):
                            data = data["facts"]
                        else:
                            data = [data]
                            
                    if isinstance(data, list) and len(data) > 0:
                        temp_facts = []
                        temp_counter = fact_counter
                        for item in data:
                            if isinstance(item, dict) and "fact" in item:
                                temp_facts.append(ImplementationFact(
                                    id=f"f{temp_counter}",
                                    source_id=src.id,
                                    fact=str(item["fact"]).strip(),
                                    fact_type=str(item.get("fact_type", "implemented_capability")).strip()
                                ))
                                temp_counter += 1
                        
                        if temp_facts:
                            facts.extend(temp_facts)
                            fact_counter = temp_counter
                            extracted_via_llm = True
                            logger.info(f"Successfully extracted {len(temp_facts)} facts via LLM for {src.path}")
                        else:
                            raise ValueError("No valid facts could be parsed from the JSON list.")
                    else:
                        raise ValueError("Parsed JSON is not a non-empty list.")
                        
                except Exception as e:
                    logger.warning(
                        f"LLM extraction failed for '{src.path}': {e}. "
                        "Falling back to static AST/regex parsing."
                    )
                    
            if not extracted_via_llm:
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
            
        elif src.role == "operational_maturity":
            operations.append(OperationalEvidence(
                id=f"o{len(operations)+1}",
                source_id=src.id,
                evidence=f"Found operational manifest: {abs_path.name}",
                evidence_type="manifest"
            ))

    # Detect primary language based on 'reality' extensions
    exts = [Path(src.path).suffix.lower() for src in sources if src.role == "reality" and Path(src.path).suffix]
    
    lang_map = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", 
        ".go": "Go", ".rs": "Rust", ".java": "Java", 
        ".cpp": "C++", ".c": "C"
    }
    
    if exts:
        most_common_ext = Counter(exts).most_common(1)[0][0]
        primary_language = lang_map.get(most_common_ext, "Unknown")
    else:
        primary_language = "Unknown"

    project_info = ProjectInfo(
        name=repo_path.name,
        primary_language=primary_language
    )
    
    return EvidenceBundle(
        project=project_info,
        sources=sources,
        intention_claims=claims,
        implementation_facts=facts,
        behavior_evidence=behaviors,
        operational_evidence=operations
    )
