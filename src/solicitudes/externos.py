"""Dos proveedores de mapas ficticios, sin red, claves ni datos personales."""


class MapaSDK:
    def __init__(self, valida=True, fallas=0):
        self.valida = valida
        self.fallas = fallas
        self.llamadas = 0

    def verificar(self, latitud, longitud):
        self.llamadas += 1
        if self.llamadas <= self.fallas:
            raise TimeoutError("MapaSDK no responde")
        return {"ubicacion_valida": self.valida}


class GeoClient:
    def __init__(self, valida=True, fallas=0):
        self.valida = valida
        self.fallas = fallas
        self.llamadas = 0

    def check(self, coordenadas):
        self.llamadas += 1
        if self.llamadas <= self.fallas:
            raise ConnectionError("GeoClient sin conexion")
        return (200 if self.valida else 422, coordenadas)
