# ForestRAG — factibilidad de IA con $0

Fecha: 25-10-2026. Investigación documental actual; no constituye inferencia ejecutada. **IA generativa: NO VERIFICADO.** La demo pública sigue siendo léxica y no redacta respuestas con LLM.

## Ruta elegida

Primero reproducir el recuperador semántico local existente, sin sustituirlo: ONNX Runtime, tokenizer, modelo y hashes ya fijados en `src/forestrag/embeddings.py`. Después comparar BM25 y recuperación híbrida en un banco nuevo. Para una demo pública sin servidor, evaluar embeddings opcionales en el navegador; mantener BM25 como experiencia predeterminada. La generación real se valida primero en laboratorio local con citas y autorización antes del contexto.

| Alternativa | Factibilidad económica | Calidad, recursos y límites | Decisión |
|---|---|---|---|
| Híbrido local BM25 + ONNX | Software local, sin API de pago | Reutilizar modelo multilingüe de 384 dimensiones. Unir rankings con RRF y evaluar; no asumir mejora automática | Primera opción técnica |
| ONNX/Transformers.js en navegador | Inferencia del visitante, sin factura cloud | WASM CPU como base; WebGPU opcional según soporte. Worker, descarga voluntaria y cancelación; no bloquear la UI | Segundo experimento aislado |
| LLM local | Modelo abierto y runtime libre | Usa RAM/CPU/GPU propios, sin servicio siempre disponible. No exponer localhost mediante túneles | Primera validación generativa posterior |
| WebLLM en navegador | Sin servidor de inferencia | WebGPU y memoria compatibles; pesos potencialmente grandes, arranque frío, batería y móvil limitantes. No garantía de razonamiento ni español suficiente | Opcional después de evaluación |
| Spaces CPU Basic | Documentado como hardware gratuito | Suspensión por inactividad, CPU limitada, disco efímero y sin SLA. No se creó cuenta ni Space; no se verificó la prevención de upgrades en una cuenta real | Alternativa no activada |
| Endpoints/GPUs/APIs por consumo | Riesgo de facturación | Créditos y pruebas gratuitas no satisfacen la política permanente | Descartado |

## Modelos y licencias

El modelo base `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` publica licencia Apache-2.0, 50 idiomas y 384 dimensiones. El proyecto usa una conversión ONNX cuantizada de Qdrant con revisión y hashes concretos: falta volver a medir su runtime aquí y cotejar licencia/atribución de esos archivos exactos antes de una distribución nueva. La evidencia semántica anterior sigue siendo histórica.

Como candidato de generación local, `Qwen/Qwen2.5-1.5B-Instruct` publica Apache-2.0. No se descargó ni ejecutó. Su calidad documental en español no se deduce de su licencia. Verificar también el distribuidor y revisión de cualquier GGUF/MLC cuantizado.

Estimación, no medición: 1.5 mil millones de parámetros a 4 bits representan unos 0.75 GB de pesos brutos; RAM total será mayor por runtime, buffers y caché de atención. No se ofrece una cifra de RAM, tiempo o compatibilidad móvil garantizada sin probar el archivo exacto. No usar ese cálculo para lanzar una descarga al visitante.

## Experimento siguiente a costo cero

1. Verificar revisión/licencia/hashes y reproducir embeddings existentes en entorno compatible, sin telemetría ni claves cloud.
2. Congelar un banco distinto de los conjuntos NEXT-001; medir Recall@3, primer resultado pertinente, abstención y latencia fría/caliente.
3. Ejecutar el modelo en Worker/WASM en escritorio y un dispositivo móvil real; medir bytes descargados, memoria observable y tiempos. WebGPU es una mejora opcional, no un requisito de acceso a la demo.
4. Ofrecer activación voluntaria y tamaño exacto de descarga. Si no hay soporte, recursos, red o el usuario cancela, conservar BM25.
5. Para generación, usar sólo contexto previamente autorizado, sin herramientas, con límites y citas comprobadas. Medir fidelidad de cada afirmación, no sólo la existencia de un ID de cita.
6. Probar instrucciones adversariales, falta de evidencia y revocación entre recuperación y respuesta. Ningún modelo decide permisos.

No están instalados aquí ONNX Runtime, tokenizer, Hugging Face Hub, Ollama ni llama-server. La conexión local impidió descargar dependencias; no se simularon embeddings ni respuestas como evidencia real.

## Fuentes primarias

- [Modelo de embeddings](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2).
- [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct).
- [ONNX Runtime Web](https://onnxruntime.ai/docs/tutorials/web/) y [compatibilidad de backends](https://onnxruntime.ai/docs/get-started/with-javascript/web.html).
- [Transformers.js y WebGPU](https://huggingface.co/docs/transformers.js/en/guides/webgpu).
- [WebLLM oficial](https://webllm.mlc.ai/docs/).
- [llama.cpp: servidor local](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md).
- [Spaces: hardware](https://huggingface.co/docs/hub/spaces-gpus).

Inferencia de ingeniería: trasladar el cómputo al cliente evita el costo de un servidor propio, pero traslada descarga y recursos al visitante; no garantiza disponibilidad o calidad.
