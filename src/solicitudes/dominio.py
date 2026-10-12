"""
Módulo de Dominio: Solicitudes de Recojo
Generado mediante ingeniería directa a partir de docs/design/clases.puml (E1-E3).
Caso 10: EcoRecicla AQP
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4


class EstadoSolicitud(Enum):
    PENDIENTE = "PENDIENTE"
    ASIGNADA = "ASIGNADA"
    RECOGIDA = "RECOGIDA"
    PESADA = "PESADA"
    PUNTOS_ACREDITADOS = "PUNTOS_ACREDITADOS"


@dataclass
class Vecino:
    id: UUID = field(default_factory=uuid4)

    def obtener_id(self) -> UUID:
        return self.id


@dataclass
class PuntoRecojo:
    codigo_distrito: str
    latitud: float
    longitud: float

    def coordenadas_validas(self) -> bool:
        return -90.0 <= self.latitud <= 90.0 and -180.0 <= self.longitud <= 180.0


@dataclass
class MaterialReciclable:
    id: UUID
    nombre: str
    aceptado: bool

    def es_aceptado(self) -> bool:
        return self.aceptado


@dataclass
class DetalleReciclable:
    material: MaterialReciclable
    peso_estimado_kg: float

    def validar(self) -> bool:
        return self.peso_estimado_kg > 0 and self.material.es_aceptado()


@dataclass
class SolicitudRecojo:
    vecino: Vecino
    punto: PuntoRecojo
    detalles: List[DetalleReciclable]
    id: UUID = field(default_factory=uuid4)
    fecha_registro: datetime = field(default_factory=datetime.now)
    estado: EstadoSolicitud = EstadoSolicitud.PENDIENTE
    ubicacion_validada_por_mapa: bool = False
    reciclador_id: Optional[UUID] = None
    fecha_recojo: Optional[datetime] = None
    peso_real_kg: Optional[float] = None
    acreditacion_id: Optional[UUID] = None

    def validar_datos(self) -> bool:
        if not self.detalles or len(self.detalles) == 0:
            return False
        return all(d.validar() for d in self.detalles) and self.punto.coordenadas_validas()

    def calcular_peso_estimado_kg(self) -> float:
        return sum(d.peso_estimado_kg for d in self.detalles)

    def registrar_pendiente(self) -> None:
        self.estado = EstadoSolicitud.PENDIENTE

    def marcar_ubicacion_validada(self) -> None:
        self.ubicacion_validada_por_mapa = True

    def asignar_reciclador(self, reciclador_id: UUID) -> None:
        self.reciclador_id = reciclador_id
        self.estado = EstadoSolicitud.ASIGNADA

    def registrar_recojo(self, fecha_recojo: datetime) -> None:
        self.fecha_recojo = fecha_recojo
        self.estado = EstadoSolicitud.RECOGIDA

    def registrar_pesaje(self, peso_real_kg: float) -> None:
        self.peso_real_kg = peso_real_kg
        self.estado = EstadoSolicitud.PESADA

    def confirmar_puntos_acreditados(self, acreditacion_id: UUID) -> None:
        self.acreditacion_id = acreditacion_id
        self.estado = EstadoSolicitud.PUNTOS_ACREDITADOS


# --- Interfaces y Puertos del Módulo (Contratos Públicos / Adaptadores) ---

class RepositorioSolicitudes(ABC):
    @abstractmethod
    def guardar(self, solicitud: SolicitudRecojo) -> None:
        raise NotImplementedError()


class CoberturaRecojo(ABC):
    @abstractmethod
    def atiende_distrito(self, codigo_distrito: str) -> bool:
        raise NotImplementedError()


class ServicioMapas(ABC):
    @abstractmethod
    def validar_ubicacion(self, latitud: float, longitud: float) -> bool:
        raise NotImplementedError()


class NotificadorSolicitud(ABC):
    @abstractmethod
    def confirmar_registro(self, solicitud_id: UUID) -> None:
        raise NotImplementedError()


class ServicioSolicitudes:
    def __init__(
        self,
        repositorio: RepositorioSolicitudes,
        cobertura: CoberturaRecojo,
        notificador: NotificadorSolicitud,
        mapas: Optional[ServicioMapas] = None
    ):
        self.repositorio = repositorio
        self.cobertura = cobertura
        self.notificador = notificador
        self.mapas = mapas

    def solicitar_recojo(
        self, vecino: Vecino, punto: PuntoRecojo, detalles: List[DetalleReciclable]
    ) -> SolicitudRecojo:
        if not self.cobertura.atiende_distrito(punto.codigo_distrito):
            raise ValueError("Distrito sin cobertura")
        
        solicitud = SolicitudRecojo(vecino=vecino, punto=punto, detalles=detalles)
        if not solicitud.validar_datos():
            raise ValueError("Datos de solicitud inválidos")

        if self.mapas and self.mapas.validar_ubicacion(punto.latitud, punto.longitud):
            solicitud.marcar_ubicacion_validada()

        self.repositorio.guardar(solicitud)
        self.notificador.confirmar_registro(solicitud.id)
        return solicitud