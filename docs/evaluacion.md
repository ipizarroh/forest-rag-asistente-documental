# Evaluación reproducible

Este documento conserva la evaluación inicial. La regresión posterior de FREG-002
está en [su evidencia](../reports/freg002/retrieval-regression.json): banco conocido,
no una evaluación nueva independiente. Las 97 pruebas de FREG-002 en Linux no
sustituyen esa medición de calidad. FREG-003 no mide de nuevo la recuperación.

Fecha de validación: 22/10/2026, America/Santiago. Resultados completos en evaluation_results.json; pruebas en test_results.json.

## Recuperación real

Se descargó y verificó un PDF FAO de 132 páginas. Se indexaron únicamente páginas físicas 43 y 47, rotuladas 27 y 31: 33 fragmentos. Embeddings ONNX multilingües de 384 dimensiones, CPU. Revisión del modelo y hashes en embeddings.py.

Conjunto de desarrollo: seis preguntas respondibles y cinco no respondibles, con respuestas de referencia y páginas esperadas. Top-k 3, umbral 0,5 definido antes de ejecutar la evaluación.

| Métrica | Resultado | Interpretación |
|---|---|---|
| Hit@3 a nivel de página | 6/6 | Al menos un fragmento de la página esperada. Medida gruesa. |
| Abstención en no respondibles | 5/5 | Sin pasajes por encima del umbral en esta muestra. |
| Todos los términos de referencia presentes | 4/6 | Cobertura superficial de evidencia, no verificación de afirmaciones. |

Casos problemáticos: P02/TreeGOER recuperó 2 de 5 términos de referencia; P03/privacidad, 2 de 3. No se ocultaron esos casos ni se ajustó el umbral para mejorar este resultado.

La métrica de términos busca secuencias normalizadas en el conjunto recuperado. No demuestra exactitud, entailment ni suficiencia de una explicación. Es más informativa que la página sola, pero exige revisión humana complementaria.

No hay conjunto reservado independiente. No se puede inferir precisión general ni rendimiento industrial. Los tiempos individuales JSON son mediciones de esta ejecución con modelo cargado; no un benchmark de latencia integral ni de arranque.

## Pruebas

40 pruebas pasaron en Windows/Python 3.12.14, incluidas dos de interfaz y una integración con PDF y embeddings reales. Una prueba del contrato Ollama usa transporte simulado; no demuestra inferencia generativa.

Se corrigió un bloqueo Windows al reemplazar el índice: el contexto de SQLite confirma transacciones pero no cierra la conexión; ahora el cierre es explícito antes del reemplazo.

La consulta real en Streamlit y la salud HTTP se verifican aparte de AppTest. No se atribuyen ahorros de tiempo, productividad ni clientes.

## Reproducción

La ruta actual exige configurar la huella emitida por una ingesta confiable antes
de consultar/evaluar. Sigue la [guía vigente](probar-forestrag.md) y la
[reproducción FREG-002](reproduce-freg002.md). Los comandos del corte inicial
se conservan en Git; no deben aplicarse omitiendo este nuevo requisito.


Para incluir integración, activar FORESTRAG_RUN_INTEGRATION=1 y ejecutar pytest. Cada ejecución conserva sus propios tiempos. PDF e índice quedan fuera de Git.

## Generación y fundamentación pendientes

Ejecutar un modelo local y revisar cada afirmación contra los fragmentos, medir citas correctas, respuestas insuficientemente respaldadas y abstenciones. Incluir documentos con instrucciones maliciosas, versiones contradictorias y preguntas cercanas al tema cuya respuesta no esté en el corpus.


## Instalación independiente y CI

Se repitieron las 40 pruebas en un venv limpio, sin paquetes del entorno base: 40/40 y pip check sin dependencias rotas. GitHub Actions pasó en Linux con Python 3.11 y 3.12 para el commit funcional 8aea2a8deab084391235147c9d2dc574546f5b73. [Ejecución comprobada](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/39889677003). La suite remota excluye la integración semántica; ésta se ejecutó localmente con pesos reales.
