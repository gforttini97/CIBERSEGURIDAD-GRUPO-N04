
## Controles implementados

Los controles se mantienen en esta carpeta porque la estructura mínima del
curso solicita un directorio raíz `controles/`.

- `control_acceso.py`: valida el rol y las capacidades permitidas.
- `control_inyeccion_prompt.py`: identifica patrones de inyección y marca los
  documentos como datos.
- `control_salida_modelo.py`: valida categorías, prioridades y borradores antes
  de una acción.
- `control_confirmacion.py`: exige confirmación booleana explícita del operador.
- `control_herramientas.py`: limita las herramientas invocables.

Cada control debe medirse sin control y con control en `evaluacion/` y
documentarse en `docs/controles.md`.
