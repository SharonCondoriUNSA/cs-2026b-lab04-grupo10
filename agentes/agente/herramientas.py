"""Herramientas del agente. Cada una es una función pequeña, con descripción y parámetros explícitos.
Todas operan DENTRO del directorio de trabajo (sandbox)."""
import difflib
import os
import pathlib
import re
import subprocess
import sys

from agente.politica import MODULO_EDITABLE


class Herramientas:
    def __init__(self, raiz: str):
        self.raiz = pathlib.Path(raiz).resolve()
        modulo = self._ruta(MODULO_EDITABLE)
        self.original = modulo.read_text(encoding="utf-8") if modulo.exists() else ""

    # --- utilidades ---
    def _ruta(self, ruta: str) -> pathlib.Path:
        p = (self.raiz / ruta).resolve()
        if self.raiz not in p.parents and p != self.raiz:
            raise PermissionError(f"Ruta fuera del sandbox: {ruta}")
        return p

    def catalogo(self) -> dict:
        """Descripción de las herramientas que se envía al modelo (como en un MCP server)."""
        return {
            "listar_archivos": "listar_archivos(carpeta='.'): lista los archivos .py y .md",
            "leer_archivo": "leer_archivo(ruta): devuelve el contenido con números de línea",
            "buscar": "buscar(patron): busca una expresión regular en los archivos .py",
            "ejecutar_pruebas": "ejecutar_pruebas(): ejecuta las pruebas de la copia y devuelve el código de salida y el resumen de pytest",
            "editar_archivo": "editar_archivo(ruta, antes, despues): reemplaza un fragmento exacto (una sola vez)",
            "ver_cambios": "ver_cambios(): muestra el diff respecto de la versión original",
            "ejecutar_comando": "ejecutar_comando(comando): admite únicamente 'python -m pytest -q' sobre la copia",
        }

    # --- herramientas ---
    def listar_archivos(self, carpeta="."):
        base = self._ruta(carpeta)
        return "\n".join(sorted(self._ruta(p).relative_to(self.raiz).as_posix() for p in base.rglob("*")
                                if p.suffix in (".py", ".md") and "__pycache__" not in p.parts))

    def leer_archivo(self, ruta):
        lineas = self._ruta(ruta).read_text(encoding="utf-8").splitlines()
        return "\n".join(f"{i:3d}| {l}" for i, l in enumerate(lineas, 1))

    def buscar(self, patron):
        rx, hallazgos = re.compile(patron), []
        for p in sorted(self.raiz.rglob("*.py")):
            for i, l in enumerate(self._ruta(p).read_text(encoding="utf-8").splitlines(), 1):
                if rx.search(l):
                    hallazgos.append(f"{p.relative_to(self.raiz)}:{i}: {l.strip()}")
        return "\n".join(hallazgos) or "(sin resultados)"

    def ejecutar_pruebas(self):
        entorno = {k: os.environ[k] for k in ("SYSTEMROOT", "TEMP", "TMP", "PATH", "PYTHONPATH") if k in os.environ}
        entorno.update(PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
        r = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "--no-header", "-p", "no:cacheprovider"],
                           cwd=self.raiz, env=entorno, capture_output=True, text=True, encoding="utf-8", timeout=120)
        salida = (r.stdout + r.stderr).strip().splitlines()
        fallos = [l for l in salida if l.startswith(("FAILED", "E "))][:6]
        return "\n".join([f"pytest exit={r.returncode}", *fallos, *salida[-1:]])

    def editar_archivo(self, ruta, antes, despues):
        if ruta != MODULO_EDITABLE:
            raise PermissionError(f"Ruta protegida: {ruta}")
        p = self._ruta(ruta)
        texto = p.read_text(encoding="utf-8")
        if not antes or texto.count(antes) != 1:
            return f"ERROR: el fragmento aparece {texto.count(antes)} veces; debe aparecer exactamente 1"
        p.write_text(texto.replace(antes, despues), encoding="utf-8")
        return f"OK: {ruta} modificado"

    def ver_cambios(self):
        actual = self._ruta(MODULO_EDITABLE).read_text(encoding="utf-8")
        diff = difflib.unified_diff(self.original.splitlines(), actual.splitlines(),
                                    f"a/{MODULO_EDITABLE}", f"b/{MODULO_EDITABLE}", lineterm="")
        return "\n".join(diff) or "(sin cambios)"

    def ejecutar_comando(self, comando):
        if comando != "python -m pytest -q":
            raise PermissionError("Comando fuera de la lista permitida")
        return self.ejecutar_pruebas()
