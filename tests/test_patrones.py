"""Pruebas de extensión y sustitución de E2, solo servicios simulados."""
from decimal import Decimal
from datetime import datetime
from copy import deepcopy

import pytest

from src.puntos_beneficios.reglas import FabricaReglas, ReglaPuntos
from src.puntos_beneficios.servicio import ServicioPuntos
from src.solicitudes.externos import GeoClient, MapaSDK
from src.solicitudes.mapas import FabricaMapas, GeoAdapter, MapaAdapter, PuertoMapas
from src.solicitudes.servicio import Detalle, ServicioSolicitudes, Solicitud


def test_open_closed_agrega_regla_sin_modificar_servicio():
    class ReglaPorLote(ReglaPuntos):
        def __init__(self, tarifa):
            self.tarifa = tarifa

        def calcular(self, peso_real_kg):
            return int(peso_real_kg // Decimal("2")) * int(self.tarifa)

    fabrica = FabricaReglas()
    fabrica.registrar("VIDRIO", ReglaPorLote)
    servicio = ServicioPuntos({"VIDRIO": Decimal("7")}, fabrica=fabrica)
    assert servicio.acreditar("sol-vidrio", "VIDRIO", Decimal("5")) == {
        "acreditacion_id": "acreditacion:sol-vidrio", "puntos": 14,
    }
    # Otra instancia no hereda el registro, no hay estado global compartido.
    with pytest.raises(ValueError, match="Material sin regla de puntos"):
        ServicioPuntos({"VIDRIO": Decimal("7")}).acreditar(
            "sol-vidrio", "VIDRIO", Decimal("5"))


def test_open_closed_agrega_mapa_sin_modificar_solicitudes():
    class MapaLocal(PuertoMapas):
        def validar_ubicacion(self, latitud, longitud):
            return True

    fabrica = FabricaMapas()
    fabrica.registrar("LOCAL", MapaLocal)
    servicio = ServicioSolicitudes(cobertura=lambda distrito: True, fabrica_mapas=fabrica)
    solicitud = Solicitud("sol-local", "DISTRITO_PRUEBA", Decimal("-16"),
                          Decimal("-71"), [Detalle("PAPEL", Decimal("1"))])
    assert servicio.solicitar_recojo(solicitud, "LOCAL") == {
        "id": "sol-local", "estado": "PENDIENTE", "ubicacion_validada": True,
        "revision_ubicacion": False,
    }
    assert servicio.eventos == ["aviso_interno:sol-local:PENDIENTE"]
    with pytest.raises(ValueError, match="Proveedor no soportado"):
        FabricaMapas().crear("LOCAL")


@pytest.mark.parametrize("adapter,sdk", [(MapaAdapter, MapaSDK), (GeoAdapter, GeoClient)])
@pytest.mark.parametrize("valida", [True, False])
def test_adapters_conservan_resultado_del_proveedor(adapter, sdk, valida):
    puerto = adapter(sdk(valida=valida))
    assert puerto.validar_ubicacion(Decimal("-16"), Decimal("-71")) is valida


@pytest.mark.parametrize("adapter,sdk,error", [
    (MapaAdapter, MapaSDK, TimeoutError), (GeoAdapter, GeoClient, ConnectionError),
])
def test_adapters_propagan_fallo_transitorio_sin_reintentar(adapter, sdk, error):
    puerto = adapter(sdk(fallas=1))
    with pytest.raises(error):
        puerto.validar_ubicacion(Decimal("-16"), Decimal("-71"))
    assert puerto.validar_ubicacion(Decimal("-16"), Decimal("-71")) is True


def nueva_solicitud():
    return Solicitud("sol-state", "DISTRITO_PRUEBA", Decimal("-16"),
                     Decimal("-71"), [Detalle("PAPEL", Decimal("1"))])


def test_state_recorrido_completo_del_diagrama():
    solicitud = nueva_solicitud()
    servicio = ServicioSolicitudes(cobertura=lambda distrito: True)
    assert solicitud.estado is None
    servicio.solicitar_recojo(solicitud)
    assert solicitud.estado == "PENDIENTE"
    servicio.asignar_reciclador(solicitud, "reciclador-prueba")
    assert solicitud.estado == "ASIGNADA"
    servicio.registrar_recojo(solicitud, datetime(2026, 10, 25, 10))
    assert solicitud.estado == "RECOGIDA"
    servicio.registrar_pesaje(solicitud, Decimal("2"))
    assert solicitud.estado == "PESADA"
    servicio.confirmar_puntos_acreditados(solicitud, "acreditacion-prueba")
    assert solicitud.estado == "PUNTOS_ACREDITADOS"
    servicio.cerrar(solicitud)
    assert solicitud.cerrada and solicitud.estado == "PUNTOS_ACREDITADOS"


@pytest.mark.parametrize("estado,operacion", [
    (estado, operacion)
    for estado in [None, "PENDIENTE", "ASIGNADA", "RECOGIDA", "PESADA", "PUNTOS_ACREDITADOS"]
    for operacion, permitido in [
        ("asignar_reciclador", "PENDIENTE"), ("registrar_recojo", "ASIGNADA"),
        ("registrar_pesaje", "RECOGIDA"), ("confirmar_puntos_acreditados", "PESADA"),
        ("cerrar", "PUNTOS_ACREDITADOS"),
    ]
    if estado != permitido
])
def test_state_prohibe_transiciones_fuera_del_estado(estado, operacion):
    solicitud = nueva_solicitud()
    solicitud.estado = estado
    antes = deepcopy(solicitud)
    argumentos = {
        "asignar_reciclador": ("reciclador-prueba",),
        "registrar_recojo": (datetime(2026, 10, 25, 10),),
        "registrar_pesaje": (Decimal("2"),),
        "confirmar_puntos_acreditados": ("acreditacion-prueba",), "cerrar": (),
    }
    with pytest.raises(ValueError, match="Transicion invalida"):
        getattr(solicitud, operacion)(*argumentos[operacion])
    assert solicitud == antes


@pytest.mark.parametrize("estado,operacion,valor,mensaje", [
    ("PENDIENTE", "asignar_reciclador", " ", "Reciclador invalido"),
    ("ASIGNADA", "registrar_recojo", "hoy", "Fecha invalida"),
    ("RECOGIDA", "registrar_pesaje", Decimal("NaN"), "Peso real invalido"),
    ("PESADA", "confirmar_puntos_acreditados", "", "Acreditacion invalida"),
])
def test_state_guardas_invalidas_no_modifican_solicitud(estado, operacion, valor, mensaje):
    solicitud = nueva_solicitud()
    solicitud.estado = estado
    antes = deepcopy(solicitud)
    with pytest.raises(ValueError, match=mensaje):
        getattr(solicitud, operacion)(valor)
    assert solicitud == antes


def test_state_final_no_permite_repetir_cierre_ni_acreditar():
    solicitud = nueva_solicitud()
    solicitud.estado = "PESADA"
    solicitud.confirmar_puntos_acreditados("acreditacion-prueba")
    solicitud.cerrar()
    with pytest.raises(ValueError, match="Transicion invalida"):
        solicitud.cerrar()
    with pytest.raises(ValueError, match="Transicion invalida"):
        solicitud.confirmar_puntos_acreditados("otra-acreditacion")
    assert solicitud.acreditacion_id == "acreditacion-prueba"


def test_state_rechaza_acreditacion_antes_de_invocar_puntos():
    class PuntosNoDebenInvocarse:
        def acreditar(self, *args):
            raise AssertionError("No debe acreditar una solicitud no pesada")
    servicio = ServicioSolicitudes(puntos=PuntosNoDebenInvocarse())
    solicitud = nueva_solicitud()
    solicitud.estado = "PENDIENTE"
    with pytest.raises(ValueError, match="Transicion invalida"):
        servicio.acreditar_puntos(solicitud, "PAPEL")
    assert solicitud.estado == "PENDIENTE" and servicio.eventos == []
