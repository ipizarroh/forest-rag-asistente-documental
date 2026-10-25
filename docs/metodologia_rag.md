# Metodología

1. Registrar fuente, permiso, licencia, hash y páginas autorizadas.
2. Validar ruta, extensión, tamaño, firma y hash.
3. Extraer por página; conservar posición física y etiqueta PDF.
4. Normalizar y fragmentar sin cruzar páginas; controlar tokens con el tokenizer real.
5. Calcular embeddings y normalizarlos; registrar identidad del modelo.
6. Persistir texto, vector y procedencia en SQLite.
7. Validar consulta, calcular embedding y recuperar top-k por coseno con umbral.
8. Mostrar pasajes, fuente e identificador; abstenerse sin candidatos.
9. Sólo con Ollama seleccionado: enviar evidencia al endpoint local fijo y validar IDs por afirmación.

Umbral inicial 0,5; top-k 3. No representan probabilidad de certeza ni una frontera universal. Requieren evaluación reservada independiente.

El baseline léxico usa hashing determinista de palabras a 512 dimensiones, sin descargas. Se identifica explícitamente y no sustituye a la búsqueda semántica.

## Frontera de generación

El modo predeterminado no sintetiza respuestas. El adaptador Ollama separa instrucciones de contexto no confiable y no ofrece herramientas. Las pruebas simuladas verifican contrato y validación, no inferencia ni calidad factual.

Validar IDs de citas no demuestra que la evidencia implique la afirmación. Esa fundamentación requiere evaluación humana y pruebas de alucinación.

