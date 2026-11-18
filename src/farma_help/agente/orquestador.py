"""Coordinación de RAG, clasificador, controles y herramienta local."""

from __future__ import annotations

from typing import Any

from farma_help.agente.enrutador import (
    CLASIFICACION,
    CONSULTA,
    CREACION_TICKET,
    detectar_intencion,
)
from farma_help.agente.flujos import preparar_borrador_ticket
from farma_help.contratos import ResultadoAgente
from farma_help.rag.permisos import validar_rol
from controles.control_acceso import verificar_capacidad
from controles.control_confirmacion import validar_confirmacion_explicita
from controles.control_herramientas import validar_herramienta
from controles.control_salida_modelo import validar_borrador_ticket


class AgenteFarmaHelp:
    def __init__(self, rag: Any, clasificador: Any, ticket_store: Any, logger: Any):
        self.rag = rag
        self.clasificador = clasificador
        self.ticket_store = ticket_store
        self.logger = logger

    def procesar(
        self,
        consulta: str,
        rol: str = "operador",
        confirmacion: bool = False,
        prioridad: str = "P3",
    ) -> ResultadoAgente:
        validar_rol(rol)
        if not consulta or not consulta.strip():
            raise ValueError("La consulta debe contener texto.")

        intencion = detectar_intencion(consulta)
        verificar_capacidad(rol, intencion)
        self.logger.registrar("consulta_recibida", rol=rol, intencion=intencion)

        if intencion == CONSULTA:
            resultado = self.rag.consultar(consulta, rol=rol)
            respuesta = resultado.get("respuesta") or "Se recuperaron fuentes para la consulta."
            self.logger.registrar(
                "consulta_documental",
                rol=rol,
                fuentes=[fuente["fragmento_id"] for fuente in resultado["fuentes"]],
            )
            return ResultadoAgente(
                intencion=intencion,
                estado="completado",
                respuesta=respuesta,
                datos=resultado,
            )

        prediccion = self.clasificador.predecir(consulta)
        self.logger.registrar(
            "clasificacion_reclamo",
            rol=rol,
            categoria=prediccion.categoria,
            confianza=prediccion.confianza,
        )

        if intencion == CLASIFICACION:
            return ResultadoAgente(
                intencion=intencion,
                estado="completado",
                respuesta=f"Categoría propuesta: {prediccion.categoria}.",
                datos={"prediccion": prediccion},
            )

        borrador = preparar_borrador_ticket(consulta, prediccion, rol, prioridad)
        validar_borrador_ticket(borrador)
        self.logger.registrar(
            "borrador_ticket",
            rol=rol,
            categoria=borrador.categoria,
            prioridad=borrador.prioridad,
        )

        if not validar_confirmacion_explicita(confirmacion):
            return ResultadoAgente(
                intencion=CREACION_TICKET,
                estado="pendiente_confirmacion",
                respuesta="Se preparó un ticket. Se requiere confirmación explícita del operador.",
                datos={"borrador": borrador},
            )

        validar_herramienta("crear_ticket")
        ticket = self.ticket_store.crear_ticket(borrador)
        self.logger.registrar("ticket_creado", rol=rol, ticket_id=ticket["ticket_id"])
        return ResultadoAgente(
            intencion=CREACION_TICKET,
            estado="completado",
            respuesta=f"Ticket creado: {ticket['ticket_id']}.",
            datos={"ticket": ticket, "borrador": borrador},
        )
