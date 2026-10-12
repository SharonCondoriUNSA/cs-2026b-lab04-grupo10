# Análisis de Ingeniería Directa e Inversa (Round-Trip) — Módulo Solicitudes

En este documento se compara el diagrama UML de diseño original (`docs/design/clases.puml`) con el código esqueleto generado en Python (`src/solicitudes/dominio.py`) y el modelo recuperado por ingeniería inversa.

## Tabla Comparativa de Diferencias (Round-Trip)

| N° | Diferencia Observada | Causa Técnica | Acción Tomada / Justificación |
|---|---|---|---|
| 1 | **Nombres en `snake_case` vs `camelCase`:** Métodos y atributos en Python usan `snake_case` (p. ej. `solicitar_recojo`, `peso_estimado_kg`) mientras que el UML usa `camelCase` (`solicitarRecojo`, `pesoEstimadoKg`). | Convención oficial de estilo PEP 8 de Python. | **Aceptada:** Se documenta la equivalencia de nombres. Cumple con la regla de consistencia del dominio C5. |
| 2 | **Representación de la Composición:** La relación de composición `SolicitudRecojo` \\(\diamondsuit\rightarrow\\) `DetalleReciclable` se genera en Python como una lista tipada `List[DetalleReciclable]`, perdiendo el símbolo explícito de diamante al re-generar UML con herramientas de ingeniería inversa. | Python no posee la palabra clave `composition` nativa; las asociaciones entre objetos se expresan mediante colecciones de referencias. | **Documentada:** Limitación propia de la ingeniería inversa en Python. El diagrama PlantUML se mantiene como fuente primaria de verdad estructural. |
| 3 | **Ausencia de Multiplicidades Explícitas en Firmas:** Las restricciones de multiplicidad (como `1..*` en los detalles del recojo o `0..1` en atributos opcionales) no quedan expresadas numéricamente en las clases Python. | El sistema de anotaciones de tipos (`type hints`) de Python no soporta restricciones de cardinalidad numérica directamente en las firmas. | **Corregida en código:** Se implementó una validación en el método `validar_datos()` que verifica explícitamente `len(self.detalles) > 0`, garantizando la regla de negocio (C3). |
| 4 | **Interfaces Abstractas:** Las interfaces PlantUML (`<<puerto>>`) se generaron como clases heredadas de `abc.ABC` con métodos `@abstractmethod`. | Python no posee la palabra reservada `interface`; utiliza Clases Base Abstractas (ABC). | **Aceptada:** Estructura idiomatica equivalente en Python que preserva la inversión de dependencias del monolito modular (ADR-001). |

## Conclusión
El proceso de Round-Trip permitió verificar la coherencia entre el diseño estático en PlantUML y la implementación del esqueleto en Python, asegurando que las reglas del dominio (C1-C5) se preserven correctamente en el código fuente.