# ForestRAG — FREG-SAH-001, implementación de ingeniería

Fecha: 25-10-2026. Rama local separada `freg-sah-001`. **No publicada ni integrada a la demo.** Resultado: GO CON CONDICIONES para laboratorio sintético, no cierre empresarial de S2.

## Implementación

Se conserva SecurityLab y su autorización SQL previa a leer fragmentos, aislamiento por organización/ámbito, capabilities, descargas protegidas, historial y revocación. La clase optativa SealedSecurityLab añade una autoridad del operador en un directorio distinto del índice.

La referencia fija una generación y huella de esquema, identidades, áreas/proyectos, capabilities, sesiones, concesiones, metadatos/versiones y checksums de fragmentos. Antes de operar se coteja con una transacción SQLite. Un escritor limitado al índice no puede sustituir políticas, recalcular checksums y aceptar un retroceso contra la referencia vigente. La huella no autentica por sí sola al operador: su procedencia y protección son supuestos explícitos.

Alta/modificación/reclasificación produce una versión inactiva pendiente de revisión. Aprobar exige la versión exacta. Toda modificación invalida concesiones y referencias previas. La retirada desactiva publicación y borra fragmentos, concesiones e historial. La eliminación lógica vacía contenido y conserva el número de versión; no equivale a borrado forense de SQLite ni de respaldos.

Los respaldos de contenido sólo contienen documentos y fragmentos: no identidades, grants, sesiones ni historial. La restauración verifica bytes contra una huella externa antes de SQLite y sólo reproduce contenido/fragmentos que corresponden a la versión y política vigentes. Omite documentos retirados, eliminados o antiguos. No importa permisos ni decisiones de un respaldo.

## Evidencia nueva

18 pruebas funcionales ejecutadas con unittest y NumPy 2.3.5. Cubren revisión exacta, reclasificación, falta de autorización, aislamiento, restricción por defecto, contexto sin canarios prohibidos, retirada, concesiones/sesiones revocadas, identidad deshabilitada, versiones obsoletas, borrado lógico, reparación positiva de contenido vigente, rollback completo del índice incluso tras reiniciar, alteración de políticas/esquema, falta de autoridad, snapshot sin tablas de identidad y hash incorrecto antes de parsear.

También se ejecuta una regresión del SecurityLab anterior. La suite histórica pytest completa sigue siendo una obligación distinta: no se afirma que 18 pruebas sustituyan todos sus contratos.

Se corrigieron manejadores SQLite abiertos en los tests y se usó un directorio temporal autorizado, fuera de la carpeta sincronizada. Los intentos fallidos iniciales no se cuentan como verificación.

## Límites y pendientes

- Un solo proceso operador; otro proceso con una referencia antigua falla cerrado y debe reabrirse.
- Commit SQLite y actualización del sello no son una transacción distribuida. Una interrupción entre ambos deja discrepancia y bloquea solicitudes; no se re-sella automáticamente. Falta un procedimiento de reconciliación offline auditado.
- No se instalaron ACL, servicios, antivirus ni políticas Windows. La separación lógica de directorios no acredita separación de privilegios. SAH02/autoridades del host sigue PARCIAL.
- Si el atacante controla el host o puede reemplazar conjuntamente índice y autoridad, no existe garantía de antirretroceso independiente del host. No se afirma protección ante ese adversario.
- Esquema nuevo optativo; no se migró una base existente automáticamente.
- No hay SSO, MFA, autorización empresarial integrada ni LLM validado.
- No hay garantía de borrar copias ya descargadas ni datos de backups anteriores.

A2-03/A3-02 avanzan en laboratorio, sin cerrar todo A2/A3 ni habilitar datos reales. Siguiente trabajo: auditar recuperación de fallos, regresión completa del nuevo esquema y provisión verificable de la autoridad en entorno aislado.
