# E2. Iteración 1 de ADD: variación por distrito

## 1. Revisar entradas

[QA-01 (H,H)](../utilidad/escenarios.md), [drivers](../drivers.md), [ADR-001](../adr/001-estilo-arquitectonico.md) y [ADR-005](../adr/005-patrones-de-diseno.md). De 3 a 12 distritos con puntos y horarios distintos. Dos integrantes, un mes y presupuesto bajo. El caso crítico sigue siendo solicitar y atender un recojo, la regla de puntos se utiliza después del pesaje.

## 2. Establecer objetivo

Incorporar un distrito en ≤ 2 días-persona con 0 cambios en consumidores. Es la prioridad por modificabilidad del Lab04. Se prueba la parte estructural de la medida y se declara separadamente el esfuerzo humano no medido. QA-06 sirve como comprobación complementaria de independencia.

## 3. Elegir elemento que se refina

Selección de configuración en los contratos de Puntos/Beneficios y Rutas/Cobertura. Se mantiene Strategy/Factory de Lab07 para calcular, no se fusionan módulos ni se consulta directamente su esquema. La fachada de laboratorio reúne las dos consultas solo para experimentar.

## 4. Elegir conceptos de diseño

| Candidato | Beneficio | Coste / trade-off | Decisión propuesta |
|---|---|---|---|
| Condicionales por distrito en cada consumidor | Implementación inicial corta | Cada alta obliga a revisar varios servicios y repetir reglas | Rechazado, no satisface 0 cambios de consumidores |
| Configuración versionada por distrito y estrategias existentes | Altas de tarifas y horarios sin editar consumidores | Validación, control de versiones y autorización de publicación | Elegido para la familia de variaciones probada |
| Un despliegue o microservicio por distrito | Aislamiento operativo independiente | 12 despliegues, migraciones y monitoreo para dos personas | Rechazado, no hay evidencia que justifique abandonar ADR-001 |
| Nueva clase Strategy por cada distrito | Admite algoritmos realmente distintos | Repite clases si solo cambia tarifa u horario | Reservado para una fórmula nueva, no para valores distintos |

## 5. Instanciar elementos y responsabilidades

El [prototipo](../../../fitness/distritos.py) incorpora ConfiguracionDistrito inmutable, CatalogoDistritos con versión creciente y ConsultaDistrital. Reutiliza FabricaReglas real del Lab07 y Decimal. La futura persistencia se propone en las tablas propias de cada módulo con distrito_id y versión. No se añade base de datos, UI administrativa ni API en E2.

## 6. Esbozar vistas y registrar decisión

Consumidor → contrato público de Puntos o Cobertura → configuración de su módulo por distrito → estrategia existente. Una publicación cambia solo la versión del distrito elegido. Para doce tarifas y franjas se prefiere configuración a infraestructura adicional. La decisión es una propuesta respaldada por este experimento, su ADR corresponde a E6.

## 7. Analizar y verificar

Comando desde la raíz: `python -m fitness.distritos`. [Salida real](evidencia-1.json).

| Medida | Antes: catálogo inicial | Después: altas por configuración |
|---|---:|---:|
| Distritos disponibles | 3 | 12 |
| Nuevos distritos rechazados / incorporados | 9 rechazados | 9 incorporados |
| Comprobaciones de puntos y horario para 12 distritos | No puede atender los nueve nuevos | 24 aprobadas |
| Archivos consumidores originales modificados durante el experimento | 0 | 0, huellas SHA-256 idénticas |
| Otros distritos alterados al cambiar D01 | No evaluado | 0 de 11 |
| Esfuerzo de integración en días-persona | No medido | No medido |

**Resultado: cumplimiento parcial de QA-01.** El prototipo demuestra altas sin editar los tres archivos de código inspeccionados. El tiempo de ejecución registrado en ms solo mide la operación local de alta de configuración, no demuestra ≤ 2 días-persona. Falta cronometrar un alta real incluyendo persistencia, permisos, pruebas y revisión para cerrar ese objetivo. QA-06 también requiere medir trabajo humano.

Supuestos: datos sintéticos D01–D12, fórmula lineal por peso ya existente, horarios de una franja por día sin feriados ni franjas nocturnas. No se representan todos los posibles reglamentos municipales. Una fórmula nueva necesita una estrategia y pruebas nuevas. El prototipo no acredita puntos ni sustituye las guardas de State. No se midió PostgreSQL, latencia de red ni carga de producción. Antes y después comparten el mismo catálogo de prueba, no se afirma que Lab07 ya contuviera horarios.

Riesgos: configuración errónea o mal autorizada, incorporación de fórmulas no representables y mezcla accidental de ámbitos. El aislamiento se evalúa en la iteración 3. La revisión cruzada E3 permanece pendiente de asignación docente.
