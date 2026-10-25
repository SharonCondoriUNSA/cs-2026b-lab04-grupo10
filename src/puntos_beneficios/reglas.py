"""Strategy y Factory por registro para reglas de puntos internas al módulo."""
from abc import ABC, abstractmethod
from collections.abc import Callable
from decimal import Decimal, ROUND_DOWN


class ReglaPuntos(ABC):
    @abstractmethod
    def calcular(self, peso_real_kg: Decimal) -> int:
        """Calcula puntos sin modificar una solicitud ni invocar servicios externos."""


class PuntosPorPeso(ReglaPuntos):
    def __init__(self, tarifa):
        self.tarifa = tarifa

    def calcular(self, peso_real_kg):
        if (not isinstance(self.tarifa, Decimal) or not self.tarifa.is_finite()
                or self.tarifa < 0):
            raise ValueError("Tarifa de puntos invalida")
        if (not isinstance(peso_real_kg, Decimal)
                or not peso_real_kg.is_finite() or peso_real_kg <= 0):
            raise ValueError("Peso real invalido")
        return int((peso_real_kg * self.tarifa).to_integral_value(rounding=ROUND_DOWN))


class FabricaReglas:
    def __init__(self):
        # La misma fórmula parametrizada cubre los dos materiales de E1.
        # No se crean clases distintas que repitan un algoritmo idéntico.
        self._constructores: dict[str, Callable[[Decimal], ReglaPuntos]] = {
            "PLASTICO": PuntosPorPeso,
            "PAPEL": PuntosPorPeso,
        }

    def registrar(self, material: str, constructor: Callable[[Decimal], ReglaPuntos]):
        self._constructores[material] = constructor

    def crear(self, material: str, tarifa) -> ReglaPuntos:
        try:
            constructor = self._constructores[material]
        except KeyError:
            raise ValueError("Material sin regla de puntos") from None
        return constructor(tarifa)
