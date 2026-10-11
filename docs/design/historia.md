# E1 - Solicitar el recojo de reciclables

## Fuente y alcance

**Referencia:** Caso 10 EcoRecicla AQP, «Solicitar el recojo de reciclables» (tabla 7 de la guía del Lab05, página 16). La historia se mantiene como base de E1 y E2, coherente con RF-01 y el ADR-001 del Lab04.

## HU-01

Como vecino, quiero solicitar el recojo de mis residuos reciclables indicando los materiales, su peso estimado y el punto de recojo, para que EcoRecicla AQP pueda gestionar su recolección.

## Criterios de aceptación

- **CA-01 (éxito):** Dado un vecino identificado, un punto de recojo en un distrito con cobertura y al menos un material aceptado con peso estimado mayor que cero, cuando solicita el recojo, entonces se guarda una solicitud con identificador único, estado PENDIENTE, punto de recojo y detalle de materiales, y se devuelve su identificador como confirmación.
- **CA-02 (error de datos):** Dado un detalle vacío, un material no aceptado o un peso estimado menor o igual que cero, cuando el vecino solicita el recojo, entonces se indica el dato inválido y no se guarda ninguna solicitud.
- **CA-03 (error de cobertura):** Dado un punto de recojo cuyo distrito no tiene cobertura, cuando el vecino solicita el recojo, entonces se informa que el distrito no está atendido y no se guarda ninguna solicitud.
- **CA-04 (fallo externo):** Dado que los datos y la cobertura son válidos y la API de mapas no responde, cuando el vecino solicita el recojo, entonces se guarda la solicitud PENDIENTE con las coordenadas ingresadas, se confirma su identificador y se informa que la comprobación externa de ubicación está pendiente.

## Supuestos de diseño para E1

Las reglas CA-02 a CA-04 precisan el diseño, no se presentan como reglas textuales de la guía. El vecino ya está identificado por un UUID. Ingresa distrito y coordenadas válidas (latitud entre -90 y 90, longitud entre -180 y 180). La cobertura se consulta por código de distrito mediante el contrato público de Rutas/Cobertura. El catálogo de materiales aceptados pertenece a Solicitudes para este alcance. El mapa comprueba opcionalmente el punto, no decide la cobertura ni bloquea el registro. Una respuesta negativa del mapa se informa para revisión, conservando la solicitud válida y sus coordenadas.

Se conserva solo el identificador del vecino y la ubicación necesaria para el recojo, sin DNI, teléfono, nombre, credenciales ni historial de desplazamientos. La ubicación requiere protección de acceso, reducir atributos no la convierte en información pública.

## Clases y relaciones para sustentación

| Clase | Responsabilidad en la historia |
|---|---|
| Vecino | Identifica al solicitante sin duplicar su perfil personal. |
| SolicitudRecojo | Representa el registro confirmado, su fecha, estado y validación opcional del mapa. |
| DetalleReciclable | Guarda el peso estimado de un material dentro de una solicitud. |
| MaterialReciclable | Identifica un tipo de material y si se acepta para recojo. |
| PuntoRecojo | Conserva el distrito y las coordenadas necesarias para recoger los residuos. |
| ServicioSolicitudes | Valida los datos, consulta cobertura, guarda la solicitud y utiliza opcionalmente mapas. |
| AdaptadorMapas | Implementa el acceso HTTPS al servicio externo de mapas. |

Un vecino realiza cero o muchas solicitudes, cada solicitud tiene un vecino. La solicitud **compone** uno o más detalles y exactamente un punto: son datos propios del registro y no se comparten entre solicitudes. El material es una **asociación**, pues existe en el catálogo aunque no haya solicitudes. No se introduce herencia: ninguna clase del flujo necesita una relación «es un». AdaptadorMapas **realiza** ServicioMapas: implementa un contrato, no hereda de una entidad. Las dependencias temporales se dibujan con línea discontinua y no llevan multiplicidades, las asociaciones y composiciones sí las incluyen en ambos extremos.

RepositorioSolicitudes es un puerto de persistencia y CoberturaRecojo es el contrato público de Rutas/Cobertura, sus implementaciones no se detallan en E1. No hay acceso directo a entidades ni tablas de otros módulos. EstadoSolicitud contiene PENDIENTE, único estado usado por esta historia, el ciclo completo sugerido en la columna E3 queda fuera del alcance y deberá ampliarse al abordar ese ejercicio.

## Artefactos

- [Diagrama fuente](clases.puml)
- [Imagen renderizada](img/clases-solicitudes.png)
- [Registro de IA y verificaciones](bitacora-ia.md)
- [Secuencia del flujo de solicitud (E2)](secuencia-solicitar-recojo.puml)
- [Imagen de la secuencia](img/secuencia-solicitar-recojo.png)

## Ampliación para E2

PWA y SolicitudController reciben y delegan la petición. NotificadorSolicitud expone un aviso interno asíncrono de confirmación de registro, asociado a la sesión identificada del vecino. El servicio lo solicita después de confirmar la persistencia; el aviso no sustituye la respuesta directa de éxito ni exige datos de contacto. Estos elementos pertenecen al flujo de solicitud, sin modificar las decisiones del Lab04.

La secuencia cubre CA-01 a CA-04: valida cada detalle en un `loop`, separa con `alt` los errores de datos y de cobertura, y conserva el registro cuando mapas falla. Los errores de datos o cobertura no alcanzan `guardar()`. El aviso `confirmarRegistro()` usa `->>` y no bloquea la respuesta. Se asume persistencia disponible; no se modelan fallos de base de datos, autenticación ni entrega garantizada del aviso. La construcción de SolicitudRecojo se documenta en una nota y no se representa como llamada de negocio.
