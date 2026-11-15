# Auditoría interna de la entrega 4.9 (R-V1, N4 y documentación)

> **Nota de conservación (añadida al copiar el informe en el expediente; el texto del auditor no se ha modificado).**
> - El informe se escribió sobre la copia `/home/claude/auditoria_4_9/munger_v2_r1`, que no forma parte del paquete. Su SHA-256 como lo entregó el auditor está en `auditoria_interna/AUDITORIA_INTERNA_4_9.md.sha256`.
> - Los scripts y salidas pequeñas del auditor que cita como `/home/claude/auditoria_4_9/tmp/<archivo>` se conservan en `auditoria_interna/material_auditor/<archivo>`. No se conservan los textos `es2024.txt` y `es2025.txt` (`pdftotext` de los PDF españoles del paquete, regenerables) ni las carpetas de escenarios, el código 4.8.1 copiado y el ESEF descomprimido (todos regenerables desde el paquete).
> - El material fijado que audita es `MATERIAL_AUDITORIA_4_9.txt` (54 huellas; SHA-256 `be02e0f8…f598`). Las cifras de este informe (63 pruebas, 15 mutaciones, 24/61, 12 pruebas de N4) son las de ese material. El tratamiento de cada hallazgo y las cifras finales están en `REGISTRO_ENTREGA_4.9.md` §6.


Auditor independiente, en un contexto separado y sin haber participado en el trabajo. Fecha: 11-nov-2026. Copia auditada: `/home/claude/auditoria_4_9/munger_v2_r1`. Todos los scripts y temporales del auditor están en `/home/claude/auditoria_4_9/tmp/`; las rutas de este informe son relativas a `munger_v2_r1/` salvo que empiecen por `/`.

Convenciones: **[Hecho]** = comprobado por el auditor con un comando o una lectura citados; **[Interpretación]** = juicio del auditor sobre un hecho; **[Propuesta]** = lo que el auditor sugiere, sin aplicarlo. El auditor no ha corregido nada en la copia.

## 0. Material fijado

- **[Hecho]** `MATERIAL_AUDITORIA_4_9.txt` tiene el SHA-256 `be02e0f86b035e183d1910118e1477bdaa4dd5ab1ba6bf2f36880b703eabf598`, el indicado en el encargo.
- **[Hecho]** Al empezar la auditoría coincidían las 54 huellas del material: `sha256sum -c` no dio ninguna línea distinta de «OK».
- **[Hecho] Incidencia causada por el auditor.** El material incluye un archivo de bytecode, `…/2026-11_Vidrala_ensayo_4_9/scripts/__pycache__/n4_investigacion.cpython-313.pyc`. A las 11:11 el auditor ejecutó `python3 -I …/scripts/test_n4_comprobaciones.py`, el comando que documenta `INFORME_N4_4_9.md`. La opción `-I` no impide escribir bytecode, así que Python regeneró ese `.pyc`, y su huella ya no coincide con la del material.
  - Es el único archivo de la copia que cambió por la auditoría, aparte del perfil de LibreOffice (ver la sección 5). Lo confirma `find . -newer MATERIAL_AUDITORIA_4_9.txt -type f`.
  - Los 53 archivos restantes del material siguen coincidiendo, y también todos los `.py` fuente.
  - El hecho es en sí mismo un hallazgo (Z-9).

## 1. Hallazgos

### Z-1 · BLOQUEANTE · Sin `cierre_vigente.json`, `ficha.py` vuelve a cerrar con cualquier auditoría APROBADO del material y le atribuye la huella del archivo actual

**[Hecho] Qué pasa.** `cierre_v2.motivo_rechazo_cierre()` solo compara la auditoría con algo registrado en dos casos: si `estado_pipeline.json` tiene `auditoria_respuesta`, o si `cierre_vigente.json` tiene `auditoria_fiel`/`solicitud` o `auditoria_sha256`. Si no hay ni lo uno ni lo otro, solo comprueba H2 y la línea «Material auditado».
- `ficha.py --estado concluido` usa esa función (no `motivo_vigencia`) y, si no hay motivo, escribe la ficha cerrada.
- Después llama a `registrar_cierre()`, que crea un `cierre_vigente.json` nuevo con `auditoria_sha256` = la huella del `auditoria.md` **actual**.
- A partir de ahí, `informe.py`, `resumen.py` y `pipeline.py --desde 14` dan el cierre por vigente.

**Reproducido** (escenarios en `/home/claude/auditoria_4_9/tmp/escenarios/`; las salidas JSON de cada caso están en `/home/claude/auditoria_4_9/tmp/`):

| Caso | Qué se hace | Resultado observado |
|---|---|---|
| a. Cierre real de la 4.6.1 (sin solicitudes), copiado | Se borra **solo** `cierre_vigente.json` y se sustituye `auditoria.md` por otra auditoría sintética APROBADO, sin solicitud y con el material fijado | `ficha.py` termina con código 0 (concluido, `cierre` APROBADO) y registra `auditoria_sha256` = b882f5d2…, la huella del archivo nuevo; la original era c051cfaa…. Después, `informe.py` da 0, `resumen.py` publica «APROBADO» y `pipeline.py --desde 14` termina en «FIN · estado concluido · auditoría APROBADO», con código 0 |
| b. Lo mismo con el código 4.8.1 (`reproduccion/codigo_4_8_1/`) | Igual que el caso a | Mismo resultado: **el defecto es anterior a la 4.9**; la 4.9 no lo introduce, pero tampoco lo cierra |
| c. Cierre de la 4.6 (`…_4_6/Vidrala`: ficha cerrada, material fijado, **sin** `cierre_vigente.json` de origen), copiado | **Sin borrar nada**, se sustituye `auditoria.md` por otra APROBADO del material | `ficha.py`, `informe.py` y `resumen.py` terminan con código 0; se crea `cierre_vigente.json` con la huella del archivo nuevo y la fila queda «concluido · APROBADO» |
| d. Cierre de la 4.9 (respuesta a una solicitud) | Se borran `estado_pipeline.json` **y** `cierre_vigente.json` y se pone otra auditoría APROBADO **sin línea de solicitud** | `ficha.py` termina con código 0 y la ficha queda cerrada con un `cierre_vigente.json` nuevo; `informe.py` termina con 0 y `resumen.py` publica la fila en los dos destinos (`concluido`, `verificacion` vacía porque no hay estado) |
| e. Control | Se borra solo `estado_pipeline.json` (lo que hace `--reiniciar`) en un cierre de la 4.9 | Se retira correctamente (código 3): la rama de `cierre_vigente.json` con huella fiel funciona |

**[Interpretación] Por qué es bloqueante.**
- El resultado es una aprobación indebida vigente por las cuatro vías.
- Contradice la compatibilidad que pedía el encargo (§3.3): «no calcular una huella del archivo actual para atribuírsela retroactivamente a una aprobación antigua». `registrar_cierre` lo hace siempre que falta el registro.
- Contradice también `ANEXO_D` («en los cierres anteriores a la 4.8.1 … `auditoria.md` tiene que ser la que registra `cierre_vigente.json`, byte a byte») y la tabla de compatibilidad de `INFORME_RV1_4_9.md` §3.
- El límite declarado («un agente que reescriba a la vez `auditoria.md`, `estado_pipeline.json` y `cierre_vigente.json` con huellas coherentes») no lo cubre: aquí no hace falta calcular ninguna huella. En el caso a basta con borrar un archivo, y en el caso c no hay que borrar nada.
- La batería de 63 pruebas no tiene ningún caso con `cierre_vigente.json` ausente.

**Cómo se reproduce:**
- `cd /home/claude/auditoria_4_9/tmp && python3 -B ataques_rv1.py 461_sin_cv sin_estado_ni_cv sin_estado`, con salida en `ataques_rv1_461_sin_cv*.json` y `ataques_rv1_sin_estado_ni_cv_sin_estado.json`.
- Con el código 4.8.1: `SCR_AUDITOR=/home/claude/auditoria_4_9/tmp/codigo481/personaje_v2/scripts BASE_AUDITOR=/home/claude/auditoria_4_9/tmp/escenarios481 SUFIJO_AUDITOR=_codigo481 python3 -B ataques_rv1.py 461_sin_cv`.
- Caso c: `python3 -B ataque_46.py`.

**[Propuesta]**
- Que `motivo_rechazo_cierre` falle del lado seguro cuando hay un cierre que acreditar y ningún registro de la respuesta aprobada: hay ficha cerrada o `historial_cierres/`, `material_auditoria.json` está fijado y no hay ni `auditoria_respuesta` ni `cierre_vigente.json`.
- Que `registrar_cierre` no calcule `auditoria_sha256` cuando no existía un registro previo que lo respaldara; para un cierre así haría falta una auditoría nueva.
- Que se añadan a la batería los casos a, c y d.
- Que el límite de `CONTINUIDAD.md` §8 y de `INFORME_RV1_4_9.md` §5 se corrija si se decide no repararlo.

### Z-2 · BLOQUEANTE (el fallo es ruidoso) · Un `auditoria.md` que no es UTF-8, o un archivo de control ilegible, rompe las cinco vías sin retirar la aprobación

**[Hecho] Qué pasa.**
- `motivo_rechazo_cierre` lee primero `open(p, encoding="utf-8").read()` (línea 314) y lanza `UnicodeDecodeError` antes de llegar a `motivo_respuesta_no_aceptada`.
- Por eso la rama «no es texto UTF-8 válido» de esa función (líneas 176–177) es **inalcanzable**.
- La excepción salta en `pipeline.py` (también sin `--desde`, porque `asegurar_vigencia` está fuera del `try`), en `ficha.py`, en `informe.py` y en `resumen.py`, siempre con código 1.
- La ficha sigue cerrada, `cierre_vigente.json` sigue presente y las filas de los dos destinos siguen en «APROBADO».

**[Hecho] Casos probados** (13 transformaciones por 4 vías, más la vía sin `--desde`; `ataques_mut_salida.txt` y `ataques_rv1_mutaciones_otras_vias.json`):
- un byte `\xff` añadido;
- la respuesta guardada en cp1252, como hace un editor de Windows;
- la respuesta guardada en UTF-16 con BOM.

En los tres casos el código es 1, el estado sigue `concluido`/`APROBADO` y los dos destinos siguen en «APROBADO». Lo mismo ocurre si `cierre_vigente.json` o `estado_pipeline.json` quedan vacíos o ilegibles (`python3 -B ataques_rv1.py ilegibles`): `JSONDecodeError`, código 1 y la aprobación sigue publicada.

**[Hecho]** La línea es la misma en el código 4.8.1 (`reproduccion/codigo_4_8_1/cierre_v2.py:234`): el defecto es anterior.

**[Interpretación]**
- No es un falso «código 0», porque el fallo se ve en la traza.
- Pero una aprobación sobre un texto que ya no es el aceptado sigue presentada como vigente en la ficha y en todos los destinos, y ninguna herramienta del sistema puede retirarla hasta que alguien repare el archivo a mano.
- El encargo pedía probar expresamente los archivos que no son UTF-8.
- `CONTINUIDAD.md` §5 afirma que «cualquier otro cambio retira la aprobación en la primera llamada», y eso no es cierto en este caso.

**[Propuesta]**
- Que `motivo_rechazo_cierre` lea los bytes una sola vez y devuelva un motivo, en vez de lanzar una excepción, si el texto no es UTF-8 (para lo que ya existe `texto_fiel`).
- Que trate como motivo de retirada un `estado_pipeline.json` o un `cierre_vigente.json` ilegibles.
- Que se añadan esos casos a la batería.

### Z-3 · IMPORTANTE · La batería de 63 pruebas no fija los límites de la lista de transformaciones inocuas ni la rama de `cierre_vigente.json` con huella fiel

**[Hecho]** El auditor añadió siete mutaciones a las 15 de `mutar_rv1.py` (`/home/claude/auditoria_4_9/tmp/mutar_extra.py`, con salida en `mutar_extra_salida.txt` y `mutar_extra.json`). Con cada una de estas cinco, la batería **sigue dando 63/63**:

| Mutación | Efecto si llegara al código |
|---|---|
| X1 · `texto_fiel` normaliza con NFKC, no con NFC | Igualaría «10²» con «102», «ﬁ» con «fi» y los dígitos de ancho completo con los normales: cambios de significado que pasarían por inocuos |
| X3 · elimina los caracteres de formato (Cf: ZWSP, BOM interior…) | Ampliaría la lista sin decisión (D-RV1a) |
| X5 · convierte el espacio no separable en un espacio normal | Ídem |
| X7 · trata VT, FF y U+2028 como saltos de línea | Ídem |
| X4 · sin estado, ignora `auditoria_fiel` de `cierre_vigente.json` (vuelve a comparar bytes) | Las pruebas F «sin `estado_pipeline.json`» siguen pasando porque solo miran el caso intacto y dos cambios que la comparación de bytes también detecta; ninguna combina «sin estado» con una transformación inocua |

(X2, que recorta todo el espacio final, sí se detecta. X6, que quita la comprobación del material en `resp`/`sol`, tampoco se detecta, pero esa comprobación es redundante con `motivo_auditoria_no_corresponde`; no se cuenta como hallazgo.)

**[Hecho]** El código actual se comporta bien en esos casos: las inserciones de ZWSP, NBSP, VT, U+2028, el BOM interior, el doble BOM y la solicitud con caracteres de ancho completo **se retiran** por las cuatro vías. Las variantes inocuas (U+037E, que NFC convierte en «;», y la combinación BOM + NFD + CRLF + sin salto final) **siguen vigentes** (`ataques_mut_salida.txt`).

**[Interpretación]**
- La reparación está bien, pero la batería no lo demostraría si cambiara.
- La afirmación «15 mutaciones, las 15 detectadas» es cierta, pero da una impresión de cobertura mayor que la real en el punto que deja abierto D-RV1a.
- Faltan también los casos de Z-1 y Z-2.

**[Propuesta]** Añadir al grupo G, como pruebas unitarias de `huella_fiel` en la lista «relevantes», una variante de compatibilidad NFKC (por ejemplo «²»), un ZWSP, un NBSP y un U+2028. Añadir también un caso F «sin estado + CRLF → vigente» y los casos de Z-1 y Z-2.

### Z-4 · IMPORTANTE · Las comprobaciones de N4 no deciden lo que el informe dice que deciden y admiten falsos positivos

**[Hecho] Leído en `…/scripts/n4_investigacion.py`:**
1. `cita_en_su_pagina`, `comparativa_coherente` y la detección de la unidad se calculan, pero **no intervienen en la clasificación** (líneas 334, 362–364, 420 y 439). Una cita fuera de su página o una comparativa «NO coherente: revisar» seguirían dando la clase 2.
   - La prueba 10 de `test_n4_comprobaciones.py` («una cita que no está en su página no se da por contrastada») solo prueba la función auxiliar, no la clasificación.
2. Las **clases 4 están fijadas** sin condición (líneas 397, 406 y 429), con explicaciones literales en el código: «Finance Lease 40.916», «nota 15, p. 57», «no hay arrendamientos financieros». Los cuadres que se calculan para esas entradas no cambian nada.
3. **La tolerancia a la errata no distingue la columna.** `cuadre_actual()` acepta un cuadre si la columna del año cuadra y hay *alguna* línea ilegible, aunque esté en la columna del año, porque en `cuadre()` un ilegible cuenta como 0.
   - La prueba 5 («importe ilegible en la columna del año: no se acepta») pasa solo porque su ejemplo descuadra la suma.
   - Con un ilegible que no la descuadra, se acepta.
4. **La detección es por rótulo.** Con estados sintéticos, `/home/claude/auditoria_4_9/tmp/engano_n4.py` (salida en `engano_n4_salida.txt`) obtiene **15 falsos positivos de 16 casos** que debían rechazarse:
   - intereses en financiación rotulados «Finance costs paid», «Gastos financieros pagados» o «Borrowing costs paid»;
   - una adquisición del año rotulada «Acquisition of businesses», «Business combinations», «Purchase of subsidiaries», «Adquisición de negocios» o «Combinaciones de negocios»;
   - activos financieros corrientes rotulados «Short-term investments», «Current financial assets», «Marketable securities», «Imposiciones a corto plazo», «Inversiones a corto plazo» o «Activos financieros corrientes»;
   - el ilegible del punto 3.

   El único caso rechazado es el de control, «Acquisition of a subsidiary».

**[Hecho] En los datos reales esto no cambia ninguna clase.** El auditor revisó las líneas de todos los bloques reales que usa la matriz (sección 2), y ninguno tiene rótulos alternativos de ese tipo. Las ocho entradas pedidas se contrastaron a mano (sección 2).

**[Interpretación]**
- No permite confirmar un cero, porque la IA no confirma y las propuestas están sin firmar. Por eso no es bloqueante.
- Pero `INFORME_N4_4_9.md` §2 («no basta con que la cita exista: se comprueba que está en su página», «la columna comparativa del informe siguiente cuadra igual») y `PROPUESTA_AUTOMATIZACION_4_9.md` §1 presentan estas comprobaciones como la base de una futura verificación automática.
- Tal como están, no podrían serlo: §2.2 de la propuesta exige ya «ninguna línea ilegible en la columna del año», y el código no lo comprueba.

**[Propuesta]**
- Que la clasificación exija `cita_en_su_pagina`, la comparativa no contradictoria y la unidad.
- Que la clase 4 dependa de comprobaciones (la norma por fecha, la ausencia de la línea y la nota de deuda).
- Que la tolerancia a la errata se limite a la columna comparativa.
- Que se clasifique por exclusión: toda línea del bloque que no esté en una lista blanca de rótulos conocidos se convierte en excepción.
- Que se añadan a `test_n4_comprobaciones.py` los casos de `engano_n4.py`.

### Z-5 · IMPORTANTE · Las decisiones de 2017–2018 se presentan como «precedentes humanos» sin respaldo en el archivo

**[Hecho]**
- `CONTINUIDAD.md` §1 («3 no aplicables … con precedentes humanos ya registrados») y `PROPUESTA_AUTOMATIZACION_4_9.md` §1 llaman humanos a los precedentes de `arrendamientos` 2017–2018 y de `arrendamientos_principal` 2017.
- En `fase1_decisiones.json` esas entradas, como la regla y la deuda 2018–2022, no tienen `fecha` ni `confirmado_por`. `INFORME_N4_4_9.md` §7 lo reconoce («sin fecha ni firma en el archivo»), pero titula la sección «Registro humano preexistente», y la matriz las guarda bajo `registro_humano`.
- `DECISIONES.md` (3-nov-2026, «Segunda empresa real: Vidrala») las recoge entre los trabajos de la sesión de construcción de la fase 1, sin atribuirlas a la persona responsable.

**[Interpretación]**
- No consta quién las tomó.
- Ninguna de esas entradas cumple los requisitos de una confirmación humana de H1: valor, fuente con página, fecha y persona.
- La propuesta D-N4-na («como ya hacen los precedentes registrados») descansa en parte en esa caracterización.

El trabajo, en cambio, **sí** las tiene en cuenta correctamente y no las altera. `fase1_decisiones.json` es idéntico al de la 4.8.1, y el razonamiento de 2018 (arrendamiento financiero de NIC 17 de 40.916 incluido en la deuda 2018 = 433.767; ver la sección 2) es coherente con la regla.

**[Propuesta]** Sustituir «precedentes humanos» por «decisiones registradas sin fecha ni firma (origen: sesión de construcción del 3-nov)». En D-N4-na, pedir a la persona responsable que confirme también esos precedentes si quiere apoyarse en ellos.

### Z-6 · MENOR · Varias cifras de efectos del informe no están en las salidas reproducibles

**[Hecho]** `efectos_n4.py` solo lee B78:D78, C83, Diagnóstico V6!C16, C52 y Motor!B255. Las copias guardadas no tienen cachés (C52 = None). Por eso **no constan en ningún archivo de salida**:
- `f` −2,76 % → −1,31 %;
- el paso de «⚠ REVISAR» a «✓ PASA» del control de rango;
- `f` −2,61 %;
- el «precio de Sí −0,0284 €» de L26.

Todas aparecen en `INFORME_N4_4_9.md` §4–§5, en `CONTINUIDAD.md`, en `DECISIONES.md` y en `VERSION`.

**[Hecho] Las cifras son correctas.**
- `f` = (X − C52) / ventas medias, según las fórmulas de Historia!C58 y C70, con las cachés del libro de referencia. Da −2,76 %, −2,61 % y −1,31 %, y el control de Diagnóstico V6!C50 (umbral −2 %) pasa de REVISAR a PASA (`python3 -B /home/claude/auditoria_4_9/tmp/comprobar_f_c48.py`).
- El precio de Sí (`P*` con G/L = k = 3) es invariante por traslación: si los tres V bajan 0,0284, `P*` baja lo mismo. Se comprobó G = 7,2106 y L = 2,4035.

**[Propuesta]**
- Añadir `Diagnóstico V6!C12` y `C50` a `SALIDAS` en `efectos_n4.py`.
- Calcular `P*` desde los V recalculados.
- Decir en el informe cuáles de esas cifras son derivadas analíticamente.

### Z-7 · MENOR · Contrastes con la versión española incompletos y textos de plantilla que no corresponden al año

**[Hecho]**
1. El PDF español de 2024 (`es_2118`) contiene la columna comparativa de 2023, que cuadra:
   - financiación 69.826, sin intereses;
   - «Pagos de intereses (12.320)»;
   - patrimonio atribuido 1.224.332 + pasivo 1.284.595 = 2.508.927.

   Pero las entradas de 2023 tienen `contrastes: {}`. C48 incluye 2023, así que la carencia 2 del informe (§6: «2017–2023 solo en inglés») está sobredimensionada para 2023.
2. `otros_activos_financieros` 2024 y 2025 no se contrastan con la versión española, aunque `INFORME_N4_4_9.md` §2 dice en general que «2024 y 2025 se repiten en la versión española». El auditor comprobó que coinciden: 752.728 / 816.395 y 712.559 / 752.728.
3. La explicación de minoritarios es un texto fijo.
   - En las entradas de 2017 a 2022 dice «Vidroporto en 2023, Envasados Eva y Glassco en 2024».
   - En 2025 atribuye a «política contable (fondo de comercio)» menciones que no lo son: las tres de 2025 son Vidroporto, el coste de la combinación y Envasados Eva/Glassco.
   - Además, no cita el dato más fuerte, la tabla de sociedades dependientes de CF_2025 (todas al 100 %; Envasados Eva al 45 % y Glassco al 20 %, por puesta en equivalencia).
4. Los pagos de arrendamientos 5.861, 6.117 y 8.314 aparecen también, idénticos, como «Expenses related to short-term leases…» en la misma nota (CF_2025.txt l. 2937). Es la discrepancia documental ya registrada en la 4.2, pero `INFORME_N4_4_9.md` §4 usa esas cifras sin recordarla.

**[Propuesta]** Contrastar 2023 con la comparativa española y `otros_activos_financieros` 2024–2025 con la versión española, generar la explicación con los contextos reales del año, citar la tabla de dependientes y recordar la discrepancia de la nota 8.

### Z-8 · MENOR · La documentación remite a archivos que no existen

**[Hecho]** No existen en la copia:
- `…_4_9/REGISTRO_ENTREGA_4.9.md`, citado en `CONTINUIDAD.md` §1, §4, §6 y §9, en `INFORME_RV1_4_9.md` §4 y en `PRECISION_ROIC_4_9.md`;
- `…_4_9/resultados/LEEME_BATERIAS_HISTORICAS.md`, citado en `CONTINUIDAD.md` §2 y §11 y en `PROMPT_NUEVA_VENTANA.md`. `CONTINUIDAD.md` §1 dice además que el LEEME de controles históricos ya está «armonizado»;
- `…_4_9/resultados/comprobar_entrega_4_9_salida.txt`, citado en `CONTINUIDAD.md` §2 y en el mensaje de arranque;
- las auditorías internas `AUDITORIA_INTERNA_4_9*.md`, citadas en `CONTINUIDAD.md` §7.

`CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt` siguen siendo los de la 4.8.1 (el encargo dice que se regenerarán).

**[Interpretación]** Probablemente son pendientes del cierre de la entrega, pero hoy `CONTINUIDAD.md` describe como hechos archivos que no están.

**[Propuesta]** No empaquetar hasta que existan, o cambiar las referencias.

### Z-9 · MENOR · `CONTINUIDAD.md` §2 no describe todo lo que escriben las pruebas y los comandos documentados

**[Hecho]**
1. Los comandos de reproducción de `INFORME_N4_4_9.md` («Cómo se reproduce todo») se dan sin `--salida`, y entonces **sobrescriben en el árbol** archivos entregados. `n4_investigacion.py` escribe por defecto en `n4/` y en `propuestas/`, `efectos_n4.py` en `n4/efectos/` (incluidas las copias `.xlsx`) y `mutar_rv1.py` en `resultados/mutaciones_rv1.json`. `comprobar_entrega_4_9.py` sí usa temporales.
2. `python3 -I …/test_n4_comprobaciones.py` (el comando documentado) escribe `scripts/__pycache__/…pyc` dentro del árbol: le ocurrió al auditor (sección 0). El manifiesto ignora `__pycache__`, pero `MATERIAL_AUDITORIA_4_9.txt` incluye ese `.pyc`, y `verificar_paquete.sh` dice «sin `__pycache__` dentro del paquete».
3. `test_estados_v2.py`, que el encargo de esta auditoría daba como ejecutable sin LibreOffice, lanza el pipeline con `--desde 1`, `--desde 2` y `--desde 3`, y usa LibreOffice. Tras ejecutarlo se modificaron cuatro archivos de `personaje_v2/.lo_perfil/` de la copia, a las 11:14. El auditor lo ejecutó porque estaba permitido; **puede haber coincidido con la otra tarea que usa LibreOffice**.
4. La copia contiene `personaje_v2/.lo_perfil/` (35 archivos que no están en el manifiesto de la 4.8.1). Si se empaquetaran, el bloque del manifiesto los contaría «de más», porque solo excluye `__pycache__`.

**[Propuesta]**
- Documentar `--salida` a un temporal en los comandos de reproducción, o cambiar los valores por defecto.
- Usar `python3 -I -B` en los comandos documentados.
- Retirar el `.pyc` del material y del paquete.
- Excluir `.lo_perfil/` al empaquetar.
- Decir en §2 que `test_estados_v2.py` usa LibreOffice.

### Z-10 · MENOR · Forma y coherencia menor

**[Hecho]**
- `PROMPT_NUEVA_VENTANA.md` (párrafo inicial): faltan comas o la «y» tras «(entrega 4.2)», «(entrega 4.3.1)», «(entrega 4.6)» y «(entrega 4.7)».
- `verificar_paquete.sh`: la cabecera dice «≈ 8–11 min» y `CONTINUIDAD.md` §2 dice «10–12 minutos»; la línea 2 sigue diciendo «entrega 4: continuidad 3.1 + piloto».
- `ANEXO_D` (cierre) conserva un tachado markdown, «~~por su contenido sin formato~~», en un texto normativo.
- `CONTINUIDAD.md` §9 se titula «en orden cronológico de la entrega que los abrió», pero 9.10–9.13 (cifras extraídas, etapa anterior, pendientes del 3-nov y L1–L4) son anteriores a 9.1 (piloto 4.1).
- `INFORME_RV1_4_9.md` §6 no lista `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` ni `VERSION` entre los archivos cambiados (remite a `CAMBIOS_ARCHIVOS.txt`, que aún no está regenerado).

**[Propuesta]** Corregir en la regeneración final.

## 2. Lo que se comprobó y está bien

**R-V1 (código y pruebas)**
- **[Hecho]** La batería `test_integridad_auditoria_v2.py` da **63/63**, con las salidas en temporales y `TMPDIR` desviado. El resultado coincide prueba a prueba con `resultados/test_integridad_auditoria_v2_salida.txt` (`/home/claude/auditoria_4_9/tmp/bateria_63_salida.txt`).
- **[Hecho]** `test_auditorias_v2.py` da **55/55** y `test_estados_v2.py` **28/28** con el código 4.9.
- **[Hecho]** `mutar_rv1.py` detecta las **15 de 15** mutaciones (`/home/claude/auditoria_4_9/tmp/mutaciones_rv1_auditor.json`).
- **[Hecho]** `comprobar_integracion_verificador_49.py` da **13 de 13**.
- **[Hecho]** La reproducción con el código 4.8.1 (24/61) y la tabla antes/después coinciden con la batería. El código conservado en `reproduccion/codigo_4_8_1/` tiene las huellas del manifiesto 4.8.1. La diferencia 61/63 se explica: el grupo G cuenta 1 prueba en lugar de 3 sin `huella_fiel`.
- **[Hecho]** Las funciones A (`huella_contenido`, sin cambios en su lógica) y B (`motivo_respuesta_no_aceptada`) están separadas. Cuando existe `auditoria_respuesta`, la vigencia solo usa B.
- **[Hecho]** `huella_fiel` cubre el texto íntegro, incluida la línea de solicitud, así que cualquier cambio de esa línea o del orden cambia la huella.
- **[Hecho]** H2 no ha cambiado: el hash de `veredicto_auditoria` es `9edf6252…`.
- **[Hecho]** Ataques que **se retiran** correctamente por las cuatro vías (paso 14, `ficha.py`, `informe.py` y `resumen.py`, en los dos destinos):
  - ZWSP, NBSP, VT y U+2028 insertados;
  - un BOM interior y un doble BOM;
  - la solicitud con caracteres de ancho completo;
  - una negación añadida.

  También se retiran sin `--desde`, y con `--desde 13` (solicitud nueva y código 10; la respuesta antigua no la responde).
- **[Hecho]** Las variantes inocuas siguen vigentes: U+037E→«;» (NFC) y BOM + NFD + CRLF + sin salto final.
- **[Hecho]** Sin `estado_pipeline.json`, con `cierre_vigente.json` de la 4.9, un cambio de la auditoría se retira.
- **[Hecho]** Un cierre de la 4.8.1 sin `fiel` solo se acredita por bytes, y uno de la 4.6.1 en CRLF se retira. Lo prueba la batería, y el código no calcula ninguna huella nueva *mientras exista* `cierre_vigente.json` (salvo en el caso de Z-1).
- **[Interpretación]** Las solicitudes duplicadas en el estado se resuelven del lado seguro: hay que manipular el estado, y una pendiente con el mismo identificador bloquea por la comprobación de pendientes.
- **[Hecho]** Expedientes históricos: el árbol, frente a `reproduccion/MANIFIESTO_4_8_1.txt`, tiene **exactamente** los 8 archivos modificados previstos, ninguno ausente, y como nuevos solo el expediente 4.9 y la batería, más `.lo_perfil/` y el manifiesto (`python3 -B /home/claude/auditoria_4_9/tmp/comparar_manifiesto_4_8_1.py`). `fase1_decisiones.json` de la referencia no ha cambiado.

**N4**
- **[Hecho]** El recuento es correcto: 38 en `fase1_v63.json → pendientes_verificacion` y 39 en el CSV. La diferencia es `('adquisiciones', 2023)` de `AR_2023.json`, cuyo `cero` se refiere a la columna 2022 («-»), mientras que 2023 tiene 254.086 (Vidroporto). Hay 28 entradas con fila y 10 auxiliares; `caja_incluye_otros_activos_financieros` = false.
- **[Hecho]** Reproducción en temporales: `n4_investigacion.py --salida/--propuestas` a `tmp/` produce `matriz_n4.csv`, `recuento_n4.json` y `propuestas_n4_sin_firmar.json` **idénticos**. `matriz_n4.json` difiere solo en la ruta del campo `efectos`. `test_n4_comprobaciones.py` da 12/12, con salida idéntica a la de referencia.
- **[Hecho] Entradas revisadas contra el texto y el PDF español** (`pdftotext`):

| Entrada | Qué se comprobó | Resultado |
|---|---|---|
| minoritarios 2025 | Balance | 1.412.878 + 901.354 = 2.314.232, en el texto y en el ES 2308 |
| minoritarios 2025 | Resultado | 209.341 = 209.341 |
| minoritarios 2025 | ESEF | Sin hechos *noncontrolling* (búsqueda sin distinguir mayúsculas) |
| minoritarios 2025 | Sociedades dependientes | Todas al 100 % |
| minoritarios 2024 | Balance | 1.309.830 + 998.342 = 2.308.172, en inglés y en español |
| minoritarios 2024 | Resultado | 298.315 = 298.315 |
| intereses 2025 | Financiación | 2.626 + 219.500 − 1.294 − 125.259 − 227.266 − 51.833 = −183.526, en inglés y en español |
| intereses 2025 | Explotación | «Pagos de intereses (20.800)» en explotación; ESEF solo `InterestPaidClassifiedAsOperatingActivities` (20.800 y 32.100) |
| intereses 2024 | Financiación | 229.495 − 31.122 − 201.931 − 233.300 − 173.938 = −410.796; intereses (32.100) en explotación |
| intereses 2023 | Financiación | 257.877 − 4.500 − 146.000 − 37.551 = 69.826 |
| intereses 2023 | Comparativa 2022 | 112.500 − 31.765 − 24.500 − 22.063 − 34.607 = −435 (la errata «112,5000» es real y está bien declarada) |
| adquisiciones 2018 | Inversión | −99.541 − 2.245 + 13 = −101.773; −86.479 − 2.541 + 246 − 235.233 = −324.007. Por la maquetación del texto, (235.233) está en la columna 2017 (Santos Barosa), y el comparativo de CF_2019 no tiene línea de adquisiciones |
| arrendamientos_principal 2018 | Nota 15, p. 57 | «Finance Lease 40,916 / -», nacido en 2018; 394.887 + 38.880 = 433.767, que es la decisión registrada de deuda 2018. Sin línea de arrendamientos en financiación (−120.363) |
| arrendamientos 2016 | Pasivos | No corrientes 406.781 y corrientes 214.528 cuadran sin arrendamientos |
| arrendamientos 2016 | Nota 3 f | Solo arrendamientos operativos; ninguna mención a un arrendamiento financiero |
| otros_activos_financieros 2024 | Activo corriente | 752.728 (y 816.395) sin inversiones financieras ni depósitos, también en el PDF español |

- **[Hecho] Clasificaciones correctas en la matriz.**
  - 35 en la clase 2: los grupos son 5 + 10 + 10 + 10, y la reserva de los 8 intereses de 2018–2025 es correcta.
  - 3 en la clase 4: es una calificación razonable bajo la regla registrada.
  - 0 en las clases 3 y 5.
- **[Hecho] Razonamiento de C48.**
  - No hay doble cómputo: C46 = 335,4 es la media del CFO de 2023–2025 y ya descuenta los intereses pagados (media 21,74).
  - Poner C48 = 21,74 restaría dos veces.
  - C52 = 335,4 − 169,7 − 0 − 4,5 = 161,2.
  - La alternativa de P3/C49 (6,764 en `fase1_v63.json` frente a 4,5 en el libro) y la hipótesis de 2,254 (media de 2.131, 2.179 y 2.452) están bien planteadas como hipótesis.
  - Las cifras de la nota 8 coinciden con el texto (movimiento del pasivo de 2025: 44.904 + 2.404 + 2.452 − 8.314 + 9.596 − 1.742 = 49.300).
- **[Hecho] Efectos.** `efectos_n4.json` es aritméticamente coherente: delta = variante − base en todas las variantes y salidas, y las huellas de las 10 copias coinciden. L26 da −0,028404 = −1/35,206. El LEEME y el campo `aviso` presentan las copias como exploratorias, sin aprobación heredada. La base reproduce 53,670 / 70,772 / 86,489, el ponderado 70,495 y el puente 160,784.
- **[Hecho] Campos humanos vacíos.** En `propuestas_n4_sin_firmar.json` (6 grupos) y en `decisiones_y_preguntas_4_9.json` (6 decisiones), `decision`, `fecha` y `confirmado_por`/`decidido_por` son `null`. Las preguntas Q-N4a y Q-ROIC1 tienen `enviada: false`.

**Documentación**
- **[Hecho]** `PRECISION_ROIC_4_9.md` es correcto:
  - las líneas 251 y 310 de `INFORME_REINVERSION_4_8_1.md` dicen lo citado;
  - `fase_b.json → palancas.roic_lp` tiene `porque`, `apoyo` y `lo_sustituiria` en los tres escenarios;
  - `fase_b.md` tiene la sección «ROIC a largo plazo (B18:D18)».
- **[Hecho]** `PROPUESTA_AUTOMATIZACION_4_9.md` está marcada como no activada y no cambia el contrato.
- **[Hecho]** `DECISIONES.md` (entrada del 11-nov), `VERSION` y `CONTINUIDAD.md` §1, §5 y §9.8 son coherentes en cifras con los informes (38, 35/8, 3, 0, −0,0284, 63, 15) y con la matriz. La numeración de §4 y §9 es correlativa.

## 3. Lo que no se pudo comprobar

- **No se ejecutó nada con LibreOffice por decisión propia:** `efectos_n4.py` (los recálculos), `verificar_paquete.sh`, `test_pipeline_sintetico.py`, `comprobar_entrega_4_9.py`, `test_resumen_v2.py`, `test_cierre_v2.py` ni los controles históricos.
  - Los valores de `efectos_n4.json` se aceptan como registrados; solo se revisó su aritmética y sus copias. `f` y el precio de Sí se derivaron a mano (Z-6).
  - Excepción involuntaria: `test_estados_v2.py`, permitido por el encargo, usa LibreOffice (Z-9).
- **Contraste parcial:** las entradas N4 de 2017–2022, distintas de las pedidas, solo se revisaron a través de los bloques que reproduce la matriz y de sus sumas; no se abrieron sus PDF.
- **Sin acceso:** las versiones españolas de 2017–2023, porque no están en el paquete.
- **Sin efecto en un paquete:** no se verificó cómo quedaría el ZIP final (manifiesto y `CAMBIOS_ARCHIVOS.txt` sin regenerar).

## 4. Tabla resumen

| Id | Gravedad | Título |
|---|---|---|
| Z-1 | BLOQUEANTE | Sin `cierre_vigente.json`, `ficha.py` vuelve a cerrar con cualquier APROBADO del material y le atribuye la huella actual. Lo dan por vigente las cuatro vías. Es anterior a la 4.9 |
| Z-2 | BLOQUEANTE (fallo ruidoso, código 1) | Un `auditoria.md` no UTF-8 o un archivo de control ilegible rompe las cinco vías y la aprobación sigue publicada; la rama «no es UTF-8» es inalcanzable |
| Z-3 | IMPORTANTE | La batería no fija los límites de las transformaciones inocuas (NFKC, Cf, NBSP, separadores) ni la rama de huella fiel sin estado; tampoco tiene casos para Z-1 y Z-2 |
| Z-4 | IMPORTANTE | Las comprobaciones N4 no usan la cita, la comparativa ni la unidad para clasificar; la clase 4 está fijada en el código; la errata no distingue columna; 15 de 16 falsos positivos sintéticos por rótulo |
| Z-5 | IMPORTANTE | Las decisiones de 2017–2018 se llaman «precedentes humanos» sin fecha ni firma ni autoría constatada |
| Z-6 | MENOR | `f`, el paso REVISAR→PASA y el precio de Sí no están en las salidas reproducibles (son correctos, derivados a mano) |
| Z-7 | MENOR | Faltan contrastes españoles de 2023 y de `otros_activos` 2024–2025; textos de plantilla anacrónicos; falta citar la tabla de dependientes y la discrepancia de la nota 8 |
| Z-8 | MENOR | Remisiones a `REGISTRO_ENTREGA_4.9.md`, `LEEME_BATERIAS_HISTORICAS.md`, `comprobar_entrega_4_9_salida.txt` y `AUDITORIA_INTERNA_4_9*.md`, que no existen |
| Z-9 | MENOR | §2 incompleto: los comandos documentados sobrescriben salidas en el árbol y escriben `__pycache__`; `.pyc` en el material; `test_estados_v2.py` usa LibreOffice; `.lo_perfil/` en el árbol |
| Z-10 | MENOR | Forma: comas en el mensaje de arranque, duración y cabecera del verificador, tachado en `ANEXO_D`, orden de §9 y lista de archivos de `INFORME_RV1_4_9.md` |

Scripts del auditor (todos en `/home/claude/auditoria_4_9/tmp/`):
- `ataques_rv1.py` (subcomandos `mutaciones`, `otras_vias`, `461_sin_cv`, `sin_estado_ni_cv`, `sin_estado_ni_cv_pipeline`, `sin_estado` e `ilegibles`);
- `ataque_46.py`;
- `mutar_extra.py`;
- `engano_n4.py`;
- `comprobar_f_c48.py`;
- `comparar_manifiesto_4_8_1.py`;
- `codigo481/`, el árbol con el código 4.8.1 para reproducir.
