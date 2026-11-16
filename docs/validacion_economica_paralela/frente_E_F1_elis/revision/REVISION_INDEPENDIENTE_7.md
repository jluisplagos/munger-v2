# Revisión independiente n.º 7 · frente E · F1 · Elis · lo afectado por C14

Fecha: 16-nov-2026. Material revisado: commit congelado `c96d544646b2fa5a66c233402a9f31332a643cec` (C15) de la rama `auditoria/economica-f1-frente-e`. C15 solo añade a C14 (`cf55865a22035aa8376d8813cd58d0f2fcdd4846`) el registro de su hash (comprobado: `git diff cf55865 c96d544` toca `ESTADO.md`, la línea de C14 en las respuestas y el manifiesto). Alcance: `git diff c11a6de cf55865`, es decir, la respuesta a R1–R8 (41 archivos). La incorporación de la revisión n.º 6 en `c11a6de` es una copia sin cambios de lo publicado en esta rama (comprobado: informe, scripts y salidas, iguales). Bases de comparación, cada una en su propio worktree: C13 (`1b80b5d…`), que es C12 (`4f3f9ba…`) más el registro de su hash; C11 (`364129a…`); y, para los scripts de la revisión n.º 5, C8 (`97441770…`). Donde digo «desde C12», la versión que he ejecutado es C13.

Se publica en la rama `auditoria/economica-f1-frente-e-revision`, sobre el commit 9711f04.

Marcas: **[P]** publicado (leído en el PDF) · **[D]** derivado · **[I]** interpretación · **[H]** hipótesis.

Este documento no contiene valoraciones, precios, recomendaciones de inversión ni declaraciones de aptitud. No adopta ninguna decisión pendiente. Se conservan C48 = 108 y E1/D3/E2/E6. No modifica el material del autor, el producto ni los libros.

---

## 0. Resultado en breve

1. **Las cifras que declara el autor se reproducen todas**, con salidas idénticas byte a byte (§2). También son idénticas a las que guarda el autor las 16 salidas de los scripts de los revisores n.º 1, 3, 4, 5 y 6 ejecutados sobre C14.
2. **Las dos filas nuevas de C14 son correctas** en página, línea, columna, ejercicio, unidad, perímetro y edición. Las he leído con MuPDF, con pdfminer y con PDFium, y a la vista en la página renderizada (§6).
   - R23 de 2021 y de 2022 cierra con residuo 0,0.
   - Los 246 intervalos de errores sin detección que declara el contraste son exactos: los he comprobado en sus dos extremos, como caja negra, con 984 ejecuciones del contraste.
   - «La clase es por pertenencia» está bien explicado. Quedan dos precisiones de redacción (S6 c y d).
3. **Estado de R1–R8 (§3):**
   - R1, R6 y R7: corregidas;
   - R2: corregida, con una observación sobre lo que la regla toma por encabezado (S5);
   - R3: corregida en sus casos, no en la clase (S1);
   - R4: corregida en sus casos; queda una clase de tabla (S4);
   - R5: corregida, salvo una fila (S3);
   - R8: corregida, con un resto de forma (S7 e).
4. **C14 no crea ninguna aceptación nueva.** En mi barrido, de 76.902 candidatas, ninguna pasa a OK. Las que pasan a FALLO o a PENDIENTE son correcciones o el efecto declarado de la regla de grupos (§4.2). No he encontrado ningún FALLO nuevo a una cifra legítima.
5. **Las tres decisiones en las que C14 no sigue la propuesta de la revisión n.º 6 se sostienen** (§5):
   - (a) no aplicar la cabecera ajena al asignar por orden: la propuesta habría dejado PENDIENTE 44 cifras legítimas y no habría retenido ninguna columna por entidad que la regla de grupos no retenga ya. El límite de la regla de grupos tiene un caso real: la tabla de las marcas con un solo ejercicio (URD 2021, 2022 y 2023), que la regla no ve;
   - (b) honorarios por firma auditora en PENDIENTE: es una elección conservadora y está declarada. Cuesta 176 cifras legítimas del grupo en cinco tablas, 16 de ellas OK en C13. Uno de sus dos argumentos no es de perímetro;
   - (c) umbral de 5,5 caracteres: separa mejor que 3. Con 3, 208 cifras con la fecha de otro ejercicio encima habrían bajado de FALLO a PENDIENTE.
6. **Objeciones nuevas: S1–S4 (menores) y S5–S7 (forma).** Ninguna afecta a las 752 filas reales.
   - **S1.** El año del título de la tabla cuenta como columna de ejercicio. En el estado de cambios en el patrimonio, el saldo de apertura declarado con su ejercicio queda en FALLO en las cinco publicaciones (en las cuatro en inglés, desde C12: es la clase de R3 y C14 no la alcanza). Declarado con el año del título, que no es el suyo, queda PENDIENTE o, en el DEU 2024, **OK en las seis dimensiones**.
   - **S2.** Una fila de segmento cuya cifra cae en una línea sin rótulo pasa como del grupo en las seis dimensiones (URD 2023 p.261: ventas y crecimientos de Escandinavia y Europa del Este).
   - **S3.** La fila «CGU France» del URD 2022 p.298 sigue OK: el número de capítulo del margen ocupa el lugar de su rótulo.
   - **S4.** La tabla con una columna por país y sin declaración de unidades (hipótesis del WACC por UGE) conserva el perímetro OK: entera en el URD 2025 y en el DEU 2024, y en sus dos últimas filas en los otros tres.
   - S2, S3 y S4 no los introduce C14. S2 y S3 están en líneas que los barridos de las pasadas 5 y 6 no recorrían: las que empiezan por un número.
7. **Ninguna conclusión material cambia.** No he encontrado ningún error en los datos reales.

---

## 1. Encargo, configuración y límites de la independencia

**Encargo.** Mensaje recibido al crearse esta sesión, entregado como aviso automático y no tecleado por una persona en ella. Lo trato como un encargo de revisión, no como una conclusión que confirmar: no doy por cierta ninguna descripción del autor sin comprobarla.

**Configuración.** Aquí no se escriben identificadores de modelo. Quien encarga puede leer la configuración de esta sesión en sus metadatos.

**Límites de la independencia:**
- **Quien encarga fija el alcance.** El encargo da los números de página de las filas nuevas, la lista de cosas que mirar y las tres decisiones que debo juzgar.
- **Leo la revisión n.º 6 entera y uso sus scripts** para comprobar las salidas que guarda el autor. Esta sesión es nueva y no conserva el contexto de ninguna pasada anterior, pero parto de sus informes, y eso me ancla en sus conclusiones y en su universo de casos.
- **La misma herramienta de extracción puede compartir errores con el autor.** Lo he reducido donde he podido:
  - las dos filas nuevas y sus contrapartes están leídas con tres motores que no son `pdftotext` y a la vista;
  - mi lectura propia del barrido usa MuPDF, un motor que ninguna pasada anterior había usado: posición, cuerpo y negrita de cada glifo, no la rejilla de caracteres;
  - las páginas de los contraejemplos de S1, S2 y S3 están vistas en la página renderizada;
  - las pruebas del verificador usan `pdftotext` por fuerza: es su entrada. Un error de extracción común a esas pruebas no se detectaría.
- **Mi lectura propia es un filtro, no una verdad.** Localiza el 99,3 % de los tokens de las páginas del grupo. «Cabecera inmediata» es un criterio mío y se equivoca en cabeceras que abarcan varias columnas. Por eso cada clase que llevo al informe está mirada en la página y pasada por el verificador oficial como proceso aparte (`contraejemplos_7.py`). No he mirado las 76.902 candidatas una a una.
- **Las variantes son mediciones, no propuestas.** Son el verificador de C14 con una sola pieza cambiada en memoria, para medir lo que aporta o cuesta cada decisión. No tocan el material del autor.
- El barrido llama a `comprobar_tabla`, la función que la ejecución oficial usa para cada fila. La equivalencia con la ejecución oficial está comprobada en las 713 y 711 filas de tabla reales de C14 y C13: ningún estado ni detalle distinto.

---

## 2. Reproducción (alcance 1)

Base 4.14 materializada desde el ZIP original de la Release (1.130.912.246 bytes, SHA-256 `bb51942c…b93e`) con `tools/base_414.py`, en un worktree de `main`: 6.798 de 6.798, `complete: true`. Libro `d2593777…92385`. Las cinco fuentes, con la huella de `fuentes.json`. Ejecución sobre una copia de la carpeta del worktree de C15. Prueba: `reproduccion_7.py` → `resultados_revisor_7/reproduccion_7.txt`.

| Cifra declarada | Resultado |
|---|---|
| Manifiesto | 236 de 236 |
| CSV regenerado desde los PDF | Idéntico (752 filas, SHA-256 `3f9ae6e6…1331`) |
| Verificador: 752 filas, 738 OK, 14 PENDIENTE, 0 FALLO | Reproducido. Código 2. JSON y registro idénticos. Las 73 páginas exportadas, idénticas |
| `test_verificar_cifras`: 108/108 | Reproducido. Registro idéntico. Composición: 21 OK, 21 PENDIENTE y 66 FALLO esperados |
| Contraste: 292 comprobaciones (136 del libro, 127 de fuente con 126 residuos, 29 algebraicas), 0 fallidas, 419 entradas | Reproducido. Código 0. JSON, tabla y registro idénticos |
| `test_contraste_residuos`: 24/24 | Reproducido. Registro idéntico |
| `cobertura_por_mutacion`: 530 filas, sin incoherencias | Reproducido. Salida idéntica: 386 por identidad, 2 solo libro, 23 sin detectar y 119 sin efecto (8 leídas y 111 no usadas) |
| Sondas: 713/713 en unidad y en perímetro | Reproducido. JSON idéntico |
| Referencias de E9 sin cambios | C53 de A1, 2,445331695332; de A2, 1,612524303305. Todo `referencia_especificacion` es igual en C8, C11, C13 y C15 |
| «Las 750 filas anteriores no cambian de estado ni de detalle» | Cierto: las 750 filas comunes tienen el mismo estado y el mismo detalle en las seis dimensiones en C13 y en C15, y ningún otro campo distinto |
| Scripts del revisor n.º 6 sobre C14 (`barrido_6`, `clases_6`, `contraejemplos_6`, `consultas_6`, `cobertura_6`, `lectura_filas_c12`) | Reproducidos. Las seis salidas, idénticas a `resultados/revisor6_*_sobre_C14.txt` |
| Scripts de los revisores n.º 1, 3, 4 y 5 sobre C14 | Reproducidos. Las diez salidas, idénticas a `resultados/*_sobre_C14.txt` |
| «Mismos resultados que sobre C12, salvo los recuentos y tres efectos de C14» | Cierto. Igualada la etiqueta de versión, nueve de las diez salidas solo difieren de las de C12 en los recuentos (750 → 752 y los que dependen de ellos) y en los tres efectos que nombra el autor: «Germany & Luxembourg» en el orden de la página, un título «France» y la columna de ajuste, PENDIENTE en lugar de FALLO en 75 casos. La décima, `barrido_tablas`, compara C8 con C14 (comprobado con `diff`, fuera de los scripts) |

`prueba_caja_no_nula.py` y sus dos salidas no cambian desde C4 (`git diff d2e585e c96d544` vacío para los tres archivos). No la he repetido: no he usado LibreOffice.

---

## 3. Estado de R1–R8 (alcance 2)

Los casos F, G, H e I son los de la revisión n.º 6 (`contraejemplos_6` sobre C14, reproducido). Los casos A–E son los míos (`contraejemplos_7.txt`).

| Objeción | Estado | Prueba |
|---|---|---|
| R1 · con el año repetido la fila se asignaba por orden | **Corregida** | F1–F6, FALLO de perímetro; F7, OK; F9–F12, PENDIENTE por la regla de grupos; F13, F14 y F19, PENDIENTE de ejercicio. En mi barrido: las 60 cifras de filas de jurisdicción quedan en FALLO y ninguna otra fila falla por esa regla; de 6.860 tokens asignados por orden, ninguno está más cerca de otra columna de ejercicio que de la asignada; los 46 tokens de las dos tablas por marca con dos ejercicios quedan PENDIENTE (`clases_7.txt`, C, D y H). Sobre la decisión de no seguir la propuesta: §5 a |
| R2 · un encabezado numerado no contaba como título | **Corregida**, con una observación | Los honorarios ya no ven «SWITZERLAND», «SWEDEN» ni «SUISSE». G9 queda con el perímetro OK (E3). La regla toma también por encabezado líneas de prosa: en G9 corta la búsqueda una de ellas, no «5.4 Share-based payments» (S5). G1–G4 siguen PENDIENTE y G5 pasa de OK a PENDIENTE, ahora por la regla de grupos: §5 b |
| R3 · «el FALLO manda» daba FALLO a cifras legítimas del cierre | **Corregida en sus casos, no en la clase** | G6 y G7, PENDIENTE; los diez valores en libros del DEU 2024 p.323, también. Pero doce saldos legítimos del estado de cambios en el patrimonio siguen en FALLO con su propio ejercicio. En los diez de las publicaciones en inglés el ejercicio falla desde C12 (S1). Sobre el umbral: §5 c |
| R4 · el título de tabla en caja normal y las columnas por país sin columna reconocida | **Corregida en sus casos** | H1–H5, PENDIENTE de perímetro. La regla del título corto retiene 1.462 tokens, todos bajo un título que nombra un país (`clases_7.txt`, G). Queda la tabla del WACC por UGE, con una columna por país y sin declaración de unidades: 266 tokens con el perímetro OK (D1–D3 y D5; S4) |
| R5 · en la tabla del fondo de comercio por UGE solo fallaba «CGU France» | **Corregida, salvo una fila** | I11–I15, FALLO. Los 102 tokens de las filas cuyo rótulo empieza por «CGU» o «UGT» quedan en FALLO. La fila «CGU France» del URD 2022 p.298 no entra en esa cuenta: su línea empieza por el número de capítulo del margen, y queda OK en las seis dimensiones (C1, C2; S3) |
| R6 · la clase «entre páginas» es por pertenencia | **Corregida** | Los 246 intervalos, exactos en sus dos extremos; umbrales 145, 99, 2 y 0; R23 de 2021–22 con dos filas correctas y residuo 0,0; dos casos nuevos en el test de residuos (§6). Dos precisiones de redacción (S6 c y d) |
| R7 · frases más fuertes que su prueba | **Corregida** | (a)–(f) acotadas en su sitio. La sexta parte de las respuestas y E9 traen frases nuevas del mismo tipo (S6) |
| R8 · varios | **Corregida**, con un resto en (c) | (a) la hora del punto de recuperación es la de su commit (C14, 02:44:21 UTC); (b) 102 candidatas pasan de FALLO a OK en edición, la columna publicada sigue en FALLO en 591 de 591 y la reexpresada en OK en 588 de 588 (`clases_6` sobre C14, reproducido); (c) el motivo de F12 nombra solo «Elis», pero el de las columnas por país sigue uniendo fragmentos de prosa cuando la tabla va tras un texto a dos columnas (D6; S7 e); (d) leído en el código |

---

## 4. Verificador (alcance 2)

### 4.1 Método

- **Barrido propio** (`barrido_7.py`). Las 459 páginas que el verificador de C14 acepta como del grupo, en los cinco PDF. Cada token numérico de cada línea, declarado como una cifra del grupo en millones de euros (o «%»), de dos columnas, con el ejercicio de la publicación, el anterior y el segundo anterior, y con la edición que la regla exige. Son 25.634 tokens y 76.902 candidatas.
  - Entran también las **líneas sin rótulo**, las que empiezan por un número: 1.822 tokens que los barridos de las pasadas 5 y 6 no recorrían.
  - En las líneas con rótulo, mis transiciones entre C13 y C14 coinciden una a una con las del barrido de la revisión n.º 6 en las páginas del grupo: dos arneses escritos por separado dan los mismos recuentos.
  - En las páginas que no son del grupo el perímetro queda siempre PENDIENTE y ninguna candidata puede quedar OK. Sus transiciones las da el barrido de la revisión n.º 6, que he vuelto a ejecutar.
- **Variantes** (`arnes7.py`). El verificador de C14 con una pieza cambiada en memoria: el umbral de alineación en 3; sin la regla de grupos; con la cabecera ajena aplicada también al asignar por orden (la propuesta que C14 no sigue); sin el encabezado numerado; sin el título corto de tabla. Cada candidata se evalúa con C14, con C13 y con las cinco.
- **Lectura propia** (`geo7.py`), con MuPDF. Para cada número: las celdas de cabecera que tiene encima en su misma banda horizontal, subiendo fila a fila, y los títulos por tipografía. Cubre 25.454 de 25.634 tokens.
- **Clases** (`clases_7.py`) y **contraejemplos** con el verificador oficial de C11, C13 y C14 como proceso aparte (`contraejemplos_7.py`, 40 casos).

### 4.2 Transiciones entre C13 y C14 (páginas del grupo, estado de la fila)

| Transición | Candidatas | Lectura [D] |
|---|---|---|
| OK → FALLO | 152 | 93, filas de UGE; 56, filas de jurisdicción; 1, una línea de prosa sobre Rusia; 2, el «3» de «IFRS 3». **Todas son correcciones** o no son cifras |
| OK → PENDIENTE | 75 | 43, regla de grupos: 27 de las columnas por marca, que son correcciones, y **16 de los honorarios por firma auditora del URD 2025 p.402, cifras legítimas del grupo (§5 b)**. 32 por ejercicio: 12 aceptaciones accidentales de C13 que C14 retira (los movimientos de la corrección por deterioro de 2023, «Impairment loss», aceptados como de 2022 en el URD 2023 p.301, y lo mismo en el URD 2025 p.349 y en el DEU 2024 p.295); 10, el «3» de «IFRS 3» de las cabeceras de reexpresión; 6, líneas de prosa; 3, números sueltos del margen o de un apartado; y el total de flujos futuros sin descontar del URD 2022 p.302, cuyo OK salía de un orden desplazado (F13). Ninguna de las 32 tiene encima solo la fecha del ejercicio declarado |
| PENDIENTE → FALLO | 11 | 8, filas de jurisdicción del URD 2023 p.346; 2, números de página de un sumario; 1, el valor razonable de los activos del plan del URD 2022 p.290 declarado 2021: la cifra está en la columna de 2022 [P], y C13 daba por bueno el ejercicio 2021 |
| FALLO → PENDIENTE | 1.127 | Tablas de vencimientos (el valor en libros y las cifras a más de 5,5 caracteres del año), columnas de plan o de medida, el estado de cambios en el patrimonio, prosa, sumarios, la columna de ajuste de las tablas de reexpresión (en edición) y 15 de la tabla por marca del DEU 2024 (en perímetro). De las 1.829 de la dimensión de ejercicio en líneas con rótulo, 24 tienen encima la fecha de otro ejercicio: 18 en columnas de vencimiento (URD 2022 p.317, «2028 and beyond», y URD 2023 p.321, «Cash flow 2026–2028»), 3 bajo una fecha de plan (URD 2023 p.312) y 3 en prosa. Coincide con lo que declara el autor |
| No OK → OK | 0 | — |
| OK → OK | 5.446 | — |

OK en las seis dimensiones: 5.673 en C13 y 5.446 en C14. De las 5.446, mi lectura da en la cabecera inmediata la fecha del ejercicio declarado en 5.113 (en 93, con otra cabecera además), ninguna fecha en 318 y **la fecha de otro ejercicio en ninguna**; 15 no tienen lectura (`clases_7.txt`, A). Las 318 son, sobre todo, la columna que queda bajo la fecha en las tablas con varias medidas, que el autor declara como límite en el informe §1 (valor en libros, deterioro, activo y pasivo de derivados), y la primera columna del estado de cambios en el patrimonio (S1).

### 4.3 Por regla

**Asignación por orden con alineación.** Corrige F13 y F14. De 6.860 tokens asignados por orden, 6.485 están a menos de 5 caracteres de su columna y ninguno queda más cerca de otra columna de ejercicio (`clases_7.txt`, C). La frase del informe «una cuenta de columnas que coincide por accidente ya no desplaza las cifras» se cumple en estas cinco publicaciones. El límite es la tolerancia de 14 caracteres: entre columnas más juntas que eso, un orden desplazado seguiría pasando [I]. No he encontrado ningún caso.

**La cabecera es la de la propia tabla.** Actúa en 13 líneas (74 tokens). Nueve son cabeceras de fechas de una tabla que empieza después de otra; cuatro son líneas de prosa con fechas, y bajo ellas ninguna candidata queda OK (`clases_7.txt`, J). Sin objeción.

**Grupos de columnas.** El verificador reconoce algún ejercicio repetido en 176 cabeceras. En 11 la repetición es periódica: las dos tablas por marca con dos ejercicios, las cinco de honorarios y cuatro cabeceras sueltas, con uno o dos tokens (tres líneas de prosa y un cuadro del número de acciones). En las otras 165 la regla no actúa: tablas de reexpresión, derivados con activo y pasivo bajo una fecha, y el impuesto por jurisdicción. Las 37 que conservan alguna candidata OK están listadas, y ninguna es una tabla con columnas por entidad (`clases_7.txt`, C). Sobre el coste y el límite: §5 a y b.

**Filas de jurisdicción o de desglose.** 60 tokens en FALLO, todos en las tres tablas del impuesto por jurisdicción, con el rótulo unido correctamente. Ninguna fila del grupo falla por esta regla. La regla lee el rótulo en la línea de la cifra y en las de arriba: una cifra en una línea sin rótulo no la activa (la clase de S2; aquí sin caso real).

**Encabezado numerado.** Corrige G9 y cambia el motivo de G1–G4. De las 418 líneas que la regla toma por encabezado en las páginas del grupo, 22 no lo son por tipografía: S5.

**Título corto de tabla.** Retiene 1.462 tokens bajo 21 títulos distintos; todos nombran un país. Sin la regla, ninguna de esas candidatas quedaría OK: el ejercicio tampoco se acredita. El título sigue vigente para las tablas siguientes que no tienen título propio, aunque no sean de ese país (S7 d).

**Cabecera con países y sin columna reconocida.** Corrige las tablas de combinaciones de negocio (H2). No llega a las tablas sin declaración de unidades: S4.

**Prefijo de UGE.** 102 tokens en FALLO. Resto: S3.

**FALLO solo con la columna alineada.** Corrige G6 y G7. El FALLO de esta rama afecta a 2.123 candidatas (`clases_7.txt`, E):
- 893 tienen encima la fecha de otro ejercicio;
- la mayoría de las demás están en las tablas de vencimientos, bajo las subcolumnas («Nominal», «Interest») de un año de vencimiento que abarca varias: el año de esa columna es, en efecto, otro;
- 10 tienen encima la fecha declarada según mi lectura: son recuentos de los planes de acciones bajo fechas de plan, con la unidad además en PENDIENTE o en FALLO;
- diez son saldos legítimos del estado de cambios en el patrimonio: S1.

**Edición con la regla de cabecera ajena.** Sin objeción. Los dos pasos de OK a FALLO son el «3» de «IFRS 3».

### 4.4 Los scripts de la revisión n.º 6 sobre C14

Las seis salidas que guarda el autor son las que dan los scripts (§2). Lo que la sexta parte de las respuestas dice de ellas es exacto, con una excepción: los 1.207 tokens de R4 (S6 h).

Dos cosas que esas salidas no pueden mostrar, por construcción:
- la clase F («cifras que fallan con los tres ejercicios en C14 y no en C13») da 0, pero no mide las cifras legítimas en FALLO: los saldos de S1 fallan con su ejercicio, no con los tres, y ya fallaban en C13;
- el barrido recorre solo las líneas con rótulo. S2, S3 y el caso del DEU 2024 p.275 de S1 están en las demás.

---

## 5. Las tres decisiones en las que C14 no sigue la propuesta de la revisión n.º 6 (alcance 3)

### (a) R1: grupos de columnas en el perímetro, y no la cabecera ajena al asignar por orden

**Se sostiene.**

- **Lo que habría costado la propuesta** [D] (`clases_7.txt`, C; variante `ajena_en_orden`). El ejercicio pasaría de OK a PENDIENTE en 891 candidatas. De ellas, 54 son OK en las seis dimensiones en C14:
  - 44 son cifras legítimas del grupo, del ejercicio declarado: 24 de las tablas de flujos de efectivo del informe de gestión (URD 2023 p.265 y DEU 2024 p.257), 16 saldos de impuestos diferidos bajo «12/31/AAAA net» y 4 totales del impuesto por jurisdicción (la fila de F7);
  - 10 son parámetros de los planes de accionariado de empleados (tipo de financiación, descuento);
  - ninguna es una columna por entidad.

  El autor tiene razón: la propuesta habría retenido el total del impuesto y otras cifras legítimas por un motivo ajeno. En las 24 de los flujos de efectivo, la «palabra ajena» habría sido el número de capítulo del margen.
- **Lo que la regla de grupos retiene** [D]: las dos tablas por marca con dos ejercicios, completas (URD 2025 p.371 y DEU 2024 p.317: 46 tokens, ninguno OK).
- **Qué cuesta:**
  - el criterio es de forma: la cabecera debe repetir un mismo bloque de ejercicios. Una tabla con una sola columna por entidad no se detecta. **Hay un caso real** [P][D]: la misma tabla de hipótesis de las marcas en los URD 2021 (p.272), 2022 (p.305) y 2023 (p.324), con una columna por marca («Elis · Le Jacquard Français · Kennedy») y sin ejercicios. La regla de grupos no actúa. La fila queda PENDIENTE por dos motivos ajenos a ella: en ejercicio, porque la cabecera no tiene columnas reconocibles; y en perímetro, porque el título corto de la tabla anterior («Sweden», «Switzerland») sigue vigente al llegar a esta (E4, E5; S7 d). En C13 el perímetro era OK;
  - con grupos desiguales tampoco actuaría [H]. No he encontrado ninguna tabla así;
  - no distingue un grupo por entidad de un grupo por medida o por contraparte: es la decisión (b).

### (b) R2: los honorarios por firma auditora (G2, G4) quedan PENDIENTE, no OK

**Se sostiene como elección conservadora, y está declarada como límite.** Uno de sus dos argumentos no vale.

- **El argumento que vale:** el verificador no distingue la columna de una firma auditora de la de una marca, y PENDIENTE no acredita nada. Es cierto: las dos cabeceras tienen la misma forma.
- **El argumento que no vale** [I]: «la columna de una firma es un desglose por firma, no el total del grupo». El perímetro dice de quién es la cifra, no si es un total. Los honorarios que el grupo paga a una firma son un gasto del grupo desglosado por contraparte, igual que la deuda del grupo desglosada por instrumento, que el verificador acepta. La cifra de una marca, en cambio, es de la marca.
- **Qué cuesta** [D] (`clases_7.txt`, D; variante `sin_grupos`):
  - sin la regla quedarían OK en las seis dimensiones 216 candidatas: 40 de las tablas por marca, que la regla retiene con razón, y **176 de las cinco tablas de honorarios**, que son cifras legítimas del grupo;
  - 16 de esas 176 eran OK en C13 (URD 2025 p.402; E1). Las otras 160 tenían el perímetro PENDIENTE en C13, por el título de país que describía R2;
  - T14 pide al frente técnico el mismo PENDIENTE para G2 y G4. Si un cálculo usara una fila así, el contraste la anotaría como pendiente y terminaría con código 2.
- **Atenuante** [D]: la propuesta de la revisión n.º 6 tampoco habría dado OK a todas. Con la cabecera ajena aplicada al orden, 29 de las 176 habrían quedado PENDIENTE en ejercicio, bajo palabras de la cabecera como «(excl» (DEU 2024 p.347, 5; URD 2021 p.298, 10; URD 2023 p.355, 14).
- Ninguna fila real está en estas tablas.

### (c) R3: umbral de alineación de 5,5 caracteres, no de 3

**Se sostiene.** Es un umbral empírico y los datos lo apoyan.

- **Lo que habría costado el 3** [D] (`clases_7.txt`, E; variante `al3`). Pasarían de FALLO a PENDIENTE 820 candidatas. Según mi lectura, 208 tienen encima la fecha de otro ejercicio, sobre todo en las tablas de planes de acciones (DEU 2024 p.306 y URD 2025 p.360, 51 cada una) y de impuestos diferidos. Es el mismo número que da el autor con la lectura del revisor n.º 6.
- **La distancia que mide el verificador** [D]. En los 2.912 tokens que tienen encima solo una fecha «dd/mm/aaaa», la distancia entre el centro del número y el del año de su columna tiene mediana 1,5; supera 3 en 373 casos (el 13 %) y 5,5 en 7. En los números de un carácter la mediana es 4,5, que es la cifra del autor. Con 3, una de cada ocho columnas bien alineadas dejaría de contar como alineada.
- **Qué cuesta:**
  - de los diez saldos legítimos de S1 que quedan en FALLO en las publicaciones en inglés, tres quedarían PENDIENTE con 3 (URD 2023 p.280 y p.281, a 4,5 y 3,5 caracteres, y uno del URD 2021 p.230, a 5,5). Los otros siete fallan con los dos umbrales: el año del título queda a 0,5 o 1,5 caracteres;
  - 24 cifras con la fecha de otro ejercicio encima, a más de 5,5, bajan de FALLO a PENDIENTE. El autor lo declara.
- El umbral no resuelve la clase de R3; solo decide dónde cae la frontera. Lo que falla en S1 no es la distancia, sino qué se toma por columna.

---

## 6. Contraste (alcance 4)

Prueba: `lectura_filas_c14.py` → `lectura_filas_c14.txt` (12 lecturas con MuPDF, pdfminer y PDFium, ninguna diferencia) y `sondas_umbral_7.py` → `sondas_umbral_7.txt`. Las dos filas nuevas, además, vistas en la página renderizada con MuPDF.

### 6.1 Las dos filas nuevas

| Fila | Página PDF (folio) | Línea y columna [P] | Ej. | Unidad y perímetro [P] | Veredicto |
|---|---|---|---|---|---|
| `VENTAS_SEG_U22_2021` | URD 2022 p.279 (277) | «SEGMENT REVENUE 956.7 · 738.6 · 499.0 · 364.3 · 234.1 · 236.1 · 19.4 · 3,048.3», columna «Total», segundo bloque, encabezado «2021» | 2021 | «(In millions of euros)»; nota 3.1 de los estados consolidados | Correcta |
| `VENTAS_SEG_U23_2022` | URD 2023 p.296 (294) | «SEGMENT REVENUE 1,189.5 · 873.8 · 580.8 · 476.6 · 347.3 · 330.9 · 21.9 · 3,820.9», columna «Total», segundo bloque, encabezado «2022» | 2022 | ídem | Correcta |

Edición: las dos son la publicación vigente para su ejercicio según la regla de la Historia [D]. En las dos tablas el total de «SEGMENT REVENUE» es igual al de «External customers» [P].

### 6.2 R23 de 2021 y 2022

| Identidad | Cálculo [D] | Residuo | Cota |
|---|---|---|---|
| R23 2021 | 3.048,3 (URD 2022 p.258) − 3.048,3 (p.279) | 0,0 | 0,10 |
| R23 2022 | 3.820,9 (URD 2023 p.276) − 3.820,9 (p.296) | 0,0 | 0,10 |

Las contrapartes de la cuenta de resultados están bajo «12/31/2021 restated(a)» y «2022 restated*» [P]. Las dos presentaciones de cada año son de la misma publicación: no hay mezcla de ediciones. Es una segunda página con su propia cabecera, su propia declaración de unidades y su encabezado de año, como R23 en 2023–25 [I].

### 6.3 Intervalos de detección

- **`errores_sin_deteccion_entre_paginas`: exacto en las 246 entradas** [D]. Para cada una he ejecutado el contraste del autor con esa sola entrada desplazada, justo dentro y justo fuera de cada extremo (0,002), y he mirado qué residuos entre páginas fallan. Dentro no falla ninguno; fuera falla alguno. No uso los coeficientes que lleva el autor.
- **`umbrales_entre_paginas`: 145, 99, 2 y 0**, exacto. Las dos de más de 5 unidades son el FCF antes de impuestos y los impuestos pagados de 2024, de −0,55 a +0,15.
- **Las 97 entradas que mueven la referencia** tienen identidad entre páginas, y ninguna otra la mueve (derivación propia: una ejecución por entrada usada, con +1,0). Su mayor error sin detectar va de 0,10 a 0,50, como dice E9.
- **El límite de la cota es inclusivo** [D]. El contraste da por bueno |residuo| ≤ cota. Con R23 y R40, cuya cota es 0,10, un error de exactamente una décima en las ventas no falla; dos décimas, sí (`sondas_umbral_7.txt`, 2). El de una décima lo detecta la comparación con el libro en las ventas de la cuenta de resultados, y nada en las de la información por segmentos ni en las del informe de gestión de 2020. De ahí S6 c.

### 6.4 «La clase es por pertenencia»

Está bien explicado en `que_acredita_cada_clase` y en el informe §0.2: basta que la entrada intervenga en una identidad entre páginas, y lo que se acredita es el número salvo un error dentro del intervalo. Dos matices [I]:
- el intervalo es el de un error en esa entrada **sola**. El JSON lo dice; el informe no. Dos errores iguales en las dos presentaciones de una cifra dejan intacta su identidad;
- los tramos cuentan el mayor error que no se detecta, no el menor que sí (S6 d).

---

## 7. Objeciones nuevas

Todas las filas existen en el PDF [P]. Las de S1, S2 y S3 las he visto además en la página renderizada. Ninguna afecta a una fila real del CSV: ninguna de las 713 filas de tabla está en las líneas de estos casos.

### S1 · menor · `verificar_cifras.py`, ejercicio (R3, resto) · el año del título de la tabla cuenta como columna de ejercicio

- **Qué ocurre** [P][D]. El estado de cambios en el patrimonio lleva el título en dos líneas: «6.1.5 Consolidated statement of changes in equity / as at December 31, 2022». En la rejilla de `pdftotext` la segunda línea va sangrada, y su «2022» cae encima de la primera columna de cifras, la del capital social. El verificador lo toma por la única columna de ejercicio de la tabla, alineada con esas cifras. Su cabecera verdadera es «Share capital».
- **Prueba.** `contraejemplos_7.txt`, A1–A18 y E2; `clases_7.txt`, E.

  | Cifra [P] | Declarada con su ejercicio | Declarada con el año del título |
  |---|---|---|
  | URD 2022 p.262 · capital a 31-12-2021, 224,1 | **FALLO** (C11: PENDIENTE) | PENDIENTE |
  | URD 2025 p.328 · capital a 31-12-2024, 236,7 | **FALLO** (C11: PENDIENTE) | PENDIENTE |
  | URD 2023 p.280 · capital a 31-12-2022, 230,1 | **FALLO** (C11: PENDIENTE) | PENDIENTE |
  | URD 2021 p.230 · capital a 31-12-2020, 221,8 | **FALLO** (C11: PENDIENTE) | PENDIENTE |
  | DEU 2024 p.274 · capital a 31-12-2023, 234,0 | **FALLO** (también en C11) | **OK en las seis dimensiones** |
  | DEU 2024 p.275 · capital a 31-12-2022, 230,1 | **FALLO** (también en C11) | **OK en las seis dimensiones**, como de 2023 y vigente |

  - Es la fila del saldo de apertura: el cierre del ejercicio anterior. El motivo en C14 es «la columna reconocida más próxima, alineada con el token (0.5 caracteres), es de 2022, no de 2021 (el token está además bajo «Share»)».
  - En total, doce cifras: diez en las cuatro publicaciones en inglés y dos en el DEU 2024. En seis, las del estado del propio ejercicio, el ejercicio es lo único que falla; en las otras seis, las del estado del ejercicio anterior, falla además la edición.
  - De las diez en inglés, nueve están pasadas por C11: allí el ejercicio quedaba PENDIENTE (A1, A3, A5, A6, A12–A15 y E2). La décima es la fila «Ajusted balance as at January 1, 2020» del URD 2021 p.231.
  - Los movimientos y el saldo de cierre de esa columna se aceptan o quedan PENDIENTE con el año del título, que es el suyo: aciertan por coincidencia (A10, A11; en el URD 2022 p.262, 11 movimientos quedan OK con «columna de 2022 (alineación con la cabecera)»).
- **Causa** [D]. Dos piezas:
  - la zona de cabecera admite la continuación sangrada de un título, y su año cuenta como una columna de ejercicio;
  - desde C12, una columna de otro ejercicio da FALLO aunque el token esté bajo una cabecera ajena. C14 lo limita a 5,5 caracteres, y aquí el año del título queda entre 0,5 y 5,5.

  En el DEU 2024 la asignación es directa: el verificador no ve el token bajo «Capital émis», y por eso allí el año del título se acepta sin más (los motivos son «columna de 2024 (alineación con la cabecera)» y «la columna es de 2024, no de 2023»).
- **Por qué importa.**
  - Es la clase de R3: un «no sé» convertido en un rechazo equivocado. `contraste_f1.py` se niega a calcular con un FALLO. C14 la corrige en las tablas de vencimientos y no aquí.
  - La inversión es completa: el ejercicio verdadero falla y el equivocado no. En el DEU 2024, un saldo de 2022 pasa como de 2023, vigente y del grupo, en las seis dimensiones. Esto último no lo introduce C12 ni C14: ya ocurría en C11.
  - El informe §1 describe la regla como «FALLO si la columna de otro ejercicio está alineada con ella». Aquí lo alineado no es una columna.
  - Es un estado principal de las cuentas consolidadas, en las cinco publicaciones.
- **Corrección propuesta.**
  - No tomar por cabecera de columnas la línea de un encabezado numerado ni su continuación: la regla de R2 ya sabe reconocer el encabezado.
  - En las filas que llevan la fecha del saldo en su rótulo, tomar el ejercicio de la fila, no de una columna (el rótulo va partido en dos líneas: «Balance as at December / 31, 2021 restated(a)»).
  - Añadir A1, A8 y A9 al test y a T14.

### S2 · menor · `verificar_cifras.py`, perímetro (Q5, resto) · una fila de segmento cuya cifra cae en una línea sin rótulo pasa como del grupo

- **Qué ocurre** [P]. En la tabla de crecimiento del informe de gestión del URD 2023 (p.261, «REVENUE BY GEOGRAPHIC REGION»), el rótulo «Scandinavia and Eastern Europe» ocupa dos líneas y las cifras van centradas entre las dos. `pdftotext` las deja en una línea propia, sin texto: «599.2 · 580.7 · 8.5% · 0.3% · -5.5% · 3.2%», con «Scandinavia and Eastern» encima y «Europe» debajo.
- **Prueba.** `contraejemplos_7.txt`, B1–B7. Quedan **OK en las seis dimensiones**, en C11, C13 y C14:
  - las ventas del segmento de 2022 (580,7) y de 2023 (599,2), declaradas del grupo;
  - su crecimiento publicado de 2023 (3,2 %) y su crecimiento orgánico (8,5 %), declarados como los del grupo con el modo «crecimiento».

  Controles: la fila «France» falla; la fila «United Kingdom and / Ireland», con la cifra en la segunda línea del rótulo, falla desde C12; el total del grupo queda OK.
- **Alcance** [D] (`clases_7.txt`, I). En las páginas del grupo, las líneas sin rótulo con dos números o más y alguna candidata OK son cuatro: esta, la de S3, la del DEU 2024 p.275 de S1 y una fila del grupo (URD 2023 p.266).
- **Causa** [D]. Todas las reglas de fila leen el rótulo en la línea de la cifra y, si está partido, en las de arriba. Si la línea de la cifra no tiene rótulo, no hay nada que leer.
- **Por qué importa.**
  - Las respuestas (quinta parte, Q5) dicen que en las tablas de crecimiento «ninguna fila de segmento queda OK en ventas ni en crecimiento orgánico», y la revisión n.º 6 lo confirmó. Era cierto en su universo: las dos pasadas barrían solo las líneas con rótulo.
  - T14 pide al frente técnico que rechace «segmento, sublínea de un segmento, país o fila «Other» como grupo» y los rótulos «partidos en dos líneas».
  - La misma ceguera vale para las reglas nuevas de C14 que leen el rótulo: jurisdicciones y UGE. Aquí sin caso real en las jurisdicciones; en las UGE, S3.
- **Atenuantes** [D]. No lo introduce C14. El informe §1 declara el límite general: una cifra de otro perímetro sin ninguna señal reconocida no se detectaría. Las cuatro filas reales de esa tabla salen de la fila TOTAL. Y la segunda línea lo cubre: las ventas de un segmento romperían R23, y su crecimiento, R42.
- **Corrección propuesta.** Cuando la línea de la cifra no tiene rótulo, tomarlo de las líneas contiguas de arriba y de abajo. Añadir B1 y B3 al test y a T14, y recorrer también las líneas sin rótulo en los barridos.

### S3 · menor · `verificar_cifras.py`, perímetro (R5, resto) · «CGU France» del URD 2022 p.298 sigue OK: el número de capítulo del margen ocupa el lugar del rótulo

- **Qué ocurre** [P]. Las páginas llevan en el margen una pestaña con el número del capítulo («6»). En el URD 2022 p.298 queda a la altura de la primera fila de la tabla del fondo de comercio por UGE, y `pdftotext` lo pone al principio de esa línea: «6 · CGU France · 1,418.1 · 1,415.1». Para el verificador el rótulo de la fila es «6».
- **Prueba.** `contraejemplos_7.txt`, C1–C4. El fondo de comercio de la UGE Francia de 2021 (1.415,1) y de 2022 (1.418,1), declarado del grupo, queda **OK en las seis dimensiones** en C11, C13 y C14. La fila siguiente, «CGU Sweden & Finland», falla desde C14; la misma fila «CGU France» del URD 2025 p.363, sin la pestaña en su línea, falla desde C12.
- **Alcance** [D] (`clases_7.txt`, I). En las páginas del grupo hay 18 líneas que empiezan por la pestaña seguida de un rótulo. Solo esta es de una UGE, un país o un segmento. Dos filas reales están en una línea así (`CAPX_LINO_U23_2023` y `_2022`, URD 2023 p.266: «5 · Linen purchases»): son cifras del grupo y su estado es correcto, pero las reglas que leen el rótulo tampoco lo ven ahí.
- **Por qué importa.** Las respuestas dicen: «las filas de UGE de las cinco publicaciones pasan a FALLO». Una no. Es la fila que citaba Q5 (E15, URD 2025 p.363), en otra edición.
- **Corrección propuesta.** Descartar como rótulo un dígito suelto al principio de la línea cuando lo sigue una celda de texto. Añadir C1 al test.

### S4 · menor · `verificar_cifras.py`, perímetro (R4, resto) · la tabla con una columna por país y sin declaración de unidades conserva el perímetro OK

- **Qué ocurre** [P]. La tabla de hipótesis del WACC por UGE lleva una columna por país («Country · France · Germany · Brazil · Denmark · Spain · Mexico · Netherlands · Sweden · Switzerland») y sus cifras son porcentajes: no declara unidades ni fechas. Está en las cinco publicaciones.
- **Prueba.** `contraejemplos_7.txt`, D1–D6; `clases_7.txt`, G. Son 266 tokens con el perímetro OK, en dos formas:
  - en el URD 2025 p.369 y en el DEU 2024 p.315 la tabla abre la página y toda ella conserva el perímetro OK (117 y 104 tokens), también la columna de Francia (D1–D3);
  - en los URD 2021 p.270, 2022 p.303 y 2023 p.322 la tabla va tras un texto. Sus filas sí fallan en perímetro (D6), salvo las dos últimas, «Pre-tax discount rate AAAA / (approximation)» (16, 15 y 14 tokens; D5). En ellas la única columna de ejercicio que ve el verificador es el año de la primera línea del rótulo.

  Es igual en C11 y en C13: no lo introduce C14.
- **Causa** [D]. La regla de columnas por país y la nueva de «cabecera con tres países o más y sin columna reconocida» necesitan una zona de cabecera, que se busca a partir de la declaración de unidades o de una línea de ejercicios. Sin ninguna de las dos no hay zona (primera forma). Con un año en el rótulo de la fila, la zona empieza en esa línea y la cabecera de países queda fuera (segunda forma) [I].
- **Por qué importa.** Poco: en todas la fila sigue PENDIENTE, porque el ejercicio no se acredita, igual que en los casos de R4. Pero es la misma clase que H2, y T14 la pide en general. La tabla hermana por marcas, con una columna por marca y sin ejercicios, tampoco se reconoce por su cabecera (§5 a).
- **Corrección propuesta.** Si no hay declaración de unidades ni línea de ejercicios, buscar la cabecera en la línea de celdas que precede al bloque de filas. No tomar por cabecera de ejercicios la primera línea de un rótulo partido. Añadir D1 y D5 al test.

### S5 · forma · `verificar_cifras.py`, perímetro (R2) · la regla del encabezado numerado toma por encabezado líneas de prosa

- **Prueba.** `clases_7.txt`, F. De las 418 líneas que `es_encabezado_numerado` acepta en las páginas del grupo, 395 son títulos por tipografía, 22 no lo son y una no tiene lectura. Las 22 son entradas de sumario y líneas de prosa que empiezan por una referencia: «Note 7.2 “Contingent liabilities” to the consolidated financial statements», «Note 5.3 “Employee benefit assets/liabilities” provides further details», «3.1 “Income from ordinary activities”;».
- **En los casos que cita el autor corta la prosa, no el encabezado** [P][D]. Para el plan de acciones G9 (URD 2025 p.360) y para la misma tabla del URD 2023 p.312, la búsqueda sube a la página anterior y se detiene en una línea de prosa: «Note 5.2 “Expenses related to employee benefits.”». En el URD 2025 p.359 esa línea es la 65 y el encabezado «5.4 Share-based payments», la 54. Son 278 de los 398 tokens cuyo perímetro libera esta regla en mi barrido (387 en las líneas con rótulo, la cifra del autor). Las respuestas dicen: «Bajo «5.4 Share-based payments», el plan de acciones G9 queda con el perímetro OK».
- **Por qué importa** [I]. El resultado es el correcto, porque el encabezado verdadero está justo encima. Pero una línea de prosa así dentro de un bloque de país liberaría sus tablas. En las cinco publicaciones no ocurre: ninguna de las 22 queda bajo un título de país.
- **Corrección propuesta.** Exigir que tras la numeración no venga una comilla ni una frase con verbo, o que la línea anterior esté en blanco. Corregir la frase de las respuestas.

### S6 · forma · respuestas (sexta y quinta parte), informe §0 y §2, E9 · frases más fuertes que su prueba o recuentos inexactos

- (a) **Respuestas, R5:** «las filas de UGE de las cinco publicaciones pasan a FALLO». Todas menos una (S3).
- (b) **Respuestas, R3:** la prueba es «clase F del revisor (cifras que fallan con los tres ejercicios en C14 y no en C13): 0». Esa clase no mide las cifras legítimas en FALLO (§4.4). Con S1, «aceptada y corregida» vale para las tablas de vencimientos, no para la clase.
- (c) **Informe §0.2 y §2, y respuestas, R6:** las ventas quedan contrastadas entre páginas «desde ±0,1». Un error de una décima exacta no hace fallar R23 ni R40; el primero que falla es de dos décimas (§6.3). Debería decir «por encima de ±0,1».
- (d) **Informe §0.2:** «145 entradas lo detectan desde 2 unidades de su última cifra, 99 entre 2 y 5, y 2 entre 5 y 10». Los tramos son del mayor error que **no** se detecta. Contando desde qué número entero de unidades se detecta en los dos sentidos: 5 desde una, 112 desde dos, 69 desde tres, 17 desde cuatro, 33 desde cinco y 10 desde seis (`sondas_umbral_7.txt`, 3). De las 145, 28 tienen el umbral en dos unidades exactas y no detectan un error de dos: por ejemplo, la línea del EFE de amortizaciones y provisiones de 2024 no falla con ±0,2 y sí con ±0,3.
- (e) **E9:** la lista de identidades de las 97 entradas que mueven la referencia incluye «R23 en 2021–22 desde C14». Las ventas de 2021 y de 2022 no mueven la referencia, y ninguna de las 97 interviene en R23 de esos años (`sondas_umbral_7.txt`, 4). La misma lista incluye R25 y R35 de 2021–22, que el propio contraste clasifica como de la misma página; eso ya estaba antes de C14. La conclusión no cambia: las 97 tienen identidad entre páginas.
- (f) **Respuestas, quinta parte, Q5:** «ninguna fila de segmento queda OK en ventas ni en crecimiento orgánico» (S2).
- (g) **Respuestas, R2:** «Bajo «5.4 Share-based payments»…» (S5).
- (h) **Respuestas, R4:** «1.207 tokens de las tablas de sensibilidad y de combinaciones de negocio pasan de OK a PENDIENTE en perímetro, y la lectura propia del revisor nombra un país en todos». La salida guardada (`revisor6_clases_6_sobre_C14.txt`, C) da 1.299 tokens: 48 por la regla de grupos y 1.251 por las dos reglas de R4. De estos, la lectura del revisor nombra un país en 1.213, no lo nombra en 23 (los títulos «Great Britain» y «Mexico» del URD 2022 p.305 y «Interest rate swap – Chile») y no tiene lectura en 15.
- **Corrección propuesta.** Ajustar cada frase a lo que su prueba cubre.

### S7 · forma · varios

- (a) `resultados/revisor5_barrido_tablas_sobre_C14.txt` empieza «versión nueva C11 · versión anterior C8» y dice «Equivalencia módulo = ejecución oficial en C11: 713 filas». Compara C8 con C14: el script se ejecutó con sus nombres por defecto. Lo he reproducido así, idéntico.
- (b) `PUNTO_DE_RECUPERACION.md` de C15, §4, paso 2: da como alcance de la pasada 7 «`git diff 9711f04..C15`». 9711f04 es un commit de la rama del revisor, que parte del primer commit del autor: esa diferencia abarca 123 archivos de la carpeta. El alcance es `c11a6de..cf55865` (41 archivos), como dice el encargo. El punto posterior al congelado (66d188c) ya no lleva esa frase.
- (c) La cabecera de `verificar_cifras.py` sigue diciendo «se comprueba en cinco dimensiones». Son seis.
- (d) El título corto de tabla sigue vigente para las tablas siguientes sin título propio. En el URD 2022 p.305, «Sweden» es el motivo de 74 tokens; 30 son de la tabla de Suecia y 44, de la tabla de las marcas y de la de sensibilidad de la marca Elis (E4, E5). El resultado, PENDIENTE, es el prudente; el motivo no es exacto, y es lo único que retiene el perímetro de esas tablas (§5 a).
- (e) R8 c, resto: el motivo de las columnas por país sigue uniendo fragmentos de prosa cuando la tabla va tras un texto a dos columnas. En el URD 2021 p.270: «la columna es la de «by using the Board are estimated discounted before WC − income horizon has duration […] France»» (D6).

---

## 8. Coherencia entre documentos (alcance 5)

He leído la sexta parte de las respuestas, el informe (§0, §1, §2, §12 y §13), la especificación (E9, T12 y T14), el README, `ESTADO.md`, `REGISTRO_CONFIGURACION.md` y `PUNTO_DE_RECUPERACION.md`.

- **Recuentos.** Coinciden entre sí y con las salidas: 752 = 713 + 39; 738, 14 y 0; 108 = 21 + 21 + 66; 292 = 136 + 127 + 29; 126 residuos (88 entre páginas y 38 de la misma página); 419 = 246 + 140 + 2 + 31; 8 de 55 páginas, con 24 entradas; 24 casos; 530 = 386 + 2 + 23 + 8 + 111; 713/713; 97; umbrales 145, 99, 2 y 0. Los 21 PENDIENTE del test que desglosa el informe §0.1 suman (1 + 1 + 2 + 6 + 11). No he encontrado ningún recuento de C13 en los documentos principales, salvo donde se cita como historia.
- **Hashes y alcance.** C14 y C15, bien registrados. El congelado solo añade el hash. Excepción: el alcance de S7 b.
- **Estado y registro.** Describen bien la pasada 6 y C14, y dejan esta pasada pendiente. El commit posterior al congelado (66d188c) registra el encargo y actualiza el punto de recuperación; no es parte del material revisado.
- **Reproducción (§13).** Los comandos funcionan tal como están escritos.
- **Afirmaciones más fuertes que su prueba:** las de S6. No encuentro otras en lo leído.
- **Afirmaciones comprobadas y ciertas:**
  - «las 750 anteriores no cambian de estado ni de detalle»;
  - «ninguna candidata pasa a OK»;
  - los recuentos de R3 (1.829, 1.716, 86, 24 y 3) y de R8 b (102, 97 y 5; 591 y 588);
  - «con 3, 208 cifras cuya cabecera alineada es de otro ejercicio pasaban de FALLO a PENDIENTE»;
  - los intervalos de las ventas con solo R42 y los del crecimiento publicado;
  - «las 97 entradas que mueven la referencia tienen identidad entre páginas»;
  - «mismos resultados que sobre C12, salvo los recuentos y tres efectos de C14»;
  - lo que el punto de recuperación dice que cubren las pruebas, y lo que no.
- **T14.** Recoge las reglas nuevas con sus casos y el límite de la alineación. Le faltan los límites de S1 a S4, que son de las mismas reglas.

---

## 9. Conclusiones materiales y lo no comprobado

**Conclusiones materiales.** Ninguna cambia: la conciliación y el FCF base, C48 = 108, el doble cómputo del arrendamiento bajo su premisa, los intangibles adquiridos pendientes de política, la reinversión necesaria no publicada como importe y `pendiente_de_datos`. Las decisiones económicas siguen pendientes de la persona responsable.

**Sobre el verificador** [I]. C14 es la primera respuesta que no crea ninguna aceptación nueva: corrige y retiene. Sus tres decisiones propias son defendibles con datos. Lo que queda es de otra naturaleza que R1–R4: no son efectos de las correcciones, sino sitios donde la rejilla de `pdftotext` no dice lo que las reglas suponen. El título cae encima de una columna, la cifra queda en una línea sin rótulo, la pestaña del margen ocupa el lugar del rótulo, la tabla no declara unidades. Los tres primeros dan OK en las seis dimensiones a una cifra de otro ejercicio o de otro perímetro, y dos de ellos no estaban en el universo de los barridos anteriores. Las reglas suponen que cada cifra tiene su rótulo en su línea y que todo lo sangrado encima de la tabla es cabecera. Lo que sostiene las cifras reales sigue siendo la segunda línea: las identidades entre páginas y la Historia. Para las entradas sin segunda línea y las de las ocho páginas sin ancla sigue valiendo lo que dice el informe: cobertura pendiente.

**No comprobado en esta pasada:**
- Lo que no cambia entre C13 y C15, salvo lo que hizo falta para reproducir.
- Los §3 a §11 del informe y el resto de la especificación: no cambian en el alcance.
- La prueba de caja no nula con LibreOffice: no cambia desde C4 y no la he repetido.
- Las candidatas del barrido una a una: he revisado las clases, sus páginas y los casos con el verificador oficial.
- Las páginas que no son del grupo, de las que solo he reproducido las transiciones con el barrido de la revisión n.º 6.
- Otras declaraciones: el barrido declara cada token solo como cifra del grupo de dos columnas. Los modos «crecimiento», «saldo», «movimientos», «titulo» y «max_cabecera» y los perímetros de segmento solo están probados en las filas reales, en el test del autor y en B3, B4 y B7. El cambio de la zona de cabecera afecta también a esos modos.
- Clases de error que mis filtros no señalan. Mi lectura no ve las cabeceras que abarcan varias columnas.
- El 0,7 % de los tokens que mi lectura no localiza.
- Cuántas de las tablas que retiene el título corto no son del país del título (S7 d): doy el caso del URD 2022 p.305 y las tres tablas de las marcas, no un recuento.
- Las reglas V-F1a a V-F1h y T8 y T14: especificadas, no implementadas.
- El árbol del hito 4.15 y la rama del frente técnico.

---

## 10. Reproducción de esta revisión

Hace falta PyMuPDF, que el entorno no trae: `pip install --target <carpeta> pymupdf`, y esa carpeta se pasa con `--pylibs`. Para `lectura_filas_c14.py` hacen falta también pdfplumber y pypdfium2. Versiones usadas: Python 3.13, poppler 24.02 (`pdftotext`), PyMuPDF 2.1 (MuPDF 1.28.6), pdfplumber 0.11.10 (pdfminer 20260107) y pypdfium2 5.13.0.

```bash
B=docs/validacion_economica_paralela/frente_E_F1_elis
C8=<worktree de 9744177>/$B ; C11=<worktree de 364129a>/$B ; C13=<worktree de 1b80b5d>/$B ; C15=<worktree de c96d544>/$B
RAIZ=<ruta>/munger_v2_r1 ; LIBS=<carpeta con pymupdf> ; TODAS=<carpeta de trabajo>/todas7.jsonl.gz
LIBRO=$RAIZ/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx
cd revision/scripts_revisor_7
python3 -I reproduccion_7.py --raiz "$RAIZ" --autor "$C15" --c13 "$C13" --otra C11="$C11" --otra C8="$C8" --revisores --c8 "$C8"
python3 -I barrido_7.py --raiz "$RAIZ" --c13 "$C13" --c14 "$C15" --pylibs "$LIBS" --todas "$TODAS" --salida ../resultados_revisor_7/barrido_7.txt
python3 -I clases_7.py --todas "$TODAS" --raiz "$RAIZ" --autor "$C15" --pylibs "$LIBS"
python3 -I contraejemplos_7.py --raiz "$RAIZ" --version C11="$C11" --version C13="$C13" --version C14="$C15"
python3 -I lectura_filas_c14.py --raiz "$RAIZ" --autor "$C15" --pylibs "$LIBS"
python3 -I sondas_umbral_7.py --autor "$C15" --libro "$LIBRO"
```

Los scripts que no llevan `--salida` escriben por la salida estándar; cada uno se guardó en el archivo de su nombre. La reproducción completa, con los scripts de los revisores anteriores, tarda unos 25 minutos.

Salidas en `revision/resultados_revisor_7/`:

| Archivo | Contenido |
|---|---|
| `reproduccion_7.txt` | Manifiesto, CSV regenerado, cadena del §13 y sondas frente a las salidas del autor; las 750 filas comunes con C13; referencia de E9 en C8, C11, C13 y C15; las 16 salidas de los scripts de los revisores n.º 1, 3, 4, 5 y 6 sobre C14 frente a las guardadas |
| `barrido_7.txt` | 76.902 candidatas de las 459 páginas del grupo: equivalencia con la ejecución oficial, transiciones C13 → C14 en líneas con rótulo y sin rótulo, y efecto de cada variante |
| `clases_7.txt` | Candidatas OK según la cabecera inmediata (A); transiciones por motivo y lectura propia (B); las tres decisiones (C, D y E); encabezado numerado (F); título corto y columnas por país (G); UGE y jurisdicciones (H); líneas sin rótulo y pestaña del margen (I); cabecera de la propia tabla (J) |
| `contraejemplos_7.txt` | 40 casos sobre filas reales con el verificador oficial de C11, C13 y C14: A (S1), B (S2), C (S3), D (S4) y E (controles de las decisiones y tabla de las marcas) |
| `lectura_filas_c14.txt` | Las dos filas nuevas y sus contrapartes leídas con MuPDF, pdfminer y PDFium; R23 de 2021 y 2022 con fracciones exactas |
| `sondas_umbral_7.txt` | Los 246 intervalos en sus dos extremos; errores de una y de dos unidades en las entradas que nombran los documentos; unidades enteras desde las que se detecta; las 97 entradas que mueven la referencia y sus identidades |

`arnes7.py` y `geo7.py` son los módulos comunes. El barrido completo (un archivo comprimido) no se guarda en el repositorio: se regenera con los comandos de arriba. Tampoco se guardan las salidas de los scripts de los revisores anteriores sobre este commit: son idénticas a las que el autor guarda en `resultados/*_sobre_C14.txt`.

Algunas comprobaciones puntuales están hechas con órdenes sueltas y no con estos scripts: las diferencias entre commits (`git diff`); la comparación de las salidas de los revisores sobre C12 y sobre C14 (`diff`, tras igualar la etiqueta de versión); la lectura de páginas concretas con `pdftotext -layout` para describir las tablas; y las consultas al barrido que desglosan las clases de §4.2, §4.3 y §5 más allá de lo que imprime `clases_7.py` (el desglose de las 32 de ejercicio, el de las candidatas en FALLO por la columna alineada, el estado de los honorarios en C13 y con la variante de la cabecera ajena, y el reparto de los 74 tokens del URD 2022 p.305).
