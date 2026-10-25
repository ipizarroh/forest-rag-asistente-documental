# ForestRAG — Informe ejecutivo-técnico FREG-002

23-10-2026 · proyecto personal independiente de ARAUCO forestal y de SSA Arauco.
Ejecución local por el mismo agente; sin auditoría institucional independiente.

## A. Resumen ejecutivo

Se publicó la rama aprobada FREG-001 y se ejecutó el siguiente incremento local.
FREG-002 retira FastEmbed, conserva los embeddings mediante ONNX Runtime directo,
actualiza Pillow para UI e incorpora verificación del índice contra una huella
externa del operador antes de parsear SQLite. **97 pruebas PASS**, también en una
instalación separada con lock de53 paquetes y hashes; scanner final sin avisos
conocidos en ambos entornos nuevos. No equivale a ausencia de vulnerabilidades.

Se conserva el aislamiento documental y los tokens de prueba del laboratorio.
SSO/MFA, separación real de permisos del host, generación LLM y uso con datos
reales siguen pendientes. La calidad de recuperación no mejora por este cambio.

## B. Recuperación y continuidad

Base: entrega local0019ce6b11 y snapshot público8088aa5, con plan A1–A5/B,
línea S0–S4 y los ocho documentos ya recuperados. No se reinició el proyecto.
El propietario aprobó ejecutar la recomendación y publicar001 en esta conversación.
Los límites de recuperación histórica permanecen en el estado maestro; no se
consultaron documentos de SSA ni sistemas corporativos.

La revisión automática rechazó subir el ZIP histórico a GitHub por seguridad de
su contenido público no demostrada. Se excluyó, sin reintento ni publicación por
partes; el original permanece en la entrega descargable anterior. La publicación
minimiza descripciones de advisories, conservando IDs/versiones/conteos.

## C. Estado técnico verificado

| Referencia | Estado |
|---|---|
| main público | eee8da5035340abef011357e5f85ad7b2fc34bc3, sin merge |
| Rama publicada | freg-critical-001, 8088aa567293b021fc2ed265b256ea718c5cb9b9 |
| Árbol público preparado/verificado | b924ed21887a40bbbdbf7691843ba5dc7d189c54 antes del receipt de publicación |
| CI publicado | run40026856745, success; Python3.11 y3.12 PASS |
| Rama nueva local | freg-002-hardening, desde8088aa5 |
| Commit técnico002 | 66d378d; SHA completo en reports/freg002/receipt.json |
| Entorno probado | Linux x86_64, Python3.12.14, ONNX Runtime1.31.0, tokenizers0.23.3 |

Git CLI no tenía credencial de escritura; el conector publicó un snapshot con
árbol idéntico al preparado. Los commits remotos difieren de los locales originales;
la correspondencia está documentada. FREG-002 no se publicó ni se hizo merge.

## D. Planificación consolidada

CR-006 retira FastEmbed por la restricción Pillow<13; CR-007 exige huella externa
y evita reabrir una ruta mutable; CR-008 registra publicación/exclusión del archivo.
A1 queda verificado para el entorno nuevo acotado. A2 tiene lector/protocolo
probados bajo amenaza definida, con provisión/ACL reales pendientes. A3/A4/B no
se cierran por extrapolación. Continúan los IDs y dependencias originales.

## E. Trabajo realizado

- `embeddings.py`: usa directamente el mismo ONNX/tokenizer fijado por revisión y
  hashes, CPU2 hilos, media de tokens reales y normalización. No carga código remoto.
- `pyproject.toml`: dependencias semánticas directas; UI Pillow13.0.0. Lock completo
  Linux/Python3.12 con53 paquetes y hashes, incluido bootstrap.
- `vector_store.py`: el constructor emite huella del temporal terminado; el lector
  exige referencia externa, limita lectura, verifica SHA256 antes de SQLite y usa
  snapshot en memoria de los mismos bytes. Checksums/IDs/norma internos se conservan.
- CLI, fixtures, prueba de integración y benchmark adaptados al contrato. Demo
  autoriza directamente la huella de su propia construcción confiable, no archivos externos.
- Seis pruebas nuevas de confianza y tres de runtime; referencia sintética congelada
  para regresión, guías de provisión/reproducción y job CI con lock configurado.
- Ocho documentos maestros reconciliados; resultados001 preservados y resultados002
  en carpeta propia. No se incluyeron datos reales confidenciales ni credenciales.

## F. Resultados de pruebas

| Prueba | Esperado | Observado / estado | Evidencia |
|---|---|---|---|
| Suite completa | Mantener regresión y nuevos contratos | 97 PASS,0 FAIL/SKIP | full-suite.xml |
| Instalación con hashes separada | Mismo resultado funcional | 97 PASS,0 FAIL/SKIP,15,58 s | locked-suite.xml |
| Equivalencia antes/después | atol/rtol1e-6, mismos tokens | 47 entradas384D, error máximo0 | semantic-reference/equivalence.json |
| Ancla/sustitución/TOCTOU/rollback | No leer evidencia alterada o retirada | 6 PASS | test_index_trust.py y XML |
| Runtime/padding/presupuesto | Contrato y valores válidos | 3 PASS | test_semantic_runtime.py y XML |
| Permisos sintéticos anteriores | Conservar S1 | 37 casos incluidos PASS | test_security_lab.py |
| pip check | Sin incompatibilidades | exit0 | receipt.json |
| Scanner completo nuevo | Sin avisos conocidos pendientes | 0 en entorno nuevo y0 en instalación bloqueada | dependency-audit-{full,locked}.json |
| Regresión de recuperación | Conservar medición | 19 PASS/11 FAIL; final11/14 pertinente,10/14 completo,5/6 abstención | retrieval-regression.json |
| GitHub Actions001 | Compatibilidad/suite/demo | success, jobs3.11/3.12 | publication-ci.json |
| CI002, Windows, SSO/MFA y LLM real | Requieren otros entornos/alcance | NOT RUN/BLOCKED | backlog |

Las suites se solapan; no sumar97+97. El banco de30 preguntas es conocido y conserva
fallos, no nuevo holdout. Comparación47:33 chunks+11 preguntas+3 textos sintéticos.
La referencia adicional de3 textos se calculó con FastEmbed0.9.0 antes de aceptar
la sustitución y se entrega para regresión del runtime directo.

Incidencias: dos aserciones nuevas se corrigieron por umbral esperado/texto del
error, sin modificar la política. El bootstrap conservó metadata pip25 junto al
módulo26 y el scanner detectó12 avisos; se reinstaló con hash, se repitió una vez
en el entorno de comprobación y se verificaron53 distribuciones únicas y scanner0.
No se eliminaron metadatos ni se ocultaron avisos manualmente. Preflight documentado.

## G. Estado de seguridad

El atacante del índice puede cambiar DB y sidecars pero no la referencia, código
o proceso del operador. En ese alcance, sustituir un índice con checksums válidos
ya no basta. Los bytes usados para SQL son exactamente los verificados: sin ventana
de reapertura de ruta. El operador debe construir desde fuentes confiables y
proteger la provisión/vigencia de la huella; las pruebas no acreditan esa separación
mediante cuentas OS distintas. No se implementó PKI ni defensa contra host comprometido.

La DB de políticas sigue dentro de confianza del operador. Restringido continúa
bloqueado; humanos y aplicaciones obedecen la misma autorización. No se agregó
LLM, herramienta de red, exportación ni otra superficie privilegiada.

## H. Dictamen Stage-Gate

| Alcance | Dictamen | Condición |
|---|---|---|
| Incremento local002 | GO CON CONDICIONES | Evidencia satisfactoria para amenaza/entorno definidos; ACL/provisión y otros sistemas pendientes |
| Portafolio/demo sintética | GO CON CONDICIONES | Explicar límites, configurar huella y usar datos autorizados |
| Publicación001 | GO, ejecutada | Archivo histórico excluido; CI PASS; sin merge |
| Publicación002 | Pendiente aprobación | Preparada localmente, aún no subida |
| Piloto real/operación empresarial | NO-GO | No se derivan de suite/scanner ni de aprobación de publicación |

## I. Entregables

Código versionado local, ocho documentos actualizados, guías, locks y evidencias
por caso en reports/freg002. La entrega incluye snapshot/bundle/patch y manifiesto;
excluye pesos, PDF, entornos, DB activa, credenciales y ZIP histórico bloqueado.
Commit final de entrega en manifiesto exterior; no se presenta como commit publicado.

## J. Recomendación técnica

FREG-003: ciclo de catálogo/versionado/retiro por fuente y separación verificable
del escritor de índice respecto de la configuración del verificador. Aceptación:
referencias retiradas inaccesibles; ancla no modificable por el escritor; rollback
rechazado; permisos conservados; evidencia real de límites del host. Seguir con
proveedor de identidad S2 y calidad A4 antes de generación B.

## DECISIONES QUE REQUIEREN APROBACIÓN DEL PROPIETARIO

Publicar el nuevo incremento FREG-002. La aprobación recibida para publicar la rama
FREG-001 ya se ejecutó. No se requiere ninguna otra autorización para el trabajo
local realizado. Merge a main y uso de datos reales permanecen fuera del alcance.
