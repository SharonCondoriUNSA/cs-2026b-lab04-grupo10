# E4. Iteración 2 ADD: continuidad del registro en ruta

## 1. Revisar entradas

[QA-02 (H,H) y QA-07](../utilidad/escenarios.md), [ADR-003 PWA](../adr/003-aplicacion-frontend.md), [ADR-005](../adr/005-patrones-de-diseno.md) y los resultados de [iteración 1](iteracion-1.md). El Lab04 ya pide IndexedDB y sincronización ≤ 30 s. Lab07 tiene eventos síncronos no durables, no una cola persistente. No se supone que un Observer en memoria garantice conservación.

## 2. Establecer objetivo

Tras 20 min sin red, conservar los 120 registros de un lote, sincronizarlos en ≤ 30 s después de recuperar conexión y producir 0 duplicados, incluso si se pierde una confirmación del servidor. Se refina la garantía funcional de conservación con una condición explícita de almacenamiento local sano.

## 3. Elegir elemento que se refina

Registro local de PWA y receptor de sincronización de Solicitudes. Los datos permanecen en IndexedDB hasta recibir confirmación, el servidor confirma después de persistir el efecto y su identificador en la misma transacción de PostgreSQL. No se crean servicios nuevos ni Redis. El estado de una solicitud se valida por State antes de aceptar una transición.

## 4. Elegir conceptos de diseño

| Alternativa | Beneficio | Coste y límite | Decisión propuesta |
|---|---|---|---|
| Envío directo sin almacenamiento local | Menos código | No conserva registros sin red | Rechazada |
| Reintentos con lista solo en memoria | Recupera fallos transitorios | Reiniciar el proceso pierde pendientes, ACK perdido duplica efectos | Rechazada como garantía de conservación |
| Buffer persistente local y receptor idempotente | Conserva pendientes y permite reenvío | Transacciones, cuotas locales, conflictos y retención de identificadores | Elegida, sobre PWA y PostgreSQL existentes |

Los reintentos de mapas del Lab07 siguen siendo válidos para consultas sin efectos. No se aplican ciegamente a una acreditación de puntos. Circuit breaker no es necesario en este experimento, no se transfiere el proveedor de pagos de AgroConecta a EcoRecicla.

## 5. Instanciar elementos y responsabilidades

[fitness/sincronizacion.py](../../../fitness/sincronizacion.py) usa dos archivos SQLite temporales como sustitutos de IndexedDB y PostgreSQL. Inserta 120 registros, cierra y reabre el almacenamiento local, los reenvía y elimina el pendiente solo tras confirmación. La clave única es (distrito, identificador). Un reintento con el mismo contenido no repite el efecto, un identificador reutilizado con otro contenido se rechaza. El contexto distrital deberá validarse como en iteración 3.

## 6. Esbozar vistas y registrar decisión

PWA → IndexedDB pendiente → API autenticada → transacción de efecto + identificador → ACK → eliminación local. Si el ACK se pierde, se repite el mismo identificador y se devuelve confirmación sin repetir el efecto. Almacenar una incidencia «Entrega no disponible» conserva ASIGNADA, no se convierte en pesaje ni acreditación. El prototipo utiliza payloads sintéticos y no implementa todas las transiciones de dominio.

Se propone conservar el buffer y la deduplicación dentro de contenedores existentes. La integración real y ADR-007 corresponden a E6. El trade-off aceptado para la propuesta es mayor complejidad de sincronización y almacenamiento a cambio de continuidad ante cortes de red.

## 7. Analizar y verificar

Comando: `python -m fitness.sincronizacion`. [Salida real de ambos escenarios](evidencia-2.json).

| Medida | Antes, modelo de envío directo sin buffer | Después, persistencia e idempotencia |
|---|---:|---:|
| Registros no transmitidos durante el corte | 120, no conservados | 120 conservados tras reapertura |
| Confirmaciones perdidas inyectadas | No aplica | 12 |
| Intentos al recuperar red | No conserva lote | 132 |
| Efectos únicos / duplicados | 0 / 0 | 120 / 0 |
| Registros perdidos / pendientes finales | 120 / 0 | 0 / 0 |
| Sincronización, 100 ms supuestos por intento | No cumple | 13.2 s modelados |
| Sincronización, sensibilidad a 250 ms por intento | No cumple | 33 s modelados, no cumple |

**Resultado: cumple QA-02 y QA-07 solo bajo los supuestos del modelo base.** El tiempo es virtual, no el tiempo medido de una red o un servidor. El límite para 132 intentos secuenciales es aproximadamente 227 ms por intento, por encima se incumplen 30 s. La sensibilidad evita declarar una garantía incondicional. La línea base sin buffer es un control hipotético, no una prueba de pérdida en la PWA del proyecto.

Supuestos: 120 registros al recuperar red, corte sin tráfico al servidor, red estable después del corte, 100 ms por intento incluyendo transacción y red, sin backoff adicional ni otros dispositivos simultáneos. No se simula una jornada completa ni se espera 20 min reales. El prototipo verifica transacciones SQLite, cierre normal y reapertura, no un apagado abrupto ni persistencia física bajo fallo eléctrico. No es una implementación de IndexedDB o PostgreSQL. Quedan pendientes pruebas en PWA real, dispositivos, almacenamiento lleno, concurrencia, retención de IDs y sincronización de conflictos de versión.

E3 sigue sin evaluación recibida, por tanto no se atribuye aquí mitigación de un riesgo crítico externo. Si llega uno, debe revisarse esta iteración. Riesgos propios atendidos: pendientes solo en memoria y duplicación tras perder ACK. El único VPS sigue siendo un punto de falla fuera del corte móvil ensayado.
