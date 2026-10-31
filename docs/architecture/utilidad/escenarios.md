# E1. Árbol de utilidad de EcoRecicla AQP

## Entradas y alcance

Se parte de [drivers.md](../drivers.md), [ADR-001](../adr/001-estilo-arquitectonico.md) y [ADR-005](../adr/005-patrones-de-diseno.md). La tabla 11 de la guía Lab08 amplía el caso 10 de **3 a 12 distritos, cada uno con su regla de puntos y horario de recojo**. Se mantienen un mes, dos integrantes, bajo presupuesto, un despliegue y esquemas por módulo. Los distritos son ámbitos de autorización dentro de los módulos, no reemplazan dichos esquemas.

Los objetivos originales QA-01 a QA-03 conservan sus identificadores. Las cargas, tamaños y umbrales nuevos son supuestos de laboratorio, pendientes de validación con usuarios y mediciones de producción. H, M y L significan alta, media y baja. La dificultad estima el trabajo de ingeniería, no el resultado de una prueba ya realizada.

## Escenarios de seis partes

| ID / atributo | Fuente | Estímulo | Entorno | Artefacto | Respuesta | Medida | Importancia, dificultad |
|---|---|---|---|---|---|---|---|
| QA-01 Modificabilidad | Municipalidad | Solicita incorporar un distrito con reglas y horario propios | Desarrollo, crecimiento de 3 a 12 distritos | Contratos de Cobertura y Puntos | Registra configuración y reutiliza estrategias sin cambiar consumidores | ≤ 2 días-persona por distrito, 0 cambios en servicios consumidores | H,H |
| QA-02 Disponibilidad | Reciclador | Registra recojos durante 20 min sin red | Ruta, dispositivo disponible y almacenamiento local sano | Registro local PWA y sincronización | Conserva y reenvía registros identificados al volver la red | 0 registros perdidos y 0 duplicados, sincronización ≤ 30 s tras recuperar red | H,H |
| QA-03 Rendimiento | Reciclador | Consulta ruta diaria | 7:00–9:00, 12 distritos, carga sintética de 12 consultas/s | Consulta del módulo Rutas | Entrega puntos ordenados autorizados | p95 ≤ 2000 ms, ventana simulada de 120 s, 4 ejecutores | H,M |
| QA-04 Seguridad / aislamiento | Administrador de un distrito | Intenta consultar o modificar datos de otro distrito | Sesión autenticada con ámbito distrital distinto | Acceso a Solicitudes y Reportes | Rechaza acceso ajeno y conserva datos originales | 0 lecturas y 0 escrituras cruzadas en 132 pares ordenados de 12 distritos | H,H |
| QA-05 Seguridad / privilegios | Cliente sin ámbito distrital confiable | Omite o falsifica el distrito de una solicitud | Petición sin autenticación válida o con parámetro distinto al ámbito autorizado | Límite de autorización de API | Rechaza la operación antes de acceder a datos | 100 % de peticiones sin ámbito rechazadas y 0 accesos con distrito falsificado en la batería del prototipo | H,M |
| QA-06 Modificabilidad | Municipalidad | Cambia tarifa o franja de un distrito existente | Operación de configuración versionada | Reglas de Puntos y catálogo de Cobertura | Publica versión para ese distrito sin alterar los otros once | 0 modificaciones de código consumidor, 0 variaciones en los otros 11 distritos, ≤ 1 día-persona | H,M |
| QA-07 Rendimiento | Reciclador | Reintenta sincronizar un lote al recuperar red | 12 distritos, hasta 120 registros pendientes por dispositivo | Receptor de sincronización | Confirma cada identificador una sola vez | Procesar 120 registros en ≤ 30 s y producir exactamente 120 efectos únicos | H,M |

QA-04 y QA-05 concretan multitenencia como aislamiento distrital. Seguridad cubre su aspecto de acceso y modificabilidad cubre la incorporación de nuevas variantes. Los tiempos humanos de QA-01 y QA-06 son presupuestos, contar archivos o ejecutar rápido un prototipo no prueba días-persona.

## Priorización y corrección de la propuesta de IA

La propuesta inicial de apoyo calificó QA-01 como (H,M) por la existencia de Strategy y Factory en Lab07. La revisión técnica la eleva a **(H,H)**: la fábrica actual selecciona material y el servicio recibe una sola tabla de tarifas, todavía no hay selección por distrito ni catálogo de horarios. Se comprueba en `src/puntos_beneficios/reglas.py` y `src/puntos_beneficios/servicio.py`. Reutilizar patrones no resuelve por sí solo el nuevo ámbito distrital.

Se prioriza QA-01 para iteración 1 por ser el atributo crítico de drivers y el detonante del crecimiento. QA-04 tiene igual calificación y se atiende en iteración 3, QA-02 en iteración 2. QA-03 y QA-07 complementan la carga y la recuperación. No se presupone que HTTPS ya esté desplegado ni que existan controles RLS.

## Artefactos y verificación

- [Fuente Graphviz](arbol.dot) y [PNG](arbol.png).
- Siete escenarios numéricos, cuatro atributos y escenarios de alta prioridad para modificabilidad y multitenencia.
- Renderización: `dot -Tpng docs/architecture/utilidad/arbol.dot -o docs/architecture/utilidad/arbol.png`.
- E1 define objetivos, no declara que el sistema desplegado ya los cumpla.
