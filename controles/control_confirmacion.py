"""Control de confirmación explícita para acciones con efecto."""


def validar_confirmacion_explicita(confirmacion: bool) -> bool:
    """Aceptar únicamente un booleano verdadero externo al modelo."""

    return type(confirmacion) is bool and confirmacion is True
