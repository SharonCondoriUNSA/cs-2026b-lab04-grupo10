"""
Módulo de Dominio: Solicitudes de Recojo
Generado mediante ingeniería directa a partir de docs/design/clases.puml (E1-E3).
Caso 10: EcoRecicla AQP
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from datetime import datetime
from decimal import Decimal
from enum import Enum
import logging
from threading import Thread
from typing import List, Optional
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)


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
    latitud: Decimal
    longitud: Decimal

    def coordenadas_validas(self) -> bool:
        return (
            isinstance(self.latitud, Decimal) and self.latitud.is_finite()
            and isinstance(self.longitud, Decimal) and self.longitud.is_finite()
            and -90 <= self.latitud <= 90 and -180 <= self.longitud <= 180
        )


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
    peso_estimado_kg: Decimal

    def validar(self) -> bool:
        return (
            isinstance(self.peso_estimado_kg, Decimal)
            and self.peso_estimado_kg.is_finite()
            and self.peso_estimado_kg > 0 and self.material.es_aceptado()
        )


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
    peso_real_kg: Optional[Decimal] = None
    acreditacion_id: Optional[UUID] = None

    def validar_datos(self) -> bool:
        if not self.detalles or len(self.detalles) == 0:
            return False
        return all(d.validar() for d in self.detalles) and self.punto.coordenadas_validas()

    def calcular_peso_estimado_kg(self) -> Decimal:
        return sum((d.peso_estimado_kg for d in self.detalles), Decimal('0'))

    def registrar_pendiente(self) -> None:
        if self.estado != EstadoSolicitud.PENDIENTE or not self.validar_datos():
            raise ValueError("No se puede registrar como pendiente")
        self.estado = EstadoSolicitud.PENDIENTE

    def marcar_ubicacion_validada(self) -> None:
        self.ubicacion_validada_por_mapa = True

    def asignar_reciclador(self, reciclador_id: UUID) -> None:
        if self.estado != EstadoSolicitud.PENDIENTE or not isinstance(reciclador_id, UUID) or not reciclador_id.int:
            raise ValueError("Asignación inválida")
        self.reciclador_id = reciclador_id
        self.estado = EstadoSolicitud.ASIGNADA

    def registrar_recojo(self, fecha_recojo: datetime) -> None:
        if self.estado != EstadoSolicitud.ASIGNADA or not isinstance(fecha_recojo, datetime):
            raise ValueError("Recojo inválido")
        self.fecha_recojo = fecha_recojo
        self.estado = EstadoSolicitud.RECOGIDA

    def registrar_pesaje(self, peso_real_kg: Decimal) -> None:
        if (
            self.estado != EstadoSolicitud.RECOGIDA
            or not isinstance(peso_real_kg, Decimal)
            or not peso_real_kg.is_finite() or peso_real_kg <= 0
        ):
            raise ValueError("Pesaje inválido")
        self.peso_real_kg = peso_real_kg
        self.estado = EstadoSolicitud.PESADA

    def confirmar_puntos_acreditados(self, acreditacion_id: UUID) -> None:
        if self.estado != EstadoSolicitud.PESADA or not isinstance(acreditacion_id, UUID) or not acreditacion_id.int:
            raise ValueError("Confirmación de acreditación inválida")
        self.acreditacion_id = acreditacion_id
        self.estado = EstadoSolicitud.PUNTOS_ACREDITADOS

    def cerrar(self) -> None:
        if self.estado != EstadoSolicitud.PUNTOS_ACREDITADOS or self.acreditacion_id is None:
            raise ValueError("La solicitud no puede cerrarse sin acreditación")
        # Fin del flujo, sin borrar datos ni añadir otro estado de negocio.


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
    def validar_ubicacion(self, latitud: Decimal, longitud: Decimal) -> bool:
        raise NotImplementedError()


class NotificadorSolicitud(ABC):
    @abstractmethod
    def confirmar_registro(self, solicitud_id: UUID) -> None:
        raise NotImplementedError()


@dataclass
class AdaptadorMapas(ServicioMapas):
    tiempo_espera_ms: int = 5000

    def validar_ubicacion(self, latitud: Decimal, longitud: Decimal) -> bool:
        raise NotImplementedError("Integrar proveedor HTTPS con tiempo de espera")


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
        solicitud = SolicitudRecojo(
            vecino=vecino, punto=replace(punto),
            detalles=[replace(d) for d in detalles],
        )
        if not solicitud.validar_datos():
            raise ValueError("Datos de solicitud inválidos")
        if not self.cobertura.atiende_distrito(punto.codigo_distrito):
            raise ValueError("Distrito sin cobertura")

        if self.mapas:
            try:
                if self.mapas.validar_ubicacion(punto.latitud, punto.longitud):
                    solicitud.marcar_ubicacion_validada()
            except (TimeoutError, ConnectionError, OSError):
                logger.warning("Comprobación de mapas pendiente")

        solicitud.registrar_pendiente()
        self.repositorio.guardar(solicitud)
        # Demostración local de despacho asíncrono, no una cola durable.
        def avisar() -> None:
            try:
                self.notificador.confirmar_registro(solicitud.id)
            except Exception:
                logger.warning("Aviso de registro no entregado")

        try:
            Thread(target=avisar, daemon=True).start()
        except RuntimeError:
            logger.warning("Aviso de registro pendiente de despacho")
        return solicitud


class SolicitudController:
    def __init__(self, servicio: ServicioSolicitudes):
        self.servicio = servicio

    def registrar_solicitud(
        self, vecino: Vecino, punto: PuntoRecojo, detalles: List[DetalleReciclable]
    ) -> SolicitudRecojo:
        return self.servicio.solicitar_recojo(vecino, punto, detalles)


class PWA:
    def solicitar_recojo(
        self, vecino: Vecino, punto: PuntoRecojo, detalles: List[DetalleReciclable]
    ) -> None:
        raise NotImplementedError("Implementar presentación y almacenamiento local")
