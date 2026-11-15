# Control de vigencia de las correcciones de la entrega 4.9 (Z-1 a Z-10)

> **Nota de conservación (añadida al copiar el informe en el expediente; el texto del auditor no se ha modificado).**
> - El control se hizo sobre la copia `/home/claude/vigencia_4_9/munger_v2_r1`, descompresión del paquete candidato, que no forma parte del paquete. El SHA-256 del informe tal como lo entregó el auditor está en `auditoria_interna/AUDITORIA_INTERNA_4_9_vigencia.md.sha256`.
> - Los scripts y salidas que cita como `/home/claude/vigencia_4_9/tmp/<archivo>` se conservan en `auditoria_interna/material_vigencia/<archivo>` (y `…/ejecuciones/`). No se conservan las carpetas de escenarios, los temporales ni las matrices N4 reproducidas, que son regenerables.
> - Las cifras de este informe (80 pruebas, 23 mutaciones, 24/77, 16 pruebas de N4, 36 comprobaciones) son las del material fijado `MATERIAL_VIGENCIA_4_9.txt`. Los hallazgos V-1 a V-7 se corrigieron después; el tratamiento y las cifras finales están en `REGISTRO_ENTREGA_4.9.md` §7, y la revisión de esas correcciones en `AUDITORIA_INTERNA_4_9_vigencia_2.md`.


Auditor interno independiente, en un contexto separado y sin haber participado en el trabajo ni en la auditoría anterior. Fecha: 11-nov-2026, de 11:42 a 12:03 (CET).

- **Copia auditada:** `/home/claude/vigencia_4_9/munger_v2_r1`. Las rutas de este informe son relativas a `munger_v2_r1/` salvo que empiecen por `/`.
- **Expediente:** `E = personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9`.
- **Scripts, salidas y escenarios del auditor:** `/home/claude/vigencia_4_9/tmp/` (las salidas de las ejecuciones están en `/home/claude/vigencia_4_9/tmp/ejecuciones/`, los escenarios en `/home/claude/vigencia_4_9/tmp/escenarios/`). `TMPDIR` se desvió a `/home/claude/vigencia_4_9/tmp/tmpdir`.

**Convenciones.**
- **[Hecho]**: comprobado por el auditor con un comando o una lectura que se cita.
- **[Interpretación]**: juicio del auditor sobre un hecho.
- **[Propuesta]**: lo que el auditor sugiere, sin aplicarlo.

El auditor no ha corregido nada en la copia. No ha ejecutado nada que use LibreOffice. Los resultados que no ejecutó se dicen expresamente en la §4.

---

## 0. Material fijado y huellas

**Al inicio** (11:42; `/home/claude/vigencia_4_9/tmp/huella_inicio.txt`):
- **[Hecho]** `E/MATERIAL_VIGENCIA_4_9.txt` tiene el SHA-256 `479cf703d00b57f4a315729635dfff7ecc9dfb7ce41e25e711da735f561be9e3`, el esperado.
- **[Hecho]** `sha256sum -c` del material, sin la línea de cabecera y ejecutado desde `munger_v2_r1/`: **101 de 101 OK** y ninguna línea distinta.
- **[Hecho]** Se guardó la huella de todos los archivos del árbol: 1.632 archivos (`/home/claude/vigencia_4_9/tmp/arbol_inicio.sha256`).

**Al final** (12:02, `/home/claude/vigencia_4_9/tmp/huella_final.txt`; se repitió la comparación del árbol completo después de la última ejecución, `test_auditorias_v2.py`, con el mismo resultado):
- **[Hecho]** La huella del material es la misma y vuelven a cumplirse las 101 de 101.
- **[Hecho]** `diff` entre las dos huellas del árbol completo: **sin diferencias**. Ningún archivo ni carpeta es posterior al material (`find . -newer E/MATERIAL_VIGENCIA_4_9.txt`, sin resultado). No hay ningún `__pycache__` ni `.pyc`.
- **[Hecho] Ninguna ejecución del auditor cambió ningún archivo de la copia.** Todos los comandos se ejecutaron con `python3 -I -B`. Las salidas fueron siempre a `--salida`/`--json` en el espacio temporal propio del auditor.

**[Hecho] LibreOffice.** Antes de cada ejecución larga se dejó constancia de `pgrep -fa soffice` (`/home/claude/vigencia_4_9/tmp/ejecuciones/pgrep_*.txt`).
- A las 11:50 y a las 11:51:41 había un `soffice.bin` en marcha con el perfil `/home/claude/verif_c1/…/.lo_perfil`. Es de la otra tarea, no de esta copia.
- Ninguna ejecución del auditor lanza LibreOffice. Antes de usar los pasos 13 y 14 se comprobó en `pipeline.py` que solo llaman a `ficha.py`, `informe.py`, `resumen.py`, `validar_esquema.py` y `diagnostico.py`. Ninguno de ellos usa `subprocess` ni `soffice` (`grep -n "subprocess\|soffice"` sin resultado). `recalc_leer_precio` solo se llama en los pasos 9, 10 y 12.

---

## 1. Vigencia de las correcciones

| Id | Veredicto | Evidencia principal |
|---|---|---|
| **Z-1** | **Vigente** | **[Hecho] Código.** `cierre_v2.motivo_rechazo_cierre`, l. 360–378: sin `auditoria_respuesta`, y sin `cierre_vigente.json` con `auditoria_fiel`+`solicitud` o con `auditoria_sha256`, devuelve «no consta la respuesta de auditoría aprobada…». **[Hecho] Reproducción propia** (`ataques_vigencia.py z1`): 4.6.1 sin `cierre_vigente.json` y con otra APROBADO del material, esta vez con una línea de solicitud inventada; las cuatro vías dan los códigos 4/3/3/3, ningún `cierre_vigente.json` creado, ninguna huella atribuida en el árbol, y los dos destinos quedan en «SIN APROBACIÓN VIGENTE». Lo mismo con otras 9 variantes nuevas (Z1b–Z1f). La batería da 6/6 en Z-1 y la mutación M21 se detecta |
| **Z-2** | **Vigente con reservas** | **[Hecho] Archivos nombrados en el hallazgo.** Para `auditoria.md` no UTF-8 (byte inválido, cp1252, UTF-16 sin BOM, sustituto suelto) y para `estado_pipeline.json` o `cierre_vigente.json` ilegibles (truncados, vacíos, con BOM, no UTF-8): retirada **sin traza** por todas las vías probadas. `pipeline.py` termina con **6**, o con **5** con un destino inaccesible. **Reserva:** la afirmación general de `VERSION` y de `CONTINUIDAD.md` §5 («un archivo de control ilegible … retira la aprobación sin traza») no es cierta para `material_auditoria.json` ni para `ficha.json` ilegibles (**V-1**), ni para un JSON válido que no es un objeto o un archivo de control que es una carpeta (**V-2**) |
| **Z-3** | **Vigente** | **[Hecho]** El grupo G tiene la prueba de NFKC «²», U+200B, NBSP, U+2028 y VT. El grupo H tiene «sin estado + CRLF → vigente». 80/80 con el código actual. Con `--codigo E/reproduccion/codigo_4_8_1` da 24/77, prueba a prueba igual que lo conservado, y las cuatro copias tienen las huellas de `MANIFIESTO_4_8_1.txt`. `mutar_rv1.py`: 23 de 23, **JSON idéntico** a `E/resultados/mutaciones_rv1.json` |
| **Z-4** | **Vigente con reservas** | **[Hecho] Código.** `aplicar_condiciones_generales` (cita, unidad, comparativa y rótulos), listas `BLANCA`, `cuadre_actual` (ilegibles solo en la columna «anterior»), y clases 4 condicionadas (l. 505, 518 y 543). **[Hecho] Reproducción.** El script anterior, adaptado a la clasificación actual, rechaza **16 de 16**. La reproducción es idéntica salvo `efectos` y la cobertura es 38/35 (8)/3/0/0. **Reserva:** de 11 engaños estructurales nuevos se rechazan 5 y **pasan 6** (**V-4**). En los textos reales no hay ninguna de esas estructuras |
| **Z-5** | **Vigente** | **[Hecho]** Ningún documento de la 4.9 llama «humanas» ni «precedentes humanos» a las decisiones de 2017–2018. Todos dicen «sin fecha ni firma». La matriz usa `registro_en_fase1_decisiones`. En `propuestas_n4_sin_firmar.json` queda la clave `separacion.registro_humano`, pero designa el archivo `fase1_decisiones.json` y su texto dice «sin fecha ni firma» |
| **Z-6** | **Vigente** | **[Hecho]** `E/n4/efectos/efectos_n4.json` contiene `f` (−2,76 %, −2,69 %, −2,61 % y −1,31 %), el paso del control C50 de «⚠ REVISAR» a «✓ PASA» en el doble cómputo, el FCF base (161,2 / 158,946 / 139,46) y el precio de Sí de cada variante. La aritmética es coherente: delta = variante − base; L26 = −0,028404 = −1/35,206; Δf lineal en C52. Con `precio_de_si.p_estrella` (k = 3) el auditor recalcula los 10 precios de Sí, idénticos; también el ponderado 0,2/0,6/0,2 y las huellas de las 10 copias. **No se recalculó ningún libro** (§4) |
| **Z-7** | **Vigente con reservas** | **[Hecho] En la matriz:** intereses 2023 contrastados con la comparativa del PDF español de 2024 (69.826, «Pagos de intereses (12.320)»); minoritarios 2023 contrastados (1.224.332 + 1.284.595 = 2.508.927); otros activos financieros 2024 y 2025 contrastados en español; explicaciones con las menciones de cada año y la tabla de dependientes de 2025 (20 % y 45 %, puesta en equivalencia); nota 8 en `INFORME_N4_4_9.md` §4 y §6. **Reservas (V-5):** contradicción interna del informe sobre 2023, un «igual en la versión española» que la propia matriz desmiente, y otros activos financieros 2023 sin contraste |
| **Z-8** | **Vigente con reservas** | **[Hecho]** Existen el registro, el LEEME, `AUDITORIA_INTERNA_4_9.md` y las demás remisiones (comprobación automática, `archivos_citados.py`). Solo faltan los pendientes que declara el encargo. **Reserva (V-7 a):** el registro, §6, ya los da por existentes |
| **Z-9** | **Vigente con reservas** | **[Hecho]** Los comandos de `INFORME_N4_4_9.md` llevan `-I -B` y `--salida`. `CONTINUIDAD.md` §2 dice qué pruebas usan LibreOffice. No hay `.pyc` en el material ni en el árbol. **Reservas (V-6 a y c):** queda en el paquete una carpeta `.lo_perfil/` vacía, heredada de la 4.8.1, y una instrucción de uso sin `-B` que escribe `__pycache__` |
| **Z-10** | **Vigente con reservas** | **[Hecho] Corregidos:** la lista del mensaje de arranque, la línea 2 de `verificar_paquete.sh`, el tachado del Anexo D, el título de §9 y la lista de archivos de `INFORME_RV1_4_9.md` §7. **Reserva (V-6 b):** las duraciones siguen sin coincidir: «≈ 10–13 min» en `verificar_paquete.sh` frente a «10–12 minutos» en `CONTINUIDAD.md` §2 |

---

## 2. Hallazgos nuevos

| Id | Gravedad | Título |
|---|---|---|
| V-1 | **Importante** | `material_auditoria.json` o `ficha.json` ilegibles: traza y código 1 en las cuatro vías; la aprobación sigue publicada |
| V-2 | Menor | JSON válido que no es un objeto, o archivo de control que es una carpeta: traza y aprobación publicada |
| V-3 | Menor | `ficha.py` sin estado reescribe `cierre_vigente.json` sin la solicitud ni la huella fiel y con la huella de bytes del archivo actual |
| V-4 | Menor | N4: seis engaños estructurales nuevos pasan la clasificación por exclusión; el informe la describe con más alcance del que tiene |
| V-5 | Menor | Restos de Z-7 en `INFORME_N4_4_9.md` y en la matriz (2023) |
| V-6 | Menor | Restos de Z-9 y Z-10: `.lo_perfil/` vacío, duraciones, uso sin `-B` y texto de la tabla antes/después |
| V-7 | Menor | Registro y límites declarados: afirmaciones adelantadas en §6 y límite de la reescritura coordinada formulado con más archivos de los necesarios |

### V-1 · IMPORTANTE · `material_auditoria.json` o `ficha.json` ilegibles: traza y código 1 en las cuatro vías; la aprobación sigue publicada

**[Hecho] Qué pasa con `material_auditoria.json`.**
- `cierre_v2.material_fijado()` (l. 58–60) usa `json.load` directamente. `motivo_rechazo_cierre` la llama en la l. 344 y `motivo_respuesta_no_aceptada` en la l. 188.
- Con `material_auditoria.json` truncado («{trunc») en un cierre de la 4.9, el resultado es `JSONDecodeError`, con traza y código 1, por el paso 14, `ficha.py`, `informe.py` y `resumen.py`.
- Después de cada llamada, el estado sigue `concluido/APROBADO`, la ficha sigue cerrada, `cierre_vigente.json` sigue presente y los dos destinos siguen en «APROBADO».
- Evidencia: `/home/claude/vigencia_4_9/tmp/ejecuciones/ataques_z2_salida.txt`, casos «Z2 material_auditoria_ilegible».

**[Hecho] Qué pasa con `ficha.json`.**
- `motivo_vigencia` ahora la lee con `_j_tolerante`. Una `ficha.json` ilegible le da `None`, es decir, «no hay salida cerrada», así que **no se archiva nada**.
- Después, `sincronizar_resumenes` (l. 831, `_j`), `resumen.py` (l. 34), `informe.py` (`cargar`) y `ficha.py` (l. 184) usan `json.load` directamente y lanzan la excepción. Con el archivo truncado se obtienen el mismo resultado, la misma traza y la misma aprobación publicada (casos «Z2 ficha_ilegible»).
- `INFORME_RV1_4_9.md` §5 declara este caso como límite («Una `ficha.json` ilegible no se ha tratado»).
- `material_auditoria.json` no está declarado en ninguna parte.

**[Hecho] Lo que dice la documentación.**
- `VERSION`: «un archivo de control ilegible o no UTF-8 retira la aprobación sin traza (Z-2)».
- `CONTINUIDAD.md` §5, fila «Integridad de la auditoría vigente»: «un archivo de control ilegible o un `auditoria.md` que no es UTF-8 retiran la aprobación sin traza (Z-2)».
- Ninguno de los dos documentos recoge el límite de `ficha.json`.

**[Interpretación]**
- Es el mismo patrón que Z-2, que la auditoría anterior calificó de bloqueante («el fallo es ruidoso»): una aprobación que ya no puede acreditarse sigue presentada como vigente y ninguna vía la retira.
- `material_auditoria.json` es un archivo de control en el sentido más estricto: fija el material que se aprobó.
- Se califica de importante, y no de bloqueante, por tres razones: la corrección de Z-2 sí cubre los tres archivos que nombraba el hallazgo; el fallo no da un falso código 0; y el límite de `ficha.json` está declarado en un informe.
- Aun así, la afirmación general de `VERSION` y de `CONTINUIDAD.md` §5 es falsa para estos dos archivos.

**[Propuesta]**
- Que `material_fijado` sea tolerante dentro de `motivo_rechazo_cierre`: un archivo ilegible es un motivo de retirada, como `leer_json_control`.
- Que una `ficha.json` ilegible se trate como «salida oficial que no es la registrada» (`motivo_vigencia` no debería devolver `None` en ese caso). `sincronizar_resumenes`, `resumen.py` e `informe.py` deberían leerla de forma tolerante.
- Añadir los dos casos al grupo H.
- Si se decide no repararlo, restringir el texto de `VERSION` y de `CONTINUIDAD.md` §5 a los tres archivos de Z-2 y declarar el límite de `ficha.json` y de `material_auditoria.json` también en `CONTINUIDAD.md` §8.

### V-2 · MENOR · JSON válido que no es un objeto, o archivo de control que es una carpeta: traza y aprobación publicada

**[Hecho]** (`ataques_z2_salida.txt`)
- **JSON válido que no es un objeto.** `leer_json_control` acepta cualquier JSON válido. Con `estado_pipeline.json` = `[]` o `cierre_vigente.json` = `[1]` se produce `AttributeError: 'list' object has no attribute 'get'`, con traza y código 1. Ocurre por las cinco vías probadas en el estado (paso 14, sin `--desde`, `ficha.py`, `informe.py` y `resumen.py`) y por las cuatro en `cierre_vigente.json`. La aprobación sigue publicada en los dos destinos.
- **Estructura interna mal formada.** Pasa lo mismo con `solicitudes_auditoria` como objeto en lugar de lista, y con `auditoria_respuesta` como texto (`AttributeError: 'str' …`).
- **`estado_pipeline.json` es una carpeta.** `ficha.py` retira bien (código 3, `IsADirectoryError` como motivo). En cambio, `pipeline.py` (paso 14 y sin `--desde`) termina con traza y código 1 sin retirar, porque `main()` solo captura `ValueError` en torno a `Pipeline(...)`.
- **`auditoria.md` es una carpeta.** El `open(p, "rb")` de la l. 325 lanza `IsADirectoryError`, con traza y código 1, y la aprobación sigue publicada.

**[Interpretación]** Hace falta un archivo manipulado o mal escrito, no una corrupción corriente, y el fallo es ruidoso. Es del mismo tipo que V-1, pero menos probable.

**[Propuesta]**
- Que `leer_json_control` exija un objeto (como `_cargar` del registro del resumen, «estructura no válida»).
- Que `motivo_rechazo_cierre` valide los tipos de `solicitudes_auditoria` y `auditoria_respuesta`.
- Que `pipeline.main` capture también `OSError`.
- Que la lectura de `auditoria.md` trate `OSError` como motivo de retirada.

### V-3 · MENOR · `ficha.py` sin estado reescribe `cierre_vigente.json` sin la solicitud ni la huella fiel y con la huella de bytes del archivo actual

**[Hecho]** (`ataques_vigencia.py registrar_cierre`; `ataques_b_salida.txt`, casos «RC»)
1. **El escenario.** Es el que la batería da por vigente (H, Z-3): un cierre de la 4.9, sin `estado_pipeline.json` y con la respuesta en CRLF. `ficha.py --estado concluido` termina con código 0.
2. **La reescritura.** `registrar_cierre` reescribe `cierre_vigente.json`:
   - antes: `auditoria_sha256` af7562ef…, `solicitud` SA-05baa423…, `auditoria_fiel` 1fff52e2…;
   - después: `auditoria_sha256` **d89c966c…**, la huella de bytes del archivo CRLF actual; `solicitud` y `auditoria_fiel` ausentes.
   - La causa: `registrar_cierre` solo copia la solicitud y la huella fiel desde `estado_pipeline.json` (l. 497–501), que no existe.
3. **La consecuencia.** Si después se restaura la respuesta original (LF, los bytes que se aceptaron), `ficha.py` la **retira** («no es la auditoría registrada en `cierre_vigente.json` … anterior a la 4.8.1»).

**[Interpretación]**
- El efecto va del lado seguro: queda una comparación más estricta.
- Pero contradice dos afirmaciones: la del código («nunca se calculan aquí para una respuesta que no las tenía») y la de `INFORME_RV1_4_9.md` §2 («copia la solicitud y la huella fiel … solo si la respuesta las tenía»).
- Atribuye a la aprobación la huella de bytes de un archivo que no es el aceptado byte a byte.
- Y convierte silenciosamente un cierre de la 4.9 en uno «anterior a la 4.8.1».

**[Propuesta]** Que `registrar_cierre`, sin estado, conserve `solicitud` y `auditoria_fiel` del `cierre_vigente.json` anterior cuando la huella fiel del archivo coincide, y no sustituya `auditoria_sha256` por la del archivo actual. Añadir el caso a la batería.

### V-4 · MENOR · N4: seis engaños estructurales nuevos pasan la clasificación por exclusión; el informe la describe con más alcance del que tiene

**[Hecho]** `/home/claude/vigencia_4_9/tmp/engano_n4_vigencia.py` (salida en `ejecuciones/engano_n4_vigencia_salida.txt` y `.json`):
- reproduce las expresiones de clasificación actuales de `main()` y después `aplicar_condiciones_generales`;
- las páginas sintéticas declaran «(thousands of euros)».

**Resultados:**
- **Casos de la auditoría anterior:** 16 de 16 rechazados. El control favorable se acepta.
- **Engaños nuevos:** de 11, se rechazan 5:
  - B6, depósito en una línea solo con importes (por la estructura del bloque);
  - B7, «Intеrest paid» con un homoglifo cirílico;
  - B8, rótulo partido «Dividends paid and / interest on borrowings»;
  - B9, «Dividends paid (incl. finance costs)»;
  - B10, «Outside shareholders' interests».
- **Se aceptan con clase 2 y debían rechazarse, 6:**
  - **B1:** el importe de los intereses en una línea **sin rótulo** dentro del bloque de financiación. `rotulos_no_reconocidos` salta las líneas sin letras (l. 213–214), pero el cuadre las suma;
  - **B2:** «Of which: interest paid…» **después** de la línea de total. El bloque termina en el total y no se examina lo que sigue;
  - **B3:** un **segundo bloque** de financiación en la página (operaciones interrumpidas) con intereses. `bloque()` toma solo el primero;
  - **B4:** un estado en **millones** con una mención suelta de «thousands of euros». `UNIDAD` se busca en toda la página;
  - **B5:** la adquisición del año en una línea solo con importes (rótulo desplazado). El cuadre la suma y ni la expresión de adquisiciones ni la lista blanca la ven;
  - **B11:** minoritarios incluidos en «Total liabilities» y desglosados aparte, después del total.

**[Hecho] En los datos reales no cambia nada.**
- En los diez `CF_<año>.txt`, la página de flujos tiene un solo bloque de financiación, ningún «of which», «miles» y no «millones».
- En los bloques de la matriz, las únicas líneas solo con importes son totales impresos aparte (financiación 2018 y 2019), que `cuadre()` saca del cuerpo.
- La reproducción de la matriz es idéntica a la entregada.

**[Hecho] Lo que dice el informe.** `INFORME_N4_4_9.md` §2 dice «cada línea del bloque tiene que estar en una lista blanca de rótulos conocidos». No es exacto para las líneas sin rótulo, ni para lo que queda fuera del bloque.

**[Interpretación]**
- No permite confirmar ningún cero: la IA no confirma y las propuestas están sin firmar.
- Afecta a la base que `PROPUESTA_AUTOMATIZACION_4_9.md` presenta para una verificación automática futura.

**[Propuesta]**
- Que una línea solo con importes dentro del cuerpo, que no sea el total, sea una excepción.
- Que se examine la página completa en busca de un segundo bloque, de líneas «of which / de los cuales» y de la unidad en la cabecera del estado.
- Añadir B1–B5 y B11 a `test_n4_comprobaciones.py`.
- Precisar la frase del §2 del informe.

### V-5 · MENOR · Restos de Z-7 en `INFORME_N4_4_9.md` y en la matriz (2023)

**[Hecho]**
1. **Contradicción interna del informe sobre 2023.**
   - `INFORME_N4_4_9.md` §2, l. 58: «De 2017 a 2023 solo se conserva la traducción inglesa».
   - El mismo informe, §6, l. 134, y el registro, §9: «2017–2022 solo en inglés … 2023 se contrasta con la columna comparativa del informe español de 2024».
2. **Un «igual» que la matriz desmiente.**
   - `N4-minoritarios-2023` dice en su explicación «Igual en la versión española (prevalece)».
   - Pero su contraste español registra `coincide_con_el_texto_ingles: false`: el texto inglés de 2023 da un total del pasivo de 1.257.579 y un total de 2.481.911; la comparativa de 2023 del PDF español de 2024 da 1.284.595 y 2.508.927.
   - Probablemente es la reexpresión de 2024. El patrimonio atribuido coincide: 1.224.332.
   - Ni la explicación ni el informe mencionan la diferencia. El cuadre se cumple en las dos versiones.
3. **Un contraste que falta.** `N4-otros_activos_financieros-2023` no tiene `contrastes` (`null`), aunque el PDF español de 2024 contiene su columna comparativa: el activo corriente de 2023 es 816.395, ya leído en el contraste de 2024. El registro, §6 (Z-7), dice «Contrastes añadidos (2023 con la comparativa del informe español de 2024)» sin esa excepción.

**[Interpretación]** No cambia ninguna clase, pero el informe y la matriz no dicen lo mismo, y «igual» oculta una reexpresión que la propia matriz detecta.

**[Propuesta]**
- Corregir la l. 58.
- Explicar en la entrada de 2023 que el cuadre es igual pero las cifras están reexpresadas.
- Añadir el contraste de otros activos financieros 2023, o declarar su ausencia en el registro.

### V-6 · MENOR · Restos de Z-9 y Z-10: `.lo_perfil/` vacío, duraciones, uso sin `-B` y texto de la tabla antes/después

**[Hecho]**
1. **Una carpeta `.lo_perfil/` vacía en el paquete.**
   - El paquete contiene `personaje_v2/pruebas/sintetico/EmpresaX_cero_pendiente/.lo_perfil/`, un árbol de carpetas vacías, con 0 archivos (`find … -type f | wc -l` = 0). No está en el manifiesto, porque no tiene archivos.
   - Ya estaba en la descompresión de la 4.8.1 (`/home/claude/pristina_481/…`, solo lectura).
   - El registro, §6 (Z-9), dice «el paquete se construye sin `__pycache__` ni `.lo_perfil/`».
2. **Duraciones que no coinciden.** La cabecera de `verificar_paquete.sh` (l. 12) dice «≈ 10–13 min en total», y `CONTINUIDAD.md` §2.2 dice «unos 10–12 minutos». Era uno de los puntos de Z-10, que el registro da por corregido.
3. **Un uso que escribe `__pycache__`.**
   - La línea de uso de `E/scripts/test_n4_comprobaciones.py` sigue siendo `python3 -I test_n4_comprobaciones.py`, sin `-B`.
   - El script importa `n4_investigacion` sin fijar `sys.dont_write_bytecode`, así que seguida al pie de la letra escribe `E/scripts/__pycache__/`. Es exactamente lo que ocurrió en Z-9.
   - El comando de `INFORME_N4_4_9.md` sí lleva `-B`.
   - En cambio, `comprobar_entrega_4_9.py` sí fija `sys.dont_write_bytecode`: su comando sin `-B` en `CONTINUIDAD.md` y en `PROMPT_NUEVA_VENTANA.md` no escribe nada.
4. **El texto de la tabla antes/después.** `E/reproduccion/tabla_antes_despues_rv1.md` (y `E/scripts/tabla_antes_despues_rv1.py`, l. 27) dicen que la reproducción usa «cierre_v2.py y pipeline.py de la 4.8.1; el resto del código es idéntico». En realidad, `E/reproduccion/codigo_4_8_1/` sustituye cuatro archivos, también `ficha.py` y `resumen.py`, como dice bien `INFORME_RV1_4_9.md` §1.

**[Propuesta]**
- Excluir también las carpetas `.lo_perfil` vacías al empaquetar.
- Igualar las duraciones.
- Añadir `-B` a la línea de uso del script, o fijar `dont_write_bytecode` en él.
- Corregir la frase de la tabla.

### V-7 · MENOR · Registro y límites declarados: afirmaciones adelantadas en §6 y límite de la reescritura coordinada formulado con más archivos de los necesarios

**[Hecho]**
1. **Afirmaciones adelantadas en el registro.**
   - `REGISTRO_ENTREGA_4.9.md` §6, fila Z-8, afirma en presente: «Existen el registro, el LEEME, las auditorías y la salida de referencia del control de la 4.9».
   - Hoy no existen `E/AUDITORIA_INTERNA_4_9_vigencia.md` ni `E/resultados/comprobar_entrega_4_9_salida.txt`. Son los pendientes que declara el encargo.
   - `comprobar_entrega_4_9.py` constata la existencia de `AUDITORIA_INTERNA_4_9_vigencia.md` (l. 210): sobre el árbol actual daría 35 de 36.
   - El LEEME presenta sus resultados como «observados sobre una descompresión limpia del ZIP de la 4.9 (§8)», y la §8 está pendiente.
2. **El límite de la reescritura coordinada necesita menos archivos de los que dice.**
   - `CONTINUIDAD.md` §5 y §8 e `INFORME_RV1_4_9.md` §5 formulan el límite como «un agente que reescriba a la vez `auditoria.md`, `estado_pipeline.json` y `cierre_vigente.json`».
   - En un cierre anterior a la 4.8.1, como el de la 4.6.1, **bastan dos archivos**: con `auditoria.md` sustituida por otra APROBADO y `cierre_vigente.json → auditoria_sha256` igual a su huella, el paso 14 termina en «concluido · paso 14», con código 0 y los dos destinos en APROBADO (caso Z1g).
   - En uno de la 4.9 basta con **borrar** el estado y reescribir `cierre_vigente.json` y `auditoria.md` (Z1h: `ficha.py` termina con 0 y los dos destinos en APROBADO).

**[Interpretación]**
- El punto 1 es esperable antes del cierre de la entrega, pero el registro no puede quedar así en la entrega final.
- El punto 2 es un límite de procedimiento ya asumido. Solo está formulado con más archivos de los necesarios.

**[Propuesta]**
- Verificar en la §8 que existan los dos archivos y que `comprobar_entrega_4_9.py` dé 36 de 36.
- Formular el límite como «quien reescriba `auditoria.md` y el registro de la respuesta (`cierre_vigente.json` y, si existe, `estado_pipeline.json`)».

---

## 3. Lo que se comprobó y está bien

**Integridad del paquete**
- **[Hecho] Manifiesto.** `MANIFIESTO_SHA256.txt` cubre exactamente los 1.631 archivos del árbol, salvo él mismo: ninguno de más, ninguno de menos, ninguna huella distinta (`/home/claude/vigencia_4_9/tmp/comparar_manifiestos.py`).
- **[Hecho] Frente a la 4.8.1.** Frente a `E/reproduccion/MANIFIESTO_4_8_1.txt` (1.539 archivos) hay:
  - **11 modificados**, exactamente los del registro §3 (más `MANIFIESTO_SHA256.txt`, que el manifiesto 4.8.1 no se lista a sí mismo);
  - 0 ausentes;
  - 93 nuevos, todos en `E/` salvo `personaje_v2/pruebas/test_integridad_auditoria_v2.py` y el manifiesto.
  - `informe.py` no cambia. Los expedientes históricos, los originales y `fase1_decisiones.json` están intactos.
- **[Hecho] `CAMBIOS_ARCHIVOS.txt` es coherente** (`comprobar_cambios.py`): 21 modificados, 954 nuevos, 0 eliminados y 655 sin cambios (= 1.630 archivos, sin él ni el manifiesto). Las huellas «nuevo» coinciden con el árbol. Las huellas «base» son las mismas que en el `CAMBIOS_ARCHIVOS.txt` de la 4.8.1. Los 655 «sin cambios» son idénticos a la 4.8.1.
- **[Hecho] H2.** El SHA-256 del código fuente de `Pipeline.veredicto_auditoria` es `9edf6252ca48c80009b5b51b52aeaa447960ab611150b908738194e526775422`, el mismo en el código actual y en `codigo_4_8_1/pipeline.py`.

**R-V1, Z-1, Z-2 y Z-3**
- **[Hecho] Batería.** `test_integridad_auditoria_v2.py` da **80/80** (11 s) con el código actual y **24/77** con `--codigo E/reproduccion/codigo_4_8_1`. En los dos casos, el grupo, el nombre y el resultado coinciden prueba a prueba con `E/resultados/test_integridad_auditoria_v2.json` y con `E/reproduccion/test_integridad_con_codigo_4_8_1.json` (`comparar_baterias.py`). Con el código 4.8.1 fallan los 16 casos del grupo H: 6 de Z-1, 9 de Z-2 y 1 de Z-3, como dice el registro.
- **[Hecho] Solicitudes.** `test_auditorias_v2.py` da **55/55** con el código 4.9 (35 s; salida en `ejecuciones/test_auditorias_salida.txt`). No creó ningún perfil de LibreOffice en los temporales y el árbol siguió idéntico.
- **[Hecho] Mutaciones.** `mutar_rv1.py --salida <tmp>`: 23 de 23 detectadas, con un JSON idéntico al conservado (`comparar_mutaciones_salida.txt`).
- **[Hecho] Integración en el verificador.** `comprobar_integracion_verificador_49.py` da 13 de 13. Antes se comprobó que solo ejecuta el bloque extraído de `verificar_paquete.sh` contra sustitutos en un temporal.
- **[Hecho] Función B, ataques nuevos** (`ataques_vigencia.py b b_estado`; salidas en `ataques_b_salida.txt` y `ataques_b_estado_salida.txt`). **Se retiran:**
  - CR CR LF intermedio; FF final; «espacio + salto» final; tabulador por espacio; NEL (U+0085) antes de la solicitud;
  - el identificador de la solicitud en hexadecimal en mayúsculas; el rótulo de la solicitud en mayúsculas o sin tilde; la solicitud en negrita, en cita o tras un ZWSP; la solicitud duplicada dentro de un bloque de código; el identificador del material en mayúsculas;
  - U+2126/U+212B añadidos; combinantes añadidos; el archivo vacío;
  - el material de la respuesta cambiado en el estado; una solicitud duplicada pendiente; una solicitud duplicada respondida por otra; `auditoria` registrada `None`.
- **[Hecho] Siguen vigentes, como declara D-RV1a:**
  - «·» → U+0387, una equivalencia canónica que NFC deshace;
  - «LF CR» al final;
  - BOM + CR + NFD + saltos finales por las cuatro vías;
  - con `fiel` vacío en el estado, la respuesta con bytes idénticos (con CRLF se retira).
- **[Hecho] Z-1, ataques nuevos** (`ataques_z1_salida.txt`). Se retiran por las vías probadas, sin crear `cierre_vigente.json` ni atribuir ninguna huella:
  - la auditoría original sin `cierre_vigente.json`;
  - `cierre_vigente.json` = `{}`, con `auditoria_sha256` nula o solo con `auditoria_fiel`;
  - el estado legible sin `auditoria_respuesta` (`ficha.py`, paso 14 y `resumen.py`);
  - `estado_pipeline.json` = `null`;
  - `--reiniciar --desde 14`.
- **[Hecho] Z-2, ataques nuevos** (`ataques_z2_salida.txt`). Se retiran sin traza, por las vías indicadas en cada caso:
  - `cierre_vigente.json` ilegible por el paso 14 y `resumen.py`;
  - el estado ilegible sin `--desde` (código 6), por `informe.py` y por `resumen.py`;
  - el estado con BOM o no UTF-8;
  - `auditoria.md` en UTF-16 sin BOM o con un sustituto suelto;
  - el estado ilegible con un destino inaccesible: código **5** por el paso 14 y sin `--desde`.
- **[Hecho] Lecturas restantes.** Las lecturas no tolerantes que quedan en los cinco scripts son `material_fijado` (V-1), `ficha.json` (V-1), `adoptar_archivo` (del estado que escribe el propio pipeline) y `registrar_cierre`/`registrar_informe`. Estas dos últimas se alcanzan solo después de una comprobación que ya leyó esos archivos.
- **[Hecho] Diff de los cuatro scripts frente a `codigo_4_8_1/`**: 174, 25, 3 y 2 líneas.
  - Solo contiene lo declarado: las funciones A y B, `texto_fiel`, `huella_fiel`, `lineas_solicitud`, `leer_json_control` y `_j_tolerante`; la rama Z-1; la lectura de bytes; `fiel` en el paso 13; `registrar_cierre` con la solicitud y la huella fiel; `try/except ValueError` en `main()`; y la lectura tolerante del estado en `ficha.py` y `resumen.py`.
  - No se encontraron cambios no declarados.
  - Única regresión semántica observada: `motivo_vigencia` trata una `ficha.json` ilegible como «sin salida cerrada» (V-1).
- **[Hecho] Expedientes reales.** Los expedientes reales con ficha cerrada sin `cierre_vigente.json` son los seis originales, Aarsleff corregido, la 4.5 y la 4.6. Con el código 4.8.1 ya se retiraban por `informe.py`, `resumen.py` y el pipeline (`CONTINUIDAD.md` §9.3); la 4.9 solo añade que `ficha.py` ya no los vuelve a cerrar. Ningún expediente real tiene `auditoria_respuesta`: no hay ningún cierre real de la 4.8.1, como dice `INFORME_RV1_4_9.md` §3.

**N4, Z-4 a Z-7**
- **[Hecho] Reproducción.** `n4_investigacion.py --salida <tmp> --propuestas <tmp>/prop` (con `efectos/efectos_n4.json` copiado a la salida, como prevé el procedimiento de `INFORME_N4_4_9.md`) produce:
  - `matriz_n4.csv`, `recuento_n4.json` y `propuestas_n4_sin_firmar.json` **idénticos byte a byte**;
  - `matriz_n4.json` idéntica salvo el campo `efectos` (la ruta), con 0 diferencias dentro de la matriz;
  - una salida de consola idéntica a `E/resultados/n4_investigacion_salida.txt`.
  - Sin `efectos/` en la salida, las 35 entradas pierden su `delta_por_1_mm`. Es coherente con el orden documentado: primero `efectos_n4.py` (`comparar_n4.py`).
- **[Hecho] Cobertura:** 38 / 35 (8 con reserva) / 3 / 0 / 0. `test_n4_comprobaciones.py` da 16/16, con una salida idéntica a la de referencia.
- **[Hecho] Código N4.**
  - Las clases 4 dependen de condiciones comprobadas: la fecha, el cuadre sin línea, las notas, el «Finance Lease 40,916», la regla y la deuda de 2018 = E22.
  - `cuadre_actual` ya no tolera un ilegible en la columna del año.
  - `aplicar_condiciones_generales` baja a la clase 3 cualquier entrada de clase 2 o 4 con un fallo.
- **[Hecho] Campos humanos.** En las propuestas y en `decisiones_y_preguntas_4_9.json` están vacíos; ninguna pregunta está enviada (lo constata `comprobar_entrega_4_9.py`, cuyo código se leyó).

**Documentación**
- **[Hecho] Cifras coherentes** en `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `DECISIONES.md` (entrada del 11-nov), `INFORME_RV1_4_9.md`, `INFORME_N4_4_9.md`, el registro, el LEEME y `comprobar_entrega_4_9.py`: 80, 23, 24/77, 16, 36 de 36, 38/35/8/3/0/0 y −0,0284. Fuera de las citas intencionadas del registro §6 y de la nota de conservación no queda ninguna cifra antigua (63, 15, 24/61, 12).
- **[Hecho] Recuento de `comprobar_entrega_4_9.py`**, leído en el código: **36 comprobaciones** (5 + 10 + 11 + 10; 8 reejecutan, 15 recalculan y 13 constatan). Coincide con «36 de 36».
- **[Hecho] Archivos citados.** Todos los archivos citados en la documentación de la 4.9 existen (`archivos_citados.py`), salvo los pendientes declarados y nombres genéricos de archivos de ejecución.
- **[Hecho] Anexo D.** Describe la función B, Z-1 y Z-2, sin tachados. Omite solo el código 5 junto al 6.
- **[Hecho] Registro §6.** Sus afirmaciones sobre Z-1, Z-2, Z-3, Z-5 y Z-6 corresponden a lo hecho: código, grupo H con 6 y 9 casos, M16–M23 y `efectos_n4.py` con C12, C50 y `p_estrella`. Las de Z-4, Z-7, Z-8, Z-9 y Z-10 corresponden con las reservas de V-4 a V-7.

---

## 4. Lo que no se pudo comprobar

- **No se ejecutó nada con LibreOffice, por restricción del encargo:**
  - `efectos_n4.py`: los valores recalculados de `efectos_n4.json` solo se revisaron en su aritmética y en sus copias;
  - `verificar_paquete.sh`;
  - `test_comprobadores.py`, `test_pipeline_sintetico.py`, `test_estados_v2.py`, `test_cierre_v2.py` y `test_resumen_v2.py`;
  - `comprobar_entrega_4_9.py`: el resultado «36 de 36» no se ha ejecutado, solo se contaron sus comprobaciones en el código;
  - los controles históricos y `comparar_baterias_*`.
- **No verificables desde esta copia:**
  - los resultados «observados» del LEEME para los controles históricos;
  - la coincidencia de 28/28 de `test_estados_v2.py` que menciona el registro §6;
  - el ZIP final, su huella y la §7–§8 del registro, que están pendientes.
- **Contraste documental parcial.** Las cifras españolas de 2023 y de 2024–2025 se revisaron a través de la matriz y del código que la genera. No se abrieron los PDF a mano.

**Scripts del auditor** (todos en `/home/claude/vigencia_4_9/tmp/`):
- `comparar_manifiestos.py`;
- `comprobar_cambios.py`;
- `comparar_baterias.py`;
- `ataques_vigencia.py` (subcomandos `z1`, `z2`, `b`, `b_estado` y `registrar_cierre`). En `ataques_b_salida.txt`, el caso «fiel_vacio_tras_CRLF» tenía un error del propio script, que vaciaba el archivo; el resultado válido es el de `ataques_b_estado_salida.txt`;
- `engano_n4_vigencia.py`;
- `comparar_n4.py`;
- `comprobar_efectos.py`;
- `archivos_citados.py`.
