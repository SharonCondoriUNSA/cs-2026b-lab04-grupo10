# E7: diagramas de patrones y clases

## Diagramas GoF aplicados

Cada archivo PlantUML se acompana de su imagen PNG regenerada desde el mismo fuente.

| Patron | Diagrama fuente | Imagen |
| --- | --- | --- |
| Strategy | [strategy.puml](strategy.puml) | [strategy.png](img/strategy.png) |
| Adapter | [adapter.puml](adapter.puml) | [adapter.png](img/adapter.png) |
| Factory | [factory.puml](factory.puml) | [factory.png](img/factory.png) |
| State | [state.puml](state.puml) | [state.png](img/state.png) |
| Observer | [observer.puml](observer.puml) | [observer.png](img/observer.png) |
| Decorator | [decorator.puml](decorator.puml) | [decorator.png](img/decorator.png) |
| Chain of Responsibility | [chain-of-responsibility.puml](chain-of-responsibility.puml) | [chain-of-responsibility.png](img/chain-of-responsibility.png) |

Los diagramas emplean estereotipos para distinguir los roles de cada patron. Strategy y Factory se aplican al calculo de puntos; Adapter y Factory a los proveedores de mapas; Adapter, Decorator y Chain of Responsibility al clasificador; State al ciclo de la solicitud y Observer a los eventos locales. Los dos usos de Decorator se muestran juntos en un diagrama.

## Actualizacion y comprobacion del diagrama de clases

Se actualizo [clases.puml](../clases.puml) para mostrar las clases que existen en el codigo refactorizado de E1-E5 y las relaciones de uso e implementacion relevantes. El archivo conserva su ruta, pero ya no representa solamente el modelo conceptual de Lab05. Ese modelo sigue en los artefactos UML anteriores; el diagrama actualizado refleja el codigo que ejecutan las pruebas.

Se genero una salida independiente con Pyreverse a partir de los nueve modulos de implementacion de solicitudes, estados, mapas, eventos, decoradores, IA y puntos/beneficios. Pyreverse analizo nueve modulos y reconocio las clases, las herencias y las dependencias entre modulos. Se contrastaron los nombres y jerarquias de clases.puml contra esa salida y las relaciones de uso se confirmaron leyendo las referencias en el codigo. En algunos casos Pyreverse no infiere asociaciones cuyo tipo es dinamico, por ejemplo los clientes externos recibidos por los adaptadores; se evita presentarlas como clases concretas de produccion en el diagrama.

La salida generada por Pyreverse se uso como evidencia de revision y no se copia como reemplazo directo: incluye detalles mecanicos y dependencias que no corresponden a una vista legible. La imagen [clases-solicitudes.png](img/clases-solicitudes.png) se regenero desde el archivo PlantUML actualizado.
