# Farma Help

Proyecto del Grupo 04 para el curso de Ciberseguridad de IA.

Farma Help es un prototipo académico de atención al cliente para una
distribuidora farmacéutica ficticia. Su objetivo es responder consultas
sobre pedidos, entregas y devoluciones, clasificar reclamos y registrar
tickets con confirmación del operador.

El proyecto utiliza exclusivamente documentos ficticios y datos sintéticos.

## Estructura principal

```text
proyecto-github/
├── README.md                         # Descripción, instalación y estructura
├── requirements.txt                  # Dependencias del proyecto
├── .env.example                      # Nombres de variables, sin secretos
├── .gitignore
│
├── notebooks/
│   └── pipeline_farma_help.ipynb     # Pipeline principal del sistema
│
├── src/
│   ├── readme.md
│   └── farma_help/
│       ├── __init__.py
│       ├── configuracion.py          # Rutas y configuración del proyecto
│       ├── contratos.py              # Tipos compartidos entre componentes
│       │
│       ├── rag/
│       │   ├── ingesta.py            # Lectura y validación de políticas
│       │   ├── fragmentacion.py      # Fragmentos y ventanas de tokens
│       │   ├── permisos.py           # Acceso al corpus según el rol
│       │   ├── embeddings.py         # Generación de embeddings
│       │   ├── indice.py             # Índices FAISS por nivel de acceso
│       │   ├── recuperador.py        # Búsqueda semántica
│       │   ├── reranking.py          # Reordenamiento de candidatos
│       │   ├── generacion.py         # Contexto y respuestas con Gemini
│       │   └── servicio.py           # Fachada principal del RAG
│       │
│       ├── modelo_clasificador/
│       │   ├── preprocesamiento.py   # Preparación de reclamos
│       │   ├── entrenamiento.py      # Entrenamiento del modelo clásico
│       │   ├── inferencia.py         # Predicción de categorías
│       │   └── servicio.py           # Interfaz del clasificador
│       │
│       ├── agente/
│       │   ├── enrutador.py          # Identificación de intención
│       │   ├── flujos.py             # Preparación de tickets
│       │   └── orquestador.py        # Coordinación del sistema
│       │
│       ├── herramientas/
│       │   └── tickets.py            # Herramienta local crear_ticket
│       │
│       └── auditoria/
│           ├── eventos.py            # Eventos auditables
│           └── registro.py            # Registro estructurado JSONL
│
├── controles/                        # Controles de seguridad implementados
│   ├── control_acceso.py             # Roles y capacidades permitidas
│   ├── control_inyeccion_prompt.py   # Defensa contra prompt injection
│   ├── control_salida_modelo.py      # Validación de salidas
│   ├── control_confirmacion.py       # Confirmación explícita
│   └── control_herramientas.py       # Lista de herramientas permitidas
│
├── datos/
│   ├── politicas/                    # Corpus documental ficticio
│   ├── reclamos/
│   │   └── reclamos_sinteticos.csv   # Datos de entrenamiento
│   └── tickets/
│       ├── .gitkeep
│       └── tickets.json              # Salida local, no versionada
│
├── evaluación/
│   ├── catalogo/                     # Ataques y consultas legítimas
│   ├── correr_evaluacion.py          # Ejecutor de pruebas adversariales
│   └── resultados/                   # JSON y gráficos versionados
│
├── registros/
│   ├── readme.md
│   └── muestra_registro.jsonl        # Evidencia sintética versionada
│
├── docs/                             # Documentación y GitHub Pages
│   ├── index.md
│   ├── ficha.md
│   ├── arquitectura.md
│   ├── modelo-de-amenazas.md
│   ├── priorizacion.md
│   ├── controles.md
│   ├── evaluacion.md
│   └── regulatorio.md
│
└── tests/
    └── test_componentes.py           # Pruebas de componentes base
```

### Responsabilidad de las áreas

- `src/farma_help/rag/`: ingesta, permisos, recuperación, reranking y generación.
- `src/farma_help/modelo_clasificador/`: clasificación de reclamos en entrega,
  facturación o devolución.
- `src/farma_help/agente/`: enrutamiento y orquestación supervisada.
- `src/farma_help/herramientas/`: operaciones locales autorizadas.
- `src/farma_help/auditoria/`: registro de consultas, fuentes, acciones y resultados.
- `controles/`: controles de seguridad que serán evaluados sin control y con control.
- `datos/`: únicamente corpus, ejemplos y estados sintéticos.
- `evaluación/`: catálogo, ejecución y resultados de la evaluación adversarial.
- `docs/`: entregables del curso y contenido de la página del proyecto.
- `tests/`: verificaciones automatizadas de la lógica modular.

## Documentación

- [Ficha del sistema](docs/ficha.md)
- [Arquitectura](docs/arquitectura.md)
- [Modelo de amenazas](docs/modelo-de-amenazas.md)
- [Controles](docs/controles.md)
- [Evaluación adversarial](docs/evaluacion.md)

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

El pipeline principal se ejecuta desde `notebooks/pipeline_farma_help.ipynb`.
La lógica modular puede importarse desde el repositorio añadiendo `src/` al
`PYTHONPATH` o ejecutando desde la raíz del proyecto.

**Estado:** prototipo modular en desarrollo. La integración final del notebook
principal y la evaluación adversarial se completarán en las siguientes etapas.
