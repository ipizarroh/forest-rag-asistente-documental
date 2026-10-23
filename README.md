# ForestRAG — Asistente Documental Forestal

Prototipo personal de **Ignacio Pizarro Hurtado**, Ingeniero Civil Industrial. Permite consultar texto forestal público mediante embeddings multilingües locales, recuperar pasajes y revisar su fuente y página.

**Proyecto independiente, sin afiliación, patrocinio ni aprobación de ARAUCO.** No contiene información interna de empresas ni material de otros proyectos. Es un trabajo de portafolio; no acredita experiencia de implementación en una operación forestal.

## Qué funciona hoy

| Estado | Funcionalidad |
|---|---|
| IMPLEMENTADO Y PROBADO | Extracción PDF por página, validación de archivo/hash/licencia y fragmentación con control de tokens. |
| IMPLEMENTADO Y PROBADO | Embeddings multilingües locales de 384 dimensiones, modelo y tokenizer fijados por revisión y hashes. |
| IMPLEMENTADO Y PROBADO | Índice SQLite, recuperación por coseno, top-k, umbral, página, fuente e ID de fragmento. |
| IMPLEMENTADO Y PROBADO | CLI, demo léxica sin descarga de modelos e interfaz Streamlit; 40 pruebas locales incluidas integración semántica y AppTest. |
| IMPLEMENTADO, VALIDACIÓN PARCIAL | Adaptador Ollama local: contrato probado con transporte simulado. No se ejecutó inferencia generativa real. |
| EN DESARROLLO | Recuperación de evidencia completa por fragmento y calibración de abstención. |
| PLANIFICADO | Más corpus autorizado, evaluación reservada, generación real, fundamentación humana y controles multiusuario. |

**El modo actual muestra pasajes recuperados. No se presenta como un RAG generativo completo validado.** No es un sistema de seguridad operacional certificado ni sustituye manuales o decisiones de profesionales autorizados.

## Evidencia de este incremento

- **40 pruebas locales pasaron** en Windows/Python 3.12.14: ingesta real PDF, metadatos, rutas, integridad, fragmentos, índice, abstención, citas, UI e integración con pesos reales.
- Corpus oficial acotado: **dos páginas** del informe FAO 2024, **33 fragmentos**, dimensiones 384.
- Evaluación de desarrollo: 11 preguntas, top-k 3, coseno mínimo 0,5. Página esperada recuperada en **6/6** consultas respondibles; abstención en **5/5** no respondibles.
- Sólo **4/6** consultas recuperaron todos los términos de referencia. TreeGOER y privacidad mostraron evidencia incompleta. Recuperar la página correcta no equivale a disponer de toda la respuesta.
- Resultados: [evaluación](docs/evaluation_results.json), [interpretación y reproducción](docs/evaluacion.md), [pruebas](docs/test_results.json).

La muestra es pequeña y se diseñó conociendo el corpus. Estos resultados no estiman precisión general, productividad ni calidad de un LLM. GitHub Actions pasó en Python 3.11 y 3.12 para el primer commit funcional. La instalación limpia también pasó las 40 pruebas locales. CI está configurada en [GitHub Actions](https://github.com/ipizarroh/forest-rag-asistente-documental/actions); su estado debe comprobarse en cada ejecución.

## Instalación

Python 3.11 o superior. Desde la raíz del proyecto:

~~~bash
git clone https://github.com/ipizarroh/forest-rag-asistente-documental.git
cd forest-rag-asistente-documental
python -m venv .venv
~~~

Activar el entorno:

~~~powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
~~~

~~~bash
# Linux/macOS
source .venv/bin/activate
~~~

~~~bash
python -m pip install -r requirements.txt
python -m pip check
~~~

Si PowerShell bloquea la activación, use directamente .venv\Scripts\python.exe con los comandos Python; no es necesario cambiar la política de seguridad.

## Demostración mínima sin pesos

~~~bash
python -m forestrag.cli demo
python -m pytest -q -m "not integration"
~~~

Usa un documento ficticio original y un baseline léxico explícito. No requiere descargar modelos ni PDF. La instalación de dependencias sí requiere Internet.

## Demostración semántica con PDF real

~~~bash
python scripts/download_model.py
python scripts/download_corpus.py
python -m forestrag.cli ingest
python -m forestrag.cli ask --question "¿Cómo ayuda la inteligencia artificial al análisis de datos obtenidos por teledetección?"
python -m forestrag.cli evaluate --out data/evaluation-local.json
python -m streamlit run app/streamlit_app.py
~~~

Abrir http://127.0.0.1:8501. La interfaz usa el índice semántico por defecto. No carga documentos arbitrarios.

Integración real después de descargar el corpus y el modelo:

~~~powershell
$env:FORESTRAG_RUN_INTEGRATION="1"
python -m pytest -q
~~~

~~~bash
FORESTRAG_RUN_INTEGRATION=1 python -m pytest -q
~~~

El ejemplo .env.example documenta variables opcionales, sin secretos. La aplicación lee el entorno del proceso; no carga archivos .env automáticamente.

## Generación opcional

El adaptador usa únicamente http://127.0.0.1:11434/api/chat. Para explorarlo, el usuario debe preparar Ollama y un modelo local, por ejemplo qwen2.5:3b, y seleccionar la opción en la UI o añadir --llm al comando ask. No se instala ni se descarga ese modelo automáticamente.

Una respuesta que cite IDs existentes todavía puede estar mal fundamentada. Quedan pendientes inferencia real y revisión afirmación por afirmación.

## Arquitectura y documentación

PDF autorizado → extracción por página → fragmentos → MiniLM multilingüe/FastEmbed → SQLite → coseno → pasajes y fuentes → Ollama opcional.

- [Arquitectura, hardware y costos](docs/arquitectura.md)
- [Fuentes y licencias](docs/fuentes.md)
- [Metodología](docs/metodologia_rag.md)
- [Seguridad](docs/seguridad.md)
- [Limitaciones](docs/limitaciones.md)
- [Roadmap de aproximadamente 21 días](docs/roadmap.md)
- [Relación con la oferta laboral](docs/alineacion_cargo.md)

Sin APIs pagadas ni infraestructura facturable. La preparación descarga paquetes y aproximadamente 0,22 GB de pesos, más cachés. SQLite usa búsqueda exacta: apropiada para esta escala, no un índice ANN de producción. Sin autenticación multiusuario, integración GIS/SAP ni despliegue cloud.

## Corpus y atribución

FAO. 2024. *El estado de los bosques del mundo 2024: Innovaciones en el sector forestal para lograr un futuro más sostenible*. Roma. https://doi.org/10.4060/cd1211es

Texto bajo CC BY 4.0; página física 2 revisada. Se usa texto de páginas físicas 43 y 47, sin imágenes, logotipos ni fotografías. La extracción y normalización no son una edición oficial ni implican respaldo de FAO. El documento CONAF revisado queda pendiente de autorización escrita y no se incorporó.

Código y material ficticio original bajo [MIT](LICENSE). Pesos, publicaciones y dependencias mantienen sus propias licencias.

## Próximo paso de mayor impacto

Mejorar recuperación de fragmentos completos y evaluarla con preguntas nuevas reservadas. Después ejecutar y evaluar un LLM local, manteniendo visibles las abstenciones y la procedencia. La credibilidad de la evidencia tiene prioridad sobre ampliar funciones.

## Descripción profesional

Desarrollo ForestRAG, un prototipo personal de consulta documental forestal con Python, embeddings multilingües locales y trazabilidad por fuente y página. Implementé extracción PDF, búsqueda vectorial en SQLite, pruebas automatizadas y evaluación reproducible. La recuperación está validada en un corpus público acotado; la generación con LLM sigue en evaluación. El proyecto documenta resultados, limitaciones y decisiones de seguridad, sin afiliación ni respaldo de ARAUCO.

