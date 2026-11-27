"""Contrato observable de idempotencia del saldo, sin servicios reales."""
from decimal import Decimal

from src.lab10.operaciones import LibroPuntos


def test_issue_01_reintentar_acreditacion_no_duplica_saldo():
    libro = LibroPuntos({"PLASTICO": Decimal("10")})
    primero = libro.acreditar("SOL-01", "PLASTICO", Decimal("2"))
    repetido = libro.acreditar("SOL-01", "PLASTICO", Decimal("2"))

    assert primero == repetido
    assert libro.saldo == 20
    assert len(libro.movimientos) == 1

    libro.acreditar("SOL-02", "PLASTICO", Decimal("3"))
    assert libro.saldo == 50
    assert len(libro.movimientos) == 2
