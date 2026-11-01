"""Prototipo de autorización distrital E4. No valida JWT ni implementa RLS.

El ámbito de ContextoConfiable debe proceder de autenticación del servidor.
Comparación con un acceso inseguro deliberado, no con una vulnerabilidad
comprobada en el código Lab07. Ejecutar: python -m fitness.aislamiento
"""
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class ContextoConfiable:
    distrito: str


class RepositorioDistrital:
    def __init__(self):
        self._datos = {f"D{i:02}": f"registro-sintetico-{i}" for i in range(1, 13)}

    def _autorizar(self, contexto, distrito_solicitado):
        if (not isinstance(contexto, ContextoConfiable)
                or contexto.distrito not in self._datos
                or contexto.distrito != distrito_solicitado):
            raise PermissionError("Ambito distrital no autorizado")

    def consultar(self, contexto, distrito_solicitado):
        self._autorizar(contexto, distrito_solicitado)
        return self._datos[distrito_solicitado]

    def actualizar(self, contexto, distrito_solicitado, valor):
        self._autorizar(contexto, distrito_solicitado)
        self._datos[distrito_solicitado] = valor


def experimentar():
    repositorio = RepositorioDistrital()
    distritos = list(repositorio._datos)
    original = dict(repositorio._datos)
    lecturas = escrituras = rechazadas = 0
    for origen in distritos:
        contexto = ContextoConfiable(origen)
        assert repositorio.consultar(contexto, origen) == original[origen]
        repositorio.actualizar(contexto, origen, original[origen])
        for destino in distritos:
            if origen == destino:
                continue
            try:
                repositorio.consultar(contexto, destino)
                lecturas += 1
            except PermissionError:
                rechazadas += 1
            try:
                repositorio.actualizar(contexto, destino, "intrusion")
                escrituras += 1
            except PermissionError:
                rechazadas += 1
    sin_ambito = 0
    for contexto in (None, ContextoConfiable(""), ContextoConfiable("INEXISTENTE")):
        for distrito in distritos:
            for operacion in (repositorio.consultar,
                              lambda ctx, dst: repositorio.actualizar(ctx, dst, "intrusion")):
                try:
                    operacion(contexto, distrito)
                except PermissionError:
                    sin_ambito += 1
    assert lecturas == escrituras == 0 and rechazadas == 264 and sin_ambito == 72
    assert original == repositorio._datos
    # Control negativo: quitar la guarda permite leer y escribir los 132 pares.
    inseguro = dict(original)
    expuestas = alteraciones = 0
    for origen in distritos:
        for destino in distritos:
            if origen != destino:
                assert inseguro[destino]
                expuestas += 1
                inseguro[destino] = "intrusion"
                alteraciones += 1
    return {"distritos": 12, "pares_cruzados": 132,
            "antes_control_inseguro_lecturas": expuestas,
            "antes_control_inseguro_escrituras": alteraciones,
            "despues_lecturas_cruzadas": lecturas, "despues_escrituras_cruzadas": escrituras,
            "operaciones_cruzadas_rechazadas": rechazadas,
            "operaciones_sin_ambito_rechazadas": sin_ambito,
            "operaciones_propias_permitidas": 24,
            "datos_originales_conservados": original == repositorio._datos}


if __name__ == "__main__":
    print(json.dumps(experimentar(), indent=2))
