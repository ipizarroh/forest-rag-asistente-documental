## Estado vigente — FREG-NEXT-001, 25-10-2026

Consultar primero [PROJECT_STATUS.md](PROJECT_STATUS.md): es la fuente única de estado y publicación. Presupuesto permanente **$0 CLP / USD 0**; ninguna aprobación pasada permite gastar. Los cortes siguientes conservan la historia, no las condiciones actuales.

NEXT01: orientación/catálogo/filtros implementados; NEXT02: recuperación BM25 probada con límites (32 tests Node, reservado 10/12); NEXT03: actualización pública VERIFICADA por CI, Pages y 23 checks externos; NEXT04: FREG-SAH-001 en rama local separada con 22 tests, sin exposición nueva; NEXT05: evaluación de IA gratuita documentada, sin inferencia real; NEXT06: integración futura de ramas preparada, sin cambios a main.

A2-03/A3-02 y S2 avanzan sólo en el laboratorio. B/S3 siguen pendientes de inferencia y evaluación reales; provisión del host y operación empresarial siguen sin verificar. Se preservan todos los IDs A1–A5/B, S0–S4 y SAH01–18 y sus dependencias; no se adjudican cierres individuales sin evidencia.

---

# ForestRAG: informe FREG-PUBLIC-ARCH-001

**Corte histórico de implementación local.** La publicación fue aprobada y ejecutada después. [FORESTRAG_INFORME_PUBLICACION_GO_001.md](FORESTRAG_INFORME_PUBLICACION_GO_001.md) contiene URL real, SHA y CI. Sus apartados sobre aprobación pendiente o ausencia de publicación describen el corte anterior.

Fecha: 24 de octubre de 2026, America/Santiago. Proyecto personal independiente de ARAUCO. Estados: VERIFICADO, HISTÓRICO, DECLARADO, PROPUESTO, NO VERIFICADO y BLOQUEADO.

## A. Viabilidad online

Se implementó una candidata funcional de demo pública limitada: tres documentos sintéticos, seis fragmentos, consultas libres o sugeridas, filtro documental y citas a secciones. Funciona en navegador mediante HTTP local. No se desplegó en Internet y no existe una URL pública verificada.

Esta candidata corresponde a las alternativas D y B del mandato: una demostración limitada con índice preconstruido. El prototipo semántico Streamlit/ONNX conserva su ruta local y necesita una validación de recursos y compatibilidad adicional antes de alojarlo.

## B. Hosting recomendado

GitHub Pages para el paquete estático, con coste nominal USD0 dentro de sus límites publicados para repositorios públicos y dominio predeterminado. No se creó ni configuró un servicio.

Se compararon Streamlit Community Cloud, Hugging Face Spaces, Render y GitHub Pages. La matriz completa está en FORESTRAG_HOSTING_EVALUATION.md. La documentación actual de Hugging Face indica que crear nuevos Spaces Docker/Gradio requiere un plan de pago, con una excepción específica de ZeroGPU; que CPU Basic no cobre por hora no significa que crear un Space de cómputo sea gratuito.

## C. Experiencia del visitante

Cuando se publique, una persona podrá abrir el enlace sin instalar programas ni crear una cuenta, elegir una pregunta o escribirla, revisar pasajes y abrir su documento de origen. Se explica que los datos son ficticios y la búsqueda es léxica. No se presenta como una conversación generada por un LLM.

La interfaz se probó en Chrome headless a 1440x1080 y 390x844. Se inspeccionaron visualmente las capturas internas de escritorio, resultados y móvil. No hubo evaluación con usuarios ni dispositivos físicos.

## D. Arquitectura y seguridad

El build Python reutiliza Source/Page, chunk_pages y LexicalEmbedder existentes. El cliente JavaScript calcula vectores léxicos de512 dimensiones y coseno. Nueve consultas contrastan sus términos/vectores frente a Python con tolerancia1e-6; no prueban equivalencia exhaustiva para todo Unicode.

La recuperación requiere coincidencia de dos términos de contenido distintos, o uno cuando la consulta sólo contiene uno. Esto reduce coincidencias debidas a stopwords o colisiones, pero no aporta comprensión semántica.

El artefacto contiene siete archivos y aproximadamente31KB antes de compresión; el tamaño y el SHA finales figuran en receipt.json. No monta API, SQLite servidor, uploads, herramientas, claves, modelo semántico o LLM. El laboratorio de autorización está separado.

Se valida corpus, esquema, digest, dimensión, norma y referencias antes de mostrar evidencia. Se usa textContent y CSP; se acotan entradas y descargas; se admite una consulta activa por pestaña y un pacing de30 consultas por minuto. Ese pacing es eludible y no constituye una cuota global antiabuso. El proveedor mantiene sus propios límites de recursos y tráfico.

## E. Trabajo implementado

Se creó una copia de trabajo aislada en C:/workspace/forestrag-public-arch-001/repo, rama freg-public-arch-001, desde a4b148f. Los cuatro documentos y carpetas FREG-003.1 sin commit permanecen en el checkout anterior.

Se añadieron build, corpus sintético, especificación de release, interfaz HTML/CSS/JS, servidor exclusivo de revisión en loopback, pruebas Python/Node/navegador, CI de lectura y un borrador inactivo de despliegue. No se modificaron los módulos centrales, dependencias del producto, main ni servicios del host.

La inspección visual detectó resultados de baja pertinencia por palabras comunes. El primer filtro, de una coincidencia de contenido, aún admitía una coincidencia genérica; una regresión lo detectó. Se exigió el mínimo descrito arriba y se repitieron las pruebas afectadas. Son ejemplos conocidos, no un benchmark reservado ni una nueva medición de precisión general.

## F. Auditoría de versionamiento

GitHub sigue mostrando main en eee8da5 y freg-critical-001 en8088aa5. Las listas consultadas de releases y refs de tags están vacías; branches devuelve protected:false y rulesets una lista vacía. Esto no equivale a auditar MFA, colaboradores o todos los ajustes de cuenta.

FREG-002 en8e7a2e8 y FREG-003 en a4b148f están locales. FREG-003.1 mantiene el mismo HEAD y documentos sin commit. El remote-tracking local origin/freg-002-hardening recuperado no acredita publicación de esa rama. La versión Python0.1.0 tampoco distingue estos estados.

Se añadieron PROJECT_STATUS.md, auditoría, estrategia, changelog y manifiesto automático. FREG identifica un incremento; demo-0.1.0-rc.1 identifica una candidata del componente de demo; SHA identifica el código; publicación es un estado adicional. No se crearon tags o releases retrospectivos.

## G. Plan de releases

Flujo: desarrollo, pruebas, revisión de seguridad/corpus, candidata, aprobación, publicación y visita externa.

Primera ruta sin modificar main: publicar la rama fuente tras autorización, ejecutar CI, revisar el resultado y publicar una rama de artefacto con los siete archivos exclusivamente. Configurar Pages para esa rama requiere permisos administrativos y aprobación.

El borrador de Actions está fuera de .github/workflows, con extensión .example. Para activarlo mediante workflow_dispatch deberá incorporarse a la rama por defecto mediante una autorización adicional. El entorno de despliegue y sus revisores deben configurarse: nombrarlo en YAML no lo protege automáticamente.

La reversión funcional debe reconstruir el código anterior con corpus/políticas vigentes. No se debe republicar ciegamente un paquete viejo con documentos retirados. La demo estática no puede revocar copias públicas descargadas ni impedir un rollback ejecutado por su publicador.

## H. Pruebas realizadas

| Ejecución | Resultado | Alcance |
|---|---|---|
| Python offline Windows | 104PASS,4 deselected;13.15s | 91 regresiones anteriores y13 pruebas nuevas; dos tests Streamlit no se recolectaron por faltar esa dependencia |
| Node24.22.1 | 15PASS finales | Motor real, nueve referencias Python, validaciones, límites, digests, pacing y ranking |
| Chrome / Playwright1.62.1 | 11PASS | Escritorio, móvil, cita, abstención, input hostil, cero requests por consulta, filtro, pacing, tamper y rutas |
| Edge | Dos intentos BLOCKED | Falló el arranque en este entorno; no se cambiaron políticas de Windows; Chrome permitió continuar |
| pip check | PASS | Entorno existente compatible; no instalación limpia |
| Construcción repetida | PASS | Bytes idénticos con mismo estado, incluyendo manifiesto |
| Semántica y LLM | NOT RUN | Cuatro casos semánticos deseleccionados; ninguna inferencia generativa |
| CI/proveedor/URL externa | NOT RUN | Preparados, sin despliegue |

Evidencia: reports/public_arch001/python-tests.xml, node-tests.txt, lexical-reference.json, browser.json, environment.json, acceptance.md y remote-state.json. El test de navegador portable está en public_demo/test_browser.cjs; requiere Playwright1.62.1 y un navegador compatible. No agrega una dependencia a producción.

El TAP registra una muestra de100 consultas calientes y RSS del proceso Node completo. Es un microbenchmark local sobre seis fragmentos, no SLA ni medida de ONNX, móvil o hosting. Los valores de la corrida final permanecen en su evidencia para evitar mezclar mediciones de versiones distintas.

## I. Plan consolidado y dictamen

Se actualizan estado, plan, backlog, bitácora, informe y matriz con enlaces al corte actual, preservando los apartados anteriores. Se recuperó el roadmap de investigación SEC desde el documento persistente y se conserva como snapshot fechado. Sus estados BLOCKED históricos no se presentan como actuales.

Se mantienen A1-A5/B, S0-S4, SAH01-18 y A2-03/A3-02. Se añaden PUB01-10. CR-PUB-001 permite trabajar en una demo sintética aislada en paralelo al endurecimiento, sin levantar las barreras para información privada.

| Ámbito | Dictamen |
|---|---|
| Ingeniería y revisión local de la demo sintética | GO CON CONDICIONES: falta CI y validación externa |
| Publicación automática inmediata | NO-GO: no aprobada ni configurada |
| Laboratorio sintético de autorización | GO CON CONDICIONES: regresiones locales, sin exposición |
| Host, ACL, MFA y cuenta del propietario | NO VERIFICADO |
| Piloto con información real confidencial | NO-GO |
| Producción empresarial | NO-GO |

## J. Próximo paso

Revisar la candidata y autorizar la publicación de la rama fuente y del artefacto. Después, ejecutar CI Linux, revisar el gate, habilitar Pages con el directorio exacto y visitar externamente su URL HTTPS. Confirmar consultas, citas, versión y rutas. Sólo entonces incorporar al README el enlace real «Probar ForestRAG».

FREG-SAH-001 continúa con autoridades de confianza, manifiesto de vigencia/retirada, invalidación entre canales y restauración que no reactive accesos. La eliminación de una fuente al reconstruir este paquete estático sólo cubre un subconjunto; no cierra A2-03/A3-02 ni habilita datos privados.

## Decisiones que requieren aprobación del propietario

1. Publicar la rama candidata y una rama de artefacto con contenido sintético, sin merge a main.
2. Habilitar GitHub Pages y realizar el primer despliegue público después de CI y revisión. El mandato adjunto, sección11, exige autorización expresa antes de esa publicación.
3. Sólo si se elige Actions: incorporar el workflow a la rama por defecto y configurar el entorno protegido. La primera ruta manual no lo necesita.

No se requieren compras, datos internos ni cambios de Windows para revisar esta candidata.

## Entregables y trazabilidad

Siete documentos requeridos, masters actualizados, código, configuración, pruebas, bundle Git, artefacto publicable, manifiesto de archivos y recibo de entrega con SHA exacto. El PDF ejecutivo y el ZIP facilitan la revisión. El commit final se identifica en Git, receipt.json y release.json; no se inventa un SHA en el documento que se está registrando.

Las capturas se utilizaron sólo para QA interno y quedan fuera del paquete. No se incluyeron archivos SSA, datos corporativos ni registros privados del host. Los hashes prueban correspondencia con una referencia; no garantizan autenticidad de un publicador comprometido ni seguridad empresarial.
