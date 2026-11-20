# Estado verificable y roadmap de ForestRAG

**Corte: 20 de noviembre de 2026.** La rama pública mantiene el prototipo documentado. Los avances ARCH-006 y ARCH-007 corresponden a laboratorio. El estado de esos experimentos se informa para orientar la revisión técnica.

## A · Publicado y verificable

- El prototipo declara la versión de paquete 0.1.0 en [pyproject.toml](../pyproject.toml). Utiliza Python, pypdf, MiniLM multilingüe local de 384 dimensiones, SQLite, CLI y Streamlit. El adaptador Ollama de esta versión tiene pruebas de contrato con transporte simulado.
- La demostración semántica incluye dos páginas físicas de una publicación de la FAO y 33 fragmentos. La evaluación de desarrollo registró 6/6 páginas esperadas, 5/5 abstenciones para casos sin respuesta y 4/6 consultas con todos los términos de referencia. Se reportaron 40 pruebas locales. [Método y límites](evaluacion.md) · [Resultados](evaluation_results.json) · [Registro de pruebas](test_results.json)
- La página recuperada es una medida de localización. Verificar una explicación exige revisar si los pasajes respaldan cada afirmación. Los casos iniciales se diseñaron con conocimiento del corpus.

## B · Laboratorio

### ARCH-006 · Cimentación

El informe de laboratorio registró contratos, trazabilidad y herramientas de evaluación, **190 pruebas aprobadas** y **113/113 rankings idénticos** con la instrumentación añadida. Se dio **GO limitado a cimentación**. La igualdad de rankings indica que se conservó el orden en ese ensayo. En esa etapa quedaron pendientes Windows nativo, Qwen3 real y las once consultas documentales históricas.

### ARCH-007 FIX04 · Comprensión documental

Las correcciones hasta FIX04 integraron extracción con Docling, JSON estructurado, Markdown derivado, fragmentación jerárquica y correspondencia con página y originales en un índice auxiliar. Se ensayaron en una copia aislada de laboratorio.

| Evidencia | Resultado y alcance |
|---|---|
| Docling 2.63.0 en Windows nativo | El informe FIX04 registró **4/4 PDF sintéticos** de aceptación, con extracción real y sin recurrir a otro extractor. Las pruebas comprobaron orden de dos y tres columnas, preservación de las fórmulas ensayadas y celdas y posiciones de la tabla sintética. |
| Integridad y reversión | Activos locales cotejados con manifiesto SHA-256. El recorrido mínimo en Windows registró una cita autenticada contra el original y la retirada y restauración del índice auxiliar. |
| Regresión | FIX04 reportó **240 pruebas aprobadas** en su ejecución y dos bloqueadas al preparar enlaces simbólicos. Una repetición posterior encontró incidencias de rutas e importaciones. El propietario reportó que dos pruebas heredadas pasaron al corregir PYTHONPATH. Falta el cierre integrado de Windows y la cobertura completa de seguridad de enlaces simbólicos (symlinks). |
| Inferencia aislada | El propietario reportó Ollama 0.40.15 y una inferencia sencilla local con Qwen3 4B Q4_K_M mediante CUDA en una RTX 3070 Ti. La generación integrada al recorrido de recuperación, citas y validación sigue pendiente. |

**Dictamen vigente: NO-GO para aprobación completa de ARCH-007.** Quedan por cerrar la regresión integrada de Windows, las pruebas de seguridad de enlaces simbólicos, la evaluación integral de OCR, las once consultas documentales históricas, la generación Qwen3 integrada al RAG y la revisión consolidada de los catorce criterios. Los aciertos sintéticos delimitan los casos observados. Para establecer desempeño sobre documentos reales hacen falta muestras autorizadas y representativas.

El experimento anterior de Linux registró pérdida de fórmulas y orden incorrecto en el banco reservado. Las correcciones de FIX04 se evaluaron en bancos sintéticos específicos. El Markdown continúa siendo un derivado, con el PDF original y su referencia conservados para revisión. Las verificaciones pendientes son trabajo de laboratorio y carecen de fecha pública comprometida.

## C · Roadmap y criterios de salida

| Etapa | Estado | Qué se necesita demostrar |
|---|---|---|
| ARCH-006 · Cimentación | GO limitado de laboratorio | Contratos, regresiones, seguridad y evaluación reproducibles dentro del alcance observado. |
| ARCH-007 · Estructura documental | NO-GO para aprobación completa | Cerrar los controles de fidelidad, integridad, reversión y compatibilidad descritos arriba. |
| ARCH-008 · Recuperación | Planificada | Comparar recuperación léxica FTS5, embeddings locales y combinación mediante RRF, con el mismo corpus y consultas. |
| ARCH-009 · Ranking | Planificada | Medir si el reranking y la selección aportan evidencia útil y qué latencia añaden. |
| ARCH-010 · Suficiencia | Planificada | Identificar cobertura, contradicciones y falta de apoyo con criterios verificables. |
| ARCH-011 · Generación fundamentada | Planificada | Evaluar afirmaciones y citas frente a la evidencia y el comportamiento de abstención. |
| ARCH-012 · Integración objetivo V0.4 | Planificada | Superar regresiones, seguridad, funcionamiento básico y restricciones de recursos del recorrido integrado. |

Seguridad, evaluación y compatibilidad funcional se verifican en cada etapa. El recorrido se construye desde cimientos y contratos de subsistema hacia integración progresiva. Una mejora aislada se conserva, modifica, revierte o descarta según su evidencia y las restricciones del sistema.

Después de esa integración se podrán investigar síntesis avanzada, análisis de sensibilidad, optimización multiobjetivo, procesamiento por lotes, informes e integración con datos y procesos empresariales. Los agentes con permisos, acceso acotado y auditoría son una línea prospectiva. Su evaluación requeriría un alcance propio.
