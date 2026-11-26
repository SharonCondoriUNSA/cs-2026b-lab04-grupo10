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
