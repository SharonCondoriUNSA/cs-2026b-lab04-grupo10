# E6. Integración de los prompts en el código

## Contrato de la integración

Los generadores reutilizan **ProveedorLLM.completar(prompt)** del Lab07, no crean otro puerto ni importan SDK de proveedores. El proveedor se inyecta en el constructor y las pruebas lo implementan leyendo grabaciones existentes, sin APIs.

| Componente | Responsabilidad |
|---|---|
| [GeneradorCriterios](../src/solicitudes/generador_criterios.py) | Genera criterios y exige que historia_id coincida con la entrada. |
| [GeneradorDocstrings](../src/solicitudes/generador_docstrings.py) | Analiza una función mediante AST, genera documentación y contrasta nombre y parámetros del JSON y Args con la firma. |
| [PlantillaJSON y excepciones](../src/solicitudes/prompts_json.py) | Carga la plantilla por versión, sustituye datos en una sola pasada y valida la respuesta con el esquema de la tarea. |
| [Pruebas con proveedor grabado](../tests/test_generadores_prompt.py) | Aceptación y rechazo mediante respuestas guardadas de E2–E5. Las alteraciones de control se realizan solo en memoria. |

Flujo: entrada validada → plantilla versionada → ProveedorLLM → JSON estricto → JSON Schema → coherencia con la entrada → diccionario validado. Si falla una comprobación, se lanza una excepción y no se devuelve una respuesta parcialmente aceptada.

## Versiones y validación

Se permiten v1, v2, v3 y v3.1, con **v3.1 por defecto**. Las plantillas y esquemas se leen desde la carpeta prompts del repositorio con rutas basadas en el módulo, no en el directorio de trabajo. Una versión arbitraria o una ruta como `../../README` se rechaza.

Las versiones anteriores se conservan para comparación, no se asume que v1 produzca una salida aceptable. v3.1 recibe cadenas JSON serializadas. Los marcadores que aparezcan dentro de los datos no se vuelven a sustituir ni a interpretar como una plantilla.

El validador usa los esquemas Draft-07 ya existentes. No elimina Markdown ni intenta reparar salidas inválidas. Rechaza claves JSON duplicadas, constantes no JSON, texto de tipo incorrecto y respuestas superiores a 64000 caracteres. Las entradas se limitan a 16000 caracteres y el identificador de historia a 40. Son presupuestos locales de esta integración, no medidas de contexto de un modelo ni requisitos textuales del docente.

En docstrings se acepta un único fragmento con una función normal o asíncrona, sin sentencias externas. AST permite identificar la firma sin ejecutar el cuerpo, sus anotaciones ni decoradores. La correspondencia de parámetros se verifica en el formato Args usado en el laboratorio. No se implementa un analizador universal de todos los estilos de documentación.

## Ejemplo con proveedor grabado

Ejecutar desde la raíz del repositorio, con las dependencias instaladas:

```python
from pathlib import Path
from src.solicitudes.ia import ProveedorLLM
from src.solicitudes.generador_criterios import GeneradorCriterios

class ProveedorArchivo(ProveedorLLM):
    def __init__(self, archivo):
        self.archivo = archivo

    def completar(self, prompt):
        return self.archivo.read_text(encoding="utf-8")

proveedor = ProveedorArchivo(Path("prompts/seguridad/grabaciones/despues/NC01.txt"))
resultado = GeneradorCriterios(proveedor, version="v3.1").generar(
    "NC01",
    "Como vecino, quiero consultar el estado de mi solicitud para saber si ya fue atendida.",
)
print(resultado["historia_id"])
```

El proveedor de archivo es un ejemplo local de sustitución, no interpreta el prompt ni genera texto nuevo. La ruta la elige el código de aplicación, no se obtiene de una respuesta del modelo. Las pruebas aplican este mismo mecanismo a grabaciones válidas y a salidas reales de v1 que no cumplen el contrato.

## Instalación y verificaciones

```console
python -m pip install -r requirements-lab09.txt
python -m unittest discover -s tests -p test_generadores_prompt.py -v
```

Las pruebas cubren respuestas válidas e inválidas en ambas tareas, identidad de historia, parámetros del docstring, selección de versión, rutas no permitidas, datos sin reinterpretación, código no ejecutado, JSON duplicado o no estándar, tipos y límites de tamaño.

## Límites

El contrato garantiza estructura y algunas correspondencias con la entrada, no la exactitud semántica completa de un criterio o una descripción. La salida sigue siendo un borrador para revisión humana. No se ejecutan escenarios generados, no se registran solicitudes, no se acreditan puntos ni se escriben docstrings automáticamente en archivos.

Los proveedores grabados de las pruebas no evalúan el comportamiento de un LLM en vivo. Los errores del proveedor se propagan, no se añaden reintentos de generación ni fallbacks que puedan ocultar un fallo. E6 requiere disponer de los archivos de prompts en el checkout, no prepara un paquete distribuible ni un endpoint web.
