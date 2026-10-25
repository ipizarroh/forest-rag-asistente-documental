# ForestRAG — aceptación pública FREG-NEXT-001

Corpus: tres documentos ficticios públicos, versión synthetic-2026-10-24-v1. No incorpora documentos nuevos. Política public-synthetic-only-v1. Candidata demo-0.2.0-rc.1. Estado de despliegue y SHA: [PROJECT_STATUS.md](PROJECT_STATUS.md).

| Caso | Contrato y prueba |
|---|---|
| UX-01 | «¿Qué puedo encontrar en ForestRAG?» abre orientación y catálogo de los tres documentos reales del paquete |
| UX-02 | Variantes sobre documentos, temas, información y capacidades usan metadatos, sin LLM |
| UX-03 | Campos de observación: primera sección de registro-terreno |
| UX-04 | Antes de comparar imágenes: sección Comparabilidad, incluida resolución y nubes |
| UX-05 | Retiro: evidencia de control-documental, sin inventar una respuesta generativa |
| UX-06 | Sugerencia selecciona su ámbito y lo informa. Una consulta manual conserva el filtro; ampliar exige pulsar el botón explícito |
| UX-07 | Sin recuperación: abstención que reconoce los límites léxicos; nunca confirma existencia de privados |
| UX-08 | Paráfrasis sobre datos que se anotan en terreno recupera campos |
| UX-09 | Caracteres especiales no ejecutan HTML, scripts, SQL ni solicitudes con el texto de la pregunta |
| UX-10 | Corpus alterado se rechaza antes de habilitar consultas |

## Pruebas

- `node --test public_demo/test_engine.mjs public_demo/test_ux.mjs`: 32 pruebas locales PASS, con controles anteriores conservados.
- `public_demo/test_ux_browser.cjs`: aceptación automatizada en 1440×1080 y 390×844. Candidata: 11 checks nuevos PASS; postdespliegue: los mismos 11 PASS en HTTPS. Se suman 12 comprobaciones externas anteriores repetidas, incluidas igualdad de assets. Los intentos locales fueron bloqueados por red y no se cuentan como PASS.
- `public_demo/test_browser.cjs`: 11 comprobaciones gráficas anteriores; se vuelven a ejecutar en la candidata.
- `tests/test_public_demo.py`: 13 casos de construcción/allowlist/integridad, ejecutables en CI.
- `tests/test_zero_cost.py`: cuatro pruebas locales PASS del control económico.

El banco `acceptance-heldout.json` se congeló antes del cambio y se ejecutó durante el desarrollo; por eso es regresión y no evaluación ciega independiente. Línea base: 12/14; candidata final: 14/14. No sumar estos resultados a los tests unitarios como si fueran ensayos independientes.

Banco adicional `acceptance-reserved.json`, congelado después de implementar ranking y antes de medir: **10/12**, con 8/10 primeros resultados documentales correctos y 2/2 abstenciones ante preguntas ajenas. SHA-256: 6d3e53dd925ada696da0efacb4f49df29991e1beb9c0634ec2e6d7729fbdc969. R06 (huella/bytes) y R10 (cosas que guarda una observación) se abstuvieron aunque existía evidencia. No se ajustaron reglas después de ese resultado. Banco elaborado internamente, pequeño y sintético; no demuestra generalización empresarial.

## Contrato de interacción

La orientación general muestra el catálogo público y conserva el selector para las siguientes consultas. El aviso explica ese comportamiento. Las sugerencias tienen un documento explícito y notifican el cambio. La consulta manual nunca cambia de filtro silenciosamente.

No es posible determinar con certeza, sólo por falta de coincidencias, si algo no existe o requiere una paráfrasis. El mensaje conserva esa incertidumbre y ofrece revisar fuentes. No hay identidades ni permisos en esta web: todos los bytes descargables son públicos. Un futuro catálogo protegido debe provenir del backend autorizado.

Evidencia: [workflow externo 40209656323](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40209656323), [JSON de navegador](reports/next001/browser-external.json) y [recibo](reports/next001/publication.json). El protocolo UX-01–10 quedó verificado para el corpus y viewports declarados, sin afirmar comprensión general ni pruebas en un teléfono físico.
