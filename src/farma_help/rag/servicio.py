"""Fachada de alto nivel para construir y consultar el RAG."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .embeddings import (
    DIMENSION_EMBEDDINGS_POR_DEFECTO,
    MODELO_EMBEDDINGS_POR_DEFECTO,
    GeneradorEmbeddingsGemini,
)
from .fragmentacion import crear_chunks_rag, crear_fragmentos
from .generacion import GeneradorGemini
from .indice import IndicesFAISS
from .ingesta import leer_politicas
from .recuperador import RecuperadorSemantico
from .reranking import cargar_reranker, reordenar_con_ventanas


LIMITE_TOKENS_RERANKER = 512
TAMANO_VENTANA = 420
SOLAPAMIENTO = 60


@dataclass
class ServicioRAG:
    recuperador: RecuperadorSemantico
    reranker: Any | None = None
    generador: GeneradorGemini | None = None

    @classmethod
    def construir(
        cls,
        carpeta_politicas: Path,
        api_key: str,
        modelo_llm: str,
        modelo_embeddings: str = MODELO_EMBEDDINGS_POR_DEFECTO,
        dimension_embeddings: int = DIMENSION_EMBEDDINGS_POR_DEFECTO,
        device: str = "cpu",
        usar_reranking: bool = True,
        reranker: Any | None = None,
        generador: GeneradorGemini | None = None,
    ) -> "ServicioRAG":
        """Construir el servicio RAG completo a partir de la carpeta de políticas."""

        documentos = leer_politicas(carpeta_politicas)
        fragmentos = crear_fragmentos(documentos)

        if usar_reranking and reranker is None:
            reranker = cargar_reranker(device=device)

        if reranker is not None:
            tokenizador = reranker.tokenizer
            chunks = crear_chunks_rag(
                fragmentos,
                tokenizador,
                LIMITE_TOKENS_RERANKER,
                tamano_ventana=TAMANO_VENTANA,
                solapamiento=SOLAPAMIENTO,
                prefijo="",
            )
        else:
            chunks = [
                {**fragmento, "fragmento_padre": fragmento["fragmento_id"], "parte": 1}
                for fragmento in fragmentos
            ]

        generador_embeddings = GeneradorEmbeddingsGemini.desde_api_key(
            api_key,
            modelo=modelo_embeddings,
            dimension=dimension_embeddings,
        )
        embeddings = generador_embeddings.codificar_documentos(
            [chunk["texto"] for chunk in chunks]
        )
        indices = IndicesFAISS.construir(embeddings, chunks)

        if generador is None:
            generador = GeneradorGemini.desde_api_key(api_key, modelo_llm)

        return cls(
            recuperador=RecuperadorSemantico(
                generador=generador_embeddings,
                indices=indices,
            ),
            reranker=reranker,
            generador=generador,
        )

    def recuperar(
        self,
        pregunta: str,
        rol: str = "operador",
        top_k: int = 10,
    ) -> list[dict]:
        candidatos = self.recuperador.recuperar(pregunta, rol=rol, top_k=top_k)
        if self.reranker is not None:
            candidatos = reordenar_con_ventanas(self.reranker, pregunta, candidatos)
        return candidatos

    def consultar(
        self,
        pregunta: str,
        rol: str = "operador",
        top_k: int = 10,
        top_contexto: int = 3,
    ) -> dict[str, Any]:
        candidatos = self.recuperar(pregunta, rol=rol, top_k=top_k)

        if not candidatos:
            return {
                "respuesta": "Información insuficiente: no se recuperaron documentos.",
                "fuentes": [],
                "candidatos": [],
            }

        fuentes = candidatos[:top_contexto]
        respuesta = (
            self.generador.generar(pregunta, fuentes)
            if self.generador is not None
            else None
        )
        return {
            "respuesta": respuesta,
            "fuentes": fuentes,
            "candidatos": candidatos,
        }
