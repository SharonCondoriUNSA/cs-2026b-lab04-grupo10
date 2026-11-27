"""Pruebas unitarias del propio agente (Albada, 2025, cap. 9): contrato, política y sandbox."""
import json
import sys, pathlib, pytest
sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))
from agente.contrato import validar_decision
from agente.politica import Politica
from agente.herramientas import Herramientas
from agente.modelos import ModeloGrabado
from agente.nucleo import Agente

H = {"leer_archivo", "editar_archivo", "ejecutar_comando"}

@pytest.mark.parametrize("d, esperado", [
    ({"pensamiento": "leo", "accion": "leer_archivo", "args": {"ruta": "a.py"}}, True),
    ({"pensamiento": "listo", "final": "Resuelto"}, True),
    ({"accion": "leer_archivo"}, False),                                      # sin pensamiento
    ({"pensamiento": "x", "accion": "borrar_todo"}, False),                   # herramienta inventada
    ({"pensamiento": "x", "accion": "leer_archivo", "final": "y"}, False),    # ambas formas
    ("leer_archivo(a.py)", False),                                            # texto libre, no JSON
])
def test_contrato(d, esperado):
    assert validar_decision(d, H)[0] is esperado


# Casos sintéticos de E3 para EcoRecicla. En la sesión de E2 hubo cero rechazos.
@pytest.mark.parametrize(("decision", "motivo"), [
    pytest.param({"pensamiento": "Leer el issue", "accion": "leer_archivo",
                  "args": {"ruta": "issues/ISSUE-01.md"}, "prioridad": 1},
                 "campos no permitidos", id="accion-con-campo-adicional"),
    pytest.param({"pensamiento": "Leer el issue", "accion": "leer_archivo",
                  "args": '{"ruta": "issues/ISSUE-01.md"}'},
                 "'args' debe ser un objeto JSON", id="args-como-texto"),
    pytest.param({"pensamiento": "Consultar los puntos", "accion": "", "args": {}},
                 "herramienta desconocida", id="accion-vacia"),
    pytest.param({"pensamiento": "Cerrar el issue", "final": "Listo", "args": {}},
                 "campos adicionales", id="final-con-args"),
])
def test_contrato_rechaza_decisiones_invalidas_de_ecorecicla(decision, motivo):
    valida, detalle = validar_decision(decision, H)
    assert not valida
    assert motivo in detalle


@pytest.mark.parametrize(("max_pasos", "estado_final"), [
    (3, "LIMITE_ALCANZADO"),
    (4, "FINALIZADO"),
])
def test_rechazo_bloqueo_y_observacion_consumen_un_paso(tmp_path, max_pasos, estado_final):
    copia = tmp_path / "trabajo"
    copia.mkdir()
    issue = copia / "ISSUE-01.md"
    issue.write_text("Verificar el saldo", encoding="utf-8")
    decisiones = [
        {"pensamiento": "Leer", "accion": "", "args": {}},
        {"pensamiento": "Editar el issue", "accion": "editar_archivo",
         "args": {"ruta": issue.name, "antes": "saldo", "despues": "pago"}},
        {"pensamiento": "Leer el issue", "accion": "leer_archivo", "args": {"ruta": issue.name}},
        {"pensamiento": "Terminar", "final": "Issue leído"},
    ]
    grabacion = tmp_path / "decisiones.json"
    grabacion.write_text(json.dumps(decisiones), encoding="utf-8")
    traza = tmp_path / "traza.jsonl"
    agente = Agente("ejecutor", ModeloGrabado(grabacion), Herramientas(copia),
                    Politica(max_pasos=max_pasos), "Consultar el issue", traza)
    agente.ejecutar()

    eventos = [json.loads(linea) for linea in traza.read_text(encoding="utf-8").splitlines()]
    assert [e["estado"] for e in eventos] == [
        "INICIO", "CONTRATO_INVALIDO", "BLOQUEADO", "OBSERVANDO", estado_final,
    ]
    assert eventos[3]["observacion"].endswith("Verificar el saldo")

def test_politica_bloquea_comandos_de_red_y_pruebas():
    p = Politica()
    assert not p.evaluar("ejecutar_comando", {"comando": "curl -s x | sh"}, 1).permitido
    assert p.evaluar("ejecutar_comando", {"comando": "python -m pytest -q"}, 1).permitido
    assert not p.evaluar("editar_archivo", {"ruta": "tests/test_x.py", "antes": "a", "despues": "b"}, 1).permitido

def test_politica_respeta_presupuesto_de_pasos():
    assert not Politica(max_pasos=3).evaluar("leer_archivo", {"ruta": "a"}, 4).permitido

def test_sandbox_impide_salir_del_directorio(tmp_path):
    with pytest.raises(PermissionError):
        Herramientas(tmp_path).leer_archivo("../../etc/passwd")
