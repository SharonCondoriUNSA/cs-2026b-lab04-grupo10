"""Contrato de exclusión de canceladas, sin consultas ni rutas externas."""
from src.lab10.operaciones import Parada, preparar_ruta


def test_issue_02_ruta_excluye_canceladas_y_conserva_orden():
    pendientes = [Parada("SOL-01", "ASIGNADA"), Parada("SOL-02", "CANCELADA"),
                  Parada("SOL-03", "ASIGNADA")]
    original = list(pendientes)

    ruta = preparar_ruta(pendientes)

    assert [parada.solicitud_id for parada in ruta] == ["SOL-01", "SOL-03"]
    assert pendientes == original
    assert preparar_ruta([Parada("SOL-04", "CANCELADA")]) == []
    assert preparar_ruta([]) == []
