# Candidata de integración técnica: 4.15, hito 2 (pendiente de revisión externa)

Rama `integracion/candidata-cierre-v2` (`jluisplagos/munger-v2-evidencias-mistral`, rama `coordinacion/cierre-v2`, `coordinacion/cierre_v2/INTEGRACION.md`:7), sobre 957af65 (entrega 4.15 · hito 2, corrección técnica tras la revisión externa del hito 1; `munger_v2_r1/VERSION`). Entrega intermedia: la revisión externa del hito 2 está pendiente (`munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/hito2/PUNTO_DE_RECUPERACION.md`, «Siguiente paso exacto»). No fusionada con main. No contiene el cierre económico F1 ni los expedientes regenerados. La revisión externa del hito 1 está en docs/revision_externa_4_15_hito1/ y el registro del hito 2 en `munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/hito2/HITO_2_4_15.md`.

La base 4.14 completa sigue conservada en main y en su Release. Para ejecutar este hito: clonar main, recuperar y verificar sus binarios con tools/base_414.py y después cambiar a esta rama. La verificación de la 4.14 no debe aplicarse al código modificado de la 4.15; usar el MANIFIESTO_SHA256.txt de esta rama para contrastar su árbol.

Esta rama conserva el código recibido del hito 2, sin incorporar correcciones propias al código del producto salvo decisión registrada. Cada nueva entrega de Claude se importa en una rama nueva con su manifiesto (docs/RECEPCION_ENTREGA_CLAUDE.md). Como integración técnica del programa de cierre, su contrato (`jluisplagos/munger-v2-evidencias-mistral`, rama `coordinacion/cierre-v2`, `coordinacion/cierre_v2/INTEGRACION.md`:26 y :31) solo admite en ella archivos aceptados tras la revisión de un contexto distinto del autor, con lista de archivos, huellas, SHA de origen, referencia de la revisión y SHA de destino.

---

# Munger V2 — código y trazabilidad

La base histórica **4.14 está recuperada y verificada**: 5790 archivos de código, documentación y textos en Git; los 1008 binarios se conservan dentro del ZIP original en Releases. El manifiesto tiene 6798 entradas, además del propio manifiesto.

Repositorio público por indicación de la persona responsable: https://github.com/jluisplagos/munger-v2

Las correcciones técnicas de los hitos 1 y 2 de la 4.15 están en el código de la candidata; los expedientes siguen sin regenerar y main conserva la 4.14 sin cambios. Otras correcciones aún en curso, como F1 en otra tarea, no están incorporadas todavía: esperar su entrega final y conservarla. El trabajo en otras sesiones debe continuar sin interrupción. La 4.14 mantiene su condición experimental supervisada y las incidencias documentadas en la revisión externa. Esta migración comprueba conservación de bytes, no aptitud financiera.

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
