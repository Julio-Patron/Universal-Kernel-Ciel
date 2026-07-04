Sí. Tomando los hallazgos de la auditoría, yo ordenaría el roadmap así: **primero cerrar operación/distribución**, luego **BYOK**, luego **memoria/ledger**, después **monorepo boundary detection**, y hasta el final **auto-refactor planner**. El planner depende de que Ciel ya entienda contexto, historial y boundaries; si lo haces antes, saldrá superficial. La auditoría marca como gaps principales: BYOK/cloud fallback, `decisions.log`, multi-product boundary detection, auto-refactor planner, PyPI, tests incompletos, CI duplicado, coverage y tooling. 

# Roadmap hacia v1.0.0

## Fase 0 — Release ops inmediato: `v0.3.1`

**Objetivo:** convertir el estado actual en paquete instalable y mantener CI confiable.

### Gaps atacados

* Publicación en PyPI.
* Dos workflows CI potencialmente duplicados.
* Falta badge CI / versión.
* Falta coverage.
* `test_evidence_extractor.py` casi vacío.

### Cambios

Archivos:

```text
.github/workflows/ci.yml
.github/workflows/publish.yml
pyproject.toml
README.md
tests/conftest.py
tests/test_ciel/test_evidence_extractor.py
```

Tareas:

```text
1. Consolidar workflows CI.
2. Añadir pytest-cov.
3. Exigir coverage mínimo inicial de 70%, luego subir a 80%.
4. Completar test_evidence_extractor.py.
5. Añadir fixtures compartidas en conftest.py.
6. Crear workflow publish-to-pypi activado por tags v*.
7. Añadir badges al README.
```

Definition of Done:

```text
- CI pasa en Python 3.10, 3.11 y 3.12.
- python -m build pasa.
- twine check dist/* pasa.
- pytest-cov reporta cobertura.
- Release tag genera paquete publicable.
```

Resultado:

```text
pip install ciel-kernel
```

---

## Fase 1 — BYOK / Cloud inference adapter: `v0.4.0`

**Objetivo:** romper la dependencia fuerte de Ollama sin romper la filosofía local-first.

### Principio central

El score canónico de Ciel debe seguir siendo determinista. BYOK mejora análisis semántico, explanations y claim understanding, pero no debe convertir el core en cloud-dependent.

### Gaps atacados

* Dependencia fuerte de Ollama.
* Semantic gap detection parcialmente implementada.
* Necesidad futura de agentes que traigan sus propias llaves.

### Arquitectura

Nuevos archivos:

```text
ciel/inference/cloud_inference_adapter.py
ciel/inference/model_router.py
ciel/inference/provenance.py
tests/test_ciel/test_cloud_inference_adapter.py
tests/test_ciel/test_model_router.py
```

Actualizar:

```text
ciel/config.py
ciel/rag/evidence_extractor.py
ciel/orchestrator/purpose_resolver.py
.env.example
README.md
docs/ARCHITECTURE.md
```

Variables:

```bash
CIEL_LLM_PROVIDER=auto
CIEL_DISABLE_LLM=0

CIEL_OLLAMA_URL=http://localhost:11434
CIEL_OLLAMA_MODEL=llama3

CIEL_OPENAI_API_KEY=
CIEL_OPENAI_MODEL=gpt-4.1-mini

CIEL_ANTHROPIC_API_KEY=
CIEL_ANTHROPIC_MODEL=claude-3-5-haiku-latest

CIEL_LLM_TIMEOUT=30
```

Orden de resolución recomendado:

```text
1. deterministic
2. local-ai / Ollama
3. cloud-ai / BYOK
4. auto = deterministic base + best available semantic layer
```

CLI:

```bash
ciel analyze . --mode deterministic
ciel analyze . --mode local-ai
ciel analyze . --mode cloud-ai
ciel analyze . --mode auto
```

Output debe incluir provenance:

```json
{
  "score_type": "deterministic",
  "llm_assisted": true,
  "provider": "openai",
  "model": "gpt-4.1-mini",
  "mode": "byok",
  "fallback_used": false
}
```

Definition of Done:

```text
- Ciel funciona sin API keys.
- Ciel funciona sin Ollama.
- Ciel usa OpenAI/Anthropic solo si el usuario provee key.
- Nunca guarda API keys en logs, reports ni decisions.log.
- El reporte distingue deterministic score vs semantic review.
- Tests mockean proveedores cloud sin llamadas reales.
```

---

## Fase 2 — Memory & Decision Ledger: `v0.5.0`

**Objetivo:** que Ciel tenga memoria persistente entre sesiones y pueda registrar decisiones auditables.

### Gaps atacados

* `memory/` presente pero no operativo.
* `decisions.log` sin vida real.
* Necesidad de operaciones de agentes persistentes.
* Base para attestations y trust gate.

### Arquitectura

Nuevos archivos:

```text
ciel/memory/decision_ledger.py
ciel/memory/session_store.py
ciel/memory/project_profile_store.py
ciel/memory/hash_chain.py
tests/test_ciel/test_decision_ledger.py
tests/test_ciel/test_memory_persistence.py
```

Estructura local:

```text
.ciel/
├── decisions.log
├── sessions/
│   └── <session_id>.json
├── project_profile.json
└── attestations/
    └── <commit_sha>.json
```

Cada entrada del ledger:

```json
{
  "id": "decision_...",
  "timestamp": "2026-07-04T...",
  "repo": "JPatronC92/universal-ai-kernel",
  "commit_sha": "...",
  "event_type": "maturity_score_issued",
  "input_hash": "...",
  "output_hash": "...",
  "previous_hash": "...",
  "entry_hash": "...",
  "ciel_version": "0.5.0"
}
```

CLI:

```bash
ciel memory init
ciel memory status
ciel memory history
ciel memory verify
ciel attest .
```

Definition of Done:

```text
- Cada análisis puede escribirse al ledger.
- El ledger es append-only.
- Hay hash chain verificable.
- Se puede detectar corrupción manual del log.
- El usuario puede desactivar memoria con CIEL_DISABLE_MEMORY=1.
- No se guardan secretos.
```

---

## Fase 3 — Multi-product Boundary Detection: `v0.6.0`

**Objetivo:** que Ciel entienda monorepos y no mezcle frontend, backend, SDKs, infra y docs como si fueran un solo producto.

### Gaps atacados

* `detect_product_boundaries.py` scaffold.
* Fase 6 incompleta.
* Necesidad de navegar monorepos gigantes.

### Arquitectura

Actualizar:

```text
ciel/skills/detect_product_boundaries.py
ciel/rag/file_scanner.py
ciel/orchestrator/source_role_assignment.py
ciel/schemas/product_boundary.py
```

Nuevos tests:

```text
tests/fixtures/monorepo_basic/
tests/fixtures/monorepo_fullstack/
tests/fixtures/monorepo_sdk_api_docs/
tests/test_ciel/test_product_boundaries.py
```

Señales para detectar boundaries:

```text
package.json
pyproject.toml
Cargo.toml
go.mod
Dockerfile
docker-compose.yml
apps/*
packages/*
services/*
infra/*
sdk/*
docs/*
```

Output esperado:

```json
{
  "products": [
    {
      "id": "frontend",
      "path": "apps/web",
      "language": "typescript",
      "framework": "nextjs",
      "role": "user_interface"
    },
    {
      "id": "api",
      "path": "services/api",
      "language": "python",
      "framework": "fastapi",
      "role": "backend_service"
    }
  ]
}
```

CLI:

```bash
ciel boundaries .
ciel analyze . --scope frontend
ciel analyze . --scope backend
ciel analyze . --scope all
```

Definition of Done:

```text
- Ciel detecta al menos 4 tipos de boundary: frontend, backend, package/sdk, infra.
- El maturity score puede calcularse por producto.
- El gap report no mezcla claims de frontend con implementación backend.
- Funciona offline.
```

---

## Fase 4 — Policy Packs / Rulesets versionados: `v0.7.0`

**Objetivo:** que Ciel pueda evaluar un repo contra estándares explícitos y versionados.

### Por qué va antes del auto-refactor planner

El planner necesita saber contra qué estándar refactorizar. Sin rulesets, solo generaría consejos genéricos.

### Nuevos directorios

```text
rulesets/
├── release-readiness.yaml
├── agent-safe-repo.yaml
├── python-package.yaml
├── mcp-server.yaml
└── monorepo.yaml
```

CLI:

```bash
ciel analyze . --ruleset release-readiness
ciel analyze . --ruleset agent-safe-repo
```

Cada ruleset:

```yaml
id: agent-safe-repo
version: 0.1.0
required:
  - tests_present
  - no_shell_execution_by_default
  - env_documented
  - ci_present
  - build_validated
thresholds:
  maturity_score_min: 0.80
```

Definition of Done:

```text
- Cada reporte incluye ruleset_id y ruleset_hash.
- El maturity score declara contra qué policy fue evaluado.
- Se puede reproducir el mismo score con el mismo commit + ruleset.
```

---

## Fase 5 — Auto-refactor Planner: `v0.8.0`

**Objetivo:** que Ciel no solo diagnostique gaps, sino que emita planes concretos, ordenados y accionables.

### Gaps atacados

* `auto_refactor_planner.py` scaffold.
* `technical_debt_resolver.py` scaffold.
* Fase 10 incompleta.

### Importante

No debe modificar archivos todavía. Primero debe planear.

### Arquitectura

Actualizar:

```text
ciel/skills/auto_refactor_planner.py
ciel/skills/technical_debt_resolver.py
ciel/schemas/refactor_plan.py
```

Output:

```json
{
  "plan_id": "refactor_...",
  "target_gap_id": "gap_...",
  "risk": "medium",
  "steps": [
    {
      "order": 1,
      "action": "create_file",
      "path": "ciel/memory/decision_ledger.py",
      "reason": "Memory ledger is documented but not implemented."
    },
    {
      "order": 2,
      "action": "add_tests",
      "path": "tests/test_ciel/test_decision_ledger.py",
      "reason": "Ledger needs corruption and append-only tests."
    }
  ]
}
```

CLI:

```bash
ciel plan-refactor .
ciel plan-refactor . --gap memory-ledger
ciel plan-refactor . --scope backend
```

Definition of Done:

```text
- Planner genera pasos concretos, no consejos vagos.
- Cada paso referencia evidence_id o gap_id.
- Plan incluye riesgo, orden, archivos afectados y tests sugeridos.
- No ejecuta cambios automáticamente.
```

---

## Fase 6 — Safe Patch Generation: `v0.9.0`

**Objetivo:** pasar de plan a patch sugerido, todavía bajo control humano.

### Arquitectura

Nuevos módulos:

```text
ciel/patches/patch_planner.py
ciel/patches/diff_generator.py
ciel/patches/safety_review.py
```

CLI:

```bash
ciel propose-patch . --gap memory-ledger
```

Reglas:

```text
- Nunca escribir directo por defecto.
- Emitir diff.
- Requerir confirmación humana.
- Bloquear cambios destructivos.
- Ejecutar tests solo si CIEL_ENABLE_EXEC=1.
```

Definition of Done:

```text
- Ciel genera patches legibles.
- Patches incluyen test plan.
- No hay auto-merge.
- Executor sigue opt-in.
```

---

## Fase 7 — Agent Trust Gate / Attestations: `v1.0.0-rc1`

**Objetivo:** convertir Ciel en una capa de confianza para agentes.

### Depende de

```text
- BYOK/provenance
- memory ledger
- ruleset hash
- deterministic score
- PyPI release
- product boundaries
```

CLI:

```bash
ciel attest . --ruleset agent-safe-repo
ciel verify-attestation attestation.json
```

Attestation:

```json
{
  "repo": "...",
  "commit_sha": "...",
  "ciel_version": "1.0.0-rc1",
  "ruleset_id": "agent-safe-repo",
  "ruleset_hash": "...",
  "score_type": "deterministic",
  "maturity_score": 0.91,
  "verdict": "agent_interaction_allowed",
  "ledger_hash": "...",
  "signature": "..."
}
```

Definition of Done:

```text
- Un agente puede verificar si debe tocar un repo.
- El resultado es reproducible.
- Hay firma o hash verificable.
- Hay salida JSON estable.
```

---

# Orden correcto de ejecución

No atacaría los gaps en el orden en que aparecen. Los atacaría así:

```text
1. v0.3.1 — PyPI, CI, coverage, tests vacíos
2. v0.4.0 — BYOK / cloud inference optional
3. v0.5.0 — Memory & Decision Ledger
4. v0.6.0 — Multi-product Boundary Detection
5. v0.7.0 — Rulesets / Policy Packs
6. v0.8.0 — Auto-refactor Planner
7. v0.9.0 — Safe Patch Generation
8. v1.0.0 — Agent Trust Gate + Signed Attestations
```

# Dependencias críticas

```text
BYOK no depende del ledger.
Ledger no depende de BYOK.
Boundary detection debe existir antes del planner serio.
Rulesets deben existir antes de attestations v1.
Auto-refactor planner depende de gaps + boundaries + rulesets.
Trust Gate depende de ledger + deterministic score + attestation.
```

# Qué haría primero

Empezaría con **v0.3.1** y luego **v0.4.0 BYOK**.

Razón: PyPI + CI + coverage te dan distribución y confianza. BYOK te quita el mayor bloqueo técnico sin ensuciar la arquitectura. Después ya vale la pena meter memoria persistente.

# Roadmap resumido

| Versión  | Objetivo               | Impacto                          |
| -------- | ---------------------- | -------------------------------- |
| `v0.3.1` | CI/PyPI/coverage/tests | Producto instalable              |
| `v0.4.0` | BYOK cloud adapter     | Rompe dependencia de Ollama      |
| `v0.5.0` | Memory ledger          | Persistencia y auditoría         |
| `v0.6.0` | Monorepo boundaries    | Contexto real por producto       |
| `v0.7.0` | Policy packs           | Evaluación contra estándares     |
| `v0.8.0` | Auto-refactor planner  | Planes accionables               |
| `v0.9.0` | Safe patch generation  | Patches humanos revisables       |
| `v1.0.0` | Trust Gate             | Certificación usable por agentes |

Mi recomendación estratégica: **no vendas Ciel como “analizador de repos”**. Con este roadmap, el posicionamiento correcto es:

```text
Ciel Kernel is a deterministic trust gate for autonomous software agents.
```
