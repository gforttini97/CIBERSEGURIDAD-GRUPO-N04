"""Fachada de alto nivel para construir y consultar el RAG."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .embeddings import cargar_modelo, generar_embeddings
from .fragmentacion import crear_chunks_rag, crear_fragmentos
from .indice import IndicesFAISS
from .ingesta import leer_politicas
from .recuperador import RecuperadorSemantico
from .reranking import reordenar


@dataclass
class ServicioRAG:
    recuperador: RecuperadorSemantico
    reranker: Any | None = None
    generador: Any | None = None

    @classmethod
    def construir(
        cls,
        carpeta_politicas: Path,
        modelo_embeddings: str = "intfloat/multilingual-e5-small",
        device: str = "cpu",
        usar_reranking: bool = False,
        reranker: Any | None = None,
        generador: Any | None = None,
    ) -> "ServicioRAG":
        documentos = leer_politicas(carpeta_politicas)
        fragmentos = crear_fragmentos(documentos)
        modelo = cargar_modelo(modelo_embeddings, device=device)
        tokenizador = modelo.tokenizer
        chunks = crear_chunks_rag(fragmentos, tokenizador, modelo.max_seq_length)
        embeddings = generar_embeddings(modelo, chunks)
        indices = IndicesFAISS.construir(embeddings, chunks)
        if usar_reranking and reranker is None:
            from .reranking import cargar_reranker

            reranker = cargar_reranker(device=device)
        return cls(
            recuperador=RecuperadorSemantico(
                modelo=modelo,
                tokenizador=tokenizador,
                indices=indices,
                limite_tokens=modelo.max_seq_length,
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
            candidatos = reordenar(self.reranker, pregunta, candidatos)
        return candidatos

    def consultar(
        self,
        pregunta: str,
        rol: str = "operador",
        top_k: int = 10,
        top_contexto: int = 3,
    ) -> dict[str, Any]:
        candidatos = self.recuperar(pregunta, rol=rol, top_k=top_k)
        fuentes = candidatos[:top_contexto]
        respuesta = self.generador.generar(pregunta, fuentes) if self.generador else None
        return {
            "respuesta": respuesta,
            "fuentes": fuentes,
            "candidatos": candidatos,
        }
