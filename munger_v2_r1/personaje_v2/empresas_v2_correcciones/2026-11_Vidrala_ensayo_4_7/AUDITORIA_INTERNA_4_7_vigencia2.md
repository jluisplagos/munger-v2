# Auditoría interna de Claude · segundo control de vigencia de la entrega 4.7

Es una auditoría interna de Claude con contexto separado, no una revisión externa: el auditor no vio cómo se hicieron los ajustes posteriores al primer control de vigencia. Su alcance es acotado: comprobar si esos ajustes resuelven V-1 a V-7 y si introducen regresiones; no repite una auditoría completa. Se distinguen **hechos comprobados por el auditor**, **interpretaciones** y **propuestas**. Las decisiones que corresponden a la persona responsable solo se proponen. Fecha: 9-nov-2026.

**Declaración de continuidad:** este control lo hace el mismo auditor que el primer control de vigencia. No es independiente de él: conoce sus casos y los repite.

## Material auditado

- `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_7/MATERIAL_VIGENCIA2_4_7.txt`, SHA-256 `2a8716b434c8042b1c5b2b34c52d16757ad9433cc6588875fd1b0587429a9a86`, que coincide con la huella del encargo.
- **Sus 63 huellas coinciden todas.** Se comprobó con `grep -v '^#' MATERIAL_VIGENCIA2_4_7.txt | sha256sum -c`, desde `/home/claude/entrega47/munger_v2_r1/` (al principio y al final) y desde la copia: ninguna línea distinta de OK.
- **Código del primer control:** el de `…/scratchpad/codigo47_vigencia/` tiene las huellas que vio ese control: `cierre_v2.py` `71bf7dfa…`, `resumen.py` `f0fbc0ab…` y `test_resumen_v2.py` `53edc0ac…`.
- **Código actual:** tiene las huellas del CIERRE §5 a las 22:15: `cierre_v2.py` `5137d986…`, `resumen.py` `dbc49cb7…`, `test_resumen_v2.py` `9dd81bb4…` y `verificar_paquete.sh` `47a1e587…`. `pipeline.py`, `ficha.py` e `informe.py` no cambian.
- **Informe del primer control:** `AUDITORIA_INTERNA_4_7_vigencia.md` del paquete es idéntico a él (SHA-256 `e0129349…`).
- **El auditor no modificó nada** en `/home/claude/entrega47/` ni en `/home/claude/entrega461/`:
  - `find /home/claude/entrega47 -newer MATERIAL_VIGENCIA2_4_7.txt` solo devuelve la propia carpeta 4.7, 4 ms posterior, que es la creación de ese archivo;
  - el manifiesto de la 4.6.1 da 0 diferencias;
  - `config_v2.json` del original conserva su huella.
- **Lugar de ejecución:** todo se ejecutó en la copia nueva `/tmp/claude-0/-home-claude/e1d9fd2f-7a4e-5443-8b0f-fae3b340b4cf/scratchpad/vig47b/munger_v2_r1/`, con `PYTHONDONTWRITEBYTECODE=1` y `python3 -B` (o `-I`).
- **Guiones,** en `/tmp/claude-0/-home-claude/e1d9fd2f-7a4e-5443-8b0f-fae3b340b4cf/scratchpad/vig47_pruebas/`:
  - `pruebas_vigencia.py`: los casos V1–V10 del primer control, sin cambios;
  - `pruebas_vigencia2.py`: casos nuevos V11–V13.
- **Salidas,** en `/tmp/claude-0/-home-claude/e1d9fd2f-7a4e-5443-8b0f-fae3b340b4cf/scratchpad/vig47b_out/`.

## Qué se ejecutó

| Comando (en la copia salvo indicación) | Resultado |
|---|---|
| `grep -v '^#' MATERIAL_VIGENCIA2_4_7.txt \| sha256sum -c` (original, solo lectura, y copia) | 63/63 OK en los dos |
| `diff -u` de `codigo47_vigencia/` frente a `personaje_v2/scripts/` y `personaje_v2/pruebas/` | **`cierre_v2.py`:** <br>• la empresa de `sincronizar_resumenes` sale de la ficha o de la ficha cerrada archivada más reciente, y el argumento solo como último recurso (l. 546); <br>• `_fila_aprobada` admite `fechas` (l. 548 y siguientes); <br>• `_fichas_cerradas_archivadas` (l. 565) sustituye a `_empresa_archivada`, que ya no existe. <br>**`resumen.py` sin ficha** aplica el mismo criterio (l. 26–28). <br>**Batería:** la prueba 21 queda dividida y aislada, y hay una prueba nueva, la 21b |
| `cd personaje_v2 && python3 -B pruebas/test_resumen_v2.py` | **34/34 PASAN**, código 0, 22,3 s |
| `cd personaje_v2 && python3 -B pruebas/test_cierre_v2.py` | **55/55 PASAN**, código 0, 2 min 2 s |
| `python3 -I …_4_7/scripts/comprobar_entrega_4_7.py` (desde la raíz de la copia) | código 1, **47 de 49**. Solo fallan los dos controles que esperan este informe. Tipos: 10 reejecutan, 27 recalculan, 12 constatan |
| Totales de `reproduccion/pruebas_resumen_con_codigo_*.txt` | 33/34 con el código del primer control (solo falla la prueba 21 aislada), 30/34 con el de la final, 27/34 con el de control, 19/34 con el de la primera y 6/34 con el de la 4.6.1. Coinciden con el CIERRE §5 y con `DECISIONES.md` |
| `pruebas_vigencia.py` (V1–V10) y `pruebas_vigencia2.py` (V11–V13) | tabla siguiente. V12 cambia `config_v2.json` **de la copia** y lo restaura después; se comprobó que queda idéntico byte a byte |
| Lectura del CIERRE §0 (l. 32–35), §5 (l. 156–183) y §6 (l. 193); del Anexo D (l. 207, 211, 216–217 y 221); de `DECISIONES.md` (l. 176–185); de `CONTINUIDAD.md` (l. 6–10, 70 y 107) y de `VERSION` | ver las tablas |

**Resultados del guion propio (hechos).** Se usan la notación y la disposición del primer control:
- «AP»: fila `concluido / APROBADO` de «Vidrala, S.A.»;
- «RET»: fila «SIN APROBACIÓN VIGENTE …»;
- el predeterminado lleva la aprobación de la 4.6.1 sin registrar.

| Caso | Antes (primer control) | Ahora |
|---|---|---|
| V3: solo `pipeline.py --config … --desde 14` | código 4; el predeterminado, AP | código 4; **el predeterminado, RET** |
| V3c: pipeline dos veces | AP | **RET** |
| V2-pipeline: árbol trasladado, invalidado por el pipeline | el predeterminado trasladado, AP | **RET**; el configurado trasladado, RET; sin pendientes |
| V3b: `informe.py` posterior | RET | RET |
| V6: un hermano en estado temprano publica en el configurado | la fila AP del expediente vigente en el predeterminado pasaba a RET | **sigue AP**; el hermano no crea registro; el original sigue vigente |
| V13 (nuevo): hermano con una ficha cerrada archivada **de otra fecha** que publica en el configurado | — | código 0; la fila del vigente sigue AP |
| V1: solo el expediente, trasladado a un árbol con un CSV ajeno | — | **igual:** por las tres vías directas, RET el real y AP el ajeno; por el pipeline del árbol nuevo, RET los dos; el predeterminado de origen, AP (límite ya declarado) |
| V4: expediente vigente, por cuatro vías | 0 / 0 / 0 / 0, todo AP | **igual** |
| V5: fila de otra empresa en el predeterminado | la de Vidrala, RET; la otra empresa, AP | **igual** |
| V7 / V7b: `resumen.py` sin ficha en un destino recibido | RET y sin publicar; un destino sin la fila queda intacto | **igual** |
| V8: descartes incompletos y completo | 5 / 5 / 5 y `retirada_pendiente`; el completo, 4 / 3 / 3 | **igual** |
| V9: registro sin `registro_id` y copia del árbol | por `informe.py`: la copia AP / RET y el original RET / RET | **igual** por `informe.py`. Por el pipeline de la copia: ahora la copia queda RET / RET (antes RET / AP) y el original RET / RET |
| V10: expediente de referencia de la 4.6.1 | sin cambios | **igual:** vigente, `[]` en las sincronizaciones y ningún archivo cambiado |
| V11 (nuevo): `resumen.py` **con ficha**, material cambiado, hacia el CSV configurado | — | código 3; **tras esa llamada, el predeterminado sin registrar sigue AP**. Un `informe.py` posterior (código 3) lo retira |
| V12 (nuevo): `resumen_csv` fijado en `config_v2.json` del paquete de la copia; invalidación directa por `informe.py`, `ficha.py` o `resumen.py <configurado>` | — | `informe.py` 3 y `ficha.py` 3: el predeterminado sin registrar queda RET. **`resumen.py <configurado>` 3: sigue AP** |

## Estado de V-1 a V-7

| Id | Estado | Evidencia |
|---|---|---|
| V-1 | **resuelto** | `cierre_v2.py` l. 546. V3, V3c y V2-pipeline dejan el predeterminado RET con el pipeline como única llamada. La prueba 21 aislada pasa ahora y falla con el código del primer control (`pruebas_resumen_con_codigo_del_control_de_vigencia.txt`, 33/34) |
| V-2 | **resuelto** | **Corrección:** l. 548 y `_fichas_cerradas_archivadas`, l. 565. <br>**Hermanos:** V6 y V13 no tocan la fila del expediente vigente; la prueba 21b pasa. <br>**F-2 por las vías directas:** se mantiene con `informe.py` y `ficha.py` (V3b y V12) y con `resumen.py` sin ficha (V7, V7b). <br>**Excepción:** no actúa con `resumen.py` con ficha hacia otro destino. Es un hueco anterior a este ajuste, que el primer control no probó (W-1) |
| V-3 | **declarado, con una precisión pendiente** | Anexo D l. 211. La consecuencia declarada coincide con V9 por una vía directa. Por el pipeline de la copia con su configuración, el CSV configurado de la copia sí se retira, porque es el destino de la llamada (W-2) |
| V-4 | **resuelto** | Las frases sobre F-2 están ahora acotadas: <br>• Anexo D l. 207: «siempre que esa fila corresponda a una ficha cerrada que el expediente archivó … la empresa sale de la ficha»; <br>• CIERRE §6 l. 193; <br>• `DECISIONES.md` l. 181. <br>`CONTINUIDAD.md` l. 10 y `VERSION` recogen los dos controles de vigencia y que el primero encontró V-1, que se corrigió. La salvedad de W-1 afecta a la frase «toda invalidación (…, `resumen.py`)» del Anexo D l. 207 |
| V-5 | **resuelto** | `test_resumen_v2.py`: `ok1 = retirada(de(pred))` justo después del pipeline. Las dos comprobaciones van en pasos separados («… la retira por sí sola (código 4)» y «…y resumen.py sin ficha no la reaviva (código 3)») |
| V-6 | **declarado** | Anexo D l. 221: «la entrada vuelve al estado `retirada_pendiente`, conserva los campos escritos y hay que marcarla de nuevo, completa». Coincide con V8 |
| V-7 | **declarado** | Anexo D l. 207 («junto a la ubicación **actual**») y l. 216–217. Coincide con V1 (el predeterminado de origen sigue AP; el pipeline del árbol nuevo retira el CSV de su configuración) |

## Hallazgos nuevos

| Id | Gravedad | Archivo y línea | Descripción | Evidencia | Propuesta |
|---|---|---|---|---|---|
| W-1 | menor | `personaje_v2/scripts/resumen.py` l. 37–42 (rama de la ficha cerrada no vigente: `archivar_salidas(c, …, csv_path)` y `retiradas_pendientes`, sin `sincronizar_resumenes`); Anexo D l. 207 | **`resumen.py` con ficha invalidada hacia un destino distinto del predeterminado no retira, en esa llamada, la aprobación sin registrar del predeterminado.** `archivar_salidas` retira en el destino de la llamada y en los registrados, pero esa rama no sincroniza. `informe.py` y `ficha.py`, en cambio, sincronizan después de archivar. No es una regresión: el código del primer control hace lo mismo. Ese control dio por resueltas «las vías directas» sin haber probado esta. | **Hechos:** <br>• V11: tras la llamada, el predeterminado sigue AP; un `informe.py` posterior lo retira; <br>• V12-resumen_otro: con `resumen_csv` fijado en el paquete, ocurre lo mismo; <br>• V12-informe y V12-ficha sí lo retiran. <br>**Interpretación:** la aprobación solo sobrevive hasta la siguiente sincronización por cualquier vía. Hoy `config_v2.json` no fija `resumen_csv`. Contradice la frase «toda invalidación (…, `resumen.py`) … También retira allí una aprobación publicada antes de la 4.7 sin registrar» | Llamar a `CIE.sincronizar_resumenes(c, pipeline.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c)` tras `archivar_salidas` en esa rama, como en `informe.py` l. 66. Añadir la prueba (V11). O, como mínimo, matizar el Anexo D l. 207. Por lectura y sin probar: `ficha.py` l. 179 (sustitución de una ficha cerrada) tampoco sincroniza tras archivar |
| W-2 | observación | Anexo D l. 211 (límite de V-3) | La consecuencia declarada («la copia retirara las filas del original y dejara aprobado su propio CSV configurado») vale para las vías directas. Por el pipeline de la copia con su configuración, el CSV configurado de la copia se retira, porque es el destino de la llamada. | V9-informe frente a V9-pipeline | Añadir «al invalidarla por una vía directa». Sin cambio de código |
| W-3 | observación | `CONTINUIDAD.md` l. 107; raíz del paquete | Sigue pendiente del empaquetado lo que ya señalaba F-7: <br>• no existen `REGISTRO_ENTREGA_4.7.md` ni `resultados/comprobar_entrega_4_7_salida.txt`; <br>• `MANIFIESTO_SHA256.txt` (`cbf63486…`) y `CAMBIOS_ARCHIVOS.txt` (`7affba59…`) siguen siendo los de la 4.6.1. | `ls` y `sha256sum` en el original | Generarlos al empaquetar |

## Comprobaciones sin hallazgo

- **V-1:** la empresa ya no puede salir de `Pipeline.E` mientras haya ficha o ficha cerrada archivada. En el expediente de referencia, las dos dan «Vidrala, S.A.».
- **V-2:**
  - el criterio de fecha solo se aplica a la retirada del predeterminado sin registrar;
  - las publicaciones registradas y el destino de la llamada se retiran igual que antes (V1, V5 y V7);
  - un estado temprano sin fichas cerradas archivadas no retira nada (V6 y la prueba 9).
- **Regresiones:** no se observan.
  - las 32 pruebas anteriores siguen pasando y las dos nuevas también;
  - `test_cierre_v2.py` da 55/55;
  - el comprobador da 47 de 49, con las integraciones 13 de 13, el bloque B regenerado byte a byte y las referencias de la 4.6.1 intactas;
  - el expediente de referencia de la 4.6.1 no cambia (V10).
- **Documentación:**
  - el CIERRE §0 (l. 32–35) describe en orden el material del primer control, ese control, los ajustes y las huellas de las 22:15;
  - el §5 da las huellas que tiene el código y los totales que dan las reproducciones;
  - `DECISIONES.md` l. 181–185 cuenta lo ocurrido.
  - **Anticipaciones:** `CONTINUIDAD.md`, `VERSION` y `DECISIONES.md` dicen que un segundo control revisó el ajuste. Este informe lo confirma para V-1 y V-2, con la salvedad de W-1.

## Veredicto

**Sin hallazgos bloqueantes**: los ajustes resuelven V-1 y V-2, y no se pierde F-2 en `informe.py`, `ficha.py` ni en `resumen.py` sin ficha. La prueba 21 queda aislada (V-5) y V-3, V-6 y V-7 están declarados en el Anexo D de acuerdo con lo observado. Las baterías dan 34/34 y 55/55, el comprobador 47 de 49 a falta de este informe, y V4, V5, V7, V8 y V10 siguen igual. Quedan tres puntos que la persona responsable debería conocer:
- **W-1 (menor):** `resumen.py` con ficha invalidada hacia un destino distinto del predeterminado no retira, en esa llamada, la aprobación sin registrar del predeterminado. La retira la siguiente sincronización por cualquier vía. El primer control no lo probó. El arreglo propuesto es una llamada a `sincronizar_resumenes`; si no se aplica, conviene matizar el Anexo D l. 207.
- **W-2 (observación):** la declaración de V-3 debería decir que vale para las vías directas.
- **W-3 (observación):** sigue pendiente el empaquetado de F-7.
