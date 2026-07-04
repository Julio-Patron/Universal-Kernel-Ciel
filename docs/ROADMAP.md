# Ciel Kernel V0 Roadmap

## Fase 0 — Documentación oficial

Crear la estructura inicial:
```txt
docs/CIEL_KERNEL_V0.md
docs/ARCHITECTURE.md
docs/SCHEMAS.md
docs/CLI_SPEC.md
docs/ROADMAP.md
```
Objetivo: Congelar contratos, arquitectura y límites.

---

## Fase 1 — CLI mínima

Implementar los comandos base:
```txt
ciel analyze
ciel purpose
ciel sources
ciel gap
ciel report
```
Objetivo: Thin CLI funcional.

---

## Fase 2 — Source Role Assignment

Implementar lógica de asignación:
```txt
file_scanner.py
source_role_assignment.py
```
Objetivo: Clasificar archivos por rol antes de extraer evidencia.

---

## Fase 3 — Evidence Extractor

Implementar extracción de evidencia:
```txt
evidence_extractor.py
```
Objetivo: Extraer claims, facts y behavior evidence.

---

## Fase 4 — Implementation Gap Detector

Implementar detector de brechas:
```txt
detect_implementation_gap.py
```
Objetivo: Comparar intención contra realidad y clasificar brechas.

---

## Fase 5 — Renderers

Implementar formatos de salida:
```txt
terminal renderer
json renderer
markdown renderer
```
Objetivo: Entregar reportes usables por humanos y agentes.

¡Entendido, Julio! Con las Fases 0 a 5 ya implementadas, Ciel V0 ha alcanzado su *Definition of Done* como un motor de diagnóstico estático. El sistema ya sabe leer, asignar roles, clasificar evidencia, detectar la brecha de implementación y recomendar.

El siguiente bloque del roadmap marca la transición de **Ciel V0 (Repo Intelligence)** hacia **Ciel V1 (Execution & Context Governance)**. Basándonos en las reglas de arquitectura establecidas (y la necesidad de procesar repositorios complejos como `tempus-mcp` o laboratorios de aislamiento como `Decision-Database`), aquí tienes la continuación oficial del documento `ROADMAP.md`.

---

## Fase 6 — Multi-Product & Boundary Detection

Implementar la separación de contextos para repositorios no monolíticos:

```txt
detect_product_boundaries.py
context_separator.py

```

Objetivo: Identificar límites internos de producto dentro de un mismo repositorio (ej. separar un motor de evaluación en Rust de sus bindings o SDKs). Condición estricta para poder auditar proyectos compuestos como `tempus-mcp` sin mezclar intenciones ni realidades.

---

## Fase 7 — Capa de Ejecución Controlada (The Executor)

Implementar el puente entre la recomendación y la acción física:

```txt
shell_executor.py
filesystem_manager.py
approval_gate.py

```

Objetivo: Permitir que Ciel ejecute acciones técnicas (crear archivos, mover directorios, compilar empaquetados) utilizando herramientas del sistema. Toda acción destructiva o de escritura requiere pasar por el `approval_gate` (aprobación humana explícita en la terminal).

---

## Fase 8 — Integración de Bitácora (Memory & Ledger)

Implementar la persistencia del razonamiento:

```txt
memory_writer.py
decision_ledger_adapter.py
decisions.log

```

Objetivo: Guardar el registro inmutable de las brechas detectadas y las acciones tomadas. Esta fase sienta las bases técnicas para conectar Ciel Kernel con infraestructuras de memoria y auditoría externa (alineado con la filosofía TempusDDB).

---

## Fase 9 — Local-First & Air-Gapped Backend

Implementar adaptadores para ejecución sin dependencias de nube:

```txt
local_inference_adapter.py
model_router.py

```

Objetivo: Asegurar que el *Reasoning Orchestrator* pueda conectarse a modelos locales (vía Ollama o binarios compilados), garantizando privacidad total y operabilidad en entornos de hardware restringido o terminales nativas.

---

## Fase 10 — Resolución Autónoma de Deuda Técnica (V1 Release)

Implementar el ciclo continuo de reparación:

```txt
technical_debt_resolver.py
auto_refactor_planner.py

```

Objetivo: Alcanzar la madurez de V1. Ciel no solo diagnostica la brecha, sino que genera un plan de refactorización paso a paso, pide permiso mediante el `approval_gate` y ejecuta los comandos necesarios para limpiar el código, aislar módulos y reducir la deuda técnica detectada en la Fase 4.

---

## Etapa de Inteligencia (Ciel V2: The Cognitive Engine)

Esta etapa marca el "relleno de los andamiajes" (scaffolds), reemplazando las reglas deterministas ingenuas (hardcoded) por razonamiento semántico impulsado por LLMs (Ollama/Cloud).

---

## Fase 11 — LLM-Powered Purpose Resolution

Rellenar el andamiaje de entendimiento de intención:

```txt
purpose_resolver.py
```

Objetivo: Reemplazar el retorno estático por un prompt al LLM que analice los documentos `docs/` o el `README.md` y extraiga dinámicamente el propósito, público objetivo y problemas que resuelve el repositorio.

---

## Fase 12 — Intelligent Evidence Extraction

Rellenar el andamiaje de abstracción de código:

```txt
evidence_extractor.py
```

Objetivo: Utilizar el LLM para parsear los archivos de la "Realidad" (código fuente) y extraer *Implementation Facts* semánticos, en lugar de depender de regex o conteo ingenuo de extensiones/clases.

---

## Fase 13 — Semantic Implementation Gap Detection

Rellenar el andamiaje de auditoría y diagnóstico:

```txt
detect_implementation_gap.py
audit_repo_maturity.py
```

Objetivo: Reemplazar el emparejamiento de palabras (word matching) por una evaluación semántica profunda, donde el LLM compare la matriz de *Intention Claims* contra los *Implementation Facts* y emita un veredicto maduro y real sobre la brecha.

---

## Fase 14 — Orchestrated Cognitive Pipeline (V2 Release)

Ensamblar el ciclo completo con IA:

```txt
reasoning_orchestrator.py
```

Objetivo: Conectar las fases 11 a 13 en una tubería asíncrona y orquestada. El comando `ciel analyze` debe correr un ciclo cognitivo completo utilizando `local_inference_adapter.py`, logrando el hito de Ciel V2 (Inteligencia Operativa).