"""Enrutamiento conservador de solicitudes."""

from __future__ import annotations


CONSULTA = "consulta_politica"
CLASIFICACION = "clasificacion_reclamo"
CREACION_TICKET = "creacion_ticket"


def detectar_intencion(texto: str) -> str:
    texto = texto.lower()
    if any(
        palabra in texto
        for palabra in ("crear ticket", "registrar ticket", "abrir ticket")
    ):
        return CREACION_TICKET
    if any(
        palabra in texto
        for palabra in ("clasificar", "categoría", "categoria", "reclamo")
    ):
        return CLASIFICACION
    return CONSULTA
