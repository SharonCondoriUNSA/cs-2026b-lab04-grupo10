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
