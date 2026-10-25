# ForestRAG — política permanente de costo monetario cero

Fecha: 25-10-2026, America/Santiago. Mandato FREG-NEXT-001. **Presupuesto autorizado: $0 CLP / USD 0.** No se habilitan tarjetas, pruebas con conversión a pago, facturación, upgrades ni servicios por consumo.

## Decisión vigente

La demo usa el repositorio público existente y GitHub Pages. Consultas y ranking se ejecutan en el dispositivo del visitante. No existe API facturable, base de datos cloud, dominio comprado, telemetría contratada ni descarga automática de modelos. Ante cuotas, se limita o suspende la función; no se contrata capacidad.

| Recurso | Cuenta / tarjeta / facturación | Límite y prevención | Estado |
|---|---|---|---|
| GitHub Pages existente | Cuenta GitHub existente; sin nueva tarjeta ni habilitación de pagos | Sitio ≤1 GB; ancho de banda blando 100 GB/mes; 10 builds/h; respetar restricciones no comerciales | Permitido para esta demo educativa pública |
| GitHub Actions | Cuenta existente; sólo runners estándar ubuntu-latest en repositorio público | Cada job se omite si el repositorio pasa a privado. Sin caches ni upload-artifact; timeout de candidata/live 10 min. Sin larger runners | Permitido para CI del proyecto |
| Python, NumPy, SQLite, Node | Sin cuenta ni tarjeta adicional | Ejecución local; licencias de las versiones instaladas y locks conservados | Permitido |
| Modelos abiertos descargables | Descargas públicas opcionales; no API de inferencia | Fijar revisión, hash y licencia antes de uso. No confundir descarga de pesos con inferencia hospedada | Investigación / próxima validación |
| Hugging Face CPU Basic | Crear un Space de cómputo nuevo exige plan pagado; no se creó cuenta | CPU Basic anuncia 2 vCPU, 16 GB RAM y disco efímero 50 GB sin tarifa horaria, pero el acceso a nuevos Spaces Gradio/Docker requiere plan pagado | Descartado para nuevo backend: plan pagado incompatible con $0 |
| API de LLM por consumo / cloud con tarjeta | Puede crear obligaciones económicas | Se descarta aunque haya créditos o un estimado de USD0 | No autorizado |
| LLM/embeddings en navegador | Sin cuenta de inferencia | Recursos del visitante, descarga voluntaria, límites de memoria, CPU y compatibilidad; fallback léxico obligatorio | Investigación |
| LLM local | Sin API pagada | No implica disponibilidad pública permanente; sólo loopback y modelos con licencia validada | Investigación; sin runtime encontrado aquí |

## Procedimiento obligatorio por decisión

Registrar si exige cuenta, tarjeta o habilitar facturación; cuota, caducidad, exceso, licencias, alternativa y bloqueo de gasto. Si cualquiera requiere una obligación monetaria, detener esa operación. No modificar la facturación del propietario.

Control implementado: `python public_demo/check_zero_cost.py`. Inspecciona los tres workflows, exige runner estándar y exclusión de repositorios privados, y rechaza caches, artefactos persistentes y acciones no incluidas en su lista permitida. Cuatro pruebas negativas/positivas verifican el contrato. Es un control acotado de configuración, no un analizador universal de costos ni una auditoría de la cuenta.

## Qué pudo comprobarse

Repositorio público verificado por GitHub; workflows revisados y limitados a herramientas existentes. No se crearon recursos comerciales ni cuentas, no se introdujeron métodos de pago y no se modificó facturación. La conexión no permite consultar la factura completa ni el estado de tarjetas de la cuenta: no se afirma haberlos auditado. No se usan esos datos como fundamento económico: los recursos seleccionados son las funciones gratuitas documentadas para repositorios públicos.

Las cuotas no garantizan disponibilidad infinita. El limitador de 30 consultas/minuto es de una pestaña, no un control del tráfico global. El artefacto se mantiene muy por debajo de 1 GB y no aloja pesos grandes.

## Fuentes oficiales consultadas

- [GitHub Pages: límites y usos permitidos](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).
- [GitHub Actions: uso y facturación](https://docs.github.com/en/actions/concepts/billing-and-usage).
- [Runners grandes facturables](https://docs.github.com/en/actions/concepts/runners/larger-runners).
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-overview) y [hardware y upgrades](https://huggingface.co/docs/hub/spaces-gpus).

Revisar condiciones antes de adoptar un recurso diferente. Los términos pueden cambiar; ante incertidumbre se conserva la demo local/estática y no se activa pago.
