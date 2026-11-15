# Segundo control de vigencia de la entrega 4.9 (correcciones de V-1 a V-7)

> **Nota de conservación (añadida al copiar el informe en el expediente; el texto del auditor no se ha modificado).**
> - El control se hizo sobre la copia `/home/claude/vigencia2_4_9/munger_v2_r1`, descompresión del paquete candidato 2, que no forma parte del paquete. El SHA-256 del informe tal como lo entregó el auditor está en `auditoria_interna/AUDITORIA_INTERNA_4_9_vigencia_2.md.sha256`.
> - Los scripts y salidas que cita como `/home/claude/vigencia2_4_9/tmp/<archivo>` se conservan en `auditoria_interna/material_vigencia_2/<archivo>` (y `…/ejecuciones/`). No se conservan las carpetas de escenarios, mezclas de código, temporales ni las matrices N4 reproducidas, que son regenerables.
> - Las cifras de este informe (96 pruebas, 28 mutaciones, 24/93, 39 comprobaciones) son las del material fijado `MATERIAL_VIGENCIA_2_4_9.txt`. Los hallazgos W-1 a W-6 se trataron después; el tratamiento y las cifras finales están en `REGISTRO_ENTREGA_4.9.md` §7 bis. Esos tratamientos no los ha revisado un tercer control independiente.


Auditor interno independiente, en un contexto separado. No participó en el trabajo, ni en la auditoría interna, ni en el primer control de vigencia. Fecha: 11-nov-2026, de 12:28 a 12:50 (CET).

- **Copia auditada:** `/home/claude/vigencia2_4_9/munger_v2_r1`. Las rutas son relativas a `munger_v2_r1/` salvo que empiecen por `/`.
- **Expediente:** `E = personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9`.
- **Espacio del auditor:** `/home/claude/vigencia2_4_9/tmp/` (`TMPDIR=/home/claude/vigencia2_4_9/tmp/tmpdir`).
  - Las salidas están en `…/tmp/ejecuciones/`.
  - Los escenarios de ataque están en `…/tmp/escenarios/`.
  - La reproducción N4 está en `…/tmp/n4rep/`.

**Convenciones.**
- **[Hecho]**: comprobado por el auditor con un comando o una lectura que se cita.
- **[Interpretación]**: juicio del auditor.
- **[Propuesta]**: sugerencia, sin aplicar.

El auditor no ha corregido nada en la copia. Lo que no ejecutó se dice en la §4. Hubo una incidencia propia con LibreOffice, que se declara en la §0.3.

---

## 0. Material, huellas y ejecuciones

### 0.1 Al inicio (12:28)
- **[Hecho]** `E/MATERIAL_VIGENCIA_2_4_9.txt` tiene el SHA-256 `b2fac6fd13dceae9a9e2faf20db9151d38a8dcec0dad81449465e03fec2e6046`, el esperado.
- **[Hecho]** `sha256sum -c` del material, sin la cabecera y desde `munger_v2_r1/`: **150 de 150 OK** (`…/tmp/sha_inicio.txt`).
- **[Hecho]** A las 12:30 se guardó la huella de todo el árbol, salvo `MANIFIESTO_SHA256.txt`: **1.679 archivos** (`…/tmp/arbol_inicio.sha256`). No había `__pycache__` ni `.pyc`, ni ningún archivo posterior al material.

### 0.2 Al final (12:46; `…/tmp/huella_final.txt`)
- **[Hecho]** El material conserva la misma huella y vuelve a dar **150 de 150 OK** (`…/tmp/sha_final.txt`).
- **[Hecho]** El árbol tiene ahora **1.714 archivos**: los mismos 1.679, con las mismas huellas, más **35 archivos nuevos en `personaje_v2/.lo_perfil/`**. La lista está en `…/tmp/ejecuciones/lo_perfil_creado_por_el_auditor.txt`.
- **[Hecho]** Ningún otro archivo cambió. No hay `__pycache__` ni `.pyc`. Todos los comandos se ejecutaron con `python3 -I -B`.
- **[Hecho] Archivos que cambiaron las ejecuciones del auditor:** solo esos 35, creados por la incidencia de la §0.3. No se han borrado: se dejan para que la persona responsable lo decida, y porque son la evidencia de la incidencia. No están en el manifiesto ni en el material.

### 0.3 LibreOffice e incidencia propia
- **[Hecho] Constancia de `pgrep -fa soffice`** antes de cada ejecución larga, en `…/tmp/ejecuciones/pgrep_*.txt`:
  - a las 12:30:49, 12:31:13 y 12:32:04 había un `soffice.bin` de la otra tarea (perfil `/home/claude/verif_c2/…/.lo_perfil`);
  - en las demás constancias, entre 12:34 y 12:44, no había ninguno.
- **[Hecho] Incidencia del auditor (12:36:05–12:36:41).**
  - **Qué pasó.** En el grupo `v3` de `…/tmp/ataques_v2.py`, el auditor llamó a `pipeline.py` sin `--desde` sobre una copia de su espacio a la que acababa de quitar `estado_pipeline.json`. Sin estado, el pipeline empieza en el **paso 0**. Ejecutó los pasos 0 a 10 hasta «ESPERANDO: fase_c_turno2».
  - **Qué lanzó.** Entre otros, `comprobar_entorno.sh`, que llama a `soffice --version`, y `recalc.sh`, que recalcula con `soffice` (12:36:39, con el perfil de la copia del escenario). El historial está en el `estado_pipeline.json` de `…/tmp/escenarios/v3__sin_estado_crlf_restaurar/exp/Vidrala/`.
  - **Qué dejó.** Además del escenario, creó `personaje_v2/.lo_perfil/` en la copia auditada (12:36:10–12:36:33).
  - **Por qué se incumplió la restricción.** El encargo prohíbe LibreOffice y prohíbe los pasos anteriores al 13.
  - **Qué se sabe de la otra tarea.** A las 12:36:04 no había ningún `soffice` suyo en marcha. No se sabe si arrancó uno durante esos ~30 s: los perfiles eran distintos.
  - **Qué se hizo después.** A las 12:37 se añadió al script una salvaguarda que rechaza `pipeline.py` sin estado o con `--desde` menor que 13 (`ataques_v2.py`, función `corre`). Ninguna otra ejecución lanzó LibreOffice.
  - **Efecto sobre los resultados de este informe.** Ninguno: el escenario afectado se descartó y el caso se repitió sin esa llamada (`ataques_v3_fi_tr_h46_salida.txt`).

---

## 1. Vigencia de las correcciones V-1 a V-7

| Id | Veredicto | Evidencia principal |
|---|---|---|
| **V-1** | **Vigente con reservas** | **[Hecho] Código.** `leer_json_control` (l. 309–321) y su uso para `material_auditoria.json` en `motivo_rechazo_cierre` (l. 364–367); `_motivo_estructura` exige «id» de texto y «archivos» como objeto; `motivo_vigencia` (l. 546–550) ya no toma una `ficha.json` ilegible por «sin salida cerrada».<br>**[Hecho] Reproducción** (`ataques_v2.py rep`):<br>• `material_auditoria.json` = «{trunc»: retirada sin traza por el paso 14 (código 4), `ficha.py`, `informe.py` y `resumen.py` (3) y `pipeline.py` sin `--desde` (retira y pide una auditoría nueva, código 10).<br>• `ficha.json` = «{trunc»: retirada sin traza por el paso 14, el pipeline, `informe.py` y `resumen.py`.<br>• `material_auditoria.json` vacío, `[]`, carpeta, con «archivos» como lista o texto, con «id» numérico o sin «id», y `ficha.json` vacía, `[]`, `null` o carpeta: también se retiran sin traza por las vías probadas (`ataques_v2.py rep` y `nuevos`).<br>**Reserva:** por `ficha.py`, la ficha ilegible se archiva y se vuelve a escribir. Con estado, la ficha reescrita no es vigente. Sin estado, `cierre_vigente.json` pierde la solicitud y la huella fiel (**W-2**) |
| **V-2** | **Vigente con reservas** | **[Hecho]** JSON válido que no es un objeto (estado `[]`, `cierre_vigente.json` `[1]`, material `[]`, ficha `[]` o `null`): retirada sin traza por las cuatro vías. `solicitudes_auditoria` como objeto y `auditoria_respuesta` como texto: igual por `ficha.py`, `informe.py` y `resumen.py`. Carpetas (estado, `auditoria.md`, `cierre_vigente.json`, material y ficha): igual por las cuatro vías, y el estado como carpeta también por el pipeline sin `--desde` (código 6). Enlaces rotos o a carpetas y `/dev/null`: ninguno deja la aprobación publicada indebidamente (`ataques_simbolicos_salida.txt`). Archivos de control sin permiso de lectura, como otro usuario (`setpriv`): retirada sin traza (`ataques_permisos_salida.txt`).<br>**Reservas:**<br>• `solicitudes_auditoria` como objeto **por el paso 14** termina con traza y código 1, aunque después de retirar;<br>• una estructura interna errónea de `ficha.json` («cierre» que no es un objeto) o una solicitud pendiente sin «id» da traza por las cuatro vías **con la aprobación publicada** (**W-1**);<br>• un `auditoria.md` sin permiso de lectura deja la aprobación publicada en la primera llamada (**W-3**) |
| **V-3** | **Vigente con reservas** | **[Hecho] Código.** `registrar_cierre`, l. 529–533. **Reproducción** (`ataques_v2.py v3`): sin estado y en CRLF, `ficha.py` termina con 0 y `cierre_vigente.json` conserva `solicitud`, `auditoria_fiel` y `auditoria_sha256` (f29285bf…). Al restaurar los bytes originales, `ficha.py` vuelve a dar 0 con las tres claves iguales, e `informe.py` da 0. La mutación M27 se detecta.<br>**Reserva:** por otra vía (una `ficha.json` ilegible y `ficha.py`), el registro vuelve a perder la solicitud y la huella fiel y guarda la huella de bytes del archivo actual (**W-2**) |
| **V-4** | **Vigente con reservas** | **[Hecho] Código.** `unidad_cabecera` (l. 243–249), `excepciones_estructura` (l. 252–266), `NCI_PAGINA` en el cuadre del balance (l. 297) y `aplicar_condiciones_generales`, que añade la condición de estructura (l. 376). `test_n4_comprobaciones.py`: **19/19**, salida idéntica a la conservada.<br>**[Hecho] Engaños** (`…/tmp/engano_n4_vigencia2.py`): se rechazan los 16 de la auditoría interna y los 11 del primer control (B1–B11), y los 4 controles favorables se aceptan.<br>**Reserva:** de 12 engaños nuevos se rechaza 1 y **pasan 11**. Algunos contradicen afirmaciones expresas de `INFORME_N4_4_9.md` §2 (**W-5**). En los textos reales no aparece ninguno |
| **V-5** | **Vigente** | **[Hecho]**<br>• `INFORME_N4_4_9.md` l. 58: «De 2017 a 2022 solo se conserva la traducción inglesa … 2023 se contrasta con la columna comparativa del informe español de 2024», igual que §6 l. 138 y el registro §9.<br>• `N4-minoritarios-2023` ya no dice «igual»: declara la reexpresión (1.284.595 y 2.508.927 frente a 1.257.579 y 2.481.911; el patrimonio atribuido coincide), con `texto_es_minoritarios` (l. 385–396).<br>• `N4-otros_activos_financieros-2023` tiene contraste con la comparativa española de 2024 (p. 9; 816.395 frente a 821.341), clase 2 |
| **V-6** | **Vigente con reservas** | **[Hecho] Corregido:**<br>• `test_n4_comprobaciones.py` dice `python3 -I -B`;<br>• la tabla antes/después y su script nombran los cinco archivos de `codigo_4_8_1`;<br>• la carpeta `.lo_perfil/` vacía de `EmpresaX_cero_pendiente` se conserva, como declara el registro.<br>**Reservas:**<br>• las duraciones siguen sin coincidir: «≈ 10–13 min» en `verificar_paquete.sh` l. 12 y «10–12 minutos» en `CONTINUIDAD.md` l. 46. El registro lo deja para la §8, que está pendiente;<br>• el registro §6, fila Z-9, sigue diciendo «el paquete se construye sin … `.lo_perfil/`», lo que contradice la §7, fila V-6 (**W-6**) |
| **V-7** | **Vigente con reservas** | **[Hecho] Corregido:**<br>• la fila Z-8 del registro §6 está redactada con el orden real;<br>• `INFORME_RV1_4_9.md` §5 y `CONTINUIDAD.md` §8 (l. 180) dicen que «bastan dos archivos».<br>**Reserva:** el límite sigue formulado con tres archivos en `CONTINUIDAD.md` §5 (l. 117: «reescriba a la vez `auditoria.md`, `estado_pipeline.json` y `cierre_vigente.json`») y en el registro §9 (l. 111). El primer control pedía corregirlo también en el §5 (**W-6**) |

---

## 2. Hallazgos nuevos

| Id | Gravedad | Título |
|---|---|---|
| W-1 | Menor | Estructura interna de `ficha.json` y de las solicitudes sin validar: traza y aprobación publicada por las cuatro vías; otros tipos del estado rompen el archivado |
| W-2 | Menor | `ficha.json` ilegible por `ficha.py`: sin estado, el registro pierde la solicitud y la huella fiel (V-3 por otra vía); con estado, la ficha reescrita no es vigente; el aviso de `ficha.py` es falso sin estado |
| W-3 | Menor | `auditoria.md` sin permiso de lectura: `archivar_salidas` mueve las salidas y falla antes de retirar las filas |
| W-4 | Menor (anterior a la 4.9) | `material_auditado` con «../» saca las salidas archivadas fuera del expediente |
| W-5 | Menor | N4: 11 de 12 engaños nuevos pasan; varias frases del §2 del informe tienen más alcance que el código; el contraste español de intereses y minoritarios no aplica las excepciones de estructura |
| W-6 | Menor | Restos documentales: límite con tres archivos, fila Z-9 del registro, alcance de «archivo de control ilegible» y descripción del caso de la ficha ilegible |

### W-1 · MENOR · Estructura interna de `ficha.json` y de las solicitudes sin validar

**[Hecho]** (`…/tmp/ataques_v2.py nuevos`; salida en `ejecuciones/ataques_nuevos_salida.txt`)

**a) Con la aprobación publicada.** Por el paso 14, `ficha.py`, `informe.py` y `resumen.py`: traza y código 1. El estado sigue en `concluido/APROBADO`, la ficha sigue cerrada y los dos destinos siguen en «APROBADO».
- `ficha.json` con `"cierre": "APROBADO"` o `"cierre": [1]`: `AttributeError` en `cierre_v2.motivo_vigencia`, l. 560 (`(F.get("cierre") or {}).get(...)`).
  - `_motivo_estructura` valida el estado, `cierre_vigente.json` (solo que sea un objeto) y el material, pero no la ficha.
  - `ficha_cerrada()` da por cerrada una ficha con cualquier «cierre» verdadero.
- Una solicitud pendiente sin «id» en `solicitudes_auditoria` (`{"estado": "pendiente"}`): `KeyError: 'id'` en `motivo_rechazo_cierre`, l. 375 (`pend[-1]['id']`).
  - `_motivo_estructura` solo comprueba que cada solicitud sea un objeto.
  - El mismo acceso está en `pipeline.py`, paso 14.

**b) Con traza después de retirar.** Las salidas ya están archivadas y los destinos retirados, pero termina con código 1.
- `solicitudes_auditoria` como objeto `{"x": 1}` **por el paso 14**: `AttributeError` en `pipeline.py`, l. 890. El paso 14 recorre las solicitudes sin la validación de `_motivo_estructura`. La batería solo prueba este caso por `informe.py`.
- Con un motivo de retirada legítimo (un `auditoria.md` que no es UTF-8) y `historial` como objeto, `cierres_archivados` como texto o `paso` como texto en el estado, `archivar_salidas` falla en l. 641, 645 o 646 por las cuatro vías.
  - Ocurre después de mover las salidas y de retirar las filas.
  - El `estado_pipeline.json` del disco queda en `concluido/APROBADO`, sin ficha.

**[Hecho]** Los dos accesos de a) ya estaban en la 4.8.1 (`codigo_4_8_1/cierre_v2.py`, l. 248 y 394).

**[Interpretación]**
- Es el patrón de V-2 («estructura interna mal formada»): hace falta un archivo manipulado, y el fallo es ruidoso.
- Contradice, para la ficha y para las solicitudes, la frase de `INFORME_RV1_4_9.md` §3: «Un JSON válido que no es un objeto, o una estructura interna errónea, es un archivo ilegible».
- No da un falso código 0.

**[Propuesta]**
- Que `_motivo_estructura` valide también que `ficha.json → cierre` sea un objeto (o nulo) y que cada solicitud tenga un «id» de texto.
- Que el paso 14 use la misma validación.
- Que `archivar_salidas` tolere tipos erróneos de `historial`, `cierres_archivados` y `paso`, o los trate como estado ilegible.

### W-2 · MENOR · `ficha.json` ilegible por `ficha.py`

**[Hecho]** (`ataques_v2.py ficha_ilegible`; salida en `ejecuciones/ataques_v3_fi_tr_h46_salida.txt`)

**a) Cierre de la 4.9 sin `estado_pipeline.json`, con `ficha.json` = «{trunc».**
1. `ficha.py --estado concluido` termina con **0**. Archiva la ficha ilegible (y, con ella, `cierre_vigente.json`), escribe una ficha nueva con «cierre» y llama a `registrar_cierre`.
2. Como `cierre_vigente.json` ya está archivado, `previo` está vacío, y no hay estado: el registro nuevo **no tiene `solicitud` ni `auditoria_fiel`**, y `auditoria_sha256` es la huella de bytes del archivo actual.
3. `ficha.py` imprime «AVISO: … la ficha nueva NO es vigente … (informe.py y resumen.py la rechazarán)». Pero `informe.py` la acepta a continuación (código 0).
4. Con la respuesta guardada antes en CRLF, una transformación inocua, el registro guarda la huella del archivo CRLF (a8ad2985… en lugar de f29285bf…). Al restaurar los bytes aceptados, `informe.py` **retira** («no es la auditoría registrada en `cierre_vigente.json` al cerrar (cierre anterior a la 4.8.1)»).
5. Es exactamente la consecuencia de V-3, por otra vía.

**b) Con estado.** `ficha.py` termina con 0 y escribe una ficha con «cierre», pero `archivar_salidas` ha puesto `auditoria = None` en el estado. La llamada siguiente a `informe.py` retira («el pipeline no registró una auditoría APROBADO válida (auditoria = None)»). La ficha reescrita no es, por tanto, vigente.

**c) La prueba.** La de la batería (grupo I, l. 638–647) solo comprueba el código 0, el archivo, la ficha con «cierre» y que exista `cierre_vigente.json`. No comprueba si la ficha reescrita es vigente.

**[Interpretación]**
- No hay una aprobación sin respaldo: la respuesta había pasado la comprobación fiel antes de archivar.
- Pero el cierre de la 4.9 se convierte en silencio en uno «anterior a la 4.8.1». Contradice `INFORME_RV1_4_9.md` §3 («No registra la huella de bytes del archivo actual») y el «Corregido» de V-3.
- La descripción «con la aprobación válida, `ficha.py` vuelve a escribir la ficha oficial» (registro §7, V-1; `INFORME_RV1_4_9.md` §3) sugiere que el cierre se recupera. Con estado no se recupera, y sin estado se recupera con un registro más débil.

**[Propuesta]**
- Que `registrar_cierre` tome `previo` del `cierre_vigente.json` recién archivado, o que `ficha.py` lo lea antes de archivar.
- O que, con una ficha ilegible, `ficha.py` no vuelva a cerrar y pida una auditoría nueva.
- En cualquier caso, que la prueba del grupo I compruebe la vigencia posterior (con y sin estado) y que el texto del aviso y de los documentos describa lo que pasa.

### W-3 · MENOR · `auditoria.md` sin permiso de lectura: archivado a medias y aprobación publicada en la primera llamada

**[Hecho]** (`ataques_v2.py permisos`, ejecutado como el usuario 65534 con `setpriv`, con `chmod 000 auditoria.md`; salida en `ejecuciones/ataques_permisos_salida.txt` y `permisos_auditoria_segunda_llamada.txt`)

1. **El motivo sí se da.** `motivo_rechazo_cierre` captura el `PermissionError` (l. 343–347) y devuelve «auditoria.md no se puede leer».
2. **El archivado falla a medias.** `archivar_salidas` mueve la ficha, el informe y `cierre_vigente.json` a `historial_cierres/03_…/` y, como `os.path.isfile(auditoria.md)` es verdadero, llama a `shutil.copy2` (l. 622–623). Ahí lanza `PermissionError`:
   - antes de escribir `RETIRADA.json`;
   - antes de `retirar_publicaciones`;
   - antes de tocar el estado.
3. **El resultado, por las cuatro vías:** traza y código 1, con los dos destinos en «APROBADO» y el estado en `concluido/APROBADO`.
4. **La llamada siguiente** (`informe.py`) encuentra que no hay ficha y retira las dos filas. El estado sigue en `concluido/APROBADO` y la carpeta archivada sigue sin `RETIRADA.json`.

**[Interpretación]**
- En la 4.8.1 el mismo caso fallaba antes, al leer, sin mover nada. La corrección de V-2 adelanta el motivo, pero el archivado queda a medias.
- La batería se ejecuta como root, que lee el archivo igualmente: no puede ver este caso.
- Es poco probable: hace falta otro usuario o un cambio de permisos.

**[Propuesta]** Que `archivar_salidas` capture `OSError` en la copia de `auditoria.md` y lo anote en `RETIRADA.json`.

### W-4 · MENOR (anterior a la 4.9) · `material_auditado` con «../» saca las salidas archivadas fuera del expediente

**[Hecho]** (`ataques_v2.py traversal`)
- **El ataque.** Con `ficha.json → cierre.material_auditado = "../../../../FUERA_DEL_EXPEDIENTE"`, las cuatro vías retiran la aprobación (códigos 0 con el aviso, 3, 3 y 4).
- **Dónde acaba el archivo.** `archivar_salidas` construye el destino como `historial_cierres/{n:02d}_{mat}` (l. 618). Mueve la ficha, el informe, `cierre_vigente.json`, la copia de la auditoría y `RETIRADA.json` a `exp/FUERA_DEL_EXPEDIENTE/`, **fuera de la carpeta del expediente**. Deja además una carpeta `historial_cierres/03_..`.
- **La misma línea en versiones anteriores:** `codigo_4_8_1/cierre_v2.py` l. 450 y la copia de la 4.8, l. 284.

**[Interpretación]**
- La retirada se hace.
- Pero el antecedente queda fuera de `historial_cierres/`, donde `_fichas_cerradas_archivadas` ya no lo ve. Esa función sirve para detectar filas aprobadas sin registrar en el resumen predeterminado.
- Hace falta una ficha manipulada.

**[Propuesta]** Sanear `mat` antes de usarlo en una ruta (por ejemplo, solo `[0-9a-f]{16}` o `sin_material`).

### W-5 · MENOR · N4: once engaños nuevos pasan; el informe describe la clasificación con más alcance

**[Hecho]** `…/tmp/engano_n4_vigencia2.py`, salida en `ejecuciones/engano_n4_vigencia2_salida.txt` y `.json`. Es el script del primer control, adaptado a las rutas, con la serie «nuevos2». Pasan con clase 2 y debían rechazarse:
- **«Of which» y sus variantes, después del total:**
  - **C1** «Thereof: interest paid …»;
  - **C2** «Of which» con un espacio no separable (U+00A0);
  - **C3** «Оf which» con un homoglifo cirílico;
  - **C4** «Including interest paid of …».
  - `DESGLOSE` (l. 239) solo reconoce «of which / de los cuales / de las cuales» con espacio normal.
- **C5:** un segundo bloque de financiación con otra cabecera («Discontinued operations – cash flows from financing activities»). `excepciones_estructura` solo cuenta las líneas que empiezan como `INI_FIN`.
- **C6 y C7:** una cabecera con «thousands of euros» y el estado «(in € millions)» o «(EUR million)». `OTRA_UNIDAD` (l. 238) solo reconoce «millions of euros / millones de euros».
- **C8:** una adquisición del año con el rótulo de la lista blanca **partido en dos líneas**: «Acquisition of a subsidiary, net of» / «the cash acquired (40) -».
  - `rotulos_no_reconocidos` une el rótulo y lo acepta.
  - `linea_adquisiciones_dos_importes` y `lineas_un_importe` buscan «acquisition of a subsidiar» en cada línea por separado, y la línea con los importes no lo contiene.
  - El cuadre suma los −40 y cuadra.
- **Minoritarios incluidos en «Total liabilities» y desglosados aparte, con otro rótulo:**
  - **C10** «Nоn-controlling» con un homoglifo;
  - **C11** «Equity attributable to other shareholders»;
  - **C12** «Intereses de terceros».
  - `NCI_PAGINA` (l. 240) no los reconoce.
- **Se rechaza:** C9, el homoglifo en el rótulo de la adquisición, porque el rótulo no está en la lista blanca.
- **Controles favorables aceptados:** 4 de 4.

**[Hecho] Afirmaciones del informe que el código no cumple.** `INFORME_N4_4_9.md` §2 dice:
- «una cabecera en millones la contradice»: falla en C6 y C7;
- «En el balance, cualquier mención de intereses minoritarios en la página («outside shareholders» incluido) impide el cuadre»: falla en C11 y C12.

**[Hecho] Lo que el límite declarado ya cubre.** El límite de §2 («los homoglifos fuera de los casos probados y estructuras de página distintas de las anteriores») cubre C3, C10 y, en buena medida, C5. No cubre C8, que es una variante de la maquetación con rótulos desplazados que el propio informe declara para el texto inglés.

**[Hecho] El contraste español.** Para intereses (l. 523) y minoritarios (l. 489), el contraste español no aplica `excepciones_estructura` ni la unidad. Para otros activos financieros sí las aplica (l. 613). El informe dice que la versión española «prevalece».

**[Hecho] En los datos reales no cambia nada.**
- En las páginas de los diez `CF_<año>.txt` usadas por la matriz no aparece ninguno de esos patrones: «thereof», «including», «€ m», «million», «other shareholders», «terceros», NBSP, cirílico, «discontinued» (`ejecuciones/n4_paginas_reales_engaños.txt`).
- En las páginas españolas de 2024 y 2025, `excepciones_estructura` da `[]` y la unidad de cabecera es verdadera.
- Las cinco adquisiciones reales no tienen ningún rótulo de adquisición partido.

**[Interpretación]**
- No permite confirmar ningún cero: la IA no confirma y las propuestas están sin firmar.
- Afecta a la base de la verificación automática futura (`PROPUESTA_AUTOMATIZACION_4_9.md`) y a la exactitud del §2.

**[Propuesta]**
- Que las expresiones de desglose, unidad y minoritarios se apliquen sobre el texto normalizado (NFKC y espacios), con más variantes, o que el §2 se limite a lo que reconocen.
- Que la detección de la adquisición use el rótulo unido, como `rotulos_no_reconocidos`.
- Que el contraste español aplique las mismas condiciones que el inglés.
- Añadir C1–C8 y C10–C12 a `test_n4_comprobaciones.py`.

### W-6 · MENOR · Restos documentales

**[Hecho]**
1. **El límite de la reescritura coordinada (V-7).** Sigue con tres archivos en `CONTINUIDAD.md` §5, l. 117, y en `REGISTRO_ENTREGA_4.9.md` §9, l. 111.
2. **El registro §6, fila Z-9.** Dice «el paquete se construye sin `__pycache__` ni `.lo_perfil/`». La §7, fila V-6, declara que se conserva `pruebas/sintetico/EmpresaX_cero_pendiente/.lo_perfil/` (vacía), y está en el árbol.
3. **«Un archivo de control ilegible retira la aprobación sin traza (Z-2, V-1 y V-2)».** Lo dicen `VERSION`, `CONTINUIDAD.md` §5 (l. 117) y `DECISIONES.md` (l. 253). Siguen sin cumplirse los casos de W-1 a) (estructura interna de la ficha y de las solicitudes) y W-3 (permisos). `INFORME_RV1_4_9.md` §5 limita bien los archivos tratados, pero no esos casos.
4. **El caso de la ficha ilegible.** El registro §7 (V-1), `INFORME_RV1_4_9.md` §3 y la cabecera de la batería (l. 51–52) lo describen como si `ficha.py` restableciera el cierre (W-2).
5. **Las duraciones de V-6.** Siguen distintas (§1). El registro las deja para la §8.
6. **La fila Z-4 del registro §6.** Mantiene «16/16» en «Dónde se comprueba», cuando la batería vigente es de 19. **[Interpretación]** Es la cifra del momento de esa corrección, pero no se marca como histórica, a diferencia de las de la auditoría, que el encabezado de la tabla sí marca.

**[Propuesta]** Igualar el límite en los tres sitios, corregir la fila Z-9 y restringir o completar la frase general cuando se traten W-1 a W-3.

---

## 3. Lo que se comprobó y está bien

**Integridad del paquete**
- **[Hecho] El manifiesto** (`…/tmp/comparar_manifiestos2.py`, salida en `ejecuciones/comparar_manifiestos2_salida.txt`):
  - `MANIFIESTO_SHA256.txt` declara 1.679 archivos y cubre exactamente los del árbol inicial, sin ninguna huella distinta;
  - los únicos archivos de más al final son los 35 de `personaje_v2/.lo_perfil/` de la §0.3.
- **[Hecho] Frente a `E/reproduccion/MANIFIESTO_4_8_1.txt`** (1.539 archivos):
  - hay 12 modificados, 0 ausentes y 141 nuevos en el árbol inicial (176 al final, contando los 35 de `.lo_perfil/`);
  - los 12 modificados son exactamente `CAMBIADOS_FRENTE_A_4_8_1` de `comprobar_entrega_4_9.py` y la lista del registro §3, que añade `MANIFIESTO_SHA256.txt`;
  - el único archivo nuevo fuera de `E/` (sin contar el manifiesto ni `.lo_perfil/`) es `personaje_v2/pruebas/test_integridad_auditoria_v2.py`;
  - ningún expediente histórico, contraste ni original ha cambiado.
- **[Hecho] Las copias de `codigo_4_8_1`.** Los cinco archivos tienen las huellas del manifiesto 4.8.1.
- **[Hecho] H2.** El SHA-256 de `inspect.getsource(Pipeline.veredicto_auditoria)` es `9edf6252ca48c80009b5b51b52aeaa447960ab611150b908738194e526775422` en el código actual y en `codigo_4_8_1/pipeline.py` (`ejecuciones/h2.txt`).
- **[Hecho]** No hay `__pycache__` ni `.pyc` en el paquete.

**R-V1 y V-1 a V-3**
- **[Hecho] La batería.**
  - `test_integridad_auditoria_v2.py` da **96/96** (12 s) con el código actual y **24/93** con `--codigo E/reproduccion/codigo_4_8_1`.
  - En los dos casos, el grupo, el nombre y el resultado coinciden prueba a prueba con `E/resultados/test_integridad_auditoria_v2.json` y con `E/reproduccion/test_integridad_con_codigo_4_8_1.json` (`…/tmp/comparar_baterias.py`).
  - Los detalles solo difieren en identificadores aleatorios y rutas temporales.
  - Los grupos suman 2 + 28 + 10 + 3 + 3 + 13 + 16 + 16 + 5 = 96. El grupo I tiene 8 casos de V-1, 7 de V-2 y 1 de V-3, como dice el registro.
- **[Hecho] Las mutaciones.** `mutar_rv1.py --salida <tmp>` da **28 de 28** detectadas, con un JSON **idéntico byte a byte** a `E/resultados/mutaciones_rv1.json` y una salida idéntica a `mutar_rv1_salida.txt`.
- **[Hecho] Las demás baterías permitidas.**
  - `test_auditorias_v2.py`: **55/55**.
  - `comprobar_integracion_verificador_49.py`: **13 de 13**. Se leyó antes: solo ejecuta el bloque extraído contra sustitutos en un temporal.
- **[Hecho] El diff de los cinco scripts frente a `codigo_4_8_1/`** (264, 35, 28, 23 y 25 líneas). Solo contiene lo que describen `INFORME_RV1_4_9.md` §1–§3 y §5:
  - `leer_json_control` exige un objeto;
  - `_motivo_estructura`;
  - `OSError` en la lectura de `auditoria.md`;
  - `motivo_vigencia` con la ficha ilegible;
  - `archivar_salidas` con la ficha ilegible y `isfile`;
  - `_j_tolerante` en `sincronizar_resumenes` y `_fichas_cerradas_archivadas`;
  - `registrar_cierre` con `previo`;
  - en `pipeline.main`, `OSError` y el tipo del estado;
  - `leer_control` local en `ficha.py`, `informe.py` y `resumen.py`.
- **[Hecho] Independencia del código antiguo (punto 2).**
  - Todas las funciones de `cierre_v2` que usan `ficha.py`, `informe.py` y `resumen.py` existen en `codigo_4_8_1/cierre_v2.py` y en la copia de la 4.8 (`…_4_8_1/reproduccion/codigo_4_8/cierre_v2.py.txt`).
  - Cada script usa su propio `leer_control`.
  - Prueba directa (`…/tmp/mezcla_codigo.py`, salida en `ejecuciones/mezcla_codigo_salida.txt`): con `cierre_v2.py` y `pipeline.py` de la 4.8.1, o de la 4.8, y los tres scripts actuales sobre una copia del cierre de la 4.6.1, `informe.py`, `resumen.py` y `ficha.py` dan 0, sin traza, y la fila queda en «APROBADO».
- **[Hecho] Otras rutas de lectura del cierre.**
  - `material_fijado` sigue leyendo sin tolerancia en l. 370, en `motivo_respuesta_no_aceptada` y en `motivo_auditoria_no_corresponde`, pero siempre después de que `leer_json_control` haya leído y validado el mismo archivo.
  - `registrar_cierre` y `registrar_informe` usan `_j`, pero solo se alcanzan después de una comprobación que ya leyó esos archivos. Un enlace roto en `cierre_vigente.json` da una traza al escribir, del lado seguro (`ataques_simbolicos_salida.txt`).
  - `material()` no tolera un archivo del material sin permiso de lectura (`resultados.json`: traza y aprobación publicada). Está dentro del límite declarado en `INFORME_RV1_4_9.md` §5 («Otros archivos del expediente … no se han tratado»).
- **[Hecho] Ataques nuevos que se retiran sin traza por las cuatro vías:**
  - los cuatro archivos de control vacíos y `auditoria.md` vacía;
  - `material_auditoria.json` con «archivos» como lista o texto, «id» numérico o sin «id»;
  - `auditoria_respuesta.fiel` numérico;
  - enlaces rotos de `cierre_vigente.json`, material o `auditoria.md`;
  - enlaces a carpetas o a `/dev/null`;
  - archivos de control sin permiso de lectura (salvo `auditoria.md`, W-3).
- **[Hecho] Casos que siguen vigentes, como corresponde:**
  - con el estado presente, los cambios de tipo en `cierre_vigente.json → auditoria_fiel`, `solicitud` o `auditoria_sha256` no intervienen;
  - `auditoria_respuesta = {}` se trata como ausente y el cierre se acredita con `cierre_vigente.json`;
  - una `auditoria.md` servida por un enlace a un archivo de bytes idénticos.

**Z-1 sobre el expediente histórico de la 4.6 (punto 5)**
- **[Hecho]** `cierre_v2.motivo_rechazo_cierre` y `motivo_vigencia`, sobre una copia de `…_4_6/Vidrala`, devuelven «no consta la respuesta de auditoría aprobada (ni estado_pipeline.json → auditoria_respuesta ni cierre_vigente.json la registran) …» (`ataques_v2.py h46`).
  - El expediente no tiene `cierre_vigente.json`.
  - Su estado tiene `auditoria = APROBADO` y no tiene `auditoria_respuesta` ni solicitudes.
- **[Hecho]** El SHA-256 de `…_4_6/Vidrala/auditoria.md` es `57f48faa…0a60f`, igual en `MANIFIESTO_4_8_1.txt` y en el manifiesto actual.
- **[Hecho]** El caso que deja de cumplirse en el control de la 4.6 es «cierre_v2.motivo_rechazo_cierre: ningún motivo de rechazo» (`…_4_6/scripts/comprobar_cierre_ensayo.py`, l. 75).
- **[Hecho]** D-RV1c (`E/propuestas/decisiones_y_preguntas_4_9.json`) lo recoge así, con los campos humanos vacíos. También `CONTINUIDAD.md` l. 14 y l. 210, `DECISIONES.md` l. 255, `INFORME_RV1_4_9.md` §3 y §5, el registro §7 y `comprobar_entrega_4_9.py` l. 125–128.
- **[Interpretación]** La consecuencia es coherente con la 4.6.1:
  - `INFORME_REPARACION_4_6_1.md` l. 159 declara para los expedientes cerrados antes de la 4.6.1 que, «si se vuelve a ejecutar sobre ellos el pipeline, `informe.py` o `resumen.py`, sus salidas se archivan hasta una auditoría nueva. Es la consecuencia buscada»;
  - la 4.9 lo extiende a `ficha.py` y a la comprobación del cierre;
  - es coherente con no atribuir huellas retroactivas (encargo §3.3): no se crea ningún `cierre_vigente.json` ni se registra la huella del archivo actual;
  - la cita de `INFORME_RV1_4_9.md` §5 es fiel.

**N4 (V-4, V-5)**
- **[Hecho] La reproducción** (`n4_investigacion.py --salida …/tmp/n4rep --propuestas …/tmp/n4rep/prop`, con `efectos/efectos_n4.json` copiado a la salida):
  - `matriz_n4.csv`, `recuento_n4.json` y `propuestas_n4_sin_firmar.json` son **idénticos byte a byte**;
  - `matriz_n4.json` solo difiere en `efectos`, que es la ruta;
  - la salida de consola es idéntica a `E/resultados/n4_investigacion_salida.txt`.
- **[Hecho] La cobertura:** 38 investigadas, 35 respaldadas (8 con reserva), 3 no aplicables, 0 sin evidencia y 0 discrepantes. El recuento es 38 frente a 39 del CSV, con la diferencia explicada.

**Coherencia documental de las cifras (punto 6)**
- **[Hecho] Coherentes en todos los documentos leídos:** 96, 28, 24/93, 19, 39 de 39, 38/35/8/3/0/0, −0,0284 y 23 de 24. Los documentos son `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `DECISIONES.md`, `E/INFORME_RV1_4_9.md`, `E/INFORME_N4_4_9.md`, `E/PROPUESTA_AUTOMATIZACION_4_9.md`, el registro, `E/propuestas/*.json` y `comprobar_entrega_4_9.py`. Fuera de las citas históricas marcadas no queda ninguna cifra antigua (80, 23 mutaciones, 24/77, 16, 36), salvo la fila Z-4 (W-6.6) y el LEEME (abajo).
- **[Hecho] El recuento de `comprobar_entrega_4_9.py`, leído en el código:**
  - por secciones: 5 + 12 + 11 + 11 = **39 comprobaciones**, contando las dos del bucle de la l. 133 y las siete de la l. 218;
  - por tipo: **8 reejecutan, 17 recalculan y 14 constatan**.
  - Coincide con «39 de 39» de su cabecera, de `CONTINUIDAD.md` l. 65 y del LEEME.
- **[Hecho] Pendientes declarados, que no son defectos de código:**
  - el registro §7 bis y §8, este informe (que `comprobar_entrega_4_9.py` constata en l. 218) y `E/resultados/comprobar_entrega_4_9_salida.txt`;
  - el LEEME de controles históricos conserva los resultados del candidato anterior:
    - «integridad **80/80**»;
    - «4.6 … 24 de 24», que con D-RV1c pasa a 23 de 24;
    - «vuelve a ejecutar las 23 mutaciones … en unos 12–15 minutos», que la cabecera del script da como «7–9 minutos»;
    - «la cubren ahora … la batería de integridad (80)»;
    - las líneas de la 4.7.1, la 4.8, la 4.8.1 y las comparaciones de baterías.
  - Se señalan para la actualización que el registro anuncia.
- **[Hecho] El registro §6–§7 (punto 8).** El tratamiento declarado de cada hallazgo corresponde al código y a las pruebas: grupos, número de casos, mutaciones M24–M28, `_motivo_estructura`, `OSError` en `pipeline.main` y en la lectura de `auditoria.md`, el contraste de 2023 (816.395 frente a 821.341), `-B` y la tabla. Las salvedades son las de W-2, W-6 y las reservas de la §1. Nada de lo que afirma como hecho falta en el árbol, salvo los pendientes que declara.

**Observaciones sin calificar de hallazgo**
- **[Hecho]** Sin `estado_pipeline.json`, `resumen.py` publica la fila del cierre que da por vigente con `verificacion` vacía, no «APROBADO»: toma el valor del estado (`ejecuciones/ataques_v3_fi_tr_h46_salida.txt`). **[Interpretación]** Es un comportamiento anterior y del lado seguro.
- **[Hecho]** Sin estado, `pipeline.py` sin `--desde` vuelve a empezar en el paso 0 (§0.3). **[Interpretación]** Es un comportamiento anterior a la 4.9. Es lo que causó la incidencia, y conviene tenerlo en cuenta en los procedimientos.

---

## 4. Lo que no se pudo comprobar

- **Por restricción del encargo** (LibreOffice o scripts prohibidos), salvo la incidencia de la §0.3, que no sirve como resultado:
  - `verificar_paquete.sh`, `test_comprobadores.py`, `test_pipeline_sintetico.py`, `test_estados_v2.py`, `test_cierre_v2.py`, `test_resumen_v2.py` y `efectos_n4.py`;
  - `comprobar_entrega_4_9.py`: el «39 de 39» solo se contó en el código, no se ejecutó;
  - los `comprobar_entrega_*` y `comparar_baterias_*` históricos;
  - el control de la 4.6 (`comprobar_cierre_ensayo.py`): no está en la lista permitida, así que el «23 de 24» no se ejecutó. Solo se comprobó el caso que deja de cumplirse.
- **Pendiente en el expediente:** el ZIP final y su huella, el registro §7 bis y §8, y los resultados finales del LEEME.
- **No revisado en este control:**
  - la coherencia interna de `CAMBIOS_ARCHIVOS.txt`;
  - los PDF, abiertos a mano. Las cifras españolas se revisaron a través de la matriz y del código que la genera.

**Scripts del auditor** (en `/home/claude/vigencia2_4_9/tmp/`):
- `ataques_v2.py`, con los grupos `rep`, `nuevos`, `traversal`, `v3`, `ficha_ilegible`, `simbolicos`, `permisos` y `h46`. Las salidas están en `ejecuciones/ataques_*_salida.txt` y `.json`.
  - Los casos «MAL» de `cierre_vigente.json` con el estado presente (`cv_fiel_numero`, `cv_solicitud_lista`, `cv_sha_numero`) son un criterio erróneo del propio script: el comportamiento correcto es seguir vigente (§3).
  - También son correctos por diseño los de la ficha ilegible, vacía o modificada por `ficha.py` (archivo y nueva ficha con aviso) y los del pipeline sin `--desde` (retira y espera, código 10).
- `comparar_baterias.py`, `comparar_manifiestos2.py`, `engano_n4_vigencia2.py` y `mezcla_codigo.py`.
- Las huellas están en `sha_inicio.txt`, `sha_final.txt`, `arbol_inicio.sha256`, `arbol_final.sha256` y `huella_final.txt`.
