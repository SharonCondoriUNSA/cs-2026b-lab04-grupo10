"""Genera el gráfico E8 desde los seis reportes de Promptfoo versionados.

Requiere matplotlib, solo para regenerar la figura, no para ejecutar la aplicación.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent


def main():
    versiones = ("v1", "v2", "v3")
    fig, ax = plt.subplots(figsize=(10, 5.5), layout="constrained")
    for tarea, etiqueta, color, desplazamiento in (
        ("criterios", "A · Criterios de aceptación", "#2166ac", -0.19),
        ("docstrings", "B · Docstrings", "#16836b", 0.19),
    ):
        tasas, cuentas = [], []
        for version in versiones:
            reporte = json.loads((BASE / tarea / f"resultados-{version}.json").read_text(encoding="utf-8"))
            stats = reporte["results"]["stats"]
            if stats["errors"]:
                raise ValueError("El gráfico requiere reportes sin errores de ejecución")
            total = stats["successes"] + stats["failures"]
            if not total:
                raise ValueError("El reporte no contiene casos")
            tasas.append(100 * stats["successes"] / total)
            cuentas.append(f'{stats["successes"]}/{total}')
        barras = ax.bar([i + desplazamiento for i in range(3)], tasas, width=0.36,
                        label=etiqueta, color=color)
        ax.bar_label(barras, labels=[f"{t:g}% ({c})" for t, c in zip(tasas, cuentas)],
                     padding=5, fontsize=10)
    ax.set(title="EcoRecicla AQP · Evaluación de prompts grabados", ylabel="Casos aprobados (%)",
           xticks=range(3), xticklabels=versiones, ylim=(0, 120))
    ax.set_yticks(range(0, 101, 25))
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.13), frameon=False, ncol=2)
    fig.text(0.02, -0.04, "8 casos por tarea · 0 errores de ejecución · No estima rendimiento de un modelo en vivo",
             fontsize=10, color="#444444")
    destino = BASE / "img" / "resultados-versiones.png"
    destino.parent.mkdir(exist_ok=True)
    fig.savefig(destino, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(destino)


if __name__ == "__main__":
    main()
