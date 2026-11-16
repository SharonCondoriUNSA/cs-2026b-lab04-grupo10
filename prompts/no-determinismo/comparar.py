"""Compara nueve respuestas nuevas sin alterarlas ni consultar modelos."""
from hashlib import sha256
import json
from pathlib import Path
import argparse
import re

from jsonschema import Draft7Validator

BASE = Path(__file__).resolve().parent


def decodificar_transporte(texto):
    """Retira solo escapes de presentación del chat, nunca corrige el JSON."""
    texto = texto.replace("\\\r\n", "\r\n").replace("\\\n", "\n")
    return re.sub(r"(?m)^(?:&#x20;[ ]*)+", lambda m: m.group().replace("&#x20;", " "), texto)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verificar", action="store_true")
    args = parser.parse_args()
    metadatos = json.loads((BASE / "metadatos.json").read_text(encoding="utf-8"))
    nombres = [f"{caso}-{i}.txt" for caso in ("H1", "H7", "H8") for i in (1, 2, 3)]
    faltantes = [n for n in nombres if not (BASE / "grabaciones" / n).is_file()]
    if faltantes:
        raise SystemExit("Experimento pendiente. Faltan respuestas: " + ", ".join(faltantes))
    if not metadatos.get("modelo") or not metadatos.get("fecha"):
        raise SystemExit("Completa el modelo visible y la fecha en metadatos.json")
    esquema = json.loads((BASE.parent / "criterios/esquema.json").read_text(encoding="utf-8"))
    validador = Draft7Validator(esquema)
    resumen = []
    for caso in ("H1", "H7", "H8"):
        entrada = (BASE / "entradas" / f"{caso}.txt").read_bytes()
        if sha256(entrada).hexdigest() != metadatos["huellas_entradas"][caso]:
            raise SystemExit(f"La entrada {caso} cambio, revisa el experimento antes de comparar")
        respuestas = []
        for i in (1, 2, 3):
            archivo = BASE / "grabaciones" / f"{caso}-{i}.txt"
            bruto = archivo.read_bytes()
            texto = bruto.decode("utf-8")
            try:
                resultado = json.loads(decodificar_transporte(texto))
                canonico = json.dumps(resultado, sort_keys=True, ensure_ascii=False)
                valido = validador.is_valid(resultado)
                identidad = isinstance(resultado, dict) and resultado.get("historia_id") == caso
            except (ValueError, RecursionError):
                canonico, valido, identidad = texto, False, False
                resultado = {}
            respuestas.append({"archivo": archivo.name, "sha256": sha256(bruto).hexdigest(),
                               "json_normalizado_sha256": sha256(canonico.encode()).hexdigest(),
                               "esquema_valido": valido, "identificador_correcto": identidad,
                               "invest_ok": resultado.get("invest_ok") if isinstance(resultado, dict) else None,
                               "coincide_invest_esperado": valido and resultado.get("invest_ok") == (caso != "H7")})
        resumen.append({"caso": caso, "variantes_textuales": len({r["sha256"] for r in respuestas}),
                        "variantes_json": len({r["json_normalizado_sha256"] for r in respuestas}),
                        "respuestas": respuestas})
    salida = BASE / "comparacion.json"
    reporte = {"metadatos": metadatos, "resultados": resumen}
    if args.verificar:
        if not salida.exists() or json.loads(salida.read_text(encoding="utf-8")) != reporte:
            raise SystemExit("La comparación no corresponde a los originales y metadatos actuales")
        print("Comparación verificada: nueve respuestas conservadas")
        return
    if salida.exists():
        raise SystemExit("comparacion.json ya existe. Conserva el resultado anterior antes de repetir")
    salida.write_text(json.dumps(reporte,
                                ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(salida)


if __name__ == "__main__":
    main()
