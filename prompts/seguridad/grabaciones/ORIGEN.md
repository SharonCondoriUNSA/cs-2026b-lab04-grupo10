# Procedencia y alcance de las respuestas E5

Las 16 respuestas de `antes/` y `despues/` fueron producidas y guardadas por el asistente Codex en esta conversación al preparar E5. Se usaron las tareas, ataques y controles de los dos datasets, con v3 como referencia y v3.1 como defensa ampliada. Se conservaron como texto JSON desde su primera escritura, no se corrigieron para obtener aprobaciones. `huellas.json` permite comprobarlo.

Se trata de una generación asistida por lotes dentro de una conversación que ya conoce el caso y la finalidad defensiva del ejercicio. No son llamadas aisladas a un modelo mediante API, no se controló temperatura ni se midió variabilidad entre conversaciones. Las dos fases son propuestas de respuesta producidas en ese contexto, no dos experimentos independientes ni evidencia causal de que v3.1 sea superior.

Promptfoo únicamente reproduce esos textos y ejecuta las aserciones, no vuelve a consultar al asistente. No se inventó una vulnerabilidad ni se degradaron respuestas de la fase anterior para mostrar una mejora. Los ataques ensayados no obtuvieron la salida impuesta en ninguna de las fases. La revisión humana del PR sigue pendiente.

Las entradas usan historias, funciones y marcas sintéticas. E5_MARCADOR_INTERNO_SINTETICO es una marca de prueba, no una credencial real. No se incluyeron datos personales ni claves de servicios.
