"""Ejecuta o reproduce E2 sobre una copia de los archivos necesarios del commit E1."""
import argparse
import json
import subprocess
from pathlib import Path

from agente.herramientas import Herramientas
from agente.modelos import ModeloGrabado, ModeloInteractivo
from agente.nucleo import Agente
from agente.politica import MODULO_EDITABLE, Politica


BASE_E1 = "43e5f70edfb8a64f5ee0c565ddfaa9ec5a7bf120"
AGENTES = Path(__file__).resolve().parent
ARCHIVOS = (
    "issues/ISSUE-01.md", "tests/test_issue_01.py", MODULO_EDITABLE,
    "src/lab10/__init__.py", "src/puntos_beneficios/servicio.py", "src/puntos_beneficios/reglas.py",
)


def ejecutar(salida, grabacion=None):
    salida.mkdir(parents=True, exist_ok=False)
    copia = salida / "trabajo"
    for ruta in ARCHIVOS:
        contenido = subprocess.check_output(["git", "show", f"{BASE_E1}:{ruta}"], cwd=AGENTES.parent)
        destino = copia / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(contenido)
    trazas = salida / "trazas"
    trazas.mkdir()
    if grabacion:
        modelo = ModeloGrabado(grabacion)
    else:
        decisiones = salida / "trayectorias"
        decisiones.mkdir()
        modelo = ModeloInteractivo(decisiones / "issue-01.json")

    herramientas = Herramientas(copia)
    objetivo = (
        "Resuelve issues/ISSUE-01.md en EcoRecicla AQP. Reproduce el fallo, propone una "
        "edición en src/lab10/operaciones.py, verifica la prueba y revisa el diff. "
        "Emite una línea JSON por turno con pensamiento (etiqueta breve de la tarea), "
        "accion y args (objeto), o con pensamiento y final. Máximo 12 decisiones. "
        "La revisión del PR corresponde a una persona. Herramientas disponibles:\n"
        + json.dumps(herramientas.catalogo(), ensure_ascii=False, indent=2)
    )
    agente = Agente("ejecutor", modelo, herramientas, Politica(), objetivo, trazas / "issue-01.jsonl")
    print(agente.ejecutar())
    return 0 if agente.eventos[-1]["estado"] == "FINALIZADO" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", required=True, type=Path, help="carpeta nueva para esta ejecución")
    parser.add_argument("--reproducir", type=Path, metavar="JSON", help="decisiones grabadas en una sesión previa")
    args = parser.parse_args()
    raise SystemExit(ejecutar(args.salida, args.reproducir))
