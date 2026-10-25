"""Reglas ingenuas del módulo interno Puntos/Beneficios, tarifas inyectadas."""
from decimal import Decimal, ROUND_DOWN


class ServicioPuntos:
    def __init__(self, tarifas):
        self.tarifas = dict(tarifas)

    def acreditar(self, solicitud_id, material, peso_real_kg):
        # Variación principal del caso 10, todavía sin Strategy ni Factory.
        if material == "PLASTICO":
            tarifa = self.tarifas.get("PLASTICO")
        elif material == "PAPEL":
            tarifa = self.tarifas.get("PAPEL")
        else:
            raise ValueError("Material sin regla de puntos")
        if not isinstance(tarifa, Decimal) or not tarifa.is_finite() or tarifa < 0:
            raise ValueError("Tarifa de puntos invalida")
        if (not isinstance(peso_real_kg, Decimal)
                or not peso_real_kg.is_finite() or peso_real_kg <= 0):
            raise ValueError("Peso real invalido")
        puntos = int((peso_real_kg * tarifa).to_integral_value(rounding=ROUND_DOWN))
        return {"acreditacion_id": f"acreditacion:{solicitud_id}", "puntos": puntos}
