# ISSUE-01: un reintento duplica los puntos acreditados

## Procedencia

Error sembrado para E1 del Lab10, según el caso EcoRecicla de la tabla 14 de la
guía v2. Solo afecta al escenario aislado src/lab10/operaciones.py. No se afirma
que el servicio original de Lab07 tenga un saldo duplicado demostrado.

## Observado

Acreditar dos veces SOL-01, PLASTICO, 2 kg y tarifa sintética 10 deja saldo 40
y dos movimientos, aunque las dos respuestas tienen el mismo identificador.

## Esperado

El reintento idéntico de una solicitud ya acreditada conserva saldo 20 y un
movimiento, devolviendo el resultado anterior. Una solicitud distinta suma sus
puntos normalmente. No basta con repetir el identificador de la respuesta.

## Prueba que lo reproduce

python -m pytest tests/test_issue_01.py -q

Test: test_issue_01_reintentar_acreditacion_no_duplica_saldo.

## Aceptación y restricciones

La prueba pasa sin modificarla ni cambiar la tarifa o el resultado esperado.
Mantener el cálculo original de ServicioPuntos. No usar una API, persistencia
real ni estado global. E2 registra el diagnóstico, edición y verificación del
agente. No se considera resuelto en E1.
