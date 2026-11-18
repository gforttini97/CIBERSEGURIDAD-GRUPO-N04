"""Tipos compartidos entre las capacidades del sistema."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PrediccionReclamo:
    categoria: str
    confianza: float


@dataclass(frozen=True)
class BorradorTicket:
    categoria: str
    descripcion: str
    prioridad: str = "P3"
    creado_por: str = ""
    metadatos: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResultadoAgente:
    intencion: str
    estado: str
    respuesta: str
    datos: dict[str, Any] = field(default_factory=dict)
