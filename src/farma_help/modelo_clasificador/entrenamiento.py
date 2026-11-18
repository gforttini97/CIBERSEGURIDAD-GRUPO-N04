"""Entrenamiento reproducible del modelo clásico."""

from __future__ import annotations

from typing import Any


def entrenar(textos: list[str], etiquetas: list[str]) -> tuple[Any, Any]:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
    except ImportError as exc:
        raise RuntimeError("Instala scikit-learn para entrenar el clasificador.") from exc
    vectorizador = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    matriz = vectorizador.fit_transform(textos)
    modelo = LogisticRegression(max_iter=1000, random_state=42)
    modelo.fit(matriz, etiquetas)
    return vectorizador, modelo
