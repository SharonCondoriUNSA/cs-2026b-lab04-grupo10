# E1. Lienzo del sistema agéntico de EcoRecicla AQP

Referencia: Guía Lab10 Sistemas Agénticos 2026B v2, Paso 2 y secciones 1.3 y
1.7. Mini framework de referencia: Lab10_recursos_Agentes_AgroConecta_v2.zip.
Su copia y adaptación corresponden a E2, no se incorporan sus trazas de
AgroConecta como si fueran ejecuciones de EcoRecicla.

## Siete decisiones justificadas

| Decisión | Elección | Justificación para el caso |
|---|---|---|
| ¿Agente o flujo fijo? | Agente para explorar y proponer correcciones de los tres issues. Flujo fijo para calcular puntos, filtrar canceladas y comprobar las pruebas. | La localización de la causa requiere leer y contrastar archivos. Las reglas del negocio y la aprobación tienen contratos objetivos y no deben delegarse a un LLM. |
| Arquetipo | Un ejecutor ReAct para E2 y E4. Planificador-ejecutor con revisión separada se compara en E5. | Empezar con un solo agente reduce coste y permite observar el bucle decisión-herramienta-observación. No se supone que más agentes produzcan mejores resultados. |
| Herramientas | Listar y leer archivos, buscar, editar src/lab10/operaciones.py, ejecutar pruebas de issues, ver diff y comandos permitidos. E4 añade mapa_repo y notas. | Capacidades mínimas para diagnosticar, corregir y verificar. Prohibir red, instalaciones, credenciales, escritura en tests y cambios en .git, workflows y módulos históricos. |
| Memoria | Historial de la tarea en E2. Notas persistentes por ejecución en E4. | El historial conserva observaciones a corto plazo. Las notas guardarán hipótesis y archivos revisados, sin mezclar ejecuciones ni presentar una hipótesis como hecho. No se requiere memoria vectorial ni datos personales. |
| Coordinación | E2/E4: agente único. E5: gestor con ejecutor y crítico de solo lectura, máximo dos rondas. | Medir la alternativa simple antes de incorporar coordinación. El crítico no edita código ni pruebas. Comparar el issue 2 en copias del mismo estado inicial. |
| Rol humano | Integrante como revisora de diff, pruebas y PR. E6 incorporará aprobación de cada edición desde consola. | Ningún agente fusiona ni aprueba su propio cambio. No se afirma que la aprobación interactiva de ediciones esté implementada en E1. |
| Control | Sandbox con copia de trabajo, contrato JSON estricto, permisos por rol, máximo 12 pasos por agente y dos rondas de coordinación. | Limitar bucles y acciones. Registrar decisiones inválidas y bloqueos sin repararlas a mano. La herramienta devuelve observaciones reales, las pruebas y el contrato definen aceptación. |

## Tareas y aceptación observable

| Issue | Error sembrado | Prueba objetiva | Entregable que lo resuelve |
|---|---|---|---|
| [01](../../issues/ISSUE-01.md) | Un reintento duplica saldo y movimientos. | tests/test_issue_01.py | E2, ejecutor ReAct interactivo. |
| [02](../../issues/ISSUE-02.md) | Se incluye una solicitud cancelada en la ruta. | tests/test_issue_02.py | E5, comparación de coordinaciones. |
| [03](../../issues/ISSUE-03.md) | Una tarifa distrital cambia el cálculo de otro distrito. | tests/test_issue_03.py | E4, herramienta nueva y memoria. |

Las tres tareas usan src/lab10/operaciones.py como escenario aislado. Se reutiliza
ServicioPuntos sin cambiar el código de Lab07–Lab09. Las pruebas observan saldo,
movimientos, rutas y resultados distritales, no nombres de variables internas.

## Estado inicial y reproducción

Instalar requirements-lab10.txt y ejecutar desde la raíz:

```console
python -m pytest tests/test_issue_01.py tests/test_issue_02.py tests/test_issue_03.py -q
```

E1 debe conservar los tres fallos de aserción. No usar xfail, saltos ni cambiar
expectativas para aparentar verde. El registro de ejecución está en
[evidencias/e1-rojo.txt](../evidencias/e1-rojo.txt). Las correcciones y sus
trazas se registrarán después. Un fallo por importación o dependencia no
constituye una reproducción válida del issue.

Los datos son sintéticos. No hay accesos a servicios reales, claves ni datos
personales. El agente trabaja en una copia y los PR se revisan por una integrante.

## Reparto y dependencias

Primera integrante: E1–E4. Segunda integrante: E5–E8. Cada entrega utiliza su
propia rama. E1 mantiene las tres pruebas en rojo. Tras E2 solo se corrige el
issue 1 y tras E4, el 3. El issue 2 permanece como línea base para E5. El estado
previo a una corrección se conserva en el historial Git para comparaciones.

No se generan métricas, aprobaciones humanas o trayectorias antes de ejecutar
el sistema. La etiqueta v1.0-agentes corresponde al cierre revisado de E8.

## Verificacion de E1, 2026-11-26

La ejecucion real de las tres pruebas nuevas obtuvo 3 failed por aserciones de
comportamiento, sin errores de coleccion. El registro completo se conserva en
evidencias/e1-rojo.txt. La suite anterior se ejecuto excluyendo solo esos tres
archivos nuevos y obtuvo 163 passed y 16 subtests passed. No se modificaron
archivos de los laboratorios anteriores. Las dependencias se instalaron fuera
del repositorio. Estas comprobaciones no son trazas de un agente ni completan E2.
