# Cuarta pasada (acotada a T1–T7) de la revisión independiente del hito 1 de la 4.15

Revisor: Fable (Claude, contexto separado de la implementación; no es una revisión humana) · 15-nov-2026.
Convención: **[Hecho]** = comprobado por el revisor ejecutando o leyendo (se dice cuál); **[Interpretación]** = lectura del revisor; **[Propuesta]** = corrección sugerida. Lo que no se ha ejecutado se dice expresamente.

## 0. Qué se ha revisado y cómo

- **Alcance:** solo lo que cambió para responder a la tercera pasada (`diff_cuarta_pasada.diff`: `verificacion_entradas.py`, `pipeline.py`, `cambiar_base.py` y tres baterías; además `verificar_paquete.sh`, que también cambia y no está en ese diff), la documentación (`HITO_1_4_15.md`, `CONTINUIDAD.md`) y el manifiesto. Lo ya corregido se ha vuelto a probar solo como regresión.
- **[Hecho]** Árbol: `revision_hito1/arbol_congelado4/munger_v2_r1`, sin modificarlo; todo se ejecutó en una copia (`/tmp/rev_fable4/congelado4`). Las huellas SHA-256 de los 81 scripts y pruebas, `verificar_paquete.sh`, `VERSION`, `CONTINUIDAD.md`, el manifiesto y la lista de cambios del árbol congelado son las mismas al empezar y al terminar, y ningún archivo del árbol tiene fecha posterior al inicio. Referencias (primeros y últimos 8 caracteres): `verificacion_entradas.py` `742ab1b5…33033e09`; `pipeline.py` `8de79fe5…6da2c58e`; `cambiar_base.py` `2661f9ba…504406c3`; `test_verificacion_entradas_415.py` `6929f90b…d2ab91e1`; `test_entrada_efectiva_415.py` `82f2441c…baea7054`; `test_integracion_v64.py` `f1c4b51d…bb3e3cb5`; `test_verificacion_entradas_414.py` `98b07f61…f3c0226a` (la misma que en la tercera pasada); `verificar_paquete.sh` `69c0395a…6f31435f`; `HITO_1_4_15.md` `d1d363ca…c841ad4d`; `CONTINUIDAD.md` `7b960cff…92efc614`.
- **[Hecho]** `diff -rq` entre el árbol de la tercera pasada y este: cambian los seis archivos del diff, `verificar_paquete.sh`, `HITO_1_4_15.md`, `CONTINUIDAD.md`, el manifiesto, la lista de cambios, el diagnóstico y los ocho JSON de la reconstrucción; son nuevos dos archivos de `reproduccion/codigo_4_14/`, dos salidas de regresión y la tercera revisión con sus sondas (idéntica byte a byte al original). Nada más.
- **Reproducciones:** `revision_hito1/reproducciones_fable/v4/` (arnés `fx4.py`). Sondas de la tercera pasada adaptadas: `q1`, `q2`, `q4`, `q4b`, `q4c`, `q5`, `q7`, `q12`. Sondas nuevas: `r1` (T1), `r2` (T2), `r4` (T4), `r5` (T5), `r6` (round), `r7` (caso nuevo del grupo D de la integración, sin LibreOffice) y `r8` (apoyo de las propuestas). Regresión de lo anterior: `v4/regresion_v3/` (doce sondas de la tercera pasada: las diez `p*`, `q9` y `q17`). Salidas literales en `v4/salidas/*.log` y `v4/regresion_v3/salidas/` (también las tres baterías, el diagnóstico regenerado y las tres mutaciones). Uso: `cd reproducciones_fable/v4 && TMPDIR=<carpeta temporal> PV=<copia de arbol_congelado4>/personaje_v2 python3 -B r2_t2_cifras.py`; para comparar con la tercera pasada, `PV=<copia de arbol_congelado3>/personaje_v2`. Todas trabajan en carpetas temporales y no escriben en `PV`.
- **No ejecutado:** nada que arranque LibreOffice (`verificar_paquete.sh`, la batería de integración, la sintética, la reconstrucción). Los tramos del pipeline se ejecutaron con un sustituto de `soffice` en el `PATH` que termina con 1. Durante la revisión había un proceso de LibreOffice de la regresión completa de la coordinación (`cand_h1_verif`): no es de esta revisión.

## 1. Veredicto

**ACEPTABLE CON CORRECCIONES** (ninguna bloqueante).

- **[Hecho]** Las tres baterías pasan (105/105, 40/40, 33/33). Los contraejemplos literales de la tercera pasada (T1, T2, T3, T4, T5) ya no pasan. El diagnóstico de los registros reales se reproduce idéntico al entregado (214/232, 207/226, 175/193) y, frente a la tercera pasada, solo cambia `Historia!L10` de Viscofan, como se declaró. El manifiesto corresponde al árbol (6.935 archivos, 0 modificados, 0 ausentes, 0 de más). No se ha encontrado nada que el árbol de la tercera pasada rechazara y este acepte, salvo una forma sintáctica inocua (`sum(a, b)` sin lista).
- **[Hecho]** **T2 sigue abierto con una variación de una línea** (U1): una cifra se escribe en la fórmula con dígitos y potencias de diez, que son constantes admitidas, y cualquier celda comprobada sirve de origen que «influye». Los 155 datos numéricos de cálculo quedan así `apto=True`, sin fuente y sin listar.
- **[Hecho]** La aritmética exacta de T1 trae dos efectos laterales menores: rechaza el 11 % de las medias de dos valores que escribe el propio generador del paquete (U2) y deja que `comprobar` no termine con un `round` de decimales enormes (U3). El control de sensibilidad de T2 rechaza derivaciones legítimas en casos límite (U4).
- **[Interpretación]** T1, T3, T4, T5, T6 y T7 hacen lo que declaran, con los residuos menores de §4. En T2 es la tercera vez que una variante de una línea sortea un control sintáctico: no puede cerrarse por esa vía (el último contraejemplo de U1 no lleva ninguna cifra escrita). Lo que procede es declararlo como límite, dejar de afirmar que «una fórmula no escribe cifras de la fuente» y, si se quiere, endurecer el control con las tres reglas de `r8`, que son compatibles con los 148 derivados reales. Con eso, a juicio del revisor, no hace falta otra pasada completa sobre este punto.

## 2. Baterías (sin LibreOffice, en la copia)

| Batería | Resultado | Código |
|---|---|---|
| test_verificacion_entradas_415.py | **105/105** PASAN | 0 |
| test_entrada_efectiva_415.py | **40/40** PASAN | 0 |
| test_verificacion_entradas_414.py | **33/33** PASAN | 0 |

- **[Hecho]** `verificar_paquete.sh` exige 105, 40 y 199 (leído). La batería de la 4.14 es idéntica byte a byte a la de la tercera pasada. Grupos de la 4.15: P, R1, R2, R3, V, RI, S, T (15 casos), J, E y N, como dice el documento.
- **[Hecho] Caso nuevo del grupo D de la integración** (`r7`, mismas órdenes que la batería, sin LibreOffice): el CAMBIO del control heredado sin declarar el modo → `entrada_efectiva.json` «estricta», `pipeline --hasta 4` se detiene en el paso 2 con `rellenar … --estricta → 7 · Análisis!C50: libro 0 · fase1_v63.json None`, sin libro de datos; la expresión del caso da PASA. Con «registrada» y su motivo, el paso 2 termina. El resto del grupo D y el 199/199 no se han ejecutado.
- **[Hecho] Mutaciones** (copia aparte, batería de la 4.15): sin canonizar los números en la huella → 104/105 (falla h17: T7 corregido); sin el control de sensibilidad → 104/105; **sin el control de constantes → 105/105** (ningún caso lo distingue: U8).

## 3. Estado de T1–T8

| Punto | Estado | Evidencia (sonda → resultado) |
|---|---|---|
| **T1** aritmética exacta | **Corregido, con dos efectos laterales** | `q4`: 0,25 por 0,887, 0,9 por 0,0335, 0,8874 y 0,8879 por 0,887, 849,0 por 849,697 y C55 con 40.000 acciones de menos → discrepancia; C55 exacto → comprobada. `q4c` (real): `Historia!L10` de Viscofan → discrepancia, como sus nueve hermanas (214/232). `r1` A: 120,4 − 120,4 = 0; 0,1 + 0,2 = 0,3; `round` de la hoja (2,5 → 3; −2,5 → −3; 0,125 → 0,13; 2,675 → 2,68). `q4b`: en los 148 derivados reales solo cambia L10. Efectos laterales: U2 y U3. |
| **T2** constantes, sensibilidad, clases de origen, escala | **Parcialmente** | `q2` A y B: los contraejemplos de la tercera pasada (`o[x] * 0 + c`, `o[x] − o[x] + c`, `min`, `round(o[x] * 0, 3) + c`, auxiliar `dato_ausente`/`no_aplicable` con el número; en bloque, 155 errores) → no apto. `q2` C: la regla de N2 (dato derivado de hipótesis, directa o por cadena) sigue funcionando con fórmulas sin constantes. `r2` D: escala 849,697 con «unidades» o «miles de €», escala 0 en un cero comprobado → error. **Residuos:** U1 (importante), U4 y U7. |
| **T3** `origenes` lista de textos | **Corregido** | `q2` D y `regresion_v3/p6`: objeto, texto o lista con un elemento que no es texto → error del contrato; con la lista, cambiar la evidencia del origen y resellar solo el origen deja el derivado desactualizado. |
| **T4** tipo de fuente por contenido | **Corregido en lo principal** | `q12` A1: bytes ajenos como `.pdf.bak`, `.bin`, sin extensión → pendiente; `.html` → discrepancia; `.pdf` sin cabecera → discrepancia. Página sin capa de texto → pendiente. `r4`: PDF sin extensión con cabecera → se contrasta con pdftotext; PDF con 295 bytes de basura delante y extensión `.pdf` → comprobada. **PDF reales:** Elis 244 de 244 y Viscofan 225 de 225, 0 rechazos por el control. **HTML real** (Elis, OCEANE 2029): la cita verdadera pasa; la misma con otra cifra → discrepancia. Residuos: U5. |
| **T5** modo de la entrada efectiva | **Corregido como se declara** | `q7`, `r5`: `cambiar_base` registra el modo en `entrada_efectiva.json` y en `fase1_metadatos.json`; borrar el archivo, renombrarlo, contradecirlo, otra grafía con mayúsculas, errata o forma de objeto en `alcance_v2.json` → `ValueError` y el paso 2 termina `no_entregable`; `estado_pipeline.json` lleva `{"modo", "declarado_en"}`. Lo que queda: U6. |
| **T6** mensajes y rótulos | **Corregido** | `q1` D: `sellar` da el motivo propio («la justificación de la materialidad no explica nada»); `resumen` ya no es `None` sin registro ni sin libro (`q1` F); `regresion_v3/q9`: ya no queda ningún `:g` en los mensajes. Restos triviales en U9. |
| **T7** pruebas | **Corregido, con un hueco** | h17 detecta la mutación; el caso del componente exige «no es un objeto»; el caso P dice que comprueba el texto; casos nuevos T1–T5, informe con registro apto y diagnóstico `None`. Hueco: U8. |
| **T8** documentación, manifiesto y reconstrucción | **Corregido en este árbol** | Manifiesto: 6.935 · 0 · 0 · 0 (lógica del bloque de `verificar_paquete.sh`, en lectura). Recuentos de `HITO_1_4_15.md` y `CONTINUIDAD.md` comprobados (§6). Los ocho JSON de la reconstrucción son de las 15:33–15:38 y llevan `modo_entrada_efectiva` (casos 3 y 4 «estricta»); el revisor no ha repetido la reconstrucción. Pendientes en U9. |

**[Hecho] Regresión de lo ya corregido** (`v4/regresion_v3/`, 12 sondas): las salidas coinciden con las de la tercera pasada salvo en lo que cambian T1–T6 (mensajes con `repr`, «escribe cifras» en lugar de «usa []», mensaje de T3, 214 por 215). N1 y N3 (`q1`), N5 y N7 (`q7`), N8, 12 y 13 siguen corregidos. La línea (3) de `p7` (213 o 214 comprobadas tras sellar) depende del orden en que la sonda recorre a los revisores; con un orden fijo, 215 en el árbol anterior y 214 en este.

## 4. Hallazgos nuevos

### Importante

**U1 · T2: una cifra sigue pudiendo escribirse en la fórmula, con constantes admitidas o sin ninguna, y el control de sensibilidad lo da por bueno.**
- **[Hecho]** `r2_t2_cifras.py` A. `Historia!F6` (ventas 2019 = 849,697, dato de cálculo) sin fuente, como derivado de `Historia!F5` (el año, 2019, comprobado). Con cada una de estas fórmulas: `apto=True comprobadas=321/321 … err=0`, `datos_como_hipotesis: []`, y `VE._constantes_no_admitidas` devuelve `[]`:

| Variante | Fórmula |
|---|---|
| año − cifra compuesta | `o["Historia!F5"] - (1*1000 + 1*100 + 6*10 + 9 + 3/10 + 3/1000)` |
| codo de `max` | `(8*100 + 4*10 + 9 + 6/10 + 9/100 + 7/1000) + max(o[…], (2*1000 + 1*10 + 9)) - (2*1000 + 1*10 + 9)` |
| `abs` | `(8*100 + … + 7/1000) + abs(o[…] - (2*1000 + 1*10 + 9))` |
| `round` negativo | `(8*100 + … + 7/1000) + round(o[…], -9)` |
| producto | `o[…] * (8*100000 + 4*10000 + 9*1000 + 6*100 + 9*10 + 7) / (2*1000 + 1*10 + 9) / 1000` |
| sin ningún literal salvo potencias de diez | `(o["Historia!L5"] - o["Historia!D5"]) * 100 + (o[L5] - o[H5]) * 10 + (o[L5] - o[C5]) + (o[L5] - o[F5]) / 10 + (o[L5] - o[C5]) / 100 + (o[L5] - o[E5]) / 1000` |

- **[Hecho]** En bloque (`r2` B): **los 155 datos numéricos publicados del cálculo**, sin fuente, como `o["Historia!F5"] ± (cifra compuesta)` y conservando la comprobación del fixture → `apto=True comprobadas=321/321`, `motivo: None`, `por_clase: {'derivado': 155, …}`, resumen `0 datos tratados como hipótesis o convención`. Con los 74 de juicio (229), igual. Sin revisor en los derivados → 155 pendientes, no apto.
- **[Hecho]** Causas. (a) Los literales se admiten por su valor, no por su papel: `8*100 + 4*10 + 9 + 6/10 + 9/100 + 7/1000` solo usa enteros de 1 a 12 y potencias de diez. (b) Un origen sumado «influye» siempre. (c) El control de sensibilidad trata `round` como identidad, así que `round(o[x], -9)`, que en la evaluación real vale 0, cuenta como un origen que influye. (d) Las diferencias entre años de la Historia (2016…2025) dan los dígitos sin escribir ninguno.
- **[Hecho]** `PV=<árbol de la tercera pasada>`: las mismas fórmulas pasaban también allí (`r2_t2_cifras_arbol3.log`). No es una regresión: es lo que la corrección de T2 no cierra.
- **[Interpretación]** Es el contraejemplo de N2 y de T2 con otra variación: un dato del cálculo queda «comprobado» sin contraste documental y sin aparecer en ninguna lista. Exige, como entonces, la firma de un revisor en cada derivado. La última fila de la tabla muestra que ninguna regla sobre los literales puede cerrarlo: que una fórmula derive de verdad el concepto es semántica, y eso es del revisor. `HITO_1_4_15.md` («Una fórmula no escribe cifras de la fuente»; «Cada origen tiene que influir en el resultado») y `CONTINUIDAD.md` («cada uno influye en el resultado y no escribe cifras de la fuente») afirman más de lo que el control garantiza.
- **[Propuesta]** (1) Declarar el límite en los dos documentos y en el docstring: el control descarta las formas triviales; no acredita que la fórmula derive el concepto. (2) Hacer visibles los derivados: su número en el `resumen` y en el informe (hoy solo está en `por_clase`). (3) Si se quiere endurecer, P1 de `r8_propuestas.py`: un literal solo como factor o divisor de una expresión que contiene un origen, o como decimales de `round` entre 0 y 12; nunca sumado, ni operado con otro literal, ni como argumento. Rechaza las cinco primeras filas y acepta los 148 derivados reales (0 afectados) y las fórmulas legítimas probadas. La sexta fila queda como límite declarado.

### Menores

**U2 · T1: las medias de un número par de valores que acaban en x,xxx5 (regresión restrictiva).**
- **[Hecho]** `r1_t1_exacta.py` B1, con el generador real (`fase1_historia.calcular_entrada`, «media», redondeo 3, que hace `round(sum / n, 3)` con floats): de 20.000 medias de valores con 3 decimales, el comprobador **rechaza el valor que escribe el generador** en el 11,0 % (n = 2), el 3,2 % (n = 4) y el 4,2 % (n = 6) de los casos con `derivacion.unidad` «mm»; con `round(…, 3)` en la fórmula, en el 25,3 %, 12,0 % y 8,4 %. Con n = 3 y n = 5, ninguno. Ejemplo: 1120,148 y 1528,871 → generador 1324,51; exacto 1324,5095; `round(float(exacto), 3)` = 1324,509.
- **[Hecho]** `r1` B2, en el registro: `Historia!D6` = 778,136 como `(o["aux:m1"] + o["aux:m2"]) / 2` con 678,210 y 878,061 y unidad «mm» → `discrepancia: la fórmula da 778.1355 y el modelo 778.136`. Con el código de la tercera pasada → comprobada.
- **[Hecho]** Causa: el resultado exacto es un empate, y lo resuelven tres reglas distintas: el generador (ruido del float), `_igual_libro` (`round` de Python sobre el float del exacto) y `_round_frac` (mitad lejos de cero). En los tres registros reales las medias son de 3 o 5 valores y no hay efecto: con `round(…, 4)` las 30 tasas de la fila 10 se reproducen, y con unidad «mm» las 12 medias del FCF base también (`q4b`).
- **[Propuesta]** P3 de `r8`: en un importe, aceptar si el libro tiene 3 decimales como mucho y |exacto − libro| ≤ 0,0005 (cualquiera de los dos sentidos del empate). Rechaza 0 de 20.000 en cada n y mantiene rechazados 849,0 por 849,697, 849,6976 por 849,697 y 0,2511 por 0,25.

**U3 · T1/T2: con un `round` de decimales enormes, `comprobar` no termina.**
- **[Hecho]** `r6_round_enorme.py`. Los decimales de `round` están exentos del límite de constantes y `_round_frac` calcula `10**n` con enteros de precisión arbitraria: n = 10⁶ → 0,1 s; 3·10⁶ → 0,7 s; 10⁷ → entre 5 y 6 s por evaluación. Con `round(o["aux:kv"], 999999999999)` en un derivado del registro, la CLI `comprobar` no termina en 60 s (proceso hijo cortado por la sonda). `comprobar` «nunca lanza», pero se queda colgado.
- **[Hecho]** La exención es asimétrica: `round(x, 15)` se admite y `round(x, -15)` da «escribe cifras [15]» (el signo es un nodo aparte).
- **[Propuesta]** Decimales de `round` entre 0 y 12 (o entre −12 y 12), con error del contrato fuera de ese rango.

**U4 · T2: el control de sensibilidad y el de constantes rechazan derivaciones legítimas en casos límite.**
- **[Hecho]** `r2` C, con orígenes publicados y comprobados → `error: los orígenes [...] no influyen en el resultado`: (a) un origen que vale exactamente −1 (`o["aux:a1"] + o["aux:m1"]`): −1 es el punto fijo de la perturbación v·(1 + 1e-7) + 1e-7; (b) producto con un cero comprobado (`o["aux:t"] * o["aux:z"]`); (c) cociente 0 / d; (d) `max(o[a], o[b])` para el argumento que no es el mayor. Y `max(o[x] - o[b], 0)` → «escribe cifras [0]»: el 0 no es una constante admitida (tampoco 0,5, 52, 360 o 365).
- **[Hecho]** Ningún derivado real cae en estos casos (`q4b`: 0 orígenes inertes, 0 constantes no admitidas, 0 orígenes de clase no admitida en 148).
- **[Propuesta]** P2 de `r8`: comprobar la dependencia en tres puntos genéricos, no en los valores reales. Acepta los cuatro casos y sigue rechazando `o[x] * 0 + c`, `o[x] − o[x] + o[y]` y `abs(o[a], o[b])`.

**U5 · T4: lo que queda en HTML y en PDF.**
- **[Hecho]** `r4_t4_tipo.py` A. La cita solo en un comentario (A2), en un atributo (A4) o en un `<script>` bien cerrado (A6) → discrepancia: bien. Pero las etiquetas se quitan con una expresión regular, y **se acepta** la cita que solo está: en un comentario con un «>» antes de la cita (A3); en un atributo con un «>» (A5, `<meta content="resumen > …">`); en un `<script>` cerrado con `</script >` (A7) o sin cerrar (A8); en el `<title>` (A9); en un elemento oculto o un `<template>` (A10). También se acepta una cifra que el HTML no contiene, partida en dos celdas contiguas («849» y «697.000», A11), porque la comparación quita todos los espacios (igual que en el PDF).
- **[Hecho]** Rechazos falsos: un HTML legítimo con la cita, en ISO-8859-1 (A12) o UTF-16 (A13) → `discrepancia: la cita está en el texto conservado, pero no en la fuente HTML` (se lee siempre como UTF-8). Ningún registro real cita un HTML (los 715 datos con fuente de los tres registros citan un `.txt`; `q4b`).
- **[Hecho]** PDF. El mismo PDF con basura delante y sin extensión `.pdf` (B2, B3) → pendiente con el mensaje «no es un PDF…», que no es cierto. Una página cuya única capa de texto es un encabezado (B6, escaneado con sello o cabecera digital) → `discrepancia … el texto conservado no es el de ese documento`: la afirmación no comprobada que T4 retiró solo para la página totalmente vacía. Un PDF que pdftotext no extrae sigue siendo «discrepancia» (leído; B8).
- **[Propuesta]** Extraer el texto con `html.parser` (comentarios, atributos, `script`, `style`, `template`) y decodificar por BOM o `meta charset`; buscar `%PDF-` en los primeros 1.024 bytes también para decidir el tipo; cuando la página del PDF da poco texto y no contiene la cita, «pendiente».

**U6 · T5: lo que queda abierto.**
- **[Hecho]** `r5_t5_modo.py`. (a) El segundo rastro falla en abierto: con `entrada_efectiva.json` borrado y `fase1_metadatos.json` sin la clave, ilegible o borrado, el modo es `('registrada', None)` y el paso 2 del expediente estricto de `cambiar_base` (con el conflicto de C48 repuesto) termina con C48 = 108; queda el rastro `{"modo": "registrada", "declarado_en": None}` en `estado_pipeline.json`. (b) `alcance_v2.json` ilegible, con la clave mal escrita («entrada_efectiba») o en forma de lista → «registrada». (c) `entrada_efectiva.json` «registrada» con motivo «x» y `alcance_v2.json` «estricta» → gana «registrada», sin error. (d) Otras grafías del nombre (`entrada-efectiva.json`, `.json.bak`, `entradaefectiva.json`) no se detectan si los metadatos no registran el modo. (e) El modo no está en la ficha, el informe ni `cierre_v2.MATERIAL_FIJO` (declarado como pendiente de la fase 2). (f) Un expediente creado de cero, sin `cambiar_base`, sigue en «registrada». (g) Ningún expediente del árbol declara todavía un modo.
- **[Interpretación]** La comprobación de entradas sigue bloqueando la aptitud en cualquier modo. Con dos archivos que retirar o editar y el rastro en `estado_pipeline.json`, el residuo es menor. (a)–(d) pueden declararse.

**U7 · Escala: una unidad monetaria con una grafía no reconocida solo exige una potencia de diez.**
- **[Hecho]** `r2` D. La fuente dice «(en miles de euros): 849,697» y el modelo tiene 849,697 millones: con unidad «miles de €» (no reconocida), escala 1 y `valor_fuente` 849,697 → `apto=True … comprobada`; con «miles de euros» (reconocida) → `error: escala 1 incoherente con las unidades`. Tampoco se reconocen «euro», «€», «en miles de euros», «MM€» o «USD». Una conversión de divisa (escala 1,0842 con «USD (millones)») pasa a ser error: es un derivado con el tipo de cambio como origen. En los registros reales las unidades monetarias son reconocidas y las demás escalas son 1 o 1e-06.
- **[Propuesta]** Unidad con «€», «eur» o «euro» fuera del vocabulario → pendiente (o ampliar el vocabulario).

**U8 · Pruebas.**
- **[Hecho]** (a) Ningún caso de la batería distingue el control de constantes: sin él, 105/105; los casos que lo nombran caen también por la regla de los orígenes o por la sensibilidad. (b) Los dos casos del auxiliar `dato_ausente`/`no_aplicable` aceptan el error del derivado o el del auxiliar: quitando una sola de las dos reglas seguirían pasando (leído). (c) No hay caso para: cifra compuesta (U1), empate de una media par (U2), decimales de `round` (U3), origen −1 o producto con cero (U4), HTML con la cita en un comentario o en otra codificación (U5), metadatos ilegibles (U6).
- **[Propuesta]** Un caso que solo detecte el control de constantes (p. ej. `o[a] + o[b] + 13 - 13` con el valor exacto) y uno por cada residuo que se corrija.

**U9 · Documentación, manifiesto y restos triviales.**
- **[Hecho]** (a) `HITO_1_4_15.md` §7 cita `resultados/verificacion_completa_hito1.txt`, que no está en el árbol congelado (la regresión estaba en marcha); `CONTINUIDAD.md` da ya «199/199». Al añadir ese archivo y esta revisión habrá que regenerar el manifiesto y la lista de cambios. (b) El párrafo de N4 del §1 sigue diciendo «salvo el ruido de la aritmética de coma flotante (1e-9 relativo a la magnitud de los orígenes)», que T1 retiró. (c) Las frases de T2 del §1 y de `CONTINUIDAD.md` (U1). (d) `CONTINUIDAD.md` dice «tres pasadas de Fable». (e) El docstring de `verificacion_entradas.py` no recoge T1–T5, y `_eval_formula` (floats) ya no lo llama nadie. (f) `PROMPT_NUEVA_VENTANA.md` es el de la 4.14 (198/198, sin las baterías nuevas); fuera del alcance declarado del hito.
- **[Hecho]** Triviales: el informe sigue diciendo «N de juicio declaradas no materiales» y `motivo` «entradas de juicio no materiales», aunque cuentan auxiliares (`informe.py` no cambia); «el texto de la fuente '…' no existe» para un `archivo_texto` fuera del paquete; «media 2025–2023» en la fuente generada; el evaluador exacto admite `sum(a, b)`, ignora el segundo argumento de `abs` (lo detecta la sensibilidad) y evalúa `(o["a"],)["b"]` como `o["b"]` (lo detecta la regla de los orígenes); `sum([])` da un 0 sin escribirlo.

## 5. Regresiones

- **[Hecho] Hacia lo permisivo:** ninguna de fondo. Las doce sondas de regresión y las ocho adaptadas no muestran nada que antes se rechazara y ahora se acepte. La única forma encontrada es sintáctica: `round(sum(o[a], o[b]) / 2, 3)` (`sum` sin lista) era «fórmula no evaluable» y ahora se comprueba (`r1` B2); el valor se deriva igualmente de sus dos orígenes.
- **[Hecho] Hacia lo restrictivo, en los registros reales:** ninguna fuera de lo declarado. Diagnóstico regenerado idéntico al entregado; frente al de la tercera pasada, la única entrada que cambia de estado es `Historia!L10` de Viscofan (los demás cambios son el último dígito de los mensajes). De los 148 derivados reales, ninguno incumple las reglas nuevas de constantes, clases de origen, forma de `origenes` o sensibilidad. 0 rechazos falsos en las 469 entradas reales con PDF.
- **[Hecho] Hacia lo restrictivo, fuera de los registros reales:** U2 (medias pares), U4 (−1, ceros, `max`, constante 0), U5 (HTML en ISO-8859-1 o UTF-16) y la conversión de divisa de U7.

## 6. Documentación y manifiesto

- **[Hecho]** Comprobado contra lo ejecutado o leído: 105/105, 40/40 y 33/33; mínimos 105, 40 y 199; diagnóstico 214/232 (1 error, 17 discrepancias, 0 no reproducibles), 207/226 (4, 15, 1) y 175/193 (1, 17, 1); su desglose (10 tasas de la fila 10 en cada uno; medias del FCF base 4, 2 y 3; 3 textos sin `equivalencia` en cada uno; «mm» en los tres; C49, C50 y H23 de Vidrala); universos de 321, 311 y 292 celdas; la regresión intermedia con 197/198 (`verificacion_completa_hito1_intermedia.txt`); los 11 archivos cambiados frente a la 4.14 en `CAMBIOS_ARCHIVOS.txt`, que coinciden con el §9; la tabla de la reconstrucción frente a sus ocho JSON.
- **[Hecho]** No comprobado por el revisor: el 32/35 de `comprobar_entrega_4_14.py`, el 199/199 de la integración y la reconstrucción (LibreOffice).
- **[Hecho]** Lo que no corresponde: U9 (a)–(d).

## 7. §3 del encargo

- **[Hecho]** Mejora respecto a la tercera pasada: el modo queda registrado en dos sitios, su falta o contradicción detiene el paso 2, y la parada estricta tiene un caso propio en la batería de integración, cuya expresión el revisor ha evaluado sin LibreOffice (PASA).
- **[Interpretación]** Sigue pudiendo declararse cumplido **con matices**, los mismos que el §8 del documento reconoce, más U6 (a) y (f).

## 8. Límites de esta revisión

- No se ha ejecutado nada con LibreOffice. De la integración, solo el caso nuevo del grupo D y los pasos 1–2.
- Los contraejemplos son sintéticos (fixture de Viscofan 4.13 con vínculo escrito a mano, como las baterías) salvo donde se dice «real»: `Historia!L10` de Viscofan, los 148 derivados y las unidades de los tres registros de la 4.14, los PDF de Elis y Viscofan y el HTML de Elis. No demuestran que los registros reales usen esas palancas: no las usan.
- P1–P3 de `r8` son comprobaciones de apoyo sobre fórmulas y registros reales, no una implementación revisada.
- No se han revisado I19, I20 ni F1. La revisión no es humana ni sustituye a la externa.

## 9. Resumen en 10 líneas

1. Las tres baterías pasan en la copia del árbol congelado: 105/105, 40/40 y 33/33; el caso nuevo de la integración (parada estricta por C50) da PASA sin LibreOffice.
2. T1, T3, T4, T5, T6, T7 y T8 están corregidos; los contraejemplos literales de la tercera pasada ya no pasan y el manifiesto corresponde al árbol (6.935 · 0 · 0 · 0).
3. Registros reales: diagnóstico idéntico al entregado (214/232, 207/226, 175/193); solo cambia `Historia!L10` de Viscofan; 0 de 148 derivados y 0 de 469 entradas con PDF afectados.
4. U1 (importante, residuo de T2): una cifra se escribe con dígitos × potencias de diez (`o[año] - (1*1000 + 1*100 + 6*10 + 9 + 3/10 + 3/1000)`); los 155 datos de cálculo quedan `apto=True`, sin fuente y sin listar.
5. U1 no se cierra con reglas sobre literales: las diferencias entre años de la Historia dan los dígitos; hay que declararlo como límite y corregir las frases de T2 en los dos documentos.
6. U2: la aritmética exacta rechaza el 11 % de las medias de dos valores que escribe el propio generador (empates x,xxx5); en los registros reales (medias de 3 y 5) no ocurre.
7. U3: `round(x, 999999999999)` deja `comprobar` sin terminar; U4: el control de sensibilidad rechaza un origen −1, un producto con cero, 0 / d y `max`.
8. U5: en HTML se acepta la cita que solo está en un comentario o atributo con «>», en un `<script>` sin cerrar, en el `<title>` o en un elemento oculto; un HTML en ISO-8859-1 se rechaza en falso.
9. U6–U9: el modo vuelve a «registrada» si faltan el archivo y los metadatos; ninguna prueba distingue el control de constantes; falta `verificacion_completa_hito1.txt` y sobra una frase de N4.
10. Veredicto: ACEPTABLE CON CORRECCIONES, ninguna bloqueante; con el límite de U1 declarado y, si se quiere, P1–P3 de `r8`, no hace falta otra pasada completa.
