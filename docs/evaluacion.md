# Evaluación adversarial

La evaluación se ejecutará exclusivamente contra el prototipo local de Farma
Help, utilizando datos sintéticos.

## Organización

- Catálogo de ataques y consultas legítimas: `evaluación/catalogo/`.
- Ejecutor: `evaluación/correr_evaluacion.py`.
- Resultados versionados: `evaluación/resultados/`.
- Muestra del registro: `registros/muestra_registro.jsonl`.

El ejecutor debe utilizar las mismas interfaces de `src/farma_help/` que usa el
producto, y debe comparar cada amenaza prioritaria sin control y con control.
La versión final reportará la tasa de éxito del ataque con intervalo de Wilson
al 95% y la tasa de falsos positivos sobre consultas legítimas.
