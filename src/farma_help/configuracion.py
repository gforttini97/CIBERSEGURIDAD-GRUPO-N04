"""Rutas y configuración compartida del prototipo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RutasProyecto:
    """Rutas de datos y salidas, todas relativas al repositorio."""

    raiz: Path
    politicas: Path
    reclamos: Path
    tickets: Path
    registros: Path

    @classmethod
    def desde_raiz(cls, raiz: Path) -> "RutasProyecto":
        raiz = Path(raiz).expanduser().resolve()
        return cls(
            raiz=raiz,
            politicas=raiz / "datos" / "politicas",
            reclamos=raiz / "datos" / "reclamos" / "reclamos_sinteticos.csv",
            tickets=raiz / "datos" / "tickets" / "tickets.json",
            registros=raiz / "registros" / "registro.jsonl",
        )

    def crear_directorios(self) -> None:
        """Crear solamente directorios de salida, nunca datos de entrada."""

        self.tickets.parent.mkdir(parents=True, exist_ok=True)
        self.registros.parent.mkdir(parents=True, exist_ok=True)


def encontrar_raiz(inicio: Path | None = None) -> Path:
    """Encontrar la raíz buscando la carpeta ``datos/politicas``."""

    punto = Path(inicio or Path.cwd()).expanduser().resolve()
    for candidato in (punto, *punto.parents):
        if (candidato / "datos" / "politicas").is_dir():
            return candidato
    raise FileNotFoundError(
        "No se encontró la raíz del proyecto. "
        "Ejecuta el notebook desde el repositorio o proporciona la ruta."
    )


def cargar_rutas(raiz: Path | None = None) -> RutasProyecto:
    """Construir la configuración de rutas del proyecto."""

    return RutasProyecto.desde_raiz(raiz or encontrar_raiz())
