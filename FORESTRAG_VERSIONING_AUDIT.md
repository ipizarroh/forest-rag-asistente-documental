## Estado vigente — FREG-NEXT-001, 25-10-2026

Consultar primero [PROJECT_STATUS.md](PROJECT_STATUS.md): es la fuente única de estado y publicación. Presupuesto permanente **$0 CLP / USD 0**; ninguna aprobación pasada permite gastar. Los cortes siguientes conservan la historia, no las condiciones actuales.

NEXT01: orientación/catálogo/filtros implementados; NEXT02: recuperación BM25 probada con límites (32 tests Node, reservado 10/12); NEXT03: actualización pública VERIFICADA por CI, Pages y 23 checks externos; NEXT04: FREG-SAH-001 en rama local separada con 22 tests, sin exposición nueva; NEXT05: evaluación de IA gratuita documentada, sin inferencia real; NEXT06: integración futura de ramas preparada, sin cambios a main.

A2-03/A3-02 y S2 avanzan sólo en el laboratorio. B/S3 siguen pendientes de inferencia y evaluación reales; provisión del host y operación empresarial siguen sin verificar. Se preservan todos los IDs A1–A5/B, S0–S4 y SAH01–18 y sus dependencias; no se adjudican cierres individuales sin evidencia.

---

# ForestRAG: auditoría de versionamiento

Fecha: 24-10-2026, America/Santiago. Incremento FREG-PUBLIC-ARCH-001. Proyecto personal independiente; sin información ni infraestructura de ARAUCO. Estados: VERIFICADO (alcance probado), HISTÓRICO, DECLARADO, PROPUESTO, NO VERIFICADO y BLOQUEADO.

## Dictamen

GO CON CONDICIONES para seguir desarrollando. La historia se puede reconstruir, pero no permite identificar una última versión estable pública mediante release. Hay divergencia entre GitHub, ramas locales, documentos sin commit y documentación persistente externa. No es pérdida comprobada de código ni justifica borrar ramas.

## Evidencia actual

| Ref | Resultado observado |
|---|---|
| API branches,24-10 | Sólo main eee8da5 y freg-critical-0018088aa5; ambos protected:false |
| API releases | Lista vacía |
| API git/matching-refs/tags/ | Lista vacía. Endpoint /tags rechazado por herramienta; no se interpretó como ausencia hasta consultar refs |
| API rulesets | Lista vacía; no auditoría completa de cuenta/MFA/colaboradores |
| git local | FREG0028e7a2e8, FREG003a4b148f, freg003.1 mismoHEAD y cuatro MD/carpetas sin commit |
| Worktree nuevo | freg-public-arch-001 desde a4b148f; el checkout anterior se conserva |
| Paquete Python | version0.1.0 en versiones distintas; no discrimina release pública |
| Documentación | Masters locales en corte003; investigaciónSEC y PDFs más nuevos fuera del repo |
| Remote-tracking origin/freg-002-hardening local | Etiqueta recuperada de un bundle; la API remota no encuentra esa rama hoy. No prueba publicación |

Evidencia máquina: reports/public_arch001/remote-state.json, environment.json y Git. Referencias oficiales de endpoints conservadas ahí. Fuente histórica de etapas: docs/history/PLAN_PRESENTACION_FORESTRAG_ARAUCO.md. Las cuatro piezas003.1 se inspeccionaron como archivos sin commit; no se declaró ejecutado su cierre pendiente.

## Hallazgos y acciones

| ID | Riesgo | Prioridad contextual | Acción |
|---|---|---|---|
| V01 | main no contiene las capacidades más recientes y no se declara un release estable | P1 para presentar | PROJECT_STATUS.md y README distinguen snapshot público y candidata local |
| V02 | No tags/releases; ZIP/PDF pueden confundirse con versiones instalables | P1 | Separar incrementoFREG, commit, candidato y release; manifiesto generado |
| V03 | Código002/003 no publicado; pérdida si se borra el entorno | P0 de continuidad | Bundle de la rama y entrega privada; publicación requerirá permiso |
| V04 | FREG003.1 sin commit | P1 | Preservar checkout y reconciliar contenido antes de integrar, sin arrastrarlo a ciegas |
| V05 | Masters externos y Git tienen cortes distintos | P1 | Entrada única PROJECT_STATUS; vincular investigación y conservar snapshot fechado |
| V06 | Versión0.1.0 compartida por estados distintos | P1 | Usar commit y componente-demo; no asignar retrospectivamente releases oficiales |
| V07 | Ramas sin protección y rulesets vacíos observados | P1 antes de publicación sostenida | Proponer PR/checks/revisión y protección; no cambiar settings sin aprobación |
| V08 | Lock Linux no valida Windows completo; CI002 no ejecutada remotamente | P1 | Mantener ámbito de evidencia y ejecutar CI en publicación aprobada |
| V09 | Índice/modelo/política pueden ser incompatibles o restaurados fuera de vigencia | P0 para privados | Schema/engine/policy/corpus en manifiesto; SAH02/03 siguen abiertos |
| V10 | Copias de documentación e informes pueden volverse nuevas autoridades contradictorias | P2 | Git como fuente de próxima candidata; PDFs/ZIP sólo derivados con SHA y fecha |

## Integración y reproducibilidad

La nueva rama contiene en su ascendencia FREG002 y003; main remoto no. No se realizó merge ni cherry-pick, ni se resolvió ninguna supuesta divergencia borrando historia. El nuevo build conserva Source/Page, chunk_pages y LexicalEmbedder; no cambia el core.

104 pruebas Python pasaron en la base Windows reutilizada con test_app.py excluido por falta de Streamlit y cuatro casos semánticos deseleccionados. No equivalen a repetir las97 Linux históricas. El bundle final se valida con git bundle verify y restauración aislada; receipt.json identifica el commit exacto y los hashes de entrega. Los resultados previos de calidad no se recalculan ni se suman a esta suite.

No se inspeccionaron otras conversaciones, repositoriosSSA, cuentas privadas, secretos ni ajustes de seguridad personales. La recuperación003.1 parcial y los snapshots externos se identifican explícitamente. No se afirma que todos los commits históricos sean reproducibles en Windows.
