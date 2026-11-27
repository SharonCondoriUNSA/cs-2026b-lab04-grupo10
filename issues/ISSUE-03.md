# ISSUE-03: cambiar la tarifa de D01 altera el cálculo de D02

## Procedencia

Error sembrado en TarifasDistritales del escenario src/lab10/operaciones.py.
El catálogo del Lab08 utiliza otra implementación y se conserva sin cambios.
Los distritos y las tarifas son sintéticos, no políticas municipales aprobadas.

## Observado

D01 y D02 parten con tarifa 10 para PLASTICO. Tras publicar tarifa 15 solo en
D01, calcular 2 kg en D02 devuelve 30 en vez de los 20 originales.

## Esperado

La actualización debe afectar solo al distrito y material indicados: D01 da 30,
D02 conserva 20 y PAPEL conserva su tarifa. El diccionario de tarifas recibido
por el constructor tampoco se modifica.

## Prueba que lo reproduce

python -m pytest tests/test_issue_03.py -q

Test: test_issue_03_actualizar_d01_no_cambia_los_puntos_de_d02.

## Aceptación y restricciones

La prueba pasa sin editarla, manteniendo ServicioPuntos y sus reglas existentes.
No introducir estado global ni modificar fitness/distritos.py. E4 resolverá el
issue con una herramienta nueva y notas persistentes, conservando la traza y
comparando sus pasos y contexto con E2, sin inventar una mejora.

## Resolución en E4

El ejecutor trabajó en una copia de E3 (`745aa66`). En la primera ejecución
de la prueba, D02 devolvió 30 puntos. El mapa obtenido con AST localizó los
métodos de `TarifasDistritales`. El agente anotó la hipótesis de un diccionario
compartido y buscó las líneas que crean, actualizan y consultan las tarifas.
El constructor usaba `dict.fromkeys` con un único diccionario para todos los
distritos. Ahora crea una copia por distrito. La misma prueba pasó y comprobó
que D01 otorga 30 puntos, D02 conserva 20 y la entrada del constructor y la
tarifa de PAPEL mantienen sus valores.

Las [notas de trabajo](../agentes/evidencias/issue-03/notas.md) conservan la
hipótesis inicial y la comprobación posterior. Las decisiones se ingresaron
por consola en `ModeloInteractivo` con apoyo de Codex. [Decisiones](../agentes/trayectorias/issue-03.json) · [Traza E4](../agentes/trazas/issue-03.jsonl) · [Diagrama](../agentes/trazas/issue-03.png)

### Comparación con E2

| Medida | E2 · Acreditación duplicada | E4 · Tarifas distritales |
|---|---:|---:|
| Decisiones, incluida la respuesta final | 8 | 11 |
| Acciones ejecutadas | 7 | 10 |
| Rechazos de contrato / bloqueos de política | 0 / 0 | 0 / 0 |
| Contexto final (caracteres del historial) | 6965 | 6517 |

E4 usó tres pasos más y terminó con 448 caracteres menos de contexto. Dos
escrituras y una lectura de notas ocuparon tres pasos. En E2 se leyeron dos
módulos completos. En E4 bastaron sus firmas y tres líneas de búsqueda para
localizar la causa. Cada ejecución resolvió un issue distinto, por lo que estas
cifras describen los dos recorridos y por sí solas no miden el efecto de la memoria.
[Traza E2](../agentes/trazas/issue-01.jsonl) · [Traza E4](../agentes/trazas/issue-03.jsonl)

### Reproducción

Desde la raíz del clon, con `requirements-lab10.txt` instalado y una carpeta
de salida nueva, ejecutar:

```console
python agentes/ejecutar_issue.py --issue 03 --salida ../e4-replay --reproducir agentes/trayectorias/issue-03.json
python agentes/agente/traza.py ../e4-replay/trazas/issue-03.jsonl
python -m pytest -q agentes/pruebas_agente tests/test_issue_01.py tests/test_issue_03.py
```

La reproducción crea la copia en `trabajo/`, con su propio `notas.md`.
Para una sesión interactiva, usar otra carpeta de salida y omitir
`--reproducir` junto con la ruta de la grabación.
