# ForestRAG - demo pública candidata

Proyecto personal de Ignacio Pizarro Hurtado, independiente de ARAUCO.

Esta rama contiene sólo los componentes públicos necesarios para construir y comprobar la demo sintética aprobada. No incluye informes privados, fuentes conectadas, documentos empresariales ni el laboratorio de permisos.

## Qué permite probar

Tres documentos ficticios, preguntas sugeridas o libres, selección de documento y fragmentos con referencias a su sección. Es búsqueda léxica; no genera respuestas con LLM ni ejecuta recuperación semántica. La consulta se procesa en el navegador.

La URL online se agregará cuando Pages esté desplegado y verificado externamente. No se declara publicada una ejecución local.

## Reproducir y comprobar

Con Python3.12 y dependencias verificadas:
```text
python -m pip install --require-hashes -r requirements-lab-linux-py312.lock
python -m pytest -q tests/test_public_demo.py
python public_demo/build.py
node --test public_demo/test_engine.mjs
python public_demo/serve.py
```

Abrir http://127.0.0.1:8768/ para revisión local. El lock corresponde a Linux/Python3.12; no debe usarse como lock de Windows sin validar wheels. Node24.22.1 se usa en CI. El visitante final no instala nada.

## Publicación

Publicar exclusivamente los siete archivos de dist/public-demo en una rama de artefacto dedicada después de CI y aprobación. No publicar la raíz de esta rama como sitio.

## Límites

Los hashes verifican correspondencia con un manifiesto; no protegen frente a un publicador que controla tanto código como referencia. El pacing de30 consultas/minuto por pestaña puede eludirse y no es una cuota global. No hay documentos privados, API, herramientas administrativas ni carga dePDF.

El prototipo técnico local y su ruta semántica son distintos de esta demo. FREG-SAH-001, retirada/restauración protegida, identidad empresarial y LLM siguen pendientes.

Ver PUBLICATION.md para procedencia, alcance y reversión.
