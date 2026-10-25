# Reproducción FREG-002

Rama local `freg-002-hardening`, aún no publicada. Proyecto personal independiente.
Linux x86_64, CPython3.12, dependencias/artefactos identificados; otro sistema
operativo/versión Python requiere su propio bloqueo. No se declara compatibilidad
Windows de esta nueva ruta sin ejecutarla allí.

```bash
python -m venv .venv-freg002
.venv-freg002/bin/python -m pip install --require-hashes -r requirements-full-linux-py312.lock
.venv-freg002/bin/python -m pip install --force-reinstall --require-hashes -r requirements-bootstrap-linux-py312.lock
.venv-freg002/bin/python -c "from importlib.metadata import distributions; assert [d.version for d in distributions() if d.metadata['Name'].lower() == 'pip'] == ['26.2.2']"
.venv-freg002/bin/python -m pip install --no-build-isolation --no-deps -e .
.venv-freg002/bin/python -m pip check
.venv-freg002/bin/python -m pytest -q -m 'not integration'
.venv-freg002/bin/python -m forestrag.cli demo
```

El lock incluye runtime, UI, tests y bootstrap (pip/setuptools); no instala scanner
ni FastEmbed. No se utilizó `--no-deps` para forzar un conflicto: primero se instala
el grafo completo bloqueado y se comprueba `pip check`. En esta rama `semantic`
depende directamente de ONNX Runtime/tokenizers/Hugging Face, y UI fija Pillow13.

La reinstalación aislada de pip corrige el residuo de metadata25 observado en este
entorno al actualizar bootstrap, aun cuando el módulo ya era26.2.2. Se verifica
inventario sin duplicados y scanner después; no se borran avisos ni metadatos a mano.
En la reinstalación de comprobación se necesitó repetir una vez el comando de
reinstalación de bootstrap hasta satisfacer el assert. Si sigue fallando, no dar
el entorno por válido: registrar el fallo y detener el gate de dependencias.

Para inferencia de embeddings y PDF reales, descargar activos públicos revisados:

```bash
.venv-freg002/bin/python scripts/download_model.py
.venv-freg002/bin/python scripts/download_corpus.py
FORESTRAG_RUN_INTEGRATION=1 .venv-freg002/bin/python -m pytest -q --junitxml=reports/freg002/full-suite.xml
```

Si el entorno tiene proxy SOCKS, Hugging Face/httpx puede necesitar `httpx[socks]`
como preparación de ese entorno; no es necesario para inferencia local con activos
presentes. Los pesos/revisión/hashes siguen fijados; ninguna inferencia descarga
código o usa proveedor externo.

Para CLI/UI semántica ejecutar ingesta confiable, copiar `index_sha256` emitido y
configurar `FORESTRAG_INDEX_SHA256` como explica [index-trust.md](index-trust.md).
No tomar esa referencia de un archivo enviado por otra persona ni recalcularla
automáticamente desde el índice al consultar. La API sintética de permisos usa
su propia DB y no cambia su política por esta variable.

El banco histórico de 30 consultas necesita el ZIP original del propietario
localmente; no se publica en GitHub. Con él en docs/history:

```bash
.venv-freg002/bin/python scripts/check_historical_benchmark.py
```

Resultados anteriores FREG-001 son inmutables en reports/freg001; el generador
histórico build_execution_evidence.py corresponde a ese corte y no se usa para
registrar FREG-002. La nueva matriz/receipt se conserva en reports/freg002.

Comparación47 reproducible: `python scripts/compare_runtimes_freg002.py` se ejecuta
en el entorno histórico aislado con FastEmbed0.9.0 y los mismos activos públicos.
No instalarlo en el entorno final ni usarlo con documentos privados. La suite final
incluye además tres vectores sintéticos congelados sin necesitar FastEmbed.

El workflow de instalación con lock queda configurado para Python3.12. Su ejecución
remota para FREG-002 sigue NO VERIFICADA mientras esta rama permanezca local.
