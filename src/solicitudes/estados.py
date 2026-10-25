"""State de SolicitudRecojo, basado en estados-solicitud.mmd del Lab05."""
from datetime import datetime
from decimal import Decimal


class Estado:
    nombre = None

    def comprobar_registro(self, solicitud):
        raise ValueError("Solicitud ya registrada")

    def registrar_pendiente(self, solicitud):
        raise ValueError("Solicitud ya registrada")

    def asignar_reciclador(self, solicitud, reciclador_id):
        raise ValueError("Transicion invalida")

    def registrar_recojo(self, solicitud, fecha_recojo):
        raise ValueError("Transicion invalida")

    def registrar_pesaje(self, solicitud, peso_real_kg):
        raise ValueError("Transicion invalida")

    def comprobar_acreditacion(self, solicitud):
        raise ValueError("Transicion invalida")

    def confirmar_puntos_acreditados(self, solicitud, acreditacion_id):
        raise ValueError("Transicion invalida")

    def cerrar(self, solicitud):
        raise ValueError("Transicion invalida")


class SinRegistrar(Estado):
    """Pseudoinicio, no es un sexto estado del dominio."""

    def comprobar_registro(self, solicitud):
        pass

    def registrar_pendiente(self, solicitud):
        solicitud._estado_objeto = Pendiente()


class Pendiente(Estado):
    nombre = "PENDIENTE"

    def asignar_reciclador(self, solicitud, reciclador_id):
        if not isinstance(reciclador_id, str) or not reciclador_id.strip():
            raise ValueError("Reciclador invalido")
        solicitud.reciclador_id = reciclador_id
        solicitud._estado_objeto = Asignada()


class Asignada(Estado):
    nombre = "ASIGNADA"

    def registrar_recojo(self, solicitud, fecha_recojo):
        if not isinstance(fecha_recojo, datetime):
            raise ValueError("Fecha invalida")
        solicitud.fecha_recojo = fecha_recojo
        solicitud._estado_objeto = Recogida()


class Recogida(Estado):
    nombre = "RECOGIDA"

    def registrar_pesaje(self, solicitud, peso_real_kg):
        if (not isinstance(peso_real_kg, Decimal)
                or not peso_real_kg.is_finite() or peso_real_kg <= 0):
            raise ValueError("Peso real invalido")
        solicitud.peso_real_kg = peso_real_kg
        solicitud._estado_objeto = Pesada()


class Pesada(Estado):
    nombre = "PESADA"

    def comprobar_acreditacion(self, solicitud):
        pass

    def confirmar_puntos_acreditados(self, solicitud, acreditacion_id):
        if not isinstance(acreditacion_id, str) or not acreditacion_id.strip():
            raise ValueError("Acreditacion invalida")
        solicitud.acreditacion_id = acreditacion_id
        solicitud._estado_objeto = PuntosAcreditados()


class PuntosAcreditados(Estado):
    nombre = "PUNTOS_ACREDITADOS"

    def cerrar(self, solicitud):
        solicitud.cerrada = True
        solicitud._estado_objeto = Finalizada()


class Finalizada(Estado):
    """Pseudofinal sin salidas, conserva la última etiqueta pública del dominio."""
    nombre = "PUNTOS_ACREDITADOS"


def desde_nombre(nombre):
    """Compatibilidad de construcción con E1, selección ajena a las transiciones."""
    tipos = {None: SinRegistrar, "PENDIENTE": Pendiente, "ASIGNADA": Asignada,
             "RECOGIDA": Recogida, "PESADA": Pesada,
             "PUNTOS_ACREDITADOS": PuntosAcreditados}
    try:
        tipo = tipos[nombre]
    except KeyError:
        raise ValueError("Estado desconocido") from None
    return tipo()
