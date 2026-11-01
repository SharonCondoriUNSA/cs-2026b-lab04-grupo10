# E5. Fitness functions en integración continua

E5 convierte reglas de arquitectura de [ADR-001](adr/001-estilo-arquitectonico.md) y [ADR-005](adr/005-patrones-de-diseno.md), y escenarios priorizados en E1, en verificaciones repetibles. El workflow [fitness.yml](../../.github/workflows/fitness.yml) las ejecuta en cada Pull Request y push. Una verificación en verde indica que estas reglas y pruebas pasaron; no demuestra propiedades que no estén cubiertas por ellas.

## Fitness functions estructurales

Se usa Import Linter, configurado en [`.importlinter`](../../.importlinter):

| ID | Regla | ADR | Verificación |
|---|---|---|---|
| FF-S1 | `src.puntos_beneficios` no puede importar `src.solicitudes`, evitando dependencia inversa entre módulos del monolito. | ADR-001 | Contrato `module-boundary`, tipo `forbidden`. |
| FF-S2 | El clasificador `src.solicitudes.ia` no importa directamente SDK de OpenAI, Anthropic, LangChain ni Google; el acceso al proveedor se mantiene detrás de `ProveedorLLM` y su adapter. | ADR-005 | Contrato `llm-adapter`, tipo `forbidden`. |

Comando local: `lint-imports`. Las relaciones entre módulos pueden conectarse mediante contratos públicos en una integración futura; la regla FF-S1 prohíbe específicamente la dependencia desde Puntos/Beneficios hacia Solicitudes, no el uso de interfaces públicas por un consumidor.

## Fitness functions de calidad

Las pruebas en [`tests/fitness/test_quality.py`](../../tests/fitness/test_quality.py) convierten medidas de escenarios en condiciones de aprobación:

| ID | Escenario | Condiciones que deben mantenerse |
|---|---|---|
| FF-Q1 | QA-02 / QA-07, continuidad y sincronización | 120 registros; cero pérdidas y duplicados; exactamente 120 efectos únicos; cero pendientes; ≤ 30 s en el modelo base. |
| FF-Q2 | QA-04, aislamiento distrital | En 132 pares ordenados, cero lecturas y escrituras cruzadas y datos originales intactos. |
| FF-Q3 | QA-05, ausencia de ámbito confiable | Rechazar las 72 operaciones con ámbito ausente, vacío o desconocido de la batería del prototipo. |

La duración para QA-02/QA-07 es simulada con 100 ms por intento y los prototipos usan datos sintéticos. Estas pruebas no demuestran latencia de red real, autenticación JWT, RLS ni aislamiento desplegado en PostgreSQL. Sus límites y supuestos siguen descritos en [iteración 2](add/iteracion-2.md) e [iteración 3](add/iteracion-3.md).

## Prueba negativa de una regla estructural

Se comprobó FF-S1 mediante una mutación temporal en `lab08-e5-fitness`: se agregó `from src.solicitudes.ia import ClasificadorResiduo` a `src/puntos_beneficios/servicio.py`. `lint-imports` terminó con código **1** e informó `module-boundary` como `BROKEN`, mostrando `src.puntos_beneficios.servicio -> src.solicitudes.ia (l.3)`. Luego se retiró la línea de prueba y se repitió el comando: los dos contratos quedaron `KEPT` (código 0). La violación no forma parte del código entregado.

## Ejecución local

```console
lint-imports
python -m pytest tests/fitness -q
```

El workflow ejecuta los mismos comandos en GitHub Actions. El último resultado debe permanecer verde antes de aprobar cada Pull Request.
