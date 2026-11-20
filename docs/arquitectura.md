# Arquitectura y decisiones

La sección inicial describe la arquitectura de la rama pública. La evolución hacia diez capas se resume al final y se vincula con el [estado y roadmap](ESTADO_Y_ROADMAP.md).

Prototipo individual, local y modular. Recuperación extractiva por defecto; generación mediante adaptador opcional.

~~~mermaid
flowchart TD
    A["PDF autorizado y manifiesto"] --> B["SHA-256 y extracción por página"]
    B --> C["Fragmentos y metadatos"]
    C --> D["Embeddings multilingües locales"]
    D --> E["SQLite: vectores y texto"]
    Q["Pregunta validada"] --> F["Embedding de consulta"]
    F --> G["Coseno exacto y umbral"]
    E --> G
    G --> H{"¿Hay pasajes?"}
    H -->|No| I["Abstención"]
    H -->|Sí| J["Pasajes y fuentes"]
    J --> K["Ollama opcional y validación de citas"]
~~~

| Componente | Decisión | Razón y límite |
|---|---|---|
| PDF | pypdf, por página | BSD; posición física y etiqueta PDF. Sin OCR ni comprensión de tablas. |
| Embeddings | FastEmbed, MiniLM multilingüe ONNX cuantizado | CPU, español y 384 dimensiones. Pesos Apache 2.0; revisión y hashes fijados. |
| Índice | SQLite y producto escalar normalizado | Sin servidor; inspección SQL. O(n·d), sin ANN; máximo 10.000 fragmentos. |
| Fragmentación | 55 palabras, solapamiento 10, máximo 120 tokens | No cruza páginas; tokenizer del modelo. Consulta máxima: 128 tokens. |
| Generación | Pasajes extractivos; Ollama opcional | Sin API pagada. No presentar búsqueda como RAG generativo completo. |
| Interfaz | Streamlit en loopback | Sin carga de archivos ni acceso multiusuario. |
| Pruebas | pytest y AppTest | CI sin pesos; integración real local separada. |

Cada fragmento conserva fuente, licencia, página, etiqueta PDF, hash documental y posición inicial. El índice verifica esquema, modelo y dimensión. Escritura temporal y reemplazo tras cerrar SQLite. Sin pickle.

Modelo: Qdrant/paraphrase-multilingual-MiniLM-L12-v2-onnx-Q.
Revisión: faf4aa4225822f3bc6376869cb1164e8e3feedd0.
Descarga explícita de cinco archivos con verificación SHA-256. Los hashes detectan cambios; no certifican ausencia de vulnerabilidades.

## Hardware y costo

Python 3.11 o superior; prueba inicial en Windows/Python 3.12, CPU y dos hilos ONNX. Sin GPU.

Reservar aproximadamente 2 GB de disco y 4 GB de RAM para instalación, caché e interfaz: estimaciones, no mediciones de consumo máximo. Pesos de embeddings: aproximadamente 0,22 GB según FastEmbed; Windows puede duplicar caché sin enlaces simbólicos. PDF: 9.832.032 bytes. Ollama 3B requiere varios GB adicionales y, como planificación, 8 GB de RAM o más según cuantización/contexto; no validado con inferencia generativa.

No se contrataron APIs, dominios, servicios cloud ni infraestructura. Internet sólo para preparación y enlaces; el índice preparado se consulta localmente. GCP queda para evaluación futura con presupuesto y autorización.

## Arquitectura objetivo en diez capas

| Capa | Responsabilidad | Estado |
|---|---|---|
| 1. Biblioteca, permisos e integridad | Alcance de la fuente, original, SHA-256, permisos y vigencia. | La rama pública usa un manifiesto de fuentes. Biblioteca y versionado ampliados en laboratorio. |
| 2. Extracción y comprensión | Extraer texto y localizar fórmulas, tablas y orden de lectura. | pypdf público. Docling y OCR en laboratorio, con límites de fidelidad. |
| 3. Normalización y estructura | Representar páginas, bloques y fragmentos con sus relaciones. | Fragmentos por página publicados. JSON, Markdown derivado y fragmentación jerárquica experimentales. |
| 4. Recuperación léxica y semántica | Proponer candidatos a partir de palabras y significado. | Demo léxica y búsqueda por coseno en la rama pública. SQLite FTS5 en laboratorio. RRF como línea de evaluación. |
| 5. Ranking y selección | Ordenar y escoger evidencia, con límites de cobertura y latencia. | Coseno y umbral publicados. Rerankers en el roadmap. |
| 6. Suficiencia documental | Identificar cobertura, contradicciones y ausencia de apoyo. | Abstención extractiva inicial publicada. Suficiencia integral por evaluar. |
| 7. Generación local | Explicar con apoyo en los pasajes admitidos. | Contrato Ollama simulado en la rama pública. Inferencia Qwen3 aislada reportada en laboratorio. |
| 8. Verificación y atribución | Conservar referencia al original y comprobar apoyo por afirmación. | Fuentes y páginas publicadas. Autenticación reforzada en laboratorio y verificación semántica integral pendiente. |
| 9. Evaluación, regresión y observabilidad | Registrar resultados, errores y recursos para comparar cambios. | Evaluación inicial pública. Instrumentación y herramientas estadísticas en laboratorio. |
| 10. Interfaz y experiencia | Consultar, mostrar alcance y ofrecer acceso a los pasajes. | CLI y Streamlit publicados. Integración objetivo por validar. |

Seguridad, evaluación científica y funcionamiento básico cruzan todas las capas. El desarrollo parte de cimientos y contratos verificables y avanza hacia integración progresiva. El [estado y roadmap](ESTADO_Y_ROADMAP.md) define los criterios vigentes por etapa.

El [caso de motivación profesional de octubre](alineacion_cargo.md) documenta el contexto del primer prototipo.
