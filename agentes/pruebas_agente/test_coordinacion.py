"""Casos de regresión de E5 para las rondas y el veredicto del revisor."""
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agente.herramientas import Herramientas
from agente.traza import prueba_pasada
from ejecutar_issue_02 import escribir_diagramas
from orquestador import ejecutar_orquestado


def modelo(*decisiones):
    return Mock(decidir=Mock(side_effect=decisiones))


def final(texto):
    return {"pensamiento": "Emitir el resultado", "final": texto}


@pytest.mark.parametrize("segunda_ronda", [False, True])
def test_solo_cuenta_rondas_ejecutadas_y_contrasta_veredicto(tmp_path, monkeypatch, segunda_ronda):
    pruebas = iter(["pytest exit=1\n1 failed", "pytest exit=0\n1 passed"])
    monkeypatch.setattr(Herramientas, "ejecutar_pruebas", lambda self: next(pruebas))
    probar = {"pensamiento": "Comprobar la ruta", "accion": "ejecutar_pruebas", "args": {}}
    cantidad = 2 if segunda_ronda else 1
    modelos = {
        "planificador": modelo(final("Revisar las rutas")),
        "ejecutor": [modelo(final("Fin del turno")) for _ in range(cantidad)],
        "revisor": [modelo(probar, final("APROBADO. Revisión completada")) for _ in range(cantidad)],
    }
    resultado = ejecutar_orquestado(tmp_path, modelos, tmp_path)
    assert resultado["rondas"] == cantidad
    assert resultado["aprobado"] is segunda_ronda
    eventos = [e for agente in resultado["agentes"] for e in agente.eventos]
    escribir_diagramas(tmp_path, [], eventos)
    diagrama = (tmp_path / "issue-02-orquestado.mmd").read_text(encoding="utf-8")
    assert "R-->>P: CAMBIOS SOLICITADOS" in diagrama
    assert ("R-->>P: APROBADO" in diagrama) is segunda_ronda


def test_una_prueba_verde_antes_de_editar_no_verifica_el_cambio():
    prueba = {"tipo": "accion", "accion": "ejecutar_pruebas", "bloqueada": False,
              "observacion": "pytest exit=0\n1 passed"}
    edicion = {"tipo": "accion", "accion": "editar_archivo", "bloqueada": False,
               "observacion": "OK: archivo modificado"}
    assert not prueba_pasada([prueba, edicion])
    assert prueba_pasada([prueba, edicion, prueba])
