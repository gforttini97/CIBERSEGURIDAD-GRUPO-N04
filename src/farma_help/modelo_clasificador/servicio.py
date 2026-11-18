"""Fachada del clasificador de reclamos."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from farma_help.contratos import PrediccionReclamo

from .entrenamiento import entrenar
from .inferencia import predecir
from .preprocesamiento import cargar_datos


@dataclass
class ClasificadorReclamos:
    vectorizador: Any
    modelo: Any

    @classmethod
    def desde_csv(cls, ruta: Path) -> "ClasificadorReclamos":
        textos, etiquetas = cargar_datos(ruta)
        vectorizador, modelo = entrenar(textos, etiquetas)
        return cls(vectorizador=vectorizador, modelo=modelo)

    def predecir(self, texto: str) -> PrediccionReclamo:
        if not texto or not texto.strip():
            raise ValueError("El reclamo debe contener texto.")
        return predecir(self.vectorizador, self.modelo, texto)
