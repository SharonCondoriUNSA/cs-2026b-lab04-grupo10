"""Línea base Lab07, decisiones concentradas antes de aplicar patrones.

No sustituye dominio.py del Lab05. Los eventos son un buzón en memoria para
despacho posterior, no entregas reales ni una cola durable.
"""
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from src.solicitudes.externos import GeoClient, MapaSDK


@dataclass
class Detalle:
    material: str
    peso_estimado_kg: Decimal


@dataclass
class Solicitud:
    id: str
    distrito: str
    latitud: Decimal
    longitud: Decimal
    detalles: list[Detalle] = field(default_factory=list)
    estado: str | None = None
    ubicacion_validada: bool = False
    reciclador_id: str | None = None
    fecha_recojo: datetime | None = None
    peso_real_kg: Decimal | None = None
    acreditacion_id: str | None = None
    puntos: int = 0
    cerrada: bool = False


class RepositorioMemoria:
    def __init__(self):
        self.registros = {}

    def guardar(self, solicitud):
        self.registros[solicitud.id] = deepcopy(solicitud)


class ServicioSolicitudes:
    def __init__(self, repositorio=None, cobertura=None, mapa=None, geo=None,
                 puntos=None):
        self.repositorio = repositorio if repositorio is not None else RepositorioMemoria()
        self.cobertura = cobertura if cobertura is not None else lambda distrito: False
        self.mapa = mapa if mapa is not None else MapaSDK()
        self.geo = geo if geo is not None else GeoClient()
        self.puntos = puntos
        self.eventos = []

    def solicitar_recojo(self, solicitud, proveedor="MAPA"):
        if solicitud.estado is not None or solicitud.cerrada:
            raise ValueError("Solicitud ya registrada")
        if not isinstance(solicitud.id, str) or not solicitud.id.strip():
            raise ValueError("Identificador invalido")
        if solicitud.id in self.repositorio.registros:
            raise ValueError("Solicitud ya registrada")
        if not solicitud.detalles:
            raise ValueError("Detalles vacios")
        for detalle in solicitud.detalles:
            if (detalle.material not in {"PLASTICO", "PAPEL"}
                    or not isinstance(detalle.peso_estimado_kg, Decimal)
                    or not detalle.peso_estimado_kg.is_finite()
                    or detalle.peso_estimado_kg <= 0):
                raise ValueError("Detalle invalido")
        for valor, limite in [(solicitud.latitud, 90), (solicitud.longitud, 180)]:
            if not isinstance(valor, Decimal) or not valor.is_finite() or abs(valor) > limite:
                raise ValueError("Coordenadas invalidas")
        if not self.cobertura(solicitud.distrito):
            raise ValueError("Distrito sin cobertura")
        validada = False
        if proveedor == "MAPA":
            for intento in range(3):
                try:
                    validada = self.mapa.verificar(solicitud.latitud, solicitud.longitud)["ubicacion_valida"]
                    break
                except (TimeoutError, ConnectionError):
                    if intento == 2:
                        validada = False
        elif proveedor == "GEO":
            for intento in range(3):
                try:
                    codigo, _ = self.geo.check((solicitud.latitud, solicitud.longitud))
                    validada = codigo == 200
                    break
                except (TimeoutError, ConnectionError):
                    if intento == 2:
                        validada = False
        else:
            raise ValueError("Proveedor no soportado")
        # Se publica éxito únicamente tras confirmar persistencia.
        pendiente = deepcopy(solicitud)
        pendiente.estado = "PENDIENTE"
        pendiente.ubicacion_validada = validada
        self.repositorio.guardar(pendiente)
        solicitud.estado = pendiente.estado
        solicitud.ubicacion_validada = validada
        solicitud.detalles = deepcopy(pendiente.detalles)
        self.eventos.append(f"aviso_interno:{solicitud.id}:PENDIENTE")
        return {"id": solicitud.id, "estado": solicitud.estado,
                "ubicacion_validada": validada, "revision_ubicacion": not validada}

    def asignar_reciclador(self, solicitud, reciclador_id):
        if solicitud.estado != "PENDIENTE" or solicitud.cerrada:
            raise ValueError("Transicion invalida")
        if not isinstance(reciclador_id, str) or not reciclador_id.strip():
            raise ValueError("Reciclador invalido")
        solicitud.reciclador_id = reciclador_id
        solicitud.estado = "ASIGNADA"

    def registrar_recojo(self, solicitud, fecha_recojo):
        if solicitud.estado != "ASIGNADA" or solicitud.cerrada:
            raise ValueError("Transicion invalida")
        if not isinstance(fecha_recojo, datetime):
            raise ValueError("Fecha invalida")
        solicitud.fecha_recojo = fecha_recojo
        solicitud.estado = "RECOGIDA"

    def registrar_pesaje(self, solicitud, peso_real_kg):
        if solicitud.estado != "RECOGIDA" or solicitud.cerrada:
            raise ValueError("Transicion invalida")
        if (not isinstance(peso_real_kg, Decimal)
                or not peso_real_kg.is_finite() or peso_real_kg <= 0):
            raise ValueError("Peso real invalido")
        solicitud.peso_real_kg = peso_real_kg
        solicitud.estado = "PESADA"

    def acreditar_puntos(self, solicitud, material):
        if solicitud.estado != "PESADA" or solicitud.cerrada:
            raise ValueError("Transicion invalida")
        if self.puntos is None:
            raise ValueError("Servicio de puntos no configurado")
        resultado = self.puntos.acreditar(solicitud.id, material, solicitud.peso_real_kg)
        self.confirmar_puntos_acreditados(solicitud, resultado["acreditacion_id"])
        solicitud.puntos = resultado["puntos"]
        self.eventos.append(f"puntos:{solicitud.id}:{solicitud.puntos}")
        self.eventos.append(f"reporte_pesaje:{solicitud.id}:{solicitud.peso_real_kg}")
        return solicitud.puntos

    def confirmar_puntos_acreditados(self, solicitud, acreditacion_id):
        if solicitud.estado != "PESADA" or solicitud.cerrada:
            raise ValueError("Transicion invalida")
        if not isinstance(acreditacion_id, str) or not acreditacion_id.strip():
            raise ValueError("Acreditacion invalida")
        solicitud.acreditacion_id = acreditacion_id
        solicitud.estado = "PUNTOS_ACREDITADOS"

    def cerrar(self, solicitud):
        if solicitud.estado != "PUNTOS_ACREDITADOS" or solicitud.cerrada:
            raise ValueError("Transicion invalida")
        solicitud.cerrada = True
