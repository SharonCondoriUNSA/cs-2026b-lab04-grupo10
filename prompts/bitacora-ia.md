# Bitácora de apoyo con IA · Lab09

## E5 · Ataques y defensas de los prompts · 2026-11-15

Herramienta: Codex, en esta conversación. Solicitud de apoyo: desarrollar E5 para EcoRecicla AQP, tomando la guía y los recursos de AgroConecta como referencia y conservando los entregables de la compañera.

Se diseñaron seis ataques y dos controles normales para las tareas de criterios y docstrings. Se añadieron prompts v3.1 con límites explícitos de confianza, datos serializados, formato, idioma, no revelación y ausencia de ejecución de acciones. Las expectativas se escribieron antes de guardar las respuestas.

Las 16 respuestas se produjeron por lotes en esta conversación, con el caso y el objetivo defensivo ya conocidos por el asistente. Se guardaron una vez y se calcularon sus huellas. No se presentan como llamadas aisladas, muestras independientes ni un experimento ciego. La procedencia y sus límites están en seguridad/grabaciones/ORIGEN.md.

Se ejecutaron las cuatro evaluaciones reales de Promptfoo 0.110.0 mediante el proveedor grabado. Cada reporte aprobó 4/4 casos y tuvo 0 errores. En conjunto, los seis ataques y dos controles aprobaron antes y después. No se atribuye una mejora cuantitativa a v3.1, no se fabricaron fallos de v3 ni se editaron grabaciones para cambiar la tasa.

Las seis pruebas de regresión de E5 pasaron. Se comprobó que el proveedor reproduce el texto sin transformarlo y rechaza combinaciones y rutas no permitidas. Los controles negativos sintéticos se usan para comprobar las aserciones, no se confunden con salidas reales de un modelo. La revisión humana del PR y la ampliación del ensayo con muestras aisladas permanecen pendientes.

Esta entrada registra el trabajo de E5, no da por completadas las cinco interacciones, la evaluación de no determinismo o el workflow que exige E7.


## E6 · Integración mediante ProveedorLLM · 2026-11-15

Solicitud de apoyo: implementar generadores con plantillas versionadas, reutilizando el puerto del Lab07, validar las respuestas con JSON Schema y probar aceptación y rechazo con proveedores grabados. Se añadieron GeneradorCriterios, GeneradorDocstrings y el cargador común PlantillaJSON, conservando ProveedorLLM y el código de clasificación existente.

La integración exige identidad de historia, nombre de función y correspondencia de parámetros en JSON y Args. Serializa los datos de v3.1 y sustituye las variables una sola vez. Analiza firmas con AST sin ejecutar el cuerpo y rechaza JSON inválido o duplicado, versiones no permitidas y entradas fuera de los límites documentados. Las respuestas no se reparan ni se aplican automáticamente al código o al dominio.

Las 16 pruebas nuevas usan grabaciones de solo lectura para ambas tareas y mutaciones sintéticas en memoria para verificar rechazos. También comprueban carga desde otro directorio y ausencia de ejecución del código de entrada. La verificación conjunta obtuvo 163 pruebas aprobadas, con 12 subpruebas aprobadas, y los dos contratos de Import Linter quedaron KEPT. Las dependencias y comandos se registran en requirements-lab09.txt y prompts/integracion.md. No se utilizó un LLM en vivo ni se presentó esta comprobación como garantía de exactitud semántica.


## E3 · Apoyo en identidad de la historia · 2026-11-15

Solicitud: corregir el primer error de los evaluadores detectado en la revisión de los PR de la compañera. Se agregó A6 a las tres configuraciones para comparar historia_id con el caso. La regresión cambió H1 a H99 solo en memoria y comprobó su rechazo, sin editar grabaciones. Las 12 pruebas Node pasaron. Se mantuvieron las tasas de las respuestas originales y se documentó la diferencia entre reforzar un evaluador y mejorar el prompt. Evidencia: criterios/iteraciones.md y criterios/tests/historia-id.test.cjs.

## E4 · Apoyo en correspondencia de parámetros y propuesta rechazada · 2026-11-15

Solicitud: corregir la aserción que solo revisaba parametros en JSON y dejaba pasar argumentos inventados dentro del docstring. Se extendió A2 a Args en v1–v3 y se comprobaron omisiones, duplicados, self, orden y secciones repetidas. Se rechazó la primera propuesta estricta de validación generada en esta sesión, que exigía una descripción en la misma línea del parámetro, porque rechazaba documentación multilínea válida. El control sintético de evidencia-rechazo-evaluador.json muestra falso rechazo con esa alternativa y aceptación con el evaluador corregido. No es una salida supuestamente producida por un LLM. Las 21 pruebas pasaron.

## Apoyo en reproducción de evaluaciones E3 y E4 · 2026-11-15

Solicitud: completar la ejecución real de Promptfoo tras corregir los evaluadores. La instalación inicial falló en una dependencia SQLite. Se preparó la herramienta fuera del repositorio y se usó la exportación --no-cache --no-write con el Python del proveedor grabado. Se regeneraron seis reportes reales, todos con 0 errores de ejecución. Criterios mantuvo 0/8, 2/8 y 8/8, docstrings 0/8, 8/8 y 8/8. Se verificaron 48 huellas de las grabaciones de E1–E4 y 33 pruebas de regresión. No se confundió la reproducción de archivos con nuevas consultas al modelo.

## E7 · Apoyo en CI y preparación del no determinismo · 2026-11-15

Solicitud: ejecutar las evaluaciones grabadas en cada PR, completar el registro de interacciones reales y comparar tres repeticiones de tres casos. Se preparó prompts.yml con permisos de lectura y sin secretos, pruebas de evaluadores, integración y seguridad, y diez evaluaciones de Promptfoo. El ejecutor trata los fallos esperados de v1/v2 como línea base y exige 0 errores de ejecución y las tasas revisadas. También conserva reportes como artefactos.

Para el no determinismo se prepararon tres entradas exactas, H1, H7 y H8, con sus hashes. El acceso automatizado a Edge se detuvo por no poder identificar con confianza la URL, no se enviaron consultas por esa herramienta. La usuaria indicó que utiliza ChatGPT y se solicitaron nueve respuestas nuevas sin corregir, manteniendo el mismo modelo. La comparación y reflexión siguen pendientes de recibirlas. No se crearon respuestas ni conclusiones ficticias para completar ese requisito. Las entradas y el procedimiento están en no-determinismo/README.md.

El registro reúne seis interacciones de apoyo de esta conversación, incluidas E5 y E6. Completar su número no implica que el requisito de no determinismo ya esté realizado ni que el workflow remoto ya haya pasado.


Verificación local del ejecutor de CI completada el 2026-11-16: diez evaluaciones reales y 64 casos procesados con las tasas de referencia y cero errores de ejecución. Las seis pruebas del ejecutor pasaron y el comparador confirmó que faltan las nueve respuestas nuevas, sin producir un archivo de resultados ficticio. La publicación y ejecución remota del workflow siguen pendientes.


## E7 · Apoyo en comparación de respuestas recibidas · 2026-11-16

La usuaria compartió las respuestas de ChatGPT y confirmó que el cuarto H1 era un duplicado al pegar. Se conservaron nueve bloques y se registró la modalidad visible «Instantánea», sin inventar una versión de modelo. La fecha registrada es la de recepción. Solo se decodifican escapes de presentación del chat para analizar JSON, sin modificar los textos conservados ni corregir las respuestas.

El comparador obtuvo tres variantes de JSON para H1, tres para H7 y dos para H8. Las nueve respuestas cumplen esquema e identidad, pero solo cuatro coinciden con la decisión INVEST esperada del dataset. H8 alterna entre true y false. Se documentaron estas discrepancias, los límites del contexto no verificado y una reflexión de cinco líneas. No se ajustaron expectativas ni grabaciones para producir una tasa superior. La comprobación remota de CI continúa pendiente de publicación.


Aclaración de procedencia del 2026-11-16: la usuaria confirmó que el modelo utilizado fue GPT-6 Instant. Se actualizó el nombre inicialmente no identificado en los metadatos, la comparación y su documentación. No se modificaron las nueve respuestas ni sus resultados, y la temperatura sigue sin conocerse.


## E7 · Apoyo en compatibilidad de CI · 2026-11-16

El registro real de Actions mostró que test_grabaciones_originales_se_conservan fallaba en Linux por la conversión automática CRLF/LF de Git. Se añadieron atributos para conservar los bytes originales de las 16 grabaciones de E5 y se comprobaron contra las huellas existentes, sin cambiar contenido, expectativas o hashes. Se habilitó además la carga de la carpeta oculta de reportes como artefacto. La comprobación de integridad permanece activa.


## E8 · Apoyo en documentación de resultados y cierre · 2026-11-16

Solicitud: preparar E8 en una rama propia siguiendo la guía y los recursos de AgroConecta. Se añadió la sección Prompt engineering (Lab 09), con tasas de los seis reportes reales y un gráfico generado desde esos JSON. Se distinguieron los datasets principales, el red teaming y la comparación de no determinismo para evitar presentar medidas diferentes como una sola tasa.

Se enlazaron contratos, integración, bitácora, CI y la lista del Paso 9 para revisión por pares. La etiqueta y la entrega se registran pendientes, sin inventar aprobaciones, integración final o cumplimiento del plazo. El script del gráfico requiere Matplotlib únicamente para regenerar documentación. No se modificaron prompts, grabaciones ni expectativas.
