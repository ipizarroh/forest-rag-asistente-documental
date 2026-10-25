# ForestRAG — estado vigente

**25-10-2026 / FREG-NEXT-001 / presupuesto permanente $0 CLP y USD 0.**

[Demo pública existente](https://ipizarroh.github.io/forest-rag-asistente-documental/). **demo-0.2.0-rc.1 desplegada** tras CI y Pages PASS. **Comprobación externa nueva PASS: 23 checks**, incluidos catálogo, filtros, móvil y hashes de seis assets HTTPS. [Recibo verificable](reports/next001/publication.json).

| Componente | Estado |
|---|---|
| Orientación, catálogo y ámbitos de sugerencias | IMPLEMENTADO y VERIFICADO local: 32 pruebas Node |
| Ranking BM25, normalización y alias limitados | PARCIAL: regresión 14/14; reservado interno 10/12; no es semántica |
| Vista móvil y aceptación gráfica nueva | VERIFICADO en candidata y HTTPS publicado: 1440×1080 y 390×844 emulado |
| FREG-SAH-001 | IMPLEMENTADO y VERIFICADO local en rama separada: 22 pruebas; sin integración/publicación |
| Host y provisión real de la autoridad | NO VERIFICADO; no se modificó Windows |
| LLM real | PENDIENTE / NO VERIFICADO |
| Información confidencial / producción | NO-GO |

Fuente de la aplicación publicada: 247bf18ad65457a0707653e22ee59b7dbde9bee4. Artefacto actual: 6a317f814b0e68d3c04f47fe6df43616dfa76a9b. CI candidata: [40208861784](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40208861784). Despliegue Pages: [40209330492](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40209330492). Ingeniería local: c4b5be3b24b2e730cefbb810004b256dcb19291e.

Base fuente recuperada: 4bd230b434f3c65385f3b5930eae28248ccfcc93. Artefacto anterior: gh-pages e0c6717d97470d5b3a0be1b2b251147c15ea1f57. main sigue en eee8da5035340abef011357e5f85ad7b2fc34bc3 y no se modifica.

## Leer primero

1. [Informe actual](FORESTRAG_FREG_NEXT_001_INFORME.md) y [aceptación UX](FORESTRAG_PUBLIC_UX_ACCEPTANCE.md).
2. [Costo cero](FORESTRAG_ZERO_COST_ARCHITECTURE.md) y [factibilidad IA](FORESTRAG_FREE_AI_FEASIBILITY.md).
3. [Seguridad local](FORESTRAG_SAH_001_IMPLEMENTATION.md) y [reconciliación](FORESTRAG_VERSION_RECONCILIATION.md).
4. [Plan maestro](FORESTRAG_PLAN_MAESTRO_INTEGRADO.md) y [backlog público](FORESTRAG_PUBLIC_DEMO_BACKLOG.md).

Se conservan A1–A5/B, S0–S4, SAH01–18, A2-03/A3-02 y los incrementos anteriores. No se cierra una etapa sólo por documentación.

Los informes previos reflejan cortes históricos. Cualquier frase antigua «no publicado» o «aprobación pendiente» no sustituye este estado. [Estado anterior conservado](docs/history/PROJECT_STATUS_PRE_NEXT_001.md).

Validación posterior al despliegue: commit de pruebas 77b0a86355589c79f23f6eb0324e3eaa72395ae7; [Tests](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40209656319), [candidata](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40209656313) y [HTTPS/UX externo](https://github.com/ipizarroh/forest-rag-asistente-documental/actions/runs/40209656323), todos SUCCESS. La publicación conserva runtime 247bf18 y artefacto 6a317f8; este registro editorial no cambia sus bytes.
