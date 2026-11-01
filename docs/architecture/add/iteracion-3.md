# E4. Iteración 3 ADD: aislamiento entre distritos

## 1. Revisar entradas

[QA-04 (H,H) y QA-05 (H,M)](../utilidad/escenarios.md), crecimiento de 3 a 12 distritos, [ADR-001](../adr/001-estilo-arquitectonico.md), [ADR-002](../adr/002-base-de-datos.md) y [configuración de iteración 1](iteracion-1.md). La consulta de un distrito no debe permitir leer, actualizar o configurar otro sin autorización. No se afirma cumplimiento legal a partir de este prototipo.

## 2. Establecer objetivo

0 lecturas y escrituras cruzadas en 132 pares ordenados de doce distritos y 100 % de operaciones sin ámbito válido rechazadas. Los administradores se restringen al distrito autorizado, los vecinos a sus propias solicitudes y los recicladores a su ruta asignada. El experimento cubre solo el primer límite, no prueba todos los roles.

## 3. Elegir elemento que se refina

Contratos de acceso a Solicitudes, Reportes y configuración distrital. El ámbito proviene de autenticación y autorización del servidor, nunca del parámetro distrito_id enviado por el cliente. Los datos se siguen organizando por esquemas de módulo y se añade un discriminador distrital dentro de sus tablas. No se cambia el estilo arquitectónico.

## 4. Elegir conceptos de diseño

| Alternativa | Aislamiento | Coste / trade-off | Decisión propuesta |
|---|---|---|---|
| Base de datos por distrito | Mayor separación física | 12 bases, migraciones y conexiones para dos personas | Rechazada para este alcance y presupuesto |
| Esquema por distrito | Separación lógica | Multiplica esquemas y altera la organización por módulo del ADR-002 | Rechazada |
| distrito_id y autorización central en repositorios públicos | Extensión menor, ámbito explícito y fail-closed | Un acceso que evada el contrato puede omitir el filtro | Verificada en el prototipo, necesaria pero insuficiente por sí sola |
| Lo anterior y políticas RLS PostgreSQL | Defensa adicional frente a filtros omitidos | Roles, políticas, pools de conexiones y contexto requieren pruebas reales | Propuesta para integración, no validada en este laboratorio local |

No se presenta RLS como implementado. Debe ensayarse con un rol de aplicación sin BYPASSRLS, sin ser propietario que eluda políticas y con contexto por transacción, evitando fugas de ámbito al reutilizar conexiones. La evaluación favorece conservar el esquema por módulo, no crear doce monolitos.

## 5. Instanciar elementos y responsabilidades

El [prototipo](../../../fitness/aislamiento.py) usa ContextoConfiable y RepositorioDistrital. El contexto representa la salida esperada de autenticación, no verifica firmas ni tokens. Ambos métodos públicos consultan una guarda común que deniega ámbitos ausentes, desconocidos o distintos al solicitado. El control inseguro omite deliberadamente esa guarda para comprobar que los intentos de ataque alcanzan datos si falta autorización.

## 6. Esbozar vistas y registrar decisión

Cliente → autenticación de API → ámbito distrital confiable → contrato público autorizado → datos de su módulo. El distrito solicitado debe coincidir con el autorizado, cambiar el parámetro no amplía permisos. Como defensa adicional se propone el mismo ámbito en RLS. La implementación de JWT, middleware y políticas SQL queda pendiente, ADR-008 se redactará en E6 con estas distinciones.

Trade-off: autorización central y defensa en base de datos reducen exposición, a cambio de complejidad de administración y validación. La configuración de reglas y horarios también debe pasar por este límite, no basta con proteger reportes. Accesos de agregación de toda la municipalidad necesitan un permiso explícito distinto, no una excepción implícita que permita saltarse el ámbito.

## 7. Analizar y verificar

Comando: `python -m fitness.aislamiento`. [Salida real](evidencia-3.json).

| Medida | Control inseguro, sin guarda | Contrato con guarda |
|---|---:|---:|
| Pares ordenados de distritos distintos | 132 | 132 |
| Lecturas cruzadas permitidas | 132 | 0 |
| Escrituras cruzadas permitidas | 132 | 0 |
| Operaciones cruzadas rechazadas | 0 | 264 |
| Operaciones sin ámbito válido rechazadas | No evaluado | 72 de 72 |
| Operaciones propias permitidas | No evaluado | 24 de 24 |
| Alteración de datos originales por los intentos rechazados | Sí | Ninguna |

**Resultado: QA-04 y QA-05 cumplen en el límite de autorización del prototipo.** No se concluye aislamiento del sistema completo, autenticación real, protección de todos los endpoints ni eficacia de RLS. El control inseguro es sintético, no una vulnerabilidad comprobada en Lab07. La comparación cuantitativa complementa la comparación de alternativas de seguridad permitida por E4.

Supuestos: un distrito por contexto de administrador, doce registros sintéticos sin datos personales, invocaciones secuenciales y ausencia de accesos que evadan el contrato. Quedan pendientes firma y expiración del token, roles, pertenencia de cada solicitud, acceso de reciclador, SQL/RLS, pool y concurrencia. La posibilidad de crear ContextoConfiable directamente en Python confirma que no es una frontera de seguridad desplegable por sí sola.

No hay hallazgos externos recibidos en E3. Se atiende un riesgo propio de mezcla distrital, sin atribuir una revisión cruzada realizada. Si se recibe un riesgo crítico, se deberá incorporar o justificar su mitigación antes de cerrar E4.
