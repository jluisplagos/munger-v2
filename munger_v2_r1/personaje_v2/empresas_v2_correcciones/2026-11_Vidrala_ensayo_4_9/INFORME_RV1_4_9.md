# R-V1 · Integridad de la respuesta de auditoría vigente (entrega 4.9)

## 1. El defecto (hallazgo externo, reproducido)

**[Hecho]** En la 4.8.1, después de aceptar una respuesta a una solicitud y cerrar, `cierre_v2.motivo_rechazo_cierre()` daba por buena cualquier `auditoria.md` cuya huella de contenido coincidiera con la registrada. Esa huella es `huella_contenido`: el multiconjunto de las palabras, **sin la línea de solicitud y sin orden**.

Seguían en concluido/APROBADO, con código 0, por las cuatro vías (el paso 14, `ficha.py`, `informe.py` y `resumen.py`) y también en el destino configurado del resumen:
- un `auditoria.md` con la solicitud cambiada, eliminada o duplicada;
- uno con las mismas palabras y otro significado: «La evidencia respalda el crecimiento; la reposición queda pendiente» frente a «La evidencia respalda la reposición; el crecimiento queda pendiente»;
- uno con las mismas líneas en otro orden;
- uno con espacios o líneas añadidos.

**[Hecho] Dos defectos más, anteriores a la 4.9.** Los encontró la auditoría interna (§6) y se reparan en esta misma entrega:
- **Z-1.** Si no había ningún registro de la respuesta aprobada (`cierre_vigente.json` borrado en un cierre de la 4.6.1, un cierre de la 4.6 que no lo tiene de origen, o un cierre de la 4.9 sin estado ni `cierre_vigente.json`), `ficha.py --estado concluido` volvía a cerrar con **cualquier** auditoría APROBADO que nombrara el material. Además, `registrar_cierre` le atribuía la huella del archivo actual.
- **Z-2.** Un `auditoria.md` que no es UTF-8 (un byte inválido, o guardado en cp1252), o un `cierre_vigente.json` o un `estado_pipeline.json` ilegibles, interrumpían las vías con una traza y código 1, y la aprobación seguía publicada.

**[Hecho] Tres defectos más del mismo tipo.** Los encontró el control de vigencia posterior (§6) y también se reparan:
- **V-1.** Lo mismo con `material_auditoria.json` o `ficha.json` ilegibles.
- **V-2.** Lo mismo con un JSON válido que no es un objeto (`[]`), con una estructura interna errónea (`solicitudes_auditoria` que no es una lista, `auditoria_respuesta` que no es un objeto) y con `estado_pipeline.json` o `auditoria.md` convertidos en carpetas.
- **V-3.** Sin `estado_pipeline.json`, `ficha.py` reescribía `cierre_vigente.json` sin la solicitud ni la huella fiel, y con la huella de bytes del archivo actual (en una transformación inocua, no la de la respuesta aceptada).

**[Hecho] Y cuatro más del segundo control de vigencia** (§6), también reparados:
- **W-1.** Una ficha con «cierre» que no es un objeto o una solicitud sin «id» daban traza con la aprobación publicada; tipos erróneos de `historial`, `cierres_archivados` o `paso` en el estado daban traza después de retirar.
- **W-2.** Con `ficha.json` ilegible, `ficha.py` volvía a cerrar (código 0) con un registro más débil o con una ficha que ya no era vigente.
- **W-3.** Con `auditoria.md` sin permiso de lectura, el archivado se interrumpía al copiarla, antes de retirar las filas.
- **W-4** (anterior a la 4.9). Un `material_auditado` con «../» en la ficha sacaba el archivo de la retirada fuera del expediente.

**Reproducción con el código de la 4.8.1.** El código está en `reproduccion/codigo_4_8_1/`: `cierre_v2.py`, `pipeline.py`, `ficha.py`, `resumen.py` e `informe.py`, que son todos los archivos de código que cambia la 4.9, con las huellas del manifiesto 4.8.1.
- La batería nueva da **24/100** con ese código (`reproduccion/test_integridad_con_codigo_4_8_1.txt` y `.json`).
- Con el código de la 4.9 da **103/103**. Hay 3 pruebas más porque el grupo de unidades solo existe con `huella_fiel`.
- La tabla prueba a prueba, con lo observado antes, está en `reproduccion/tabla_antes_despues_rv1.md`.

**Matices de la reproducción:**
- La sustitución por otra aprobación y el cambio de material ya se retiraban en la 4.8.1. En la tabla, la primera falla solo por el texto del diagnóstico, que ahora es más preciso.
- En Z-1, con el código 4.8.1, el paso 14, `informe.py` y `resumen.py` ya retiraban en la primera llamada («no hay `cierre_vigente.json`»), pero **`ficha.py` volvía a cerrar** (código 0, ficha cerrada). Después, las demás vías daban el cierre nuevo por vigente.

## 2. La reparación

**[Hecho] Dos funciones separadas** (`personaje_v2/scripts/cierre_v2.py`):
- **A. Detección de posibles reutilizaciones** (paso 13): `huella_contenido`, sin cambios. Es un detector **conservador**, que admite falsos positivos (dos textos con las mismas palabras se tratan como el mismo). Sirve para **rechazar** una aprobación reutilizada y **no sirve para aceptar** la identidad de una respuesta. Su descripción lo dice ahora expresamente.
- **B. Comprobación fiel de que el informe vigente es la respuesta aceptada** (`motivo_respuesta_no_aceptada`, que usan la vigencia y el cierre). Comprueba **por separado**:
  1. **la solicitud:** exactamente una línea «Solicitud de auditoría», que es la de la respuesta aceptada y que `estado_pipeline.json` registra como respondida por esa respuesta;
  2. **el material** (sin cambios): el material actual es el fijado y el aprobado;
  3. **la respuesta:** `huella_fiel`, el SHA-256 del texto **íntegro y en su orden** tras aplicar solo las transformaciones inocuas.

**Transformaciones inocuas admitidas** (`cierre_v2.TRANSFORMACIONES_INOCUAS`, lista cerrada):
- una marca BOM UTF-8 al principio;
- los finales de línea CRLF o CR, que se leen como LF;
- los saltos de línea al final del archivo;
- la forma Unicode NFC o NFD, que son canónicamente equivalentes.

**Cualquier otra diferencia retira la aprobación**: palabras, orden de palabras o de líneas, mayúsculas, espacios (también el espacio no separable o el de anchura cero), líneas en blanco, separadores como VT o U+2028, caracteres de compatibilidad (NFKC no se aplica), puntuación o la propia línea de solicitud. No es un clasificador de significado: es una comparación fiel del texto.

**Sin registro de la respuesta aprobada, no se cierra (Z-1).** Si ni `estado_pipeline.json` (`auditoria_respuesta`) ni `cierre_vigente.json` registran qué `auditoria.md` se aprobó, ningún APROBADO confirma el cierre ni lo mantiene vigente: hace falta una auditoría nueva (paso 13). Así no se atribuye ninguna huella al archivo actual (encargo §3.3).

**Archivos que no se pueden leer (Z-2).** `motivo_rechazo_cierre` lee los bytes una vez. Un `auditoria.md` que no es UTF-8, o un `estado_pipeline.json` o un `cierre_vigente.json` ilegibles, son ahora **motivos de retirada**, no excepciones:
- el archivado y la retirada del resumen toleran esos archivos;
- `ficha.py`, `informe.py` y `resumen.py` leen el estado y la ficha con una función local tolerante, sin depender de funciones nuevas de `cierre_v2.py` (así, las reproducciones históricas que combinan código antiguo de `cierre_v2.py` con estos scripts siguen funcionando);
- con `estado_pipeline.json` ilegible, `pipeline.py` retira primero la salida cerrada y termina con código 6 («ESTADO DEL PIPELINE ILEGIBLE»), o con código 5 si queda una retirada pendiente.

**Dónde se registra la respuesta aceptada.**
- El paso 13 (`pipeline.py`) la guarda con su huella fiel: `auditoria_respuesta.fiel` y `respuesta_fiel` en la solicitud.
- El cierre (`registrar_cierre`) copia la solicitud y la huella fiel a `cierre_vigente.json`, pero solo si la respuesta las tenía y coinciden con el archivo.
- Si falta `estado_pipeline.json`, la vigencia usa lo registrado en `cierre_vigente.json`.

**Se conservan:**
- las solicitudes persistentes;
- su independencia de las fechas;
- el detector del paso 13;
- la retirada del cierre al pedir una auditoría nueva (Q-T5);
- H2: `veredicto_auditoria` es idéntica a la de la 4.7.1, con huella `9edf6252…`.

## 3. Compatibilidad y migración

| Cierre | Qué se acredita | Con otro archivo |
|---|---|---|
| Anterior a la 4.8.1, con `cierre_vigente.json` (como el de la 4.6.1) | Los bytes que registra `cierre_vigente.json` (sin cambios) | Se retira. Con CRLF también, porque no hay huella fiel registrada ni se calcula una |
| Anterior a la 4.6.1, **sin** `cierre_vigente.json` (como el de la 4.6), o cualquier cierre sin estado ni `cierre_vigente.json` | Nada: no consta qué auditoría lo aprobó | No se vuelve a cerrar ni sigue vigente; hace falta una auditoría nueva (Z-1) |
| De la 4.8.1, respuesta sin `fiel` | Los **bytes exactos** de `auditoria_respuesta.sha256` | Se retira con «la correspondencia no puede acreditarse … hace falta una auditoría nueva». No se le atribuye ninguna huella nueva (encargo §3.3) |
| De la 4.9 | Solicitud, material y huella fiel (en el estado o, sin él, en `cierre_vigente.json`) | Se retira, salvo con las transformaciones inocuas |

Más reglas de compatibilidad:
- A ninguna auditoría histórica se le asigna una solicitud.
- Los artefactos anteriores (respuestas, `historial_cierres/`, `auditorias_conocidas.json`) no cambian.

**[Hecho] Los expedientes reales del paquete no cambian.** El único cierre aprobado en uso es el de la 4.6.1, que tiene `cierre_vigente.json` y sigue vigente por las cuatro vías (grupo F). Ningún expediente real tiene un cierre de la 4.8.1. El expediente de la 4.6 (sin `cierre_vigente.json`) es histórico y no se modifica. Si se volviera a ejecutar sobre él `ficha.py`, ya no se cerraría con cualquier APROBADO: haría falta una auditoría nueva, como ya preveía la 4.6.1 para esos expedientes. Por eso su control da 23 de 24 sobre el árbol 4.9 (§5).

**Más archivos que no se pueden leer (V-1 y V-2, control de vigencia).**
- `material_auditoria.json` ilegible o sin «id» y «archivos»: motivo de retirada.
- `ficha.json` ilegible: `motivo_vigencia` ya no lo toma por «sin salida cerrada», sino como una salida oficial que no puede acreditarse. El paso 14, `informe.py` y `resumen.py` la archivan y retiran la aprobación. `ficha.py` hace lo mismo y no vuelve a cerrar: hace falta una auditoría nueva (W-2; la primera corrección de V-1 la reescribía, y el segundo control de vigencia mostró que el registro resultante era más débil o no vigente).
- Una ficha cuyo «cierre» no es un objeto, una solicitud sin «id» y los tipos erróneos de `historial`, `cierres_archivados` o `paso` también son archivos ilegibles (W-1). `pipeline.py` los trata como un estado ilegible: retira y termina con código 6.
- `auditoria.md` sin permiso de lectura no interrumpe el archivado: la retirada sigue y `RETIRADA.json` dice que no se pudo copiar (W-3).
- El nombre de la carpeta del archivo se limpia, así que un identificador con «../» no sale del expediente (W-4).
- Un JSON válido que no es un objeto, o una estructura interna errónea, es un archivo ilegible.
- `estado_pipeline.json` como carpeta: `pipeline.py` retira y termina con código 6. `auditoria.md` como carpeta: motivo de retirada.

**Sin estado, el registro conserva la respuesta aceptada (V-3).** Si `estado_pipeline.json` no existe, `registrar_cierre` conserva de `cierre_vigente.json` la solicitud, la huella fiel y la huella de bytes de la respuesta aceptada cuando la huella fiel del archivo coincide. No registra la huella de bytes del archivo actual.

## 4. Pruebas de aceptación (`personaje_v2/pruebas/test_integridad_auditoria_v2.py`, 103, obligatorias)

La batería es obligatoria en `verificar_paquete.sh completa`: su bloque va antes del de solicitudes y exige al menos 103 pruebas. Lo comprueba `scripts/comprobar_integracion_verificador_49.py`, que da 13 de 13.

**Cómo se prueba.**
- Cada caso parte de una copia del mismo cierre: una respuesta sintética válida a una solicitud, publicada en el resumen predeterminado y en un destino configurado, o el cierre de la 4.6.1 o el de la 4.6.
- Se observa la **primera llamada**: código, estado, auditoría, ficha, informe, `cierre_vigente.json`, las filas de los dos destinos, el historial del resumen y `RETIRADA.json`.
- Las auditorías son sintéticas y lo dicen («(sintético)», «auditoría sintética de la prueba R-V1»).

| Grupo | Qué prueba | Resultado |
|---|---|---|
| A | Cierre base: código 0, concluido/APROBADO, respuesta registrada con su huella fiel | 2/2 |
| B | 7 cambios × 4 vías: solicitud cambiada, eliminada o duplicada; mismas palabras con otro significado; mismas líneas en otro orden; respuesta sustituida; material modificado. Aprobación retirada en la primera llamada (código 4 en el paso 14 y 3 en los generadores), en los dos destinos, con historial y diagnóstico propio | 28/28 |
| C | CRLF (×4 vías), CR, BOM, sin salto final y NFD: siguen vigentes. Espacios al final de línea y línea en blanco intercalada: se retiran | 10/10 |
| D | Destino inaccesible: código 5, «RETIRADA PENDIENTE» con el destino identificado, el pipeline se detiene con 5 y, al restaurar el destino, la retirada se completa | 3/3 |
| E | Reanudación: restaurar los bytes originales no reactiva el cierre; `--desde 13` registra una solicitud nueva, la respuesta antigua no la responde y una respuesta legítima nueva cierra (código 0) y se vuelve a publicar en los dos destinos; el historial conserva el cierre retirado | 3/3 |
| F | Compatibilidad: 4.6.1 vigente por las 4 vías y sin solicitud retroactiva; 4.6.1 en CRLF, retirado; 4.8.1 sin `fiel`: intacta, vigente; con CRLF o reordenada, retirada; 4.9 sin `estado_pipeline.json`: intacta, vigente; reordenada o con otra solicitud, retirada; solicitud no registrada como respondida, retirada | 13/13 |
| I | Hallazgos del control de vigencia. **V-1:** `material_auditoria.json` ilegible (×4 vías) y `ficha.json` ilegible (×4 vías). **V-2:** estado `[]` (`ficha.py` y pipeline), `cierre_vigente.json` `[1]`, `solicitudes_auditoria` como objeto, `auditoria_respuesta` como texto, estado y `auditoria.md` como carpetas. **V-3:** sin estado y en CRLF, `cierre_vigente.json` conserva la respuesta aceptada y, al restaurar los bytes originales, sigue vigente. **Segundo control:** `ficha.json` ilegible por `ficha.py`, con y sin estado, no vuelve a cerrar (W-2); «cierre» que no es un objeto (×2 vías) y solicitud sin «id» (W-1); solicitudes como objeto e «historial» como objeto por el paso 14 (código 6); material con «../» (W-4) | 23/23 |
| H | Hallazgos de la auditoría interna. **Z-1:** 4.6.1 sin `cierre_vigente.json` con otra aprobación (×4 vías), cierre de la 4.6 y cierre de la 4.9 sin estado ni `cierre_vigente.json`: ninguno se vuelve a cerrar ni crea un `cierre_vigente.json`. **Z-2:** no UTF-8 (×4 vías), cp1252, `cierre_vigente.json` ilegible (×2), estado vacío (`ficha.py`) e ilegible (pipeline, código 6): se retira sin traza. **Z-3:** sin estado y en CRLF, vigente por la huella fiel | 16/16 |
| G | Unidades: `huella_fiel` (también los límites de la lista cerrada: NFKC, U+200B, NBSP, U+2028, VT), `huella_contenido` (detector) y H2 idéntica | 5/5 |

**Las baterías anteriores siguen pasando con el código 4.9:** solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55. Los resultados de la verificación final están en `REGISTRO_ENTREGA_4.9.md` §8.

**Mutaciones** (`scripts/mutar_rv1.py`): se probaron **31** mutaciones del código y **las 31 hacen fallar la batería** (`resultados/mutaciones_rv1.json`).
- En la primera tanda (15), la mutación «la huella fiel no tiene en cuenta el orden de las líneas» no la detectaba ninguna prueba. Se añadieron el caso «mismas líneas en otro orden» y una prueba unitaria correcta.
- Tras la auditoría interna (Z-3) se añadieron 8 mutaciones más:
  - límites de la lista cerrada: NFKC, caracteres de formato, NBSP y separadores;
  - la rama de `cierre_vigente.json` con huella fiel;
  - Z-1;
  - Z-2 (no UTF-8 y `cierre_vigente.json` ilegible).
- Tras el control de vigencia se añadieron 5 más (M24–M28): `material_auditoria.json` ilegible, JSON que no es un objeto, `ficha.json` ilegible, el registro sin estado (V-3) y el estado como carpeta.
- Tras el segundo control de vigencia, 3 más (M29–M31): la ficha con «cierre» que no es un objeto, `ficha.py` que vuelve a cerrar sobre una ficha ilegible y el identificador del material sin limpiar en la ruta.

## 5. Límites declarados

- **No hay clasificador de significado.** Una respuesta nueva que diga lo contrario con otras palabras es otra respuesta, y solo la acepta una solicitud nueva (paso 13) con H2.
- **Autoría.** La comprobación garantiza que `auditoria.md` es el texto aceptado según los archivos de registro. Un agente que reescriba de forma coherente `auditoria.md` y los registros que la acreditan no se detecta. Basta con dos archivos: en un cierre de la 4.6.1, `auditoria.md` y `cierre_vigente.json`; en uno de la 4.9, borrar `estado_pipeline.json` y reescribir los otros dos. Es la misma garantía de procedimiento que la autoría humana (sección 8 de `CONTINUIDAD.md`). Borrar archivos de registro, sin reescribirlos, ya no basta (Z-1).
- **Fechas.** Las salidas de los pasos 5–10 siguen con el criterio de fechas (Q-T4, sin cambios).
- **Archivos ilegibles.** Se tratan `auditoria.md`, `estado_pipeline.json`, `cierre_vigente.json`, `material_auditoria.json` y `ficha.json` (Z-2, V-1, V-2 y W-1): que no se puedan leer, que no sean un objeto y los campos que lee el cierre (`cierre` de la ficha; `solicitudes_auditoria`, `auditoria_respuesta`, `historial`, `cierres_archivados` y `paso` del estado; `id` y `archivos` del material). Otros campos internos y otros archivos del expediente (por ejemplo, los JSON de las fases) no se han validado.
- **Permisos.** El caso de `auditoria.md` sin permiso de lectura (W-3) se corrigió leyendo el código; la batería se ejecuta como superusuario y no puede reproducirlo.
- **El expediente histórico de la 4.6 (sin `cierre_vigente.json`).** Por Z-1, `motivo_rechazo_cierre` ya no lo acepta: su control (`…_4_6/scripts/comprobar_cierre_ensayo.py`) da **23 de 24** sobre el árbol 4.9. El único caso que no cumple es «ningún motivo de rechazo». Es la consecuencia buscada, la misma que la 4.6.1 declaró para la vigencia («Expedientes cerrados antes de la 4.6.1: … sus salidas se archivan hasta una auditoría nueva»). El expediente no se modifica. Queda como decisión D-RV1c.

## 6. Auditoría interna

La auditoría interna de Claude, con contexto separado (`AUDITORIA_INTERNA_4_9.md`), encontró dos bloqueantes (Z-1 y Z-2), tres importantes (Z-3 a Z-5) y cinco menores. El control de vigencia posterior (`AUDITORIA_INTERNA_4_9_vigencia.md`) dio todas las correcciones por vigentes, seis con reservas, y encontró siete hallazgos nuevos: uno importante (V-1) y seis menores. Un segundo control de vigencia (`AUDITORIA_INTERNA_4_9_vigencia_2.md`) dio las correcciones de V-1 a V-7 por vigentes, seis con reservas, y encontró seis hallazgos menores más (W-1 a W-6). El tratamiento de todos está en `REGISTRO_ENTREGA_4.9.md` §6, §7 y §7 bis; los de W-1 a W-6 no los ha revisado un control independiente posterior.

## 7. Archivos cambiados

**Modificados:**
- `personaje_v2/scripts/cierre_v2.py`, `pipeline.py`, `ficha.py`, `informe.py` y `resumen.py`;
- `personaje_v2/ANEXO_D_salidas_y_formatos.md` y `personaje_v2/DECISIONES.md`;
- `verificar_paquete.sh`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y `VERSION`.

**Nuevo:** `personaje_v2/pruebas/test_integridad_auditoria_v2.py`.

La lista completa, con las huellas, está en `CAMBIOS_ARCHIVOS.txt`.
