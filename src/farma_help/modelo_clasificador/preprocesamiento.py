"""Carga y preparación de datos sintéticos del clasificador."""

from __future__ import annotations

import csv
import re
from pathlib import Path


def normalizar_texto(texto: str) -> str:
    return re.sub(r"\s+", " ", str(texto).strip().lower())


def cargar_datos(ruta: Path) -> tuple[list[str], list[str]]:
    textos: list[str] = []
    etiquetas: list[str] = []
    with Path(ruta).open(encoding="utf-8", newline="") as archivo:
        for fila in csv.DictReader(archivo):
            if not fila.get("texto") or not fila.get("categoria"):
                raise ValueError("Cada reclamo debe tener texto y categoria.")
            textos.append(normalizar_texto(fila["texto"]))
            etiquetas.append(normalizar_texto(fila["categoria"]))
    if not textos:
        raise ValueError("El archivo de reclamos no contiene datos.")
    return textos, etiquetas
