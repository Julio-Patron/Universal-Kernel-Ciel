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
