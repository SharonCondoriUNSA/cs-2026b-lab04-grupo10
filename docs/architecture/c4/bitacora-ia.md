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
## Revisión de E1 (18/10/2026)
- **Herramienta:** Codex.
- **Solicitud de apoyo:** Revisar E1 respecto de la guía y los antecedentes de los Laboratorios 04 y 05, y corregir únicamente los errores encontrados.
- **Resultado y decisión:** Se conservan la estructura del inventario, el prompt original y los estilos del contexto. Se retira el proveedor externo de pagos, porque Puntos y Beneficios es un módulo interno. Se eliminan Celery y Redis del inventario por no estar respaldados por los ADR. Se corrigen las fuentes de la PWA, PostgreSQL y WhatsApp, y se omite la versión de PostgreSQL no acordada. El servicio de mapas valida coordenadas, la cobertura distrital corresponde al módulo Rutas y Cobertura. La indicación original de tres servicios externos se ajusta a los dos respaldados por el diseño previo.
- **Verificación:** Structurizr CLI v2025.11.09 ejecutó `validate -workspace docs/architecture/c4/workspace.dsl` con Java 23 y terminó sin errores, código de salida 0. El contexto conserva tres personas, el sistema principal, dos sistemas con etiqueta `Externo`, relaciones con intención, título y descripción. El registro anterior se conserva como antecedente de la propuesta inicial.
