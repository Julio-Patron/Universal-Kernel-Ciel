# Ciel Kernel: Sistema Operativo de Inteligencia y Gobernanza de Contexto

## Documento Maestro V0

---

## 1. Definición Operativa

**Ciel Kernel** es una capa de inteligencia y orquestación diseñada para coordinar agentes de software, herramientas, memoria y código con un propósito estricto:

> **Convertir información dispersa de un proyecto en decisiones técnicas y comerciales ejecutables.**

Ciel rompe con el paradigma de los asistentes de desarrollo tradicionales:

* **No es un chatbot:** no busca responder preguntas genéricas en la superficie.
* **No es solo un RAG estándar:** no recupera información de forma masiva basándose únicamente en similitud semántica.
* **No es solo una CLI:** la interfaz de comandos es una capa delgada (*Thin CLI*); la verdadera inteligencia reside en contratos JSON estructurados y lógica interna gobernada (*Fat Logic*).

Ciel funciona como un **micro-kernel de criterio estratégico**. Es un sistema jerárquico que evalúa el estado del software no solo por su validez sintáctica, sino por su madurez técnica, coherencia arquitectónica y viabilidad comercial.

---

## 2. Origen: Evolución de `universal-ai-kernel`

Ciel V0 nace como evolución técnica del repositorio:

```txt
JPatronC92/universal-ai-kernel
```

Este repositorio ya contiene la base conceptual:

* Mandatos operativos rígidos para agentes.
* Reglas de disciplina.
* Habilidades basadas en Procedimientos Operativos Estándar, o SOPs.
* Ciclo de ejecución disciplinado.
* Prevención de alucinaciones.
* Enfoque en trazabilidad mediante una bitácora tipo Tempus DDB.

Ciel no descarta esa base. La madura y la convierte en un **sistema ejecutable de análisis, gobernanza y decisión**.

El paso evolutivo es este:

```txt
universal-ai-kernel
  → kernel de disciplina para agentes

Ciel Kernel
  → kernel de inteligencia, contexto, evidencia, brecha y decisión
```

---

## 3. Problema que Resuelve

Los agentes autónomos actuales sufren de **ceguera por exceso de contexto** y falta de criterio operativo.

Sus principales fallas son:

1. **Ingesta sin propósito**
   Preguntan:

   > “¿Qué información encuentro?”
   > en lugar de:
   > “¿Qué decisión tengo que tomar?”

2. **Aplanamiento de autoridad**
   Tratan un `README.md`, el código fuente, los logs, los tests y los comentarios como si tuvieran el mismo nivel de verdad.

3. **Confusión entre visión y realidad**
   No distinguen entre lo que el proyecto quiere ser y lo que realmente está implementado.

4. **Acción prematura**
   Refactorizan, escriben features o cambian arquitectura antes de entender el producto, el estado real y la prioridad comercial.

5. **Recomendaciones genéricas**
   Dicen “agrega tests”, “mejora docs” o “refactoriza” sin medir qué acción genera más valor ahora.

Ciel resuelve esto imponiendo una cadena de procesamiento estricta:

```txt
Propósito → Roles de fuente → Evidencia → Brecha → Decisión → Ejecución controlada
```

---

## 6. Concepto Clave: Intención vs Realidad

Ciel no descarta el README cuando existe código.

El README y la documentación representan la **Intención**.

El código fuente representa la **Realidad**.

Los tests y logs representan el **Comportamiento**.

Docker, CI/CD y release configs representan la **Operación**.

| Dimensión      | Fuentes                 | Significado                          |
| -------------- | ----------------------- | ------------------------------------ |
| Intención      | README, docs, roadmap   | Lo que el proyecto quiere ser        |
| Realidad       | Código, AST, manifests  | Lo que el proyecto es hoy            |
| Comportamiento | Tests, logs, ejemplos   | Lo que realmente funciona            |
| Operación      | Docker, CI/CD, releases | Qué tan listo está para distribuirse |

La fricción entre intención y realidad produce el:

## Implementation Gap

---

## 7. Implementation Gap

El **Implementation Gap** es la brecha entre lo que el proyecto promete y lo que realmente existe.

Ciel clasifica cada discrepancia en categorías estrictas:

```txt
implemented
partially_implemented
roadmap_gap
technical_debt
obsolete_documentation
contradicted_by_code
unsupported_claim
unknown_requires_runtime_test
```

### Categorías

#### `implemented`

La intención, la realidad y el comportamiento están alineados.

Acción típica:

```txt
Empaquetar, documentar, vender o desplegar.
```

---

#### `partially_implemented`

Existe código funcional, pero no cubre toda la especificación.

Acción típica:

```txt
Validar tracción con la parte funcional antes de completar todo el roadmap.
```

---

#### `roadmap_gap`

La documentación promete algo que todavía no existe en código.

Acción típica:

```txt
Evaluar si realmente conviene construirlo ahora.
```

---

#### `technical_debt`

Existe implementación, pero con estructura frágil, sin tests, duplicación o riesgos.

Acción típica:

```txt
Refactorizar antes de escalar.
```

---

#### `obsolete_documentation`

El código avanzó más que la documentación.

Acción típica:

```txt
Regenerar documentación desde la realidad actual.
```

---

#### `contradicted_by_code`

El código hace algo opuesto a lo documentado.

Acción típica:

```txt
Alerta de riesgo alto. Requiere revisión manual.
```

---

#### `unsupported_claim`

Una afirmación no puede comprobarse con las fuentes disponibles.

Acción típica:

```txt
Solicitar evidencia adicional o marcar como reclamo no validado.
```

---

#### `unknown_requires_runtime_test`

No se puede determinar con análisis estático.

Acción típica:

```txt
Ejecutar pruebas, build o benchmark.
```

---

## 12. Why `tempus-mcp` is not the V0 Starting Point

`tempus-mcp` queda excluido como punto de partida de Ciel V0.

Aunque es estratégicamente importante, no es un repositorio simple de un solo producto. Es un repositorio integrado compuesto por proyectos que originalmente fueron individuales, entre ellos:

* `SES`
* `tempus-engine`
* `tempus-ddb`

Estos proyectos internos tienen sus propios:

* README.
* Dockerfiles.
* Benchmarks.
* Supuestos arquitectónicos.
* Historial conceptual.
* Niveles de madurez.

Usar `tempus-mcp` como objetivo inicial obligaría a Ciel V0 a resolver análisis multiproyecto antes de haber validado el caso más simple:

```txt
un repositorio
  → una intención
  → una realidad
  → una brecha de implementación
  → un plan de decisión
```

Por lo tanto:

* `universal-ai-kernel` es el punto de partida de Ciel V0.
* `jsonlogic-fast` puede usarse como caso técnico limpio temprano.
* `tempus-mcp` se reserva como benchmark avanzado para una fase posterior.
* Antes de analizar correctamente `tempus-mcp`, Ciel necesitará una skill dedicada:

```txt
detect_product_boundaries
```

Esa skill deberá detectar límites internos de producto, separar contextos y generar reportes independientes por unidad funcional.

---

## 13. Non-Goals de V0

Para proteger foco, Ciel V0 no hará todavía:

* Modificación automática de código.
* Refactors autónomos.
* Commits automáticos.
* Pull Requests automáticos.
* Publicación de paquetes.
* Despliegues.
* Memoria vectorial pesada.
* Multiagente distribuido.
* Análisis profundo de monorepos o repos multiproducto.
* Ejecución de comandos destructivos sin aprobación explícita.
* Integración compleja con GitHub Issues o CI/CD.

Ciel V0 se limita a:

```txt
leer → clasificar → comparar → diagnosticar → recomendar
```

---

## 14. Definition of Done de V0

Ciel V0 estará terminado cuando pueda autoanalizarse localmente con:

```bash
ciel analyze ./universal-ai-kernel
```

Y devolver consistentemente:

1. **Identidad detectada**
   Qué dice el proyecto que es.

2. **Resumen de intención**
   Claims principales extraídos del README/docs.

3. **Mapeo de realidad**
   Qué componentes existen realmente en archivos.

4. **Comportamiento comprobable**
   Tests, ejemplos o evidencia de ejecución disponibles.

5. **Matriz de brecha**
   Qué claims están implementados, parciales, ausentes o contradichos.

6. **Puntaje de madurez**
   Claridad de intención, completitud, estabilidad, operación y preparación comercial.

7. **Veredicto**
   Estado real del proyecto.

8. **Acción prioritaria**
   Qué debe hacerse primero y por qué.

9. **Salida terminal limpia**

10. **Export JSON**

11. **Export Markdown**

---

## 17. Decisión Oficial

Ciel V0 nace como evolución de:

```txt
JPatronC92/universal-ai-kernel
```

`universal-ai-kernel` aporta el alma:

* Disciplina.
* SOPs.
* Mandato operativo.
* Ciclo de ejecución.
* Prevención de alucinaciones.
* Trazabilidad conceptual.

Ciel Kernel V0 aporta el cerebro:

* Purpose Resolver.
* Source Role Assignment.
* Layered Retrieval.
* Evidence Bundle.
* Intention vs Reality Diff.
* Implementation Gap Report.
* Decision Plan.

La tesis final es:

> **Ciel Kernel es un sistema operativo de inteligencia para agentes de software que convierte contexto disperso en decisiones técnicas y comerciales ejecutables mediante gobernanza jerárquica, evidencia clasificada y detección de brecha entre intención y realidad.**
