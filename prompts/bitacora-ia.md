# Bitácora de apoyo con IA · Lab09

## E5 · Ataques y defensas de los prompts · 2026-11-15

Herramienta: Codex, en esta conversación. Solicitud de apoyo: desarrollar E5 para EcoRecicla AQP, tomando la guía y los recursos de AgroConecta como referencia y conservando los entregables de la compañera.

Se diseñaron seis ataques y dos controles normales para las tareas de criterios y docstrings. Se añadieron prompts v3.1 con límites explícitos de confianza, datos serializados, formato, idioma, no revelación y ausencia de ejecución de acciones. Las expectativas se escribieron antes de guardar las respuestas.

Las 16 respuestas se produjeron por lotes en esta conversación, con el caso y el objetivo defensivo ya conocidos por el asistente. Se guardaron una vez y se calcularon sus huellas. No se presentan como llamadas aisladas, muestras independientes ni un experimento ciego. La procedencia y sus límites están en seguridad/grabaciones/ORIGEN.md.

Se ejecutaron las cuatro evaluaciones reales de Promptfoo 0.110.0 mediante el proveedor grabado. Cada reporte aprobó 4/4 casos y tuvo 0 errores. En conjunto, los seis ataques y dos controles aprobaron antes y después. No se atribuye una mejora cuantitativa a v3.1, no se fabricaron fallos de v3 ni se editaron grabaciones para cambiar la tasa.

Las seis pruebas de regresión de E5 pasaron. Se comprobó que el proveedor reproduce el texto sin transformarlo y rechaza combinaciones y rutas no permitidas. Los controles negativos sintéticos se usan para comprobar las aserciones, no se confunden con salidas reales de un modelo. La revisión humana del PR y la ampliación del ensayo con muestras aisladas permanecen pendientes.

Esta entrada registra el trabajo de E5, no da por completadas las cinco interacciones, la evaluación de no determinismo o el workflow que exige E7.
