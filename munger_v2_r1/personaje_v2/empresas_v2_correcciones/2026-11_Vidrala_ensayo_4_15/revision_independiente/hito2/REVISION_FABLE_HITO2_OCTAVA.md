# Revisión independiente del hito 2 de la 4.15 · octava comprobación, dirigida (candidata 0a0020b)

Revisor: Fable (Claude, contexto separado del autor del cambio; no es una revisión humana ni sustituye a la externa) · 16-nov-2026.
Convención: **[Hecho]** = comprobado por el revisor ejecutando o leyendo (se dice cuál); **[Interpretación]** = lectura del revisor; **[Propuesta]** = corrección sugerida. Lo que no se ha ejecutado se dice expresamente.
El sistema es experimental y supervisado. Nada de lo que sigue acredita aptitud para dinero real, ni esta revisión tampoco.
Alcance: comprobación dirigida y breve. Solo lo cambiado entre la candidata de la séptima comprobación (45ff57c) y esta (0a0020b): el carácter de X1, las pruebas de X2, X5 con su prueba (cambio nuevo, no revisado antes por nadie), el mínimo 61→62 de `verificar_paquete.sh` y el registro corregido (X3). No se repite la revisión completa ni se revisa el sentido económico de ningún dato, de F1 ni del 108 de C48.

**ESTADO DE ESTE DOCUMENTO: DEFINITIVO.** Todas las ejecuciones que se citan han terminado (08:02–08:38 UTC) y la comprobación de integridad final está hecha (§5).

## 0. Qué se ha revisado y cómo

- **Material:** el árbol congelado `rev8/munger_v2_r1` (commit 0a0020b; solo lectura); el cambio de código `git diff 45ff57c 0a0020b -- …/scripts …/pruebas verificar_paquete.sh` (99 líneas, cinco archivos, leído entero; guardado en `salidas8/DIFF_SEPTIMA_A_OCTAVA_codigo.diff`, SHA-256 `e1fa95ef…bc1e58db`); el informe en borrador de la séptima comprobación con `sondas7/` y `salidas7/`; los árboles de trabajo de la séptima (`rev7/fable/`, solo lectura, como referencia); y el registro (`hito2/HITO_2_4_15.md`, `hito2/PUNTO_DE_RECUPERACION.md`, `CONTINUIDAD.md` §1 y la lista de baterías, `VERSION`, `PROMPT_NUEVA_VENTANA.md`), leído como declaración del autor y comprobado (§2.5).
- **[Hecho] El manifiesto es conforme:** 7683 entradas, 7683 huellas iguales, 0 distintas, 0 ausentes, 0 archivos de más (el árbol tiene 7684 archivos: los 7683 y el propio manifiesto). `CAMBIOS_ARCHIVOS.txt` coincide con él (36 modificados y 7006 nuevos, todas las huellas iguales).
- **[Hecho] El árbol congelado es el commit 0a0020b** en los siete archivos comprobados uno a uno con `git show` (los cinco de código que cambian, `test_verificacion_entradas_414.py` y `test_comprobadores.py`; `h6` y la tabla de huellas al construir los árboles).
- **[Hecho] El material de la séptima no se ha retocado:** el informe que va en el árbol es, byte a byte, el borrador que dejó el revisor en `rev7/fable/`; `sondas7/` es idéntico al suyo; los 13 `resultado.json` de `salidas7/mut7/` son los de sus mutaciones.
- **Dónde se ha trabajado:** todo en `rev8/fable/`, sin copias completas: `copia/` (árbol ligero de esta candidata: `scripts/`, `pruebas/` y `esquema/` copiados; el resto, enlaces simbólicos al árbol congelado, que solo se lee), `prev/` (lo mismo con el código de 45ff57c, sacado con `git archive`), `mut8/` (mutaciones) y `fix8t/` (una propuesta opcional de pruebas, Y3). `/home/user/munger-v2` solo se ha leído (`git diff`, `show`, `archive`, `blame`, `log`, `status`, `rev-parse`).
- **[Hecho] No se ha lanzado LibreOffice, `pipeline.py` ni `verificar_paquete.sh`.** Todas las sondas y baterías llevan delante en el `PATH` un sustituto de `soffice` que registra el intento y termina con 1: no hay ningún intento registrado (`salidas8/INTENTOS_SOFFICE.log` no existe). De `verificar_paquete.sh` solo se ha analizado la sintaxis (`bash -n`).
- **Una desviación respecto del encargo, que se declara:** `test_comprobadores.py` figuraba entre las baterías permitidas (esperado 114/114), pero dos de sus cinco partes (`h1_recorrido` y `h1_reutilizacion`) lanzan `pipeline.py` y LibreOffice (`pruebas/test_comprobadores.py:236`, `:465`, `:499`; lo dice también `CONTINUIDAD.md:128`). Como eso está prohibido en esta pasada, **solo se han ejecutado las partes `h2`, `h1` y `h3`** (76 de las 114 comprobaciones). El 114/114 no se ha reproducido (§2.3 y §4).
- **Datos reales y sintéticos:** donde dice «real» se han leído las extracciones `fase1_partes/`, los textos conservados, los siete registros `verificacion_entradas.json` de la 4.14 y los PDF del árbol; lo demás es texto construido por el revisor o el fixture sintético de las baterías. Los contraejemplos sintéticos demuestran lo que el control acepta o rechaza, no que los datos reales lo hagan: **no lo hacen** (§2.2 y §2.4).

## 1. Dictamen

**ACEPTABLE CON CORRECCIONES, solo de declaración en el registro. No se exige ningún cambio de código.** El código y las pruebas de X1, X2 y X5 son conformes; lo que falta es que el registro diga, para el control de la fase 1 que X5 ha tocado, lo mismo que ya dice para la verificación de las entradas (Y1), y una frase inexacta (Y4 a).

- **[Hecho] X1 y X2: CONFORME.** La verificación mecánica que dejó la séptima (`sondas7/verificar_correccion_x1.py`, ejecutada tal cual sobre el árbol congelado) termina «CONFORME», código 0. `verificacion_entradas.py` tiene la huella `4b00aa2a42ae45743ef4f31669faad36a7effb81affe828fd4975a2ca98c86cd`. Ese archivo y `test_verificacion_entradas_415.py` son, byte a byte, los del árbol `fix7` que la séptima probó, y los que salen de aplicar `sondas7/propuestas7.py` a 45ff57c. En el código cambia **un carácter** de la línea 542. Con la batería entera, las dos mutaciones de esa línea que en la séptima pasaban 190/190 ahora se detectan (`v7c` y el descuido de X1: 189/190 y código 1 las dos).
- **[Hecho] X5: conforme.** `importe_completo` cierra lo que X5 señalaba («849,7» dentro de «1'849,7» y de «1’849,7»; «849» dentro de «849'697» y de «849’697») y sus variantes; **no abre nada**: en 751.144 pares (importe, texto) recorridos de forma exhaustiva, el código nuevo nunca acepta lo que el anterior rechazaba, y sin apóstrofo en el texto los dos coinciden siempre. **Ningún rechazo falso en datos reales:** en los 32 expedientes con `fase1_partes/` (320 años, 17.956 componentes), `comprobar_anio` da los mismos errores y los mismos ceros pendientes con los dos códigos, e `importe_completo` da lo mismo en cada línea y en cada página; en los 45 textos conservados distintos (283 archivos) no hay ninguna «cifra + apóstrofo + cifra»; C48 de Elis se reconstruye en 108,0. **La prueba nueva detecta las mutaciones pedidas** (sin el cambio, solo delante, solo detrás, solo ASCII, solo tipográfico): a nivel de unidad, esas cinco y cuatro más; con la batería entera, esas cinco y dos más (61/62 y código 1 en las siete).
- **[Hecho] Baterías sobre el árbol:** entradas 4.15 **190/190**, entrada efectiva **62/62**, entradas 4.14 **33/33**, código 0, ninguna línea FALLA. `test_comprobadores.py`, solo las partes sin LibreOffice: **76/76** (H2 39, H1 23, H3 14).
- **[Hecho] Registros reales:** el diagnóstico de los tres registros finales y el inventario de signo son idénticos byte a byte a los entregados; `q12_pdf.py` B: 244 y 225, 0 rechazadas.
- **[Hecho] El registro corregido:** los ocho puntos de X3, (a)–(h), están resueltos, y lo que ahora dicen §1 y §5 de `HITO_2_4_15.md` coincide con lo que hace el código en las 47 formas probadas. **Ninguna afirmación da por cerrado lo pendiente.** Falta lo de Y1; hay tres precisiones menores (Y4).
- **[Hecho] El cambio de código se limita a lo declarado:** cinco archivos; en `verificacion_entradas.py`, un carácter; en `fase1_historia.py`, solo la función `importe_completo` (docstring y expresión); en las dos baterías, solo las sentencias de X2 y la prueba de X5; en `verificar_paquete.sh`, «61» → «62» en tres líneas.

**¿Hace falta cambiar código?** [Interpretación] **No.** Ninguno de los hallazgos de esta pasada lo pide. Y2 va en el sentido de aceptar, pero no es de este diff, ya existía en la base 4.14, no admite nada que el límite L1 ya declarado del control no admita, y ninguna extracción real tiene esa forma. Y3 es una mejora opcional de la prueba, en el sentido prudente.

**¿Qué debe corregirse antes de cerrar el bloque técnico?** [Interpretación] Solo el registro:
1. **Y1:** declarar en `HITO_2_4_15.md` §5 que los límites del apóstrofo y de los miles con espacio valen también para `fase1_historia.importe_completo`, y sus costes prudentes (texto propuesto en §3).
2. **Y4 (a):** en `CONTINUIDAD.md:10`, «Regresiones completas de las candidatas anteriores: PASA» no es exacto (la primera, `c2d2b96`, falló en 5 bloques; lo dice el propio `HITO_2_4_15.md` §4).
3. Anotar el resultado de esta comprobación donde el registro la da por pendiente (`HITO_2_4_15.md` §5, fila 7.ª, y §8; `PUNTO_DE_RECUPERACION.md`).

**¿Qué puede quedar como límite declarado?** [Interpretación] Lo de Y1 y Y2, y los costes prudentes de X5 (§2.2). Los demás límites ya declarados no cambian.

**¿Hace falta otra pasada?** [Interpretación] **No.** Las correcciones que se piden son de texto y no tocan código ni pruebas: basta que el autor las aplique y regenere el manifiesto. Si se toca cualquier archivo de `scripts/` o `pruebas/` (también si se aplica la propuesta opcional de Y3), esa línea necesita su batería y su comprobación.

**Lo que esta comprobación NO cierra** (sigue pendiente, como dice el registro): la **regresión completa y la reconstrucción de C48 de esta candidata** (las ejecuta otra sesión; §4), el **114/114** de `test_comprobadores.py`, **F1**, la **regeneración y auditoría de los expedientes**, **H9/I19**, **U1**, **U6 (a)** y el **control de la entrega 4.14 (29/35)**.

## 2. Las seis comprobaciones pedidas

### 2.1 X1/X2 · verificación mecánica

Todo **[Hecho]**. Salidas: `salidas8/verificar_correccion_x1_congelado.log`, `salidas8/h1_x1x2_identidad.log`, `salidas8/mutaciones8_ve_lanzamiento.log`.

- `python3 -I -B <rev8>/…/hito2/sondas7/verificar_correccion_x1.py <rev8>/munger_v2_r1`, **el script entregado, sin adaptar** (es el mismo archivo que el de `rev7/fable/sondas7/`, SHA-256 `c6475a2b…80bc33aa`; como junto a él no hay un árbol `copia/`, saca el código de 45ff57c con `git show`, solo lectura, y comprueba su huella `7abbb081…`). Resultado: **«RESULTADO: CONFORME»**, código 0:
  - código: es el mismo programa (árbol sintáctico) que 45ff57c con el carácter repuesto, y la huella **es** `4b00aa2a…a98c86cd` («ni un comentario de más»);
  - X1: los 17 casos del trozo de un número con apóstrofo dan «ausente» (con el código de 45ff57c, 11 daban «ok»); los 5 controles de la cifra entera, «ok»;
  - X2: el bloque de pruebas del árbol pasa 5 de 5 con su código, **falla con el de 45ff57c** (`{("Total 1'849,7", 849.7, "Total 1'849,7"): 'ok'}`) y detecta las seis variantes de la línea `:542`.
- Identidad con lo propuesto (`h1`): `scripts/verificacion_entradas.py` y `pruebas/test_verificacion_entradas_415.py` del árbol congelado son **byte a byte** los del árbol `fix7` de la séptima (`4b00aa2a…` y `88c62dfc…`), y también los que resultan de aplicar las cuatro sustituciones de `sondas7/propuestas7.py` (tres de pruebas y una de código) a los dos archivos de 45ff57c sacados de git. Entre 45ff57c y el árbol, en `verificacion_entradas.py` cambia una línea, la 542, con una sola operación: la inserción del apóstrofo ASCII (`(?<!\d[’])` → `(?<!\d['’])`).
- Como el archivo es el de `fix7`, vale para él lo que la séptima ejecutó sobre `fix7` y consta en `salidas7/` (baterías 190/190, 61/61 y 33/33; registros reales; diferencial de 113.243 citas con 0 diferencias frente a la propuesta de la sexta). Aquí se han repetido las baterías y los registros reales (§2.3 y §2.4), no el diferencial.
- Con la batería entera (`mutaciones8_ve.py`, árbol ligero aparte): las dos mutaciones de la línea `:542` que en la séptima pasaban 190/190 con las pruebas de 45ff57c **se detectan ahora**. `v7c` (el límite final sin apóstrofos): **189/190, código 1**; falla «(V3, V7)» con `("Total 849'697", 849, "Total 849'697"): 'ok'` y su par con «’». El límite inicial solo con «’» (la línea de 45ff57c: X1): **189/190, código 1**; falla «(V3, V7)» con `("Total 1'849,7", 849.7, "Total 1'849,7"): 'ok'`; es lo mismo que la séptima obtuvo con su árbol `fix7t` (sus pruebas son, byte a byte, las del árbol). Las otras nueve mutaciones de W1 constan como detectadas en `salidas7/mut7/` con las pruebas de 45ff57c, que las de esta candidata solo amplían (casos añadidos y una condición más; ninguna aserción se rebaja); no se han repetido.

### 2.2 X5 · `fase1_historia.importe_completo` (cambio nuevo)

`scripts/fase1_historia.py:90-94`, usado en `:203` (el impreso en su línea) y `:207` (el impreso en su página), las dos veces dentro de `comprobar_anio` (regla R-b de la reparación H1). `comprobar_anio` lo llaman `preparar`, `construir` y la orden `comprobar-anio`. No hay ningún otro uso en `scripts/`, `pruebas/` (salvo la prueba nueva), `v6/scripts/` ni el kit. `calcular_entrada` (C48) no lo usa: contrasta con `verificacion_entradas._cita_cifra`.

**Qué cambia** [Hecho] (leído; `x5a` A). Antes: `(?<![\d.,])` + importe + `(?![\d.,]*\d)`. Ahora: `(?<![\d.,])(?<!\d['’])` + importe + `(?![\d.,'’]*\d)`. Por delante se añade «no va precedido de cifra + apóstrofo»; por detrás, el apóstrofo entra en la clase de lo que puede seguir hasta otra cifra. El docstring dice lo que hace.

**Cierra lo que X5 señalaba** [Hecho] (`x5a` B y D, `x5e`).
- Los cuatro casos de la séptima (`g11`) pasan de True a False: «849,7» en «Total 1'849,7» y en «Total 1’849,7»; «849» en «Total 849'697» y en «Total 849’697». También el grupo de en medio y el último de «1'234'567», la cabeza y la cola con apóstrofo («1'234», «234'567»), las dos columnas («1'849,7 1'702,3»), el paréntesis, el negativo y el trozo con decimales detrás: 15 de los 35 casos cambian, todos de True a False.
- En 4.000 números bien formados con miles con apóstrofo (ASCII o «’»), de 200.865 trozos propios que empiezan y acaban en cifra y no están sueltos en la línea, el código anterior aceptaba 21.384 como importe completo; **el nuevo, ninguno**. El número entero se reconoce siempre.
- En su uso (`comprobar_anio`, expedientes sintéticos mínimos como los de `test_comprobadores.py` h1): los cuatro casos pasan de ACEPTADO a RECHAZADO («no está en su línea como importe completo»); también la línea cortada tras el apóstrofo cuando el trozo no está suelto en la página (rechazo por la comprobación en la página).

**No abre nada hacia lo permisivo** [Hecho] (`x5a` C; leído).
- Por construcción: las dos condiciones nuevas solo añaden rechazos (una condición negativa más por delante; por detrás, una clase que contiene a la anterior). Y los dos usos son `not importe_completo(…)` → error: un False más solo puede añadir un error, nunca quitarlo.
- Comprobado de forma exhaustiva: todos los textos de hasta 6 caracteres de un alfabeto de 9 símbolos (`1 8 , . ' ’ espacio a (`) con 10 importes: 751.144 pares en los que el importe está en el texto; difieren 46.264; **0 casos de False→True**; **0 diferencias en textos sin apóstrofo**; en todas las diferencias hay un apóstrofo pegado a una cifra.

**Coste** [Hecho] (`x5g`). No cambia de orden: en tiras adversas de 10.000 «1,» o «1'» sin espacios y en 100.000 repeticiones de un importe que no es el buscado, los dos códigos tardan lo mismo (menos de 1 ms y unos 30 ms); en la página real más larga, décimas de milisegundo.

**Rechazos falsos en datos reales: ninguno** [Hecho] (`x5b`, `x5c`).
- Los **32 expedientes** del árbol con `fase1_partes/` (23 con `texto/` conservado; los otros 9 —los seis de `empresas_v2/`, el de H3 y dos reproducciones de Viscofan— no lo llevan y dan el mismo error «archivo ausente» con los dos códigos): **320 años**, `comprobar_anio` con el código de 45ff57c y con el del árbol da **los mismos errores y los mismos ceros pendientes**. 212 años sin errores con el código nuevo (los mismos que con el anterior).
- Componente a componente: **17.956 componentes**; el impreso es importe completo en su línea en 17.950 con los dos códigos (los seis que no, tampoco lo eran antes: son de los originales de `empresas_v2/Hermes` y `empresas_v2/Rational`, entre ellos los dos ejemplos del propio docstring, «6.0» dentro de «196.0» y «7» dentro de «7,608»); de los 12.134 con página examinable, 12.134 en su página con los dos códigos. **0 diferencias.**
- Textos: 283 archivos `texto/*.txt`, 45 contenidos distintos: **0** «cifra + apóstrofo + cifra», ni ASCII, ni «’», ni «ʼ ′ ´ ` ‘». Hay 24 apóstrofos pegados a una cifra por un solo lado («Beat'30» y «Beat’30», «('000 €)», «January ’08», «d’1,25», «d’1 an» y el posesivo «SBF 120’s»): ninguno cambia nada, porque al otro lado del apóstrofo no hay cifra. 140 componentes tienen algún apóstrofo en su línea: todos dan lo mismo.
- **C48 de Elis** (`…_4_15/configuracion/cambio_elis_c48_4_15.json`): sus tres componentes (2023, 2024 y 2025) no tienen «cifra + apóstrofo + cifra» en la cita; `calcular_entrada("C48", …, carpeta=…_4_14/elis_decisiones/Elis)` con el código del árbol contrasta cada componente con su página y da **108,0** (sin redondear, 108,0).
- La orden `fase1_historia.py comprobar-anio` (no usa LibreOffice), sobre **copias** (`texto/` y `fase1_partes/`) de `elis_decisiones/Elis`, `viscofan_decisiones/Viscofan` y `vidrala_decisiones/Vidrala`: 30 años, código 0 en todos, **misma salida y mismo código** con el script de 45ff57c y con el del árbol; las copias quedan idénticas a los originales.

**La prueba nueva** [Hecho] (`pruebas/test_entrada_efectiva_415.py:371-375`; `x5d`, `mutaciones8.py`). Diez casos: los cuatro de X5 (False), dos que ya se rechazaban («1.849,7», «7,608»), y cuatro controles (True): el importe suelto, el número entero con apóstrofo dos veces y el posesivo «120’s» en la línea.
- Con el código del árbol pasa; con el de 45ff57c **falla** (los cuatro casos de X5 dan True).

| Mutación de la línea del `return` | Sentido | A nivel de unidad | Con la batería entera |
|---|---|---|---|
| `m0` · se quita el cambio (la línea de 45ff57c) | acepta | detectada | **detectada**: 61/62, código 1, falla «(séptima comprobación, X5)» |
| `m1` · el apóstrofo solo cuenta por delante | acepta | detectada | **detectada**: 61/62 |
| `m2` · solo por detrás | acepta | detectada | **detectada**: 61/62 |
| `m3` · solo el ASCII, en los dos lados | acepta | detectada | **detectada**: 61/62 |
| `m4` · solo «’», en los dos lados | acepta | detectada | **detectada**: 61/62 |
| `m5` · por delante solo ASCII | acepta | detectada | no ejecutada |
| `m6` · por delante solo «’» (el descuido de X1, aquí) | acepta | detectada | **detectada**: 61/62 |
| `m7` · por detrás solo ASCII | acepta | detectada | no ejecutada |
| `m8` · por detrás solo «’» | acepta | detectada | **detectada**: 61/62 |
| `m9` · por detrás, un solo separador y una cifra (la forma de `verificacion_entradas`) | acepta, solo en formas que no existen («7,,6», «7.'6») | no detectada | no ejecutada |
| `s1` · cualquier apóstrofo delante bloquea, aunque no haya cifra antes («d’1,5») | prudente | no detectada | no ejecutada |
| `s2` · cualquier apóstrofo detrás bloquea, aunque no siga cifra («120’s» con impreso 120) | prudente | no detectada | no ejecutada |
| `s3` · un apóstrofo en cualquier punto posterior de la línea bloquea | prudente | no detectada | no ejecutada |

- Las nueve mutaciones razonables del tratamiento del apóstrofo (`m0`–`m8`) se detectan; las siete ejecutadas con la batería entera dan 61/62 y código 1, y en todas falla solo la prueba de X5. Las que el punto de recuperación dice que la hacen fallar (sin el cambio, solo delante, solo detrás, solo ASCII): reproducido.
- No detectadas: `m9` (no es del apóstrofo: tampoco había prueba de dos separadores seguidos antes de este cambio) y `s1`–`s3`, que rechazan de más (Y3).
- El mínimo de `verificar_paquete.sh` (`h7`): `bash -n`, sintaxis correcta; la condición del bloque, aplicada a salidas ya obtenidas, da PASA con 62/62 y **FALLA** con 61/62 y con 61/61 (si se quitara la prueba, la verificación completa lo diría).

**Costes prudentes: formas legítimas que ahora se rechazan** [Hecho] (`x5a` E, `x5e` 12 y 13). Una cifra pegada a un apóstrofo que no es un separador de miles deja de valer como importe completo: «Q1'24» o «Q1’24» con impreso 24, «5'30» con 30, «2'5» con 5 o con 2 (un decimal escrito con apóstrofo), una llamada de nota tras una comilla de cierre («‘Vision 2030’1» con 2030), «'2023'849» con 849. En `comprobar_anio` es un error («no está en su línea como importe completo») si el impreso solo aparece así. **No cambian:** «9M’24 849,7», «H1’24: 24 tiendas» (la cifra está además suelta), «FY’24», el posesivo «120’s», «d’1,5 %», «l’exercice 2023», «849' 697». Ninguna extracción real tiene esas formas. Es lo mismo que X4 anotó en `verificacion_entradas.py`, aquí.

**Lo que sigue aceptando (no es de este cambio)** [Hecho] (`x5a` B). Igual que en `verificacion_entradas.py`: solo «'» y «’» cuentan; con «ʼ», «′», «´», «`» o «‘», «849,7» sigue valiendo dentro de «1ʼ849,7». Y los miles con espacio: «849,7» vale dentro de «1 849,7» (también con espacio duro, que `norm()` convierte en espacio). El registro lo declara para la verificación de las entradas, no para este control (Y1).

**Dos notas sobre el uso** [Hecho] (`x5e` 7, 8, 14–17).
- Un `impreso` escrito con apóstrofo de miles («1'849,7») no llega a `importe_completo`: `numero()` no lo admite («no numérico») y `comprobar_anio` lo rechaza antes. Ya era así. Los dos controles positivos de la prueba con el número entero con apóstrofo ejercen la función, no un caso que `comprobar_anio` acepte.
- R-a solo exige que la `linea` sea una subcadena de su página: Y2.

### 2.3 Baterías permitidas

Todo **[Hecho]**. En `fable/copia/`, como las lanza `verificar_paquete.sh` (`cd personaje_v2 && python3 -B pruebas/…`), con el sustituto de `soffice` delante en el `PATH`. Salidas: `salidas8/bateria_*.log`.

| Batería | Esperado | Obtenido | Tiempo |
|---|---|---|---|
| `test_verificacion_entradas_415.py` | 190/190 | **190/190**, código 0, 0 líneas FALLA | 521 s |
| `test_entrada_efectiva_415.py` | 62/62 | **62/62**, código 0, 0 líneas FALLA (la de X5, PASA) | 50 s |
| `test_verificacion_entradas_414.py` | 33/33 | **33/33**, código 0, 0 líneas FALLA | 92 s |
| `test_comprobadores.py` | 114/114 | **76/76 en las partes `h2`, `h1` y `h3`** (H2 39, H1 23, H3 14), código 0. **No ejecutadas:** `h1_recorrido` y `h1_reutilizacion` (las otras 38), porque lanzan `pipeline.py` y LibreOffice | 14 s |

- La parte `h1` (23) es la que ejerce `comprobar_anio` e `importe_completo` con los casos del contrato de la reparación H1 («123» dentro de «91234», etc.) y la orden `comprobar-anio`: pasa entera con el cambio de X5.
- Ningún intento de lanzar LibreOffice en ninguna batería ni sonda.
- Los tiempos se midieron con la regresión completa de la otra sesión en marcha: son orientativos.

### 2.4 Registros reales

Todo **[Hecho]**, con el código del árbol congelado (`python3 -I -B`, que no escribe en él; el diagnóstico y `q12` trabajan en copias temporales bajo el `TMPDIR` del revisor). Salidas: `salidas8/registros_reales.log` y `salidas8/reales/`.

- **Diagnóstico** (`cd …_4_14 && python3 -I -B ../2026-11_Vidrala_ensayo_4_15/scripts/diagnostico_registros_4_14.py <árbol>/personaje_v2 viscofan_decisiones/Viscofan vidrala_decisiones/Vidrala elis_decisiones/Elis`): **idéntico byte a byte** a `hito2/resultados/diagnostico_registros_4_14_con_reglas_hito2.json` (SHA-256 `91b6a33e…d587553a`): Viscofan 214/232 (1 error, 17 discrepancias), Vidrala 207/226 (4 errores, 15 discrepancias, 1 entrada no reproducible), Elis 175/193 (1 error, 17 discrepancias, 1 entrada no reproducible). Los otros cuatro registros (`viscofan` 211/232, `vidrala` 204/226, `elis_motor_A` 169/193 y `vidrala_decisiones_INVALIDO…` 186/226) dan, byte a byte, lo que la séptima obtuvo con `fix7`.
- **Inventario de signo** (`…/hito2/scripts/inventario_signo_registros.py`, llamado como en `sondas7/registros_reales.sh`) de los siete registros: **idéntico byte a byte** a `hito2/resultados/inventario_signo_registros_reales.json` (SHA-256 `5716dc3c…26ad3a3c`): las 1.645 entradas numéricas con página, «ok».
- **PDF reales** (`q12_pdf.py` parte B, copiado sin cambios a `sondas8/`, con `PV=<árbol>/personaje_v2`; usa `pdftotext`): Elis, 247 entradas con fuente `texto/…`, 244 pasan citando el `.txt` y 244 citando el PDF; Viscofan, 228, 225 y 225. **0 rechazadas** solo por el control del PDF.

### 2.5 El registro corregido (X3)

Todo **[Hecho]**: leído, y `r5` donde se cita (lo que el registro declara frente a `_cita_cifra` del árbol; 47 formas: 45 declaradas, un control y una informativa; **0 discordancias**).

| Punto de X3 | Estado | Evidencia |
|---|---|---|
| **(a)** cuatro «pendientes» que eran discrepancias | **Resuelto** | `HITO_2_4_15.md:153-156`: van ahora bajo «discrepancias por prudencia (bloquean siempre)». Reproducido: el intervalo partido por un salto de línea, «signo_distinto»; «. . . .130,8» y «ejercicio .849,7», «ausente»; «Q1'24» con 24, «ausente» (con 45ff57c se aceptaba: era X1). Las once formas que quedan como «pendientes por prudencia» (`:150-152`) dan pendiente |
| **(b)** un límite declarado que ya no existía («$» en en_numero) | **Resuelto** | La frase ya no está. El caso («Ventas 2023⏎849,7 millones» citada «849,7 mill») da pendiente |
| **(c)** dos frases de §1 desfasadas | **Resuelto** | `:34-35`: el guion entre dos enteros solo es intervalo entre dos años de 1900 a 2100 o fecha «d-m-aaaa»; lo demás, pendiente. `:39-40`: cortada dentro de un número, discrepancia; dentro de una palabra o no localizada, pendiente. Reproducido («2019-2020», «FY2023-2024», «31-12-2024», aceptadas; «9-10», «1850-1899», «XFY2023-2024», pendientes). Precisión menor: Y4 (c) |
| **(d)** límites sin nombrar | **Resuelto para la verificación de las entradas; falta el control de la fase 1 (Y1)** | `:146-149`: el importe que parece un año y la regla de la fecha, «en el sentido de aceptar». `:157-159`: los apóstrofos raros y los miles con espacio, «en el sentido de aceptar». `:153-156`: X4 y la cifra entera con «’», como discrepancias. Reproducido, forma por forma |
| **(e)** el criterio | **Resuelto** | `:138-141`: «los huecos nuevos en el sentido de aceptar … se han corregido … Siguen declarados, en el sentido de aceptar, los límites que se enumeran abajo como tales». La enumeración coincide con los rotulados así en la lista |
| **(f)** lo que se daba por corregido | **Resuelto** | `:135` (fila 6.ª: «aplicados … en `45ff57c`; al aplicar W3 se perdió el apóstrofo ASCII en una línea (X1) y `v7c` quedó sin prueba (X2)») y `PUNTO_DE_RECUPERACION.md:11-17` |
| **(g)** la comprobación dirigida «final» dada por hecha | **Resuelto** | `HITO_2_4_15.md:189-191` («una séptima comprobación dirigida (en borrador…)») y `CONTINUIDAD.md:10`. Precisión: Y4 (a) |
| **(h)** restos menores | **Resuelto** | `PUNTO_DE_RECUPERACION.md` ya no dice que `PROMPT_NUEVA_VENTANA.md` sea el de la 4.14; `VERSION` dice «seis revisiones independientes y una séptima comprobación dirigida, con sus correcciones X1, X2 y X5» |

**Las afirmaciones nuevas, una a una** [Hecho].

| Afirmación | Resultado |
|---|---|
| `test_verificacion_entradas_415.py` 190/190, y qué lleva ahora «(V3, V7)» y «(V5)»; «el número de pruebas no cambia» (`HITO` §4) | Reproducido; el diff es el propuesto |
| `test_entrada_efectiva_415.py` 62/62; mínimo 62 (`HITO` §4; `CONTINUIDAD.md:10` y `:119`; `PROMPT_NUEVA_VENTANA.md:25`) | Reproducido; el mínimo, leído y probado (`h7`) |
| «`45ff57c`: RESULTADO GLOBAL: PASA … pasaba con la regresión X1 dentro» (`HITO` §4; `PUNTO:8-10`) | Consta en `resultados/verificacion_completa_45ff57c.txt` (18 bloques, ninguno en FALLA, código 0) y en `reconstruccion_c48_45ff57c/`. No reproducido. Las siete regresiones registradas: seis PASA y `c2d2b96` FALLA (5 bloques) |
| X1: «queda con SHA-256 `4b00aa2a…`, el archivo exacto que la séptima comprobación ejecutó … (árbol `fix7`)» (`PUNTO:12-15`) | Reproducido (§2.1) |
| X2: «tal como los propuso el revisor» (`PUNTO:16-17`) | Reproducido, byte a byte |
| X5: «Las mutaciones (sin el cambio, solo delante, solo detrás, solo ASCII) la hacen fallar. **No revisado todavía por otro agente**» (`PUNTO:18-20`) | Reproducido (§2.2). Lo segundo era cierto al congelar; es esta comprobación |
| «Baterías sobre el árbol corregido: … 190/190 … 62/62 … 33/33, comprobadores 114/114» (`PUNTO:22`) | Las tres primeras, reproducidas. De la cuarta, 76/76 en las partes sin LibreOffice; el resto, no ejecutado: Y4 (b) |
| «Registros reales con el código corregido: diagnóstico idéntico byte a byte, inventario de signo igual, PDF reales (q12 B): 244/244 y 225/225, 0 rechazos falsos» (`PUNTO:23-24`) | Reproducido (§2.4) |
| La séptima «es un borrador … El dictamen, X1–X5, las baterías sobre `fix7` (190/190, 61/61, 33/33) y las diez mutaciones de W1 con la batería entera (nueve detectadas; `v7c`, no, por X2) sí estaban terminados y constan en `salidas7/`» (`PUNTO:31-35`; `HITO` §5, fila 7.ª) | Consta: `salidas7/propuestas7/fix7_bateria_*.log` (190/190, 61/61, 33/33, código 0) y `salidas7/mut7/*/resultado.json` (las diez de W1: nueve con código 1 y 189/190 o 60/61; `v7c`, 190/190). El resumen que hace del dictamen es fiel al §1 de aquel informe |
| «X4 declarado» (`HITO` §5, fila 7.ª) | Sí (`:153-156`); reproducido |
| «X5 (permisivo, ya en la 4.14)» | Sí: esas líneas vienen del commit de la base (`git blame`, solo lectura) |
| Tabla de límites de §5 | Reproducida, forma por forma (`r5`) |

**Lo pendiente no se da por cerrado en ningún sitio** [Hecho] (leído en los cinco documentos).

| Pendiente | Dónde consta como pendiente |
|---|---|
| Regresión completa y reconstrucción de C48 de **esta** candidata | `PUNTO:25` («pendientes (no se dan por superadas)») y `:41`; `HITO` §4 y `CONTINUIDAD.md:10` remiten al punto de recuperación |
| Esta comprobación (verificación mecánica de X1/X2, X5 y el registro) | `PUNTO:39-40`; `HITO` §5, fila 7.ª («Pendiente: verificación mecánica … por otro agente») |
| F1 | `HITO` §7; `PUNTO:49`; `CONTINUIDAD.md:11`; `VERSION` |
| Regeneración y auditoría de los expedientes | `HITO` §7; `PUNTO:48`; `CONTINUIDAD.md:11`; `VERSION` |
| H9/I19 | `HITO` §3, §5 y §7; `PUNTO:42-43`; `CONTINUIDAD.md:11` |
| U1 y U6 (a) | `HITO` §2, §5 y §7; `PUNTO:44-47` |
| Control de la entrega 4.14: 29/35 | `HITO` §4 y `PUNTO:26`: «No se da por superado» |

`PROMPT_NUEVA_VENTANA.md` da los recuentos como lo **esperado** al ejecutar la verificación, no como un resultado, y dice «No se declara cerrado ningún requisito pendiente». `VERSION` no afirma ningún resultado de pruebas.

### 2.6 Alcance del cambio de código

Todo **[Hecho]** (`h6`; `git diff --name-status 45ff57c 0a0020b`, solo lectura).

- Cambian 136 archivos: **5 de código**, 113 del informe, sondas y salidas de la séptima, 11 de resultados (la regresión de 45ff57c y su reconstrucción de C48) y 7 de registro y empaquetado (`CONTINUIDAD.md`, `VERSION`, `PROMPT_NUEVA_VENTANA.md`, `HITO_2_4_15.md`, `PUNTO_DE_RECUPERACION.md`, el manifiesto y `CAMBIOS_ARCHIVOS.txt`). Ninguno borrado. Nada en `esquema/`, `v6/`, el kit, `contrastes/`, `empresas_v2/`, `prompts/`, `corpus/`, `tools/` ni `docs/`.
- `scripts/verificacion_entradas.py`: −1 +1, la línea 542; un carácter. Por árbol sintáctico, solo cambia `_lectura_cifra`.
- `scripts/fase1_historia.py`: −2 +3, líneas 92-94 (el final del docstring y el `return`). Por árbol sintáctico, solo cambia `importe_completo`.
- `pruebas/test_verificacion_entradas_415.py`: −3 +10; cambian tres sentencias: el diccionario `v3`, `mal_v3` y la condición de «(V5)». Es el bloque propuesto por la séptima.
- `pruebas/test_entrada_efectiva_415.py`: +5; tres sentencias nuevas (`x5`, `mal_x5` y su `paso`). Ninguna prueba existente cambia.
- `verificar_paquete.sh`: tres líneas (24, 171 y 174), y en cada una solo «61» → «62».

## 3. Hallazgos

Ninguno afecta a un dato real ni pide cambiar código. Los números de línea son los de esta candidata.

### Y1 · OBSERVACIÓN (declaración; lo que queda sin decir va en el sentido de aceptar en (i) y en el prudente en (ii) y (iii)) · El registro da X5 por corregido y no declara, para el control de la fase 1, los límites y costes que sí declara para la verificación de las entradas

`hito2/HITO_2_4_15.md:105-106`, `:136`, `:143-166`; `scripts/fase1_historia.py:90-94`.

- **[Hecho]** (`x5a` B y E, `x5e`, `r5` al final). El registro nombra X5 dos veces (la prueba, en §4; «corregidos X1, X2, X3 y X5», en la tabla de §5) y la lista de límites de §5 habla solo de citas («citada «849,7» queda comprobada»). De `importe_completo` no dice que:
  1. **(i) siguen aceptándose** las mismas dos formas que en `verificacion_entradas.py`: los signos parecidos al apóstrofo («849,7» vale como importe completo dentro de «1ʼ849,7», «1′849,7», «1´849,7», «1`849,7», «1‘849,7») y los miles con espacio («849,7» dentro de «1 849,7»; también «573,7» dentro de «4 573,7», la forma de los informes en francés, que `numero()` admite desde el 14-nov);
  2. **(ii) se rechazan por prudencia** (error de `comprobar-anio`) las cifras pegadas a un apóstrofo que no es separador de miles: «Q1'24» con impreso 24, «5'30» con 30, «2'5» con 5, una llamada de nota tras comilla de cierre;
  3. **(iii)** un `impreso` escrito con apóstrofo de miles («1'849,7») no es numérico para la fase 1 (`numero()`): un informe con ese separador no pasa `comprobar-anio` con el número entero (ya era así; prudente).
- **[Hecho]** Ninguna extracción ni texto real tiene esas formas (§2.2).
- **[Interpretación]** Es el mismo criterio que la séptima aplicó en X3 (d): los límites en el sentido de aceptar tienen que estar en el registro, que es lo que leerá la revisión externa. Aquí los límites son los mismos que ya están declarados; falta decir que valen también en el otro control.
- **[Propuesta]** Añadir a la lista de `HITO_2_4_15.md` §5 una entrada como esta (no requiere código):
  > - Fase 1 (`fase1_historia.importe_completo`, X5): valen los mismos límites **en el sentido de aceptar** que en la verificación de las entradas: solo «'» y «’» cuentan como separadores de miles («849,7» sigue valiendo como importe completo dentro de «1ʼ849,7») y los miles con espacio tampoco («573,7» vale dentro de «4 573,7»). **Por prudencia** (error de `comprobar-anio`): una cifra pegada a un apóstrofo que no es separador de miles («Q1'24» con impreso 24, una llamada de nota tras una comilla de cierre) deja de valer como importe completo, y un `impreso` escrito con apóstrofo de miles («1'849,7») no es numérico para la fase 1. R-a solo exige que la `linea` sea una subcadena de su página (Y2; dentro de L1).

### Y2 · OBSERVACIÓN (fuera del diff; ya existía en la base 4.14; en el sentido de aceptar; no admite nada que el límite L1 declarado no admita) · R-a comprueba la `linea` como subcadena: cortada justo en un separador de miles, deja el trozo «completo en su línea»

`scripts/fase1_historia.py:203-208`.

- **[Hecho]** (`x5e` 14–17). `comprobar_anio` exige (R-b) que el impreso sea importe completo en la `linea` **tal como la da la extracción**, (R-a) que esa línea sea una subcadena de la página (`norm(lin) not in P[pg]`, sin límites) y (R-b) que el impreso sea importe completo en algún punto de la página. Con la página «Capital expenditure 1'849,7 millones⏎Other items 849,7», la línea «849,7 millones» y el impreso «849,7»: **ACEPTADO**, con el código anterior y con el nuevo. Igual con punto de miles («1.849,7 millones»): no es un asunto del apóstrofo.
- **[Hecho]** X5 lo estrecha y no puede cerrarlo: si el trozo **no** está suelto en otro punto de la página, el código nuevo lo rechaza por la comprobación en la página (caso 14; el anterior lo aceptaba). Con punto ya se rechazaba (caso 15).
- **[Hecho]** No es de este diff: las líneas 203-208 vienen del commit de la base 4.14 (`git blame`, solo lectura). El prompt de extracción pide la línea literal «recortada a ≤ 200 caracteres» (`prompts/historia_anio.md:35`): una línea parcial es legítima.
- **[Hecho]** En las extracciones reales no hay ninguna línea así (`x5f`): de 1.690 combinaciones distintas (archivo, página, línea, impreso), en las 1.690 la línea tiene alguna aparición en su página que no está cortada dentro de un número; solo 3 líneas empiezan por cifra.
- **[Hecho]** El control declara desde la reparación H1 que no valida concepto, columna, unidad ni signo (L1–L4: `CONTINUIDAD.md:276`, `REGISTRO_IMPLEMENTACION_H1-H3.md:168`), y la batería lo fija: «Revenue 123» citado para el capex se acepta (`test_comprobadores.py`, h1, caso 2).
- **[Interpretación]** Para que el caso se acepte, la misma cifra tiene que estar suelta en otra línea de la página; y entonces la extracción podría citar esa otra línea entera y pasar igual, por L1. Lo que R-a deja pasar aquí no añade nada a lo que L1 ya declara que el control no ve. Por eso no se pide corregirlo en este hito: es anterior a él, ajeno a su objeto, estrecho y sin casos reales.
- **[Propuesta]** Decirlo en una frase junto a L1 (va incluida en el texto de Y1). Si algún día se corrige, no es una línea: hay que decidir qué es una línea cortada por los dos extremos (también la que empieza o acaba en el separador), sin rechazar las líneas legítimamente recortadas a 200 caracteres; necesita su diseño, su prueba y su revisión, en la tarea que toque la fase 1. No se propone código aquí.

### Y3 · OBSERVACIÓN (pruebas; en el sentido prudente) · La prueba de X5 no fija que un apóstrofo que no está entre dos cifras no bloquea

`pruebas/test_entrada_efectiva_415.py:371-375`.

- **[Hecho]** (`x5d`). Los cuatro controles positivos no tienen ningún apóstrofo pegado al importe salvo como parte de él: el posesivo «120’s» está en la línea, pero el importe del caso es «849,7». Tres mutaciones que rechazan de más pasan la prueba: cualquier apóstrofo delante bloquea (`s1`: «d’1,5» con 1,5 daría False), cualquier apóstrofo detrás bloquea (`s2`: «120’s» con 120), y un apóstrofo en cualquier punto posterior de la línea bloquea (`s3`).
- **[Interpretación]** Van en el sentido prudente (un rechazo de más es un error visible de `comprobar-anio`, no una cifra aceptada) y las formas afectadas existen en los textos reales («120’s», «d’…»), donde hoy pasan. Puede quedar como está.
- **[Propuesta] (opcional; no hace falta para cerrar)** Dos controles más en el diccionario `x5`. Diff exacto (es el contenido de `salidas8/propuestas8_fix8t.diff`; en el archivo fuente el apóstrofo tipográfico va escrito con su escape de Python, `\u2019`):
  ```diff
  --- a/munger_v2_r1/personaje_v2/pruebas/test_entrada_efectiva_415.py
  +++ b/munger_v2_r1/personaje_v2/pruebas/test_entrada_efectiva_415.py
  @@ -370,7 +370,9 @@
   paso("C", "(segunda revisión, residuo del h13) un componente que no es un objeto: error explícito (no AttributeError)", bool(e) and bool(e2) and "no es un objeto" in e2, (e, e2))
   x5 = {("849,7", "Total 1'849,7"): False, ("849,7", "Total 1\u2019849,7"): False, ("849", "Total 849'697"): False, ("849", "Total 849\u2019697"): False,
         ("849,7", "Total 1.849,7"): False, ("7", "Total 7,608"): False, ("849,7", "Total 849,7"): True, ("1'849,7", "Total 1'849,7"): True,
  -      ("849'697", "Total 849'697"): True, ("849,7", "Ventas SBF 120\u2019s 849,7"): True}
  +      ("849'697", "Total 849'697"): True, ("849,7", "Ventas SBF 120\u2019s 849,7"): True,
  +      # (octava, propuesta del revisor, Y3) un apóstrofo que no está entre dos cifras no bloquea: posesivo tras la cifra y elisión antes de ella
  +      ("120", "Ventas SBF 120\u2019s 849,7"): True, ("1,5", "taux d\u20191,5 %"): True}
   mal_x5 = {k_: FH.importe_completo(*k_) for k_, e_ in x5.items() if FH.importe_completo(*k_) != e_}
   paso("C", "(séptima comprobación, X5) importe_completo: el apóstrofo de miles (ASCII o tipográfico) es parte del número; «849,7» no está completo en «1'849,7»", not mal_x5, mal_x5)
   
  ```
  Probado en el árbol ligero `fable/fix8t/` (el código de 0a0020b sin tocar y solo esa prueba cambiada): la batería entera, **62/62**, código 0; a nivel de unidad, el bloque pasa con el código del árbol, falla con el de 45ff57c, y detecta `m0`–`m8` y además `s1`, `s2` y `s3` (`salidas8/propuestas8_unidad.log`, `salidas8/propuestas8_fix8t_bateria_ee415.log`). El bloque de arriba, extraído de este informe, se aplica limpio con `patch -p1` sobre el archivo del árbol congelado (en una copia temporal) y da el archivo probado (`salidas8/propuestas8_diff_del_informe_aplica.log`). El número de pruebas no cambia. No se ha probado con la regresión completa.

### Y4 · OBSERVACIÓN (declaración) · Tres precisiones del registro

Todo **[Hecho]** (leído).

- **(a) `CONTINUIDAD.md:10`:** «Regresiones completas de las candidatas anteriores: **PASA**». Una de las anteriores, la primera (`c2d2b96`), falló en 5 bloques: lo dice `HITO_2_4_15.md:111-112` y está en `resultados/verificacion_completa_candidata_c2d2b96_FALLA.txt`. [Propuesta] «… de las seis candidatas anteriores desde `92b2362`: PASA (la primera, `c2d2b96`, falló en 5 bloques y se corrigió)».
- **(b) `PUNTO_DE_RECUPERACION.md:22`:** «comprobadores **114/114**» sobre el árbol corregido. No se ha podido reproducir sin LibreOffice (76/76 en las tres partes que no lo usan) y, a diferencia de las otras cifras de esa frase, no hay en el árbol una salida de esa ejecución con esta candidata (la de la regresión de 45ff57c es de otro código). No se dice que sea falso: se dice que en el árbol consta solo como declaración del autor. (Solo leído, y no es material de esta revisión: el registro de la regresión completa de esta candidata que ejecuta la otra sesión dice ya «114/114 comprobaciones PASAN»; §4.)
- **(c) `HITO_2_4_15.md:34`:** «dos años crecientes». El código admite también dos años iguales (`1900 ≤ anterior ≤ cifra ≤ 2100`): «Plan 2023-2023» con +2023 se lee en positivo (`r5`). Es la misma regla ya declarada del importe que parece un año; bastaría «no decrecientes». Sin importancia.

## 4. Lo que no se ha hecho

- Nada con LibreOffice ni con el pipeline. No se han ejecutado `test_relevo_i19_415.py`, `test_pipeline_sintetico.py`, `test_integracion_v64.py`, `test_auditorias_v2.py`, `test_cierre_v2.py`, `test_estados_v2.py`, `test_resumen_v2.py`, `test_integridad_auditoria_v2.py`, `test_trazabilidad_v2.py`, `test_vigencia_h5.py`, `test_juicio_objetivo_414.py` ni `verificar_paquete.sh`.
- **De `test_comprobadores.py` no se han ejecutado las partes `h1_recorrido` y `h1_reutilizacion`** (38 de las 114 comprobaciones): lanzan `pipeline.py` y LibreOffice. El 114/114 no se ha reproducido.
- **[Hecho, solo leído; no es material de esta revisión] La regresión completa de esta candidata** la ejecuta otra sesión sobre su propia copia (`scratchpad/reg8/`): los 74 archivos de código de esa copia (`scripts/`, `pruebas/`, `v6/scripts/` y `verificar_paquete.sh`) son idénticos a los del árbol congelado. A las 08:38 UTC su registro (`reg8/verificacion_completa_final.txt`, empezado a las 08:01 UTC) llevaba 10 bloques con resultado, todos en PASA (entre ellos «114/114 comprobaciones PASAN», 190/190, 62/62 y el relevo caducado 5/5), y seguía en la batería de la integración V6.4: no había terminado. El revisor no la ha reproducido ni la da por superada; tampoco la reconstrucción de C48, que va después.
- No se ha ejecutado `fase1_historia.py construir` ni `preparar` sobre expedientes reales: `importe_completo` solo se usa dentro de `comprobar_anio`, que es lo que se ha comparado año a año.
- No se ha comprobado el «control de la entrega 4.14: 29/35» ni las cifras de §0 del registro (ZIP, base materializada, manifiesto del hito 1).
- De `q12_pdf.py` solo se ha ejecutado la parte B.
- No se han repetido las sondas de las pasadas anteriores sobre código que no cambia (el diferencial aleatorio de la séptima, `g9`; unidades, HTML, relevo, fichas…). Lo que la séptima ejecutó sobre `fix7` vale para este `verificacion_entradas.py` porque es el mismo archivo, byte a byte; no se ha vuelto a ejecutar.
- Mutaciones con la batería entera: de X5, siete (`m0`–`m4`, `m6`, `m8`); de la línea `:542`, dos. Las demás, solo a nivel de unidad. Las de las pasadas anteriores no se han repetido.
- La propuesta opcional de Y3 no se ha probado con la regresión completa.
- No se ha revisado el sentido económico de ningún dato, de F1 ni del 108 de C48.

## 5. Integridad del árbol congelado y del repositorio

- **[Hecho] El árbol congelado no ha cambiado.** Al empezar (08:02 UTC) y al terminar (08:38 UTC, después de la última lectura del árbol) se calcularon las huellas SHA-256 de sus 7683 archivos (todos salvo el manifiesto): las dos listas son idénticas (`huellas_arbol_congelado_inicio.txt` y `huellas_arbol_congelado_fin.txt`; SHA-256 de las dos, `cfe8ce74…e4f5d653`) y coinciden con `MANIFIESTO_SHA256.txt` (7683 de 7683; 0 distintas, 0 ausentes, 0 de más). El árbol tiene 7684 archivos, ningún enlace, ningún `__pycache__` ni `.lo_perfil`, y ninguna entrada con fecha posterior al inicio de esta comprobación.
- **[Hecho] `rev7/` (los árboles de la séptima) no se ha tocado:** ninguna entrada con fecha posterior al inicio.
- **[Hecho] `/home/user/munger-v2` no se ha tocado:** `git status` sin cambios, `HEAD` en `0a0020b9e213…`, rama `claude/hopeful-bardeen-qap6y0`, ningún `stash`. Solo se han usado `git diff`, `show`, `archive`, `blame`, `log`, `status` y `rev-parse`.
- **[Hecho] Ningún intento de lanzar LibreOffice:** `salidas8/INTENTOS_SOFFICE.log` no existe. No queda en marcha ningún proceso del revisor.
- Todo lo escrito por esta comprobación está en `rev8/fable/` (unos 70 MB: árboles ligeros, copias temporales de tres expedientes para `x5c`, sondas y salidas).

## 6. Índice de sondas y salidas

Todo en `/tmp/claude-0/-home-user-munger-v2/ace24ef4-365c-50f9-bb78-93416041e669/scratchpad/rev8/fable/`. Sondas en `sondas8/`; salidas en `salidas8/`, con el nombre de la sonda y extensión `.log`. Uso: `cd sondas8 && python3 -I -B <sonda>.py` (o `bash <sonda>.sh`).

| Sonda | Qué prueba | Punto |
|---|---|---|
| `construir_arboles8.py` | los árboles ligeros `copia/` (0a0020b) y `prev/` (45ff57c) | §0 |
| `comun8.py` | arnés: carga en un mismo proceso `fase1_historia` de 0a0020b y de 45ff57c | — |
| *(entregada)* `sondas7/verificar_correccion_x1.py` | la verificación mecánica de X1/X2, tal cual, sobre el árbol congelado → `verificar_correccion_x1_congelado.log` | §2.1 |
| `h1_x1x2_identidad.py` | lo aplicado es byte a byte lo propuesto (`fix7` y `propuestas7.py` sobre 45ff57c); un carácter en `:542` | §2.1 |
| `mutaciones8_ve.py` | las dos mutaciones de `:542` con la batería 4.15 entera → `mutaciones8_ve_lanzamiento.log`, `mut8/<nombre>/` | §2.1 |
| `x5a_importe_completo_unidad.py` | `importe_completo` nuevo frente al anterior: casos, monotonía exhaustiva, cierre en números bien formados, costes | §2.2 |
| `x5b_reales.py` | los 32 expedientes con `fase1_partes/`: `comprobar_anio` e `importe_completo` con los dos códigos; apóstrofos en los textos; C48 de Elis | §2.2 |
| `x5c_cli_comprobar_anio.sh` | la orden `comprobar-anio` sobre copias de tres expedientes reales, con los dos códigos | §2.2 |
| `mutantes8.py`, `x5d_prueba_x5_mutaciones_unidad.py` | la prueba nueva de X5 contra el árbol, 45ff57c y trece mutaciones, a nivel de unidad | §2.2, Y3 |
| `mutaciones8.py` | siete mutaciones de X5 con la batería de la entrada efectiva entera → `mutaciones8_lanzamiento.log`, `mut8/<nombre>/` | §2.2 |
| `x5e_comprobar_anio_sintetico.py` | X5 en su uso: `comprobar_anio` con 17 expedientes sintéticos mínimos, con los dos códigos | §2.2, Y1, Y2 |
| `x5f_linea_cortada_reales.py` | ¿hay líneas reales cortadas dentro de un número? | Y2 |
| `x5g_coste.py` | coste de `importe_completo` nuevo frente al anterior en textos adversos y en la página real más larga | §2.2 |
| `h7_minimo_62.sh` | sintaxis de `verificar_paquete.sh` y su condición del mínimo 62 sobre salidas ya obtenidas (no lo ejecuta) | §2.2 |
| `run_bateria8.sh` | lanzador de las baterías permitidas (rechaza las partes de `test_comprobadores.py` que usan LibreOffice) → `bateria_*.log` | §2.3 |
| `registros_reales8.sh`, `q12_pdf.py` *(copia sin cambios)* | diagnóstico, inventario de signo y PDF reales → `registros_reales.log`, `reales/` | §2.4 |
| `r5_registro_limites.py` | el registro corregido (§1 y §5) frente al código del árbol, forma por forma; y lo que no dice de X5 | §2.5, Y1, Y4 |
| `h6_alcance_diff.py` | qué cambia entre 45ff57c y 0a0020b, por archivo y por árbol sintáctico | §2.6 |
| `propuestas8.py` | la propuesta opcional de Y3: árbol `fix8t/`, diff y evaluación → `propuestas8_fix8t.diff`, `propuestas8_unidad.log`, `propuestas8_fix8t_bateria_ee415.log`, `propuestas8_diff_del_informe_aplica.log` | Y3 |

Otras salidas: `DIFF_SEPTIMA_A_OCTAVA_codigo.diff` (el cambio de código revisado), `huellas_arbol_congelado_inicio.txt` y `huellas_arbol_congelado_fin.txt` (en `fable/`).
