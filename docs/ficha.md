# Farma Help — Ficha del sistema

## Propósito y usuarios

Farma Help es un prototipo académico para el equipo de atención al cliente
de una distribuidora farmacéutica ficticia. Ayuda a consultar políticas
sobre pedidos, entregas y devoluciones, clasificar reclamos y registrar
tickets para su seguimiento.

## Componentes

1. **Asistente documental (RAG):** recupera fragmentos de las políticas
   ficticias y los usa para responder consultas, indicando qué documento
   respalda la respuesta.
2. **Clasificador de reclamos:** un modelo de aprendizaje automático
   clásico asigna cada reclamo a una categoría: entrega, facturación
   o devolución.
3. **Agente con herramientas:** prepara un ticket y lo registra localmente
   solo después de que el operador confirme la acción.

## Datos y procedencia

El equipo creará políticas ficticias, ejemplos de reclamos etiquetados
y casos de prueba sintéticos. El proyecto no utilizará datos de clientes,
pacientes, pedidos ni empresas reales.

## Permisos

El operador puede consultar las políticas, clasificar reclamos y confirmar
la creación de tickets. El asistente puede leer el corpus y usar la
herramienta local de registro. No puede modificar las políticas ni enviar
tickets a sistemas externos.
