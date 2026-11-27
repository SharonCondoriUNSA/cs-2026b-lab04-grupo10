"""Escenario E1 con tres errores sembrados para el ejercicio de agentes.

No forma parte de la ejecución de los servicios de Lab07–Lab09. Se reutiliza
su cálculo de puntos, sin modificarlo. Datos y saldos son sintéticos y locales.
"""
from dataclasses import dataclass
from decimal import Decimal

from src.puntos_beneficios.servicio import ServicioPuntos


class LibroPuntos:
    def __init__(self, tarifas):
        self.servicio = ServicioPuntos(tarifas)
        self.movimientos = []

    @property
    def saldo(self):
        return sum(movimiento["puntos"] for movimiento in self.movimientos)

    def acreditar(self, solicitud_id, material, peso_real_kg):
        resultado = self.servicio.acreditar(solicitud_id, material, peso_real_kg)
        for movimiento in self.movimientos:
            if movimiento["acreditacion_id"] == resultado["acreditacion_id"]:
                return dict(movimiento)
        self.movimientos.append(resultado)
        return dict(resultado)


@dataclass(frozen=True)
class Parada:
    solicitud_id: str
    estado: str


def preparar_ruta(solicitudes):
    """Devuelve una lista nueva sin modificar las solicitudes recibidas."""
    return list(solicitudes)


class TarifasDistritales:
    def __init__(self, distritos, tarifas):
        self._tarifas = {distrito: dict(tarifas) for distrito in distritos}

    def actualizar(self, distrito, material, tarifa):
        self._tarifas[distrito][material] = tarifa

    def calcular(self, distrito, material, peso_real_kg: Decimal):
        servicio = ServicioPuntos(self._tarifas[distrito])
        return servicio.acreditar("calculo-sintetico", material, peso_real_kg)["puntos"]
