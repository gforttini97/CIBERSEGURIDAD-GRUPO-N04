"""Reordenamiento opcional de candidatos recuperados."""

from __future__ import annotations

from typing import Any

import numpy as np


MODELO_RERANKING_POR_DEFECTO = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"


def cargar_reranker(nombre: str = MODELO_RERANKING_POR_DEFECTO, device: str = "cpu") -> Any:
    try:
        from sentence_transformers import CrossEncoder
    except ImportError as exc:
        raise RuntimeError("Instala sentence-transformers para usar reranking.") from exc
    return CrossEncoder(nombre, device=device, max_length=512)


def reordenar(reranker: Any, pregunta: str, candidatos: list[dict]) -> list[dict]:
    if not candidatos:
        return []
    pares = [[pregunta, candidato["texto"]] for candidato in candidatos]
    puntuaciones = np.asarray(
        reranker.predict(pares, show_progress_bar=False)
    ).reshape(-1)
    if len(puntuaciones) != len(candidatos) or not np.isfinite(puntuaciones).all():
        raise ValueError("Puntuaciones de reranking inválidas.")
    resultado = [
        {**candidato, "puntuacion_reranking": float(puntuacion)}
        for candidato, puntuacion in zip(candidatos, puntuaciones)
    ]
    return sorted(
        resultado,
        key=lambda fila: fila["puntuacion_reranking"],
        reverse=True,
    )
