"""Lectura, normalización y metadatos del corpus documental."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable


ARCHIVOS_POLITICAS = (
    "POL-REC-001.md",
    "POL-INT-002.md",
    "POL-TKT-003.md",
)


def _cabecera(texto: str) -> re.Match[str] | None:
    return re.match(r"\A---\s*\n(.*?)\n---[ \t]*(?:\n|$)", texto, re.DOTALL)


def extraer_metadatos(texto: str) -> dict[str, str]:
    """Extraer los metadatos YAML simples de las políticas del curso."""

    cabecera = _cabecera(texto)
    if not cabecera:
        raise ValueError("El documento no tiene una cabecera válida.")
    metadatos: dict[str, str] = {}
    for linea in cabecera[1].splitlines():
        clave, separador, valor = linea.partition(":")
        if separador:
            clave = clave.strip()
            if clave in metadatos:
                raise ValueError(f"Metadato duplicado: {clave}")
            metadatos[clave] = valor.strip().strip("\"'")
    return metadatos


def normalizar_politica(nombre: str, texto: str) -> str:
    """Normalizar defectos conocidos sin modificar el archivo original."""

    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = re.sub(r"^(#{2,6}[ \t]+\d+)\\\.", r"\1.", texto, flags=re.MULTILINE)
    for marca in ("PÚBLICO", "INTERNO"):
        texto = texto.replace(rf"\[{marca}\]", f"[{marca}]")

    if nombre == "POL-REC-001.md":
        patron = (
            r"\A---\s*\n\s*##[ \t]+doc\\?_id:[ \t]*(POL-REC-001)"
            r"[ \t]+version:[ \t]*\"([^\"\n]+)\""
            r"[ \t]+clasificacion:[ \t]*(publico)"
            r"[ \t]+vigencia:[ \t]*(\d{4}-\d{2}-\d{2})[ \t]*(?:\n|$)"
        )

        def reconstruir(match: re.Match[str]) -> str:
            return (
                "---\n"
                f"doc_id: {match[1]}\n"
                f"version: \"{match[2]}\"\n"
                f"clasificacion: {match[3]}\n"
                f"vigencia: {match[4]}\n"
                "---\n"
            )

        texto = re.sub(patron, reconstruir, texto)

    if not _cabecera(texto):
        raise ValueError(f"Cabecera inválida en {nombre}.")
    metadatos = extraer_metadatos(texto)
    for campo in ("doc_id", "version", "clasificacion", "vigencia"):
        if not metadatos.get(campo):
            raise ValueError(f"Falta '{campo}' en {nombre}.")
    if metadatos["doc_id"] != Path(nombre).stem:
        raise ValueError(f"El doc_id no coincide con el archivo: {nombre}.")
    return texto


def leer_politicas(
    carpeta: Path,
    nombres: Iterable[str] = ARCHIVOS_POLITICAS,
) -> dict[str, str]:
    """Leer y validar el corpus permitido para el prototipo."""

    carpeta = Path(carpeta)
    documentos: dict[str, str] = {}
    for nombre in nombres:
        archivo = carpeta / nombre
        if not archivo.is_file():
            raise FileNotFoundError(f"No se encuentra la política: {archivo}")
        texto_original = archivo.read_text(encoding="utf-8-sig")
        if not texto_original.strip():
            raise ValueError(f"La política está vacía: {nombre}")
        documentos[nombre] = normalizar_politica(nombre, texto_original)
    return documentos
