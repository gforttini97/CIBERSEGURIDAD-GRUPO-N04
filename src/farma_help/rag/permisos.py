"""Política de acceso al corpus documental."""

ROLES_VALIDOS = {
    "contacto_cliente",
    "operador",
    "supervisor_atencion",
    "finanzas",
    "calidad",
    "administrador",
}

ROLES_CON_ACCESO_INTERNO = {
    "supervisor_atencion",
    "finanzas",
}


def validar_rol(rol: str) -> str:
    if rol not in ROLES_VALIDOS:
        raise ValueError(f"Rol no reconocido: {rol}")
    return rol


def acceso_para_rol(rol: str) -> str:
    validar_rol(rol)
    return "interno" if rol in ROLES_CON_ACCESO_INTERNO else "publico"


def obtener_fragmentos_permitidos(rol: str, fragmentos: list[dict]) -> list[dict]:
    """Filtrar antes de recuperar; la consulta no puede cambiar el rol."""

    validar_rol(rol)
    return [
        fragmento
        for fragmento in fragmentos
        if fragmento["clasificacion"] == "publico"
        or (
            fragmento["clasificacion"] == "interno"
            and rol in ROLES_CON_ACCESO_INTERNO
        )
    ]


def verificar_fragmento_autorizado(rol: str, fragmento: dict) -> None:
    validar_rol(rol)
    if fragmento.get("clasificacion") == "interno" and rol not in ROLES_CON_ACCESO_INTERNO:
        raise PermissionError("El fragmento no está autorizado para este rol.")
