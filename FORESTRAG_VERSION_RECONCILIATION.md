# ForestRAG — reconciliación FREG-NEXT-001

Fecha: 25-10-2026. Fuente única vigente: [PROJECT_STATUS.md](PROJECT_STATUS.md). Los informes anteriores son cortes históricos; no determinan el despliegue actual.

| Rama recuperada | HEAD observado al inicio | Función |
|---|---|---|
| main | eee8da5035340abef011357e5f85ad7b2fc34bc3 | Corte histórico; no modificar |
| freg-critical-001 | 8088aa567293b021fc2ed265b256ea718c5cb9b9 | Laboratorio FREG-001 histórico |
| freg-public-arch-001 | 4bd230b434f3c65385f3b5930eae28248ccfcc93 | Fuente pública más reciente recuperada |
| gh-pages | e0c6717d97470d5b3a0be1b2b251147c15ea1f57 | Siete archivos de la demo previamente publicada |

El ancestro común de critical y public es main. Public está cuatro commits por delante de main; frente a critical figura cuatro por delante y dos por detrás. No se interpreta el diff de tres puntos como diferencia directa de los dos árboles.

Comparación directa de blobs: critical tiene 71 archivos; public, 147. Hay 46 idénticos, 25 modificados, 76 sólo en public y ninguno exclusivo de critical. security_lab.py, security_http.py y test_security_lab.py son idénticos en ambas ramas. Los cambios FREG-002 se reconocen por ONNX directo, locks e índice con ancla externa. Los resultados históricos de esos incrementos se conservan como históricos.

## Recuperación local

La carpeta inicial estaba vacía. git clone falló por conectividad. Se recuperaron los 147 archivos de un SHA fijo por el conector y se comprobó cada hash de blob Git: 147/147 coincidentes. No se recuperó un checkout anterior de Work con modificaciones sin publicar. No se afirma haberlas encontrado.

El repositorio local se creó como snapshot de recuperación; su commit raíz local no es el SHA remoto ni pretende reconstruir toda su historia. Los cambios remotos se crean con el padre remoto verdadero mediante GitHub, sin force ni cambios a main. FREG-SAH-001 usa un worktree/rama local independiente; su código nuevo no se publica automáticamente.

## Componentes separados

- Código fuente: commit en freg-public-arch-001, registrado en el recibo vigente.
- Aplicación: demo-0.2.0-rc.1.
- Recuperación: bm25-metadata-alias-v1; encoder léxico de compatibilidad conservado, no modelo semántico.
- Corpus: synthetic-2026-10-24-v1, sin cambios de contenido.
- Política pública: public-synthetic-only-v1.
- Índice/artefacto: hashes por archivo y entradas de construcción en release.json.
- Despliegue: commit independiente en gh-pages. Los cambios editoriales no equivalen a un nuevo runtime.
- No hay tag estable nuevo; es una versión candidata.

## Integración futura a main, sin ejecutarla

Comparar árboles exactos y contratos de cada componente; separar el cambio público de la ingeniería protegida; comprobar locks, regresión, banco de calidad y exposición de archivos; preparar PR revisable con pruebas y límites; solicitar decisión del propietario. No hacer force push, merge automático ni reescritura de historia. El código SAH debe auditarse y recibir una decisión de integración específica.

## Reversión pública

Revertir código mediante un nuevo commit descendiente en gh-pages, conservando el corpus y política actualmente aprobados. No mover la rama a un paquete antiguo si eso reintroduciría documentos retirados. Para este incremento el corpus no cambió: puede conservarse el paquete previo como referencia, pero debe verificarse su compatibilidad con el manifiesto y política actuales antes de servirlo. Validar hashes, catálogo, abstención y móvil después de cualquier reversión.
