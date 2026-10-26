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

Se genero una salida independiente con Pyreverse en dos ejecuciones: siete modulos de Solicitudes y dos de Puntos/Beneficios. Esto evita que los dos archivos servicio.py colisionen al analizarlos juntos sin paquetes explicitos. Se contrastaron las clases y herencias reconocidas, sin asumir que Pyreverse resuelva todas las dependencias dinamicas entre modulos. Se contrastaron los nombres y jerarquias de clases.puml contra esa salida y las relaciones de uso se confirmaron leyendo las referencias en el codigo. En algunos casos Pyreverse no infiere asociaciones cuyo tipo es dinamico, por ejemplo los clientes externos recibidos por los adaptadores; se evita presentarlas como clases concretas de produccion en el diagrama.

La salida generada por Pyreverse se uso como evidencia de revision y no se copia como reemplazo directo: incluye detalles mecanicos y dependencias que no corresponden a una vista legible. La imagen [clases-solicitudes.png](../img/clases-solicitudes.png) se regenero desde el archivo PlantUML actualizado.

## Reproduccion de la comprobacion con Pyreverse

```powershell
pyreverse -o puml -p solicitudes -d RUTA_TEMPORAL src/solicitudes/servicio.py src/solicitudes/modelos.py src/solicitudes/estados.py src/solicitudes/mapas.py src/solicitudes/eventos.py src/solicitudes/decoradores.py src/solicitudes/ia.py
pyreverse -o puml -p puntos -d RUTA_TEMPORAL src/puntos_beneficios/servicio.py src/puntos_beneficios/reglas.py
```

RUTA_TEMPORAL debe ser una carpeta existente fuera del repositorio. Resultado de la revision: 7 y 2 modulos analizados, respectivamente. Al pasar los nueve archivos juntos se reconocian ocho modulos por la colision del nombre servicio. Se comprobaron en las salidas ambas clases de servicio y las jerarquias de los patrones. La salida no infiere todas las asociaciones dinamicas, estas se revisan en el codigo. El resumen de evidencia se conserva en [pyreverse-verificacion.txt](pyreverse-verificacion.txt).

Correcciones de revision: Decorator muestra MapaAdapter y GeoAdapter, el cliente LLM se identifica como contrato externo esperado y Estado se representa como clase base, coherente con su implementacion. No se modifico el codigo funcional.
