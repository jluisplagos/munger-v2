# Cierre técnico del bloque A · reparación del resumen configurado (entrega 4.7)

Es una declaración de Claude; nada de esto está comprobado externamente por ChatGPT. El cierre técnico tiene cuatro fechas (9-nov-2026, UTC):
- el **primer cierre** (20:20), anterior a la primera auditoría interna;
- el **cierre revisado** (21:05), tras corregir sus hallazgos;
- el **cierre final** (21:36), tras la auditoría de control;
- el **cierre definitivo** (21:58), tras la auditoría final, con los ajustes del control de vigencia (22:15).

## 0. Orden real de los trabajos

El encargo pide registrar el cierre técnico antes de introducir variantes financieras. Lo que ocurrió no siguió del todo ese orden, y se declara así.

| Momento (UTC, 9-nov-2026) | Hecho |
|---|---|
| antes de las 20:20 | Bloque A implantado y probado: 18/18 y 55/55, reproducciones e integración en el verificador. `scripts/analisis_n1_n3.py`, la réplica y la matriz en Python, ya se había redactado y ejecutado. Es de solo lectura sobre el expediente de referencia y no escribe ningún libro |
| 20:20 | Comprobaciones del primer cierre y huellas del código, registradas en la §2 |
| 20:26 | `scripts/propuesta_excel.py` genera los dos libros de propuesta |
| 20:28 | Se escribe este documento por primera vez. Decía que el cierre se había registrado «antes de introducir variantes financieras en ningún libro de propuesta», pero el archivo se escribió después de los libros (auditoría interna, H-17). Las huellas de código que registraba sí eran las de las 20:20 |
| ≈ 20:40 | Auditoría interna de Claude sobre el material fijado (`MATERIAL_AUDITADO_4_7.txt`): tres hallazgos importantes del bloque A (H-1 a H-3) y varios menores |
| 20:53–20:59 | Código del bloque A corregido (`cierre_v2.py` 20:53, `resumen.py` y `pipeline.py` 20:54) y batería ampliada a 24 pruebas, ejecutada contra el código nuevo, el auditado y el de la 4.6.1 |
| 20:59–21:03 | **Bloque B rehecho** antes del cierre revisado: formulación anterior del N1 conservada (20:59), script y matriz nuevos (21:02), libros de propuesta regenerados (21:02–21:03) |
| 21:05 | **Cierre revisado**, en la §3. Después, la cabecera de `verificar_paquete.sh` se ajusta (21:05:44), tras la salida conservada de su integración (20:59) |
| 21:09 | Se fija el material de la auditoría de control (`MATERIAL_CONTROL_4_7.txt`) |
| ≈ 21:10–21:28 | Auditoría de control de las correcciones: sin bloqueantes; dos hallazgos importantes (C-1 y C-2) y varios menores |
| 21:30–21:35 | Correcciones de C-1 a C-3 y salida humana de C-2 (`cierre_v2.py` 21:30), batería ampliada a 29 pruebas (21:31) y observaciones C-7, C-8 y C-11 en el bloque B (21:35). Las cifras financieras no cambian y los libros de propuesta no se regeneran, porque T1 y M1 son los mismos |
| 21:35 | También se editan `verificar_paquete.sh` (mínimo 29) y `comprobar_integracion_verificador_47.py`, y se regenera su salida (auditoría final, F-8) |
| 21:36 | **Cierre final**, en la §4 |
| 21:38 | Se fija el material de la auditoría final (`MATERIAL_FINAL_4_7.txt`) |
| ≈ 21:39–21:52 | Auditoría final: sin bloqueantes; dos hallazgos importantes (F-1, una regresión de la corrección de C-2, y F-2, un hueco anterior a la 4.7) y varios menores |
| 21:52–21:58 | Correcciones de F-1, F-2, F-3 y F-5a (`cierre_v2.py` y `resumen.py`, 21:52); batería de 32 pruebas, ejecutada contra el código actual y el de cada auditoría; verificador con mínimo 32; documentación de F-4 a F-9 |
| 21:58 | **Cierre definitivo**, en la §5 |
| 21:59 | Se fija el material del control de vigencia (`MATERIAL_VIGENCIA_4_7.txt`) |
| ≈ 22:00–22:10 | Control de vigencia: sin bloqueantes. Un hallazgo importante: V-1, F-2 no actuaba por el pipeline configurado porque el pipeline pasa el nombre de la carpeta como empresa. Varios menores (V-2 a V-7) |
| 22:10–22:15 | Ajustes del control de vigencia: la empresa se toma de la ficha y se exige que la fila sea de una ficha cerrada archivada por el expediente (V-1, V-2); prueba 21 aislada y prueba nueva 21b (V-5); V-3, V-6 y V-7 declarados en el Anexo D. Batería de 34 pruebas y verificador con mínimo 34 |
| 22:15 | Huellas definitivas (§5). Los ajustes pasan por un segundo control de vigencia (`AUDITORIA_INTERNA_4_7_vigencia2.md`) |

Los libros de propuesta y la matriz no usan el código del bloque A. Las variantes financieras no dependen de su cierre ni lo modifican. Las ejecuciones con el código de la 4.6.1 dejaron cachés de bytecode (`__pycache__`, 4 archivos `.pyc`) en el árbol de trabajo de la 4.6.1 (`/home/claude/entrega461/`, fuera del paquete). Las 1.354 huellas de su manifiesto siguen intactas. Desde la auditoría de control se usa `PYTHONDONTWRITEBYTECODE=1` (C-9).

## 1. Primer cierre (20:20 UTC): hechos

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Reproducción con el código 4.6.1 (árbol íntegro de la 4.6.1) | el fallo se reproduce en las dos rutas | `reproduccion/reproduccion_resumen_codigo_4_6_1.txt` |
| Reproducción con el código 4.7 | «NO SE REPRODUCE» en las dos rutas | `reproduccion/reproduccion_resumen_codigo_4_7.txt` |
| `test_resumen_v2.py`, versión de 18 pruebas | 18/18 con el código 4.7; 5/18 con el 4.6.1 | conservadas en la primera auditoría |
| `test_cierre_v2.py` | 55/55 | — |
| Expediente de referencia de la 4.6.1 con el código 4.7 | vigente, sin retiradas pendientes y sin `publicaciones_resumen.json` | consulta directa a `cierre_v2` |

## 2. Huellas del primer cierre (código auditado)

| Archivo | SHA-256 a las 20:20 UTC |
|---|---|
| `personaje_v2/scripts/cierre_v2.py` | `340b86561867d3da4185e16ed5ecbadc6d63d34fceed0f5c54155a8f830d2f79` |
| `personaje_v2/scripts/ficha.py` | `7760643ff7fd28ab971418d40448dd1630f458781cefab08125bcc9083e62bdb` |
| `personaje_v2/scripts/informe.py` | `ac9d33b57817f69d6ab05f00640ac19577f714b3c80efa04aaa85e59b11b14a8` |
| `personaje_v2/scripts/pipeline.py` | `5855d3127809396713368a15d97e103589b9bf6c34b3774b1dcbeddf4ce532fd` |
| `personaje_v2/scripts/resumen.py` | `67d7722abf225fa616c9f348941c68e0cae8b2a31007064cd9666714fe2349b3` |
| `verificar_paquete.sh` | `53fd6c19f39e533152a1838294228b114b7aef8c9b00eec0c0529bd395c9ab68` |
| `personaje_v2/pruebas/test_resumen_v2.py` | `01e78e9a23126be4780d5e4434690e2b08d4730a2a31228c17250135a2c628b3` |

## 3. Cierre revisado (21:05 UTC) tras la auditoría interna

| Hallazgo | Corrección | Prueba nueva o ampliada |
|---|---|---|
| H-1 · destino ausente marcado «retirada» | Si la carpeta del destino no está accesible, la retirada queda pendiente (código 5). Si falta el CSV en una carpeta accesible, la entrada queda `sin_archivo` y se vuelve a comprobar en cada sincronización | «carpeta del destino ausente…», «CSV ausente en carpeta accesible…» |
| H-2 · ligado por ruta absoluta | Ruta real (`realpath`). Las entradas de una ruta que ya no existe (expediente trasladado o renombrado) se adoptan y se anotan en `trasladado_desde`. Las de otra ruta que sigue existiendo son de otro expediente, el original de una copia, y no se tocan | «expediente trasladado o renombrado…» |
| H-3 · `resumen.py` sin ficha | Sin `ficha.json` sincroniza, informa de las retiradas pendientes y termina con 5 o 3, sin publicar | «resumen.py con las salidas archivadas…» |
| H-8 · registro borrado o ilegible | Un registro ilegible se trata como retirada pendiente (código 5) y no se sobrescribe. Cada cambio escribe además un respaldo (`.publicaciones_resumen.respaldo.json`), que se usa si falta el registro | «registro ilegible…», «registro borrado…» |
| H-9 · código 5 nacido dentro de la ejecución | El pipeline comprueba las retiradas pendientes también al terminar, sea cual sea el código (0, 4 o 10), y devuelve 5 si las hay | por lectura de código; no hay prueba que lo provoque sin agentes |
| H-18 · historial predeterminado | La prueba de la secuencia comprueba también el historial del resumen predeterminado | prueba 2 ampliada |
| H-7 · CSV compartido | **No se corrige; se documenta.** La fila del resumen se identifica por empresa, sin el material ni el expediente, y añadirlos cambiaría el formato del Anexo D. Si dos expedientes de la misma empresa publican en el mismo CSV, invalidar uno retira también la fila del otro, y una copia invalidada con la configuración compartida retira la fila del original. Es el sentido conservador: quita una aprobación, no la crea | — |
| Límite residual de H-8 | Si se borran a la vez el registro y su respaldo, el expediente no tiene forma de saber dónde publicó | — |

**Resultados del cierre revisado:**
- `test_resumen_v2.py`: **24/24** con el código revisado (`resultados/test_resumen_v2_salida.txt`);
- la misma batería da **18/24** con el código auditado, con las 6 pruebas nuevas en FALLA (`reproduccion/pruebas_resumen_con_codigo_4_7_auditado.txt`), y **5/24** con el de la 4.6.1 (`reproduccion/pruebas_resumen_con_codigo_4_6_1.txt`);
- `test_cierre_v2.py`: 55/55 (`resultados/test_cierre_v2_salida_codigo_4_7.txt`);
- verificador: el mínimo del bloque del resumen sube a 24; las dos integraciones dan 13 de 13;
- el expediente de referencia de la 4.6.1 sigue vigente, sin registro de publicaciones.

**Huellas del cierre revisado** (sustituidas por las del cierre final en `cierre_v2.py`, `verificar_paquete.sh` y `test_resumen_v2.py`):

| Archivo | SHA-256 a las 21:05 UTC |
|---|---|
| `personaje_v2/scripts/cierre_v2.py` | `2e0904a2479869db2a3303266e7f111237ff3563c4d9038722d9115b1232b12b` |
| `personaje_v2/scripts/ficha.py` | `7760643ff7fd28ab971418d40448dd1630f458781cefab08125bcc9083e62bdb` |
| `personaje_v2/scripts/informe.py` | `ac9d33b57817f69d6ab05f00640ac19577f714b3c80efa04aaa85e59b11b14a8` |
| `personaje_v2/scripts/pipeline.py` | `ee4ab923f38c56be95c0cc7fd24b9ded7e2c6464d7f2cba9cd9d5a66d6e7a73f` |
| `personaje_v2/scripts/resumen.py` | `dacbb38ac6ac2df1d19090b2efb395c975ab1cbbb38a56b27d172c5e0f20a8f8` |
| `verificar_paquete.sh` | `ffcf6d4faf13a592afc7aecb5ad2144e7a841ce52d95cec9860c2b76094f76e0` |
| `personaje_v2/pruebas/test_resumen_v2.py` | `65135e5a5fea7b71a7bfa0ac4aeacb7e525490fdcfbdc675d3ee0f330dfed09d` |

La huella de `verificar_paquete.sh` incluye el ajuste de la estimación de tiempo de su cabecera. `scripts/comprobar_entrega_4_7.py` compara el código actual con esta segunda tabla.

## 4. Cierre final (21:36 UTC) tras la auditoría de control

| Hallazgo de control | Corrección | Prueba |
|---|---|---|
| C-1 · copia del árbol con el original vivo; otro expediente en la ruta antigua | El registro lleva un `registro_id`. Si una entrada es de otra ruta y allí sigue un expediente con el **mismo** `registro_id`, este es una **copia**: registra como propios los destinos equivalentes (ruta trasladada) que existan y sean distintos de los del original, recibe un `registro_id` nuevo y guarda las entradas del original en `heredadas_del_original`, sin tocar sus filas. Si no (ruta ausente, otro expediente o sin registro), es el **original trasladado o renombrado** y adopta sus entradas | «copia de todo el árbol…», «expediente renombrado con otro expediente en la ruta antigua…» |
| C-2 · traslado completo con código 5 permanente | Al adoptar, cada destino usa la ruta trasladada si existe. **Salida humana:** la persona responsable puede marcar una entrada con estado «descartada», `descartado_por` y `fecha_descarte`; esa entrada deja de bloquear. Claude no lo hace | «traslado de todo el árbol…»; «destino que no volverá…», con un registro humano simulado en la prueba |
| C-3 · registro ilegible | Se retiran igualmente el destino conocido de la llamada y los del respaldo, si es legible, y el código sigue siendo 5. La escritura es atómica (temporal y `os.replace`). La recuperación desde el respaldo se avisa por la salida de error | «registro ilegible: … se retiran el resumen predeterminado y los destinos del respaldo legible» |
| C-4 · redacción | Anexo D y §5: la copia respeta lo del original **mientras este siga en la ruta registrada con el mismo registro**. Si el original se movió o se borró, la copia adopta y retira, en el sentido conservador | — |
| C-5, C-6, C-9 | Orden real completo (§0); documentación ajustada a los veredictos reales; cachés declaradas | — |
| C-10 · punto de montaje vacío | **No se corrige; se declara** en el Anexo D: una carpeta accesible y vacía, por ejemplo una unidad desmontada con su punto de montaje presente, deja la entrada `sin_archivo` (código 3), que se revisa en cada sincronización | — |
| C-12 · veredicto anclado | El comprobador lee el veredicto en la línea que sigue a «## Veredicto» | — |

**Resultados del cierre final:**
- `test_resumen_v2.py`: **29/29** con el código final;
- con el código de la auditoría de control, 25/29: fallan las 4 de C-1a, C-1b, C-2 y C-3. La de la salida humana pasa también con ese código, porque una entrada «descartada» nunca contó como viva; la prueba deja fijada la salida;
- con el código de la primera auditoría, 18/29; con el de la 4.6.1, 5/29;
- `test_cierre_v2.py`: 55/55;
- mínimo del verificador: 29; integración: 13 de 13.

**Huellas del cierre final** (sustituidas por las del cierre definitivo en `cierre_v2.py`, `resumen.py`, `verificar_paquete.sh` y `test_resumen_v2.py`):

| Archivo | SHA-256 a las 21:36 UTC |
|---|---|
| `personaje_v2/scripts/cierre_v2.py` | `eb94596659219b0abe3676aa54cc0929119da1430f81f4770410c108c0f75b7e` |
| `personaje_v2/scripts/ficha.py` | `7760643ff7fd28ab971418d40448dd1630f458781cefab08125bcc9083e62bdb` |
| `personaje_v2/scripts/informe.py` | `ac9d33b57817f69d6ab05f00640ac19577f714b3c80efa04aaa85e59b11b14a8` |
| `personaje_v2/scripts/pipeline.py` | `ee4ab923f38c56be95c0cc7fd24b9ded7e2c6464d7f2cba9cd9d5a66d6e7a73f` |
| `personaje_v2/scripts/resumen.py` | `dacbb38ac6ac2df1d19090b2efb395c975ab1cbbb38a56b27d172c5e0f20a8f8` |
| `verificar_paquete.sh` | `5ca246f09d997829c92705f44ea78afe98553ce1b9d2a304b860668062dc6c47` |
| `personaje_v2/pruebas/test_resumen_v2.py` | `6254512593679220fa1cc0c66576fd3f2cc196aea3733f4c8b9dbbfedcfc393e` |

## 5. Cierre definitivo (21:58 UTC) tras la auditoría final

| Hallazgo final | Corrección | Prueba |
|---|---|---|
| F-1 · regresión: la traslación sustituía un destino accesible por un CSV ajeno equivalente | Solo se traslada un destino cuya carpeta registrada ya no está accesible; si lo está, se conserva el registrado | «expediente trasladado a un árbol con un CSV equivalente ajeno…» |
| F-2 · aprobación sin registrar (anterior a la 4.7) en el resumen predeterminado | El resumen predeterminado del expediente es siempre un destino conocido. Sin salida oficial vigente, una fila APROBADO de la empresa allí se retira. `resumen.py` sin ficha retira también en el destino que recibe | «aprobación sin registrar en el resumen predeterminado…» |
| F-3 · descarte incompleto | Un descarte sin `descartado_por` o sin `fecha_descarte` sigue como retirada pendiente (código 5) | «descarte incompleto (falta descartado_por)…» |
| F-5a · registros sin `registro_id` | Sin `registro_id` no se reconoce ninguna copia; cualquier otra ruta se trata como traslado | — |
| F-4, F-5b, F-6 | Declarados como límites, o redacción corregida, en el Anexo D | — |
| F-7, F-8, F-9 | `CONTINUIDAD.md` y `VERSION` ajustados; filas del §0; efecto sin 2024 calculado con la réplica en el informe financiero | — |

**Resultados:**
- `test_resumen_v2.py`: **32/32** con el código definitivo;
- con el código de cada auditoría: 29/32 (final), 26/32 (control) y 18/32 (primera); con el de la 4.6.1, 5/32 (`reproduccion/pruebas_resumen_con_codigo_de_la_*.txt` y `…_4_6_1.txt`);
- `test_cierre_v2.py`: 55/55;
- mínimo del verificador: 32; integración: 13 de 13;
- controles de la 4.6.1 sobre su expediente: 23 de 23.

**Huellas del cierre definitivo antes del control de vigencia** (21:58; cambian `cierre_v2.py`, `resumen.py`, `verificar_paquete.sh` y `test_resumen_v2.py`):

| Archivo | SHA-256 a las 21:58 UTC |
|---|---|
| `personaje_v2/scripts/cierre_v2.py` | `71bf7dfa3415396c0c60d5654d709820343afa586481e73b2741ee0f7a65b93d` |
| `personaje_v2/scripts/ficha.py` | `7760643ff7fd28ab971418d40448dd1630f458781cefab08125bcc9083e62bdb` |
| `personaje_v2/scripts/informe.py` | `ac9d33b57817f69d6ab05f00640ac19577f714b3c80efa04aaa85e59b11b14a8` |
| `personaje_v2/scripts/pipeline.py` | `ee4ab923f38c56be95c0cc7fd24b9ded7e2c6464d7f2cba9cd9d5a66d6e7a73f` |
| `personaje_v2/scripts/resumen.py` | `f0fbc0ab13c6f34ad3010708df306b64fddfc01da229a348ff2faa571d4570e2` |
| `verificar_paquete.sh` | `da5fead2f92ed0089f58e30a6a58b1e3ba3b0e335eda9178ab348807d0948674` |
| `personaje_v2/pruebas/test_resumen_v2.py` | `53edc0acaffcc95d60bea80af4f7a93786116251447dbd55b088a2b50bc8f82b` |

**Ajustes del control de vigencia (22:15 UTC):**

| Hallazgo | Ajuste | Prueba |
|---|---|---|
| V-1 · el pipeline pasaba como empresa el nombre de la carpeta | La empresa sale de la ficha o de la ficha cerrada archivada; el argumento solo se usa como último recurso | prueba 21, aislada: «… la invalidación por el pipeline configurado la retira por sí sola» |
| V-2 · un expediente hermano retiraba la fila de otro | Solo se retira una fila del predeterminado sin registrar si corresponde a una ficha cerrada que este expediente archivó: misma empresa y misma fecha | prueba 21b, «fila aprobada del predeterminado que no corresponde a una ficha cerrada de este expediente: no se retira» |
| V-3, V-6, V-7 | Declarados en el Anexo D | — |

**Resultados tras los ajustes:**
- `test_resumen_v2.py`: **34/34**;
- con el código de cada control: 33/34 (vigencia), 30/34 (final), 27/34 (control) y 19/34 (primera);
- con el de la 4.6.1: 6/34. La prueba 21b pasa también con códigos anteriores, que no retiraban el predeterminado sin registrar, y deja fijado el criterio;
- `test_cierre_v2.py`: 55/55;
- mínimo del verificador: 34; integración: 13 de 13.

**Huellas del cierre definitivo:**

| Archivo | SHA-256 a las 22:15 UTC |
|---|---|
| `personaje_v2/scripts/cierre_v2.py` | `5137d98695e2a843a02b575016c05eea2ebd512918a6704742d0a04e63b774e3` |
| `personaje_v2/scripts/ficha.py` | `7760643ff7fd28ab971418d40448dd1630f458781cefab08125bcc9083e62bdb` |
| `personaje_v2/scripts/informe.py` | `ac9d33b57817f69d6ab05f00640ac19577f714b3c80efa04aaa85e59b11b14a8` |
| `personaje_v2/scripts/pipeline.py` | `ee4ab923f38c56be95c0cc7fd24b9ded7e2c6464d7f2cba9cd9d5a66d6e7a73f` |
| `personaje_v2/scripts/resumen.py` | `dbc49cb7ba3191df2ee6ec6ebd8363b56253fe10d41cbdd4033338029d63c6c7` |
| `verificar_paquete.sh` | `47a1e58734cfabe56c4452860bc6254ab40c5926f55315508e44d12da2a0fdb0` |
| `personaje_v2/pruebas/test_resumen_v2.py` | `9dd81bb4a76f705e35e385f5d273d172c30f74109ef857790bfa66ea89ebe0a8` |

`scripts/comprobar_entrega_4_7.py` compara el código actual con esta tabla.

## 6. Qué hace la reparación

El detalle está en el Anexo D, «Destinos registrados del resumen (reparación 4.7)», y en `DECISIONES.md`, 9-nov-2026. En resumen:
- `publicaciones_resumen.json` y su respaldo registran cada destino efectivo (ruta absoluta), la empresa, el expediente (ruta real), el material aprobado y un `registro_id`;
- todas las vías de invalidación retiran la aprobación en esos destinos, aunque las salidas ya estén archivadas, y sin buscar en el sistema de archivos más allá de la ruta equivalente de un destino ya registrado;
- un destino inaccesible o un registro ilegible deja «retirada pendiente» con su error y el código 5, hasta que vuelve el acceso o la persona responsable descarta el destino;
- **copias:** una copia con el original vivo en su ruta registrada retira solo en sus propios destinos;
- **traslados:** un expediente o un árbol trasladado conserva sus publicaciones;
- el resumen predeterminado de la ubicación actual es un destino conocido, también para una aprobación sin registrar que corresponda a una ficha cerrada archivada por el expediente;
- **límites declarados:** el CSV compartido (H-7) y su extensión a una copia llevada a otro árbol (F-4), los registros y respaldos borrados a la vez, el punto de montaje vacío (C-10) y la copia colocada en la ruta antigua antes de sincronizar (F-5b).

Cifras, fuentes, fases, libros y el registro humano P1 (SHA-256 `b4e47afc…c445a4`) siguen idénticos a la 4.6.1. Los valores de control son 53,67 / 70,77 / 86,49, ponderado 70,50 y precio de Sí 65,69. Son resultados mecánicos del ensayo, no una comparación válida con el precio de 87,9 del 3-nov-2026.
