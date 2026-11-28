# E6: aprobación humana de ediciones

## Comportamiento

Cada decisión `editar_archivo` pasa por `Politica` y solicita aprobación en la
consola antes de ejecutar la sustitución. El mensaje muestra la ruta y los textos
anterior y propuesto para que la persona pueda revisar el cambio concreto. Solo
`s` y `n` son respuestas válidas; una entrada ambigua vuelve a solicitarse. EOF
o una interrupción deniega la operación; en ese caso, `Agente` registra el
bloqueo y no ejecuta la herramienta.

La verificación de la ruta permitida ocurre antes de solicitar aprobación, por
lo que no se puede aprobar una edición fuera de `src/lab10/operaciones.py`. La
respuesta afirmativa queda registrada en la traza como `aprobacion`; los rechazos
aparecen como acciones `BLOQUEADO` con el motivo de política. Cada nueva edición
vuelve a pedir aprobación.

El cambio extiende el agente E5: el ejecutor del orquestador utiliza la misma
política con aprobación humana. El planificador no edita y el revisor conserva
permisos de solo lectura. La hoja de ruta de cuatro etapas está en
[`delegacion.md`](../delegacion.md).

## Verificación

Comando ejecutado desde la raíz del repositorio:

```console
.venv-e5-temp/Scripts/python.exe -m pytest agentes/pruebas_agente/test_aprobacion.py agentes/pruebas_agente/test_agente.py -q
```

Tras incorporar los dos casos de reproducción, el comando obtuvo **28 passed**.
Las pruebas cubren aceptación, rechazo, reintento ante
respuesta inválida, fin de entrada, petición en cada edición, bloqueo sin
modificar el archivo y registro de la aprobación concedida.

## Operación desde consola

Al ejecutar un flujo que proponga una edición, revisar el archivo y ambos textos
mostrados. Responder `s` para permitir esa sustitución o `n` para rechazarla. Una
entrada distinta vuelve a solicitarse. La aprobación autoriza únicamente la
edición concreta mostrada; una propuesta posterior vuelve a requerir aprobación.

El comando de reproducción de los issues 1 y 3 comprueba la última prueba
ejecutada sobre la copia final antes de anunciar la resolución. Si se rechaza
la sustitución y la prueba continúa en rojo, informa que el issue queda
pendiente y devuelve un código de salida distinto de cero. La traza conserva
la respuesta original del modelo y el resultado observado de la prueba.
