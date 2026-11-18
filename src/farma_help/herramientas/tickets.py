"""Persistencia local y acotada de tickets sintéticos."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from farma_help.contratos import BorradorTicket


class TicketStore:
    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)

    def _leer(self) -> list[dict[str, Any]]:
        if not self.ruta.exists():
            return []
        contenido = json.loads(self.ruta.read_text(encoding="utf-8"))
        if not isinstance(contenido, list):
            raise ValueError("El almacén de tickets debe contener una lista JSON.")
        return contenido

    def crear_ticket(self, borrador: BorradorTicket) -> dict[str, Any]:
        tickets = self._leer()
        ticket = {
            "ticket_id": f"TKT-{uuid4().hex[:8].upper()}",
            "categoria": borrador.categoria,
            "descripcion": borrador.descripcion,
            "prioridad": borrador.prioridad,
            "estado": "abierto",
            "creado_por": borrador.creado_por,
            "creado_en": datetime.now(timezone.utc).isoformat(),
        }
        tickets.append(ticket)
        self.ruta.write_text(
            json.dumps(tickets, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return ticket
