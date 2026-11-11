# Farma Help — Política de privacidad y protección de datos

**Código:** POL-PRIV-001  
**Versión:** 1.0  
**Vigencia de la simulación:** 5 de noviembre de 2026  
**Entidad ficticia:** Distribuidora Farma Horizonte  
**Responsable:** Oficial de Privacidad ficticio  
**Aprobador ficticio:** Gerencia de Operaciones

> Documento íntegramente ficticio para el proyecto académico Farma Help. Los nombres, canales, plazos y condiciones son inventados; no constituye una política de privacidad real ni normativa peruana vigente. Todos los datos personales mencionados en el prototipo deben ser sintéticos.

## 1\. Objetivo y alcance

Esta política describe, dentro de la simulación, cómo Distribuidora Farma Horizonte trata los datos personales que ingresan al asistente de atención al cliente Farma Help: consultas, reclamos, tickets y registros de eventos. Busca que el prototipo maneje datos mínimos, con finalidades declaradas y plazos de conservación definidos.

Aplica a los datos sintéticos registrados por el portal Farma Help, el correo ficticio `privacidad@farmahorizonte.example` y el teléfono ficticio `TEL-DEMO-001`. No aplica a sistemas ajenos al prototipo ni a datos reales de personas: el ingreso de datos reales está prohibido por las reglas del proyecto.

## 2\. Principios de la simulación

* **Datos sintéticos únicamente:** ningún flujo del prototipo debe contener nombres, documentos de identidad, teléfonos, correos ni direcciones de personas reales.
* **Minimización:** solo se solicita la información necesaria para atender la consulta o el reclamo (código de cliente ficticio, número de pedido sintético, descripción del caso).
* **Finalidad:** los datos se usan solo para atender el caso que los originó y para la evaluación académica del prototipo.
* **Trazabilidad:** toda consulta y todo ticket queda en el registro de eventos con fecha, usuario y resultado.
* **No reidentificación:** está prohibido intentar vincular datos sintéticos con personas reales.

## 3\. Datos que se tratan

| Categoría | Ejemplos sintéticos | Finalidad |
|---|---|---|
| Identificación del contacto | Código de cliente `CLI-0000`, nombre ficticio del establecimiento | Atender y dar seguimiento al caso |
| Datos de la operación | Número de pedido `PED-0000`, lote, comprobante ficticio | Evaluar reclamos y devoluciones |
| Contenido del caso | Descripción del problema, evidencia declarada | Clasificar y resolver el ticket |
| Registro técnico | Marca de tiempo, tipo de evento, modelo usado | Auditoría y métricas del prototipo |

El asistente no solicita ni almacena datos de salud de pacientes. Si un usuario ingresa datos clínicos o de terceros, el caso se registra como fuera de alcance y se deriva conforme a la política de reclamos (POL-REC-001).

## 4\. Conservación

Los registros de eventos y tickets sintéticos se conservan durante el ciclo académico de la simulación y se eliminan al cierre del proyecto. Ningún dato se conserva "por si acaso": cada categoría tiene una finalidad declarada en la sección 3 y desaparece con ella.

Las muestras de corridas que se publiquen en el repositorio deben contener exclusivamente datos sintéticos y ser revisadas antes de versionarse.

## 5\. Derechos de los titulares (simulados)

Dentro de la ficción, el contacto autorizado de un cliente puede ejercer los derechos de acceso, rectificación, cancelación y oposición escribiendo al correo ficticio `privacidad@farmahorizonte.example`. El plazo simulado de respuesta es de 10 días hábiles. El asistente puede informar este procedimiento, pero no ejecuta por sí solo la rectificación ni la eliminación: esas acciones requieren un operador autorizado en la simulación.

## 6\. Seguridad y gestión de incidentes

Las credenciales del prototipo (por ejemplo, la clave de la API del modelo de lenguaje) se guardan solo en archivos locales excluidos del control de versiones; cada integrante usa la suya. Ninguna credencial forma parte de los datos tratados por esta política.

Un incidente de seguridad simulado —por ejemplo, la aparición de datos reales en el registro o la fuga de una credencial— se reporta de inmediato al equipo del proyecto, se contiene retirando el dato o rotando la credencial, y se documenta como parte de la evaluación. La exposición de una credencial en el historial del repositorio se trata como comprometida aunque el archivo se borre después.

## 7\. Relación con otras políticas

La atención, clasificación y resolución de consultas y reclamos se rige por la política POL-REC-001. Esta política no crea derechos comerciales ni modifica los plazos de devolución; regula únicamente el tratamiento de los datos dentro de la simulación.
