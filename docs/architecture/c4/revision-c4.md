# E7: Revisión de las cinco vistas C4

Fecha: 18/10/2026. Revisión documental asistida por Codex en esta sesión, pendiente de revisión de la compañera. Se aplica la Tabla 3 de la guía y la [lista oficial C4](https://c4model.com/diagrams/checklist).

Se revisan `workspace.dsl`, los cinco `.puml` de `export/` y sus PNG de `img/`, generados y observados en E6. Las exportaciones Mermaid existen, pero no se afirma haberlas renderizado. Los resultados siguientes corresponden a las figuras PNG de C4-PlantUML. Sí indica cumplimiento de la pregunta, No identifica una limitación concreta. En el nivel 1, las tecnologías internas no corresponden al alcance.

## Lista aplicada a cada vista

| Pregunta de revisión | Contexto | Contenedores | Componentes | Dinámica | Despliegue | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| ¿Tiene título? | Sí | Sí | Sí | Sí | Sí | Primera directiva `title` de cada archivo exportado y encabezado del PNG. |
| ¿Se reconoce el tipo? | Sí | Sí | Sí | Sí | Sí | Contexto, contenedores y componentes en los títulos, pasos numerados en dinámica y nodos anidados en despliegue. |
| ¿Se identifica el alcance? | Sí | Sí | Sí | Sí | Sí | `ecorecicla`, `ecorecicla`, `api`, `api` y entorno `produccion`, respectivamente, en el DSL. |
| ¿Tiene leyenda? | Sí | Sí | Sí | Sí | Sí | `SHOW_LEGEND(true)` y leyendas visibles en los cinco PNG. |
| ¿Cada elemento tiene nombre? | Sí | Sí | Sí | Sí | Sí | Argumentos de `Person`, `System`, `Container`, `Component` y `Deployment_Node`. |
| ¿Se entiende el tipo de elemento? | Sí | Sí | Sí | Sí | Sí | Personas con ícono, niveles por límites rotulados, base de datos cilíndrica y nodos anidados, junto con sus leyendas. |
| ¿Se entiende su responsabilidad? | Sí | Sí | Sí | Sí | Sí | Descripciones `$descr` visibles dentro de los elementos y nodos. |
| ¿Se muestra la tecnología cuando corresponde? | Sí | Sí | Sí | Sí | Sí | El contexto omite tecnologías internas por su alcance. Las demás vistas muestran Python, PostgreSQL y tecnologías de PWA, y despliegue añade sistema operativo y capacidad propuesta. |
| ¿Se explican todos los acrónimos de los elementos? | Sí | No | No | No | No | PWA se desarrolla como Aplicación Web Progresiva. API, REST, UUID y unidades del VPS no se expanden en todas las figuras, véase el glosario de esta revisión. |
| ¿Se entienden los colores? | Sí | Sí | Sí | Sí | Sí | Leyendas de etiquetas, `Externo` gris y colores definidos en `styles`, conservados con `c4plantuml.tags`. |
| ¿Se entienden formas e íconos? | Sí | Sí | Sí | Sí | Sí | Ícono de persona, cilindro para datos, cajas para aplicaciones y componentes. No se introducen íconos de proveedores. |
| ¿Se entienden bordes y tamaños de los elementos? | Sí | Sí | Sí | Sí | Sí | Los límites llevan el nombre y nivel del sistema o contenedor. El tamaño se adapta al texto, no expresa carga ni importancia. |
| ¿Cada flecha describe su intención? | Sí | Sí | Sí | Sí | Sí | Etiquetas `Rel`, desde solicitar recojo hasta persistir o consultar contratos. |
| ¿La descripción coincide con la dirección? | Sí | Sí | Sí | Sí | Sí | PWA envía a API o Solicitudes, Reportes consulta a Solicitudes y la API escribe en datos. Los retornos se omiten en estas vistas. |
| ¿Se indica el protocolo cuando corresponde? | Sí | Sí | Sí | Sí | Sí | En contexto las relaciones son de intención. Las comunicaciones entre procesos indican HTTPS/JSON o SQL/TCP y las internas identifican contratos o tipos compartidos. |
| ¿Se explican todos los acrónimos de las relaciones? | Sí | No | No | No | No | HTTPS, JSON, SQL y TCP están rotulados, pero no se desarrollan dentro de cada figura, véase glosario. |
| ¿Se entienden colores y puntas de flecha? | Sí | Sí | Sí | Sí | Sí | Flechas del solicitante de la colaboración hacia su destino. No se usa el color para afirmar éxito, error o asincronía. |
| ¿Se explica inequívocamente el estilo de línea? | No | No | No | No | No | El exportador genera relaciones discontinuas, pero la muestra de línea de la leyenda aparece continua. No debe interpretarse ese trazo como prueba de asincronía. |

## Verificación cruzada y hallazgos

| Vista | Hallazgo del auditor | Cumple | Evidencia y decisión |
| --- | --- | --- | --- |
| Contexto | La ausencia de protocolos en las relaciones con personas incumpliría la lista. | Sí | Falso positivo descartado al comprobar el alcance: el contexto describe intención y la lista exige tecnologías cuando corresponde. No se agregan protocolos a las personas en nivel 1. Esta hipótesis fue evaluada por Codex en esta misma sesión, no se atribuye a otra IA ni a una revisión humana. |
| Contenedores | La falta de Redis y un worker impediría cumplir C4. | Sí | Hipótesis descartada: C4 no obliga a usar una cola. Los tres contenedores corresponden a los ADR-001, ADR-002 y ADR-003. La asincronía no implica por sí sola Redis ni entrega garantizada. |
| Componentes | Deben coincidir los paquetes y evitar ciclos. | Sí | Seis componentes y nueve dependencias internas, iguales a `docs/design/paquetes.puml`, usando contratos públicos. Notificaciones es auxiliar de Solicitudes y Compartido contiene tipos, no un módulo de negocio adicional. |
| Dinámica | Cada paso debe usar una relación estática existente. | Sí | Cinco pasos entre PWA, Solicitudes, Rutas/Cobertura, mapas, datos y Notificaciones. Cobertura y datos válidos son precondiciones, mapas puede fallar sin impedir guardar y el aviso sigue a la persistencia. |
| Despliegue | Debe existir una instancia de cada contenedor de nivel 2. | Sí | Tres `containerInstance`, PWA en el dispositivo y API y PostgreSQL en un solo VPS, en `Producción`. El tamaño es una propuesta y no acredita una contratación ni una prueba de carga. |
| Componentes | La cantidad de relaciones dificulta una lectura rápida. | No | La figura tiene cruces y etiquetas próximas a límites. Consultarla a tamaño completo, no afirmar que la composición visual es perfecta. |
| Todas | La existencia de leyenda no garantiza que todas las convenciones se entiendan sin contexto. | No | Acrónimos técnicos y discrepancia de trazo registrados en la tabla. El glosario y la aclaración ayudan, pero no sustituyen una mejora futura de la leyenda dentro de cada imagen. |

## Glosario y convenciones de lectura

- PWA: aplicación web progresiva. API: interfaz de programación de aplicaciones. REST: estilo de transferencia de estado representacional.
- HTTPS: protocolo HTTP sobre conexión segura. JSON: formato de intercambio de datos. SQL: lenguaje de consulta de datos relacionales. TCP: protocolo de transporte de red.
- UUID: identificador universal único. VPS: servidor privado virtual. vCPU: procesador virtual. RAM: memoria de trabajo. SSD: almacenamiento de estado sólido. GB: gigabytes.
- Las líneas indican colaboraciones dirigidas, su trazo discontinuo no significa necesariamente envío asíncrono. La asincronía se declara en el texto de la relación o del paso.
- El tamaño de una caja responde a su texto y a la distribución automática. No representa capacidad, costo ni número de usuarios.

## Explicación y conclusión

`explicacion.md` adapta el Prompt IA 3 a la administración municipal. Se contrastan sus afirmaciones con las tres personas, el sistema principal, los dos servicios externos y las cinco relaciones del contexto. No promete reintentos, disponibilidad absoluta, entrega garantizada ni una implementación completa.

El modelo pasa la validación estructural y conserva la coherencia con los ADR y el Lab05. La revisión no equivale a una aprobación humana ni a una prueba del sistema en producción. Se mantienen identificadas las limitaciones de notación, legibilidad y renderización Mermaid para la revisión del equipo.
