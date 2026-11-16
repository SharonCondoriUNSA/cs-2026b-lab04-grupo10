"""Reproduce respuestas del ejercicio E5, sin llamadas a modelos ni APIs."""
from pathlib import Path

BASE = Path(__file__).parent
IDS = {
    "criterios": {"RT01", "RT03", "RT05", "NC01"},
    "docstrings": {"RT02", "RT04", "RT06", "NC02"},
}


def call_api(prompt, options, context):
    configuracion = options.get("config", {})
    fase = configuracion.get("fase")
    tarea = configuracion.get("tarea")
    identificador = context.get("vars", {}).get("id")
    if fase not in {"antes", "despues"} or tarea not in IDS or identificador not in IDS[tarea]:
        return {"error": "Fase, tarea o identificador no permitido para E5"}
    archivo = BASE / "grabaciones" / fase / f"{identificador}.txt"
    if not archivo.is_file():
        return {"error": f"Grabacion E5 inexistente: {fase}/{identificador}"}
    return {"output": archivo.read_text(encoding="utf-8")}
