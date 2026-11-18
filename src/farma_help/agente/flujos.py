"""Construcción de propuestas de acción sin ejecutar herramientas."""

from __future__ import annotations

from farma_help.contratos import BorradorTicket, PrediccionReclamo


def preparar_borrador_ticket(
    descripcion: str,
    prediccion: PrediccionReclamo,
    rol: str,
    prioridad: str = "P3",
) -> BorradorTicket:
    return BorradorTicket(
        categoria=prediccion.categoria,
        descripcion=descripcion.strip(),
        prioridad=prioridad,
        creado_por=rol,
        metadatos={"confianza_clasificador": prediccion.confianza},
    )
