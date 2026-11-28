"""Aprobación humana en consola para propuestas de edición del agente."""


def aprobar_edicion_en_consola(args: dict) -> bool:
    """Muestra la sustitución exacta y exige aprobación explícita en cada edición.

    Solo ``s`` y ``n`` son respuestas válidas. EOF o una interrupción deniega la
    edición para fallar de forma segura.
    """
    print("\n=== Solicitud de aprobación humana ===")
    print(f"Archivo: {args.get('ruta', '(sin ruta)')}")
    print("--- Texto que se reemplazará ---")
    print(args.get("antes", ""))
    print("--- Texto propuesto ---")
    print(args.get("despues", ""))
    try:
        while True:
            respuesta = input("¿Autoriza esta edición? [s/n]: ").strip().casefold()
            if respuesta in {"s", "n"}:
                return respuesta == "s"
            print("Respuesta inválida. Escriba únicamente s o n.")
    except (EOFError, KeyboardInterrupt):
        print("Aprobación no recibida; se deniega la edición.")
        return False
