# E4: iteraciones de la Tarea B

## Alcance

La Tarea B genera docstrings y documentación breve para funciones del caso EcoRecicla AQP. Se eligieron ocho funciones existentes en `src/solicitudes/dominio.py` y `src/puntos_beneficios/reglas.py`; los fragmentos de `casos.yaml` conservan sus firmas y cuerpos relevantes. Se evalúan funciones sin parámetros de entrada, métodos que cambian el estado y métodos con retorno, para comprobar que `self` no se documente como argumento.

| Caso | Función | Origen |
| --- | --- | --- |
| D1 | `coordenadas_validas` | `src/solicitudes/dominio.py` |
| D2 | `calcular_peso_estimado_kg` | `src/solicitudes/dominio.py` |
| D3 | `registrar_pendiente` | `src/solicitudes/dominio.py` |
| D4 | `asignar_reciclador` | `src/solicitudes/dominio.py` |
| D5 | `registrar_recojo` | `src/solicitudes/dominio.py` |
| D6 | `registrar_pesaje` | `src/solicitudes/dominio.py` |
| D7 | `acreditar` | `src/puntos_beneficios/servicio.py` |
| D8 | `calcular` | `src/puntos_beneficios/reglas.py` |

## Contrato y aserciones

`contrato.json` define una salida JSON con nombre, resumen, docstring, parámetros, retorno y excepciones. `casos.yaml` fija el nombre y la lista de parámetros esperados para cada función.

La evaluación aplica seis aserciones a cada caso:

| Aserción | Comprobación |
| --- | --- |
| A1 | La respuesta satisface el esquema JSON. |
| A2 | Los nombres del JSON y de la sección Args del docstring coinciden con los parámetros esperados, en orden, sin omisiones, duplicados, `self`/`cls` ni parámetros inexistentes. |
| A3 | Cada parámetro documentado tiene una descripción no vacía. |
| A4 | El docstring no usa cercas Markdown y contiene el resumen. |
| A5 | El nombre coincide exactamente con el de la función. |
| A6 | Distingue los métodos que no retornan un valor y los que sí lo hacen. |

A2 cubre el criterio central de la guía: documentar todos los parámetros y no describir parámetros inexistentes. Las otras cinco aserciones verifican formato, calidad mínima y coherencia con la función.

## Evolución de los prompts

| Versión | Cambio | Resultado local |
| --- | --- | --- |
| v1 | Solicitud abierta de docstring y documentación. | 0/8 casos aprobados; las respuestas de referencia no fuerzan JSON ni el inventario de argumentos. |
| v2 | Añade JSON, idioma español, exclusión de `self`/`cls` y campos de retorno/excepciones. | 8/8 aprobados; 0 errores de evaluación. |
| v3 | Hace explícito que la firma y el cuerpo son la fuente de verdad; exige correspondencia entre JSON y docstring y limita inferencias. | 8/8 aprobados; 0 errores de evaluación. |

v1 falla porque devuelve solo un docstring en texto libre y no puede satisfacer el contrato estructurado. v2 ya alcanza el 100 % en este conjunto. v3 conserva la tasa e incorpora instrucciones más estrictas para reducir inferencias no justificadas; en estos ocho casos no mejora la métrica frente a v2. Esta limitación queda visible en vez de atribuirle una mejora que los resultados no muestran.

## Ejecución reproducible

Desde esta carpeta, con Promptfoo 0.110.0:

```powershell
npx --yes promptfoo@0.110.0 eval --no-cache -c promptfooconfig-v1.yaml -o resultados-v1.json
npx --yes promptfoo@0.110.0 eval --no-cache -c promptfooconfig-v2.yaml -o resultados-v2.json
npx --yes promptfoo@0.110.0 eval --no-cache -c promptfooconfig-v3.yaml -o resultados-v3.json
```

v1 termina con estado distinto de cero porque las salidas libres no cumplen el contrato; v2 y v3 terminan correctamente. Las respuestas D1–D8 de cada versión fueron generadas por GPT en esta sesión aplicando el prompt correspondiente a cada fragmento y se guardaron sin edición posterior. El proveedor `proveedor_grabado.py` reproduce esas respuestas para que Promptfoo evalúe el mismo texto de forma determinista; no es una llamada en vivo durante `promptfoo eval`. La procedencia está registrada en cada `grabaciones/<versión>/ORIGEN.md`.

## Corrección de A2 durante la revisión

La aserción original verificaba los nombres en `parametros`, pero no los de `docstring`. Por ello, una respuesta de D4 podía conservar `reciclador_id` en el JSON e inventar `parametro_inexistente` dentro de Args sin que la evaluación detectara el error. Es un falso negativo del evaluador, no un cambio de la respuesta grabada.

Se corrigió A2 en las tres versiones para verificar ambos lugares. Se exige una sola sección Args cuando hay parámetros y ninguna en los métodos sin parámetros de entrada. Los nombres deben coincidir exactamente con la lista esperada. Se aceptan tipos entre paréntesis y descripciones continuadas con mayor sangría, siguiendo el estilo usado en estas grabaciones. Esta comprobación se limita a ese formato, no analiza todos los estilos posibles de docstrings ni garantiza la veracidad semántica de cada descripción.

```console
node --test prompts/docstrings/tests/parametros-docstring.test.cjs
```

Las 21 pruebas de regresión pasaron, incluyendo parámetros inventados, omitidos, duplicados, orden incorrecto, self, secciones duplicadas y descripciones vacías, además de respuestas válidas y descripciones multilínea. La repetición con JSON Schema en Python y las aserciones JavaScript en Node conserva las tasas v1 0/8, v2 8/8 y v3 8/8. No es una ejecución completa de Promptfoo. Los reportes `resultados-v*.json` se conservan como evidencia histórica anterior a esta corrección y deben regenerarse con la CLI cuando esté disponible. No se modificaron los prompts ni las grabaciones.
