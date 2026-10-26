# ADR-005: Patrones de diseño para el flujo de solicitudes

Estado: Aceptado
Fecha: 2026-10-25
Decisores: Equipo de desarrollo Grupo 10

## Contexto

El flujo de solicitud de recojo concentra decisiones que pueden cambiar por reglas de puntos, proveedores externos, estado de la solicitud, avisos y validaciones de una clasificación asistida por IA. En la versión inicial, varias decisiones se resolvían con condicionales o con responsabilidades técnicas mezcladas en el servicio. La modificabilidad es un atributo de calidad prioritario para EcoRecicla AQP (QA-01, ADR-001), pero el MVP también debe ser entendible para un equipo pequeño y mantenerse en un único despliegue.

## Alternativas consideradas

1. Mantener las decisiones en condicionales dentro de los servicios: menor estructura inicial, pero cada variante nueva exige modificar el flujo central y aumenta el acoplamiento.
2. Aplicar patrones GoF a las responsabilidades variables identificadas en la línea base, conservando pruebas de caracterización y agregando pruebas de patrón.
3. Adoptar patrones adicionales como Abstract Factory o Singleton: podrían agregar abstracciones, aunque no hay familias de productos relacionadas y el estado global dificultaría la sustitución de dependencias en pruebas.

## Decisión

Se aceptan los siguientes patrones, aplicados solo donde resuelven una variación o responsabilidad observada:

- **Strategy y Factory por registro:** ReglaPuntos abstrae el cálculo; FabricaReglas selecciona constructores registrados. FabricaMapas selecciona adaptadores de mapas.
- **Adapter:** MapaAdapter y GeoAdapter traducen los contratos de proveedores de mapas a PuertoMapas; AdaptadorProveedorLLM traduce invoke().content al puerto ProveedorLLM.
- **State:** la entidad Solicitud delega las transiciones en objetos de estado y rechaza operaciones fuera de orden.
- **Observer:** PublicadorEventos notifica suscriptores locales después de persistir o acreditar; no realiza envíos externos ni garantiza entrega durable.
- **Decorator:** ConReintentos agrega reintentos limitados a consultas de mapas; ConCacheClasificador almacena en memoria resultados validados.
- **Chain of Responsibility:** CadenaGuardrails procesa validadores de entrada y salida en orden, deteniéndose ante el primer rechazo.

Se rechaza **Abstract Factory** porque mapas y reglas de puntos varían independientemente y no forman familias que deban construirse juntas. Se rechaza **Singleton** porque no se necesita estado global y este dificultaría aislar instancias y sustituir dependencias en pruebas.

## Consecuencias

### Positivas

- Nuevas reglas y proveedores pueden registrarse o adaptarse sin reescribir los servicios consumidores.
- State concentra las transiciones permitidas y las guardas de cada etapa.
- Observer desacopla los avisos internos de la persistencia; Decorator encapsula reintentos y caché.
- Las pruebas verifican las extensiones, los rechazos y el comportamiento observable del flujo.

### Negativas / riesgos

- Hay más clases, interfaces y relaciones que comprender que en la versión inicial.
- Los registros de fábricas requieren configurar constructores válidos por instancia.
- La caché es local al proceso y no tiene persistencia; la entrega de eventos es síncrona y no durable.
- Los guardrails limitan el formato de salida de IA, pero no prueban la calidad semántica de un proveedor real, que no está conectado.

## Evidencia

- [Análisis de olores y decisiones de E1](../../design/patrones/olores.md).
- [Strategy, Adapter y Factory](../../design/patrones/e2-strategy-adapter-factory.md).
- [State](../../design/patrones/e3-state.md).
- [Observer y Decorator](../../design/patrones/e4-observer-decorator.md).
- [Clasificación asistida por IA y guardrails](../../design/patrones/e5-ia.md).
- [Métricas y trade-off](../../design/patrones/metricas.md).
- [Pruebas de comportamiento y patrones](../../../tests/test_comportamiento.py) y [pruebas de patrones](../../../tests/test_patrones.py).
