# Revisión independiente del hito 2 de la 4.15 · tercera pasada (candidata f3d15e8)

Revisor: Fable (Claude, contexto separado del autor del cambio; no es una revisión humana ni sustituye a la externa) · 15/16-nov-2026.
Convención: **[Hecho]** = comprobado por el revisor ejecutando o leyendo (se dice cuál); **[Interpretación]** = lectura del revisor; **[Propuesta]** = corrección sugerida. Lo que no se ha ejecutado se dice expresamente.
El sistema es experimental y supervisado. Nada de lo que sigue acredita aptitud para dinero real, ni esta revisión tampoco.
Alcance: comprobación acotada. Solo lo cambiado entre la candidata de la segunda pasada (92b2362) y esta (f3d15e8), y el estado de los hallazgos N1–N11 de la segunda pasada y de lo que quedaba de H5, H6, H7, H9, H11 y H14. No se repite la revisión completa.

## 0. Qué se ha revisado y cómo

- **Material:** el árbol congelado `rev3/munger_v2_r1` (commit f3d15e8), `rev3/DIFF_ESTABLE_A_TERCERA.diff` (527 líneas, leído entero; SHA-256 `af4ca571…b2f2afaa`), los informes y las sondas de las dos pasadas anteriores (`…_4_15/revision_independiente/hito2/`) y `hito2/PUNTO_DE_RECUPERACION.md`, leído como declaración del autor y comprobado punto por punto (§1, §2 y §7).
- **[Hecho] El manifiesto es conforme:** 7207 entradas, 0 distintas, 0 ausentes, 0 de más (`sha256sum -c`; el único archivo que no lista es el propio manifiesto). `CAMBIOS_ARCHIVOS.txt` coincide con él (36 modificados y 6530 nuevos respecto de la base original, todas las huellas iguales a las del manifiesto).
- **[Hecho] El diff es exactamente el paso de una candidata a la otra.** `git diff 92b2362 f3d15e8` (solo lectura), restringido a los seis archivos del diff entregado, coincide con él línea a línea. `git diff --name-status` da 102 archivos: los seis de código y pruebas (`verificacion_entradas.py`, `ficha.py`, `pipeline.py`, `test_verificacion_entradas_415.py`, `test_entrada_efectiva_415.py` y `verificar_paquete.sh`), `CAMBIOS_ARCHIVOS.txt`, el manifiesto, `PUNTO_DE_RECUPERACION.md`, 12 archivos de resultados (mutaciones de H2, regresión de la estable y reconstrucción de C48) y los 81 de la segunda pasada. No hay más cambios de código: `informe.py`, `cierre_v2.py`, `fase1_historia.py`, el esquema de la ficha, `test_verificacion_entradas_414.py` y `test_relevo_i19_415.py` tienen las huellas que anotó la segunda pasada.
- **[Hecho] El árbol congelado no se ha modificado** (§9). Todo se ejecutó en `rev3/fable/`, sin copias completas del árbol: `copia/` (árbol ligero de esta candidata: `scripts/`, `pruebas/` y `esquema/` copiados; el resto, enlaces simbólicos al árbol congelado, que solo se lee), `prev/` (lo mismo con el código de 92b2362, sacado con `git archive`, para comparar antes y después) y `mut3/` (mutaciones) y `prop/` (las propuestas del revisor, §3 al final). `/home/user/munger-v2` solo se ha leído.
- **[Hecho] No se ha lanzado LibreOffice ni `pipeline.py`.** Todas las sondas y baterías llevan delante en el `PATH` un sustituto de `soffice` que registra el intento y termina con 1; no hubo ninguno (`fable/salidas/INTENTOS_SOFFICE.log` no existe). No se han ejecutado `test_relevo_i19_415.py`, `test_pipeline_sintetico.py`, `test_integracion_v64.py`, `test_auditorias_v2.py`, `test_cierre_v2.py`, `test_estados_v2.py`, `test_resumen_v2.py`, `test_integridad_auditoria_v2.py`, `test_trazabilidad_v2.py` ni `verificar_paquete.sh`: se han leído. Sí se han ejecutado las tres baterías permitidas, `ficha.py` e `informe.py --provisional` sobre copias temporales (como hace la batería), `pdftotext` y, a nivel de unidad, `pipeline.modo_entrada_efectiva` y `Pipeline.solicitud_auditoria_vigente` importando el módulo (no ejecutan ningún paso).
- **Sondas y salidas:** las de las dos pasadas anteriores, copiadas a `fable/sondas/` y `fable/sondas2/` con adaptaciones mínimas (rótulos «anterior» = 92b2362 y «tercera» = f3d15e8; recorrer el árbol siguiendo los enlaces); las nuevas, en `fable/sondas3/` (`r1`…`r16`, `mutaciones3.py`); salidas en `fable/salidas/` (índice en §10). Uso: `cd fable/sondas3 && python3 -I -B rN_….py`.
- **Datos reales y sintéticos:** donde dice «real» se han leído los siete registros `verificacion_entradas.json` de la 4.14, sus textos conservados y los PDF que hay en el árbol; lo demás es el fixture sintético de la batería. Los contraejemplos sintéticos demuestran lo que el control acepta o rechaza, no que los registros reales lo hagan: **no lo hacen** (§7).

## 1. Dictamen

**ACEPTABLE CON CORRECCIONES.** Las correcciones de la segunda pasada hacen lo que declaran en N1, N2 (informe), N3, N4, N5 y N10, los registros reales no cambian y las pruebas existentes no se han rebajado. Pero dos de las correcciones (N9 en U7 y N6 en el HTML) abren un hueco **en el sentido de aceptar** que la candidata anterior no tenía, una tercera (N10) rechaza como discrepancia citas legítimas, y N3 deja un resto. Son correcciones pequeñas y locales; ninguna afecta a un registro real.

- **[Hecho]** Las tres baterías permitidas pasan en la copia: 173/173, 60/60 y 33/33, código 0, sin intentos de lanzar LibreOffice. Los mínimos de `verificar_paquete.sh` (173, 60 y 5) coinciden con lo que hay. Las baterías del hito 1, sin tocar, pasan con este código (105/105 y 40/40). En el diff de las baterías solo hay casos añadidos: ninguna aserción anterior cambia.
- **[Hecho]** Registros reales: el diagnóstico de los tres registros finales es idéntico byte a byte al entregado y al de la candidata anterior; el inventario de signo, también (1.645 entradas «ok»: 526 negativas, 1.082 positivas y 37 ceros). Las 602 entradas reales de Elis, Viscofan y Vidrala que pasan el contraste citando su texto conservado y tienen su PDF en el árbol pasan igual citando el PDF: ningún rechazo por la lectura nueva de N3 (el autor declara 469 de Elis y Viscofan: reproducido; se añaden 133 de Vidrala).
- **[Hecho]** De los once hallazgos de la segunda pasada: corregidos N1, N4, N5 y N10; corregidos en parte N2, N3, N6, N7, N9 y N11; N8 sigue igual y el autor lo declara límite. Tabla en §2.
- **[Hecho]** Hallazgos nuevos (§3): cuatro menores de código (T1–T4), uno menor de pruebas (T5) y cinco observaciones (T6–T10).
  - **T1** (regresión de U7): una unidad monetaria no reconocida que mencione «tipo de cambio» o lleve una moneda tras una barra («miles de euros a tipo de cambio constante», «millones de euros/EUR million») ya no queda pendiente; con ella, un error de escala de mil queda **comprobado**. La candidata anterior lo dejaba pendiente.
  - **T2**: la regla del «fragmento completo» da **discrepancia**, con un mensaje que dice que la cita no contiene el valor, cuando la cita acaba o empieza justo en la cifra y la página lleva algo pegado («849.7m», «2,95x», «CHF7.3», «849,7¹») o el rótulo va tras un punto pegado («2.3.Deuda…»). Antes valía. En las páginas reales hay 182 cifras de esa forma; ninguna entrada real está afectada.
  - **T3** (regresión de H7): el modo XHTML se decide por el contenido; en un `.html` que lleve el `xmlns` de XHTML, «`<div hidden/>`» vuelve a no ocultar lo que sigue. La lista de codificaciones admite por prefijo códecs que un navegador no lee.
  - **T4** (resto de N3): si la cita no se localiza con sus palabras en el texto del documento (una palabra partida en el PDF, un guion blando en el HTML), la lectura nueva se omite en silencio y manda el texto conservado.
- **[Hecho] Pruebas.** De las 31 mutaciones de las reglas que entran con esta candidata, 17 se detectan y 14 no (entre ellas la de N4, cuatro de las cinco de N3 y la que amplía la exención de U7). Las nueve que el autor declara cubiertas ahora (`h1g`, `h9a`, m12, m16, m17, m20, m22, m29 y H6 ±) se detectan todas. De las otras catorce que la segunda pasada dejó sin detectar, ninguna se detecta (§6 y T5).
- **[Interpretación]** Antes de cerrar el hito el revisor corregiría T1 y T3 (cada una, una línea y su prueba negativa), corregiría T2 o, como mínimo, cambiaría la categoría y el mensaje, y corregiría T4 o lo declararía; añadiría las pruebas de T5 y llevaría los límites declarados (N8, H12, la parte de CSS de H7, m47, lo que queda de N5) al código y al registro del hito (en la candidata congelada no constan; un commit posterior, que no se ha revisado, ya los lista en el registro).
- **[Hecho]** Las propuestas de T1 a T4, aplicadas juntas sobre una copia, pasan las tres baterías permitidas (173/173, 60/60 y 33/33) y dejan idénticos el diagnóstico y el inventario de los registros reales (§3, al final). No son código entregado.
- **¿Hace falta otra pasada?** **Sí, corta.** [Interpretación] T1 y T3 son regresiones en el sentido de aceptar y no deberían quedar como límites; corregirlas es cambiar código, y todo cambio de código lo revisa un agente distinto del autor. Basta una comprobación dirigida de lo que se cambie para T1–T4 (unas pocas líneas de `verificacion_entradas.py` y sus pruebas), con las sondas `r2`, `r4b`, `r5`, `r7`, `r7b` y `r8` de esta pasada, las tres baterías y, si se toca `_apariciones_en_pagina`, además `n2`, `n11`, `n12`, `r10` y el diagnóstico de los registros reales. No hace falta repetir nada más de esta revisión. Si solo se cambiara documentación, no haría falta.
- **[Hecho, solo leído]** La regresión completa de esta candidata no la ha ejecutado el revisor; la de la otra sesión terminó con «RESULTADO GLOBAL: PASA» (§8).

## 2. Estado de los hallazgos de la segunda pasada y de los residuos de la primera

Todo lo de la columna «Evidencia» es **[Hecho]** (sonda ejecutada sobre esta candidata; lo que es por lectura se dice). La gravedad es la de la pasada que lo encontró.

| Hallazgo | Gravedad | Estado | Evidencia |
|---|---|---|---|
| **N1** · sin registro ni `entrada_efectiva.json`, la ficha y el informe V6.3 callaban la aptitud por entradas | MENOR | **Corregido**, con el alcance que propuso la segunda pasada | `n5` B4–B6: con el modo que el paso 2 de la 4.15 registra en `estado_pipeline.json`, con el modo declarado en `alcance_v2.json` o con `fase1_metadatos.json` que lo registra, la ficha lleva el bloque y el informe dice «apta por entradas: no … Apta para dinero real: no» aunque se borren los dos archivos (antes: sin bloque). B1: un expediente de la 4.14 sin esas señales sigue sin bloque al borrar el registro (es la «salida histórica» del diseño). `r1`: en las 96 carpetas del árbol con estado, ficha, cierre, alcance o metadatos, la condición nueva da lo mismo que la anterior (89 sin bloque y 7 con él) y ningún alcance ni metadatos es ilegible. `r9`: los 12 expedientes cerrados generan ficha e informe provisionales idénticos byte a byte con los dos códigos. Pruebas: T5 |
| **N2** · con el modo aplicado distinto del declarado, el informe V6.4 decía «sí» en un bloque y «no» en el otro | MENOR | **Corregido** en el informe y en `aptitud_de_uso`; queda un resto en la ficha (T7) | `n5` A1 y A2 (V6.4.1, registro apto): los dos bloques del informe dicen «apta por entradas: no»; `aptitud_de_uso.verificacion_entradas.apto_por_entradas = false` y `motivos_no_apto` lleva el motivo del modo. Resto: `verificacion_entradas.resumen.apto_por_entradas` sigue en `true` dentro del bloque que dice `false` |
| **N3** · con fuente PDF o HTML, la cifra y su signo se leían solo en el texto conservado | MENOR | **Corregido en parte** (T4) | `n4`: los seis casos (PDF y HTML; paréntesis, menos y cifra con un dígito más) pasan de comprobada a discrepancia. `r3`: 602 entradas reales citadas contra su PDF, ningún rechazo por la lectura nueva. `r4`: columnas y celdas contiguas no dan rechazos en falso. Resto: `r4b` (la cita no se localiza en el documento) |
| **N4** · bastaba que la cita tocara la cifra | MENOR | **Corregido**; sin prueba propia (T5) | `n2` C1–C4, `n11` a1–a4 y `r5` A1–A6: «ausente» (discrepancia). Las 1.645 entradas reales no cambian (`n3`) |
| **N5** · un guion pegado entre dos cifras se leía siempre como intervalo | MENOR | **Corregido** en lo que pedía la propuesta | `n7`: los cuatro casos que aceptaban el signo contrario («T4-15,2», «…financiero1-149,5», «2023-849,7», «1.234,5-567,8») quedan pendientes. Sigue leyéndose como intervalo un entero de hasta cuatro cifras pegado a otro («2023-849»); ahora quedan pendientes rangos con decimales o miles (T8) |
| **N6** · tres regresiones del HTML | MENOR | **Corregido en parte, con una regresión nueva** (T3) | `n6` (igual con Python 3.13.18, 3.12.3 y 3.11.18): de 16 a 7 casos señalados. Corregido: XHTML con `<script/>`, `<div style="display:none"/>`, `<span hidden/>`, `<style/>`, `<textarea/>` autocerrados (A1, A2, A4–A6); `<summary hidden>` y con `display:none` (B4, B5); `ibm850` y `euc-kr` (E7, E8). Sin cambio: en un documento HTML, una etiqueta con prefijo que lleva `hidden` o `display:none` sigue dándose por visible (A10, A11); B6, B7, C3, E5, E9 |
| **N7** · reglas nuevas sin prueba | MENOR (pruebas) | **Corregido en parte** | De las 23 mutaciones que la segunda pasada encontró sin detectar, ahora se detectan 9, que son las que el autor declara: `h1g` (el cálculo del hito 1 de C48 con las citas recortadas, en `calcular_entrada`), `h9a` (el modo distinto con un registro apto), `h6f`, `m20`, `m12`, `m16`, `m17`, `m22` y `h7k` (la m29). Siguen sin detectarse 14: `h9d` (la declaración del modo con error), `h1e`, `h1f`, `h6a`–`h6e`, `h7g`, `h7m`, `h7n`, `h14b`, `i20b` y `m47`. De las reglas nuevas de esta candidata, 14 de 31 mutaciones tampoco se detectan (T5) |
| **N8** · lo que queda de la sensibilidad | OBSERVACIÓN | **Sin cambio; el autor lo declara límite** (en la candidata, solo en el punto de recuperación) | `n1`, `n9` y `n14`: salidas idénticas a las de la segunda pasada (orden de los orígenes en fórmulas anidadas; `min(o[año], 0)` deja comprobados los 11 ceros de cálculo sin fuente) |
| **N9** · U7, U6 y H14: rechazos en falso | OBSERVACIÓN | **Corregido en parte, con una regresión nueva** (T1) y un efecto en U6 (T6) | U7: «USD por EUR», «EUR/USD», «tipo de cambio EUR/USD» ya no quedan pendientes (`n8` A y B1); siguen pendientes «EUR por ADR», «€/MWh», «millones de DKK», «euro». U6: `tasa_efectiva`, `entrega_efectiva`, `entrada_de_efectivo`, `fecha_entrada_efectiva` y `entrada_efectiva_motivo` ya no son erratas; `nota_entrada_efectiva` lo sigue siendo; `{"modo": "estricta"}` y `{"entrada_estricta": true}` siguen dejando «registrada» sin aviso (`n8` D). H14: «Ninguno.», «none» y «.» dan error; siguen pasando «ninguno (dato directo)», «no aplica», «n.a.», «–», «x»; un cero con signo −1 y «ninguno» sigue dando error; el orden de los controles no cambia (`n8` B y C) |
| **N10** · coste, un rechazo en falso y dos casos límite | OBSERVACIÓN | **Corregido**, con un efecto nuevo (T2) | Coste: la página de una sola línea con 2.000 apariciones pasa de 126 s a 2,4 s y la de 5.000, de 315 s a 2,0 s (`n3` c). «Total 849,697.000» con «Subtotal 849,697.0001» en otra línea: comprobada (`n11` b1). «(» al final de una línea y «849,697.000)» en la siguiente: pendiente (`n11` c1). Relevo: el motivo ya no se arrastra a una solicitud posterior y una lista mal formada no da excepción (`r16`); restos en T9 |
| **N11** · documentación y restos | OBSERVACIÓN | **En parte** (T10) | Retiradas `_igual` y `_texto_pagina`. Siguen `MONEDAS` y, ahora sin uso, `TOL_ABS` y `TOL_REL`; los tres comentarios que ya no son ciertos; `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y el borrador `HITO_2_4_15.md` sin actualizar (el autor lo declara pendiente) |
| **H5** · formatos pendientes o con el signo contrario | MENOR | **Corregido en parte**; sin más cambio que N5 y «cifra)» | `s1`: 24 casos distintos de lo esperado, de 70 (antes 25); `s21`: igual (264 bien, 36 pendientes en falso, 36 aceptan el contrario: es H3); `s11`: 7, igual. Sin cambio: «[149,5]», «±149,5», «CR»/«DR», «(4 573,7)», «(-149,5)», «149,5-» |
| **H6** · sensibilidad | MENOR | **Corregido en parte**; sin cambio (es N8) | `s16`, `s17`, `s6` y `s18`: salidas idénticas. Pruebas: se detectan `h6f` (perturbación en los dos sentidos) y `m20` (constante en el punto real); `h6a`–`h6e` siguen sin detectarse |
| **H7** · HTML | MENOR | **Corregido en parte** | `s7`: 23 casos señalados, igual; `s7b`, `s8` y `s19`, iguales. Lo cambiado es N6 (y T3). Las clases CSS, `sr-only`, `font-size:0`, `opacity:0` y lo demás siguen igual; el autor lo declara límite solo en el punto de recuperación |
| **H9** · modo distinto que no detiene nada; el relevo vuelve siempre al paso 12 | MENOR | **Corregido en parte** | Corregido N2. Sin cambio (por lectura): el relevo vuelve siempre al paso 12 (`pipeline.py:1064`), también si cambió `entrada_efectiva.json` o `fase_c.json` (el autor lo deja abierto en el punto de recuperación); nada detiene el pipeline; el prompt de la auditoría no lleva el motivo (queda en `solicitud_auditoria.json`). `s9` y `s10`, iguales |
| **H11** · lo que las baterías no distinguen | MENOR | **Corregido en parte** | De las siete mutaciones de la primera pasada que seguían sin detectarse, ahora se detectan seis: m12, m16, m17, m20, m22 y m29 (`h7k`). La m47 no, y el autor la declara |
| **H14** · varios | OBSERVACIÓN | **Corregido en parte** | Lo de N9 (lista de tratamientos). Sin cambio: el esquema no exige el bloque (por diseño) y su descripción no nombra las señales nuevas de N1 (T10); «784.366 - 784.366» se lee de dos maneras |
| **H3**, **H12**, **H13** | — | **Sin cambio** | H3 consta como límite en el docstring de `_signo_en_cita`; H12, solo en el punto de recuperación; H13: la documentación de cierre sigue pendiente |

## 3. Hallazgos nuevos

Ninguno afecta a un registro real. T1 a T4 son defectos del código que entran con las correcciones de la segunda pasada; T5, de las pruebas; T6 a T10, observaciones. Los números de línea son los de esta candidata.

### T1 · MENOR · N9/U7: la exención del «tipo de cambio» saca de U7 importes; con ellos, un error de escala de mil queda comprobado

`verificacion_entradas.py:166` (`tipo_cambio`), `:1258-1267` (lo que hace el control con una unidad que no es monetaria).

- **[Hecho]** `r7` A, la función unidad a unidad (candidata anterior → tercera). Pasan de «pendiente por U7» a «no monetaria», además de los tipos de cambio que se querían eximir: «millones de euros a tipo de cambio constante», «miles de euros (a tipo de cambio constante)», «millones de euros al tipo de cambio de cierre», «EUR million at constant exchange rates», «miles de USD convertidos al tipo de cambio medio», «millones de dólares (tipo de cambio de cierre)», «millones de euros/EUR million», «Miles de € / € thousand», «USD (millones) / EUR (millones)», «miles de coronas/euros» y «millones de pesos por euros». Siguen pendientes «miles de €», «MM€», «EUR millones» y «millones de DKK».
- **[Hecho]** `r7b`, registro completo (fixture de la batería), con los dos códigos. La fuente publica 849,697 «en miles» y el registro lo lleva al modelo, que tiene 849,697 millones, con escala 1: mil veces de más.

  | Unidad declarada (escala 1) | 92b2362 | f3d15e8 |
  |---|---|---|
  | «miles de euros» | error: escala incoherente | error: escala incoherente |
  | «miles de €» | pendiente (U7) | pendiente (U7) |
  | «miles de euros a tipo de cambio constante» | pendiente (U7) | **comprobada** |
  | «EUR thousand at constant exchange rates» | pendiente (U7) | **comprobada** |
  | «millones de euros/EUR million» | pendiente (U7) | **comprobada** |
  | «Miles de € / € thousand» | pendiente (U7) | **comprobada** |

- **[Hecho]** La prueba nueva solo mira que dos tipos de cambio no queden pendientes; ningún caso mira que un importe siga pendiente. La mutación `n9c`, que amplía la exención a cualquier unidad con «por», «per» o una barra («€/MWh» y «EUR por tonelada» dejarían de quedar pendientes), pasa las baterías enteras (173/173).
- **[Hecho]** Ninguna entrada real usa una unidad así (las de los registros son «millones de euros», «miles de euros», «EUR por acción», «euros por acción», «año», «acciones», «texto», «moneda» y «norma») y el diagnóstico no cambia.
- **Causa.** La exención se decide por tres subcadenas en cualquier parte de la unidad («tipo de cambio», «exchange rate», o «por», «per» o «/» seguidos de una moneda), no por la forma de un tipo de cambio. Una unidad no reconocida que no es monetaria admite cualquier escala que sea potencia de diez.
- **[Interpretación]** Es una regresión en el sentido de aceptar, en un control que el hito declara (U7). «A tipo de cambio constante» es un calificativo corriente de los importes en los informes anuales, y las cabeceras bilingües con barra, también.
- **[Propuesta]** Eximir solo cuando la unidad **entera** es un par de monedas («USD por EUR», «EUR/USD», con «tipo de cambio» delante o sin él) y no lleva ninguna palabra de escala (miles, millones, thousand, million, mm, k, m). Añadir a la batería casos negativos: «millones de euros a tipo de cambio constante» y «millones de euros/EUR million» siguen pendientes.

### T2 · MENOR · N10: la regla del «fragmento completo» da por discrepancia citas legítimas cuya cifra se publica entera

`verificacion_entradas.py:477` (los límites de la cita), `:538-543` (la cita que solo aparece «sucia» se clasifica como «ausente»), `:1083-1084` (el mensaje).

- **[Hecho]** `r2` A y B, `_cita_cifra` con la página, los dos códigos. Dieciséis casos pasan de «ok» a «ausente»:
  - algo pegado **detrás** de la cifra y la cita acaba en la cifra: «Revenue 849.7m» citado «Revenue 849.7»; «£1.2bn»; «12,5x»; «+3,5pp»; «849,7M€»; «150MW»; una llamada de nota «849,7¹» o «849,7a»; «-130.8m» citado «130.8»;
  - algo pegado **delante** y la cita empieza en la cifra: «EUR849,7 millones» citado «849,7 millones»; «CHF849.7»; «FY2024 849,7» citado «2024 849,7»;
  - el rótulo tras un punto o una coma pegados: «2.3.Deuda financiera neta 849,7» citado «Deuda financiera neta 849,7»; «…ejercicio.Total 849,7»; «neto,consolidado 849,7».

  Con el trozo pegado dentro de la cita («Revenue 849.7m») o separado por un espacio, «ok». De 24 citas que empiezan o acaban en puntuación, paréntesis, símbolos o cifras con signo («(130,8)», «130,8)», «(130,8», «-130,8», «−130,8», «+130,8», «€130,8», «130,8 €.», «Ventas 130,8;», la cifra seguida de punto, coma, «%», «€», «(1)», «*» o «…»), 23 siguen «ok» y la otra (C19, un guion de cero seguido de «(1)») ya se rechazaba con la candidata anterior (`r2` C1–C24). Las citas cortadas dentro de un **número** se rechazan, como debe ser (`r2` D1–D5).
- **[Hecho]** `r2` E, registro completo: la entrada queda en **discrepancia** con el texto «la cita no contiene el valor de la fuente 849697.0 como cifra completa de la página (formato equivalente, sin redondear)». La cita lo contiene; el motivo que da `_cita_cifra` («la cita empieza o acaba dentro de una palabra o de una cifra de la página») no llega al mensaje.
- **[Hecho]** En las páginas reales esas formas existen (`r2b`, 34 textos conservados): 312 cifras con decimales llevan una letra pegada detrás (sobre todo los múltiplos de Vidrala y Elis: «DEUDA/EBITDA 2,95x 2,87x 2,72x», «3.75x») y 33 una letra pegada delante (la mayoría, códigos como «CCM4.1»; también «revenue of CHF7.3 million»). `r2c`, sobre las que llevan un código de moneda delante o «x», «m», «bn», «pp», «k» o «M» detrás: en 182 apariciones, la cita cortada en la cifra pasa de «ok» a «ausente»; con el trozo pegado dentro de la cita sigue «ok».
- **[Hecho]** Lo que lo acota: ninguna entrada real cambia (§7); en 6.432 citas cortadas entre palabras sobre las líneas reales de 1.608 entradas, ninguna pasa de «ok» a rechazo (`r10`).
- **Causa.** El límite trata igual las letras y las cifras (`\w`), y el punto y la coma. Está pensado para la cita cortada dentro de un número y alcanza a la cita que acaba junto a una letra. La clasificación «ausente» (R3) presupone que la cifra citada no es la publicada, y aquí lo es.
- **[Interpretación]** Va en el sentido seguro, pero es una discrepancia falsa con un mensaje que señala al valor: quien lo lea puede «corregir» el valor en vez de alargar la cita.
- **[Propuesta]** (1) Límite según la clase del carácter: si la cita empieza o acaba en una cifra, que no vaya pegada a otra cifra ni a un separador con cifra (la misma regla que ya usa `_lectura_cifra`); si empieza o acaba en una letra, que no vaya pegada a otra letra. Así «Total 5» sigue sin contar dentro de «Subtotal 5,01» y «849.7» cuenta en «849.7m». (2) «Ausente» solo si el corte cae dentro de un número; si cae dentro de una palabra, «no_localizada» (pendiente) con su motivo. (3) Llevar el motivo al mensaje. Comprobar con `n2`, `n11`, `n12`, `r2`, `r10` y el diagnóstico.

### T3 · MENOR · N6: el modo XHTML se decide por el contenido, y la lista de codificaciones, por prefijos

`verificacion_entradas.py:873` (`self.xhtml`), `:905-912` (`handle_startendtag`), `:842` (codificaciones).

- **[Hecho]** `r8` A (igual con Python 3.13.18, 3.12.3 y 3.11.18). Un archivo `.html` se trata como XHTML si empieza por «`<?xml`» o si sus primeros 4.096 caracteres contienen `xmlns="http://www.w3.org/1999/xhtml"`. Un navegador decide por el tipo del archivo: un `.html` lo analiza siempre como HTML, donde la barra de «`<div hidden/>`» no cierra nada. Resultado, con el texto citado detrás del elemento:

  | Caso (archivo `.html`) | Navegador | 92b2362 | f3d15e8 |
  |---|---|---|---|
  | A1 con el `xmlns`: `<div hidden/>` | oculta | ausente | **presente** |
  | A2 con el `xmlns`: `<div style="display:none"/>` | oculta | ausente | **presente** |
  | A3 con el `xmlns`: `<script src="x.js"/>` | oculta | ausente | **presente** |
  | A4 que empieza por `<?xml …?>`: `<div hidden/>` | oculta | ausente | **presente** |
  | A5 con el `xmlns`: `<textarea/>` | oculta | ausente | **presente** |
  | A10 que solo menciona el `xmlns` en un comentario: `<div hidden/>` | oculta | ausente | **presente** |
  | A6 control, sin `xmlns`: `<div hidden/>` | oculta | ausente | ausente |

  Y al revés: un `.xhtml` sin declaración XML y con el `xmlns` entre comillas simples, o después de los primeros 4.096 caracteres, sigue rechazándose (A8, A9), como antes.
- **[Hecho]** `r8` B. La lista admitida pasa a aceptar por prefijo («cp4», «cp8», «euc_», «iso2022_»), y `big5hkscs` por nombre: 26 códecs más de los que Python tiene con alias, y otros sin alias (`cp874`, `cp875`). Los navegadores (lista WHATWG) leen `cp866`, `cp874`, `euc_kr`, `iso2022_jp` y `big5hkscs`; los demás no: las páginas de códigos de DOS (`cp437`, `cp850`…`cp869`), variantes de `iso2022_jp` y de `euc_jis`, `iso2022_kr`, y dos EBCDIC (`cp424`, `cp875`). B1: un documento que declara `charset=cp875` con la cita codificada en EBCDIC da «presente» (antes, pendiente); un navegador no conoce esa etiqueta y muestra otra cosa. B3: `iso-2022-kr`, que un navegador no decodifica, da «presente».
- **[Hecho]** Las dos fuentes HTML reales del árbol no llevan el `xmlns` ni cambian (`s8`); ningún registro cita un HTML.
- **Causa.** El modo se infiere del contenido y no de cómo se abre el archivo. La propuesta de la segunda pasada decía «XML si la extensión es `.xhtml`/`.xht` o empieza por `<?xml`»: la segunda mitad era imprecisa, y A4 lo muestra; la comprobación del `xmlns` la amplía. En las codificaciones se pedía añadir tres nombres y se añadieron cuatro prefijos.
- **[Interpretación]** Reabre para una clase de documentos lo que corrigió H7 («`<div hidden/>` oculta lo que sigue»). El `xmlns` de XHTML es frecuente en archivos `.html` (XHTML 1.0 servido como HTML, exportaciones de Word); el elemento autocerrado oculto, no: hace falta un documento mal formado o construido a propósito.
- **[Propuesta]** Modo XML solo por la extensión del archivo (`.xhtml`, `.xht`), que es lo que decide un navegador con un archivo local; con eso A8 y A9 dejan de rechazarse. Lista explícita de codificaciones, sin prefijos: las de WHATWG (`euc_kr`, `cp866`, `cp874`) y, si se quiere `ibm850`, las páginas de códigos compatibles con ASCII una a una; nunca EBCDIC ni `iso2022_kr`. Un caso de la batería con `.html` + `xmlns` + `<div hidden/>`.

### T4 · MENOR · N3 (resto): si la cita no se localiza con sus palabras en el texto del documento, la lectura nueva se omite en silencio

`verificacion_entradas.py:1079` (las lecturas «no_localizada» se descartan), `:1046` y `:1064` (la presencia de la cita en el documento se comprueba sin guiones blandos, en el HTML, o sin espacios, en el PDF).

- **[Hecho]** `r4b`, registro completo. El documento publica «-849697.000 total», el texto conservado no lleva el menos y la cita es «849697.000 total», con `valor_fuente` positivo:
  - caso 1, el PDF dice «total»: discrepancia (N3 lo detecta);
  - caso 2, el texto del PDF parte la palabra («to tal»): **comprobada**;
  - caso 3, el texto del PDF junta dos palabras («totaldel ejercicio»): **comprobada**;
  - casos 4 y 5, el HTML lleva un guion blando o un espacio de ancho cero dentro de la palabra: **comprobada**.

  En los cuatro, la lectura de la cita en el documento es «no_localizada». Con la candidata anterior los cinco eran comprobados: no es una regresión, es lo que queda de N3.
- **[Hecho]** `r3b`: en las 602 entradas reales con PDF, la cita se localiza siempre en el texto con «-layout» y se lee «ok» (en 226, también sin layout). Dejar pendiente la entrada cuando ningún texto del documento localiza la cita no rechazaría ninguna.
- **[Hecho]** En el sentido contrario, la lectura nueva no rechaza entradas legítimas: `r3` (602 reales, 0), `r4` A y B (columnas con el guion del cero, celdas contiguas del HTML, que el texto visible separa con dos espacios). Deja pendiente, y antes comprobaba, una tabla de columnas estrechas en la que «pdftotext» pone el guion del cero a un espacio de la cifra y el texto conservado, hecho con otro extractor, a más (`r4` A6.2 y A6.3): es conservador y coherente con la regla del guion a un espacio.
- **Causa.** El control que exige la cita en el documento compara sin espacios (PDF) o sin guiones blandos (HTML); la lectura exige las palabras separadas igual; cuando no casan, se descarta sin decirlo.
- **[Interpretación]** Hacen falta dos infidelidades a la vez (un texto conservado que perdió el signo y una diferencia tipográfica en una palabra de la cita), pero las dos son propias del mismo supuesto de N3: un texto conservado que no sale de «pdftotext».
- **[Propuesta]** Si hay texto del documento y en ninguno se localiza la cita, pendiente («la cita está en el documento, pero no con sus palabras: el signo no puede leerse en él»). O declararlo como límite.

### T5 · MENOR (pruebas) · Reglas nuevas que ninguna prueba protege

`pruebas/test_verificacion_entradas_415.py:991-1058` (grupo RW) y `:1087-1108` (H9 y N2 con el registro apto); `pruebas/test_entrada_efectiva_415.py:100-105`, `:354-355` y `:411-425`.

- **[Hecho]** De las 31 mutaciones de las reglas que entran con esta candidata (§6), 14 no las detecta ninguna de las tres baterías. Por hallazgo:
  - **N4 (1 de 1).** `n4_solapa`: con la regla anterior (basta que la cita toque la cifra) las baterías pasan enteras. Los casos que la batería pone para N4 (la cita «0» de «849697.000») los decide el límite del fragmento de N10, no esta regla. Los que solo decide N4 están en `r5` A: la cita acaba en el separador («Total 849.» de «Total 849.697») o empieza en él, o los miles van con espacio («697.000» de «849 697.000»).
  - **N3 (4 de 5).** `n3b` (no se lee el HTML), `n3c` (del documento solo cuenta el signo distinto: una cifra ausente o un signo indeterminado se ignoran), `n3d` y `n3e` (solo uno de los dos textos del PDF). La única prueba es un PDF con el menos.
  - **N1 (2 de 3).** `n1b` (sin la señal de `alcance_v2.json` ni de `fase1_metadatos.json`) y `n1c` (un alcance ilegible deja de mostrar el bloque): la prueba nueva solo cubre el modo registrado en el estado.
  - **N10 (3 de 6).** `n10a1` y `n10a2`: cada límite del fragmento por separado (los casos de la batería los decide cualquiera de los dos; sin ninguno, sí falla); `n10c`: el recorte que acota el coste (no hay prueba de coste).
  - **N9 (2 de 6).** `n9c`: la exención del tipo de cambio ampliada (es T1: falta el caso negativo); `u6g`: el umbral de U6 entre 0,88 y 0,92.
  - **N5 (1 de 3)** y **N2 (1 de 3).** `n5c`: que el entero anterior al guion no lleve nada pegado delante («T4-15»); `n2c`: `motivos_no_apto` sin el motivo del modo.
- **[Hecho]** Se detectan las otras 17: `n5a`, `n5b`, `n10a`, `n10b`, `n10d`, `n3a`, `n6a`–`n6d`, `n9a`, `n9b`, `n1a`, `n2a`, `n2b`, `u6e` y `u6f`.
- **[Hecho]** De las 23 que la segunda pasada dejó sin detectar, se detectan las nueve que el autor declara y no las otras catorce: `h9d` (una declaración del modo con error y el registro apto: la prueba nueva de H9 solo cubre el modo distinto), `h1e`, `h1f`, `h6a`–`h6e`, `h7g`, `h7m`, `h7n`, `h14b`, `i20b` y `m47`.
- **[Interpretación]** En esos puntos el código hace lo que declara (lo confirman las sondas); falta la prueba. Las que más importan: el caso negativo de U7 (con él T1 no habría entrado), N4, N3 con un HTML y con una cifra ausente en el documento, y las señales de N1.
- **[Propuesta]** Un caso por hueco: (1) «millones de euros a tipo de cambio constante» → pendiente; (2) `("Total 849.", 849697, "Total 849.697")` y `("697.000", 849697, "Total 849 697.000")` → «ausente»; (3) el caso de N3 con una fuente HTML, y con el PDF publicando la cifra con un dígito más; (4) la ficha con solo un `alcance_v2.json` que declara el modo, y con el alcance ilegible → con bloque; (5) una declaración ilegible con un registro apto → no apta en los dos bloques; (6) «Variación T4-15» → pendiente; (7) una cita que empieza dentro de una palabra y otra que acaba dentro de un número, por separado. Y las de N7 de la segunda pasada que se quieran cerrar.

### T6 · OBSERVACIÓN · N9/U6: con el umbral 0,88 una de cada cinco erratas dobles vuelve a dejar el modo en «registrada» en silencio

`pipeline.py:127`.

- **[Hecho]** `r6`. Las 805 erratas de una edición de la clave (borrar, cambiar, insertar una letra, trasponer dos) se detectan con 0,8 y con 0,88. De 23.462 erratas de dos ediciones (muestra con semilla fija), con 0,8 quedaban sin detectar 2; con 0,88, **5.163 (22 %)**: «emtrada_efectiba», «entrada_efectibo», «entrara_efectiba». También dejan de detectarse «entrada_efec» y «ent_efectiva». En el otro sentido, `nota_entrada_efectiva` y `entrada_efectiva_nota` siguen siendo «erratas» (0,882) y `entrada_efectiva_motivo` o `fecha_entrada_efectiva` no: depende de que el añadido tenga cuatro letras o cinco.
- **[Hecho]** Los alcances reales no cambian (`n13`: 40 carpetas, todas «registrada» con los dos códigos). El modo aplicado se ve en la ficha y en el informe.
- **Causa.** Un umbral de parecido no separa una errata de una clave legítima parecida: al subirlo se cambian rechazos en falso por silencios.
- **[Interpretación]** El cambio quita rechazos en falso a costa de la propiedad que U6 b declara (una errata no deja el modo en «registrada» en silencio).
- **[Propuesta]** La de la segunda pasada: un contrato cerrado de claves de `alcance_v2.json`. O mantener 0,8 y eximir por nombre las claves legítimas conocidas.

### T7 · OBSERVACIÓN · N2: en la ficha queda un «apto_por_entradas: true» dentro del bloque que dice «false»

`ficha.py:91` (el bloque de I20 guarda el resumen sin el modo), `pipeline.py:1036-1039` (por lectura).

- **[Hecho]** `n5` A1 y A2: `verificacion_entradas.apto_por_entradas = false`, `verificacion_entradas.resumen.apto_por_entradas = true` y `aptitud_de_uso.verificacion_entradas.apto_por_entradas = false`: dos copias del mismo resumen en la misma ficha dicen cosas distintas. El informe no lo muestra (lee el indicador de fuera).
- **[Hecho, por lectura]** El paso 12 sigue anotando «apta por entradas: sí» en `estado_pipeline.json → verificacion_entradas` y en el historial, sin el modo. Ningún script lo lee.
- **Causa.** N2 se corrigió en `aptitud_de_uso`, que recibe el motivo del modo; el bloque de I20 sigue guardando el resumen del registro tal cual.
- **[Propuesta]** La de la segunda pasada: una sola función que decida «apto por entradas» (registro y modo) para los dos bloques y para el paso 12.

### T8 · OBSERVACIÓN · N5, N10 y N3: lo que sigue pasando y lo que ahora queda pendiente

`verificacion_entradas.py:456` (intervalo), `:449` («cifra)» sin «(»).

- **[Hecho]** `r5` B. Sigue leyéndose como intervalo, y por tanto en positivo, un entero de hasta cuatro cifras pegado por un guion a otro: «Saldo 2023-849» (que publica −849) vale para +849 y da discrepancia con −849; «Resultado financiero 1-149», igual. Entra en lo que proponía la segunda pasada («entero-entero»); en los textos reales no hay ningún importe negativo así (`n15`, igual).
- **[Hecho]** `r5` B. Quedan pendientes, y antes valían, rangos legítimos: «FY2023-2024» (el año con un prefijo pegado), «10000-20000» (más de cuatro cifras), «10.000-20.000», «7-7,5 %» y «1,5-2,5 millones». Es lo que pedía la propuesta para las cifras con decimales o miles; los otros dos casos van algo más allá.
- **[Hecho]** `r5` C. «cifra)» sin «(» se decide mirando si hay algún «(» antes en la línea: con otro paréntesis ya cerrado («(nota 5) 849,7)» y el «(» del negativo en la línea anterior) se lee en positivo (C3); y una cifra positiva al final de un inciso de dos líneas («(incluye amortización de⏎849,7)»), citada en su segunda línea, queda pendiente (C4).
- **Causa.** La regla del intervalo mira solo la forma de las dos cifras (enteros de una a cuatro cifras, el anterior sin nada pegado delante); la de «cifra)», si hay algún «(» en la línea.
- **[Propuesta]** Declararlo en el docstring de `_signo_en_cita`, junto a H3. Para «cifra)», contar los paréntesis sin cerrar en vez de buscar uno cualquiera.

### T9 · OBSERVACIÓN · N10 (relevo): dos restos y ninguna prueba nueva

`pipeline.py:373-378` y `:1095-1097`.

- **[Hecho]** `r16`, a nivel de unidad. Con el estado que deja el paso 13 (el relevo lleva `material_refijado`), el motivo de la solicitud nueva nombra el relevo, el relevo queda ligado a ella y una solicitud posterior por otra causa no lo arrastra. Una lista mal formada (texto, objeto, número, nulo, lista de textos) ya no da excepción.
- **[Hecho]** Restos: si `archivos_cambiados` del relevo no es una lista de textos, `TypeError` sin controlar; y un relevo anterior a esta candidata (ya con `solicitud` y sin `material_refijado`) recibe como `material_refijado` el siguiente material que fije el paso 13 por cualquier otra causa, que no es el suyo.
- **[Hecho, por lectura]** `test_relevo_i19_415.py` no cambia: prueba que la solicitud nueva comunica el relevo, no que no se arrastre ni el estado mal formado.
- **Causa.** `material_refijado` se anota en el último relevo que no lo tenga, sin mirar si ya tiene solicitud; y la forma del relevo no se valida por dentro.
- **[Propuesta]** Anotar `material_refijado` solo en un relevo sin `solicitud`; una prueba de unidad como `r16`.

### T10 · OBSERVACIÓN · Documentación y restos

`verificacion_entradas.py:124`, `:420`, `:422`, `:857` y `:1083-1084`; `esquema/ficha.esquema.json` (descripción del bloque `verificacion_entradas`); `pruebas/test_verificacion_entradas_415.py:385` y `:625`.

- **[Hecho]** Código sin uso: `MONEDAS` (`:422`) y, desde que se retiró `_igual`, `TOL_ABS` y `TOL_REL` (`:124`), cuyo comentario habla de una tolerancia de 0,0011 que ya no se aplica.
- **[Hecho]** Comentarios que no son ciertos, como en la segunda pasada: `:420` («siempre un signo menos (no se usa para imprimir un cero)»), el docstring de `_texto_html_visible` (`:857`, `aria-hidden`), el del módulo (fórmula constante en el punto real, sin la excepción del suelo).
- **[Hecho]** La descripción del bloque `verificacion_entradas` en `ficha.esquema.json` sigue diciendo que lo llevan «los expedientes con registro de entradas o declaración del modo (entrada_efectiva.json)»: no nombra las señales que añade N1.
- **[Hecho]** Cuando la discrepancia de N3 es una cifra ausente en el documento, el mensaje es el general («la cita no contiene el valor…») sin «(en el documento de la fuente, no en el texto conservado)» (`r4` C6, `n4` 4 y 8): se lee como si faltara en el texto conservado.
- **[Hecho]** En la candidata congelada, los límites que el autor declara (N8, H12, la parte de CSS de H7, m47) constan solo en `PUNTO_DE_RECUPERACION.md`; no están en el código ni en `HITO_2_4_15.md`, que es todavía el borrador de la primera candidata (`_pasaje_en_pagina`, `aria-hidden`, 141/52/4). `VERSION` y `CONTINUIDAD.md` dicen «hito 1 … sin I19, I20 ni F1». El autor lo tiene anotado como pendiente. **[Hecho, solo leído, fuera del material]** Mientras se hacía esta revisión la rama recibió dos commits posteriores (`01c6894` y `de5322f`: registro de la regresión y documentación de cierre) que actualizan esos cuatro documentos y listan esos límites en el registro del hito; no tocan `scripts/` ni `pruebas/` y no se han revisado.
- **[Hecho]** No es de este diff: `test_verificacion_entradas_415.py` calcula `HOY` al empezar y `sellar` vuelve a leer la fecha del sistema; una ejecución que cruza la medianoche se aborta (§6, incidencia). Una regresión completa lanzada poco antes de medianoche fallaría por eso.

### Las propuestas de T1 a T4, probadas juntas

No es código entregado ni revisado: es una comprobación de que lo que se propone es compatible con lo que hay. `sondas3/propuestas3.py` aplica las cuatro propuestas (ocho cambios en `verificacion_entradas.py`; el diff, de 47 líneas, está en `salidas/propuestas3_T1_T4.diff`) sobre una copia ligera, `fable/prop/`. Salidas en `salidas/propuestas/`.

- **[Hecho] Baterías permitidas con las propuestas:** 173/173, 60/60 y 33/33, código 0.
- **[Hecho] Registros reales con las propuestas:** el diagnóstico de los tres registros finales es idéntico byte a byte al entregado, y el inventario de signo, igual (1.645 «ok»). Los PDF reales (`r3`): las mismas 602 entradas pasan. Con el signo contrario, ningún «ok» (`n12`, `r10`, `r3`).
- **[Hecho] T1** (`r7b`): los importes con «tipo de cambio» o con una moneda tras la barra vuelven a pendiente; «USD por EUR», «EUR/USD» y «tipo de cambio EUR/USD» siguen sin quedar pendientes.
- **[Hecho] T2** (`r2`, `r2c`, `r10`): desaparecen los dieciséis rechazos en falso (queda C19, que ya estaba) y las 182 apariciones reales vuelven a «ok»; las citas cortadas dentro de un número siguen «ausente»; una cita cortada dentro de una palabra queda pendiente («Subtotal 849,7» citado «total 849,7»). `n2`: 0 casos distintos de lo esperado; `n4`, `n11`, `n12`, `r5`, `s2`, `s14`, `s15`, `s11`, `s21` y `s1`: mismos estados que esta candidata.
- **[Hecho] T3** (`r8`): A1–A5 y A10 vuelven a «ausente»; A8 y A9 pasan a «presente»; `cp875` e `iso-2022-kr`, pendientes; `ibm850` y `euc-kr` se siguen leyendo.
- **[Hecho] T4** (`r4b`): los casos 2 y 3 (PDF) quedan pendientes y los casos 4 y 5 (HTML), en discrepancia. El coste: el control 6 (el PDF publica la cifra en positivo con una palabra de la cita partida) queda pendiente; en los 602 datos reales no ocurre.
- No se han probado con la regresión completa ni con LibreOffice.

## 4. Lo cambiado que está bien

| Punto | [Hecho] | Sonda / salida |
|---|---|---|
| Baterías permitidas | En la copia: 173/173 (296 s), 60/60 (49 s) y 33/33 (49 s), código 0; ningún intento de lanzar LibreOffice. Los mínimos de `verificar_paquete.sh` (173, 60 y 5) coinciden | `salidas/bateria_*.log`, `baterias_rc.txt` |
| Pruebas existentes | En el diff de las dos baterías solo hay líneas añadidas (más la restauración del estado que exige la prueba nueva de N1); ninguna aserción anterior cambia. Las baterías del hito 1 pasan con este código: 105/105 y 40/40 | diff, `s20` |
| Contraejemplo externo y su variante | La sonda original de la revisión externa y la variante de la cita recortada: `apto_por_entradas=False`, igual que en la segunda pasada | `externa_sondas_original_sobre_tercera.json`, `s2b` |
| H1, sin regresión | `s2`, `s14`, `s15` y `s11`: mismas salidas que en la segunda pasada (cambian dos mensajes). `n12`: sobre las páginas reales, la línea completa, la cita con la línea siguiente y la cita cortada tras la cifra dan «ok» en todas (1.645, 1.645 y 327); la cifra sola queda pendiente en menos casos (de 70 a 21 sin marcas, de 49 a 12 con ellas); con el signo contrario, ningún «ok» | `n2`, `n12`, `r10` |
| N1 y N2 no cambian fichas cerradas | Los 12 expedientes cerrados del árbol generan la misma ficha y el mismo informe provisionales, byte a byte, con los dos códigos y con las dos configuraciones | `r9`, `r1` |
| N3 | Seis contraejemplos rechazados; de las 608 entradas reales con PDF, las 602 que pasan citando el texto pasan igual citando el PDF | `n4`, `r3`, `r4` |
| N4 | La cita «0», «…: 8», «7.000» o «…: 849» ya no acredita 849697 | `n2` C, `n11` a, `r5` A |
| N10, coste | 126 s → 2,4 s y 315 s → 2,0 s en la página de una sola línea con 2.000 y 5.000 apariciones de la cita | `n3` c |
| N10, relevo | Sin arrastre y sin excepción con la lista mal formada | `r16` |
| U6 en el árbol | `pipeline.modo_entrada_efectiva` da `('registrada', None)` en las 40 carpetas con los dos códigos | `n13` |
| Esquema | Las 104 fichas del árbol validan igual (el esquema no cambia) | `n10` |
| Empaquetado | Manifiesto conforme; `CAMBIOS_ARCHIVOS.txt` coherente con él | §0 |

## 5. Respuesta a las preguntas de esta pasada

1. **La cifra dentro de la cita y la cita como fragmento completo: ¿rechazos falsos en citas reales?** **[Hecho]** Ninguno en las páginas reales (`n12`, `r10`, §7). Ninguno nuevo en 24 formas de citas que empiezan o acaban en puntuación, paréntesis, símbolos o cifras con signo (`r2` C). Sí cuando la cita acaba o empieza justo en la cifra y la página lleva pegada una letra, una unidad, un código o una llamada de nota, o el rótulo va tras un punto pegado (T2).
2. **La clasificación «ausente» de una cita cortada.** **[Hecho]** Es correcta cuando el corte cae dentro de un número (`r2` D, `n2` B3, B4 y B6). Cuando cae junto a una letra, la cifra se publica entera y «discrepancia» no es la categoría (T2).
3. **La lectura adicional en el PDF o el HTML frente a diferencias legítimas con «pdftotext».** **[Hecho]** Ningún rechazo en los 602 datos reales con PDF ni en las formas sintéticas de columnas y celdas. Un caso conservador (columnas estrechas con otro extractor) queda pendiente. Y cuando la cita no se localiza en el documento, la lectura se omite (T4). Un negativo con los paréntesis en celdas aparte de un HTML («(», cifra, «)») no puede citarse como «(cifra)»: ya era así con la candidata anterior (`r4` B4).
4. **«cifra)» sin «(».** **[Hecho]** Queda pendiente, como se pretende; dos restos en T8.
5. **Intervalos.** **[Hecho]** Corregido lo que aceptaba el signo contrario con decimales; restos y rangos que pasan a pendiente en T8.
6. **N1 y N2 en la ficha.** **[Hecho]** No cambian la huella de ninguna ficha histórica cerrada (`r1`, `r9`; la regresión completa de la otra sesión, leída, pasa las cinco baterías del cierre). En el informe ya no hay bloques contradictorios; en la ficha queda uno interno (T7).
7. **El umbral de erratas de U6.** **[Hecho]** Quita cinco de los seis rechazos en falso y deja pasar el 22 % de las erratas dobles (T6).
8. **El relevo.** **[Hecho]** `material_refijado` hace lo que se pretende y el estado mal formado ya no rompe; dos restos y ninguna prueba (T9).
9. **Tipos de cambio en U7.** **[Hecho]** Los tipos de cambio ya no quedan pendientes; con ellos salen de U7 importes (T1).

## 6. Mutaciones

Una regla quitada o alterada cada vez, en un árbol ligero aparte (`sondas3/mutaciones3.py`, sobre el arnés de la segunda pasada; resultados en `fable/mut3/<nombre>/resultado.json`). Baterías: las tres permitidas, las que correspondan a cada regla. El control sin cambio de regla pasa entero (60/60, 33/33 y 173/173).

**[Hecho]** 55 mutaciones y 68 ejecuciones de batería; todas terminan con código 0 o 1, cada detección lleva sus líneas FALLA (una, `u6e`, aborta la batería con el `ValueError` de la regla alterada) y ninguna queda sin resultado.

- **Reglas nuevas de esta candidata (31):** 17 detectadas y 14 no.
- **Las que el autor declara cubiertas ahora (9) y `h9d`:** las nueve, detectadas; `h9d`, no.
- **Las otras que la segunda pasada dejó sin detectar (13):** ninguna se detecta.

**[Hecho] Incidencia.** Una ejecución (`h6e`) cruzó la medianoche UTC y la batería se abortó sin resultado: calcula `HOY` al empezar (`test_verificacion_entradas_415.py:385`) y `sellar` vuelve a leer la fecha del sistema, así que en `:625` sale con «sellar solo sella la revisión de hoy (2026-11-16); la fecha '2026-11-15' no lo es». Se descartó y se repitió. Por precaución se repitieron también `h7g`, que había empezado a las 23:59 (mismo resultado las dos veces), y el control, que el día 16 pasa entero igual que el 15 (60/60, 33/33 y 173/173). No es de este diff (T10).

| Mutación | Hallazgo | Qué se quita o altera | Resultado | Baterías |
|---|---|---|---|---|
| `c00_control` | — | control: sin cambio de regla (solo un comentario); las baterías tienen que pasar enteras en el árbol ligero | pasa entera | entrada efectiva: 60/60; entradas 4.14: 33/33; entradas 4.15: 173/173 |
| `n4_solapa` | N4 | la cifra vuelve a valer con que la cita la TOQUE (solapamiento), sin tener que estar dentro | **NO detectada** | entradas 4.15: 173/173; entrada efectiva: 60/60 |
| `n5a_intervalo_cualquiera` | N5 | cualquier guion pegado entre dos cifras vuelve a leerse como intervalo (+1), como antes de la corrección | detectada | entradas 4.15: 172/173, fallan 1 («(N4, N5, N10) la cifra tiene que estar dentro de la cita; «T4-15,2» y «2023-849,…») |
| `n5b_sin_entero_despues` | N5 | el intervalo ya no exige que la cifra que sigue al guion sea un entero de 1 a 4 dígitos («2023-849,7» vuelve a ser positivo) | detectada | entradas 4.15: 172/173, fallan 1 («(N4, N5, N10) la cifra tiene que estar dentro de la cita; «T4-15,2» y «2023-849,…») |
| `n5c_sin_limite_antes` | N5 | el intervalo ya no exige que el entero anterior al guion sea un número completo («T4-15» o «1.234-567» se leen como intervalo) | **NO detectada** | entradas 4.15: 173/173 |
| `n10a_sin_limites` | N10 | la cita vuelve a buscarse como subcadena (sin límites de fragmento completo ni al principio ni al final) | detectada | entradas 4.15: 172/173, fallan 1 («(N4, N5, N10) la cifra tiene que estar dentro de la cita; «T4-15,2» y «2023-849,…»); entrada efectiva: 60/60 |
| `n10a1_sin_limite_inicial` | N10 | la cita puede empezar dentro de una palabra o de una cifra de la página (sin el límite inicial) | **NO detectada** | entradas 4.15: 173/173; entrada efectiva: 60/60 |
| `n10a2_sin_limite_final` | N10 | la cita puede acabar dentro de una palabra o de una cifra de la página (sin el límite final) | **NO detectada** | entradas 4.15: 173/173; entrada efectiva: 60/60 |
| `n10b_cierre_sin_apertura` | N10 | «cifra)» sin «(» en la línea vuelve a leerse como positivo | detectada | entradas 4.15: 172/173, fallan 1 («(N4, N5, N10) la cifra tiene que estar dentro de la cita; «T4-15,2» y «2023-849,…») |
| `n10c_sin_recorte_400` | N10 | se quita el recorte del contexto a 400 caracteres (coste con una línea muy larga) | **NO detectada** | entradas 4.15: 173/173 |
| `n10d_cortada_no_localizada` | N10/R3 | una cita que solo está como fragmento de una palabra o de una cifra vuelve a ser «no_localizada» (pendiente), no «ausente» (discrepancia) | detectada | entradas 4.15: 169/173, fallan 4 («(H1/R3) cita cortada dentro de un número (la página publica 8496970 y la cita «……»); entrada efectiva: 60/60 |
| `n3a_sin_lectura_documento` | N3 | la cifra y su signo dejan de leerse en el PDF o el HTML (solo en el texto conservado, como antes) | detectada | entradas 4.15: 172/173, fallan 1 («(N3) fuente PDF cuyo texto conservado perdió el signo menos y cita recortada a l…») |
| `n3b_html_no_se_lee` | N3 | la lectura adicional se hace en el PDF pero no en el HTML | **NO detectada** | entradas 4.15: 173/173 |
| `n3c_solo_signo_distinto` | N3 | del documento solo cuenta un signo distinto (una cifra ausente o un signo indeterminado en el documento se ignoran) | **NO detectada** | entradas 4.15: 173/173 |
| `n3d_solo_layout` | N3 | del PDF solo se lee el texto con «-layout» (no el del orden de lectura) | **NO detectada** | entradas 4.15: 173/173 |
| `n3e_solo_sin_layout` | N3 | del PDF solo se lee el texto sin «-layout» | **NO detectada** | entradas 4.15: 173/173 |
| `n6a_sin_xhtml` | N6 | se quita el modo XHTML (un elemento autocerrado no vacío vuelve a ocultar lo que sigue) | detectada | entradas 4.15: 172/173, fallan 1 («(N6) XHTML con &lt;script/> y &lt;div style=display:none/> autocerrados no oculta lo q…») |
| `n6b_summary_hidden_visible` | N6 | un &lt;summary hidden> de un &lt;details> cerrado vuelve a darse por visible | detectada | entradas 4.15: 172/173, fallan 1 («(N6) XHTML con &lt;script/> y &lt;div style=display:none/> autocerrados no oculta lo q…») |
| `n6c_sin_codecs_nuevos` | N6 | ibm850, cp866, cp874, euc-kr e iso-2022 vuelven a quedar pendientes | detectada | entradas 4.15: 172/173, fallan 1 («(N6) XHTML con &lt;script/> y &lt;div style=display:none/> autocerrados no oculta lo q…») |
| `n6d_xhtml_siempre` | N6 | todo documento se trata como XHTML (en HTML, «&lt;div hidden/>» deja de ocultar lo que sigue) | detectada | entradas 4.15: 172/173, fallan 1 («(H7) HTML: details cerrado, summary de un details cerrado, dialog sin open, &lt;div…») |
| `n9a_sin_tipo_cambio` | N9 | un tipo de cambio («USD por EUR») vuelve a ser una unidad monetaria no reconocida | detectada | entradas 4.15: 172/173, fallan 1 («(N9) un tipo de cambio («USD por EUR», «EUR/USD») no es una unidad monetaria sin…») |
| `n9b_tratamiento_literal` | N9 | el tratamiento vuelve a compararse literalmente («Ninguno.» pasa) | detectada | entradas 4.15: 172/173, fallan 1 («(N9) signo −1 con el tratamiento «Ninguno.»: error, como «ninguno» · ['discrepan…») |
| `n9c_cualquier_mencion_tipo_cambio` | N9 | control inverso: la exención del tipo de cambio se amplía a cualquier unidad con una barra o «por» («€/MWh», «EUR por tonelada» dejan de quedar pendientes) | **NO detectada** | entradas 4.15: 173/173 |
| `n1a_sin_senal_estado` | N1 | el bloque de I20 deja de depender del modo registrado por el paso 2 en estado_pipeline.json | detectada | entrada efectiva: 59/60, fallan 1 («(hito 2, N1) sin registro de entradas ni entrada_efectiva.json pero con el modo…») |
| `n1b_sin_declara_modo` | N1 | el bloque de I20 deja de depender del modo declarado en alcance_v2.json o fase1_metadatos.json | **NO detectada** | entrada efectiva: 60/60 |
| `n1c_ilegible_no_declara` | N1 | un alcance_v2.json o fase1_metadatos.json ilegible deja de hacer que se muestre el bloque | **NO detectada** | entrada efectiva: 60/60 |
| `n2a_aptitud_sin_modo` | N2 | aptitud_de_uso vuelve a ignorar el motivo del modo (el párrafo de la V6.4 dice «sí» con el modo distinto) | detectada | entradas 4.15: 172/173, fallan 1 («(hito 2, H9 y N2) registro apto con el modo aplicado («registrada») distinto del…»); entrada efectiva: 60/60 |
| `n2b_resumen_sin_actualizar` | N2 | con el modo distinto, el resumen de aptitud_de_uso sigue diciendo apto_por_entradas = true (solo cambia el motivo) | detectada | entradas 4.15: 172/173, fallan 1 («(hito 2, H9 y N2) registro apto con el modo aplicado («registrada») distinto del…») |
| `n2c_motivos_sin_modo` | N2 | con el modo distinto, motivos_no_apto no da el motivo (apto_e no se pone a False; el resumen sí) | **NO detectada** | entradas 4.15: 173/173 |
| `u6e_umbral_080` | N9/U6 | el umbral de erratas de la clave vuelve a 0,8 («tasa_efectiva» vuelve a ser un error) | detectada | entrada efectiva: abortada (ValueError: alcance_v2.json tiene la clave 'tasa_efectiva', que parece) |
| `u6f_umbral_097` | N9/U6 | el umbral de erratas sube a 0,97 (una errata de una letra, «entrada_efectiba», deja de detectarse) | detectada | entrada efectiva: 59/60, fallan 1 («(hito 2, U6 b y c) erratas de la clave en alcance_v2.json, alcance ilegible o qu…») |
| `u6g_umbral_092` | N9/U6 | el umbral de erratas sube a 0,92 (dos erratas o una clave con sufijo dejan de detectarse; una letra, todavía) | **NO detectada** | entrada efectiva: 60/60 |
| `h1g_calc_sin_pagina` | H1/N7 | calcular_entrada lee la cifra y el signo del componente en la cita, no en la página | detectada | entrada efectiva: 59/60, fallan 1 («(hito 2, H1) el cálculo del hito 1 con cada cita recortada a la cifra («130,8» f…») |
| `h9a_modo_distinto_no_impide` | H9/N7 | un modo aplicado distinto del declarado (o una declaración con error) deja de impedir «apto por entradas» en el bloque de I20 | detectada | entrada efectiva: 60/60; entradas 4.15: 172/173, fallan 1 («(hito 2, H9 y N2) registro apto con el modo aplicado («registrada») distinto del…») |
| `h9d_error_declaracion_no_impide` | H9/N7 | una declaración del modo con error deja de impedir «apto por entradas» | **NO detectada** | entrada efectiva: 60/60; entradas 4.15: 173/173 |
| `m12_tolerancia_0_00055` | H11 | (m12) tolerancia de importes ampliada a 0,00055 | detectada | entradas 4.15: 172/173, fallan 1 («(H11, m12) importe: 849,69751 no es 849,697 (la distancia admitida es exactament…») |
| `m16_sin_limite_nodos` | H11 | (m16) sin límite de nodos de la fórmula | detectada | entradas 4.15: 172/173, fallan 1 («(H11, m16 y m17) los límites de nodos y de longitud de la fórmula actúan cada un…») |
| `m17_sin_limite_longitud` | H11 | (m17) sin límite de longitud de la fórmula | detectada | entradas 4.15: 172/173, fallan 1 («(H11, m16 y m17) los límites de nodos y de longitud de la fórmula actúan cada un…») |
| `m20_sin_constante_local` | H6/H11 | (m20) se quita el error «constante en el punto real» | detectada | entradas 4.15: 172/173, fallan 1 («(H11, m20) una fórmula constante en el punto real (min(a + b, 1) con a + b > 1):…») |
| `m22_cero_exento_en_todo` | H11 | (m22) el 0 queda exento en cualquier posición de la fórmula, no solo en min/max | detectada | entradas 4.15: 172/173, fallan 1 («(H11, m22) el 0 solo es una constante admitida como argumento de min o max…») |
| `h7k_pdf_cabecera_al_principio` | H7/H11 | (m29) el tipo PDF exige la cabecera al principio (un PDF con bytes previos y sin extensión deja de reconocerse) | detectada | entradas 4.15: 172/173, fallan 1 («(H11, m29) un PDF con bytes previos y sin extensión es un PDF (la cabecera puede…») |
| `h6f_local_solo_arriba` | H6 | la perturbación local vuelve a ser solo hacia arriba | detectada | entradas 4.15: 172/173, fallan 1 («(H6) min(a, b) con a = b: los dos influyen en el punto real hacia abajo (la pert…») |
| `h1e_no_localizada_vale` | H1 | contraste_pagina da por buena una cita «no_localizada» (ni pendiente ni discrepancia) | **NO detectada** | entradas 4.15: 173/173 |
| `h1f_sin_ventana` | H1 | se leen todas las cifras de la línea, no solo las de la cita (sin ventana) | **NO detectada** | entradas 4.15: 173/173; entrada efectiva: 60/60 |
| `h6a_semilla_por_formula` | H6 | la semilla vuelve a depender del texto de la fórmula | **NO detectada** | entradas 4.15: 173/173 |
| `h6b_sin_puntos_extremos` | H6 | se quitan los puntos extremos (±10⁹) de cada origen | **NO detectada** | entradas 4.15: 173/173 |
| `h6c_sin_suelo_cero` | H6 | se quita la excepción del suelo cero (max(a − b, 0) cuando actúa vuelve a ser error) | **NO detectada** | entradas 4.15: 173/173 |
| `h6d_suelo_sin_exigir_cero` | H6 | la excepción del suelo vale aunque el resultado no sea 0 | **NO detectada** | entradas 4.15: 173/173 |
| `h6e_cero_sin_suelo` | H6 | una fórmula constante en el punto real vale siempre que el resultado sea 0, tenga o no un suelo en cero | **NO detectada** | entradas 4.15: 173/173 |
| `h7g_ix_no_en_linea` | H7 | las etiquetas con espacio de nombres (ix:nonFraction) dejan de tratarse como en línea | **NO detectada** | entradas 4.15: 173/173 |
| `h7m_sin_quitar_guion_blando` | H7 | el guion blando y el espacio de ancho cero dejan de quitarse al comparar | **NO detectada** | entradas 4.15: 173/173 |
| `h7n_sin_etiquetas_en_linea_nuevas` | H7 | &lt;ins>, &lt;del>, &lt;label>, &lt;big> y &lt;tt> dejan de ser en línea | **NO detectada** | entradas 4.15: 173/173 |
| `h14b_esquema_dinero_real` | H14 | el esquema deja de fijar aptitud_de_uso.apto_para_dinero_real en false | **NO detectada** | entrada efectiva: 60/60; entradas 4.15: 173/173; entradas 4.14: 33/33 |
| `i20b_bloque_sin_declaracion` | I20 | la ficha no lleva el bloque con solo entrada_efectiva.json (sin registro ni señales del estado o del alcance) | **NO detectada** | entrada efectiva: 60/60 |
| `m47_u1_informe_sin_derivados` | H11 | (m47) el informe V6.4 no dice cuántos derivados comprobados hay | **NO detectada** | entradas 4.15: 173/173 |

## 7. Registros reales

- **[Hecho] Diagnóstico** (`…_4_15/scripts/diagnostico_registros_4_14.py`, con `python3 -I -B`) de los tres registros finales con el código de esta candidata y con el de la anterior: idénticos entre sí y, byte a byte, a `hito2/resultados/diagnostico_registros_4_14_con_reglas_hito2.json`: Viscofan 214/232 (1 error, 17 discrepancias), Vidrala 207/226 (4 errores, 15 discrepancias, 1 entrada no reproducible), Elis 175/193 (1 error, 17 discrepancias, 1 entrada no reproducible). Los otros cuatro registros del árbol dan también lo mismo con los dos códigos (`viscofan` 211/232, `vidrala` 204/226, `elis_motor_A` 169/193 y `vidrala_decisiones_INVALIDO…` 186/226). Salidas: `diagnostico_reales_codigo_{copia,prev}.json`, `diag4_*.json`, `diag4b_*.json`.
- **[Hecho] Inventario de signo** (`…/hito2/scripts/inventario_signo_registros.py`) de los siete registros: 1.645 entradas numéricas con página, todas «ok» (526 negativas, 1.082 positivas y 37 ceros), igual con los dos códigos e idéntico byte a byte al entregado (`hito2/resultados/inventario_signo_registros_reales.json`).
- **[Hecho] PDF reales** (`r3`, que amplía la parte B de `q12_pdf.py` de la tercera pasada del hito 1 a Vidrala y a los dos códigos). Cada entrada se contrasta citando el `.txt` y citando el PDF con el `.txt` como `archivo_texto`:

  | Expediente | Entradas con fuente `texto/…` y PDF | Pasan citando el `.txt` | Pasan citando el PDF, 92b2362 | Pasan citando el PDF, f3d15e8 | Rechazadas solo por N3 |
  |---|---|---|---|---|---|
  | Elis | 247 | 244 | 244 | 244 | 0 |
  | Viscofan | 228 | 225 | 225 | 225 | 0 |
  | Vidrala (PDF de 2016–2022) | 133 | 133 | 133 | 133 | 0 |

  Sobre el PDF, la línea completa pasa en las 602; la cifra sola pasa o queda pendiente (menos pendientes que antes); con el signo contrario no pasa ninguna, en ninguna variante. La parte B de `q12_pdf.py`, ejecutada tal cual con los dos códigos, da lo mismo para Elis y Viscofan (244 y 225; 0 rechazadas solo por el control del PDF).
- **[Hecho] Citas alternativas y diferencial sobre las páginas reales** (`n12`, `r10`): véase §4 (H1). Con el signo contrario al real no hay ningún «ok» en ninguna variante ni con ningún corte.
- **[Hecho] Ninguna regla nueva toca una entrada real.** U7 y H14: `s3d` igual; las unidades de los registros no cambian de trato (`n8` A). U6: `n13`. N1: `r1` y `r9`. Derivados: los 148 siguen igual (`s18`). C48 de Elis: 108,0 con el texto de fuente completo (`s13`, igual).

## 8. Lo que no se ha hecho

- Nada con LibreOffice ni con el pipeline. La parte del relevo de N10 se ha revisado por lectura y a nivel de unidad (`r16`); `test_relevo_i19_415.py` no se ha ejecutado.
- **[Hecho, solo leído]** La regresión completa de esta candidata la ejecutó otra sesión sobre una copia con las mismas huellas de código (`scratchpad/reg3/`, que no es material de esta revisión ni está en el árbol congelado): empezó a las 22:34 UTC y terminó a las 23:30 UTC con «RESULTADO GLOBAL: PASA», código 0, 56 min 1 s y todos los bloques en PASA (entre ellos 173/173, 60/60, 33/33, 5/5 del relevo, 199/199 de integración, 78/78 de trazabilidad y las cinco baterías del cierre: 103/103, 55/55, 28/28, 45/45 y 55/55). El revisor no la ha reproducido. Sus sondas y mutaciones corrieron a la vez en la misma máquina, con prioridad baja.
- No se ha comprobado el «control de la entrega 4.14: 29/35» que cita el punto de recuperación.
- De `q12_pdf.py` (tercera pasada del hito 1) solo se ha ejecutado la parte B, la de los PDF reales.
- No se han repetido `s3b` y `s5` de la primera pasada: llaman a funciones retiradas antes de la segunda pasada y lo que prueban (la regla de la columna en los registros reales, U2) no cambia en este diff; `s3e` y `s3`, que cubren lo primero, dan lo mismo. `s4` y `s12` tampoco (`cierre_v2.py` no cambia; el manifiesto se comprobó directamente).
- Las propuestas de T1 a T4 se han probado con las tres baterías permitidas y con los registros reales (§3, al final), no con la regresión completa. Las de T5 a T10 no se han probado.
- No se ha revisado el sentido económico de ningún dato, de F1 ni del 108 de C48.
- `html.parser` solo se ha probado con Python 3.13.18, 3.12.3 y 3.11.18.

## 9. Integridad del árbol congelado

- **[Hecho]** Listado de huellas SHA-256 de los 7208 archivos del árbol congelado al empezar (15-nov-2026, 22:35 UTC; `fable/huellas_arbol_congelado_inicio.txt`), en una comprobación intermedia (23:36 UTC) y al terminar (16-nov-2026, 00:30 UTC; `fable/huellas_arbol_congelado_fin.txt`): idénticos (SHA-256 de los listados: `3d46d78a…982aee01`). Ningún archivo ni carpeta del árbol tiene fecha posterior al inicio de la revisión, y el manifiesto sigue conforme al terminar.
- **[Hecho]** La copia ligera (`fable/copia/`) tiene al terminar sus `scripts/`, `pruebas/` y `esquema/` idénticos a los del árbol congelado (`diff -rq`) y sin `__pycache__`: todas las sondas se ejecutaron contra el código congelado tal cual. `fable/prev/` tiene las huellas que la segunda pasada anotó para 92b2362.
- **[Hecho]** `/home/user/munger-v2` solo se ha leído (`git diff`, `git archive`, `git show`). Al terminar, `git status` está limpio y la rama está en `de5322f`, dos commits después de la candidata; los hizo otra sesión durante esta revisión (T10) y no se han revisado.
- **[Hecho]** `fable/salidas/INTENTOS_SOFFICE.log` no existe: ninguna sonda ni batería intentó lanzar LibreOffice.
- **[Hecho]** Huellas de referencia de lo revisado (primeros y últimos 8 caracteres): `verificacion_entradas.py` `c52017d6…d5ed0de0`; `ficha.py` `9df65269…c3ed0852`; `pipeline.py` `466acd7e…9e4a4586`; `informe.py` `eabe0546…c083a43d`, `cierre_v2.py` `6d89a81a…b379c813`, `fase1_historia.py` `b74494db…f67e90b2` y `ficha.esquema.json` `eefed485…b81cc165` (los cuatro, sin cambio); `test_verificacion_entradas_415.py` `ad95e234…519ef303`; `test_entrada_efectiva_415.py` `7969e6a2…3e7224d5`; `test_verificacion_entradas_414.py` `e14147d0…ca07724f`, `test_relevo_i19_415.py` `663a9225…8b58dea4` y `test_cierre_v2.py` `970cc094…8f389c87` (sin cambio); `verificar_paquete.sh` `5934a411…6791e6dc`; `MANIFIESTO_SHA256.txt` `188dc634…854b9a35`; `CAMBIOS_ARCHIVOS.txt` `a1226b59…6e76d155`; `DIFF_ESTABLE_A_TERCERA.diff` `af4ca571…b2f2afaa`. De 92b2362 (`fable/prev/`): `verificacion_entradas.py` `99de635e…404ae6aa`, `ficha.py` `53046986…625fd5de`, `pipeline.py` `d3817251…a9721be5`.

## 10. Índice de sondas

Todo en `/tmp/claude-0/-home-user-munger-v2/ace24ef4-365c-50f9-bb78-93416041e669/scratchpad/rev3/fable/`. Salidas en `salidas/`, con el nombre de la sonda y extensión `.log` (las ejecutadas con el código de 92b2362, con el sufijo `_anterior`).

**Sondas nuevas** (`sondas3/`; `comun3.py` es su arnés: carga `verificacion_entradas` de las dos candidatas en el mismo proceso):

| Sonda | Qué prueba | Hallazgo |
|---|---|---|
| `r1_bloque_fichas_historicas.py` | la condición nueva del bloque de I20 en las 96 carpetas del árbol | N1 |
| `r2_limites_de_la_cita.py` | 57 citas en el límite: algo pegado a la cifra, puntuación, paréntesis, símbolos, signo, cortes dentro de un número; y el mensaje en el registro | T2, N4, N10 |
| `r2b_tokens_pegados_fuentes_reales.py`, `r2c_tokens_pegados_pagina_real.py` | cuántas cifras de los 34 textos reales llevan algo pegado y qué hace la regla con ellas | T2 |
| `r3_pdf_reales.py`, `r3b_pdf_reales_localizacion.py` | N3 con los PDF reales de Elis, Viscofan y Vidrala; en cuántas entradas se hace la lectura en el documento | N3, T4, §7 |
| `r4_n3_documento.py`, `r4b_n3_no_localizada.py` | N3 en el registro con PDF y HTML sintéticos: columnas, celdas, y la cita que no se localiza | N3, T4, T8 |
| `r5_n4_n5_n10_unidad.py` | N4 (lo que solo decide esa regla), intervalos y «cifra)» | N4, T5, T8 |
| `r6_u6_umbral.py` | erratas de una y dos ediciones con los umbrales 0,8 y 0,88 | T6 |
| `r7_u7_tipo_de_cambio.py`, `r7b_u7_registro.py` | la exención del tipo de cambio, unidad a unidad y en el registro con los dos códigos | T1 |
| `r8_html_xhtml_codecs.py` | el modo XHTML por contenido y las codificaciones admitidas | T3 |
| `r9_fichas_historicas.py` | ficha e informe provisionales de los 12 expedientes cerrados con los dos códigos | N1, N2 |
| `r10_diferencial_reales.py` | 12.864 citas generadas sobre las líneas reales, con los dos códigos y los dos signos | T2, §4 |
| `r16_relevo_unidad.py` | el relevo con `material_refijado`, a nivel de unidad | N10, T9 |
| `mutaciones3.py`, `mutaciones3_resumen.py` | mutaciones (§6); tabla en `salidas/mutaciones3_tabla.md` | T5, N7, H11 |
| `propuestas3.py` | aplica juntas las propuestas de T1 a T4 sobre `fable/prop/`; baterías y sondas con ellas, en `salidas/propuestas/` | §3, al final |
| `sondas_hito1/q12_pdf.py` (parte B, sin cambios) | PDF reales de Elis y Viscofan, como en la tercera pasada del hito 1 | §7 |

**Sondas de la segunda pasada, repetidas** (`sondas2/`): `n1`, `n9`, `n14`, `n15` y `n10` dan la misma salida; `n13`, igual con los dos códigos; `n17`, igual (las cinco carpetas con solo la clave del paso 12 no cambian con la condición que se adoptó); `n2`: 0 casos distintos de lo esperado (antes 6: B3, B8 y C1–C4); `n3`: coste; `n4`: los seis casos, rechazados; `n5`: N1 y N2; `n6`: de 16 a 7 señalados; `n7`: 27 bien, 13 pendientes en falso, 5 ambiguos aceptados (antes 25, 9, 7 y 4 que aceptaban el contrario); `n8`: N9; `n11`: N4 y N10; `n12`: §4; `n16`: su estado sintético no lleva `material_refijado` y por eso ya no muestra el motivo (lo sustituye `r16`).

**Sondas de la primera pasada, repetidas** (`sondas/`): `s2`, `s14`, `s15`, `s11`, `s1b`, `s21`, `s13`, `s19`, `s16`, `s17`, `s6`, `s18`, `s3`, `s3c`, `s3d`, `s3e`, `s9`, `s10`, `s7`, `s7b`, `s8`, la sonda externa original y `s2b`: misma salida que en la segunda pasada (en `s2` cambian dos mensajes y en `s9` los números de línea). `s1`: «149,5)» pasa a pendiente (24 de 70). `s20`: 40/40 y 105/105.
