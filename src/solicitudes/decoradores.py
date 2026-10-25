"""Decorator de reintentos para consultas de mapas sin efectos de negocio."""
from src.solicitudes.mapas import PuertoMapas


class ConReintentos(PuertoMapas):
    def __init__(self, envuelto: PuertoMapas, max_intentos=3):
        if type(max_intentos) is not int or max_intentos < 1:
            raise ValueError("Numero de intentos invalido")
        self.envuelto = envuelto
        self.max_intentos = max_intentos

    def validar_ubicacion(self, latitud, longitud):
        for _ in range(self.max_intentos):
            try:
                return self.envuelto.validar_ubicacion(latitud, longitud)
            except (TimeoutError, ConnectionError):
                pass
        return False
