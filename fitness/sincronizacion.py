"""Experimento E4: almacenamiento SQLite como sustituto local de IndexedDB.

No es la PWA ni PostgreSQL. Simula red caída y ACK perdido con reloj virtual,
pero ejecuta las transacciones e idempotencia contra archivos temporales reales.
Ejecutar: python -m fitness.sincronizacion
"""
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory


def conectar(ruta):
    conexion = sqlite3.connect(ruta)
    conexion.execute("PRAGMA synchronous = FULL")
    conexion.execute("CREATE TABLE IF NOT EXISTS registros ("
                     "distrito TEXT, identificador TEXT, payload TEXT NOT NULL, "
                     "PRIMARY KEY (distrito, identificador))")
    return conexion


def recibir(servidor, distrito, identificador, payload):
    """Un reintento idéntico es idempotente, un ID con otro contenido se rechaza."""
    with servidor:
        anterior = servidor.execute(
            "SELECT payload FROM registros WHERE distrito=? AND identificador=?",
            (distrito, identificador)).fetchone()
        if anterior is not None and anterior[0] != payload:
            raise ValueError("Identificador reutilizado con otro contenido")
        servidor.execute("INSERT OR IGNORE INTO registros VALUES (?, ?, ?)",
                         (distrito, identificador, payload))


def experimentar(total=120, servicio_s=0.1):
    if total <= 0 or servicio_s <= 0:
        raise ValueError("Parametros positivos requeridos")
    with TemporaryDirectory(prefix="ecorecicla-sync-") as temporal:
        local_path = Path(temporal) / "local.sqlite"
        servidor_path = Path(temporal) / "servidor.sqlite"
        local = conectar(local_path)
        # Lote al final de 20 min offline, todo queda confirmado localmente.
        with local:
            local.executemany("INSERT INTO registros VALUES (?, ?, ?)",
                              [("D01", f"R{i:03}", f"pesaje:{i}") for i in range(total)])
        local.close()
        # Reabrir archivos verifica persistencia tras cierre normal, no corte eléctrico.
        local = conectar(local_path)
        servidor = conectar(servidor_path)
        conservados = local.execute("SELECT count(*) FROM registros").fetchone()[0]
        tiempo = 0.0
        llamadas = ack_perdidos = 0
        for i, (distrito, identificador, payload) in enumerate(
                local.execute("SELECT * FROM registros ORDER BY identificador").fetchall()):
            recibir(servidor, distrito, identificador, payload)
            tiempo += servicio_s
            llamadas += 1
            if i % 10 == 0:
                ack_perdidos += 1
                # El servidor confirma, el ACK no llega. Se reabre y reintenta.
                servidor.close()
                servidor = conectar(servidor_path)
                recibir(servidor, distrito, identificador, payload)
                tiempo += servicio_s
                llamadas += 1
            with local:
                local.execute("DELETE FROM registros WHERE distrito=? AND identificador=?",
                              (distrito, identificador))
        efectos = servidor.execute("SELECT count(*) FROM registros").fetchone()[0]
        pendientes = local.execute("SELECT count(*) FROM registros").fetchone()[0]
        conflicto_rechazado = False
        try:
            recibir(servidor, "D01", "R000", "otro-contenido")
        except ValueError:
            conflicto_rechazado = True
        local.close()
        servidor.close()
        assert conservados == total and efectos == total and pendientes == 0
        assert conflicto_rechazado
        return {"offline_minutos": 20, "total": total,
                "antes_sin_buffer_perdidos": total,
                "conservados_tras_reapertura": conservados,
                "efectos_unicos": efectos, "perdidos": total - efectos,
                "duplicados": max(0, efectos - total), "pendientes": pendientes,
                "ack_perdidos_inyectados": ack_perdidos, "llamadas": llamadas,
                "servicio_s_supuesto": servicio_s,
                "sincronizacion_s_modelada": round(tiempo, 3),
                "cumple_30_s_en_modelo": tiempo <= 30,
                "conflicto_de_contenido_rechazado": conflicto_rechazado}


if __name__ == "__main__":
    print(json.dumps({"base": experimentar(),
                      "sensibilidad_servicio_lento": experimentar(servicio_s=0.25)}, indent=2))
