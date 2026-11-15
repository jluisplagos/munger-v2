# Revisión independiente del hito 2 de la 4.15 (candidata c2d2b96)

Revisor: Fable (Claude, contexto separado del autor del cambio; no es una revisión humana ni sustituye a la externa) · 15-nov-2026.
Convención: **[Hecho]** = comprobado por el revisor ejecutando o leyendo (se dice cuál); **[Interpretación]** = lectura del revisor; **[Propuesta]** = corrección sugerida. Lo que no se ha ejecutado se dice expresamente.
El sistema es experimental y supervisado. Nada de lo que sigue acredita aptitud para dinero real, ni esta revisión tampoco.

## 0. Qué se ha revisado y cómo

- **Material:** el árbol congelado `rev_hito2/munger_v2_r1` (commit c2d2b96, manifiesto de 7031 entradas; la rama ha seguido avanzando después —`c0dcbd0` al escribir esto— y esos cambios no se han revisado) y `DIFF_HITO1_A_CANDIDATA.diff` (1328 líneas, leído entero). Archivos cambiados: `scripts/{verificacion_entradas,fase1_historia,ficha,informe,cierre_v2,pipeline}.py`, `esquema/ficha.esquema.json`, `pruebas/{test_verificacion_entradas_415,test_entrada_efectiva_415}.py`, `pruebas/test_relevo_i19_415.py` (nuevo), `verificar_paquete.sh` y `configuracion/cambio_elis_c48_4_15.json`. `verificacion_entradas.py` se ha leído entero (1491 líneas); de los demás, lo cambiado y lo que lo rodea.
- **Encargo leído en el original:** `docs/revision_externa_4_15_hito1/REVISION.md` y `PROMPT_PARA_CLAUDE.md`, la cuarta pasada (`REVISION_FABLE_HITO1_CUARTA.md` y sus sondas `r1`, `r2`, `r4`, `r6`, `r8`), `INCIDENCIAS_4_14.md` (I19, I20) y `HITO_1_4_15.md`.
- **[Hecho] El árbol congelado no se ha modificado.** Huella SHA-256 de sus 7085 archivos al empezar (`fable/huellas_arbol_congelado_inicio.txt`) y al terminar (`fable/huellas_arbol_congelado_fin.txt`): idénticas (§8). Todo se ejecutó en copias propias: `fable/copia/` (candidata), `fable/copia_hito1/` (la misma con los archivos de `reproduccion/codigo_4_15_hito1/`, para comparar) y árboles ligeros `fable/mut*/` (mutaciones). `/home/user/munger-v2` solo se ha leído.
- **[Hecho] No se ha lanzado LibreOffice ni `pipeline.py`.** Todas las sondas llevan delante en el `PATH` un sustituto de `soffice` que registra el intento y termina con 1 (`fable/bin/soffice`); no hubo ningún intento (`fable/salidas/INTENTOS_SOFFICE.log` no existe). No se han ejecutado `test_relevo_i19_415.py`, `test_pipeline_sintetico.py`, `test_integracion_v64.py`, `test_auditorias_v2.py`, `verificar_paquete.sh` ni la reconstrucción de C48. Sí `ficha.py` e `informe.py --provisional` sobre copias (como hace la batería), `pdftotext` y las tres baterías permitidas.
- **Sondas y salidas:** `fable/sondas/*.py` y `fable/salidas/*.log` (índice en §9). Uso: `cd fable/sondas && python3 -I -B sNN_….py`; con `PV=<copia>/personaje_v2` se ejecutan contra otro código (así se hicieron las comparaciones con el hito 1). Trabajan en `fable/tmp/` y no escriben en ningún árbol.
- **Datos reales y sintéticos:** donde dice «real» se han leído los registros `verificacion_entradas.json` y las fuentes de los expedientes de la 4.14; lo demás es el fixture sintético de la batería (copia de Viscofan 4.13 con registro y vínculos escritos por el arnés). Los contraejemplos sintéticos demuestran lo que el control no detecta, no que los registros reales lo hagan: **no lo hacen** (§2).

## 1. Dictamen

**ACEPTABLE CON CORRECCIONES.** Una corrección es importante y condiciona dar por cerrado R415-SIGNO (y, con él, R3); otra importante afecta a las pruebas. El resto son menores u observaciones.

- **[Hecho]** Las tres baterías permitidas pasan en la copia: 141/141, 52/52 y 33/33. El contraejemplo literal de la revisión externa ya no pasa. Los registros reales no cambian de estado con las reglas nuevas (diagnóstico idéntico al del hito 1 y al entregado). C48 de Elis sigue en 108,0 con los mismos términos. Las baterías del hito 1, sin tocar, pasan con el código del hito 2 (105/105 y 40/40).
- **[Hecho] H1 (importante).** El signo y la «cifra completa» se leen dentro de la cita, no en la página. Con la misma página del contraejemplo externo («-849697.000»), basta que la cita sea solo la cifra para que la entrada vuelva a quedar `apto_por_entradas=True` y comprobada. La sonda de la revisión externa, con una línea cambiada, lo reproduce. Lo mismo en `calcular_entrada`: el cálculo del hito 1 de C48 (130,8 frente a «(130,8)») se acepta sin declarar la conversión si cada cita se recorta a la cifra. Y una cita cortada dentro de un número acredita 849.697 donde la página publica 8.496.970, o un cero donde publica 0,49 (la cita cortada dentro de un número ya se aceptaba en el hito 1: no es una regresión, es el mismo hueco).
- **[Hecho] H2 (importante, pruebas).** La línea nueva de I20 trae las mismas frases que buscaban las pruebas del párrafo de aptitud de la V6.4. Un informe V6.4 cuyo párrafo de aptitud dijera «Apta para dinero real: sí» pasa hoy las dos baterías (141/141 y 33/33). Con el código y las pruebas del hito 1, la misma mutación se detectaba (§4).
- **[Interpretación]** Lo demás hace lo que declara, con los residuos de §3. H1 exige cambiar `verificacion_entradas.py` y `fase1_historia.py`: la regresión completa tendrá que repetirse sobre la candidata corregida. A juicio del revisor, con H1 y H2 corregidos y sus contraejemplos en las baterías, basta una revisión acotada de ese cambio.

## 2. Lo comprobado que está bien

| Punto | [Hecho] | Sonda / salida |
|---|---|---|
| Baterías | 141/141 (260 s), 52/52 (40 s), 33/33 (52 s), código 0; ningún intento de lanzar LibreOffice | `salidas/bateria_*.log`, `salidas/baterias_rc.txt` |
| Pruebas existentes | Las baterías del hito 1 (105 y 40 pruebas), sin tocar salvo la aserción de R3 que el hito 2 cambia a propósito, pasan con el código del hito 2: 105/105 y 40/40. El diff de las pruebas solo añade casos y cambia esa aserción | `s20`, `salidas/s20_….log` |
| Aserción cambiada de R3 | Es correcta: «(149,5)» valía para +149,5, que es justo lo que la revisión externa señaló como defecto. Ahora vale para −149,5 y se comprueba que no vale para +149,5 | diff, `test_verificacion_entradas_415.py:294-298` |
| Contraejemplo externo | La sonda original de la revisión externa, sobre la candidata: `apto_por_entradas=False`, discrepancia «R415-SIGNO»; `_cita_contiene` da False en los tres casos de signo | `externa_sondas_independientes_ORIGINAL.py`, `salidas/externa_sondas_original_sobre_candidata.json` |
| Registros reales | Diagnóstico (`diagnostico_registros_4_14.py`) con el código del hito 2 y con el del hito 1: idénticos entre sí y a los entregados (214/232, 207/226, 175/193; mismos errores y discrepancias, texto incluido) | `salidas/diagnostico_reales_codigo_hito{1,2}.json` |
| Signo en los registros reales | 1.410 entradas numéricas con fuente de texto en seis expedientes: 460 negativas, 918 positivas y 32 ceros, todas «ok». En ninguna el contexto de la página alrededor de la cita cambia la lectura, ninguna cita empieza o acaba dentro de una cifra, ninguna tiene una aparición indeterminada. El inventario del autor se reproduce | `s3`, `salidas/s3_….log` |
| Transformación en los registros reales | valor_fuente negativo con signo −1 en 59, 50 y 43 entradas (Elis, Vidrala, Viscofan), todas con un «tratamiento» que explica la conversión; ninguna con «ninguno» | `s3d` |
| Auxiliares | Un auxiliar (`aux:`) se contrasta con su signo igual que una celda | `s11` F |
| C48 de Elis | 108,0 con la carpeta del expediente; operación, años, términos, redondeo y decisión idénticos al hito 1; los tres componentes solo añaden `valor_fuente` (−130,8, −150,8, −177,9), `signo` −1 y `tratamiento`; el cálculo del hito 1 tal cual se rechaza con diagnóstico. No se ha repetido la reconstrucción con LibreOffice: los ocho JSON del autor (`hito2/resultados/reconstruccion_c48_tras_signo/`) dicen 108 → 108 con y sin valores migrados y diferencia 0 en el precio de Sí | `s13`, `s2` C1 y C4 |
| U2 | `_importe_libro_exacto` equivale a «el libro es el exacto o uno de sus redondeos a 3 decimales con cualquier regla de empate». En 200.000 pares: lo que el hito 2 acepta y el hito 1 rechazaba son 27.100 casos, todos empates exactos (distancia 0,0005); el hito 2 no rechaza nada que el hito 1 aceptara, salvo un libro con ruido binario (849.6970000000001). No es una tolerancia general | `s5` |
| U3 | Fórmulas dentro y fuera de los límites, anidamientos, literales enormes, potencias, lambdas, atributos: error controlado o resultado en menos de 0,02 s. `comprobar` no se cuelga | `s6` A |
| U4 | Los casos declarados se aceptan también en el registro (origen −1, producto por un cero, 0 / d, argumento menor de un max, max(…, 0) con el suelo inactivo); `o[x] * 0 + c`, `o[x] − o[x] + o[y]` y `min(o[x], 12)` siguen rechazados | `s6` B, `s16` |
| U1 | Los derivados comprobados se cuentan y se listan en el resultado y en el resumen | `s16` 3 y 5 |
| U5 | Los casos de la cuarta pasada están corregidos. En las dos fuentes HTML reales de Elis, los 46 bloques con cifras se encuentran en el texto visible (los 2 que no, son un artefacto de la referencia del revisor con `<br>`). El mismo resultado con Python 3.13.18, 3.12.3 y 3.11.18 salvo un caso | `s7`, `s7b`, `s8` |
| I20 | La ficha y el informe V6.3 y V6.4.1 llevan el bloque y validan su esquema; las fichas oficiales de la 4.14 siguen validando; `verificacion_entradas.apto_para_dinero_real = true` no valida; `verify_quotes_v2.py` pasa sobre los informes generados | `s9` |
| Material | Añadir `entrada_efectiva.json` a `MATERIAL_FIJO` no cambia el identificador del material de ninguno de los 30 expedientes del árbol con material fijado (ninguno tiene ese archivo) | `s4` |
| I19 (lectura) | Tres expedientes reales esperan la auditoría con el material fijado distinto del vigente (`elis_motor_A/Elis`, `vidrala/Vidrala`, `viscofan/Viscofan`; cambia `verificacion_entradas.json`): el paso 13 nuevo los detectaría. Por lectura: una respuesta a la solicitud antigua no se acepta, las solicitudes no se borran (quedan «sustituida») y no hay vuelta al paso 12 en un relanzamiento sin cambios | `s10`; `pipeline.py:1016-1033`, `:331-370`, `:380-447` |
| Manifiesto | Las 7031 entradas coinciden con el árbol: 0 ausentes, 0 distintas | `salidas/s12_….log`, §0 |

## 3. Hallazgos

### H1 · IMPORTANTE · R415-SIGNO y R3 se burlan recortando la cita: la cifra y su signo se leen dentro de la cita, no en la página

`verificacion_entradas.py:948-951` (la cita se busca en la página como subcadena), `:468-476` (`_pasaje_en_pagina`), `:491-499` (el texto examinado es solo el pasaje; los límites de «cifra completa» y `_signo_en_cita` se evalúan en él), `:986-996`; `fase1_historia.py:403-410`.

- **[Hecho]** `s2b_externa_variante_cita_recortada.py` es la sonda de la revisión externa con una línea cambiada: la página conservada sigue publicando «Partida sintética de Historia!F6: -849697.000», y la cita es «849697.000». Resultado: `apto_por_entradas: True`, `checked_cell: True`, con `valor_fuente` 849697, signo 1 y tratamiento «ninguno». La sonda original, sin cambiar, da `False`.
- **[Hecho]** `s2_cita_recortada.py`, registro sintético completo: B1 página «…: -849697.000» y cita «849697.000»; B2 página «…: (849,697.000)» y cita «849,697.000»; B3 cita «849,697.000) (1.000)»; B4 página con «−» Unicode. Las cuatro: `apto=True comprobadas=321/321`. El sentido inverso (página positiva, valor_fuente negativo) sí se rechaza.
- **[Hecho]** `s2` C2, con los componentes reales de C48: el cálculo del **hito 1** (130,8 / 150,8 / 177,9 positivos, sin `valor_fuente`, `signo` ni `tratamiento`) con cada cita recortada a la cifra («130,8», «150.8», «177.9») → `ACEPTADO valor=108.0`. Sin recortar → error «signo_distinto». La conversión de un pago publicado entre paréntesis vuelve a poder pasar sin declararse.
- **[Hecho]** `s14_r3_cita_cortada.py` (la cita cortada dentro de un número): la página publica 8496970 y la cita «…: 849697» → APTA y comprobada con valor_fuente 849697; página 1849697.000 y cita «849697.000» → apta; página 849697.499 y cita cortada en el punto → apta; página «849.697.123» y cita «…849.697» → apta; cero comprobado con página «Partida: 0.49» y cita «Partida: 0» → apta; cero comprobado con página «Ejercicio 2019» y cita «0» → apta. Con el código del hito 1 pasa lo mismo: **no es una regresión**, pero deja sin efecto la garantía de R3 («0,49 no es 0», «el 0 de 2019») que la revisión externa dio por verificada con citas completas.
- **[Hecho]** Mecanismos emparentados (`s11`): si la cita aparece dos veces en la página, se lee la primera (C1: primera aparición con el guion en otra columna y segunda con el guion a un espacio → apta; al revés → pendiente). Si el pasaje no se localiza con `re.I` pero la cita normalizada sí está en la página, el signo se lee en la cita con los espacios que escribió el extractor (D1: página «İmporte - 849697.000», cita «i̇mporte -  849697.000» con dos espacios → apta; con la cita literal → pendiente).
- **[Hecho]** Ningún registro real lo usa (`s3`: 0 entradas donde el contexto cambie la lectura, 0 citas cortadas dentro de una cifra).
- **Causa.** `_norm_txt(cita) in _norm_txt(pag)` es una búsqueda de subcadena. Después, `_cita_cifra` toma como texto el pasaje de la página que casa con la cita y nada más: una marca de signo pegada por fuera («(», «-», «−») o el resto de un número no entran en lo que se examina.
- **[Interpretación]** Es el mismo defecto que R415-SIGNO con una variación de una línea, y puede ocurrir sin intención: un extractor que cita solo la cifra. Mientras siga abierto no puede declararse que «la cita se contrasta con su signo» ni que la cifra es «completa».
- **[Propuesta]** (1) Leer la cifra y su signo en la página, en la línea donde está el pasaje: los límites de cifra completa y `_signo_en_cita` sobre la línea, para las apariciones de la cifra que caen dentro del pasaje. (2) Considerar todas las apariciones de la cita; lecturas distintas → pendiente. (3) Pasaje no localizado → pendiente; no leer el signo en la cita. (4) La misma función en `calcular_entrada`. (5) Contraejemplos en las baterías: la variante de la sonda externa, «150,8» frente a «(150,8)» en C48, 8496970/849697, 0.49/0, dos apariciones. `s15_propuesta_contexto_pagina.py` es un boceto de apoyo (no una implementación revisada): rechaza los 13 contraejemplos, da la misma categoría que la candidata en las 32 formas de la batería SG y **no cambia ninguna de las 1.410 entradas numéricas reales**.

### H2 · IMPORTANTE (pruebas) · Las pruebas existentes del párrafo de aptitud quedan rebajadas de hecho por la línea nueva de I20

`informe.py:209-216` (línea nueva) frente a `test_verificacion_entradas_414.py:267-274` y `test_verificacion_entradas_415.py:907-913`.

- **[Hecho]** La línea de I20 se añade en todas las plantillas y contiene «apta por entradas: sí/no» y «Apta para dinero real: no.». Las pruebas del párrafo de aptitud de la V6.4 comprueban solo que esas subcadenas están en el informe (`"apta por entradas: no" in inf and "Apta para dinero real: no" in inf`).
- **[Hecho]** Mutación `m39` (el párrafo de aptitud de la V6.4 dice «Apta para dinero real: sí»): candidata → 33/33 y 141/141, **no detectada**. `m40` (ese párrafo dice siempre «apta por entradas: sí»): **no detectada**. Las mismas mutaciones sobre el código y las pruebas del hito 1: `m39` detectada (entradas 4.14: 31/33, fallan 2; entradas 4.15: 105/105); `m40` detectada (entradas 4.14: 32/33, fallan 1; entradas 4.15: 104/105, fallan 1).
- **[Hecho]** `m37` (la línea nueva de I20 dice «Apta para dinero real: sí» cuando el registro es apto por entradas): **no detectada** (entrada efectiva: 52/52; entradas 4.15: 141/141; entradas 4.14: 33/33). Ninguna prueba comprueba la frase de la línea nueva con un registro apto. Con las tres mutaciones a la vista: en la candidata, cualquiera de las dos frases puede decir «sí» mientras la otra diga «no».
- **[Interpretación]** El código es correcto: los dos textos dicen «no». Lo que se pierde es la capacidad de las baterías de detectar una regresión en la frase que protege la regla central del proyecto. El encargo pide «mantén sin rebajar las pruebas existentes».
- **[Propuesta]** Comprobar la ausencia de «Apta para dinero real: sí» en todo el informe, contar las apariciones de cada frase (una por bloque) y comprobar cada bloque por separado (la línea de I20 y el párrafo de aptitud).

### H3 · MENOR · Un menos separado de su cifra por dos o más espacios se lee como «otra columna»: la cifra negativa se acredita como positiva

`verificacion_entradas.py:462-463`, `:465`, `:494`.

- **[Hecho]** `s21_signo_formatos.py` (28 formas de imprimir un número con signo conocido × 4 escrituras × 3 contextos): 19 formas se leen bien en las 12 combinaciones; 5 quedan pendientes en falso; **4 aceptan el signo contrario**: «-     n», «−     n», «-€    n» y «(EUR n)».
- **[Hecho]** `s11` A, registro completo, valor_fuente positivo, signo 1: página «…:   -          849,697.000 €» (formato de contabilidad de una hoja de cálculo en configuración europea: el menos a la izquierda de la celda y la cifra a la derecha) → apta; «-£   849,697.000» → apta; «−  849 697,000» (menos Unicode a dos espacios) → apta. Declarar lo que publica la página (valor_fuente negativo, signo −1) da **discrepancia** en falso. Con esa misma página, un cero comprobado también pasa («cero impreso como guion», `s1b`).
- **[Hecho]** La regla tiene uso real y legítimo: 7 entradas de los registros de Vidrala y Viscofan toman su signo positivo de ella, y en las siete el guion es de verdad el cero de otra columna (`s3b`, `s3e`). En las páginas citadas hay 41, 145 y 59 apariciones de «guion + 2 o más espacios + cifra».
- **[Interpretación]** Que el guion sea un cero de otra columna o un menos alineado a la izquierda no se puede saber sin la geometría de la tabla. La regla acierta en los registros reales, pero es una suposición, y el encargo pedía dejar pendiente lo que no pueda determinarse.
- **[Propuesta]** Declarar el límite en el docstring. Listar en el resultado las entradas cuyo signo sale de esta regla (como `derivados_comprobados`), para que el revisor independiente las mire: son pocas. Tratar como indeterminado el caso con un símbolo de moneda entre el guion y los espacios («-£   …», «- €   …») y el menos Unicode a dos o más espacios.

### H4 · MENOR · El menos Unicode «−» sí se usa para imprimir un cero en una fuente real

`verificacion_entradas.py:428` («siempre un signo menos (no se usa para imprimir un cero)»), `:455-456`, `:494`.

- **[Hecho]** `s3c`: `Elis - 2017 Registration Document.txt`, página 228: «Net gains on site disposals … −                 42.2». El «−» (U+2212) es el cero de una columna.
- **[Hecho]** `s11` E1: un cero comprobado cuya página imprime «−» → **discrepancia** en falso («la cita no contiene el valor de la fuente 0»); con guion ASCII → apta. (El patrón del cero solo admite `-`, `–`, `—`; ya era así en el hito 1.)
- **[Hecho]** `s11` A5 y A6: «… − 849697.000» (menos Unicode a un espacio) se lee como negativo sin duda: apta con valor_fuente negativo y discrepancia con positivo. Con el guion ASCII, el mismo caso es «indeterminado» (pendiente). En una tabla estrecha donde «−» sea el cero de la columna anterior, una cifra positiva se acreditaría como negativa.
- **[Hecho]** Ninguna entrada real cae en esto.
- **[Propuesta]** Tratar «−» como los demás guiones en el patrón del cero y en la regla de un espacio (indeterminado), y corregir el comentario.

### H5 · MENOR · Formatos legítimos que quedan pendientes o se leen con el signo contrario

`verificacion_entradas.py:433-465`. Sondas `s1`, `s1b`, `s11` B, `s21`.

- **[Hecho] Se aceptan con el signo que la cita no publica:** «(EUR 849,697.000)» (negativo contable con el código de moneda dentro del paréntesis) → apta como positivo (`s11` B1); «(4 573,7)» y «-4 573,7» valen para +573,7 (el límite declarado de «4 573,7» alcanza ahora al signo); una llamada de nota «(3)» vale para −3; «[149,5]», «<149,5>» y «±149,5» se leen como positivos; con una aparición con el signo correcto y otra indeterminada, vale («Importe 149,5 - 149,5» para +149,5).
- **[Hecho] Quedan pendientes o en discrepancia en falso:** negativos «(3,2 %)», «(3.2%)», «(149.5m)», «(849,697.000 m)», «(-149,5)», «$-149.5», «(1)-149,5» y «149,5-» (este último, a propósito); positivos en un inciso «(12,5 % de las ventas)» o «(149,5 millones)»; años en una fecha o un intervalo: «31-12-2024», «31-dic-2024», «FY 2023-2024», «2-3 %».
- **[Hecho]** Ninguna de las 1.410 entradas reales está en estos casos. Los rechazos van en el sentido seguro.
- **[Propuesta]** Admitir dentro del paréntesis una unidad o un «%» detrás de la cifra y un código de moneda delante; admitir «$-» y «(-…)»; no tratar como signo el guion de una fecha. Lo demás, declararlo.

### H6 · MENOR · U4: el veredicto de la sensibilidad «estructural» depende de cómo se escriba la fórmula, y `max(a − b, 0)` se rechaza justo cuando el suelo actúa

`verificacion_entradas.py:647-682` (semilla `f"{semilla}|{formula}"`, 3 puntos, perturbación solo hacia arriba), `:1234-1236`.

- **[Hecho]** `s17_u4_semilla.py`, 2.000 escrituras equivalentes de cada fórmula (cambia el nombre de los orígenes): `max(a, b)` con b el menor se declara con orígenes inertes en el 3,0 %; `min(a, b)` con b el mayor, 12,9 %; `max(a − b, c − d)`, 12,2 %; `max(a, b, c)`, 16,9 %; `min(max(a, b), c)`, 47,5 %. La misma fórmula `max(o["aux:p1"], o["aux:p2"])` pasa con 1 a 29 espacios tras la coma y falla con 30. Los controles (`a × z` con z = 0; `0 / d`) no fallan nunca.
- **[Hecho]** `s6` B y `s16` 1: `max(o[a] − o[b], 0)` con a < b (resultado 0: el caso para el que se escribe la fórmula) → error «constante en ese punto». Igual `min(o[a], 0)` con a > 0 y el producto de dos ceros comprobados.
- **[Hecho]** Ningún derivado real usa `abs`, `min`, `max`, `sum` ni `round` (`s18`: 148 derivados, 0 afectados; reproducen lo mismo con las reglas del hito 1 y del hito 2).
- **Causa.** Tres puntos al azar y una perturbación siempre positiva: en `min(a, b)`, b solo «influye» si en el punto generado b < a (probabilidad ½ por punto).
- **[Propuesta]** Perturbar en los dos sentidos y con más puntos (con 16, la probabilidad de un falso «inerte» es despreciable), y semilla que no dependa de los espacios; aceptar «constante en el punto real» cuando el valor sale de una constante exenta de min/max (el 0) y los orígenes influyen estructuralmente. Añadir un caso de `min` y uno con el suelo activo.

### H7 · MENOR · U5: «texto visible» promete más de lo que hace, rechaza HTML legítimo y el tipo PDF se decide por «%PDF-» en cualquier sitio del primer kilobyte

`verificacion_entradas.py:753-855`, `:764-791`, `:866`.

- **[Hecho] Se da por visible lo que un navegador no muestra** (`s7` A): texto oculto por una clase CSS (hoja en `<style>`), `font-size:0`, `opacity:0`, fuera de pantalla, `display:/**/none`, clase `sr-only`; `<details>` cerrado, `<dialog>`, contenido alternativo de `<canvas>`, `<video>`, `<noembed>`, `<noframes>`, `<rp>`; sintaxis autocerrada en elementos que no son vacíos (`<div hidden/>`, `<script/>`, `<title/>`: en HTML la barra se ignora); un `</div>` dentro de una celda que no cierra el `div` oculto exterior; `<script><!-- <script> </script> CITA --></script>` (`s7b`); y codecs que solo existen en Python: `charset=unicode_escape` y `charset=utf-7` hacen «visible» una cifra que el archivo no muestra (C5, C6).
- **[Hecho] Se rechaza lo que un navegador muestra** (`s7` B, C): un documento sin `</head>` (cierre opcional en HTML5) → todo el cuerpo queda oculto y la entrada en **discrepancia**; `<p hidden>…<p>` y `<li hidden>…<li>` (cierre implícito); `aria-hidden="true"` (se ve en pantalla); iXBRL con el paréntesis fuera de la etiqueta, `(<ix:nonFraction>849.697</ix:nonFraction>)` → «( 849.697 )», que no es «(849.697)» (es la forma de los informes ESEF); etiquetas en línea que no están en la lista (`<ins>`, `<label>`, `<big>`, `<tt>`) parten una palabra; `&shy;` y el espacio de ancho cero; ISO-8859-1 declarado con bytes de windows-1252 (–, €: los navegadores leen esa etiqueta como windows-1252); UTF-16 sin BOM (es UTF-8 válido con NUL: discrepancia, no «pendiente»); `<meta charset>` dentro de un comentario; «charset=» en el contenido de otra meta; un byte inválido suelto en un UTF-8 declarado (pendiente); `charset=rot13` → `LookupError`, que `comprobar` recoge como «entrada mal formada».
- **[Hecho]** `s19`: un HTML legítimo que menciona «%PDF-» en su primer kilobyte se trata como PDF → **discrepancia** («pdftotext no puede extraer la página»); un texto conservado `.txt` cuya primera página lo menciona → pendiente. Con el código del hito 1 los dos se comprobaban. A cambio, el PDF con bytes previos y sin extensión ya se contrasta (lo que se buscaba).
- **[Hecho]** Ningún registro real cita un HTML, y las dos fuentes HTML reales no dan rechazos (`s8`).
- **[Propuesta]** Decir en el docstring que «visible» es «fuera de las construcciones listadas», no lo que resulta de las hojas de estilo. Cerrar `head` al llegar `<body>` o el primer elemento de contenido, y el `<p>`/`<li>` anterior al abrirse otro. Tratar como en línea las etiquetas desconocidas con prefijo (`ix:`) o comparar también sin espacios alrededor de paréntesis y «%». Admitir solo codificaciones de la lista WHATWG y leer «iso-8859-1» como windows-1252. Para `.txt`, `.htm` y `.html`, exigir la cabecera `%PDF-` al principio.

### H8 · MENOR · I20: el informe V6.3 no dice lo que no se contrastó, y el motivo se corta

`informe.py:209-216`.

- **[Hecho]** `s9` B, V6.3 (copia de Elis) con un registro sintético apto que tiene 1 derivado sin fuente (`o["Historia!F5"] - (5*100 + 6*1 + 2/10)`), 2 entradas de juicio no materiales, 1 lectura externa sin bytes y 11 no aplicables. La ficha lo lleva en `verificacion_entradas.resumen`. El informe dice solo: «apta por entradas: sí (291 de 292 celdas del universo comprobadas). Entrada efectiva: … Apta para dinero real: no.» No menciona derivados, no materiales, lecturas externas ni no aplicables. En la V6.4 el párrafo de aptitud sí los da (N1, N2 y U1).
- **[Hecho]** `s9` A: con el registro no apto, el motivo se corta a 300 caracteres a mitad de palabra («…(0 sin el juicio de materiali.») y se pierden los recuentos del final: entradas materiales sin comprobar, desactualizadas, discrepancias, errores y sin entrada.
- **[Interpretación]** La mitigación de U1 («se cuentan y se listan: resumen, ficha e informe») no llega al informe V6.3. Con U1 abierto por diseño (H12), es donde más falta hace.
- **[Propuesta]** Que la línea de I20 use el mismo detalle que el párrafo de la V6.4 (o el texto de `resumen`), sin cortar a mitad de frase.

### H9 · MENOR · I20 e I19: un modo aplicado distinto del declarado se muestra pero no detiene nada, y el relevo vuelve siempre al paso 12

`ficha.py:80-83`, `informe.py:215`, `pipeline.py:616-622` (el modo solo se aplica en el paso 2), `:1030` (el relevo fija `paso = 12`).

- **[Hecho]** `s9` C: con `estado_pipeline.json → entrada_efectiva` «estricta» y `entrada_efectiva.json` «registrada» con motivo, la ficha da `coinciden: False` y el informe lo avisa, pero `apto_por_entradas` sigue en `True` y el esquema valida. Con la declaración ilegible, lo mismo. Ningún control consulta `coinciden` (solo `ficha.py:83` e `informe.py:215`).
- **[Hecho, por lectura; no ejecutado]** Con I19, cualquier cambio del material mientras se espera la auditoría lleva al paso 12. Si lo que cambió es `entrada_efectiva.json`, el modo nuevo no se aplica al libro (eso es el paso 2) y se pide la auditoría de un material cuyo modo declarado no es el aplicado. Si cambió `fase_c.json`, `fase_b.json` o `alcance_v2.json`, el paso 12 repite esquemas, celdas, gramática y citas (`verificar_todo.sh`), pero no la coherencia de la fase C del paso 10 ni el paso 11; el estado propuesto sigue siendo el que fijó el paso 11 con la fase C anterior. `reaplicar_configuracion` (4.11) sí vuelve «al primer paso que depende» del archivo cambiado.
- **[Hecho, por lectura]** `relevos_caducados` queda en `estado_pipeline.json` y en el registro; ni el prompt de la auditoría ni la ficha ni el informe dicen que el material cambió durante la espera ni qué archivos.
- **[Interpretación]** No abre nada que `--desde 12` no permitiera ya; lo hace sin que nadie lo pida. La comprobación de entradas no reproducibles protege el caso de C48 con cualquier modo.
- **[Propuesta]** En el relevo, mirar `archivos_cambiados`: si hay algo que no produce el paso 12 o el 13, volver al paso que lo produce (2 para `entrada_efectiva.json`) o detenerse con un diagnóstico que pida `--desde N`. Tratar `coinciden: False` o una declaración con error como motivo para no fijar el material. Dar al auditor la lista de archivos cambiados.

### H10 · MENOR · C48: el texto de «fuente» se corta a 1500 caracteres y pierde la fuente y la página del componente de 2025

`fase1_historia.py:424` (`[:1500]`).

- **[Hecho]** `s13`: con el CAMBIO del hito 2, el texto antes de la decisión mide exactamente 1500 y termina en «…(4.15, hito 2, R415-SIGNO: conversión». Faltan el final del tratamiento de 2025, «(texto/Elis - 2025 Universal Registration Document.txt p.327)» y el término «2025 arrendamientos_principal (Historia) …». Con el CAMBIO del hito 1 medía 1195 y estaba entero.
- **[Hecho]** El corte está también en el resultado del autor: `hito2/resultados/reconstruccion_c48_tras_signo/3_elis_4_15_construir.json` contiene «…R415-SIGNO: conversión. Tratamiento del inversor del 10-nov-2026…».
- **[Interpretación]** El valor (108,0) y el `calculo` estructurado están completos; lo que queda incompleto es el texto que va a la evidencia documental del expediente regenerado.
- **[Propuesta]** No cortar antes de listar todos los términos (el tratamiento, una vez; por componente, «= −1 × −130,8 publicado») y una prueba de que el texto nombra la fuente y la página de cada componente.

### H11 · MENOR · Pruebas: lo que las baterías no distinguen

- **[Hecho]** Mutaciones (§4). No detectadas además de las de H2: `m12` (tolerancia de importes ampliada a 0,00055); `m15` (el dato publicado vuelve a la comparación del hito 1 (_igual_libro con floats)); `m16` (sin límite de nodos de la fórmula); `m17` (sin límite de longitud de la fórmula); `m20` (se quita el error «constante en el punto real» (not locales)); `m22` (el 0 queda exento en cualquier posición de la fórmula, no solo en min/max); `m25` (el atributo `hidden` deja de ocultar el elemento (display:none, visibility:hidden y aria-hidden siguen ocultando)); `m29` (el tipo PDF vuelve a exigir la cabecera al principio (como en el hito 1)); `m31` (la ficha dice siempre apto_por_entradas = false); `m33` (el informe no avisa de que el modo aplicado no coincide con el declarado); `m47` (el informe V6.4 no dice cuántos derivados comprobados hay).
- **[Hecho]** No hay ningún caso para: la cita recortada (H1), en `verificacion_entradas` ni en `calcular_entrada`; el aviso de que el modo aplicado no coincide (la aserción de `test_entrada_efectiva_415.py:356` admite `coinciden is None`, y en el fixture siempre lo es); `min` o un suelo activo (H6); el cero impreso como «−» (H4); el límite de nodos y el de longitud por separado (la fórmula de la prueba incumple los dos).
- **[Hecho]** `test_relevo_i19_415.py` se ha leído, no ejecutado. Cubre el camino principal (relevo, solicitud «sustituida», respuesta antigua que no cierra, cierre con la vigente). No comprueba de forma directa que un relanzamiento sin cambios no añade un relevo (lo detectaría de forma indirecta: el análisis no terminaría), ni un cambio que haga fallar el paso 12.
- **[Propuesta]** Un caso por cada hueco que se corrija; para el límite de la tolerancia, exacto = libro + 0,00050001.

### H12 · OBSERVACIÓN · U1 y U4: lo que ahora se acepta y conviene declarar

- **[Hecho]** `s16` 5: los 146 datos numéricos de cálculo publicados del fixture, sin fuente, como `o["Historia!F5"] ± (cifra compuesta)` → `apto=True`, 321/321, 0 errores; el resumen dice «146 derivados comprobados (su significado económico lo acredita la revisión independiente, no el control automático)». Es el límite declarado de U1: ahora se ve en el resultado, en la ficha y en el informe V6.4 (no en el V6.3: H8).
- **[Hecho]** `s6` C y `s16` 4: prohibir los decimales negativos de `round` no cierra «el origen anulado por un round»: `(7*100 + 3*10 + 8/10 + 3/100 + 3/1000) + round(o["Historia!F5"] / 1000000000000)` → apta. La sensibilidad trata `round` como la identidad.
- **[Hecho]** Formas que el hito 1 rechazaba por «origen inerte» y ahora pasan (`s6` B, `s16` 2): `o[b] + o[a] * o[z]` con z un cero comprobado, y `min(o[b], o[a])` con a mayor. El valor sale de b; a es decorativo. No permiten escribir una cifra que no se pudiera ya (U1).
- **[Propuesta]** Decirlo en el docstring (U3 y U4) con estos ejemplos.

### H13 · OBSERVACIÓN · Empaquetado y documentación de la candidata

- **[Hecho]** El árbol congelado tiene 53 archivos que no están en el manifiesto: 36 de `personaje_v2/.lo_perfil/` (un perfil de LibreOffice, con fechas de las 16:51–17:07, anteriores a esta revisión) y 17 `.pyc`. El bloque del manifiesto de `verificar_paquete.sh`, ejecutado en lectura sobre el árbol, da «7031 archivos en el manifiesto · modificados 0 · ausentes 0 · de más 36 … FALLA» (`s12`). El paquete tiene que salir de un árbol limpio.
- **[Hecho]** `VERSION` dice «hito 1 … sin I19, I20 ni F1»; `CONTINUIDAD.md` es el del hito 1 (I19 e I20 como pendientes, línea 185: la aptitud solo en la V6.4 y la V6.4.1); no hay documento del hito 2. El manifiesto sí dice «hito 2 (candidata)».
- **[Hecho]** `resumen.py` no lleva la aptitud por entradas en ninguna plantilla, y `prompts/verificacion.md` no nombra el modo de la entrada efectiva ni el bloque nuevo. I20 hablaba de la ficha y el informe.

### H14 · OBSERVACIÓN · Varios

- **[Hecho]** El esquema no exige el bloque `verificacion_entradas` (una ficha nueva sin él valida: `s9` E) ni fija `aptitud_de_uso.apto_para_dinero_real` en `false` (con `true` valida; ya era así). El bloque nuevo sí lo fija.
- **[Hecho]** Un `signo` −1 con `tratamiento` «ninguno» se acepta (`s11` B5): se exige que el campo no esté vacío, no que explique la conversión. Los registros reales la explican siempre.
- **[Hecho]** El informe dice «sin declaración: expediente anterior a la 4.15» de cualquier expediente sin declaración, también de uno nuevo creado sin `cambiar_base.py` (U6 f de la cuarta pasada).
- **[Hecho]** Código sin uso tras el cambio: `_igual_libro`, `_igual`, `_eval_formula`, `_texto_pagina`; `_cita_contiene` solo lo usan las pruebas.
- **[Hecho]** «784.366 - 784.366» vale como cero impreso como guion y, a la vez, el signo de la segunda cifra queda indeterminado (`s1b`): las dos reglas leen el mismo guion de dos maneras. Ya era así para el cero.
- **[Hecho, registro real; fuera del cambio]** `aux:otros_inv_2018` de Vidrala cita «Acquisition of intangible assets - 13» (`CF_2019.txt`, p. 12). **[Interpretación]** Por la suma de la columna (−99.541 − 2.245 + 13 = −101.773), el 13 parece corresponder a la primera línea de la tabla (cobros por ventas de inmovilizado) y las etiquetas están desplazadas una línea en el texto extraído. Es pertinencia, del revisor del registro; se anota porque salió al mirar la regla de H3.

## 4. Mutaciones

Una regla quitada o alterada cada vez, en un árbol ligero aparte (`sondas/mutaciones.py`; resultados en `fable/mut/<nombre>/resultado.json`, `fable/mut_hito1/` para la comparación). El control sin cambio de regla pasa entero (141/141, 52/52, 33/33).

| Mutación | Qué se quita o altera | Resultado | Baterías |
|---|---|---|---|
| `m01` | R415-SIGNO: _signo_en_cita devuelve siempre +1 (la marca de signo se ignora) | detectada | entradas 4.15: abortada, fallan 4; entrada efectiva: abortada (ValueError: el componente pagos_arrendamientos_con_intereses…) |
| `m02` | R415-SIGNO: contraste_pagina lee el signo en la cita, no en el pasaje de la página | detectada | entradas 4.15: 140/141, fallan 1 |
| `m03` | R415-SIGNO: un signo indeterminado se da por bueno (ni pendiente ni discrepancia) | detectada | entradas 4.15: 137/141, fallan 4 |
| `m04` | R415-SIGNO: el signo contrario deja la entrada pendiente en vez de discrepancia | detectada | entradas 4.15: 138/141, fallan 3 |
| `m05` | R415-SIGNO: el guion a dos o más espacios se lee como signo menos (no como otra columna) | detectada | entradas 4.15: 140/141, fallan 1 |
| `m06` | R415-SIGNO: el guion a UN espacio se lee como signo menos (no indeterminado) | detectada | entradas 4.15: 139/141, fallan 2 |
| `m07` | R415-SIGNO: la cifra con los dos signos a la vez vale si alguno coincide | detectada | entradas 4.15: 139/141, fallan 2 |
| `m08` | R415-SIGNO (calcular_entrada): no se exige valor = signo × valor_fuente | detectada | entrada efectiva: 50/52, fallan 2 |
| `m09` | R415-SIGNO (calcular_entrada): no se exige «tratamiento» | detectada | entrada efectiva: 51/52, fallan 1 |
| `m10` | R415-SIGNO (calcular_entrada): la cita se contrasta con el valor absoluto de la cifra publicada, como en el hito 1 (sin signo) | detectada | entrada efectiva: 51/52, fallan 1 |
| `m11` | U2: tolerancia de importes ampliada a una milésima (0,001) | detectada | entradas 4.15: 140/141, fallan 1 |
| `m12` | U2: tolerancia de importes ampliada a 0,00055 | **NO detectada** | entradas 4.15: 141/141 |
| `m13` | U2: se quita la condición de que el libro tenga 3 decimales como mucho | detectada | entradas 4.15: 140/141, fallan 1 |
| `m14` | U2: el empate vale también sin unidad monetaria en el derivado | detectada | entradas 4.15: 139/141, fallan 2 |
| `m15` | U2: el dato publicado vuelve a la comparación del hito 1 (_igual_libro con floats) | **NO detectada** | entradas 4.15: 141/141 |
| `m16` | U3: sin límite de nodos de la fórmula | **NO detectada** | entradas 4.15: 141/141 |
| `m17` | U3: sin límite de longitud de la fórmula | **NO detectada** | entradas 4.15: 141/141 |
| `m18` | U3: round admite decimales negativos (−12 a 12) en las dos comprobaciones | equivalente (no cuenta): «-9» no es un literal, es un menos aplicado a 9, y `_validar_formula` lo rechaza antes de mirar el rango | entradas 4.15: 141/141 |
| `m19` | U4: la sensibilidad vuelve a ser solo local (sin puntos genéricos) | detectada | entradas 4.15: 140/141, fallan 1 |
| `m20` | U4: se quita el error «constante en el punto real» (not locales) | **NO detectada** | entradas 4.15: 141/141 |
| `m21` | T2/U4: se quita el error de los orígenes inertes | detectada | entradas 4.15: 140/141, fallan 1 |
| `m22` | U4: el 0 queda exento en cualquier posición de la fórmula, no solo en min/max | **NO detectada** | entradas 4.15: 141/141 |
| `m23` | T2: se quita el control de constantes | detectada | entradas 4.15: 140/141, fallan 1 |
| `m24` | U1: los derivados comprobados no se listan | detectada | entradas 4.15: 140/141, fallan 1 |
| `m25` | U5: el atributo `hidden` deja de ocultar el elemento (display:none, visibility:hidden y aria-hidden siguen ocultando) | **NO detectada** | entradas 4.15: 141/141 |
| `m26` | U5: la cita se compara con el HTML sin espacios (como en el hito 1) | detectada | entradas 4.15: 140/141, fallan 1 |
| `m27` | U5: no se lee el charset declarado (solo BOM o UTF-8) | detectada | entradas 4.15: 140/141, fallan 1 |
| `m28` | U5: sin declaración y sin UTF-8 válido, se adivina ISO-8859-1 | detectada | entradas 4.15: 140/141, fallan 1 |
| `m29` | U5: el tipo PDF vuelve a exigir la cabecera al principio (como en el hito 1) | **NO detectada** | entradas 4.15: 141/141 |
| `m30` | I20: la ficha no lleva el bloque verificacion_entradas | detectada | entrada efectiva: 47/52, fallan 5; entradas 4.15: 141/141 |
| `m31` | I20: la ficha dice siempre apto_por_entradas = false | **NO detectada** | entrada efectiva: 52/52; entradas 4.15: 141/141; entradas 4.14: 33/33 |
| `m32` | I20: la ficha dice siempre apto_por_entradas = true | detectada | entrada efectiva: 50/52, fallan 2; entradas 4.15: 141/141; entradas 4.14: 33/33 |
| `m33` | I20: el informe no avisa de que el modo aplicado no coincide con el declarado | **NO detectada** | entrada efectiva: 52/52 |
| `m34` | I20: la ficha dice siempre que el modo aplicado y el declarado coinciden | detectada | entrada efectiva: 51/52, fallan 1 |
| `m35` | I20: entrada_efectiva.json no entra en el material auditado | detectada | entrada efectiva: 51/52, fallan 1 |
| `m36` | I20: una declaración ilegible se muestra como «registrada» | detectada | entrada efectiva: 51/52, fallan 1 |
| `m37` | I20: el informe dice «Apta para dinero real: sí» si es apta por entradas | **NO detectada** | entrada efectiva: 52/52; entradas 4.15: 141/141; entradas 4.14: 33/33 |
| `m38` | R415-SIGNO: el cero impreso como guion se busca en la cita y no en el pasaje de la página (mutación de control) | detectada | entradas 4.15: 140/141, fallan 1 |
| `m39` | informe V6.4 (párrafo de aptitud de la 4.14): dice «Apta para dinero real: sí» | **NO detectada** | entradas 4.14: 33/33; entradas 4.15: 141/141 |
| `m40` | informe V6.4 (párrafo de aptitud de la 4.14): dice siempre «apta por entradas: sí» | **NO detectada** | entradas 4.14: 33/33; entradas 4.15: 141/141 |
| `m47` | U1: el informe V6.4 no dice cuántos derivados comprobados hay | **NO detectada** | entradas 4.15: 141/141 |
| `m48` | I20: el informe no dice el modo declarado ahora ni su procedencia | detectada | entrada efectiva: 49/52, fallan 3 |

**[Hecho]** 27 de 41 mutaciones detectadas; 14 no detectadas (aparte, una mutación equivalente).

Las mismas mutaciones del párrafo de aptitud de la V6.4 sobre el **código y las pruebas del hito 1** (`fable/mut_hito1/`):

| Mutación | Resultado | Baterías |
|---|---|---|
| `m39` | detectada | entradas 4.14: 31/33, fallan 2; entradas 4.15: 105/105 |
| `m40` | detectada | entradas 4.14: 32/33, fallan 1; entradas 4.15: 104/105, fallan 1 |

## 5. Respuesta a las seis preguntas del encargo de revisión

1. **Signo.** Sí hay citas en las que se acepta una cifra con el signo contrario al publicado: la cita recortada (H1), el menos separado por dos o más espacios (H3), «− x» a un espacio cuando «−» es un cero (H4), «(EUR x)» (H5). Hay rechazos falsos de formatos legítimos (H4, H5), ninguno en los registros reales. `_pasaje_en_pagina` toma la primera aparición y puede no localizar el pasaje (H1). Caminos sin signo: las lecturas externas no se contrastan (nunca cuentan como comprobadas), los datos de texto y los ceros no tienen signo, los auxiliares sí se contrastan, y `calcular_entrada` sin carpeta no contrasta la cita (ya era así; `construir` la llama con carpeta). La transformación declarada solo admite ±1 y exige igualdad exacta: no sirve para legitimar otra magnitud; sí puede eludirse entera con la cita recortada (H1).
2. **U2–U5 y U1.** `_importe_libro_exacto` no es una tolerancia general. Regresión hacia lo permisivo: los orígenes decorativos y el round que anula un origen (H12), dentro del límite declarado de U1. Falsos «inerte» según la escritura de la fórmula (H6). El 0 exento en min/max no permite escribir cifras. Los límites de coste funcionan. HTML: H7.
3. **I19.** Por lectura: no hay bucle, no se cierra con un material distinto y no se pierden solicitudes. Repite el paso 12 para cualquier cambio, también cuando haría falta volver más atrás (H9). No ejecutado.
4. **I20.** La ficha y el informe no presentan nada como apto para dinero real. El informe V6.3 puede decir «apta por entradas: sí (N de M comprobadas)» sin decir cuántas son derivados sin fuente o no materiales (H8). No se rompe ningún expediente anterior (material y esquema) ni las citas.
5. **Pruebas.** Las nuevas detectan la mayoría de las mutaciones (§4). No se ha rebajado el texto de ninguna prueba existente, salvo la aserción de R3, que es correcta; pero dos quedan rebajadas de hecho (H2).
6. **Registros reales.** Ningún rechazo falso nuevo ni aceptación indebida: diagnóstico idéntico, 1.410 entradas «ok».

## 6. Lo que no se ha hecho

- Nada con LibreOffice ni con el pipeline: I19 y su batería están revisados por lectura; la reconstrucción de C48 «con y sin valores migrados» es la del autor, no repetida.
- No se ha ejecutado la regresión completa (corre en otra sesión).
- No se ha revisado el sentido económico de ningún dato, de F1 ni del 108 de C48.
- Las propuestas (`s15`) son bocetos de apoyo, no implementaciones revisadas.
- La dependencia de `html.parser` respecto de la versión de Python solo se ha podido probar con 3.13.18, 3.12.3 y 3.11.18, las tres con las correcciones de seguridad recientes.

## 7. Resumen en diez líneas

1. Baterías en la copia: 141/141, 52/52, 33/33; las del hito 1 pasan con el código del hito 2 (105/105, 40/40).
2. El contraejemplo literal de la revisión externa ya no pasa; los registros reales no cambian (214/232, 207/226, 175/193; 1.410 entradas numéricas «ok»).
3. **H1 (importante):** con la cita recortada a la cifra, la página «-849697.000» vuelve a dar `apto=True`; el cálculo del hito 1 de C48 pasa sin declarar la conversión; una cita cortada acredita 849.697 donde se publica 8.496.970 y un cero donde se publica 0,49.
4. La causa es una: la cifra y su signo se leen dentro de la cita. Leerlos en la página no cambia ninguna entrada real (`s15`).
5. **H2 (importante, pruebas):** un informe V6.4 con «Apta para dinero real: sí» en su párrafo de aptitud pasa hoy las baterías; con el hito 1 se detectaba.
6. H3–H5: un menos separado de la cifra se lee como otra columna; «−» sí imprime un cero en Elis 2017; «(EUR x)» se lee positivo; «(3,2 %)», «$-x» y las fechas quedan pendientes.
7. H6: `min` y `max` legítimos fallan entre el 3 % y el 47 % de las veces según cómo se escriba la fórmula; `max(a − b, 0)` falla cuando el suelo actúa.
8. H7: HTML con clases CSS, `<details>` o sin `</head>`; iXBRL; «%PDF-» en el primer kilobyte.
9. H8–H10: el informe V6.3 no dice cuántos derivados hay; el modo distinto no detiene nada y el relevo vuelve siempre al paso 12; el texto de fuente de C48 se corta y pierde la página de 2025.
10. Dictamen: ACEPTABLE CON CORRECCIONES. H1 y H2 antes de cerrar; H1 obliga a repetir la regresión.

## 8. Integridad del árbol congelado

- **[Hecho]** Listado de huellas SHA-256 de los 7085 archivos del árbol congelado al empezar (15-nov-2026, 17:13 UTC) y al terminar (18:56 UTC): idénticos (SHA-256 de los dos listados: `6a32b2c522aa2ad8…55b505d9`). Ningún archivo del árbol tiene fecha posterior al inicio de la revisión.
- **[Hecho]** `git status` de `/home/user/munger-v2`: sin cambios. `fable/salidas/INTENTOS_SOFFICE.log` no existe: ninguna sonda intentó lanzar LibreOffice.
- **[Hecho]** Huellas de referencia de lo revisado (primeros y últimos 8 caracteres): `verificacion_entradas.py` `b24b11f9…59c293fa`; `fase1_historia.py` `d01d3d7b…ba0eaaf1`; `ficha.py` `eeccaf29…a43799a8`; `informe.py` `2f68034c…efaacad5`; `cierre_v2.py` `6d89a81a…b379c813`; `pipeline.py` `c7cb80a6…d91e36e1`; `ficha.esquema.json` `dd04c552…eecd9668`; `test_verificacion_entradas_415.py` `c62d221d…bae34e7c`; `test_entrada_efectiva_415.py` `1261e68b…ae6bdefc`; `test_relevo_i19_415.py` `968373bd…c6347c17`; `verificar_paquete.sh` `bb2f727a…90078da0`; `cambio_elis_c48_4_15.json` `838b5f5a…d193fabc`; `MANIFIESTO_SHA256.txt` `f74c8a2b…5d8c7a5f`; `DIFF_HITO1_A_CANDIDATA.diff` `4c1d3ac4…8ca6982b`.

## 9. Índice de sondas

Todas en `/tmp/claude-0/-home-user-munger-v2/ace24ef4-365c-50f9-bb78-93416041e669/scratchpad/rev_hito2/fable/sondas/`; salidas en `…/fable/salidas/` con el mismo nombre y extensión `.log` (las ejecutadas con el código del hito 1, con el sufijo `_codigo_hito1`).

| Sonda | Qué prueba | Hallazgo |
|---|---|---|
| `comun.py`, `fx5.py` | arnés (el fixture de la batería, tomado de `fx4.py`) | — |
| `s1_signo_unidad.py`, `s1b_signo_unidad_extra.py` | 70 + 12 formatos de signo en `_cita_cifra` | H3, H4, H5 |
| `s2_cita_recortada.py` | cita recortada: unidad, registro completo y C48 | H1 |
| `s2b_externa_variante_cita_recortada.py`, `externa_sondas_independientes_ORIGINAL.py` | la sonda externa, original y con una línea cambiada | H1, §2 |
| `s3_registros_reales_contexto.py` | registros reales: signo, contexto de la página, citas cortadas | §2, H1 |
| `s3b_…guion_columna.py`, `s3e_siete_entradas_regla_columna.py` | uso real de la regla del guion a 2+ espacios | H3 |
| `s3c_menos_unicode_cero_elis.py` | «−» como cero en fuentes reales | H4 |
| `s3d_…signo_tratamiento.py` | signo y tratamiento en los registros reales | §2, H14 |
| `s4_material_expedientes_anteriores.py` | identificador del material en 30 expedientes | §2 |
| `s5_u2_importe.py` | U2: diferencial de 200.000 pares | §2 |
| `s6_u3_u4_formulas.py` | U3 (coste), U4 (sensibilidad), U1 (unidad) | H6, H12 |
| `s7_u5_html.py`, `s7b_html_detalle.py` | HTML: 61 casos en tres intérpretes | H7 |
| `s8_u5_html_real.py` | las dos fuentes HTML reales de Elis | §2 |
| `s9_i20_ficha_informe.py` | I20: ficha e informe V6.3 y V6.4.1, esquema, citas | H8, H9, H14 |
| `s10_i19_relevo_real.py` | I19: condición del relevo en expedientes reales | §2 |
| `s11_signo_registro.py` | signo en el registro completo: formatos, dos apariciones, auxiliares | H1, H3, H4, H5 |
| `s21_signo_formatos.py` | tabla sistemática: 28 formas × 4 escrituras × 3 contextos | H3, H5 |
| `s12_bloque_manifiesto_de_verificar_paquete.py` | bloque del manifiesto, en lectura | H13 |
| `s13_c48_fuente.py` | C48: valor, términos y texto de fuente | H10, §2 |
| `s14_r3_cita_cortada.py` | R3 con la cita cortada dentro de una cifra | H1 |
| `s15_propuesta_contexto_pagina.py` | boceto de la propuesta de H1 y su efecto en los registros reales | H1 |
| `s16_u1_u4_registro.py` | U1 y U4 en el registro completo | H6, H12 |
| `s17_u4_semilla.py` | U4: dependencia de la escritura de la fórmula | H6 |
| `s18_derivados_reales.py` | los 148 derivados reales con las reglas nuevas | §2, H6 |
| `s19_tipo_fuente.py`, `pdfmin.py` | tipo de la fuente por su contenido | H7 |
| `s20_pruebas_hito1_con_codigo_hito2.py` | baterías del hito 1 contra el código del hito 2 | §2 |
| `mutaciones.py`, `mutaciones_resumen.py` | mutaciones | H2, H11, §4 |
