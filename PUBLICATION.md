# FREG-PUBLIC-ARCH-001-GO - alcance público

Fecha:24-10-2026, America/Santiago.
El propietario autorizó publicar la candidata local ca423062f8e9b83f12365a42248c7e65d6107f45, condicionada a CI y controles previos, sin modificar main.

La revisión automática rechazó el snapshot completo por incluir documentación de fuentes privadas. Este paquete reduce materialmente la publicación a demo, fuentes compartidas mínimas, pruebas, dependencias y licencia. No contiene esa documentación ni enlaces privados. La continuidad completa y su copiaGit original permanecen fuera de esta rama pública.

Los archivos de ejecución de public_demo y los cuatro módulos compartidos se copiaron byte a byte de la candidata aprobada. Sólo README, este documento y reglas de empaquetado son nuevos. No se altera el comportamiento de búsqueda aprobado. El transporte API produce otro commit; se comprobará el árbol y se registrará su SHA remoto.

La CI de esta rama valida el subconjunto público:13 casos Python y15 casos Node; no sustituye las104 pruebas locales históricas, las11 comprobaciones de navegador ni la suite completa del prototipo. La versión sigue siendo demo-0.1.0-rc.1, no una release empresarial estable.

Para revertir, deshabilitar temporalmente Pages si existe exposición indebida, identificar el SHA desplegado y reconstruir código revisado con corpus vigente. No borrar historial ni republicar paquetes viejos con fuentes retiradas. Conservar registros de la incidencia y repetir CI/verificación externa antes de promover.
