## Estado vigente — FREG-NEXT-001, 25-10-2026

Consultar primero [PROJECT_STATUS.md](PROJECT_STATUS.md): es la fuente única de estado y publicación. Presupuesto permanente **$0 CLP / USD 0**; ninguna aprobación pasada permite gastar. Los cortes siguientes conservan la historia, no las condiciones actuales.

NEXT01: orientación/catálogo/filtros implementados; NEXT02: recuperación BM25 probada con límites (32 tests Node, reservado 10/12); NEXT03: publicación condicionada a CI y comprobación externa; NEXT04: FREG-SAH-001 en rama local separada con 18 tests, sin exposición nueva; NEXT05: evaluación de IA gratuita documentada, sin inferencia real; NEXT06: integración futura de ramas preparada, sin cambios a main.

A2-03/A3-02 y S2 avanzan sólo en el laboratorio. B/S3 siguen pendientes de inferencia y evaluación reales; provisión del host y operación empresarial siguen sin verificar. Se preservan todos los IDs A1–A5/B, S0–S4 y SAH01–18 y sus dependencias; no se adjudican cierres individuales sin evidencia.

---

# ForestRAG: seguridad de la demo pública

Fecha: 24-10-2026, America/Santiago. Incremento FREG-PUBLIC-ARCH-001. Proyecto personal independiente; sin información ni infraestructura de ARAUCO. Estados: VERIFICADO (alcance probado), HISTÓRICO, DECLARADO, PROPUESTO, NO VERIFICADO y BLOQUEADO.

## Modelo específico

Activos: integridad del código/corpus, confianza del visitante, cuentaGitHub, recursos de hosting y equipo de build. Datos: exclusivamente tres documentos sintéticos públicos, derivados también públicos. Actores: visitante, automatización, autor de contenido, mantenedor, publicador malicioso/comprometido. Fronteras: editor→build; build→artefacto; publicador→hostingHTTPS; contenido→DOM; consulta→motor local. El laboratorio autenticado y sus archivos no están conectados.

| ID / STRIDE | Escenario | Control y prueba | Riesgo restante |
|---|---|---|---|
| PD01/S | Suplantar al mantenedor | MFA resistente al phishing y revisión de acceso propuestas; commit/manifest visibles | CuentaGitHub yMFA no auditadas |
| PD02/T | Alterar corpus aislado o referencias | SHA/tamaño antes deparseo, schemas, IDs/normas, chunk→sección; pruebasPython/Node/UI10 | Coeditar código+manifest+corpus supera hash; autoridad de publicación debe protegerse |
| PD03/R | Publicación sin trazabilidad | Git/manifest/receipt; aprobación previa | No hay firma, attestation ni auditoría externa |
| PD04/I | Publicar DB, env o docs privados | Directorio allowlist, corpus fail closed, prueba de paquete y rutasUI11 | La revisión del corpus depende del publicador; cualquier contenido estático es descargable |
| PD05/D | Sobrecargar consultas o archivos | 320caracteres/64términos, máx200chunks/12docs/1MB; pacing30/min por pestaña y1consulta activa | Pacing eludible porbot; no límiteglobal. Tráfico de assets depende del proveedor y cuotas |
| PD06/E | Entrar a herramientas administrativas | No API, upload, LLM, toolcalling o conexión con lab | El host de build conserva autoridad y necesita endurecimientoSAH |
| PD07/T/I | XSS desde consulta/documento | textContent, CSPself, nada deinnerHTML/eval; UI05, Node y checkfuente | CSPmeta no soporta todas las directivas de header; headers finales no verificados |
| PD08/T | Inyección directa/indirecta de instrucciones | Texto tratado como dato; sin LLM/agentes/acciones ni cambio de política por consulta | No prueba resistencia de un LLM futuro |
| PD09/T/I | Restore revive datos retirados | Rebuild sinfuente, prueba de ausencia y digestnuevo | No denylist protegida/antirollback ni purgaCDN; SAH03 sigue abierto |
| PD10/I | Filtrar consultas enlogs/cachés | Consulta sólo en memoria del navegador; seisrequests de assets observados, sin tráfico por consulta | Proveedor puede registrar IP/UA al servir assets; no inspeccionados logs del proveedor |
| PD11/T/E | Cadena de suministro | Sin paquetesJS/CDN en runtime; build usa baseline/local y lock; ActionsSHA40 preparados | No scanneractual, instalaciónlimpia ni CIremota ejecutados |

SQLi/SSRF/CSRF de estado servidor no tienen una ruta de ejecución en este subconjunto: no se monta servidorSQL ni acepta URL, cookies de sesión o escrituras. Esto no exonera la seguridad del hosting ni del futuro backend. Abrir PDFs arbitrarios en servidor sigue prohibido.

## Controles ejecutados y límites

- Build deniega privado, clasificación desconocida, synthetic:false, falta de aprobación, estado retirado, campos extra, ids/rutas ambiguos y schema desconocido.
- Payload máximo1MB; JSONmanifest16KB; lectura de stream acotada; vectores positivos/finitos/norma1 y dimensiones512; referencias existentes y texto dentro de la sección.
- Interfaz deshabilitada si el payload no coincide con el hash del manifiesto. Fallo demostrado con una respuesta alterada en un contexto de navegador aislado.
- Selector sólo filtra documentos públicos; no representa identidad o permiso. No contiene selector de roles.
- Fuente completa y citas se obtienen del mismo corpus aprobado. No rutas arbitrarias ni claves en frontend.
- Datos del usuario no se persisten ni se añaden a URL; noanalytics, cookies propias, localStorage o caché de respuestas. Las capacidades del propio navegador/hosting no fueron auditadas.
- Cuota30/min es cortesía de cliente, no una barrera antiIA o antiDDoS. Cualquier persona o IA puede descargar el corpus público completo por diseño. La ausencia de backend evita consumo de inferencia compartido, pero siguen existiendo límites de banda del proveedor.

## Gates previos a publicar

| Gate | Estado actual | Evidencia / acción |
|---|---|---|
| Sólo corpus sintético aprobado y paquete allowlist | PASS local | Python/Node; hashes y contenido del paquete |
| Pruebas funcionales y adversariales del cliente | PASS local | 104Python,15Node,11UI; límites de alcance en informe |
| Escritura/lectura administrativa inexistentes | PASS para artefacto | No backend; revisión y rutas de servidor de prueba |
| UI escritorio/móvil | PASS Chrome emulado | 1440x1080 y390x844; no evaluación móvil física ni WCAG integral |
| Build limpio reproducible y cadena de evidencia | Comprobar en recibo final | Commit, gitbundle, dosbuilds, hashes |
| CI Linux de la candidata | NOT RUN | Publicar rama requiere aprobación; ejecutar antes de promover |
| Cuenta, permisos, Pages, HTTPS y origen final | NO VERIFICADO | Configuración por propietario y visita externa |
| Abuso de assets/monitoreo y presupuesto del proveedor | DISEÑADO | Revisar cuotas/alertas; no servicio pagado activado |
| Autorización primera publicación | PENDIENTE | Requerida expresamente por FREG-PUBLIC-ARCH-001 §11 |

Dictamen: GO CON CONDICIONES para revisión de candidata sintética; publicación bloqueada hasta autorización y checks remotos. NO-GO para incorporar documentos privados, piloto confidencial o producción. El uso de referencias OWASP/ZeroTrust del estudio previo no es una certificación.

PendientesFREG-SAH-001: protección efectiva de política/ancla enhost, retiro/restore con estado vigente, identidad real, reautorización entre canales, logs/backup/IR. No se cierran por haber retirado una fuente del paquete estático.
