# Auditoría de Consistencia UML (Reglas C1 – C5) — EcoRecicla AQP

En este documento se evalúa la consistencia cruzada entre los artefactos UML del sistema (`clases.puml`, `secuencia-solicitar-recojo.puml`, `estados-solicitud.mmd`, `actividades-ruta-diaria.puml` y `paquetes.puml`) y el esqueleto de código en Python (`src/solicitudes/dominio.py`).

## Matriz de Hallazgos y Verificación del Equipo

Revisión actualizada el 2026-10-13 con E5 corregido (ab89d24) y E6 corregido y actualizado con main (634a1ca). La tabla conserva los hallazgos de la propuesta original y distingue lo comprobado en los archivos de lo que no se reproduce. Las comprobaciones técnicas de esta actualización se realizaron con apoyo de Codex, sin atribuir una nueva revisión humana al equipo.

| Regla | Elemento Auditado | Hallazgo Reportado por la IA | Verificación del Equipo / Decisión |
|---|---|---|---|
| **C1** | Secuencia $\rightarrow$ Clases | La propuesta inicial señaló que validarUbicacion recibía PuntoRecojo completo. | **No reproducido:** La secuencia ya usa validarUbicacion(punto.latitud, punto.longitud), coherente con la firma de clases. No fue necesario modificarla. Se comprobaron las 13 llamadas y todas tienen operación en el receptor. |
| **C2 / C4** | Estados y actividades $\rightarrow$ Clases y paquetes | **FALSO POSITIVO REPORTADO EN LA PROPUESTA ORIGINAL:** Se exigía una asociación directa entre SolicitudRecojo y el paquete puntos_beneficios para confirmarPuntosAcreditados(). | **Rechazado:** La operación recibe la confirmación en SolicitudRecojo y aparece en estados y actividades, no en la secuencia E2. No requiere asociación directa a un paquete. E5 distingue el contrato de solicitud AcreditadorPuntos del método receptor. El hallazgo confunde dos responsabilidades y las notaciones de clase y paquete. |
| **C2** | Estados $\rightarrow$ Clases y código | PESADA a PUNTOS_ACREDITADOS requiere confirmarPuntosAcreditados(). | **Verificado:** Las seis operaciones de transición existen en SolicitudRecojo y sus equivalentes Python. Los cinco estados coinciden con la enumeración. E6 valida el estado de origen y el identificador de acreditación, las confirmaciones externas siguen siendo precondiciones del servicio. La existencia del método por sí sola no prueba autorización ni integración real. |
| **C3** | Multiplicidades | La composición SolicitudRecojo–DetalleReciclable es 1 a 1..*. | **Verificado:** Coincide con CA-01 y CA-02, la validación rechaza detalles vacíos. Las cuatro asociaciones del UML indican multiplicidades en ambos extremos. E6 copia punto y detalles al registrar, el material sigue asociado al catálogo. La salida de pyreverse no recupera todas las multiplicidades ni la composición, limitación documentada en round-trip.md. |
| **C4** | Paquetes | Se requiere un grafo sin ciclos y contratos públicos coherentes con ADR-001. | **Verificado en el modelo:** Las nueve dependencias de E5 no forman ciclos. Reportes consume FuentePesajes de Solicitudes, Solicitudes no depende de Reportes. Se conservan cuatro módulos de dominio y se justifican notificaciones como auxiliar y compartido como tipos, sin compartir entidades ni esquemas. Los contratos nuevos son precisiones de diseño, no implementaciones verificadas. |
| **C5** | Lenguaje del Dominio | Los métodos y variables en Python usan `snake_case` (`solicitar_recojo`), mientras que UML usa `camelCase` (`solicitarRecojo`). | **Aceptada (Equivalencia):** Se confirmó que la variación responde a las convenciones de estilo de Python (PEP 8). Los sustantivos y verbos del dominio se preservan idénticos. |

## Conclusión
Se comprobaron C1-C5 en las versiones indicadas del modelo y del esqueleto. Se corrigió la atribución de una modificación inexistente de la secuencia y se explicó el falso positivo reportado en la propuesta original. No se afirma validación de APIs reales ni implementación completa. El aviso asíncrono de E6 es demostrativo, y la autorización, confirmaciones externas y operación offline de la PWA no se implementan en ese esqueleto.


## Referencias verificadas

| Regla | Archivo y línea |
|---|---|
| C1 | secuencia-solicitar-recojo.puml:51 |
| C2 | estados-solicitud.mmd:16 |
| C3 | clases.puml:88 |
| C4 | paquetes.puml:19 |
| C5 | ../../src/solicitudes/dominio.py:184 |
