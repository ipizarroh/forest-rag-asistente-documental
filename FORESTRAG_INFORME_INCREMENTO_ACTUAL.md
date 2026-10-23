# ForestRAG — Informe ejecutivo-técnico del incremento

FREG-CRITICAL-001 · 23 de octubre de 2026 · corte local de esta ejecución.
Autoría técnica: un mismo agente con perspectivas integradas, sin auditor externo.

**Nota de publicación posterior al corte:** el propietario aprobó publicar la rama.
La publicación excluye el ZIP histórico rechazado por revisión automática; éste
permanece en la entrega descargable original. Código y evidencia nueva conservan
trazabilidad mediante `reports/publication001/receipt.json`. Los apartados siguientes
describen el corte anterior a la aprobación, no el estado de publicación posterior.

## A. Resumen ejecutivo

Se recuperó el plan y la auditoría anterior, se contrastó GitHub y se implementó
un laboratorio sintético de autorización documental, acompañado de correcciones
acotadas de integridad/ingesta y pruebas. Hay trabajo técnico ejecutado: **88 pruebas
PASS**, incluidas **48 nuevas**; entorno mínimo independiente **85 PASS**. Los
conteos se solapan. El banco de calidad anterior conserva **11 fallos de 30**.

El backend decide permisos antes de recuperar payloads y preparar contexto.
Usuarios de Operaciones, RRHH, administrador limitado, otra organización y una
aplicación reciben distinta evidencia. Descargas, historial, revocación y cuotas
tienen pruebas reales. No hay datos confidenciales reales ni llamadas generativas.

Limitaciones principales: tokens sólo de prueba, sin SSO/MFA; Restringido bloqueado;
la UI histórica sigue pública; checksum no protege frente a reescritura total del
host; el entorno completo conserva 35 avisos Pillow. Piloto real/producción NO-GO.

## B. Recuperación de contexto

Se revisaron mensajes visibles, resúmenes de contexto conectado, los cinco commits
Git accesibles, los 42 archivos originales, documentación/código/pruebas/workflow,
el plan de presentación y el ZIP histórico. Tres copias del plan son idénticas;
se conserva una copia con hash. ZIP: 42 entradas, CRC correcto y 41 hashes verificados.
Fuentes E00–E11 y niveles de confianza: [estado maestro](FORESTRAG_ESTADO_MAESTRO_Y_CONTINUIDAD.md).

No se recuperó historial íntegro de conversaciones distintas, archivos no encontrados
ni evidencia de correos. Los resúmenes son secundarios, no sustituyen pruebas.
No se accedió a archivos, datos o credenciales de SSA Arauco ni a sistemas corporativos.

## C. Estado técnico verificado

- Remoto original: `main`, **eee8da5035340abef011357e5f85ad7b2fc34bc3**, sin cambios
  posteriores al corte auditado al recuperar esta sesión.
- Rama local: **freg-critical-001**. Commit de implementación:
  **783272010deab841f2a10592248eacbb82c5f5c9**. El commit de empaquetado/documentación
  final se identifica en `DELIVERY_MANIFEST.json` exterior al snapshot.
- Linux x86_64/Python 3.12.14. No se publicó la rama, no se hizo merge y no corrió
  GitHub Actions para estos cambios. Commit local de autor técnico identificado como
  agente; no se atribuye revisión/aprobación humana.

Ruta pública: **pypdf**, normalización, chunks por página, MiniLM multilingüe 384D,
SQLite y coseno; CLI/Streamlit. El prompt decía PyMuPDF: se registra la discrepancia.
Se descargaron/verificaron PDF FAO y cinco archivos del modelo; no se incluyen en ZIP.

Ruta nueva: API HTTP loopback + sesiones opacas en SQLite + capacidades + política
por organización/área/proyecto/recurso + chunks versionados + baseline léxico 512D
+ pasajes extractivos. No se mezcla esa DB con el índice público. Ollama sigue
sin inferencia real validada; mocks sólo prueban contrato.

## D. Planificación consolidada

Se preservaron los días 1–21, A1–A5 y B del plan recuperado. CR-001–CR-005 integran
seguridad transversal S0–S4 y explican el adelanto de robustez. A1/A2/A3 sólo se
cierran parcialmente; S1 es un subconjunto coherente de laboratorio, no cierre
de la ruta empresarial. [Plan](FORESTRAG_PLAN_MAESTRO_INTEGRADO.md) y
[backlog](FORESTRAG_BACKLOG_PRIORIZADO.md) mantienen dependencias/aceptación/evidencias.
No se inventaron horas ejecutadas, fechas de entrega ni aprobaciones anteriores.

## E. Trabajo realizado

| Archivos | Cambio y propósito |
|---|---|
| src/forestrag/security_lab.py | Identidades de prueba, sesión/TTL/revocación, autorización SQL previa, documentos/versiones, grants, descargas/historial, cuotas/auditoría |
| src/forestrag/security_http.py | API local de tres rutas, Bearer, límites, Host/Origin, no-store, errores sin metadatos privados; sin administración remota |
| src/forestrag/vector_store.py, preprocessing.py | Schema2, asociación checksum/payload/vector, ID derivado, norma e inventario; escritura atómica conservada |
| ingestion.py, generation.py | Rechazar pages=[], PDF incompleto controlado, normalizar saltos de línea, envelope [] controlado, tag cloud rechazado |
| pyproject.toml, requirements-lab-linux-py312.lock | pypdf6.21.2; lock core con hashes por plataforma; no forzar conflicto Pillow/FastEmbed |
| tests/test_security_lab.py, test_audit_regressions.py | 37 casos de laboratorio + 11 regresiones, incluyendo HTTP/socket y frontera antes del contexto |
| scripts/demo_security.py, check_historical_benchmark.py, build_execution_evidence.py | Demo sin imprimir tokens, banco conocido reproducible, receipts/matriz por caso |
| README, docs/roadmap.md, docs/seguridad.md, app/streamlit_app.py, docs/security-lab.md | Alcance visible y separación UI pública/laboratorio, reproducción |
| 8 documentos FORESTRAG_*, docs/history, reports/freg001 | Continuidad, plan, amenazas, permisos, pruebas, backlog, decisiones y resultados |

No se borró historia. El plan/ZIP original están preservados byte por byte. No se
añadieron herramientas por prestigio, servicios de pago ni infraestructura externa.

## F. Resultados de pruebas

| Ejecución | Resultado observado | Evidencia |
|---|---|---|
| Base antes de editar, sin activos semánticos | 39 PASS, 1 SKIP, exit0 | reports/freg001/baseline.json |
| Suite completa con PDF/modelo reales | 88 PASS, 0 FAIL/SKIP, 12,67 s en última ejecución | reports/freg001/full-suite.xml |
| Entorno mínimo limpio, reinstalación lock con hashes | 85 PASS, 0 FAIL, 8,71 s tras reinstalación | reports/freg001/lab-clean-suite.xml |
| Casos nuevos incluidos en las suites | 48 PASS: 37 seguridad + 11 regresiones | test-cases.json y tests fuente |
| pip check full/mínimo | exit0 ambos | execution-receipt.json |
| Scanner pip-audit2.10.1, full | 35 avisos, todos Pillow12.3.0; exit1 por hallazgos | dependency-audit-full.json |
| Scanner mínimo | 0 avisos conocidos; exit0 | dependency-audit-lab.json |
| Demo HTTP real cinco identidades/descarga denegada | Respuestas diferenciadas y 404 sin canario | http-demo.json |
| Banco anterior 30 preguntas conocidas | 19 PASS / 11 FAIL | retrieval-regression.json, cada caso |
| Subconjunto final histórico, reejecutado | Pertinencia11/14; completo10/14; abstención5/6 | Misma evidencia, no nuevo holdout |
| Generación real G01–G08 | NOT RUN | Modelo/runtime generativo no preparados |
| SSO/MFA, TLS remoto, backup/restore, carga sostenida | BLOCKED o NOT RUN según matriz | Diseño/backlog; no capacidad empresarial validada |

Los XML, JSON por prueba y comandos de [matriz](FORESTRAG_SECURITY_TEST_MATRIX.md)
permiten reproducir resultados. El scanner full incluye herramientas de preparación
y auditoría; no equivale exactamente al árbol mínimo del producto. No se agregan
sus avisos al total histórico ni se presentan como explotaciones.

La actualización del parser cambió espacios (R11 antes de `)`) e índices de palabras.
El primer intento se detuvo; se realinearon referencias sólo si letras/puntuación
sin espacios eran idénticas, antes de puntuar. Se conserva el banco original y se
registran referencias afectadas. No hay prueba causal de mejora por seguridad ni
validación en documentos nuevos. Completitud observada: 10/14 en el antiguo
subconjunto final y 12/20 sobre todas las preguntas respondibles del banco conocido.

## G. Estado de seguridad

**Implementado y probado en laboratorio:** token de prueba no elegido por prompt,
expiración/revocación, capacidad separada para servicio, denegación por defecto,
organización/área/proyecto + grant, SQL antes de payload, protección de títulos/citas/
descarga/historial, versiones/retiro, no caché de respuesta, cuota persistida,
concurrencia y registro local sin tokens ni preguntas. Canarios confidenciales
no aparecen en respuestas/contexto de usuarios no autorizados en la muestra.

**Diseñado/pendiente:** SSO/MFA real, autenticidad externa de índices/políticas,
cifrado en reposo/TLS remoto, operador endurecido, alertas, detección conductual,
retención/restauración, cadenas full sin dependencia vulnerable y pruebas LLM reales.
Restringido permanece bloqueado. Cuenta/host comprometidos y copias ya descargadas
son riesgos residuales. Checksum coeditable y un prompt no los resuelven.

Se consultaron fuentes primarias OWASP GenAI2025, ASVS estable5.0.0, NIST800-207,
MITRE y Microsoft ARTEX del21-10-2026; correspondencia concreta en el
[threat model](FORESTRAG_SECURITY_THREAT_MODEL.md). Se extraen principios de scopes
y revocación de aplicaciones, sin extrapolar ataques Microsoft365 a esta arquitectura.
No hay certificación, conformidad integral ni pentest independiente.

## H. Dictamen Stage-Gate

| Alcance | Dictamen | Razón |
|---|---|---|
| Continuar desarrollo local autorizado | GO | Fuentes recuperadas y subconjunto técnico probado |
| Preparación de portafolio | GO CON CONDICIONES | Declarar límites/fallos, conservar evidencia y no exagerar capacidades |
| Demostración sintética local | GO CON CONDICIONES | Seguir guía, entorno mínimo, sin exposición remota ni datos reales; accesibilidad desde navegador externo a Work no validada |
| Piloto con información real | NO-GO | Identidad/integridad/infraestructura/operación/licencias y autorización de datos pendientes |
| Operación empresarial | NO-GO | Sin pruebas operacionales, disponibilidad, respuesta a incidentes ni garantías necesarias |
| Generación real | NO VERIFICADO | No se ejecutó LLM real |

## I. Entregables

Los ocho documentos obligatorios se encuentran en la raíz del snapshot; pruebas,
logs estructurados y receipts en `reports/freg001/`; originales en `docs/history/`;
guía en `docs/security-lab.md`. El paquete descargable incluye fuente versionada,
diff contra eee8da5, bundle Git para restaurar la rama y manifiesto con hashes.
Excluye entornos virtuales, PDF, pesos, DB de ejecución y credenciales. No hay
enlace de rama GitHub nueva porque no se publicó.

## J. Recomendación técnica

**FREG-002:** terminar la deuda crítica A1/A2 manteniendo S1. Primero resolver la
dependencia FastEmbed/Pillow con alternativa compatible y evidencia de equivalencia
semántica; después proteger la referencia de integridad bajo amenaza definida;
reproducir instalación limpia/lock y repetir seguridad/recuperación. Aceptación:
sin avisos aplicables sin tratamiento, alteraciones rechazadas, retiro verificable,
suite funcional y permisos conservados. Después A3/A4, B/S3 y A5/S4 según dependencias.

## DECISIONES QUE REQUIEREN APROBACIÓN DEL PROPIETARIO

**Publicar estos cambios en GitHub (push y, si se desea, PR).** El código y las
evidencias ya están preparados localmente para revisión. El mandato prohíbe hacer
push público/merge sin aprobación expresa; no se realizó ninguna de esas acciones.
No se requiere autorización adicional para el trabajo local ya ejecutado.
