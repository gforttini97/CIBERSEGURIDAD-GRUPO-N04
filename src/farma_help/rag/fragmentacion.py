"""Creación de fragmentos semánticos y ventanas compatibles con el modelo."""

from __future__ import annotations

import re
from typing import Any

from .ingesta import extraer_metadatos


def crear_fragmentos(documentos: dict[str, str]) -> list[dict[str, Any]]:
    """Convertir cada sección principal en un fragmento con trazabilidad."""

    resultado: list[dict[str, Any]] = []
    for nombre, texto in documentos.items():
        metadatos = extraer_metadatos(texto)
        encabezados = list(re.finditer(r"^##[ \t]+(.+)$", texto, re.MULTILINE))
        for indice, encabezado in enumerate(encabezados):
            titulo = encabezado.group(1).strip()
            numero = re.match(r"(\d+)\.", titulo)
            if not numero:
                raise ValueError(f"Sección sin número en {nombre}: {titulo}")
            inicio = encabezado.start()
            fin = encabezados[indice + 1].start() if indice + 1 < len(encabezados) else len(texto)
            clasificacion = metadatos["clasificacion"]
            if clasificacion == "mixto":
                if "[INTERNO]" in titulo:
                    clasificacion = "interno"
                elif "[PÚBLICO]" in titulo:
                    clasificacion = "publico"
                else:
                    raise ValueError(
                        f"La sección no tiene clasificación en {nombre}: {titulo}"
                    )
            if clasificacion not in {"publico", "interno"}:
                raise ValueError(f"Clasificación desconocida en {nombre}: {clasificacion}")
            fragmento_id = f"{metadatos['doc_id']}_v{metadatos['version']}_s{numero[1]}"
            resultado.append(
                {
                    "fragmento_id": fragmento_id,
                    "fragmento_padre": fragmento_id,
                    "archivo": nombre,
                    "doc_id": metadatos["doc_id"],
                    "version": metadatos["version"],
                    "vigencia": metadatos["vigencia"],
                    "seccion": numero[1],
                    "titulo": titulo,
                    "clasificacion": clasificacion,
                    "parte": 1,
                    "texto": texto[inicio:fin].strip(),
                }
            )
    ids = [fragmento["fragmento_id"] for fragmento in resultado]
    if len(ids) != len(set(ids)):
        raise ValueError("Se encontraron identificadores de fragmentos duplicados.")
    return resultado


def crear_chunks_rag(
    fragmentos: list[dict[str, Any]],
    tokenizador: Any,
    limite_tokens: int,
    tamano_ventana: int = 420,
    solapamiento: int = 60,
) -> list[dict[str, Any]]:
    """Subdividir fragmentos largos sin perder sus metadatos."""

    if solapamiento >= tamano_ventana:
        raise ValueError("El solapamiento debe ser menor que la ventana.")
    chunks: list[dict[str, Any]] = []
    for fragmento in fragmentos:
        texto = fragmento["texto"]
        entrada = tokenizador("passage: " + texto, add_special_tokens=True, truncation=False)
        cantidad = len(entrada["input_ids"])
        if cantidad <= limite_tokens:
            chunks.append({**fragmento, "tokens_entrada": cantidad})
            continue
        codificacion = tokenizador(
            texto,
            add_special_tokens=False,
            truncation=False,
            return_offsets_mapping=True,
        )
        posiciones = codificacion["offset_mapping"]
        inicio_token = 0
        parte = 1
        while inicio_token < len(posiciones):
            fin_token = min(inicio_token + tamano_ventana, len(posiciones))
            inicio_caracter = 0 if inicio_token == 0 else posiciones[inicio_token][0]
            fin_caracter = len(texto) if fin_token == len(posiciones) else posiciones[fin_token - 1][1]
            nuevo = {
                **fragmento,
                "fragmento_id": f"{fragmento['fragmento_id']}_p{parte}",
                "fragmento_padre": fragmento["fragmento_id"],
                "parte": parte,
                "texto": texto[inicio_caracter:fin_caracter],
            }
            nuevo["tokens_entrada"] = len(
                tokenizador(
                    "passage: " + nuevo["texto"],
                    add_special_tokens=True,
                    truncation=False,
                )["input_ids"]
            )
            if nuevo["tokens_entrada"] > limite_tokens:
                raise ValueError(f"El chunk aún excede el límite: {nuevo['fragmento_id']}")
            chunks.append(nuevo)
            if fin_token == len(posiciones):
                break
            inicio_token = fin_token - solapamiento
            parte += 1
    return chunks
