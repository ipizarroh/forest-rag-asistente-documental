# Probar ForestRAG

Esta guía corresponde a la copia de desarrollo basada en FREG-002 y su actualización
editorial FREG-003. Todavía no están publicadas estas dos entregas. Clonar `main`
o la rama pública `freg-critical-001` obtiene versiones anteriores: sus instrucciones
y dependencias no deben mezclarse con las de esta copia.

Desde la entrega local, abre la carpeta que contiene `README.md` y `pyproject.toml`.
La instalación necesita Internet. Conserva los saltos de línea LF de los archivos
con huella: el paquete fuente los preserva. Al clonar un bundle en Windows, usa
`git -c core.autocrlf=false -c core.eol=lf clone RUTA_DEL_BUNDLE carpeta-destino`
(reemplaza ambas rutas por las de tu entrega); no cambies el hash esperado del manifiesto. Las demostraciones sintéticas no descargan PDF ni modelos.

## 1. Preparar un entorno para las demostraciones pequeñas

Python 3.11 o superior. Los bloqueos con hashes de FREG-002 sólo corresponden a
Linux x86_64 / Python 3.12; consulta la [reproducción completa](reproduce-freg002.md)
para ese entorno. Los comandos siguientes instalan el núcleo y las pruebas,
sin la interfaz ni los pesos semánticos.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m forestrag.cli demo
```

No hace falta activar el entorno. En los comandos siguientes, usa
`.\.venv\Scripts\python.exe` donde aparezca `python`, también en el segundo terminal.

### Linux / macOS

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pip check
.venv/bin/python -m forestrag.cli demo
```

En los comandos siguientes, usa `.venv/bin/python` donde aparezca `python`,
también en el segundo terminal. El lock de Linux no acredita compatibilidad con macOS.

### Qué debes observar

La demo usa una búsqueda léxica sobre un documento ficticio original. Devuelve un
objeto JSON con pasajes y citas para una pregunta sobre campos de una orden de
mantenimiento. No es la búsqueda semántica de la captura ni usa un modelo generativo.

## 2. Comparar permisos con documentos ficticios

Desde la misma carpeta:

```bash
python -m forestrag.security_http init
python -m forestrag.security_http serve
```

El servidor escucha en `http://127.0.0.1:8510`. Déjalo abierto y, en otro terminal
con el mismo entorno y carpeta, ejecuta:

```bash
python scripts/demo_security.py
```

El script hace la misma consulta para cinco identidades y comprueba la denegación
de una descarga. Debe mostrar cinco líneas `PASS` y una descarga no autorizada
con estado `404` y `PASS`. No debe imprimir tokens.

`init` crea credenciales aleatorias locales, válidas como máximo una hora, en
`data/security-lab/`, excluido de Git. No las compartas ni las incluyas en entregas.
No sobrescribe un laboratorio existente. Si caducan, consulta la administración
local en la [guía del laboratorio](security-lab.md); repetir `init` sobre los mismos
archivos no los renueva. En Windows, su modo 0600 no acredita protección NTFS.
Detén el servidor con Ctrl+C al terminar.

Es una API de laboratorio, sin interfaz de chat empresarial. La interfaz pública
Streamlit utiliza otro índice y no hereda estos permisos.

## 3. Abrir el prototipo semántico con texto público

Esta ruta utiliza un modelo local de embeddings, aproximadamente 252 MB de artefactos,
y el PDF público revisado, aproximadamente 9,8 MB. No descarga un LLM generativo.
No se incluyen los activos en la entrega.

Tras preparar el entorno, instala las opciones semántica e interfaz:

```bash
python -m pip install -e ".[semantic,ui,dev]"
python -m pip check
python scripts/download_model.py
python scripts/download_corpus.py
python -m forestrag.cli ingest
```

Conserva el valor `index_sha256` que entrega **esa construcción confiable**.
Configúralo en el terminal que hará las consultas:

```powershell
# PowerShell: reemplazar el texto por la huella emitida al construir.
$env:FORESTRAG_INDEX_SHA256="HUELLA_EMITIDA_POR_INGEST"
```

```bash
# Linux/macOS: reemplazar el texto por la huella emitida al construir.
export FORESTRAG_INDEX_SHA256=HUELLA_EMITIDA_POR_INGEST
```

El texto de ejemplo no es una huella válida. No recalcules la referencia desde
un índice que te haya enviado otra persona: debe proceder de la construcción confiable.
La huella no es una contraseña. Consulta el [diseño de confianza](index-trust.md).

```bash
python -m forestrag.cli ask --question "¿Cómo ayuda la inteligencia artificial al análisis de datos obtenidos por teledetección?"
python -m streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

Abre `http://127.0.0.1:8501`. Deja desactivada la opción experimental de Ollama:
el modo demostrado entrega fragmentos, fuentes y páginas. Si no hay evidencia
suficiente, corresponde revisar la fuente o abstenerse.

## 4. Profundizar y comprobar

- [Reproducción completa y pruebas con activos reales](reproduce-freg002.md).
- [Laboratorio: permisos, revocación, cuotas y límites](security-lab.md).
- [Evaluación y alcance de las métricas](evaluacion.md).
- [Fuentes, licencias y corpus autorizado](fuentes.md).
- [Evidencia de esta revisión editorial](../reports/freg003/validation.json).

Las pruebas de Linux de FREG-002 son evidencia anterior conservada. El informe
FREG-003 identifica por separado los comandos ejecutados en Windows, las rutas
no ejecutadas y cualquier bloqueo de instalación. Esta revisión del README
no amplía el alcance a datos empresariales.

## Si Windows restringe el directorio temporal

En esta sesión, el temporal del entorno de ejecución bloqueó reemplazos de archivos.
Se resolvió usando un directorio autorizado, sin cambiar la política de seguridad:

```powershell
New-Item -ItemType Directory -Force .pip-temp | Out-Null
$env:TEMP=(Resolve-Path .pip-temp).Path
$env:TMP=$env:TEMP
# Repetir la instalación desde este terminal.
```

Para repetir las pruebas acotadas sin el temporal restringido:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/test_security_lab.py tests/test_index_trust.py --basetemp=data/pytest-local
```

Pytest administra y limpia su basetemp: elige una carpeta exclusiva para estas
pruebas, sin documentos propios. Los temporales de instalación quedan fuera
del paquete fuente y no deben versionarse.
