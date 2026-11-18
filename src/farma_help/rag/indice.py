"""Índices vectoriales separados por nivel de acceso."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class IndicesFAISS:
    indices: dict[str, Any]
    chunks_por_acceso: dict[str, list[dict]]

    @classmethod
    def construir(cls, embeddings: Any, chunks: list[dict]) -> "IndicesFAISS":
        try:
            import faiss
        except ImportError as exc:
            raise RuntimeError("Instala faiss-cpu para construir el índice RAG.") from exc

        posiciones = {
            "publico": [
                i for i, chunk in enumerate(chunks)
                if chunk["clasificacion"] == "publico"
            ],
            "interno": list(range(len(chunks))),
        }
        indices: dict[str, Any] = {}
        chunks_por_acceso: dict[str, list[dict]] = {}
        for acceso, posiciones_acceso in posiciones.items():
            vectores = np.ascontiguousarray(embeddings[posiciones_acceso], dtype=np.float32)
            indice = faiss.IndexFlatIP(vectores.shape[1])
            indice.add(vectores)
            indices[acceso] = indice
            chunks_por_acceso[acceso] = [chunks[i] for i in posiciones_acceso]
        return cls(indices=indices, chunks_por_acceso=chunks_por_acceso)
