# Revisión independiente del hito 2 de la 4.15 · séptima comprobación, dirigida (candidata 45ff57c)

Revisor: Fable (Claude, contexto separado del autor del cambio; no es una revisión humana ni sustituye a la externa) · 16-nov-2026.
Convención: **[Hecho]** = comprobado por el revisor ejecutando o leyendo (se dice cuál); **[Interpretación]** = lectura del revisor; **[Propuesta]** = corrección sugerida. Lo que no se ha ejecutado se dice expresamente.
El sistema es experimental y supervisado. Nada de lo que sigue acredita aptitud para dinero real, ni esta revisión tampoco.
Alcance: comprobación dirigida y breve. Solo lo cambiado entre la candidata de la sexta comprobación (8196522) y esta (45ff57c): W3, W4 y W5 en `verificacion_entradas.py`, las pruebas de W1 y el registro del hito. No se repite la revisión completa ni se revisa el sentido económico de ningún dato, de F1 ni del 108 de C48.

## 0. Qué se ha revisado y cómo

- **Material:** el árbol congelado `rev7/munger_v2_r1` (commit 45ff57c), `rev7/DIFF_SEXTA_A_SEPTIMA.diff` (95 líneas, leído entero; SHA-256 `06b1adcc…a4b7f48c`), el informe y las sondas de la sexta comprobación (`…_4_15/revision_independiente/hito2/REVISION_FABLE_HITO2_SEXTA.md`, `sondas6/`, `sondas5/`) y el registro del hito (`hito2/HITO_2_4_15.md`, `hito2/PUNTO_DE_RECUPERACION.md`), leído como declaración del autor y comprobado (§7).
- **[Hecho] El manifiesto es conforme:** 7559 entradas, 7559 «OK» con `sha256sum -c`, 0 distintas, 0 ausentes; el único archivo del árbol que no lista es el propio manifiesto (7560 archivos). `CAMBIOS_ARCHIVOS.txt` coincide con él (36 modificados y 6882 nuevos, todas las huellas iguales).
- **[Hecho] El diff es exactamente el paso de una candidata a la otra en el código:** `git diff 8196522 45ff57c` (solo lectura) restringido a `scripts/`, `pruebas/`, `esquema/` y `verificar_paquete.sh` coincide byte a byte con el diff entregado. Cambian tres archivos: `verificacion_entradas.py` (seis líneas), `test_verificacion_entradas_415.py` y `test_entrada_efectiva_415.py`. `verificar_paquete.sh` no cambia (`8158d256…4160beb3`; los mínimos siguen en 190 y 61). El `git diff` completo tiene 82 archivos (73 nuevos y 9 modificados): los 79 que no son esos tres son el informe y las sondas de la sexta comprobación (62), resultados (11: la regresión de 8196522 y la reconstrucción de C48), el registro del hito, el punto de recuperación, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, el manifiesto y `CAMBIOS_ARCHIVOS.txt`.
- **[Hecho] El árbol congelado es el commit 45ff57c** en los veinte archivos comprobados uno a uno (código, pruebas, esquema, documentación, manifiesto y cambios). `ficha.py`, `pipeline.py`, `informe.py`, `cierre_v2.py`, `fase1_historia.py`, `ficha.esquema.json`, `test_verificacion_entradas_414.py`, `test_relevo_i19_415.py` y `test_cierre_v2.py` tienen las huellas que anotó la sexta comprobación.
- **[Hecho] Lo aplicado frente a lo propuesto.** La sexta comprobación entregó sus propuestas como código (`sondas6/propuestas6.py`). Reconstruidas sobre 8196522 con ese mismo script (`fable/prop6`, huella `832ac4f7…2ce5b396`, la que anotó la sexta) y comparadas con la candidata: las pruebas coinciden (un caso más en la candidata, el del apóstrofo tipográfico) y el código coincide, comentarios aparte, **salvo en un carácter de una línea** (`:542`; hallazgo X1). Comprobado también por el árbol sintáctico (`g10`): el de la candidata difiere del de la propuesta en una sola constante, la expresión de `:542`; el de la candidata con ese carácter repuesto es **idéntico** al de la propuesta.
- **Dónde se ha trabajado:** todo en `rev7/fable/`, sin copias completas: `copia/` (árbol ligero de esta candidata: `scripts/`, `pruebas/` y `esquema/` copiados; el resto, enlaces simbólicos al árbol congelado, que solo se lee), `prev/` (lo mismo con el código de 8196522, sacado con `git archive`), `c876/` (`verificacion_entradas.py` de 876bfc2), `prop6/` y `prop6t/` (8196522 con las propuestas de la sexta), `fix7t/` y `fix7/` (45ff57c con las propuestas de esta pasada: solo pruebas, y pruebas más un carácter de código; §3 al final) y `mut7/` (mutaciones). `/home/user/munger-v2` solo se ha leído.
- **[Hecho] No se ha lanzado LibreOffice ni `pipeline.py`.** Todas las sondas y baterías llevan delante en el `PATH` un sustituto de `soffice` que registra el intento y termina con 1 (§9). No se han ejecutado `test_relevo_i19_415.py`, `test_pipeline_sintetico.py`, `test_integracion_v64.py`, `test_auditorias_v2.py`, `test_cierre_v2.py`, `test_estados_v2.py`, `test_resumen_v2.py`, `test_integridad_auditoria_v2.py`, `test_trazabilidad_v2.py` ni `verificar_paquete.sh`. Sí las tres baterías permitidas, `pdftotext` y lo que las baterías ejecutan (`ficha.py` e `informe.py --provisional` sobre copias temporales).
- **Sondas y salidas:** las entregadas `e3`, `e7` (sondas6) y `d7` (sondas5), adaptadas a `fable/sondas7/` (solo cambian el arnés y los rótulos: VE = 45ff57c, VP = 8196522, la tercera columna = lo que proponía la sexta; cada una lo dice en su primera línea); `e9` se sustituye por `g5`, `g6` y `g9`, que hacen lo mismo con esta candidata; las nuevas, `g1`…`g9`, `mutantes7.py`, `mutaciones7.py` y `propuestas7.py`. Salidas en `fable/salidas/` (índice en §10). Uso: `cd fable/sondas7 && python3 -I -B gN_….py`.
- **Datos reales y sintéticos:** donde dice «real» se han leído los siete registros `verificacion_entradas.json` de la 4.14, sus textos conservados y los PDF del árbol; lo demás es el fixture sintético de la batería o texto construido por el revisor. Los contraejemplos sintéticos demuestran lo que el control acepta o rechaza, no que los registros reales lo hagan: **no lo hacen** (§6).

## 1. Dictamen

**ACEPTABLE CON CORRECCIONES.** Hay **una corrección de código que debe hacerse antes de cerrar el bloque técnico** (X1: un carácter en una línea), con sus casos de prueba (X2), y correcciones de declaración en el registro del hito (X3). Ninguna afecta a un registro real. **Tal como está, la candidata 45ff57c no debe darse por cerrada:** acepta un caso que la candidata anterior rechazaba y la batería no lo ve.

- **[Hecho] W3, W4 y W5 están aplicados como se propusieron en cinco de las seis líneas cambiadas, y hacen lo que declaran.** El apóstrofo tipográfico «’» cuenta ya como parte de un número en los límites de la cita, en los dos lados de `en_numero` y en el límite final de la cifra («1’849,7» citada «849,7» y «849’697» citada «Total 849» pasan de aceptadas a discrepancia); la cifra citada sola que además está dentro de un número con apóstrofo vuelve a leerse en su aparición suelta (W4); el mensaje del máximo dice «más de 200 veces» (W5).
- **[Hecho] En la sexta línea (`verificacion_entradas.py:542`, el límite inicial de la cifra en `_lectura_cifra`) se ha perdido el apóstrofo ASCII (X1).** 8196522 tenía `(?<!\d')`; la sexta propuso `(?<!\d['’])`; la candidata lleva `(?<!\d[’])`. Consecuencia: con una fuente que separa los miles con apóstrofo ASCII, la cifra de **detrás** del apóstrofo vuelve a valer cuando la cita contiene el número entero: página y cita «Total 1'849,7», valor 849,7 → **«ok»** (8196522: «ausente»). Es la parte de V7 que 8196522 había cerrado, reabierta. En el registro completo (fixture sintético), una entrada cuya fuente publica «1'849'697» y que declara 849697 queda **comprobada** y el registro **apto por entradas**; con 8196522 era una discrepancia. El comentario de esa misma línea dice que «1'849,7» no contiene 849,7.
- **[Hecho] La batería no lo ve (X2).** Las tres baterías pasan enteras con la candidata (190/190, 61/61 y 33/33). Desde que los límites de la cita llevan el apóstrofo (W4), los casos de prueba del apóstrofo se resuelven antes de llegar a `_lectura_cifra`: el resultado de ninguna prueba depende ya de los límites de cifra de `:542` con un apóstrofo. Por eso pasa X1, y por eso la mutación `v7c` —una de las diez de W1— vuelve a quedar sin detectar.
- **[Hecho] W1: nueve de las diez mutaciones se detectan ahora; `v7c`, no.** @@W1_RESUMEN@@
- **[Hecho] Fuera de X1, lo cambiado no abre ningún hueco hacia lo permisivo.** En 113.243 citas aleatorias (`g9`), toda diferencia entre la candidata y lo que proponía la sexta está en una página con un apóstrofo ASCII entre cifras (2.365; en 1.376 la candidata acepta lo que la propuesta rechaza: es X1), y ninguna en una página sin apóstrofo entre cifras. Con el carácter repuesto (`fix7`), 0 diferencias con la propuesta de la sexta.
- **[Hecho] Rechazos en falso nuevos:** ninguno en un registro real. Con el apóstrofo tipográfico pasa lo que W6 anotó para el ASCII: una «cifra + ’ + cifra» que no es un separador de miles deja de leerse y da **discrepancia** («Q1’24» con valor 24, «5’30» con valor 30, una llamada de nota tras una comilla de cierre, «‘Vision 2030’1», con valor 2030) (X4). Es prudente y puede declararse.
- **[Hecho] Registros reales:** el diagnóstico de los tres registros finales y el inventario de signo son idénticos byte a byte a los entregados, con la candidata, con 8196522 y con la corrección propuesta; las 469 entradas reales de Elis y Viscofan que pasan citando el texto pasan igual citando el PDF; 12.864 citas generadas sobre las páginas reales dan los mismos estados con los dos códigos; las 1.645 citas reales, «ok» con el mismo detalle; en los 73 textos conservados no hay ninguna «cifra + apóstrofo + cifra», ni ASCII ni tipográfico (§6).
- **[Hecho] El registro del hito** declara W2, W6, V5 con una fuente HTML y V6, y sus cifras de pruebas y regresiones se reproducen o constan en los archivos que cita. Pero (X3): da por corregidos W3 y las pruebas de W1 sin el resto que aquí se describe; llama «pendientes por prudencia» a cuatro formas que son **discrepancias**; conserva un límite que ya no existe y dos frases de §1 que ya no son la regla; y no nombra tres límites que las revisiones dejaron para declarar, los tres en el sentido de aceptar (§7).

**¿Qué debe corregirse antes de cerrar el bloque técnico?** [Interpretación]

1. **En el código, X1:** en `verificacion_entradas.py:542`, `(?<!\d[’])` → `(?<!\d['’])`. Un carácter. No es un límite declarable: va en el sentido de aceptar, es una regresión de esta misma candidata respecto de 8196522, contradice el comentario de la línea y lo que el registro da por corregido, y el criterio del propio autor es corregir lo que acepta. Con ese carácter, `verificacion_entradas.py` queda con SHA-256 `4b00aa2a42ae45743ef4f31669faad36a7effb81affe828fd4975a2ca98c86cd`: es el archivo exacto que esta comprobación ha ejecutado con las tres baterías, los registros reales y las sondas (§3 al final).
2. **En las pruebas, X2:** los casos de la cita **completa** con el valor cortado (`("Total 1'849,7", 849.7, "Total 1'849,7")` y `("Total 849'697", 849, "Total 849'697")`, y los dos iguales con «’»), que son los únicos que llegan a `:542`. Sin ellos, ni X1 ni `v7c` los ve la batería. Las líneas exactas, en §3 (X2) y en `sondas7/propuestas7.py`.
3. **En el registro del hito, X3:** quitar o corregir lo que no es cierto (puntos a, b y c) y añadir los límites que faltan (punto d). No requiere código.
4. Después, lo que el propio punto de recuperación prevé cuando hay cambio de código: las tres baterías y la regresión completa de la candidata final (la que está en marcha es la de 45ff57c, cuyo código cambia en una línea).

**¿Qué puede quedar como límite declarado?** [Interpretación] W2, W6 (dicho como lo que es: discrepancia prudente), V5 con una fuente HTML, V6, X4, los signos parecidos al apóstrofo que no son «'» ni «’» (resto de W3: «ʼ», «′», «´», «`», «‘»), el importe que parece un año («Saldo 2023-2049»), la regla de la fecha («Notas 5-6-1849») y X5 (el apóstrofo en `fase1_historia.importe_completo`). Los cuatro últimos van en el sentido de aceptar y son inherentes a las reglas o muy estrechos; ninguno es de este diff.

**¿Hace falta otra pasada?** [Interpretación] **No hace falta otra revisión como esta.** La corrección de X1 es un carácter que deja el código igual, comentarios aparte, al que la sexta comprobación propuso y probó, y que aquí se ha vuelto a probar. Basta una **verificación mecánica, de minutos, por un agente distinto del autor**:

1. `python3 -I -B sondas7/verificar_correccion_x1.py <ruta a …/munger_v2_r1 corregido>`: tiene que terminar «CONFORME» (código 0). Comprueba que `verificacion_entradas.py` es el mismo programa que el probado aquí (por su árbol sintáctico; dice además si la huella es exactamente `4b00aa2a…a98c86cd`), que los 17 casos de X1 dan «ausente» y los controles «ok», y que el bloque de pruebas del árbol pasa con su código, **falla con el código de 45ff57c** y detecta las seis variantes de la línea `:542`. Probado: `fix7`, conforme; la candidata, `fix7t` (solo pruebas) y `prop6` (el código bien y las pruebas de la sexta), no conformes (`salidas/verificar_correccion_x1_*.log`);
2. las tres baterías y la regresión completa de la candidata final;
3. una lectura del registro corregido contra la lista de X3.

Si al corregir se toca alguna otra línea de `verificacion_entradas.py`, el paso 1 lo dirá («NO CONFORME» en el código) y esa línea necesitará su comprobación dirigida.

## 2. Estado de W1–W6

Todo lo de la columna «Evidencia» es **[Hecho]** (sonda ejecutada sobre esta candidata). La gravedad es la que les dio la sexta comprobación.

| Hallazgo | Gravedad | Estado | Evidencia |
|---|---|---|---|
| **W1** · la prueba de V2 no probaba V2, la de V5 no detectaba la falta del corte y cuatro reglas sin caso | MENOR (pruebas) | **Corregido como se propuso en nueve de las diez mutaciones; `v7c` vuelve a quedar sin detectar (X2)** | Los casos son los propuestos, más uno («849,7» en «1’849,7»). `g5` (unidad): con el código de 876bfc2 fallan cuatro de las cinco pruebas del bloque (V1, V2, V3/V7 y V5) y con el de 8196522, una (el caso de «’»). Se detectan `v2a`, `v2b`, `v2c`, `v5a`, `v7a`, `v7d`, `v3b`, `t8d` y `t6c`; `v7c` no. Con la batería entera: §5 |
| **W2** · «real» es una marca de moneda: una unidad con «real» en otro sentido queda pendiente | MENOR (rechazo prudente) | **Sin cambio; declarado en `HITO_2_4_15.md` §5 (U7)** | `e7` D, registro: «% real», «tipo real», «crecimiento real (%)», «valor real», «real estate» y «tipo de cambio real», pendientes (no apto); «%» y «veces», comprobadas; «real por euro» y «EUR/real», comprobadas (tipo de cambio). `g7` C |
| **W3** · el apóstrofo tipográfico no contaba: «1’849,7» contenía 849,7 | OBSERVACIÓN (en el sentido de aceptar) | **Corregido para «’» (U+2019); al aplicarlo se pierde el ASCII en `:542` (X1)** | `e3` A13–A14, `g1` B19–B22: «1’849,7» citada «849,7» o entera con valor 849,7, y «849’697» citada «Total 849» o entera con valor 849, de «ok» a «ausente». `g2` G11, registro: «1’849.697» con valor 849,697, de comprobada (apto) a discrepancia. `e3` B: en la tabla de `en_numero`, el único par que cambia es «7’» (de pendiente a discrepancia). Resto, sin cambio y sin declarar: «ʼ», «′», «´», «`» y «‘» siguen sin contar (`e3` A13–A14, `g7` D); la cifra entera con «’» («1’849.7» = 1849,7) sigue sin reconocerse, ahora sin que se acepte el trozo. Coste: X4 |
| **W4** · los límites de la cita no llevaban el apóstrofo | OBSERVACIÓN | **Corregido** | `e7` B, `g9` A: página «Total 1'849,7⏎Otros 849,7», cita «849,7»: de pendiente a «ok»; «Total 849'697⏎Total 849», cita «Total 849»: de pendiente a «ok»; «9'774⏎ 9 320», cita «9», valor −9: de pendiente a «signo_distinto» (vuelve la discrepancia); la cita cortada «otal 849» ante «'697», de pendiente a discrepancia (el corte cae en un número: es la regla). `_apariciones_en_pagina("849,7", "Total 1'849,7")` da 0 apariciones. Sin prueba que lo fije (`w4b`, `w4e`, `w4g`, `w4h`; va en el sentido prudente) |
| **W5** · el mensaje del máximo decía «aparece 201 veces» | OBSERVACIÓN | **Corregido** | `e7` C: con 201, 202, 400 y 100.000 apariciones dice «la cita aparece más de 200 veces en la página». Sin prueba (`w5a`). Con una fuente HTML sigue diciendo «en la página» aunque cuente el documento (declarado, V5) |
| **W6** · rechazos nuevos de V3, V7 y V2 | OBSERVACIÓN | **Declarado en §5, pero como «pendientes» y son discrepancias (X3 a); «Q1'24» vuelve a aceptarse por X1** | `g7` A: «. . . .130,8», «ejercicio .849,7» y el intervalo partido por un salto de línea dan «ausente» o «signo_distinto» (discrepancia), no un pendiente. «Q1'24» con valor 24 y la cita completa: «ausente» con 8196522 y «ok» con la candidata (`e3` A16, `g8`) |

**Los puntos que el encargo pedía mirar.** Todo **[Hecho]**.

| Punto | Resultado |
|---|---|
| `e3` (apóstrofo y `en_numero`) | Lo anterior. Además, A2 y A10 —la cita completa con el valor cortado— pasan de «ausente» a «ok» (X1), y A16, A21 y A22 («Q1'24», «5'30», «'2023'849») vuelven a «ok». Textos reales: 0 «cifra + apóstrofo + cifra»; las 1.645 citas reales, «ok» con los dos códigos |
| `e7` (V6 declarado, límites de la cita, mensaje, «real») | Los diez ejemplos de la línea «+1» del docstring, conformes; W4 y W5, corregidos; W2, sin cambio |
| `e9` (las propuestas a nivel de unidad) → `g5`, `g6`, `g9` | Las pruebas de la candidata frente a cada mutación (`g5`), las pruebas propuestas ahora frente a la candidata, a la corrección y a cada mutación (`g6`) y el diferencial con la propuesta de la sexta y con 8196522 (`g9`): §3 y §5 |
| `d7` (bordes a nivel de unidad) | Cuarenta casos; ninguno cambia de estado entre 8196522, la candidata y la propuesta de la sexta (los intervalos, las fechas, el decimal sin cero, los miles con espacio, «real» y `\Z` en `en_numero`, como estaban) |
| Mutaciones de W1 con la batería entera | §5 |
| Tres baterías, diagnóstico, inventario de signo y PDF reales | 190/190, 61/61 y 33/33; idénticos byte a byte; 0 rechazadas (§4 y §6) |

## 3. Hallazgos nuevos

Ninguno afecta a un registro real. Los números de línea son los de esta candidata. X1 y X2 son de este diff y hay que corregirlos; X3, del registro; X4, un coste de lo corregido; X5 no es de este diff.

### X1 · MENOR (regresión, en el sentido de aceptar; debe corregirse antes de cerrar) · En `_lectura_cifra` se ha perdido el apóstrofo ASCII del límite inicial de la cifra: «Total 1'849,7» vuelve a contener 849,7

`scripts/verificacion_entradas.py:542`.

- **[Hecho] La línea** (`g1` A, `g10`; leída carácter a carácter). 876bfc2: `(?<![\d.,])` + cifra. 8196522 (corrección de V7): `(?<![\d.,])(?<!\d')` + cifra. Propuesta de la sexta (W3; `sondas6/propuestas6.py`): `(?<![\d.,])(?<!\d['’])`. **45ff57c: `(?<![\d.,])(?<!\d[’])`**: la clase lleva solo U+2019. En las otras cinco expresiones cambiadas (`:514`, `:515`, `:591`, `:592` y el límite final de la propia `:542`) están los dos caracteres. El comentario de `:542` dice «(hito 2, V7 y W3) «1'849,7» ni «1’849,7» contienen 849,7».
- **[Hecho] A nivel de unidad** (`g1` B, `e3` A): de 14 casos con apóstrofo ASCII en los que la cita se localiza (la cita completa, el número solo o un tramo que empieza antes del número), 11 pasan de «ausente» (8196522) a **«ok»** (45ff57c): «Total 1'849,7» con 849,7; «1'849,7» con 849,7; «Total 1'234'567» con 567 y con 234567; «1'849.7» con 849,7; «Empleados 12'345» con 345; «Resultado -1'849,7» y «Resultado (1'849,7)» con +849,7; «Ventas CHF 1'849,7 millones» con 849,7; «Ventas 1'849,7 1'702,3» con 702,3; «de 1'849,7» con 849,7. Dos más pasan de «ausente» a «signo_distinto» (con el valor en negativo: siguen siendo discrepancia) y uno sigue «ausente» (la cifra entre dos apóstrofos, que para el límite final). Con la propuesta de la sexta, los 14 dan «ausente». Los controles (la cifra entera: «1'849.7» = 1849,7, «849'697» = 849697, «1'234'567» = 1234567) dan «ok» con todos los códigos.
- **[Hecho] Lo que sigue cerrado:** la cita **cortada** («849,7» en «1'849,7», el doble corte «849,7 mill»), porque ahora la paran los límites de la cita y `en_numero` (W4), que sí llevan el apóstrofo ASCII; y el corte por **detrás** («Total 849» o la cita entera con valor 849 en «849'697»), porque el límite final de `:542` lleva los dos apóstrofos.
- **[Hecho] En el registro completo** (`g2`, fixture sintético de la batería, con los tres códigos):

  | La página dice | El registro declara | 8196522 | 45ff57c | con el carácter repuesto |
  |---|---|---|---|---|
  | «…: 1'849'697» (cita: la línea entera) | 849697 (miles de euros) | discrepancia, no apto | **comprobada, apto** | discrepancia, no apto |
  | «…: 23'849'697» | 849697 | discrepancia, no apto | **comprobada, apto** | discrepancia, no apto |
  | «…: 1'849'697» (cita: solo el número) | 849697 | discrepancia, no apto | **comprobada, apto** | discrepancia, no apto |
  | «…: 1'849'697.000» | 849697 | discrepancia, no apto | **comprobada, apto** | discrepancia, no apto |
  | «…: 1'849.697» (unidad «veces») | 849,697 | discrepancia, no apto | **comprobada, apto** | discrepancia, no apto |
  | «…: 1’849.697» (tipográfico; W3) | 849,697 | **comprobada, apto** | discrepancia, no apto | discrepancia, no apto |
  | «…: 849'697» (la cifra entera; control) | 849697 | comprobada, apto | comprobada, apto | comprobada, apto |

  La candidata cierra el caso tipográfico y abre el ASCII; el carácter repuesto cierra los dos.
- **[Hecho] Diferencial** (`g9` B, 113.243 citas aleatorias, el generador y la semilla de `e9` de la sexta). Candidata frente a la propuesta de la sexta: 2.365 diferencias, **todas** en páginas con un apóstrofo ASCII entre cifras; en 1.376 la candidata da «ok» y la propuesta «ausente»; en las otras 989 la candidata da «signo_distinto» o indeterminado donde la propuesta da «ausente». Ninguna diferencia en páginas sin apóstrofo entre cifras. Candidata frente a 8196522 (5.947 diferencias, todas en páginas con un apóstrofo entre cifras): deja de dar «ok» en 2.056 (2.047 en páginas con «’»: W3; 9 en páginas con solo ASCII: W4, una cita que empieza dentro de un número) y pasa a «ok» en 1.381: las 1.376 de «ausente» a «ok» (X1) y 5 de pendiente a «ok» (W4: la aparición de la cita dentro de un número con apóstrofo deja de contar y queda la lectura de la cifra suelta; iguales en la propuesta de la sexta). Las otras 2.510 cambian entre pendiente y discrepancia o entre dos discrepancias.
- **[Hecho] Otras formas que vuelven a aceptarse** (`g8`, `e3` A16–A22): «Q1'24» con valor 24, «5'30» con valor 30, «'2023'849» con valor 849 y «sube 2'5 puntos» con valor 5 (un decimal escrito con apóstrofo: se acepta la parte decimal como cifra). Con 8196522 daban «ausente» (el coste declarado en W6).
- **[Hecho] Alcance** (leído): `_cita_cifra` es la función que usan el contraste de cada entrada con su página (`:1134`), la lectura en el documento PDF o HTML (`:1138`) y el consumidor `fase1_historia.calcular_entrada` (`fase1_historia.py:405`, los componentes de un cálculo como el de C48); los tres pasan por `:542`.
- **[Hecho] Ningún registro real se ve afectado:** en los 73 textos conservados citados no hay ninguna «cifra + apóstrofo + cifra» (`e3` D), las 1.645 citas reales dan «ok» con el mismo detalle con los cuatro códigos (`g9` C) y el diagnóstico es idéntico (§6).
- **[Hecho] Por qué pasa la batería:** X2.
- **[Interpretación]** Es un descuido al aplicar W3 (se sustituyó el apóstrofo en vez de añadirle el tipográfico), no una decisión: el comentario de la línea y el registro dicen lo contrario de lo que hace. Es estrecho —hace falta una fuente con miles separados por apóstrofo ASCII (informes suizos; `pdftotext` da «'» o «’» según el documento) y una entrada cuyo valor sea justo el trozo de detrás— y ningún expediente lo usa. Pero va en el sentido de aceptar, lo introduce esta candidata y reabre lo que 8196522 había cerrado.
- **[Propuesta]** `(?<!\d[’])` → `(?<!\d['’])` en `:542`. Probado (`fix7`, al final de esta sección). Para que no vuelva a pasar: (1) cuando una revisión entrega sus propuestas como código (aquí, `propuestas6.py` y el árbol `prop6`), comparar con `diff` el archivo resultante con el del revisor antes de congelar: esta desviación habría salido como la única línea distinta fuera de los comentarios; (2) una sola constante con la clase de los apóstrofos (p. ej. `APOSTROFOS = "'’"`) usada en las seis expresiones, en vez de seis clases escritas a mano. Lo segundo no se ha probado y no es necesario para cerrar.

### X2 · MENOR (pruebas) · Desde W4, ninguna prueba depende de los límites de cifra de `_lectura_cifra` con un apóstrofo: `v7c` vuelve a quedar sin detectar y X1 pasa 190/190

`pruebas/test_verificacion_entradas_415.py:1136-1141` (el bloque «(V3, V7)»), frente a `scripts/verificacion_entradas.py:514-515` y `:542`.

- **[Hecho]** (`g1` C). Los tres casos de la batería con apóstrofo —`("849,7", 849.7, "Total 1'849,7")`, `("Total 849", 849, "Total 849'697")` y `("849,7", 849.7, "Total 1’849,7")`— tienen la cita **cortada**. Con 8196522 la cita contaba como una aparición y la cifra se leía (y se rechazaba) en `_lectura_cifra`. Con la candidata, `_apariciones_en_pagina` ya no la cuenta (0 apariciones: W4) y el «ausente» sale de `en_numero`. `_lectura_cifra` no se ejecuta en ninguno de los tres. El cuarto caso («849,7 mill», doble corte) tampoco llegaba.
- **[Hecho] Mutaciones** (`g5`, a nivel de unidad; con la batería entera, §5). Sobre la línea `:542` no se detecta ninguna: quitar todo el límite del apóstrofo por delante (`x1a`), dejarlo solo con el ASCII (`x1b`: se pierde W3 por delante), quitar los apóstrofos del límite final (`v7c`), dejarlo solo con el ASCII (`w3b`) o solo con «’» (`w3c`). La propia candidata es, respecto de lo propuesto, una de esas variantes (solo «’» por delante) y pasa 190/190. Tampoco se detectan cuatro de las ocho de los límites de la cita (`w4b`, `w4e`, `w4g`, `w4h`: sin ellos la cita vuelve a contar como aparición y la cifra se rechaza igual en `:542`; solo cambian un «ok» por un pendiente) ni la del mensaje (`w5a`). Sí se detectan `w4a`, `w4f`, `w4c` y `w4d`.
- **[Hecho] De dónde viene.** La sexta comprobación evaluó sus casos de prueba contra las mutaciones sobre el árbol con **solo** las pruebas (`prop6t`: el código de 8196522, sin W4), donde `("Total 849", 849, "Total 849'697")` sí detectaba `v7c`. Sobre el árbol con las pruebas **y** el código (`prop6`) solo ejecutó las baterías, no las mutaciones. Con W4 aplicado, ese caso deja de llegar a la línea. El hueco sale de la combinación de dos propuestas del revisor anterior; el autor aplicó los casos tal como se le dieron.
- **[Interpretación]** `v7c` va en el sentido de aceptar («849» dentro de «849'697» con la cita entera) y X1 demuestra que el riesgo no es teórico: una regresión en esa línea ha pasado la batería en esta misma candidata.
- **[Propuesta]** En el diccionario `v3` (`sondas7/propuestas7.py`, árbol `fix7t`; el número de pruebas no cambia):
  1. la cita completa con el valor cortado: `("Total 1'849,7", 849.7, "Total 1'849,7"): "ausente"`, `("Total 1’849,7", 849.7, "Total 1’849,7"): "ausente"`, `("Total 849'697", 849, "Total 849'697"): "ausente"`, `("Total 849’697", 849, "Total 849’697"): "ausente"`;
  2. dos controles, para que una corrección no se pase de estricta: `("Total 1'849.7", 1849.7, "Total 1'849.7"): "ok"`, `("Total 849'697", 849697, "Total 849'697"): "ok"`;
  3. W4: `("849,7", 849.7, "Total 1'849,7\nOtros 849,7"): "ok"`, `("Total 849", 849, "Total 849'697\nTotal 849"): "ok"` y los dos iguales con «’»;
  4. W5: añadir `"más de" in r_v5[1]` a la condición de la prueba «(V5)»;
  5. como ahora hay casos con la misma página, que el detalle del fallo lleve la clave entera (`mal_v3 = {k_: …}`).
  - Evaluado (`g6`): con esos casos, **la candidata falla** «(V3, V7)» —`{("Total 1'849,7", 849.7, "Total 1'849,7"): 'ok'}`—, el código con el carácter repuesto pasa las cinco pruebas del bloque, y las 25 mutaciones de `verificacion_entradas.py` evaluadas sobre el código corregido se detectan todas (las seis de `:542`, las ocho de W4, la de W5, las ocho de W1 que tocan ese archivo y dos vecinas).

### X3 · OBSERVACIÓN (declaración) · El registro del hito: lo que da por corregido, cuatro «pendientes» que son discrepancias, un límite que ya no existe, dos frases de §1 desfasadas y tres límites sin nombrar

`hito2/HITO_2_4_15.md:34`, `:38`, `:130`, `:132`, `:139-144`, `:174`; `hito2/PUNTO_DE_RECUPERACION.md:37`, `:52`; `CONTINUIDAD.md:10`. Detalle, afirmación por afirmación, en §7. Todo **[Hecho]** (leído, y `g7` donde se cita).

- **(a) Cuatro formas declaradas «pendientes por prudencia» son discrepancias** (`:139-141`; `g7` A). «. . . .130,8» y «ejercicio .849,7», citadas desde la cifra o enteras, dan «ausente»; el intervalo partido por un salto de línea («Plan 2023⏎–2026» con +2026) da «signo_distinto»; «Q1'24» con valor 24 daba «ausente» con 8196522 y con la candidata se **acepta** (X1). Las otras once formas de esa lista sí quedan pendientes. La diferencia importa: una discrepancia bloquea siempre; un pendiente no bloquea en una entrada de juicio no material con la materialidad revisada. La sexta comprobación las describió como rechazos que «vuelven a discrepancia» (W6).
- **(b) Un límite declarado que ya no existe** (`:143-144`): «“$” en en_numero da una discrepancia prudente tras una línea que acaba en cifra (Q6, V7)». Se corrigió en 8196522 (`\Z`), y la batería lo fija desde esta candidata: `("849,7 mill", 849.7, "Ventas 2023\n849,7 millones")` → pendiente (`g7` B, `d7` D1).
- **(c) Dos frases de §1 que ya no son la regla.** `:34`: «Un guion entre dos enteros es un intervalo o una fecha» —desde T8 y Q3 solo lo es entre dos años crecientes de 1900 a 2100 o en una fecha «d-m-aaaa»; lo demás queda pendiente, como dice el propio §5—. `:38`: «una cita que solo está como parte de una palabra o cifra → discrepancia» —desde T2, cortada dentro de una palabra queda **pendiente**; solo dentro de un número es discrepancia—.
- **(d) Límites que las revisiones dejaron para declarar y que el registro no nombra** (`g7` D), todos en el sentido de aceptar:
  1. el importe que parece un año: «Saldo 2023-2049» (publica −2049) se lee en positivo; y la regla de la fecha, que solo mira la forma: «Notas 5-6-1849» con +1849, «ok» (quinta comprobación, V6; sexta, fila V6 y §2). Tampoco están en el docstring;
  2. los signos parecidos al apóstrofo que no son «'» ni «’» —«ʼ», «′», «´», «`», «‘»—: «1ʼ849,7» sigue conteniendo 849,7 (sexta, W3; su propuesta solo cubría «’»);
  3. los miles con espacio («1 849,7» citada «849,7», «ok»): está declarado en el docstring de `_cita_contiene`, no en el registro.
  - Y dos costes de lo corregido ahora, prudentes: X4, y que la cifra entera con «’» («1’849.7» = 1849,7) no se reconoce (una fuente con ese separador da discrepancia con el valor correcto).
- **(e) El criterio** (`:132`): «lo que va en el sentido de aceptar se corrige, no se declara». Tal como está escrito no es cierto de la lista que le sigue, que declara cuatro límites en ese sentido (H3, el guion separado por varios espacios; el carácter invisible entre el signo y la cifra; el signo escrito con palabras —los tres, reproducidos en `g7` B—; y H7, lo que ocultan las clases CSS, leído), más los de (d). [Propuesta] decirlo como es: los huecos **nuevos** en el sentido de aceptar que han señalado las revisiones desde la tercera se han corregido; siguen declarados, en ese sentido, los que se enumeran.
- **(f) Lo que da por corregido** (`:130`; `PUNTO_DE_RECUPERACION.md:37`): «corregidos W1 (pruebas), W3, W4, W5». Con esta candidata: W4 y W5, sí; W3, sí para «’», con la regresión X1; W1, salvo `v7c`.
- **(g) La comprobación dirigida final** se da por hecha en `HITO_2_4_15.md:174` («seis revisiones independientes de este hito (y la comprobación dirigida final)») y en `CONTINUIDAD.md:10` («Seis revisiones independientes (Fable) y una comprobación dirigida final en `…/revision_independiente/hito2/`»): en este árbol no existe todavía (es esta) y su resultado no es «sin correcciones». El punto de recuperación sí la da por pendiente. `CONTINUIDAD.md:10` dice también «Regresiones completas de las candidatas conformes: PASA»; la de esta candidata está pendiente.
- **(h) Restos menores.** `PUNTO_DE_RECUPERACION.md:52` dice que `PROMPT_NUEVA_VENTANA.md` «sigue siendo el de la 4.14» y, en `:11`, que se actualizó (se actualizó: es el de la 4.15, hito 2). `VERSION` sigue diciendo «tres revisiones independientes» (el punto de recuperación lo da por pendiente de actualizar).
- **[Interpretación]** Nada de esto cambia lo que el control hace. Pero el registro es lo que leerá la revisión externa: lo que afirma tiene que ser cierto, y los límites que aceptan son justo los que conviene que estén.

### X4 · OBSERVACIÓN (rechazo prudente nuevo; coste de W3 y W4) · Con «’» entre cifras que no es un separador de miles, la cifra deja de leerse: discrepancia

`scripts/verificacion_entradas.py:514-515`, `:542`, `:591-592`.

- **[Hecho]** (`g8`, `e3` A). Lo que W6 anotó para el apóstrofo ASCII pasa ahora con el tipográfico, que es el que escriben los procesadores de texto: «Ventas Q1’24 crecen» con valor 24 (cita entera o desde la cifra), «Tiempo 5’30» con valor 30, «sube 2’5 puntos» con valor 5 y una llamada de nota tras una comilla de cierre —«the ‘Vision 2030’1 plan» con valor 2030, cita entera o «Vision 2030»— pasan de «ok» a «ausente». No cambian «9M’24 849,7» (la cifra de después), «H1’24: 24 tiendas» (la cifra aparece además suelta), «FY’24» (sin cifra delante), el posesivo «SBF 120’s» (forma real de los textos de Elis), «d’1,5 %» ni «l’exercice 2023».
- **[Hecho]** Ninguna entrada real tiene esa forma: 0 «cifra + ’ + cifra» en los 73 textos; los 40 apóstrofos pegados a una cifra son posesivos (`e3` D).
- **[Interpretación]** Va en el sentido prudente (discrepancia, nunca comprobada) y es el precio de tratar «’» como separador de miles. La llamada de nota tras comilla es la forma más plausible en un informe; es del mismo tipo que el límite ya declarado de `<sup>` pegado a la cifra en HTML. Para declarar, como discrepancia.

### X5 · OBSERVACIÓN (fuera del diff; ya existía en la 4.14; en el sentido de aceptar) · El control de la fase 1 `importe_completo` tampoco trata el apóstrofo como parte de un número

`scripts/fase1_historia.py:93` (usado en `:202` y `:206`).

- **[Hecho]** (`g11`). `importe_completo(imp, texto)` —la comprobación de la fase 1 de que el importe impreso de un componente está en su línea y en su página «como importe completo»— usa `(?<![\d.,])` + importe + `(?![\d.,]*\d)`. Rechaza «849,7» dentro de «1.849,7» y de «1,849,7», y «7» dentro de «7,608», pero acepta «849,7» dentro de «1'849,7» y de «1’849,7», y «849» dentro de «849'697» y de «849’697». Es el mismo límite que V7 y W3 señalaron en `verificacion_entradas.py`, en otro control. El archivo no cambia desde `d54ee13` (las correcciones de la primera pasada de este hito) y esas líneas no se han tocado desde el commit de la base 4.14 (`88b2a27`; `git log -L`, solo lectura); ningún informe de las pasadas anteriores nombra esa función.
- **[Hecho]** Ningún texto real tiene «cifra + apóstrofo + cifra» (`e3` D).
- **[Interpretación]** No es de este diff ni lo abre esta candidata; se anota porque es el mismo defecto y, corregido X1, quedaría como el único sitio donde el apóstrofo no cuenta. Para declarar junto a los demás; si se corrige, cuando se toque ese archivo, con su prueba.

### Las propuestas, probadas juntas

No es código entregado ni revisado: es una comprobación de que lo que se propone es compatible con lo que hay. `sondas7/propuestas7.py` escribe dos árboles ligeros sobre el código de 45ff57c: `fable/fix7t/` (solo las pruebas de X2; diff en `salidas/propuestas7_fix7t.diff`) y `fable/fix7/` (las pruebas y el carácter de X1; `salidas/propuestas7_fix7.diff`).

- **[Hecho] El código de `fix7` es la candidata con un carácter más** (`diff` de una línea, la `:542`; SHA-256 de `verificacion_entradas.py`: `4b00aa2a42ae45743ef4f31669faad36a7effb81affe828fd4975a2ca98c86cd`) y es **el mismo programa** que el que la sexta comprobación propuso y probó (`prop6`): los dos árboles sintácticos son idénticos (`g10`; las cuatro líneas distintas lo son solo en el comentario final). Lo que la sexta ejecutó sobre `prop6` vale, pues, para este código.
@@PROP_BATERIAS@@
- **[Hecho] Registros reales con `fix7`:** el diagnóstico de los tres registros finales y de los otros cuatro, y el inventario de signo, idénticos byte a byte a los entregados y a los de la candidata; `q12_pdf` B, 244 y 225, 0 rechazadas (§6).
- **[Hecho] A nivel de unidad:** `g1` (los 14 casos de X1, «ausente»; los controles, «ok»), `g2` (registro: tabla de X1), `g6` (el bloque de pruebas propuesto y las 25 mutaciones), `g8` (las formas que no son miles: iguales a la propuesta de la sexta), `g9` B3 (113.243 citas aleatorias: 0 diferencias con la propuesta de la sexta) y `g9` C (las 1.645 citas reales, iguales en estado y detalle). `g9` B3 se ejecutó con una versión anterior de `fix7` que solo difería de la definitiva en un comentario añadido al final de la línea `:542` (el programa es el mismo: `g10`); las demás, con la definitiva.
- No se han probado con la regresión completa ni con LibreOffice.

## 4. Lo cambiado que está bien

| Punto | [Hecho] | Sonda / salida |
|---|---|---|
| Baterías permitidas | En la copia, como las lanza `verificar_paquete.sh` (`python3 -B`): 190/190 (566 s), 61/61 (60 s) y 33/33 (99 s), código 0, ninguna línea FALLA. Ningún intento de lanzar LibreOffice. El mínimo de `verificar_paquete.sh` (190 y 61) coincide con lo que hay: el número de pruebas no cambia (los casos nuevos entran en pruebas que ya existían) | `salidas/bateria_*.log` |
| Pruebas existentes | En el diff de las dos baterías hay casos añadidos a cuatro diccionarios (`v1`, `v2`, `q3b`, `v3`) y a un bucle, y una condición más en «(V5)»; en «(V2)», los dos casos antiguos pasan a citar las dos líneas y uno se conserva además con la cita antigua. Ninguna aserción se rebaja y el número de pruebas no cambia | diff |
| W1, V2 | Los casos con la cita que abarca las dos líneas distinguen `\Z` de `$`: `v2a`, `v2b` y `v2c`, detectadas | `g5`, §5 |
| W1, V5 | La prueba comprueba ahora cuántas apariciones se recogen (201) además del reloj: `v5a` y `v5b`, detectadas | `g5`, §5 |
| W1, lo demás | «miles de real» (`v7d`), el doble corte (`v7a`), `\Z` en `en_numero` (`v3b`), la fecha con una cifra que no es un año (`t8d`) y la clave a tres ediciones (`t6c`), detectadas | `g5`, §5 |
| W3 | «’» cuenta en los límites de la cita, en `en_numero` (principio y final) y en el límite final de la cifra; por delante de la cifra, también (lo que falta ahí es el ASCII: X1) | `e3`, `g1`, `g2` |
| W4 | La cifra citada sola que además está dentro de un número con apóstrofo se lee en su aparición suelta; la discrepancia que había pasado a pendiente vuelve a discrepancia | `e7` B, `g9` A |
| W5 | El mensaje no afirma un recuento que no se hace | `e7` C |
| V6 declarado | Los diez ejemplos de la línea «+1» del docstring se comportan como dice | `e7` A |
| Bordes | Cuarenta casos de intervalos, fechas, decimal sin cero, miles con espacio y `\Z`: ningún cambio | `d7` |
| Diferencial | Fuera de las páginas con un apóstrofo entre cifras, 0 diferencias con 8196522 y con la propuesta de la sexta en 113.243 citas | `g9` |
| Páginas reales | 12.864 citas generadas sobre las líneas reales de 1.608 entradas: los mismos estados con los dos códigos; con el signo contrario, ningún «ok» | `r10` |
| Empaquetado | Manifiesto conforme (7559/7559) y `CAMBIOS_ARCHIVOS.txt` coincidente | §0 |

## 5. Pruebas y mutaciones

Dos maneras de mirar lo mismo.

**A nivel de unidad** (`g5`, segundos): el bloque de las cinco pruebas de `test_verificacion_entradas_415.py:1123-1146` (son llamadas puras a `VE`) se ejecuta tal cual contra la candidata, contra el código de 8196522 y de 876bfc2, contra la propuesta de la sexta y contra cada mutación cargada en memoria; para T6 se repite el bucle de las «erratas dobles» de `test_entrada_efectiva_415.py:354-356`.

- **[Hecho]** Con la candidata pasan las cinco. Con el código de 876bfc2 (sin V1–V7) fallan cuatro: «(V1, V4)», «(V2)», «(V3, V7)» y «(V5)» —las de V2 y V5, que en la sexta no detectaban nada, ahora sí—; «(Q3, V4)» pasa, como debe. Con el de 8196522 falla una, «(V3, V7)», por el caso de «’».
- **[Hecho]** De las 25 definiciones sobre `verificacion_entradas.py` (24 mutaciones y la corrección propuesta), 14 mutaciones se detectan y 10 no; la corrección propuesta pasa entera. De las nueve de W1 que tocan ese archivo, ocho se detectan; `v7c`, no. `t6c` (en `pipeline.py`): detectada por la clave «emtrada_efextiba» (tres ediciones, proporción 0,800).
- **[Hecho]** No detectadas: `v7c`, `x1a`, `x1b`, `w3b`, `w3c` (las cinco de la línea `:542`, en el sentido de aceptar), `w4b`, `w4e`, `w4g`, `w4h` (límites de la cita; en el sentido prudente) y `w5a` (el mensaje).

**Con la batería entera** (`mutaciones7.py`, con el arnés entregado de la cuarta comprobación: una regla quitada o alterada cada vez, en un árbol ligero aparte; resultados en `fable/mut7/<nombre>/resultado.json`).

@@MUT@@

## 6. Registros reales

- **[Hecho] Diagnóstico** (`…_4_15/scripts/diagnostico_registros_4_14.py`, con `python3 -I -B`) de los tres registros finales con el código de esta candidata, con el de la anterior y con la corrección propuesta: idénticos entre sí y, byte a byte, a `hito2/resultados/diagnostico_registros_4_14_con_reglas_hito2.json` (SHA-256 `91b6a33e…d587553a`): Viscofan 214/232 (1 error, 17 discrepancias), Vidrala 207/226 (4 errores, 15 discrepancias, 1 entrada no reproducible), Elis 175/193 (1 error, 17 discrepancias, 1 entrada no reproducible). Los otros cuatro registros del árbol dan lo mismo con los tres códigos (`viscofan` 211/232, `vidrala` 204/226, `elis_motor_A` 169/193 y `vidrala_decisiones_INVALIDO…` 186/226).
- **[Hecho] Inventario de signo** (`…/hito2/scripts/inventario_signo_registros.py`) de los siete registros: 1.645 entradas numéricas con página, todas «ok» (526 negativas, 1.082 positivas y 37 ceros); igual con los tres códigos e idéntico byte a byte al entregado (`hito2/resultados/inventario_signo_registros_reales.json`, SHA-256 `5716dc3c…26ad3a3c`).
- **[Hecho] PDF reales.** La parte B de `q12_pdf.py`, ejecutada tal cual con los tres códigos: Elis, 247 entradas con fuente `texto/…`, 244 pasan citando el `.txt` y 244 citando el PDF; Viscofan, 228, 225 y 225; 0 rechazadas solo por el control del PDF.
- **[Hecho] Ninguna regla cambiada toca una entrada real.** En los 73 textos conservados citados no hay ninguna «cifra + apóstrofo + cifra», ni ASCII ni con «’», «ʼ», «′», «´», «`» o «‘»; los 40 apóstrofos pegados a una cifra son posesivos («SBF 120’s») (`e3` D). Las 1.645 citas reales con fuente de texto dan «ok» con el mismo detalle con 8196522, la candidata, la propuesta de la sexta y la corrección (`g9` C). Citas generadas sobre las páginas reales (`r10`): 12.864, los mismos estados con los dos códigos.

## 7. El registro del hito, afirmación por afirmación

`hito2/HITO_2_4_15.md` (§4, §5 y §8) y `hito2/PUNTO_DE_RECUPERACION.md`. Todo **[Hecho]**: «reproducido» = ejecutado por el revisor; «consta» = está en el archivo que se cita, leído y no reproducido.

| Afirmación | Resultado |
|---|---|
| `test_verificacion_entradas_415.py`: 190/190; `test_entrada_efectiva_415.py`: 61/61; `test_verificacion_entradas_414.py`: 33/33; mínimos 190, 61 y 5 | Reproducido (190, 61 y 33). Los mínimos son los de `verificar_paquete.sh` (leído; el 5 es de `test_relevo_i19_415.py`, que no se ha ejecutado) |
| `test_relevo_i19_415.py`: 5/5 | No ejecutado (lanza LibreOffice). Consta en `resultados/verificacion_completa_8196522.txt` |
| Regresiones completas: `c2d2b96` FALLA en 5 bloques; `92b2362`, `f3d15e8`, `7a6583b`, `876bfc2` y `8196522`, RESULTADO GLOBAL: PASA | Consta en los seis `resultados/verificacion_completa_*.txt`. La de esta candidata, pendiente: lo dice el punto de recuperación |
| Reconstrucción de C48 con el código de cada candidata conforme | Consta para 8196522 (`resultados/reconstruccion_c48_8196522/`, ocho casos). No reproducida; no se revisa su sentido |
| Registros reales: diagnóstico idéntico byte a byte, inventario de signo igual, PDF reales sin rechazos falsos | Reproducido con esta candidata (§6) |
| «Mutaciones: … quedan sin prueba algunas que se declaran» | Cierto, y hay que añadir las de la línea `:542` (X2) mientras no entren sus casos |
| Control de la entrega 4.14: 29/35 | No comprobado |
| Tabla de las seis pasadas: candidata y dictamen de cada una | Conforme con los seis informes (leídos sus dictámenes) |
| 6.ª: «corregidos W1 (pruebas), W3, W4, W5» | W4 y W5, sí. W3, sí para «’», con la regresión X1. W1, nueve de diez (X2). X3 (f) |
| «Criterio aplicado: lo que va en el sentido de aceptar se corrige, no se declara» | No es exacto: X3 (e) |
| Límites declarados, signo: H3; once formas pendientes («(149.5m)», «(-x)», «31-dic-2024», «2024-25», «12-2024», «7-7,5 %», «2-3 %», «100-150», años decrecientes, el día de una fecha ISO, «31-12-24») | Reproducido: H3 se lee en positivo; las once, pendientes (`g7` A y B) |
| …«un intervalo partido por un salto de línea, «Q1'24», «. . . .130,8», «ejercicio .849,7»», como pendientes | No: son discrepancias, y «Q1'24» se acepta con esta candidata. X3 (a) |
| …«un carácter invisible entre el signo y la cifra la hace leer en positivo»; «el signo escrito con palabras no se reconoce» | Reproducido (`g7` B). Van en el sentido de aceptar |
| …«“$” en en_numero da una discrepancia prudente tras una línea que acaba en cifra (Q6, V7)» | Ya no: es un pendiente desde 8196522. X3 (b) |
| …diferencias tipográficas entre el texto conservado y el documento (T4); ISO-8859-9 y -11 | No repetido: su código no cambia (sondas de la cuarta comprobación) |
| U7: «real» con otro sentido deja la unidad pendiente (W2); «dólares por euro», también | Reproducido (`e7` D, `g7` C) |
| HTML: lo que ocultan las clases CSS (H7); la «página» es el documento entero y una cita repetida más de 200 veces queda pendiente (V5); `<sup>`; `.xht` | No repetido: las funciones de HTML no cambian en el diff. El umbral de 200 y el mensaje, sí (`e7` C) |
| Fórmulas: H12 y N8 | No repetido: fuera de este diff |
| U6/T6: «entrega_efectiva» y «entrada_de_efectivo» dan error por errata (Q5) | Reproducido: las dos detienen el paso; «tasa_efectiva», no (`g7` C) |
| §1: «Un guion entre dos enteros es un intervalo o una fecha»; «una cita que solo está como parte de una palabra o cifra → discrepancia» | Ya no son la regla. X3 (c) |
| §8 y `CONTINUIDAD.md:10`: «seis revisiones … y la comprobación dirigida final» | Las seis, sí. La comprobación dirigida es esta: X3 (g) |
| Punto de recuperación: «comprobación dirigida de W1 y W3–W5 y regresión completa: pendientes»; «No se da por superada» | Conforme |
| Lo que falta en la lista de límites | El importe que parece un año y la regla de la fecha; los signos parecidos al apóstrofo; los miles con espacio; X4. X3 (d) |

## 8. Lo que no se ha hecho

- Nada con LibreOffice ni con el pipeline. `test_relevo_i19_415.py` no se ha ejecutado (no cambia en esta candidata).
- **[Hecho, solo leído; no es material de esta revisión] La regresión completa de esta candidata** la ejecuta otra sesión sobre su propia copia (`scratchpad/reg7/`, cuyo `verificacion_entradas.py` tiene la huella de esta candidata, `7abbb081…9227c41b`) mientras se hace esta comprobación. @@REGRESION@@ El revisor no la ha reproducido. Sea cual sea su resultado, es la de 45ff57c: tras corregir X1 el código cambia en una línea y la batería 4.15 gana casos.
- No se ha comprobado el «control de la entrega 4.14: 29/35» ni las cifras de §0 del registro (ZIP, base materializada, manifiesto del hito 1).
- De `q12_pdf.py` solo se ha ejecutado la parte B, la de los PDF reales.
- No se han repetido las sondas de las pasadas anteriores que tocan código que no cambia (unidades y monedas, intervalos y `\Z`, HTML y codificaciones, lectura en el documento, U6, relevo, fichas): entre 8196522 y 45ff57c solo cambian seis líneas de `verificacion_entradas.py`, todas con el apóstrofo o el mensaje del máximo. De las de la sexta se han repetido `e3`, `e7` y `d7`; de la tercera, `r10`.
- @@NO_HECHO_MUT@@
- Las propuestas de esta pasada no se han probado con la regresión completa ni con LibreOffice.
- No se ha revisado el sentido económico de ningún dato, de F1 ni del 108 de C48.
- Los tiempos se midieron con la máquina cargada (la regresión completa de la otra sesión y, a la vez, entre tres y seis procesos propios): son orientativos.

## 9. Integridad del árbol congelado

@@INTEGRIDAD@@

## 10. Índice de sondas

Todo en `/tmp/claude-0/-home-user-munger-v2/ace24ef4-365c-50f9-bb78-93416041e669/scratchpad/rev7/fable/`. Salidas en `salidas/`, con el nombre de la sonda y extensión `.log` (las ejecutadas con el código de 8196522, con el sufijo `_anterior`; con la corrección propuesta, `_fix7`; los registros reales, en `salidas/reales/`; las baterías sobre los árboles con las propuestas, en `salidas/propuestas7/`).

**Sondas nuevas** (`sondas7/`; el arnés `comun7.py` carga en el mismo proceso `verificacion_entradas` de 45ff57c, 8196522, 8196522 con las propuestas de la sexta y 876bfc2):

| Sonda | Qué prueba | Hallazgo |
|---|---|---|
| `g1_lectura_apostrofo_ascii.py` | la línea `:542` en cada código, carácter a carácter; 25 casos a nivel de unidad (la cita completa o el número solo con el valor cortado, con signo, paréntesis, moneda y dos columnas; lo que sigue cerrado; el tipográfico; los controles); por qué vía se resuelven los casos de la batería | X1, X2 |
| `g2_registro_apostrofo_ascii.py` | lo mismo en el registro completo (fixture de la batería), con la candidata, con 8196522 (`_anterior`) y con la corrección (`_fix7`) | X1, W3 |
| `g5_pruebas_unidad_y_mutaciones.py` | el bloque de pruebas de la candidata contra la candidata, 8196522, 876bfc2, la propuesta de la sexta y cada definición de `mutantes7.py`; T6 | W1, X2 |
| `g6_propuestas7_unidad.py` | el bloque de pruebas propuesto (`fix7t`) contra la candidata (tiene que fallar), la corrección (tiene que pasar) y 25 mutaciones sobre el código corregido | X2, §3 al final |
| `g7_limites_declarados_hito.py` | cada límite del signo, de U7 y de U6 que declara `HITO_2_4_15.md` §5, contra el código; y los que no nombra | X3 |
| `g8_coste_apostrofo_tipografico.py` | «cifra + apóstrofo + cifra» que no es un separador de miles, con «'» y con «’», con los cuatro códigos | X4, X1 |
| `g11_importe_completo_fase1.py` | fuera del diff: `fase1_historia.importe_completo` con apóstrofos | X5 |
| `g10_equivalencia_ast.py` | el árbol sintáctico de `verificacion_entradas.py` de 8196522, la candidata, la propuesta de la sexta y la candidata con el carácter repuesto: cuáles son el mismo programa y en qué constante difieren | X1, §3 al final |
| `g9_diferencial_y_citas_reales.py` | los casos de `e9` B; diferencial aleatorio de `_cita_cifra` (113.243 citas) de la candidata frente a la propuesta de la sexta y frente a 8196522, y de la corrección frente a la propuesta; las 1.645 citas reales | X1, §1 |
| `mutantes7.py`, `mutaciones7.py` | mutaciones (§5); resultados en `mut7/<nombre>/resultado.json` | W1, X2 |
| `propuestas7.py`, `baterias_propuestas7.sh` | escribe `fable/fix7t` y `fable/fix7` (diff en `salidas/propuestas7_*.diff`) y ejecuta las baterías sobre ellos | §3 al final |
| `propuestas6_sobre_prev.py` | el `propuestas6.py` entregado, aplicado sobre el código de 8196522 (reconstruye `prop6` y `prop6t`) | §0 |
| `construir_arboles.py`, `adaptar_sondas.py` | los árboles ligeros y la adaptación de `e3`, `e7` y `d7` | — |
| `registros_reales.sh` | diagnóstico, inventario de signo y `q12_pdf` B con los tres códigos, y la comparación con lo entregado | §6 |
| `verificar_correccion_x1.py` | verificación mecánica de la corrección de X1 y X2 sobre un árbol dado (código por árbol sintáctico y huella; los casos de X1; el bloque de pruebas con el código del árbol, con el de 45ff57c y con las seis variantes de `:542`) | §1 |
| `integridad_final.sh`, `finalizar_informe7.py` | la comprobación de integridad de §9 y el relleno de las tablas de este informe a partir de los resultados | §9 |

**Sondas entregadas, repetidas** (adaptadas: solo el arnés y los rótulos): `e3_apostrofo_y_en_numero.py` y `e7_v6_declarado_y_casos_sueltos.py` (de `sondas6/`), `d7_unidad_bordes.py` (de `sondas5/`), todas en `sondas7/`; `r10_diferencial_reales.py` (de `sondas3/`, con su arnés `comun3.py` adaptado). **Del hito 1:** `q12_pdf.py`, parte B, sin cambios (se ejecuta desde el árbol congelado). El arnés de mutaciones (`sondas4/mutaciones4.py`) y el fixture (`sondas/fx5.py`) son los entregados, sin cambios.
