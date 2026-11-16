"""El workflow no debe confundir una base fallida con un error de evaluación."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("evaluar_prompts", Path(__file__).resolve().parents[1] / "scripts/evaluar_prompts.py")
evaluador = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluador)


def reporte(aprobados=8, total=8, errores=0):
    return {"results": {"stats": {"successes": aprobados, "failures": total - aprobados, "errors": errores},
                        "results": [{"gradingResult": {"pass": i < aprobados}} for i in range(total)]}}


class EvaluacionTests(unittest.TestCase):
    def test_acepta_version_final_aprobada(self):
        self.assertEqual(evaluador.validar_reporte(reporte(), 0, 8, 8)["tasa"], 100)

    def test_acepta_base_con_fallos_esperados_y_codigo_100(self):
        self.assertEqual(evaluador.validar_reporte(reporte(0), 100, 8, 0)["aprobados"], 0)

    def test_rechaza_regresion_aunque_la_cli_no_tenga_errores(self):
        with self.assertRaises(ValueError):
            evaluador.validar_reporte(reporte(7), 100, 8, 8)

    def test_rechaza_errores_de_proveedor_y_salida_inesperada(self):
        for datos,codigo in ((reporte(errores=1), 0), (reporte(), 1)):
            with self.subTest(codigo=codigo), self.assertRaises(ValueError):
                evaluador.validar_reporte(datos, codigo, 8, 8)

    def test_rechaza_reportes_incompletos(self):
        datos = reporte()
        datos["results"]["results"].pop()
        with self.assertRaises(ValueError):
            evaluador.validar_reporte(datos, 0, 8, 8)
        datos = deepcopy(reporte())
        datos["results"]["results"][0]["gradingResult"] = None
        with self.assertRaises(ValueError):
            evaluador.validar_reporte(datos, 0, 8, 8)

    def test_rechaza_codigo_cero_si_hubo_fallos_y_viceversa(self):
        for datos,codigo,esperados in ((reporte(0), 0, 0), (reporte(), 100, 8)):
            with self.subTest(codigo=codigo), self.assertRaises(ValueError):
                evaluador.validar_reporte(datos, codigo, 8, esperados)


if __name__ == "__main__":
    unittest.main()
