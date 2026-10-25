# ForestRAG: análisis y plan para presentación profesional ante ARAUCO

Fecha: 23 de octubre de 2026, America/Santiago.
Estado: PROPUESTA DE TRABAJO; no se implementaron correcciones en esta fase.
Proyecto personal de Ignacio Pizarro Hurtado, Ingeniero Civil Industrial. Independiente de ARAUCO y separado de SSA Arauco.

## 1. Decisión ejecutiva

La recomendación es preparar primero una demostración extractiva confiable y reproducible. Esa versión puede sostener una conversación técnica valiosa sobre Python, datos, embeddings, evaluación y seguridad. La generación real con LLM debe ser un segundo incremento con evidencia propia.

Presentarse como candidato no exige acreditar una plataforma industrial terminada. Sí exige distinguir qué funciona, cómo se midió, qué falló y qué se corrigió. El valor actual del proyecto es localizar y mostrar evidencia documental; no hay ahorro operacional, productividad o retorno económico medido.

El dictamen vigente sigue siendo GO CON CONDICIONES para portafolio, NO-GO para piloto y NO-GO para producción. Esta revisión de planificación no cierra ningún hallazgo.

## 2. Qué se verificó en esta fase

- Main remoto sigue en eee8da5035340abef011357e5f85ad7b2fc34bc3.
- Se revisaron README, árbol completo de 42 archivos, módulos de ingestión, índice y generación, dependencias directas y workflow.
- Se leyeron los nueve entregables textuales de auditoría, incluido el JSON completo de 58 casos.
- Se comprobó la copia local del ZIP original: 42 entradas, 41 hashes del manifiesto coincidentes y sin errores CRC. Es una comprobación del paquete existente, no una nueva ejecución de pruebas del producto.
- La oferta pública de Ingeniero/a de Desarrollo IA, San Andrés, Concepción, seguía accesible en la consulta del 23 de octubre; indicaba publicación del 21 de octubre de 2026.
- No se reejecutaron pytest, el benchmark ni el scanner. Sus cifras se identifican como evidencia de la auditoría anterior del mismo commit.
- No se cambiaron código, dependencias, índices del producto ni GitHub. No se realizaron commits o publicaciones.

Los diez entregables de auditoría están disponibles fuera del repositorio. El árbol publicado no contiene esos informes ni su harness; no deben describirse como ya incorporados a GitHub.

Repositorio: [ForestRAG](https://github.com/ipizarroh/forest-rag-asistente-documental).
Referencia inmutable: [commit auditado](https://github.com/ipizarroh/forest-rag-asistente-documental/tree/eee8da5035340abef011357e5f85ad7b2fc34bc3).

## 3. Estado técnico explicado

El flujo demostrado es PDF autorizado → extracción por página → normalización → fragmentos → embeddings reales locales → SQLite → búsqueda por coseno → pasajes con fuente y página.

El corpus real contiene sólo dos páginas del informe FAO 2024, físicas 43 y 47, con 33 fragmentos en la configuración predeterminada. Los embeddings son multilingües, de 384 dimensiones. La consulta utiliza top-3 y umbral 0,5. Hay CLI, Streamlit, pruebas y CI.

El adaptador Ollama existe: construye el prompt, pide JSON y valida que los IDs citados pertenezcan a los resultados recuperados. No se ejecutó un LLM real en la auditoría. Validar esos IDs no demuestra que el texto de una afirmación se desprenda de la fuente.

No hay OCR, reconstrucción de tablas, agentes con herramientas, integración SAP/GIS/GCP ni modelos predictivos propios. La demostración se debe identificar como consulta documental extractiva mientras no se complete la ruta generativa.

### Evidencia histórica que debe conservarse

| Dimensión | Resultado auditado | Interpretación |
|---|---:|---|
| Suite original en instalación limpia | 40/40; 8,59 s | Pasan los contratos existentes; no cubren todos los defectos nuevos |
| Banco nuevo | 58 casos; 50 ejecutados y 8 NOT_RUN | Generación real pendiente |
| Recall@3 reservado | 10/14 = 71,4 % | Hay evidencia pertinente para parte de las preguntas respondibles |
| Evidencia completa top-3 | 8/14 = 57,1 % | Encontrar contexto relacionado no asegura cubrir la respuesta |
| Abstención correcta reservada | 5/6 = 83,3 % | Un caso sin respuesta obtiene pasajes relacionados |
| Abstención indebida | 1/14 = 7,1 % | Una pregunta respondible queda sin evidencia recuperada |
| Precision@3 / MRR / nDCG@3 | 0,2619 / 0,6786 / 0,6181 | Métricas de ranking sobre referencias textuales |
| Citas estructurales, índice intacto | 63/63 pasajes; 33/33 chunks reconstruidos | Procedencia correcta en estado normal; no fidelidad generativa |
| Red Team local | 9 PASS y 11 FAIL de 20 | Contratos heterogéneos, no once ataques remotos |
| Latencia caliente reservada | mediana 18,728 ms; p95 22,852 ms | Incluye embedding de consulta y búsqueda; excluye arranque y LLM |

El conjunto final sólo tiene 20 preguntas, 14 respondibles y 6 sin respuesta. La cobertura completa se calculó por superposición textual de referencias previamente fijadas, sin evaluador humano externo. No es una estimación de precisión empresarial.

BM25 obtuvo mejor ranking en este corpus mínimo. Eso justifica comparar alternativas sencillas; no demuestra superioridad general de BM25 ni mejora de embeddings sobre cualquier baseline. Las 210 filas comparativas son treinta preguntas repetidas en siete configuraciones.

### Causas concretas de los principales fallos

| Hallazgos | Causa identificada en código/evidencia | Consecuencia |
|---|---|---|
| F02 | La lectura confía en payload y asociación vector-fuente; verifica dimensión/finitud, pero no norma y correspondencia completa | Con escritura local del índice se aceptan texto/página alterados, vectores intercambiados y score >1 |
| F10/F12 | Dependencias directas fijadas, transitivas sin lock; versiones con avisos en el scanner histórico | Deuda de mantenimiento; exposición condicionada a la ruta funcional y a entradas no confiables |
| F03/F11 | El índice conserva un snapshot sin ciclo ejecutable de vigencia/retiro ni manifiesto completo de construcción | Una fuente cambiada o retirada puede seguir apareciendo sin aviso |
| F04 | La selección usa source.pages o todas las páginas | Una lista vacía amplía el alcance |
| F06 | Contratos incompletos y excepciones no traducidas a errores de dominio | PDF corrupto, metadata ausente o envelope JSON de tipo incorrecto interrumpen el flujo |
| F05 | Se distingue ID, sin deduplicar contenido equivalente entre documentos | Copias con IDs distintos monopolizan top-k |
| F01 | Ranking, umbral y fragmentación no siempre recuperan conjuntamente el span requerido | Contexto incompleto o abstención incorrecta |
| F07 | La expresión regular operacional no normaliza adecuadamente espacios | Un salto de línea evita una detección conocida |
| F08/F13 | Validación estructural de citas y ausencia de inferencia real evaluada | Fidelidad y resistencia del generador no demostradas |
| F09 | Un tag cloud cumple la expresión de nombre de modelo, aun usando loopback | Riesgo condicionado a configuración futura del servidor; no fuga observada |
| F14 | Evaluación puntual sin métricas operativas continuas | Brecha para operación sostenida, no incidente demostrado en la demo |

El scanner histórico registró 104 avisos: pypdf 6.10.0, 57; Pillow 12.3.0, 35; pip 25.0.1, 12. No son 104 explotaciones en ForestRAG. pypdf participa directamente en parsing; algunas rutas de Pillow no existen en el producto y pip es bootstrap. El siguiente scanner debe actualizar la evaluación de aplicabilidad, no repetir ese total como si fuera vigente indefinidamente.

## 4. Incremento mínimo recomendado: demo extractiva preparada para evaluación técnica

Nombre de trabajo: incremento A, propuesto. No se ha creado una rama o release con ese nombre.

Incluye correcciones verificables, evaluación nueva y presentación. No exige implementar multiusuario, nube, agentes o integraciones industriales. Mantiene una instalación local, documentos públicos autorizados y un alcance explícito de consulta documental.

| Orden | Trabajo y módulos afectados | Prueba/criterio de cierre propuesto | Esfuerzo orientativo |
|---|---|---|---:|
| A1 | Dependencias y resolución reproducible: pyproject, requirements y CI. Actualizar versiones compatibles según avisos aplicables; separar bootstrap y herramientas de test | Instalación limpia, pip check, suite y semántica real; scanner sin avisos aplicables pendientes no justificados; lock/restricciones documentadas para plataforma | 4–8 h |
| A2 | Integridad: vector_store, preprocessing y metadatos. Validar campos obligatorios, IDs derivados, dimensión, finitud, norma y correspondencia; manifestar corpus/modelo/preparación y proteger la referencia de integridad | T10–T13 como regresión: alteraciones detectadas/rechazadas antes de mostrar evidencia; rangos y errores controlados; no coeditar referencia confiable e índice bajo la misma amenaza sin reconocer el límite | 8–16 h |
| A3 | Contratos y ciclo documental: ingestion, cli, generation y UI. Distinguir pages=[] de selección omitida; traducir errores; versionar snapshot y retiro; normalizar espacios; política de modelo local | Regresiones T04/T06/T08/T09/T16/T18; fuente retirada excluida o advertida; envelope inválido controlado; tags no autorizados rechazados sin llamada | 6–12 h |
| A4 | Recuperación: comparar default, BM25, combinación simple y contexto vecino; deduplicar por contenido preservando versiones legítimas | Elegir con desarrollo; medir con reservado nuevo congelado; reportar relevancia, completitud, abstenciones y coste de latencia sin escoger sólo ejemplos exitosos | 8–16 h |
| A5 | Evidencia y presentación: README, instrucciones, resultados, revisión humana de muestra y guion. Ofrecer sólo funciones ejecutables o explicar precondiciones antes de activarlas | Otra persona puede seguir instalación y demo; suite incluye lo corregido; resultados asociados a nuevo commit; alcance y límites visibles; borrador publicable revisado | 4–8 h |

Total orientativo: 30–60 horas de ingeniería más el tiempo de revisión humana y contingencias. Son estimaciones de planificación, no trabajo ejecutado, compromiso de plazo o presupuesto contractual. No incluyen preparación de producción ni integrar un LLM. Las tareas A2 y A3 dependen de definir el formato de índice y su política de fuentes; A4 se evalúa sobre esa base estable.

### Criterio de presentación del incremento A

- Instalación y ejecución reproducibles, con corpus y versiones identificados.
- F02 y los avisos aplicables de F10 resueltos o delimitados con evidencia suficiente para el alcance local. Una advertencia por sí sola no sustituye una corrección posible.
- Regresiones de ingestión, errores, retiro, duplicados y filtro consistentes con su contrato documentado.
- Recuperación evaluada en un nuevo conjunto; cada cifra con denominador y fuente.
- Citas comprobadas en índice intacto y fallo controlado ante artefacto alterado.
- La UI y la descripción profesional dicen recuperación extractiva, sin prometer generación validada.
- Demo local con datos autorizados; sin publicación de un servicio abierto o recepción de PDFs arbitrarios.
- Sin secretos, fotografías de terceros ni documentación interna en el paquete publicable.

No es necesario ampliar el corpus para afirmar que la demo acotada funciona. Ampliarlo puede mejorar valor y diversidad de evaluación, pero sólo cuando existan licencia verificada y referencias revisadas. Dos páginas no deben presentarse como cobertura del negocio forestal.

### Evaluación futura sin sobreajuste

Se propone un banco total de 60 preguntas nuevas: 20 de desarrollo y 40 reservadas, con 24 respondibles y 16 sin respuesta en el reservado. La cantidad debe reducirse o ampliarse con justificación si el corpus no aporta diversidad real; no completar cupos con paráfrasis casi idénticas.

Congelar preguntas, referencias textuales, documento/página, grados y parámetros de aceptación antes del ensayo. El conjunto anterior queda como regresión. Una partición nueva de preguntas sobre las mismas fuentes no equivale a validación en documentos o hechos nunca vistos.

Los objetivos históricos de piloto se conservan como referencia: recall >=85 %, evidencia completa >=80 % y abstención correcta >=90 %. Con 24/16 casos, se necesitan al menos 21/24, 20/24 y 15/16 respectivamente. Son umbrales internos, no exigencias de ARAUCO ni garantía estadística de utilidad industrial.

La presentación de portafolio puede explicar resultados menores de forma honesta; para recomendar una versión mejorada conviene demostrar una mejora estable frente a la base y cerrar los hallazgos que afectan su uso previsto. No reutilizar el gate de portafolio como autorización de piloto.

## 5. Dos rutas diferenciadas

| Aspecto | Ruta A: demo extractiva sólida | Ruta B: RAG con generación real validada |
|---|---|---|
| Promesa | Localizar y mostrar evidencia verificable | Producir una respuesta limitada a evidencia recuperada |
| Dependencia inicial | Correcciones y evaluación del incremento A | Base A estable; runtime y modelo local identificados |
| Generación | No necesaria; no se ofrece como capacidad validada | Inferencia real, no mock |
| Evaluación | Recuperación, abstención, procedencia y errores | Lo anterior más respaldo por afirmación, contradicciones, cifras/unidades, inyección y latencia integral |
| Costo facturable previsto | Sin APIs pagadas; costo local de equipo y tiempo no valorado monetariamente | Mantener local; medir recursos antes de comprometer rendimiento |
| Ventaja profesional | Muestra ingeniería y evaluación defendibles pronto | Añade evidencia directa de IA generativa |
| Riesgo de alcance | Corpus demasiado pequeño o claims exagerados | Confundir citas válidas con verdad o esconder fallos del LLM |

Recomendación: terminar A y después B. La ruta A ya permite presentar el trabajo con valor; la ruta B fortalece específicamente la dimensión generativa si se ejecuta y mide correctamente.

### Alcance concreto de B

1. Seleccionar un modelo local compatible con RAM/CPU disponibles y licencia de uso, fijando versión, pesos y configuración. El nombre qwen2.5:3b del código no acredita que ése sea el modelo elegido o ejecutado.
2. Verificar política local-only del servidor y modelos permitidos; deshabilitar cloud y herramientas. Registrar límites de petición, respuesta y tiempo.
3. Evaluar el generador aislado con fragmentos revisados: hechos, cifras/unidades, evidencia ausente, contradicciones, inyección directa/indirecta y manipulación de citas.
4. Revisar cada afirmación como respaldada completa, parcial o no respaldada; documentar criterio y revisión humana. No usar sólo IDs ni el mismo modelo como juez.
5. Ejecutar después el flujo integral, identificar errores de recuperación frente a generación y medir latencia total, recursos y abstenciones.
6. Convertir G01–G08 en pruebas reales con resultados. Repetir un subconjunto para comprobar variación; temperatura 0 no demuestra determinismo.
7. Mantener visible el modo extractivo y una salida de abstención verificable.

Propuesta inicial de evaluación B: al menos 20 casos respondibles, 10 de ausencia/contradicción y los ocho escenarios G; contabilizar afirmaciones y ejecuciones reales. Antes de probar, acordar objetivo de >=95 % de afirmaciones completamente respaldadas y >=90 % de abstención correcta, además de cero fugas ficticias observadas, cero cifras/unidades críticas inventadas y cero instrucciones operacionales indebidas en la muestra. Son criterios propuestos para laboratorio; deben revisarse con el alcance y congelarse antes de medir.

Esfuerzo adicional orientativo B: 16–32 horas de ingeniería más revisión humana y contingencias por compatibilidad de modelo/runtime. El hardware y tiempo efectivo aún no se han medido para ese generador.

## 6. Guion de demostración: seis minutos

El guion se apoya en resultados históricos. Debe ensayarse otra vez sobre la versión que se mostrará; no dar por asegurados sus resultados futuros.

| Tiempo | Acción | Evidencia / explicación |
|---|---|---|
| 0:00–0:40 | Presentar problema, alcance y arquitectura | “Localizo evidencia documental pública y muestro su origen. Es un proyecto personal, no una solución de ARAUCO.” |
| 0:40–1:40 | R01: “¿Qué tres modalidades de innovación tecnológica distingue esta sección de FAO?” | PASS histórico, cobertura 1, página física 43. Abrir fuente y distinguir página PDF de rótulo |
| 1:40–2:30 | R18: “¿Qué capacidades de identificación de árboles atribuye FAO a las máquinas con sensores e IA?” | PASS histórico, cobertura 1, página física 47. Mostrar texto y límites de interpretación |
| 2:30–3:15 | R25: “¿Cuál es el intervalo de lubricación en horas del motor de una máquina modelo DEMO-X999?” | Sin pasajes en auditoría. No inventar una especificación ni un consejo de mantenimiento |
| 3:15–4:15 | R07: pregunta por el registro gratuito y qué datos puede enviar una persona desde su teléfono | FAIL histórico por cobertura 0,5395. Explicar que recuperar el tema no basta; mostrar corrección sólo si ya existe y fue evaluada |
| 4:15–5:15 | Mostrar prueba de integridad y regresión, sin manipular datos reales durante la demo | Contrastar evidencia anterior con resultado posterior únicamente cuando esté implementado. Si sigue pendiente, mostrarlo como deuda |
| 5:15–6:00 | Mostrar tabla antes/después, límites y siguiente paso | Separar extracción de generación, portafolio de piloto, y métricas de laboratorio de utilidad empresarial |

Contingencia: captura o video de respaldo sólo como ejecución registrada de una versión identificada, nunca como sustituto oculto de una demo en vivo. No incluir datos personales o internos. El guion es propuesta; no se grabó material nuevo en esta fase.

### Qué puede decir Ignacio

“Desarrollé ForestRAG como proyecto personal de consulta documental forestal con Python y embeddings locales. Implementé ingestión PDF, búsqueda y trazabilidad por página. Separé las pruebas de recuperación de las de generación y audité la base en un entorno limpio. Encontré límites de cobertura e integridad y definí cómo corregirlos y comprobarlos. Hoy la evidencia demostrada es extractiva; el adaptador generativo requiere inferencia real y evaluación propia.”

Tras implementar A podrá añadir qué defectos corrigió y qué métricas nuevas obtuvo, usando cifras de esa versión. Esa afirmación todavía no corresponde.

Sería incorrecto decir “agente industrial”, “RAG completo validado”, “cero alucinaciones”, “integrado con ARAUCO/SAP/GIS/GCP”, “ahorro de costos demostrado” o “seguridad certificada”.

## 7. Relevancia para el cargo

La oferta pública relaciona el cargo con soluciones IA, datos forestales, RAG, pipelines, validación, MLOps, trazabilidad y gobierno. Es razonable destacar la evidencia concreta de Python, procesamiento PDF, embeddings, pruebas y capacidad de revisión crítica.

La generación, operación sostenida y gobierno están demostrados sólo parcialmente. SAP/GIS, cloud, telemetría y modelos predictivos no están abordados. El proyecto no tiene que simular todas esas responsabilidades para ser útil en una entrevista.

Referencia verificada: [oferta ARAUCO](https://jobs.arauco.com/Chile/job/Concepci%C3%B3n-Ingenieroa-de-Desarrollo-IA-San-Andr%C3%A9s-BI/1442269800/). Esta valoración es una interpretación profesional de requisitos públicos, no evaluación oficial de la empresa ni promesa de selección.

## 8. Dictamen por nivel de uso

| Nivel | Estado actual | Qué permitiría cambiar el dictamen |
|---|---|---|
| Presentación de portafolio | GO CON CONDICIONES | Ya puede explicarse como experimento acotado con limitaciones. El incremento A aportaría una versión más sólida; el cierre debe comprobarse antes de llamarlo terminado |
| Piloto empresarial controlado | NO-GO en este commit | Resolver/aceptar riesgos aplicables, cumplir criterios congelados de calidad, definir dueño de datos/proceso, vigencia, acceso/retención y autorización; validar LLM si forma parte del piloto |
| Producción industrial | NO-GO | Nueva evaluación operacional, seguridad, disponibilidad, validación de dominio y autorizaciones; no se deriva de aprobar una demo o del nuevo benchmark |

No se detectó fuga sensible o ejecución peligrosa en la muestra anterior, pero eso no certifica ausencia de riesgos. La separación metodológica de la auditoría no equivale a revisión institucional independiente.

## 9. Entregables de una futura implementación

- Código corregido en versión identificada, con cambios atribuibles a hallazgos.
- Matriz F01–F14 actualizada con evidencia de cierre o justificación de alcance; F13 seguirá pendiente en A.
- Pruebas de regresión y resultados del reservado nuevo; comparación con base histórica claramente etiquetada.
- Inventario y scanner actualizado con aplicabilidad, sin PoCs peligrosos.
- Manifiesto de corpus/modelo/preparación y política de snapshot.
- README breve, instrucciones de reproducción, guion y evidencia visible de ejecución.
- Borrador de publicación revisable. Una publicación posterior será una acción distinta; no se realizó en este análisis.

No se requiere contratar servicios ni sumar arquitectura por apariencia. La mejora con mayor retorno es que una persona pueda reproducir la demo, verificar su evidencia y entender sus límites.

## 10. Base documental revisada

AUDITORIA_EJECUTIVA_FORESTRAG.md; AUDITORIA_TECNICA_FORESTRAG.md; EVALUACION_RAG_FORESTRAG.json; RED_TEAM_FORESTRAG.md; GOBIERNO_Y_TRAZABILIDAD_FORESTRAG.md; MATRIZ_HALLAZGOS_FORESTRAG.csv; MATRIZ_COMPETENCIAS_ARAUCO.md; PLAN_REMEdIACION_FORESTRAG.md; EVIDENCIAS_AUDITORIA_FORESTRAG.zip; DICTAMEN_FINAL_FORESTRAG.md.

Los resultados de producto citados pertenecen al commit eee8da5. Este documento incorpora lectura actual de fuentes y planificación; no presenta las correcciones o las pruebas futuras como ejecutadas.
