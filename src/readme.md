
## Código modular

La implementación nueva del producto se organiza en el paquete
`src/farma_help/`:

- `rag/`: corpus, fragmentación, permisos, embeddings, FAISS, reranking y generación.
- `modelo_clasificador/`: entrenamiento e inferencia del clasificador de reclamos.
- `agente/`: enrutamiento, flujos y orquestación.
- `herramientas/`: persistencia local de tickets.
- `auditoria/`: registro estructurado en JSONL.
- `configuracion.py` y `contratos.py`: configuración y tipos compartidos.

El notebook original `Farma_Help_Hito1_ok.ipynb` permanece en esta carpeta y
no fue modificado. En una etapa posterior podrá convertirse en el notebook
principal del pipeline, utilizando estas interfaces sin copiar la lógica.
