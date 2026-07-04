# Ciel Architecture — Hierarchical RAG & Context Governance

## 1. El Pipeline de Ejecución Determinista

Ciel procesa cada comando con una cadena cerrada para evitar que el LLM alucine:

```txt
CLI Command
  → Purpose Resolver
  → Source Role Assignment
  → Layered Retrieval
  → Evidence Bundle
  → Intention vs Reality Diff
  → Implementation Gap Report
  → Decision Plan
  → Output Summary
```

## 2. La Pirámide de Autoridad (Las 7 Capas de Contexto)

En caso de conflicto de datos o instrucciones contradictorias, las capas superiores vetan absolutamente a las inferiores:

```txt
Capa 0 > Capa 1 > Capa 2 > Capa 3 > Capa 4 > Capa 5 > Capa 6
```

### Capa 0 — Core Directive
Autoridad máxima. Define los principios rígidos del kernel. (ej. Proteger foco, Generar valor comercial, Reducir deuda técnica).

### Capa 1 — Strategic Context
Define los objetivos comerciales o estratégicos vigentes y exclusiones (ej. evitar sobreingeniería).
Responde: *“¿Hacia dónde vamos?”*

### Capa 2 — Project Context
Define el perfil analítico y la identidad del repositorio analizado (nombre del repo, lenguaje principal, estado conocido).
Responde: *“¿Qué sabemos de este proyecto?”*

### Capa 3 — Task Context & Active Memory
La petición actual del usuario fusionada con correcciones explícitas recientes.
Responde: *“¿Qué estamos intentando resolver ahora?”*

### Capa 4 — Evidence RAG
Extracción quirúrgica de datos. Recuperación dirigida de evidencia (README, código fuente, tests). No se recupera información hasta saber qué decisión se intenta tomar.

### Capa 5 — Session Log
Memoria temporal de la sesión para mantener continuidad, sin mandar sobre evidencia verificable.

### Capa 6 — Execution Context
Define permisos operativos locales (ej. can_read_files, can_edit_files).
Responde: *“¿Qué puede hacer Ciel ahora?”*

## 3. Arquitectura del Repositorio V0

Estructura propuesta:

```txt
ciel-kernel/
├── pyproject.toml
├── README.md
├── docs/
│   ├── CIEL_KERNEL_V0.md
│   ├── ARCHITECTURE.md
│   ├── SCHEMAS.md
│   ├── CLI_SPEC.md
│   └── ROADMAP.md
├── core/
│   ├── directive.yaml
│   └── judgment_rules.yaml
├── ciel/
│   ├── __init__.py
│   ├── cli/
│   │   ├── main.py
│   │   └── render.py
│   ├── schemas/
│   │   ├── purpose.py
│   │   ├── evidence.py
│   └── gap_report.py
│   ├── orchestrator/
│   │   ├── purpose_resolver.py
│   │   ├── source_role_assignment.py
│   │   ├── retrieval_planner.py
│   │   └── reasoning_orchestrator.py
│   ├── rag/
│   │   ├── file_scanner.py
│   │   └── evidence_extractor.py
│   └── skills/
│       ├── detect_implementation_gap.py
│       └── audit_repo_maturity.py
└── memory/
    ├── project_profiles/
    └── decisions.log
```
