"""Lista permitida de herramientas del agente."""


HERRAMIENTAS_PERMITIDAS = {"crear_ticket"}


def validar_herramienta(nombre: str) -> None:
    if nombre not in HERRAMIENTAS_PERMITIDAS:
        raise PermissionError(f"Herramienta no autorizada: {nombre}")
