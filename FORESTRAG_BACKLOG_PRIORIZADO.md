# ForestRAG — Backlog priorizado

FREG-CRITICAL-001 · 23-10-2026. Estimaciones relativas: B/M/A, no horas consumidas.
IDs A1–A5/B preservados de E02; S0–S4 nuevos. Matriz de pruebas y receipt son las
evidencias exigidas, no basta marcar una casilla. Sin fechas comprometidas.

| ID | Etapa original / seguridad | Objetivo y riesgo | Dependencia / prioridad / complejidad | Archivos | Pruebas / aceptación / evidencia | Estado y próxima acción |
|---|---|---|---|---|---|---|
| S0 | Fundación / transversal | Recuperar historia sin inventarla | Ninguna / P0 / M | 8 documentos, docs/history | Commit+hash, plan previo, base; E01–E05 | VERIFICADO; incorporar sólo nueva evidencia trazable |
| A1 | Robustez / S2 | Dependencias aplicables y resolución reproducible; F10/F12 | S0 / P0 / M | pyproject, lock, workflow | Instalación limpia + semántica + scanner + pip check; E06–E08 | PARCIAL; resolver FastEmbed/Pillow sin --no-deps incompatible; lock full |
| A2 | Recuperación / S1–S2 | Integridad y procedencia; F02/F11 | S0/A1 / P0 / A | vector_store, preprocessing, receipts | Mutaciones rechazadas + referencia externa protegida; E06/E10 | PARCIAL; diseñar ancla confiable y amenaza de escritor local |
| A3 | Robustez / S1–S2 | Contratos y ciclo documental; F03/F04/F06/F07/F09 | A2 formato / P0 / M | ingestion, generation, CLI, lab | [] no amplía, errores traducidos, retiro/versión, modelo permitido | PARCIAL; ciclo de retiro del snapshot público y parsing aislado |
| S1 | Recuperación/robustez / incremento Security | Identidad de prueba, autorización previa y recursos protegidos | A1–A3 subconjunto / P0 / M | security_lab/http, tests, fixtures | AC01–AC18 positivos/negativos; sin datos prohibidos en contexto; E06/E07 | VERIFICADO en alcance sintético; mantener regresión y límites |
| S2 | Robustez / identidad e infraestructura | Cerrar deuda de autenticidad, sesiones/operador, SSO/MFA | A1–A3/S1 / P0 / A | futuro proveedor de identidad, política/índice, CI | MFA real, scopes revocables, fail closed, backup/restore probado | PROPUESTO; primero FastEmbed/Pillow y ancla de integridad; seguir con identidades |
| A4 | Calidad / transversal | Recuperar evidencia completa y deduplicar; F01/F05 | A2/A3 estables / P1 / M | retrieval, preprocessing, evaluation | Desarrollo comparativo, nuevo reservado congelado; completitud/abstención/citas | PROPUESTO; E09 sólo regresión, congelar nuevo banco antes de ajustar |
| B | Generación / S3 | Validar LLM real y respaldo; F08/F13 | A estable, licencia/runtime / P1 / A | generation, generative tests | G01–G08 reales, respaldo por afirmación, latencia y recursos | BLOQUEADO para cierre; seleccionar runtime/modelo local después de dependencias |
| S3 | Generación/robustez / adversarial con LLM | Injection/exfiltración sin expansión de autoridad | S1/S2/B / P1 / A | context boundary, tests/model harness | Canarios prohibidos nunca en contexto; repetir con modelo real | PROPUESTO; no confundir mock con inferencia |
| A5 | Presentación / S4 | Demo reproducible y relato honesto | A1–A4 según alcance / P1 / M | README, guides, reports | Otra persona reproduce, guion/versiones, diferencias visibles | PARCIAL; paquete local probado, falta revisión humana y publicación aprobada |
| S4 | Presentación / auditoría y operación | Evidencia/gates; retención, observabilidad y desempeño; F14 | S1–S3 según uso / P1 / M | reports, threat model, guía operacional | Matriz por prueba, restauración, incidentes, carga y costos medidos | PARCIAL documental; falta operación y revisión externa |

## Siguiente incremento concreto: FREG-002

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
