# Ciel Kernel JSON Contracts and Schemas

## 1. Purpose Resolver Schema
Convierte una petición ambigua en una decisión concreta.

```json
{
  "schema_version": "ciel.purpose.v1.0",
  "task": {
    "type": "repo_analysis",
    "decision_needed": "what_to_do_first",
    "output_mode": "diagnostic_and_plan"
  },
  "purpose": {
    "primary_question": "What is the gap between project intention and current implementation reality?",
    "success_criteria": [
      "identify project intention",
      "identify current implementation",
      "detect implementation gaps",
      "recommend next action"
    ]
  }
}
```

## 2. Source Role Assignment Schema
Clasifica fuentes antes del RAG basado en ruta, nombre y extensión.

```json
{
  "README.md": "intention",
  "docs/": "intention",
  "src/": "reality",
  "tests/": "behavior",
  "Cargo.toml": "structure",
  "Dockerfile": "deployment",
  ".github/workflows/": "operational_maturity"
}
```

## 3. Evidence Bundle Schema
Contrato estructurado que consolida claims y hechos. Las skills solo leen el `EvidenceBundle`.

```json
{
  "schema_version": "ciel.evidence.v1.0",
  "project": {
    "name": "example-project",
    "primary_language": "Rust"
  },
  "sources": [
    {
      "id": "s1",
      "path": "README.md",
      "role": "intention",
      "confidence": 0.95
    },
    {
      "id": "s2",
      "path": "src/lib.rs",
      "role": "reality",
      "confidence": 0.98
    }
  ],
  "intention_claims": [
    {
      "id": "c1",
      "source_id": "s1",
      "claim": "Deterministic logic evaluation engine built for speed",
      "claim_type": "capability"
    }
  ],
  "implementation_facts": [
    {
      "id": "f1",
      "source_id": "s2",
      "fact": "Core evaluation logic implemented in Rust",
      "fact_type": "implemented_capability"
    }
  ],
  "behavior_evidence": []
}
```

## 4. Implementation Gap Report Schema
Salida canónica del análisis.

```json
{
  "schema_version": "ciel.gap_report.v1.0",
  "project": {
    "name": "example-project"
  },
  "gap_matrix": [
    {
      "claim_id": "c1",
      "claim": "Deterministic logic evaluation engine built for speed",
      "status": "implemented",
      "classification": "production_ready",
      "evidence": ["f1"],
      "severity": "low",
      "interpretation": "The documented core claim is backed by implementation.",
      "recommended_action": "Package this capability as the commercial core."
    }
  ],
  "maturity_score": {
    "intention_clarity": 0.9,
    "implementation_completeness": 0.75,
    "behavior_confidence": 0.8,
    "operational_readiness": 0.55,
    "commercial_readiness": 0.65
  },
  "verdict": {
    "stage": "technical_core_ready",
    "summary": "The core engine appears valuable, but distribution and packaging remain incomplete.",
    "main_bottleneck": "commercial_distribution_layer"
  },
  "next_actions": [
    {
      "priority": 1,
      "type": "packaging",
      "description": "Define stable public API and package the working core as the first sellable unit.",
      "reason": "The core claim is implemented; commercial value depends on distribution."
    }
  ]
}
```
