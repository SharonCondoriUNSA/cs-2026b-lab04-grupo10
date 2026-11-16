"""Ejecuta promptfoo sin APIs y distingue fallos esperados de errores de ejecución."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

RAIZ = Path(__file__).resolve().parents[1]
# Tasas de referencia de las respuestas grabadas. Las bases fallan deliberadamente.
EVALUACIONES = (
    ("criterios-v1", "prompts/criterios", "promptfooconfig.yaml", 8, 0),
    ("criterios-v2", "prompts/criterios", "promptfooconfig-v2.yaml", 8, 2),
    ("criterios-v3", "prompts/criterios", "promptfooconfig-v3.yaml", 8, 8),
    ("docstrings-v1", "prompts/docstrings", "promptfooconfig-v1.yaml", 8, 0),
    ("docstrings-v2", "prompts/docstrings", "promptfooconfig-v2.yaml", 8, 8),
    ("docstrings-v3", "prompts/docstrings", "promptfooconfig-v3.yaml", 8, 8),
    ("seguridad-criterios-antes", "prompts/seguridad", "promptfooconfig-criterios-antes.yaml", 4, 4),
    ("seguridad-criterios-despues", "prompts/seguridad", "promptfooconfig-criterios-despues.yaml", 4, 4),
    ("seguridad-docstrings-antes", "prompts/seguridad", "promptfooconfig-docstrings-antes.yaml", 4, 4),
    ("seguridad-docstrings-despues", "prompts/seguridad", "promptfooconfig-docstrings-despues.yaml", 4, 4),
)


def validar_reporte(reporte, codigo, total, aprobados):
    resultados = reporte.get("results", {})
    estadisticas = resultados.get("stats", {})
    filas = resultados.get("results", [])
    if codigo not in {0, 100}:
        raise ValueError("La CLI termino con un error no esperado")
    if estadisticas.get("errors") != 0:
        raise ValueError("El reporte contiene errores de ejecucion")
    if (estadisticas.get("successes"), estadisticas.get("failures")) != (aprobados, total - aprobados):
        raise ValueError("La tasa cambio respecto a las grabaciones revisadas")
    if len(filas) != total or not all(fila.get("gradingResult") for fila in filas):
        raise ValueError("Faltan casos o resultados de las aserciones")
    esperada = 0 if aprobados == total else 100
    if codigo != esperada:
        raise ValueError("El codigo de salida contradice el resultado de evaluacion")
    return {"aprobados": aprobados, "total": total, "errores": 0,
            "tasa": round(aprobados * 100 / total, 2), "codigo": codigo}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli-node", type=Path, help="CLI ya instalada, solo para reproduccion local")
    parser.add_argument("--salida", type=Path, default=RAIZ / ".ci-resultados")
    opciones = parser.parse_args()
    salida = opciones.salida.resolve()
    salida.mkdir(parents=True, exist_ok=True)
    cli = (["node", str(opciones.cli_node.resolve())] if opciones.cli_node else
           ["npx.cmd" if os.name == "nt" else "npx", "--yes", "promptfoo@0.110.0"])
    entorno = os.environ.copy()
    entorno.update(PROMPTFOO_DISABLE_TELEMETRY="1", PROMPTFOO_DISABLE_UPDATE="1",
                   PROMPTFOO_PYTHON=sys.executable)
    resumen = []
    for nombre, carpeta, configuracion, total, aprobados in EVALUACIONES:
        reporte = salida / f"{nombre}.json"
        if reporte.exists():
            raise RuntimeError(f"Usa una carpeta de salida nueva, ya existe {reporte.name}")
        with (salida / f"{nombre}.log").open("w", encoding="utf-8") as registro:
            proceso = subprocess.run(cli + ["eval", "--no-cache", "--no-write", "--no-progress-bar",
                                            "-c", configuracion, "-o", str(reporte)],
                                     cwd=RAIZ / carpeta, env=entorno, stdout=registro,
                                     stderr=subprocess.STDOUT, timeout=300, check=False)
        try:
            resultado = validar_reporte(json.loads(reporte.read_text(encoding="utf-8")),
                                        proceso.returncode, total, aprobados)
        except (OSError, ValueError) as error:
            raise RuntimeError(f"{nombre}: {error}. Consulta el registro de la CLI") from error
        resumen.append({"evaluacion": nombre, **resultado})
        print(f"{nombre}: {aprobados}/{total}, 0 errores", flush=True)
    (salida / "resumen.json").write_text(json.dumps(resumen, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
