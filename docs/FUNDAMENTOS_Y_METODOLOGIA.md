# Fundamentos y metodología de ForestRAG

ForestRAG investiga cómo recuperar y explicar información documental con evidencia verificable, dentro de las restricciones de un equipo local. El método del proyecto parte de una pregunta y termina en una decisión que otra persona puede revisar.

## Cinco disciplinas, cinco aportes

| Disciplina | Aplicación al proyecto | Estado al 20 de noviembre de 2026 |
|---|---|---|
| Ingeniería de software | Diseñar contratos de extracción, búsqueda y citas, conservar compatibilidad y verificar fallos, regresiones y reversión. | Prototipo público con pruebas y fuentes rastreables. Contratos y regresiones ampliados en laboratorio. |
| Estadística e inferencia | Definir preguntas y respuestas de referencia, analizar errores, reservar conjuntos independientes y comparar condiciones sobre los mismos casos. | Resultados descriptivos públicos. Comparaciones pareadas y bootstrap agrupado por documento en laboratorio. Calibración, sensibilidad y estimación general quedan por evaluar. |
| IA y recuperación de información | Extraer y representar, indexar, recuperar por relevancia, seleccionar evidencia y comprobar si respalda una afirmación. | Recuperación semántica local publicada. Extracción estructurada en laboratorio. Fusión, ranking, suficiencia y verificación integrada tienen etapas propias. |
| Investigación de operaciones | Medir recursos y calidad, comparar configuraciones factibles y estudiar compromisos entre objetivos. | Hay conteos y mediciones por etapa en laboratorio. Optimización formal, dominancia y fronteras de Pareto son líneas de investigación. |
| Ingeniería de procesos y mejora continua | Diagnosticar causas, aislar cuellos de botella, ensayar cambios acotados, documentar su efecto y elegir la siguiente iteración. | Desarrollo por etapas con criterios de salida. Una regresión abierta puede mantener un NO-GO aunque otros controles pasen. |

## Cómo se decide

**Problema → fundamento → hipótesis → implementación → experimento → análisis → decisión → iteración.**

1. Define el problema y la unidad de evaluación, por ejemplo, página, pasaje o afirmación. Fija la versión del corpus, el original, la referencia esperada y las restricciones.
2. Declara la hipótesis, la línea base, las variables que cambian y las que permanecen fijas. Registra la procedencia de las etiquetas, incluyendo si son sintéticas, curadas o evaluadas por una persona.
3. Evalúa en dos grupos cuando el alcance lo permita. Usa desarrollo para ajustar y un conjunto reservado para comprobar. Tras abrir la reserva, una nueva ronda de ajuste requiere una reserva nueva para sostener independencia.
4. Compara por pregunta en las mismas condiciones. Cuando varias preguntas comparten documento, trata esa dependencia al estimar incertidumbre. Informa denominadores, distribución de errores, intervalos cuando procedan y límites de generalización.
5. Decide si conservar, modificar, revertir o descartar. Registra métricas, restricciones, incertidumbre y consecuencia técnica aunque la hipótesis quede sin apoyo.

La coincidencia léxica o semántica ayuda a localizar un pasaje. El respaldo de una afirmación exige comprobar su significado, alcance y condiciones contra el original. Una puntuación de similitud requiere un estudio específico antes de interpretarse como probabilidad de certeza.

## Qué se mide y qué decisiones permite

| Variable | Unidad o control | Decisión que informa |
|---|---|---|
| Localización y orden | Página o pasaje esperado en top-k, posición del primer hit y duplicados | Ajustar recuperación y ranking con casos nuevos. |
| Fidelidad documental | Orden, fórmulas, celdas, unidades y condiciones comparadas con el PDF | Mantener el derivado, corregirlo o usar la ruta anterior. |
| Suficiencia y atribución | Cobertura de hechos, apoyo por afirmación, citas resolubles, contradicciones y abstenciones | Elegir si hay evidencia suficiente para responder. |
| Rendimiento | Tiempo de extracción, indexación, recuperación y generación. CPU, GPU, RAM, VRAM, almacenamiento y latencia. Energía, si puede medirse con método reproducible. | Identificar cuellos de botella, costo de reconstrucción y viabilidad en hardware local. |
| Integridad y seguridad | Hash, página física, permisos, versiones, regresiones e índice reversible | Aprobar, mantener en laboratorio o revertir. |

Una comparación de extracción y Markdown mantiene fijos el documento y el objetivo de búsqueda. En laboratorio se incluyó un control con la misma segmentación para aislar el efecto del formato y otro con las mismas ventanas para contrastar extractores. El conteo distingue tokens de documento, fragmento y contexto. En la evaluación inicial del laboratorio, el Markdown anotado añadió tokens al documento y el contexto de evidencia permaneció igual. La [evaluación pública](evaluacion.md) y el [estado de laboratorio](ESTADO_Y_ROADMAP.md) corresponden a conjuntos y versiones distintos.

El presupuesto monetario adicional de cero, el hardware disponible, la privacidad y la capacidad de revertir cambios delimitan las configuraciones factibles. Se propone comparar calidad y recursos mediante sensibilidad y dominancia. Una configuración sería dominada si otra iguala o mejora todos los objetivos medidos y supera al menos uno, bajo las mismas restricciones. Una frontera de Pareto solo sería interpretable para alternativas medidas y condiciones comparables. La energía, el rendimiento sobre corpus amplios y una frontera validada quedan pendientes.

## Referencias y decisiones

Un catálogo de 42 obras orienta la investigación. La selección siguiente enlaza fuentes primarias que informan decisiones concretas. La inclusión de una obra indica su papel como referencia en el proyecto.

| Referencia | Decisión que informa |
|---|---|
| [Designing Data-Intensive Applications](https://dataintensive.net/) | Separar el original y el catálogo de las representaciones e índices que se pueden reconstruir. |
| [Software Engineering at Google · Testing Overview](https://abseil.io/resources/swe-book/html/ch11.html) y [Building Secure and Reliable Systems · Testing Code](https://google.github.io/building-secure-and-reliable-systems/raw/ch13.html) | Probar contratos para cambiar subsistemas y comprobar integridad y reversión ante fallos. |
| [An Introduction to Statistical Learning](https://www.statlearning.com/) | Diseñar desarrollo y evaluación, y usar remuestreo con supuestos explícitos. |
| [Introduction to Information Retrieval · Evaluation](https://www.cambridge.org/highereducation/books/introduction-to-information-retrieval/669D108D20F556C5C30957D63B5AB65C/evaluation-in-information-retrieval/1DE7AC4EC9996792D8590212D735AF15) y [Lewis et al. · Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | Distinguir relevancia de recuperación, cobertura de información y generación sustentada. |
| [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/) | Orientar la investigación futura de decisiones con varios objetivos y restricciones. |
| [IHI · Model for Improvement](https://www.ihi.org/library/model-for-improvement) | Fijar una pregunta y una medición, ensayar a pequeña escala y revisar antes de ampliar. |
