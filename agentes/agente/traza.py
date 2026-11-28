"""Convierte la traza JSONL del ejecutor en un diagrama Mermaid y métricas."""
import argparse
import json
from pathlib import Path


def prueba_pasada(eventos):
    """Comprueba la última prueba ejecutada sobre la versión final de la copia."""
    for e in reversed(eventos):
        if e["tipo"] != "accion" or e["bloqueada"]:
            continue
        accion, observacion = e["accion"], e["observacion"]
        if accion == "editar_archivo" and observacion.startswith("OK:"):
            return False
        if accion == "ejecutar_pruebas" or (
            accion == "ejecutar_comando" and e["args"].get("comando") == "python -m pytest -q"
        ):
            return observacion.partition("\n")[0] == "pytest exit=0"
    return False


def etiqueta(texto):
    return (texto.replace("#", " ").replace(";", ",").replace("<", "‹")
            .replace(">", "›").replace("\n", " ")[:100])


def resumir(evento):
    obs = evento["observacion"]
    if obs.startswith("ERROR"):
        return obs
    if evento["accion"] == "leer_archivo":
        return Path(evento["args"]["ruta"]).name
    if evento["accion"] == "mapa_repo":
        archivos = sum(linea.endswith(".py") and not linea.startswith(" ") for linea in obs.splitlines())
        return f"Mapa de {archivos} archivos Python"
    if evento["accion"] == "leer_notas":
        cantidad = sum(linea.startswith("- ") for linea in obs.splitlines())
        return f"Notas recuperadas: {cantidad}"
    if evento["accion"] == "ver_cambios" and obs.startswith("---"):
        return f"Diff de {len(obs.splitlines())} líneas"
    return obs.splitlines()[-1] if obs else "(sin salida)"


def a_mermaid(eventos):
    lineas = ["sequenceDiagram", "    autonumber", "    actor U as Solicitante",
              "    participant A as Ejecutor ReAct", "    participant C as Contrato y política",
              "    participant H as Herramientas"]
    for e in eventos:
        if e["tipo"] == "objetivo":
            lineas.append("    U->>A: Objetivo del issue")
        elif e["tipo"] == "accion":
            lineas.append(f"    A->>C: {etiqueta(e['accion'])}")
            if e["bloqueada"]:
                lineas.append(f"    C--xA: {etiqueta(e['observacion'])}")
            else:
                lineas.extend(["    C->>H: Ejecutar", f"    H-->>A: {etiqueta(resumir(e))}"])
        elif e["tipo"] == "final":
            lineas.extend(["    A->>C: Respuesta final", "    C-->>A: Válida",
                           "    A-->>U: Resultado para revisión"])
        elif e["tipo"] == "limite":
            lineas.append("    A-->>U: Presupuesto agotado")
    return "\n".join(lineas) + "\n"


def metricas(eventos):
    acciones = [e for e in eventos if e["tipo"] == "accion"]
    return {
        "decisiones": sum(e["tipo"] in ("accion", "final") for e in eventos),
        "acciones_ejecutadas": sum(not e["bloqueada"] for e in acciones),
        "rechazos_contrato": sum(e["estado"] == "CONTRATO_INVALIDO" for e in acciones),
        "bloqueos_politica": sum(e["estado"] == "BLOQUEADO" for e in acciones),
        "contexto_final_caracteres": eventos[-1]["contexto_caracteres"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    predeterminada = Path(__file__).resolve().parents[1] / "trazas" / "issue-01.jsonl"
    parser.add_argument("archivo", type=Path, nargs="?", default=predeterminada)
    archivo = parser.parse_args().archivo
    eventos = [json.loads(linea) for linea in archivo.read_text(encoding="utf-8").splitlines()]
    archivo.with_suffix(".mmd").write_text(a_mermaid(eventos), encoding="utf-8")
    print(json.dumps(metricas(eventos), ensure_ascii=False, indent=2))
