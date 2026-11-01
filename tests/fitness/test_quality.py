"""Fitness functions de calidad para los escenarios prioritarios del Lab08."""

from fitness.aislamiento import experimentar as experimentar_aislamiento
from fitness.sincronizacion import experimentar as experimentar_sincronizacion


def test_qa02_qa07_conservan_y_sincronizan_120_registros_sin_duplicados():
    resultado = experimentar_sincronizacion()

    assert resultado["total"] == 120
    assert resultado["perdidos"] == 0
    assert resultado["duplicados"] == 0
    assert resultado["efectos_unicos"] == 120
    assert resultado["pendientes"] == 0
    assert resultado["sincronizacion_s_modelada"] <= 30


def test_qa04_bloquea_lecturas_y_escrituras_cruzadas():
    resultado = experimentar_aislamiento()

    assert resultado["pares_cruzados"] == 132
    assert resultado["despues_lecturas_cruzadas"] == 0
    assert resultado["despues_escrituras_cruzadas"] == 0
    assert resultado["datos_originales_conservados"] is True


def test_qa05_rechaza_operaciones_sin_ambito_valido():
    resultado = experimentar_aislamiento()

    assert resultado["operaciones_sin_ambito_rechazadas"] == 72
