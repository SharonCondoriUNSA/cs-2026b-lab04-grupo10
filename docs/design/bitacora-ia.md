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

## E5 - Diagrama de paquetes y Regla C4 (sin ciclos) (2026-10-12)

**Herramienta:** Gemini Notebook (asistente de IA).

**Instrucción recibida:** Elaboración del diagrama de paquetes para el monolito modular EcoRecicla AQP (ADR-001) y verificación de la Regla C4 (ausencia de dependencias cíclicas).

### Prompt de IA utilizado

> Actúa como arquitecto de software. Contexto: monolito modular EcoRecicla AQP (ADR-001). Genera un diagrama de paquetes en PlantUML que agrupe las clases del sistema en sus respectivos módulos (`solicitudes`, `rutas_cobertura`, `puntos_beneficios`, `reportes`, `notificaciones` y el paquete transversal `compartido`). Modela las dependencias entre paquetes indicando el puerto o contrato consumido y agrega una nota explícita verificando la Regla C4 (sin ciclos entre paquetes).

### Propuesta y estructura de paquetes

La propuesta generada en `docs/design/paquetes.puml` organiza el sistema en seis paquetes dentro del espacio de nombres `ecorecicla`:

- **`solicitudes`:** módulo principal del dominio, encargado de gestionar las solicitudes de recojo y su ciclo de vida.
- **`rutas_cobertura`:** módulo que expone el contrato público `CoberturaRecojo` para validar los distritos con cobertura de atención.
- **`puntos_beneficios`:** módulo que procesa la acreditación de puntos mediante el método `confirmarPuntosAcreditados()`.
- **`notificaciones`:** módulo responsable del envío asíncrono de notificaciones mediante el contrato `NotificadorSolicitud`.
- **`reportes`:** módulo encargado de consultar métricas y acumulados de toneladas recicladas.
- **`compartido`:** paquete transversal que contiene tipos de datos comunes y reutilizables.

### Verificación de la Regla C4 (ausencia de ciclos)

Se analizó el grafo de dependencias entre paquetes para verificar la ausencia de ciclos, conforme a la regla establecida en el ADR-001.

Las dependencias identificadas son las siguientes:

- `solicitudes` → `rutas_cobertura`, mediante el contrato `CoberturaRecojo`.
- `solicitudes` → `puntos_beneficios`, mediante el método `confirmarPuntosAcreditados()`.
- `solicitudes` → `notificaciones`, mediante el contrato `NotificadorSolicitud`.
- `solicitudes` → `compartido`, para utilizar tipos de datos comunes.
- `reportes` → `solicitudes`, para consultar información de solo lectura destinada a las métricas.
- `rutas_cobertura` → `compartido`.
- `puntos_beneficios` → `compartido`.
- `notificaciones` → `compartido`.
- `reportes` → `compartido`.

**Conclusión:** La estructura propuesta no presenta dependencias cíclicas entre los paquetes, siempre que las relaciones implementadas respeten las direcciones indicadas. Por tanto, se cumple la Regla C4 de ausencia de ciclos en el grafo de dependencias.

### Verificaciones realizadas y Git

- **Sintaxis y renderizado:** se verificó la sintaxis del diagrama PlantUML y se generó el archivo PNG `docs/design/img/paquetes.png`. Se revisaron la legibilidad de la nota explicativa y las relaciones representadas mediante flechas discontinuas (`..>`).
- **Git:** los cambios se prepararon en la rama `lab05-e5-paquetes`, creada a partir de la rama `main` actualizada.