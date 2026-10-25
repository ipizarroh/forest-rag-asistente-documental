# ForestRAG — informe FREG-NEXT-001

Fecha: 25-10-2026, America/Santiago. Mandato: GO CON CONDICIONES, presupuesto permanente $0. Estado y SHA vigentes en [PROJECT_STATUS.md](PROJECT_STATUS.md).

## A. Estado y trabajo

Se recuperaron 147 blobs exactos de 4bd230b. La demo conserva tres documentos ficticios y su diseño. Se implementaron catálogo por metadatos, orientación, sugerencias con ámbito explícito, conservación del filtro manual, ampliación voluntaria, estados accesibles y abstención honesta.

El ranking usa BM25 (k1=1.2, b=.75), un refuerzo de metadatos .25, normalización y vocabulario limitado documentado en el motor. Exige al menos dos términos distintos cuando existen y cobertura de 60% de términos de contenido. No es búsqueda semántica ni un LLM.

## B. Consulta del propietario

«¿Qué puedo encontrar en ForestRAG?» muestra tres documentos públicos, sus secciones y enlaces para explorarlos. La ruta de orientación declara capacidades y límites; no inventa una síntesis generativa.

## C. Calidad

32 pruebas Node locales PASS, cuatro pruebas del control económico PASS y matriz UX-01–10 preparada para navegador de escritorio/móvil. Regresión de 14 consultas: 12/14 antes, 14/14 después. Banco reservado interno posterior, sin reajuste: 10/12; dos falsos negativos. Resultados pequeños, sintéticos y no independientes de una auditoría humana.

La red del entorno bloqueó clone, descarga de dependencias y navegador localhost. Se recuperó código por GitHub y se delegó la ejecución gráfica al workflow autorizado, no a un nuevo servicio. El recibo de CI/despliegue se añade tras observarlo; no se atribuyen pruebas antiguas al commit nuevo.

## D. Seguridad

FREG-SAH-001 añade en una rama local independiente revisión documental, retirada, restauración de contenido conservando política vigente y un sello separado del índice. 22 pruebas funcionales locales PASS. [Alcance, supuestos y pendientes](FORESTRAG_SAH_001_IMPLEMENTATION.md). No se publica el nuevo componente protegido ni se cierra el gate de host.

## E. Presupuesto y arquitectura futura

No se crearon servicios comerciales ni se habilitaron pagos. La demo usa Pages existente y CI de runners estándar en repositorio público, sin cache/artifact storage solicitado por estos workflows. [Política y límites comprobados](FORESTRAG_ZERO_COST_ARCHITECTURE.md). No se auditó la factura ni los métodos de pago de toda la cuenta.

La ruta recomendada es revalidar el ONNX local ya existente, después comparar híbrido y embeddings opcionales en navegador con fallback BM25. Generación posterior en laboratorio local, con inferencia real, licencia, calidad de español y citas medidas. [Factibilidad y fuentes oficiales](FORESTRAG_FREE_AI_FEASIBILITY.md).

## F. Versiones y continuidad

No se cambia main ni se fuerza historia. La publicación pública sólo puede avanzar tras CI; siete assets sintéticos en gh-pages, SHA registrado y verificación HTTPS posterior. Se mantienen A1–A5/B, S0–S4, SAH01–18, A2-03/A3-02 y la historia FREG. [Reconciliación](FORESTRAG_VERSION_RECONCILIATION.md).

## G. Gates al preparar la candidata

| Área | Dictamen |
|---|---|
| Demo / móvil | GO CON CONDICIONES, condicionado al recibo CI y postdespliegue |
| Búsqueda | GO CON CONDICIONES: casos obligatorios y limitaciones de paráfrasis explícitas |
| Seguridad documental | GO CON CONDICIONES, sólo laboratorio local probado |
| Integridad | GO CON CONDICIONES dentro del adversario limitado al índice |
| Versionamiento | Trazabilidad por blobs y commits; consultar recibo vigente |
| Presupuesto | GO para recursos gratuitos delimitados; sin auditoría de facturación de toda la cuenta |
| IA generativa | NO VERIFICADO; sin inferencia ejecutada |
| Host Windows | NO VERIFICADO |
| Piloto confidencial / producción | NO-GO |

## H. Siguiente incremento

FREG-NEXT-002: revalidar ONNX local y medir un híbrido contra BM25 en banco nuevo; ampliar pruebas de recuperación segura y revisar provisión de la autoridad. Aceptación: dependencias/licencias/hashes fijados, inferencia real reproducible, métricas publicadas aunque no mejoren, costo cero, ningún cambio a main ni exposición protegida. No sustituir pruebas por respuestas simuladas.
