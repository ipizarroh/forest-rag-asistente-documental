# ForestRAG - publicación FREG-PUBLIC-ARCH-001-GO

25-10-2026 UTC / 24-10-2026 America/Santiago. Estados: VERIFICADO, HISTÓRICO, DECLARADO, PROPUESTO, NO VERIFICADO y BLOQUEADO. Confianza alta para SHA, resultados y URL contrastados; sin inferir protección empresarial.

## A. Publicación

**PUBLICADO: [Probar ForestRAG](https://ipizarroh.github.io/forest-rag-asistente-documental/).**

Código completo revisado de la candidata y demo estática de siete archivos. Sin cuenta ni instalación. Búsqueda léxica sobre tres documentos ficticios, seis fragmentos, citas, filtro y abstención. Generación real y semántica online pendientes.

## B. Repositorio

| Elemento | Referencia verificada |
|---|---|
| Repositorio público | ipizarroh/forest-rag-asistente-documental |
| Rama fuente | freg-public-arch-001 |
| Fuente de ejecución | 7abc2a7133662ff811bfcdf0c09866cad31cc5ef |
| Revisión de pruebas externas | a4426a611077453031128c31a64e45b9fc45d86c |
| Artefacto, rama gh-pages | e0c6717d97470d5b3a0be1b2b251147c15ea1f57 |
| Árbol del artefacto | 06d46a801bf07fcefae0a97ff738df0ed5e73fbb |
| main conservado | eee8da5035340abef011357e5f85ad7b2fc34bc3 |

La candidata local aprobada ca423062f8e9b83f12365a42248c7e65d6107f45 se transportó mediante snapshots revisados; se conservaron los hashes de ejecución. El historial público original permanece. Los commits locales intermedios y materiales privados conservan su evidencia privada: no se afirma haber publicado cada archivo histórico.

Este informe y ajustes editoriales posteriores pueden tener otro SHA; no alteran release.json del despliegue. Sin merge, cambio de main, force push ni release estable.

## C. CI

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Python 3.11 offline | 106 PASS; 4 integración deseleccionadas | [40154113668](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40154113668) |
| Python 3.12 offline | 106 PASS; 4 deseleccionadas | Mismo run, job separado |
| Python 3.12, entorno completo fijado | 106 PASS; 4 deseleccionadas; pip check PASS | Mismo run, full-locked-environment |
| Construcción pública | 13 Python PASS, 15 JavaScript PASS | [40154113712](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40154113712) |
| Chromium externo | 12 PASS, sin errores de página | [40154113711](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40154113711) |
| Pages | success | [40153806543](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40153806543) |
| HTTP externo con TLS validado | Seis archivos idénticos | reports/public_go001/external-http.json |
| Inferencia semántica/generativa actual | NOT RUN | Sin extrapolar historia |
| Reversión en el proveedor | NOT RUN | Procedimiento documentado |

Las suites se solapan y no se suman como cobertura. pip check mide compatibilidad, no vulnerabilidades. La inspección indicativa de patrones de secretos cubrió archivos revisados; no es análisis forense del host o de todo el historial.

## D. Seguridad

La primera revisión automática rechazó un snapshot amplio por documentos derivados de una fuente privada y un enlace privado. Se publicó primero un mínimo revisado. Tras la instrucción explícita adicional del propietario, se publicó el código completo revisado, excluyendo íntegramente el snapshot privado y retirando URLs/identificadores privados y metadatos del perfil del host. El payload revisado fue aceptado.

No se publicaron bases locales, credenciales, modelos descargados, el archivo histórico de auditoría ni información interna de ARAUCO. El despliegue contiene .nojekyll, index.html, style.css, app.mjs, engine.mjs, corpus.json y release.json.

Corpus sintético público aprobado, esquema/hashes verificados, textContent, consultas en memoria, sin herramientas ni API de escritura. Rutas de backend examinadas: 404. POST al corpus rechazado. El límite por pestaña es eludible y no impide extracción masiva. Un corpus público puede descargarse por personas o bots.

## E. URL

https://ipizarroh.github.io/forest-rag-asistente-documental/

Obtenida del despliegue y comprobada con HTTP 200, validación TLS normal y comparación de bytes. No se dedujo sólo del nombre del repositorio. homepage del repositorio queda sin actualizar: esta conexión no expone esa operación. El enlace real sí está en el README de la rama publicada.

## F. Navegador

Prueba 2026-10-25T02:21:48.896Z, contexto sin autenticación en runner GitHub, Chromium, escritorio 1440x1080 y móvil emulado 390x844.

Se verificaron apertura, consulta sugerida y cita, abstención, entrada hostil sin ejecutar código ni transmitir la pregunta, filtro, ritmo por pestaña, ausencia de errores, vista y consulta móvil, corpus alterado bloqueado, rutas sin backend/escritura y seis archivos HTTPS idénticos. Casos: reports/public_go001/browser-external.json.

Chrome local negó github.io con ERR_NETWORK_ACCESS_DENIED; no se alteraron políticas del equipo. HTTP sí funcionó y la prueba externa CI pasó. Safari, Firefox, teléfonos físicos, carga masiva y disponibilidad continua: NOT RUN.

## G. Documentación

README, guía pública, estado, continuidad, plan, backlog, bitácora y versiones actualizados con evidencia. Los cortes anteriores se conservan como históricos.

La demo complementa el prototipo local: laboratorio, SQLite, ONNX y CLI están en el código; no se exponen mediante Pages.

## H. Versión, gate y reversión

demo-0.1.0-rc.1; corpus synthetic-2026-10-24-v1; motor lexical-sha256-512-v1; política public-synthetic-only-v1.

| Ámbito | Dictamen |
|---|---|
| Portafolio y demo pública sintética | GO CON CONDICIONES |
| Laboratorio sintético local | GO CON CONDICIONES, regresión CI; sin identidad empresarial |
| Host Windows, MFA y cuentas del propietario | NO VERIFICADO |
| Piloto confidencial real | NO-GO |
| Producción empresarial | NO-GO |

Reversión: identificar SHA activo; ante exposición, deshabilitar Pages; corregir mediante nueva revisión o reconstruir código anterior con corpus/política vigentes. Repetir CI y visita externa antes de promover. No se ensayó revertir el proveedor. Las copias públicas descargadas no se pueden revocar.

## I. Límites y evidencias

Tres documentos ficticios y recuperación léxica no demuestran calidad general, SSO/MFA, autorización empresarial integrada, seguridad del host ni fidelidad de un LLM. No se garantiza funcionar al 100% en todo dispositivo, red o navegador.

Evidencias: reports/public_go001/ci.json, browser-external.json y external-http.json; pruebas y workflows versionados. Los registros de GitHub conservan resultados y SHA. Las omisiones privadas no se sustituyen por resultados inventados.

## J. Siguiente incremento

FREG-SAH-001, A2-03/A3-02: autoridad confiable de configuración/índices, retiro documental, invalidación de canales y restauración sin reactivar información retirada. Aceptación: pruebas positivas/negativas con corpus sintético, revocación por solicitud, canales sin referencias retiradas y restore seguro conservando regresión.

PUB09 mantiene ensayo de reversión y monitoreo. PUB10, semántica/LLM online, depende de calidad, capacidad y controles: requiere desarrollo y validación, no sólo subir archivos. Sin compras ni datos empresariales.

## Decisiones que requieren aprobación del propietario

Ninguna adicional para esta publicación ya autorizada. No se solicita merge a main, recursos pagados ni información real.
