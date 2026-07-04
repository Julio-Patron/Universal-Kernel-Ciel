Ciel Kernel: Sistema Operativo de Inteligencia y Gobernanza de Contexto
Documento Maestro V0
1. Definición Operativa
Ciel Kernel es una capa de inteligencia y orquestación diseñada para coordinar agentes de software, herramientas, memoria y código con un propósito estricto:

Convertir información dispersa de un proyecto en decisiones técnicas y comerciales ejecutables.

Ciel rompe con el paradigma de los asistentes de desarrollo tradicionales:

No es un chatbot: no busca responder preguntas genéricas en la superficie.
No es solo un RAG estándar: no recupera información de forma masiva basándose únicamente en similitud semántica.
No es solo una CLI: la interfaz de comandos es una capa delgada (Thin CLI); la verdadera inteligencia reside en contratos JSON estructurados y lógica interna gobernada (Fat Logic).
Ciel funciona como un micro-kernel de criterio estratégico. Es un sistema jerárquico que evalúa el estado del software no solo por su validez sintáctica, sino por su madurez técnica, coherencia arquitectónica y viabilidad comercial.

2. Origen: Evolución de universal-ai-kernel
Ciel V0 nace como evolución técnica del repositorio:

JPatronC92/universal-ai-kernel
Este repositorio ya contiene la base conceptual:

Mandatos operativos rígidos para agentes.
Reglas de disciplina.
Habilidades basadas en Procedimientos Operativos Estándar, o SOPs.
Ciclo de ejecución disciplinado.
Prevención de alucinaciones.
Enfoque en trazabilidad mediante una bitácora tipo Tempus DDB.
Ciel no descarta esa base. La madura y la convierte en un sistema ejecutable de análisis, gobernanza y decisión.

El paso evolutivo es este:

universal-ai-kernel
  → kernel de disciplina para agentes

Ciel Kernel
  → kernel de inteligencia, contexto, evidencia, brecha y decisión
3. Problema que Resuelve
Los agentes autónomos actuales sufren de ceguera por exceso de contexto y falta de criterio operativo.

Sus principales fallas son:

Ingesta sin propósito Preguntan:

“¿Qué información encuentro?” en lugar de: “¿Qué decisión tengo que tomar?”

Aplanamiento de autoridad Tratan un README.md, el código fuente, los logs, los tests y los comentarios como si tuvieran el mismo nivel de verdad.

Confusión entre visión y realidad No distinguen entre lo que el proyecto quiere ser y lo que realmente está implementado.

Acción prematura Refactorizan, escriben features o cambian arquitectura antes de entender el producto, el estado real y la prioridad comercial.

Recomendaciones genéricas Dicen “agrega tests”, “mejora docs” o “refactoriza” sin medir qué acción genera más valor ahora.

Ciel resuelve esto imponiendo una cadena de procesamiento estricta:

Propósito → Roles de fuente → Evidencia → Brecha → Decisión → Ejecución controlada
4. Paradigma Central: Hierarchical RAG + Context Governance
Ciel usa un modelo de RAG jerárquico con gobernanza de contexto.

No recupera información al azar. Primero determina el propósito de la tarea y luego decide qué información necesita.

El principio es:

No más contexto. Mejor contexto, en el orden correcto.

5. Pirámide de Autoridad
Ciel opera con capas jerárquicas. Si hay conflicto entre capas, gana la capa superior.

Capa 0 > Capa 1 > Capa 2 > Capa 3 > Capa 4 > Capa 5 > Capa 6
Capa 0 — Core Directive
Autoridad máxima. Define los principios rígidos del kernel.

Ejemplos:

Proteger foco.
Generar valor comercial.
Reducir deuda técnica.
Evitar sobreingeniería.
No modificar código crítico sin plan.
No asumir que el código representa toda la visión del proyecto.
Contrastar siempre intención contra realidad.
Capa 1 — Strategic Context
Define los objetivos estratégicos actuales.

Ejemplos:

current_goal: "Convertir repos técnicos en productos comerciales"
avoid:
  - features sin cliente
  - cripto/on-chain prematuro
  - dashboards antes de producto
  - sobreingeniería
Esta capa responde:

“¿Hacia dónde vamos?”

Capa 2 — Project Context
Define la identidad del proyecto analizado.

Ejemplos:

Nombre del repo.
Lenguaje principal.
Tipo de producto.
Estado conocido.
Riesgos estructurales.
Límites del análisis.
Esta capa responde:

“¿Qué sabemos de este proyecto?”

Capa 3 — Task Context & Active Memory
Contiene la petición puntual del usuario y correcciones recientes.

Ejemplo:

"Analiza este repo, pero no descartes el README: úsalo como intención y compáralo contra el código."
Esta capa responde:

“¿Qué estamos intentando resolver ahora?”

Capa 4 — Evidence RAG
Recuperación quirúrgica y dirigida de evidencia.

Fuentes posibles:

README.
Documentación.
Código fuente.
Tests.
Manifests.
Dockerfiles.
CI/CD.
Benchmarks.
Logs.
Ejemplos.
Regla central:

No se recupera información hasta saber qué decisión se intenta tomar.

Capa 5 — Session Log
Memoria temporal de la sesión.

Sirve para mantener continuidad, pero no debe mandar sobre directrices, estrategia o evidencia verificable.

Capa 6 — Execution Context
Define permisos operativos.

Ejemplo:

can_read_files: true
can_edit_files: false
can_run_tests: true
can_commit: false
can_publish: false
Esta capa responde:

“¿Qué puede hacer Ciel ahora?”

6. Concepto Clave: Intención vs Realidad
Ciel no descarta el README cuando existe código.

El README y la documentación representan la Intención.

El código fuente representa la Realidad.

Los tests y logs representan el Comportamiento.

Docker, CI/CD y release configs representan la Operación.

Dimensión	Fuentes	Significado
Intención	README, docs, roadmap	Lo que el proyecto quiere ser
Realidad	Código, AST, manifests	Lo que el proyecto es hoy
Comportamiento	Tests, logs, ejemplos	Lo que realmente funciona
Operación	Docker, CI/CD, releases	Qué tan listo está para distribuirse
La fricción entre intención y realidad produce el:

Implementation Gap
7. Implementation Gap
El Implementation Gap es la brecha entre lo que el proyecto promete y lo que realmente existe.

Ciel clasifica cada discrepancia en categorías estrictas:

implemented
partially_implemented
roadmap_gap
technical_debt
obsolete_documentation
contradicted_by_code
unsupported_claim
unknown_requires_runtime_test
Categorías
implemented
La intención, la realidad y el comportamiento están alineados.

Acción típica:

Empaquetar, documentar, vender o desplegar.
partially_implemented
Existe código funcional, pero no cubre toda la especificación.

Acción típica:

Validar tracción con la parte funcional antes de completar todo el roadmap.
roadmap_gap
La documentación promete algo que todavía no existe en código.

Acción típica:

Evaluar si realmente conviene construirlo ahora.
technical_debt
Existe implementación, pero con estructura frágil, sin tests, duplicación o riesgos.

Acción típica:

Refactorizar antes de escalar.
obsolete_documentation
El código avanzó más que la documentación.

Acción típica:

Regenerar documentación desde la realidad actual.
contradicted_by_code
El código hace algo opuesto a lo documentado.

Acción típica:

Alerta de riesgo alto. Requiere revisión manual.
unsupported_claim
Una afirmación no puede comprobarse con las fuentes disponibles.

Acción típica:

Solicitar evidencia adicional o marcar como reclamo no validado.
unknown_requires_runtime_test
No se puede determinar con análisis estático.

Acción típica:

Ejecutar pruebas, build o benchmark.
8. Pipeline de Ejecución Determinista V0
Ciel procesa cada comando con una cadena cerrada:

CLI Command
  → Purpose Resolver
  → Source Role Assignment
  → Layered Retrieval
  → Evidence Bundle
  → Intention vs Reality Diff
  → Implementation Gap Report
  → Decision Plan
  → Output Summary
9. Componentes Principales
9.1 Purpose Resolver
Convierte una petición ambigua en una decisión concreta.

Ejemplo:

Usuario:
"Revisa este repo."

Ciel:
"Determinar la brecha entre la intención documentada y la realidad implementada para decidir la siguiente acción de mayor valor."
Output esperado:

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
9.2 Source Role Assignment
Clasifica fuentes antes del RAG.

Tiene dos fases:

Static Assignment
Basado en ruta, nombre y extensión.

{
  "README.md": "intention",
  "docs/": "intention",
  "src/": "reality",
  "tests/": "behavior",
  "Cargo.toml": "structure",
  "Dockerfile": "deployment",
  ".github/workflows/": "operational_maturity"
}
Dynamic Validation
Corrige o complementa el rol según contenido real.

Ejemplo:

README.md puede ser intención, pero si contiene comandos de despliegue también aporta evidencia operativa.
9.3 Layered Retrieval
Recupera únicamente la evidencia necesaria para responder el propósito.

No busca todo.

Busca lo que necesita para responder preguntas como:

¿Qué promete el proyecto?
¿Qué existe realmente?
¿Qué funciona?
¿Qué está listo para distribuirse?
¿Qué falta?
¿Qué conviene hacer primero?
9.4 Evidence Bundle
Contrato estructurado que consolida claims y hechos.

Las skills no leen archivos directamente. Las skills solo leen el EvidenceBundle.

Esto evita improvisación, pérdida de trazabilidad y análisis arbitrario.

Ejemplo:

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
9.5 Intention vs Reality Diff
Compara:

intention_claims
  contra
implementation_facts
  contra
behavior_evidence
  contra
operational_evidence
Produce la matriz de brecha.

9.6 Implementation Gap Report
Salida canónica del análisis.

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
10. Arquitectura del Repositorio V0
Estructura propuesta:

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
│   │   └── gap_report.py
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
11. CLI V0
La CLI debe ser delgada.

La inteligencia no vive en los comandos. La inteligencia vive en los contratos y el orquestador.

Comandos mínimos:

ciel analyze ./repo
Ejecuta el análisis completo.

ciel purpose "Analiza este repo y dime qué hacer primero"
Devuelve el PurposeObject.

ciel sources ./repo
Muestra el Source Role Assignment.

ciel gap ./repo
Ejecuta solo la detección de brecha.

ciel report ./repo --format json
Exporta reporte JSON.

ciel report ./repo --format markdown
Exporta reporte Markdown.

12. Why tempus-mcp is not the V0 Starting Point
tempus-mcp queda excluido como punto de partida de Ciel V0.

Aunque es estratégicamente importante, no es un repositorio simple de un solo producto. Es un repositorio integrado compuesto por proyectos que originalmente fueron individuales, entre ellos:

SES
tempus-engine
tempus-ddb
Estos proyectos internos tienen sus propios:

README.
Dockerfiles.
Benchmarks.
Supuestos arquitectónicos.
Historial conceptual.
Niveles de madurez.
Usar tempus-mcp como objetivo inicial obligaría a Ciel V0 a resolver análisis multiproyecto antes de haber validado el caso más simple:

un repositorio
  → una intención
  → una realidad
  → una brecha de implementación
  → un plan de decisión
Por lo tanto:

universal-ai-kernel es el punto de partida de Ciel V0.
jsonlogic-fast puede usarse como caso técnico limpio temprano.
tempus-mcp se reserva como benchmark avanzado para una fase posterior.
Antes de analizar correctamente tempus-mcp, Ciel necesitará una skill dedicada:
detect_product_boundaries
Esa skill deberá detectar límites internos de producto, separar contextos y generar reportes independientes por unidad funcional.

13. Non-Goals de V0
Para proteger foco, Ciel V0 no hará todavía:

Modificación automática de código.
Refactors autónomos.
Commits automáticos.
Pull Requests automáticos.
Publicación de paquetes.
Despliegues.
Memoria vectorial pesada.
Multiagente distribuido.
Análisis profundo de monorepos o repos multiproducto.
Ejecución de comandos destructivos sin aprobación explícita.
Integración compleja con GitHub Issues o CI/CD.
Ciel V0 se limita a:

leer → clasificar → comparar → diagnosticar → recomendar
14. Definition of Done de V0
Ciel V0 estará terminado cuando pueda autoanalizarse localmente con:

ciel analyze ./universal-ai-kernel
Y devolver consistentemente:

Identidad detectada Qué dice el proyecto que es.

Resumen de intención Claims principales extraídos del README/docs.

Mapeo de realidad Qué componentes existen realmente en archivos.

Comportamiento comprobable Tests, ejemplos o evidencia de ejecución disponibles.

Matriz de brecha Qué claims están implementados, parciales, ausentes o contradichos.

Puntaje de madurez Claridad de intención, completitud, estabilidad, operación y preparación comercial.

Veredicto Estado real del proyecto.

Acción prioritaria Qué debe hacerse primero y por qué.

Salida terminal limpia

Export JSON

Export Markdown

15. Roadmap V0
Fase 0 — Documentación oficial
Crear:

docs/CIEL_KERNEL_V0.md
docs/ARCHITECTURE.md
docs/SCHEMAS.md
docs/CLI_SPEC.md
docs/ROADMAP.md
Objetivo:

Congelar contratos, arquitectura y límites.
Fase 1 — CLI mínima
Implementar:

ciel analyze
ciel purpose
ciel sources
ciel gap
ciel report
Objetivo:

Thin CLI funcional.
Fase 2 — Source Role Assignment
Implementar:

file_scanner.py
source_role_assignment.py
Objetivo:

Clasificar archivos por rol antes de extraer evidencia.
Fase 3 — Evidence Extractor
Implementar:

evidence_extractor.py
Objetivo:

Extraer claims, facts y behavior evidence.
Fase 4 — Implementation Gap Detector
Implementar:

detect_implementation_gap.py
Objetivo:

Comparar intención contra realidad y clasificar brechas.
Fase 5 — Renderers
Implementar:

terminal renderer
json renderer
markdown renderer
Objetivo:

Entregar reportes usables por humanos y agentes.
16. Primera Tarea para el Agente Asíncrono
El primer trabajo del agente no debe ser programar la CLI.

Debe preparar la base oficial del proyecto.

Instrucción:

Trabaja en el repositorio JPatronC92/universal-ai-kernel.

Crea una rama llamada ciel-v0.

Crea la carpeta docs/.

Agrega los siguientes archivos:

docs/CIEL_KERNEL_V0.md
docs/ARCHITECTURE.md
docs/SCHEMAS.md
docs/CLI_SPEC.md
docs/ROADMAP.md

Usa este documento maestro como base para CIEL_KERNEL_V0.md.

Extrae:
- arquitectura hacia ARCHITECTURE.md
- contratos JSON hacia SCHEMAS.md
- comandos hacia CLI_SPEC.md
- fases hacia ROADMAP.md

No borres AGENTS.md.
No borres las skills actuales.
No uses tempus-mcp como base de V0.
No implementes ejecución autónoma todavía.
No agregues análisis multiproducto todavía.
No edites código funcional todavía.

El objetivo de esta fase es congelar la documentación oficial y los contratos de desarrollo de Ciel Kernel V0.
17. Decisión Oficial
Ciel V0 nace como evolución de:

JPatronC92/universal-ai-kernel
universal-ai-kernel aporta el alma:

Disciplina.
SOPs.
Mandato operativo.
Ciclo de ejecución.
Prevención de alucinaciones.
Trazabilidad conceptual.
Ciel Kernel V0 aporta el cerebro:

Purpose Resolver.
Source Role Assignment.
Layered Retrieval.
Evidence Bundle.
Intention vs Reality Diff.
Implementation Gap Report.
Decision Plan.
La tesis final es:

Ciel Kernel es un sistema operativo de inteligencia para agentes de software que convierte contexto disperso en decisiones técnicas y comerciales ejecutables mediante gobernanza jerárquica, evidencia clasificada y detección de brecha entre intención y realidad.