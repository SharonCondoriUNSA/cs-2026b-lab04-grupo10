# E5: comparación de coordinación para ISSUE-02

## Protocolo y procedencia

Se resolvió el mismo estado inicial de `ISSUE-02` en dos copias independientes de `d9156e1`. La variante única usa un agente con hasta 12 decisiones. La coordinada usa planificador sin herramientas, ejecutor y revisor de solo lectura; el ciclo actor-crítico tiene un máximo de dos rondas. Las trayectorias JSON fueron redactadas por GPT en esta sesión para documentar decisiones reproducibles y se reprodujeron localmente con `ModeloGrabado`; no se hizo una llamada en vivo a un proveedor externo. Las herramientas sí ejecutaron las pruebas y editaron únicamente las copias de trabajo.

## Resultados

| Medida | Agente único | Planificador–ejecutor–revisor |
|---|---:|---:|
| Rondas actor-crítico | No aplica | 1 de 2 |
| Decisiones registradas | 8 | 13 |
| Acciones ejecutadas / bloqueadas | 7 / 0 | 10 / 0 |
| Contexto final (caracteres) | 6511 | 10796 acumulados entre roles |
| Fallo inicial reproducido | sí | sí |
| Prueba tras la corrección | pasó | pasó |
| Hallazgo adicional del revisor | No aplica | No; corroboró el contrato y no encontró una omisión del agente único |

El contexto coordinado se suma por rol porque cada agente conserva un historial independiente; por tanto, no equivale al contexto de una única conversación. El total de decisiones incluye las respuestas finales de cada rol.

## Evidencia

- Trayectorias: `agentes/trayectorias/issue-02-*.json`.
- Traza de la variante única: `agentes/trazas/issue-02-unico.jsonl` y diagrama Mermaid asociado.
- Trazas por rol y traza combinada: `agentes/trazas/issue-02-orquestado/` y `agentes/trazas/issue-02-orquestado.jsonl`.
- Diagramas Mermaid: `agentes/trazas/issue-02-unico.mmd` y `agentes/trazas/issue-02-orquestado.mmd`.

## Conclusión (7 líneas)

1. Ambas variantes resolvieron el mismo contrato desde copias limpias.
2. La prueba específica pasó y el cambio conserva orden y entrada original.
3. La coordinación añade decisiones y contexto porque separa los roles.
4. El revisor confirmó el resultado, pero no descubrió un defecto que el agente único hubiera omitido.
5. El límite de dos rondas evita que el ciclo de revisión crezca sin control.
6. Para este issue acotado, el costo adicional no se justifica por el resultado observado.
7. La coordinación sería más útil si el cambio tuviera mayor riesgo o varias decisiones independientes.
