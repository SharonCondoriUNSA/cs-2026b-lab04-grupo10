"""Bucle del agente: pensar -> actuar -> observar (ReAct), modelado como máquina de estados.

Estados: DECIDIENDO -> VALIDANDO_CONTRATO -> EVALUANDO_POLITICA -> EJECUTANDO -> OBSERVANDO -> DECIDIENDO ...
Estados finales: FINALIZADO (respuesta final) o LIMITE_ALCANZADO (presupuesto de pasos agotado).
"""
import json
import time
from agente.contrato import validar_decision


class Agente:
    def __init__(self, nombre, modelo, herramientas, politica, objetivo, traza_archivo):
        self.nombre, self.modelo, self.h, self.politica = nombre, modelo, herramientas, politica
        self.historial = [{"role": "user", "content": objetivo}]       # memoria de corto plazo
        self.traza_archivo, self.eventos = traza_archivo, []

    def _registrar(self, **evento):
        evento["t"] = round(time.perf_counter() - self._t0, 3)
        evento["agente"] = self.nombre
        evento["contexto_caracteres"] = sum(len(m["content"]) for m in self.historial)
        self.eventos.append(evento)

    def ejecutar(self) -> str:
        self._t0 = time.perf_counter()
        self._registrar(tipo="objetivo", estado="INICIO", texto=self.historial[0]["content"])
        conocidas = set(self.h.catalogo())
        for paso in range(1, self.politica.max_pasos + 1):
            d = self.modelo.decidir(self.historial)                       # DECIDIENDO
            self.historial.append({"role": "assistant", "content": json.dumps(d, ensure_ascii=False)})
            ok, motivo = validar_decision(d, conocidas)                   # VALIDANDO_CONTRATO
            if not ok:
                obs = f"ERROR DE CONTRATO: {motivo}. Responda solo con el JSON del protocolo."
                self._registrar(tipo="accion", estado="CONTRATO_INVALIDO", paso=paso, pensamiento=str(d)[:200],
                                accion="(ninguna)", args={}, observacion=obs, bloqueada=True)
            elif "final" in d:
                self._registrar(tipo="final", estado="FINALIZADO", paso=paso, pensamiento=d["pensamiento"], texto=d["final"])
                break
            else:
                accion, args = d["accion"], d.get("args", {})
                veredicto = self.politica.evaluar(accion, args, paso)     # EVALUANDO_POLITICA
                if veredicto.permitido:
                    try:
                        obs = getattr(self.h, accion)(**args)             # EJECUTANDO
                    except Exception as e:                                # el error también es una observación
                        obs = f"ERROR: {type(e).__name__}: {e}"
                    self._registrar(tipo="accion", estado="OBSERVANDO", paso=paso, pensamiento=d["pensamiento"],
                                    accion=accion, args=args, observacion=obs, bloqueada=False)
                else:
                    obs = f"BLOQUEADO POR LA POLÍTICA: {veredicto.motivo}"
                    self._registrar(tipo="accion", estado="BLOQUEADO", paso=paso,
                                    pensamiento=d["pensamiento"], accion=accion, args=args, observacion=obs, bloqueada=True)
            self.historial.append({"role": "user", "content": f"Observación: {obs}"})   # OBSERVANDO -> DECIDIENDO
        else:
            self._registrar(tipo="limite", estado="LIMITE_ALCANZADO",
                            texto=f"Se alcanzó el máximo de {self.politica.max_pasos} decisiones")
        with open(self.traza_archivo, "w", encoding="utf-8") as f:
            for e in self.eventos:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        return self.eventos[-1].get("texto", "(sin respuesta final)")
