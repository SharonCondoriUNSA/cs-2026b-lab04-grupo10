# Bitácora IA, Lab07

Se utilizó Codex como apoyo para elaborar propuestas de código y pruebas, revisar los patrones y explicar sus decisiones. Se conservan los prompts utilizados y los resultados comprobados.

## E1, línea base y detector de olores, 25/10/2026

- **Herramienta:** Codex.
- **Solicitud recibida:** Desarrollar primero E1 de EcoRecicla AQP siguiendo la guía y los recursos AgroConecta como referencia, conservar la estructura del repositorio. E2-E4 se trabajarán posteriormente y E5-E8 corresponden a la compañera.
- **Instrucción de elaboración aplicada:** Implementa una versión ingenua del registro de recojo según la secuencia del Lab05, con dos servicios de mapas simulados y firmas distintas. Mantén la cobertura interna y el registro PENDIENTE cuando falle mapas. Prepara el ciclo de estados y el cálculo posterior de puntos, con tarifas de prueba configurables y sin trasladar el cálculo fuera de Puntos/Beneficios. Añade al menos ocho pruebas de caracterización con fixture parametrizado, mide la complejidad real y aplica el Prompt IA 1, sin refactorizar todavía.
- **Propuesta:** Servicio de Solicitudes con condicionales y reintentos duplicados, módulo interno de puntos con selección por material, repositorio y buzón de eventos en memoria. No se modifica dominio.py del Lab05. El prompt de revisión adaptado y su tabla de resultados están completos en olores.md.
- **Verificación:** 28 caracterizaciones aprobadas. Radon registró complejidad 25 en solicitar_recojo y 9 en acreditar. La salida está en radon-antes.txt. La comprobación conjunta con las siete pruebas locales del Lab05 también pasó.
- **Decisión:** Conservar la línea base para comparar, preparar los patrones justificados y rechazar Abstract Factory por ausencia de familias de productos. Tarifas, redondeo y reintentos son supuestos documentados del ejercicio.

## E2, Strategy, Adapter y Factory, 25/10/2026

- **Herramienta:** Codex.
- **Solicitud recibida:** Continuar con E2 tras subir E1 para revisión por Pull Request.
- **Prompt IA 2 adaptado y utilizado:** Aplica únicamente Strategy, Adapter y Factory por registro a la versión antes de EcoRecicla AQP. Usa Strategy para la variación principal de reglas de puntos y Adapter para las interfaces simuladas de mapas. Conserva comportamiento observable, mensajes de error, tarifas y truncamiento, estados, datos guardados y eventos de test_comportamiento.py. No introduzcas Singleton, estado global, State, Observer ni Decorator. Deja antes/ intacta, añade la versión refactorizada al fixture y demuestra una variante nueva sin modificar los servicios. Explica en tres líneas el olor eliminado.
- **Propuesta aplicada:** Se crean puertos pequeños, adaptadores de mapas y registros de constructores por instancia. El servicio de puntos delega a ReglaPuntos, las tarifas existentes comparten PuntosPorPeso porque no difieren de algoritmo. Se conservan los módulos y el contrato público entre Solicitudes y Puntos/Beneficios, sin compartir entidades. La versión después se coloca directamente en src/solicitudes y src/puntos_beneficios, siguiendo la estructura de la guía.
- **Verificación:** 78 casos aprobados sobre ambas versiones y los patrones. Se comprobó la extensión mediante registros y la traducción de los adaptadores sin reglas de negocio.
- **Decisión:** Conservar Strategy, Adapter y Factory. Una regla nueva de puntos no amplía automáticamente el catálogo de materiales. State, Observer y Decorator se reservan para E3 y E4.

## E3, State de solicitudes, 25/10/2026

- **Herramienta:** Codex.
- **Solicitud recibida:** Continuar con E3 después de preparar el PR de E2.
- **Instrucción aplicada:** Implementa únicamente State usando estados-solicitud.mmd del Lab05. La clase base debe prohibir las transiciones y las clases concretas permitir solo las correspondientes. Mantén cinco estados de dominio, todas las operaciones del diagrama, las guardas y las etiquetas observables. Delega desde Solicitudes al objeto estado y conserva las pruebas antes/después, sin agregar Observer ni Decorator ni modificar la versión antes.
- **Propuesta:** Se crea estados.py con base prohibitiva, cinco estados concretos y pseudoinicio y pseudofinal. La entidad en modelos.py almacena el objeto de estado, conserva la interfaz de construcción de E1 y expone operaciones delegadas. El servicio deja de comparar nombres de estado. Puntos/Beneficios sigue calculando, Solicitudes solo confirma la acreditación.
- **Verificación:** 110 casos aprobados. Se comprobaron el ciclo completo, transiciones prohibidas y guardas sin modificación de datos al fallar.
- **Decisión:** Se conserva State y la compatibilidad de las propiedades públicas usadas por las pruebas. SinRegistrar y Finalizada son pseudoelementos, no nuevas etiquetas de negocio. La versión antes y el modelo del Lab05 quedan intactos, Observer y Decorator se reservan a E4. Pendiente de revisión de la compañera.

## E4, Observer y Decorator, 25/10/2026

- **Herramienta:** Codex.
- **Solicitud recibida:** Desarrollar E4 después de preparar el PR de E3.
- **Instrucción aplicada:** Reemplaza los avisos agregados a mano por Observer con al menos dos suscriptores y extrae los reintentos caracterizados en E1 a un Decorator del puerto de mapas. Mantén resultados, estados, errores y orden de eventos observables. Agrega pruebas para ambos patrones y conserva la versión antes, sin implementar E5-E8.
- **Propuesta:** Publicador por instancia con eventos inmutables y dos suscriptores predeterminados, AvisosInternos y ProyeccionPesajes. Se permite suscribir consumidores adicionales y se registran errores para que un fallo no revierta la persistencia ni impida invocar otros consumidores. ConReintentos envuelve el puerto de mapas y conserva tres intentos ante fallos transitorios, sin repetir respuestas negativas ni efectos de acreditación.
- **Verificación:** 122 casos aprobados. Se verificaron dos suscriptores, publicación después de persistir, aislamiento de fallos y reintentos limitados a errores transitorios.
- **Decisión:** Aplicar Decorator a los reintentos ya identificados en E1. Observer conserva el buzón local de eventos, sin envíos externos ni garantía de entrega durable.

## E5, aislamiento del componente de IA, 25/10/2026

- **Herramienta:** La inteligencia artificial utilizada fue GPT.
- **Prompt:** Ayúdame a comprender el E5 de EcoRecicla AQP y oriéntame durante su desarrollo. Explícame cómo aislar la clasificación de residuos detrás de ProveedorLLM, con un adaptador, caché Decorator y dos o más guardrails. Considera el catálogo actual (PLASTICO y PAPEL), sugiere pruebas con un LLM simulado y cuida la compatibilidad con E1-E4. Presenta una propuesta razonada que pueda revisar y adaptar; evita servicios reales, claves y cambios ajenos a E5.
- **Propuesta:** Se agregó ClasificadorResiduo en src/solicitudes/ia.py, con Adapter para un cliente invoke(prompt).content, caché en memoria del resultado validado y guardrails para entrada vacía, longitud máxima y categoría de salida. NO_CLASIFICABLE solicita revisión manual y no se acepta como material para registrar una solicitud. Se dejó el clasificador aislado del servicio de solicitudes.
- **Corrección detectada por una prueba:** La prueba de caché con descripciones de longitud diferente pero texto equivalente tras normalizar espacios falló inicialmente. La caché consultaba su clave antes de comprobar la longitud de la entrada original. Se movieron los guardrails de entrada antes de la búsqueda en caché; la descripción excesiva ahora se rechaza incluso si su forma normalizada ya existe.
- **Verificación:** La suite de E1-E5 ejecutada con proveedores simulados terminó con 138 pruebas aprobadas. La prueba de regresión pasa y git diff --check no reportó errores.
- **Decisión:** Conservar Strategy/Adapter para intercambiar el proveedor, Decorator para cachear solo clasificaciones validadas y la cadena de guardrails para bloquear entradas y salidas inválidas. No se integró un LLM real; no se guardan datos ni claves externas.


## E7, diagramas de patrones y clases, 25/10/2026

- **Herramienta:** La inteligencia artificial utilizada fue GPT.
- **Prompt:** Ayúdame a entender y completar E7 del Lab07 de EcoRecicla AQP. Oriéntame para identificar los patrones GoF realmente aplicados en E2-E5 y diagramar sus clases con estereotipos PlantUML. Ayúdame también a actualizar el diagrama de clases de Lab05 para que represente el código vigente, contrastándolo con Pyreverse; conserva los artefactos anteriores, genera PNG desde los fuentes y señala cualquier diferencia entre el modelo conceptual y las clases implementadas. No inventes clases ni relaciones que no estén en el repositorio.
- **Propuesta:** Se prepararon siete diagramas PlantUML, uno por patrón aplicado: Strategy, Adapter, Factory, State, Observer, Decorator y Chain of Responsibility. El diagrama Decorator presenta por separado el envoltorio de reintentos de mapas y la caché del clasificador. Se actualizó docs/design/clases.puml para el código E1-E5, manteniendo los artefactos conceptuales anteriores del Lab05.
- **Verificación:** PlantUML generó los siete PNG de patrones y la nueva imagen de clases. Pyreverse analizó nueve módulos de implementación; se contrastaron las clases y las jerarquías del diagrama con esa salida y se validaron las asociaciones de uso en el código. Se distinguen del modelo de dominio conceptual de Lab05 las clases efectivamente implementadas en Lab07.
- **Decisión:** Conservar fuentes PlantUML y PNG juntos en docs/design/patrones/; actualizar la imagen de clases existente. Los adaptadores de LLM reciben un cliente externo por interfaz dinámica, por ello el diagrama los muestra como puerto/adaptador sin afirmar que exista un cliente real en el repositorio.
