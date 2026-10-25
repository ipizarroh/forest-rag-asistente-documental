# Confianza del índice — FREG-002

VERIFICADO en pruebas locales: el lector exige una huella SHA256 externa, configurada
por el operador en `FORESTRAG_INDEX_SHA256` o por el llamador confiable mediante
`trusted_sha256`. No se toma de metadatos ni sidecars del índice. No es una credencial
ni clasificación documental: no reemplaza autenticación/autorización.

## Amenaza y autoridad

El atacante puede reemplazar íntegramente el SQLite y sus archivos adyacentes,
incluidos checksums y manifiesto. No puede cambiar código, proceso ni configuración
del operador. Este último construye desde fuentes revisadas en un directorio sin
escritores ajenos y conserva la huella fuera del ámbito modificable por el atacante.
La huella puede ser conocida públicamente; su integridad, vigencia y origen deben
estar protegidos. Si el atacante cambia también esa referencia o controla el host,
este control no lo detiene. No se implementó firma PKI ni provisión IAM de la huella.

## Procedimiento

1. El operador ejecuta ingesta confiable. El constructor calcula `index_sha256` sobre
   el archivo temporal terminado antes de publicarlo mediante reemplazo atómico.
2. Tras revisar fuente/versión, configura esa huella para CLI/UI por un canal fuera
   del directorio del índice. No hay API ni campo de pregunta para cambiarla.
3. El lector carga como máximo 200 MB, compara SHA256 **antes de SQLite** y usa esos
   mismos bytes en una conexión SQLite en memoria, sólo lectura. No reabre la ruta.
4. Sin referencia válida, con sustitución o artefacto inválido, falla cerrado.
5. Para una actualización, el operador construye/revisa y autoriza una nueva huella.
   El índice viejo falla contra ella; retirar la referencia impide nuevas lecturas.

La aplicación no autoacepta una nueva huella cada vez que encuentra un archivo.
La demo y el benchmark pasan directamente el resultado de su propio constructor
confiable en la misma ejecución. Ese patrón no autoriza autoaprobar archivos externos.

## Evidencia y límites

`tests/test_index_trust.py` prueba: ausencia de ancla; alteración antes de parsear;
reemplazo estructuralmente válido con sidecar coeditado; cambio de ruta entre hash
y SQLite; actualización autorizada, rollback y retiro; SQLite inválido controlado.
Las pruebas usan referencias controladas por el test y archivos ficticios, no un
despliegue con dos cuentas del sistema operativo. La separación de permisos/ACL,
protección del proceso y canal real de provisión siguen siendo requisitos de despliegue.

El snapshot puede consumir memoria adicional cercana al tamaño del archivo más
la copia SQLite; sólo se midió el corpus pequeño. Esta modalidad no es un almacén
vectorial grande ni un sistema de actualización online. La DB de políticas del
laboratorio sigue bajo confianza del operador local y no se convierte en firmada.
