# Instalación y ejecución del pipeline RAG

Este documento resume el entorno, la instalación de dependencias y la ejecución del notebook `notebooks/pipeline_farma_help.ipynb` para el prototipo Farma Help.

## Entorno base

- **Sistema operativo:** Linux
- **Python usado en este proyecto:** 3.13.9
- **Gestor de paquetes:** `pip` (incluido en el entorno virtual)

Verificar la versión instalada:

```bash
python3 --version
```

> En este equipo el intérprete se encuentra en `/home/edison/anaconda3/bin/python3`, pero el procedimiento es el mismo con cualquier Python 3.13+.

## 1. Crear el entorno virtual

Desde la raíz del repositorio:

```bash
cd /home/edison/Desktop/MAESTRIA_DS/ciberseguridad_de_ia/proyecto-github

python3 -m venv .venv
```

Esto crea la carpeta `.venv/` con una instalación aislada de Python.

## 2. Activar el entorno virtual

```bash
source .venv/bin/activate
```

Cuando el entorno esté activo, el prompt muestra algo similar a:

```bash
(.venv) usuario@equipo:~/.../proyecto-github$
```

Para desactivarlo:

```bash
deactivate
```

## 3. Instalar las dependencias

Con el entorno activo:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye:

- `numpy`
- `scikit-learn`
- `sentence-transformers`
- `faiss-cpu`
- `google-genai`
- `python-dotenv`
- `jupyter`

La primera instalación descarga varios paquetes pesados (PyTorch, transformers, modelos de Hugging Face, etc.), por lo que puede tardar varios minutos.

## 4. Configurar variables de entorno

Crear o editar el archivo `.env` en la raíz del repositorio con al menos estas variables:

```env
GEMINI_API_KEY=tu_clave_aqui
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

> Nunca subir el archivo `.env` al repositorio. Debe estar ignorado en `.gitignore`.

## 5. Ejecutar los tests

Antes de correr el notebook, se pueden validar los componentes básicos:

```bash
source .venv/bin/activate
python -m unittest tests.test_componentes -v
```

Resultado esperado:

```text
Ran 3 tests in 0.002s
OK
```

## 6. Ejecutar el notebook

### Opción A: desde Jupyter (interactivo)

```bash
source .venv/bin/activate
jupyter notebook notebooks/pipeline_farma_help.ipynb
```

Se abrirá el navegador con el notebook listo para ejecutar celda por celda.

### Opción B: en modo headless (sin abrir navegador)

Útil para automatizar la ejecución o verificar que todo funciona:

```bash
source .venv/bin/activate
jupyter nbconvert \
  --to notebook \
  --execute notebooks/pipeline_farma_help.ipynb \
  --output-dir notebooks \
  --output pipeline_farma_help_ejecutado.ipynb
```

Esto genera `notebooks/pipeline_farma_help_ejecutado.ipynb` con las salidas de cada celda.

## Notas sobre la ejecución

- La primera vez se descarga el modelo de reranking `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` desde Hugging Face (varios cientos de MB).
- Las llamadas a Gemini consumen la API key configurada en `.env`. En la capa gratuita puede aparecer un rate limit si se envían muchos embeddings en un solo lote; el código ya está ajustado para procesarlos en lotes de 32.
- Se observan dos warnings comunes que no afectan el resultado:
  - `Warning: You are sending unauthenticated requests to the HF Hub...` — se soluciona creando un token en Hugging Face, pero no es obligatorio.
  - `[transformers] Token indices sequence length is longer than the specified maximum sequence length for this model (694 > 512)` — aparece durante la carga del modelo de reranking; se verificó que ningún par pregunta-ventana supera 512 tokens en la predicción real.

## Comandos rápidos

```bash
# Activar entorno
source .venv/bin/activate

# Tests
python -m unittest tests.test_componentes -v

# Notebook interactivo
jupyter notebook notebooks/pipeline_farma_help.ipynb

# Notebook headless
jupyter nbconvert --to notebook --execute notebooks/pipeline_farma_help.ipynb --output-dir notebooks --output pipeline_farma_help_ejecutado.ipynb
```
