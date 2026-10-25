# E2: Strategy, Adapter y Factory por registro

## Roles y ubicación

| Rol | Archivo y responsabilidad |
| --- | --- |
| Strategy | `src/puntos_beneficios/reglas.py`, puerto `ReglaPuntos.calcular`. `PuntosPorPeso` conserva la fórmula y truncamiento de E1, con la tarifa de cada material. |
| Factory por registro de reglas | `FabricaReglas` selecciona el constructor por material. Cada instancia tiene su propio registro, sin Singleton ni estado global. |
| Cliente de las reglas | `src/puntos_beneficios/servicio.py`, acredita por la estrategia elegida sin `if/elif` por material. |
| Adapter | `src/solicitudes/mapas.py`, `MapaAdapter` traduce el diccionario de MapaSDK y `GeoAdapter` la tupla de GeoClient al puerto `PuertoMapas`. |
| Factory por registro de mapas | `FabricaMapas` permite registrar constructores y seleccionar un proveedor sin condicionales por variante. |
| Servicio refactorizado | `src/solicitudes/servicio.py`, preserva validaciones, estados, eventos y persistencia. Sus transiciones todavía usan condicionales, State corresponde a E3. |

La versión después se ubica directamente en `src/<modulo>/`, como indica la estructura del Lab07. `antes/` permanece intacta. Se reutilizan las clases de datos y el repositorio en memoria de la línea base, sin heredar su servicio ni delegarle el flujo refactorizado.

Las dos tarifas de E1 usan la misma fórmula, por eso comparten una estrategia parametrizada en lugar de duplicar clases. El puerto permite algoritmos distintos, demostrado con `ReglaPorLote` en la prueba de extensión. La regla ilustrativa para VIDRIO prueba el servicio público de Puntos/Beneficios, no amplía por sí sola el catálogo de materiales admitidos al registrar solicitudes, que conserva el comportamiento de E1.

Los adaptadores no calculan puntos, no deciden cobertura, no reintentan y no producen eventos. Los errores transitorios se propagan. El bucle de reintentos sigue en Solicitudes con el límite de E1, todavía no se implementa Decorator. Factory se utiliza en el sentido de registro de constructores pedido por la guía, sin añadir una jerarquía Abstract Factory.

## Tres líneas sobre los olores eliminados

1. Strategy y Factory eliminan la selección por material en el servicio de puntos y permiten incorporar una regla registrando un constructor.
2. Adapter impide que Solicitudes conozca las firmas y formatos de respuesta incompatibles de cada SDK de mapas.
3. El registro de mapas elimina el `if/elif` por proveedor, manteniendo cobertura, reintentos y confirmación como responsabilidades separadas de los adaptadores.

## Verificaciones

```powershell
python -m pytest tests/test_comportamiento.py tests/test_patrones.py -v
```

Resultado del 25/10/2026: **78 passed**, 35 casos de caracterización por versión y ocho casos de patrones. Las 28 caracterizaciones originales conservan sus expectativas. Se añadieron siete casos por versión para reglas desconocidas, tarifas inválidas y tarifa cero. El fixture elige también el servicio de puntos correspondiente a cada versión, evitando ejecutar siempre el cálculo anterior.

Las pruebas `test_open_closed_agrega_regla_sin_modificar_servicio` y `test_open_closed_agrega_mapa_sin_modificar_solicitudes` comprueban extensión y aislamiento de registros. Los otros seis casos verifican sustitución de los dos adaptadores y propagación de fallos transitorios. Solo se utilizan dobles locales.

Se conserva como referencia `radon-antes.txt`. No se actualiza esa métrica con el código después ni se afirma completado E6. E3, E4 y las actividades de la compañera no se desarrollan en este commit.
