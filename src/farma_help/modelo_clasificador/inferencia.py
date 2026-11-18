"""Inferencia aislada del clasificador."""

from __future__ import annotations

from typing import Any

import numpy as np

from farma_help.contratos import PrediccionReclamo
from .preprocesamiento import normalizar_texto


def predecir(vectorizador: Any, modelo: Any, texto: str) -> PrediccionReclamo:
    matriz = vectorizador.transform([normalizar_texto(texto)])
    probabilidades = modelo.predict_proba(matriz)[0]
    posicion = int(np.argmax(probabilidades))
    return PrediccionReclamo(
        categoria=str(modelo.classes_[posicion]),
        confianza=float(probabilidades[posicion]),
    )
