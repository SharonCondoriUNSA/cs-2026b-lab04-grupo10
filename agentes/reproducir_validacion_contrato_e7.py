"""Reproduce el rechazo contractual de una decisión inválida del agente en E7."""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agente.herramientas import Herramientas
from agente.modelos import ModeloGrabado
from agente.nucleo import Agente
from agente.politica import Politica
from agente.traza import a_mermaid


def main() -> None:
    trayectoria = RAIZ / "agentes" / "trayectorias" / "validacion-contrato-e7.json"
    traza = RAIZ / "agentes" / "trazas" / "validacion-contrato-e7.jsonl"
    agente = Agente(
        "ejecutor-prueba-contrato",
        ModeloGrabado(trayectoria),
        Herramientas(RAIZ),
        Politica(),
        "Probar que el contrato rechaza una herramienta no existente.",
        traza,
    )
    respuesta = agente.ejecutar()
    eventos = agente.eventos
    estados = [evento["estado"] for evento in eventos]
    if "CONTRATO_INVALIDO" not in estados or estados[-1] != "FINALIZADO":
        raise SystemExit(f"La comprobación no produjo el resultado esperado: {estados}")

    mermaid = traza.with_suffix(".mmd")
    mermaid.write_text(a_mermaid(eventos), encoding="utf-8")
    rechazo = next(evento for evento in eventos if evento["estado"] == "CONTRATO_INVALIDO")
    print(f"Estado: {rechazo['estado']}")
    print(f"Observación: {rechazo['observacion']}")
    print(f"Respuesta final: {respuesta}")
    print(f"Traza: {traza.relative_to(RAIZ)}")
    print(f"Diagrama: {mermaid.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
