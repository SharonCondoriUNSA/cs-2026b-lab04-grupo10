"""Contrato observable de aislamiento de tarifas, con distritos sintéticos."""
from decimal import Decimal

from src.lab10.operaciones import TarifasDistritales


def test_issue_03_actualizar_d01_no_cambia_los_puntos_de_d02():
    tarifas_entrada = {"PLASTICO": Decimal("10"), "PAPEL": Decimal("5")}
    catalogo = TarifasDistritales(["D01", "D02"], tarifas_entrada)
    assert catalogo.calcular("D02", "PLASTICO", Decimal("2")) == 20

    catalogo.actualizar("D01", "PLASTICO", Decimal("15"))

    assert catalogo.calcular("D01", "PLASTICO", Decimal("2")) == 30
    assert catalogo.calcular("D02", "PLASTICO", Decimal("2")) == 20
    assert catalogo.calcular("D01", "PAPEL", Decimal("2")) == 10
    assert tarifas_entrada["PLASTICO"] == Decimal("10")
