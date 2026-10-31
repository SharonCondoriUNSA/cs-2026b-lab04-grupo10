"""Prototipo E2, configuración distrital sintética. No modifica el código Lab07.

Ejecutar desde la raíz: python -m fitness.distritos
No representa configuración aprobada por municipalidades ni una base de datos real.
"""
from dataclasses import dataclass, replace
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from src.puntos_beneficios.reglas import FabricaReglas


@dataclass(frozen=True)
class ConfiguracionDistrito:
    distrito: str
    tarifa: Decimal
    inicio_hora: int
    fin_hora: int
    version: int = 1

    def __post_init__(self):
        if not self.distrito or not self.tarifa.is_finite() or self.tarifa < 0:
            raise ValueError("Configuracion distrital invalida")
        if not 0 <= self.inicio_hora < self.fin_hora <= 24 or self.version < 1:
            raise ValueError("Horario o version invalidos")


class CatalogoDistritos:
    def __init__(self, configuraciones):
        self._configuraciones = {}
        for configuracion in configuraciones:
            self.incorporar(configuracion)

    def incorporar(self, configuracion):
        if configuracion.distrito in self._configuraciones:
            raise ValueError("Distrito ya registrado")
        self._configuraciones[configuracion.distrito] = configuracion

    def obtener(self, distrito):
        try:
            return self._configuraciones[distrito]
        except KeyError:
            raise ValueError("Distrito sin configurar") from None

    def publicar(self, configuracion):
        anterior = self.obtener(configuracion.distrito)
        if configuracion.version <= anterior.version:
            raise ValueError("Version no creciente")
        self._configuraciones[configuracion.distrito] = configuracion


class ConsultaDistrital:
    """Fachada de laboratorio. Contratos de puntos y cobertura siguen separados.

    En integración se exponen dos contratos públicos por los módulos respectivos.
    Esta fachada no accede a sus esquemas ni acredita solicitudes de recojo.
    """
    def __init__(self, catalogo, fabrica=None):
        self.catalogo = catalogo
        self.fabrica = fabrica if fabrica is not None else FabricaReglas()

    def calcular(self, distrito, material, peso):
        configuracion = self.catalogo.obtener(distrito)
        return self.fabrica.crear(material, configuracion.tarifa).calcular(peso)

    def horario(self, distrito):
        configuracion = self.catalogo.obtener(distrito)
        return configuracion.inicio_hora, configuracion.fin_hora


def configuraciones():
    return [ConfiguracionDistrito(f"D{i:02}", Decimal(i), 7 + i % 4, 9 + i % 4)
            for i in range(1, 13)]


def huellas_consumidores():
    raiz = Path(__file__).resolve().parents[1]
    return {nombre: sha256((raiz / nombre).read_bytes()).hexdigest() for nombre in (
        "src/solicitudes/servicio.py", "src/puntos_beneficios/servicio.py",
        "src/puntos_beneficios/reglas.py")}


def experimentar():
    datos = configuraciones()
    antes = huellas_consumidores()
    catalogo = CatalogoDistritos(datos[:3])
    servicio = ConsultaDistrital(catalogo)
    peso = Decimal("2")
    rechazados_antes = 0
    for dato in datos[3:]:
        try:
            servicio.horario(dato.distrito)
        except ValueError:
            rechazados_antes += 1
    inicio = perf_counter()
    for dato in datos[3:]:
        catalogo.incorporar(dato)
    alta_ms = (perf_counter() - inicio) * 1000
    verificaciones = 0
    for dato in datos:
        assert servicio.calcular(dato.distrito, "PLASTICO", peso) == int(dato.tarifa * peso)
        assert servicio.horario(dato.distrito) == (dato.inicio_hora, dato.fin_hora)
        verificaciones += 2
    otros_antes = {dato.distrito: (servicio.calcular(dato.distrito, "PLASTICO", peso),
                                 servicio.horario(dato.distrito)) for dato in datos[1:]}
    catalogo.publicar(replace(datos[0], tarifa=Decimal("99"), inicio_hora=6,
                             fin_hora=8, version=2))
    assert servicio.calcular("D01", "PLASTICO", peso) == 198
    assert servicio.horario("D01") == (6, 8)
    alterados = sum(otros_antes[dato.distrito] != (
        servicio.calcular(dato.distrito, "PLASTICO", peso), servicio.horario(dato.distrito))
        for dato in datos[1:])
    despues = huellas_consumidores()
    assert antes == despues and alterados == 0
    return {"distritos_antes": 3, "distritos_despues": 12,
            "altas_rechazadas_antes": rechazados_antes, "altas_configuradas": 9,
            "comprobaciones_regla_horario": verificaciones,
            "archivos_consumidores_modificados": sum(antes[k] != despues[k] for k in antes),
            "otros_distritos_alterados": alterados, "alta_configuracion_ms": round(alta_ms, 4),
            "huellas_consumidores": despues,
            "dias_persona": None, "limite": "No se midio esfuerzo humano de integracion"}


if __name__ == "__main__":
    print(json.dumps(experimentar(), ensure_ascii=False, indent=2))
