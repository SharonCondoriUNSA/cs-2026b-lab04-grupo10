"""Reproduce E5: agente único frente al flujo planificador-ejecutor-revisor."""
import argparse
import json
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
from agente.traza import a_mermaid, etiqueta, prueba_pasada, resumir
from orquestador import ejecutar_orquestado, veredicto_revisor

BASE = "d9156e1b816ec23d9e6c8208f3614039675632cd"
ARCHIVOS = (
    "src/lab10/operaciones.py", "src/lab10/__init__.py",
    "src/puntos_beneficios/servicio.py", "src/puntos_beneficios/reglas.py",
    "issues/ISSUE-02.md", "tests/test_issue_02.py",
)


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


def fallo_reproducido(eventos: list[dict]) -> bool:
    return any(e.get("accion") == "ejecutar_pruebas" and
               e.get("observacion", "").startswith("pytest exit=1") and
               "FAILED tests/test_issue_02.py" in e.get("observacion", "") for e in eventos)


def ejecutar_unico(trazas: Path) -> dict:
    destino = trazas / "issue-02-unico.jsonl"
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


def ejecutar_dos_roles(trazas: Path) -> dict:
    carpeta = trazas / "issue-02-orquestado"
    carpeta.mkdir()
    modelos = {
        "planificador": ModeloGrabado(AGENTES / "trayectorias" / "issue-02-planificador.json"),
        "ejecutor": [ModeloGrabado(AGENTES / "trayectorias" / "issue-02-ejecutor.json")],
        "revisor": [ModeloGrabado(AGENTES / "trayectorias" / "issue-02-revisor.json")],
    }
    for rol in ("ejecutor", "revisor"):
        segunda = AGENTES / "trayectorias" / f"issue-02-{rol}-r2.json"
        if segunda.is_file():
            modelos[rol].append(ModeloGrabado(segunda))
    with tempfile.TemporaryDirectory(prefix="lab10-e5-orquestado-") as tmp:
        resultado = ejecutar_orquestado(preparar_copia(Path(tmp)), modelos, carpeta)
    lista_eventos = []
    por_rol = {}
    for agente in resultado["agentes"]:
        eventos = agente.eventos
        lista_eventos.extend(eventos)
        nombre = agente.traza_archivo.stem
        por_rol[nombre] = metricas(eventos)
    combinado = trazas / "issue-02-orquestado.jsonl"
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


def escribir_diagramas(trazas: Path, unico: list[dict], coordinado: list[dict]) -> None:
    (trazas / "issue-02-unico.mmd").write_text(a_mermaid(unico), encoding="utf-8")
    lineas = ["sequenceDiagram", "    autonumber", "    participant P as Planificador",
              "    participant E as Ejecutor", "    participant R as Revisor", "    participant T as Herramientas y política"]
    turno = []
    for e in coordinado:
        rol = e["agente"].split("_r")[0]
        actor = {"planificador": "P", "ejecutor": "E", "revisor": "R"}[rol]
        if e["tipo"] == "objetivo":
            turno = []
            if actor == "R":
                lineas.append("    E-->>R: Cambio y resultados")
            elif actor == "E":
                numero = e["agente"].split("_r")[1]
                lineas.append(f"    P-->>E: Plan y objetivo de la ronda {numero}")
        turno.append(e)
        if e["tipo"] == "accion":
            lineas.append(f"    {actor}->>T: {etiqueta(e['accion'])}")
            observacion = e["observacion"] if e["bloqueada"] else resumir(e)
            lineas.append(f"    T-->>{actor}: {etiqueta(observacion)}")
        elif actor == "R" and e["tipo"] in ("final", "limite"):
            estado = veredicto_revisor(turno).partition(".")[0]
            lineas.append(f"    R-->>P: {etiqueta(estado)}")
    (trazas / "issue-02-orquestado.mmd").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def escribir_informe(evidencia: Path, unico: dict, coordinado: dict) -> None:
    evidencia.mkdir(parents=True)
    m1, m2 = unico["metricas"], coordinado["metricas"]
    p = evidencia / "comparacion.md"
    estado_unico = "pasó" if prueba_pasada(unico["eventos"]) else "sin prueba final aprobada"
    estado_coordinado = "pasó" if prueba_pasada(coordinado["eventos"]) else "sin prueba final aprobada"
    resuelto = (prueba_pasada(unico["eventos"]) and prueba_pasada(coordinado["eventos"])
                and coordinado["aprobado"] and fallo_reproducido(unico["eventos"])
                and fallo_reproducido(coordinado["eventos"]))
    conclusion = ("Ambas variantes resolvieron el mismo contrato desde copias limpias." if resuelto
                  else "La evidencia de esta ejecución es insuficiente para dar el issue por resuelto en ambas variantes.")
    contenido = f'''# E5: comparación de coordinación para ISSUE-02

## Protocolo y procedencia

Las dos variantes partieron de copias independientes de `{BASE[:7]}`. La variante única usa un agente con hasta 12 decisiones. La coordinada usa planificador sin herramientas, ejecutor y revisor de solo lectura. El máximo es de dos rondas. Las decisiones proceden de las trayectorias de E5 preparadas con apoyo de GPT y reproducidas con `ModeloGrabado`. Las herramientas operan en copias de trabajo.

## Resultados

| Medida | Agente único | Planificador–ejecutor–revisor |
|---|---:|---:|
| Rondas actor-crítico | No aplica | {coordinado['rondas']} de 2 |
| Decisiones registradas | {m1['decisiones']} | {m2['decisiones']} |
| Acciones ejecutadas / bloqueadas | {m1['acciones_ejecutadas']} / {m1['acciones_bloqueadas']} | {m2['acciones_ejecutadas']} / {m2['acciones_bloqueadas']} |
| Contexto final (caracteres) | {m1['contexto_final_caracteres']} | {m2['contexto_final_caracteres']} acumulados entre roles |
| Fallo inicial reproducido | {'sí' if fallo_reproducido(unico['eventos']) else 'no'} | {'sí' if fallo_reproducido(coordinado['eventos']) else 'no'} |
| Última verificación de la copia | {estado_unico} | {estado_coordinado} |
| Veredicto y hallazgos del revisor | No aplica | {coordinado['veredicto']} |

El contexto coordinado se suma por rol porque cada agente conserva un historial independiente; por tanto, no equivale al contexto de una única conversación. El total de decisiones incluye las respuestas finales de cada rol.

## Evidencia

Las decisiones grabadas se encuentran en `agentes/trayectorias/issue-02-*.json` del repositorio.
Las observaciones de esta ejecución se pueden consultar en la [traza del agente único](../../trazas/issue-02-unico.jsonl)
y la [traza coordinada](../../trazas/issue-02-orquestado.jsonl).
Para reproducirlas en una carpeta nueva, ejecutar desde la raíz
`python agentes/ejecutar_issue_02.py --salida ../replay-e5`.

## Conclusión (7 líneas)

1. {conclusion}
2. La prueba de rutas verifica exclusión de canceladas, orden y conservación de la entrada.
3. El agente único empleó {m1['decisiones']} decisiones y la coordinación empleó {m2['decisiones']}.
4. Se completaron {coordinado['rondas']} rondas de revisión de un máximo de dos.
5. El agente único registró {m1['acciones_bloqueadas']} acciones bloqueadas y la variante coordinada registró {m2['acciones_bloqueadas']}.
6. El contexto agregado del equipo fue de {m2['contexto_final_caracteres']} caracteres, frente a {m1['contexto_final_caracteres']} del agente único.
7. {'Para satisfacer esta prueba de rutas bastó el agente único. En este caso, incorporar dos roles adicionales no fue necesario para alcanzar el resultado funcional.' if resuelto else 'Queda pendiente verificar la resolución antes de valorar el costo de coordinar los roles.'}
'''
    p.write_text(contenido, encoding="utf-8")
    (evidencia / "metricas.json").write_text(json.dumps({"agente_unico": m1, "orquestado": m2,
        "rondas": coordinado["rondas"], "aprobado": coordinado["aprobado"]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, help="directorio nuevo para las trazas y el informe")
    salida = parser.parse_args().salida
    if salida is None:
        salida = Path(tempfile.mkdtemp(prefix="lab10-e5-"))
    else:
        salida.mkdir(parents=True, exist_ok=False)
    print(f"Evidencias de la ejecución: {salida.resolve()}")
    trazas = salida / "trazas"
    trazas.mkdir()
    unico = ejecutar_unico(trazas)
    coordinado = ejecutar_dos_roles(trazas)
    escribir_diagramas(trazas, unico["eventos"], coordinado["eventos"])
    escribir_informe(salida / "evidencias" / "issue-02", unico, coordinado)
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
