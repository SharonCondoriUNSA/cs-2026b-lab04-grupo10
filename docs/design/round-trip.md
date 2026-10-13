# Análisis de Ingeniería Directa e Inversa (Round-Trip) — Módulo Solicitudes

En este documento se compara el diagrama UML de diseño original (`docs/design/clases.puml`) con el código esqueleto generado en Python (`src/solicitudes/dominio.py`) y el modelo recuperado por ingeniería inversa en classes_solicitudes.puml, ejecutado el 2026-10-13 con pylint 4.1.3 y astroid 4.3.4.

## Tabla Comparativa de Diferencias (Round-Trip)

| N° | Diferencia Observada | Causa Técnica | Acción Tomada / Justificación |
|---|---|---|---|
| 1 | **Nombres en `snake_case` vs `camelCase`:** Métodos y atributos en Python usan `snake_case` (p. ej. `solicitar_recojo`, `peso_estimado_kg`) mientras que el UML usa `camelCase` (`solicitarRecojo`, `pesoEstimadoKg`). | Convención oficial de estilo PEP 8 de Python. | **Aceptada:** Se documenta la equivalencia de nombres. Cumple con la regla de consistencia del dominio C5. |
| 2 | **Representación de la Composición:** La relación de composición `SolicitudRecojo` \\(\diamondsuit\rightarrow\\) `DetalleReciclable` se genera en Python como una lista tipada `List[DetalleReciclable]`, perdiendo el símbolo explícito de diamante al re-generar UML con herramientas de ingeniería inversa. | Python no posee la palabra clave `composition` nativa; las asociaciones entre objetos se expresan mediante colecciones de referencias. | **Documentada:** Limitación propia de la ingeniería inversa en Python. El diagrama PlantUML se mantiene como fuente primaria de verdad estructural. |
| 3 | **Ausencia de Multiplicidades Explícitas en Firmas:** Las restricciones de multiplicidad (como `1..*` en los detalles del recojo o `0..1` en atributos opcionales) no quedan expresadas numéricamente en las clases Python. | El sistema de anotaciones de tipos (`type hints`) de Python no soporta restricciones de cardinalidad numérica directamente en las firmas. | **Corregida en código:** Se implementó una validación en el método `validar_datos()` que verifica explícitamente `len(self.detalles) > 0`, garantizando la regla de negocio (C3). |
| 4 | **Interfaces Abstractas:** Las interfaces PlantUML (`<<puerto>>`) se generaron como clases heredadas de `abc.ABC` con métodos `@abstractmethod`. | Python no posee la palabra reservada `interface`; utiliza Clases Base Abstractas (ABC). | **Aceptada:** Estructura idiomatica equivalente en Python que preserva la inversión de dependencias del monolito modular (ADR-001). |

## Diferencias adicionales observadas
Las diferencias se contrastaron con la salida real, que no recupera el diamante de composición ni las multiplicidades. Además, se observaron estas diferencias:

| N.º | Diferencia observada | Causa | Acción |
|---|---|---|---|
| 5 | AdaptadorMapas y PWA tienen operaciones representadas como abstractas. | pyreverse interpreta los cuerpos que lanzan NotImplementedError como abstractos. | Se documenta la limitación, las clases son esqueletos sin integración externa ni UI implementada. |
| 6 | EstadoSolicitud se representa como clase con name, sin los cinco valores. | La representación inversa de Enum no conserva la notación del diseño. | Se conserva el Enum de Python y el UML original. |
| 7 | No aparecen todas las dependencias temporales de operaciones. | La herramienta infiere principalmente relaciones desde atributos y clases base. | Se mantiene el diagrama de diseño para las colaboraciones de E2. |

## Ejecución y artefactos verificados

- [Diagrama inverso generado](classes_solicitudes.puml)
- [Imagen del diagrama inverso](img/classes_solicitudes.png)

## Generación y verificación

Se ejecutó pyreverse para obtener el diagrama de clases desde el código Python:

    pyreverse -o puml -p solicitudes -d docs/design src/solicitudes/dominio.py

El PlantUML generado pasó la comprobación de sintaxis y se revisó su imagen PNG. También pasaron siete pruebas locales de validación y manejo de errores.

Se completaron las clases y operaciones faltantes y se corrigieron los tipos y las transiciones para mantener coherencia con el diseño.

PWA y AdaptadorMapas permanecen como esqueletos. El aviso asíncrono es una demostración local, sin garantía de entrega. Las pruebas se conservaron solo en el entorno local, no forman parte de esta entrega.
## Conclusión

El round-trip se ejecutó realmente con pyreverse. Su salida presenta limitaciones y no sustituye las multiplicidades y reglas del diagrama de diseño. No se declara una implementación completa de la PWA ni de servicios externos.
