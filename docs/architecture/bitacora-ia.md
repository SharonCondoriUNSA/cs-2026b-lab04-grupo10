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