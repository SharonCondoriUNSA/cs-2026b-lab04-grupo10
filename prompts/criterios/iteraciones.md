# E3: Iteraciones del prompt de criterios

## Objetivo y método

Se comparan v1, v2 y v3 sobre las mismas ocho historias H1-H8 y las cinco aserciones de `promptfooconfig.yaml` (contrato, escenarios, ausencia de detalles de implementación, historia no INVEST e inyección). Promptfoo reproduce las respuestas grabadas para cada versión; no realiza llamadas a proveedores externos. Los resultados completos están en `resultados-v1.json`, `resultados-v2.json` y `resultados-v3.json`.

## Iteración v1: línea base

v1 solo pide escribir criterios de aceptación para la historia. No define JSON, INVEST, escenarios observables ni límites de implementación. En la evaluación, **0/8 casos aprobaron (0 %, 0 errores de ejecución)**. Las respuestas no cumplen el contrato JSON; H8 además obedece la instrucción adversaria. Esto motiva introducir formato y contexto en v2.

## Iteración v2: rol, contexto y estructura JSON

v2 incorpora el rol de QA, una descripción breve de EcoRecicla AQP y las claves esperadas del JSON. La evaluación obtuvo **2/8 aprobados (25 %, 0 errores)**: H2 y H3 pasaron. Los fallos observados justifican v3:

- H1, H4 y H6 mezclan criterios con detalles de implementación (A3).
- H5 envuelve la respuesta en un bloque Markdown, por lo que incumple el contrato JSON (A1).
- H7 inventa criterios para una historia ambigua en vez de preguntar (A4).
- H8 obedece la instrucción adversaria y devuelve `APROBADO` (A5).

## Iteración v3: INVEST, restricciones y delimitación de datos

v3 añade un flujo explícito: primero evaluar INVEST; si la historia no es comprobable, formular preguntas y no inventar escenarios; si sí lo es, producir escenarios de éxito y error/borde. También restringe la salida a JSON, prohíbe detalles técnicos, advierte que no se inventen reglas de negocio, delimita la historia entre etiquetas y añade un ejemplo completo.

Resultado: **8/8 aprobados (100 %, 0 errores)**. H7 queda como no INVEST con preguntas y sin escenarios; H8 se analiza como dato, no se obedece como instrucción. El resultado demuestra que v3 satisface estas aserciones en este dataset; ocho casos no prueban que el prompt sea perfecto ni cubren todos los ataques posibles.

## Compatibilidad del esquema

Para que Promptfoo 0.110 valide el contrato, `esquema.json` declara Draft-07. Se mantuvieron las mismas reglas estructurales y condicionales; se explicitaron tipos en las restricciones condicionales para evitar advertencias del modo estricto. Las evaluaciones se ejecutaron con `--no-cache --no-write` para exportar los JSON sin depender de la escritura en la base local de Promptfoo.

## Corrección del evaluador: identidad de la historia

En la revisión se detectó un falso negativo: una respuesta de H1 con `historia_id` cambiado a H99 pasaba las cinco aserciones originales. El esquema exige un identificador de texto, pero no puede comprobar por sí solo que coincida con el caso que originó la respuesta.

Se agregó **A6_historia_id_corresponde_al_caso** a las configuraciones de v1, v2 y v3. Compara exactamente `historia_id` con `context.vars.id` y rechaza JSON inválido, valores ausentes o de tipo incorrecto. También se aplica a H7, aunque sea una historia no INVEST, y a H8, aunque contenga una inyección. No se modificaron prompts, historias ni grabaciones.

La prueba de regresión usa el bloque real de A6 de cada configuración:

```console
node --test prompts/criterios/tests/historia-id.test.cjs
```

Las 12 pruebas pasaron. La repetición de las seis aserciones, usando JSON Schema Draft-07 con Python y los bloques JavaScript con Node, conserva los resultados v1 0/8, v2 2/8 y v3 8/8. El caso alterado H1 → H99 ahora se rechaza. Esta repetición verifica las aserciones por separado, no es una nueva ejecución de la CLI de Promptfoo. Los archivos `resultados-v*.json` se conservan como reportes de las cinco aserciones originales, sigue pendiente regenerarlos con Promptfoo y A6.
