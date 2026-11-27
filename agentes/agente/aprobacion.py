"""Aprobación humana en consola para propuestas de edición del agente."""


def aprobar_edicion_en_consola(args: dict) -> bool:
    """Muestra la sustitución exacta y exige aprobación explícita en cada edición.

    La respuesta afirmativa es ``s``, ``si`` o ``sí``. Cualquier otra respuesta,
    incluida EOF, deniega la edición para fallar de forma segura.
    """
    print("\n=== Solicitud de aprobación humana ===")
    print(f"Archivo: {args.get('ruta', '(sin ruta)')}")
    print("--- Texto que se reemplazará ---")
    print(args.get("antes", ""))
    print("--- Texto propuesto ---")
    print(args.get("despues", ""))
    try:
        respuesta = input("¿Autoriza esta edición? [s/N]: ").strip().casefold()
    except (EOFError, KeyboardInterrupt):
        print("Aprobación no recibida; se deniega la edición.")
        return False
    return respuesta in {"s", "si", "sí"}
