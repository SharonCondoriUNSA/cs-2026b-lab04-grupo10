"""Pruebas de extensión y sustitución de E2, solo servicios simulados."""
from decimal import Decimal

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
