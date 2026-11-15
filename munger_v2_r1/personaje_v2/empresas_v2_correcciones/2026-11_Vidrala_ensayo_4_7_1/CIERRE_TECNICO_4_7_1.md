# Cierre técnico de W-1 · entrega 4.7.1

Es una declaración de Claude; nada de esto está comprobado externamente por ChatGPT. El primer cierre se registró el 10-nov-2026 a las 09:58 UTC, antes de la auditoría interna de Claude de la 4.7.1. Esa auditoría encontró un hallazgo bloqueante (W-a) y otros menores e importantes, y el cierre se revisó: la §5 recoge los cambios y la §6, las huellas del cierre revisado.

## 1. El hallazgo

La revisión independiente de la 4.7 (§1) reprodujo W-1, que la propia 4.7 había dejado declarado como abierto. La secuencia fue esta:
- se parte de una copia del expediente aprobado de la 4.6.1, con la aprobación anterior a la 4.7 sin registrar en `resumen_v2.csv`;
- se añade un marcador en `fase_c.json → celdas.B101`;
- se ejecuta `resumen.py COPIA OTRO_DESTINO.csv`.

El resultado: código 3, salidas archivadas, y la fila del resumen predeterminado sigue en «concluido / APROBADO». La rama de ficha cerrada no vigente de `resumen.py` archivaba, pero no sincronizaba.

## 2. Reparación (primer cierre, 09:58 UTC)

| Archivo | Cambio |
|---|---|
| `personaje_v2/scripts/resumen.py` | En la rama de ficha cerrada no vigente, tras `archivar_salidas`, llama a `sincronizar_resumenes` y luego a `retiradas_pendientes`, como hace `informe.py`. Termina con código 5 si queda una retirada pendiente y con 3 si no |
| `personaje_v2/scripts/ficha.py` | En la ruta análoga que señaló el auditor interno de la 4.7, la sustitución de una ficha cerrada, sincroniza en la misma llamada tras escribir la ficha nueva (código 5 si queda pendiente). Esa sustitución archiva la anterior y deja el pipeline sin aprobación registrada, como en la 4.6.1 |
| `personaje_v2/scripts/cierre_v2.py` | `sincronizar_resumenes` identificaba la aprobación sin registrar del predeterminado por su contenido publicado exacto frente a las fichas cerradas archivadas, y la conservaba si era la de la ficha oficial vigente. **La auditoría interna lo encontró defectuoso (W-a): ver §5** |
| `personaje_v2/pruebas/test_resumen_v2.py` | Tres pruebas nuevas (23–25): la secuencia de la revisión, el otro destino también aprobado y la sustitución en `ficha.py`. **En esta primera versión no comprobaban juntos todo lo pedido (W-c): la 23 solo miraba el historial del predeterminado y la 24, solo las filas. Ver §5** |
| `verificar_paquete.sh` | Mínimo de la batería del resumen: 37 (45 desde la §5) |

## 3. Observación sobre `ficha.py`

No es un cambio, sino un comportamiento previo, de la 4.6.1. Al sustituir una ficha cerrada, `ficha.py` escribe la nueva con su `cierre`, devuelve 0 y deja el pipeline sin aprobación registrada. Esa ficha no es vigente, e `informe.py` y `resumen.py` la rechazan después. Desde la 4.7.1, la retirada ocurre en la misma llamada y la salida lleva un «AVISO» (W-d). Si `ficha.py` debe negarse a escribir la ficha nueva lo decide la persona responsable; no se ha cambiado.

Dentro del pipeline, la misma sustitución terminaba en «concluido · APROBADO», código 0, sin ficha ni informe y con el estado sobrescrito (W-e, anterior a la 4.7.1). Desde la §5 termina con código 4.

## 4. Huellas del primer cierre (09:58 UTC, material de la auditoría interna)

| Archivo | SHA-256 a las 09:58 UTC |
|---|---|
| `personaje_v2/scripts/cierre_v2.py` | `f7f281861a3db6c44a17214366222c01b225277bc1c8f0655dff4f02934a381f` |
| `personaje_v2/scripts/ficha.py` | `62ac0c4ec83093d271d4f92c2cbf48d3d6b8101f63396b89ab5732e681c850fd` |
| `personaje_v2/scripts/informe.py` | `ac9d33b57817f69d6ab05f00640ac19577f714b3c80efa04aaa85e59b11b14a8` |
| `personaje_v2/scripts/pipeline.py` | `ee4ab923f38c56be95c0cc7fd24b9ded7e2c6464d7f2cba9cd9d5a66d6e7a73f` |
| `personaje_v2/scripts/resumen.py` | `8e289606f6fdc4298716113bda659ec2c76107b1994afca8e7091c7a94f56382` |
| `verificar_paquete.sh` | `34bf9ab9ef09efb987b909c6032fa7a91c9c4277fddbe7081335ccbacd57c3c6` |
| `personaje_v2/pruebas/test_resumen_v2.py` | `9017a54e597c14337f71ab016376b167051e7cd192edce6f6efdbf53676d3f88` |

## 5. Cierre revisado tras la auditoría interna de Claude

La auditoría (`AUDITORIA_INTERNA_4_7_1.md`, material `MATERIAL_AUDITORIA_4_7_1.txt`) dio «Con hallazgos bloqueantes» (1). Estos son los hallazgos del bloque W y lo que se hizo con cada uno:

| Hallazgo | Gravedad | Corrección |
|---|---|---|
| W-a · el contenido exacto como criterio de detección hacía permanente una aprobación caducada que la 4.7 retiraba (fila reescrita por una hoja de cálculo, ficha editada tras el cierre) | bloqueante | `cierre_v2.py`: la **detección** vuelve a ser la de la 4.7, por empresa y fecha de una ficha cerrada archivada, y la fecha se lee también en los formatos de una hoja de cálculo (`_fechas`, `_misma_fecha`). El contenido solo **excluye** la fila de la ficha oficial vigente, con los números normalizados (`_igual`, tolerancia relativa de 10⁻⁶). Si la exclusión falla, la fila se retira y `resumen.py` la vuelve a publicar. Lo mismo en la rama sin ficha de `resumen.py`. Límite residual declarado en el Anexo D (fecha cambiada o ilegible) |
| W-b · con el registro ilegible, la ruta de W-1 no retiraba el predeterminado | menor | la detección del predeterminado se hace antes de leer el registro y se retira también en la rama del registro ilegible |
| W-c · las pruebas 23–25 no fijaban todo lo pedido | importante | 23 y 24 comprueban ahora de inmediato las dos filas, los dos historiales, las salidas archivadas, `estado_pipeline` (sin cierre ni aprobación, con el archivo en `cierres_archivados`), el registro y el reintento; ocho pruebas nuevas (26–32) cubren W-a (cuatro variantes y la conservación de la fila vigente reescrita), W-b, W-f y W-e |
| W-d · `ficha.py` directo devuelve 0 al sustituir | menor | documentado en el Anexo D y con un «AVISO» en la salida; el cambio de código queda como decisión de la persona responsable |
| W-e · dentro del pipeline, la sustitución terminaba en «concluido», código 0, sin salidas y con el estado sobrescrito | importante (anterior) | `pipeline.py`: tras cada generador de `salidas_finales`, `adoptar_archivo` adopta el archivo que dejaron en el disco (estado, auditoría, paso, `cierres_archivados` e historial). El paso 14 no declara el cierre si ya no existe: termina con «CIERRE RECHAZADO» y código 4. El mensaje final dice ahora «No queda ninguna salida oficial vigente» |
| W-f · un destino «retirada» cuya fila reaparece no se volvía a retirar | menor (anterior) | `retirar_publicaciones` vuelve a retirar el destino de la llamada aunque ya figure en el registro como retirado |
| W-g · la fila retirada del predeterminado decía «material sin registrar» | menor | se pasa el material de la ficha archivada que coincide, que figura en la fila, en el historial y en el registro |

Los hallazgos N-a, N-b y N-c del N3 se corrigieron en `INFORME_N3_SUBSANACION.md` y en D-N3b, sin cambios de cálculo. C-a (el control debe reejecutar), C-b (cabecera del control de integración y el 0 de `ficha.py` en el Anexo D) y C-c (empaquetado) están resueltos en `comprobar_entrega_4_7_1.py`, en la documentación y en el paquete.

**Hechos del cierre revisado:**

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Reproducción de W-1 con el código 4.7 | REPRODUCIDO | `reproduccion/reproduccion_w1_codigo_4_7.txt` |
| La misma secuencia con el código revisado | NO SE REPRODUCE | `reproduccion/reproduccion_w1_codigo_4_7_1.txt` |
| `test_resumen_v2.py`, código revisado | 45/45 | `resultados/test_resumen_v2_salida.txt` |
| La misma batería con el código 4.7 | 35/45: fallan las 3 de W-1 y 7 de las 8 nuevas (pasa la de conservación de la fila vigente) | `reproduccion/pruebas_resumen_con_codigo_4_7.txt` |
| La misma batería con el código que vio la auditoría | 36/45: fallan 9 (la 23 por el material de W-g, la 25 por el aviso de W-d y las 7 nuevas de W-a, W-b, W-e y W-f) | `reproduccion/pruebas_resumen_con_codigo_auditado.txt` |
| `test_cierre_v2.py` | 55/55 | `resultados/test_cierre_v2_salida.txt` |
| `test_pipeline_sintetico.py` (pipeline cambiado) | 30/30, con los mismos nombres que la línea de base (se comprueba en `verificar_paquete.sh completa`) | `resultados/test_pipeline_sintetico_salida.txt` |
| Integración en el verificador | 4.7.1, mínimo 45: 13 de 13. 4.6.1, cierre: 13 de 13 | `resultados/comprobar_integracion_verificador_471_salida.txt` |
| Batería de la 4.7 sobre el árbol 4.7.1 | 46 de 49 | `resultados/comprobar_entrega_4_7_en_arbol_4_7_1.txt` |

Los tres controles de la 4.7 que no cumplen sobre el árbol 4.7.1 están ligados por diseño al código y a la documentación de la 4.7: las huellas del código del bloque A, la integración con un mínimo de 34 y el material de su control de vigencia. Sobre su referencia intacta, el ZIP de la 4.7, da 49 de 49 (verificación de la 4.7; la auditoría interna lo repitió).

## 6. Huellas del cierre revisado

| Archivo | SHA-256 a las 10:53 UTC |
|---|---|
| `personaje_v2/scripts/cierre_v2.py` | `83406153ad6557f99eddd556788aec13185c71465d7a321ddf1ec4d7ce33477a` |
| `personaje_v2/scripts/ficha.py` | `003cbad4959dcc7a7ec8af4fb3d40d933502f21dcdaf7cb172915fade1fae21a` |
| `personaje_v2/scripts/informe.py` | `ac9d33b57817f69d6ab05f00640ac19577f714b3c80efa04aaa85e59b11b14a8` |
| `personaje_v2/scripts/pipeline.py` | `677567c31f8bc760832e279205a2ac30c6f14ff1244990b99ac179ea135ce768` |
| `personaje_v2/scripts/resumen.py` | `9352c5f938ac27fcddfded591c56bec1a437fb5fd58e7cf5fb2af838fe8b8d0a` |
| `verificar_paquete.sh` | `5b771c34906dc8bfe6f4662121f50275edd12a411a595ece8c887161bfba7864` |
| `personaje_v2/pruebas/test_resumen_v2.py` | `223e0095ae574a06b01f187fd36a0f01a6161c3e96800a20786bdda17c64984b` |

`scripts/comprobar_entrega_4_7_1.py` compara el código actual con la última tabla de huellas de este documento.
