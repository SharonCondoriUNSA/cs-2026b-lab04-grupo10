# E7. Evaluación automática de prompts

El workflow [prompts.yml](../.github/workflows/prompts.yml) se ejecuta en cada PR, al publicar en main o ramas lab09 y por activación manual. Usa Node 22, Python 3.12 y Promptfoo 0.110.0. Solo tiene permisos de lectura y no necesita claves de modelos.

Se prueban los 33 controles Node de los evaluadores y las pruebas Python de integración, seguridad y del ejecutor de CI. Después [evaluar_prompts.py](../scripts/evaluar_prompts.py) invoca `npx --yes promptfoo@0.110.0 eval` para diez configuraciones con el proveedor grabado, `--no-cache` y `--no-write`. Los JSON y registros se guardan como artefactos, no sobrescriben los reportes versionados.

| Conjunto | Aprobados esperados |
|---|---:|
| Criterios v1 | 0/8 |
| Criterios v2 | 2/8 |
| Criterios v3 | 8/8 |
| Docstrings v1 | 0/8 |
| Docstrings v2 | 8/8 |
| Docstrings v3 | 8/8 |
| Seguridad criterios antes / después | 4/4 en cada fase |
| Seguridad docstrings antes / después | 4/4 en cada fase |

Las versiones iniciales fallan deliberadamente. El ejecutor acepta código 100 solo cuando el reporte contiene esos fallos esperados, todos los casos y cero errores de ejecución. Rechaza errores del proveedor, reportes incompletos, tasas distintas y códigos incoherentes. No se usa `continue-on-error` para ocultar fallos. Las tasas de referencia corresponden a estas grabaciones revisadas, no a una estimación de un modelo en vivo.

Se ejecutaron localmente las diez evaluaciones con la CLI instalada fuera del repositorio, todas con las tasas esperadas y cero errores. Las seis pruebas del ejecutor pasaron. El YAML se revisó estructuralmente, pero el resultado remoto solo podrá verificarse después de publicar esta rama y ejecutar Actions.

Para reproducir con dependencias instaladas y salida nueva:

```console
python scripts/evaluar_prompts.py --salida .ci-resultados/nueva-ejecucion
```

La opción `--cli-node` permite indicar una instalación ya disponible de la misma CLI en el entorno local, sin cambiar los proveedores ni las evaluaciones. Si la carpeta de salida contiene reportes, se pide otra carpeta para no mezclar evidencias anteriores.

## Estado del entregable

- Workflow preparado y ejecutor comprobado localmente.
- [Bitácora](bitacora-ia.md) con seis interacciones reales y una propuesta rechazada con [evidencia](evidencia-rechazo-evaluador.json).
- [No determinismo](no-determinismo/README.md) documentado con nueve respuestas proporcionadas por la usuaria, comparación y reflexión de cinco líneas. Se informa el modelo exacto no identificado, el transporte del pegado y la diferencia entre esquema (9/9) y decisión INVEST esperada (4/9).

La preparación local de E7 está completa. Falta publicar la rama y comprobar la ejecución remota de Actions. El workflow también verifica la integridad de la comparación de no determinismo, sin exigir una tasa funcional perfecta ni ocultar las discrepancias observadas.
