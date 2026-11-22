"""Reordenamiento de candidatos recuperados con CrossEncoder."""

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
    """Reordenar candidatos usando únicamente pares pregunta-texto completos."""

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


def preparar_ventanas_reranking(
    pregunta: str,
    texto: str,
    tokenizador: Any,
    limite_tokens: int,
) -> list[str]:
    """Dividir un candidato en ventanas que, junto a la pregunta, caben en el reranker.

    La función garantiza que ningún par pregunta-ventana supere ``limite_tokens``,
    sin omitir contenido del texto original.
    """

    def longitud_par(fragmento: str) -> int:
        return len(
            tokenizador(
                pregunta,
                fragmento,
                add_special_tokens=True,
                truncation=False,
            )["input_ids"]
        )

    if longitud_par(texto) <= limite_tokens:
        return [texto]

    presupuesto = limite_tokens - longitud_par("")
    if presupuesto < 32:
        raise ValueError(
            "La pregunta es demasiado larga para el reranker. Por favor, acórtala."
        )

    codificacion = tokenizador(
        texto,
        add_special_tokens=False,
        truncation=False,
        return_offsets_mapping=True,
    )
    posiciones = codificacion["offset_mapping"]
    if not posiciones:
        raise ValueError("No se pudo dividir el texto recuperado.")

    ventanas: list[str] = []
    inicio = 0
    while inicio < len(posiciones):
        fin = min(inicio + min(350, presupuesto - 8), len(posiciones))
        while fin > inicio:
            desde = 0 if inicio == 0 else posiciones[inicio][0]
            hasta = len(texto) if fin == len(posiciones) else posiciones[fin - 1][1]
            ventana = texto[desde:hasta]
            if longitud_par(ventana) <= limite_tokens:
                break
            fin -= 1
        else:
            raise ValueError("No se pudo crear una ventana válida.")

        ventanas.append(ventana)
        if fin == len(posiciones):
            break

        solapamiento = min(50, (fin - inicio) // 4)
        inicio = fin - solapamiento

    return ventanas


def reordenar_con_ventanas(
    reranker: Any,
    pregunta: str,
    candidatos: list[dict],
) -> list[dict]:
    """Reordenar candidatos permitiendo ventanas para textos largos.

    Cada candidato recibe la mayor puntuación obtenida entre sus ventanas.
    """

    if not candidatos:
        return []

    tokenizador = reranker.tokenizer
    limite_tokens = getattr(reranker, "max_length", 512)

    pares: list[list[str]] = []
    candidato_por_par: list[int] = []

    for indice, chunk in enumerate(candidatos):
        ventanas = preparar_ventanas_reranking(
            pregunta,
            chunk["texto"],
            tokenizador,
            limite_tokens,
        )
        for ventana in ventanas:
            pares.append([pregunta, ventana])
            candidato_por_par.append(indice)

    puntuaciones = np.asarray(
        reranker.predict(pares, batch_size=4, show_progress_bar=False)
    ).reshape(-1)

    if len(puntuaciones) != len(pares) or not np.isfinite(puntuaciones).all():
        raise ValueError("Puntuaciones de reranking inválidas.")

    mejores_puntuaciones = [float("-inf") for _ in candidatos]
    for indice, puntuacion in zip(candidato_por_par, puntuaciones):
        mejores_puntuaciones[indice] = max(
            mejores_puntuaciones[indice],
            float(puntuacion),
        )

    orden = sorted(
        range(len(candidatos)),
        key=lambda i: mejores_puntuaciones[i],
        reverse=True,
    )

    return [
        {
            **candidatos[i],
            "puntuacion_reranking": mejores_puntuaciones[i],
            "posicion_faiss": i + 1,
        }
        for i in orden
    ]
