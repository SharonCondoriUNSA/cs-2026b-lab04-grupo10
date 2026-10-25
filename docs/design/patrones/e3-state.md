# E3: State para SolicitudRecojo

Referencia: `docs/design/estados-solicitud.mmd`, Lab05. La entidad conserva el nombre público `Solicitud` utilizado en la línea base del Lab07.

## Correspondencia con el diagrama

| Origen | Método de la entidad | Estado que permite la operación | Destino |
| --- | --- | --- | --- |
| Inicio | `registrar_pendiente()` | `SinRegistrar` | PENDIENTE |
| PENDIENTE | `asignar_reciclador(reciclador_id)` | `Pendiente` | ASIGNADA |
| ASIGNADA | `registrar_recojo(fecha_recojo)` | `Asignada` | RECOGIDA |
| RECOGIDA | `registrar_pesaje(peso_real_kg)` | `Recogida` | PESADA |
| PESADA | `confirmar_puntos_acreditados(acreditacion_id)` | `Pesada` | PUNTOS_ACREDITADOS |
| PUNTOS_ACREDITADOS | `cerrar()` | `PuntosAcreditados` | Final |

`Estado` prohíbe por defecto todas las transiciones. Cada subclase redefine solo las permitidas. `SinRegistrar` y `Finalizada` representan pseudoinicio y pseudofinal, no agregan estados del dominio. Al cerrar se conserva públicamente PUNTOS_ACREDITADOS y se activa `cerrada`, como en E1.

Las guardas comprueban identificador de reciclador, fecha, peso real positivo y finito y referencia de acreditación antes de modificar datos. El registro inicial se invoca desde el servicio después de comprobar datos y cobertura. Se trabaja con las mismas precondiciones de sesión autorizada, recojo confirmado y acreditación confirmada que en E1, no se añaden sistemas de autorización ni acreditación externos.

## Cambios

- `src/solicitudes/estados.py` contiene la base prohibitiva y los estados concretos.
- `src/solicitudes/modelos.py` mantiene el constructor y los campos de la línea base y almacena un objeto de estado por solicitud. Reutiliza la clase de datos original, no hereda el servicio ingenuo.
- `src/solicitudes/servicio.py` delega las transiciones en la entidad. Antes de llamar a Puntos/Beneficios consulta al estado si la acreditación está permitida.
- La propiedad `estado` conserva las etiquetas de texto que observan las pruebas. Su setter admite la construcción de escenarios de prueba de E1 y selecciona un objeto mediante un diccionario, no decide las transiciones. En el flujo ordinario las transiciones las ejecutan los métodos de estado.
- El indicador `cerrada` se respeta para impedir operaciones después del fin. No hay condicionales sobre el nombre de otro estado en las clases de State.
- La instantánea se guarda antes de confirmar el registro al objeto del llamador y antes del aviso, manteniendo la semántica de persistencia de E1.

La versión `antes/`, los SDK simulados y la medición inicial se conservan. No se incorpora Observer ni Decorator, corresponden a E4. Los diagramas UML del Lab05 no se modifican en este ejercicio, su actualización con los patrones corresponde a E7 del Lab07.

## Comprobación

```powershell
python -m pytest tests/test_comportamiento.py tests/test_patrones.py -v
```

Resultado del 25/10/2026: **110 passed**. Se conservan 70 casos de caracterización sobre antes y después y ocho casos de E2. E3 añade 32 casos, recorrido completo, 25 combinaciones prohibidas, cuatro guardas inválidas, cierre definitivo y bloqueo de acreditación fuera de estado. Se comprueba que una operación rechazada no modifique la solicitud y que la acreditación inválida no invoque al colaborador de puntos.

E3 depende de E1 y E2, todavía no representa una revisión humana ni una integración en main.
