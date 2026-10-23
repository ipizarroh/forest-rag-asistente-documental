# Arquitectura y decisiones

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

