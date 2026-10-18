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