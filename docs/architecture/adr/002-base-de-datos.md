# ADR-002: Elección de PostgreSQL con esquemas aislados por módulo

**Estado:** Aceptado  
**Fecha:** 2026-10-03  
**Decisores:** Equipo de desarrollo Grupo 10

## Contexto

Se requiere almacenar la información operacional de EcoRecicla AQP: solicitudes de recojo (**RF-01**), asignación de rutas geográficas (**RF-02**), transacciones de puntos acumulados (**RF-04**) y reportes de toneladas recicladas (**RF-05**).

La solución debe ser económica (**R-03**) y mantener la modificabilidad e independencia de módulos (**QA-01**).

## Alternativas consideradas

1. **MongoDB (Base de datos NoSQL documental):** Flexible para documentos JSON, pero carece de soporte nativo para consultas relacionales complejas y consistencia estricta en transacciones de puntos.

2. **Bases de datos independientes por módulo (Múltiples instancias SQL):** Brinda aislamiento estricto, pero incrementa los costos y el consumo de memoria RAM en un VPS económico (**R-03**).

3. **PostgreSQL con esquemas aislados por módulo (Relacional):** Una sola instancia de PostgreSQL organizada en esquemas lógicos independientes (`solicitudes`, `rutas`, `puntos`, `reportes`).

## Decisión

Usaremos **PostgreSQL** dentro de una sola instancia de servidor, aplicando **esquemas lógicos independientes por módulo** para garantizar el aislamiento de datos y facilitar la consistencia en el registro de solicitudes y canje de puntos.

## Consecuencias

### Positivas

- Bajo costo de infraestructura (**R-03**).
- Fuerte consistencia ACID para la acumulación y canje de puntos (**RF-04**).
- Aislamiento lógico que evita dependencias cruzadas entre módulos (**QA-01**).

### Negativas / riesgos

- Al compartir la misma instancia física de base de datos, una falla grave a nivel de servidor impactaría a todos los módulos.