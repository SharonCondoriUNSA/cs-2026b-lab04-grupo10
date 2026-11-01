# ADR-007: Buffer local y sincronización idempotente

**Estado:** Propuesto para revisión del equipo

**Fecha:** 2026-10-31

**Decisores:** Equipo de desarrollo Grupo 10

## Contexto

QA-02 requiere conservar registros durante 20 minutos sin red y sincronizar sin pérdidas ni duplicados; QA-07 fija un lote de 120 registros y un máximo de 30 segundos al recuperar la conexión. ADR-003 eligió una PWA y ADR-002 una instancia PostgreSQL. ADR-005 aclara que el Observer del Lab07 es síncrono y en memoria, por lo que no ofrece una cola durable.

## Alternativas consideradas

1. **Envío directo sin buffer:** menos complejidad, pero no conserva los registros cuando no hay red.
2. **Reintentos solo en memoria:** resuelve algunos fallos transitorios, pero pierde pendientes al reiniciar y puede duplicar efectos si se pierde un ACK.
3. **Cola persistente local y receptor idempotente en la API:** conserva registros y permite reintentar usando una identidad estable; añade almacenamiento, transacciones, manejo de cuotas y retención de identificadores.
4. **Nuevo broker/servicio de mensajería:** ofrece capacidades adicionales, pero aumenta el costo y la operación del MVP sin evidencia que lo justifique.

## Decisión

Se propone mantener en IndexedDB de la PWA cada registro pendiente con un identificador estable. Al recuperar la conectividad, el cliente reenvía el mismo identificador hasta recibir ACK. La API registra el efecto de negocio y la clave de idempotencia en una transacción PostgreSQL; solo después confirma. Un reintento idéntico devuelve la confirmación existente sin repetir el efecto; reutilizar la clave con contenido distinto se rechaza. El cliente elimina el pendiente únicamente al recibir el ACK. La funcionalidad de persistencia y sincronización real queda pendiente de integración.

## Evidencia y trade-off aceptado

En [iteración 2](../add/iteracion-2.md) y [evidencia-2.json](../add/evidencia-2.json), el prototipo SQLite conservó 120 registros tras cierre y reapertura normal, inyectó 12 ACK perdidos y completó 132 llamadas para obtener 120 efectos únicos, cero pérdidas, cero duplicados y cero pendientes. El tiempo modelado fue 13.2 s con 100 ms supuestos por llamada; con 250 ms fue 33 s y excedió el límite. El identificador reutilizado con otro contenido se rechazó.

SQLite sustituye a IndexedDB y PostgreSQL en el experimento, y el tiempo es virtual, no una medición de red. Se acepta mayor complejidad de almacenamiento e idempotencia para lograr continuidad condicionada a almacenamiento local sano y rendimiento suficiente; no se afirma que QA-02/QA-07 estén garantizados en producción.

## Consecuencias

### Positivas

- Los pendientes sobreviven a la pérdida de conectividad y a un cierre normal de la PWA.
- Repetir una solicitud con la misma clave evita duplicar su efecto.
- Se conserva el despliegue monolítico y no se incorpora un broker.

### Riesgos y límites

- El almacenamiento local puede llenarse, ser borrado o fallar; se requiere mostrar su estado y evitar confirmar una escritura no persistida.
- Los identificadores deben conservarse durante la ventana de reintentos; los conflictos de versión necesitan una política aparte.
- Para 132 intentos secuenciales, el modelo supera 30 s con 250 ms por intento. Hace falta medir la implementación real y definir concurrencia/backoff.
- El prototipo no es una implementación de IndexedDB ni de PostgreSQL y no ensaya un apagado abrupto.

## Relación con C4

En [`workspace.dsl`](../c4/workspace.dsl), la PWA describe IndexedDB para QA-02/QA-07, la API representa el receptor idempotente y PostgreSQL identifica la clave única por distrito e identificador. Se mantienen los tres contenedores existentes.
