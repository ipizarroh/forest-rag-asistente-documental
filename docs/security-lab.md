# Laboratorio ForestRAG Security — FREG-CRITICAL-001

Entidades y documentos inventados. API extractiva en loopback, sin llamadas a LLM,
proveedores de identidad, servicios facturables ni infraestructura de ARAUCO.
La CLI/Streamlit histórica sigue siendo exclusiva de corpus público.

## Preparación mínima

Desde esta copia de desarrollo basada en FREG-002 (aún no publicada). El laboratorio
FREG-001 ya existe en la rama pública anterior; no confundir sus dependencias:

```bash
python -m venv .venv-lab
.venv-lab/bin/python -m pip install --require-hashes -r requirements-lab-linux-py312.lock
.venv-lab/bin/python -m pip install -e . --no-deps
.venv-lab/bin/python -m pytest -q tests/test_security_lab.py tests/test_audit_regressions.py
.venv-lab/bin/python -m forestrag.security_http init
.venv-lab/bin/python -m forestrag.security_http serve
```

En Windows usar `.venv-lab\Scripts\python.exe` e instalar `-e '.[dev]'`. El bloqueo con hashes entregado
corresponde sólo a Linux x86_64/Python 3.12; las otras plataformas usan pyproject
y necesitan su propio bloqueo/verificación. No instalar `semantic`/`ui` en el
entorno mínimo si sólo se evalúan permisos. En el corte histórico FREG-001,
FastEmbed exigía Pillow <13; FREG-002 retira FastEmbed y fija Pillow13 para la UI.

`init` no reemplaza archivos. Crea DB 0600 y credenciales aleatorias 0600 en
`data/security-lab/`, excluido de Git. En Windows validar las ACL del directorio:
el modo POSIX 0600 no prueba protección NTFS. Los tokens duran como máximo una hora;
no se imprimen en consola. No subir, pegar en el chat ni incorporar el archivo al ZIP.

## Consulta reproducible sin exponer tokens en el historial del shell

Con el servidor en ejecución, en otro terminal:

```bash
.venv-lab/bin/python scripts/demo_security.py
```

El script lee credenciales del archivo local, hace la misma pregunta para cinco
identidades, verifica las diferencias y la denegación de descarga, y sólo imprime
IDs ficticios y estados HTTP. API:

| Ruta | Operación | Protección |
|---|---|---|
| POST /query | JSON con sólo `question` | Bearer vigente + capacidad query + autorización SQL |
| GET /documents/{id} | Texto sintético | Bearer + capacidad download + política vigente |
| GET /history | Referencias recientes | Bearer + propietario + política y versión vigentes |

No hay rutas de administración, upload, exportación, índice o descarga por ruta
de disco. No hay caché de respuestas/búsquedas: se reevalúa cada petición.
Todas las respuestas HTTP usan `Cache-Control: no-store`. Historial guarda sólo
referencias (máximo 100 por identidad), nunca texto de preguntas/respuestas.
No se pueden retirar copias de texto ya entregadas a alguien autorizado.

## Administración confiable de prueba

El operador local usa `SecurityLab` desde Python: `issue_token`, `revoke_token`,
`disable_principal`, `set_grant`, `put_document`, `delete_document`. No son
operaciones del chatbot ni capacidades del usuario `admin`. Cambiar un documento
invalida fragmentos/historial anteriores y revoca sus concesiones para revisión.
La asignación real de una credencial a una persona sigue fuera del laboratorio.

Las cuotas son por identidad, persistidas (30 solicitudes/60 s), compartidas
entre sus tokens. Cuatro solicitudes concurrentes y cuatro hilos HTTP como máximo;
timeout de socket 3 s, cuerpo 8192 bytes y pregunta 1000 caracteres. No equivale a
protección DDoS ni detector de extracción masiva. Cuentas diferentes no comparten
cuota, y el límite de ventana permite ráfagas en su frontera.

El laboratorio rechaza acceso a Restringido, incluso con una concesión. No se
simula MFA mediante un booleano editable o un selector. SSO/MFA real, TLS remoto,
cifrado en reposo, alertas, backup/restauración y pruebas con LLM siguen pendientes.
