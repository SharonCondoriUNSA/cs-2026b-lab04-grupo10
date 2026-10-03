# ADR-001: Adopción del estilo Monolito Modular para EcoRecicla AQP

**Estado:** Aceptado  
**Fecha:** 2026-10-03  
**Decisores:** Equipo de desarrollo Grupo 10

## Contexto

El sistema EcoRecicla AQP debe lanzarse como un MVP en un plazo de 1 mes (**R-01**) con un equipo reducido de 2 desarrolladores (**R-02**) y bajo presupuesto de infraestructura (**R-03**).

Además, el atributo de calidad crítico del sistema es la **Modificabilidad (QA-01)**, requiriendo la integración de nuevos distritos de Arequipa o reglas de canje de puntos sin alterar otros componentes del sistema.

## Alternativas consideradas

1. **Monolito en Capas (n-tier):** Construcción rápida inicial, pero propenso al acoplamiento entre capas a medida que evoluciona el sistema.

2. **Microservicios:** Aislamiento total de servicios, pero genera una complejidad operativa inmanejable para un equipo de 3 desarrolladores.

3. **Monolito Modular:** Despliegue único dividido en módulos independientes por dominio con contratos e interfaces explícitas.

## Decisión

Usaremos el estilo **Monolito Modular** organizado en módulos delimitados:

- Solicitudes
- Rutas/Cobertura
- Puntos/Beneficios
- Reportes

Cada módulo expondrá interfaces públicas estrictas de aplicación y mantendrá su propio esquema de datos.

## Consecuencias

### Positivas

- Despliegue sencillo en un único VPS (**R-03**).
- Entrega rápida del MVP (**R-01**).
- Aislamiento de módulos que facilita modificar o añadir distritos (**QA-01**).
- Permite una migración futura a microservicios si el volumen de carga crece.

### Negativas / riesgos

- Requiere disciplina en el equipo para no acoplar los módulos mediante importaciones directas no autorizadas.