# Matriz de decisión de estilos arquitectónicos — EcoRecicla AQP

## 1. Alternativas de estilo consideradas

- **A. Monolito en Capas (n-tier):** Descomposición del sistema en capas tradicionales (Presentación, Lógica de Negocio y Acceso a Datos) desplegadas en un único servidor. Ofrece alta simplicidad inicial, pero es propenso al acoplamiento entre capas a medida que evoluciona el sistema.

- **B. Microservicios:** Descomposición del sistema en servicios independientes por dominio (Solicitudes, Rutas, Puntos/Canjes, Reportes), cada uno con su propia base de datos. Brinda aislamiento total y alta escalabilidad, pero genera una complejidad operativa excesiva para un equipo pequeño de 3 personas.

- **C. Monolito Modular (Elegido):** Un solo despliegue físico organizado internamente en módulos de dominio con límites explícitos e interfaces bien definidas. Mantiene la simplicidad operativa de un solo servidor garantizando alta modificabilidad.

## 2. Criterios de evaluación y pesos (Suma = 100 %)

| Criterio | Peso | Justificación (Driver relacionado) |
| :--- | :---: | :--- |
| **1. Modificabilidad** | 25 % | **QA-01 (Atributo Crítico):** Requisito del Caso 10 para incorporar nuevos distritos de Arequipa o reglas de puntos en ≤ 2 días-persona sin alterar otros módulos. |
| **2. Tiempo de entrega** | 20 % | **R-01:** Restricción estricta de tener el MVP listo y desplegado en producción en máximo 1 mes. |
| **3. Costo de infraestructura** | 15 % | **R-03:** Presupuesto bajo; infraestructura basada en un solo VPS económico. |
| **4. Simplicidad DevOps** | 15 % | **R-02:** El equipo de 3 integrantes debe enfocarse en la lógica de negocio sin sobrecarga de gestión de servidores. |
| **5. Disponibilidad y tolerancia a fallos** | 10 % | **QA-02:** Registro seguro de solicitudes de recojo aun ante caídas temporales de servicios externos o red móvil. |
| **6. Rendimiento y latencia** | 10 % | **QA-03:** Consultas fluidas del mapa de rutas en horas pico de recojo (p95 ≤ 2 segundos). |
| **7. Usabilidad móvil** | 5 % | Interfaz ágil e integración directa con las aplicaciones para recicladores en ruta y vecinos. |

## 3. Matriz de decisión ponderada

**Puntaje: 1 = Muy malo, 2 = Malo, 3 = Regular, 4 = Bueno, 5 = Excelente**


| Criterio (Peso) | A. Capas | B. Microservicios | C. Monolito Modular | Justificación de puntajes |
| :--- | :---: | :---: | :---: | :--- |
| **1. Modificabilidad** (25 %) | 2 | 5 | 4 | Capas tiende a acoplarse; Microservicios aísla totalmente; Monolito Modular aísla con límites explícitos. |
| **2. Tiempo de entrega** (20 %) | 5 | 2 | 4 | Capas es el más rápido inicialmente; Microservicios requiere configurar comunicación de red; Monolito Modular permite avance modular paralelo. |
| **3. Costo de infraestructura** (15 %) | 5 | 2 | 5 | Un solo VPS económico para Capas y Monolito Modular; Microservicios requiere múltiples instancias/contenedores. |
| **4. Simplicidad DevOps** (15 %) | 5 | 1 | 4 | Capas y Monolito Modular usan un solo pipeline CI/CD; Microservicios exige orquestación y service mesh. |
| **5. Disponibilidad** (10 %) | 2 | 4 | 3 | Microservicios aísla fallos de proceso; Monolito Modular requiere colas o almacenamiento local para mitigar caídas. |
| **6. Rendimiento / Latencia** (10 %) | 4 | 3 | 4 | Monolito Modular y Capas ejecutan llamadas en memoria; Microservicios agrega latencia de red inter-servicio. |
| **7. Usabilidad móvil** (5 %) | 3 | 4 | 4 | Monolito Modular y Microservicios ofrecen APIs REST limpias adaptadas a clientes móviles. |
| **TOTAL PONDERADO** | **3.75** | **3.00** | **4.05** | **Gana la Alternativa C: Monolito Modular** |

### Cálculo detallado de los totales

- **Monolito en Capas (A):**

  $(0.25 \times 2) + (0.20 \times 5) + (0.15 \times 5) + (0.15 \times 5) + (0.10 \times 2) + (0.10 \times 4) + (0.05 \times 3) = 0.50 + 1.00 + 0.75 + 0.75 + 0.20 + 0.40 + 0.15 = \mathbf{3.75}$

- **Microservicios (B):**

  $(0.25 \times 5) + (0.20 \times 2) + (0.15 \times 2) + (0.15 \times 1) + (0.10 \times 4) + (0.10 \times 3) + (0.05 \times 4) = 1.25 + 0.40 + 0.30 + 0.15 + 0.40 + 0.30 + 0.20 = \mathbf{3.00}$

- **Monolito Modular (C):**

  $(0.25 \times 4) + (0.20 \times 4) + (0.15 \times 5) + (0.15 \times 4) + (0.10 \times 3) + (0.10 \times 4) + (0.05 \times 4) = 1.00 + 0.80 + 0.75 + 0.60 + 0.30 + 0.40 + 0.20 = \mathbf{4.05}$

## 4. Conclusión

Seleccionamos la alternativa de **Monolito Modular** (puntaje **4.05**) debido a que satisface de forma equilibrada la restricción de entrega en 1 mes (**R-01**) y el bajo costo (**R-03**), garantizando el atributo crítico de **Modificabilidad (QA-01)** al delimitar los módulos mediante contratos explícitos.

Para mayores detalles sobre las decisiones de diseño derivadas de esta elección, consultar el [ADR-001: Estilo arquitectónico](adr/001-estilo-arquitectonico.md).