"""Observer local, registra intenciones de aviso, no realiza envíos externos."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class EventoSolicitud:
    tipo: str
    solicitud_id: str
    puntos: int = 0
    peso_real_kg: Decimal | None = None


class Suscriptor(ABC):
    @abstractmethod
    def recibir(self, evento: EventoSolicitud) -> None:
        """Consume datos del evento sin recibir la entidad mutable."""


class PublicadorEventos:
    def __init__(self):
        self._suscriptores = []
        self.fallos = []

    def suscribir(self, suscriptor: Suscriptor):
        self._suscriptores.append(suscriptor)

    def publicar(self, evento: EventoSolicitud):
        for suscriptor in tuple(self._suscriptores):
            try:
                suscriptor.recibir(evento)
            except Exception as error:
                # Un consumidor que falla no revierte el registro ni bloquea al resto.
                self.fallos.append((evento.solicitud_id, type(error).__name__))


class AvisosInternos(Suscriptor):
    def __init__(self, buzon):
        self.buzon = buzon

    def recibir(self, evento):
        if evento.tipo == "REGISTRADA":
            self.buzon.append(f"aviso_interno:{evento.solicitud_id}:PENDIENTE")
        elif evento.tipo == "PUNTOS_ACREDITADOS":
            self.buzon.append(f"puntos:{evento.solicitud_id}:{evento.puntos}")


class ProyeccionPesajes(Suscriptor):
    """Consumidor ilustrativo de eventos, sin acceder al esquema de Solicitudes."""
    def __init__(self, buzon):
        self.buzon = buzon

    def recibir(self, evento):
        if evento.tipo == "PUNTOS_ACREDITADOS":
            self.buzon.append(f"reporte_pesaje:{evento.solicitud_id}:{evento.peso_real_kg}")
