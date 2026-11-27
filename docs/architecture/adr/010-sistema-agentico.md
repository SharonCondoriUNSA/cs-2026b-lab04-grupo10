# ADR-010: Arquitectura del sistema agéntico de EcoRecicla AQP

**Estado:** Propuesto para revisión del equipo
**Fecha:** 2026-11-26
**Decisores:** Equipo de desarrollo Grupo 10

## Contexto

En el Lab 10 se construyó un agente para atender issues acotados de EcoRecicla AQP. El flujo debe consultar el repositorio, proponer cambios, ejecutar verificaciones y dejar evidencia reproducible. Una edición incorrecta podría modificar archivos fuera del alcance o integrarse sin revisión; por ello, la autonomía debe limitarse con contratos, política, herramientas permitidas y aprobación humana.

El prototipo incluye un agente ReAct de un solo rol, una variante actor-crítico con planificador, ejecutor y revisor, y una variante con memoria de repositorio. E6 añade aprobación explícita antes de cada edición. Las ejecuciones se registran en trazas JSONL. Las evidencias no acreditan despliegue autónomo ni integración automática.

## Alternativas consideradas

1. **Agente único sin herramientas controladas:** simple, pero no permite verificar las acciones ni limitar de forma efectiva sus efectos.
2. **Agente ReAct con herramientas y política:** conserva un ciclo sencillo y auditable, aunque concentra planificación, ejecución y revisión en un rol.
3. **Orquestación de varios roles con herramientas y política compartidas:** separa planificación, ejecución y revisión, a cambio de más pasos, contexto y coordinación.
4. **Automatización que publica e integra cambios:** reduce intervención manual, pero excede la evidencia y los controles implementados en el laboratorio.

## Decisión

Usaremos un agente basado en el ciclo **decidir → validar contrato → evaluar política → ejecutar o bloquear → observar**, que continúa hasta una respuesta final o hasta alcanzar el límite de pasos. El modelo se abstrae detrás de una interfaz; las herramientas se exponen mediante un catálogo y operan sobre una copia de trabajo.

Para tareas que requieren coordinación, el orquestador distribuye el trabajo entre planificador, ejecutor y revisor. La memoria de repositorio es una capacidad adicional del conjunto de herramientas, no una autorización para ampliar el acceso.

La política mantiene una lista de herramientas y un límite de pasos. En la configuración E6, solo se permite editar `src/lab10/operaciones.py`, y cada edición requiere que una persona apruebe el reemplazo exacto en consola. Las pruebas permitidas y la vista del diff apoyan la verificación. La aprobación humana del cambio, publicación del Pull Request e integración continúan bajo responsabilidad del equipo.

## Evidencia y alcance

- El [diagrama de estados](../../../agentes/diseno/estados.png) representa el ciclo del agente y sus estados finales.
- Las [trazas de E2, E4 y E5](../../../agentes/trazas/) conservan ejecuciones de los issues 1, 2 y 3; las métricas derivadas se resumen en [`agentes/observacion.md`](../../../agentes/observacion.md).
- E5 compara el agente único y la variante actor-crítico para el issue 2. La ejecución coordinada registró una ronda y la aprobación del revisor; el análisis de E7 informa mayor número de pasos y contexto que en la variante única, sin una mejora observada en ese issue acotado.
- E6 prueba la solicitud de aprobación, el rechazo, entradas inválidas, EOF y el bloqueo sin modificar el archivo. Estas pruebas no equivalen a una sesión interactiva real revisada por una integrante.

## Consecuencias

### Positivas

- Las decisiones, acciones y observaciones quedan trazadas para inspección.
- Los contratos y la política rechazan decisiones inválidas, herramientas no permitidas y ediciones fuera de la ruta autorizada.
- Cada edición requiere una aprobación explícita; el sistema deniega por defecto ante rechazo o falta de respuesta válida.
- La coordinación por roles y la memoria se pueden evaluar manteniendo una política común.

### Riesgos y límites

- Una traza correcta no demuestra que el modelo responderá correctamente en casos futuros.
- La variante actor-crítico puede aumentar pasos y contexto sin mejorar el resultado de una tarea pequeña.
- Las pruebas de aprobación verifican el mecanismo, pero no acreditan por sí solas una revisión humana de cada ejecución real.
- El prototipo trabaja en un entorno local controlado; no tiene autorización para red, credenciales, `git push` ni `git merge`.
- El equipo debe revisar el diff y las pruebas antes de aceptar cualquier cambio.

## Relación con otros entregables

La arquitectura se implementa en [`agentes/agente/`](../../../agentes/agente/), se coordina en [`agentes/orquestador.py`](../../../agentes/orquestador.py) y se describe junto con la delegación progresiva en [`agentes/delegacion.md`](../../../agentes/delegacion.md). La máquina de estados, las ejecuciones y la observación se enlazan desde la sección [Sistemas agénticos (Lab 10)](../../../README.md#sistemas-agénticos-lab-10) del README.
