# Probar ForestRAG online

**[Abrir la demo pública](https://ipizarroh.github.io/forest-rag-asistente-documental/)**

No necesitas una cuenta ni instalar Python. Usa un navegador moderno con JavaScript habilitado.

1. Elige una pregunta sugerida o escribe tu consulta.
2. Pulsa **Buscar evidencia**.
3. Abre la cita del resultado para revisar la sección original.
4. Puedes filtrar por documento y repetir la consulta.

Prueba estas preguntas:

- ¿Qué campos registra una observación de terreno?
- ¿Para qué sirven las imágenes en el monitoreo forestal?
- ¿Cómo se retira un documento de esta demo?

La demo contiene tres documentos completamente ficticios. Muestra pasajes mediante búsqueda léxica; no redacta respuestas con un LLM. Una pregunta fuera del corpus debe producir abstención. Los ejemplos no son instrucciones operacionales reales.

## Versión y validación

demo-0.1.0-rc.1. Fuente de ejecución 7abc2a7133662ff811bfcdf0c09866cad31cc5ef. Artefacto e0c6717d97470d5b3a0be1b2b251147c15ea1f57.

Se verificaron HTTPS, consultas, una cita, abstención, filtro y vista móvil de 390 píxeles mediante Chromium en GitHub. Son pruebas con móvil emulado; Safari, Firefox y teléfonos físicos no se probaron. [Informe completo](../FORESTRAG_INFORME_PUBLICACION_GO_001.md).

## Reproducción local para el mantenedor

Desde esta rama y con las dependencias core instaladas, ejecutar python public_demo/build.py y después python public_demo/serve.py. Abrir http://127.0.0.1:8768/. El servidor sirve sólo dist/public-demo sobre loopback.

En Linux/Python 3.12 se puede instalar requirements-lab-linux-py312.lock con --require-hashes. Ese lock no es portable a Windows; consulta la [guía local](probar-forestrag.md).

Pruebas: python -m pytest -q tests/test_public_demo.py; después del build, node --test public_demo/test_engine.mjs. La prueba externa está en public_demo/test_live.cjs y public-demo-live.yml. Sus dependencias tienen versiones e integridades fijadas; compara contra una revisión independiente del artefacto. Debe actualizarse deliberadamente al promover otro artefacto.

## Informar un problema

Describe navegador, pregunta y comportamiento observado mediante un issue del repositorio, usando ejemplos ficticios. Evita información personal o confidencial. [Versiones y reversión](../FORESTRAG_VERSIONING_STRATEGY.md).
