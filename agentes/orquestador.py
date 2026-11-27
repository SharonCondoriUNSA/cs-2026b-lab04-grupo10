"""Coordinación planificador -> ejecutor -> revisor para el issue 2 de EcoRecicla.

El planificador no dispone de herramientas de escritura. El revisor puede inspeccionar
y probar, pero no editar. Cada variante debe recibir su propia copia del estado inicial.
"""
from pathlib import Path

from agente.herramientas import Herramientas
from agente.nucleo import Agente
from agente.politica import Politica

MAX_RONDAS = 2
HERRAMIENTAS_REVISOR = {"leer_archivo", "buscar", "ejecutar_pruebas", "ver_cambios"}


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
    veredicto = ""

    for numero in range(1, MAX_RONDAS + 1):
        if numero > len(modelos.get("ejecutor", [])) or numero > len(modelos.get("revisor", [])):
            veredicto = "CAMBIOS SOLICITADOS. No hay trayectorias grabadas disponibles para otra ronda."
            break
        retro = "" if numero == 1 else f"\nCambios solicitados por el revisor: {veredicto}"
        ejecutor = Agente(
            f"ejecutor_r{numero}", modelos["ejecutor"][numero - 1], herramientas,
            Politica(max_pasos=12),
            f"Resuelve issues/ISSUE-02.md siguiendo este plan:\n{plan}{retro}\n"
            f"Herramientas disponibles:\n{herramientas.catalogo()}",
            trazas / f"ejecutor-r{numero}.jsonl",
        )
        resultado = ejecutor.ejecutar()
        revisor = Agente(
            f"revisor_r{numero}", modelos["revisor"][numero - 1], herramientas,
            Politica(herramientas_permitidas=set(HERRAMIENTAS_REVISOR), max_pasos=8),
            "Revisa independientemente el cambio contra ISSUE-02.md. Lee el requisito, "
            "inspecciona el diff y ejecuta las pruebas. Termina con APROBADO o "
            "CAMBIOS SOLICITADOS y evidencia concreta. No edites archivos.\n"
            f"Resumen del ejecutor: {resultado}",
            trazas / f"revisor-r{numero}.jsonl",
        )
        veredicto = revisor.ejecutar()
        agentes.extend((ejecutor, revisor))
        if veredicto.lstrip().startswith("APROBADO"):
            break

    return {
        "plan": plan,
        "resultado_ejecutor": resultado,
        "veredicto": veredicto,
        "rondas": numero,
        "agentes": agentes,
        "aprobado": veredicto.lstrip().startswith("APROBADO"),
    }
