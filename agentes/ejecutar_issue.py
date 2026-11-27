"""Ejecuta o reproduce un issue en una copia de su versión previa a la corrección."""
import argparse
import json
import subprocess
from pathlib import Path

from agente.herramientas import Herramientas, HerramientasConMemoria
from agente.modelos import ModeloGrabado, ModeloInteractivo
from agente.nucleo import Agente
from agente.politica import MODULO_EDITABLE, Politica


BASES = {
    "01": "43e5f70edfb8a64f5ee0c565ddfaa9ec5a7bf120",  # E1
    "03": "745aa668e50a8692ab0862752e0ed25f17964639",  # E3
}
AGENTES = Path(__file__).resolve().parent
ARCHIVOS = (
    MODULO_EDITABLE,
    "src/lab10/__init__.py", "src/puntos_beneficios/servicio.py", "src/puntos_beneficios/reglas.py",
)


def ejecutar(salida, grabacion=None, numero="01"):
    base = BASES[numero]
    salida.mkdir(parents=True, exist_ok=False)
    copia = salida / "trabajo"
    for ruta in (*ARCHIVOS, f"issues/ISSUE-{numero}.md", f"tests/test_issue_{numero}.py"):
        contenido = subprocess.check_output(["git", "show", f"{base}:{ruta}"], cwd=AGENTES.parent)
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
        modelo = ModeloInteractivo(decisiones / f"issue-{numero}.json")

    politica = Politica()
    if numero == "03":
        herramientas = HerramientasConMemoria(copia)
        politica.herramientas_permitidas.update({"mapa_repo", "anotar", "leer_notas"})
    else:
        herramientas = Herramientas(copia)
    objetivo = (
        f"Resuelve issues/ISSUE-{numero}.md en EcoRecicla AQP. Reproduce el fallo, propone una "
        "edición en src/lab10/operaciones.py, verifica la prueba y revisa el diff. "
        "Emite una línea JSON por turno con pensamiento (etiqueta breve de la tarea), "
        "accion y args (objeto), o con pensamiento y final. Máximo 12 decisiones. "
        "La revisión del PR corresponde a una persona. Herramientas disponibles:\n"
        + json.dumps(herramientas.catalogo(), ensure_ascii=False, indent=2)
    )
    agente = Agente("ejecutor", modelo, herramientas, politica, objetivo, trazas / f"issue-{numero}.jsonl")
    print(agente.ejecutar())
    return 0 if agente.eventos[-1]["estado"] == "FINALIZADO" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue", choices=BASES, default="01", help="01 (E2) o 03 (E4)")
    parser.add_argument("--salida", required=True, type=Path, help="carpeta nueva para esta ejecución")
    parser.add_argument("--reproducir", type=Path, metavar="JSON", help="decisiones grabadas en una sesión previa")
    args = parser.parse_args()
    return ejecutar(args.salida, args.reproducir, args.issue)


if __name__ == "__main__":
    raise SystemExit(main())
