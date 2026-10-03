# Drivers arquitectónicos — EcoRecicla AQP

## 1. Requisitos funcionales clave

| ID | Requisito | Actor | Prioridad |
|---|---|---|---|
| RF-01 | Solicitar recojo de residuos reciclables indicando tipo y peso | Vecino | Alta |
| RF-02 | Visualizar la ruta del día y la lista de recojos asignados | Reciclador | Alta |
| RF-03 | Registrar las toneladas recicladas y validar las entregas | Reciclador | Alta |
| RF-04 | Acumular y consultar puntos canjeables por recojos verificados | Vecino | Alta |
| RF-05 | Generar reportes consolidados de toneladas recicladas por distrito | Municipalidad | Media |

## 2. Atributos de calidad (ordenados por prioridad)

- **Modificabilidad** — Es el atributo crítico porque el sistema debe permitir incorporar nuevos distritos o nuevas reglas de canje de puntos sin modificar los demás módulos.

- **Disponibilidad** — Las solicitudes de recojo deben registrarse y no perderse ante fallas temporales de servicios externos.

- **Rendimiento** — Las consultas de rutas deben responder rápidamente durante las horas pico de recojo.

- **Capacidad de interacción (Usabilidad)** — La interfaz debe ser ágil y accesible para recicladores que utilizan dispositivos móviles durante sus rutas.

## 3. Restricciones

| ID | Tipo | Restricción |
|---|---|---|
| R-01 | Plazo | El MVP debe estar en producción en un máximo de 1 mes. |
| R-02 | Equipo | Máximo 3 integrantes en el equipo, utilizando tecnologías que ya dominan. |
| R-03 | Presupuesto | Presupuesto bajo; se debe priorizar infraestructura de bajo costo. |
| R-04 | Normativa | Cumplimiento de la Ley 29733 de Protección de Datos Personales. |

## 4. Escenarios de atributos de calidad

| ID | Atributo | Fuente | Estímulo | Entorno | Artefacto | Respuesta | Medida |
|---|---|---|---|---|---|---|---|
| QA-01 | Modificabilidad | Municipalidad | Solicita incorporar un nuevo distrito | Desarrollo | Módulo de Cobertura | Se añade la lógica de asignación geográfica sin modificar los demás módulos | Implementación en ≤ 2 días-persona |
| QA-02 | Disponibilidad | Vecino | Envía una solicitud de recojo cuando un servicio externo no responde | Operación normal | Módulo de Solicitudes | La solicitud se guarda localmente y se reintenta posteriormente | 0 solicitudes perdidas; reintento ≤ 10 min |
| QA-03 | Rendimiento | Reciclador | Consulta la ruta optimizada del día | Hora pico (7:00–9:00 a. m.) | Módulo de Rutas | Devuelve la lista ordenada de puntos de recojo | p95 ≤ 2 segundos |