"""Documentación estructurada, sin ejecutar código ni escribir docstrings en archivos."""
import ast
import json
import re

from src.solicitudes.ia import ProveedorLLM
from src.solicitudes.prompts_json import (
    EntradaPromptInvalida, PlantillaJSON, RespuestaPromptInvalida, validar_texto,
)


def _firma(codigo):
    try:
        modulo = ast.parse(codigo)
    except (SyntaxError, ValueError, RecursionError):
        raise EntradaPromptInvalida("El codigo no tiene sintaxis Python valida") from None
    if len(modulo.body) != 1 or not isinstance(modulo.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)):
        raise EntradaPromptInvalida("Se requiere exactamente una funcion, sin sentencias externas")
    funcion = modulo.body[0]
    argumentos = funcion.args
    parametros = [a.arg for a in argumentos.posonlyargs + argumentos.args if a.arg not in {"self", "cls"}]
    if argumentos.vararg:
        parametros.append(argumentos.vararg.arg)
    parametros.extend(a.arg for a in argumentos.kwonlyargs)
    if argumentos.kwarg:
        parametros.append(argumentos.kwarg.arg)
    return funcion.name, parametros


def _parametros_docstring(docstring):
    lineas = docstring.splitlines()
    encabezados = [i for i, linea in enumerate(lineas) if re.fullmatch(r"Args:[ \t]*", linea)]
    if not encabezados:
        return []
    if len(encabezados) != 1:
        raise RespuestaPromptInvalida("El docstring contiene secciones Args duplicadas")
    nombres = []
    sangria = None
    necesita_descripcion = False
    for linea in lineas[encabezados[0] + 1:]:
        if not linea.strip():
            continue
        if not linea[0].isspace():
            break
        parametro = re.fullmatch(r"([ \t]+)(\*{0,2}[A-Za-z_]\w*)(?:[ \t]*\([^)]*\))?:[ \t]*(.*)", linea)
        if parametro:
            if sangria is None:
                sangria = len(parametro[1])
            if len(parametro[1]) != sangria or necesita_descripcion:
                raise RespuestaPromptInvalida("Formato de parametros Args invalido")
            nombres.append(parametro[2].lstrip("*"))
            necesita_descripcion = not parametro[3].strip()
        else:
            profundidad = len(linea) - len(linea.lstrip())
            if sangria is None or profundidad <= sangria:
                raise RespuestaPromptInvalida("Descripcion de parametro invalida")
            necesita_descripcion = False
    if necesita_descripcion:
        raise RespuestaPromptInvalida("Parametro sin descripcion en Args")
    return nombres


class GeneradorDocstrings:
    def __init__(self, proveedor: ProveedorLLM, version="v3.1"):
        self.contrato = PlantillaJSON(proveedor, "docstrings", version)

    def generar(self, codigo: str) -> dict:
        validar_texto(codigo, "codigo")
        nombre, esperados = _firma(codigo)
        resultado = self.contrato.generar({
            "funcion": codigo, "funcion_json": json.dumps(codigo, ensure_ascii=False),
        })
        if resultado["nombre"] != nombre:
            raise RespuestaPromptInvalida("El nombre de respuesta no coincide con la funcion")
        declarados = [p["nombre"] for p in resultado["parametros"]]
        documentados = _parametros_docstring(resultado["docstring"])
        tiene_args = bool(re.search(r"^Args:[ \t]*$", resultado["docstring"], re.MULTILINE))
        if declarados != esperados or documentados != esperados or (not esperados and tiene_args):
            raise RespuestaPromptInvalida("Los parametros JSON y Args no coinciden con la firma")
        return resultado
