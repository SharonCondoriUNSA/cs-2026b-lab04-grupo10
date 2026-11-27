# E6: delegación progresiva en EcoRecicla AQP

La autonomía se aumenta por evidencia y de forma gradual. La persona conserva la
aprobación del Pull Request y la integración; ningún nivel concede acceso a
credenciales, servicios reales, red, `git push` ni `git merge`. Las etapas
describen cómo cambia la supervisión humana, no permisos para modificar el
dominio fuera del sandbox.

| Rol humano | Permisos del agente en EcoRecicla | Evidencia para pasar a la siguiente etapa |
|---|---|---|
| **Ejecutor** | Solo lectura y diagnóstico. El agente puede listar, buscar y leer el issue, el código y las pruebas; presenta una propuesta. La persona aplica los cambios. | Trazas reproducibles de los issues 1, 2 y 3; cada diagnóstico identifica la causa; las pruebas objetivas distinguen el estado inicial del esperado. No basta una respuesta final del modelo. |
| **Revisor** | Puede editar únicamente `src/lab10/operaciones.py` en una copia de trabajo. `Politica` muestra el reemplazo exacto y exige `s` o `n` antes de **cada** edición. Puede ejecutar las pruebas permitidas y mostrar el diff; no puede editar pruebas ni integrar cambios. **Esta es la etapa implementada en E6.** | Trazas con las aprobaciones o denegaciones de cada edición; entradas distintas de `s`/`n` rechazadas; pruebas de los tres issues aprobadas después de cada corrección; diff dentro del archivo permitido; revisión humana del resultado. E6 prueba el mecanismo, pero aún no aporta una sesión interactiva real del equipo, por lo que no se declara superada esta etapa. |
| **Colaborador** | Tras evidencia suficiente, podría proponer y aplicar varios cambios de bajo riesgo dentro de una rama o copia aislada, ejecutar pruebas y preparar un diff. Mantiene aprobación humana previa para cada edición y no puede publicar ni fusionar. | Varias ejecuciones reales revisadas por una integrante, todas con aprobación registrada, suite relevante en verde, cero ediciones fuera del alcance y sin regresiones. Una prueba fallida debe detener la promoción hasta explicar y corregir su causa. |
| **Gobernador** | La persona define objetivo, rutas permitidas, presupuesto y pruebas. El agente podría planificar tareas y ejecutar las herramientas autorizadas en una rama aislada. Se mantienen prohibidos secretos, red, publicación y merge; una persona revisa y aprueba el PR. | Evidencia repetida de trazas completas, cumplimiento de límites, pruebas en verde y revisión de seguridad de herramientas y rutas. La promoción requiere acuerdo del equipo; una sola tarea exitosa no la justifica. |

## Estado actual y evidencias

El sistema conserva supervisión humana en el nivel **Revisor**: la edición se
solicita en consola y la política deniega la operación por defecto si la persona
no responde válidamente. Las pruebas de E6 verifican `s`, `n`, entradas inválidas,
EOF, bloqueo sin modificación del archivo y registro de aprobación. Las trazas de
E2, E4 y E5 muestran resultados de los tres issues, pero preceden a la aprobación
interactiva; no se usan como evidencia de aprobaciones humanas reales. Por ello,
el equipo no se atribuye todavía autonomía de Colaborador o Gobernador.

Evidencia relacionada: [traza de issue 1](trazas/issue-01.jsonl), [traza del
agente único en issue 2](trazas/issue-02-unico.jsonl), [traza coordinada de issue
2](trazas/issue-02-orquestado.jsonl), [traza de issue 3](trazas/issue-03.jsonl) y
[pruebas de aprobación](pruebas_agente/test_aprobacion.py).
