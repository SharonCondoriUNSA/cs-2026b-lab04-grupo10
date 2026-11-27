"""Pruebas E6 para aprobación humana de cada edición propuesta."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from agente.aprobacion import aprobar_edicion_en_consola
from agente.herramientas import Herramientas
from agente.modelos import ModeloGrabado
from agente.nucleo import Agente
from agente.politica import MODULO_EDITABLE, Politica


EDICION = {
    "ruta": MODULO_EDITABLE,
    "antes": "return list(solicitudes)",
    "despues": '[p for p in solicitudes if p.estado != "CANCELADA"]',
}


def test_consola_acepta_s_y_muestra_el_cambio(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "s")

    assert aprobar_edicion_en_consola(EDICION)

    salida = capsys.readouterr().out
    assert MODULO_EDITABLE in salida
    assert EDICION["antes"] in salida
    assert EDICION["despues"] in salida


def test_consola_acepta_n(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert not aprobar_edicion_en_consola(EDICION)


def test_consola_rechaza_entrada_no_valida_y_vuelve_a_preguntar(monkeypatch, capsys):
    respuestas = iter(("sí", "s"))
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    assert aprobar_edicion_en_consola(EDICION)
    assert "Respuesta inválida" in capsys.readouterr().out


def test_consola_deniega_si_no_hay_entrada(monkeypatch):
    def sin_entrada(_):
        raise EOFError

    monkeypatch.setattr("builtins.input", sin_entrada)
    assert not aprobar_edicion_en_consola(EDICION)


def test_politica_solicita_aprobacion_en_cada_edicion():
    recibidas = []
    politica = Politica(aprobar_edicion=lambda args: recibidas.append(args.copy()) or True)

    primera = politica.evaluar("editar_archivo", EDICION, 1)
    segunda = politica.evaluar("editar_archivo", EDICION, 2)

    assert primera.permitido and segunda.permitido
    assert primera.motivo == "Aprobación humana concedida en consola"
    assert recibidas == [EDICION, EDICION]


def test_politica_predeterminada_pide_aprobacion_en_consola(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "s")

    decision = Politica().evaluar("editar_archivo", EDICION, 1)

    assert decision.permitido
    assert decision.motivo == "Aprobación humana concedida en consola"


def test_politica_bloquea_si_se_deniega_la_edicion():
    politica = Politica(aprobar_edicion=lambda _: False)

    decision = politica.evaluar("editar_archivo", EDICION, 1)

    assert not decision.permitido
    assert "denegó" in decision.motivo


def ejecutar_edicion(tmp_path, aprobar):
    ruta = tmp_path / MODULO_EDITABLE
    ruta.parent.mkdir(parents=True)
    ruta.write_text("estado = 'antes'\n", encoding="utf-8")
    grabacion = tmp_path / "decisiones.json"
    grabacion.write_text(json.dumps([
        {"pensamiento": "Solicitaré la edición", "accion": "editar_archivo", "args": {
            "ruta": MODULO_EDITABLE, "antes": "antes", "despues": "después"}},
        {"pensamiento": "Terminaré", "final": "Fin"},
    ]), encoding="utf-8")
    agente = Agente("ejecutor", ModeloGrabado(grabacion), Herramientas(tmp_path),
                    Politica(aprobar_edicion=aprobar), "Prueba de aprobación", tmp_path / "traza.jsonl")
    agente.ejecutar()
    eventos = [json.loads(linea) for linea in (tmp_path / "traza.jsonl").read_text(encoding="utf-8").splitlines()]
    return ruta, eventos


def test_edicion_denegada_no_modifica_archivo(tmp_path):
    ruta, eventos = ejecutar_edicion(tmp_path, lambda _: False)

    assert ruta.read_text(encoding="utf-8") == "estado = 'antes'\n"
    assert eventos[1]["estado"] == "BLOQUEADO"
    assert "no concedió" in eventos[1]["observacion"]


def test_edicion_aprobada_se_ejecuta_y_queda_en_traza(tmp_path):
    ruta, eventos = ejecutar_edicion(tmp_path, lambda _: True)

    assert ruta.read_text(encoding="utf-8") == "estado = 'después'\n"
    assert eventos[1]["estado"] == "OBSERVANDO"
    assert eventos[1]["aprobacion"] == "Aprobación humana concedida en consola"
