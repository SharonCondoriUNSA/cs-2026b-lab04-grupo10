# ADR-001: Uso de Monolito Modular

Estado: Aceptado  
Fecha: 2026-10-03  
Decisores: Equipo del proyecto

## Contexto

EcoRecicla AQP necesita implementar un MVP en producción en un plazo máximo de un mes (R-01), considerando además un presupuesto bajo y un equipo de máximo tres desarrolladores (R-02).

El sistema debe permitir incorporar nuevos distritos o nuevas reglas de canje de puntos en un máximo de dos días-persona sin modificar otros módulos, por lo que la modificabilidad es el atributo de calidad crítico (QA-01).

Además, el sistema debe registrar solicitudes de recojo, gestionar rutas, administrar puntos y generar reportes de toneladas recicladas (RF-01, RF-02, RF-03 y RF-04).

## Alternativas consideradas

1. Monolito en Capas
2. Microservicios
3. Monolito Modular

## Decisión

Usaremos una arquitectura de **Monolito Modular**, organizando el sistema en módulos de dominio con límites explícitos.

Los principales módulos serán:

- Módulo de Solicitudes y Recojo.
- Módulo de Rutas y Cobertura.
- Módulo de Puntos y Beneficios.
- Módulo de Reportes de Toneladas.

Esta alternativa permite mantener una estructura modular y facilitar cambios futuros, sin agregar la complejidad de infraestructura y despliegue propia de una arquitectura de microservicios.

## Consecuencias

### Positivas

- Facilita la incorporación de nuevos distritos y reglas de puntos.
- Permite separar claramente las responsabilidades del sistema.
- Reduce la complejidad de despliegue y operación.
- Se adapta al plazo de un mes para desarrollar el MVP.
- Requiere una infraestructura más sencilla y económica.

### Negativas / riesgos

- Un fallo en el despliegue del monolito puede afectar a todo el sistema.
- Los módulos comparten el mismo despliegue.
- A medida que el sistema crezca, será necesario mantener estrictamente los límites entre módulos para evitar dependencias innecesarias.