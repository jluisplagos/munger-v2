# Segunda revisión interna de la reparación 4.13.1 (H5): instantánea i2

**Carácter.** Revisión INTERNA (subagente de Claude, contexto separado; mismo revisor que la primera, D1). No es una revisión externa.

**Versión examinada.** `/home/claude/trabajo_4_14/instantaneas/i2/munger_v2_r1`. `sha256sum -c huellas.txt` da OK en los seis archivos, también al terminar esta revisión. Huellas: `cierre_v2.py` 8629cd58…; `ficha.py`, `informe.py`, `resumen.py` y `pipeline.py` iguales a i1; `test_vigencia_h5.py` e5ce604a…. El diff `hitos/hito1/cambios_i1_a_i2_cierre_v2.diff` coincide con lo que declara el autor.

**Método.**
- Copia propia en `/home/claude/trabajo_4_14/agentes/D2/arbol/`. Para comparar, `personaje_v2/scripts_i1/` es la misma copia con el `cierre_v2.py` de i1 (d4d41bb3…).
- No se ejecutaron `pipeline.py`, LibreOffice ni baterías.
- Sondas en `/home/claude/trabajo_4_14/agentes/D2/sondas/`:
  - `sonda_d2.py`: escenarios nuevos N1–N5;
  - `sonda_d1*.py`: las de la primera revisión, repetidas sobre i2.
- Salidas: `salida_d2_i2.txt`, `salida_d2_i1.txt` y `salida_d1_en_i2.txt`.
- El paso 13 y el arranque del paso 14 se emulan como en D1. Las auditorías de esas emulaciones son sintéticas.
- Forma de cada comando: `cd …/D2/sondas && python3 -B -I sonda_d2.py /home/claude/trabajo_4_14/agentes/D2/arbol/munger_v2_r1/personaje_v2/scripts i2`. Para comparar con i1, `scripts_i1 i1`.

**Escrituras fuera de la copia.** `find /home/claude/trabajo /home/claude/trabajo_4_14 -newer agentes/D2/sondas/marca_sondas -not -path "*/agentes/D2/*"` solo devuelve `instantaneas/i2/…/pruebas/_v64/casos/…`: libros recalculados y el perfil de LibreOffice de la batería de regresiones que corre en paralelo. Las sondas no escriben ahí. Ninguna ruta con «D2» aparece fuera de la copia.

## Estado de D1-1 a D1-11

| Id | Estado | Evidencia (hecho) |
|---|---|---|
| D1-1 | **Resuelto** | S1 sobre i2: B cierra (`ficha 0 · informe 0 · resumen 0`), su solicitud nueva no queda anotada y la fila y la vigencia de A no cambian. Ya no se busca por nombre de empresa. |
| D1-2 | **Resuelto en el caso habitual**; con límite (ver D2-1) | S3 sobre i2, las tres vías: `rc1=5`, `retirada_pendiente` visible y estado `None/None`. La fila sigue APROBADO, pero la retirada pendiente se ve, como pide §4. Depende de la línea del historial (D2-1). |
| D1-3 | **Resuelto** | X4b: `(3, 3, 3, 3)`, sin reactivación. N5, con un cierre nuevo de i2 cuya publicación está sellada y sin FIN en el historial: `(3, [3, 3, 3])`. En i1, N5 daba `(3, [0, 0, 0])` y reactivaba. |
| D1-4 | **Resuelto** | S2: código 5 y aprobación conservada. Tras restaurar el registro, `ficha 0 · informe 0 · resumen 0`. X3 sin anotación. |
| D1-5 | **Resuelto** | S6: la retirada anota `legado-sha256`. Restaurados ficha, cierre, informe y estado: «la aprobación del cierre anterior a la 4.8.1 (auditoría c051cfaaecb6…) ya se retiró…», y `resumen.py` da 3. |
| D1-6 | **Resuelto** | S4: con `aprobaciones_retiradas.json` ilegible, el cierre sigue `VIGENTE` y `resumen.py` da 0. |
| D1-7 | **Declarado** (sin cambios) | S5: la restauración en espejo sigue reactivando (`VIGENTE`). X1 y X2: borrar solo una señal no reactiva. |
| D1-8 | **Resuelto** | El motivo nombra la señal, por ejemplo «…publicada (estado_pipeline.json registra el FIN del paso 14…)». |
| D1-9 | **Declarado** (sin cambios) | X5: `ficha.py --provisional` da 0 y deja `APROBADO/concluido`. |
| D1-10 | **Resuelto**, con el mismo límite que D1-2 | El `csv_path` de la vía se retira con la empresa que da el historial (código, cierre_v2.py ~1021-1028). Sin una línea del historial reconocible no hay empresa, y tampoco se retira el destino de la vía (D2-1). |
| D1-11 | **En curso** | `regresiones_i1/resumen.txt`: las ocho baterías PASAN sobre i1. `regresiones_i2/resumen.txt`: por ahora solo `test_vigencia_h5` (55/55); la integración V6.4 sigue corriendo. |
| S10 (fila en un CSV con un nombre no registrado) | **Declarado** | La fila sigue APROBADO, con `sin_archivo` y código 3, por prudencia. |

## Hallazgos nuevos

| Id | Gravedad | Hecho comprobado (evidencia reproducible) | Consecuencia (interpretación) | Propuesta |
|---|---|---|---|---|
| D2-1 | Importante | **Cuando no hay registro, la retirada depende de una línea de registro de una ejecución truncada a 200 caracteres.** `destinos_publicados_en_el_estado` (cierre_v2.py 676-690) busca `OK: fila de (.+?) en (\S+\.csv)` en el historial. Esas líneas las escribe `pipeline.run()` con `salida.splitlines()[-1][:200]` (pipeline.py 107). **Montaje:** sondas N1, sin ficha, cierre, registro ni respaldo. Con la línea original: `rc=3` y fila «SIN APROBACIÓN». Con la publicación hecha en una ruta de 212 caracteres (la línea queda truncada antes de `.csv`) o en una ruta con un espacio: `rc=3`, fila **`APROBADO`**, registro `[]` y `pendientes: []`. Con i1 (que buscaba por nombre de empresa), las tres variantes retiran la fila. En el paquete actual, la línea más larga que el revisor encontró mide 188 de 200 caracteres (Viscofan, ensayo 4.12, V6.4): basta con trasladar el árbol a una carpeta 13 caracteres más profunda. | Reaparece D1-2 (aprobación publicada sin retirada pendiente visible, código 3) para cualquier expediente sin registro publicado desde una ruta larga o con espacios. Un caso típico es una ruta de usuario del tipo «Mis documentos». Es una regresión respecto a i1 en esas rutas. | Que la publicación quede registrada de forma estructurada, no en un texto de registro truncado. Por ejemplo, que `publicaciones_de_la_aprobacion` lleve también la empresa y que `destinos_publicados_en_el_estado` la use (ver D2-4). Como mínimo, un patrón que admita espacios (`en (.+\.csv)$`) y que el paso 14 guarde la ruta completa en un campo propio. |
| D2-2 | Importante | **La tercera señal de `motivo_aprobacion_retirada` convierte una retirada «por prudencia» de la sincronización en la pérdida de una aprobación vigente.** Montaje N2:<br>1. cierre legítimo emulado en el resumen predeterminado V6.4: `0/0/0`; la ficha nueva y la archivada por Y-h tienen la misma fecha (2026-11-12);<br>2. se redondea `precio_si` a dos decimales en la fila del CSV, como haría una hoja de cálculo;<br>3. `CIE.sincronizar_resumenes(c, VER)`, lo mismo que hace `pipeline.py` al arrancar (línea 1712).<br>La rama F-2 de la sincronización (`_fila_aprobada`, y en `retirar_publicaciones` la línea 1302 `elif previa not in objetivos`) retira la entrada del cierre vigente, que ya está sellada con su identidad. El código lo hace a propósito («la fila se retira y resumen.py la vuelve a publicar», comentario de `sincronizar_resumenes`). **i2:** `vigencia: la aprobación de la solicitud SA-e83a… ya se retiró (… antecedente publicaciones_resumen.json …)`; `resumen.py` da 3 y archiva el cierre: estado `None/None`, la solicitud anotada como retirada, RETIRADA.json 2. **i1:** `vigencia: VIGENTE` y `resumen.py` da 0, que vuelve a publicar. | Un cierre vigente y sano, con el material intacto, pierde su auditoría humana sin vuelta atrás por una edición de presentación del CSV. Rompe el control positivo «cierre legítimo» (§9). Es una regresión nueva de i2 (cierre_v2.py 765-772 junto con el sellado de 1336-1343). | Que solo cuente como señal la entrada retirada por una invalidación de la aprobación (sin `conservar_material`, o con el motivo de `archivar_salidas`), no la que retira la sincronización de un cierre vigente. Otra opción: que la rama F-2 no retire la entrada con la identidad del cierre vigente, sino que la deje para volver a publicar. Añadir N2 a la batería. |
| D2-3 | Menor | **`_fin_del_paso_14_tras` acepta cualquier «paso 14 · FIN», también el de una terminación que no cierra.** Montaje N3: intervalo legítimo con «respuesta a la solicitud <id>» y, después, «paso 14 · FIN · estado no_entregable · …». Esa línea la escribe `terminar()` con el paso del estado (pipeline.py 146), por ejemplo cuando falla `reaplicar_configuracion` al arrancar en el intervalo (pipeline.py ~1735). Al reanudar el paso 14: i2 da `ficha 3`, retira y anota la solicitud nueva; i1 da `ficha 0` y cierra. | Un caso marginal: hay que reanudar con `--desde 14` después de un `no_entregable` en el intervalo. Muestra que la señal no es específica del cierre. | Buscar el FIN de cierre que escribe el paso 14 (`FIN · estado <concluido|pendiente_*> · auditoría APROBADO`), no cualquier FIN. |
| D2-4 | Observación | **`publicaciones_de_la_aprobacion` no sobrevive al flujo del pipeline.** `resumen.py` (vía `registrar_publicacion`) escribe la clave en `estado_pipeline.json` en disco. Después, `salidas_finales` guarda el estado de memoria (`self.guardar()`, pipeline.py 210), y `adoptar_archivo` (213-229) solo fusiona `cierres_archivados`, `auditoria`, `estado_analisis`, `paso` e `historial`. Comprobado por lectura, sin ejecutar el pipeline. Con llamadas a mano sí se conserva (N5: 1 entrada). | Una de las señales «del estado» que se declaran solo existe en las publicaciones hechas a mano. Las otras señales, el sello del registro y el FIN, cubren el flujo del pipeline. | Fusionar la clave en `adoptar_archivo`, o que la escriba el propio pipeline. Es necesario si se adopta la propuesta de D2-1. |
| D2-5 | Observación | `senal_publicacion` sigue aceptando **cualquier** entrada «publicada» del primer registro legible, no solo las de esta aprobación (cierre_v2.py 651-652). El revisor no encontró ningún flujo legítimo que deje una «publicada» ajena en el intervalo (Y-h y `_propias` las resuelven). | Es un riesgo residual si una retirada de Y-h falla por una excepción (la entrada se queda «publicada»). | Si la entrada tiene identidad, exigir que coincida. |

## Lo que se comprobó que funciona en i2 (hechos)

- **Intervalo legítimo.**
  - S0: `0/0/0`.
  - N4, con el historial que deja el pipeline real («respuesta a la solicitud <id>» sin FIN después): `0/0/0` y sin anotación.
  - S7, con `retirada_pendiente`: código 5, y al volver el destino, `0/0/0`.
  - SA, con `sin_archivo`: `0/0/0`.
  - S2 y X3, con registro ilegible: código 5 sin perder la aprobación.
- **Primeras llamadas y retirada:**
  - S8: en una copia con `registro_id`, la retirada no toca el original;
  - S9: llamadas repetidas `[3, 3, 3, 3]`, con un solo antecedente;
  - X1 y X2: borrar una sola señal no reactiva la aprobación;
  - R1 y R2: recuperación con una auditoría nueva, `0/0/0`;
  - S6: legado 4.6.1 retirado y no reactivable.
- **Escritura acotada a la copia.** El traslado de los destinos del historial a la carpeta actual mantiene la retirada dentro de la copia: en S3 y N1 el registro queda con rutas de la copia, y `find -newer` no muestra escrituras fuera de ella.
- **Batería.** El grupo I de `test_vigencia_h5.py` monta D1-1 a D1-6 con las mismas emulaciones. No cubre N1 (ruta larga o con espacio), N2 (retirada de prudencia de un cierre vigente) ni N3.
