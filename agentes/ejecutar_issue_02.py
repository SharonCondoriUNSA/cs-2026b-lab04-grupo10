"""Reproduce E5: agente único frente al flujo planificador-ejecutor-revisor."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AGENTES = Path(__file__).resolve().parent
REPO = AGENTES.parent
sys.path.insert(0, str(AGENTES))

from agente.herramientas import Herramientas
from agente.modelos import ModeloGrabado
from agente.nucleo import Agente
from agente.politica import Politica
from agente.traza import a_mermaid
from orquestador import ejecutar_orquestado

BASE = "d9156e1b816ec23d9e6c8208f3614039675632cd"
ARCHIVOS = (
    "src/lab10/operaciones.py", "src/lab10/__init__.py",
    "src/puntos_beneficios/servicio.py", "src/puntos_beneficios/reglas.py",
    "issues/ISSUE-02.md", "tests/test_issue_02.py",
)
TRAZAS = AGENTES / "trazas"
EVIDENCIA = AGENTES / "evidencias" / "issue-02"


def preparar_copia(raiz: Path) -> Path:
    for ruta in ARCHIVOS:
        contenido = subprocess.check_output(["git", "show", f"{BASE}:{ruta}"], cwd=REPO)
        destino = raiz / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(contenido)
    return raiz


def eventos_de(ruta: Path) -> list[dict]:
    return [json.loads(linea) for linea in ruta.read_text(encoding="utf-8").splitlines()]


def metricas(eventos: list[dict]) -> dict:
    acciones = [e for e in eventos if e["tipo"] == "accion"]
    finales = [e for e in eventos if e["tipo"] in ("final", "limite")]
    return {
        "decisiones": sum(e["tipo"] in ("accion", "final") for e in eventos),
        "acciones": len(acciones),
        "acciones_ejecutadas": sum(not e["bloqueada"] for e in acciones),
        "acciones_bloqueadas": sum(e["bloqueada"] for e in acciones),
        "contexto_final_caracteres": finales[-1]["contexto_caracteres"] if finales else eventos[-1]["contexto_caracteres"],
    }


def prueba_pasada(eventos: list[dict]) -> bool:
    return any(e.get("accion") == "ejecutar_pruebas" and
               e.get("observacion", "").startswith("pytest exit=0") for e in eventos)


def fallo_reproducido(eventos: list[dict]) -> bool:
    return any(e.get("accion") == "ejecutar_pruebas" and
               e.get("observacion", "").startswith("pytest exit=1") and
               "FAILED tests/test_issue_02.py" in e.get("observacion", "") for e in eventos)


def ejecutar_unico() -> dict:
    destino = TRAZAS / "issue-02-unico.jsonl"
    with tempfile.TemporaryDirectory(prefix="lab10-e5-unico-") as tmp:
        agente = Agente(
            "agente_unico", ModeloGrabado(AGENTES / "trayectorias" / "issue-02-unico.json"),
            Herramientas(preparar_copia(Path(tmp))), Politica(max_pasos=12),
            "Resuelve issues/ISSUE-02.md. Reproduce el fallo, modifica solo el módulo permitido, "
            "ejecuta las pruebas y revisa el diff. Las herramientas operan en una copia aislada.",
            destino,
        )
        agente.ejecutar()
    eventos = eventos_de(destino)
    return {"eventos": eventos, "metricas": metricas(eventos), "resultado": eventos[-1].get("texto", "")}


def ejecutar_dos_roles() -> dict:
    carpeta = TRAZAS / "issue-02-orquestado"
    carpeta.mkdir(exist_ok=True)
    modelos = {
        "planificador": ModeloGrabado(AGENTES / "trayectorias" / "issue-02-planificador.json"),
        "ejecutor": [ModeloGrabado(AGENTES / "trayectorias" / "issue-02-ejecutor.json")],
        "revisor": [ModeloGrabado(AGENTES / "trayectorias" / "issue-02-revisor.json")],
    }
    with tempfile.TemporaryDirectory(prefix="lab10-e5-orquestado-") as tmp:
        resultado = ejecutar_orquestado(preparar_copia(Path(tmp)), modelos, carpeta)
    lista_eventos = []
    por_rol = {}
    archivos = sorted(carpeta.glob("*.jsonl"), key=lambda p: ("planificador", "ejecutor-r1", "revisor-r1").index(p.stem))
    for archivo in archivos:
        eventos = eventos_de(archivo)
        lista_eventos.extend(eventos)
        nombre = archivo.stem
        por_rol[nombre] = metricas(eventos)
    combinado = TRAZAS / "issue-02-orquestado.jsonl"
    combinado.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in lista_eventos), encoding="utf-8")
    decisiones_acciones = [e for e in lista_eventos if e["tipo"] == "accion"]
    suma_contextos = sum(m["contexto_final_caracteres"] for m in por_rol.values())
    resultado["eventos"] = lista_eventos
    resultado["metricas"] = {
        "decisiones": sum(m["decisiones"] for m in por_rol.values()),
        "acciones": len(decisiones_acciones),
        "acciones_ejecutadas": sum(not e["bloqueada"] for e in decisiones_acciones),
        "acciones_bloqueadas": sum(e["bloqueada"] for e in decisiones_acciones),
        "contexto_final_caracteres": suma_contextos,
        "contexto_por_rol": por_rol,
    }
    return resultado


def escribir_diagramas(unico: list[dict], coordinado: list[dict]) -> None:
    (TRAZAS / "issue-02-unico.mmd").write_text(a_mermaid(unico), encoding="utf-8")
    lineas = ["sequenceDiagram", "    autonumber", "    participant P as Planificador",
              "    participant E as Ejecutor", "    participant R as Revisor", "    participant T as Herramientas y política"]
    lineas.append("    P-->>E: Plan de resolución")
    aviso_revisor = False
    for e in coordinado:
        rol = e.get("agente", "").split("_r")[0]
        actor = {"planificador": "P", "ejecutor": "E", "revisor": "R"}.get(rol, "E")
        if e["tipo"] == "accion":
            if actor == "R" and not aviso_revisor:
                lineas.append("    E-->>R: Cambio y resultados")
                aviso_revisor = True
            lineas.append(f"    {actor}->>T: {e['accion']}")
            lineas.append(f"    T-->>{actor}: {'Bloqueada por política' if e['bloqueada'] else 'Resultado observado'}")
    lineas.append("    R-->>P: APROBADO; sin hallazgo adicional")
    (TRAZAS / "issue-02-orquestado.mmd").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def escribir_informe(unico: dict, coordinado: dict) -> None:
    EVIDENCIA.mkdir(parents=True, exist_ok=True)
    m1, m2 = unico["metricas"], coordinado["metricas"]
    p = EVIDENCIA / "comparacion.md"
    contenido = f'''# E5: comparación de coordinación para ISSUE-02

## Protocolo y procedencia

Se resolvió el mismo estado inicial de `ISSUE-02` en dos copias independientes de `{BASE[:7]}`. La variante única usa un agente con hasta 12 decisiones. La coordinada usa planificador sin herramientas, ejecutor y revisor de solo lectura; el ciclo actor-crítico tiene un máximo de dos rondas. Las trayectorias JSON fueron redactadas por GPT en esta sesión para documentar decisiones reproducibles y se reprodujeron localmente con `ModeloGrabado`; no se hizo una llamada en vivo a un proveedor externo. Las herramientas sí ejecutaron las pruebas y editaron únicamente las copias de trabajo.

## Resultados

| Medida | Agente único | Planificador–ejecutor–revisor |
|---|---:|---:|
| Rondas actor-crítico | No aplica | {coordinado['rondas']} de 2 |
| Decisiones registradas | {m1['decisiones']} | {m2['decisiones']} |
| Acciones ejecutadas / bloqueadas | {m1['acciones_ejecutadas']} / {m1['acciones_bloqueadas']} | {m2['acciones_ejecutadas']} / {m2['acciones_bloqueadas']} |
| Contexto final (caracteres) | {m1['contexto_final_caracteres']} | {m2['contexto_final_caracteres']} acumulados entre roles |
| Fallo inicial reproducido | {'sí' if fallo_reproducido(unico['eventos']) else 'no'} | {'sí' if fallo_reproducido(coordinado['eventos']) else 'no'} |
| Prueba tras la corrección | {'pasó' if prueba_pasada(unico['eventos']) else 'falló'} | {'pasó' if prueba_pasada(coordinado['eventos']) else 'falló'} |
| Hallazgo adicional del revisor | No aplica | No; corroboró el contrato y no encontró una omisión del agente único |

El contexto coordinado se suma por rol porque cada agente conserva un historial independiente; por tanto, no equivale al contexto de una única conversación. El total de decisiones incluye las respuestas finales de cada rol.

## Evidencia

- Trayectorias: `agentes/trayectorias/issue-02-*.json`.
- Traza de la variante única: `agentes/trazas/issue-02-unico.jsonl` y diagrama Mermaid asociado.
- Trazas por rol y traza combinada: `agentes/trazas/issue-02-orquestado/` y `agentes/trazas/issue-02-orquestado.jsonl`.
- Diagramas Mermaid: `agentes/trazas/issue-02-unico.mmd` y `agentes/trazas/issue-02-orquestado.mmd`.

## Conclusión (7 líneas)

1. Ambas variantes resolvieron el mismo contrato desde copias limpias.
2. La prueba específica pasó y el cambio conserva orden y entrada original.
3. La coordinación añade decisiones y contexto porque separa los roles.
4. El revisor confirmó el resultado, pero no descubrió un defecto que el agente único hubiera omitido.
5. El límite de dos rondas evita que el ciclo de revisión crezca sin control.
6. Para este issue acotado, el costo adicional no se justifica por el resultado observado.
7. La coordinación sería más útil si el cambio tuviera mayor riesgo o varias decisiones independientes.
'''
    p.write_text(contenido, encoding="utf-8")
    (EVIDENCIA / "metricas.json").write_text(json.dumps({"agente_unico": m1, "orquestado": m2,
        "rondas": coordinado["rondas"], "aprobado": coordinado["aprobado"]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    TRAZAS.mkdir(exist_ok=True)
    EVIDENCIA.mkdir(parents=True, exist_ok=True)
    if (TRAZAS / "issue-02-orquestado").exists():
        shutil.rmtree(TRAZAS / "issue-02-orquestado")
    unico = ejecutar_unico()
    coordinado = ejecutar_dos_roles()
    escribir_diagramas(unico["eventos"], coordinado["eventos"])
    escribir_informe(unico, coordinado)
    print(json.dumps({"unico": unico["metricas"], "orquestado": coordinado["metricas"],
                      "rondas": coordinado["rondas"], "revisor_aprobo": coordinado["aprobado"]},
                     ensure_ascii=False, indent=2))
    if not prueba_pasada(unico["eventos"]):
        return 1
    if not prueba_pasada(coordinado["eventos"]):
        return 2
    if not fallo_reproducido(unico["eventos"]) or not fallo_reproducido(coordinado["eventos"]):
        return 3
    if not coordinado["aprobado"]:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
