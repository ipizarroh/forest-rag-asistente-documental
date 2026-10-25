# ForestRAG: backlog integrado de demo pública

Fecha: 24-10-2026, America/Santiago. Incremento FREG-PUBLIC-ARCH-001. Proyecto personal independiente; sin información ni infraestructura de ARAUCO. Estados: VERIFICADO (alcance probado), HISTÓRICO, DECLARADO, PROPUESTO, NO VERIFICADO y BLOQUEADO.

P0/P1 se refieren al uso indicado, no severidad universal. ComplejidadB/M/A relativa. CostoUSD0 significa sin nuevas licencias/servicios, no tiempo de trabajo gratuito. Responsable operativo por asignar al propietario/mantenedor.

| ID | Etapa / proceso / seguridad | Objetivo y riesgo | Dependencia / prioridad / complejidad / coste | Archivos y pruebas | Criterio / evidencia | Estado / próxima acción |
|---|---|---|---|---|---|---|
| PUB01 | S0/A1, P08/P09, SAH01 | Recuperar código y evitar divergencia | Checkout003 / P0 continuidad / M /0 | state,audit,remote-state | SHA/remoto/local separados, anteriores preservados | VERIFICADO parcial; falta cleanfull/semántica/scanner |
| PUB02 | A5/S4, P08/P10, SAH14/18 | Hosting viable sin gasto implícito | PUB01 / P1 demo / M /0 | hosting y fuentesH01-H14 | Coste/recursos/limitaciones fechados | VERIFICADO documental; revalidar al publicar |
| PUB03 | A2/A5, P02/P09, SAH03/05 | Identificar componentes y release | PUB01 / P1 / M /0 | build.py,release-spec,tests | Hashes,commit,corpus,motor,política,dependencias; dosbuilds iguales | IMPLEMENTADO local; recibo final |
| PUB04 | A3-02/S2, P01/P02/P06, SAH03 | Excluir fuente al reconstruir demo | PUB03 / P0 para nuevo paquete / M /0 | corpus,build,test_retirement | Sinid/texto/fragmentos retirados; digestnuevo | VERIFICADO limitado; no cierra restore/cachés/privados |
| PUB05 | A5/S4, P06/P10 | Probar sin instalar y revisar fuentes | PUB03 / P1 / M /0 | web/,browser.json | Consulta/sugerencias/citas/abstención y390px | VERIFICADO Chrome; revisión humana pendiente |
| PUB06 | S2/S4, P04/P10, SAH07/14 | Reducir ejecución/filtración/abuso | PUB03/04 / P0 publicación / M /0 | security,engine,tests | Corpusprivado/alterado rechazado, inputsacotados, sin API/tools | VERIFICADO cliente; cuotas/headers reales pendientes |
| PUB07 | A1/S4, P09, SAH05/18 | CI revisable y promoción controlada | PUB03/06 / P1 / M /0 enrepo público | public-demo-tests.yml, draftdeploy | SHAacciones,readonlytests; CI Linux verde antes de publicar | PREPARADO, NOT RUN remoto |
| PUB08 | A5/S4, P09/P10 | ObtenerURL exacta aprobada | PUB07+propietario / P1 / B-M /0 propuesto | Pagesartifactbranch,guía | Sólo7assets,HTTPS,URLexterna verificada,READMEenlace real | BLOQUEADO por aprobación; no URLinventada |
| PUB09 | S4, P07/P10, SAH14/17 | Medir uso/retirar/revertir sin revivir fuentes | PUB08+SAH03 / P1 / M /0 propuesto | release,rollback,monitoreo | Visita externa,errores/banda,shutdown; vigencia corpus | PROPUESTO; ensayo proveedor pendiente |
| PUB10 | A4/B/S3, P03/P05/P10, SAH11/12 | Semántica/generaciónreal online | A1/A2/A3estables, nuevo banco / P2demo / A /por evaluar | servidorStreamlit/ONNX y banco | RAM/cold/warm/carga; citas y contexto real | PROPUESTO; no atribuir a demo estática |

## Secuencia y dependencia con el plan histórico

Primero preservar código y evidencia, crear candidata pública mínima y validar paquetes. Luego revisar/pedir aprobación de publicación; trasCI y Pages, visitar la URL desde fuera y actualizarREADME. Paralelamente continuarFREG-SAH-001 enA2-03/A3-02: autoridades de confianza, retirada completa y restore. No iniciar privados por haber publicado la demo.

El mandato actual autoriza expresamente trabajoA5 online en paralelo. ControlCR-PUB-001 registra ese cambio frente al roadmap de investigación que desaconsejaba UI antes deSAH. La excepción sólo cubre el artefacto sintético sin backend; no cambia los gates de plataforma protegida.

Siguientes criterios concretos: PUB08 URLexterna HTTPS válida sin registro, tresconsultas y cita comprobadas; SHA/manifest visible igual al aprobado; denegación de rutas privadas; archivos publicadosexactos; prueba de volver al códigoprevio con corpus vigente; registrar cuota y responsable. Si un punto falla, mantenerNO-GO para ampliar exposición.
