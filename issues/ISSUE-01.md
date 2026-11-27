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

## Resolución en E2

El ejecutor trabajó en una copia de los archivos del issue del commit E1
(43e5f70). Se usó el mini framework de AgroConecta v2 del laboratorio, adaptado
a EcoRecicla. Codex respondió por consola a ModeloInteractivo, una decisión por
observación. El contrato aceptó las ocho decisiones: siete acciones y una
respuesta final. La política registró cero bloqueos. El historial final sumó
6965 caracteres de contenido de los mensajes.

La primera ejecución de la prueba mostró un saldo de 40 en vez de 20. El cambio
en LibroPuntos.acreditar devuelve una copia del movimiento anterior cuando el
servicio ya emitió ese identificador. En la segunda ejecución, la misma prueba
verificó el saldo de 20 tras el reintento y de 50 tras una solicitud distinta.

[Decisiones](../agentes/trayectorias/issue-01.json) ·
[Traza de ejecución](../agentes/trazas/issue-01.jsonl) ·
[Diagrama Mermaid](../agentes/trazas/issue-01.mmd) ·
[Diagrama en PNG](../agentes/trazas/issue-01.png)

### Cómo reproducirlo

Desde la raíz de un clon que incluya el commit E1, con las dependencias de
requirements-lab10.txt instaladas, ejecutar:

```console
python agentes/issue_01.py --salida ../e2-replay --reproducir agentes/trayectorias/issue-01.json
python agentes/agente/traza.py ../e2-replay/trazas/issue-01.jsonl
python -m pytest -q tests/test_issue_01.py agentes/pruebas_agente
```

Usar un directorio de salida nuevo en cada ejecución. La primera orden crea la
copia en trabajo/ y vuelve a ejecutar las herramientas con las decisiones
grabadas. La segunda genera el diagrama a partir de la nueva traza. Para iniciar
una sesión interactiva, ejecutar la primera orden sin la opción --reproducir ni
su archivo e ingresar una respuesta JSON por turno.
