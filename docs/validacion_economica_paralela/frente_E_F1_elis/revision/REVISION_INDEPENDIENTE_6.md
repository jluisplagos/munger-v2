# Revisión independiente n.º 6 · frente E · F1 · Elis · lo afectado por C12

Fecha: 16-nov-2026. Material revisado: commit congelado `1b80b5d5348e6e39dd1d632cafbbbf4e5dd3685a` (C13) de la rama `auditoria/economica-f1-frente-e`. C13 solo añade a C12 (`4f3f9ba9c8240143269368c41787736b3867e97b`) el registro de su hash (comprobado: `git diff 4f3f9ba 1b80b5d` toca `ESTADO.md`, una línea de las respuestas y el manifiesto). Alcance: `git diff 364129a 1b80b5d`, es decir, la incorporación de la revisión n.º 5 (`202f566`) y la respuesta a Q1–Q7 (C12). Bases de comparación: C11 (`364129a…`) y, para los scripts de la revisión n.º 5, C8 (`97441770…`), cada una en su propio worktree.

Se publica en la rama `auditoria/economica-f1-frente-e-revision`, sobre el commit 595d2f6.

Marcas: **[P]** publicado (leído en el PDF) · **[D]** derivado · **[I]** interpretación · **[H]** hipótesis.

Este documento no contiene valoraciones, precios, recomendaciones de inversión ni declaraciones de aptitud. No adopta ninguna decisión pendiente. Se conservan C48 = 108 y E1/D3/E2/E6. No modifica el material del autor, el producto ni los libros.

---

## 0. Resultado en breve

1. **Las cifras que declara el autor se reproducen todas**, con salidas idénticas byte a byte (§2). También son idénticas a las que guarda el autor las salidas de los scripts de los revisores n.º 1, 3, 4 y 5 ejecutados sobre C13.
2. **Las siete filas nuevas de C12 son correctas** en página, línea, columna, ejercicio, unidad, perímetro y edición. Las he leído con pdfminer (por la posición real de las palabras), con PDFium y a la vista, en la página renderizada (§5).
   - R41, R8 de 2021–22 y R24 de 2023 cierran con residuo 0,0.
   - R42 da los residuos y las cotas que declara el autor. La linealización es correcta y la cota es adecuada.
   - El límite de sensibilidad de R42 que declara el autor es cierto, pero el caso que da no es el único (R6).
3. **Cobertura (§6).** Los recuentos del autor son exactos: 244 / 140 / 2 / 31, y 8 de 53 páginas, con 24 entradas, sin identidad entre páginas. Las 97 entradas que mueven la referencia tienen identidad entre páginas y ninguna otra la mueve. Lo he derivado por otra vía: el coeficiente de cada entrada en cada identidad. Dos matices, sin efecto en la referencia (R6).
4. **Estado de Q1–Q7 (§3):**
   - Q1, Q3 y Q6: corregidas;
   - Q4: corregida para los bloques de pensiones, con dos efectos nuevos (R2 y R4);
   - Q2 y Q5: corregidas en parte;
   - Q7: corregida, con un resto.
5. **C12 introduce cuatro clases nuevas de error en el verificador.** Ninguna afecta a las 750 filas reales, cuyo estado y detalle no cambian.
   - **R1, falsos negativos.** Cuando la cabecera repite el mismo año una vez por medida o por entidad, cada aparición es ahora una columna distinta y la fila se asigna por orden. El ejercicio queda acreditado, y en esas tablas era lo único que retenía las cifras de otro perímetro: las reglas de perímetro no las ven. Casos reales:
     - el impuesto por jurisdicción fiscal: «of which Ireland», «European Union (excluding France)» y «Excluding the European Union» pasan como del grupo en las seis dimensiones en 56 cifras (en C11, en 12);
     - las columnas por marca («Elis», «Le Jacquard Français», «Kennedy Hygiene»): 24 cifras pasan de PENDIENTE a OK. El autor declara que las columnas por sociedad quedan PENDIENTE;
     - en el URD 2022 p.302 la cuenta de columnas coincide por accidente y el orden queda desplazado: el valor en libros de los arrendamientos, que es la cifra legítima, queda en FALLO, y el total de flujos sin descontar, OK. Es la inversión que describía Q2, creada ahora por C12 en otra edición.
   - **R2, falsos positivos.** Un encabezado con número («NOTE 13 …») no cuenta como título. La tabla de honorarios de los auditores, que es del grupo, queda PENDIENTE en cuatro de las cinco publicaciones porque el título anterior es el último país de la lista de sociedades.
   - **R3, FALLO a cifras legítimas.** El valor en libros de cada deuda en el DEU 2024 p.323, declarado 2024, pasa de PENDIENTE a FALLO (10 cifras).
   - **R4, regresión del perímetro.** El título de tabla en caja normal («Mexico», «France») ya no cuenta, y las tablas de sensibilidad del deterioro por país pasan de PENDIENTE a OK en perímetro (429 cifras). Lo mismo, las catorce columnas por país de la tabla de combinaciones de negocio del URD 2022 p.274 (224 cifras). Ninguna queda OK en la fila: el ejercicio sigue sin acreditar.
6. **Las transiciones del barrido.** El encargo recoge una afirmación del autor: en su muestra, las transiciones nuevas a FALLO o a PENDIENTE son correcciones. En mi barrido:
   - se cumple en las 664 que pasan de OK a FALLO;
   - no se cumple en 31 de las 226 que pasan de OK a PENDIENTE (R2), ni en 11 cifras que pasan de PENDIENTE a FALLO (R1 y R3);
   - de las 767 que pasan a OK, 588 son la columna reexpresada y 68 son cifras de otro perímetro (R1) (§4.2).
7. **Ninguna conclusión material cambia.** No he encontrado ningún error en los datos reales. Las objeciones nuevas son menores (R1–R5) o de forma (R6–R8).

---

## 1. Encargo, configuración y límites de la independencia

**Encargo.** Mensaje de la sesión autora, recibido al crearse esta sesión. Lo trato como un encargo de revisión, no como una conclusión que confirmar: no doy por cierta ninguna descripción del autor sin comprobarla.

**Configuración.** Aquí no se escriben identificadores de modelo. La sesión autora puede leer la configuración de esta sesión en sus metadatos.

**Límites de la independencia:**
- **La sesión autora crea esta sesión y le encarga esta pasada. El alcance lo fija ella**, y el encargo da números de página y la lista de cosas que mirar.
- **Leo los informes de los revisores anteriores** (pasadas 1, 3, 4 y 5) y sus scripts. Esta sesión es nueva y no conserva el contexto de ninguna de ellas. Parto de sus informes, y eso también me ancla en sus conclusiones.
- **La misma herramienta de extracción puede compartir errores con el autor.** Lo he reducido donde he podido:
  - las siete filas nuevas, las entradas que contrastan con ellas y las tablas de crecimiento están leídas con pdfminer y con PDFium, no con `pdftotext`, y las siete filas, además, a la vista;
  - la lectura propia del barrido decide la columna de cada número por la posición de las palabras en puntos (pdfminer) y los títulos por la tipografía, no por la rejilla de caracteres de `pdftotext` ni por las mayúsculas;
  - las pruebas del verificador usan `pdftotext` por fuerza: es la entrada del propio verificador. Un error de extracción común a esas pruebas no se detectaría.
- **Mi lectura propia es un filtro, no una verdad.** Localiza el 97,5 % de los tokens de las páginas del grupo y se equivoca en algunas tablas sin declaración de unidades. Por eso cada clase que llevo al informe está mirada en la página y pasada por el verificador oficial como proceso aparte (`contraejemplos_6.py`). No he mirado las 122.604 candidatas una a una.
- El barrido llama a `comprobar_tabla`, la función que la ejecución oficial usa para cada fila, cargada como módulo. La equivalencia con la ejecución oficial está comprobada en las 711 y 704 filas de tabla reales de C13 y C11: ningún estado ni detalle distinto.

---

## 2. Reproducción (alcance 5)

Base 4.14 materializada desde el ZIP original de la Release (1.130.912.246 bytes, SHA-256 `bb51942c…b93e`) con `tools/base_414.py`, en un worktree de `main`: 6.798 de 6.798, `complete: true`. Libro `d2593777…92385`. Las cinco fuentes, con la huella de `fuentes.json`. Ejecución sobre una copia del worktree de 1b80b5d.

| Cifra declarada | Resultado |
|---|---|
| Manifiesto | 201 de 201 |
| CSV regenerado desde los PDF | Idéntico (SHA-256 `576b423c…da28`) |
| Verificador: 750 filas, 736 OK, 14 PENDIENTE, 0 FALLO | Reproducido. Código 2. JSON y registro idénticos. Las 71 páginas exportadas, idénticas |
| `test_verificar_cifras`: 89/89 | Reproducido. Registro idéntico. Composición: 20 OK, 10 PENDIENTE y 59 FALLO esperados |
| Contraste: 290 comprobaciones (136 del libro, 125 de fuente con 124 residuos, 29 algebraicas), 0 fallidas, 417 entradas | Reproducido. Código 0. JSON, tabla y registro idénticos |
| `test_contraste_residuos`: 22/22 | Reproducido. Registro idéntico |
| `cobertura_por_mutacion`: 528 filas, sin incoherencias | Reproducido. Salida idéntica: 384 por identidad, 2 solo libro, 23 sin detectar, 8 leídas sin efecto y 111 no usadas |
| Sondas: 711/711 en unidad y en perímetro | Reproducido. El JSON solo difiere en la etiqueta de versión que le pasé |
| Referencias de E9 sin cambios | C53 de A1, 2,445331695332; de A2, 1,612524303305. Todo `referencia_especificacion` es igual en C8, C11 y C13 |
| «Las 743 filas anteriores no cambian de estado» | Cierto: las 743 filas comunes tienen el mismo estado y el mismo detalle en las seis dimensiones en C11 y en C13 |
| Scripts del revisor n.º 5 sobre C12 (`contraejemplos_5`, `clases_5`, `barrido_tablas`, `cobertura_propia`) | Reproducidos sobre C13. Las cuatro salidas, idénticas a `resultados/revisor5_*_sobre_C12.txt` |
| Scripts de los revisores n.º 1, 3 y 4 sobre C12 | Reproducidos sobre C13. Seis salidas idénticas a `resultados/*_sobre_C12.txt`. Frente a las de C10 cambian los recuentos y las páginas sin ancla (de 13 a 8), como corresponde a las filas e identidades nuevas |

`prueba_caja_no_nula.py` y sus dos salidas no cambian desde C4 (`git diff d2e585e 1b80b5d` vacío para los tres archivos). No la he repetido. La copia del informe, de los scripts y de las salidas de la revisión n.º 5 en la rama del autor es igual a la de esta rama.

---

## 3. Estado de Q1–Q7 (alcance 1)

| Objeción | Estado | Prueba |
|---|---|---|
| Q1 · la columna «published» pasaba como edición vigente | **Corregida** | `clases_5` sobre C13: 589 de 589 en FALLO y la reexpresada, 589 de 589 en OK. Lectura propia (`clases_6.txt`, B): 591 tokens bajo una cabecera «published», «reported» o «publié» en 20 páginas; 590 en FALLO de edición y 1 que no es una cifra (el «3» de la cabecera «IFRS 3», que ya pasaba en C11). Reexpresada: 588 de PENDIENTE a OK. Casos I5 e I6. Límite declarado: la tabla del informe de gestión del URD 2022 (p.247), que imprime la cifra publicada bajo «2021 restated» |
| Q2 · la asignación por orden aceptaba la columna equivocada | **Corregida en parte** | Corregidos sus casos. En las 19 páginas de balance, toda declaración con el ejercicio de su cabecera queda OK y toda declaración con otro ejercicio, FALLO (`clases_6.txt`, G; en el URD 2021 p.228, 126 y 252; C11 daba 36 OK erróneos y 54 FALLO erróneos). I1–I4. Las tablas de vencimientos del URD 2025, del DEU 2024 y del URD 2023 quedan PENDIENTE, como dice el autor (F15, F16). Pero el método no cambia, como él mismo declara, y ese PENDIENTE depende de una cuenta de columnas: **C12 crea la misma inversión en el URD 2022 p.302** (F13, F14; R1) |
| Q3 · la marca «(a)» dejaba PENDIENTE cifras legítimas y rebajaba FALLO a PENDIENTE | **Corregida** | `clases_5`, S: 75 de 75 legítimas en OK y 75 de 75 de otro ejercicio en FALLO. En mi barrido, ninguna de las 146 que pasan de FALLO a PENDIENTE es una cifra de otro ejercicio en una tabla de dos ejercicios: son índices, prosa, planes de acciones y tablas de medidas (`clases_6.txt`, A). Efecto nuevo de la regla «el FALLO manda»: R3 |
| Q4 · el criterio de título dejaba pasar los bloques por país | **Corregida** para los bloques de pensiones, con dos efectos nuevos | Bloques «X – DETAILS» y «DÉTAIL POUR X» por lectura propia (encabezado por tipografía): 637 tokens en 19 páginas, **ninguno OK** en C13 (`clases_6.txt`, G). `clases_5`, P: 367 PENDIENTE y 9 FALLO de 376. I9. Efectos nuevos: R2 (tablas del grupo que quedan PENDIENTE) y R4 (títulos de tabla que dejan de contar) |
| Q5 · filas de segmento, de país o de UGE con rótulos fuera de las listas | **Corregida en parte** | Tablas de crecimiento: ninguna fila de segmento OK (`clases_5`, G); I10. R42 ancla las cinco tablas (§5.3). «CGU France» queda en FALLO (I11). Pero **las demás filas de la misma tabla de fondo de comercio por UGE siguen OK** en las seis dimensiones: «CGU Denmark», «CGU Sweden & Finland», «UGT Irlande»… Son 93 candidatas en las cinco publicaciones (I12–I15; `clases_6.txt`, E): R5. Las filas por jurisdicción fiscal, de la misma clase, pasan ahora más que en C11 (R1) |
| Q6 · tres frases sobre la referencia más fuertes que su prueba | **Corregida** | Las 97 entradas que mueven la referencia tienen identidad entre páginas; ninguna otra la mueve (`cobertura_6.txt`, 3, por coeficientes; `cobertura_propia` del revisor n.º 5 sobre C13). E9, respuestas y punto de recuperación, alineados. `cobertura_por_mutacion.py` informa de la clase «solo misma página»: 0 |
| Q7 · forma | **Corregida, con un resto** | (a), (c) y (e): hechas. (b): corregida en 0caa7ee, pero se repite en la versión nueva del punto de recuperación (R8). (d): la precisión está añadida, pero la frase que precisa ya no es general tras C12 (R7). (f): el motivo nombra ya la cabecera completa («Great Britain», «Latvia»); cuando hay prosa en la zona de cabecera, une palabras ajenas (F12, R8) |

---

## 4. Verificador (alcance 2)

### 4.1 Método

- **Barrido diferencial propio** (`barrido_6.py`). Cada token numérico de cada línea con rótulo de las 2.026 páginas de los cinco PDF, declarado como una cifra del grupo en millones de euros (o «%»), de dos columnas, con el ejercicio de la publicación, el anterior y el segundo anterior, y con la edición que la regla exige. Son 122.604 candidatas (40.868 tokens), 71.436 de ellas en las 459 páginas que el verificador acepta como del grupo. Cada una se evalúa con el verificador de C11 y con el de C13.
- **Lectura propia** (`geom.py`, `lectura_geometrica.py`). Para cada token de las páginas del grupo, con pdfminer: celdas de cabecera alineadas por la derecha con el número, fechas que nombran, palabras que no son fechas ni calificadores, marca «published» o «restated», título de la tabla y encabezado de bloque por tipografía. Cubre 23.211 de 23.812 tokens.
- **Clases** (`clases_6.py`) y **contraejemplos** con el verificador oficial como proceso aparte (`contraejemplos_6.py`).

### 4.2 Transiciones entre C11 y C13 (páginas del grupo, estado de la fila)

| Transición | Candidatas | Lectura [D] |
|---|---|---|
| OK → FALLO | 664 | 595 por edición: 590 de la columna publicada y 5 de la columna de ajuste. 42 por ejercicio: 36 del balance del URD 2021, 4 del plan de acciones de empleados del URD 2025 p.362 y 2 de las hipótesis de pensiones de Francia del URD 2023 p.308; en las 42 la cifra es del otro ejercicio [P]. 27 por perímetro: filas de segmento, de país o «CGU France». **Todas son correcciones** |
| OK → PENDIENTE | 226 | 171, bloques de pensiones de un país: correcciones. 24 por ejercicio: prosa, cabeceras «IFRS 3», tablas de medidas y totales de vencimientos; ahí PENDIENTE es razonable. **31, honorarios de auditores: cifras legítimas del grupo (R2)** |
| PENDIENTE → FALLO | 3.420 | 1.736, cabecera de otro ejercicio: correcciones. El resto, columnas de medida, de plan o de vencimiento, prosa e índices. **Entre ellas, al menos 11 cifras legítimas del cierre (R1 y R3)** |
| FALLO → PENDIENTE | 146 | Índices, prosa, planes de acciones y tablas de medidas. Ninguna es una cifra de otro ejercicio en una tabla de dos ejercicios |
| No OK → OK | 767 | 588, columna reexpresada de las tablas de reexpresión: correcciones. **Otras 179** (`clases_6.txt`, D): 62 de los estados del URD 2021 (correcciones de Q2 y Q3); 4 del total del grupo del DEU 2024 p.321; 19 aceptaciones correctas en tablas con el año repetido (la fila TOTAL del impuesto por jurisdicción y los honorarios por firma auditora); **68 cifras de otro perímetro (R1)**; 16 de planes de acciones bajo «2022 plan» y similares, y 10 sueltas (prosa y líneas de unidades), que no he clasificado más |
| OK → OK | 4.882 | — |

OK en las seis dimensiones: 5.772 en C11 y 5.649 en C13. La dimensión de unidad no cambia en ninguna candidata. Los motivos de las 664 y de las 226 están en `consultas_6.txt`, 1; las 6 que pasan a FALLO por ejercicio fuera del balance del URD 2021 y las 24 que pasan a PENDIENTE por ejercicio, una a una, en `consultas_6.txt`, 2.

### 4.3 Por regla

**Columnas distintas para el mismo año y línea más cercana.**
- *Lo que corrige.* Las tablas de reexpresión (Q1), el balance del URD 2021 (Q2) y, por la regla de la línea más cercana, la sensibilidad de las pensiones: en el URD 2023 p.309–311, el URD 2025 p.357–359 y el DEU 2024 p.303–305, la tabla lleva su propia cabecera («12/31/2023») alineada con la columna del año anterior de la tabla de arriba. C11 aceptaba 2022 y rechazaba 2023; C13, al revés, que es lo correcto [P] (I7, I8).
- *Efecto nuevo: más tablas se asignan por orden.* Con una columna por aparición del año, la cuenta de columnas iguala a la de números en las tablas que repiten el año por medida o por entidad. En el impuesto por jurisdicción, las marcas y los honorarios por firma, el orden da el ejercicio correcto [P]. Pero la rama por orden no mira las demás palabras de la cabecera, que era la protección de C9 para las columnas por sociedad, y en esas tablas el ejercicio sin acreditar era lo único que retenía las cifras de otro perímetro: R1.
- *Falso FALLO nuevo.* Cuando la cuenta coincide por accidente, el orden queda desplazado: URD 2022 p.302 (R1, F13 y F14).

**Apertura «01/01/AAAA» como ejercicio anterior.** La única columna de apertura de las páginas del grupo es la del balance del URD 2021 p.228 (42 tokens). Declarada 2020, FALLO (42 de 42); declarada 2019, el ejercicio queda OK y la edición falla siempre, porque ninguna fuente presenta 2019. Sin objeción. Observación [I]: la columna es «01/01/2020 Adjusted (a)», un saldo de apertura ajustado, que no es el cierre publicado de 2019.

**`edicion_de_columna`.** Sin falsos positivos en cifras legítimas: las 588 de la columna reexpresada quedan OK. La regla marca también 97 candidatas de la columna de ajuste («IFRS 3») con el motivo «la columna es la publicada»: no son cifras de un ejercicio, pero el motivo es inexacto (R8).

**Celdas y calificadores de cabecera.** Sin objeción. Las cabeceras «restated (a)», «Restated (a)» y «Adjusted (a)» ya no dejan PENDIENTE las cifras legítimas.

**El FALLO que manda sobre la cabecera ajena.** Restaura el FALLO de las cifras de otro ejercicio (Q3). Pero da FALLO a cifras legítimas del cierre que están bajo una cabecera de medida y junto a columnas de años futuros: R3.

**`titulo_de_pais_encima_v2`.**
- *Lo que corrige.* Los bloques de pensiones, también con el título en la página anterior.
- *Falsos positivos nuevos.* `es_titulo` excluye las líneas con cifras y las que no van en mayúsculas, así que un encabezado numerado no corta la búsqueda: R2.
- *Regresión.* Solo cuenta el título en mayúsculas. El título de tabla en caja normal que C10 sí veía deja de contar: R4.

**`normalizar_rotulo` y `rotulo_completo`.** Sin falsos positivos: las 51 cifras que pasan a FALLO de perímetro por estas reglas son filas de segmento o de país [P]. Resto: R5. Detalle sin caso real: `segmento_de_sublinea` cuenta las filas de segmento con el rótulo normalizado, pero atribuye la sublínea con el rótulo sin normalizar (línea 843). En las cinco tablas de EBITDA por segmento los rótulos llevan «&»: las sublíneas de los seis segmentos quedan en FALLO y solo queda OK la del total [P][D] (`consultas_6.txt`, 5).

### 4.4 Las cuatro clases que nombra el encargo (`clases_6.txt`, G)

| Clase | Tokens y páginas | Resultado en C13 |
|---|---|---|
| Pensiones por país | 637 en 19 | Ninguna candidata OK. Perímetro: 227 de OK a PENDIENTE; 410 ya estaban PENDIENTE |
| Balances | 1.923 en 19 | Con el ejercicio de su cabecera, OK; con otro, FALLO. Sin excepción |
| Sensibilidad del deterioro por país, UGE o marca | 565 en 14 | Perímetro: 465 de PENDIENTE a OK (R4). 27 candidatas OK en las seis dimensiones: las tablas por marca (R1) |
| Listas de sociedades por país | 1.952 en 30 | Ninguna candidata OK. Perímetro: 1.813 de OK a PENDIENTE. La tabla que sigue a la lista, la de honorarios de auditores, queda PENDIENTE (R2) |

---

## 5. Contraste (alcance 3)

Prueba: `lectura_filas_c12.py` → `resultados_revisor_6/lectura_filas_c12.txt`. 25 lecturas con pdfminer y con PDFium, ninguna diferencia. Las siete filas, además, vistas en la página renderizada.

### 5.1 Las siete filas nuevas

| Fila | Página PDF (folio) | Línea y columna [P] | Ej. | Unidad y perímetro [P] | Veredicto |
|---|---|---|---|---|---|
| `BAI_NOTA9_U22_2021` | URD 2022 p.326 (324) | «Income (loss) before tax 285.1 · 171.0», columna «12/31/2021» | 2021 | «(In millions of euros)»; nota 9 de los estados consolidados | Correcta |
| `BAI_NOTA9_U23_2022` | URD 2023 p.345 (343) | «INCOME (LOSS) BEFORE TAX 372.9 · 282.3», columna «2022 restated*» | 2022 | ídem | Correcta |
| `CF_DAP_U22_2021` | URD 2022 p.261 (259) | «Depreciation, amortization and provisions 4.5 · 790.8 · 745.7», columna «12/31/2021 restated (a)» | 2021 | «(in million of euros)»; estado de flujos consolidado | Correcta |
| `PROV_TOT_U22_2021` | URD 2022 p.284 (282) | «TOTAL ADDITIONS TO OR REVERSALS OF PROVISIONS 6.1 · (0.3)», columna «12/31/2021» | 2021 | «(In millions of euros)»; nota 4.5 | Correcta |
| `CF_DAP_U23_2022` | URD 2023 p.279 (277) | «Depreciation, amortization and provisions 4.5 · 885.3 · 793.6», columna «2022 restated*» | 2022 | «(In millions of euros)»; estado de flujos consolidado | Correcta |
| `PROV_TOT_U23_2022` | URD 2023 p.301 (299) | «TOTAL ADDITIONS TO OR REVERSALS OF PROVISIONS (8.1) · 6.1», columna «2022 restated*» | 2022 | «(In millions of euros)»; nota 4.5 | Correcta |
| `DN_ADQ_FR_2023` | DEU 2024 p.260 (258) | «Acquisitions de filiales, sous déduction de la trésorerie acquise (183,3) · (82,1)», columna «2023 retraité*» | 2023 | «(en millions d'euros)»; «Résultats du Groupe», tabla del endeudamiento financiero neto | Correcta |

Edición: las siete son la publicación vigente para su ejercicio según la regla de la Historia [D].

Observaciones:
- En el URD 2022, las notas 9 y 4.5 rotulan la columna comparativa «12/31/2021», sin «restated»; los estados principales, «12/31/2021 restated (a)» [P]. Las cifras de las notas son las reexpresadas: cuadran con los estados reexpresados con residuo 0,0 [D].
- El puente de la deuda neta del DEU 2024 imprime la cifra reexpresada, (82,1), bajo «2023 retraité*» [P]. No repite el caso del informe de gestión del URD 2022 (p.247), que imprimía la publicada bajo «2021 restated».

### 5.2 Identidades

| Identidad | Cálculo [D] | Residuo | Cota |
|---|---|---|---|
| R41 2021 | 171,0 (p.258) − 171,0 (p.326) | 0,0 | 0,10 |
| R41 2022 | 282,3 (p.276) − 282,3 (p.345) | 0,0 | 0,10 |
| R8 2021 | 745,7 (p.261) − (744,8 + 0,6 + 0,3) (p.284) | 0,0 | 0,20 |
| R8 2022 | 793,6 (p.279) − (799,0 + 0,7 − 6,1) (p.301) | 0,0 | 0,20 |
| R24 2023 | 82,1 (p.273) − 82,1 (p.260) | 0,0 | 0,10 |

- **R41** es una reproducción de la línea de la cuenta de resultados en la tabla de la nota 9, como R21 en 2023–25. Vale como segunda página con su propia cabecera y su propia declaración de unidades [I].
- **R8.** El signo es coherente: en la nota, las dotaciones netas van con el signo del resultado ((0,3), cargo; 6,1, reversión) [P]. La misma identidad cierra con la columna de 2022 del propio URD 2022: 796,2 + 0,7 − 6,1 = 790,8, que es la línea del EFE [P][D]. Es una identidad de la publicación, no una coincidencia.
- **R24.** Las dos cifras son la reexpresada [P].

### 5.3 R42

| Ejercicio | Ventas / ventas del año anterior | Publicado | Residuo | Cota linealizada | Cota exacta (peor caso) |
|---|---|---|---|---|---|
| 2021 | 3.048,3 / 2.806,3 → 8,6235 % | 8,6 % | −0,0235 | 0,053717 | 0,053717 |
| 2022 | 3.820,9 / 3.048,3 → 25,3453 % | 25,3 % | −0,0453 | 0,053696 | 0,053696 |
| 2023 | 4.309,4 / 3.820,9 → 12,7849 % | 12,8 % | +0,0151 | 0,052784 | 0,052785 |
| 2024 | 4.573,7 / 4.309,4 → 6,1331 % | 6,1 % | −0,0331 | 0,052392 | 0,052392 |
| 2025 | 4.796,8 / 4.573,7 → 4,8779 % | 4,9 % | +0,0221 | 0,052240 | 0,052240 |

- **¿Es correcta la linealización?** Sí [D]. Las derivadas son las del código: 1 respecto al publicado, −100/V₋₁ respecto a las ventas y 100·V/V₋₁² respecto a las del año anterior. La cota exacta, con las tres cifras en su extremo de redondeo, difiere de la linealizada en menos de 7·10⁻⁸. El autor declara menos de 10⁻⁶.
- **¿Es adecuada la cota?** Sí [D][I]. Es el error máximo de redondeo de las tres cifras impresas, si el crecimiento publicado se calcula con las ventas sin redondear. Es estrecha: un cambio de una décima en el crecimiento publicado se detecta los cinco años, en los dos sentidos (el umbral va de 0,008 a 0,099 puntos).
- **¿Ancla las tablas de crecimiento?** Sí [P][D]. Ninguna de las 35 filas de segmento de las cinco tablas cerraría R42: la más próxima es «Royaume-Uni et Irlande» en 2024, con 6,6 % frente a 6,133 %, a 0,47 puntos de una cota de 0,052.
- **Mezcla de ediciones.** R42 compara el crecimiento de la publicación de cada ejercicio con las ventas de la edición vigente, que es la siguiente. Cierra porque las ventas no se reexpresaron de 2021 a 2024 [P: 3.048,3, 3.820,9, 4.309,4 y 4.573,7 en las cuentas de resultados de las dos ediciones]. Si un año se reexpresaran, R42 fallaría sin error en los datos [I].
- **¿Es cierto el límite de sensibilidad que declara el autor?** Sí; el caso que da no es el único: R6.

---

## 6. Cobertura (alcance 4)

Prueba: `cobertura_6.py` → `resultados_revisor_6/cobertura_6.txt`. Una ejecución del contraste del autor por entrada usada, con la entrada aumentada en 1 y el verificador saltado. De ahí sale el coeficiente de cada entrada en cada identidad y, con el residuo y la cota, el menor error de cada signo que la hace fallar.

| Declarado por el autor | Derivación propia | ¿Coincide? |
|---|---|---|
| 244 con identidad entre páginas | 244, entrada por entrada (coeficiente no nulo en alguna identidad entre páginas) | Sí |
| 140 solo de su página · 2 solo con la Historia · 31 sin segunda línea | 140 · 2 · 31 | Sí |
| 8 de 53 páginas sin identidad entre páginas, con 24 entradas, 9 de ellas con solo identidad de su página | 8, 24 y 9 | Sí |
| Las 97 entradas que mueven la referencia tienen identidad entre páginas | 97 de 97 | Sí |
| Ninguna otra la mueve | 0 de las 140, 0 de las 2 y 0 de las 31 | Sí |

**¿Hay entradas cuya unidad o perímetro se presenten como acreditados sin serlo?** En los recuentos, no. Dos matices (R6):

- **La clase es por pertenencia, no por sensibilidad.** Umbral garantizado de las 244, en unidades de la última cifra impresa: 141, hasta 2; 99, de 2 a 5; 3, de 5 a 10; 1, más de 10. Las cuatro últimas:
  - `IS_VENTAS_U23_2022` (3.820,9): entre −2,30 y +0,26 no falla ninguna identidad entre páginas;
  - `IS_VENTAS_U22_2021` (3.048,3): entre −0,20 y +0,85;
  - `FCF_ANTES_2024` y `CF_IMPPAG_2024`: entre −0,55 y +0,15, por R11 de 2024.

  Las dos ventas pasan en C12 de «solo Historia» a «entre páginas» sin más identidad que R42. Las cuatro tienen otra comprobación exacta (la Historia o una identidad de su página) y **ninguna mueve la referencia**.
- **Las 97 que mueven la referencia** están mejor cubiertas: 46 se detectan desde 2 unidades de la última cifra y 51 entre 2 y 5 (como máximo ±0,5, en las líneas del circulante por R5).
- **Por tabla, no por página.** Si la tabla de una entrada es la declaración de unidades más próxima por encima de su línea, hay 60 tablas y 9 sin ninguna entrada contrastada entre páginas, con 26 entradas. La diferencia con las 8 páginas y 24 entradas del autor es una tabla del DEU 2024 p.296 con `OOIE_EARN_FR_2023` y `OOIE_PLUSV_FR_2023`, que ya están declaradas sin segunda línea. No cambia nada.

Tres de las ocho páginas sin identidad entre páginas (URD 2023 p.346, DEU 2024 p.338 y URD 2025 p.393) contienen la tabla de impuesto por jurisdicción de R1. Las entradas reales de esas páginas (`TAXDIF_*`) están en otra tabla, la de impuestos diferidos, y no cambian [P].

---

## 7. Objeciones nuevas

Todas las filas existen en el PDF [P]. Ninguna afecta a una fila real del CSV.

### R1 · menor · `verificar_cifras.py`, ejercicio y perímetro (C12) · con el año repetido en la cabecera la fila se asigna por orden: cifras de otro perímetro pasan como del grupo, y en un caso el orden está desplazado

- **Qué ocurre** [D]. Desde C12 cada aparición del mismo año es una columna (`columnas_de_cabecera`). En las tablas que repiten el año una vez por medida o por entidad, la cuenta de columnas reconocidas iguala ahora a la de números de la línea, y `columna_de_token` asigna por orden. En C11 daban dos columnas para seis números (URD 2025 p.393 y p.371, DEU 2024 p.338), se asignaba por alineación y el ejercicio quedaba sin acreditar. La rama por orden no comprueba la alineación ni mira las demás palabras de la cabecera: la regla de C9 para un país, una sociedad o un ajuste solo actúa en la rama por alineación. En el URD 2023 p.346, con tres números y dos columnas, se sigue asignando por alineación; lo que cambia es que hay una segunda columna «2023».
- **Prueba.** `contraejemplos_6.txt`, F1–F19; `clases_6.txt`, D, D2 y E; `consultas_6.txt`, 3 y 4 (columnas reconocidas en cada versión).
  - *Impuesto por jurisdicción fiscal* (URD 2025 p.393, DEU 2024 p.338, URD 2023 p.346). Cabecera: «Income (loss) before tax 2025 · Tax recognized 2025 · Average effective tax rate 2025 · … 2024 · … 2024 · … 2024». El orden da el ejercicio correcto [P]. Pero las filas «European Union (excluding France)», «of which Ireland», «Non-cooperative jurisdictions…» y «Excluding the European Union» son un desglose por jurisdicción, y las reglas de perímetro no las reconocen. Declaradas del grupo:

    | Publicación | OK en las seis dimensiones en C11 | En C13 |
    |---|---|---|
    | DEU 2024 p.338 | 0 | 24 |
    | URD 2025 p.393 | 8 | 24 |
    | URD 2023 p.346 | 4 | 8 |

    Ejemplos: «dont Irlande 8,2», resultado antes de impuestos de Irlanda de 2024 (F4); «› of which Ireland 1.8», impuesto de Irlanda de 2025 (F1). La fila «France» sí falla (F8). El TOTAL, que es del grupo, queda OK, y es correcto (F7).
  - *Columnas por marca* (URD 2025 p.371, DEU 2024 p.317). «Elis · Le Jacquard Français · Kennedy Hygiene», cada una con dos fechas. El orden da el ejercicio correcto [P]; la columna es de una marca, no del grupo. Las 18 cifras del URD 2025 pasan de PENDIENTE a OK (F9, F10). En el DEU 2024, las 6 de Kennedy Hygiene quedan OK; las de las otras dos marcas, en FALLO de perímetro con un motivo que une palabras de prosa (F11, F12; R8).
  - *Vencimientos de arrendamientos del URD 2022 p.302.* Cabecera: «Carrying value · Cash flow 2023 · Cash flow 2024 · Cash flow 2025-2026-2027 · Cash flow 2028 and beyond · Estimate of future cash flows as at 12/31/2022». En C13 las columnas reconocidas son seis (2023, 2024, 2025, 2027, 2028 y 2022: «2026» se funde con «2025» por estar a menos de seis caracteres), tantas como números; en C11 eran siete. El orden asigna cada número a la cabecera siguiente: el valor en libros, 485,5, declarado 2022, queda en **FALLO** («la columna es de 2023»), y el total, 612,1, queda **OK** («columna de 2022 (orden con la cabecera)») (F13, F14). En C11, los dos PENDIENTE.
  - *La corrección de Q2 en las demás ediciones depende de la misma cuenta.* En el URD 2025 p.366, C11 reconocía seis columnas para seis números (la inversión de Q2) y C13 reconoce cinco, por la misma fusión: por eso quedan PENDIENTE (F15, F16).
  - *Honorarios por firma auditora* (URD 2025 p.402; F17, F18): el orden da el ejercicio correcto y la cifra es del grupo. La aceptación es correcta; la cito porque el mecanismo es el mismo. *Una línea de prosa* (URD 2023 p.261 l.22) queda OK: F19.
- **Por qué importa.**
  - Son 68 cifras de otro perímetro que pasan de PENDIENTE a OK en las seis dimensiones: 44 de jurisdicción y 24 de marca. C11 las retenía solo porque no acreditaba el ejercicio.
  - Tres de las páginas son de las ocho en las que, según el informe, la unidad y el perímetro descansan en el verificador.
  - Dos frases del autor dejan de ser generales: «columnas por sociedad: PENDIENTE» y «en las tablas de vencimientos las dos quedan PENDIENTE» (R7).
  - T14 pide al frente técnico las mismas reglas, entre ellas «dos fechas del mismo año».
- **Corrección propuesta.**
  - Ejercicio: al asignar por orden, comprobar que cada número está alineado con la cabecera que se le asigna; si no, PENDIENTE. Y aplicar también en esa rama la regla de C9: si encima de la fecha de la columna hay un nombre que no es una columna reconocida ni un calificador («Kennedy Hygiene»), el ejercicio queda sin acreditar.
  - Perímetro: una fila cuyo rótulo nombra un país, una región o una jurisdicción tras «of which», «dont», «excluding» u «hors» no es del grupo (la clase de R5).
  - Añadir F1, F4, F9, F13 y F14 al test y a T14.

### R2 · menor · `verificar_cifras.py`, perímetro (C12) · una tabla del grupo que sigue a un bloque de país queda PENDIENTE si su encabezado lleva número

- **Prueba.** `contraejemplos_6.txt`, G1–G5 y G9; `clases_6.txt`, C.
  - *Honorarios de los auditores (nota 13)*, tras la lista de sociedades: URD 2021 p.298, URD 2022 p.336, URD 2023 p.355 y DEU 2024 p.347. 164 tokens pasan de perímetro OK a PENDIENTE; el título que ve el verificador es «SWITZERLAND», «SWEDEN» o «SUISSE». 31 candidatas que eran OK en las seis dimensiones quedan PENDIENTE; por ejemplo, el total de honorarios de Mazars de 2022, 0,7 (G2), y el de 2024, 0,8 (G4).
  - En el URD 2025 p.402 no ocurre: el encabezado ocupa dos líneas y la segunda, «THE FINANCIAL STATEMENTS», no lleva cifras (G5).
  - *Planes de acciones (nota 5.4)*, tras el bloque «SWITZERLAND – DETAILS»: URD 2023 p.312, URD 2025 p.360 y DEU 2024 p.306, 353 tokens (G9). No son importes en millones, pero el motivo es ajeno a la tabla.
- **Causa** [D]. `es_titulo` descarta toda línea con cifras y toda línea que no vaya en mayúsculas. «NOTE 13 STATUTORY AUDITORS' FEES» lleva un número; «5.4 Share-based payments» lleva un número y va en caja normal. Ninguna cuenta, y la búsqueda sigue hacia arriba, hasta el principio de la página y la página anterior.
- **Por qué importa.** Estas 31 transiciones a PENDIENTE no son correcciones. PENDIENTE no es FALLO, pero el contraste termina con código 2 si usa una fila así.
- **Corrección propuesta.** Tratar como título, y como final de la búsqueda, una línea que empieza por una numeración de nota o de apartado («NOTE 13 …», «5.4 …»), vaya o no en mayúsculas. Añadir G2 y G4 al test como positivos, y a T14.

### R3 · menor · `verificar_cifras.py`, ejercicio (C12) · «el FALLO manda» da FALLO a cifras legítimas del cierre bajo una cabecera de medida

- **Prueba.** `contraejemplos_6.txt`, G6–G8; `clases_6.txt`, F; `consultas_6.txt`, 4. DEU 2024 p.323, vencimientos de la deuda: la primera columna es «Valeur comptable / Coût amorti» a 31-12-2024 y las siguientes, «Flux de trésorerie 2025», «2026»… Las 10 cifras de valor en libros (354,6 de las convertibles, 705,8 del USPP…), declaradas 2024, pasan de PENDIENTE a FALLO: «la columna reconocida más próxima es de 2025». En la misma tabla de las otras cuatro publicaciones siguen PENDIENTE (G8).
- **Causa** [D]. La regla nueva da FALLO si la columna reconocida más próxima es de otro ejercicio, aunque el token esté bajo una cabecera ajena. Aquí la cabecera ajena es la de la cifra, y el año más próximo es el de la columna vecina.
- **Por qué importa.** `contraste_f1.py` se niega a calcular con un FALLO. Para estas cifras, C12 convierte un «no sé» en un rechazo equivocado. En mi barrido hay 527 tokens que en C13 fallan con los tres ejercicios y en C11 no; casi todos son columnas de vencimiento o de plan, y 11 son cifras del cierre (estas 10 y el valor en libros de R1).
- **Corrección propuesta.** Mantener el FALLO solo si la columna de otro ejercicio está alineada con el token (por ejemplo, a 3 caracteres o menos); si no, PENDIENTE. Añadir G6 al test, con PENDIENTE esperado.

### R4 · menor · `verificar_cifras.py`, perímetro (C12) · el título de tabla en caja normal y las columnas por país sin columna de fecha dejan de detectarse

- **Prueba.** `contraejemplos_6.txt`, H1–H5; `clases_6.txt`, C y G.
  - *Sensibilidad del deterioro por UGE* (URD 2021 p.271–272, URD 2022 p.304–305, URD 2023 p.323–324, DEU 2024 p.316–317, URD 2025 p.370–371). Cada tabla lleva encima el nombre de su país: «France», «Germany», «Mexico»… 429 tokens pasan de perímetro PENDIENTE (C11) a OK (C13), y otros 5 de una tabla «Mexico» que mi lectura no clasifica. Lo mismo, «Interest rate swap – Chile» (URD 2021 p.288; 7 tokens).
  - *Combinaciones de negocio del URD 2022 p.274.* Catorce columnas por país («Germany · Brazil · Chile…») y una primera columna con el total. Los 224 tokens pasan de perímetro PENDIENTE a OK, también los de la columna de Alemania (H2).
  - En todas la fila sigue PENDIENTE, porque el ejercicio no se acredita.
- **Causa** [D].
  - El título debe ir en mayúsculas; «Mexico» no va. El criterio de C10 (`titulo_de_pais_encima`) tomaba la primera línea corta sin cifras por encima de la tabla.
  - Lo que queda en la línea de unidades solo cuenta si es un único país.
  - `pais_de_columna` necesita alguna columna reconocida (una fecha, «Total») para saber dónde empiezan las columnas; en la p.274 no hay ninguna.
- **Frases más fuertes que la prueba.** Respuestas, Q4: en las tablas de combinaciones de negocio «ahora decide la regla de las columnas por país». En la del URD 2022 p.274 esa regla no actúa. T14 e informe §1 describen el criterio nuevo, pero no dicen que el de C10 deja de aplicarse a los títulos de tabla.
- **Corrección propuesta.** Conservar el criterio de C10 junto al nuevo: una línea corta, sin cifras, pegada encima de la cabecera de la tabla y que nombra un país deja el perímetro PENDIENTE. Con tres países o más en la cabecera y ninguna columna reconocida, PENDIENTE. Añadir H1 y H2 al test y a T14.

### R5 · menor · `verificar_cifras.py`, perímetro (Q5, resto) · en la tabla de fondo de comercio por UGE solo falla «CGU France»

- **Prueba.** `contraejemplos_6.txt`, I11–I15; `clases_6.txt`, E. La tabla de la nota 6.1 da el fondo de comercio de cada UGE. «CGU France» queda en FALLO desde C12. Las demás filas, declaradas del grupo, quedan OK en las seis dimensiones en C11 y en C13:

  | Publicación | Candidatas OK | Ejemplo |
  |---|---|---|
  | URD 2025 p.363 | 24 | «CGU Denmark 412.2» |
  | DEU 2024 p.309 | 24 | «UGT Irlande 76,1» |
  | URD 2023 p.316 | 16 | «CGU Great Britain» |
  | URD 2022 p.298 | 15 | «CGU Mexico» |
  | URD 2021 p.265 | 14 | «CGU United Kingdom 101.4» |

- **Causa** [D]. El prefijo «CGU» o «UGT» se quita para comparar con la lista de segmentos, y «France» es un segmento. `tabla_por_paises` compara el rótulo sin normalizar con la lista de países, y «CGU Denmark» no empieza por un país.
- **Por qué importa.** Q5 citaba esta tabla (caso E15). La respuesta corrige el caso citado, no la tabla.
- **Corrección propuesta.** Aplicar `normalizar_rotulo` también antes de comparar con la lista de países, o tratar como tabla por UGE la que tiene tres filas o más con ese prefijo. Añadir I12 e I14 al test.

### R6 · forma · informe §0 y §2, respuestas (Q5), `cobertura_entradas` · la clase «entre páginas» es por pertenencia, y el caso que ilustra el límite de R42 no es el único

- **Qué dice el material.**
  - `que_acredita_cada_clase`: una identidad entre páginas acredita «el número y, de forma indirecta, su unidad y su perímetro».
  - Informe §2: «un +3 en las ventas del año anterior mueve el crecimiento unos 0,07 puntos, y en 2024 eso no supera la cota». Las respuestas dicen lo mismo. «Lo que queda abierto tras C12» declara el límite en general: «R42 frente a las ventas».
- **Prueba.** `cobertura_6.txt`, 2 y 3; `lectura_filas_c12.txt`, R42.
  - Cierto: en 2024, +3,0 en las ventas de 2023 lleva el residuo de −0,0331 a +0,0408, dentro de 0,0524.
  - No es el único caso de ±3,0 que R42 no detecta [D]: −3,0 en las ventas del propio año en 2022 y en 2024; +3,0 en las del propio año en 2025 (de +0,0221 a −0,0435), y −3,0 en las del año anterior en 2025. En general, R42 solo detecta un error en unas ventas desde 0,2 a 3,7 millones, según el año y el signo.
  - Las ventas de 2021 y de 2022 no tienen más identidad entre páginas que R42 (§6). Para ellas, «acredita el número» es más fuerte que la prueba: R42 las fija dentro de un intervalo de 1,05 y de 2,55 millones.
- **Atenuantes** [D]. Las dos coinciden con la Historia del libro y ninguna mueve la referencia. Las ventas de 2020, 2023, 2024 y 2025 tienen R40 o R23.
- **Corrección propuesta.**
  - Decir en `que_acredita_cada_clase` y en §0.2 que la clase es por pertenencia, y dar el umbral de detección de las entradas cuya única identidad entre páginas es R42.
  - Sustituir el caso de 2024 por el intervalo de cada año.
  - Una identidad lineal para las ventas de 2021 y 2022 (la información por segmentos del URD 2022 y del URD 2023) las dejaría como a las de 2023–25.

### R7 · forma · informe §1, respuestas (C9, Q2, Q4) y T14 · frases más fuertes que su prueba

- (a) **Informe §1, límites:** «En tablas con varias medidas bajo una misma fecha (valor en libros y valor razonable), de vencimientos o de movimientos, una fila declarada como de dos ejercicios queda PENDIENTE». Vale para los casos del test; no es general:
  - en la tabla de instrumentos financieros (URD 2023 p.338 y sus equivalentes), la columna que queda bajo la fecha, el valor en libros, se acepta, y con razón [P]; las demás quedan PENDIENTE. Ya era así en C11;
  - en la de vencimientos de la deuda del DEU 2024 p.323 el resultado es FALLO (R3);
  - en la de vencimientos de arrendamientos del URD 2022 p.302, un OK y un FALLO (R1).
- (b) **Respuestas, Q2:** «en las tablas de vencimientos (B17 y B18) las dos quedan PENDIENTE». Cierto para B17 y B18; no para el URD 2022 p.302 (R1).
- (c) **Respuestas, C9, «Límite que queda»**, precisado en C12: las columnas por sociedad «quedan PENDIENTE en ejercicio». El caso del test del autor, una sociedad adquirida (URD 2023 p.294), sigue PENDIENTE. Las columnas por marca, que son de la misma clase —una columna por entidad—, quedan OK tras C12 (R1). La misma frase está en «Lo que queda abierto tras C12» y en el punto de recuperación.
- (d) **Respuestas, Q4:** «Ahora decide la regla de las columnas por país» (R4).
- (e) **Punto de recuperación:** «Q1–Q6 corregidas en sus casos». Es exacto, y es lo que las pruebas del autor cubren: los casos del revisor n.º 5. Las transiciones a OK fuera de esos casos no se miran, y ahí están las de R1.
- (f) **T14** incluye «dos fechas del mismo año» entre lo que el frente técnico debe implementar, sin el límite de R1.
- **Corrección propuesta.** Acotar cada frase a lo que su prueba cubre y nombrar R1–R5 en «Lo que queda abierto» y en T14.

### R8 · forma · varios

- (a) `PUNTO_DE_RECUPERACION.md`: «hacia las 00:15 UTC». El commit que lo contiene, C12, es de las 00:11:29 UTC. Es la observación de Q7 (b), en la versión nueva.
- (b) El motivo de la regla de edición dice «la columna es la publicada» también para 97 candidatas de la columna de ajuste («IFRS 3»).
- (c) El motivo de `pais_de_columna` une palabras de prosa de la zona de cabecera: «la columna es la de «plus scénario et élaboré grands les amorties non de des tests Elis 31/12/2024»» (F12). Esa regla da FALLO de perímetro a la marca Elis y deja OK a Kennedy Hygiene en la misma línea.
- (d) `segmento_de_sublinea` cuenta con el rótulo normalizado y atribuye con el rótulo sin normalizar (§4.3). Sin caso real.

---

## 8. Coherencia entre documentos (alcance 6)

He leído la quinta parte de las respuestas, el informe (§0, §1, §2, §12 y §13), la especificación (E9, T12 y T14), el README, `ESTADO.md`, `REGISTRO_CONFIGURACION.md` y `PUNTO_DE_RECUPERACION.md`.

- **Recuentos.** Coinciden entre sí y con las salidas: 750 = 711 + 39; 736, 14 y 0; 89 = 20 + 10 + 59; 290 = 136 + 125 + 29; 124 residuos; 417 = 244 + 140 + 2 + 31; 8 de 53 páginas, 24 entradas y 9; 22 casos; 528 = 384 + 2 + 23 + 8 + 111; 409 con efecto; 711/711; 97. No queda ningún recuento de C11 en los documentos principales, salvo donde se cita como historia.
- **Hashes y alcance.** C12 y C13, bien registrados. El congelado solo añade el hash.
- **Estado y registro.** Describen bien la pasada 5 y C12, y dejan esta pasada pendiente.
- **Reproducción (§13).** Los comandos funcionan tal como están escritos.
- **Afirmaciones más fuertes que su prueba:** las de R4, R6 y R7. No encuentro otras en lo leído.
- **Afirmaciones comprobadas y ciertas:** «las 743 anteriores no cambian de estado»; «ninguna fila de segmento queda OK» en las tablas de crecimiento; «ninguna cifra en millones queda OK» en los bloques de pensiones; «las 97 entradas que mueven la referencia tienen identidad entre páginas»; los residuos y las cotas de R42 y su error de segundo orden.

---

## 9. Conclusiones materiales y lo no comprobado

**Conclusiones materiales.** Ninguna cambia: la conciliación y el FCF base, C48 = 108, el doble cómputo del arrendamiento bajo su premisa, los intangibles adquiridos pendientes de política, la reinversión necesaria no publicada como importe y `pendiente_de_datos`. Las decisiones económicas siguen pendientes de la persona responsable.

**Sobre el verificador** [I]. R1–R4 son efectos de las correcciones de C12, como Q3 lo fue de la de C9. Las reglas son heurísticas sobre la rejilla de caracteres, y el autor lo declara. Dos de los resultados de esta pasada dependen de una cuenta: que el número de columnas reconocidas iguale o no al de números de la línea decide entre asignar por orden o por alineación, y esa cuenta cambia con detalles como la separación entre dos años. Lo que sostiene las cifras reales no es el verificador solo, sino la segunda línea: las identidades entre páginas y la Historia. Eso no ha cambiado. Para las entradas sin segunda línea y las de las ocho páginas sin ancla sigue valiendo lo que dice el informe: cobertura pendiente.

**No comprobado en esta pasada:**
- Lo que no cambia entre C11 y C13, salvo lo que hizo falta para reproducir.
- Los §3 a §11 del informe y el resto de la especificación: no cambian en el alcance.
- La prueba de caja no nula con LibreOffice: no cambia desde C4 y no la he repetido.
- Las candidatas del barrido una a una: he revisado las clases, sus páginas y un ejemplo de cada una con el verificador oficial.
- El 2,5 % de los tokens de las páginas del grupo que mi lectura no localiza, y las páginas que no son del grupo, de las que solo he mirado las transiciones.
- Clases de error que mis filtros no señalan. El barrido no es exhaustivo: declara cada token solo como cifra del grupo de dos columnas.
- Las reglas V-F1a a V-F1h y T8 y T14: especificadas, no implementadas.
- El árbol del hito 4.15 y la rama del frente técnico.

---

## 10. Reproducción de esta revisión

```bash
B=docs/validacion_economica_paralela/frente_E_F1_elis
C11=<worktree de 364129a>/$B ; C13=<worktree de 1b80b5d>/$B
RAIZ=<ruta>/munger_v2_r1
LIBRO=$RAIZ/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx
cd revision/scripts_revisor_6
python3 -I lectura_filas_c12.py --raiz "$RAIZ" --autor "$C13"                                  # pdfminer y pypdfium2
python3 -I barrido_6.py --raiz "$RAIZ" --anterior C11="$C11" --nueva C13="$C13" --todas /tmp/b6/todas.jsonl.gz --salida ../resultados_revisor_6/barrido_6.txt
python3 -I lectura_geometrica.py --raiz "$RAIZ" --autor "$C13" --todas /tmp/b6/todas.jsonl.gz --salida /tmp/b6/lectura.jsonl.gz --solo-grupo
python3 -I clases_6.py --todas /tmp/b6/todas.jsonl.gz --lectura /tmp/b6/lectura.jsonl.gz
python3 -I contraejemplos_6.py --raiz "$RAIZ" --version C11="$C11" --version C13="$C13"
python3 -I cobertura_6.py --raiz "$RAIZ" --autor "$C13" --libro "$LIBRO"
python3 -I consultas_6.py --raiz "$RAIZ" --todas /tmp/b6/todas.jsonl.gz --anterior C11="$C11" --nueva C13="$C13"
```

Los scripts que no llevan `--salida` escriben por la salida estándar; cada uno se guardó en el archivo de su nombre.

Salidas en `revision/resultados_revisor_6/`:

| Archivo | Contenido |
|---|---|
| `lectura_filas_c12.txt` | Las siete filas nuevas y las 18 entradas que contrastan, leídas con pdfminer y PDFium; identidades R41, R8, R24 y R42 con fracciones exactas; cota linealizada y exacta de R42; umbrales de detección; filas de segmento frente a R42 |
| `barrido_6.txt` | 122.604 candidatas de las 2.026 páginas: equivalencia con la ejecución oficial y transiciones de estado entre C11 y C13 por fila, por dimensión y por motivo |
| `clases_6.txt` | Las transiciones cruzadas con la lectura propia: ejercicio (A), edición (B), perímetro (C), candidatas que pasan a OK (D, D2), filas de subperímetro (E), cifras que pasan a fallar con los tres ejercicios (F) y las cuatro clases del encargo (G) |
| `contraejemplos_6.txt` | 48 casos sobre filas reales con el verificador oficial de C11 y de C13: F (R1), G (R2 y R3), H (R4) e I (controles de Q1–Q5 y R5) |
| `cobertura_6.txt` | Clase por pertenencia derivada de los coeficientes, umbral de detección de cada entrada, entradas que mueven la referencia y anclaje por tabla |
| `consultas_6.txt` | Motivos de las transiciones de OK a FALLO y de OK a PENDIENTE; columnas que cada versión reconoce en las cabeceras de R1 y R4; valor en libros de las tablas de vencimientos; sublíneas de EBITDA por segmento |

`arnes6.py` y `geom.py` son los módulos comunes. El barrido completo y la lectura (dos archivos comprimidos) no se guardan en el repositorio: se regeneran con los comandos de arriba. No se guardan aquí las salidas de los scripts de los revisores anteriores sobre este commit: son idénticas a las que el autor guarda en `resultados/*_sobre_C12.txt`.
