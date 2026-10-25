# E1: Versión antes, caracterización y olores

Caso 10, EcoRecicla AQP. Fecha: 25/10/2026. Rama: `lab07-e1-antes`.

## Alcance y antecedentes

Se toma el flujo Solicitar el recojo de reciclables de `docs/design/secuencia-solicitar-recojo.puml`. Se validan detalles, coordenadas y cobertura antes de persistir. Mapas no determina cobertura y su fallo no impide guardar PENDIENTE. El aviso es interno y se solicita después de persistir, sin teléfonos ni envío real por WhatsApp.

`src/solicitudes/antes/servicio.py` es una línea base nueva para refactorizar, no modifica ni reemplaza `src/solicitudes/dominio.py` del Lab05. El ejemplo AgroConecta se utilizó como referencia de estructura, fixture y SDK simulados, sin copiar el dominio de pagos. Sus recursos están fuera del repositorio, en las carpetas hermanas `ejemplo/` y `docs/` y en `LEEME.md`, y no se incluyen en el commit.

La tabla 7 de la guía del Lab07, página 16, propone reglas de puntos como variación principal. Para prepararla sin acreditar durante el registro, se añade una operación posterior a PESADA. El cálculo permanece en el módulo interno Puntos/Beneficios, en `src/puntos_beneficios/antes/servicio.py`. Solicitudes usa su operación pública y solo registra la confirmación. No se convierte Puntos/Beneficios en proveedor externo ni se comparten entidades entre módulos.

## Supuestos explícitos de esta línea base

- Se asume sesión autorizada en la capa que invoca el servicio, no se almacenan perfiles ni datos personales.
- Las tarifas por kilogramo se inyectan, los valores 10 para plástico y 5 para papel existen únicamente en las pruebas. Los puntos fraccionarios se truncan hacia abajo. Son decisiones ilustrativas del ejercicio, no una política municipal obtenida de los ADR.
- Los proveedores ficticios MAPA y GEO tienen firmas y respuestas distintas, uno devuelve un diccionario y el otro un código con una tupla. Solo se reintentan errores transitorios, hasta tres intentos sin esperas reales. Este límite es una política local nueva para caracterizar y después extraer, el Lab05 no especificaba cuántos reintentos realizar.
- Un proveedor de mapas no soportado produce error sin persistir. Tres fallos transitorios o una respuesta negativa conservan la solicitud con revisión de ubicación pendiente.
- El repositorio en memoria ofrece una instantánea del registro inicial. Las transiciones posteriores se ejercitan en memoria, no son una implementación completa de persistencia del ciclo.
- `eventos` representa solicitudes de despacho posterior, no entregas confirmadas. No hay hilo, red ni garantía de entrega. Al acreditar se emiten eventos de puntos y pesaje para caracterizar la futura separación por Observer.
- `cerrada` representa el final de la máquina del Lab05 sin añadir un sexto estado. Los métodos corresponden a asignar, recoger, pesar, confirmar acreditación y cerrar, con el registro inicial en `solicitar_recojo`.

## Prompt IA 1 adaptado y utilizado

Herramienta: Codex, esta conversación. Solicitud recibida: desarrollar únicamente E1 inicialmente, conforme a la guía y tomando los recursos del profesor como referencia.

> Actúa como revisor de código experto en refactorización y patrones GoF. Revisa src/solicitudes/antes/servicio.py y src/puntos_beneficios/antes/servicio.py junto con la salida real radon-antes.txt. Contexto: EcoRecicla AQP, monolito modular del ADR-001, secuencia y estados del Lab05. Identifica al menos cuatro olores, indicando líneas, patrón propuesto o ninguno, principio SOLID, costo y decisión técnica. No escribas todavía el refactor, no uses Singleton ni propongas patrones sin olor concreto. Contrasta especialmente Strategy para reglas de puntos, Adapter para mapas, State para solicitudes y Observer para avisos. Evalúa si Abstract Factory se justifica y recházala si no hay familias de productos.

Se aplica como revisión adicional en esta misma sesión, no se registra una consulta ficticia a otra IA. Las decisiones siguientes son las adoptadas para preparar el refactor autorizado, quedan disponibles para revisión de la compañera y no acreditan una aprobación humana ya realizada.

## Resultado y decisiones

Las líneas corresponden a los archivos de esta versión E1, antes de refactorizar.

| Archivo y líneas | Olor observado | Patrón propuesto | Principio SOLID | Costo o límite | Decisión registrada |
| --- | --- | --- | --- | --- | --- |
| `src/puntos_beneficios/antes/servicio.py:11-16` | Condicional por material, cada nueva regla exige modificar el servicio de puntos. | Strategy y Factory por registro | O, abierto/cerrado, y D, inversión de dependencias | Interfaz, estrategias y registro adicionales, mantener tarifas como configuración. | Adoptar en E2 para la variación principal del caso. |
| `src/solicitudes/antes/servicio.py:74-91` | Solicitudes conoce las firmas, diccionario y código de cada SDK de mapas. | Adapter y Factory por registro | D y I, interfaces pequeñas | Un adaptador por SDK, sin trasladar reglas de cobertura ni cálculo de puntos al adaptador. | Adoptar en E2, conservar el resultado observable. |
| `src/solicitudes/antes/servicio.py:75-90` | Reintentos duplicados y mezclados con registro y selección del proveedor. | Decorator | S, responsabilidad única | Debe distinguir fallos transitorios y conservar el máximo de tres intentos, no reintentar operaciones de efectos no idempotentes. | Adoptar en E4 para la consulta de mapas. |
| `src/solicitudes/antes/servicio.py:107-155` | Condicionales repetidos que permiten o prohíben operaciones según estado. | State | S y O | Clase base y una clase por estado, conservar guardas y las cinco etiquetas del Lab05. | Adoptar en E3, sin añadir cancelaciones ajenas al diagrama. |
| `src/solicitudes/antes/servicio.py:102-104,140-141` | El servicio construye y agrega a mano los avisos de registro, puntos y pesajes. | Observer | S y O | Registro de suscriptores y política de fallos, conservar el aviso posterior a persistir. | Adoptar en E4, sin afirmar entrega externa garantizada. |
| `src/solicitudes/antes/servicio.py:55-105` | Método largo con validación, SDK, reintentos, copia, persistencia y aviso, complejidad 25. | Ninguno adicional por sí mismo | S | Extraer funciones puede bastar para validaciones, más clases no garantizan mejor diseño. | Dividir por responsabilidades durante E2-E4, no introducir patrones solo para bajar la métrica. |
| Creación de proveedores en `src/solicitudes/antes/servicio.py:49-50` | Se podría agrupar la creación de mapas y puntos como una familia de objetos. | Abstract Factory | No hay mejora demostrada frente a un registro simple | Mapas y reglas de puntos varían de forma independiente, sin familias que deban crearse juntas. Añadiría acoplamiento y clases. | **Rechazada**, basta la Factory por registro solicitada, no hay un olor que justifique Abstract Factory. |

## Verificación y reproducción

Con Python 3.12.14, pytest 9.1.1 y radon 6.0.1:

```powershell
python -m pip install pytest==9.1.1 radon==6.0.1
python -m pytest tests/test_comportamiento.py -v
python -m radon cc -s -a src/solicitudes/antes src/puntos_beneficios/antes
```

En esta sesión las dependencias se instalaron en una carpeta de apoyo fuera del repositorio. Se invocó pytest.main y la entrada de módulo de radon con esa carpeta en sys.path. El entorno restringido no podía leer dichos paquetes y se autorizó la ejecución fuera del aislamiento. No se cambió ninguna dependencia global del proyecto.

Resultado observado: **28 casos pasaron**, mediante 17 funciones de prueba y sus parametrizaciones. El fixture importa solo `src.solicitudes.antes.servicio` en E1. En E2 se añadirá el módulo de la versión refactorizada al mismo fixture y se adaptará la construcción del colaborador Puntos a esa versión, sin alterar las expectativas del contrato. Todavía no existe una versión después aprobada por estas pruebas.

Se cubren éxito con ambos mapas, detalles vacíos, peso cero, negativo y no finito, material no aceptado, límites geográficos, coordenadas inválidas, falta de cobertura, recuperación tras dos fallos, agotamiento tras tres, respuesta negativa, proveedor no soportado, error de persistencia, duplicados, copia de datos, ciclo válido y transición inválida. Las aserciones comprueban respuestas, estado, datos guardados, eventos y excepciones, no tipos concretos de futuros patrones ni número de llamadas privadas.

La salida completa de complejidad está en [radon-antes.txt](radon-antes.txt). Resultado: `solicitar_recojo` D (25), `ServicioPuntos.acreditar` B (9), promedio de los 17 bloques B (5.117647058823529). Son métricas de la línea base, no se afirma todavía una mejora ni se desarrolla E6.
