"""Generación de criterios mediante el puerto ProveedorLLM del Lab07."""
import json

from src.solicitudes.ia import ProveedorLLM
from src.solicitudes.prompts_json import (
    PlantillaJSON, RespuestaPromptInvalida, validar_texto,
)


class GeneradorCriterios:
    def __init__(self, proveedor: ProveedorLLM, version="v3.1"):
        self.contrato = PlantillaJSON(proveedor, "criterios", version)

    def generar(self, historia_id: str, historia: str) -> dict:
        validar_texto(historia_id, "historia_id", maximo=40)
        validar_texto(historia, "historia")
        resultado = self.contrato.generar({
            "id": historia_id, "historia": historia,
            "id_json": json.dumps(historia_id, ensure_ascii=False),
            "historia_json": json.dumps(historia, ensure_ascii=False),
        })
        if resultado["historia_id"] != historia_id:
            raise RespuestaPromptInvalida("El identificador de respuesta no coincide con la historia")
        return resultado
