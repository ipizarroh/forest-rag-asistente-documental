# ForestRAG — Plan maestro integrado

## Actualización FREG-PUBLIC-ARCH-001 - 24-10-2026

CR-PUB-001: el nuevo mandato autoriza una candidata pública sintética y auditoría de versiones en paralelo a FREG-SAH-001. Es una excepción explícita de alcance a la recomendación anterior de postergar UI: no expone el backend/lab ni habilita privados. Se conservan A1-A5/B, S0-S4, SAH01-18 y A2-03/A3-02.

- PUB01-07: candidata estática local, manifiesto, pruebas y documentación; ver [backlog de demo](FORESTRAG_PUBLIC_DEMO_BACKLOG.md).
- PUB08-09: publicación/visita externa/operación pendientes de autorización y CI.
- PUB10: semántica/LLM online futura, sin imputar a la búsqueda léxica actual.
- FREG-SAH-001: recuperar base (realizado de forma parcial con checkout003 y regresionesWindows), proteger autoridades (pendiente), retiro y restore completos (pendientes). La eliminación al reconstruir el corpus público sólo cubre un subconjunto.
- Fuentes: [referencias de continuidad privadas omitidas](PUBLICATION.md), [estado de versiones](PROJECT_STATUS.md), [informe actual](FORESTRAG_PUBLIC_DEMO_IMPLEMENTATION.md).

Ninguna nueva rama se publicó ni se modificó main. Los gates previos de piloto/producción permanecen NO-GO.

## Actualización FREG-003 — presentación, 23-10-2026

CR-009: instrucción explícita del propietario cambia la ejecución FREG-003 a README,
navegación y presentación A5. No se elimina ni se declara terminada la propuesta
técnica previa: retiro documental y separación/provisión de confianza siguen en
A2/A3/S2 para el próximo incremento técnico. No se cambia el orden de sus
dependencias ni se inicia generación B.

Entregables: README completo, guía de prueba, vista previa local, comparación,
validación de enlaces/comandos y continuidad. Cierre editorial GO CON CONDICIONES:
revisión interna y pruebas acotadas, sin validación de comprensión por terceros.
FREG-002 y FREG-003 quedan locales; no existe autorización específica para
publicarlos o hacer merge. La CI pública confirmada corresponde a FREG-001.

Actualización FREG-002 (23-10-2026): propietario autorizó publicación001 y ejecutar
la recomendación. A1 avanza a entorno completo compatible, scanner sin avisos
conocidos y lock Linux/Python3.12 probado. A2 incorpora ancla externa obligatoria
y snapshot sin TOCTOU; protección real de configuración/ACL sigue pendiente.
No se reinicia el plan ni se cierran A3/A4/B. La prioridad técnica pendiente es A2/A3/S2:
ciclo de retiro de documentos públicos y separación/provisión verificable de
confianza del host, antes de ampliar datos o habilitar generación real.

CR-006: retirar FastEmbed en favor de ONNX Runtime ya utilizado, conservando pesos
y comparando47 entradas antes de aceptar el cambio. Motivo: quitar la restricción
Pillow<13. CR-007: toda lectura exige huella externa del operador; cambia configuración
de CLI/UI y scripts, con migración documentada. No cambia autorización del laboratorio.
CR-008: publicación mediante conector con árbol verificado y ZIP histórico excluido.

FREG-CRITICAL-001 · 23-10-2026 · plan vigente, dependencias antes que fechas.
Procedencia E00–E11 en el estado maestro. Se conserva literalmente E02 en
docs/history; no se presenta como un plan que ya hubiera sido ejecutado.

## Control de cambios

| Cambio | Motivo y dependencia | Impacto |
|---|---|---|
| CR-001: integrar ForestRAG Security | Mandato E00; nueva frontera documental | Seguridad transversal y S0–S4 identificables |
| CR-002: ejecutar un subconjunto A1/A2/A3 antes de S1 | Dependencias y procedencia condicionan evidencia | A1–A3 parciales; no cierre artificial de A |
| CR-003: separar laboratorio del índice público | Streamlit/CLI no tienen identidad | El laboratorio no habilita corpus privado en UI original |
| CR-004: Restringido bloqueado | Sin proveedor real de autenticación reforzada | Conserva categoría sin fingir MFA |
| CR-005: entorno mínimo sin FastEmbed/UI | Pillow vulnerable y restricción FastEmbed <13 | Demo de permisos puede validarse sin esa dependencia; deuda full permanece |

## Trazabilidad al plan anterior

| Etapa original | Incremento histórico | Integración actual | Estado |
|---|---|---|---|
| Días 1–3, fundación | Base previa | S0 recuperación, fuentes, threat model | VERIFICADO, límites de historia explícitos |
| Días 4–7, recuperación | Base previa | A2 procedencia + S1 SQL autorizado | VERIFICADO acotado; A2 parcial |
| Días 8–10, calidad | A4 | Comparación y evidencia completa con seguridad conservada | PROPUESTO; sólo regresión anterior ejecutada |
| Días 11–14, generación | B | LLM real después de seguridad e integridad estables | BLOQUEADO por dependencias de cierre/validación |
| Días 15–17, robustez | A1/A2/A3 | S1 identidad/prerrecuperación; S2 endurecimiento | Trabajo anticipado justificado; no toda robustez terminada |
| Días 18–21, presentación | A5 | S4 demo controlada, pruebas y relato profesional | Parcial; revisión humana pendiente |

Las estimaciones históricas A1 4–8h, A2 8–16h, A3 6–12h, A4 8–16h y A5 4–8h
(30–60h), B 16–32h, se conservan como propuestas de E02. No son horas consumidas,
compromiso de plazo ni presupuesto aprobado. El nuevo alcance no cabe automáticamente
en los 21 días anteriores; no se ha medido su duración real.

## Secuencia vigente y criterios

1. **S0 / bloque A:** recuperar y contrastar. Cierre con fuentes, hash/commit,
   suite base y separación de resultados históricos. GO para desarrollo local.
2. **A1–A3 + S1 / bloques B–D:** estabilización parcial y laboratorio extractivo
   seguro. Cierre del subconjunto exige misma consulta/roles distintos, SQL previo,
   descargas, aislamiento, revocación, cuotas y evidencia sin secretos. Implementado
   y probado; GO CON CONDICIONES sólo para laboratorio sintético local.
3. **S2 + completar A1/A2/A3:** resolver cadena FastEmbed/Pillow sin forzar versiones
   incompatibles; referencia confiable del índice; ciclo de retiro público; sesiones
   y operador endurecidos. No introducir datos reales para probar estos cambios.
4. **A4 / bloque E:** deduplicación/contexto/ranking, referencias de desarrollo y
   nuevo reservado congelado antes de medir. Banco anterior sólo regresión. No
   escoger ejemplos para simular mejora. Calidad sigue siendo deuda independiente.
5. **B + S3 / bloque E:** runtime/modelo local con licencia y configuración verificadas;
   ejecutar G01–G08 reales y pruebas de autorización/contexto con ese modelo.
6. **A5 + S4 / bloque F:** matriz de evidencia final, instalación por otra persona,
   guion, costo/latencia integral medidos y revisión externa identificada si existe.

## Política transversal

Cada incremento debe mapear requisito → riesgo → diseño → código → prueba → evidencia
→ gate. Cambios de corpus/política invalidan resultados afectados. La clasificación
no concede acceso global: se combinan organización, ámbito y concesiones por recurso.
Humano, bot o aplicación obedecen la misma autorización; scopes de aplicación separados.

No generación, agente, exportación, caché ni nueva interfaz puede saltarse el backend
autorizado. Para nuevas superficies, primero prueba negativa y positiva, después
habilitación. Sin contrato implementado, esa superficie permanece ausente/bloqueada.

## Gates conservados

Portafolio: GO CON CONDICIONES, explicando estado real. Demo sintética local: GO CON
CONDICIONES dentro de la guía. Piloto con datos reales y operación empresarial:
NO-GO. Los umbrales históricos propuestos de piloto (recall ≥85%, completitud ≥80%,
abstención ≥90%) son internos, no política ARAUCO, y no bastan para seguridad legal/
operacional. Pasar pytest o usar OWASP/NIST no certifica cumplimiento.
