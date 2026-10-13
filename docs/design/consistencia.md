# Auditoría de Consistencia UML (Reglas C1 – C5) — EcoRecicla AQP

En este documento se evalúa la consistencia cruzada entre los artefactos UML del sistema (`clases.puml`, `secuencia-solicitar-recojo.puml`, `estados-solicitud.mmd`, `actividades-ruta-diaria.puml` y `paquetes.puml`) y el esqueleto de código en Python (`src/solicitudes/dominio.py`).

## Matriz de Hallazgos y Verificación del Equipo

| Regla | Elemento Auditado | Hallazgo Reportado por la IA | Verificación del Equipo / Decisión |
|---|---|---|---|
| **C1** | Secuencia $\rightarrow$ Clases | La llamada `validarUbicacion()` en la secuencia enviaba la entidad `PuntoRecojo` completa en lugar de los atributos primarios. | **Correcto (Corregido):** Se verificó la firma en `clases.puml` que exige `validarUbicacion(latitud: Decimal, longitud: Decimal)`. Se ajustaron los parámetros en la secuencia para mantener consistencia estricta de tipos. |
| **C1** | Secuencia $\rightarrow$ Clases | **FALSO POSITIVO DE LA IA:** "El método `confirmarPuntosAcreditados()` invocado en la solicitud no tiene relación de asociación directa con el paquete `puntos_beneficios`." | **Rechazado (Falso Positivo):** La IA interpretó erróneamente que se requería una asociación UML de clase. `SolicitudRecojo` no debe estar acoplada al paquete de beneficios; únicamente expone la operación de dominio `confirmarPuntosAcreditados(acreditacionId: UUID)` para recibir la confirmación. Se respeta el aislamiento modular del ADR-001. |
| **C2** | Estados $\rightarrow$ Clases | La transición del estado `PESADA` a `PUNTOS_ACREDITADOS` requiere la invocación de `confirmarPuntosAcreditados()`. | **Verificado (Correcto):** La operación existe explícitamente en la clase `SolicitudRecojo` (`clases.puml`) y en el esqueleto de Python (`src/solicitudes/dominio.py`), garantizando la provocación válida del cambio de estado. |
| **C3** | Multiplicidades | La composición entre `SolicitudRecojo` y `DetalleReciclable` es `1` a `1..*`. | **Verificado (Correcto):** Coincide con la regla de negocio del dominio: no se permite registrar una solicitud sin al menos un detalle de material reciclable. Reforzado con validación en código. |
| **C4** | Paquetes | La relación entre `solicitudes` y los paquetes de soporte (`rutas_cobertura`, `puntos_beneficios`, `notificaciones`) es unidireccional. | **Verificado (Correcto):** Las dependencias forman un Grafo Acíclico Dirigido (DAG). Ningún módulo consumido depende de regreso hacia `solicitudes`, cumpliendo la regla C4 al 100 %. |
| **C5** | Lenguaje del Dominio | Los métodos y variables en Python usan `snake_case` (`solicitar_recojo`), mientras que UML usa `camelCase` (`solicitarRecojo`). | **Aceptada (Equivalencia):** Se confirmó que la variación responde a las convenciones de estilo de Python (PEP 8). Los sustantivos y verbos del dominio se preservan idénticos. |

## Conclusión
Se confirmaron 5 reglas de consistencia cumplidas satisfactoriamente. Se identificó y descartó 1 falso positivo de la IA referente al acoplamiento entre módulos, preservando las decisiones arquitectónicas del ADR-001.