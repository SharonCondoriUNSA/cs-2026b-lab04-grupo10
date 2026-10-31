# Bitácora de uso de IA: EcoRecicla AQP

## 1. Objetivo

Esta bitácora registra el uso de herramientas de Inteligencia Artificial durante el análisis y diseño de la arquitectura de EcoRecicla AQP.

Las propuestas generadas por IA fueron revisadas por el equipo antes de ser aceptadas, modificadas o rechazadas. La IA se utilizó como herramienta de apoyo y no como sustituto de la decisión del equipo.

---

## 2. Registro de interacciones

### Interacción 1: Evaluación de estilos arquitectónicos

**Herramienta:** ChatGPT

**Prompt / consulta:**  
Compara Monolito en Capas, Microservicios y Monolito Modular para EcoRecicla AQP. Considera que el MVP debe estar listo en un mes, el equipo es pequeño, existe un presupuesto bajo y la modificabilidad es el atributo de calidad crítico.

**Propuesta de la IA:**  
La IA comparó las tres alternativas y propuso el Monolito Modular como la opción más equilibrada, debido a que permite mantener un único despliegue y, al mismo tiempo, separar las funcionalidades mediante módulos con límites explícitos.

**Verificación del equipo:**  
El equipo contrastó la propuesta con los drivers arquitectónicos definidos en E1 y con los resultados de la matriz de decisión de E2. Se comprobó que Microservicios introduce una complejidad operativa innecesaria para el tamaño del equipo y el plazo disponible.

**Decisión:**  
Se aceptó el Monolito Modular como estilo arquitectónico para EcoRecicla AQP.

---

### Interacción 2: Revisión de la matriz de decisión

**Herramienta:** ChatGPT

**Prompt / consulta:**  
Revisa una matriz de decisión para EcoRecicla AQP considerando los criterios de modificabilidad, tiempo de entrega, costo de infraestructura, simplicidad DevOps, disponibilidad, rendimiento y usabilidad móvil.

**Propuesta de la IA:**  
La IA ayudó a revisar la relación entre los criterios, sus pesos y los drivers del sistema, comparando Monolito en Capas, Microservicios y Monolito Modular.

**Verificación del equipo:**  
El equipo verificó que los pesos sumaran 100 %, revisó los puntajes asignados y comprobó manualmente los cálculos ponderados. También se revisó que los criterios estuvieran relacionados con los requisitos, atributos de calidad y restricciones del proyecto.

**Decisión:**  
Se mantuvo al Monolito Modular como alternativa seleccionada al obtener el mejor equilibrio entre modificabilidad, tiempo de entrega, costo y simplicidad operativa.

---

### Interacción 3: Generación del diagrama PlantUML

**Herramienta:** ChatGPT

**Prompt / consulta:**  
Genera una propuesta de diagrama PlantUML para representar el Monolito en Capas como la segunda mejor alternativa arquitectónica descartada para EcoRecicla AQP.

**Propuesta de la IA:**  
La IA propuso representar una capa de presentación, una capa de lógica de negocio, una capa de acceso a datos, PostgreSQL y los servicios externos de mapas y WhatsApp.

**Verificación del equipo:**  
El equipo generó el diagrama mediante PlantUML en Visual Studio Code y comprobó visualmente que las dependencias respetaran la organización por capas y que los elementos representados fueran coherentes con los requisitos del sistema.

**Decisión:**  
Se aceptó la estructura general y se ajustó la presentación visual del diagrama antes de incorporarlo al repositorio.

---

### Interacción 4: Diagrama de despliegue con Python Diagrams

**Herramienta:** ChatGPT

**Prompt / consulta:**  
Propón un diagrama de despliegue para EcoRecicla AQP utilizando Python Diagrams. Debe mostrar los clientes, acceso por Internet, el VPS, el Monolito Modular, PostgreSQL y los servicios externos.

**Propuesta de la IA:**  
La IA propuso representar a los vecinos, municipalidad y recicladores como clientes; Internet mediante HTTPS; un VPS con la PWA + API REST y el Monolito Modular; PostgreSQL como almacenamiento; y las APIs de mapas y WhatsApp como servicios externos.

**Verificación del equipo:**  
El equipo instaló y verificó Graphviz y Python Diagrams, ejecutó el código y revisó el PNG generado. Se realizaron ajustes de distribución, etiquetas, tipografía e iconos para mejorar la legibilidad.

**Decisión:**  
Se aceptó la estructura de despliegue después de los ajustes realizados por el equipo y se generó la imagen final desde el código Python.

---

### Interacción 5: Corrección de una propuesta de IA

**Herramienta:** ChatGPT

**Prompt / consulta:**  
Agrega WhatsApp Business API como servicio externo en el diagrama de despliegue utilizando Python Diagrams.

**Propuesta de la IA:**  
Inicialmente la IA propuso importar un nodo `Whatsapp` desde `diagrams.saas.chat` para representar el servicio.

**Verificación del equipo:**  
Al ejecutar el código se obtuvo un `ImportError`, debido a que el nodo `Whatsapp` propuesto no estaba disponible en la versión instalada de Python Diagrams. El equipo verificó el problema mediante la ejecución real del código y descartó esa implementación.

Posteriormente se utilizó un icono local de WhatsApp mediante `Custom`, manteniendo el servicio identificado como “WhatsApp Business API”.

**Decisión:**  
Se rechazó la propuesta inicial de la IA y se reemplazó por una solución verificada que funciona correctamente con el entorno utilizado por el equipo.

---

## 3. Reflexión

El uso de IA permitió generar alternativas, revisar decisiones y acelerar la elaboración de los diagramas. Sin embargo, las respuestas no fueron aceptadas automáticamente.

Durante el laboratorio fue necesario contrastar las propuestas con los drivers arquitectónicos, realizar cálculos manuales, ejecutar el código generado y corregir propuestas incompatibles con las herramientas utilizadas.

El caso del nodo de WhatsApp evidenció la importancia de verificar técnicamente las respuestas generadas por IA antes de incorporarlas al proyecto. Por ello, las decisiones finales fueron tomadas por el equipo a partir de los requisitos, restricciones y resultados obtenidos durante las pruebas.

## Lab08 · E1 · Apoyo en escenarios y revisión (2026-10-31)

Prompt IA 1 adaptado y utilizado en esta sesión: «Actúa como arquitecto de EcoRecicla AQP. Usa drivers.md, ADR-001 y ADR-005. El caso crece de 3 a 12 distritos, con puntos y horarios propios. Propón escenarios de seis partes para rendimiento, disponibilidad, seguridad y modificabilidad, con medidas numéricas y calificación importancia/dificultad H/M/L. Respeta un mes, dos integrantes, presupuesto bajo y monolito modular. No propongas soluciones todavía».

Propuesta inicial: QA-01 (H,M) por las fábricas de Lab07. Corrección de la revisión técnica con apoyo de IA: (H,H), las fábricas seleccionan material y no resuelven ámbito distrital ni horarios. Se conservaron QA-01 a QA-03 y se añadieron QA-04 a QA-07 con supuestos explícitos. No se registra aprobación humana ni medición de producción. El árbol y la tabla documentan la propuesta para revisión del equipo.

Verificaciones E1: Graphviz generó arbol.png sin errores, se revisó visualmente el PNG y git diff --check pasó. Los cambios anteriores de despliegue.py y test_solicitudes.py se excluyen del commit.


## Lab08 · E2 · Apoyo en alternativas y prototipo (2026-10-31)

Prompt IA 2 adaptado y utilizado: «Para QA-01 de EcoRecicla, incorporar distritos con puntos y horario propios en ≤ 2 días-persona sin cambiar consumidores, propón al menos tres conceptos de diseño. Explica qué mejoran y empeoran, coste relativo y complejidad. Respeta dos integrantes, un mes, presupuesto bajo, ADR-001 y patrones ADR-005. Construye evidencia antes/después y distingue medidas de laboratorio de esfuerzo humano».

Se compararon condicionales, configuración versionada, despliegues separados y estrategias por distrito. Se propone configuración para tarifas y franjas representables y se rechazan los despliegues separados. La ejecución real del prototipo incorporó nueve distritos, pasó 24 comprobaciones y mantuvo las huellas de tres archivos consumidores. Cambiar D01 no alteró los otros once. La revisión corrigió una posible conclusión excesiva: ms de ejecución no equivalen a días-persona, QA-01 queda parcialmente verificado. No se modifica código de producción ni se declara una aprobación del equipo. Salida conservada en add/evidencia-1.json.

## Lab08 · E3 · Preparación, no evaluación realizada (2026-10-31)

El equipo indicó que el docente realizará la revisión y que no habrá evaluación entre grupos. Se actualizó atam-lite.md para registrar ese procedimiento y preparar la respuesta a las observaciones que envíe. No se abrió un issue a otro grupo ni se ejecutó el Prompt IA 3 como evaluación cruzada. La revisión del docente y la respuesta del equipo siguen pendientes.


## Lab08 · E4 · Apoyo en continuidad y aislamiento (2026-10-31)

Instrucción de trabajo aplicada a la iteración 2: «Refina QA-02 y QA-07 conservando PWA y monolito modular. Compara envío directo, reintentos en memoria y buffer persistente con receptor idempotente. Produce evidencia antes/después y una sensibilidad del límite de 30 s. No confundas SQLite local con IndexedDB o PostgreSQL reales».

Se adaptó la idea de experimentación del recurso docente al registro de recojos, sin copiar su flujo de pagos. El primer intento local no pudo abrir SQLite en el temporal del sandbox. La repetición con acceso autorizado ejecutó ambas variantes: 120 efectos únicos, 0 pérdidas y duplicados, 12 ACK perdidos. Con 100 ms por intento el reloj virtual arroja 13.2 s, con 250 ms arroja 33 s y el escenario falla. Se conserva esa sensibilidad, no se ajustaron cifras para ocultar el incumplimiento. La reapertura se describe como cierre normal, no como prueba de corte eléctrico.

Instrucción aplicada a la iteración 3: «Refina QA-04 y QA-05 para doce distritos. Compara alternativas respetando esquemas por módulo y prueba 132 pares cruzados, lecturas, escrituras y ámbitos ausentes. Separa la guarda local de autenticación real y RLS no implementados».

El prototipo denegó 264 operaciones cruzadas y 72 sin ámbito válido, permitió 24 propias y conservó los datos. El control negativo inseguro permite 132 lecturas y 132 escrituras, es sintético y no prueba una vulnerabilidad del Lab07. Se propone contexto autorizado y defensa RLS posterior, sin declarar tokens o políticas SQL ya implementados. No hay riesgo crítico recibido de otro grupo porque E3 sigue pendiente.

Verificaciones realizadas: ejecución de los tres prototipos, cuatro rechazos de configuración inválida, sintaxis Python y enlaces relativos nuevos. Las 138 pruebas de comportamiento y patrones del Lab07 siguen pasando. Se revisaron los resultados JSON y su correspondencia con las tablas ADD. git diff --check sin errores. No se incorpora la carpeta de ejemplos, los cambios anteriores ni entregables E5-E8.
