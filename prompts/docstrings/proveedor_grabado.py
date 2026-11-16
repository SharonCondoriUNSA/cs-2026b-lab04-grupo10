"""Proveedor local que reproduce respuestas registradas para los prompts de docstrings."""

from pathlib import Path


ROOT = Path(__file__).parent


def call_api(prompt, options, context):
    case_id = context.get("vars", {}).get("id")
    if not case_id:
        return {"error": "El caso de prueba debe proporcionar vars.id"}
    version = options.get("config", {}).get("version", "v1")
    if version not in {"v1", "v2", "v3"}:
        return {"error": f"Versión de grabación no válida: {version}"}
    recording = ROOT / "grabaciones" / version / f"{case_id}.txt"
    if not recording.is_file():
        return {"error": f"No existe una grabación para {case_id}"}
    return {"output": recording.read_text(encoding="utf-8")}
