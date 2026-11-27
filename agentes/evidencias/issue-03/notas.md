- Revisado: issues/ISSUE-03.md y mapa de src/lab10/operaciones.py. D02 da 30 en vez de 20. Hipótesis: los distritos comparten un diccionario de tarifas.
- Verificado en src/lab10/operaciones.py: dict.fromkeys compartía el mismo diccionario. Con una copia por distrito, la prueba del issue 3 pasa: D01 da 30 y D02 conserva 20.

## Comparación observada con E2

Según las trazas, E2 (issue 1) terminó en 8 decisiones y 6965 caracteres de contexto; E4 (issue 3) terminó en 11 decisiones y 6517 caracteres. En esta ejecución, E4 necesitó 3 decisiones más y terminó con 448 caracteres menos de contexto. Por tanto, no necesitó menos pasos, aunque sí registró menos caracteres de contexto. Como E2 y E4 resolvieron issues distintos, esta comparación describe las trazas observadas y no demuestra que la herramienta de mapa o la memoria hayan causado la diferencia.
