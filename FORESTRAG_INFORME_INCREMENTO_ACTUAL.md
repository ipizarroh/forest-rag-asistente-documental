# ForestRAG — Informe FREG-003: README y presentación

## Incremento actual - FREG-PUBLIC-ARCH-001

Informe vigente: [FORESTRAG_PUBLIC_DEMO_IMPLEMENTATION.md](FORESTRAG_PUBLIC_DEMO_IMPLEMENTATION.md). Navegación y estado publicado/local: [PROJECT_STATUS.md](PROJECT_STATUS.md). Los apartados siguientes se conservan como historial del corte anterior, sin convertir resultadosLinux en nuevos resultadosWindows.

23-10-2026. Proyecto personal independiente. Revisión editorial y técnica por un
mismo agente; no auditoría externa ni aprobación empresarial.

## A. Resumen ejecutivo

Se rediseñó el README para presentar primero el problema, el valor y el
funcionamiento. Se separan las capacidades actuales del prototipo, el laboratorio
sintético independiente y la experiencia empresarial futura. Se conservan los
documentos técnicos e históricos y se añade una guía de pruebas accesible.

La copia FREG-002 fue restaurada y contrastada; no se cambió código funcional.
Instalación mínima, demo documental y comparación HTTP funcionaron en Windows.
43 pruebas existentes de permisos/integridad pasaron después de resolver
restricciones del directorio temporal. FREG-002 y FREG-003 siguen sin publicar.

## B. Contexto y diagnóstico editorial

Fuente de requisitos: prompt del propietario «FREG-003: rediseño del README y
presentación del proyecto», recibido el 23-10-2026. Se leyó completo desde el
adjunto, no sólo desde un resumen. La entrega FREG-002 fue recuperada íntegramente
del paquete de 550.877 bytes, SHA-256
e38ef771d70c8d5f0481f95f3b8d6ff1f72b310296f224cf58620a44f0bc021e.

Problemas del README anterior:
- La presentación competía desde el inicio con continuidad, huellas, dependencias
  y exclusiones de publicación.
- Los resultados de 40 pruebas históricas aparecían junto a actualizaciones nuevas,
  sin una lectura rápida del estado global.
- Instalación, integración y generación experimental ocupaban gran parte del texto.
- Faltaba describir la experiencia objetivo desde la perspectiva del usuario.
- Había repetición de alcance personal, límites, arquitectura y pasos siguientes.

Comparación: 172 a 114 líneas y 1.228 a 855 palabras. El primer bloque presenta
el valor sin introducir dependencias, hashes ni auditorías.

El nuevo orden es producto → problema → funcionamiento → capacidades presentes →
visión → seguridad → prueba → fundamentos y continuidad. El detalle se consulta
cuando el lector lo necesita. No se aplica Pareto como una proporción matemática.

## C. Estado técnico verificado

| Elemento | Estado |
|---|---|
| Base local recuperada | freg-002-hardening, 8e7a2e8f0a2076b3bdf1564888a8a07f9b59e6d8 |
| Rama de esta ejecución | freg-003-readme, local; commit final en el manifiesto de entrega |
| Rama pública revisada | freg-critical-001; su README contiene el corte anterior |
| Publicación anterior | 8088aa5, referencia conservada en receipt001; CI run40026856745 confirmada success en Python3.11/3.12 |
| Fuente documental | pypdf, MiniLM multilingüe con ONNX Runtime directo, SQLite y CLI/Streamlit |
| Seguridad | Laboratorio separado con datos/identidades inventados; sin integración con la UI pública |
| Generación real | No validada; adaptador Ollama no equivale a inferencia probada |

Los 97 resultados de Linux de FREG-002 se recuperan con sus XML y hashes; no se
declaran como nuevas pruebas Windows. No se consultó el proyecto SSA, documentos
corporativos ni infraestructura ARAUCO.

## D. Planificación consolidada

CR-009 aplica la prioridad editorial A5 del propietario. La sugerencia técnica
anterior para FREG-003 se mantiene abierta en A2/A3/S2. No se borran ni se renumeran
etapas originales; A5 completo tampoco se declara cerrado por renovar el README.

La publicación queda expresamente fuera de esta ejecución. El lector recibe una
copia local basada en FREG-002, no la promesa de encontrar estos cambios en main.

## E. Trabajo realizado

- README reescrito en español, sin insignias ni tablas extensas; flujo visual en
  texto compatible con Markdown, sin dependencias de Mermaid o recursos externos.
- Captura auténtica conservada y revisada. Su leyenda distingue evidencia extractiva
  de una respuesta generada; no se atribuye una nueva ejecución UI a esta imagen.
- Nueva guía docs/probar-forestrag.md: instalación mínima, demo léxica, laboratorio,
  ruta semántica, huella de confianza y límites por plataforma.
- Correcciones documentales acotadas en evaluación, laboratorio, arquitectura y
  limitaciones para que no contradigan FREG-002.
- Estado, plan, backlog, bitácora y matriz actualizados. Informe FREG-002 preservado
  en docs/history/FORESTRAG_INFORME_FREG002.md y en Git.
- Vista previa HTML local y diff contra 8e7a2e8. Sólo cambian documentación y
  artefactos de validación; ninguna dependencia ni comportamiento del producto.

## F. Pruebas y evidencias

| ID | Requisito / escenario | Esperado | Observado | Estado | Evidencia |
|---|---|---|---|---|---|
| DOC01 | Enlaces, imágenes y anclas de documentos modificados | Destinos locales existentes y dentro del repositorio | 37 enlaces locales y 2 externos del README con HTTP200 | PASS | reports/freg003/validation.json |
| DOC02 | Formato Markdown | Parseo, bloques y jerarquía válidos | CommonMark con extensión de tablas; sin HTML complejo en README | PASS | validation.json y vista previa |
| DOC03 | Conservar funcionalidad | Sin diferencias en runtime/dependencias/tests/CI | Comparación con base FREG-002 | PASS | validation.json y diff |
| CMD01 | Instalación mínima + pip check | Resolver núcleo/dev y sin incompatibilidades | Instalada; pip check exit0 | PASS | commands.json |
| CMD02 | Demo CLI del README | Pasajes/citas ficticios, no abstención | exit0; modo extractive | PASS | commands.json |
| CMD03/04 | Inicialización, servidor y cliente HTTP | 5 identidades PASS y descarga denegada 404 | 6 comprobaciones PASS, sin tokens impresos | PASS | commands.json |
| CMD05 | Primer intento de 43 pruebas Windows | Completar suite | 38 PASS, 5 errores de temporales WinError5 | FAIL inicial, conservado | commands-attempt-3.json |
| CMD06 | Repetición en directorio autorizado | 43 PASS, sin cambiar código | 43 PASS,0 FAIL/ERROR/SKIP;10,68s | PASS | windows-security.xml, commands.json |
| HIST002 | Pruebas/equivalencia previas | Evidencia consistente | XML97+hashes y equivalencia47 conservados | HISTÓRICO verificado como artefacto | reports/freg002 |
| UI/SEM | Inferencia semántica e interfaz Windows actuales | Modelo/PDF y UI real | No ejecutadas en esta revisión editorial | NOT RUN | alcance explícito |
| LLM | Generación de respuestas real | Inferencia y respaldo por afirmación | No ejecutada | NOT RUN | backlog |
| HUM01 | Comprensión por lectores externos | Entender el proyecto en primer minuto | Sin estudio de lectores | NOT RUN | revisión pendiente |

No se suman las 43 pruebas actuales a las 97 anteriores: son conjuntos solapados.
La vista previa HTML se generó y se comprobó su estructura. El navegador headless
no produjo captura en este entorno: la inspección visual de esa página queda
NO VERIFICADA. La captura histórica de la aplicación sí fue inspeccionada. No se
certifica el renderizador de GitHub.

Incidencias:
1. El instalador no pudo escribir en su temporal restringido. Se repitió la misma
   instalación usando TEMP/TMP dentro del directorio autorizado; pasó.
2. La conversión CRLF del checkout alteró el fixture hasheado. Dos intentos de demo
   fallaron correctamente. Se restauraron bytes de Git y configuración LF local;
   no se modificó la huella del manifiesto ni se desactivó su validación.
3. Cinco fixtures de pytest fallaron al reemplazar archivos en el temporal
   restringido. La repetición usó --basetemp en el área de trabajo y pasó.

## G. Seguridad y comunicación

El README afirma sólo capacidades presentes en código/evidencia. No ofrece
seguridad absoluta, SSO/MFA existente, uso empresarial, fechas ni productividad.
No publica contraseñas ni tokens. La clasificación Restringido continúa denegada.
No se alteran las fronteras de autorización ni se introduce acceso al LLM.

No se repitió el scanner de dependencias en Windows; la ausencia de avisos de
FREG-002 es un resultado histórico del entorno Linux, no una garantía actual.

## H. Stage-Gate y evaluación editorial

**GO CON CONDICIONES para el incremento editorial local:** requisitos principales
cubiertos, documentación y comandos comprobados. Falta revisión del propietario
y prueba de comprensión con un lector externo.

| Criterio editorial | Puntos | Justificación |
|---|---|---|
| Claridad no técnica | 23/25 | Problema y términos explicados antes del detalle; instalación aún requiere familiaridad básica |
| Comprensión y valor | 18/20 | Usuario, propósito y ejemplo visibles; utilidad organizacional no medida |
| Funcionamiento | 14/15 | Flujo breve y diferencia búsqueda/generación explícita; no hay video guiado |
| Presente y futuro | 15/15 | Prototipo, laboratorio separado y visión futura rotulados; publicación local advertida |
| Presentación y navegación | 9/10 | Jerarquía, captura real y enlaces; sin comprobación en móvil por un tercero |
| Rigor y honestidad | 9/10 | Corpus, entornos y límites explícitos; depende de mantener la documentación vigente |
| Documentación adicional | 5/5 | Guías, arquitectura, evaluación, seguridad y continuidad accesibles |

**Autoevaluación: 93/100.** Juicio editorial interno razonado, no métrica objetiva
de comprensión ni evaluación de terceros. No se declara una nota perfecta.

Portafolio y demostración sintética: GO CON CONDICIONES. Piloto con datos
confidenciales y operación empresarial: NO-GO; este cambio no altera esos gates.

## I. Entregables

README.md completo; docs/probar-forestrag.md; continuidad reconciliada; evidencia
en reports/freg003; vista previa HTML; diff editorial y bundle Git verificable
en la entrega organizada. El manifiesto exterior identifica commit/hashes.
Los paquetes excluyen entornos, PDF, pesos, bases activas, credenciales y el ZIP
histórico de auditoría excluido anteriormente de publicación.

## J. Recomendación técnica

Continuar A2/A3/S2 sobre la base FREG-002: catálogo/versionado/retiro por fuente
pública, y separación real entre quien escribe el índice y quien protege la
referencia del verificador. Aceptación: ancla no editable por el escritor,
referencias retiradas inaccesibles, rechazo de rollback, permisos y regresión
conservados con evidencia del límite del host. Después abordar calidad A4 y
proveedor de identidad antes de generación B.

## DECISIONES QUE REQUIEREN APROBACIÓN DEL PROPIETARIO

Publicar FREG-002 y el README FREG-003 requiere autorización específica, según
el prompt actual. La rama se dejó local. No se requiere aprobación adicional
para los cambios reversibles y verificaciones ya realizados. Merge a main,
datos reales y despliegue siguen fuera del alcance.
