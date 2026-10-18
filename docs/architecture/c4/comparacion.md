# Comparación: Diagrama de Secuencia UML vs. Vista Dinámica C4

El diagrama de secuencia UML del Lab05 muestra firmas, retornos, líneas de vida y fragmentos `alt` y `loop`, orientados a los desarrolladores.
La vista dinámica C4 resume el mismo registro en cinco interacciones entre la PWA, componentes, mapas y persistencia, para comunicar el flujo a arquitectos, líderes técnicos y evaluadores.
Se omiten las clases, la iteración por detalles, los retornos HTTP y las ramas de error de datos o falta de cobertura, que impiden guardar en la secuencia UML. Se representa el escenario con datos y cobertura válidos.
La comprobación de mapas es opcional, su fallo permite guardar PENDIENTE con ubicación por revisar. Después de confirmar la persistencia se solicita el aviso interno asíncrono, sin añadir Redis ni envío por WhatsApp a este escenario.
