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

## Archivos pesados: subida pendiente

Los binarios no están subidos. La conexión permite guardar código y crear el borrador de Release,
pero uploads.github.com devuelve HTTP 401 al intentar adjuntar archivos, incluso el pequeño .sha256.

Hay un borrador en https://github.com/jluisplagos/munger-v2/releases llamado
«Base 4.14 — ZIP original (pendiente de adjuntar)». La persona responsable puede
adjuntar allí desde su equipo el ZIP original completo de 1130912246 bytes, cuya huella figura arriba.
No requiere subir las 54 partes por separado ni detener el encargo que Claude está ejecutando.
La Release debe permanecer como borrador hasta adjuntar y verificar el archivo.

Cuando la Release base-4.14 tenga el ZIP original verificado y esté publicada:

    gh release download base-4.14 --repo jluisplagos/munger-v2 --pattern munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip --dir .downloads
    python tools/base_414.py materialize --source .downloads/munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip
    python tools/base_414.py verify --report docs/VERIFICACION_BASE_COMPLETA_LOCAL.json

La verificación completa debe devolver código 0 y complete:true.
No ejecutar estos comandos sobre las correcciones en curso de Claude.

Existe además una recuperación parcial preparada localmente: 814 binarios mediante 542 objetos únicos,
en un ZIP de 466225808 bytes. Su identidad se conserva en baselines/4.14_assets.json
y las herramientas restore_assets_414.py y sus pruebas están disponibles. Ese paquete tampoco se ha subido.
Faltan aquí 194 binarios y 462 archivos de texto de la base histórica.

Para recibir la próxima entrega corregida, seguir docs/RECEPCION_ENTREGA_CLAUDE.md.
