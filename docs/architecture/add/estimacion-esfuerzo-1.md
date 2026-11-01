# E2. Estimación del esfuerzo de incorporar un distrito

Fecha: 2026-11-01. Origen: observación de revisión de la compañera sobre QA-01. **Es una estimación de ingeniería propuesta con apoyo de IA, no un registro de horas trabajadas ni una estimación ya aprobada por el equipo.**

## Alcance y unidad

Se estima el alta de **un distrito** con una tarifa por material y una franja de recojo representables por los contratos de la iteración 1. Incluye aclarar la regla, configurar, conectar con persistencia, verificar permisos, probar, revisar y publicar. La revisión de ambas integrantes se suma al esfuerzo, no se divide entre dos personas.

Se adopta para esta comparación **1 día-persona = 8 horas-persona**, por tanto QA-01 permite **16 horas-persona**. Es una convención explícita de planificación, no una jornada establecida por la guía. Días-persona expresan esfuerzo acumulado, no plazo calendario.

Supuestos de aplicabilidad:

- Tarifas, materiales, horario y autorización municipal están definidos antes de comenzar. No se necesitan feriados, turnos nocturnos ni una fórmula nueva.
- Los mecanismos genéricos de configuración versionada, API, repositorios, autorización y despliegue están disponibles para reutilizarse. Se incluye conectar y verificar el nuevo distrito en ellos, no construirlos desde cero.
- El equipo conoce los módulos y tiene un entorno de pruebas disponible. No se migra información histórica ni se modifica el código de consumidores.
- No hay integración con un proveedor nuevo ni cambios legales o de infraestructura. Las esperas de aprobación externas no son horas de trabajo, aunque sí pueden alargar el calendario.

**El repositorio actual contiene un prototipo, no todos esos mecanismos integrados.** Esta estimación aplica al alta cuando exista esa base reutilizable. El trabajo inicial para habilitarla requiere una estimación aparte y no se oculta dentro de las horas del alta. Si QA-01 se interpreta como integrar el primer distrito desde el estado actual, todavía no se acredita su cumplimiento.

## Desglose reproducible

Los valores siguientes son juicios de planificación para un cambio pequeño, no duraciones deducidas de los milisegundos del prototipo. O es optimista, M más probable y P pesimista. Otra persona puede revisar cada partida y recalcular el resultado con la misma fórmula.

| Actividad y resultado verificable | O (h-persona) | M (h-persona) | P (h-persona) |
|---|---:|---:|---:|
| Confirmar tarifa, material y horario, dejar criterios del alta | 0.5 | 1 | 1.5 |
| Preparar configuración versionada y validaciones del distrito | 1 | 1.5 | 2.5 |
| Integrar la configuración con los repositorios y su publicación transaccional | 1 | 2 | 3 |
| Conectar permisos distritales y comprobar rechazos de accesos ajenos | 0.5 | 1 | 2 |
| Probar reglas, horarios, reversión y regresión de los otros once distritos | 1 | 2 | 3 |
| Revisar el cambio entre integrantes y corregir observaciones | 1 | 1.5 | 2 |
| Publicar, comprobar el alta y documentar versión y reversión | 0.5 | 1 | 2 |
| **Total** | **5.5** | **10** | **16** |

Las tareas no son mediciones independientes de una distribución estadística conocida. PERT sirve aquí como regla de cálculo auditable, no como intervalo de confianza ni garantía probabilística.

## Cálculo y comparación con QA-01

Se usa `E = (O + 4 × M + P) / 6` y una reserva explícita del 25 % para retrabajo no detallado. Aplicar la fórmula a los totales equivale a sumar la estimación de cada tarea.

| Paso | Cálculo | Resultado |
|---|---|---:|
| Esfuerzo ponderado | (5.5 + 4 × 10 + 16) / 6 | 10.25 h-persona |
| Reserva | 10.25 × 0.25 | 2.5625 h-persona |
| Estimación con reserva | 10.25 × 1.25 | 12.8125 h-persona |
| Conversión a días-persona | 12.8125 / 8 | 1.6015625, aproximadamente **1.60 días-persona** |
| Margen frente al límite | 16 − 12.8125 | 3.1875 h-persona |
| Sensibilidad pesimista con reserva | 16 × 1.25 / 8 | **2.50 días-persona**, supera el límite |

**Conclusión:** el alta reutilizando mecanismos disponibles es compatible con QA-01 en la estimación central, **1.60 ≤ 2 días-persona**. No queda garantizada, el escenario pesimista llega a 2.50. Se mantiene la evidencia estructural de 0 cambios en consumidores, pero no se declara cumplimiento empírico del esfuerzo ni del primer desarrollo de esos mecanismos.

Si cambia la convención de jornada, también cambia la comparación. Por ejemplo, con 6 horas por día-persona, 12.8125 / 6 = 2.1354 y la estimación central supera 2 días-persona. La convención debe ser revisada por el equipo antes de adoptar el presupuesto.

## Cómo contrastar la estimación con una medición real

En el siguiente alta, cada integrante registrará inicio, fin y tiempo activo por actividad, incluyendo revisión y correcciones. Se suman las horas-persona de ambas, se convierten con la jornada acordada y se comparan con 16 horas-persona. Se adjuntarán commit inicial y final, configuración, pruebas y aprobación. La construcción previa de mecanismos genéricos se registrará por separado y se indicará si el criterio evaluado la incluye. Estos registros están pendientes, no se completan con valores ficticios.

Referencias: [iteración 1](iteracion-1.md), [salida del experimento estructural](evidencia-1.json) y [QA-01](../utilidad/escenarios.md).
