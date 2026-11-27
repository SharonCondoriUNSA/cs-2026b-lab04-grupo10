# E6: aprobación humana de ediciones

## Comportamiento

Cada decisión `editar_archivo` pasa por `Politica` y solicita aprobación en la
consola antes de ejecutar la sustitución. El mensaje muestra la ruta y los textos
anterior y propuesto para que la persona pueda revisar el cambio concreto. Solo
`s`, `si` o `sí` autoriza la edición. Una negativa, una respuesta ambigua, EOF o
una interrupción deniega la operación; en ese caso, `Agente` registra el bloqueo
y no ejecuta la herramienta.

La verificación de la ruta permitida ocurre antes de solicitar aprobación, por
lo que no se puede aprobar una edición fuera de `src/lab10/operaciones.py`. La
respuesta afirmativa queda registrada en la traza como `aprobacion`; los rechazos
aparecen como acciones `BLOQUEADO` con el motivo de política. Cada nueva edición
vuelve a pedir aprobación.

El cambio extiende el agente E5: el ejecutor del orquestador utiliza la misma
política con aprobación humana. El planificador no edita y el revisor conserva
permisos de solo lectura.

## Verificación

Comando ejecutado desde la raíz del repositorio:

```console
.venv-e5-temp/Scripts/python.exe -m pytest agentes/pruebas_agente/test_aprobacion.py agentes/pruebas_agente/test_agente.py -q
```

Resultado: **26 passed**. Las pruebas cubren aceptación, rechazo, respuestas
ambiguas, fin de entrada, petición en cada edición, bloqueo sin modificar el
archivo y registro de la aprobación concedida. También se comprobó la sintaxis
de los módulos y `git diff --check` no reportó errores.

## Operación desde consola

Al ejecutar un flujo que proponga una edición, revisar el archivo y ambos textos
mostrados. Responder `s` para permitir esa sustitución o cualquier otra respuesta
para bloquearla. La aprobación autoriza únicamente la edición concreta mostrada;
una propuesta posterior vuelve a requerir aprobación.
