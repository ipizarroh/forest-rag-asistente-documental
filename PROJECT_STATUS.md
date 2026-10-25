# ForestRAG: estado de versiones

Fecha: 24-10-2026, America/Santiago. Incremento FREG-PUBLIC-ARCH-001. Proyecto personal independiente; sin información ni infraestructura de ARAUCO. Estados: VERIFICADO (alcance probado), HISTÓRICO, DECLARADO, PROPUESTO, NO VERIFICADO y BLOQUEADO.

**Entrada única de continuidad para esta candidata. No hay demo online publicada ni release estable etiquetada.**

| Ámbito | Referencia | Estado verificable |
|---|---|---|
| GitHub main | eee8da5035340abef011357e5f85ad7b2fc34bc3 | Snapshot histórico; no incorpora FREG-001/002/003 |
| GitHub freg-critical-001 | 8088aa567293b021fc2ed265b256ea718c5cb9b9 | Laboratorio sintético publicado; no plataforma empresarial |
| Local FREG-002 | 8e7a2e8f0a2076b3bdf1564888a8a07f9b59e6d8 | Endurecimiento, ONNX directo; evidencia Linux histórica |
| Local FREG-003 | a4b148f524127d23929074b62d4329bd4b8ee769 | README; evidencia Windows acotada |
| Local FREG-003.1 | Rama freg-003-1-dossier, HEAD a4b148f | Cuatro MD y carpetas sin commit; preservados en el checkout anterior |
| Investigación de seguridad | FREG-SEC-RESEARCH-001, documentos persistentes | Ampliación documental; no implementación empresarial |
| Candidata actual | Rama local freg-public-arch-001, demo-0.1.0-rc.1 | Demo estática sintética implementada; SHA exacto en release.json del paquete y Git |

## Leer primero

1. [Informe del incremento](FORESTRAG_PUBLIC_DEMO_IMPLEMENTATION.md).
2. [Auditoría de versiones](FORESTRAG_VERSIONING_AUDIT.md) y [convenciones](FORESTRAG_VERSIONING_STRATEGY.md).
3. [Arquitectura](FORESTRAG_PUBLIC_DEMO_ARCHITECTURE.md), [hosting](FORESTRAG_HOSTING_EVALUATION.md) y [seguridad](FORESTRAG_PUBLIC_DEMO_SECURITY.md).
4. [Backlog](FORESTRAG_PUBLIC_DEMO_BACKLOG.md) y [plan maestro integrado](FORESTRAG_PLAN_MAESTRO_INTEGRADO.md).

Los identificadores FREG describen incrementos; no prueban que una versión esté publicada. Los ZIP/PDF son snapshots derivados. El código de cada commit y su manifiesto son la referencia reproducible; los documentos externos mantienen su fecha y procedencia. No se renumeran A1-A5/B, S0-S4 ni SAH01-18.

GO CON CONDICIONES para revisión local de la demo. Publicación requiere aprobación y verificación externa. Piloto con información confidencial y producción: NO-GO.
