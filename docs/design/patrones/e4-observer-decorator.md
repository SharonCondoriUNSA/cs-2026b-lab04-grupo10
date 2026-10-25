# E4: Observer y Decorator

## Observer, avisos y proyección de pesajes

`src/solicitudes/eventos.py` define el publicador, la interfaz `Suscriptor` y eventos inmutables que contienen solo identificador y valores necesarios, sin pasar la entidad mutable a los consumidores.

El servicio publica `REGISTRADA` después de guardar y `PUNTOS_ACREDITADOS` después de confirmar la acreditación. Por defecto registra dos suscriptores:

1. `AvisosInternos`, genera las mismas intenciones de aviso de registro y puntos que observaban las pruebas de E1.
2. `ProyeccionPesajes`, genera la misma entrada de pesaje al acreditar, sin leer directamente el esquema de Solicitudes ni invocar código del módulo Reportes.

Los suscriptores conservan el orden observable de los eventos de E1. Puede añadirse un consumidor mediante `suscribir()` sin modificar el servicio. Si se inyecta un publicador personalizado, el llamador configura sus propios suscriptores, los dos predeterminados se agregan solo cuando se usa la configuración por defecto. Cada instancia mantiene su propio registro.

Los manejadores se ejecutan localmente y de forma síncrona para añadir intenciones al buzón en memoria. No se realiza un envío externo ni se implementa una cola durable, un hilo ni una garantía de entrega. La entrega posterior del aviso continúa fuera del alcance de este prototipo. Si un manejador falla, el publicador registra el tipo de error y permite continuar a los restantes, sin revertir el registro ya persistido.

## Decorator, reintentos de mapas

`src/solicitudes/decoradores.py` define `ConReintentos`, que implementa el mismo `PuertoMapas` que el objeto envuelto. Añade reintentos sin cambiar los adaptadores y sin introducir reglas de cobertura o puntos.

- Mantiene tres intentos como configuración predeterminada de E1.
- Repite únicamente `TimeoutError` y `ConnectionError`, sin esperas reales en las pruebas.
- Una respuesta válida o negativa termina inmediatamente la consulta.
- Si se agotan los intentos, devuelve False, el servicio guarda PENDIENTE con revisión de ubicación, como antes.
- Otros errores se propagan. Solo se envuelven consultas de mapas, no la acreditación ni la persistencia, evitando repetir efectos de negocio.

La tabla del caso 10 también sugiere Decorator para campañas o bonificaciones. E4 permite extraer una responsabilidad transversal, se eligieron los reintentos porque su duplicación se identificó y caracterizó en E1. No se inventa una bonificación municipal ni se modifica el cálculo de puntos para demostrar el patrón.

## Pruebas y resultado

```powershell
python -m pytest tests/test_comportamiento.py tests/test_patrones.py -v
```

Resultado del 25/10/2026: **122 passed**, 70 caracterizaciones de ambas versiones, ocho casos de E2, 32 de E3 y 12 nuevos de E4.

Observer se demuestra con dos suscriptores independientes que observan el registro ya persistido, el flujo completo con los dos consumidores predeterminados y la continuación tras un consumidor fallido. Decorator se demuestra con recuperación, agotamiento de intentos, respuesta negativa sin reintento, propagación de error no transitorio y rechazo de configuración inválida.

El servicio ya no agrega manualmente los mensajes a `eventos` ni contiene el bucle de reintentos. La línea base, los simuladores, el dominio del Lab05 y la salida inicial de Radon permanecen intactos. Este commit solo desarrolla E4, la función IA, las métricas comparativas, los diagramas y el cierre del Lab07 corresponden a E5-E8 de la compañera.
