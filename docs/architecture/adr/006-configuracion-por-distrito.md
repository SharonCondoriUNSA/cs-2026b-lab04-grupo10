# ADR-006: Configuración versionada por distrito

**Estado:** Propuesto para revisión del equipo

**Fecha:** 2026-10-31

**Decisores:** Equipo de desarrollo Grupo 10

## Contexto

El escenario [QA-01](../utilidad/escenarios.md) exige crecer de 3 a 12 distritos con reglas de puntos y horarios propios, sin modificar los consumidores. QA-06 requiere actualizar la configuración de un distrito sin alterar los otros once. El equipo mantiene el plazo de un mes, dos integrantes y bajo presupuesto (R-01 a R-03). ADR-001 conserva el monolito modular y ADR-005 ya ofrece Strategy y Factory para variaciones de cálculo.

## Alternativas consideradas

1. **Condicionales por distrito en cada consumidor:** sencillos al inicio, pero cada alta obliga a editar y probar varios consumidores; no satisface la medida de QA-01.
2. **Configuración versionada dentro de los módulos existentes:** separa tarifa de Puntos/Beneficios y horario/cobertura de Rutas, sin cambiar a quienes consumen sus contratos. Añade validación, versionado y control de autorización de cambios.
3. **Despliegue o base de datos por distrito:** ofrece aislamiento físico, pero agrega operación, migraciones y costo para doce distritos y un equipo de dos personas.
4. **Una clase Strategy por distrito:** permite reglas distintas, pero repite código cuando solo cambian valores de tarifa u horario.

## Decisión

Se propone guardar tarifas versionadas en el esquema de Puntos/Beneficios y horarios/cobertura versionados en el esquema de Rutas/Cobertura. Los módulos publican contratos para consultar y actualizar sus propios datos. Se conserva `FabricaReglas` para elegir la fórmula por material; se crean nuevas estrategias solo cuando cambie la fórmula, no por cada distrito. No se agrega un servicio, despliegue o esquema de base de datos por distrito.

## Evidencia y trade-off aceptado

En [iteración 1](../add/iteracion-1.md) y [evidencia-1.json](../add/evidencia-1.json), el prototipo pasó de 3 a 12 distritos, incorporó 9 configuraciones, realizó 24 comprobaciones de regla y horario, registró 0 cambios en los tres archivos consumidores observados y 0 alteraciones a los otros 11 distritos al modificar D01.

El experimento valida la estructura en memoria, no la persistencia ni los permisos en PostgreSQL. La [estimación de esfuerzo de E2](../add/estimacion-esfuerzo-1.md) desglosa siete actividades y aplica PERT más una reserva del 25 %. Con una convención de 8 horas-persona por día-persona, da 12.8125 horas-persona, aproximadamente **1.60 días-persona**, frente al límite de **2 días-persona** de QA-01. El caso pesimista con reserva llega a **2.50 días-persona**, por lo que el límite no está garantizado.

La estimación corresponde al alta sobre mecanismos reutilizables de API, persistencia y autorización, cuya construcción inicial no está incluida. Son valores de planificación propuestos para revisión, no horas medidas ni prueba de cumplimiento desde el estado actual del prototipo. QA-06 requiere su propia comprobación de esfuerzo. Se acepta el costo de validar y versionar cambios para evitar modificar consumidores, el catálogo experimental no se declara ya integrado al producto.

## Consecuencias

### Positivas

- Un nuevo distrito puede configurarse en los módulos existentes sin replicar despliegues.
- Cambios de tarifa y horario se pueden versionar por distrito.
- Las fórmulas siguen usando Strategy/Factory cuando hay una variación algorítmica real.

### Riesgos y límites

- Una configuración errónea o una publicación no autorizada puede afectar la operación de un distrito.
- La consistencia entre los esquemas y la protección de `distrito_id` requieren controles de autorización, tratados en ADR-008.
- Los resultados sintéticos no prueban el tiempo humano requerido por QA-01/QA-06.

## Relación con C4

En [`workspace.dsl`](../c4/workspace.dsl), los contenedores PWA, API y PostgreSQL permanecen. Las descripciones de Rutas/Cobertura y Puntos/Beneficios identifican QA-01 y QA-06; no se añade infraestructura para cada distrito.
