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
| A2 | Documenta todos los parámetros de la firma, en orden, sin `self`/`cls` ni parámetros inexistentes. |
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
