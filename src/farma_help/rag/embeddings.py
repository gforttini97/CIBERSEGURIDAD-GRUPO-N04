"""Generación de embeddings mediante la API de Gemini."""

from __future__ import annotations

from typing import Any

import numpy as np


MODELO_EMBEDDINGS_POR_DEFECTO = "gemini-embedding-001"
DIMENSION_EMBEDDINGS_POR_DEFECTO = 768


def _normalizar_nombre_modelo(nombre: str) -> str:
    """Garantizar la forma ``models/...`` que espera la API de Gemini."""

    nombre = nombre.strip()
    if not nombre.startswith("models/"):
        return f"models/{nombre}"
    return nombre


class GeneradorEmbeddingsGemini:
    """Adaptador de embeddings usando ``google-genai``.

    Los vectores se normalizan antes de devolverse para que FAISS pueda
    usar ``IndexFlatIP`` como aproximador de la similitud coseno.
    """

    def __init__(
        self,
        cliente: Any,
        modelo: str = MODELO_EMBEDDINGS_POR_DEFECTO,
        dimension: int = DIMENSION_EMBEDDINGS_POR_DEFECTO,
        tamano_lote: int = 32,
    ):
        self.cliente = cliente
        self.modelo = _normalizar_nombre_modelo(modelo)
        self.dimension = dimension
        self.tamano_lote = tamano_lote

    @classmethod
    def desde_api_key(
        cls,
        api_key: str,
        modelo: str = MODELO_EMBEDDINGS_POR_DEFECTO,
        dimension: int = DIMENSION_EMBEDDINGS_POR_DEFECTO,
        tamano_lote: int = 32,
    ) -> "GeneradorEmbeddingsGemini":
        if not api_key:
            raise ValueError("Se requiere una API key para generar embeddings.")
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "Instala google-genai para usar embeddings de Gemini."
            ) from exc
        return cls(genai.Client(api_key=api_key), modelo, dimension, tamano_lote)

    def _extraer_vectores(self, respuesta: Any) -> np.ndarray:
        """Convertir la respuesta de la API en una matriz float32."""

        embeddings = getattr(respuesta, "embeddings", respuesta)
        if embeddings is None:
            raise RuntimeError("La respuesta de embeddings está vacía.")

        vectores: list[np.ndarray] = []
        for emb in embeddings:
            valores = getattr(emb, "values", None)
            if valores is not None:
                vector = np.asarray(valores, dtype=np.float32)
            else:
                vector = np.asarray(emb, dtype=np.float32)
            if vector.ndim != 1:
                raise ValueError(f"Embedding con forma inesperada: {vector.shape}")
            vectores.append(vector)

        return np.vstack(vectores).astype(np.float32)

    def _normalizar(self, matriz: np.ndarray) -> np.ndarray:
        normas = np.linalg.norm(matriz, axis=1, keepdims=True)
        normas = np.where(normas == 0, 1.0, normas)
        return (matriz / normas).astype(np.float32)

    def _embed(self, textos: list[str], task_type: str) -> np.ndarray:
        try:
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError("Instala google-genai para usar embeddings de Gemini.") from exc

        # Procesar por lotes pequeños para respetar los límites de la API gratuita.
        lotes = [
            textos[i : i + self.tamano_lote]
            for i in range(0, len(textos), self.tamano_lote)
        ]
        vectores_lotes: list[np.ndarray] = []

        for lote in lotes:
            respuesta = self.cliente.models.embed_content(
                model=self.modelo,
                contents=lote,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=self.dimension,
                ),
            )
            vectores_lotes.append(self._extraer_vectores(respuesta))

        vectores = np.vstack(vectores_lotes)

        if vectores.shape[0] != len(textos):
            raise ValueError(
                f"La cantidad de vectores ({vectores.shape[0]}) no coincide "
                f"con la cantidad de textos ({len(textos)})."
            )
        if not np.isfinite(vectores).all():
            raise ValueError("Se encontraron valores numéricos inválidos en los embeddings.")

        return self._normalizar(vectores)

    def codificar_documentos(self, textos: list[str]) -> np.ndarray:
        """Generar embeddings para el corpus indexado."""

        return self._embed(textos, "RETRIEVAL_DOCUMENT")

    def codificar_consultas(self, textos: list[str]) -> np.ndarray:
        """Generar embeddings para una o más preguntas."""

        return self._embed(textos, "RETRIEVAL_QUERY")
