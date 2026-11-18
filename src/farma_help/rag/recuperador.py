"""Recuperación semántica con permisos aplicados antes de la búsqueda."""

from __future__ import annotations

from typing import Any

import numpy as np

from .indice import IndicesFAISS
from .permisos import acceso_para_rol, validar_rol, verificar_fragmento_autorizado


class RecuperadorSemantico:
    def __init__(
        self,
        modelo: Any,
        tokenizador: Any,
        indices: IndicesFAISS,
        limite_tokens: int,
    ):
        self.modelo = modelo
        self.tokenizador = tokenizador
        self.indices = indices
        self.limite_tokens = limite_tokens

    def recuperar(
        self,
        pregunta: str,
        rol: str = "operador",
        top_k: int = 5,
    ) -> list[dict]:
        validar_rol(rol)
        if not isinstance(pregunta, str) or not pregunta.strip():
            raise ValueError("La pregunta debe contener texto.")
        if type(top_k) is not int or top_k < 1:
            raise ValueError("top_k debe ser un entero positivo.")

        entrada = "query: " + pregunta.strip()
        cantidad_tokens = len(
            self.tokenizador(
                entrada,
                add_special_tokens=True,
                truncation=False,
            )["input_ids"]
        )
        if cantidad_tokens > self.limite_tokens:
            raise ValueError("La pregunta supera el límite del modelo.")

        acceso = acceso_para_rol(rol)
        indice = self.indices.indices[acceso]
        corpus = self.indices.chunks_por_acceso[acceso]
        vector = self.modelo.encode(
            [entrada],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        vector = np.ascontiguousarray(vector, dtype=np.float32)
        cantidad = min(top_k, indice.ntotal)
        puntuaciones, posiciones = indice.search(vector, cantidad)

        resultados = []
        for puntuacion, posicion in zip(puntuaciones[0], posiciones[0]):
            if posicion < 0:
                continue
            chunk = corpus[int(posicion)]
            verificar_fragmento_autorizado(rol, chunk)
            resultados.append({**chunk, "similitud": float(puntuacion)})
        return resultados
