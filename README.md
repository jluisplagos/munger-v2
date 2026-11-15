# Munger V2 — código y trazabilidad

Preparación de la base histórica 4.14. La migración todavía está incompleta:
faltan archivos que no se han recibido en esta sesión.

Repositorio: https://github.com/jluisplagos/munger-v2
Visibilidad pública por indicación de la persona responsable.

El estado financiero de la 4.14 sigue siendo experimental supervisado. Los bloqueos de la revisión externa se conservan en docs/.
Subir los archivos a GitHub no acredita aptitud para decisiones con dinero real.

## Estructura

- munger_v2_r1/: rutas originales del proyecto, sin cambios de fórmulas ni reparaciones.
- baselines/4.14.json: inventario completo, tamaños, SHA-256 y destino de cada archivo.
- baselines/4.14_MANIFIESTO_SHA256.txt: manifiesto original intacto.
- tools/base_414.py: verifica la copia o recupera archivos desde la base completa.
- docs/: estado de migración y revisión externa.

Git conserva código, contratos, instrucciones, registros y textos fuente.
Los PDF, libros Excel y otros binarios se mantienen aparte. La propuesta es conservar el ZIP original en una Release
de GitHub, etiqueta base-4.14, o en otro almacenamiento autorizado. No hay binarios subidos todavía.
El ZIP completo pesa 1130912246 bytes y su SHA-256 es
bb51942cefb848e409a4828e3faeb70f94aa4d29af39cda6d90cd0a97cb7b93e.

## Completar la migración desde el paquete que ya tiene la persona responsable

Primero reconstruir el ZIP con las 54 partes y las instrucciones de PARTES.txt.
También sirve la extracción completa e intacta del ZIP.

Con Python 3.10 o posterior, sin paquetes adicionales:

    python tools/base_414.py materialize --source "RUTA_AL_ZIP_O_CARPETA" --git-only
    python tools/base_414.py verify --git-only --report docs/VERIFICACION_MIGRACION_GIT.json

El importador comprueba TODOS los archivos del origen contra el manifiesto antes de escribir.
No sobrescribe archivos modificados. Falla ante origen incompleto o huellas diferentes.
Después se incorporan a Git los textos recuperados; los binarios permanecen fuera de Git.

Para ejecutar el proyecto, recuperar también los binarios:

    python tools/base_414.py materialize --source "RUTA_AL_ZIP_O_CARPETA"
    python tools/base_414.py verify --report docs/VERIFICACION_BASE_COMPLETA.json

La verificación debe dar complete:true y cero ausentes/alterados.
Estos comandos verifican la base histórica 4.14, no una versión corregida posterior.

## GitHub y Claude

El repositorio es público por indicación de la persona responsable.
Esta preparación puede publicarse como migración incompleta. Antes de declararla base de trabajo completa, completar y comprobar el inventario.
No usar una conexión de lectura del chat como prueba de que Claude puede ejecutar el proyecto o guardar cambios.

Después de autorizar la cuenta y subir una base completa de código:
- usar un entorno con acceso al repositorio y capacidad para ejecutar Python y LibreOffice;
- recuperar los binarios desde la base identificada;
- ejecutar comprobar_entorno.sh;
- probar una rama de trabajo y comprobar que los cambios se conservan;
- retomar el encargo correctivo de docs/ sin alterar los originales.

La integración GitHub de Claude y la conexión GitHub de ChatGPT son autorizaciones distintas.
No añadir credenciales de acceso al repositorio.

## Desarrollo

La rama de la migración debe conservar la base sin reparaciones mezcladas.
Crear después una rama de correcciones. Una nueva plantilla o referencia económica necesita su versión y pruebas.
Conservar las fuentes y las evidencias que sostienen cada resultado.

No se incluye un flujo CI que afirme PASA sin tener fuentes, binarios y entorno completos.

## Trabajo que Claude ya está ejecutando

NO detenerlo, reiniciarlo ni cambiarlo de ventana para esta migración.
Esta preparación contiene la base histórica 4.14 disponible aquí. No contiene las correcciones aún en curso en el entorno de Claude.
Cuando Claude termine, conservar su entrega completa y sus huellas antes de importarla en una rama nueva.
Si entrega un parche, conservar su referencia exacta a la base y verificar su aplicación sobre una copia completa.
La herramienta base_414.py solo sirve para la base histórica: NO ejecutarla sobre la versión corregida.
La importación de una entrega posterior necesita su propio manifiesto y revisión de cambios.

No es necesario volver a ejecutar el encargo para trasladar sus resultados a GitHub.
La fuente de las correcciones es la entrega final de Claude; no esta copia parcial antigua.

## Archivos pesados disponibles

Release de recuperación parcial: https://github.com/jluisplagos/munger-v2/releases/tag/base-4.14-binarios-disponibles

Un ZIP de 466225808 bytes conserva 814 archivos binarios mediante 542 objetos únicos.
Faltan 194 binarios de la base y los 462 archivos de texto ya declarados.
Las rutas y huellas se conservan en baselines/4.14.json; la identidad del ZIP está en baselines/4.14_assets.json.
Este ZIP de recuperación no se descomprime directamente encima del proyecto: los objetos están deduplicados.

Con GitHub CLI, desde la raíz del repositorio clonado:

    gh release download base-4.14-binarios-disponibles --repo jluisplagos/munger-v2 --pattern munger_4.14_binarios_disponibles.zip --dir .downloads
    python tools/restore_assets_414.py --source .downloads/munger_4.14_binarios_disponibles.zip --report docs/VERIFICACION_BINARIOS_LOCAL.json

El código de salida esperado es 1 mientras la base esté incompleta; el informe identifica los ausentes.
No se sobrescriben archivos distintos. No ejecutar sobre las correcciones en curso de Claude.
Para recibir su próxima entrega, seguir docs/RECEPCION_ENTREGA_CLAUDE.md.
