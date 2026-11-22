# Instalación y ejecución del pipeline RAG en PowerShell (Windows)

Guía para preparar y ejecutar el prototipo Farma Help en un entorno Windows usando PowerShell.

## 1. Instalar Python

### Opción recomendada: winget

Abrir PowerShell como administrador y ejecutar:

```powershell
winget install Python.Python.3.13
```

Si aparece el instalador gráfico, marcar la opción **"Add Python to PATH"**.

Verificar la instalación:

```powershell
python --version
```

Debería mostrar algo como `Python 3.13.x`.

### Alternativa: Anaconda

Recomendada si ya trabajas con entornos de ciencia de datos:

```powershell
winget install Anaconda.Anaconda3
```

Después de instalar Anaconda, usar el **Anaconda PowerShell Prompt** para los pasos siguientes.

> Si PowerShell muestra un error al ejecutar scripts del entorno virtual, ejecutar una vez:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

## 2. Navegar al proyecto

```powershell
cd C:\ruta\del\proyecto\proyecto-github
```

Ajusta la ruta según donde tengas clonado el repositorio.

## 3. Crear el entorno virtual

```powershell
python -m venv .venv
```

## 4. Activar el entorno virtual

```powershell
.venv\Scripts\Activate.ps1
```

El prompt cambiará para mostrar `(.venv)` al inicio.

Para desactivarlo:

```powershell
deactivate
```

## 5. Instalar dependencias

Con el entorno activo:

```powershell
pip install -r requirements.txt
```

Esto instala:

- `numpy`
- `scikit-learn`
- `sentence-transformers`
- `faiss-cpu`
- `google-genai`
- `python-dotenv`
- `jupyter`

La primera instalación descarga PyTorch, transformers y modelos de Hugging Face, por lo que puede tardar varios minutos.

## 6. Configurar variables de entorno

Crear un archivo `.env` en la raíz del repositorio con el siguiente contenido:

```env
GEMINI_API_KEY=tu_clave_aqui
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

> No subir el archivo `.env` al repositorio. Debe estar ignorado en `.gitignore`.

## 7. Ejecutar los tests

Con el entorno activo:

```powershell
python -m unittest tests.test_componentes -v
```

Resultado esperado:

```text
Ran 3 tests in 0.002s
OK
```

## 8. Ejecutar el notebook

### Opción A: desde Jupyter (interactivo)

```powershell
jupyter notebook notebooks\pipeline_farma_help.ipynb
```

Se abrirá el navegador con el notebook listo para ejecutar celda por celda.

### Opción B: en modo headless (sin abrir navegador)

Útil para verificar que todo funciona de forma automatizada:

```powershell
jupyter nbconvert `
  --to notebook `
  --execute notebooks\pipeline_farma_help.ipynb `
  --output-dir notebooks `
  --output pipeline_farma_help_ejecutado.ipynb
```

Esto genera `notebooks\pipeline_farma_help_ejecutado.ipynb` con las salidas de cada celda.

## Notas sobre la ejecución

- La primera vez se descarga el modelo de reranking `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` desde Hugging Face (varios cientos de MB).
- Las llamadas a Gemini consumen la API key configurada en `.env`. En la capa gratuita puede aparecer un rate limit si se envían muchos embeddings en un solo lote; el código ya está ajustado para procesarlos en lotes de 32.
- Se observan dos warnings comunes que no afectan el resultado:
  - `Warning: You are sending unauthenticated requests to the HF Hub...` — se soluciona creando un token en Hugging Face, pero no es obligatorio.
  - `[transformers] Token indices sequence length is longer than the specified maximum sequence length for this model (694 > 512)` — aparece durante la carga del modelo de reranking; se verificó que ningún par pregunta-ventana supera 512 tokens en la predicción real.

## Comandos rápidos

```powershell
# Activar entorno
.venv\Scripts\Activate.ps1

# Tests
python -m unittest tests.test_componentes -v

# Notebook interactivo
jupyter notebook notebooks\pipeline_farma_help.ipynb

# Notebook headless
jupyter nbconvert --to notebook --execute notebooks\pipeline_farma_help.ipynb --output-dir notebooks --output pipeline_farma_help_ejecutado.ipynb
```
