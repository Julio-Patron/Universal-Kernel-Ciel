
DISEÑO INTEGRAL DE PRODUCTO · ROADMAP · ESTRATEGIA COMERCIAL
Documento maestro v1.0 · 16 de julio de 2026


Contenido
1. Decisión ejecutiva
2. Arquitectura de marca e identidad
3. Problema y oportunidad
4. Cliente, usuario y trabajo a resolver
5. Definición exacta del producto
6. Experiencia de producto y UX
7. Modelo de evidencia y reglas de decisión
8. Arquitectura técnica
9. Transformación del repositorio existente
10. Alcance del MVP
11. Roadmap completo
12. Estrategia comercial
13. Packaging y precios
14. Go-to-market y ventas
15. Competencia y diferenciación
16. Economía y escenarios
17. Adversidades y respuestas
18. Métricas y criterios de decisión
19. Plan operativo de 90 días
20. Backlog inicial
21. Mensajes de lanzamiento
22. Referencias y supuestos


1. Decisión ejecutiva
El mejor producto derivado de Universal AI Kernel es un GitHub Check obligatorio que responde una pregunta única: ¿este pull request demostró que cumplió sus criterios de aceptación?


MergeProof no intentará revisar estilo, seguridad, arquitectura, vulnerabilidades, documentación y calidad general al mismo tiempo. Esos mercados ya están ocupados. La cuña es más estrecha y verificable: convertir criterios de aceptación en una matriz de prueba vinculada al diff y a resultados de CI.
La condición para que el producto se vuelva necesario es que el check sea requerido por GitHub Rulesets. Cuando falla, el PR no puede fusionarse. GitHub permite imponer reglas y combinar reglas restrictivas; su Checks API permite a una GitHub App publicar check runs vinculados al commit. (GitHub Docs, consulta 16-jul-2026).

Qué se vende realmente
Menos trabajo declarado como terminado sin pruebas suficientes.
Menos revisión manual dedicada a comprobar el alcance básico.
Una trazabilidad ligera entre requisito, cambio, prueba, ejecución y commit.
Un recibo defendible ante clientes, QA y auditoría interna.
Qué no se vende
Una garantía de ausencia de defectos.
Una auditoría completa del repositorio.
Un sustituto de revisión humana, QA, SAST o pruebas end-to-end.
Una IA que decide de manera opaca si el código es “bueno”.
2. Arquitectura de marca e identidad
Para preservar los activos existentes sin confundir al mercado se adopta una arquitectura de tres niveles:

Nombre y tagline

Sistema verbal
La voz debe ser breve, verificable y operacional. Evitar lenguaje antropomórfico o absoluto. El vocabulario de estado es limitado:

Sistema visual


3. Problema y oportunidad
La generación de código es cada vez más barata y paralela. GitHub documenta agentes cloud, tareas autónomas, ejecución paralela, PRs y revisiones. La consecuencia comercial no es que falte más código: falta una forma barata de comprobar que el código entregado corresponde al trabajo solicitado.
Problema operativo
1.  Un issue o PR contiene criterios de aceptación, a menudo ambiguos o incompletos.
2.  Un desarrollador o agente modifica código y declara la tarea terminada.
3.  CI confirma que “las pruebas pasan”, pero no demuestra qué criterio cubre cada prueba.
4.  El revisor debe reconstruir manualmente la relación entre requisito, diff y comportamiento.
5.  Si el equipo tiene alta velocidad de PRs, esa reconstrucción se omite o se hace superficialmente.
Oportunidad
MergeProof ocupa el espacio entre el tracker, el diff y CI. No reemplaza ninguna herramienta: crea la relación ausente y la transforma en una condición de merge.

Por qué ahora
Los agentes generan más PRs y reducen el costo de producir cambios.
GitHub ya proporciona el punto de enforcement mediante Rulesets y Checks.
Los reviewers de IA existentes se concentran en detectar problemas generales, no en producir una cadena ejecutada criterio→prueba→resultado.
El análisis puede ejecutarse dentro de CI, reduciendo costos de infraestructura y objeciones de privacidad.
Hipótesis comercial

4. Cliente, usuario y trabajo a resolver
Perfil de cliente ideal inicial

Jobs to be Done

Segmentos prioritarios
1.  Agencias de desarrollo que necesitan defender entregables y reducir retrabajo no cobrado.
2.  SaaS pequeños que adoptaron Codex, Copilot, Claude Code, Cursor u otros agentes.
3.  Equipos con contratistas o contribuciones remotas donde la intención del cambio se pierde.
4.  Plataformas internas que quieren estandarizar quality gates sin comprar un ALM empresarial.
5. Definición exacta del producto

Contrato de entrada
El MVP exige un bloque explícito en el cuerpo del PR. Esto evita depender inicialmente de Linear, Jira o de enlaces ambiguos a issues:

Contrato de salida

Estados

Principios no negociables
El LLM propone vínculos; no puede producir PROVEN sin evidencia concreta.
Toda prueba debe estar asociada a una ejecución y un commit.
Un check inconcluso falla cerrado o queda neutral según política, nunca pasa silenciosamente.
Cada waiver identifica autor, motivo, criterio, commit y fecha.
El recibo incluye la versión exacta de política y del motor.

6. Experiencia de producto y UX
La interfaz principal no será un dashboard. Será el pull request. El dashboard aparece sólo cuando existe necesidad pagada de administración, retención y políticas organizacionales.
Flujo de activación
1.  Instalar la GitHub App o añadir la Action.
2.  Ejecutar `mergeproof init`, que crea `.mergeproof.yml` y un PR template.
3.  Abrir un PR de ejemplo con dos criterios.
4.  MergeProof corre en shadow mode y publica una matriz sin bloquear.
5.  El equipo corrige mapeos o añade anotaciones `@proof AC-x` cuando sea necesario.
6.  El maintainer activa `tempus/mergeproof` como required check.
7.  Cada PR futuro debe pasar o registrar un waiver.
Tiempo al primer valor

Superficies del MVP

Flujos críticos
A. PR correcto. MergeProof identifica criterios, ingiere resultados, vincula evidencia y pasa.
B. Código sin prueba. El criterio queda PARTIAL y propone el test o anotación faltante.
C. Criterio no verificable. El sistema lo marca NOT_TESTABLE y exige policy o waiver.
D. CI flaky. El sistema separa “test execution failed” de “acceptance proof failed”; no inventa ausencia de evidencia.
E. Cambio posterior. Cualquier nuevo commit invalida el recibo anterior y vuelve a ejecutar el check.
Diseño del mensaje de error
Cada bloqueo debe contener: estado, evidencia encontrada, evidencia faltante, acción concreta y comando de diagnóstico. Nunca mostrar sólo “confidence too low”.

7. Modelo de evidencia y reglas de decisión
La unidad central no es el archivo ni el comentario del modelo. Es un Proof Link: una relación versionada entre un criterio y una pieza de evidencia.
Tipos de evidencia

Regla de decisión inicial

Modelo de datos mínimo

Estrategia de mapeo
1.  Coincidencia explícita: `@proof AC-3` en nombre, comentario o manifest. Máxima prioridad.
2.  Relación estructural: test importa o ejecuta símbolos modificados.
3.  Coincidencia semántica: criterio, nombres, docstrings y assertions.
4.  Cobertura de patch: líneas modificadas ejecutadas por la prueba, cuando esté disponible.
5.  LLM como adjudicador de candidatos, nunca como sustituto de ejecución.
Precisión antes que cobertura
En el MVP es preferible dejar un criterio PARTIAL que producir un falso PROVEN. La confianza comercial se destruye con una sola autorización falsa; un falso bloqueo es molesto, pero explicable y corregible.
8. Arquitectura técnica

Componentes

Decisiones tecnológicas
Mantener Python para el MVP. El código existente ya es Python y reescribir en Rust no mejora la validación comercial.
Paquete core sin estado + CLI + contenedor GitHub Action.
FastAPI sólo para webhooks, licencias y receipt endpoints cuando aparezca la GitHub App.
SQLite local para desarrollo; PostgreSQL para control plane multi-tenant.
Pydantic para contratos versionados; YAML para políticas.
OpenTelemetry y logs estructurados desde la beta pagada.
Código fuente permanece en el runner. SaaS metadata-only por defecto.
Permisos de GitHub
La App debe pedir el mínimo: Metadata read, Pull requests read, Contents read, Checks write y Issues read sólo si se habilita importación de criterios. GitHub restringe la creación de check runs a GitHub Apps con permiso de escritura en Checks; esto hace que la App sea el vehículo correcto para el producto comercial.
Seguridad y privacidad
No almacenar código fuente por defecto.
No enviar secretos ni variables de CI al modelo.
Redactar strings de alta entropía y rutas configuradas.
BYOK y modelo local en planes superiores.
Recibos exportables y verificables sin depender del dashboard.
Aislar tenants y rotar installation tokens automáticamente.
9. Transformación del repositorio existente
El repo actual no debe desecharse. Debe cambiar de producto y vocabulario. La extracción se realiza por sustitución dirigida, no por reescritura completa.

Estructura recomendada

Regla de migración

10. Alcance del MVP
Incluido
GitHub únicamente.
Criterios explícitos en el cuerpo del PR.
Python, TypeScript/JavaScript y Rust para extracción básica.
JUnit XML como formato universal; adapters convenientes para pytest, Jest/Vitest y Cargo.
Estados PROVEN, PARTIAL, UNPROVEN, NOT_TESTABLE y WAIVED.
GitHub Check summary y annotations.
Config YAML y CLI de diagnóstico.
Shadow mode y enforcement mode.
Recibo JSON firmado/hash-linked.
Excluido
Revisión general de bugs, seguridad o estilo.
Generación automática de código o tests.
Linear, Jira, GitLab y Bitbucket.
Dashboard analítico completo.
Cobertura formal de lenguajes y frameworks ilimitados.
Prueba automática de criterios puramente visuales o subjetivos.
Compliance regulatorio certificado.
Control de acciones de agentes; eso pertenece a Tempus Gate.
Criterios de aceptación del MVP
1.  Instalación en repositorio de ejemplo en menos de 15 minutos.
2.  Extrae 100% de criterios bien formados del PR template.
3.  Ingiere JUnit XML y verifica que corresponde al head SHA.
4.  Publica un Check Run actualizado por cada commit.
5.  Nunca produce PROVEN sin ejecución exitosa vinculada.
6.  Permite anotación explícita `@proof AC-x`.
7.  Waiver requiere rol, motivo y expiración.
8.  Procesa un PR mediano en menos de 90 segundos, excluyendo tiempo de tests.
9.  No envía código fuente fuera del runner en modo privacy-default.
10.  Tiene una suite de 50+ fixtures con casos positivos, ambiguos y adversariales.
11. Roadmap completo

Fase 0 — Contratos y extracción (semanas 1–2)
Congelar features legacy y crear rama `product/mergeproof`.
Definir schemas v1, fixtures y política por defecto.
Crear `mergeproof analyze-pr --event event.json`.
Implementar parser de PR criteria y JUnit adapter.
Crear landing mínima y lista de 50 prospectos.

Fase 1 — Shadow MVP (semanas 3–6)
GitHub Action, annotations, receipt y `mergeproof explain`.
Extractores Python/TS/Rust y mapeo explícito `@proof`.
Semántica opcional con LLM; modo determinista funcional.
5 repositorios de design partners en shadow mode.

Fase 2 — Enforcement beta (semanas 7–10)
GitHub App básica y Check Run propio.
Waivers, roles y policy hash.
Required-check onboarding.
Privacidad documentada y threat model.
10 repositorios activos; 3 equipos usan enforcement.

Fase 3 — Pilotos pagados (semanas 11–16)
Oferta de piloto de 6 semanas por USD 5,000.
Reporte semanal de proof gaps y rework evitado.
Soporte a un segundo framework de test según demanda pagada.
Caso de estudio y evaluación de seguridad externa limitada.

Fase 4 — Self-serve y equipo (meses 5–8)
Instalación de App, checkout, licencias y repositorios administrados.
Políticas de organización, retención y Slack notifications.
Importación opcional desde linked issues y Linear.
Dashboard mínimo: repos, policies, receipts, billing.
Fase 5 — Enterprise selectivo (meses 9–12)
BYOK, single-tenant y self-hosted.
SSO/SAML sólo con contrato firmado.
GHES o GitLab sólo si dos clientes pagan por ello.
SLA y exportación a SIEM.
12. Estrategia comercial
La estrategia óptima no comienza con un SaaS barato y publicidad. Comienza con pilotos pagados que financian precisión, seguridad y onboarding. El self-serve se añade cuando el producto ya pasa required checks sin asistencia continua.
Secuencia comercial
1.  Diagnóstico gratuito de tres PRs recientes: muestra criterios sin evidencia.
2.  Shadow mode durante una semana: no bloquea, mide el problema real.
3.  Piloto pagado de seis semanas: configura enforcement en 2–5 repositorios.
4.  Revisión de resultados: proof gaps detectados, tiempo de revisión, rework y falsos bloqueos.
5.  Contrato anual prepagado: políticas, retención, soporte y más repositorios.
6.  Expansión por organización, no por asientos.
Oferta de piloto

Por qué cobrar desde el inicio
El producto toca el merge y requiere compromiso real del cliente.
Los pilotos gratuitos atraen curiosidad, no urgencia.
El pago valida presupuesto y permite dedicar soporte sin convertirlo en consultoría abierta.
La tarifa se puede acreditar parcialmente para reducir fricción de conversión.
Estrategia de maximización de margen
Análisis local en CI para evitar costos de compute y almacenamiento de código.
Cobro por repositorios o organización; no por cada humano o agente.
Contratos anuales prepagados para financiar desarrollo.
Adaptadores especiales como servicios de implementación con alcance cerrado.
Control plane ligero; no construir un data plane cloud completo.
Soporte de lanzamiento separado del soporte recurrente.
13. Packaging y precios
El mercado de PR review cobra aproximadamente USD 20–48 por usuario/mes en planes de equipo: Graphite publica USD 20 y USD 40; CodeRabbit USD 24 y USD 48; Qodo publica un plan Pro Team desde USD 30 con créditos. MergeProof es más estrecho, por lo que debe cobrar menos que un stack completo para equipos pequeños y más por enforcement, privacidad y contratos anuales en cuentas avanzadas. (Páginas oficiales, 16-jul-2026).

Reglas de pricing
No ofrecer “unlimited enterprise” sin mínimo anual.
No descontar más de 20% salvo prepago plurianual o referencia pública.
Cobrar implementación adicional si requiere runner privado, GHES o formatos de test no soportados.
No crear créditos de IA; el cliente compra cobertura de repositorios y enforcement.
BYOK reduce COGS, pero sigue siendo una característica de plan superior por control y soporte.
Expansión de cuenta
El land es 2–5 repositorios. El expand ocurre cuando la organización convierte el check en regla común, aumenta retención de recibos, añade políticas, integra trackers o requiere despliegue privado.
14. Go-to-market y ventas
Canal inicial: founder-led outbound
Seleccionar empresas con señales observables: contratación de AI engineers, uso público de coding agents, gran volumen de PRs, agencia con entregas frecuentes o contenido sobre “vibe coding” y revisión.
Oferta de entrada

Cadencia de prospección

Mensaje outbound

Contenido que sí puede generar demanda
Índice mensual “Acceptance Proof Gap” sobre PRs públicos de agentes.
Casos de estudio: criterio sin prueba que CI no detectó.
Plantillas de PR contract y políticas open source.
Comparativas prácticas: tests passing vs acceptance proven.
Integraciones y ejemplos para Codex, Copilot, Claude Code y Cursor sin posicionarse contra ellos.
Canales posteriores
GitHub Marketplace, cuando la activación sea self-serve.
Alianzas con agencias de desarrollo y consultores DevSecOps.
Integradores de QA y testing automation.
Programas de design partners con agentes de código.
Resellers sólo después de tener onboarding repetible.
15. Competencia y diferenciación
CodeRabbit, Qodo y Graphite ofrecen revisiones, reglas, analytics, fixes y controles de PR. Competir por amplitud sería una mala estrategia. MergeProof debe ser complementario: un check de evidencia que puede convivir con cualquiera de ellos.

Moat realista
Dataset de PRs, criterios y proof links corregidos por usuarios.
Adapters y conformance suite para frameworks de test.
Recibos versionados y verificables como formato abierto.
Integración profunda con required checks y workflows existentes.
Confianza derivada de baja tasa de falsos PROVEN, no de claims de “mejor modelo”.
Posicionamiento

16. Economía y escenarios
Estos escenarios son objetivos operativos, no pronósticos. Suponen fundador técnico, ventas directas, infraestructura ligera y contratos anuales netos del crédito de piloto.

Objetivos económicos
Margen bruto objetivo superior a 85% una vez estabilizado, gracias al análisis local.
CAC inicial dominado por tiempo del fundador, no publicidad.
Payback del CAC menor a 6 meses en contratos anuales.
Soporte recurrente menor a 2 horas por cliente/mes en self-serve y menor a 6 horas en Business.
Más del 60% de ingresos nuevos en modalidad anual prepaga al final del primer año.
Gastos prioritarios
1.  Revisión de seguridad y privacidad.
2.  GitHub App, firma de releases y supply-chain hardening.
3.  Fixtures, adapters y documentación de onboarding.
4.  Asesoría legal para marca, términos, DPA y limitación de responsabilidad.
5.  Observabilidad y soporte, antes que un dashboard vistoso.
Gastos a evitar
Equipo comercial grande antes de product-market fit.
Publicidad pagada generalista.
Reescritura completa del motor.
Soporte simultáneo para todas las forjas y trackers.
Certificaciones costosas sin contrato que las financie.
17. Adversidades y respuestas

Regla general

18. Métricas y criterios de decisión
North Star

Producto

Negocio

Señales para continuar
Tres equipos mantienen el check requerido durante cuatro semanas.
Al menos dos pilotos pagan USD 5,000 sin requerir integración a medida desproporcionada.
Se detectan proof gaps que los clientes reconocen como reales y costosos.
La instalación puede completarse sin sesión del fundador.
Existe demanda pagada por retención, policies o despliegue privado.
Señales para pivotar
La mayoría de equipos no escribe criterios suficientemente verificables.
Los falsos bloqueos permanecen por encima de 10% después de mapping explícito.
Los clientes consideran suficiente CI + code review existente.
Nadie acepta convertir el check en required.
El valor percibido está sólo en reportes retroactivos.
Pivot cercano

19. Plan operativo de 90 días

Rutina semanal del fundador

Principio de ejecución

20. Backlog inicial

21. Mensajes de lanzamiento
Landing page

Subheadline: Tempus MergeProof links every acceptance criterion to code and tests that actually ran, then blocks the pull request when proof is missing.
Tres beneficios:
Required proof: unsupported criteria fail before merge.
Runs inside CI: your source code stays in your runner.
Verifiable receipt: criterion, evidence, test run, policy and commit are linked.
CTA: Protect your first pull request.
Pitch de 30 segundos
Los agentes ya pueden producir pull requests más rápido de lo que un equipo puede verificarlos. CI dice que las pruebas pasan, pero no demuestra que cada criterio de aceptación esté cubierto. Tempus MergeProof convierte los criterios del PR en un contrato, los vincula con el diff y pruebas ejecutadas, y publica un required check. Si falta evidencia, no hay merge. No es otro code reviewer: es una prueba de que el trabajo declarado está hecho.
Demo de cinco minutos
1.  Mostrar un PR con cuatro criterios y CI verde.
2.  MergeProof marca dos PROVEN, uno PARTIAL y uno UNPROVEN; el merge está bloqueado.
3.  Abrir AC-3 y mostrar código encontrado, pero prueba faltante.
4.  Añadir test con `@proof AC-3`; push.
5.  Mostrar nuevo recibo, PASS y merge habilitado.
Mensajes que deben evitarse
“Garantiza que no hay bugs”.
“Reemplaza a QA y revisión humana”.
“Comprende cualquier requisito automáticamente”.
“Compliance instantáneo”.
“El mejor AI code reviewer”.
22. Referencias y supuestos
Fecha de mercado: 16 de julio de 2026. Los precios y capacidades pueden cambiar; deben verificarse antes de publicar materiales comerciales.
Fuentes oficiales de plataforma y competencia
GitHub Docs — About rulesets
GitHub Docs — Available rules for rulesets
GitHub Docs — REST API endpoints for check runs
GitHub Docs — About Copilot cloud agent
CodeRabbit — Pricing
Qodo — Pricing
Graphite — Pricing
Investigación técnica contextual
Al-Msie'deen (2023) — Requirements Traceability: Recovering and Visualizing Traceability Links
Hey & Frattini (2026) — How Requirements Quality Makes (or Breaks) Traceability Link Recovery
Zhou et al. (2026) — Change And Cover: PR-Based Regression Test Augmentation
Base técnica
Evaluación del repositorio `JPatronC92/universal-ai-kernel`, rama por defecto observada en el commit `fad33c8ab17140607d36922b976a89ea033a4fbf` (release v0.9.0). El documento asume que los módulos de schemas, scanner, evidence extractor, rulesets, model router y decision ledger son la base de Ciel Evidence Engine.
Supuestos económicos
Empresa inicialmente pequeña y founder-led.
Costos de cloud bajos porque el análisis corre localmente.
Piloto de USD 5,000 con 50% acreditable al anual.
No se incluyen impuestos, comisiones, salarios ni gasto legal en escenarios de bookings.
Los escenarios no son promesas de ingresos; son umbrales de planificación.
