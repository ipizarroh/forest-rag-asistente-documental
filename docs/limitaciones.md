# Limitaciones

Alcance: la interfaz documental pública y el laboratorio sintético de permisos
son componentes separados. El laboratorio no habilita autenticación empresarial
ni acceso a documentos privados en la UI. FREG-003 sólo cambia su presentación.

- Corpus oficial de dos páginas de FAO 2024: verifica un pipeline, no una base industrial representativa.
- Sin información interna de ARAUCO. Sin procedimientos reales de mantenimiento.
- Sin OCR, tablas estructuradas ni gráficos. Varias columnas pueden alterar el orden de lectura.
- Fragmentación por palabras con límite de tokens; puede separar una respuesta de sus detalles.
- Sin búsqueda híbrida ni reranker. Coseno y umbral no garantizan que exista respuesta.
- Evaluación inicial de desarrollo. Recuperar la página correcta no equivale a recuperar todos los hechos de referencia.
- Validar citas no prueba fundamentación.
- Ollama: adaptador con contrato probado; inferencia real y alucinaciones pendientes. No se declara RAG generativo completo validado.
- Sin autenticación multiusuario, disponibilidad, monitoreo productivo, GIS, SAP ni cloud.
- Límites de archivo no hacen segura la ingesta de PDF hostiles.
- Sin certificación operacional ni sustitución de procedimientos oficiales.

