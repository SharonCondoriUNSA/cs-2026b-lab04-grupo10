# ADR-003: Adopción de Progressive Web App (PWA) para vecinos y recicladores

**Estado:** Aceptado  
**Fecha:** 2026-10-03  
**Decisores:** Equipo de desarrollo Grupo 10

## Contexto

EcoRecicla AQP requiere que los vecinos soliciten recojos (**RF-01**) y que los recicladores consulten sus rutas en movilidad (**RF-02**).

Los recicladores operan en ruta en distritos de Arequipa donde la conectividad móvil puede ser inestable o presentar caídas de señal (**QA-02**).

El equipo tiene restricción de plazo (1 mes, **R-01**) y 2 desarrolladores (**R-02**).

## Alternativas consideradas

1. **Aplicaciones nativas independientes (Android / iOS):** Excelente rendimiento, pero requiere mantener múltiples códigos base y excede el plazo de 1 mes y la capacidad del equipo (**R-01**, **R-02**).

2. **Progressive Web App (PWA) única e instalable:** Un solo código base web con soporte de Service Workers y almacenamiento local (IndexedDB) para operación sin conexión o con red inestable (**QA-02**).

## Decisión

Desarrollaremos la interfaz móvil y web utilizando una **Progressive Web App (PWA)** instalable.

Permitirá a los recicladores y vecinos registrar solicitudes de manera offline temporal cuando falle la red móvil, sincronizando los datos automáticamente al restablecerse la conexión (**QA-02**).

## Consecuencias

### Positivas

- Código único para web y móvil que acelera la entrega (**R-01**, **R-02**).
- No requiere pagos de licencias en tiendas de aplicaciones (**R-03**).
- Asegura la disponibilidad de registro de solicitudes ante caídas de red (**QA-02**).

### Negativas / riesgos

- Acceso limitado a ciertas APIs de hardware nativo avanzado en comparación con una aplicación nativa tradicional.