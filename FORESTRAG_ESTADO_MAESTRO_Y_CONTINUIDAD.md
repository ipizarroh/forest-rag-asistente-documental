# ForestRAG — Estado maestro y continuidad

## Actualización FREG-PUBLIC-ARCH-001-GO

VERIFICADO: fuente completa revisada en freg-public-arch-001, ejecución web desde 7abc2a7 y artefacto gh-pages e0c6717. URL https://ipizarroh.github.io/forest-rag-asistente-documental/. CI validó a4426a6: 106 pruebas por entorno Python, 13 de build, 15 Node y 12 externas. main sin cambios. Confianza alta para este alcance; suites solapadas y cuatro pruebas de integración semántica no ejecutadas.

El propietario aprobó rama y Pages y solicitó todos los archivos publicables. Se excluyó el documento de origen privado y se retiraron referencias privadas. No se publican modelos, bases privadas, secretos ni información empresarial. Publicar código no convierte el laboratorio en servicio empresarial.

Procedencia: [FORESTRAG_INFORME_PUBLICACION_GO_001.md](FORESTRAG_INFORME_PUBLICACION_GO_001.md), reports/public_go001/ci.json y browser-external.json. Se conservan FREG-SAH-001, A2-03/A3-02 y los identificadores históricos. Este corte prevalece para publicación; el resto mantiene sus fechas y alcance.

## Estado vigente - FREG-PUBLIC-ARCH-001, 24-10-2026

Entrada de navegación: [PROJECT_STATUS.md](PROJECT_STATUS.md). La cronología inferior se conserva como cortes anteriores, no como estado automáticamente actualizado.

| Procedencia | Afirmación | Estado/confianza |
|---|---|---|
| APIbranches/releases/refs/rulesets, reports/public_arch001/remote-state.json | main eee8da5 y0018088aa5; sin tags/releases públicos observados; reglas según alcance deAPI | VERIFICADO, alta para respuestas obtenidas; no auditoría de cuenta |
| Git local | 0028e7a2e8 y003a4b148f recuperados;003.1 conserva cuatroMD y carpetas sincommit | VERIFICADO, alta;003.1 no cerrado |
| Prompt adjunto FREG-PUBLIC-ARCH-001 | Public demo y gobierno de versiones; sin despliegue/push/main sin permiso | DECLARADO, mandato actual |
| Rama local freg-public-arch-001 | Candidata estática sintética implementada; sin backend/LLM | VERIFICADO, pruebas y fuentes; SHAfinal en recibo/manifiesto |
| XMLPython/TAPNode/browser.json | 104PASS Python (4semánticosdeseleccionados,2UIoriginalexcluidos),15PASSNode,11PASSChrome | VERIFICADO acotado; no fullsemántica ni CIremota |
| Roadmap de investigaciónSEC leído de documento persistente | SAH01-18 y FREG-SAH-001 se incorporan sin renumerar | HISTÓRICO documental; snapshot en docs/history |
| Hosting/protección de cuenta/URLexterna | Pages propuesto; proveedor y credenciales de propietario no configurados | PROPUESTO / NO VERIFICADO |

No se accedió a SSA Arauco ni datos corporativos. No se consideran nuevas pruebas de Windows-host, MFA, revocación empresarial, LLM o scanner. Las diferencias entre main y local, y las limitaciones de versiones se detallan en la [auditoría](FORESTRAG_VERSIONING_AUDIT.md). Confianza externa de índices y retirada protegida siguen pendientes.

## Estado vigente FREG-003 — presentación, 23-10-2026

**VERIFICADO / alta:** se recuperó la entrega FREG-002 `8e7a2e8f0a2076b3bdf1564888a8a07f9b59e6d8`
desde su bundle, verificando SHA-256 del paquete y `git fsck --strict`. Rama de
trabajo nueva: `freg-003-readme`. No se publicaron FREG-002/FREG-003 ni se modificó main.

**DECLARADO / alta:** el propietario asigna FREG-003 al rediseño completo del README.
Sustituye el alcance de ejecución sugerido antes para ese número; las tareas
técnicas A2/A3/S2 permanecen abiertas, con sus identificadores y dependencias.
Origen: prompt «FREG-003: rediseño del README y presentación del proyecto», recibido
en esta conversación el 23-10-2026. Hash del adjunto en reports/freg003/validation.json.

| Afirmación del corte | Estado / confianza | Evidencia |
|---|---|---|
| README renovado, guía breve y navegación hacia documentación técnica | VERIFICADO / alta | README.md, docs/probar-forestrag.md, diff y validación FREG-003 |
| Código funcional, dependencias, pruebas y workflow sin cambios respecto de FREG-002 | VERIFICADO / alta | Comparación Git contra 8e7a2e8; sólo documentación y evidencias nuevas |
| Demo léxica y comparación HTTP con cinco identidades en Windows | VERIFICADO / alta | reports/freg003/commands.json; descarga no autorizada 404, sin imprimir tokens |
| 43 pruebas de permisos/integridad en Windows/Python 3.12.3 | VERIFICADO / alta, acotado | reports/freg003/windows-security.xml; no incluye UI ni inferencia semántica real |
| 97 pruebas de FREG-002 y equivalencia de 47 entradas | HISTÓRICO / alta | Evidencia recuperada reports/freg002, hashes contrastados; no son nuevas ejecuciones Windows |
| Experiencia empresarial integrada, SSO/MFA y generación LLM real | PROPUESTO / NO VERIFICADO | No implementados/validados por este incremento editorial |
| Revisión del README por una persona ajena al desarrollo | NO VERIFICADO | Evaluación editorial interna; no estudio de usuarios |

Incidencias reproducibles: Git convirtió LF a CRLF en la copia Windows y la demo
rechazó correctamente el fixture por hash. Se restauraron los bytes originales
del Git confiable y se fijó la configuración local LF; no se cambió el manifiesto
ni se debilitó la verificación. Instalación y primeras pruebas encontraron
`WinError 5` en temporales restringidos; se usaron directorios autorizados de
trabajo. Fallos e intentos se preservan junto al resultado final.

El alcance sigue siendo portafolio/demostración sintética local con condiciones.
Datos confidenciales reales y operación empresarial siguen NO-GO. Las secciones
siguientes conservan los cortes previos y deben interpretarse con sus fechas.

## Estado vigente FREG-002 — 23-10-2026

La rama pública aprobada `freg-critical-001` está en
`8088aa567293b021fc2ed265b256ea718c5cb9b9`; main permanece en eee8da5.
GitHub Actions run40026856745 terminó success. El ZIP histórico se excluyó tras
rechazo de revisión automática; permanece en la entrega original del propietario.
Correspondencia de publicación: reports/publication001/receipt.json.

FREG-002 se desarrolla localmente en `freg-002-hardening`, desde ese commit público.
El commit técnico de este incremento se registra en reports/freg002/receipt.json;
no se publicó esta nueva rama ni se autorizó merge a main.

| Afirmación actual | Estado/confianza | Evidencia |
|---|---|---|
| FastEmbed retirado; mismos pesos/revisión y tokenización, ONNX Runtime directo | VERIFICADO/alta | semantic-reference.json + semantic-equivalence.json: 47 entradas, error máximo0 |
| 384 dimensiones y contrato de embeddings conservado en muestra | VERIFICADO/alta | Equivalencia + referencia sintética congelada + suite real |
| Pillow13 UI; entorno completo nuevo sin avisos conocidos al corte | VERIFICADO/alta, acotado | reports/freg002/dependency-audit-full.json; no certificación |
| Huella externa obligatoria y SQLite desde bytes verificados | VERIFICADO/alta | tests/test_index_trust.py; docs/index-trust.md |
| Separación real de ACL/provisión de confianza del host | NO VERIFICADO | Precondición de despliegue; tests no crean dos cuentas OS |
| Tokens/permisos/aislamiento del laboratorio | VERIFICADO, misma política | Suite ampliada conserva los37 casos S1 |
| Semántica y calidad del banco conocido | VERIFICADO, limitada | Regresión30:19 PASS/11 FAIL; final11/14 pertinente,10/14 completo,5/6 abstención |
| Lock de runtime/UI/dev/bootstrap | VERIFICADO para Linux x86_64/Python3.12 | requirements-full-linux-py312.lock, instalación separada y locked-suite.xml |
| SSO/MFA, LLM real, TLS remoto, backups y operación | BLOQUEADO/NO VERIFICADO | Sin cambio respecto del corte anterior |

Las pruebas/receipt actuales están en reports/freg002; reports/freg001 es evidencia
histórica y no se sobrescribe. La arquitectura vigente es pypdf→chunks→ONNX Runtime
local→SQLite con ancla externa; el laboratorio de autorización sigue aislado.
F10 se resuelve para el entorno nuevo probado, no para instalaciones antiguas que
conserven FastEmbed/Pillow12. F02 mejora bajo amenaza de escritor del índice sin
control de la configuración; no equivale a resistir un host/proceso comprometido.

## Corte anterior FREG-CRITICAL-001 conservado para trazabilidad

Versión FREG-CRITICAL-001 · corte 23-10-2026 · proyecto personal independiente de
Ignacio Pizarro Hurtado para preparación profesional ante ARAUCO forestal.
Sin afiliación, acceso interno, credenciales o infraestructura de ARAUCO.
SSA Arauco queda fuera del alcance. Este archivo es el estado reconciliado vigente.

## Estados y procedencia

VERIFICADO: inspeccionado/ejecutado en esta sesión. HISTÓRICO: evidencia recuperada,
no resultado nuevo. DECLARADO: instrucción o antecedente del propietario.
PROPUESTO: diseño/backlog sin cierre. NO VERIFICADO: evidencia insuficiente.
BLOQUEADO: dependencia impide el uso indicado. La confianza es sobre la afirmación
acotada, nunca sobre seguridad absoluta. Perspectivas técnicas integradas por un
mismo agente; no doce auditores ni revisión institucional independiente.

| Ref. | Fuente y fecha | Estado/confianza | Alcance |
|---|---|---|---|
| E00 | Prompt FREG-CRITICAL-001 y conversación accesible, 23-10-2026 | DECLARADO/alta | Mandato, exclusiones, nuevos requisitos y autorización local |
| E01 | Git remoto y clon, rama main, eee8da5035340abef011357e5f85ad7b2fc34bc3 | VERIFICADO/alta | Cinco commits, 42 archivos originales; sin commits remotos posteriores al corte |
| E02 | [Plan recuperado](docs/history/PLAN_PRESENTACION_FORESTRAG_ARAUCO.md) | HISTÓRICO/alta | Tres copias idénticas; SHA256 8a2aa4098580c969ed2c63735129021f2f80feadb39143fae97c704277783a21 |
| E03 | [Registro del ZIP original](docs/history/README.md) | HISTÓRICO/alta | Archivo conservado en entrega descargable, excluido del repositorio público; 42 entradas y 41 hashes comprobados |
| E04 | src/forestrag, app, tests, pyproject, workflow originales | VERIFICADO/alta | Arquitectura contrastada con E01, antes de cambios |
| E05 | reports/freg001/baseline.json | VERIFICADO/alta | Base Linux: 39 PASS, 1 SKIP sin activos semánticos al inicio |
| E06 | [Suite completa](reports/freg001/full-suite.xml) | VERIFICADO/alta | Pytest con modelo/PDF reales; resultados por caso |
| E07 | [Entorno mínimo](reports/freg001/lab-clean-suite.xml) | VERIFICADO/alta | Instalación core independiente; regresiones y laboratorio |
| E08 | reports/freg001/dependency-audit-{full,lab}.json | VERIFICADO/alta | Scanner al corte, no prueba de ausencia de vulnerabilidades |
| E09 | [Regresión de recuperación](reports/freg001/retrieval-regression.json) | VERIFICADO/alta | Banco anterior conocido, referencias reconciliadas sólo por espacios |
| E10 | reports/freg001/execution-receipt.json y test-cases.json | VERIFICADO/alta | Entorno, hashes, comandos, resultados y limitaciones |
| E11 | Búsqueda de contexto personal del 23-10-2026 | HISTÓRICO/media | Resúmenes confirman independencia y pendientes, no historial íntegro |

E03 SHA256: fbba88be1b62cc4fc6fc28244f2dc88e411883ae0631669afa4288dcc98098ed.
Los artefactos originales se conservan sin modificar; los informes dentro del ZIP
identifican commit, banco, scanner y restricciones. E02 era propuesta, no ejecución.
El informe de entrega y el manifiesto exterior identifican el commit local final;
base de implementación E01, rama local `freg-critical-001`. No se hizo push/merge.

Actualización de publicación, 23-10-2026: propietario autorizó publicar la rama y
continuar FREG-002. La revisión automática rechazó el archivo ZIP histórico; se
excluye ese binario del repositorio público y se conserva sin modificar fuera
de GitHub. La correspondencia de commits/contenido se registra en
`reports/publication001/receipt.json`. No se autoriza merge a main.

## Objetivo y evolución

HISTÓRICO, alta (README, docs/roadmap.md, E02): construir un asistente documental
forestal trazable con Python, embeddings locales y RAG progresivo como portafolio.
No se midió ahorro, productividad, utilidad industrial ni resultados de contratación.

| Fecha America/Santiago | Commit/etapa | Evidencia y decisión |
|---|---|---|
| 22-10-2026 22:59 | c0b77a5, fundación | E01: estructura, alcance, fuentes |
| 22-10-2026 23:27 | 8aea2a8, prototipo | E01: ingesta/recuperación y pruebas |
| 22-10-2026 23:33 | 5a28c3a, documentación | E01: arquitectura/resultados |
| 22-10-2026 23:35 | 70e5bae, reproducibilidad | E01: instalación limpia/CI |
| 22-10-2026 23:39 | eee8da5, evidencia visual | E01: captura real local |
| 23-10-2026, auditoría y plan | E03/E02 | HISTÓRICO: 14 hallazgos, A1–A5 propuestos; sin correcciones |
| 23-10-2026, continuidad actual | FREG-CRITICAL-001 | VERIFICADO: rama local, estabilización parcial y laboratorio probado |

## Arquitectura verificada

**Ruta pública original, E04/E06:** pypdf → páginas físicas/rótulos → normalización
NFKC → chunks de 55 palabras, solape 10 y presupuesto 120 tokens → FastEmbed 0.9.0,
MiniLM multilingüe 384D → SQLite → coseno/top-3/umbral 0,5 → pasajes con citas.
CLI y Streamlit; Ollama opcional separado, sin herramientas. No se ejecutó generación
real. La búsqueda exacta recorre un índice pequeño, no es ANN industrial.

**Ruta sintética nueva, E06/E07:** HTTP loopback → token opaco de prueba validado en
SQLite → capacidad de operación → SQL con organización/área/proyecto/clasificación
y concesión documental → chunks/versiones autorizados → baseline léxico 512D →
pasajes y enlaces internos protegidos. Misma política para usuarios y aplicaciones.
El contexto preparado se inspecciona en pruebas; no se entrega a un LLM real.
Políticas, ingesta y revocación son del operador local confiable; sin API administrativa.

VERIFICADO: el código nuevo detecta alteraciones de payload/vector/inventario y
exige schema 2; índices previos requieren reconstrucción explícita. Los checksums
coeditables NO autentican un índice ante un escritor malicioso. E06, F02 parcial.

## Resultados y límites históricos

HISTÓRICO, alta, E03: suite original 40/40 en Windows; banco 58 casos distintos:
30 recuperación + 20 adversariales ejecutados, 8 generativos NOT_RUN. Resultado
agregado 28 PASS/22 FAIL, no porcentaje de precisión. Subconjunto reservado original:
pertinencia 10/14, evidencia completa 8/14, abstención 5/6. Red Team 9 PASS/11 FAIL.
63/63 pasajes normales con procedencia estructural, no prueba de respaldo semántico.
Scanner histórico: 57 avisos pypdf, 35 Pillow, 12 pip; no 104 explotaciones reales.

VERIFICADO, E06/E07/E09: suite ampliada 88 PASS, suite mínima 85 PASS; 48 casos
nuevos de seguridad/regresión incluidos, no adicionales al total 88. Banco conocido
30: 19 PASS/11 FAIL; antiguo final 11/14 pertinente, 10/14 completo, 5/6 abstención.
El parser cambia espacios, índices de palabras e IDs de algunos chunks: E09 conserva
la reconciliación. No atribuir causalmente una mejora a seguridad ni llamarlo nuevo holdout.

## Funcionalidad y discrepancias

| Tema | Estado actual | Evidencia/limitación |
|---|---|---|
| Extracción/embeddings/CLI/Streamlit | VERIFICADO, acotado | E06, corpus de dos páginas |
| Motor PDF | VERIFICADO: pypdf, no PyMuPDF | E04/pyproject; discrepancia con E00 histórico |
| Identidad/autorización | VERIFICADO sólo en laboratorio | E06/E07; CLI/Streamlit público sigue sin identidad |
| Restringido/MFA | BLOQUEADO | Denegación constante; no MFA simulado |
| Integridad criptográfica contra escritor del host | PROPUESTO | A2 no cerrado; firma/referencia externa pendiente |
| Vigencia/retiro | VERIFICADO sólo laboratorio | Versiones, revocación y borrado lógico de canales; índice público es snapshot manual |
| Generación real/fidelidad | NO VERIFICADO | Adaptador y mocks no sustituyen inferencia |
| Corpus amplio, OCR, tablas, SAP/GIS/cloud/agentes | PROPUESTO o fuera de alcance | Sin evidencia de implementación |
| CI de esta rama | NO VERIFICADO | No publicada; suite local no es ejecución GitHub Actions |

## Hallazgos F01–F14 reconciliados

| ID | Estado del hallazgo tras ejecución | Evidencia / siguiente acción |
|---|---|---|
| F01 | Abierto | E09 mantiene fallos; A4 con banco nuevo congelado |
| F02 | Parcial | E06 rechaza mutaciones; falta autenticidad con referencia protegida |
| F03 | Parcial | Laboratorio invalida versiones/borrado; snapshot público manual |
| F04 | Corregido en caso observado | E06: pages=[] ya no amplía alcance |
| F05 | Abierto | Sin deduplicación interdocumental |
| F06 | Parcial | Metadata ausente, PDF incompleto y envelope [] controlados; no sandbox/parser exhaustivo |
| F07 | Corregido en caso observado | Normalización de espacios; filtro sigue no exhaustivo |
| F08 | Abierto | IDs válidos no demuestran que las afirmaciones estén respaldadas |
| F09 | Parcial | Tag cloud rechazado; no política demostrada del servidor Ollama |
| F10 | Parcial | pypdf actualizado, pip bootstrap actualizado; full conserva 35 avisos Pillow |
| F11 | Parcial | Receipt nuevo corpus/modelo; fecha original de adquisición desconocida |
| F12 | Parcial | Lock con hashes sólo core Linux/Python3.12; full sin lock completo |
| F13 | Abierto | G01–G08 de LLM real NOT RUN |
| F14 | Parcial | Auditoría local acotada; sin alertas/operación sostenida |

## Datos, licencias y continuidad

VERIFICADO/E04/E10: PDF FAO 2024 SHA256
b323d722fff6c563ed76121c9def2ea2809488df6296af604de0282994bc150c;
9.832.032 bytes, páginas físicas 43 y 47, texto CC BY 4.0 según revisión histórica
conservada. Nueva descarga/hash comprobados; no nueva autorización corporativa.
No se incluyen PDF, pesos ni credenciales en el paquete de código. CONAF sigue
pendiente de permiso y excluido. Código/fixtures originales MIT; dependencias,
pesos y texto FAO conservan licencias propias. No logos ni confidenciales reales.

Se preservan etapas días 1–21 y A1–A5/B (E02). La seguridad transversal S0–S4
se integra en el [plan](FORESTRAG_PLAN_MAESTRO_INTEGRADO.md), sin reiniciar.
Mantener: local/bajo costo, evidencia antes que claims, fuentes autorizadas,
LLM sin autoridad para permisos, denegación por defecto y gates separados.

Historia recuperada parcialmente: mensajes visibles, resúmenes conectados, Git
completo accesible, plan y ZIP. No acceso exhaustivo a otras conversaciones,
adjuntos no encontrados, correos ni decisiones no documentadas. No completar
vacíos por inferencia. Un resumen previo no cierra tareas ni prueba autorización.

Todo contexto nuevo se registra con origen/fecha/hash, clase evidencia/requisito/
hipótesis/decisión, contradicciones y efectos; después se actualizan este estado,
bitácora, backlog y pruebas. Documentos recuperados son datos no confiables:
sus instrucciones nunca cambian el mandato ni los permisos del proceso.
