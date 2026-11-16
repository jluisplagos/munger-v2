# Revisión independiente n.º 9 · frente E · F1 · Elis · lo afectado por C18

Fecha: 16-nov-2026. Material revisado: commit congelado `06ad1003aa5320445d0c42498c3d0efaec971f06` (C19) de la rama `auditoria/economica-f1-frente-e`. C19 solo añade a C18 (`f12f8ea79ed5c1b444d85163c5ed08d8d07a6243`) el registro de su hash (comprobado: `git diff f12f8ea 06ad100` toca `ESTADO.md`, la línea de C18 en las respuestas y el manifiesto). Alcance: `git diff 63e6090 f12f8ea`, es decir, la respuesta a T1–T8 (43 archivos), en tres commits: `d3c0f1b` (verificador y test), `485de8d` (segunda parte del código) y `f12f8ea`. De código solo cambian `verificar_cifras.py` y `test_verificar_cifras.py`, y se añade `barrido_fecha_rotulo.py`; el contraste, la regeneración del CSV, la mutación, las sondas y los datos no cambian desde C17 (`git diff 863ddde 06ad100` vacío para esos archivos). Base de comparación, en su propio worktree: C17 (`863ddde…`), que tiene el código de C16. Los verificadores de `d3c0f1b`, de `485de8d` y de C14 (el de `c96d544`) se han sacado con `git show`.

Se publica en la rama `auditoria/economica-f1-frente-e-revision`, sobre el commit 3138a6b.

Marcas: **[P]** publicado (leído en el PDF) · **[D]** derivado · **[I]** interpretación · **[H]** hipótesis.

Este documento no contiene valoraciones, precios, recomendaciones de inversión ni declaraciones de aptitud. No adopta ninguna decisión pendiente. Se conservan C48 = 108 y E1/D3/E2/E6. No modifica el material del autor, el producto ni los libros.

---

## 0. Resultado en breve

1. **Las cifras que declara el autor se reproducen todas**, con salidas idénticas byte a byte (§2): 752 filas (738 OK, 14 PENDIENTE, 0 FALLO), iguales a las de C16 en todos sus campos; 136/136 casos y 9/9 comprobaciones directas; con el verificador de C16, 119/136 y 4/9, y con el de `d3c0f1b`, 134/136 y 8/9; 292 comprobaciones del contraste; 24/24; 530 filas de mutación; 713/713 en las sondas; referencia de E9 sin cambios.
2. **Los scripts de las revisiones n.º 6 a 8 sobre C18**, vueltos a ejecutar sin cambios: 16 de 19. Doce salidas son idénticas a las que guarda el autor y cuatro difieren en lo esperable (la línea del tiempo, el recuento del manifiesto en las dos reproducciones y la tipografía, que aquí no he podido leer). Los tres que faltan necesitan una biblioteca que este entorno no tiene (§1 y §4.8).
3. **Mi barrido propio** (51.492 tokens de las 2.026 páginas, 154.476 candidatas) da las mismas transiciones que declara el autor: 414 de OK a PENDIENTE, 101 de PENDIENTE a FALLO, 588 de FALLO a PENDIENTE y **ninguna candidata pasa a OK**. Todas se explican por T1–T5 y por la regla del año del rótulo (§4.2). Coincide con el barrido de la revisión n.º 8, escrito por separado.
4. **T1.** De las 411 aceptaciones que la regla de la fecha daba en C16 quedan diez, y las diez están en tablas de una sola columna: lo he comprobado leyendo la cabecera de cada una [P]. **No queda ningún saldo OK cuya columna nadie compruebe** en las cinco publicaciones. La regla mide «una sola columna» en la fila, no en la tabla (U3).
5. **T2.** La regla da ejercicio en 207 líneas; frente a C16, 200 iguales, 7 nuevas y 500 fuera, como dice el autor. **Ningún saldo en millones de euros queda fuera** [P][D]: lo he comprobado con una clasificación propia de las 364 líneas con una fecha completa en el rótulo y cifras a su derecha (§4.4). Pero de las 207, saldos en millones de euros de páginas del grupo son 114. Entre las demás hay 24 filas de recuentos de planes de acciones, 20 de la tabla del capital social y 6 entradas de sumario: «los recuentos con fecha vuelven a la regla de las columnas» solo es cierto para una parte (U2).
6. **T3.** Las siete líneas nuevas son rótulos de su propio saldo [P]; los saldos de apertura y de cierre de los diez estados de cambios en el patrimonio quedan reconocidos. La unión de líneas que terminan en el día o en el año no tiene ningún efecto fuera de esas siete (§4.5).
7. **La regla nueva de `f12f8ea` sí retira cifras** (U1). Retira 2.722 tokens; 2.704 son años o días de un rótulo. De los otros 18, **ocho son ceros reales** de filas de planes de acciones («as at 12/31/2025 · 0 · 92,485 …») que la regla da por «el día de la fecha». La causa es anterior a C18: el verificador localiza cada token buscando su texto en la línea, y el «0» aparece antes dentro de la fecha del rótulo. Con esa búsqueda, 385 tokens de 299 líneas quedan en una posición que no es la suya; **ninguno es de una fila real del CSV**. En tres publicaciones desplaza una columna la fila «Number of fatal accidents» [P].
8. **T4, T5 y T6** corrigen lo señalado y sus recuentos son exactos (§4.7). Efectos laterales, sin cambio de estado: dos líneas de organigrama reciben una cabecera de países (T4) y 34 filas hechas solo de cifras, que empiezan por un dígito suelto, se tratan como la pestaña del capítulo (T5, U4).
9. **Los límites declarados se sostienen** (§5), con dos precisiones: el coste de T2 no está bien descrito (U2) y el límite de T2 es más ancho de lo que dice T14 (U5 d).
10. **El test prueba lo que dice** (§6). Los 19 casos nuevos y las nueve comprobaciones directas distinguen el código de C18 del de C16 y del de `d3c0f1b`.
11. **Documentos** (§8): los recuentos coinciden entre sí y con las salidas. Seis frases son más fuertes que su prueba o inexactas (U6); la más clara, en E9: dice que en R42 de 2023–25 no interviene ninguna de las 97 entradas, y su propia fuente lista cinco intervenciones.
12. **Objeciones nuevas: U1 y U2 (menores) y U3–U6 (forma). Ninguna afecta a las 752 filas reales. Ninguna conclusión material cambia.** No he encontrado ningún error en los datos reales.

---

## 1. Encargo, configuración y límites de la independencia

**Encargo.** Mensaje recibido al crearse esta sesión, entregado como aviso automático y no tecleado por una persona en ella. Lo trato como un encargo de revisión, no como una conclusión que confirmar: no doy por cierta ninguna descripción del autor sin comprobarla.

**Configuración.** Aquí no se escriben identificadores de modelo. Quien encarga puede leer la configuración de esta sesión en sus metadatos.

**Límites de la independencia:**
- **Quien encarga fija el alcance** y señala qué mirar: los recuentos de T1, las tres condiciones de T2, la unión de T3, el rótulo más corto, la regla del año del rótulo, T4–T6 y los límites declarados.
- **He leído la revisión n.º 8 entera y la octava parte de las respuestas antes que el código**, y he usado los scripts de las revisiones n.º 6 a 8 para comprobar las salidas guardadas. Esta sesión es nueva y no conserva el contexto de ninguna pasada, pero parte de sus informes y de su universo de casos.
- **La herramienta de extracción es común.** Mi barrido usa `pdftotext` por fuerza: es la entrada del verificador. Lo he reducido así:
  - la posición de cada token la calculo con un tokenizador propio, celda a celda, que da los mismos tokens que el verificador en las 22.594 líneas con cifras (`spans_9.py`). Son 54.248 tokens contando los 2.756 marcadores («-»), que el barrido no declara como cifras: de ahí sus 51.492 tokens en 22.324 líneas;
  - las filas de U1 están leídas con pdfminer, otro motor, con la coordenada de cada palabra (`lectura_posiciones_9.py`), y dos de ellas, vistas en la página renderizada: URD 2025 p.360 y URD 2021 p.176;
  - un error de extracción común a `pdftotext` y a mis lecturas con esa herramienta no se detectaría.
- **No he podido usar MuPDF.** El entorno no trae PyMuPDF y no se me permitió instalarlo. Por eso no he vuelto a ejecutar `barrido_7.py`, `clases_7.py` ni `lectura_filas_c14.py`, y `clases_8.py` sale sin la tipografía de su sección K. Lo que esas salidas dicen del perímetro en las líneas sin rótulo lo he comprobado con mi barrido (§4.7).
- **Mis clases son un filtro, no una verdad.** He leído una a una las 207 líneas en que la regla da ejercicio, las 32 con cifras que C18 deja fuera, las firmas de las 187 líneas con fecha y sin regla, las 16 que toman la fecha de arriba, los 18 tokens mal retirados, las 26 líneas de una sola columna con la cabecera de su tabla y las líneas en que cambia cada función. No he mirado las 154.476 candidatas una a una.
- **Las sondas sintéticas son mías** y sus páginas, inventadas: lo que muestran es hipotético [H] mientras no aparezca en una publicación. El informe da, junto a cada una, cuántas líneas reales tienen esa forma.
- **Los identificadores de sondeo de los demás modos son míos** (15). Fijan el modo por su prefijo, como hace el verificador; no son filas del autor.
- Mi barrido llama a `comprobar_tabla`, la función que la ejecución oficial usa para cada fila. Equivalencia comprobada en las 713 filas de tabla reales de C16 y de C18: los mismos estados y detalles. Los contraejemplos de `contraejemplos_9.py` no la usan: ejecutan el verificador oficial como proceso aparte.
- **Esta sesión es distinta de la autora y de las ocho revisiones anteriores, pero es un agente de la misma clase**, no una persona, y recibe el encargo por el mismo cauce. Un sesgo de lectura común a esa clase no se descarta.

---

## 2. Reproducción (alcance 1)

Base 4.14 materializada desde el ZIP original de la Release (1.130.912.246 bytes, SHA-256 `bb51942c…b93e`) con `tools/base_414.py`, en un worktree de `main`: 6.798 de 6.798, `complete: true`. Libro `d2593777…92385`. Las cinco fuentes, con la huella de `fuentes.json`. Ejecución sobre una copia de la carpeta del worktree de C19. Prueba: `reproduccion_9.py` → `resultados_revisor_9/reproduccion_9.txt`.

| Cifra declarada | Resultado |
|---|---|
| Manifiesto | 324 de 324 |
| CSV regenerado desde los PDF | Idéntico (752 filas: 713 de tabla y 39 de texto; SHA-256 `3f9ae6e6…1331`), e idéntico al de C17 |
| Verificador: 752 filas, 738 OK, 14 PENDIENTE, 0 FALLO | Reproducido. Código 2. JSON y registro idénticos. Las 73 páginas exportadas, idénticas. Las 14 PENDIENTE, del URD 2022 p.302 |
| «Salida idéntica byte a byte a la de C16» | Cierto. El verificador de C16 sobre el mismo CSV da un JSON idéntico al de C18 y al que guarda C17: ninguna de las 752 filas cambia en ningún campo. Las 73 páginas que exporta, idénticas |
| `test_verificar_cifras`: 136/136 y 9/9 | Reproducido. Registro idéntico. Composición: 23 OK, 36 PENDIENTE y 77 FALLO esperados |
| «Con el verificador de C16, 119/136 y 4/9; con el de `d3c0f1b`, 134/136 y 8/9» | Reproducido, ejecutando el test de C18 con cada verificador. Con el de `d3c0f1b` fallan los tres que dice el autor: el caso de la reserva de coberturas, el del año del rótulo y la comprobación de la viñeta |
| Contraste: 292 comprobaciones (136 del libro, 127 de fuente, 29 algebraicas), 0 fallidas, 419 entradas | Reproducido. Código 0. JSON, tabla y registro idénticos, y los tres idénticos a los de C17 |
| `test_contraste_residuos`: 24/24 | Reproducido. Registro idéntico |
| `cobertura_por_mutacion`: 530 filas, sin incoherencias | Reproducido. Salida idéntica a la guardada y a la de C17: 386 por identidad, 2 solo libro, 23 sin detectar y 119 no usadas |
| Sondas: 713/713 en unidad y en perímetro | Reproducido. JSON idéntico al guardado; igual al de C16 salvo la etiqueta de versión |
| Referencias de E9 sin cambios | `referencia_especificacion` es igual en C17 y en la ejecución de hoy (C53 de A1, 2,445331695332; de A2, 1,612524303305) |
| `barrido_fecha_rotulo.py`: 207 líneas (191 y 16); frente a C16, 200, 7 y 500 (302 de una celda y 198 de dos o más, 166 de ellas con un token o ninguno) | Reproducido. Salida idéntica a la guardada. Mi barrido, con otro arnés, da los mismos seis recuentos (`clases_9.txt`, C) |
| Scripts de las revisiones n.º 6 a 8 sobre C18 | Vueltos a ejecutar 16 de 19 (`relanzar_revisores_6_8.sh` → `comparacion_6_8.txt`): §4.8 |
| «Scripts de los revisores n.º 1 a 5: mismas salidas que sobre C16, salvo `barrido_tablas`» | No los he vuelto a ejecutar. He comparado las salidas que guarda el autor sobre C16 y sobre C18, igualada la etiqueta de versión: nueve son iguales y `barrido_tablas` difiere en 141 líneas, como dice. En ella, las candidatas OK bajan de 6.395 a 6.059 y 1.298 pasan de NO_APLICA a PENDIENTE en columna, como dice |

`prueba_caja_no_nula.py` y sus dos salidas no cambian desde C4 (`git diff d2e585e 06ad100` vacío para los tres archivos). No la he repetido: no he usado LibreOffice.

---

## 3. Estado de T1–T8 (alcance 2)

Los casos T son los de la revisión n.º 8 (`contraejemplos_8` sobre C18, reproducido e idéntico). Sus letras no siguen el número de la objeción: T4a y T4b son de la objeción T2 (la fecha de la línea de encima); T5a–T5d, de la objeción T4; y T6a–T6c, de la objeción T5. Los casos U y H son los míos: `contraejemplos_9.txt` (filas reales, verificador oficial de C16 y de C18 como proceso aparte) y `sondas_sinteticas_9.txt` (páginas inventadas).

| Objeción | Estado | Prueba |
|---|---|---|
| T1 · un saldo de una tabla con columnas por concepto quedaba OK sin que nada comprobara la columna | **Corregida**, con un límite no declarado | T1a, T1d y T1e, de OK a PENDIENTE de columna; T1b, FALLO; T1c, OK. De las 411 aceptaciones quedan diez, todas en tablas de una sola columna [P]. «Una sola columna» se cuenta en los tokens de la fila: U3 |
| T2 · la regla se disparaba en líneas que no son filas de saldo y daba el ejercicio a tokens que no son cifras | **Corregida en sus casos; resto y un efecto nuevo** | T2a–T2e, de OK a PENDIENTE. Las 500 líneas que salen no son saldos en millones [P][D]. Resto: la regla sigue en 24 filas de recuentos de planes, 20 del capital social y 6 de sumario (U2). Efecto nuevo: ocho ceros reales retirados como «el día de la fecha» (U1) |
| T3 · la regla no reconocía la mitad de los cierres del estado de cambios en el patrimonio | **Corregida** | T3a–T3e reciben el ejercicio; siete líneas nuevas, las siete rótulos de su saldo [P]. La unión con `fecha` no cambia nada fuera de ellas |
| T4 · en el DEU 2024 p.315 dos filas de la tabla del WACC por país conservaban el perímetro OK | **Corregida** | T5a y T5b, PENDIENTE. 54 candidatas (18 tokens) de OK a PENDIENTE, todas de esa página: es el único cambio de perímetro de ese sentido. Dos líneas de organigrama reciben además una cabecera de países, sin cambio de estado (U5 b) |
| T5 · el rótulo de las líneas contiguas tomaba líneas que no son el rótulo de la fila | **Corregida**, con una observación | De 2.015 líneas con cifras (327 del grupo) a 266 (16), como dice el autor. T6a deja de fallar, T6b vuelve a FALLO. El criterio de la pestaña es más ancho que el de `rotulo`: U4 |
| T6 · el criterio de la puntuación dejaba prosa dentro y títulos fuera | **Corregida en lo que declara** | De 409 a 407 encabezados en las páginas del grupo; de 982 a 976 en las demás sin la línea de debajo y a 980 con ella. Vuelven los cinco títulos en mayúsculas. Ningún estado cambia |
| T7 · frases más fuertes que su prueba | **(a), (b), (d), (e), (f) y (g), corregidas; (c), en parte** | Precisadas en su sitio. En E9, la lista de 2021–22 es exacta; la de 2023–25 omite R42 y afirma lo contrario de su fuente (U6 a) |
| T8 · varios | **Corregidas** | (a) El argumento retirado sale de T14 y lleva nota en la sexta parte. (b) El paso 4 manda leer las partes séptima y octava. (c) La cabecera del verificador describe las reglas nuevas. (d) Los tres URD, en el informe y en la séptima parte. (e) `reproduccion_7` dice 322 de 322 con código 0; sobre el congelado da 324 de 324, porque las dos salidas de reproducción se añaden después al manifiesto, y así se declara. (f) La copia de la revisión n.º 8 es idéntica: 18 de 18 archivos |

---

## 4. Verificador (alcance 2)

### 4.1 Método

- **Barrido propio** (`barrido_9.py`). Todas las líneas no vacías de las 2.026 páginas. Dos niveles:
  - **funciones**: cada función que C18 cambia o añade se llama directamente sobre cada línea, o sobre cada token, con el código de C16 y con el de C18: la regla de la fecha del rótulo con y sin posición, el rótulo del saldo, la unión con y sin `fecha`, las columnas de datos, `token_del_rotulo`, la cabecera de países, los rótulos contiguos, el encabezado numerado con la línea de debajo y sin ella, la zona de cabecera y el título de país. Cuatro funciones que C18 reescribe sin querer cambiarlas dan lo mismo en las 25.351 líneas registradas;
  - **filas**: cada token se declara como cifra del grupo en el modo de dos columnas, con el ejercicio de la publicación, el anterior y el segundo anterior: 154.476 candidatas, evaluadas con `comprobar_tabla` de las dos versiones. Además, el perímetro de cada uno de los siete segmentos.
- **Los demás modos** (`modos_9.py`): fuera del modo de dos columnas, el resultado solo puede cambiar por `token_del_rotulo` o por la zona de cabecera. Los 2.722 tokens por los que pasa uno de esos dos caminos se evalúan con 15 identificadores de sondeo.
- **Clases y consultas** (`clases_9.py`, `consultas_9.py`), con una clasificación propia de las líneas con fecha: otra expresión de la fecha y otra unión de las líneas de encima, más ancha que la del autor.
- **Posición de los tokens** (`spans_9.py`): §4.6 y U1.
- **Versiones intermedias** (`intermedias_9.py`): lo que la octava parte dice de `d3c0f1b` y de `485de8d`.
- **Contraejemplos** con el verificador oficial como proceso aparte (`contraejemplos_9.py`, 19 casos) y **sondas sintéticas** (`sondas_sinteticas_9.py`, 14).

### 4.2 Transiciones entre C16 y C18 (todas las páginas)

| Transición de la fila | Candidatas | Causa [D] (`clases_9.txt`, A; `consultas_9.txt`, Q1) |
|---|---|---|
| No OK → OK | 0 | — |
| OK → PENDIENTE | 414 | 331 por la columna (T1): cifras de saldos en filas de varias columnas. 80 por la regla de `f12f8ea`: 78 años de un rótulo y los dos «31» de «DECEMBER, 31». 3 por T2: el año de la línea de prosa del DEU 2024 p.257 y dos pestañas «6» |
| PENDIENTE → FALLO | 101 | 69 por T3: cifras de los cierres que ahora se reconocen, declaradas con otro ejercicio. 32 por T2: recuentos con fecha cuyo ejercicio vuelve a la regla de las columnas |
| FALLO → PENDIENTE | 588 | 541 años de un rótulo declarados con otro ejercicio. 10 con el motivo «día de la fecha»: dos son días y **ocho son ceros reales** (U1). 31 por T2 y 6 por T5 (la pestaña junto a un párrafo) |
| OK → OK | 5.526 | — |

OK en las seis dimensiones: 5.940 en C16 y 5.526 en C18. Son los recuentos del autor. Por dimensión: columna, 2.346 de NO_APLICA a PENDIENTE; ejercicio, 1.951 cambios; perímetro, 54 de OK a PENDIENTE y 9 de FALLO a OK. En el universo del barrido de la revisión n.º 6, vuelto a ejecutar: 336, 101 y 35, y 2.310 candidatas de columna (770 tokens, 54 páginas), como dice el autor.

**Los demás modos** (`modos_9.txt`). Ninguna candidata pasa a OK. Dejan de ser OK 18, todas el año de un rótulo: fechas, dos pies de página y una línea de prosa. Es lo que dice el autor y lo que da `barrido_8` sobre C18.

### 4.3 T1: qué queda OK

- **Las diez que quedan** [P] (`clases_9.txt`, B): los saldos de apertura y de cierre de la tabla de deterioro de clientes de las cinco publicaciones. Las diez tienen «columna» en NO_APLICA con el motivo «una sola columna de datos».
- **Las tablas son de una sola columna** [P]. La regla da ejercicio en 26 líneas con una sola columna de datos. He leído la cabecera de la tabla de las 26: «Impairment loss» o «Dépréciation» (10); «Total equity» o «Capitaux propres» de las cuentas de la sociedad dominante (6, en millones) y la misma tabla de los URD 2021 y 2022, en miles de euros y sin título de columna (4); y seis entradas de sumario. Ninguna tabla tiene otra columna, y en ninguna otra línea de esas tablas hay más de una cifra.
- **Fuera de esas diez, ninguna candidata queda OK con el ejercicio dado por la regla.** Las 2.346 candidatas a la derecha de un rótulo de saldo en filas de varias columnas tienen la columna PENDIENTE.
- **Coste** [D]: 331 cifras legítimas de saldos que C16 aceptaba vuelven a PENDIENTE. Es el lado prudente y el autor lo dice: «la regla de S1 casi no acredita».
- **Límite no declarado:** U3.

### 4.4 T2: dónde se dispara la regla y qué deja fuera

**Lo que deja fuera.** C16 daba ejercicio en 700 líneas y C18, en 207. Las 500 que salen son las que dice el autor: 302 de una sola celda y 198 de dos o más (166 con un token o ninguno y 32 con dos o más). He leído las 32: número de acciones (15), porcentaje de autocartera (5), derechos adquiridos (5) y otros recuentos de los planes (7). Ninguna es un saldo en millones de euros [P].

**Lo que podría faltar.** Para saber si la regla deja fuera saldos legítimos no basta con comparar con C16. He buscado, con una expresión propia de la fecha y una unión propia de las líneas de encima, todas las líneas cuyo rótulo lleva una fecha completa y que tienen alguna cifra a su derecha: **364 líneas** (`clases_9.txt`, C). La regla de C18 se dispara en 177 y no en 187. Clasificadas por las palabras que acompañan a la fecha (47 firmas):
- con la regla: «as at» (85), «au» (22), «net carrying amount as at» (22), «balance as at» (14), «valeur nette comptable au» (6) y «solde au» (5); esas mismas fórmulas con «restated», «retraité», «adjusted» o «published» (16); y siete rótulos del estado de cambios en el patrimonio partidos tras «as at», en los que mi unión se queda en la línea de la fecha;
- sin la regla, 104 con solo la fecha por rótulo (la tabla de la historia del capital, cabeceras con fechas, entradas de sumario y el total de una tabla por países rotulado «12/31/2022», que es un flujo) y 83 con otras palabras: recuentos de acciones y de planes, valores en euros de la autocartera, sensibilidades en porcentaje y prosa.

**Ninguna de las 187 es un saldo en millones de euros** [P][D]. En estas cinco publicaciones todos los rótulos de saldo con fecha tienen una de las formas que la regla admite. No hay ninguna línea de una sola celda con la fecha y una cifra pegada.

**Tampoco hay saldos a otra fecha** [P][D]. La regla solo admite el 1 de enero y el 31 de diciembre, y mi expresión, con el mes en letra, solo enero y diciembre. He buscado aparte cualquier mes: de las 408 líneas con una fecha completa en la primera celda y cifras a su derecha, 186 llevan una fecha que no es ninguna de esas dos. Solo cuatro están en páginas del grupo, y las dos únicas que dicen «as at» o «at» son prosa (URD 2021 p.245 y URD 2023 p.389). Con la fecha en una línea de rótulo de encima no hay ninguna.

**Dónde se dispara.** Mi clasificación de las 207 (`clases_9.txt`, B):

| Clase | Líneas |
|---|---|
| Saldo en millones de euros, página del grupo | 114 |
| Línea sin cifras a la derecha del rótulo (cabeceras con fecha) | 30 |
| Recuento de un plan de acciones con el rótulo partido antes de «as at» o «au» | 24 |
| Tabla del capital social (número de acciones, nominal y capital en euros) | 20 |
| Saldo de las cuentas de la sociedad dominante, en millones (6) o en miles (4) | 10 |
| Entrada de sumario: la cifra es el número de página | 6 |
| Saldo del URD 2022 p.302, donde no se localiza la declaración de unidades | 3 |

Las 114 son los saldos que describe el autor. Lo demás, en U2.

- **En las 114 líneas de saldos no hay conflicto entre la fecha de la fila y la columna** [D]. Con el código de C14, anterior a la regla, 561 de sus 575 cifras quedaban sin columna de ejercicio; las otras 14 son del estado de cambios en el patrimonio, donde la «columna» era el año del título (S1). En los planes de acciones sí lo hay, y es de esperar: la columna es el año de concesión.
- **La línea en minúscula que continúa la fila anterior.** La condición corta la unión en 272 líneas. Solo en tres tenía efecto, las tres del URD 2022 p.350 (T4b y sus dos filas «of which»). Sin objeción.
- **La pestaña del margen derecho.** No hay ninguna fila de saldo con la pestaña a la derecha: los doce últimos tokens de un solo dígito que toman el ejercicio son recuentos de planes (`clases_9.txt`, I).

### 4.5 T3: la unión de las líneas que terminan en el día o en el año

- Con `fecha`, la unión cambia en 497 líneas: en 225 une más líneas y en 272 une menos (la regla de la minúscula). **La regla solo se dispara en siete de ellas**, las que el autor lista: cinco cierres del estado de cambios en el patrimonio y dos valores netos contables reexpresados del URD 2023 (`clases_9.txt`, D).
- En las otras 218 que unen más, lo que se une no es parte del rótulo de la fila («Critère 1» sobre «Critère 2», «l'exercice 2024» sobre «(en euros)», el título de un apartado sobre su texto). **No tiene efecto**: sin la fórmula del saldo y la fecha, o con otra palabra, la regla no se dispara.
- Las 16 líneas que toman la fecha de una línea de encima son las del autor. He leído la línea que queda por encima de lo unido en las 16: ocho veces es la cabecera de la tabla y ocho, una fila de datos que no es un rótulo partido («INCOME (LOSS)», «RÉSULTAT GLOBAL» y, en dos, «Accumulated amortization and impairment restated*»). En las 16 el rótulo unido es el de su propio saldo [P].
- Los saldos de apertura y de cierre de los diez estados quedan reconocidos: 21 líneas de doce columnas (el URD 2021 p.231 tiene dos aperturas, la publicada y la ajustada).

### 4.6 La regla de `f12f8ea`: el año y el día del rótulo

`token_del_rotulo` da un motivo en 2.722 tokens: 2.711 años y 11 días (`clases_9.txt`, E; `consultas_9.txt`, Q2).

| Qué es el token | Tokens | Candidatas OK en C16 que retira |
|---|---|---|
| Año de una fecha del rótulo | 1.156 | 66 |
| Año del pie de página (páginas pares) | 936 | 11 |
| Año al final de un rótulo sin fecha («WACC 2024», «Elis in 2022») | 587 | 1 |
| Año en medio del rótulo | 32 | 0 |
| «Día» | 11 | 2 |

- **Los años son años** [P]. En los 587 que van al final de un rótulo sin fecha he mirado la palabra que los precede («in», «year», «l'exercice», «since», «until», «WACC», «Refinancement»…): ninguno es una cifra pegada al rótulo. En estas publicaciones un importe de dos mil y pico lleva separador de miles. Nueve de los 2.711 no están en el rótulo sino en otra celda, mal localizados; también son años.
- **De los once «días», dos lo son.** Los otros nueve son ocho ceros reales y una pestaña del capítulo: U1.
- **Ninguna fila real** tiene su cifra dentro de la celda del rótulo: 0 de 713 (`consultas_9.txt`, Q5).
- **Lo que la regla no alcanza**, y sigue igual que en C16 (U5 c): dentro de la celda del rótulo quedan 2.346 tokens que la regla no retira, y 58 candidatas de esos tokens, que no son cifras, quedan OK en las seis dimensiones.

### 4.7 T4, T5 y T6

**T4.** `cabecera_de_paises` cambia en 22 tokens de 4 líneas (`clases_9.txt`, F): las dos filas del DEU 2024 p.315 (18 tokens, la corrección) y dos líneas de organigrama fuera de las páginas del grupo (DEU 2024 p.391 y URD 2025 p.449: «HOLDINGS Ltd · 100% · 100% · ELIS BELGIUM»), que ahora reciben una cabecera de países. Su perímetro ya era PENDIENTE por la cabecera de la página. La regla que salta «la primera línea del rótulo» salta también un título de verdad cuando está justo encima de una fila de datos con su misma sangría (H11) [H]: no hay ningún caso real con cambio de estado.

**T5.** `rotulos_sin_rotulo` devuelve algún rótulo en 266 líneas con cifras (16 en páginas del grupo), frente a 2.015 (327) en C16: los números del autor. Contando también las líneas sin cifras, 422 frente a 3.625 (`clases_9.txt`, G).
- Causa del cambio en las 3.390 líneas: la línea empieza por un dígito suelto (1.015), el rótulo lleva viñeta (881), o la línea contigua es larga, está sangrada o las dos cosas (1.494).
- **Qué se deja de detectar:** en 48 líneas C16 daba un rótulo contiguo que nombra un país, un segmento o una jurisdicción y C18 no. He leído las 48: leyendas de organigramas, direcciones, prosa, pestañas y siete rótulos con viñeta, todos sin cifras. El perímetro del grupo solo cambia en las tres líneas de la pestaña junto a un párrafo (9 candidatas, de FALLO a OK), y el de un segmento, en una («ELIS COLOMBIA», T6b). Ninguna fila de un segmento deja de fallar como del grupo.
- Las 16 líneas con cifras de páginas del grupo que conservan rótulos contiguos: el caso de Escandinavia (URD 2023 p.261), la fila «2023 (approximation)» del DEU 2024 p.315 y años, títulos y entradas de sumario. Ninguna asociación da un país o un segmento equivocado.
- Lo que la revisión n.º 7 decía de las líneas sin rótulo sobre C18 no lo he podido volver a ejecutar (§1). Mi barrido da lo mismo que declara el autor: 9 candidatas de FALLO a OK en perímetro y ninguna fila a OK.
- El criterio de la pestaña: U4.

**T6.** Encabezados numerados (`clases_9.txt`, H):

| | Páginas del grupo | Las demás |
|---|---|---|
| C16 | 409 | 982 |
| C18 sin la línea de debajo | 407 | 976 |
| C18 con la línea de debajo, como la llama el verificador | 407 | 980 |

- Dejan de serlo nueve líneas, las nueve prosa («Note 7.2 to the…», «6.2 of the 2022 Universal Registration Document, available»). Pasan a serlo cinco, las cinco títulos en mayúsculas.
- **Efecto:** la zona de cabecera cambia en una línea de prosa, sin que cambie ninguna candidata, y el título de país de encima no cambia en ninguna. Todas las transiciones de §4.2 se explican sin T6, como dice el autor.

### 4.8 Los scripts de las revisiones n.º 6 a 8 sobre C18

Vueltos a ejecutar con los scripts de la rama de revisión, no con la copia del autor (que es idéntica). Versión anterior, el worktree de C17 (`comparacion_6_8.txt`):

| Scripts | Resultado |
|---|---|
| Revisión n.º 6: los seis | Idénticos a los guardados |
| Revisión n.º 7: `contraejemplos_7` y `sondas_umbral_7` | Idénticos |
| Revisión n.º 7: `reproduccion_7` | Dos líneas distintas, las del manifiesto: 324 de 324 sobre el congelado y 322 de 322 en la guardada (T8 e, declarado) |
| Revisión n.º 7: `barrido_7`, `clases_7` y `lectura_filas_c14` | **No ejecutados**: necesitan PyMuPDF |
| Revisión n.º 8: `consultas_8`, `contraejemplos_8`, `lectura_saldos_8` y `sondas_8` | Idénticos |
| Revisión n.º 8: `barrido_8` | Una línea distinta, la del tiempo |
| Revisión n.º 8: `clases_8` | Distinta solo en la sección K: aquí sale sin la tipografía |
| Revisión n.º 8: `reproduccion_8` | Distinta en el recuento del manifiesto (324 y 322) y en los segundos de cada paso |

Lo que la octava parte dice de esas salidas es exacto en lo que he comprobado en ellas:
- `contraejemplos_6`: los 48 casos, con el mismo estado y el mismo motivo en C16 y en C18;
- `contraejemplos_7`: de 40 casos, 7 cambian de estado (A1, A3, A5–A7, A10 y A12, de OK a PENDIENTE);
- `contraejemplos_8`: los 25 casos, como se describe en T1–T5;
- `barrido_6`, `barrido_8` y las clases: las transiciones de §4.2;
- `sondas_umbral_7`: 246 de 246; `sondas_8`, igual que sobre C16.

---

## 5. Los límites declarados de C18 y su coste (alcance 3)

### (a) T2 · los recuentos con fecha vuelven a la regla de las columnas (coste)

**El coste se sostiene; su descripción no es exacta.**
- **Qué cuesta** [D]: nada en aceptaciones. Las filas de recuento no pueden quedar OK: la unidad falla o queda pendiente. Cambia el diagnóstico de la dimensión del ejercicio: en 42 candidatas pasa de OK a FALLO y en 3 de FALLO a OK. De ellas, 40 y 2 están en once filas de planes, por la columna del año de concesión del plan; las otras 2 y 1, en dos filas «Number of shares as at…» del URD 2021 p.291, por la columna de su tabla.
- **Qué no es exacto** [P][D]: no todos los recuentos vuelven a la regla de las columnas. De las líneas de recuentos de acciones, derechos y beneficiarios con fecha y cifras a la derecha, 31 la pierden y 24 la conservan, más las 20 de la tabla del capital social (`consultas_9.txt`, Q6). La misma fila toma una regla u otra según por dónde parta `pdftotext` su rótulo: U2.

### (b) T2 · una fila con solo la fórmula del saldo bajo una línea de fecha de la fila anterior (límite)

**Se sostiene.** No hay ningún caso en las cinco publicaciones: las 16 líneas que toman la fecha de arriba son rótulos de su propio saldo (§4.5).
- **Qué costaría** [H] (`sondas_sinteticas_9.txt`, H5 y H14): la fila tomaría el ejercicio de la fecha de la fila anterior. En una tabla de varias columnas no se acredita nada: con ese ejercicio la columna queda PENDIENTE, y declarada con el ejercicio de su columna, falla. En una tabla de una sola columna quedaría aceptada con el ejercicio de la otra fila. Ya era así en C16.
- El límite es más ancho de lo que dice T14: U5 d.

### (c) T5 · el margen izquierdo en lugar de la sangría de los rótulos (límite)

**Se sostiene.** No cuesta ninguna detección en las páginas del grupo (§4.7). El umbral de 12 caracteres deja fuera las líneas de rótulo de una tabla que no empiece en el margen: en estas publicaciones son leyendas de organigramas y prosa a dos columnas.

### (d) T6 · los títulos en minúsculas partidos tras una coma y las entradas de sumario (límites)

**Se sostienen.** Ningún estado depende de ellos (§4.7). No he vuelto a contar las doce entradas de sumario ni los cuatro títulos: su recuento es de la revisión n.º 8, con tipografía.

### (e) T1 · con varias columnas de datos, la columna queda PENDIENTE (límite)

**Se sostiene.** Es la opción que la revisión n.º 8 proponía. Cuesta las 331 aceptaciones legítimas de C16 (§4.3).

---

## 6. El test (alcance 4)

`test_verificar_cifras.py` gana 19 casos (2 positivos, 11 PENDIENTE y 6 FALLO), cambia dos de OK a PENDIENTE (A1 y A10) y añade nueve comprobaciones directas. 23 + 36 + 77 = 136.

- **Los casos nuevos distinguen las versiones.** Con el verificador de C16 fallan 17 casos y 5 comprobaciones; con el de `d3c0f1b`, 2 y 1. Cada regla nueva tiene al menos un caso que solo pasa con ella.
- **Prueban lo que dicen**, con estas precisiones:
  - **T2c** («2023)» de una línea de prosa): queda PENDIENTE, como dice. No lo retira la regla del año del rótulo, cuya expresión no admite el paréntesis: lo retiene la regla de las columnas, que no encuentra columna (U5 c).
  - **La excepción «Total» de S4** se prueba sobre `cabecera_de_paises`, no sobre el perímetro. La frase de la octava parte («la columna bajo «Total» no deja el perímetro PENDIENTE y la de Francia, sí») es más ancha que la comprobación. La he hecho con `comprobar_perimetro` sobre las mismas dos líneas, en una página del grupo: OK bajo «Total» y PENDIENTE bajo «France» (H12). La frase es cierta.
  - **El caso de una sola columna** (deterioro de clientes) es de una tabla de una sola columna. No hay ningún caso de una fila con una sola cifra en una tabla de varias (U3).
  - **«Sin detalle»** (T4b): exige que el motivo del ejercicio no diga «rótulo». Prueba que la fila no toma la fecha de arriba.
- **Lo que el test no cubre** [I]: una cifra cuyo texto aparece antes en la línea (U1); un recuento con el rótulo partido antes de «as at» (U2); una fila de cifras que empieza por un dígito suelto (U4).

---

## 7. Objeciones nuevas

Todas las filas citadas existen en el PDF [P]. Ninguna afecta a una fila real del CSV: la salida de las 752 es idéntica en C16 y en C18.

### U1 · menor · `verificar_cifras.py`, posición de los tokens y regla de `f12f8ea` · la regla del «día de la fecha» retira cifras reales, y la posición de un token no es la suya cuando su texto aparece antes en la línea

- **Qué ocurre** [P][D]. `spans_numericos` localiza cada token con `linea.find(token, desde)`: la primera aparición de su texto a partir del final del token anterior. Si ese texto está antes dentro de otra celda, la posición es la de esa celda.
  - En «as at 12/31/2025 · 0 · 92,485 · 0 · 35,701 …» (URD 2025 p.360), el primer «0» de la fila se localiza en el «0» de «2025».
  - `token_del_rotulo` ve entonces un entero de 0 a 31 dentro de un rótulo con fecha y lo da por «el día de la fecha del rótulo de la fila, no una cifra».
- **Prueba.** `spans_9.txt`; `contraejemplos_9.txt`, U1 y U2; `consultas_9.txt`, Q2; `lectura_posiciones_9.txt` (pdfminer); `sondas_sinteticas_9.txt`, H3 y H4.

  | Cifra [P] | Declaración | C16 | C18 |
  |---|---|---|---|
  | URD 2025 p.360 · «Number of rights lapsed or forfeited / as at 12/31/2025», primera cifra (0) | 2025 | ejercicio OK por la fecha | ejercicio PENDIENTE: «el día de la fecha» |
  | la misma | 2024 | **FALLO** de ejercicio | PENDIENTE |
  | DEU 2024 p.306 · «Nombre de droits devenus caducs / au 31/12/2024», primera cifra (0) | 2023 | **FALLO** de ejercicio | PENDIENTE |
  | la misma, con un identificador de saldo | 2024 | ejercicio OK | ejercicio PENDIENTE |
  | URD 2021 p.176 · «Number of fatal accidents · 0(a) · 0 · 0» bajo «Group 2021 · Group 2020 · Group 2019»: el «0» de 2020 | 2021 | **ejercicio OK** | **ejercicio OK** |
  | el mismo | 2020 | FALLO de ejercicio | FALLO de ejercicio |

- **Cuánto** [D].
  - **La regla nueva:** 18 tokens que da por año o día del rótulo no están en el rótulo. Ocho son ceros reales de filas de planes de acciones (DEU 2024 p.306 y p.361; URD 2025 p.360 y p.417), uno es la pestaña del capítulo y nueve son años de otra celda. Los ocho ceros reciben un motivo falso; declarados con otro ejercicio, pasan de FALLO a PENDIENTE; en el modo de saldo pierden el ejercicio OK.
  - **La causa, anterior a C18:** 385 tokens de 299 líneas tienen una posición que no es la suya (129 en páginas del grupo): 117 marcadores «-» y 268 cifras, 223 de ellas enteros sin separador. 143 caen dentro del rótulo, 176 en otra celda de texto y 66 dentro de un token anterior.
  - **La columna:** con la posición verdadera, cuatro candidatas dejan de tener el ejercicio OK en C18 (once en C16). Son la fila «Number of fatal accidents» de los URD 2021, 2022 y 2023: la celda con llamada («0(a)») no es un token, y el «0» siguiente se localiza dentro de ella, bajo la columna de al lado.
  - **Las filas reales:** ninguna de las 713 tiene su token mal localizado ni está en una línea afectada. Ninguna candidata OK deja de serlo, ni al revés, salvo un año de una línea de prosa.
- **Por qué importa.**
  - C18 añade tres usos de esa posición: `token_del_rotulo`, la condición «a la derecha del rótulo» de la regla de la fecha y `columnas_de_datos`. En una fila de dos columnas cuya primera cifra esté en la fecha del rótulo, la fila cuenta una sola columna y la segunda cifra queda OK sin que se compruebe su columna (H3) [H].
  - Con cifras distintas, el desplazamiento puede aceptar una cifra de otro ejercicio en las cuatro dimensiones que he evaluado: en «Impact of a 0.5 point decrease · 0.5 · 5» bajo «2022 · 2021», el «5» de 2021 se localiza dentro de «0.5» y pasa como de 2022; declarado 2021, falla (H4) [H]. No he encontrado ese caso en las cinco publicaciones.
  - T14 pasa estas reglas al frente técnico. En tablas de enteros (recuentos, miles sin decimales) la coincidencia es fácil; en las de Elis en millones, con un decimal, no la he visto.
- **Atenuantes.** Ninguna fila real. PENDIENTE no acredita. Los ocho ceros son recuentos, que no pueden quedar OK.
- **Causa** [D]. La posición se busca por texto después de haber partido la línea en celdas. La tokenización ya sabe en qué celda y en qué palabra está cada token.
- **Corrección propuesta.** Que la tokenización devuelva la posición de cada token, sin buscarla después. `spans_9.py` lo hace con la misma regla, da los mismos tokens en las 22.594 líneas y deja las 713 filas reales como están. Añadir al test U1a (ejercicio OK por la fecha, sin el motivo del día) y U2a (FALLO de ejercicio).

### U2 · menor · `verificar_cifras.py`, ejercicio (T2, resto) · la regla sigue disparándose en filas que no son saldos, y el rótulo más corto la devolvió a los recuentos de los planes

- **Qué ocurre** [P][D]. `rotulo_de_saldo` toma el rótulo más corto, de abajo arriba, que lleva la fórmula y la fecha. Cuando un rótulo se parte antes de «as at», la última línea ya los lleva, y la primera, que dice de qué es la fila, no se mira.
  - «Number of rights outstanding» / «as at 12/31/2022 · - · 548,801 …» (URD 2022 p.294): la regla ve «as at 12/31/2022» y da el ejercicio.
  - «Number of rights outstanding as at 12/31/2021 · …» (URD 2021 p.261), en una sola línea: no es la fórmula de un saldo, y decide la columna.
  - «6.1.5 Consolidated statement of changes in equity» / «as at December 31, 2021 · 228» (URD 2021 p.225, sumario): la regla da el ejercicio al número de página.
- **Prueba.** `clases_9.txt`, B; `consultas_9.txt`, Q6; `contraejemplos_9.txt`, U3a–U3d; `intermedias_9.txt`.
  - **24 filas de recuentos de planes** con cifras toman la regla (y una más sin cifras limpias): DEU 2024 p.306 y p.361; URD 2021 p.261 y p.312; URD 2022 p.294; URD 2023 p.312 y p.369; URD 2025 p.360 y p.417.
  - **20 filas de la tabla del capital social**, rotuladas solo «As at 12/31/2021»: número de acciones, nominal y capital en euros.
  - **6 entradas de sumario** (URD 2021 p.225, URD 2022 p.257 y URD 2023 p.275). La revisión n.º 8 las citaba (T2 a); siguen igual que en C16.
  - **El segundo commit.** De `d3c0f1b` a `485de8d` la regla vuelve a 33 líneas: los siete saldos que dice la octava parte, el saldo «published» y **25 filas de recuentos de planes** que `d3c0f1b` dejaba fuera.
- **Qué consecuencias tiene** [D].
  - **Ninguna aceptación.** En los planes, la unidad queda PENDIENTE y la columna también; en el capital social, la unidad falla o queda pendiente y la página no es del grupo; en el sumario, la página no declara unidades ni lleva pie.
  - **El diagnóstico depende de la partición.** La misma fila toma el ejercicio de su fecha en una página y el del año de concesión del plan en otra (U3b y U3c).
  - **La unidad pierde su señal.** En «as at 12/31/2022 · 402 · 457 · 20 …», que es «Number of working beneficiaries», la línea no dice «Number of»: la unidad queda PENDIENTE solo porque la página no declara ninguna (U3d).
  - Los ocho ceros de U1 están en estas filas.
- **Por qué importa.** La octava parte, el informe §1, T14, `ESTADO.md` y el punto de recuperación dicen que la regla «solo vale en filas de saldo» y que los recuentos con fecha «no toman el ejercicio de la fecha» y «vuelven a la regla de las columnas». Es cierto para 31 líneas y no para 44. El ejemplo que da la octava parte, «Number of rights outstanding as at 12/31/2022», sí la toma en el URD 2022 p.294.
- **Atenuante.** Para estos recuentos, el ejercicio de la fecha es el correcto: lo decía el propio autor en C16.
- **Corrección propuesta.** Elegir una de las dos y decirla:
  - o los recuentos con fecha toman el ejercicio de su fecha, y se declara así;
  - o no lo toman, y entonces la línea de encima cuenta para la condición de las palabras cuando es la primera línea del rótulo de la fila: está justo debajo de una fila de datos, y una cabecera de columna («Cash flow hedges») o una línea de unidades no lo están. Y la regla no se aplica si la línea de encima es un encabezado numerado (el sumario).
  En los dos casos, ajustar las frases y añadir U3b y U3a al test.

### U3 · forma · `verificar_cifras.py`, columna (T1, límite no declarado) · «una sola columna de datos» se mide en los tokens de la fila, no en las columnas de la tabla

- **Qué ocurre** [D]. `columnas_de_datos` cuenta los tokens numéricos a la derecha del rótulo. No cuenta una celda vacía ni una celda con llamada («12.0(a)» no es un token), y un token mal localizado dentro del rótulo tampoco (U1).
- **Prueba.** `sondas_sinteticas_9.txt`, H1–H3 [H]: en una tabla de tres columnas, una fila de saldo con una sola cifra limpia queda OK en las cuatro dimensiones evaluadas, con «columna» en NO_APLICA, esté la cifra bajo «Total» (H1, las otras dos celdas llevan llamada) o bajo «Vehicles» (H2, las otras dos están vacías). En una tabla de dos columnas ocurre lo mismo si la primera cifra se localiza dentro de la fecha del rótulo (H3).
- **En los PDF** [P]: ningún caso. Las 26 líneas con la regla y una sola columna de datos están en tablas de una sola columna (§4.3). En las filas de planes del URD 2025 p.360 la cuenta es menor que la real (cuatro de ocho), pero sigue siendo mayor que uno.
- **Corrección propuesta.** Contar las columnas en la tabla: el máximo de las filas del bloque, con las celdas con llamada, o las celdas de la cabecera. O declarar el límite en el informe y en T14.

### U4 · forma · `verificar_cifras.py`, perímetro (T5) · el criterio de la pestaña es más ancho que el de `rotulo`

- **Qué ocurre** [D]. `rotulos_sin_rotulo` devuelve la lista vacía si la primera celda es un dígito suelto. `rotulo` (S3) solo toma el dígito por pestaña si le sigue una celda de texto. Una fila de cifras sin rótulo cuya primera cifra tiene un solo dígito queda sin rótulo contiguo.
- **Prueba.** `clases_9.txt`, G; `sondas_sinteticas_9.txt`, H9 y H10.
  - **34 líneas reales** [P] están hechas solo de cifras y empiezan por un dígito suelto («0 · 0», «0 · 3 · (a)», «1 · 2 · 3», «5 · 10»): recuentos, escalas de gráficos, numeraciones y alguna pestaña seguida de una cifra. Dos están en páginas del grupo, en tablas de planes de acciones. En C16, 24 recibían un rótulo contiguo; ninguno nombra un segmento, un país ni una jurisdicción. Otras 57 son la pestaña o una numeración seguidas de texto que empieza por un número (una dirección, un título).
  - **Sintética** [H]: «Scandinavia and Eastern» / «5 · 3» / «Europe», declarada del grupo: FALLO de perímetro en C16 y OK en C18. Con «15 · 13», FALLO en las dos.
- **Por qué importa** [I]. Poco: en una tabla en millones con un decimal no hay cifras de un solo dígito. Es la clase de S2 para tablas de enteros.
- **Además.** La cabecera del verificador dice «no para una línea que solo lleva la pestaña del capítulo»; el código lo aplica a toda línea que empieza por un dígito suelto.
- **Corrección propuesta.** El mismo criterio que `rotulo`: dígito suelto seguido de una celda de texto, o línea que solo lleva el dígito.

### U5 · forma · `verificar_cifras.py` · restos de las reglas de C18

- (a) **«published» en el rótulo.** La regla admite «published», «publié» y «reported» y da el ejercicio. Nada mira que la fila sea la cifra anterior a la reexpresión: la regla de la edición de Q1 solo lee la cabecera de la columna. Caso real [P]: «As at December 31, 2019, published» (URD 2021 p.257); falla en edición por otra razón, porque 2019 queda fuera de las publicaciones, y tiene tres columnas (U3e). En una tabla de una sola columna y con el ejercicio anterior al de la publicación, nada impediría declararla vigente: la sonda H8 da OK en las cuatro dimensiones evaluadas y `edicion_de_columna` no devuelve nada [H].
- (b) **T4.** La línea de una sola celda justo encima de una fila de datos se salta siempre, sea la primera línea del rótulo o un título. En H11 [H], una fila de una tabla del grupo que sigue a una tabla por países pasa de perímetro OK a PENDIENTE: el lado prudente. Efecto real: las dos líneas de organigrama de §4.7, sin cambio de estado.
- (c) **Lo que la regla del año no alcanza** (`consultas_9.txt`, Q3 y Q4; `contraejemplos_9.txt`, U4). Ya era así en C16:
  - 60 años con paréntesis dentro del rótulo («2023)», «(2023)»): no casan con la expresión; ninguno queda OK;
  - **55 folios del pie de las páginas impares** («Elis | Universal Registration Document 2022 | 259»): OK en las seis dimensiones como 259,0 millones de 2021. La regla retira el año del pie de las páginas pares y no el folio de las impares;
  - tres «1» de «As at January 1» sobre las columnas de la tabla: OK en las seis dimensiones. La regla del día exige la fecha completa;
  - 58 años sueltos de líneas de cabecera, fuera de un rótulo de texto: siguen OK. La frase del autor se limita, con razón, al «rótulo de texto de la fila».
- (d) **El límite de T2 es más ancho que «Balance» o «Solde».** Lo toma cualquier rótulo hecho solo de las palabras que la regla admite: «Restated», «Net», «Published» (H6) [H].
- **Corrección propuesta.** (a) Con «published», «publié» o «reported» en el rótulo, la edición no puede ser la vigente. (c) Tratar el pie de página como lo que es, y no evaluar como cifra un token de una celda con letras. (b) y (d), declararlos.

### U6 · forma · respuestas (octava parte), informe §1, E9, T14, `ESTADO.md` y punto de recuperación · frases más fuertes que su prueba o recuentos inexactos

- (a) **E9 y octava parte, T7 c:** «en R42 de esos años no interviene ninguna» y «ya no cita […] R42 de 2023–25». La fuente que cita, `sondas_8.py`, sección 3, lista para 2023–25 «R42 (5)»: las ventas de 2023, 2024 y 2025, que mueven la referencia, intervienen en R42 de esos años (`resultados/contraste_f1.json`: `IS_VENTAS_2025` tiene «R42 2025» entre sus identidades entre páginas). Son 18 identidades, no 17. La lista de 2021–22 es exacta. La conclusión no cambia: las 97 tienen identidad entre páginas.
- (b) **Octava parte (T2), informe §1, T14, `ESTADO.md` y punto de recuperación:** los recuentos con fecha «no toman el ejercicio de la fecha» y «vuelven a la regla de las columnas»; la regla «solo vale en filas de saldo» (U2).
- (c) **Octava parte, T2, «un efecto de la primera versión»:** dice que el rótulo más corto devuelve siete saldos. Devuelve la regla a 33 líneas (U2).
- (d) **Octava parte, T2, «otro efecto»:** los cuatro años quedaban OK «alineados con la columna del ejercicio anterior». Tres sí; el «2021» del URD 2022 p.323 pasaba como cifra de 2022 (`intermedias_9.txt`, 2).
- (e) **Informe §1:**
  - «ni la fila que está bajo la línea que continúa el rótulo de la anterior», sin la condición de que esa línea empiece en minúscula;
  - «ni los títulos con fecha»: las entradas de sumario la toman (U2);
  - la lista «Límites que quedan» no recoge los límites que C18 declara en T2, T5 y T6. Están en las respuestas, en T14 y en el punto de recuperación.
- (f) **T14:** el límite de T2, «solo «Balance» o «Solde»» (U5 d).
- (g) **Punto de recuperación §1 y octava parte:** «las seis tablas del WACC por país». Son cinco, una por publicación; seis son sus líneas de cabecera, porque la del DEU 2024 va en dos.
- **Corrección propuesta.** Ajustar cada frase a lo que su prueba cubre.

---

## 8. Coherencia entre documentos (alcance 5)

He leído la octava parte de las respuestas y las precisiones de C18 en la sexta y la séptima, el informe (§0, §1, §12 y §13), la especificación (E9, T12 y T14), el README, `ESTADO.md`, `REGISTRO_CONFIGURACION.md`, `PUNTO_DE_RECUPERACION.md` y la cabecera del verificador.

- **Recuentos.** Coinciden entre sí y con las salidas: 752 = 713 + 39; 738, 14 y 0; 136 = 23 + 36 + 77, y los 36 PENDIENTE que desglosa el informe §0.1 suman (1 + 1 + 2 + 6 + 11 + 4 + 11); 9 comprobaciones directas; 292 = 136 + 127 + 29; 24; 530; 713/713; 207 = 191 + 16; 200, 7 y 500 (302 + 198; 166 + 32); 346, 341 y 5; 411; 331 y 10; 336, 101 y 35; 414, 101 y 588; 78 + 5 = 83; 541; 54 candidatas y 18 tokens; 266 (16) y 2.015 (327); 409, 407, 982 y 976; 2.310, 770 y 54.
- **Hashes y alcance.** C18 y C19, bien registrados. El congelado solo añade el hash. El alcance del punto de recuperación, `git diff 63e6090 C18`, es el del encargo.
- **Estado y registro.** Describen bien la pasada 8 y C18, y dejan esta pasada pendiente. No puedo comprobar lo que el registro dice de los metadatos de la sesión autora.
- **Reproducción (§13).** Los comandos funcionan tal como están escritos.
- **Afirmaciones comprobadas y ciertas:**
  - «las 752 filas reales no cambian» y «la salida, el registro y las páginas exportadas son idénticos byte a byte»;
  - «C18 no crea ninguna aceptación»: ninguna candidata pasa a OK en ningún modo;
  - «de las 346 aceptaciones de C16 quedan diez» y «con una sola columna de datos»: las diez tablas tienen una sola columna;
  - «ninguna es un saldo en millones de euros», de las 500 líneas que salen;
  - «en las 16 el rótulo unido es el de su propio saldo»;
  - «los 20 saldos de apertura y de cierre […] quedan reconocidos»;
  - lo que se dice de `d3c0f1b`: los siete saldos que dejaba de reconocer y las cuatro aceptaciones del año del rótulo, que ya tenía C14 (`intermedias_9.txt`);
  - «18 candidatas dejan de ser OK, todas años de un rótulo», en los demás modos;
  - «ninguno cambia un estado», de los límites de T6.
- **Afirmaciones más fuertes que su prueba:** las de U6.
- **T14.** Recoge las reglas nuevas con sus casos y los límites de T2 y T6. Le faltan el límite de U3 y lo que dice U2.

---

## 9. Conclusiones materiales y lo no comprobado

**Conclusiones materiales.** Ninguna cambia: la conciliación y el FCF base, C48 = 108, el doble cómputo del arrendamiento bajo su premisa, los intangibles adquiridos pendientes de política, la reinversión necesaria no publicada como importe y `pendiente_de_datos`. Las decisiones económicas siguen pendientes de la persona responsable.

**Sobre el verificador** [I]. C18 corrige bien lo que se le señaló y es más prudente que C16: no crea ninguna aceptación y retira casi todas las que la regla de la fecha había abierto. Los recuentos del autor son exactos; he encontrado frases inexactas, no números. Lo que queda es de dos clases. Una es la de siempre, reglas sobre el texto del rótulo que dependen de por dónde parte la línea `pdftotext` (U2, U4, U5). La otra es más antigua que esta pasada y no la había señalado ninguna revisión: la posición de un token se busca por su texto y a veces no es la suya (U1). No toca ninguna fila real, pero de ella dependen la columna de cada cifra y tres reglas nuevas, y es la primera vez que una regla la usa para decir que algo no es una cifra. Lo que sostiene las cifras reales sigue siendo la segunda línea: las identidades entre páginas y la Historia.

**No comprobado en esta pasada:**
- `barrido_7.py`, `clases_7.py` y `lectura_filas_c14.py` sobre C18, y la tipografía de la sección K de `clases_8.py`: sin PyMuPDF.
- La prueba de caja no nula con LibreOffice: no cambia desde C4 y no la he repetido.
- Los scripts de las revisiones n.º 1 a 5 sobre C18: solo he comparado las salidas guardadas.
- Lo que no cambia entre C17 y C19, salvo lo que hizo falta para reproducir. Los §2 a §11 del informe y el resto de la especificación.
- Las doce entradas de sumario y los cuatro títulos en minúsculas de los límites de T6: recuento de la revisión n.º 8.
- Lo que `REGISTRO_CONFIGURACION.md` dice de los metadatos de las sesiones.
- Las candidatas del barrido una a una. He leído las líneas que digo en §1.
- Con el perímetro de un segmento solo he evaluado la dimensión de perímetro.
- En las sondas sintéticas, el literal y la edición no se evalúan.
- Si las filas reales dependen de la posición de otro modo que el medido: he comprobado que ninguna tiene su token mal localizado ni comparte línea con uno que lo esté.
- Clases de error que mis filtros no señalan. Un error de extracción común a `pdftotext` y a mis lecturas.
- Las reglas V-F1a a V-F1h y T8 y T14: especificadas, no implementadas.
- El árbol del hito 4.15 y la rama del frente técnico.

---

## 10. Reproducción de esta revisión

Hacen falta pdfplumber, para `lectura_posiciones_9.py` y los scripts de la revisión n.º 6, y pypdfium2, para los de las revisiones n.º 6 y 8. Versiones usadas: Python 3.13, poppler 24.02 (`pdftotext`, `pdftoppm`), pdfplumber 0.11.10 (pdfminer 20260107) y pypdfium2.

```bash
B=docs/validacion_economica_paralela/frente_E_F1_elis
C17=<worktree de 863ddde>/$B ; C19=<worktree de 06ad100>/$B
RAIZ=<ruta>/munger_v2_r1 ; W=<carpeta de trabajo> ; REV=<esta rama>/$B/revision
git show d3c0f1b:$B/scripts/verificar_cifras.py > $W/v_d3c0f1b.py
git show 485de8d:$B/scripts/verificar_cifras.py > $W/v_485de8d.py
git show c96d544:$B/scripts/verificar_cifras.py > $W/v_C14.py
cd $REV/scripts_revisor_9
python3 -I -B reproduccion_9.py --raiz "$RAIZ" --autor "$C19" --c16 "$C17" --d3c0f1b $W/v_d3c0f1b.py --trabajo "$W/repro9"
python3 -I -B barrido_9.py --raiz "$RAIZ" --c16 "$C17" --c18 "$C19" --todas "$W/todas9.jsonl.gz" --salida ../resultados_revisor_9/barrido_9.txt
python3 -I -B clases_9.py --todas "$W/todas9.jsonl.gz" --raiz "$RAIZ" --c16 "$C17" --c18 "$C19"
python3 -I -B consultas_9.py --todas "$W/todas9.jsonl.gz" --raiz "$RAIZ" --c18 "$C19"
python3 -I -B modos_9.py --todas "$W/todas9.jsonl.gz" --raiz "$RAIZ" --c16 "$C17" --c18 "$C19"
python3 -I -B spans_9.py --raiz "$RAIZ" --c16 "$C17" --c18 "$C19"
python3 -I -B intermedias_9.py --raiz "$RAIZ" --c18 "$C19" --version C14=$W/v_C14.py --version C16="$C17" --version d3c0f1b=$W/v_d3c0f1b.py --version 485de8d=$W/v_485de8d.py
python3 -I -B contraejemplos_9.py --raiz "$RAIZ" --version C16="$C17" --version C18="$C19"
python3 -I -B sondas_sinteticas_9.py --raiz "$RAIZ" --c16 "$C17" --c18 "$C19"
python3 -I -B lectura_posiciones_9.py --raiz "$RAIZ" --c18 "$C19"
./relanzar_revisores_6_8.sh "$RAIZ" "$C17" "$C19" "$REV" "$W/rev68"
```

Los scripts que no llevan `--salida` escriben por la salida estándar; cada uno se guardó en el archivo de su nombre. `reproduccion_9.py` deja su salida en la carpeta de trabajo. El barrido tarda unos 6 minutos con cuatro procesos; `spans_9.py`, unos 5; `modos_9.py`, unos 10; los scripts de las revisiones n.º 6 a 8, unos 30.

Salidas en `revision/resultados_revisor_9/`:

| Archivo | Contenido |
|---|---|
| `reproduccion_9.txt` | Manifiesto, CSV regenerado, cadena del §13 y sondas frente a las salidas del autor; el verificador de C16 sobre el mismo CSV; el test de C18 con los verificadores de C16 y de `d3c0f1b`; el contraste frente al de C17 y la referencia de E9; el barrido del autor |
| `barrido_9.txt` | 51.492 tokens de las 2.026 páginas: equivalencia con la ejecución oficial, controles y transiciones C16 → C18 de las 154.476 candidatas |
| `clases_9.txt` | Transiciones con su causa (A); la regla de la fecha en C18, su clasificación y las líneas de una sola columna (B); dónde da ejercicio la regla en cada versión y clasificación propia de las líneas con fecha (C); la unión con `fecha` (D); `token_del_rotulo` (E); `cabecera_de_paises` (F); `rotulos_sin_rotulo` (G); `es_encabezado_numerado` (H); comprobaciones puntuales (I) |
| `consultas_9.txt` | Transiciones por motivo de la regla nueva (Q1); los tokens con el motivo del día (Q2); tokens del rótulo que la regla no retira (Q3); años sueltos (Q4); filas reales con el token en el rótulo (Q5); recuentos con fecha con y sin la regla (Q6) |
| `modos_9.txt` | Los 2.722 tokens por los que pasa `token_del_rotulo` o un cambio de zona, en los demás modos de control |
| `spans_9.txt` | Tokens mal localizados en todas las páginas; filas reales afectadas; efecto en C16 y en C18 de sustituir la posición por la verdadera |
| `intermedias_9.txt` | La regla de la fecha en C14, C16, `d3c0f1b`, `485de8d` y C18, y el año de cuatro rótulos de saldo en cada versión |
| `contraejemplos_9.txt` | 19 casos sobre filas reales con el verificador oficial de C16 y de C18: U1 (el cero en la fecha), U2 (el desplazamiento de columna), U3 (la regla en filas que no son saldos), U4 (tokens del rótulo que no son cifras) y U5 (controles) |
| `sondas_sinteticas_9.txt` | 14 sondas sobre páginas inventadas, H1–H14 |
| `lectura_posiciones_9.txt` | Las filas de U1 leídas con pdfminer, con la coordenada de cada palabra |
| `comparacion_6_8.txt` | Las 16 salidas de los scripts de las revisiones n.º 6 a 8 sobre C18 frente a las guardadas; la copia del autor frente a la rama de revisión; las salidas guardadas de las revisiones n.º 1 a 5 sobre C16 frente a sobre C18 |

`arnes9.py` es el módulo común. Los bloques de `contraejemplos_9.py` se numeran U1 a U5 y no coinciden uno a uno con las objeciones: sus bloques U1 y U2 son la objeción U1, su bloque U3 son las objeciones U2 y U5 a, y su bloque U4, la U5 c. El barrido completo (un archivo comprimido) no se guarda en el repositorio: se regenera con los comandos de arriba. Tampoco se guardan las salidas de los scripts de las revisiones n.º 6 a 8 sobre este commit: son las que guarda el autor, con las diferencias de `comparacion_6_8.txt`.

Algunas comprobaciones están hechas con órdenes sueltas y no con estos scripts: las diferencias entre commits (`git diff`); la lectura de páginas con `pdftotext -layout`, entre ellas la de la cabecera de la tabla de las 26 líneas de una sola columna y la del URD 2022 p.275; la vista de dos páginas renderizadas con `pdftoppm` (URD 2025 p.360 y URD 2021 p.176); la tabla de estados de los casos de `contraejemplos_6`, `contraejemplos_7` y `contraejemplos_8` en las salidas guardadas; las citas de los documentos del autor (`grep`); la lista de las entradas que intervienen en R42 en `contraste_f1.json`; las 104 líneas con solo la fecha por rótulo y sin la regla; la palabra que precede a los 587 años de un rótulo sin fecha; lo que la regla de las columnas de C14 daba a las 575 cifras de las 114 líneas de saldos; los dos tokens cuyo perímetro depende de la posición (dos años de una línea de prosa del URD 2025 p.339); y el recuento de los marcadores (2.756 tokens; 270 líneas solo llevan marcadores), que cuadra el universo de `spans_9.py` con el del barrido; las 13 líneas de las 42 candidatas cuyo ejercicio pasa de OK a FALLO; y la búsqueda de rótulos con una fecha de cualquier mes (§4.4).
