# Incorporar la entrega que Claude está preparando

No interrumpir ni repetir su encargo. Esta migración no sustituye su entorno de trabajo.

Cuando termine:

1. Conservar el ZIP final, su SHA-256, el manifiesto, la verificación externa al ZIP y el registro de cambios. Si es un parche, conservar también la identidad exacta de su base.
2. Subir el ZIP completo a una Release nueva de este repositorio, con el nombre y la versión reales de la entrega. No dividirlo para adjuntarlo al chat. GitHub admite el ZIP histórico de 1,13 GB dentro de su límite de 2 GiB por archivo de Release. Comprobar el tamaño del nuevo ZIP antes de elegir este método.
3. Comprobar la huella del ZIP descargado y la integridad de sus miembros. Extraerlo en una carpeta nueva y verificar el manifiesto de ESA entrega. No usar base_414.py ni restore_assets_414.py para una entrega posterior.
4. Crear una rama nueva e importar su código y documentación, conservando exactamente los bytes originales y registrando aparte los binarios y sus rutas. Comparar contra la base histórica completa. Si falta un archivo de referencia, declarar la comparación pendiente: un archivo ausente aquí no es automáticamente un archivo añadido por Claude.
5. Ejecutar los controles que la entrega establece sobre la copia materializada y registrar resultados reales. La subida a GitHub no convierte pruebas anteriores en pruebas de esta copia.
6. Revisar las reparaciones contra los contraejemplos externos y los bloqueos económicos documentados. No dar por apto un resultado financiero solo porque las comprobaciones de software pasen.

Para la base histórica aún faltan 462 archivos de texto y 194 binarios. La fuente más directa para completarla es el ZIP original 4.14 que ya tiene la persona responsable o el entorno anterior de Claude. Si los originales se han preservado, puede subirse ese ZIP completo a una Release de base y verificarse con baselines/4.14.json. No reconstruirlo mezclando las correcciones nuevas.

El paquete de binarios disponibles publicado ahora es parcial y contiene objetos deduplicados. Su restituidor restaura las rutas originales y comprueba sus SHA-256; no sustituye al ZIP original completo.
