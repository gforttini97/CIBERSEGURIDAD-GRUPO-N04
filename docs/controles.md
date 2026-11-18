# Controles y riesgo residual

Los controles implementados se encuentran en la carpeta raíz `controles/` y
son utilizados por el orquestador en `src/farma_help/agente/`.

| Control | Archivo | Amenaza que reduce | Evidencia esperada |
|---|---|---|---|
| Control de acceso | `controles/control_acceso.py` | Elevación de privilegios y divulgación de información | Solicitud con rol no autorizado rechazada |
| Defensa contra inyección | `controles/control_inyeccion_prompt.py` | Manipulación del comportamiento del modelo | Documento tratado como dato, no como instrucción |
| Validación de salida | `controles/control_salida_modelo.py` | Manipulación y ejecución de acciones inválidas | Borrador con categoría o prioridad inválida rechazado |
| Confirmación explícita | `controles/control_confirmacion.py` | Creación no autorizada de tickets | Ticket no creado sin confirmación del operador |
| Lista de herramientas | `controles/control_herramientas.py` | Ejecución de herramientas no declaradas | Herramienta fuera de la lista permitida rechazada |

La evaluación final debe medir al menos tres amenazas prioritarias sin control y
con control, reportando tasa de éxito, intervalo de Wilson al 95%, falsos
positivos y un ejemplo concreto que el control deja pasar.
