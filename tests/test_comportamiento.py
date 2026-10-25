"""El mismo contrato observable se ejecuta sobre antes y versión refactorizada."""
import importlib
from datetime import datetime
from decimal import Decimal

import pytest

from src.solicitudes.externos import GeoClient, MapaSDK


@pytest.fixture(params=["src.solicitudes.antes.servicio", "src.solicitudes.servicio"])
def m(request):
    return importlib.import_module(request.param)


def solicitud(m):
    return m.Solicitud("sol-1", "DISTRITO_PRUEBA", Decimal("-16.4"),
                       Decimal("-71.5"), [m.Detalle("PLASTICO", Decimal("2"))])


def servicio(m, **kwargs):
    versiones_puntos = {
        "src.solicitudes.antes.servicio": "src.puntos_beneficios.antes.servicio",
        "src.solicitudes.servicio": "src.puntos_beneficios.servicio",
    }
    ServicioPuntos = importlib.import_module(versiones_puntos[m.__name__]).ServicioPuntos
    kwargs.setdefault("cobertura", lambda distrito: distrito == "DISTRITO_PRUEBA")
    kwargs.setdefault("puntos", ServicioPuntos({"PLASTICO": Decimal("10"),
                                              "PAPEL": Decimal("5")}))
    return m.ServicioSolicitudes(**kwargs)


@pytest.mark.parametrize("proveedor", ["MAPA", "GEO"])
def test_registro_exitoso_guarda_y_encola_aviso(m, proveedor):
    s, p = servicio(m), solicitud(m)
    assert s.solicitar_recojo(p, proveedor) == {
        "id": "sol-1", "estado": "PENDIENTE", "ubicacion_validada": True,
        "revision_ubicacion": False,
    }
    assert s.repositorio.registros[p.id].estado == "PENDIENTE"
    assert s.eventos == ["aviso_interno:sol-1:PENDIENTE"]


def test_sin_detalles_no_persiste_ni_emite_eventos(m):
    s, p = servicio(m), solicitud(m)
    p.detalles = []
    with pytest.raises(ValueError, match="Detalles vacios"):
        s.solicitar_recojo(p)
    assert p.estado is None and s.repositorio.registros == {} and s.eventos == []


@pytest.mark.parametrize("peso", [Decimal("0"), Decimal("-1"), Decimal("NaN"),
                                  Decimal("Infinity")])
def test_peso_estimado_invalido_no_persiste(m, peso):
    s, p = servicio(m), solicitud(m)
    p.detalles[0].peso_estimado_kg = peso
    with pytest.raises(ValueError, match="Detalle invalido"):
        s.solicitar_recojo(p)
    assert s.repositorio.registros == {} and s.eventos == []


def test_material_no_aceptado(m):
    s, p = servicio(m), solicitud(m)
    p.detalles[0].material = "PELIGROSO"
    with pytest.raises(ValueError, match="Detalle invalido"):
        s.solicitar_recojo(p)
    assert p.estado is None and s.repositorio.registros == {}


@pytest.mark.parametrize("latitud,longitud", [("90", "180"), ("-90", "-180")])
def test_limites_geograficos_son_validos(m, latitud, longitud):
    s, p = servicio(m), solicitud(m)
    p.latitud, p.longitud = Decimal(latitud), Decimal(longitud)
    assert s.solicitar_recojo(p)["estado"] == "PENDIENTE"


@pytest.mark.parametrize("latitud,longitud", [("90.01", "0"), ("0", "-180.01"),
                                             ("NaN", "0")])
def test_coordenadas_invalidas_no_persisten(m, latitud, longitud):
    s, p = servicio(m), solicitud(m)
    p.latitud, p.longitud = Decimal(latitud), Decimal(longitud)
    with pytest.raises(ValueError, match="Coordenadas invalidas"):
        s.solicitar_recojo(p)
    assert s.repositorio.registros == {} and s.eventos == []


def test_distrito_sin_cobertura_no_persiste(m):
    s, p = servicio(m), solicitud(m)
    p.distrito = "SIN_COBERTURA"
    with pytest.raises(ValueError, match="Distrito sin cobertura"):
        s.solicitar_recojo(p)
    assert p.estado is None and s.repositorio.registros == {} and s.eventos == []


@pytest.mark.parametrize("proveedor", ["MAPA", "GEO"])
def test_dos_fallas_transitorias_permiten_verificar(m, proveedor):
    # El resultado distingue recuperación de abandono inmediato o prematuro.
    s = servicio(m, mapa=MapaSDK(fallas=2), geo=GeoClient(fallas=2))
    assert s.solicitar_recojo(solicitud(m), proveedor)["ubicacion_validada"] is True


@pytest.mark.parametrize("proveedor", ["MAPA", "GEO"])
def test_tres_fallas_conservan_registro_pendiente(m, proveedor):
    s = servicio(m, mapa=MapaSDK(fallas=3), geo=GeoClient(fallas=3))
    p = solicitud(m)
    resultado = s.solicitar_recojo(p, proveedor)
    assert resultado["estado"] == "PENDIENTE" and resultado["revision_ubicacion"]
    assert not s.repositorio.registros[p.id].ubicacion_validada
    assert s.eventos == ["aviso_interno:sol-1:PENDIENTE"]


@pytest.mark.parametrize("proveedor", ["MAPA", "GEO"])
def test_mapa_rechaza_sin_perder_solicitud(m, proveedor):
    s = servicio(m, mapa=MapaSDK(valida=False), geo=GeoClient(valida=False))
    assert s.solicitar_recojo(solicitud(m), proveedor)["revision_ubicacion"] is True


def test_proveedor_desconocido_no_persiste(m):
    s, p = servicio(m), solicitud(m)
    with pytest.raises(ValueError, match="Proveedor no soportado"):
        s.solicitar_recojo(p, "OTRO")
    assert p.estado is None and s.repositorio.registros == {} and s.eventos == []


def test_fallo_de_persistencia_no_confirma_ni_avisa(m):
    class RepositorioCaido(m.RepositorioMemoria):
        def guardar(self, solicitud):
            raise OSError("Persistencia no disponible")
    s, p = servicio(m, repositorio=RepositorioCaido()), solicitud(m)
    with pytest.raises(OSError, match="Persistencia no disponible"):
        s.solicitar_recojo(p)
    assert p.estado is None and s.eventos == []


def test_no_registra_dos_veces(m):
    s, p = servicio(m), solicitud(m)
    s.solicitar_recojo(p)
    with pytest.raises(ValueError, match="Solicitud ya registrada"):
        s.solicitar_recojo(p)
    assert len(s.eventos) == 1 and len(s.repositorio.registros) == 1


def test_registro_conserva_copia_de_detalles(m):
    s, p = servicio(m), solicitud(m)
    s.solicitar_recojo(p)
    p.detalles[0].peso_estimado_kg = Decimal("100")
    assert s.repositorio.registros[p.id].detalles[0].peso_estimado_kg == Decimal("2")


@pytest.mark.parametrize("material,esperado", [("PLASTICO", 22), ("PAPEL", 11)])
def test_ciclo_completo_acredita_con_peso_real_y_cierra(m, material, esperado):
    s, p = servicio(m), solicitud(m)
    s.solicitar_recojo(p)
    s.asignar_reciclador(p, "reciclador-prueba")
    s.registrar_recojo(p, datetime(2026, 10, 25, 10))
    s.registrar_pesaje(p, Decimal("2.25"))
    assert s.acreditar_puntos(p, material) == esperado
    assert p.estado == "PUNTOS_ACREDITADOS" and p.acreditacion_id
    assert s.eventos[-2:] == [f"puntos:sol-1:{esperado}", "reporte_pesaje:sol-1:2.25"]
    s.cerrar(p)
    assert p.cerrada is True
    with pytest.raises(ValueError, match="Transicion invalida"):
        s.acreditar_puntos(p, material)


def test_pesaje_fuera_de_orden_no_cambia_estado(m):
    s, p = servicio(m), solicitud(m)
    s.solicitar_recojo(p)
    with pytest.raises(ValueError, match="Transicion invalida"):
        s.registrar_pesaje(p, Decimal("1"))
    assert p.estado == "PENDIENTE" and p.peso_real_kg is None


def test_peso_real_cero_no_avanza(m):
    s, p = servicio(m), solicitud(m)
    s.solicitar_recojo(p)
    s.asignar_reciclador(p, "reciclador-prueba")
    s.registrar_recojo(p, datetime(2026, 10, 25, 10))
    with pytest.raises(ValueError, match="Peso real invalido"):
        s.registrar_pesaje(p, Decimal("0"))
    assert p.estado == "RECOGIDA" and p.peso_real_kg is None


@pytest.mark.parametrize("material", ["VIDRIO", "DESCONOCIDO"])
def test_regla_desconocida_no_acredita(m, material):
    s, p = servicio(m), solicitud(m)
    p.estado, p.peso_real_kg = "PESADA", Decimal("2")
    with pytest.raises(ValueError, match="Material sin regla de puntos"):
        s.acreditar_puntos(p, material)
    assert p.estado == "PESADA" and p.acreditacion_id is None and s.eventos == []


@pytest.mark.parametrize("tarifa", [None, Decimal("-1"), Decimal("NaN"),
                                    Decimal("Infinity")])
def test_tarifa_invalida_no_acredita(m, tarifa):
    s, p = servicio(m), solicitud(m)
    s.puntos.tarifas["PLASTICO"] = tarifa
    p.estado, p.peso_real_kg = "PESADA", Decimal("2")
    with pytest.raises(ValueError, match="Tarifa de puntos invalida"):
        s.acreditar_puntos(p, "PLASTICO")
    assert p.estado == "PESADA" and p.acreditacion_id is None and s.eventos == []


def test_tarifa_cero_es_valida(m):
    s, p = servicio(m), solicitud(m)
    s.puntos.tarifas["PAPEL"] = Decimal("0")
    p.estado, p.peso_real_kg = "PESADA", Decimal("2")
    assert s.acreditar_puntos(p, "PAPEL") == 0
    assert p.estado == "PUNTOS_ACREDITADOS"
