"""Carga de plantillas versionadas y validación estricta para el Lab09."""
import json
from pathlib import Path
import re

from jsonschema import Draft7Validator, ValidationError

from src.solicitudes.ia import ProveedorLLM

RAIZ_PROMPTS = Path(__file__).resolve().parents[2] / "prompts"
VERSIONES = frozenset({"v1", "v2", "v3", "v3.1"})
MAX_ENTRADA = 16_000
MAX_RESPUESTA = 64_000


class EntradaPromptInvalida(ValueError):
    """La entrada no puede procesarse dentro del alcance del generador."""


class RespuestaPromptInvalida(ValueError):
    """La respuesta del proveedor incumple el contrato de la tarea."""


def validar_texto(valor, nombre, maximo=MAX_ENTRADA):
    if not isinstance(valor, str) or not valor.strip() or len(valor) > maximo:
        raise EntradaPromptInvalida(f"{nombre}: texto no vacio de hasta {maximo} caracteres requerido")


def _objeto_sin_duplicados(pares):
    objeto = {}
    for clave, valor in pares:
        if clave in objeto:
            raise ValueError("Clave JSON duplicada")
        objeto[clave] = valor
    return objeto


def _rechazar_constante(valor):
    raise ValueError("Constante no permitida en JSON")


class PlantillaJSON:
    """No ejecuta plantillas ni respuestas, solo sustituye variables conocidas."""
    def __init__(self, proveedor: ProveedorLLM, tarea: str, version: str):
        if tarea not in {"criterios", "docstrings"} or version not in VERSIONES:
            raise EntradaPromptInvalida("Tarea o version de plantilla no permitida")
        carpeta = RAIZ_PROMPTS / tarea
        self.plantilla = (carpeta / f"{version}.txt").read_text(encoding="utf-8")
        nombre = "esquema.json" if tarea == "criterios" else "contrato.json"
        esquema = json.loads((carpeta / nombre).read_text(encoding="utf-8"))
        Draft7Validator.check_schema(esquema)
        self.validador = Draft7Validator(esquema)
        self.proveedor = proveedor

    def generar(self, variables):
        def sustituir(coincidencia):
            nombre = coincidencia.group(1)
            if nombre not in variables:
                raise EntradaPromptInvalida("Variable requerida por la plantilla no disponible")
            return variables[nombre]

        # Una sola pasada. Un {{nombre}} dentro de los datos no se vuelve a interpretar.
        prompt = re.sub(r"\{\{\s*(\w+)\s*\}\}", sustituir, self.plantilla)
        respuesta = self.proveedor.completar(prompt)
        if not isinstance(respuesta, str) or len(respuesta) > MAX_RESPUESTA:
            raise RespuestaPromptInvalida("El proveedor debe devolver texto dentro del limite permitido")
        try:
            resultado = json.loads(respuesta, object_pairs_hook=_objeto_sin_duplicados,
                                   parse_constant=_rechazar_constante)
            self.validador.validate(resultado)
        except (ValueError, ValidationError, RecursionError):
            raise RespuestaPromptInvalida("La respuesta no es JSON estricto conforme al esquema") from None
        return resultado
