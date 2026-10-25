"""Puerto, adaptadores técnicos y registro de mapas, sin reglas de negocio."""
from abc import ABC, abstractmethod
from collections.abc import Callable
from decimal import Decimal


class PuertoMapas(ABC):
    @abstractmethod
    def validar_ubicacion(self, latitud: Decimal, longitud: Decimal) -> bool:
        """Traduce la respuesta del proveedor, los errores transitorios se propagan."""


class MapaAdapter(PuertoMapas):
    def __init__(self, sdk):
        self.sdk = sdk

    def validar_ubicacion(self, latitud, longitud):
        return self.sdk.verificar(latitud, longitud)["ubicacion_valida"]


class GeoAdapter(PuertoMapas):
    def __init__(self, cliente):
        self.cliente = cliente

    def validar_ubicacion(self, latitud, longitud):
        codigo, _ = self.cliente.check((latitud, longitud))
        return codigo == 200


class FabricaMapas:
    def __init__(self):
        self._constructores: dict[str, Callable[[], PuertoMapas]] = {}

    def registrar(self, nombre: str, constructor: Callable[[], PuertoMapas]):
        self._constructores[nombre] = constructor

    def crear(self, nombre: str) -> PuertoMapas:
        try:
            constructor = self._constructores[nombre]
        except KeyError:
            raise ValueError("Proveedor no soportado") from None
        return constructor()
