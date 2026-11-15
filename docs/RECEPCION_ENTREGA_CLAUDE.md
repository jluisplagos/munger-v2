# Incorporar la entrega que Claude está preparando

No interrumpir ni repetir su encargo. Esta migración no sustituye su entorno de trabajo.

Cuando termine:

1. Conservar el ZIP final, su SHA-256, el manifiesto, la verificación externa al ZIP y el registro de cambios. Si es un parche, conservar también la identidad exacta de su base.
2. Subir el ZIP completo a una Release nueva de este repositorio, con el nombre y la versión reales de la entrega. No dividirlo para adjuntarlo al chat. GitHub admite el ZIP histórico de 1,13 GB dentro de su límite de 2 GiB por archivo de Release. Comprobar el tamaño del nuevo ZIP antes de elegir este método.
3. Comprobar la huella del ZIP descargado y la integridad de sus miembros. Extraerlo en una carpeta nueva y verificar el manifiesto de ESA entrega. No usar base_414.py ni restore_assets_414.py para una entrega posterior.
4. Crear una rama nueva e importar su código y documentación, conservando exactamente los bytes originales y registrando aparte los binarios y sus rutas. Comparar contra la base histórica completa. Si falta un archivo de referencia, declarar la comparación pendiente: un archivo ausente aquí no es automáticamente un archivo añadido por Claude.
5. Ejecutar los controles que la entrega establece sobre la copia materializada y registrar resultados reales. La subida a GitHub no convierte pruebas anteriores en pruebas de esta copia.
6. Revisar las reparaciones contra los contraejemplos externos y los bloqueos económicos documentados. No dar por apto un resultado financiero solo porque las comprobaciones de software pasen.

La base histórica ya está completa y verificada: el ZIP original de la Release base-4.14 conserva los 1008 binarios y Git contiene los 5790 archivos de texto, además del manifiesto. Materializar y verificar esa base permite comparar la nueva entrega sin confundir ausencias locales con altas de archivos.

La alternativa parcial de binarios preparada inicialmente no llegó a subirse y queda sustituida por el ZIP original completo. No volver a pedir las 54 partes para esta base: ya está conservada en GitHub.
