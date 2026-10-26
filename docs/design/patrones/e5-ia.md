# E5: componente de IA aislado

## Función y alcance

EcoRecicla AQP usa un clasificador que propone el tipo de residuo a partir de una descripción. El clasificador devuelve exclusivamente PLASTICO, PAPEL o NO_CLASIFICABLE. Los dos primeros valores corresponden a los materiales aceptados por el flujo actual de solicitudes. La clasificación es una sugerencia: no crea solicitudes, no modifica sus estados y no acredita puntos. No hay conexión a un proveedor remoto ni se requieren claves.

## Patrones y responsabilidades

| Elemento | Archivo / clase | Responsabilidad |
| --- | --- | --- |
| Strategy / puerto | src/solicitudes/ia.py, ProveedorLLM | Contrato intercambiable para generar texto. |
| Adapter | AdaptadorProveedorLLM | Traduce invoke(prompt).content al puerto completar(prompt). |
| Decorator | ConCacheClasificador | Valida la descripción original y cachea en memoria resultados exitosos usando una clave normalizada; no almacena errores ni respuestas rechazadas. |
| Chain of Responsibility | CadenaGuardrails | Ejecuta validadores en orden y detiene el flujo ante el primer rechazo. |
| Guardrails de entrada | DescripcionNoVacia, DescripcionDeLongitudPermitida | Rechazan entradas vacías, de tipo incorrecto o mayores a 300 caracteres antes de llamar al proveedor. |
| Guardrails de salida | RespuestaNoVacia, CategoriaPermitida | Rechazan salidas vacías, explicaciones libres o categorías que no estén en la lista permitida. |
| Servicio | ClasificadorResiduo | Construye una instrucción acotada, llama al puerto y devuelve únicamente una categoría validada. |

El flujo separa el adaptador del proveedor de los guardrails. El texto generado no se usa directamente como material válido hasta que atraviesa la cadena de validación. NO_CLASIFICABLE requiere revisión manual y no es un material aceptable para registrar una solicitud.

## Verificaciones

Pruebas automatizadas: tests/test_patrones.py.

    python -m pytest tests/test_patrones.py -v

Las pruebas usan clientes locales simulados. Cubren clasificación válida y no clasificable, entradas vacías y extensas, respuestas inválidas, adaptación de un cliente de proveedor, caché de respuestas válidas y ausencia de caché para respuestas rechazadas. La prueba de regresión también comprueba que la validación de longitud precede a la búsqueda en caché. No se prueba la calidad semántica de un LLM real ni una integración externa.
