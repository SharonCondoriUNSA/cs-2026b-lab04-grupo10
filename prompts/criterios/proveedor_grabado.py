"""Proveedor local de respuestas grabadas para la evaluación de E2."""

from pathlib import Path


BASE = Path(__file__).parent / "grabaciones" / "v1"


def call_api(prompt, options, context):
    """Devuelve la grabación correspondiente al ID del caso de prueba."""
    case_id = context.get("vars", {}).get("id")
    if not case_id:
        return {"error": "El caso de prueba debe proporcionar vars.id"}

    recording = BASE / f"{case_id}.txt"
    if not recording.is_file():
        return {"error": f"No existe una grabación para {case_id}"}

    return {"output": recording.read_text(encoding="utf-8")}
