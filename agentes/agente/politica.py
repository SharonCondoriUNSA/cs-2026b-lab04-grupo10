"""Guardrails: qué puede hacer el agente, cuántas veces y con qué aprobación."""
from dataclasses import dataclass, field


MODULO_EDITABLE = "src/lab10/operaciones.py"


@dataclass
class Decision:
    permitido: bool
    motivo: str = ""


@dataclass
class Politica:
    herramientas_permitidas: set = field(default_factory=lambda: {
        "listar_archivos", "leer_archivo", "buscar", "ejecutar_pruebas", "editar_archivo", "ver_cambios", "ejecutar_comando"})
    max_pasos: int = 12
    aprobar_edicion = None                          # función opcional: humano en el circuito (human-in-the-loop)

    def evaluar(self, accion: str, args: dict, paso: int) -> Decision:
        if paso > self.max_pasos:
            return Decision(False, f"Se alcanzó el máximo de {self.max_pasos} pasos")
        if accion not in self.herramientas_permitidas:
            return Decision(False, f"Herramienta no permitida: {accion}")
        if accion == "ejecutar_comando":
            cmd = args.get("comando", "")
            if cmd != "python -m pytest -q":
                return Decision(False, f"Comando fuera de la lista permitida: {cmd!r}")
        if accion == "editar_archivo":
            ruta = args.get("ruta", "")
            if ruta != MODULO_EDITABLE:
                return Decision(False, f"Ruta protegida: {ruta}")
            if self.aprobar_edicion and not self.aprobar_edicion(args):
                return Decision(False, "El revisor humano rechazó la edición")
        return Decision(True)
