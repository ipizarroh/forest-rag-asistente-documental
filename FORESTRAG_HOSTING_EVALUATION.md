# ForestRAG: evaluación de hosting

Fecha: 24-10-2026, America/Santiago. Incremento FREG-PUBLIC-ARCH-001. Proyecto personal independiente; sin información ni infraestructura de ARAUCO. Estados: VERIFICADO (alcance probado), HISTÓRICO, DECLARADO, PROPUESTO, NO VERIFICADO y BLOQUEADO.

## Recomendación

PROPUESTO: GitHub Pages para la candidata estática con corpus exclusivamente sintético. Mantiene la cuenta y el repositorio actuales, no requiere backend o secretos y ofrece HTTPS. La compatibilidad es con esta demo limitada, no con la aplicación Streamlit/ONNX completa. No se creó ningún servicio ni se activó facturación.

## Comparación técnica y económica

| Criterio | GitHub Pages / Free público | Streamlit Community Cloud | Hugging Face Spaces | Render |
|---|---|---|---|---|
| Tipo evaluado | Sitio estático | Aplicación Python | Static o Docker CPU Basic | Free web service o Static Site |
| Python/Streamlit | No en servidor; build mediante Actions | Sí, ruta nativa | Docker para Streamlit; Static no ejecuta Python | Sí, Python o Docker; compatibilidad Streamlit requiere verificación |
| CPU/RAM | Sin runtime Python contratado; navegador del visitante | Publica rangos aproximados fechados febrero2024: 0.078-2 cores, 690MB-2.7GB; no garantía de asignación actual | CPU Basic: 2vCPU/16GB | Web Free: 0.1CPU/512MB según documentación oficial; estático sin runtime Python |
| ONNX directo | No en servidor; WASM sería otro incremento | Posible si dependencias Linux y memoria funcionan; NO VERIFICADO | Posible con Docker CPU; NO VERIFICADO | Posible con Python/Docker; 512MB puede resultar insuficiente; NO VERIFICADO |
| Modelos | No se descargan | Descarga fijada por hash antes de habilitar; arranque pendiente | Puede descargar artefactos; validarlos y revisar egress | Descarga/reinicio y egress afectan arranque; pendiente |
| Disco/SQLite | Assets públicos, sin SQLite servidor | Disco no tratado como almacenamiento durable; SQLite sólo snapshot regenerable | 50GB por defecto no persistentes; SQLite mutable requiere diseño durable | FS efímero; SQLite mutable se pierde con reinicio/hibernación/redeploy; disco persistente sólo pago |
| Arranque/suspensión | No servidor de app que despertar; latencia real aún no medida online | Duerme tras 12h sin tráfico; reactivación por visitante | CPU gratuito duerme; guía GPU menciona 48h, revisar plan; Static no usa ese runtime | Web Free duerme tras15min; reactivación aproximada1min publicada por proveedor; Static no equivale a Web Free |
| Solicitudes/consumo | 1GB sitio, 100GB/mes soft bandwidth; límites y429 posibles | Recursos compartidos; no cuota de aplicación antiabuso garantizada | Rate limits de Hub y recursos según modalidad; sin cuota propia verificada | 750h Free por workspace/mes; ancho de banda y builds con cuotas |
| HTTPS/seguridad | HTTPS disponible; sin secretos en cliente; CSP meta con límites | HTTPS proveedor y settings; XSRF/CORS y exposición requieren revisión | URL HTTPS; Static trata todo dato de cliente como público | TLS gestionado; código/servicio necesitan controles de entrada y cuotas |
| Secretos | No usarlos; cualquier asset puede descargarse | Settings de secretos servidor; no imprimirlos | Settings de Secrets en Docker; no usar secretos en Static | Variables/secret files servidor; no incluirlos en Static |
| GitHub/CI | Integración directa, Actions; aprobación y artefacto revisado | Conecta GitHub y puede redeployar cambios de la rama elegida | Repo Git de Space; sincronización GitHub añade token/proceso | Integra GitHub; auto deploy debe restringirse a revisiones aprobadas |
| Reversión | Republicar paquete aprobado; reconstruir con corpus vigente | Revertir revisión y redeploy; verificar estado de datos | Revisión Git y reconstrucción; no presupone restore de datos | Free sólo dos despliegues anteriores según docs; reconstrucción y datos aparte |
| Coste inicial | USD0 con repo público y dominio github.io | USD0 del servicio gratuito | Static USD0; nuevo Docker CPU Basic requiere PRO, USD9/mes personal | Free Web/Static USD0 sujeto cuotas; paid web 0.5c-512mb USD7/mes observado |
| Mantenimiento | Bajo: fuente, build, revisión, cuota, TLS | Bajo-medio: dependencias, arranque, límites, reinicios | Medio con Docker/sync; bajo Static | Medio web; bajo Static |
| Dependencia de proveedor | Baja: siete assets portables | Media: UI Streamlit y plataforma | Baja-media: Git/Docker; condiciones de creación cambiaron | Media: config despliegue, cuotas y disco |

Precios USD observados el 24-10-2026; sin impuestos, cambio a CLP, dominio propio ni servicios extra. Los valores no son una cotización ni garantizan permanencia de planes. La página de precios Render se recuperó parcialmente; se contrastó el resultado indexado oficial con las guías de planes. No se aceptaron condiciones comerciales ni se ingresó una tarjeta.

## Escenarios de coste

| Escenario | Supuestos explícitos | Estimación y decisión |
|---|---|---|
| Demo estática, 1000 visitas/mes | ~31KB de assets por visita sin caché; 20 builds cortos; repo público; dominio github.io | ~31MB/mes de assets, USD0 dentro de límites publicados; tráfico HTTP/TLS adicional no contado |
| Demo estática, 10000 visitas/mes | Mismo paquete y sin APIs; sin almacenamiento de consultas | ~310MB/mes de assets, USD0 dentro del soft limit de Pages; no prueba de carga |
| Streamlit semántico | Un servicio Community gratuito; modelo histórico ~252MB en disco | USD0 nominal; viabilidad RAM/tiempo/uso no medida, no garantizar servicio continuo |
| HF Docker nuevo | PRO personal y CPU Basic sin upgrade | USD9/mes nominal; otros recursos/suscripción organizacional son distintos |
| Render web continuo pequeño | 0.5c-512mb, sin disco persistente ni extra usage | USD7/mes nominal; no demuestra que 512MB soporte ONNX |

Render advierte cobros por sobreconsumo si existe medio de pago; sin él puede suspender servicios/builds. Un plan gratuito no autoriza gasto variable. No se recomienda contratar una opción pagada en esta fase.

## Condiciones de elección

Pages encaja en un portafolio educativo público; no para transacciones sensibles o SaaS comercial. Revisar condiciones si el proyecto cambia de finalidad. El repositorio ya es público, pero el estado exacto de plan, permisos administrativos, Pages y entorno de aprobación no fue verificado. No publicar como atajo la raíz del repo.

Si se decide demostrar semántica real online, medir primero proceso Python/ONNX completo y considerar Streamlit Community Cloud con índice inmutable y dependencias Linux fijadas. Elegirlo sólo tras medir cold/warm, RSS, concurrencia, reinicio y recursos del proveedor. No atribuir al paquete estático las capacidades del prototipo local.

## Fuentes oficiales consultadas

- H01 GitHub Pages, finalidad/límites y Free público: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- H02 HTTPS Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https
- H03 Workflows Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- H04 Actions y runners públicos estándar: https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job
- H05 Streamlit gratuito: https://docs.streamlit.io/deploy/streamlit-community-cloud
- H06 Recursos, suspensión y actualización: https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app
- H07 Conexión/permisos: https://docs.streamlit.io/deploy/streamlit-community-cloud/status
- H08 Spaces: https://huggingface.co/docs/hub/spaces-overview
- H09 Suspensión/hardware: https://huggingface.co/docs/hub/spaces-gpus
- H10 PRO: https://huggingface.co/pro
- H11 Render Free: https://render.com/docs/free
- H12 Precios: https://render.com/pricing
- H13 Recursos Free oficiales: https://render.com/articles/from-side-project-to-production-scaling-your-first-app
- H14 Planes actuales: https://render.com/docs/compute-plans

Todas son páginas vivas; fecha de consulta24-10-2026. La URL tentativa render.com/docs/deploy-streamlit no fue accesible y no respalda la selección.
