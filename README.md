# Auditoría económica paralela — F1

Esta rama añade únicamente revisión documental y un encargo económico separado sobre la base congelada de la 4.15 hito1. No modifica el producto. F1 permanece abierto.

Leer primero [la coordinación](docs/validacion_economica_paralela/COORDINACION.md), [el inicio de conciliación](docs/validacion_economica_paralela/F1_INICIO_CONCILIACION.md) y [el encargo para la segunda tarea](docs/validacion_economica_paralela/PROMPT_FRENTE_ECONOMICO.md).

---

# Rama de revisión: 4.15, hito 1

Entrega intermedia recibida de Claude, con una revisión externa en curso. No fusionada con main. El hito no contiene el cierre económico F1 ni los expedientes regenerados. Hay un contraejemplo nuevo del control de signos; consultar docs/revision_externa_4_15_hito1/.

La base 4.14 completa sigue conservada en main y en su Release. Para ejecutar este hito: clonar main, recuperar y verificar sus binarios con tools/base_414.py y después cambiar a esta rama. La verificación de la 4.14 no debe aplicarse al código modificado de la 4.15; usar el MANIFIESTO_SHA256.txt de esta rama para contrastar su árbol.

El trabajo actual de Claude continúa aparte. Esta rama conserva exactamente el código recibido, sin incorporar correcciones propias al producto.

---

# Munger V2 — código y trazabilidad

La base histórica **4.14 está recuperada y verificada**: 5790 archivos de código, documentación y textos en Git; los 1008 binarios se conservan dentro del ZIP original en Releases. El manifiesto tiene 6798 entradas, además del propio manifiesto.

Repositorio público por indicación de la persona responsable: https://github.com/jluisplagos/munger-v2

Las correcciones que Claude está preparando no están incorporadas todavía. Su trabajo debe continuar sin interrupción. La 4.14 mantiene su condición experimental supervisada y las incidencias documentadas en la revisión externa. Esta migración comprueba conservación de bytes, no aptitud financiera.

## Estructura

- `munger_v2_r1/`: rutas originales de los archivos versionados, sin modificar las fórmulas ni reparar la base.
- `baselines/4.14.json`: rutas, tamaños, SHA-256 y destino de los 6798 archivos originales.
- `baselines/4.14_MANIFIESTO_SHA256.txt`: manifiesto original intacto.
- `tools/base_414.py`: verifica o recupera la base histórica completa.
- `docs/BASE_4_14_INTEGRITY.json`: comprobación del ZIP descargado y de sus miembros.
- `docs/RECEPCION_ENTREGA_CLAUDE.md`: cómo incorporar la próxima entrega sin repetir el encargo.

## Descargar los archivos pesados y recuperar el proyecto

Release del ZIP original: https://github.com/jluisplagos/munger-v2/releases/tag/base-4.14

Archivo: `munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip`.
Tamaño: **1130912246 bytes**. SHA-256:

    bb51942cefb848e409a4828e3faeb70f94aa4d29af39cda6d90cd0a97cb7b93e

Se ha descargado y comprobado su SHA-256 completo. Los 6798 miembros del manifiesto y el propio manifiesto se han leído hasta el final, verificando CRC y SHA-256. Se recuperaron los 656 archivos que faltaban en la preparación inicial; ninguna entrada sigue pendiente.

Con Python 3.10 o posterior y GitHub CLI, desde la raíz del repositorio clonado:

    gh release download base-4.14 --repo jluisplagos/munger-v2 --pattern munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip --dir .downloads
    python tools/base_414.py materialize --source .downloads/munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip
    python tools/base_414.py verify --report docs/VERIFICACION_BASE_COMPLETA_LOCAL.json

También se puede descargar el ZIP manualmente de la Release y pasar su ruta a `--source`.
La verificación completa debe devolver código 0, `complete:true` y ningún archivo ausente o alterado.
El importador verifica todo el origen antes de escribir y rechaza sobrescribir archivos modificados. Conserva las rutas y los bytes originales. Usa una copia nueva para este procedimiento, separada de las correcciones en curso.

Para verificar solo lo que se conserva en Git:

    python tools/base_414.py verify --git-only

## Continuidad con Claude

No detener, reiniciar ni cambiar de ventana el encargo actual para esta migración.
Cuando termine, conservar su entrega con sus huellas y seguir `docs/RECEPCION_ENTREGA_CLAUDE.md`: importarla como una versión nueva en otra rama, con su propio manifiesto y binarios. No ejecutar las herramientas de la base 4.14 sobre la versión corregida.

La integración GitHub del chat permite consultar archivos; la ejecución y el guardado de cambios requieren un entorno con esas capacidades. En una sesión nueva, comprobar acceso al repositorio, Python, LibreOffice y descarga de la Release antes de empezar el pipeline. El comprobador de entorno está en `munger_v2_r1/personaje_v2/scripts/comprobar_entorno.sh`.

No añadir credenciales al repositorio. LibreOffice y los pipelines que lo usan van en secuencia. Mantener originales, fuentes y evidencias; no reactivar aprobaciones retiradas ni aceptar una auditoría de material distinto.

Los registros históricos de la migración parcial se conservan para trazabilidad. `baselines/4.14_assets.json` y `tools/restore_assets_414.py` describen una alternativa parcial que no llegó a subirse: queda sustituida por el ZIP original completo de la Release.
