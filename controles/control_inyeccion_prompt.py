"""Detección básica y tratamiento de documentos como datos."""

from __future__ import annotations

import re


PATRONES_SOSPECHOSOS = (
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignora\s+(todas\s+)?las\s+instrucciones",
    r"system\s+prompt",
    r"revela\s+(la|el)\s+.*(clave|secreto|prompt)",
)


def contiene_inyeccion(texto: str) -> bool:
    return any(
        re.search(patron, texto, flags=re.IGNORECASE)
        for patron in PATRONES_SOSPECHOSOS
    )


def envolver_como_datos(texto: str) -> str:
    """Marcar contenido documental como evidencia, no como instrucciones."""

    return "<documento_dato>\n" + texto + "\n</documento_dato>"
