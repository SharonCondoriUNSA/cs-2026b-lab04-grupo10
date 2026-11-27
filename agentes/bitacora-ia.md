# E7: bitácora de apoyo con IA

Las solicitudes se resumen fielmente de las interacciones de trabajo del equipo
con GPT durante el 26/11/2026. Las verificaciones distinguen las propuestas del
asistente de los resultados realmente obtenidos en las copias del repositorio.

## Interacción 1 — Preparación de E5

- **Fecha:** 26/11/2026
- **Herramienta:** GPT
- **Prompt (resumen fiel):** “Prepara E5 localmente, siguiendo la guía, sobre el issue 2 y con ramas; no lo publiques.”
- **Propuesta:** Comparar agente único con planificador–ejecutor–revisor en copias independientes, guardar trayectorias y métricas.
- **Verificación:** La prueba del issue 2 falló en el estado inicial porque incluía SOL-02 CANCELADA y pasó después de aplicar el filtro; la variante coordinada también pasó.
- **Decisión:** Aceptar la estructura y conservar la procedencia de las trayectorias: se reprodujeron con `ModeloGrabado`, sin llamada API en vivo.

## Interacción 2 — Reproducción local de E5

- **Fecha:** 26/11/2026
- **Herramienta:** GPT
- **Prompt (resumen fiel):** “¿Qué comando ejecuto desde CMD para generar las evidencias de E5?”
- **Propuesta:** Ejecutar `agentes/ejecutar_issue_02.py` con el Python del entorno que contiene pytest.
- **Verificación:** La primera ejecución con Python global informó que no encontraba `pytest`; al usar `.venv-e5-temp`, las pruebas pasaron y la salida coincidió con las métricas registradas.
- **Decisión:** Usar el entorno del proyecto y no reportar el primer error de dependencia como fallo del código.

## Interacción 3 — Base del PR de E5

- **Fecha:** 26/11/2026
- **Herramienta:** GPT
- **Prompt (resumen fiel):** “¿Está bien que el PR de E5 tenga `main` como base?”
- **Propuesta:** Base `main`, compare `lab10-e5-coordinacion`.
- **Verificación:** La captura de GitHub mostró el PR de E5 hacia `main`; E1–E4 ya estaban integrados allí.
- **Decisión:** Mantener `main` como base para E5.

## Interacción 4 — Aprobación humana y omisión de E6

- **Fecha:** 26/11/2026
- **Herramienta:** GPT
- **Prompt (resumen fiel):** “Prepara E6 y luego E7 en ramas locales; revisa si E7 debe depender de E6.”
- **Propuesta inicial:** Activar aprobación en consola y documentar las pruebas de E6.
- **Error detectado por revisión de la guía:** La primera preparación de E6 omitió `delegacion.md` y aceptaba `si`/`sí`, aunque la guía pide los cuatro roles y validar solo `s` o `n`.
- **Verificación y corrección:** Se releyó E6 de la guía; se añadió la hoja de delegación, se restringió la entrada a `s`/`n` y las pruebas de aprobación y agente terminaron con **26 passed**.
- **Decisión:** Actualizar la misma rama E6 y su PR antes de usarla como base de E7. Esta omisión fue una falla del apoyo de GPT detectada en la revisión contra la guía.

## Interacción 5 — Dependencia de E7

- **Fecha:** 26/11/2026
- **Herramienta:** GPT
- **Prompt (resumen fiel):** “¿E7 también tiene que ser creciente o depende del contenido?”
- **Propuesta:** Comprobar la Tabla 13 y los requisitos de E7 antes de elegir la base.
- **Verificación:** E7 requiere las métricas de las trazas de los tres issues, que están en E2, E4 y E5; el trabajo está organizado en ramas propias y E7 conserva el E6 corregido en la secuencia del equipo.
- **Decisión:** Crear `lab10-e7-observacion-bitacora` desde `lab10-e6-aprobacion-humana`; no inferir dependencias solo por el número del entregable.

## Interacción 6 — Métricas y errores observados

- **Fecha:** 26/11/2026
- **Herramienta:** GPT
- **Prompt (resumen fiel):** “Prepara E7 con la tabla de métricas de los tres issues, el diagrama de una trayectoria y cinco o más interacciones.”
- **Propuesta:** Contar pasos, rondas, herramientas, rechazos de contrato, bloqueos y contexto final directamente de los JSONL; incluir el diagrama coordinado de E5.
- **Verificación:** Se contrastaron las cuentas con eventos de E2, E4 y ambas variantes de E5. Las pruebas detectaron los defectos iniciales de los tres issues antes de que cada ejecución los corrigiera.
- **Decisión:** Incluir los datos de las cuatro ejecuciones (issue 2 aparece dos veces) y aclarar que esos fallos iniciales eran los defectos sembrados del sistema, no fallos posteriores de las correcciones.
