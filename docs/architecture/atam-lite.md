# E3 y E7. ATAM-lite de EcoRecicla AQP

## Estado de la revisión externa

**Pendiente de revisión del docente.** Por indicación del curso, no se realizará revisión entre grupos. A la fecha de este registro, el equipo no ha recibido observaciones externas. Cuando el docente las envíe, se copiarán en la tabla correspondiente y se responderán con evidencia.

## Alcance y método

Se revisaron internamente el [árbol de utilidad y escenarios](utilidad/escenarios.md), la [iteración 1](add/iteracion-1.md), la [iteración 2](add/iteracion-2.md), la [iteración 3](add/iteracion-3.md), los [resultados JSON](add/evidencia-1.json), [evidencia-2.json](add/evidencia-2.json) y [evidencia-3.json](add/evidencia-3.json), los ADR-006 a ADR-008 y el [workspace C4](c4/workspace.dsl). El Prompt IA 3 se adaptó como apoyo para este análisis del propio modelo; cada hallazgo se contrastó con los archivos y resultados citados. No representa una evaluación de otro grupo ni reemplaza la revisión pendiente del docente.

## Punto de sensibilidad

**QA-02/QA-07: latencia de cada intento de sincronización.** El lote produce 132 llamadas por los 120 registros y 12 ACK perdidos. Con 100 ms por llamada, el modelo estima 13.2 s y cumple el límite de 30 s; con 250 ms, estima 33 s y falla. El máximo teórico bajo el supuesto secuencial es `30 s / 132 = 0.227 s` por llamada. Por tanto, la decisión depende de que el tiempo medio total de cada intento, incluidos red y transacción, se mantenga aproximadamente por debajo de 227 ms. Es un resultado del modelo virtual, no una medición de red real.

## Trade-off verificado

**QA-01/QA-06: configuración por distrito dentro de módulos frente a infraestructura separada.** El prototipo versionado incorporó 9 configuraciones, pasó 24 comprobaciones y no modificó los tres archivos consumidores observados, cambiar D01 no alteró los otros 11 distritos. La configuración dentro de los módulos evita duplicar despliegues para el equipo de dos integrantes. El costo aceptado es validar y autorizar cambios versionados. La [estimación de E2](add/estimacion-esfuerzo-1.md) calcula **1.60 días-persona** centrales frente al límite de 2, con PERT, reserva del 25 % y una convención de 8 horas por día-persona. El caso pesimista con reserva llega a **2.50 días-persona**. La estimación supone mecanismos reutilizables de API, persistencia y autorización, cuya construcción inicial no está incluida. No son horas medidas ni garantía de cumplimiento desde el prototipo actual. QA-06 requiere su propia comprobación y no se verificó persistencia real en PostgreSQL.

## Matriz de riesgos propios

La probabilidad (P) y el impacto (I) se estiman cualitativamente de 1 (bajo) a 5 (muy alto); no son frecuencias medidas. Puntaje = P × I. Bandas: crítico 15–25, alto 10–14, moderado 5–9, bajo 1–4.

| ID | Hallazgo / riesgo | P | I | Puntaje / zona | Evidencia | Mitigación o decisión |
|---|---|---:|---:|---|---|---|
| R-01 | Sin JWT/middleware y RLS reales, una ruta de producción que omita el contrato distrital podría exponer o modificar datos de otro distrito. | 4 | 5 | 20 / Crítico | [ADR-008](adr/008-autorizacion-distrital.md) declara esos controles pendientes; el prototipo solo ejercita una guarda local ([evidencia-3](add/evidencia-3.json)). | **No aceptar para producción.** Implementar contexto desde autenticación, revisar todos los endpoints, configurar RLS con rol sin `BYPASSRLS` y probar contexto transaccional y pool. Repetir QA-04/QA-05 contra PostgreSQL real. |
| R-02 | La PWA real podría perder pendientes por cuota, borrado o fallo de IndexedDB; el prototipo no usa IndexedDB. | 3 | 5 | 15 / Crítico | [ADR-007](adr/007-sincronizacion-idempotente.md) y [iteración 2](add/iteracion-2.md) señalan que SQLite sustituyó a IndexedDB y asumió almacenamiento local sano. | **No aceptar como garantía de producción.** Integrar escritura durable en IndexedDB, manejar cuota y errores, y probar almacenamiento lleno, cierre abrupto, reapertura y reintentos antes de afirmar QA-02. |
| R-03 | La sincronización excede 30 s cuando cada una de las 132 llamadas secuenciales supera aproximadamente 227 ms. | 3 | 4 | 12 / Alto | [evidencia-2.json](add/evidencia-2.json): 13.2 s modelados a 100 ms y 33 s a 250 ms. | Medir el endpoint real con red y PostgreSQL; optimizar por lote o concurrencia con idempotencia, y conservar una prueba para el límite de 30 s. No declarar cumplimiento solo por el caso base. |
| R-04 | El esfuerzo de alta podría superar 2 días-persona, especialmente sin mecanismos genéricos reutilizables. | 4 | 3 | 12 / Alto | La [estimación de E2](add/estimacion-esfuerzo-1.md) da 1.60 días-persona centrales y 2.50 pesimistas. [evidencia-1.json](add/evidencia-1.json) mantiene `dias_persona` sin valor porque el prototipo no mide trabajo humano. | Riesgo abierto. Contrastar la estimación con un alta real, incluyendo integración, permisos, pruebas y revisión. Estimar por separado la construcción inicial de los mecanismos. No declarar QA-01 cumplido por la estimación central ni extenderla a QA-06. |
| R-05 | Un cambio posterior podría romper el workflow o integrarse sin comprobar su última ejecución. | 2 | 3 | 6 / Moderado | Las ramas E5–E8 ya están publicadas. La captura de Actions compartida por la usuaria muestra ejecuciones verdes de los PR [#37](https://github.com/SharonCondoriUNSA/cs-2026b-lab04-grupo10/pull/37/checks), [#38](https://github.com/SharonCondoriUNSA/cs-2026b-lab04-grupo10/pull/38/checks), [#39](https://github.com/SharonCondoriUNSA/cs-2026b-lab04-grupo10/pull/39/checks) y [#40](https://github.com/SharonCondoriUNSA/cs-2026b-lab04-grupo10/pull/40/checks). | El pendiente original de publicar y obtener una ejecución remota quedó resuelto para las ejecuciones mostradas. Se mantiene este riesgo residual, comprobar que el check corresponde al último commit antes de integrar. La captura previa no acredita automáticamente las correcciones posteriores. |
| R-06 | Un cambio de tarifa u horario mal autorizado o con versión inválida podría afectar el distrito equivocado. | 2 | 4 | 8 / Moderado | [evidencia-1.json](add/evidencia-1.json) cubre datos sintéticos en memoria, no persistencia ni permisos reales; [ADR-006](adr/006-configuracion-por-distrito.md). | Validar versión creciente y ámbito autorizado en el contrato público de cada módulo; añadir pruebas con PostgreSQL y registro de cambios al integrar. |

### Tratamiento de la zona crítica

R-01 y R-02 permanecen abiertos y no se aceptan para un despliegue de producción. Sus mitigaciones requieren implementación y pruebas reales; los prototipos actuales no bastan para cerrarlos. La condición y evidencia de cierre quedan especificadas en sus filas.

## No-riesgo comprobado en el alcance ensayado

**La pérdida de ACK no produjo efectos duplicados en el prototipo de E4.** Se inyectaron 12 ACK perdidos; el receptor SQLite recibió 132 llamadas y produjo exactamente 120 efectos únicos, con 0 duplicados, 0 pérdidas y 0 pendientes ([evidencia-2.json](add/evidencia-2.json)). Por ello, “el escenario modelado duplica efectos cuando se pierde un ACK” es un no-riesgo para esa simulación. No se extrapola al endpoint productivo, que aún no está implementado.

## Falso positivo del apoyo de IA

Al aplicar el Prompt IA 3, la IA marcó como hallazgo incumplido que E3 no tenía issue ni evaluación de otro grupo. Se verificó que el docente indicó al equipo que él realizaría la revisión y que no habría revisión entre grupos; el estado pendiente y el procedimiento están consignados al inicio de este archivo. Por esa instrucción del curso, la observación de IA es un **falso positivo respecto al procedimiento acordado**. La revisión externa del docente sí continúa pendiente y no se presenta como completada.

## Observaciones externas y respuesta

No se han recibido observaciones del docente al momento de esta actualización. La revisión entre grupos no aplica por indicación del curso.

| Observación recibida del docente | Evidencia citada | Respuesta del equipo | Acción |
|---|---|---|---|
| Pendiente de recepción | Pendiente | Se registrará y aceptará o refutará con evidencia cuando llegue. | Pendiente |

## Prompt IA 3 adaptado para revisión interna

> Actúa como evaluador ATAM escéptico del modelo de EcoRecicla AQP. Examina el árbol de utilidad, las iteraciones ADD 1–3, sus resultados JSON, los ADR-006 a ADR-008 y el workspace C4. Para los escenarios (H,*) identifica puntos de sensibilidad, trade-offs, riesgos con probabilidad e impacto de 1 a 5 y un no-riesgo. Cita archivos y resultados concretos. Separa resultados del prototipo de garantías de producción, identifica evidencia faltante y formula preguntas verificables. No inventes mediciones, no atribuyas una revisión externa y respeta las decisiones comunicadas por el curso.

La IA se usó como apoyo interno. Los hallazgos y el falso positivo se contrastaron con la evidencia local y con la indicación del docente comunicada por el equipo; no se abrió un issue a otro grupo.

## Referencias de E3

- [Árbol de utilidad y escenarios](utilidad/escenarios.md) y [árbol PNG](utilidad/arbol.png).
- [Iteración 1](add/iteracion-1.md), [iteración 2](add/iteracion-2.md) e [iteración 3](add/iteracion-3.md).
- [ADR-001](adr/001-estilo-arquitectonico.md), [ADR-005](adr/005-patrones-de-diseno.md), [ADR-006](adr/006-configuracion-por-distrito.md), [ADR-007](adr/007-sincronizacion-idempotente.md) y [ADR-008](adr/008-autorizacion-distrital.md).
- [Vista de contenedores exportada](c4/export/structurizr-VistaContenedores.puml) y [workspace C4](c4/workspace.dsl).
