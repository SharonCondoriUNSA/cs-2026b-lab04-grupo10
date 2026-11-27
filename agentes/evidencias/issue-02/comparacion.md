# E5: comparación de coordinación para ISSUE-02

## Protocolo y procedencia

Las dos variantes partieron de copias independientes de `d9156e1`. La variante única usa un agente con hasta 12 decisiones. La coordinada usa planificador sin herramientas, ejecutor y revisor de solo lectura. El máximo es de dos rondas. Las decisiones proceden de las trayectorias de E5 preparadas con apoyo de GPT y reproducidas con `ModeloGrabado`. Las herramientas operan en copias de trabajo.

## Resultados

| Medida | Agente único | Planificador–ejecutor–revisor |
|---|---:|---:|
| Rondas actor-crítico | No aplica | 1 de 2 |
| Decisiones registradas | 8 | 13 |
| Acciones ejecutadas / bloqueadas | 7 / 0 | 10 / 0 |
| Contexto final (caracteres) | 6511 | 10796 acumulados entre roles |
| Fallo inicial reproducido | sí | sí |
| Última verificación de la copia | pasó | pasó |
| Veredicto y hallazgos del revisor | No aplica | APROBADO. Evidencia: el diff solo modifica preparar_ruta, excluye CANCELADA mediante una lista nueva y la prueba específica pasa, incluyendo orden, no mutación, lista vacía y solo canceladas. No encontré una condición omitida por el agente único; la revisión corroboró su resultado. |

El contexto coordinado se suma por rol porque cada agente conserva un historial independiente; por tanto, no equivale al contexto de una única conversación. El total de decisiones incluye las respuestas finales de cada rol.

## Evidencia

Las decisiones grabadas se encuentran en `agentes/trayectorias/issue-02-*.json` del repositorio.
Las observaciones de esta ejecución se pueden consultar en la [traza del agente único](../../trazas/issue-02-unico.jsonl)
y la [traza coordinada](../../trazas/issue-02-orquestado.jsonl).
Para reproducirlas en una carpeta nueva, ejecutar desde la raíz
`python agentes/ejecutar_issue_02.py --salida ../replay-e5`.

## Conclusión (7 líneas)

1. Ambas variantes resolvieron el mismo contrato desde copias limpias.
2. La prueba de rutas verifica exclusión de canceladas, orden y conservación de la entrada.
3. El agente único empleó 8 decisiones y la coordinación empleó 13.
4. Se completaron 1 rondas de revisión de un máximo de dos.
5. El agente único registró 0 acciones bloqueadas y la variante coordinada registró 0.
6. El contexto agregado del equipo fue de 10796 caracteres, frente a 6511 del agente único.
7. Para satisfacer esta prueba de rutas bastó el agente único. En este caso, incorporar dos roles adicionales no fue necesario para alcanzar el resultado funcional.
