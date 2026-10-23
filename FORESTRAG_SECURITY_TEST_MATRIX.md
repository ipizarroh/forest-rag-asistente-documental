# ForestRAG — Matriz de pruebas de seguridad e ingeniería

FREG-CRITICAL-001 · 23-10-2026. Evidencia primaria: XML E06/E07 y
[test-cases.json](reports/freg001/test-cases.json), con **una fila por caso pytest**,
requisito, escenario, aserciones esperadas, resultado observado y evidencia.
Esta tabla agrupa requisitos; no suma ensayos repetidos como casos nuevos.
PASS/FAIL/BLOCKED/NOT RUN son resultados de pruebas; los gates son decisiones distintas.

| ID / requisito | Escenario y resultado esperado | Observado | Estado | Evidencia |
|---|---|---|---|---|
| AC01 acceso diferenciado | Misma pregunta, sujetos distintos | ops: public/ops/injection; hr: public/hr; admin: public | PASS | test_ac01_ac02*, E06/E07 |
| AC02 utilidad autorizada | Obtener contenido útil propio | PINO-101 para ops, NOMINA ficticia para hr | PASS | Mismo test, aserciones de contenido |
| AC03 metadatos protegidos | Ningún texto/título/cita/enlace privado en respuesta no autorizada | Canarios/títulos ausentes | PASS | test_ac03_ac11*, E06/E07 |
| AC04 referencias manipuladas | Solicitar hr/other/restricted/inexistente como ops | 404 en cuatro casos | PASS | test_ac04_ac05* parametrizado |
| AC05 descarga directa | HTTP real autorizado/denegado/inexistente/anónimo | 200/404/404/401; 404 mismo cuerpo | PASS | test_http_real_auth_query_download_and_no_store |
| AC06 injection | Prompt y documento dicen elevar permisos/descargar RRHH | Sin concesión, sin lectura de hr | PASS extractivo | test_ac06*; LLM real NOT RUN |
| AC07 revocación/caché | Revocar grant/token/desactivar; repetir operaciones | Sin doc tras revocar, token nuevo no revive principal deshabilitado | PASS | test_ac07*, sin caché de resultados |
| AC08 historial | Consultar RRHH y leer como ops; repetir consultas | Sólo referencias del propietario | PASS | test_ac08* |
| AC09 automatización | Agotar cuota, token nuevo/reinicio/ventana; petición simultánea | 429 real; restablece siguiente ventana; concurrencia bloqueada | PASS acotado | test_ac09* |
| AC10 auditoría | Permitir/denegar/token inválido; inspeccionar DB | allowed/denied/unauthenticated, sin secreto ni pregunta | PASS | test_ac10* |
| AC11 contexto | Instrumentar deserialización y build_messages | Sólo public/ops/injection; canarios privados ausentes | PASS | test_ac03_ac11*, no inferencia real |
| AC12 retiro | Borrar doc y cambiar versión/política | Sin chunks/grants/referencias accesibles antiguas | PASS | test_ac12*, test_update* |
| AC13 aislamiento org/área/proyecto | Grant explícito con ámbito incorrecto | Sigue 404; otra organización sólo ve evidencia propia/pública | PASS | test_org_area_project* |
| AC14 clasificación | Restringido/desconocida/vacía y publicación retirada | Denegación aun con grant | PASS | test_unknown_classification*, test_public* |
| AC15 autenticación | Expirado, nombre, token inventado, sin token | 401; cuerpo no acepta rol/usuario | PASS | test_expired*, test_http_rejects* |
| AC16 servicio | app consulta pero intenta descargar/historial y se revoca | 200 query, 403 otras, 401 revocado | PASS | test_application* |
| AC17 integridad autorizada | Corromper chunk/documento; consultar usuario ajeno | Error controlado propio, ajeno sigue útil | PASS | test_corrupt_authorized* |
| AC18 superficie HTTP | Traversal, percent-encoding, export, index, user en URL, admin; Host/Origin | 404/403; no bind de red | PASS | test_http_no_alternate*, test_http_origin*, test_server* |
| F02 integridad índice público | Alterar payload/intercambiar vector/escalar/borrar fila | Rechazo antes de evidencia | PASS | test_f02* (4); no firma contra escritor total |
| F04 selección vacía | pages=[] | Error, no ampliar a todo | PASS | test_f04* |
| F06 contratos | Metadata ausente, PDF incompleto, envelope [] | ValueError/RuntimeError traducidos | PASS en muestra | test_f06* |
| F07 filtro | Separar orden peligrosa con salto de línea | Detecta ejemplo | PASS acotado | test_f07*; no detector exhaustivo |
| F09 modelo | Tag cloud | Error sin conexión | PASS acotado | test_f09*; configuración del runtime pendiente |
| ENG01 regresión original | Extracción/fragmentación/vectores/recuperación/citas/UI | 40 originales pasan con activos reales | PASS | E06, tests heredados |
| ENG02 ambiente mínimo | Instalación separada core, pip check y pruebas sin UI/modelo | 85 PASS; pip check exit 0 | PASS | E07/E10 |
| ENG03 dependencias | Scanner full y mínimo | Full:35 avisos Pillow; mínimo:0 avisos conocidos | FAIL full / PASS mínimo | E08, no equivale a ausencia de vulnerabilidades |
| R01–R30 calidad | Reaplicar banco conocido, top-3 y umbral 0,5 | 19 PASS/11 FAIL; detalles por fila | MIXTO | E09; sin nuevo holdout |
| G01–G08 generador | Modelo real: respaldo, contradicción, injection, cifras, abstención | Sin modelo generativo/runtime preparado | NOT RUN | E03 y reporte actual |
| ENT01 identidad empresarial | SSO/MFA y asignación real de identidad | Sólo token de prueba; Restringido bloqueado | BLOCKED | Diseño, S2 |
| ENT02 infraestructura | TLS remoto, cifrado, backups/restauración, alertas, carga sostenida | No ejecutado | NOT RUN | Backlog S2/S4 |

## Cobertura y reproducibilidad

No se estima porcentaje de cobertura ni probabilidad de seguridad. Pytest completo:
88 PASS, incluyendo 48 casos nuevos (37 laboratorio, 11 regresiones). El mínimo
85 PASS excluye tres pruebas de UI/integración semántica. Base antes de cambios:
39 PASS/1 SKIP; después se descargaron/verificaron activos y se ejecutó integración.
Los conteos de suites se solapan: no sumarlos. El banco de 30 preguntas es otra
evaluación con fallos reales, no contradice que la suite de contratos pase.

```bash
FORESTRAG_RUN_INTEGRATION=1 .venv/bin/python -m pytest -q --junitxml=reports/freg001/full-suite.xml
.venv-lab/bin/python -m pytest -q tests/test_pipeline.py tests/test_generation_evaluation.py tests/test_ingestion.py tests/test_security_lab.py tests/test_audit_regressions.py --junitxml=reports/freg001/lab-clean-suite.xml
.venv/bin/python scripts/check_historical_benchmark.py
```

Las pruebas sobre mocks Ollama son sólo contratos. Las pruebas de seguridad usan
canarios ficticios, HTTP local y evidencia previa al ranking/contexto. Ninguna se
aprueba por una frase del chatbot. No se atacó infraestructura externa.
