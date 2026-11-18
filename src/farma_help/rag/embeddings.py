"""Carga del modelo de embeddings y codificación del corpus."""

from __future__ import annotations

from typing import Any


MODELO_EMBEDDINGS_POR_DEFECTO = "intfloat/multilingual-e5-small"


def cargar_modelo(nombre: str = MODELO_EMBEDDINGS_POR_DEFECTO, device: str = "cpu") -> Any:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "Instala sentence-transformers para construir el índice RAG."
        ) from exc
    return SentenceTransformer(nombre, device=device)


def generar_embeddings(modelo: Any, chunks: list[dict]) -> Any:
    textos = ["passage: " + chunk["texto"] for chunk in chunks]
    return modelo.encode(
        textos,
        batch_size=8,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
