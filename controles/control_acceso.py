"""Control de rol y capacidades permitidas."""

from __future__ import annotations

from farma_help.rag.permisos import validar_rol


CAPACIDADES_POR_ROL = {
    "contacto_cliente": {"consulta_politica", "clasificacion_reclamo"},
    "operador": {"consulta_politica", "clasificacion_reclamo", "creacion_ticket"},
    "supervisor_atencion": {"consulta_politica", "clasificacion_reclamo", "creacion_ticket"},
    "finanzas": {"consulta_politica", "clasificacion_reclamo"},
    "calidad": {"consulta_politica", "clasificacion_reclamo"},
    "administrador": {"consulta_politica", "clasificacion_reclamo", "creacion_ticket"},
}


def verificar_capacidad(rol: str, capacidad: str) -> None:
    validar_rol(rol)
    if capacidad not in CAPACIDADES_POR_ROL[rol]:
        raise PermissionError(f"El rol '{rol}' no puede ejecutar '{capacidad}'.")
