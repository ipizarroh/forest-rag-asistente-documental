## Estado vigente — FREG-NEXT-001, 25-10-2026

Consultar primero [PROJECT_STATUS.md](PROJECT_STATUS.md): es la fuente única de estado y publicación. Presupuesto permanente **$0 CLP / USD 0**; ninguna aprobación pasada permite gastar. Los cortes siguientes conservan la historia, no las condiciones actuales.

NEXT01: orientación/catálogo/filtros implementados; NEXT02: recuperación BM25 probada con límites (32 tests Node, reservado 10/12); NEXT03: publicación condicionada a CI y comprobación externa; NEXT04: FREG-SAH-001 en rama local separada con 18 tests, sin exposición nueva; NEXT05: evaluación de IA gratuita documentada, sin inferencia real; NEXT06: integración futura de ramas preparada, sin cambios a main.

A2-03/A3-02 y S2 avanzan sólo en el laboratorio. B/S3 siguen pendientes de inferencia y evaluación reales; provisión del host y operación empresarial siguen sin verificar. Se preservan todos los IDs A1–A5/B, S0–S4 y SAH01–18 y sus dependencias; no se adjudican cierres individuales sin evidencia.

---

# ForestRAG — Backlog priorizado

## Ampliación vigente - FREG-PUBLIC-ARCH-001

Se incorpora [PUB01-10](FORESTRAG_PUBLIC_DEMO_BACKLOG.md) por mandato24-10-2026. No renumera ni cierra A2-03/A3-02, A1-A5/B, S0-S4 o SAH01-18. El orden sigue dependencias: candidata sintética local → aprobación y CI → publicación exacta → visita externa. FREG-SAH-001 continúa para autoridades, retirada y restauración; esas barreras son bloqueantes para privados y no se eluden mediante el frontend estático.

Ver [plan maestro](FORESTRAG_PLAN_MAESTRO_INTEGRADO.md) y [estado de versiones](PROJECT_STATUS.md). Las tablas siguientes son el backlog del corte003/002 conservado.

## Actualización vigente FREG-003 — presentación

La nueva instrucción del propietario asigna este incremento a A5. El alcance
técnico propuesto antes bajo el mismo número se conserva en A2/A3/S2 y se ejecutará
como siguiente incremento técnico, sin renumerar esas tareas ni declararlas cerradas.

| ID | Etapa / seguridad | Objetivo y riesgo | Dependencias / prioridad / complejidad | Archivos | Aceptación y evidencia | Estado / próxima acción |
|---|---|---|---|---|---|---|
| A5-README-003 | A5 / comunicación de límites S4 | Comprensión inicial sin sobreprometer seguridad ni confundir laboratorio/UI | Base FREG-002 / P1 por instrucción del propietario / M | README, guía, informe, continuidad | Enlaces válidos, comandos comprobados, presente/futuro separados, diff, vista previa, valoración razonada | VERIFICADO local; revisión del propietario y prueba de comprensión por tercero pendientes |
| A2/A3/S2 — siguiente técnico | Robustez / confianza | Retiro por fuente y separación real escritor/verificador | A2 de FREG-002 / P0 / A | Catálogo, provisión, pruebas de host | Referencias retiradas inaccesibles, rollback rechazado, ancla no editable por escritor | PROPUESTO; no implementado por el cambio editorial |

Actualización vigente FREG-002, 23-10-2026: A1 verificado para entorno nuevo
Linux/Python3.12 (53 dependencias bloqueadas, scanner sin avisos conocidos, suite97).
A2 implementado/probado bajo amenaza definida de escritor del índice sin control
de ancla; provisión/ACL de host siguen pendientes. Las tareas restantes conservan
sus IDs. FREG-001 publicado y CI3.11/3.12 PASS; FREG-002 permanece local.

FREG-CRITICAL-001 · 23-10-2026. Estimaciones relativas: B/M/A, no horas consumidas.
IDs A1–A5/B preservados de E02; S0–S4 nuevos. Matriz de pruebas y receipt son las
evidencias exigidas, no basta marcar una casilla. Sin fechas comprometidas.

| ID | Etapa original / seguridad | Objetivo y riesgo | Dependencia / prioridad / complejidad | Archivos | Pruebas / aceptación / evidencia | Estado y próxima acción |
|---|---|---|---|---|---|---|
| S0 | Fundación / transversal | Recuperar historia sin inventarla | Ninguna / P0 / M | 8 documentos, docs/history | Commit+hash, plan previo, base; E01–E05 | VERIFICADO; incorporar sólo nueva evidencia trazable |
| A1 | Robustez / S2 | Dependencias aplicables y resolución reproducible; F10/F12 | S0 / P0 / M | pyproject, locks, workflow | Full nuevo, semántica97, scanner0 y lock53; reports/freg002 | VERIFICADO Linux/Python3.12; validar otros ambientes y CI de002 al publicar |
| A2 | Recuperación / S1–S2 | Integridad y procedencia; F02/F11 | S0/A1 / P0 / A | vector_store, preprocessing, receipts | Ancla externa, snapshot y6 pruebas de sustitución/rollback; reports/freg002 | GO CON CONDICIONES para lector; probar provisión/ACL reales en el próximo incremento técnico |
| A3 | Robustez / S1–S2 | Contratos y ciclo documental; F03/F04/F06/F07/F09 | A2 formato / P0 / M | ingestion, generation, CLI, lab | [] no amplía, errores traducidos, retiro/versión, modelo permitido | PARCIAL; ciclo de retiro del snapshot público y parsing aislado |
| S1 | Recuperación/robustez / incremento Security | Identidad de prueba, autorización previa y recursos protegidos | A1–A3 subconjunto / P0 / M | security_lab/http, tests, fixtures | AC01–AC18 positivos/negativos; sin datos prohibidos en contexto; E06/E07 | VERIFICADO en alcance sintético; mantener regresión y límites |
| S2 | Robustez / identidad e infraestructura | Cerrar deuda de autenticidad, sesiones/operador, SSO/MFA | A1–A3/S1 / P0 / A | futuro proveedor de identidad, política/índice, CI | MFA real, scopes revocables, fail closed, backup/restore probado | PROPUESTO; primero FastEmbed/Pillow y ancla de integridad; seguir con identidades |
| A4 | Calidad / transversal | Recuperar evidencia completa y deduplicar; F01/F05 | A2/A3 estables / P1 / M | retrieval, preprocessing, evaluation | Desarrollo comparativo, nuevo reservado congelado; completitud/abstención/citas | PROPUESTO; E09 sólo regresión, congelar nuevo banco antes de ajustar |
| B | Generación / S3 | Validar LLM real y respaldo; F08/F13 | A estable, licencia/runtime / P1 / A | generation, generative tests | G01–G08 reales, respaldo por afirmación, latencia y recursos | BLOQUEADO para cierre; seleccionar runtime/modelo local después de dependencias |
| S3 | Generación/robustez / adversarial con LLM | Injection/exfiltración sin expansión de autoridad | S1/S2/B / P1 / A | context boundary, tests/model harness | Canarios prohibidos nunca en contexto; repetir con modelo real | PROPUESTO; no confundir mock con inferencia |
| A5 | Presentación / S4 | Demo reproducible y relato honesto | A1–A4 según alcance / P1 / M | README, guides, reports | Otra persona reproduce, guion/versiones, diferencias visibles | PARCIAL; paquete local probado, falta revisión humana y publicación aprobada |
| S4 | Presentación / auditoría y operación | Evidencia/gates; retención, observabilidad y desempeño; F14 | S1–S3 según uso / P1 / M | reports, threat model, guía operacional | Matriz por prueba, restauración, incidentes, carga y costos medidos | PARCIAL documental; falta operación y revisión externa |

## Recomendación anterior FREG-002 — ejecutada en su alcance local

Objetivo: terminar la porción crítica de A1 y A2 con la base S1 conservada. Orden:
1) resolver/eliminar la ruta Pillow vulnerable mediante una alternativa compatible
y justificar impacto; 2) repetir semántica y banco conocido con comparación de
vectores/fragmentos; 3) definir quién protege la referencia confiable del índice y
probar sustitución/alteración/retiro; 4) generar lock del entorno elegido y reproducir
desde cero; 5) repetir AC01–AC18 y actualizar gates. Ninguna prueba usa datos reales.

Aceptación: pip check, ausencia de avisos aplicables sin tratamiento explícito,
evidencia reproducible de integridad bajo amenaza definida, regresión funcional y
sin pérdida de aislamiento. No cerrar A completo antes de A4/A5; no iniciar piloto.
SSO/MFA, UI de permisos y LLM se ejecutan después según dependencias, no por estética.

## Propuesta técnica anterior para FREG-003 — pendiente como A2/A3/S2

Completar A3 y el requisito operacional de A2: catálogo/versionado/retiro por fuente
pública y separación verificable entre escritor del índice y configuración del
verificador. Probar cambio de autorización/retiro/rollback con identidades del host
o un contenedor local, sin servicios facturables ni datos reales. Después diseñar
adaptación a proveedor de identidad real S2, conservando denegación de Restringido.
Aceptación: sin referencias retiradas accesibles, ancla no modificable por escritor,
revocación en nuevas solicitudes, suite funcional/de seguridad vigente y evidencia
del límite de host. A4 conserva prioridad de calidad independiente antes de B.
