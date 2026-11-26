# ISSUE-02: la ruta conserva solicitudes canceladas

## Procedencia

Error sembrado del escenario aislado src/lab10/operaciones.py. El proyecto no
tenía un servicio de construcción de rutas implementado con este contrato.
Es un ejercicio de la tabla 14, no una incidencia reportada por usuarios reales.

## Observado

La ruta contiene SOL-01 ASIGNADA, SOL-02 CANCELADA y SOL-03 ASIGNADA. SOL-02
permanece incluida pese a su cancelación.

## Esperado

Excluir las solicitudes CANCELADA, conservar el orden relativo de las restantes
y no modificar la lista de entrada. Una lista vacía o solo de canceladas genera
una ruta vacía. No se añaden reglas sobre otros estados en este contrato.

## Prueba que lo reproduce

python -m pytest tests/test_issue_02.py -q

Test: test_issue_02_ruta_excluye_canceladas_y_conserva_orden.

## Aceptación y restricciones

La prueba pasa sin editarla. No consultar mapas ni servicios reales. E5 resolverá
este mismo estado inicial en dos copias independientes para comparar agente
único y actor-crítico. No reutilizar una copia ya corregida en la segunda variante.
