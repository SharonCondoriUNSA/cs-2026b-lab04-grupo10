# E6: métricas y trade-off

**Fecha:** 25/10/2026. **Python:** 3.12.14. **Radon:** 6.0.1.

## Alcance y método

La línea base corresponde a los archivos que E1 midió con Radon: los servicios ingenuos de Solicitudes y Puntos/Beneficios en sus carpetas antes. Para la comparación posterior E1-E4 se midieron los módulos refactorizados de esos dos contextos, excluyendo las carpetas antes, los dobles externos de prueba y el dominio UML preexistente del Lab05. El componente de IA de E5 se informa aparte porque es funcionalidad nueva y no tiene equivalente en la línea base.

Radon Complexity (CC) cuenta bloques de clases, funciones y métodos. Por eso el promedio global no compara exactamente las mismas unidades: los patrones extraen el flujo en más bloques pequeños. El resultado completo por bloque de la versión final, incluidos los métodos de E5, está en [radon-despues.txt](radon-despues.txt); la medición de la línea base permanece en [radon-antes.txt](radon-antes.txt). SLOC corresponde al campo sloc de radon raw; no se cuentan pruebas.

## Resumen

| Versión / alcance | Bloques Radon | Complejidad promedio | SLOC | Interpretación |
| --- | ---: | ---: | ---: | --- |
| Antes, E1 | 17 | 5.12 (B) | 150 | Línea base de Solicitudes y Puntos/Beneficios. |
| Después, E1-E4 | 86 | 2.07 (A) | 300 | Refactor por patrones en los módulos medidos. |
| Componente nuevo, E5 | 28 | 2.11 (A) | 100 | Clasificador IA, sin contraparte antes. |
| Después acumulado, E1-E5 | 114 | 2.08 (A) | 400 | E1-E4 más el componente IA nuevo. |

## Complejidad de operaciones representativas

| Operación | Antes | Después de E1-E4 | Observación |
| --- | ---: | ---: | --- |
| ServicioSolicitudes.solicitar_recojo | 25 (D) | 15 (C) | Disminuye al delegar la consulta de mapas y separar la validación; todavía concentra varias validaciones del caso. |
| ServicioPuntos.acreditar | 9 (B) | 1 (A) | La selección de la regla sale del servicio; PuntosPorPeso.calcular tiene CC 7 (B), por lo que la lógica de cálculo se mantiene y no desaparece. |
| ServicioSolicitudes.asignar_reciclador | 5 (A) | 1 (A) | El servicio delega; Pendiente.asignar_reciclador tiene CC 3 (A). |
| ServicioSolicitudes.registrar_recojo | 4 (A) | 1 (A) | El servicio delega; Asignada.registrar_recojo tiene CC 2 (A). |
| ServicioSolicitudes.registrar_pesaje | 6 (B) | 1 (A) | El servicio delega; Recogida.registrar_pesaje tiene CC 4 (A). |
| ServicioSolicitudes.acreditar_puntos | 4 (A) | 2 (A) | Se conserva la coordinación con Puntos/Beneficios y el estado decide si la operación procede. |
| ServicioSolicitudes.__init__ | 5 (A) | 9 (B) | Aumenta por la configuración de adaptadores, publicador y dependencias opcionales. |

Las delegaciones distribuyen las decisiones entre servicio, entidad, estados y estrategias. Los valores de un método de servicio después del refactor no representan por sí solos la complejidad acumulada de todos los objetos que participan en el flujo; la tabla muestra esa distribución para evitar atribuir toda la reducción a una sola operación.

## SLOC por fuente

| Versión | Archivo | SLOC |
| --- | --- | ---: |
| Antes | src/solicitudes/antes/servicio.py | 132 |
| Antes | src/puntos_beneficios/antes/servicio.py | 18 |
| Después E1-E4 | src/solicitudes/servicio.py | 78 |
| Después E1-E4 | src/solicitudes/modelos.py | 30 |
| Después E1-E4 | src/solicitudes/estados.py | 72 |
| Después E1-E4 | src/solicitudes/mapas.py | 28 |
| Después E1-E4 | src/solicitudes/eventos.py | 38 |
| Después E1-E4 | src/solicitudes/decoradores.py | 14 |
| Después E1-E4 | src/puntos_beneficios/servicio.py | 9 |
| Después E1-E4 | src/puntos_beneficios/reglas.py | 31 |
| E5, adicional | src/solicitudes/ia.py | 100 |

## Trade-off (6 líneas)

- La complejidad de solicitar_recojo baja de 25 a 15, aunque sigue siendo el método más complejo del flujo.
- Strategy, Adapter, State, Observer y Decorator separan decisiones que antes estaban concentradas en los servicios.
- El costo es más código: el alcance refactorizado E1-E4 pasa de 150 a 300 SLOC; E5 agrega otros 100 SLOC.
- Hay más clases, interfaces y delegaciones que el equipo debe entender y mantener.
- El promedio Radon baja de 5.12 a 2.07 en E1-E4, pero parte del cambio se explica porque hay más bloques pequeños.
- La versión antes habría bastado para un prototipo pequeño, con pocos proveedores y reglas estables, sin previsión de incorporar variantes.

## Patrón no aplicado

Se rechazó **Abstract Factory**: los proveedores de mapas y las reglas de puntos varían de forma independiente y no forman familias de objetos que deban crearse juntas. El registro de constructores usado en E2 resuelve la selección con menos acoplamiento. También se descartó Singleton para evitar estado global y preservar la sustitución de dependencias en pruebas; estas razones coinciden con el análisis de olores de E1.

## Reproducción

Con Radon 6.0.1:

    radon cc -s -a src/solicitudes/antes src/puntos_beneficios/antes
    radon raw -s -j src/solicitudes/antes src/puntos_beneficios/antes

Para después E1-E4, se aplican los mismos subcomandos a los ocho archivos listados en la tabla SLOC, sin incluir ia.py. Para las métricas acumuladas E1-E5 se añade src/solicitudes/ia.py. Los archivos de antes se conservan para caracterización y comparación; no se incluyen en las cifras de después.
