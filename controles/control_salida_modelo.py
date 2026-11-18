"""Validaciones de salidas antes de permitir efectos secundarios."""

from __future__ import annotations

from farma_help.contratos import BorradorTicket


CATEGORIAS_VALIDAS = {"entrega", "facturacion", "devolucion"}
PRIORIDADES_VALIDAS = {"P1", "P2", "P3"}


def validar_borrador_ticket(borrador: BorradorTicket) -> None:
    if borrador.categoria not in CATEGORIAS_VALIDAS:
        raise ValueError("La categoría del ticket no está permitida.")
    if borrador.prioridad not in PRIORIDADES_VALIDAS:
        raise ValueError("La prioridad del ticket no está permitida.")
    if not borrador.descripcion.strip():
        raise ValueError("El ticket debe tener una descripción.")
