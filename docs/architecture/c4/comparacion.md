# Comparación: Diagrama de Secuencia UML vs. Vista Dinámica C4

El diagrama de secuencia UML del Lab05 muestra firmas, retornos, líneas de vida y fragmentos `alt` y `loop`, orientados a los desarrolladores.
La vista dinámica C4 resume el mismo registro en cinco interacciones entre la PWA, componentes, mapas y persistencia, para comunicar el flujo a arquitectos, líderes técnicos y evaluadores.
Se omiten las clases, la iteración por detalles, los retornos HTTP y las ramas de error de datos o falta de cobertura, que impiden guardar en la secuencia UML. Se representa el escenario con datos y cobertura válidos.
La comprobación de mapas es opcional, su fallo permite guardar PENDIENTE con ubicación por revisar. Después de confirmar la persistencia se solicita el aviso interno asíncrono, sin añadir Redis ni envío por WhatsApp a este escenario.

## E6: Contexto manual frente al modelo exportado

| Aspecto | C4-PlantUML escrito a mano | Structurizr DSL exportado |
| --- | --- | --- |
| Tiempo invertido | No se cronometró la redacción y revisión del archivo manual, no se atribuye una duración ficticia. Para este contexto se escribieron seis elementos y cinco relaciones. | En una repetición local se midieron 0.77 s para exportar las cinco vistas a C4-PlantUML y 0.83 s para Mermaid. Son tiempos de exportación, no del modelado ni de la revisión visual. |
| Errores y diferencias encontrados | El contexto manual pasó la comprobación de sintaxis, sin errores detectados. Se compararon los nombres de sus seis elementos y las etiquetas de sus cinco relaciones con el contexto exportado. | La exportación inicial no conservó los colores de las etiquetas. Se activó `c4plantuml.tags` en el workspace y se regeneraron las imágenes. Mermaid y PlantUML distribuyen los elementos de forma diferente, y el contexto manual utiliza `System_Ext` para los sistemas externos. |
| Cambio del nombre de un contenedor | Este contexto de nivel 1 no muestra contenedores, por lo que un cambio exclusivo de nombre de la API no lo afecta. Los diagramas de contenedores mantenidos a mano sí requieren revisar cada archivo donde se repita ese nombre. | Se cambia el nombre en una declaración del workspace y se reexportan las vistas afectadas y sus PNG. Si cambia el nombre del sistema principal, también debe actualizarse el contexto manual independiente. |

### Reproducción

Se utilizó Structurizr CLI v2025.11.09 con Java 23, y PlantUML 1.2024.3 con Java 8 y Graphviz. Los archivos de `export/` son salidas generadas, las correcciones se realizan en `workspace.dsl` y luego se vuelve a exportar.

```powershell
structurizr.bat validate -workspace docs/architecture/c4/workspace.dsl
structurizr.bat export -workspace docs/architecture/c4/workspace.dsl -format plantuml/c4plantuml -output docs/architecture/c4/export
structurizr.bat export -workspace docs/architecture/c4/workspace.dsl -format mermaid -output docs/architecture/c4/export
java -jar plantuml.jar -charset UTF-8 -tpng -o ../img "docs/architecture/c4/export/*.puml"
java -jar plantuml.jar -charset UTF-8 -tpng -o img docs/architecture/c4/contexto-manual.puml
```

Los comandos suponen que Structurizr CLI está en PATH y se proporciona la ruta local de plantuml.jar. Las herramientas de apoyo se mantienen fuera del repositorio.

Se revisaron visualmente los seis PNG. La vista de componentes contiene más relaciones y debe consultarse a tamaño completo, conserva cruces de líneas propios de la distribución automática. Los PNG se generaron desde C4-PlantUML, los archivos Mermaid se exportaron, pero no se renderizaron ni se validaron con un motor Mermaid en esta revisión.
