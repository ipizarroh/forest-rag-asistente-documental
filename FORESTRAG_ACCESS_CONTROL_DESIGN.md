# ForestRAG — Diseño de control de acceso

FREG-CRITICAL-001 · 23-10-2026. Diseño y subconjunto implementado, no política de
ARAUCO. Evidencias E06/E07 en el estado maestro; código security_lab.py/security_http.py.

## Identidad y autoridad

VERIFICADO: credenciales de prueba opacas de 256 bits aleatorios, almacenadas como
SHA256 en SQLite, TTL máximo 3600 s. El operador local entrega el secreto fuera del
chat; el backend vincula token con sujeto, organización y capacidades persistidas.
No se aceptan `user`, `role`, `org`, `mfa` ni identidad elegida en preguntas/JSON.
El token prueba posesión de la credencial emitida, no identidad civil ni afiliación.

Usuarios y servicios tienen registros separados por `kind`; la aplicación `app`
sólo puede consultar, carece de descarga e historial. Roles descriptivos no otorgan
permisos implícitos. `admin` es un lector limitado, no operador del host. Crear
usuarios/grants, ingresar/eliminar documentos y revocar son funciones del operador
confiable local; no hay rutas de administración ni herramientas del LLM.

PROPUESTO para otra fase: OIDC/SSO con validación de issuer/audience/exp/nonce,
MFA real según riesgo y credenciales de servicio de corta duración/revocables.
No hay pantalla de login ni MFA implementados. No definir un booleano `mfa=true`
controlable por el cliente como sustituto de autenticación reforzada.

## Clasificación y política implementada

| Clase | Política inicial del propietario | Laboratorio actual |
|---|---|---|
| Público | Reglas explícitas de publicación | `public` y `published=1`, recurso activo; API requiere token de prueba |
| Interno | Identidad y ámbito autorizado | Organización igual y membresías en área/proyecto si el documento las exige |
| Confidencial | Permiso explícito al recurso/proyecto | Lo anterior + grant individual al documento |
| Restringido | Autenticación reforzada y acceso limitado | BLOQUEADO siempre, aun con grant; proveedor MFA pendiente |
| Ausente/desconocida | Denegar | Ninguna rama SQL permite recuperarla |

La publicación pública es explícita y permite acceso a identidades de otras
organizaciones. Los demás recursos nunca cruzan organización. El acceso confidencial
requiere simultáneamente ámbitos y grant; compartir clasificación o rol no basta.
No se implementaron grants por grupo/proyecto: se usan membresías de proyecto y
concesión individual. Este subconjunto ABAC + relación usuario/documento es más
pequeño que un motor de políticas genérico. Capacidades de operación aportan la
separación por función; no se vende como RBAC corporativo completo.

## Flujo y almacenamiento

1. HTTP valida Host loopback, origen, cuerpo y ruta; credencial sólo en Authorization.
2. Backend valida sesión, sujeto activo y capacidad requerida, consume cuota.
3. SQL aplica política contra documento activo y versión vigente **antes** de
   seleccionar payload/vector. Ninguna colección global de evidencia llega al ranking.
4. `checked_chunk` comprueba checksum, ID derivado, norma y vínculo con documento/hash.
5. Ranking devuelve sólo hits autorizados; `build_messages` prepara contexto con
   ellos. Las pruebas instrumentan esa frontera; en esta versión no se llama a LLM.
6. Pasajes muestran citas sólo autorizadas y enlaces `/documents/{id}`; cada descarga
   vuelve a evaluar política. No hay URL de archivo de disco ni recurso estático privado.

`documents`: organización, área, proyecto, clasificación, publicación, actividad,
versión, título, contenido y SHA. `chunks`: FK documento + versión + JSON con
SHA/página/start/ID y vector/checksum. La política vigente se hereda mediante JOIN,
no copias obsoletas de ACL dentro del texto. FKs habilitadas por conexión.
`principals/areas/projects/capabilities/grants/sessions`: política del servidor.

## Laboratorio ficticio

| Identidad | Ámbito/capacidad | Evidencia permitida para «inventario» |
|---|---|---|
| ops | bosque-demo, operations/north, lector | public, ops, injection |
| hr | bosque-demo, hr/people, grant hr | public, hr |
| admin | bosque-demo, sin membresías de área/proyecto | public |
| other | otra-demo, operations/north | public, other |
| app | servicio bosque-demo, operations/north, sólo query | public, ops, injection |

Hay seis documentos: público, interno Operaciones, confidencial RRHH, restringido,
interno de otra organización y un interno con instrucciones maliciosas. Todos los
nombres, claves canario, presupuestos y cantidades son inventados bajo MIT.
La descarga puede pedir más documentos permitidos que los tres resultados del ranking;
top-k no es un mecanismo de autorización. El documento adversarial puede mostrarse
como texto; sus órdenes no cambian la política ni llaman herramientas.

## Superficies y estado

| Superficie | Control / estado |
|---|---|
| Búsqueda/chunks/contexto/citas | VERIFICADO, misma política antes del ranking |
| Índice/metadatos privados | Sin ruta HTTP de listado/índice; datos filtrados por SQL |
| Descargas/vista previa | Descarga protegida; no vista previa independiente |
| Historial | Sólo referencias propias, reautorizadas por documento/versión; máximo 100 |
| Respuestas guardadas/caché | Ausentes; no texto persistido ni caché de resultados/generación |
| Exportaciones/informes privados | Ausentes; no rutas habilitadas |
| Reindexación/eliminación/grants | Sólo operador del host; no privilegio del usuario admin |
| CLI/Streamlit original | Sin autorización; exclusivamente corpus público revisado |

## Revocación, eliminación y recursos

VERIFICADO: revocar token o desactivar sujeto impide nuevas solicitudes; cuota por
sujeto sobrevive emisión de otro token y reinicio. Retirar grant afecta consulta,
descarga e historial. Cambiar documento reemplaza chunks/versiones, borra referencias
anteriores y revoca grants; borrar documento elimina chunks, grants e historial por FK.
Solicitudes en curso pueden haber entregado datos antes de la revocación. No se
revocan copias legítimamente descargadas, cachés de clientes desobedientes o backups.

Sin caché de resultados: no hay invalidación fingida. `Cache-Control: no-store`
en HTTP. Embeddings léxicos no se comparten como respuestas. Serialización mediante
lock del proceso y transacciones SQLite; no se validó despliegue multiproceso/remoto.
Cuota 30 solicitudes/60 s por identidad, concurrencia 4, hilos HTTP 4, cuerpo 8192
bytes/pregunta 1000 caracteres, documento 100 KB, máximo 100 documentos, 10001 filas
de recuperación detectan desborde. Auditoría conserva últimas 2000 decisiones:
fecha, sujeto, operación y resultado; sin token/pregunta/contenido ni ID sensible.

## Límites y controles pendientes

HTTP sólo 127.0.0.1, sin TLS: no apto para exponer por túnel/red. DB y tokens se crean
0600 en POSIX; cifrado en reposo, ACL Windows y host endurecido no demostrados.
Operador/proceso con acceso al host está dentro de la frontera confiable. Sin firma
externa del índice/políticas, trazas inmutables, SIEM, alertas o detector conductual
de extracción. No hay protección suficiente frente a DDoS, token robado o colusión
de múltiples cuentas. Backups/restauración y retención empresarial siguen PROPUESTOS.
No usar este laboratorio para información confidencial real.
