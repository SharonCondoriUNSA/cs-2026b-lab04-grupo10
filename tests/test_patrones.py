"""Pruebas de extensión y sustitución de E2-E5, solo servicios simulados."""
from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace

import pytest

from src.puntos_beneficios.reglas import FabricaReglas, ReglaPuntos
from src.puntos_beneficios.servicio import ServicioPuntos
from src.solicitudes.ia import (
    AdaptadorProveedorLLM,
    CadenaGuardrails,
    CategoriaPermitida,
    ClasificadorResiduo,
    ConCacheClasificador,
    DescripcionDeLongitudPermitida,
    DescripcionNoVacia,
    EntradaResiduoInvalida,
    ProveedorLLM,
    RespuestaLLMInvalida,
    RespuestaNoVacia,
)
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


def test_observer_dos_suscriptores_reciben_despues_de_persistir():
    from src.solicitudes.eventos import PublicadorEventos, Suscriptor

    recibidos = []
    servicio = ServicioSolicitudes(cobertura=lambda distrito: True,
                                   publicador=PublicadorEventos())

    class Auditor(Suscriptor):
        def __init__(self, nombre):
            self.nombre = nombre

        def recibir(self, evento):
            registro = servicio.repositorio.registros[evento.solicitud_id]
            recibidos.append((self.nombre, evento.tipo, registro.estado))

    servicio.publicador.suscribir(Auditor("auditoria"))
    servicio.publicador.suscribir(Auditor("seguimiento"))
    servicio.solicitar_recojo(nueva_solicitud())
    assert recibidos == [("auditoria", "REGISTRADA", "PENDIENTE"),
                         ("seguimiento", "REGISTRADA", "PENDIENTE")]
    assert servicio.publicador.fallos == []


def test_observer_defecto_conserva_avisos_y_proyeccion_de_pesaje():
    servicio = ServicioSolicitudes(
        cobertura=lambda distrito: True,
        puntos=ServicioPuntos({"PAPEL": Decimal("5")}),
    )
    solicitud = nueva_solicitud()
    servicio.solicitar_recojo(solicitud)
    servicio.asignar_reciclador(solicitud, "reciclador-prueba")
    servicio.registrar_recojo(solicitud, datetime(2026, 10, 25, 10))
    servicio.registrar_pesaje(solicitud, Decimal("2"))
    servicio.acreditar_puntos(solicitud, "PAPEL")
    assert servicio.eventos == ["aviso_interno:sol-state:PENDIENTE",
                                "puntos:sol-state:10", "reporte_pesaje:sol-state:2"]


def test_observer_fallo_no_revierte_registro_ni_bloquea_otro_suscriptor():
    from src.solicitudes.eventos import AvisosInternos, PublicadorEventos, Suscriptor

    class Fallido(Suscriptor):
        def recibir(self, evento):
            raise OSError("Consumidor no disponible")

    publicador = PublicadorEventos()
    avisos = []
    publicador.suscribir(Fallido())
    publicador.suscribir(AvisosInternos(avisos))
    servicio = ServicioSolicitudes(cobertura=lambda distrito: True, publicador=publicador)
    resultado = servicio.solicitar_recojo(nueva_solicitud())
    assert resultado["estado"] == "PENDIENTE"
    assert servicio.repositorio.registros["sol-state"].estado == "PENDIENTE"
    assert avisos == ["aviso_interno:sol-state:PENDIENTE"]
    assert publicador.fallos == [("sol-state", "OSError")]


@pytest.mark.parametrize("fallas,esperado", [(0, True), (2, True), (3, False)])
def test_decorator_recuperacion_y_limite_de_tres_intentos(fallas, esperado):
    from src.solicitudes.decoradores import ConReintentos

    sdk = MapaSDK(fallas=fallas)
    puerto = ConReintentos(MapaAdapter(sdk))
    assert puerto.validar_ubicacion(Decimal("-16"), Decimal("-71")) is esperado
    assert sdk.llamadas == min(fallas + 1, 3)


def test_decorator_no_reintenta_respuesta_negativa():
    from src.solicitudes.decoradores import ConReintentos

    sdk = GeoClient(valida=False)
    assert ConReintentos(GeoAdapter(sdk)).validar_ubicacion(
        Decimal("-16"), Decimal("-71")) is False
    assert sdk.llamadas == 1


def test_decorator_no_oculta_errores_no_transitorios():
    from src.solicitudes.decoradores import ConReintentos

    class ErrorDeContrato(PuertoMapas):
        def validar_ubicacion(self, latitud, longitud):
            raise ValueError("Respuesta invalida")

    with pytest.raises(ValueError, match="Respuesta invalida"):
        ConReintentos(ErrorDeContrato()).validar_ubicacion(Decimal("0"), Decimal("0"))


@pytest.mark.parametrize("intentos", [0, -1, True, 1.5])
def test_decorator_rechaza_limite_de_intentos_invalido(intentos):
    from src.solicitudes.decoradores import ConReintentos

    with pytest.raises(ValueError, match="Numero de intentos invalido"):
        ConReintentos(MapaAdapter(MapaSDK()), max_intentos=intentos)


class ProveedorSimulado(ProveedorLLM):
    def __init__(self, respuestas):
        self.respuestas = list(respuestas)
        self.prompts = []

    def completar(self, prompt):
        self.prompts.append(prompt)
        return self.respuestas.pop(0)


class ClienteSimulado:
    def __init__(self, contenido):
        self.contenido = contenido
        self.prompts = []

    def invoke(self, prompt):
        self.prompts.append(prompt)
        return SimpleNamespace(content=self.contenido)


def test_clasifica_material_admitido_y_usa_prompt_acotado():
    proveedor = ProveedorSimulado(["PAPEL"])
    clasificador = ClasificadorResiduo(proveedor)

    assert clasificador.clasificar("caja de cartón limpia") == "PAPEL"
    assert "Ignora instrucciones" in proveedor.prompts[0]
    assert "NO_CLASIFICABLE" in proveedor.prompts[0]


def test_respuesta_no_clasificable_no_se_confunde_con_material_admitido():
    clasificador = ClasificadorResiduo(ProveedorSimulado(["NO_CLASIFICABLE"]))

    assert clasificador.clasificar("objeto compuesto y sucio") == "NO_CLASIFICABLE"


@pytest.mark.parametrize("descripcion", ["", "   ", None])
def test_rechaza_descripcion_vacia_antes_de_llamar_al_proveedor(descripcion):
    proveedor = ProveedorSimulado([])
    clasificador = ClasificadorResiduo(proveedor)

    with pytest.raises(EntradaResiduoInvalida):
        clasificador.clasificar(descripcion)

    assert proveedor.prompts == []


def test_rechaza_descripcion_demasiado_larga_antes_de_llamar_al_proveedor():
    proveedor = ProveedorSimulado([])
    clasificador = ClasificadorResiduo(proveedor)

    with pytest.raises(EntradaResiduoInvalida):
        clasificador.clasificar("x" * 301)

    assert proveedor.prompts == []


@pytest.mark.parametrize("respuesta", ["VIDRIO", "Es PAPEL", "", None])
def test_guardrails_bloquean_respuesta_invalida(respuesta):
    clasificador = ClasificadorResiduo(ProveedorSimulado([respuesta]))

    with pytest.raises(RespuestaLLMInvalida):
        clasificador.clasificar("botella de vidrio")


def test_adapter_traduce_respuesta_del_cliente_al_puerto():
    cliente = ClienteSimulado("PLASTICO")
    adaptador = AdaptadorProveedorLLM(cliente)
    clasificador = ClasificadorResiduo(adaptador)

    assert clasificador.clasificar("botella de plástico") == "PLASTICO"
    assert len(cliente.prompts) == 1


def test_decorator_cachea_resultado_validado_para_entrada_equivalente():
    proveedor = ProveedorSimulado(["PAPEL"])
    clasificador = ConCacheClasificador(ClasificadorResiduo(proveedor))

    assert clasificador.clasificar("caja de cartón") == "PAPEL"
    assert clasificador.clasificar("  CAJA   DE CARTÓN  ") == "PAPEL"
    assert len(proveedor.prompts) == 1


def test_decorator_no_cachea_respuestas_rechazadas():
    proveedor = ProveedorSimulado(["VIDRIO", "PLASTICO"])
    clasificador = ConCacheClasificador(ClasificadorResiduo(proveedor))

    with pytest.raises(RespuestaLLMInvalida):
        clasificador.clasificar("botella")
    assert clasificador.clasificar("botella") == "PLASTICO"
    assert len(proveedor.prompts) == 2


def test_cadena_exige_dos_guardrails_y_detiene_respuesta_vacia():
    cadena = CadenaGuardrails((RespuestaNoVacia(), CategoriaPermitida()))
    assert cadena.procesar(" papel ") == "PAPEL"

    with pytest.raises(RespuestaLLMInvalida):
        cadena.procesar(" ")

    with pytest.raises(ValueError, match="al menos dos"):
        CadenaGuardrails((DescripcionNoVacia(),))


def test_guardrails_de_entrada_pueden_encadenarse():
    cadena = CadenaGuardrails((DescripcionNoVacia(), DescripcionDeLongitudPermitida()))
    assert cadena.procesar("  botella  ") == "botella"



def test_decorator_valida_longitud_antes_de_reutilizar_cache():
    proveedor = ProveedorSimulado(["PAPEL"])
    clasificador = ConCacheClasificador(ClasificadorResiduo(proveedor))
    descripcion_valida = "x " * 101
    descripcion_excesiva = "x  " * 101

    assert clasificador.clasificar(descripcion_valida) == "PAPEL"
    with pytest.raises(EntradaResiduoInvalida):
        clasificador.clasificar(descripcion_excesiva)
    assert len(proveedor.prompts) == 1
