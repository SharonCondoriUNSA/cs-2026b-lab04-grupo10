"""Servicio interno de acreditación, delega el cálculo a la regla seleccionada."""
from src.puntos_beneficios.reglas import FabricaReglas


class ServicioPuntos:
    def __init__(self, tarifas, fabrica=None):
        self.tarifas = dict(tarifas)
        self.fabrica = fabrica if fabrica is not None else FabricaReglas()

    def acreditar(self, solicitud_id, material, peso_real_kg):
        regla = self.fabrica.crear(material, self.tarifas.get(material))
        puntos = regla.calcular(peso_real_kg)
        return {"acreditacion_id": f"acreditacion:{solicitud_id}", "puntos": puntos}
