"""Escritor JSONL para evidencias de seguridad y trazabilidad."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .eventos import EVENTOS


_SECRETO = re.compile(r"(?i)(api[_-]?key|token|secret)(\s*[=:]\s*)[^\s,;]+")


def _sanitizar(valor: Any) -> Any:
    if isinstance(valor, str):
        return _SECRETO.sub(r"\1\2[REDACTADO]", valor)
    if isinstance(valor, dict):
        return {clave: _sanitizar(item) for clave, item in valor.items()}
    if isinstance(valor, list):
        return [_sanitizar(item) for item in valor]
    return valor


class RegistroAuditoria:
    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)

    def registrar(self, evento: str, **datos: Any) -> dict[str, Any]:
        if evento not in EVENTOS:
            raise ValueError(f"Evento no definido: {evento}")
        registro = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "evento": evento,
            **_sanitizar(datos),
        }
        with self.ruta.open("a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
        return registro
