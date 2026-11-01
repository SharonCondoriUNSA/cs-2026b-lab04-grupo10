# ADR-008: Autorización con ámbito distrital

**Estado:** Propuesto para revisión del equipo

**Fecha:** 2026-10-31

**Decisores:** Equipo de desarrollo Grupo 10

## Contexto

QA-04 exige cero lecturas y escrituras cruzadas entre 12 distritos; QA-05 exige rechazar operaciones sin ámbito confiable o con un distrito solicitado distinto del autorizado. ADR-001 y ADR-002 mantienen un monolito modular con esquemas por módulo. Un `distrito_id` enviado por el cliente no prueba autorización y no debe decidir por sí solo el acceso.

## Alternativas consideradas

1. **Filtrar solo por el distrito enviado por el cliente:** sencillo, pero permite cambiar el parámetro para intentar acceder a otro distrito.
2. **Bases de datos separadas por distrito:** ofrecen aislamiento físico, con mayor costo operativo, conexiones y migraciones.
3. **Ámbito derivado de autenticación en la API, validado por contratos/repositorios y `distrito_id` en las filas:** conserva esquemas por módulo; una ruta que omita el contrato central aún puede exponer datos.
4. **La alternativa 3 con políticas PostgreSQL RLS:** añade defensa en profundidad, pero exige roles sin bypass, contexto por transacción y pruebas del pool de conexiones.

## Decisión

Se propone que la API derive un ámbito distrital confiable de la identidad y autorización autenticadas, rechace si falta o no coincide con el distrito solicitado y pase ese ámbito explícitamente a los contratos públicos de acceso. `distrito_id` se conserva en las filas de los módulos que lo necesitan. Se propone añadir RLS en PostgreSQL como defensa adicional, con rol de aplicación sin `BYPASSRLS`, contexto por transacción y pruebas de reutilización de conexiones. RLS, JWT y middleware real no se declaran implementados por el prototipo.

## Evidencia y trade-off aceptado

En [iteración 3](../add/iteracion-3.md) y [evidencia-3.json](../add/evidencia-3.json), el prototipo sintético recorrió los 132 pares ordenados de distritos distintos: rechazó 264 operaciones cruzadas (lecturas y escrituras), permitió 0 accesos cruzados y mantuvo intactos los datos. Rechazó 72 operaciones sin ámbito válido y permitió 24 operaciones propias. El control negativo sintético, sin guarda, habría permitido 132 lecturas y 132 escrituras cruzadas.

La prueba no verifica tokens, roles, endpoints, base de datos ni RLS. Se acepta la carga de mantener contexto y políticas por transacción para reducir el riesgo de exposición; se debe probar la implementación con una base real antes de afirmar aislamiento del sistema.

## Consecuencias

### Positivas

- Cambiar un parámetro distrital no amplía permisos.
- Los módulos mantienen sus esquemas y pueden centralizar la validación de su contrato público.
- RLS puede proteger filas frente a una consulta que omita un filtro de aplicación, una vez configurado y probado correctamente.

### Riesgos y límites

- Un contexto autenticado incorrectamente, una ruta que evite el contrato o una política mal configurada puede permitir acceso indebido.
- La conexión reutilizada sin restablecer el ámbito por transacción puede filtrar contexto entre solicitudes.
- El prototipo local solo demuestra la guarda de un contrato; no acredita autenticación ni seguridad desplegada.

## Relación con C4

En [`workspace.dsl`](../c4/workspace.dsl), las descripciones de API, Solicitudes, Reportes y PostgreSQL señalan QA-04/QA-05 y distinguen el ámbito propuesto de JWT/RLS aún no implementados. No se añade un servicio de autenticación independiente.
