"""Entidad refactorizada, conserva el constructor y etiquetas de la línea base."""
from src.solicitudes.antes.servicio import Detalle, RepositorioMemoria
from src.solicitudes.antes.servicio import Solicitud as SolicitudAntes
from src.solicitudes.estados import Finalizada, desde_nombre


class Solicitud(SolicitudAntes):
    @property
    def estado(self):
        return self._estado_objeto.nombre

    @estado.setter
    def estado(self, nombre):
        self._estado_objeto = desde_nombre(nombre)

    def _estado_actual(self):
        # Compatibilidad con el indicador público de cierre de E1.
        if self.cerrada:
            return Finalizada()
        return self._estado_objeto

    def comprobar_registro(self):
        self._estado_actual().comprobar_registro(self)

    def registrar_pendiente(self):
        """Se invoca tras validar datos y cobertura en el servicio de registro."""
        self._estado_actual().registrar_pendiente(self)

    def asignar_reciclador(self, reciclador_id):
        self._estado_actual().asignar_reciclador(self, reciclador_id)

    def registrar_recojo(self, fecha_recojo):
        self._estado_actual().registrar_recojo(self, fecha_recojo)

    def registrar_pesaje(self, peso_real_kg):
        self._estado_actual().registrar_pesaje(self, peso_real_kg)

    def comprobar_acreditacion(self):
        self._estado_actual().comprobar_acreditacion(self)

    def confirmar_puntos_acreditados(self, acreditacion_id):
        self._estado_actual().confirmar_puntos_acreditados(self, acreditacion_id)

    def cerrar(self):
        self._estado_actual().cerrar(self)
