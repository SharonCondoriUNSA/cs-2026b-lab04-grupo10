"""Coordinación planificador -> ejecutor -> revisor para el issue 2 de EcoRecicla.

El planificador no dispone de herramientas de escritura. El revisor puede inspeccionar
y probar, pero no editar. Cada variante debe recibir su propia copia del estado inicial.
"""
from pathlib import Path

from agente.herramientas import Herramientas
from agente.nucleo import Agente
from agente.politica import Politica
from agente.traza import prueba_pasada

MAX_RONDAS = 2
HERRAMIENTAS_REVISOR = {"leer_archivo", "buscar", "ejecutar_pruebas", "ver_cambios"}


def veredicto_revisor(eventos):
    final = eventos[-1]
    if final["tipo"] != "final":
        return "CAMBIOS SOLICITADOS. El revisor terminó sin emitir un veredicto."
    texto = final["texto"].strip()
    if texto.startswith("APROBADO") and not prueba_pasada(eventos):
        return "CAMBIOS SOLICITADOS. El revisor no verificó una prueba final aprobada."
    return texto


def ejecutar_orquestado(raiz_trabajo: Path, modelos: dict, trazas: Path) -> dict:
    """Ejecuta roles grabados sobre una copia de trabajo ya preparada.

    ``modelos`` debe contener ``planificador`` y listas ``ejecutor``/``revisor``
    (una entrada por ronda). Retorna resultados y agentes para medir el contexto.
    """
    herramientas = Herramientas(raiz_trabajo)
    planificador = Agente(
        "planificador", modelos["planificador"], herramientas,
        Politica(herramientas_permitidas=set(), max_pasos=1),
        "Planifica la solución de issues/ISSUE-02.md. No ejecutes acciones; devuelve "
        "un plan breve que respete el contrato y los límites del sandbox.",
        trazas / "planificador.jsonl",
    )
    plan = planificador.ejecutar()
    agentes = [planificador]
    resultado = ""
    veredicto = "Sin ronda de revisión disponible."
    rondas = 0

    for numero, modelo_ejecutor, modelo_revisor in zip(
        range(1, MAX_RONDAS + 1), modelos["ejecutor"], modelos["revisor"]
    ):
        retro = "" if numero == 1 else f"\nCambios solicitados por el revisor: {veredicto}"
        ejecutor = Agente(
            f"ejecutor_r{numero}", modelo_ejecutor, herramientas,
            Politica(max_pasos=12),
            f"Resuelve issues/ISSUE-02.md siguiendo este plan:\n{plan}{retro}\n"
            f"Herramientas disponibles:\n{herramientas.catalogo()}",
            trazas / f"ejecutor-r{numero}.jsonl",
        )
        resultado = ejecutor.ejecutar()
        revisor = Agente(
            f"revisor_r{numero}", modelo_revisor, herramientas,
            Politica(herramientas_permitidas=set(HERRAMIENTAS_REVISOR), max_pasos=8),
            "Revisa independientemente el cambio contra ISSUE-02.md. Lee el requisito, "
            "inspecciona el diff y ejecuta las pruebas. Termina con APROBADO o "
            "CAMBIOS SOLICITADOS y evidencia concreta. No edites archivos.\n"
            f"Resumen del ejecutor: {resultado}",
            trazas / f"revisor-r{numero}.jsonl",
        )
        revisor.ejecutar()
        veredicto = veredicto_revisor(revisor.eventos)
        rondas = numero
        agentes.extend((ejecutor, revisor))
        if veredicto.lstrip().startswith("APROBADO"):
            break

    return {
        "plan": plan,
        "resultado_ejecutor": resultado,
        "veredicto": veredicto,
        "rondas": rondas,
        "agentes": agentes,
        "aprobado": veredicto.lstrip().startswith("APROBADO"),
    }
