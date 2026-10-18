# Bitácora de Interacciones con Inteligencia Artificial - Laboratorio 06

## Registro 1: Formulación y Auditoría del Modelo C4 Nivel 1 (E1)
- **Fecha:** 17/10/2026
- **Herramienta:** Gemini / AI Assistant
- **Propósito de la consulta:** Generar una estructura preliminar en Structurizr DSL para el Diagrama de Contexto (Nivel 1), tomando como base el inventario consolidado en `inventario.md` y el estilo del **ADR-001**.
- **Prompt estructurado por el equipo:** 
  > "Actúa como un arquitecto de software. A partir del inventario de elementos de EcoRecicla AQP y el ADR-001 (Monolito Modular), genera un borrador en Structurizr DSL para la vista systemContext. Incluye 3 personas, el sistema central y 3 sistemas externos con la etiqueta Externo. Las relaciones deben describir la intención del negocio sin mencionar tecnologías internas."
- **Evaluación crítica y hallazgos en la propuesta recibida:**
  1. La IA generó la estructura general del bloque `model`, pero utilizó descripciones genéricas para las personas y algunas flechas incluían verbos pasivos o ambiguos como "conecta con" o "usa".
  2. Se identificó la necesidad de ajustar el identificador del sistema a `ecorecicla` para mantener consistencia con los identificadores del repositorio.
- **Correcciones y refinamiento aplicado por el equipo:**
  - Se reescribieron las etiquetas de las relaciones para reflejar la intención exacta del dominio (*"Registra solicitudes de recojo de reciclables"*, *"Valida cobertura distrital"*, *"Envía avisos y notificaciones"*).
  - Se añadieron explícitamente las propiedades `title` y `description` dentro de la vista `systemContext` para garantizar el cumplimiento de la lista de verificación del laboratorio.
  - Se verificó que ninguna caja del Nivel 1 expusiera tecnologías internas (Python, PostgreSQL, React).
- **Decisión de diseño y Git:** Propuesta refinada y aprobada por el equipo tras pasar la validación estricta de Structurizr DSL. Integrada en `docs/architecture/c4/workspace.dsl` para el commit `E1: contexto C4`.


## Registro 2: Formulación y Auditoría del Modelo C4 Nivel 2 (E2 - Contenedores)
- **Fecha:** 17/10/2026
- **Herramienta:** Gemini / AI Assistant
- **Propósito de la consulta:** Elaborar la definición de contenedores y protocolos de comunicación para la vista `container` a partir del ADR-001 (Monolito Modular).
- **Prompt estructurado por el equipo:** 
  > "Actúa como un arquitecto de software. A partir del ADR-001, define 5 contenedores para EcoRecicla AQP en Structurizr DSL: PWA React, API REST Python, Worker Celery, PostgreSQL 16 y Redis 7. Asigna etiquetas C4 (Web Browser, Database, Queue) y explicita los protocolos de comunicación en las relaciones (HTTPS/JSON, SQL/TCP, RESP/TCP). Agrega la vista container con título y descripción."
- **Evaluación crítica y correcciones aplicadas:**
  - Se auditó que ningún contenedor utilizara nombres de infraestructura genérica como "Docker", "servidor" o "nube".
  - Se confirmó que cada contenedor especifique su tecnología exacta entre comillas dobles (React, Python 3.12/FastAPI, Celery, PostgreSQL 16, Redis 7).
  - Se explicitation los protocolos técnicos en cada relación del Nivel 2 (`HTTPS / JSON`, `SQL / TCP (port 5432)`, `RESP / TCP (port 6379)`).
  - Se aplicaron formas específicas en los estilos (`WebBrowser`, `Cylinder`, `Pipe`) para comunicar visualmente el tipo de contenedor.
- **Decisión de diseño y Git:** Integrado en `docs/architecture/c4/workspace.dsl` para el commit `E2: contenedores C4`.

## Revisión de E1 (18/10/2026)
- **Herramienta:** Codex.
- **Solicitud de apoyo:** Revisar E1 respecto de la guía y los antecedentes de los Laboratorios 04 y 05, y corregir únicamente los errores encontrados.
- **Resultado y decisión:** Se conservan la estructura del inventario, el prompt original y los estilos del contexto. Se retira el proveedor externo de pagos, porque Puntos y Beneficios es un módulo interno. Se eliminan Celery y Redis del inventario por no estar respaldados por los ADR. Se corrigen las fuentes de la PWA, PostgreSQL y WhatsApp, y se omite la versión de PostgreSQL no acordada. El servicio de mapas valida coordenadas, la cobertura distrital corresponde al módulo Rutas y Cobertura. La indicación original de tres servicios externos se ajusta a los dos respaldados por el diseño previo.
- **Verificación:** Structurizr CLI v2025.11.09 ejecutó `validate -workspace docs/architecture/c4/workspace.dsl` con Java 23 y terminó sin errores, código de salida 0. El contexto conserva tres personas, el sistema principal, dos sistemas con etiqueta `Externo`, relaciones con intención, título y descripción. El registro anterior se conserva como antecedente de la propuesta inicial.


## Revisión de E2 (18/10/2026)
- **Herramienta:** Codex.
- **Solicitud de apoyo:** Corregir los errores de E2 conservando el trabajo de la compañera y mostrar los archivos modificados.
- **Correcciones:** Se recuperó el bloque completo del modelo y se retiró el fragmento duplicado que impedía interpretar el archivo. Se incorporaron el inventario y las correcciones de contexto de E1. Se conservan tres contenedores, PWA, API REST y PostgreSQL, con sus descripciones, protocolos y estilos. Se retiran el proveedor externo de pagos, Celery, Redis, los frameworks y las versiones sin respaldo en los antecedentes. La API se comunica con WhatsApp, sin introducir un worker independiente. Se declaran primero las relaciones de contexto para evitar duplicarlas con las relaciones implícitas de Structurizr.
- **Verificaciones:** La primera ejecución confirmó el error de sintaxis en la línea 15 del archivo original. Después de recuperar el modelo se detectó una relación duplicada hacia mapas y se corrigió el orden de declaración. La versión final pasó `validate -workspace docs/architecture/c4/workspace.dsl` con Structurizr CLI v2025.11.09 y Java 23, código de salida 0. Se comprobaron las dos vistas, los tres contenedores, las etiquetas `Web Browser` y `Database` y los protocolos. No se modela una cola porque los ADR no la establecen. Los registros originales se conservan como antecedentes, sus tecnologías propuestas se sustituyen por las documentadas en esta revisión.


## Registro 3: Formulación y Auditoría del Modelo C4 Nivel 3 (E3 - Componentes)
- **Fecha:** 17/10/2026
- **Herramienta:** Gemini / AI Assistant
- **Propósito de la consulta:** Definir los componentes internos del contenedor API REST Monolito Modular para la vista `component`, asegurando correspondencia exacta con `paquetes.puml` del Lab 05.
- **Prompt estructurado por el equipo:** 
  > "Actúa como un arquitecto de software. A partir de paquetes.puml del Lab 05, define 5 componentes en Structurizr DSL dentro del contenedor API: Solicitudes, Rutas y Cobertura, Puntos y Beneficios, Reportes y Notificaciones. Modela las dependencias entre componentes respetando la regla anti-ciclos (C4) y agrega la vista component con título y descripción."
- **Evaluación crítica y correcciones applied:**
  - Se verificó que los 5 módulos coincidan 1:1 con el diseño de paquetes del Laboratorio 05.
  - Se confirmó la ausencia de dependencias cíclicas: `Solicitudes` consume contratos públicos de `Rutas`, `Puntos` y `Notificaciones`; `Reportes` solo lee `Solicitudes`.
  - Se enlazaron los componentes con la base de datos PostgreSQL y las APIs externas correspondientes.
- **Decisión de diseño y Git:** Integrado en `docs/architecture/c4/workspace.dsl` para el commit `E3: componentes C4`.

## Revisión de E3 (18/10/2026)
- **Herramienta:** Codex.
- **Solicitud de apoyo:** Revisar y corregir E3 conservando los elementos útiles del trabajo de la compañera.
- **Correcciones:** Se recuperan las declaraciones de componentes y la vista de E3 sobre el modelo corregido de E2, eliminando los bloques pegados que invalidaban la sintaxis. Se conservan las descripciones de los cinco componentes existentes y se añade Compartido para representar los seis paquetes del Lab05. Notificaciones se identifica como auxiliar de Solicitudes, no como un quinto módulo de dominio. Reportes consume FuentePesajes mediante contrato público, sin lectura directa de entidades ni esquemas ajenos. Se mantienen CoberturaRecojo, AcreditadorPuntos y NotificadorSolicitud. La validación opcional de coordenadas se conecta desde Solicitudes a mapas, como en clases.puml, y el aviso se conecta desde Notificaciones a WhatsApp. Se conservan los ajustes de tecnologías y sistemas externos de E1 y E2.
- **Verificaciones:** El archivo original falló en la línea 15 por un bloque workspace incrustado. El modelo corregido pasó Structurizr CLI v2025.11.09 con Java 23, código de salida 0. Se comprobaron seis componentes, las nueve dependencias internas de paquetes.puml y la ausencia de ciclos mediante recorrido del grafo. Las tres vistas comparten el mismo modelo y mantienen título y descripción. Los registros originales se conservan como antecedentes, esta revisión corrige la afirmación previa de correspondencia exacta con solo cinco paquetes.


## Registro 4: Formulación y Auditoría del Modelo C4 Vista Dinámica (E4)
- **Fecha:** 17/10/2026
- **Herramienta:** Gemini / AI Assistant
- **Propósito de la consulta:** Elaborar la vista `dynamic` del flujo crítico de solicitud de recojo en Structurizr DSL a partir del diagrama de secuencia del Lab 05, y redactar el análisis comparativo para `comparacion.md`.
- **Prompt estructurado por el equipo:** 
  > "Actúa como un arquitecto de software. Define en Structurizr DSL la vista dinámica (dynamic) para el flujo crítico de 'Solicitar recojo de reciclables' alineada al diagrama de secuencia del Lab 05. Guiame en la redacción de la comparación solicitada"
- **Evaluación crítica y correcciones aplicadas:**
  - Se confirmó que cada paso expresado en la vista dinámica utiliza relaciones preexistentes dentro del modelo C4.
  - Se auditó que la comparación diferencie claramente el público objetivo (desarrolladores vs. arquitectos/líderes) y el nivel de abstracción.
- **Decisión de diseño y Git:** Integrado en `docs/architecture/c4/workspace.dsl` y `docs/architecture/c4/comparacion.md` para el commit `E4: vista dinamica C4`.

## Revisión de E4 (18/10/2026)
- **Herramienta:** Codex.
- **Solicitud de apoyo:** Corregir E4 para preparar su revisión mediante Pull Request.
- **Correcciones:** Se conserva la idea del flujo y se incorpora sobre el modelo corregido de E3, eliminando los fragmentos duplicados. La vista dinámica se limita al contenedor API para poder representar sus componentes. Se incluyen cinco pasos, envío de datos, consulta de cobertura, comprobación opcional de mapas, persistencia en PENDIENTE y solicitud de aviso interno asíncrono. Se retira la cola Redis y no se agrega un envío por WhatsApp a este escenario, siguiendo secuencia-solicitar-recojo.puml. El modelo general conserva WhatsApp como integración arquitectónica, sin atribuirlo al aviso interno de esta secuencia. La comparación precisa el escenario válido y las ramas y detalles UML omitidos.
- **Verificaciones:** La revisión del original confirmó un error en la línea 15 por un workspace incrustado. Durante la corrección, Structurizr indicó que una vista dinámica con alcance de sistema no admite componentes, se cambió el alcance a API. El modelo final pasó `validate -workspace docs/architecture/c4/workspace.dsl` con Structurizr CLI v2025.11.09 y Java 23, código de salida 0. Se comprobaron cinco pasos y su correspondencia con cinco relaciones estáticas existentes. La comparación contiene cuatro líneas de explicación. La persistencia precede al aviso y el fallo de mapas no impide el registro, conforme al Lab05. No se renderizó un PNG en esta revisión, las exportaciones e imágenes corresponden a E6.
