# Seguridad

Aplicación individual en loopback con corpus público revisado. Sin autenticación ni permisos por documento: no exponer como servicio multiusuario con datos privados.

Esta descripción corresponde a CLI/Streamlit originales. El laboratorio aislado de
FREG-CRITICAL-001 sí implementa autorización de prueba; ver
[diseño y límites](../FORESTRAG_ACCESS_CONTROL_DESIGN.md) y
[guía](security-lab.md). Ningún documento privado debe conectarse al índice original.

| Riesgo | Control implementado | Límite |
|---|---|---|
| Filtración | Sin claves; .env, datos y pesos excluidos de Git; corpus explícito. | Revisar contenido antes de publicar. |
| Archivos inesperados | Extensión, firma, hash, ruta resuelta y máximo 20 MiB. | No antivirus ni sandbox de PDF. |
| Recursos | Límites de páginas, texto, flujo, pregunta, contexto y respuesta. | La descompresión puede consumir recursos antes del control. |
| Prompt injection | Contexto no confiable separado; sin herramientas ni ejecución. | Un prompt no elimina este riesgo. |
| Citas falsas | IDs existentes exigidos por afirmación. | IDs válidos no prueban veracidad. |
| Contexto externo | Ollama fijo en 127.0.0.1; sin proxy ni redirecciones. | Verificar configuración y registros del servidor local. |
| SQL y deserialización | Consultas estáticas, parámetros, JSON y float32; sin pickle. | Aceptar índices confiables. |
| Acciones riesgosas | Filtro conservador de ejemplos y avisos. | No cubre toda formulación o idioma. |

Sin registro automático de preguntas en disco. La evaluación sí escribe su conjunto público si se solicita salida. Un despliegue requiere política de retención.

Versiones directas fijadas; pesos y tokenizer verificados por revisión y hashes. Sin código remoto del modelo. CI con permiso de lectura y sin secretos. Las pruebas no son una auditoría integral. Pendientes: revisión de vulnerabilidades y bloqueo con hashes de dependencias transitivas.

Producción requiere autorización documental antes de recuperar, autenticación, cifrado, respaldos, ingesta aislada, límites por usuario, observabilidad y pruebas adversariales. No se desplegó infraestructura.

