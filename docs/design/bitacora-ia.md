# Bitácora de IA - Lab05, únicamente E1

**Fecha:** 2026-10-10 (America/Lima). **Herramienta:** Codex, en esta conversación.

Este registro corresponde a la elaboración y revisión realizadas por el asistente en esta sesión. No atribuye verificaciones al equipo humano ni inventa consultas a otra IA. La bitácora del Lab04 permanece intacta. No se ejecuta la auditoría E7 ni se simulan sus cinco interacciones.

## Prompt IA 1 adaptado y utilizado como instrucción de generación

La solicitud original del usuario es la instrucción recibida. El siguiente texto explicita su adaptación al Prompt IA 1 de la guía, aplicada por Codex dentro de esta misma sesión para construir `clases.puml`; no fue enviado como una segunda consulta a un servicio externo.

```text
Actúa como diseñador de software orientado a objetos.
Contexto: EcoRecicla AQP, módulo Solicitudes de un monolito modular.
ADR-001: despliegue único; módulos Solicitudes, Rutas/Cobertura,
Puntos/Beneficios y Reportes; contratos públicos explícitos y esquema
de datos propio por módulo. No cambies las decisiones del Lab04.

Historia: Como vecino, quiero solicitar el recojo de mis residuos
reciclables indicando los materiales, su peso estimado y el punto
de recojo, para que EcoRecicla AQP pueda gestionar su recolección.

Criterios Dado/Cuando/Entonces:
1. Dado un vecino identificado, un punto en distrito con cobertura y
al menos un material aceptado con peso mayor que cero, cuando solicita
el recojo, entonces se guarda una solicitud única PENDIENTE con su
punto y detalles y se devuelve el identificador como confirmación.
2. Dado un detalle vacío, material no aceptado o peso no positivo,
cuando solicita el recojo, entonces se informa el dato inválido y
no se guarda ninguna solicitud.
3. Dado un punto en distrito sin cobertura, cuando solicita el recojo,
entonces se informa la falta de cobertura y no se guarda la solicitud.
4. Dado que los datos y cobertura son válidos y mapas no responde,
cuando solicita el recojo, entonces se guarda la solicitud PENDIENTE
con coordenadas ingresadas y se informa la comprobación pendiente.

Tarea: genera un diagrama de clases PlantUML con al menos seis clases
derivadas de la historia, atributos tipados y visibilidad, operaciones,
multiplicidades en ambos extremos de todas las asociaciones, una
enumeración de estado y una interfaz como puerto de la API de mapas.
Modela su adaptador como realización, no como herencia de una entidad.
Expresa la consulta de cobertura mediante un contrato público.
Usa composición solo para datos propios de la solicitud y asociación
para el catálogo de materiales. Evita datos personales innecesarios.
Formato de la propuesta: solo código PlantUML. Documenta supuestos
en comentarios. Limita el estado a PENDIENTE para esta historia;
no desarrolles E2-E8 ni código de implementación.
```

## Propuesta y revisión efectiva

La propuesta generada en `clases.puml` contiene siete clases, tres interfaces y una enumeración. Se revisó contra la historia, RF-01 y el ADR-001, sin reutilizar nombres ni entidades de AgroConecta.

| Elemento revisado | Decisión y fundamento |
|---|---|
| Vecino con UUID | Aceptado: identifica al actor sin duplicar DNI, teléfono, nombre ni credenciales. |
| Solicitud y detalles | Aceptada composición `1` a `1..*`: no hay solicitud válida sin materiales; cada detalle pertenece a una sola solicitud. |
| Punto de recojo | Aceptada composición `1` a `1`: representa una copia propia del punto ingresado, no un domicilio compartido. |
| Material | Aceptada asociación `0..*` a `1`: el catálogo existe con independencia de los detalles. |
| AdaptadorMapas y ServicioMapas | Aceptada realización: sustituibilidad del proveedor a través del contrato externo. No se justifica herencia entre entidades. |
| CoberturaRecojo | Aceptado contrato público de Rutas/Cobertura; no se accede a clases internas ni se cruzan tablas de módulos. |
| EstadoSolicitud | Aceptado PENDIENTE para E1; no se genera el ciclo de vida del ejercicio E3. |
| Dependencias del servicio | Corrección realizada tras la primera renderización: se añadieron dependencias explícitas a PuntoRecojo y DetalleReciclable, usados en los parámetros y en la validación. |

No se encontraron ni se simularon propuestas de DNI, herencia incorrecta o asociaciones sin cardinalidad para luego atribuirles una corrección ficticia. Las reglas de cobertura, catálogo y mapa opcional son supuestos de diseño identificados en `historia.md`.

## Verificaciones realizadas

- Lectura del PDF con pypdf y revisión visual de la página 16 renderizada con Poppler: la fila del caso 10 confirma «Solicitar el recojo de reciclables». Se leyeron README, drivers, matriz, ADR, diagramas y bitácora del Lab04. No se encontró AGENTS.md dentro del espacio de trabajo.
- Git: raíz `cs-2026b-lab04-grupo10`; remoto origin `https://github.com/SharonCondoriUNSA/cs-2026b-lab04-grupo10`; rama principal local `main` y referencia origin/HEAD hacia origin/main. No se verificó el servidor remoto mediante fetch. Rama E1 inexistente antes de crear `lab05-e1-clases` desde main (`f1915ba`).
- Existía un cambio ajeno en `docs/architecture/diagramas/despliegue.py`: eliminación de un comentario y una línea vacía. Se conservó; no se hizo pull porque el árbol no estaba limpio. El índice estaba vacío antes de E1.
- AgroConecta está en una carpeta hermana, fuera de la raíz Git. `git ls-files -- Lab05_recursos_UML_AgroConecta` no devuelve archivos. Se añadió la exclusión local `/Lab05_recursos_UML_AgroConecta/` sin sobrescribir el contenido de `.git/info/exclude`; `git check-ignore --no-index` confirmó el patrón. No se modificaron los ejemplos.
- El ejecutable `java` del PATH no devolvió resultado durante los sondeos. Se usó directamente el Java 8 local de `C:/Program Files/Java/jre1.8.0_491/bin/java.exe`, compatible con el JAR disponible. La guía recomienda Java 17+, por lo que se documenta esta diferencia del entorno. PlantUML local: 1.2024.3; Graphviz seleccionado: `C:/Program Files/Graphviz/bin/dot.exe`. No se descargaron herramientas ni se envió el diagrama a un servidor.
- PlantUML `-checkonly -charset UTF-8 docs/design/clases.puml`: comprobación real de sintaxis. Renderización `-graphvizdot "C:/Program Files/Graphviz/bin/dot.exe" -charset UTF-8 -tpng -o img docs/design/clases.puml`: PNG generado localmente. El JAR usado está en `C:/Users/USUARIO/.vscode/extensions/jebbs.plantuml-2.18.1/plantuml.jar`.
- Revisión visual del PNG, incluida la versión final tras añadir dependencias: textos, cardinalidades, diamantes de composición y triángulo de realización legibles, sin recortes. C3 y C5 revisadas en E1. C4 revisada respecto al contrato con Cobertura, sin afirmar una auditoría de paquetes E5. C1 y C2 no se verifican porque no se desarrollan secuencia ni estados.
- Revisión final del diff preparado y `git diff --cached --check`: solo historia, PlantUML, PNG y esta bitácora bajo `docs/design/`; sin AgroConecta ni archivos del Lab04. Se agregaron únicamente las cuatro rutas explícitas de E1.

## Límites y pendiente

Se verificó el modelo y su renderización; no hay implementación, pruebas funcionales ni integración real con mapas o persistencia. Los supuestos de negocio requieren validación del equipo. La actualización de main queda pendiente por el cambio preexistente; no se hace stash, push, PR, integración, etiqueta ni E2-E8.

## E2 - Secuencia del flujo crítico (2026-10-10)

**Herramienta:** Codex, esta conversación. **Instrucción recibida:** «okey gracias ahora hagamos E2». Se consultaron de nuevo los requisitos E2 de la página 16 y la historia y clases actuales. El registro E1 anterior describe su alcance en el momento de realizarlo; esta sección documenta la continuación autorizada.

**Propuesta:** secuencia de solicitud con actor, PWA, controlador, servicio, punto, detalle, material, contratos de cobertura y mapas, solicitud, repositorio y puerto de aviso interno (12 líneas de vida). Incluye validación por detalle con `loop`, alternativas de datos inválidos, falta de cobertura y mapas sin respuesta, retornos y aviso asíncrono tras persistir. El aviso dentro de la aplicación es un supuesto añadido para E2, sin teléfonos ni cambios al ADR-001.

**Correcciones efectivas:** se añadieron PWA.solicitarRecojo, SolicitudController.registrarSolicitud y NotificadorSolicitud.confirmarRegistro al diagrama de clases con sus dependencias para satisfacer C1. Se regeneró su PNG. Se actualizó el alcance introductorio de historia.md porque la secuencia ya existe. No se añadieron estados ni funcionalidades E3-E8.

**Verificación C1:** todas las llamadas de operación tienen receptor y operación declarada en clases.puml. El primer comprobador por expresión regular contabilizaba solo cuatro llamadas porque omitía las líneas indentadas; se corrigió su patrón para aceptar espacios iniciales y comprobar todas las llamadas, sin cambiar la secuencia por ese defecto del comprobador. Los retornos, mensajes de presentación al actor y la nota de construcción no son llamadas de operaciones. La llamada a mapas se corresponde tanto con el puerto como con la operación del adaptador.

| Receptor | Operaciones usadas en la secuencia |
|---|---|
| PWA | solicitarRecojo |
| SolicitudController | registrarSolicitud |
| ServicioSolicitudes | solicitarRecojo |
| PuntoRecojo | coordenadasValidas |
| DetalleReciclable | validar |
| MaterialReciclable | esAceptado |
| CoberturaRecojo | atiendeDistrito |
| ServicioMapas / AdaptadorMapas | validarUbicacion |
| SolicitudRecojo | validarDatos, marcarUbicacionValidada, registrarPendiente |
| RepositorioSolicitudes | guardar |
| NotificadorSolicitud | confirmarRegistro |

**Otras verificaciones:** PlantUML local `-checkonly -charset UTF-8` y renderización PNG de clases y secuencia con el JAR y Java ya documentados; revisión visual de ambos PNG sin texto cortado. Se revisaron las ramas de error para confirmar que no persisten y CA-04 para confirmar que el fallo de mapas no descarta el registro. No se ejecutaron pruebas de una aplicación, pues son modelos UML.

**Git:** rama nueva lab05-e2-secuencia basada en el commit E1 b8a2d2f. El cambio preexistente de despliegue.py se conserva fuera del índice. Los ejemplos de AgroConecta solo se leyeron. Se revisaron el diff y las rutas preparadas y se ejecutó `git diff --cached --check`; se agregó cada archivo por su ruta. El commit inicial utilizó el mensaje de la guía `E2: secuencia`, sin push, PR ni integración en esa continuación.

**Solicitud posterior del usuario:** se autorizó cambiar el mensaje y subir la rama al repositorio. El mensaje elegido es `feat: E2 Lab05 - secuencia de solicitud de recojo de reciclables`. Esta indicación sustituye el mensaje exacto de la guía. Se mantiene fuera del commit el cambio de despliegue.py y no se abre PR ni se integra la rama.

## E3 - Máquina de estados (2026-10-10)

**Herramienta:** Codex, esta conversación. **Instrucción recibida:** «okey ahora haz por favor 3». Se leyeron los requisitos E3 en páginas 16-17 de la guía y se contrastaron con clases.puml y ADR-001.

**Propuesta aplicada:** `estados-solicitud.mmd`, Mermaid stateDiagram-v2, con los cinco estados propuestos para el caso 10, inicio y final. Seis transiciones nombradas por operaciones de SolicitudRecojo y seis guardas. Se conserva la secuencia E2: el registro inicial sigue en PENDIENTE y no depende del éxito de mapas.

**Correcciones efectivas de consistencia:** se amplió EstadoSolicitud y se añadieron asignarReciclador, registrarRecojo, registrarPesaje, confirmarPuntosAcreditados y cerrar a SolicitudRecojo. Se agregaron los datos opcionales de identificador de reciclador, fecha de recojo, peso real y referencia de acreditación. Solo se registra la confirmación del módulo Puntos/Beneficios, sin cambiar sus decisiones ni modelar su implementación. Se corrigieron los textos de alcance de historia.md y se regeneró la imagen de clases.

**Validación real:** se pegó el código en mermaid.live y el editor lo reconoció como diagrama de estados, versión mostrada v12.1.0. La vista renderizada mostró los cinco estados, las seis etiquetas de transición, guardas y notas, sin error de sintaxis. El intento de descargar PNG mediante el botón del editor no completó la descarga dentro del tiempo disponible. Se recuperó el SVG renderizado mediante el inventario de recursos de la página; se eliminó únicamente la transformación de zoom de la vista y se fijaron dimensiones y fondo para guardar un SVG independiente en img/estados-solicitud.svg. No se afirma haber exportado PNG de estados. Se guardó una captura de evidencia fuera del repositorio, en la raíz del espacio de trabajo.

**C2 y revisión estructural:** se comprobaron los nombres de las seis operaciones de transición contra SolicitudRecojo, la igualdad de los cinco identificadores con la enumeración y la salida de todos los estados hacia el final. Se revisaron las guardas y se documentó que un avance inválido conserva el estado. cerrar() termina el flujo sin borrar datos; las guardas de asignación y acreditación presuponen confirmaciones autorizadas por los contratos públicos. También se volvió a comprobar C1 de E2, sin modificar su secuencia.

**Otras verificaciones:** comprobación de sintaxis PlantUML de clases.puml y regeneración local del PNG con Java, JAR y Graphviz documentados en E1. Revisión visual del diagrama de estados en el editor y de la imagen de clases. El SVG conserva el contenido generado por Mermaid, incluidos los textos HTML de sus etiquetas. No se verificó una implementación ni se simularon pruebas funcionales.

**Corrección de exportación:** la primera comprobación XML del SVG detectó etiquetas HTML `<br>` sin cierre en las notas. Se normalizaron a `<br/>` sin alterar su texto; la comprobación XML posterior pasó. Se verificaron automáticamente cinco estados iguales a la enumeración, seis guardas, seis operaciones existentes y salida de todos los estados. La comprobación de las 13 llamadas C1 de E2 también pasó.

**Git:** rama lab05-e3-estados creada desde E2 c4f01eb. Se preparan solo las rutas de diseño de E3 y los ajustes de consistencia, se revisa el diff y se ejecuta git diff --cached --check. Se conserva fuera del commit el cambio de despliegue.py; AgroConecta permanece intacto. Commit local `E3: estados`, sin push, PR, integración ni E4-E8.

**Revisión posterior del archivo aportado por el usuario:** se encontró img/estados-solicitud.png y la eliminación del SVG anterior. Se revisó visualmente el PNG (1592 x 3276): contiene título, cinco estados, inicio, final, las seis operaciones y guardas y las dos notas, sin recortes y con texto legible. Se conserva el reemplazo realizado por el usuario, se actualiza el enlace de historia.md y se incorpora al commit local E3. Los registros previos de exportación SVG describen el proceso anterior, no el formato final entregado. No se verificó cómo obtuvo el usuario el PNG ni se afirma que fue descargado automáticamente por Codex.

## E4 - Actividades de la ruta diaria (2026-10-10)

**Herramienta:** Codex, esta conversación. **Instrucción recibida:** «Ahora el E4». Se tomó el foco «Ruta diaria del reciclador» de la tabla 7, los requisitos E4 de la guía leídos durante E3, los drivers RF-02 a RF-05 y QA-02, ADR-001 y el ciclo de estados E3. El ejemplo de actividades AgroConecta solo se leyó como referencia de sintaxis.

**Propuesta:** tres particiones, consulta de ruta y recorrido de paradas con while, decisiones de disponibilidad, entrega, conexión, validación de recojo, peso y acreditación; fork/join para acreditación y comunicación a Reportes. Sin conexión se conserva el registro en PWA sin anticipar estados del servidor; se documenta su procesamiento al sincronizar. Ante errores se conserva el estado válido previo, sin añadir estados a E3.

**Revisión y cambios efectivos del asistente:** se aclaró que un fallo de comunicación a Reportes deja un pendiente sin perder el pesaje. Se ordenaron las particiones para situar al Vecino junto al Reciclador y se ajustó el ancho de texto para facilitar lectura. Estos ajustes son del asistente, no de una revisión humana.

**Verificaciones:** comprobación PlantUML -checkonly y renderización PNG local con el entorno ya documentado. Revisión visual de actividades, decisiones, bucle y barras de fork/join. Correspondencia de los cambios de estado con E3 y de los contratos entre módulos con ADR-001. No se desarrollan E5-E8 ni se modifica Lab04.

**Revisión humana E4 (estado al 2026-10-10):** pendiente en ese momento. Se solicitó al usuario que actúe como vecino o reciclador, revise el flujo y señale un cambio concreto, incluyendo el lugar/momento del pesaje. La actualización comunicada el 2026-10-11 se registra al final de esta sección.

**Aclaración recibida del usuario:** «Todavía no hemos realizado la revisión con mi compañera. Deja ese apartado como pendiente y continúa con el borrador, sin registrar una validación humana como realizada». Se mantiene E4 como borrador técnico verificado y se deja pendiente la revisión con la compañera y el cambio que resulte de ella. Esta aclaración no valida el proceso ni confirma el supuesto de pesaje en el punto de recojo.

**Git:** rama lab05-e4-actividades creada desde E3 522f3b6. Se conserva el cambio de despliegue.py; AgroConecta no se modifica ni se prepara para commit. La preparación y revisión se limitan a las rutas de actividades, su PNG, historia y bitácora. No se hace push, PR ni integración.

**Actualización solicitada el 2026-10-11:** el usuario informó que su compañera revisó E4 y proporcionó el resultado y el bloque de validación siguiente para incorporarlos. Este registro se basa en lo comunicado por el usuario; el asistente no presenció la simulación. La rama de entrega no disponible ya existía; se precisaron sus etiquetas para identificar la ausencia del vecino, nombrar la incidencia, indicar almacenamiento en la PWA y posterior reprogramación conservando ASIGNADA. Se regeneró el PNG, se comprobó la sintaxis y se revisó visualmente. No se encontraron contradicciones con clases y estados: la rama no invoca registrarRecojo ni cambia a RECOGIDA. El detalle de reprogramación queda fuera del modelo actual. Se conservan las notas históricas anteriores como registro del estado previo, no como pendientes actuales.

### Validación del proceso con el usuario

Se revisó el diagrama de actividades simulando el recorrido del reciclador durante una jornada de recojo.

Resultado de la revisión: Se identificó la necesidad de contemplar el caso en que el vecino no se encuentre disponible en el punto de recojo.

Ajuste incorporado: Se documentó la rama de decisión para registrar la incidencia «Entrega no disponible», almacenar el registro localmente en la PWA y mantener la solicitud en estado ASIGNADA para su posterior reprogramación.
